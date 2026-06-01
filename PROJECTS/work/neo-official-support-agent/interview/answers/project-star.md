# Neo 官网智能客服 · STAR / 简历素材

> 本文件是派生表达层，只用于求职和面试。不产生项目事实；若与 `../../docs/product/PRD.md`、`../../docs/decision/TECH_PROPOSAL.md`、`../../docs/architecture/ARCHITECTURE.md`、`../../docs/implementation/IMPLEMENTATION_DESIGN.md` 冲突，以真值层文档为准。

## 诚实边界

- 项目时间：2025.02-2025.07。我的角色：产品方案一人负责。
- **已完成**（M0-M8）：PRD → 技术方向 → 安全架构 → 系统架构 → 实现契约 → 工程计划 → Eval 体系 → 运行验证 → 方法论提取。prototype eval：mocked oracle 100/100，LLM router 四档横扫 critical_bypass=0 跨全档，14B+ 98/100（main）、7/7（T1 留出集）。
- **已设计未执行**（M9-M13）：生产部署、Runtime 可观测性、事故响应、持续 Eval、持续改进闭环——架构上已预留模块化边界和可观测性接口，等待 Neo 内部 owner 确认后推进。
- 当前不能声称官网客服已上线、客服时间降低、CSAT 提升、转人工率下降等业务结果。

---

## STAR 版本 A：从需求到生产全周期的工业级 Agent 架构

**Situation**

Neo 官网没有独立客服入口，用户支持依赖 Discord 社区。用户问题混合官方概念解释、Neo N3 / Neo X 链上状态查询、可疑链接校验、钱包/交易所边界和投资建议——错误回答不是体验问题，是资金安全问题。

**Task**

一人负责从零设计官网智能客服方案。不只是「做一个能回答问题的 bot」，而是设计一个从需求分析到生产部署、从安全架构到持续改进的完整系统——每个阶段有明确的交付物和自检标准。

**Action**

全周期分四个阶段、14 个 Milestone：

**设计阶段（M0-M5）**：从「这是不是 RAG 能解决的」开始——分析 Neo 场景的特殊性（官方地址/bridge/合约/tx status 不能靠向量相似度判断），拒绝泛 RAG 和开放 ReAct，收敛为 Policy-constrained support orchestrator。安全架构四层：动作空间=全部只读（让危险操作从能力层面不存在）→ Deny Layer（secret/投资/写链在 LLM 前拦截）→ Allow Matrix（intent → 工具子集，deny 覆盖 allow）→ Grounding Verifier（claims vs evidence 逐条对照，硬事实 exact match 裁决，异常 fail closed）。工程决策：Neo N3 / Neo X 双 adapter（UTXO 和 EVM 语义不同不合并在一个工具）、Pydantic v2 单一 schema 源（防止手写 schema 和运行时校验漂移）、9 条 design commitments 作为可校验的安全不变量。部署接口预留模块化边界，eval 体系在 service 代码之前建立。

**验证阶段（M6-M7）**：100 条 eval cases、8 个任务语义指标，基于执行轨迹而非最终答案。先 mocked oracle 验证确定性层，再 Qwen2.5 四档（7/14/32/72B）横扫验证安全不变量与 router 能力无关。critical_bypass=0 跨全档——连 policy_resolution 崩到 0.27 的 7B 也是 0 bypass。T1 留出集 7/7 验证修复不是过拟合。从验证结果中提取了 9 条可迁移原则和 Detection Hardening Loop playbook。

**生产阶段（M9-M11，已设计）**：生产部署以 PRD §10 的 7 条上线门槛为 gate。Runtime 可观测性采用 AgentOps 内置设计——Append-only Log + KV Cache 优化 + TLA dashboard（DC-001~DC-009 实时违反率），不等部署后外挂补丁。事故响应：Kill switch（per intent/network/adapter）、事故模板（RPC/Explorer/Bridge/Docs 故障）、rollback + 回放机制、post-incident eval 流程。

**持续改进阶段（M12-M13，已设计）**：生产 trace 采样 → 人工标注 → heldout 扩充 → regression 检测，形成 eval 集随生产增长的闭环。模型升级→四档横扫→对比历史 baseline，判断哪些 Harness 组件可移除。事故复盘 → DC 修订，生产 pattern → playbook 更新。

**Result**

已完成 M0-M8：PRD、技术提案、架构设计、实现设计、implementation plan、registry ops plan、9 条 design commitments、可运行 eval harness、100 条 eval cases。Mocked oracle 100/100；LLM router 四档横扫 critical_bypass=0 跨全档。M9-M13 已设计，架构层面预留了模块化边界和可观测性接口。当前未上线，无业务降本数据。

---

## STAR 版本 B：关键架构取舍的深度论证

### B1 · 为什么不是 RAG

RAG 的核心假设：语义最相似的文档段落 ≈ 正确答案。这个假设在 Neo 场景下不成立——「最相似的文档段落」≠「正确的官方地址」。官方地址、bridge 合约、tx status 需要 exact match，不能靠向量相似度。

**选择**：高风险事实走 registry exact lookup（确定性），解释性内容走 docs retriever（RAG 只用于低风险路径）。

### B2 · 为什么双 adapter 不合并在一个工具

直觉：Neo N3 和 Neo X 都是查链上状态，做成一个统一链工具更简洁。但 N3（UTXO 风格，application log / VM state FAULT）和 Neo X（EVM 风格，receipt / revert reason）的失败诊断语义完全不同。如果统一成一个工具，模型需要自己区分两种链的语义——增加认知负荷和出错概率。

**选择**：各一个专用 adapter。和「万能工具要主动让位」同一原则——专用工具把操作限制在可控范围内。

### B3 · 为什么 verifier 不看 compiler 的自我解释

compiler 可以在文字里写「以上事实均来自官方 registry」，verifier 看到可能被误导放行。切断「被审查者操纵审查者」的路径——verifier 只看 claims + evidence，不看 compiler 的自我辩护。

**选择**：verifier 输入只有 claims 和 evidence_bundle。和 YOLO Classifier「评审者不看 agent 的文字回复」完全一致。

### B4 · 为什么 Policy Gate 两层裁决不用单表

单表加 `decision: deny|allow` 列的「deny 优先」只是约定——有人把 critical intent 误填 allow，表不拦。拆成 Deny Layer（保安，先跑）+ Allow Matrix（菜单，后查），结构上让 critical 永不为 allow。

**选择**：两层裁决。安全靠结构，不靠约定。

### B5 · 为什么 Eval 在 Service 之前建

传统做法是先上线再监控。但 Web3 客服的上线成本不是「答错了再修」——第一次答错官方地址就可能是资金损失。eval harness 和 runtime pipeline 共享同一套代码路径（eval = runtime 离线执行模式），保证了「eval 通过的 = 生产也会通过的」。

**选择**：Eval 先行，AgentOps 内置，不等到部署后外挂补丁。

---

## 简历素材

> 只能在你愿意把「设计 / 方案 / prototype」写进简历时使用；如果目标公司只认可已上线工程结果，应弱化或不写。

- 负责 Neo 官网智能客服全周期产品与技术方案设计（14 个 Milestone，从需求分析到持续改进闭环），将依赖 Discord 社区的支持流程收敛为面向官网入口的安全方案。
- 设计高风险 Web3 support agent 的四层安全架构：动作空间=全部只读、Deny Layer + Allow Matrix 两层裁决、Grounding Verifier（claims vs evidence 逐条对照，硬事实 exact match 裁决）。
- 工程决策：Neo N3 / Neo X 双 adapter（UTXO 和 EVM 语义不同不合并在一个工具）、Pydantic v2 单一 schema 源、9 条 design commitments 作为可校验安全不变量。
- 设计 100 条 eval cases + 8 个任务语义指标，基于执行轨迹评估。Qwen2.5 四档模型横扫验证安全不变量与 router 能力无关（critical_bypass=0 跨全档）。
- 生产阶段设计：Runtime 可观测性（AgentOps 内置，不等外挂补丁）、事故响应（Kill switch + 事故模板 + rollback）、持续 Eval（production trace → heldout 扩充 → regression）、持续改进闭环（模型升级横扫 → DC 修订 → playbook 更新）。

---

## 面试 30 秒版本

> Neo 官网原来没有独立客服，主要依赖 Discord 和全球开发者维护。我负责设计官网智能客服方案时，发现它不是普通 RAG 问答——官方地址、bridge、合约、交易状态和投资建议都属于高风险事实，RAG 答错是体验问题，这里答错是资金损失。核心设计是把 LLM 限制在理解、路由和表达，把事实判断和动作授权下沉到 registry、只读链上工具、policy gate 和 grounding verifier——确定性层裁决安全，LLM 只做语义。四档模型横扫验证安全不变量与 router 能力无关，critical_bypass=0 跨全档。架构从 day-1 就预留了生产可观测性、事故响应和持续改进的接口。当前未上线，无业务降本数据。

## 面试 3 分钟版本

> Neo 官网原来没有独立客服，用户支持依赖 Discord 社区。我一人负责官网智能客服的全周期方案设计——从需求分析到生产部署的持续改进闭环，14 个 Milestone。

> 第一件事是判断这到底是不是 RAG 能解决的。Neo 场景里用户问「这个地址是不是官方的」「这笔交易成功了吗」「这个 bridge 能用吗」——RAG 的核心假设是「最相似的文档段落 ≈ 正确答案」，但这个假设在官方地址、合约、交易状态上不成立。最相似的文档段落不等于正确的官方地址。所以方案拒绝泛 RAG 和开放 ReAct，收敛为 Policy-constrained support orchestrator——LLM 只做理解、路由和表达，事实判断和动作授权全部下沉到确定性层。

> 安全架构四层。第一层动作空间=全部只读——没有签名、转账、钱包连接能力，让危险操作从能力层面就不存在。这比任何 deny 规则都可靠——规则可能被绕过，能力的缺失不可能被绕过。第二层 Deny Layer，secret、投资建议、写链请求在 LLM 之前拦截。第三层 Allow Matrix，每个 intent 对应允许的工具子集，deny 永远覆盖 allow。第四层 Grounding Verifier，高风险回答的 claims 和 evidence bundle 逐条对照，硬事实 exact match 裁决，异常 fail closed。verifier 只看 claims 和 evidence，不看 compiler 自己的文字解释——切断被审查者操纵审查者的路径。

> 工程上几个关键取舍。Neo N3 和 Neo X 做了双 adapter 不合并在一个工具里——UTXO 和 EVM 的失败诊断语义完全不同，统一工具会增加模型的认知负荷。Pydantic v2 做单一 schema 源，`.model_json_schema()` 生成 JSON Schema 喂 LLM，运行时校验即同一个 model——防止手写 schema 和运行时校验漂移。9 条 design commitments 作为可校验的安全不变量。

> 验证上，100 条 eval cases、8 个任务语义指标，全部基于执行轨迹而不是最终答案——检查 decision、answer_mode、tools、evidence、claims 每个节点。先 mocked oracle 验证确定性层 100/100，再 Qwen2.5 四档横扫验证核心假设：安全不变量到底跟 router 能力有没有关系？结果 critical_bypass=0 跨全档成立——连 policy_resolution 崩到 27% 的 7B 模型也是 0 bypass。T1 留出集 7/7 验证修复不是过拟合。

> 生产阶段虽然没执行但架构上预留了：Runtime 可观测性采用 AgentOps 内置设计——不等部署后外挂补丁；事故响应的 Kill switch 和 rollback 机制；持续 Eval 的 production trace → heldout 扩充 → regression 闭环；持续改进的模型升级横扫 → DC 修订 → playbook 更新。当前未上线，没有业务降本数据。
