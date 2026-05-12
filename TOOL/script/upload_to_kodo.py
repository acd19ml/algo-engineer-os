#!/usr/bin/env python3
"""Upload local files under TOOL/audios to Qiniu Kodo."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

try:
    from dotenv import load_dotenv as load_dotenv_file
except ImportError:
    load_dotenv_file = None


SCRIPT_DIR = Path(__file__).resolve().parent
TOOL_DIR = SCRIPT_DIR.parent
REPO_ROOT = TOOL_DIR.parent
DEFAULT_INPUT_DIR = TOOL_DIR / "audios"
DEFAULT_MANIFEST = TOOL_DIR / "kodo_uploads.json"
SUPPORTED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
    ".opus",
    ".amr",
    ".webm",
}


@dataclass(frozen=True)
class KodoSettings:
    access_key: str
    secret_key: str
    bucket: str
    domain: str
    key_prefix: str
    private_bucket: bool
    token_expires: int


def truthy(value: str | None) -> bool:
    return value is not None and value.strip().lower() in {"1", "true", "yes", "y", "on"}


def first_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value.strip()
    return None


def load_simple_env(env_path: Path) -> None:
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def load_env_file(explicit_env: Path | None) -> Path | None:
    candidates = [explicit_env] if explicit_env else [Path.cwd() / ".env", SCRIPT_DIR / ".env", REPO_ROOT / ".env"]
    for candidate in candidates:
        if candidate and candidate.exists():
            if load_dotenv_file:
                load_dotenv_file(candidate)
            else:
                load_simple_env(candidate)
            return candidate
    if load_dotenv_file:
        load_dotenv_file()
    return None


def read_settings() -> KodoSettings:
    expires_raw = os.getenv("QINIU_UPLOAD_TOKEN_EXPIRES", "3600").strip()
    try:
        token_expires = int(expires_raw)
    except ValueError as exc:
        raise RuntimeError("QINIU_UPLOAD_TOKEN_EXPIRES must be an integer number of seconds.") from exc

    values = {
        "QINIU_ACCESS_KEY": first_env("QINIU_ACCESS_KEY", "QINIU_AK"),
        "QINIU_SECRET_KEY": first_env("QINIU_SECRET_KEY", "QINIU_SK"),
        "QINIU_BUCKET": first_env("QINIU_BUCKET"),
        "QINIU_DOMAIN": first_env("QINIU_DOMAIN", "QINIU_BUCKET_DOMAIN"),
    }
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise RuntimeError("Missing Kodo env vars: " + ", ".join(missing))

    return KodoSettings(
        access_key=values["QINIU_ACCESS_KEY"] or "",
        secret_key=values["QINIU_SECRET_KEY"] or "",
        bucket=values["QINIU_BUCKET"] or "",
        domain=values["QINIU_DOMAIN"] or "",
        key_prefix=os.getenv("QINIU_KEY_PREFIX", "asr-audios").strip().strip("/"),
        private_bucket=truthy(os.getenv("QINIU_PRIVATE_BUCKET")),
        token_expires=token_expires,
    )


def list_input_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    files = [
        path
        for path in sorted(input_path.iterdir())
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    if not files:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise FileNotFoundError(f"No supported files found in {input_path}. Supported formats: {supported}")
    return files


def object_key(path: Path, settings: KodoSettings, preserve_name: bool) -> str:
    file_name = path.name if preserve_name else f"{path.stem}{path.suffix.lower()}"
    return f"{settings.key_prefix}/{file_name}" if settings.key_prefix else file_name


def public_url(domain: str, key: str) -> str:
    domain = domain.strip()
    if not domain.startswith(("http://", "https://")):
        domain = f"http://{domain}"
    return f"{domain.rstrip('/')}/{quote(key)}"


def upload_file(path: Path, settings: KodoSettings, key: str, overwrite: bool) -> dict[str, Any]:
    try:
        from qiniu import Auth, put_file
    except ImportError as exc:
        raise RuntimeError("Missing qiniu package. Install dependencies with: pip install -r TOOL/script/requirements.txt") from exc

    auth = Auth(settings.access_key, settings.secret_key)
    token = auth.upload_token(settings.bucket, key, settings.token_expires) if overwrite else auth.upload_token(settings.bucket, key, settings.token_expires, policy={"insertOnly": 1})
    ret, info = put_file(token, key, str(path))
    status_code = getattr(info, "status_code", None)
    if status_code not in {200, 614}:
        raise RuntimeError(f"Kodo upload failed for {path.name}: status={status_code}, info={info}, ret={ret}")
    url = public_url(settings.domain, key)
    if settings.private_bucket:
        url = auth.private_download_url(url, expires=settings.token_expires)
    return {
        "local_path": str(path),
        "bucket": settings.bucket,
        "key": key,
        "url": url,
        "hash": ret.get("hash") if isinstance(ret, dict) else None,
        "status_code": status_code,
        "uploaded": status_code == 200,
    }


def write_manifest(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Upload files from TOOL/audios to Qiniu Kodo.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_DIR, help="Audio file or directory to upload.")
    parser.add_argument("--env", type=Path, default=None, help="Path to .env file.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="Where to write upload result JSON.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of files to upload.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing Kodo objects with the same key.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned object keys without uploading.")
    parser.add_argument("--normalize-name", action="store_true", help="Lowercase only the file extension in the Kodo key.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    env_path = load_env_file(args.env)

    try:
        settings = read_settings()
        files = list_input_files(args.input.resolve())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.limit is not None:
        files = files[: args.limit]

    print(f"Loaded env: {env_path or 'system environment'}")
    print(f"Input: {args.input.resolve()}")
    print(f"Bucket: {settings.bucket}")
    print(f"Domain: {settings.domain}")
    print(f"Files: {len(files)}")

    rows: list[dict[str, Any]] = []
    for path in files:
        key = object_key(path, settings, preserve_name=not args.normalize_name)
        if args.dry_run:
            url = public_url(settings.domain, key)
            print(f"DRY-RUN {path.name} -> {key} -> {url}")
            rows.append({"local_path": str(path), "bucket": settings.bucket, "key": key, "url": url, "uploaded": False})
            continue

        try:
            row = upload_file(path, settings, key, overwrite=args.overwrite)
        except Exception as exc:
            print(f"ERROR {path.name}: {exc}", file=sys.stderr)
            return 1
        rows.append(row)
        action = "UPLOADED" if row["uploaded"] else "EXISTS"
        print(f"{action} {path.name} -> {row['url']}")

    if args.dry_run:
        print("Manifest not written in dry-run mode.")
    else:
        write_manifest(args.manifest.resolve(), rows)
        print(f"Manifest: {args.manifest.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
