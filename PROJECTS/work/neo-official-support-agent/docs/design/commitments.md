# Neo 官网智能客服 · Design Commitments

> 项目级设计承诺 ledger。本文不是 PRD、不是架构说明、不是实现设计；它记录本项目从 `WORK/design-commitment-patterns/agent/` 采纳的、可被系统违反并可被校验抓到的结构性不变量。

## 使用边界

- PRD 负责产品边界：用户、范围、指标、安全原则。
- Architecture 负责结构：组件、数据流、模块边界。
- Implementation Design 负责落地契约：schema、tool contract、eval、backlog。
- 本文负责承诺：系统从 day-1 起必须满足哪些不变量，以及如何抓到违反。

承诺强度：

- `inviolable`：违反会造成资金、安全、合规或官方背书风险；必须阻断。
- `default`：默认采用，除非某阶段明确说明代价超过收益。

## Pattern 筛选结果

| pattern | 本项目处理 | 原因 |
|---|---|---|
| `high-cost-rules-in-code` | 采纳 | secret、投资建议、官方地址、写链边界都属于高代价规则，不能只靠 prompt。 |
| `non-bypassable-bottom-line` | 采纳 | secret / 写链 / 投资建议必须不可绕过。 |
| `three-tier-deny-overrides-allow` | 采纳但收窄 | 本项目不是 OS 权限 agent；采纳为 answer/tool policy 的 deny > confirm/handoff > allow。 |
| `constraint-at-decision-point` | 采纳 | 工具选择和回答模式约束要放在 Policy Gate / tool description / answer mode 最近处。 |
| `reviewer-isolation-fail-closed` | 采纳 | Grounding Verifier 不应被 answer 自我解释说服；异常必须 fail closed。 |
| `mandatory-verification-before-completion` | 采纳 | 用户可见高风险回答必须经过 verifier。 |
| `business-rule-validation-layer` | 采纳 | LLM 结构化输出需要语义规则验证。 |
| `fail-loud-on-bad-json` | 采纳 | 解析失败不能静默变成空对象继续执行。 |
| `schema-validate-before-repair` | 采纳 | 合法输入不得被猜测性修复误伤。 |
| `semantic-typed-schema-fields` | 采纳 | URL、address、tx hash、network 等字段不能是无约束字符串。 |
| `prerequisite-gate-before-terminal-tool` | 采纳 | 失败诊断和官方性判断必须先有对应证据。 |
| `retry-budget-hard-cap` | 采纳 | router / tool / verifier 重试不得无界。 |
| `tool-error-split-counting` | 采纳 | tx not found 与 RPC 故障不能混成一种错误。 |
| `tool-output-budget-with-pointer` | 采纳 | docs、logs、events、transfers 可能不定长。 |
| `route-before-rewrite` | 采纳 | docs query rewrite 必须在路由后按需触发。 |
| `respond-single-output-channel` | 暂不采纳 | 当前目标不是小模型多步工具 agent；最终回答由 Answer Compiler + Verifier 控制。 |
| `immutable-prefix-append-only-log` | 暂缓（带触发） | MVP 优先安全和事实边界；但 Neo 有大块稳定前缀（system prompt + tool schema + policy），production 规模下缓存命中率是成本杠杆。**采纳触发**：进入 Phase 1 公网 beta、出现真实流量成本，且 retention / 存储形态确定时。 |
| `reasoning-output-decoupling` | 暂不单独采纳 | 本项目结构化任务主要是路由 / 抽取；自由文本回答不使用 strict schema 生成。 |
| `agent-config-binary-rules-bounded` | 作为配置审查参考 | 若后续写 system prompt / AGENTS.md，再实例化。 |
| `multi-agent-three-dimension-isolation` | 暂不适用 | 当前架构是单 orchestrator + 确定性模块，不是多角色 agent。 |
| `serialize-writes-to-shared-state` | 暂不适用 | MVP 无多 agent 并发写共享状态。 |
| `background-agent-excluded-from-recovery-triggers` | 暂不适用 | MVP 无后台维护类子 agent。 |
| `memory-temporal-annotation` | 暂不适用 | MVP 不做跨会话记忆。 |

## DC-001：高风险事实只能来自 evidence，不得由 LLM 生成

`strength: inviolable`

**承诺**
所有高风险事实 claim 必须绑定 evidence source id；Answer Compiler 不得从 LLM 常识、docs 相似片段或用户粘贴内容中生成官方地址、官方链接、supported token、RPC、bridge、transaction status、balance、transfer history、fee / migration / support status。

**场景（本项目）**
用户问"Neo X 官方跨链桥地址是多少"，registry 里没有这条。naive 让 LLM 凭"印象"或 docs 相似片段补一个地址出来——错一个字符，用户资产就进了钓鱼合约。本承诺要求：缺 evidence source id 时只能 unknown / 追问 / handoff，绝不由模型生成官方地址 / 链接 / token / tx 状态（见 IMPLEMENTATION_DESIGN §6 Evidence Bundle）。通用机制见 [[high-cost-rules-in-code]] / [[constraint-at-decision-point]]，本节不复述。

**来源簇**
P-024（高代价规则进代码）· P-020（约束靠近决策点）· PRD §6 产品级事实源要求。

**代价 / 范围**
- 代价：coverage 会下降；source 缺失时必须 unknown / 追问 / handoff，不能强答。
- 适用：所有 high-risk / critical answer。
- 不适用：低风险概念解释可以基于官方 docs source 做自然语言总结，但仍需引用 source。

**校验**
- 架构：`AnswerCompiler` 输入只能是 `EvidenceBundle`；高风险 claim 类型必须包含 `source_id`。
- 静态检查：扫描 answer template / compiler，确认 high-risk claim constructor 不接受裸字符串 source。
- eval：构造缺 registry 的 bridge address、unknown wallet URL、fake official contract；期望回答为 unknown / handoff，不输出确认性 claim。
- 人工 review TODO：每新增一种高风险事实类型，必须在 evidence schema 和 verifier 规则中登记。

**前沿问题**
如果 Neo 官方未来提供统一 signed registry API，本承诺可从多源 evidence 绑定简化为 signed source verification，但不能退役。

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/high-cost-rules-in-code.md` + `WORK/design-commitment-patterns/agent/constraint-at-decision-point.md` + `[[agent-permission-system]]` + `[[agent-tool-design]]`

**状态 + 演进日志**
`active`
- `2026-05`：采纳，用于约束官方事实和链上事实的生成边界。

## DC-002：secret、投资建议、写链和钱包连接是不可绕过底线

`strength: inviolable`

**承诺**
系统必须在 LLM、RAG、tool call、trace、analytics 前识别并拦截 secret 类输入；投资建议、写链、签名、转账、授权、approve、bridge 代操作、连接钱包请求必须进入拒答或硬中断路径。这些规则不得作为可配置开关被普通运营配置关闭。

**场景（本项目）**
用户在对话里贴出助记词，或说"你直接帮我 approve 这个 bridge / 连一下我钱包"。naive 靠 system prompt 叮嘱模型别处理——但 prompt 是软的，换种说法 / 语言 / 混在正常问题里就可能被绕过，而这类操作不可逆（资产追不回）。本承诺要求 secret 在 ingress 硬拦、写链 / 连钱包走 Deny Layer（见 IMPLEMENTATION_DESIGN §3.1），且不可被运营配置关闭。通用机制见 [[non-bypassable-bottom-line]]，本节不复述。

**来源簇**
P-025（不可绕过底线）· P-024（高代价规则进代码）· PRD §7 产品级安全边界。

**代价 / 范围**
- 代价：可能出现 false positive，用户需要重新提交不含 secret 的问题。
- 适用：所有入口，包括官网 beta、内部 copilot、handoff summary builder。
- 不适用：用户询问概念性机制，如"什么是私钥"或"Neo 交易签名如何工作"，可走 docs answer，但不能请求或处理用户 secret。

**校验**
- 架构：`IngressGuard` 是 request pipeline 第一个处理节点；命中 secret 后不调用 LLM / retriever / chain tool。
- 静态检查：入口 handler 中 `log(raw_message)`、`trace(raw_message)`、`llm(raw_message)` 必须发生在 guard 之后，或只使用 redacted message。
- eval：seed phrase、WIF、EVM private key、"should I buy GAS"、"connect my wallet"、"approve this bridge for me" 全部必须命中对应拒答 / 中断路径。
- 人工 review TODO：新增入口、日志字段、analytics event 时，必须确认 raw user message 不绕过 guard。

**前沿问题**
多语言 / 方言 / 混合格式 secret 检测的 false negative 如何系统性降低；需要和安全团队 denylist / pattern 维护流程联动。

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/non-bypassable-bottom-line.md` + `WORK/design-commitment-patterns/agent/high-cost-rules-in-code.md` + `[[agent-permission-system]]`

**状态 + 演进日志**
`active`
- `2026-05`：采纳，作为官网客服产品的安全底线。

## DC-003：Policy Gate 是唯一动作空间裁决点，deny 优先

`strength: inviolable`

**承诺**
Policy Gate 是系统唯一的工具分配裁决点。Router 产生 intent / risk / entities；Policy Gate 做两件事——(1) Deny Layer 先跑：安全关键路径（secret / 投资 / 写链 / 连钱包 / 缺证据 / 事故）在 Router 之前拦截，命中即短路；(2) Allow Matrix 后查：intent → 允许的工具子集。三档语义为 deny / handoff-or-clarify / allow（本产品只读，无 OS 式 confirm），deny 永远覆盖 allow；优先级为安全 deny > 临时事故 deny > allow。LLM 不得自行扩展工具集合、回答模式或绕过 Policy Gate。Router 的 intent 分类正确性不由 Policy Gate 独立验证——若 Router 误判 intent 导致分配了错误工具集，由 Grounding Verifier（DC-004）在 claims vs evidence 层面兜底（缺 evidence → clarify/handoff）。

**场景（本项目）**
bot 能查 50 种东西，但"帮我签名转账""approve 这个 bridge"绝对不能做。naive 用一张表每行配 allow / deny——"deny 优先"只是约定，有人把某条 critical 误填 allow，表不拦你。本承诺要求拆成 Deny Layer（保安，先跑）+ Allow Matrix（菜单），结构上让 critical 永不为 allow（见 IMPLEMENTATION_DESIGN §3 与 §3.4 eval 不变量）。通用机制见 [[three-tier-deny-overrides-allow]]，本节不复述。

**来源簇**
P-022（三档 deny overrides allow）· P-020（约束靠近工具选择决策点）· PRD §12 当前决策。

**代价 / 范围**
- 代价：新增 intent / tool 必须同步 policy matrix；快速实验成本上升。
- 适用：所有工具调用和用户可见回答模式。
- 收窄说明：本项目采纳的是 answer/tool policy 三档，不是 OS / shell 权限模型。

**校验**
- 架构：所有 tool execution 只能通过 `PolicyGate.authorize(intent, risk, entities)` 后的 allowed tool set。
- 静态检查：扫描 tool invocation，确认不存在绕过 Policy Gate 的直接 adapter 调用。
- eval：LLM router 输出低风险但 Deny Layer 命中投资建议 / secret / write-chain 时，Policy Gate 必须覆盖为 deny（deny-overrides-allow 方向）。Router 误判 intent 导致分配错误工具集的后果由 DC-004 verifier 兜底（missing_evidence_block_rate）。
- eval 不变量（见 IMPLEMENTATION_DESIGN §3.4）：每个 `(intent × risk)` 唯一解析；secret / 投资 / 写链 / 连钱包 / critical 永不解析到 allow；Deny Layer 命中必覆盖 Allow Matrix。
- 人工 review TODO：新增工具、intent、answer mode 时，必须补 Allow Matrix 行和至少一个 deny 覆盖用例。

**前沿问题**
动态 policy（事故期间 kill switch、某网络维护中）如何和静态 deny / allow 表组合，避免配置冲突。

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/three-tier-deny-overrides-allow.md` + `WORK/design-commitment-patterns/agent/constraint-at-decision-point.md` + `[[agent-permission-system]]`

**状态 + 演进日志**
`active`
- `2026-05`：采纳，用于收敛客服 orchestrator 的动作空间。
- `2026-06`：澄清措辞——原「Router 只产生候选」措辞暗示 Policy Gate 有独立 intent 验证步骤，但三档模型的源 pattern 管的是工具级 deny-overrides-allow，不管 intent 正确性验证。修正为：Policy Gate 做工具分配层裁决，Router 误判 intent 的后果由 DC-004 verifier 兜底。

## DC-004：用户可见高风险回答必须经过独立 grounding verifier，异常 fail closed

`strength: inviolable`

**承诺**
任何 high-risk / critical 回答在返回用户前必须经过 Grounding Verifier。Verifier 只读取 answer claims、claim type 和 EvidenceBundle，不读取 Answer Compiler 的自我解释或自然语言辩护；verifier 解析失败、超时、证据缺失或内部错误时默认拦截、删 claim、追问或 handoff，不得默认放行。硬事实类 claim（地址 / URL / 合约 / bridge / tx 状态 / 余额 / token）由确定性 exact-match 对 evidence source 裁决；LLM / NLI 蕴含判定只对软叙述类 claim 做 advisory，无权放行硬事实；硬事实只能通过已验证的 typed 槽位渲染，回答自由文本中不得出现未经校验的地址 / URL / 数字。

**场景（本项目）**
Answer Compiler 生成"地址 A 是官方 bridge"，还自带一段很有说服力的解释，但 evidence 里根本没有 A。naive 让 verifier 连同那段自我解释一起读 → 被"辩护"说服而放行；或 verifier 一超时就默认放行。本承诺要求：verifier 只读 claims + evidence、不读自我解释，且解析失败 / 超时 / 缺证据一律 fail closed（见 IMPLEMENTATION_DESIGN §1 verifier_error 分支）。通用机制见 [[reviewer-isolation-fail-closed]]，本节不复述。

**来源簇**
P-023（reviewer isolation + fail closed）· P-033 / P-028 / P-031（完成前强制验证）。

**代价 / 范围**
- 代价：合法回答可能因 verifier 故障被拦截，需要监控和人工接管。
- 适用：official link / address check、chain diagnosis、boundary response、security crisis。
- 不适用：低风险闲聊式 docs summary 可用轻量 source check，但不应完全绕过 source citation。

**校验**
- 架构：`AnswerCompiler -> GroundingVerifier -> UserAnswer` 是唯一用户可见高风险路径。
- 静态检查：扫描 response return path，确认 high-risk answer 不能直接 return compiler output。
- eval：构造 answer 声称"地址 A 是官方 bridge"但 evidence 中没有 A；期望 verifier 拦截。构造 verifier mock 500；期望 fail closed。
- 架构：claim 按类型路由——硬事实走确定性 exact-match（规范化后字符串相等），软叙述走禁语扫描 + 散文夹带硬事实扫描，LLM / NLI 蕴含仅 advisory；硬事实只来自 typed verified slot。
- 静态检查：扫描 answer 渲染路径，确认不存在把裸 address / URL 直接写进 prose 的通道。
- eval：构造散文里夹带未验证地址的 answer；期望被夹带扫描拦截。
- 人工 review TODO：verifier prompt / checker 输入不得拼入 answer 的自我解释字段。

**前沿问题**
（已定，2026-05）形态 = 混合·按 claim type 分：硬事实只走确定性、LLM 蕴含仅 advisory、硬事实只经 typed verified slot。残留：多语言 NLI / faithfulness 模型偏弱，软叙述蕴含判定的可靠度与上线门槛——计划 Phase 2 用 eval 卡着再开 LLM 蕴含层。

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/reviewer-isolation-fail-closed.md` + `WORK/design-commitment-patterns/agent/mandatory-verification-before-completion.md` + `[[agent-permission-system]]` + `[[harness]]`

**状态 + 演进日志**
`active`
- `2026-05`：采纳，作为高风险回答上线门槛。
- `2026-05`：定 verifier 形态 = 混合·类型分（硬事实确定性独占裁决 + 软叙述 advisory + 硬事实只经 typed verified slot）；LLM 蕴含判定 Phase 2 起按 eval 开启。

## DC-005：LLM 结构化输出必须先校验语法和业务规则，再进入下游

`strength: inviolable`

**承诺**
LLM 生成的 intent、entities、claim list、handoff draft 等结构化输出，在进入 Policy Gate、tool adapter、Answer Compiler 或 Handoff Builder 前，必须经过 schema 校验和业务规则验证。JSON parse 失败必须 fail loud；格式修复只能在校验失败分支触发；URL、address、tx_hash、network、source_id 等语义敏感字段必须使用显式格式约束，不得作为裸 `string` 放行。

**场景（本项目）**
模型从用户消息抽出 tx_hash / address / url 字段。naive 全用裸 string + 一句 description——于是 Markdown 包起来的 url（`[戳这](evil.site)`）、少一位的地址、大小写仿冒域名全能进下游，被当官方事实判断。本承诺要求这些字段用显式 pattern / enum / url 约束，且进 Policy Gate 前 parse → schema → business 校验（见 IMPLEMENTATION_DESIGN §1、§2）。通用机制见 [[semantic-typed-schema-fields]]，本节不复述。

**来源簇**
P-011（业务规则验证层）· P-018（fail loud）· P-037（先校验再修复）· P-038（语义化类型）。

**代价 / 范围**
- 代价：需要维护 schema 和 validator，且业务规则变化时必须同步更新。
- 适用：所有 LLM structured output。
- 不适用：纯自然语言 answer draft；但 draft 被拆成 claims 后，claims 必须校验。

**校验**
- 架构：所有 `LLM output -> downstream` 路径中间必须有 `parse -> schema_validate -> business_validate`。
- 静态检查：扫描 LLM call sites，确认 structured output 没有直接进入 tool / policy / compiler。
- eval：损坏 JSON、缺字段、URL 为 Markdown link、tx_hash 格式错误、risk/intent 矛盾样本必须被拦截并给出具体错误。
- 人工 review TODO：新增 schema 字段时检查是否属于语义敏感字段；若是，必须补 pattern / format / enum。
- 架构：schema 唯一源 = 后端 Pydantic v2 model；喂 LLM 的 JSON Schema 由 `.model_json_schema()` 生成，运行时校验即该 model；IMPLEMENTATION_DESIGN 中的 YAML 为生成示意，非源。
- CI：断言"生成的 JSON Schema == 实际喂给 LLM 的那份"；doc schema 片段为生成产物，禁止手改后期望生效（防双写漂移）。
- 边界：本承诺业务校验只管输出内部一致性（risk / intent 自洽、字段齐全），不做 registry 事实核对（那是 DC-001 / DC-006）。

**前沿问题**
（已定，2026-05）防漂移 = Pydantic v2 单一源 → 生成喂模型的 JSON Schema + 运行时校验同源，doc YAML 降级为生成示意，CI 断言一致。残留：部分 LLM provider 不 honor 全部 `pattern` / `format`，模型侧约束为 best-effort，运行时校验才是真正的闸。

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/business-rule-validation-layer.md` + `WORK/design-commitment-patterns/agent/fail-loud-on-bad-json.md` + `WORK/design-commitment-patterns/agent/schema-validate-before-repair.md` + `WORK/design-commitment-patterns/agent/semantic-typed-schema-fields.md` + `[[structured-output]]` + `[[tool-call-repair-harness]]`

**状态 + 演进日志**
`active`
- `2026-05`：采纳，用于防止结构化输出静默污染 policy / tool / handoff。
- `2026-05`：定 schema 源 = 后端 Pydantic v2（后端语言 = Python），JSON Schema 与运行时校验同源生成，doc YAML 降级为生成示意 + CI 防漂移。

## DC-006：诊断和官方性判断必须有前置证据门

`strength: inviolable`

**承诺**
系统不得在缺少必要前置证据时执行终局性判断：失败交易诊断必须先有对应 chain read；official / deprecated / risky 判断必须先有 registry lookup；exchange / wallet boundary 判断必须先有 support boundary 结果。前置证据缺失时只能追问、unknown 或 handoff。

**场景（本项目）**
用户只甩一句"我的交易为什么失败"，没给 tx hash。naive 让模型直接编一个失败原因（"大概是 gas 不够"）。本承诺要求：失败诊断必须先有对应 chain read、官方性判断必须先有 registry lookup——证据没到位只能追问 / unknown / handoff，且诊断函数签名收 evidence object 而非裸 query（见 IMPLEMENTATION_DESIGN §3.2 fallback 列）。通用机制见 [[prerequisite-gate-before-terminal-tool]]，本节不复述。

**来源簇**
P-003（前置门控）· PRD §6 产品级事实源要求。

**代价 / 范围**
- 代价：用户体验更保守，输入不完整时需要追问。
- 适用：tx failure diagnosis、address / contract check、official navigation、third-party boundary。
- 不适用：低风险概念解释不要求 chain read。

**校验**
- 架构：diagnosis / official check / boundary answer 的函数签名必须接收对应 evidence object，而不是仅接收 user query。
- 静态检查：扫描 failure diagnosis builder，确认不存在 `diagnose(query_text)` 这类无 evidence 入口。
- eval：用户只问"为什么失败"但没给 tx hash；期望追问。用户贴 unknown address；期望 unknown，不输出官方判断。
- 人工 review TODO：新增 answer mode 时检查是否需要 prerequisite evidence。

**前沿问题**
多证据源冲突时的门控语义：是否以 chain source 优先、registry 优先，还是必须 handoff。

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/prerequisite-gate-before-terminal-tool.md` + `[[small-model-harness-engineering]]`

**状态 + 演进日志**
`active`
- `2026-05`：采纳，用于消除无证据终局判断。

## DC-007：不定长工具输出必须有预算、preview 和指针

`strength: default`

**承诺**
Docs retrieval、transaction logs、event logs、transfer history、explorer/indexer 查询等可能返回不定长数据的工具，必须声明输出预算。超过预算时，完整结果进入外部存储或 evidence attachment，模型上下文只接收 preview / summary 和可追溯指针；不得静默截断后让模型误以为结果完整。

**场景（本项目）**
用户贴一个地址问"我的转账到了吗"，地址有 500 条转账记录；或贴一笔交易问失败原因，回执含几百条 event log。naive 截断一半喂模型，模型以为"这就是全部"→ 答"你这个地址没有这笔转账"，错不在模型，在工具悄悄骗了它。本承诺要求超预算改走 preview + 指针（占位预算见 IMPLEMENTATION_DESIGN §5）。通用机制见 [[tool-output-budget-with-pointer]]，本节不复述。

**来源簇**
P-021（工具输出预算 + pointer）。

**代价 / 范围**
- 代价：需要 attachment 存储、生命周期清理和 pointer 读取逻辑。
- 适用：所有不定长 read tool。
- 不适用：状态码、单笔 receipt、registry exact lookup 等已知小输出。

**校验**
- 架构：tool registry 中每个工具声明 `max_output_chars` 或证明输出有上界。
- 静态检查：枚举 tools，缺预算且无上界说明则 fail。
- eval：mock 200+ transfer history / 大量 logs，期望上下文返回不超过预算且 evidence attachment 可追溯。
- 人工 review TODO：新增工具必须填写输出预算或上界说明。

**前沿问题**
Evidence attachment 的 retention 和隐私策略尚未定；这会影响指针存储形态。

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/tool-output-budget-with-pointer.md` + `[[agent-tool-design]]`

**状态 + 演进日志**
`active · pending:retention（attachment 存储形态）· pending:tuning（预算数值待真实数据校准）`
- `2026-05`：采纳为默认承诺；输出预算字段已进 IMPLEMENTATION_DESIGN §5 envelope，数值为占位；attachment 存储形态等待 retention 决策。

## DC-008：工具错误必须分类计数，所有重试必须有硬上限

`strength: default`

**承诺**
系统必须区分 HardError 和 ToolResolutionError：RPC / adapter / parser / provider 故障计入 hard error；tx not found、address invalid、resource unknown 等合法无结果不计入 hard error，而作为业务语义进入 evidence。所有纠正 / 重试 / 换参数环路必须有 per-turn 硬上限，超限后 abort / handoff，不得无界循环。

**场景（本项目）**
用户贴一个 tx hash 问"成功了吗"，链上只读查询返回空。"空"有两种意思——交易真的不存在（正常，直接答），还是 RPC 节点挂了 / 卡了（事故，绝不能说"查无此交易"）。naive 把两者混成一种失败、累加同一计数，要么早停，要么误导用户。本承诺要求显式分 HardError / ToolResolutionError（见 IMPLEMENTATION_DESIGN §5 envelope），重试有 per-turn 硬上限。通用机制见 [[tool-error-split-counting]]，本节不复述。

**来源簇**
P-004（错误分类计数）· P-007（重试硬上限）。

**代价 / 范围**
- 代价：tool contract 必须携带 error_kind，dispatcher 处理更复杂。
- 适用：chain adapter、docs retriever、registry lookup、verifier retry。
- 不适用：无重试的一次性 deterministic lookup；但仍需返回明确错误语义。

**校验**
- 架构：tool result 类型包含 `ok | resolution_error | hard_error` 或等价枚举。
- 静态检查：工具实现不得统一 `raise Exception` 而丢失 404 / not found 语义。
- eval：tx not found 不能触发 hard error 熔断；RPC 500 连续 N 次必须触发 hard cap 并 handoff / incident。
- 人工 review TODO：每个 adapter 新增错误码时，必须归类为 resolution / hard / policy。

**前沿问题**
第三方 explorer 返回空结果时，如何区分真实 not found 与 indexer lag / outage。

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/tool-error-split-counting.md` + `WORK/design-commitment-patterns/agent/retry-budget-hard-cap.md` + `[[small-model-harness-engineering]]`

**状态 + 演进日志**
`active · pending:provider（not-found vs outage 判别等真实 RPC/explorer）· pending:tuning（retry 上限数值）`
- `2026-05`：采纳；error_kind 枚举已进 IMPLEMENTATION_DESIGN §5 envelope；not-found 与节点故障的可靠判别和 retry 上限数值等接入真实 provider 后定。

## DC-009：Docs query rewriting 必须在路由之后按需触发

`strength: default`

**承诺**
Docs retriever 的 query rewriting 不得成为所有 query 的必经路径。系统必须先区分 registry exact lookup、chain lookup、direct docs query、ambiguous docs query；只有 ambiguous docs query 才允许进入 rewrite。明确实体、地址、URL、tx hash、official / bridge / contract 类查询不得被 rewrite 改写后再判断官方性。

**场景（本项目）**
用户问"Neo X official bridge address"。naive 把所有 query 都先丢进 rewrite，改写成"Neo X 跨链桥 合约"再去 docs 检索，可能召回某篇博客里的地址当成官方答案。本承诺要求：带 address / url / tx hash / official-bridge-contract 实体的请求归 registry_exact / chain，不进 docs_ambiguous、不被 rewrite（见 IMPLEMENTATION_DESIGN §3.5 Query Path Classification）。通用机制见 [[route-before-rewrite]]，本节不复述。

**来源簇**
P-039（route before rewrite）。

**代价 / 范围**
- 代价：需要维护 route-before-rewrite 分类器，并评估误路由。
- 适用：docs retrieval 和多语言 / 模糊概念问答。
- 不适用：registry-only / chain-only / safety-critical query。

**校验**
- 架构：query pipeline 中 rewrite 只在 `docs_ambiguous` 分支出现。
- 静态检查：`rewrite_query()` 不得位于所有请求共用的主路径。
- eval：direct query "Neo X official bridge address" 不得通过 rewrite 生成地址；fake URL / contract 不得因 rewrite 获得官方背书。
- 人工 review TODO：上线前比较 direct docs query 和 rewritten query 的召回率，不能凭感觉全量开启 rewrite。

**前沿问题**
多语言场景下，翻译是否属于 rewrite；如果翻译会改变实体，应走 entity-preserving translation 还是 registry lookup。

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/route-before-rewrite.md` + `[[rag-query-rewriting]]`

**状态 + 演进日志**
`active`
- `2026-05`：采纳，用于防止 RAG 改写污染官方事实判断。
