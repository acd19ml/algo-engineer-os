# Neo 官网智能客服 · Registry Ops Plan

> 本文件补 registry owner、review SLA、source governance、provider 选择和 bridge 边界。它不把候选 URL 写成生产事实源；所有生产 source 必须由 Neo 内部 owner 确认。

## 1. Registry 分层

| 层 | 内容 | 能否直接回答用户 | 说明 |
|---|---|---|---|
| `verified` | owner 已确认、source_url 可追溯、last_verified_at 未过期 | 可以 | Phase 1 官网只读 Beta 的最低要求。 |
| `candidate` | 来自 Neo 官方页面 / 官方文档入口，但 owner 未确认 | 仅 internal copilot / eval | 可以用于 prototype，不可作为生产背书。 |
| `ecosystem_listed` | Neo 官网列出的生态工具，例如 explorer / wallet | 可以导航，但必须说明不是 Neo 自营 | 不可写成“Neo 官方运营”。 |
| `unknown` | 无 registry 命中 | 不背书 | 回答 `unknown_not_verified`。 |
| `risky` | security denylist 或已知钓鱼 / lookalike | 警告 | 需要 security owner。 |

## 2. Proposed Owner Matrix

| Registry | Proposed owner | Reviewer | SLA |
|---|---|---|---|
| Network Registry | protocol_ops / neo_x_ops | engineering lead | critical: 7 days; normal: 30 days |
| Token Registry | protocol_ops | ecosystem / legal if public claim | 30 days |
| Official Link Registry | web / devrel | security for wallet / bridge links | 14 days |
| Contract / Address Registry | protocol_ops / security | second reviewer required | critical: 7 days |
| Wallet Registry | ecosystem / devrel | security | 30 days |
| Support Boundary Registry | support / legal | product owner | 90 days or policy change |
| Phishing / Risky URL Denylist | security | security reviewer | continuous; emergency update allowed |

这些 owner 名称是职责占位，不是 Neo 组织结构事实。

## 3. Review Rules

| Change type | Review rule | Reason |
|---|---|---|
| Add official bridge / contract address | 2 reviewers + official source URL + exact address normalization | 错误地址可能造成资金损失。 |
| Deprecate official link / contract | 2 reviewers + replacement / warning text | 避免旧入口继续被背书。 |
| Add explorer / wallet resource | 1 owner + source URL + ownership label | 区分 official-owned 与 ecosystem-listed。 |
| Add risky domain / address | security owner approval | 避免误伤，但安全优先。 |
| Add support boundary | support / legal review | 影响承诺和责任边界。 |

## 4. Storage Plan

### Phase 0 Prototype

- `registries/*.yaml` in repo.
- PR review = registry review.
- CI checks schema、duplicate id、expired `last_verified_at`、URL normalization、address normalization。

### Phase 1 Beta

- 仍可用 Git-backed registry，但需要 signed release artifact。
- Runtime 只读加载 `registry_bundle_version`。
- Admin edit 不直接改 production，必须生成 pending change。

### Phase 2+

- 如果已有 Neo CMS / internal config，迁入内部系统。
- 保留 exportable signed snapshot，eval 和 replay 使用同一 snapshot。

## 5. Official Source Candidates Checked On 2026-06-01

| Record | Candidate source | Registry treatment |
|---|---|---|
| Neo official site | https://neo.org/ | `candidate` until web owner confirms. |
| Neo developer resources | https://neo.org/dev | `candidate`; explorer / SDK resources may be `ecosystem_listed` rather than official-owned. |
| Neo N3 docs | https://docs.neo.org/docs/n3/overview.html | `candidate` docs source. |
| Neo N3 native tokens | https://docs.neo.org/docs/n3/foundation/Native%20tokens.html | `candidate` token role source. |
| Neo N3 native contracts | https://docs.neo.org/docs/n3/reference/rpc/getcontractstate.html | `candidate` native contract hash source. |
| Neo N3 RPC API | https://developers.neo.org/docs/n3/reference/rpc/api | `candidate` adapter source for N3 read methods. |
| Neo N3 SDK RPC | https://developers.neo.org/docs/n3/develop/tool/sdk/rpc | `candidate`; notes plugin dependencies for ApplicationLogs / TokensTracker. |
| Neo X site | https://x.neo.org/ | `candidate` Neo X official entry. |
| Neo X network info | https://xdocs.ngd.network/development/development-environment-information | `candidate`; contains chain id, RPC, explorer and bridge links. |
| Neo X JSON-RPC | https://xdocs.ngd.network/development/json-rpc-api | `candidate` EVM adapter source. |
| Neo X bridge quick start | https://xdocs.ngd.network/bridge/quick-start-bridging-assets | `candidate` bridge UX source. |
| Neo X system contracts | https://xdocs.ngd.network/governance/neo-x-system-contracts | `candidate` system contract source, including Bridge system contract. |
| Status page | candidate found by search, not confirmed from Neo official navigation | keep `unknown_not_verified` until owner confirms. |

## 6. Provider Policy

| Provider class | Allowed in prototype | Allowed in production | Notes |
|---|---|---|---|
| Official docs URL | yes | yes after owner confirmation | Used for docs / registry source. |
| Official RPC endpoint in docs | yes | yes after ops approval | Need uptime / rate-limit / incident handling. |
| Ecosystem explorer listed by Neo | yes | yes with `ecosystem_listed` label | Do not claim Neo-operated. |
| Random third-party RPC / explorer | no | no | Can be used only as engineering experiment outside support answer. |
| User-provided explorer text | as adversarial data only | no trust | Treat as data, never instruction. |

## 7. Bridge Boundary

What the bot can do:

- Provide verified bridge entry link from registry.
- Explain bridge direction at a high level from official docs.
- Check a user-provided contract address only by exact registry match.
- Diagnose visible tx status on Neo N3 / Neo X if the user provides tx hash and network.

What the bot cannot do:

- Connect wallet.
- Ask user to sign / approve / bridge.
- Operate bridge for the user.
- Claim unsupported bridge route / token support without registry evidence.
- Diagnose full cross-chain lifecycle unless bridge indexer / status source is approved.

MVP stance: **bridge full lifecycle diagnosis is out of scope**. The bot supports official navigation and per-chain tx status only.

## 8. Expiry Policy

| Record type | Expiry rule |
|---|---|
| Official bridge / contract / wallet download | stale after 7 days if not reviewed. |
| Official docs link | stale after 30 days if not reviewed. |
| Ecosystem explorer / wallet resource | stale after 30 days. |
| Support boundary | stale after 90 days or legal / support policy change. |
| Risky domain / address | no auto-expiry; requires security review to remove. |

Stale critical record behavior: do not output as verified; answer with handoff or unknown.
