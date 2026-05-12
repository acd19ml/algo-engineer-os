#!/usr/bin/env python3
"""Transcribe audio files under TOOL/audios with Qiniu QNAIGC ASR."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

try:
    from dotenv import load_dotenv as load_dotenv_file
except ImportError:
    load_dotenv_file = None


SCRIPT_DIR = Path(__file__).resolve().parent
TOOL_DIR = SCRIPT_DIR.parent
REPO_ROOT = TOOL_DIR.parent
DEFAULT_INPUT_DIR = TOOL_DIR / "audios"
DEFAULT_OUTPUT_DIR = TOOL_DIR / "transcripts"
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
class Settings:
    api_key: str
    asr_url: str
    model: str
    audio_base_url: str | None
    qiniu_access_key: str | None
    qiniu_secret_key: str | None
    qiniu_bucket: str | None
    qiniu_domain: str | None
    qiniu_key_prefix: str
    qiniu_private_bucket: bool
    qiniu_upload_token_expires: int


def truthy(value: str | None) -> bool:
    return value is not None and value.strip().lower() in {"1", "true", "yes", "y", "on"}


def first_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value.strip()
    return None


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


def read_settings() -> Settings:
    api_key = first_env("QNAIGC_API_KEY", "QINIU_ASR_API_KEY", "API_KEY")
    if not api_key or api_key == "<API_KEY>":
        raise RuntimeError("Missing API key. Set QNAIGC_API_KEY in .env.")

    expires_raw = os.getenv("QINIU_UPLOAD_TOKEN_EXPIRES", "3600").strip()
    try:
        upload_token_expires = int(expires_raw)
    except ValueError as exc:
        raise RuntimeError("QINIU_UPLOAD_TOKEN_EXPIRES must be an integer number of seconds.") from exc

    return Settings(
        api_key=api_key,
        asr_url=os.getenv("QNAIGC_ASR_URL", "https://api.qnaigc.com/v1/voice/asr").strip(),
        model=os.getenv("QNAIGC_ASR_MODEL", "asr").strip(),
        audio_base_url=first_env("QNAIGC_AUDIO_BASE_URL", "AUDIO_BASE_URL"),
        qiniu_access_key=first_env("QINIU_ACCESS_KEY", "QINIU_AK"),
        qiniu_secret_key=first_env("QINIU_SECRET_KEY", "QINIU_SK"),
        qiniu_bucket=first_env("QINIU_BUCKET"),
        qiniu_domain=first_env("QINIU_DOMAIN", "QINIU_BUCKET_DOMAIN"),
        qiniu_key_prefix=os.getenv("QINIU_KEY_PREFIX", "asr-audios").strip().strip("/"),
        qiniu_private_bucket=truthy(os.getenv("QINIU_PRIVATE_BUCKET")),
        qiniu_upload_token_expires=upload_token_expires,
    )


def find_audio_files(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    files = [
        path
        for path in sorted(input_dir.iterdir())
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    if not files:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise FileNotFoundError(f"No audio files found in {input_dir}. Supported formats: {supported}")
    return files


def public_url_from_base(base_url: str, audio_path: Path) -> str:
    return f"{base_url.rstrip('/')}/{quote(audio_path.name)}"


def qiniu_public_url(domain: str, key: str) -> str:
    domain = domain.strip()
    if not domain.startswith(("http://", "https://")):
        domain = f"http://{domain}"
    return f"{domain.rstrip('/')}/{quote(key)}"


def upload_to_qiniu(audio_path: Path, settings: Settings) -> str:
    missing = [
        name
        for name, value in {
            "QINIU_ACCESS_KEY": settings.qiniu_access_key,
            "QINIU_SECRET_KEY": settings.qiniu_secret_key,
            "QINIU_BUCKET": settings.qiniu_bucket,
            "QINIU_DOMAIN": settings.qiniu_domain,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(
            "ASR requires an audio URL. Set QNAIGC_AUDIO_BASE_URL, or configure Kodo upload env vars: "
            + ", ".join(missing)
        )

    try:
        from qiniu import Auth, put_file
    except ImportError as exc:
        raise RuntimeError("Missing qiniu package. Install dependencies with: pip install -r TOOL/script/requirements.txt") from exc

    key = f"{settings.qiniu_key_prefix}/{audio_path.name}" if settings.qiniu_key_prefix else audio_path.name
    auth = Auth(settings.qiniu_access_key, settings.qiniu_secret_key)
    token = auth.upload_token(settings.qiniu_bucket, key, settings.qiniu_upload_token_expires)
    ret, info = put_file(token, key, str(audio_path))
    status_code = getattr(info, "status_code", None)
    if status_code != 200:
        raise RuntimeError(f"Qiniu upload failed for {audio_path.name}: status={status_code}, info={info}, ret={ret}")

    audio_url = qiniu_public_url(settings.qiniu_domain or "", key)
    if settings.qiniu_private_bucket:
        audio_url = auth.private_download_url(audio_url, expires=settings.qiniu_upload_token_expires)
    return audio_url


def resolve_audio_url(audio_path: Path, settings: Settings, upload: bool) -> str:
    if settings.audio_base_url:
        return public_url_from_base(settings.audio_base_url, audio_path)
    if upload:
        return upload_to_qiniu(audio_path, settings)
    raise RuntimeError(
        "No public audio URL source configured. Set QNAIGC_AUDIO_BASE_URL or pass --upload with Qiniu Kodo env vars."
    )


def call_asr(audio_url: str, audio_format: str, settings: Settings, timeout: int) -> dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.api_key}",
    }
    payload = {
        "model": settings.model,
        "audio": {
            "format": audio_format.lstrip(".").lower(),
            "url": audio_url,
        },
    }
    response = requests.post(settings.asr_url, headers=headers, json=payload, timeout=timeout)
    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError(f"ASR returned non-JSON response: HTTP {response.status_code} {response.text[:500]}") from exc
    if response.status_code >= 400:
        raise RuntimeError(f"ASR request failed: HTTP {response.status_code} {json.dumps(body, ensure_ascii=False)}")
    return body


def extract_text(value: Any) -> str | None:
    if isinstance(value, dict):
        for key in ("text", "transcript", "result", "content"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
        for key in ("data", "result", "results", "output"):
            candidate = extract_text(value.get(key))
            if candidate:
                return candidate
        for candidate_value in value.values():
            candidate = extract_text(candidate_value)
            if candidate:
                return candidate
    elif isinstance(value, list):
        parts = [candidate for item in value if (candidate := extract_text(item))]
        if parts:
            return "\n".join(parts)
    return None


def write_outputs(output_dir: Path, audio_path: Path, response_body: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = audio_path.stem
    json_path = output_dir / f"{stem}.json"
    txt_path = output_dir / f"{stem}.txt"

    json_path.write_text(json.dumps(response_body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    text = extract_text(response_body)
    txt_path.write_text((text or json.dumps(response_body, ensure_ascii=False, indent=2)) + "\n", encoding="utf-8")
    return txt_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Transcribe audio files from TOOL/audios with Qiniu QNAIGC ASR.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR, help="Directory containing audio files.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for .txt and raw .json outputs.")
    parser.add_argument("--env", type=Path, default=None, help="Path to .env file.")
    parser.add_argument("--upload", action="store_true", help="Upload local files to Qiniu Kodo when QNAIGC_AUDIO_BASE_URL is not set.")
    parser.add_argument("--timeout", type=int, default=120, help="HTTP timeout in seconds for each ASR request.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of files to process.")
    parser.add_argument("--force", action="store_true", help="Re-run files even when output .txt already exists.")
    parser.add_argument("--dry-run", action="store_true", help="Validate config and print planned files without calling ASR.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    env_path = load_env_file(args.env)

    try:
        settings = read_settings()
        audio_files = find_audio_files(args.input_dir.resolve())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.limit is not None:
        audio_files = audio_files[: args.limit]

    print(f"Loaded env: {env_path or 'system environment'}")
    print(f"Input dir: {args.input_dir.resolve()}")
    print(f"Output dir: {args.output_dir.resolve()}")
    print(f"Files: {len(audio_files)}")

    for audio_path in audio_files:
        txt_path = args.output_dir / f"{audio_path.stem}.txt"
        if txt_path.exists() and not args.force:
            print(f"SKIP {audio_path.name}: {txt_path} already exists. Use --force to re-run.")
            continue

        try:
            audio_url = resolve_audio_url(audio_path, settings, upload=args.upload)
            if args.dry_run:
                print(f"DRY-RUN {audio_path.name}: format={audio_path.suffix.lstrip('.').lower()} url={audio_url}")
                continue

            print(f"ASR {audio_path.name}")
            response_body = call_asr(audio_url, audio_path.suffix, settings, timeout=args.timeout)
            written_txt = write_outputs(args.output_dir, audio_path, response_body)
            text = extract_text(response_body)
            if text:
                print(f"WROTE {written_txt}")
                print(text)
            else:
                print(f"WROTE {written_txt}; no obvious text field found, raw JSON copied to txt.")
        except Exception as exc:
            print(f"ERROR {audio_path.name}: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
