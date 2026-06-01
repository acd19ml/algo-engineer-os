"""Pydantic v2 schemas — single source of truth for the eval runner.

These models are the runnable counterpart of IMPLEMENTATION_DESIGN.md §2 / §5 / §6
and the eval-cases.yaml / eval-fixtures.yaml schema. DC-005 locks Pydantic v2 as the
single schema source; these classes ARE that source for the prototype.

Nothing here invents product facts. Models only describe the shape of:
  - eval cases / expectations (eval-cases.yaml)
  - fixture bodies (eval-fixtures.yaml)
  - the System-Under-Test (SUT) output that the runner compares against expectations
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


# --------------------------------------------------------------------------- #
# Enums (IMPLEMENTATION_DESIGN §2, §3)
# --------------------------------------------------------------------------- #
class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Decision(str, Enum):
    deny = "deny"
    handoff_or_clarify = "handoff-or-clarify"
    allow = "allow"


class AnswerMode(str, Enum):
    docs_answer = "docs_answer"
    registry_template = "registry_template"
    chain_diagnosis = "chain_diagnosis"
    boundary_template = "boundary_template"
    hard_interrupt = "hard_interrupt"
    refusal = "refusal"
    clarification = "clarification"
    handoff = "handoff"


class QueryPath(str, Enum):
    registry_exact = "registry_exact"
    chain = "chain"
    docs_direct = "docs_direct"
    docs_ambiguous = "docs_ambiguous"
    none = "none"


class ToolStatus(str, Enum):
    ok = "ok"
    resolution_error = "resolution_error"  # not_found / invalid: business semantics, enters evidence
    hard_error = "hard_error"  # rpc/adapter/parser/provider failure


class VerifierStatus(str, Enum):
    passed = "passed"
    blocked = "blocked"
    skipped_low_risk = "skipped_low_risk"
    fail_closed = "fail_closed"


# --------------------------------------------------------------------------- #
# Eval case / expectation (eval-cases.yaml)
# --------------------------------------------------------------------------- #
class Expected(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: Decision
    answer_mode: AnswerMode
    required_tools: list[str] = Field(default_factory=list)
    forbidden_tools: list[str] = Field(default_factory=list)
    required_evidence_types: list[str] = Field(default_factory=list)
    forbidden_claim_types: list[str] = Field(default_factory=list)
    must_include_source: bool = False
    must_not_persist_raw: bool = False


class CaseFixtures(BaseModel):
    model_config = ConfigDict(extra="forbid")

    registry_ids: list[str] = Field(default_factory=list)
    tool_fixture_ids: list[str] = Field(default_factory=list)
    docs_source_ids: list[str] = Field(default_factory=list)


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    suite: str
    user_message: str
    expected: Expected
    fixtures: CaseFixtures


# --------------------------------------------------------------------------- #
# Fixture bodies (eval-fixtures.yaml). Loose models: fixtures carry many
# optional, type-specific fields, so we keep extra=allow and read by key.
# --------------------------------------------------------------------------- #
class RegistryFixture(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    type: str
    # common optional fields used by the SUT / verifier
    verification_state: Optional[str] = None
    response_state: Optional[str] = None
    url: Optional[str] = None
    address: Optional[str] = None
    symbol: Optional[str] = None
    role: Optional[str] = None
    network: Optional[str] = None
    chain_family: Optional[str] = None
    supported: Optional[Any] = None
    handoff: Optional[str] = None


class DocsFixture(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    title: str
    url: Optional[str] = None
    claims: list[str] = Field(default_factory=list)
    malicious_text: Optional[str] = None


class ToolFixture(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    kind: str
    provides_tools: list[str] = Field(default_factory=list)
    envelope: dict[str, Any] = Field(default_factory=dict)
    # secret_detection fixtures use these instead of an envelope
    pattern_class: Optional[str] = None
    severity: Optional[str] = None
    must_not_persist_raw: Optional[bool] = None


# --------------------------------------------------------------------------- #
# Entities (IMPLEMENTATION_DESIGN §2)
# --------------------------------------------------------------------------- #
class Entities(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tx_hashes: list[str] = Field(default_factory=list)
    addresses: list[str] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)
    networks: list[str] = Field(default_factory=list)
    token_symbols: list[str] = Field(default_factory=list)
    # malformed entities that LOOK like a hash/address but fail format validation
    malformed_tx_like: list[str] = Field(default_factory=list)
    network_ambiguous: bool = False
    possible_secrets_redacted: bool = False


# --------------------------------------------------------------------------- #
# SUT output — what the deterministic pipeline produces per case.
# The runner compares these fields against Expected.
# --------------------------------------------------------------------------- #
class SUTResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    intent: str
    intent_source: str  # "mocked_from_suite" | "llm_router" | "rule_router"
    risk: RiskLevel

    decision: Decision
    answer_mode: AnswerMode
    query_path: QueryPath

    tools_called: list[str] = Field(default_factory=list)
    evidence_types: list[str] = Field(default_factory=list)
    claim_types: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)

    has_source: bool = False
    persisted_raw: bool = False  # did raw user_message reach log/llm/tool/retriever?
    handoff_required: bool = False
    verifier_status: VerifierStatus = VerifierStatus.skipped_low_risk

    # bookkeeping for metrics / debugging
    tool_error_kind: Optional[str] = None  # resolution_error | hard_error | None
    deny_reason: Optional[str] = None
    notes: list[str] = Field(default_factory=list)
