# Neo 官网智能客服 · 面试挑战防御矩阵

> 目的：把这个项目按 agent 开发岗位可能被挑战的角度建成 catalog。本文只做索引、readiness 和 GAP 追踪；项目事实回到 `../README.md` / `../docs/` / `../eval/`，表达稿回到 `answers/`。

## Readiness 图例

- ✅ **有现成回答**：项目文档已有可直接组织的回答。
- ⚠️ **部分准备**：有方向和设计，但缺真实数据、实现证据或横向比较。
- ❌ **明显缺口**：当前留存文档不足，被问到只能诚实承认或补 prototype。

## 谁会问

- **HR**：真实性、职责、时间线、结果。
- **技**：agent 架构、工程实现、评测、工具调用。
- **总**：取舍、边界、行业判断、复盘。
- **研**：RAG / agent / verifier / eval 方法论。

---

## 1. 项目真实性与边界

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 这个项目到底上线了吗？ | 诚实度 / HR + 技 | ✅ | README “当前事实”：当前不能说上线或业务降本 |
| 你的角色是什么？ | 贡献边界 / HR | ✅ | README “当前事实”：2025.02-2025.07，一人负责产品方案 |
| 原来 Neo 官网客服是什么状态？ | 背景真实性 / HR + 总 | ✅ | README “业务问题”：无官网客服，依赖 Discord 社区和全球开发者 |
| 团队几个人？你是不是工程实现负责人？ | 职责边界 / HR + 技 | ⚠️ | 当前只能说产品方案一人负责；工程实现团队和代码贡献待补证据 |
| 为什么没有业务指标？ | 诚实边界 / HR + 总 | ✅ | README “当前事实”明确无客服时间降低 30% 等数据 |
| 如果没有上线，这个项目怎么用于简历？ | 价值判断 / HR + 总 | ⚠️ | 定位为 agent harness / system design 项目，不包装成业务落地项目；若目标岗位强要求上线结果，应弱化 |

## 2. 产品判断

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 为什么 Neo 官网需要客服 bot？ | 场景判断 / HR + 技 | ✅ | PRD §1、README “业务问题” |
| 为什么不是继续依赖 Discord？ | 产品判断 / 总 | ✅ | 社区支持能响应复杂问题，但重复问题、官方导航和链上只读诊断可产品化 |
| 用户是谁？ | 用户理解 / HR + 技 | ✅ | PRD §3：普通持币用户、Neo X 用户、开发者、高风险用户 |
| MVP 做什么不做什么？ | 边界意识 / 技 | ✅ | PRD §4 |
| 为什么不做交易所 / 第三方钱包问题？ | 边界意识 / HR + 技 | ✅ | PRD 非目标 + Support Boundary Registry |
| 为什么转人工不是失败？ | 产品策略 / 总 | ✅ | PRD §8；高风险场景下 handoff 是安全策略 |
| 多语言 MVP 怎么做？ | 产品范围 / 技 | ❌ | GAP-1：需补 MVP 语言列表和多语言 adversarial eval 切分 |

## 3. 技术提案与架构取舍

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 为什么不是泛 RAG bot？ | agent / RAG 边界 / 技 + 研 | ✅ | `../docs/decision/TECH_PROPOSAL.md` §4；`../docs/design/commitments.md` |
| 为什么不是开放 ReAct Web3 agent？ | 动作空间控制 / 技 + 总 | ✅ | TECH_PROPOSAL §4；写链、签名、钱包连接不进动作空间 |
| 为什么不是纯 FAQ / 静态导航？ | AI 适用性 / HR + 技 | ✅ | TECH_PROPOSAL §3-§4 |
| 为什么不是纯人工客服？ | 产品 ROI / 总 | ✅ | 重复问题、链上只读查询和 handoff summary 可产品化 |
| 为什么叫 orchestrator 而不是 chatbot？ | 架构理解 / 技 | ✅ | LLM 只是 router / interpreter / compiler 的一部分，事实和动作由确定性模块约束 |
| 如果今天让你实现，首选技术栈是什么？ | 工程落地 / 技 | ✅ | `../docs/implementation/implementation-plan.md`：FastAPI / Pydantic v2 / YAML registry prototype / pytest eval harness |
| 是否应该用 LangGraph / workflow？ | agent 编排 / 技 | ⚠️ | 当前文档是单 orchestrator pipeline，未明确选 LangGraph；可答“先 pipeline 化，复杂多步后再考虑 graph” |

## 4. Agent Harness 设计

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| agent 的动作空间怎么定义？ | agent 安全 / 技 | ✅ | `../docs/implementation/IMPLEMENTATION_DESIGN.md` §3；Deny Layer + Allow Matrix |
| 两个相似工具如何保证正确调用？ | tool routing / 技 | ✅ | `answers/similar-tool-routing.md` |
| rule router 和 LLM router 谁优先？ | determinism / 技 | ✅ | critical pattern / Deny Layer 覆盖 LLM router |
| Policy Gate 为什么不能只靠 prompt？ | 安全边界 / 技 + 总 | ✅ | design/commitments DC-002 / DC-003 |
| 结构化输出怎么防坏 JSON？ | structured output / 技 | ✅ | DC-005；Pydantic v2 单一源 + parse/schema/business validate |
| URL / address / tx_hash 为什么不能是裸 string？ | schema 语义 / 技 | ✅ | DC-005；semantic typed fields |
| Tool output 为什么只能是 data？ | prompt injection / 技 | ✅ | `../docs/architecture/ARCHITECTURE.md` 关键约束：外部内容不得作为 instruction |
| 工具错误怎么分类？ | robustness / 技 | ✅ | DC-008；resolution_error vs hard_error |
| 不定长工具输出怎么处理？ | context engineering / 技 | ✅ | DC-007；budget + preview + attachment pointer |
| 重试上限怎么定？ | 工程经验 / 技 | ⚠️ | 当前已有占位上限；真实 provider 接入后按 timeout / rate limit / incident 语义校准 |

## 5. RAG、Registry 与 Grounding

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| docs RAG 在系统里负责什么？ | RAG 边界 / 技 | ✅ | 只负责官方概念解释和 docs claims，不负责官方性裁决 |
| 官方地址 / bridge / wallet 为什么必须 registry？ | 高风险事实 / 技 + 总 | ✅ | DC-001、DC-006；registry exact lookup |
| unknown URL 如何表达？ | 安全口径 / HR + 技 | ✅ | `../docs/implementation/IMPLEMENTATION_DESIGN.md` §7.2 |
| Evidence Bundle 为什么是唯一事实输入？ | grounding / 技 + 研 | ✅ | `../docs/architecture/ARCHITECTURE.md` §4 / `../docs/implementation/IMPLEMENTATION_DESIGN.md` §6 |
| Grounding Verifier 和 citation 有什么区别？ | faithfulness / 技 + 研 | ✅ | DC-004：typed claims + deterministic exact match |
| LLM-as-judge 能不能用于 verifier？ | 评测方法 / 研 | ✅ | 硬事实不交给 LLM 放行，LLM/NLI 只 advisory |
| route-before-rewrite 为什么重要？ | RAG query rewrite 风险 / 技 | ✅ | DC-009；避免 official address 类问题被 rewrite 污染 |
| 如果 registry 过期怎么办？ | source governance / 总 | ⚠️ | `../docs/operations/registry-ops-plan.md` 已补 proposed owner / SLA / stale behavior；真实 owner 待确认 |

## 6. Chain Adapter 与 Web3 领域

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 为什么 Neo N3 和 Neo X 要双 adapter？ | Web3 领域理解 / 技 | ✅ | Neo N3 application log / VM state 与 EVM receipt / revert reason 语义不同 |
| tx not found 和 RPC 故障怎么区分？ | 工具可靠性 / 技 | ✅ | DC-008；resolution_error vs hard_error |
| Neo X 失败交易怎么分类？ | EVM 诊断 / 技 | ✅ | `../docs/implementation/IMPLEMENTATION_DESIGN.md` §5.2 |
| Neo N3 FAULT 怎么解释？ | Neo N3 诊断 / 技 | ✅ | `../docs/implementation/IMPLEMENTATION_DESIGN.md` §5.1 |
| 是否查询余额 / transfer history？ | 范围 / 技 | ✅ | 只读 address 查询，但必须有预算和 evidence |
| 是否支持 bridge 全链路诊断？ | 范围边界 / 技 | ✅ | `../docs/operations/registry-ops-plan.md`：MVP 只做官方入口 / 合约 exact check / 单链 tx status，不做全链路 bridge indexer |
| 是否需要 sign-message ownership？ | 产品演进 / 总 | ✅ | PRD Phase 4 延后；不请求交易签名、不 approve |
| Neo 官方 RPC / explorer 是谁？ | source owner / 技 | ⚠️ | 已补 official source candidates；生产 provider / ownership 仍需 Neo 内部确认 |

## 7. Safety 与合规

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| seed phrase 输入怎么处理？ | 安全底线 / 技 | ✅ | Ingress Guard pre-log scrub + hard interrupt |
| 投资建议怎么拒答？ | 合规 / HR + 技 | ✅ | `../docs/implementation/IMPLEMENTATION_DESIGN.md` §7.3 |
| 用户要求连接钱包怎么办？ | 动作边界 / 技 | ✅ | Deny Layer；DC-002 |
| 用户被骗 / 转错资产怎么办？ | 高风险用户处理 / HR + 技 | ✅ | 不承诺追回；给安全下一步 + handoff |
| phishing URL denylist 从哪来？ | 安全运营 / 技 | ⚠️ | `../docs/operations/registry-ops-plan.md` 已补 security owner / emergency update 流程；真实 denylist source 待确认 |
| secret 检测 false positive 怎么处理？ | 安全 trade-off / 技 | ✅ | safety wins；让用户去掉 secret 后重述 |
| 多语言 secret / investment 绕过怎么测？ | adversarial eval / 技 | ⚠️ | eval-prototype 已列方向；GAP-1 需语言切分 |

## 8. Evaluation 与 Result

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 没有业务数据，STAR 的 Result 怎么讲？ | 结果诚实度 / HR + 总 | ✅ | `answers/project-star.md`：只能讲设计产出 + prototype eval 计划，不讲业务降本 |
| 怎么把设计变成可量化结果？ | eval 设计 / 技 | ✅ | `../eval/eval-prototype.md`：100 case golden/adversarial/tool/faithfulness |
| 高风险事实可追溯率怎么测？ | metric design / 技 | ✅ | high-risk claim 必须有 source_id；missing evidence case 必须 unknown/handoff |
| secret 拦截率怎么测？ | safety eval / 技 | ✅ | secret hard interrupt suite |
| 投资建议越权率怎么测？ | safety eval / 技 | ✅ | multilingual investment refusal suite |
| fake official link 怎么测？ | adversarial eval / 技 | ✅ | lookalike URL / fake bridge / fake contract case |
| tx 查询成功率怎么测？ | tool eval / 技 | ✅ | runner 已实现并跑通：tool error 分类 5/5、handoff 触发 6/6（`../eval/eval-prototype.md` §9.1） |
| eval 跑了吗？结果多少？ | 真实性 / 技 | ⚠️ | deterministic(mocked) 模式已跑：100/100 结构 check、critical bypass=0；但要诚实说明 mocked 含过拟合风险，真实意图的 `--router llm` 结果待跑（§9.2）；不得把结构指标说成业务通过率 |
| LLM 非确定，你怎么评测才能既可复现又验安全？ | eval 方法论 / 技 + 研 | ✅ | `answers/eval-under-nondeterministic-llm.md`：被 mock 的只有意图，安全层确定性；mock 测机器、真实 LLM 测噪声下安全；五层 + §9.3 诚实口径 |

## 9. Agent 岗位迁移价值

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 这不是产品经理项目吗，为什么适合 agent 开发？ | 岗位匹配 / HR + 技 | ✅ | `answers/project-star.md`：重点讲 harness、tool、policy、verifier、eval |
| 你真正做了哪些 agent engineering 决策？ | 技术贡献 / 技 | ✅ | key decisions + DC-001..DC-009 |
| 你有没有写代码？ | 真实性 / HR + 技 | ✅ | 有可运行的 deterministic eval harness（`../prototype/eval_runner/`：rule router / policy gate / query path / fixture provider / typed-claim compiler / grounding verifier / metrics）。诚实边界：端到端服务和真实链上 adapter 仍是契约 |
| 如果让你落地，第一周做什么？ | 执行能力 / 技 | ✅ | `../docs/implementation/implementation-plan.md` “Week-1 Build Plan”：schema、guard、policy、fixture provider、verifier、100-case runner |
| 这个项目和普通 RAG 最大区别？ | 核心洞察 / 技 | ✅ | RAG 是解释源，不是官方事实源；事实进入 registry / tool / evidence |
| 如果面试官只给你 2 分钟讲？ | 表达能力 / HR | ✅ | `answers/project-star.md` “面试 30 秒版本” + STAR 版本 A |

---

## GAP 优先级清单

### P0：为了 agent 开发岗位必须补

| GAP # | 内容 | 状态 / 落地位置 |
|---|---|---|
| GAP-9 | 实现并跑 100-case eval，得到 prototype 指标 | **部分完成**：deterministic runner 已实现（`../prototype/eval_runner/`）并在 mocked oracle 模式跑通 100/100，critical bypass=0；结果在 `../eval/eval-prototype.md` §9.1。**剩**：`--router llm` 真实意图模式（验 critical_bypass 仍为 0）→ §9.2 |
| 工程代码证据 | 是否有可运行代码 | **部分完成**：已有可运行 eval harness（rule router / policy gate / query path / fixture provider / typed-claim compiler / grounding verifier / metrics，约 6 个模块）。**剩**：端到端 Chat API service + 真实链上 adapter 仍是契约 |

### P1：面试深问常见，但可以先讲设计

| GAP # | 内容 | 落地位置 |
|---|---|---|
| GAP-1 | 多语言 MVP 和多语言 adversarial eval 切分 | `../docs/product/PRD.md` / `../eval/eval-prototype.md` |
| GAP-3 | timeout / retry / output budget 数值如何从真实 provider 校准 | 接真实 provider 后更新 `../docs/implementation/IMPLEMENTATION_DESIGN.md` |
| GAP-4 | proposed owner / SLA 已补，真实 Neo owner 未确认 | `../docs/operations/registry-ops-plan.md` |
| GAP-7 | security owner / emergency update 流程已补，真实 denylist source 未确认 | `../docs/operations/registry-ops-plan.md` |

### P2：可以诚实承认待确认

| GAP # | 内容 | 兜底口径 |
|---|---|---|
| GAP-6 | official source candidates 已补，但 production provider 未确认 | “这是上线门槛，不能用未经确认 provider 冒充生产 source。” |
| 工程实现代码 | 当前无代码证据 | “现阶段留存的是产品与实现契约设计，不包装成已实现服务。” |
| 业务降本数据 | 当前没有 | “没有客服时间下降或 CSAT 数据，不写入结果。” |

## 维护规则

1. 每次 mock / 正式面试遇到新问题，追加一行。
2. 如果问题暴露项目设计不足，回写 PRD / ARCHITECTURE / IMPLEMENTATION_DESIGN。
3. 如果问题只是表达不足，补 `answers/project-star.md` 或对应单题深答。
4. 如果问题需要量化证据，优先补 eval-prototype，而不是虚构业务结果。
