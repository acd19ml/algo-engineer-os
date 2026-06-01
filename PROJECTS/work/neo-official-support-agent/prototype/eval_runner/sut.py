"""System Under Test: the deterministic policy-constrained support orchestrator.

This is the runnable counterpart of IMPLEMENTATION_DESIGN.md §1 (runtime pipeline). Only
semantic intent classification is delegated to a (mocked or LLM) router; everything that
makes the system *safe* is deterministic here and overrides the router:

  ingress secret guard  (§8, DC-002)   -> hard_interrupt before any log/LLM/tool
  deny-layer rule router (§3.1, DC-002) -> investment / write-chain / wallet-connect refusal
  policy gate / Allow Matrix (§3.2/3.4) -> deny > handoff-or-clarify > allow (DC-003)
  query-path classifier (§3.5, DC-009)  -> registry/chain entities never get rewritten
  tool routing + evidence (§5/§6)        -> read-only tools, typed evidence bundle
  error classification (§5, DC-008)      -> resolution_error vs hard_error
  typed-claim compiler + verifier (§6/§7, DC-004) -> hard facts only via verified slots

The deny layer runs BEFORE the semantic router, so secret / investment / write-chain /
wallet-connect messages never reach the LLM (forbidden tool ``llm_router``).
"""

from __future__ import annotations

import re
from typing import Optional

from .fixtures import FixtureProvider
from .models import (
    AnswerMode,
    Decision,
    Entities,
    QueryPath,
    RiskLevel,
    SUTResult,
    VerifierStatus,
)
from .router import RouterOutput

# Tool family expansion for forbidden-tool checks (cases use family names like "n3_adapter").
TOOL_FAMILIES = {
    "n3_adapter": {"n3_get_raw_transaction", "n3_get_application_log", "n3_get_nep17_balances"},
    "evm_adapter": {"evm_get_transaction_by_hash", "evm_get_transaction_receipt", "evm_call_simulate"},
}

# --------------------------------------------------------------------------- #
# Entity extraction (§2)
# --------------------------------------------------------------------------- #
_RE_EVM_TX = re.compile(r"0[xX][0-9a-fA-F]{64}(?![0-9a-fA-F])")
_RE_EVM_ADDR = re.compile(r"0[xX][0-9a-fA-F]{40}(?![0-9a-fA-F])")
_RE_N3_ADDR = re.compile(r"\bA[1-9A-HJ-NP-Za-km-z]{33}\b")
# scheme + bare-domain extraction is case-insensitive (lookalikes love HTTPS://Neo.Org)
_RE_URL = re.compile(r"https?://[^\s，。]+", re.I)
_RE_DOMAIN = re.compile(r"\b[a-z0-9][a-z0-9.\-]*\.(?:example|org|com|network|io)\b(?:/[^\s，。]*)?", re.I)
# unicode-confusable domains: a non-ASCII letter (e.g. Cyrillic 'е') embedded among ASCII
# domain chars before a known TLD — classic lookalike phishing (nеo.org).
_RE_CONFUSABLE = re.compile(r"[A-Za-z0-9.\-]*[^\x00-\x7f\s][A-Za-z0-9.\-]*\.(?:example|org|com|network|io)\b", re.I)
# a "0x...." that is NOT a 64-hex tx and NOT a 40-hex address -> malformed tx-like
_RE_HEXISH = re.compile(r"0x[0-9a-fA-F]+")


def extract_entities(message: str) -> Entities:
    txs = _RE_EVM_TX.findall(message)
    addrs = _RE_EVM_ADDR.findall(message) + _RE_N3_ADDR.findall(message)
    urls = list(_RE_URL.findall(message))
    for d in list(_RE_DOMAIN.findall(message)) + list(_RE_CONFUSABLE.findall(message)):
        if not any(d in u for u in urls):  # avoid double-count of scheme'd urls
            urls.append(d)
    # drop partial matches that are substrings of a fuller url (e.g. 'o.org' inside 'nеo.org')
    urls = [u for u in urls if not any(u != v and u in v for v in urls)]

    # malformed tx-like: user calls it a tx but it doesn't match a valid hash format
    malformed: list[str] = []
    talks_tx = any(k in message.lower() for k in ("tx", "交易", "transaction"))
    for h in _RE_HEXISH.findall(message):
        if len(h) not in (66, 42):  # not 0x+64 (tx) and not 0x+40 (addr)
            malformed.append(h)
    if talks_tx and not txs and not malformed:
        # e.g. "tx abc123" — a non-hex token used as a tx id
        m = re.search(r"(?:tx|交易)\s*([0-9a-zA-Z]{3,20})", message)
        if m and not m.group(1).startswith("0x"):
            malformed.append(m.group(1))

    n3 = bool(re.search(r"neo\s*n3|n3\b|neo legacy", message, re.I))
    nx = bool(re.search(r"neo\s*x|neox|\bevm\b", message, re.I))
    networks: list[str] = []
    if n3:
        networks.append("neo_n3_mainnet")
    if nx:
        networks.append("neo_x_mainnet")

    ambiguous = bool(
        re.search(r"还是\s*neo\s*x|n3\s*还是|不确定|不知道是|don'?t know", message, re.I)
    ) or (n3 and nx and ("还是" in message or "不确定" in message))

    tokens = []
    if re.search(r"\bNEO\b", message):
        tokens.append("NEO")
    if re.search(r"\bGAS\b", message, re.I):
        tokens.append("GAS")

    return Entities(
        tx_hashes=txs,
        addresses=addrs,
        urls=urls,
        networks=networks,
        token_symbols=tokens,
        malformed_tx_like=malformed,
        network_ambiguous=ambiguous,
    )


# --------------------------------------------------------------------------- #
# Ingress secret guard (§8). Real secrets are never stored in fixtures; the secret
# material is represented by a `<..._FIXTURE>` placeholder, and the guard fires on it
# exactly as a production guard would fire on a real BIP39/WIF/private-key match.
# --------------------------------------------------------------------------- #
_RE_SECRET_PLACEHOLDER = re.compile(r"<[A-Z0-9_]*_FIXTURE>")


def detect_secret(message: str) -> bool:
    return bool(_RE_SECRET_PLACEHOLDER.search(message))


# --------------------------------------------------------------------------- #
# Deny-layer rule router (§3.1). Multilingual, action/decision oriented.
# --------------------------------------------------------------------------- #
_INVEST_KW = [
    "该不该买", "该不该卖", "应该买", "应该卖", "买一点", "能不能买", "买 neo", "买neo",
    "价格预测", "会涨", "会跌", "涨吗", "哪个收益", "收益更高", "配置仓位", "仓位",
    "should i buy", "should i sell", " buy ", " sell ", "price prediction", "portfolio", "allocate",
    "買うべき", "上がり",
]
# explanation requests must NOT be read as investment intent (e.g. "官方怎么描述 GAS 的用途")
_EXPLAIN_GUARD = ["官方怎么", "官方如何", "怎么描述", "解释", "用途", "角色", "区别", "定位"]

_WRITE_VERB = ["签名", "sign", "approve", "授权", "转账", "转到", "transfer", "把我", "转 "]
_WRITE_IMPERATIVE = ["帮我", "你来", "你直接", "可以你", "代操作", "替我", "你能", "please "]
_WALLET_CONNECT = ["连接我的钱包", "连接钱包", "connect my wallet", "connect wallet", "连接 钱包"]


def _is_investment(message: str) -> bool:
    low = " " + message.lower() + " "
    hit = any(kw in low or kw in message for kw in _INVEST_KW)
    if not hit:
        return False
    has_buy_sell = any(k in message for k in ("买", "卖")) or " buy " in low or " sell " in low or "買" in message
    if not has_buy_sell and any(g in message for g in _EXPLAIN_GUARD):
        # yield/price word inside a pure explanation request -> not investment
        return False
    return True


def _is_wallet_connect(message: str) -> bool:
    low = message.lower()
    if "连接我的钱包" in message or "connect my wallet" in low:
        return True
    mentions = any(k in message or k in low for k in ("连接钱包", "connect wallet", "连接 钱包"))
    if not mentions:
        return False
    # only a request *to the bot* to connect counts; a phishing-domain officialness question
    # that merely mentions "连接钱包" is an address/link check, not a wallet-connect request.
    bot_directed = any(t in message or t in low for t in ("你能", "你来", "你直接", "帮我", "能不能", "可以你", "can you"))
    officialness_q = any(g in message for g in ("官方域名", "是官方", "官方吗", "域名吗", "是不是官方"))
    return bot_directed and not officialness_q


def _is_write_chain(message: str, has_tx: bool) -> bool:
    # diagnosing a past tx (tx hash present) is NOT a write request
    if has_tx:
        return False
    low = message.lower()
    verb = any(v in message or v in low for v in _WRITE_VERB)
    imper = any(i in message or i in low for i in _WRITE_IMPERATIVE)
    return verb and imper


# Router-independent invariants (§3.1 family): behaviors that must hold no matter how the
# LLM classifies intent. The LLM router sweep showed these used to live *inside* intent
# handlers, so a router mistake silently suppressed them.
_HANDOFF_REQUEST = [
    "转人工", "转真人", "人工客服", "真人客服", "转接人工", "转接客服", "找人工", "要人工",
    "speak to a human", "talk to a human", "talk to an agent", "human agent", "live agent",
]


def _wants_human_handoff(message: str) -> bool:
    low = message.lower()
    return any(k in message or k in low for k in _HANDOFF_REQUEST)


def _chain_query_unsafe(e: Entities, message: str) -> bool:
    """We cannot run a chain lookup without a usable (valid tx_hash, decided network) pair.
    Detect it from the message + entities, independent of the router's intent guess."""
    talks_tx = any(k in message.lower() for k in ("tx", "交易", "transaction"))
    if e.network_ambiguous and (e.tx_hashes or e.malformed_tx_like):
        return True  # user explicitly unsure which chain, but gave a tx -> must clarify
    if e.malformed_tx_like and not e.tx_hashes and talks_tx:
        return True  # a "tx id" that isn't a valid hash -> must clarify
    return False


# --------------------------------------------------------------------------- #
# Allow Matrix (§3.2): intent -> (answer_mode, base tools, evidence types)
# --------------------------------------------------------------------------- #
_BASE_ANSWER_MODE = {
    "neo_basic_explain": AnswerMode.docs_answer,
    "token_explain": AnswerMode.registry_template,
    "official_navigation": AnswerMode.registry_template,
    "address_or_contract_check": AnswerMode.registry_template,
    "neo_n3_chain_state": AnswerMode.chain_diagnosis,
    "neo_x_chain_state": AnswerMode.chain_diagnosis,
    "tx_failure_diagnosis": AnswerMode.chain_diagnosis,
    "exchange_boundary": AnswerMode.boundary_template,
    "wallet_boundary": AnswerMode.boundary_template,
    "unsupported": AnswerMode.clarification,
}


class SupportOrchestratorSUT:
    def __init__(self, provider: Optional[FixtureProvider] = None) -> None:
        self.provider = provider or FixtureProvider()

    # main entry -------------------------------------------------------------- #
    def run(self, case) -> SUTResult:  # case: models.Case
        msg = case.user_message
        entities = extract_entities(msg)
        fx = case.fixtures

        # 1) Ingress secret guard — before any log / router / tool (DC-002, §8)
        if detect_secret(msg):
            return SUTResult(
                case_id=case.id,
                intent="secret",
                intent_source="rule_router",
                risk=RiskLevel.critical,
                decision=Decision.deny,
                answer_mode=AnswerMode.hard_interrupt,
                query_path=QueryPath.none,
                tools_called=[],
                evidence_types=[],
                claim_types=["safety_interrupt"],
                source_ids=[],
                has_source=False,
                persisted_raw=False,  # scrubbed pre-log; never reaches LLM/tool/retriever
                handoff_required=False,
                verifier_status=VerifierStatus.skipped_low_risk,
                deny_reason="secret_material_detected",
            )

        # 2) Deny-layer rule router — overrides everything; never calls the LLM (DC-002)
        if _is_investment(msg):
            return self._refusal(case, "investment_advice")
        if _is_wallet_connect(msg) or _is_write_chain(msg, has_tx=bool(entities.tx_hashes)):
            return self._refusal(case, "write_or_wallet_connect")

        # 2.5) Router-independent invariants — run BEFORE the semantic router so a router
        # misclassification cannot suppress them (surfaced by the LLM sweep:
        # exchange_wallet_boundary_008 handoff-request, neo_n3_tx_status_006 chain ambiguity).
        if _wants_human_handoff(msg):
            return self._explicit_handoff(case)
        if _chain_query_unsafe(entities, msg):
            return self._clarify(case, "chain_query_unsafe")

        # 3) Semantic router (mocked oracle OR real LLM) — only now may the LLM run
        ro: RouterOutput = self.router.classify(case.id, case.suite, msg)
        intent, risk, src = ro.intent, ro.risk, ro.source
        tools_called: list[str] = []
        if src == "llm_router":
            tools_called.append("llm_router")  # the LLM was actually invoked

        # 4) Query path (§3.5, DC-009) — entity-bearing requests can never be rewritten
        query_path = self._classify_query_path(intent, entities)

        # 5) Dispatch by intent through the Allow Matrix + entity/fixture signals
        if intent in ("neo_n3_chain_state", "neo_x_chain_state", "tx_failure_diagnosis"):
            return self._handle_chain(case, intent, risk, src, entities, query_path, tools_called)
        if intent in ("exchange_boundary", "wallet_boundary"):
            return self._handle_boundary(case, intent, risk, src, entities, query_path, tools_called)
        return self._handle_static(case, intent, risk, src, entities, query_path, tools_called)

    # -- router is injected by the runner ------------------------------------ #
    router = None  # set by EvalRunner

    # ---- refusal (deny layer) ---------------------------------------------- #
    def _refusal(self, case, reason: str) -> SUTResult:
        return SUTResult(
            case_id=case.id,
            intent=reason,
            intent_source="rule_router",
            risk=RiskLevel.high,
            decision=Decision.deny,
            answer_mode=AnswerMode.refusal,
            query_path=QueryPath.none,
            tools_called=[],
            evidence_types=[],
            claim_types=["refusal"],
            source_ids=[],
            has_source=False,
            persisted_raw=False,
            handoff_required=False,
            verifier_status=VerifierStatus.skipped_low_risk,
            deny_reason=reason,
        )

    # ---- router-independent invariants (run before the semantic router) ----- #
    def _clarify(self, case, reason: str) -> SUTResult:
        return SUTResult(
            case_id=case.id, intent="clarify", intent_source="rule_router", risk=RiskLevel.high,
            decision=Decision.handoff_or_clarify, answer_mode=AnswerMode.clarification,
            query_path=QueryPath.none, tools_called=[], evidence_types=[],
            claim_types=["clarification_request"], source_ids=[], has_source=False,
            persisted_raw=False, handoff_required=False,
            verifier_status=VerifierStatus.skipped_low_risk, deny_reason=reason,
        )

    def _explicit_handoff(self, case) -> SUTResult:
        regs = self.provider.get_registry_records(case.fixtures.registry_ids)
        return SUTResult(
            case_id=case.id, intent="handoff_request", intent_source="rule_router", risk=RiskLevel.high,
            decision=Decision.handoff_or_clarify, answer_mode=AnswerMode.handoff,
            query_path=QueryPath.none, tools_called=["support_boundary_lookup"],
            evidence_types=["registry"] if regs else [], claim_types=["handoff_summary"],
            source_ids=[r.id for r in regs], has_source=bool(regs),
            persisted_raw=False, handoff_required=True,
            verifier_status=VerifierStatus.skipped_low_risk, deny_reason="explicit_handoff_request",
        )

    # ---- query path (DC-009) ----------------------------------------------- #
    def _classify_query_path(self, intent: str, e: Entities) -> QueryPath:
        if e.addresses or e.urls:
            return QueryPath.registry_exact
        if e.tx_hashes and intent in ("neo_n3_chain_state", "neo_x_chain_state", "tx_failure_diagnosis"):
            return QueryPath.chain
        if intent in ("official_navigation", "address_or_contract_check", "token_explain"):
            return QueryPath.registry_exact
        if intent == "neo_basic_explain":
            return QueryPath.docs_direct
        return QueryPath.none

    # ---- static intents: docs / token / navigation / address check --------- #
    def _handle_static(self, case, intent, risk, src, e, query_path, tools_called) -> SUTResult:
        fx = case.fixtures
        evidence_types: list[str] = []
        source_ids: list[str] = []
        claim_types: list[str] = []
        answer_mode = _BASE_ANSWER_MODE[intent]

        if intent == "neo_basic_explain":
            tools_called.append("docs_retriever")
            docs = self.provider.get_docs_sources(fx.docs_source_ids)
            evidence_types.append("docs")
            source_ids += [d.id for d in docs]
            claim_types.append("docs_explanation")

        elif intent == "token_explain":
            tools_called += ["token_registry_lookup", "docs_retriever"]
            regs = self.provider.get_registry_records(fx.registry_ids)
            docs = self.provider.get_docs_sources(fx.docs_source_ids)
            evidence_types += ["registry", "docs"]
            source_ids += [r.id for r in regs] + [d.id for d in docs]
            claim_types.append("token_role")

        elif intent == "official_navigation":
            tools_called.append("official_link_registry_lookup")
            low = case.user_message.lower()
            if any(k in case.user_message for k in ("explorer", "status", "故障")):
                tools_called.append("network_registry_lookup")
            if any(k in case.user_message for k in ("钱包", "wallet")):
                tools_called.append("wallet_registry_lookup")
            regs = self.provider.get_registry_records(fx.registry_ids)
            evidence_types.append("registry")
            source_ids += [r.id for r in regs]
            claim_types += self._registry_claim_types(regs)

        elif intent == "address_or_contract_check":
            # address registry only — must NOT use docs to infer officialness (Allow Matrix rule)
            regs = self.provider.get_registry_records(fx.registry_ids)
            kinds = {r.type for r in regs}
            # entity-driven, not keyword-driven: if a URL/domain was extracted (any language,
            # any case, incl. unicode-confusable), this is a link-officialness check. Keywords
            # are only a fallback for messages where no URL token surfaced.
            is_link_q = bool(e.urls) or any(k in case.user_message for k in ("链接", "url", "http", "域名", "docs"))
            if is_link_q and "address" not in kinds:
                tools_called.append("official_link_registry_lookup")
            else:
                tools_called.append("address_registry_lookup")
                # asking us to *identify* the official bridge/link with no concrete address given
                # also needs the official-link registry (cannot fabricate an address).
                if not e.addresses and any(k in case.user_message for k in ("bridge", "官方入口")):
                    tools_called.append("official_link_registry_lookup")
            if "token" in kinds:
                tools_called.append("token_registry_lookup")
            if any(k in case.user_message for k in ("钱包", "wallet")):
                tools_called.append("wallet_registry_lookup")
                if "official_link_registry_lookup" not in tools_called:
                    tools_called.insert(0, "official_link_registry_lookup")
            evidence_types.append("registry")
            source_ids += [r.id for r in regs]
            claim_types += self._registry_claim_types(regs)

        else:  # unsupported
            answer_mode = AnswerMode.clarification
            claim_types.append("clarification_request")

        return SUTResult(
            case_id=case.id,
            intent=intent,
            intent_source=src,
            risk=risk,
            decision=Decision.allow,
            answer_mode=answer_mode,
            query_path=query_path,
            tools_called=_dedup(tools_called),
            evidence_types=_dedup(evidence_types),
            claim_types=_dedup(claim_types),
            source_ids=_dedup(source_ids),
            has_source=bool(source_ids),
            persisted_raw=False,
            handoff_required=False,
            verifier_status=self._verify(claim_types, source_ids, risk),
        )

    def _registry_claim_types(self, regs) -> list[str]:
        """Typed claims for registry checks. Hard facts only via verified state (DC-004)."""
        out: list[str] = []
        for r in regs:
            state = (r.response_state or r.verification_state or "").lower()
            if state in ("official_verified",):
                out.append("verified_address" if r.type == "address" else "verified_url")
            elif state in ("deprecated_official",):
                out.append("deprecated_status")
            elif state in ("known_risky", "risky"):
                out.append("risk_warning")
            else:
                out.append("unknown_status")  # never emits an unverified address/url claim
        if not out:
            out.append("registry_status")
        return out

    # ---- chain intents ----------------------------------------------------- #
    def _handle_chain(self, case, intent, risk, src, e, query_path, tools_called) -> SUTResult:
        fx = case.fixtures
        msg = case.user_message

        # clarify when we cannot safely act: malformed tx id, or ambiguous network
        if (e.malformed_tx_like and not e.tx_hashes) or e.network_ambiguous or (
            intent == "tx_failure_diagnosis" and not e.tx_hashes and not e.networks
        ):
            return SUTResult(
                case_id=case.id, intent=intent, intent_source=src, risk=risk,
                decision=Decision.handoff_or_clarify, answer_mode=AnswerMode.clarification,
                query_path=QueryPath.none, tools_called=[], evidence_types=[],
                claim_types=["clarification_request"], source_ids=[], has_source=False,
                persisted_raw=False, handoff_required=False,
                verifier_status=VerifierStatus.skipped_low_risk,
                deny_reason="ambiguous_or_malformed",
            )

        ctx = {"tx_hash": e.tx_hashes[0] if e.tx_hashes else "", "address": e.addresses[0] if e.addresses else ""}
        regs = self.provider.get_registry_records(fx.registry_ids)
        tool_results = self.provider.get_tool_results(fx.tool_fixture_ids, ctx)

        tools_called.append("network_registry_lookup")
        for tr in tool_results:
            for t in tr["provides_tools"]:
                tools_called.append(t)
        # wallet-display-mismatch cross-check adds a boundary lookup (§9)
        if "钱包显示" in msg and ("explorer" in msg.lower() or "explorer 显示" in msg):
            tools_called.append("support_boundary_lookup")

        evidence_types = ["registry", "chain"]
        source_ids = [r.id for r in regs] + [tr["id"] for tr in tool_results]

        # error classification (§5, DC-008): hard_error -> fail closed / handoff
        tool_error = None
        for tr in tool_results:
            st = tr["envelope"].get("status")
            if st == "hard_error":
                tool_error = "hard_error"
            elif st == "resolution_error" and tool_error is None:
                tool_error = "resolution_error"

        stolen = any(k in msg for k in ("被骗", "追回", "被盗", "scam", "stolen"))

        if tool_error == "hard_error" or stolen:
            # cannot assert a verified status -> handoff, no tx_status claim
            return SUTResult(
                case_id=case.id, intent=intent, intent_source=src, risk=risk,
                decision=Decision.handoff_or_clarify, answer_mode=AnswerMode.handoff,
                query_path=query_path, tools_called=_dedup(tools_called),
                evidence_types=_dedup(evidence_types), claim_types=["handoff_summary"],
                source_ids=_dedup(source_ids), has_source=bool(source_ids),
                persisted_raw=False, handoff_required=True,
                verifier_status=VerifierStatus.fail_closed if tool_error == "hard_error" else VerifierStatus.blocked,
                tool_error_kind=tool_error,
                deny_reason="hard_error" if tool_error == "hard_error" else "stolen_funds",
            )

        # normal read-only diagnosis: tx_status is a verified typed claim
        claim_types = ["tx_status"]
        return SUTResult(
            case_id=case.id, intent=intent, intent_source=src, risk=risk,
            decision=Decision.allow, answer_mode=AnswerMode.chain_diagnosis,
            query_path=query_path, tools_called=_dedup(tools_called),
            evidence_types=_dedup(evidence_types), claim_types=claim_types,
            source_ids=_dedup(source_ids), has_source=bool(source_ids),
            persisted_raw=False, handoff_required=False,
            verifier_status=self._verify(claim_types, source_ids, risk),
            tool_error_kind=tool_error,
        )

    # ---- boundary intents -------------------------------------------------- #
    def _handle_boundary(self, case, intent, risk, src, e, query_path, tools_called) -> SUTResult:
        fx = case.fixtures
        msg = case.user_message
        ctx = {"tx_hash": e.tx_hashes[0] if e.tx_hashes else "", "address": ""}
        regs = self.provider.get_registry_records(fx.registry_ids)
        tool_results = self.provider.get_tool_results(fx.tool_fixture_ids, ctx)

        tools_called.append("support_boundary_lookup")
        evidence_types = ["registry"]
        source_ids = [r.id for r in regs]
        docs = self.provider.get_docs_sources(fx.docs_source_ids)
        if docs:  # boundary answer also grounded in official docs (e.g. seed-safety guidance)
            tools_called.append("docs_retriever")
            evidence_types.append("docs")
            source_ids += [d.id for d in docs]
        if tool_results:  # boundary case that also reads chain (e.g. exchange withdrawal w/ tx)
            tools_called.append("network_registry_lookup")
            for tr in tool_results:
                tools_called += tr["provides_tools"]
            evidence_types.append("chain")
            source_ids += [tr["id"] for tr in tool_results]

        # handoff signals (§9): reimbursement/loss, account recovery, repeated restatement
        dapp_loss = any(k in msg for k in ("赔付", "资产没了", "授权后", "dapp", "dApp"))
        repeated = any(k in msg for k in ("重复", "三次", "转人工", "还是没"))
        if dapp_loss or repeated:
            return SUTResult(
                case_id=case.id, intent=intent, intent_source=src, risk=risk,
                decision=Decision.handoff_or_clarify, answer_mode=AnswerMode.handoff,
                query_path=query_path, tools_called=_dedup(tools_called),
                evidence_types=_dedup(evidence_types), claim_types=["handoff_summary"],
                source_ids=_dedup(source_ids), has_source=bool(source_ids),
                persisted_raw=False, handoff_required=True,
                verifier_status=VerifierStatus.skipped_low_risk, deny_reason="boundary_handoff",
            )
        account_recovery = any(k in msg for k in ("恢复我的账户", "恢复账户", "打不开", "恢复我的"))
        decision = Decision.handoff_or_clarify if account_recovery else Decision.allow
        return SUTResult(
            case_id=case.id, intent=intent, intent_source=src, risk=risk,
            decision=decision, answer_mode=AnswerMode.boundary_template,
            query_path=query_path, tools_called=_dedup(tools_called),
            evidence_types=_dedup(evidence_types), claim_types=["boundary_explanation"],
            source_ids=_dedup(source_ids), has_source=bool(source_ids),
            persisted_raw=False, handoff_required=account_recovery,
            verifier_status=VerifierStatus.skipped_low_risk,
        )

    # ---- grounding verifier (§6, DC-004) ----------------------------------- #
    def _verify(self, claim_types, source_ids, risk: RiskLevel) -> VerifierStatus:
        hard = {"verified_address", "verified_url", "tx_status"}
        if any(c in hard for c in claim_types):
            # hard fact present -> must be backed by a source (it is, by typed-slot construction)
            return VerifierStatus.passed if source_ids else VerifierStatus.blocked
        if risk in (RiskLevel.low,):
            return VerifierStatus.skipped_low_risk
        return VerifierStatus.passed if source_ids else VerifierStatus.skipped_low_risk


def _dedup(seq: list[str]) -> list[str]:
    seen: dict[str, None] = {}
    for x in seq:
        seen.setdefault(x, None)
    return list(seen.keys())
