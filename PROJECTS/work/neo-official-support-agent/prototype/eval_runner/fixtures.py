"""Fixture provider — implements the contract in eval-runner-spec.md §3.

Loads eval-fixtures.yaml and serves registry / docs / tool / secret fixtures to the
SUT. Tool fixtures may contain placeholders like ``{{case.tx_hash}}`` / ``{{case.address}}``;
the provider substitutes the entities extracted from the case before returning, so a single
success fixture is reused across cases instead of being copied per case (spec §3).

This is a TEST provider over repo-local YAML. It is NOT a production registry and must not
be treated as confirmed Neo official data (eval-fixtures.yaml header).
"""

from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any, Optional

import yaml

from .models import DocsFixture, RegistryFixture, ToolFixture

_PLACEHOLDER_RE = re.compile(r"\{\{\s*case\.([a-zA-Z_]+)\s*\}\}")


def _project_root() -> Path:
    # eval_runner/ -> prototype/ -> <project root>
    return Path(__file__).resolve().parents[2]


def _substitute(value: Any, ctx: dict[str, str]) -> Any:
    """Recursively replace {{case.<field>}} placeholders inside a fixture body."""
    if isinstance(value, str):
        def repl(m: re.Match) -> str:
            return ctx.get(m.group(1), m.group(0))

        return _PLACEHOLDER_RE.sub(repl, value)
    if isinstance(value, list):
        return [_substitute(v, ctx) for v in value]
    if isinstance(value, dict):
        return {k: _substitute(v, ctx) for k, v in value.items()}
    return value


class FixtureProvider:
    def __init__(self, fixtures_path: Optional[Path] = None) -> None:
        self.path = fixtures_path or (_project_root() / "eval" / "eval-fixtures.yaml")
        raw = yaml.safe_load(self.path.read_text(encoding="utf-8"))

        self.registry: dict[str, RegistryFixture] = {
            f["id"]: RegistryFixture(**f) for f in raw.get("registry_fixtures", [])
        }
        self.docs: dict[str, DocsFixture] = {
            f["id"]: DocsFixture(**f) for f in raw.get("docs_fixtures", [])
        }
        self.tools: dict[str, ToolFixture] = {
            f["id"]: ToolFixture(**f) for f in raw.get("tool_fixtures", [])
        }

    # ---- spec §3 contract --------------------------------------------------- #
    def get_registry_records(self, ids: list[str]) -> list[RegistryFixture]:
        return [self.registry[i] for i in ids if i in self.registry]

    def get_docs_sources(self, ids: list[str]) -> list[DocsFixture]:
        return [self.docs[i] for i in ids if i in self.docs]

    def get_tool_results(self, ids: list[str], case_ctx: dict[str, str]) -> list[dict[str, Any]]:
        """Return resolved tool envelopes with placeholders substituted.

        Each item: {id, kind, provides_tools, envelope}. secret_detection fixtures
        have no envelope and are routed via get_secret_detection_fixture instead.
        """
        results: list[dict[str, Any]] = []
        for i in ids:
            tf = self.tools.get(i)
            if tf is None or tf.kind == "secret_detection":
                continue
            envelope = _substitute(copy.deepcopy(tf.envelope), case_ctx)
            results.append(
                {
                    "id": tf.id,
                    "kind": tf.kind,
                    "provides_tools": list(tf.provides_tools),
                    "envelope": envelope,
                }
            )
        return results

    def get_secret_detection_fixture(self, ids: list[str]) -> Optional[ToolFixture]:
        for i in ids:
            tf = self.tools.get(i)
            if tf is not None and tf.kind == "secret_detection":
                return tf
        return None

    # ---- helpers for coverage + lookups ------------------------------------ #
    def all_ids(self) -> set[str]:
        return set(self.registry) | set(self.docs) | set(self.tools)

    def missing_ids(self, ids: list[str]) -> list[str]:
        known = self.all_ids()
        return [i for i in ids if i not in known]
