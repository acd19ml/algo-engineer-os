# Neo 官网智能客服 · Implementation Plan

> 本文件补 `README.md` 中的「原型 / Chat API request-response 未定」和 `interview-defense-matrix.md` 的 GAP-2。它是工程落地计划，不替代 PRD、Architecture 或 Implementation Design。

## 1. 当前结论

MVP 先做 **单体 Python service + 模块化边界**：

| 层 | 选择 | 原因 |
|---|---|---|
| API service | FastAPI | Chat API、admin API、eval job 都是 HTTP / job 型接口；后续可拆服务。 |
| Schema | Pydantic v2 | 已在 design commitments 中锁定为结构化输出单一源。 |
| Registry prototype | repo 内 YAML + schema validation | 方便 review、diff、eval；production 再迁到 CMS / DB / signed config。 |
| Eval runner | pytest + deterministic fixture providers | 先验证 policy / routing / verifier，不依赖真实链上 provider。 |
| Docs index | 静态 docs fixture + source metadata | Phase 0 先小集，Phase 1 再接 crawler / search index。 |
| Observability | redacted JSONL traces + metric counters | 先保证 secret 不落原文，再做 tracing 平台接入。 |

不先上 LangGraph。当前流程是单入口、强 policy、有限工具集合，pipeline 更容易证明每个 gate 不可绕过。只有当 Phase 2 出现多轮诊断、incident 联动和人工审核队列后，再评估 graph / workflow。

## 2. Official Source Candidates

以下是 2026-06-01 检索到的官方或官方入口候选。它们可用于 prototype registry / fixture，但进入生产前仍需 Neo 内部 owner 确认。

| 范围 | 候选 source | 当前用法 |
|---|---|---|
| Neo 主站 | https://neo.org/ | official site allowlist。 |
| Neo developer resources | https://neo.org/dev | developer / explorer / SDK 资源入口候选；其中 explorer 多为生态工具，不能默认写成 Neo 自营。 |
| Neo N3 docs | https://docs.neo.org/docs/n3/overview.html | N3 概念和产品解释来源。 |
| Neo N3 native tokens | https://docs.neo.org/docs/n3/foundation/Native%20tokens.html | NEO / GAS 角色 fixture 依据。 |
| Neo N3 native contracts | https://docs.neo.org/docs/n3/reference/rpc/getcontractstate.html | NeoToken native contract hash fixture 依据。 |
| Neo N3 RPC API | https://developers.neo.org/docs/n3/reference/rpc/api | N3 `getrawtransaction`、`getapplicationlog`、`getnep17balances` 等 adapter contract 依据。 |
| Neo N3 SDK RPC | https://developers.neo.org/docs/n3/develop/tool/sdk/rpc | N3 RPC endpoint / plugin 依赖说明依据。 |
| Neo X official site | https://x.neo.org/ | Neo X 入口、docs / explorer / bridge 入口候选。 |
| Neo X network docs | https://xdocs.ngd.network/development/development-environment-information | Neo X chain id、RPC、explorer、bridge link 候选。 |
| Neo X JSON-RPC | https://xdocs.ngd.network/development/json-rpc-api | EVM adapter read calls 依据。 |
| Neo X bridge docs | https://xdocs.ngd.network/bridge/quick-start-bridging-assets | bridge UX / supported direction 的说明依据。 |
| Neo X system contracts | https://xdocs.ngd.network/governance/neo-x-system-contracts | Neo X system contract fixture 依据。 |

## 3. Chat API v0

### 3.1 Request

```yaml
POST /api/support/chat
content-type: application/json

body:
  conversation_id: string?
  user_message: string
  locale: string?
  channel: official_website | internal_copilot | eval
  user_context:
    region: string?
    authenticated: false
  debug:
    fixture_case_id: string?        # eval only
```

约束：

- `user_message` 进入任何 log / trace / LLM 前必须先过 ingress guard。
- `authenticated` MVP 固定 false；不接钱包、不接用户账户态。
- `fixture_case_id` 只允许 `channel=eval` 时使用，不能出现在官网入口。

### 3.2 Response

```yaml
status: ok | hard_interrupt | refusal | clarification | handoff | error
answer_mode: docs_answer | registry_template | chain_diagnosis | boundary_template | hard_interrupt | refusal | clarification | handoff
message: string
sources:
  - source_id: string
    kind: registry | docs | chain | incident
    label: string
    url: string?
handoff:
  required: boolean
  reason: string?
  recommended_team: support | devrel | security | exchange_redirect | wallet_vendor | none
safety:
  raw_secret_detected: boolean
  redacted: boolean
diagnostics:
  intent: string
  risk: low | medium | high | critical
  query_path: registry_exact | chain | docs_direct | docs_ambiguous | none
  policy_decision: deny | handoff-or-clarify | allow
  verifier_status: passed | blocked | skipped_low_risk | fail_closed
```

约束：

- `diagnostics` 默认只给 internal copilot / eval；官网用户只看 message、sources、handoff。
- `message` 中的 URL、address、tx status、balance、token role 必须来自 typed verified slot。
- `sources` 不能把 LLM answer compiler 作为 source。

## 4. Admin API v0

Phase 0 不做完整后台，先用 PR + review 管理 YAML registry。若要暴露 Admin API，最小接口如下：

```yaml
POST /api/admin/registry/propose-change
GET  /api/admin/registry/changes/{change_id}
POST /api/admin/registry/changes/{change_id}/approve
POST /api/admin/registry/changes/{change_id}/reject
```

Admin API 必须满足：

- 所有 change 带 `owner`、`reviewer`、`source_url`、`source_checked_at`。
- critical registry change 需要双人 review。
- 删除 / deprecated 必须保留旧记录和替代路径。

## 5. Eval Job v0

```yaml
POST /api/eval/run
body:
  case_file: ../../eval/eval-cases.yaml
  fixture_file: ../../eval/eval-fixtures.yaml
  mode: deterministic_fixture | llm_router_mock | llm_integrated
```

最小实现顺序：

1. `fixture_coverage_check`：所有 case 引用的 fixture id 都存在。
2. `policy_only_run`：不生成自然语言，只跑 guard / entity / router / policy / query_path。
3. `tool_fixture_run`：用 fixture provider 生成 Evidence Bundle。
4. `answer_contract_run`：生成 typed claims，不要求文案完美。
5. `verifier_run`：验证 hard facts exact match。

## 6. Week-1 Build Plan

| Day | 目标 | 输出 |
|---:|---|---|
| 1 | 建 FastAPI skeleton + Pydantic schemas | request / response / entities / policy / evidence models |
| 2 | Ingress Guard + rule router | secret / investment / write-chain / wallet-connect tests |
| 3 | Policy Gate + query path classifier | Allow Matrix tests + route-before-rewrite tests |
| 4 | Fixture registry + mocked chain adapters | `../../eval/eval-fixtures.yaml` provider |
| 5 | Answer typed claims + verifier | hard facts exact-match checks |
| 6 | Eval runner | 100 cases deterministic run |
| 7 | Result table + gap review | prototype metrics, no business KPI claim |

## 7. Still Open

| 问题 | 当前处理 |
|---|---|
| 真实 production provider | 只列 official source candidates；上线前 Neo 内部确认。 |
| Registry storage | prototype 用 YAML；production 在 registry ops plan 中决定。 |
| retention | 默认最小化；tx/address 存储等待隐私确认。 |
| multilingual MVP | 先把 secret / investment 放入 multilingual adversarial suite，完整多语言 docs QA 延后。 |
