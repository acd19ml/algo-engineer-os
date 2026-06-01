# Neo 官网智能客服 · 项目入口

> 本文件是入口和路由表，不是完整 PRD、不是架构设计、不是面试稿。读者应该能从这里判断：想看某类问题，应该打开哪份文档。

## 业务问题

Neo 官网原来没有独立客服入口，用户支持主要依赖 Discord 社区和全球开发者维护。这个模式能处理复杂社区问题，但对官网入口存在三个业务问题：

1. 重复问题无法产品化：Neo / Neo N3 / Neo X / NEO / GAS / wallet / explorer / bridge 等基础问题长期重复出现。
2. 问题类型混杂：一个用户输入可能同时包含官方链接校验、交易哈希、交易所提现、钱包展示异常、可疑链接和投资建议。
3. 错误背书成本高：官方地址、合约、bridge、钱包下载入口、交易状态一旦答错，可能造成资金损失或错误信任。

所以项目本身要解决的问题是：

> 为 Neo 官网设计一个可安全承接官方解释、官方导航、只读链上诊断、安全拦截和人工升级摘要的支持入口。

`policy-constrained support orchestrator` 是技术方案结论，不是业务问题本身。业务问题的 source of truth 在 [`docs/product/PRD.md`](./docs/product/PRD.md)，技术方案的 source of truth 在 [`docs/decision/TECH_PROPOSAL.md`](./docs/decision/TECH_PROPOSAL.md) / [`docs/architecture/ARCHITECTURE.md`](./docs/architecture/ARCHITECTURE.md) / [`docs/implementation/IMPLEMENTATION_DESIGN.md`](./docs/implementation/IMPLEMENTATION_DESIGN.md)。

## 当前事实

| 项 | 事实 |
|---|---|
| 时间 | 2025.02-2025.07 |
| 公司 / 组织 | Neo 智能经济 |
| 项目形态 | Neo official website support bot / 官网智能客服方案 |
| 我的角色 | 产品方案一人负责；当前留存材料主要是产品、技术方案、架构和实现设计 |
| 当前状态 | `in-progress`：方案与评测 cases 已整理，未运行 prototype runner，未声称上线 |
| 诚实边界 | 无客服时间下降、CSAT、真实转人工率等业务结果；不能声称已上线或已产生业务降本 |

## 目录分层

根目录只保留入口和机器索引。其它内容按职责进入子目录：

| 目录 | 放什么 | 不放什么 | 未来扩展 |
|---|---|---|---|
| [`docs/`](./docs/) | PRD、技术提案、架构、实现设计、运维计划、设计承诺 | eval cases、runner 代码、面试稿 | source governance、API plan、implementation decision record |
| [`eval/`](./eval/) | eval 方案、100 cases、fixtures、runner spec、未来结果表 | 生产代码、面试表达 | eval results、failure reports、case generation notes |
| [`prototype/`](./prototype/) | 最小可运行 prototype、deterministic runner、未来 schema / services | 业务叙事和 STAR | `eval-runner/`、`schemas/`、`service/`、`fixtures-adapter/` |
| [`interview/`](./interview/) | 面试防御矩阵、STAR、单题深答 | 项目事实源 | 更多高频问题、mock 复盘 |

## 文档架构

这套目录按四个 methodology 约束组织：

- `three-tier-decision-docs`：方向、结构、落地分层，避免混成一份“大设计文档”。
- `ai-product-decision-four-questions`：每个 AI 决策必须能回答场景判断、风险意识、标准感、边界感。
- `architecture-design-six-steps`：先产品定位和原型 / API / 数据，再模块拆分和详细设计。
- `answer-form-for-mechanisms`：面试回答必须从问题和反事实推导设计，不只复述名词。

### 真值层

| 文档 | 负责什么 | 不负责什么 | 什么时候看 |
|---|---|---|---|
| [`README.md`](./README.md) | 项目入口、文档地图、当前事实、阅读路由 | 不新增产品范围、技术决策或面试结论 | 不知道从哪开始时 |
| [`meta.yaml`](./meta.yaml) | 机器可读 metadata、artifact 清单、source priority | 不承载叙事和论证 | 同步索引 / registry 时 |
| [`docs/product/PRD.md`](./docs/product/PRD.md) | 用户、业务问题、产品范围、非目标、成功指标、上线阶段、业务 open questions | 不定义 API、schema、工具契约、模块实现 | 想看“做什么 / 不做什么 / 为什么对用户有用” |
| [`docs/decision/TECH_PROPOSAL.md`](./docs/decision/TECH_PROPOSAL.md) | 该不该做、为什么不是 Discord-only / FAQ / 泛 RAG / 开放 ReAct / 纯人工 | 不维护组件图、字段、schema、runner | 想看“为什么这样做而不是别的方案” |
| [`docs/architecture/ARCHITECTURE.md`](./docs/architecture/ARCHITECTURE.md) | 系统由哪些组件组成、组件边界、数据资产、部署视图、模块拆分 | 不维护字段级 schema、具体 adapter 输入输出、eval case | 想看“系统整体怎么组织” |
| [`docs/implementation/IMPLEMENTATION_DESIGN.md`](./docs/implementation/IMPLEMENTATION_DESIGN.md) | runtime pipeline、intent / entity / policy、registry schema、tool contract、evidence、answer compiler、eval checks、MVP backlog | 不重新论证该不该做，不定义业务目标 | 想看“如果开发，接口和规则怎么落地” |
| [`docs/implementation/implementation-plan.md`](./docs/implementation/implementation-plan.md) | 技术栈、Chat API v0、Admin API v0、Eval Job v0、week-1 build plan | 不改变产品范围，不声称已实现 | 想看“如果明天开工，怎么开发” |
| [`docs/operations/registry-ops-plan.md`](./docs/operations/registry-ops-plan.md) | registry 分层、owner / reviewer / SLA、官方 source candidates、provider policy、bridge 边界 | 不把 candidate source 升级成生产事实 | 想看“官方 source 怎么治理” |
| [`docs/design/commitments.md`](./docs/design/commitments.md) | 项目采纳的不可违反设计不变量和校验方式 | 不做 PRD / 架构 / 实现设计的替代品 | 想看“哪些结构性底线不能被实现破坏” |

### 验证层

| 文档 | 负责什么 | 不负责什么 | 什么时候看 |
|---|---|---|---|
| [`eval/eval-prototype.md`](./eval/eval-prototype.md) | prototype eval 目标、metrics、suite、runner shape、未运行前后 STAR 口径 | 不声称业务结果，不替代真实 runner 输出 | 想看“怎么证明方案能工作” |
| [`eval/eval-cases.yaml`](./eval/eval-cases.yaml) | 100 条 golden / adversarial / tool / boundary case fixtures | 不代表真实用户日志，不代表 Neo 官方 source | 写 runner / 检查覆盖面时 |
| [`eval/eval-fixtures.yaml`](./eval/eval-fixtures.yaml) | registry / docs / tool fixture bodies | 不代表生产 registry，不代表真实用户日志 | 接 deterministic runner 时 |
| [`eval/eval-runner-spec.md`](./eval/eval-runner-spec.md) | runner modes、fixture provider contract、checks、metrics | 不代表已运行结果 | 实现 eval runner 前 |

### 派生层

| 文档 | 负责什么 | 不负责什么 | 什么时候看 |
|---|---|---|---|
| [`interview/interview-defense-matrix.md`](./interview/interview-defense-matrix.md) | 面试挑战 catalog、readiness、GAP 追踪 | 不产生项目事实，不替代 source docs | 准备面试或 mock 后补缺口 |
| [`interview/answers/`](./interview/answers/) | 单题深答、金句、追问防守 | 不产生项目事实；必须引用真值层 | 面试前复习某个高频问题 |
| [`interview/answers/project-star.md`](./interview/answers/project-star.md) | STAR、简历素材、诚实边界 | 不定义产品和技术方案 | 需要把项目转成求职表达时 |
| [`interview/answers/similar-tool-routing.md`](./interview/answers/similar-tool-routing.md) | “相似工具如何正确调用”的单题深答 | 不替代 implementation design 和 eval runner | 被问 tool routing 时 |
| [`interview/answers/eval-under-nondeterministic-llm.md`](./interview/answers/eval-under-nondeterministic-llm.md) | “LLM 非确定怎么评测：mock vs 真实 LLM”的单题深答（五层框架） | 不替代 eval-prototype 的真实结果 | 被问 eval 方法论 / mock 是否有意义时 |

## 阅读路由

| 你想回答的问题 | 先看 | 再看 |
|---|---|---|
| 这个项目解决什么业务问题？ | [`docs/product/PRD.md`](./docs/product/PRD.md) | 本 README “业务问题” |
| 为什么不能继续只靠 Discord 社区？ | [`docs/decision/TECH_PROPOSAL.md`](./docs/decision/TECH_PROPOSAL.md) | [`docs/product/PRD.md`](./docs/product/PRD.md) |
| 为什么不是 FAQ / 泛 RAG / 开放 ReAct？ | [`docs/decision/TECH_PROPOSAL.md`](./docs/decision/TECH_PROPOSAL.md) | [`docs/design/commitments.md`](./docs/design/commitments.md) |
| 系统有哪些模块？ | [`docs/architecture/ARCHITECTURE.md`](./docs/architecture/ARCHITECTURE.md) | [`docs/implementation/IMPLEMENTATION_DESIGN.md`](./docs/implementation/IMPLEMENTATION_DESIGN.md) |
| 两个相似工具怎么避免误调？ | [`interview/answers/similar-tool-routing.md`](./interview/answers/similar-tool-routing.md) | [`docs/implementation/IMPLEMENTATION_DESIGN.md`](./docs/implementation/IMPLEMENTATION_DESIGN.md) §1 / §3 |
| 高风险事实如何防幻觉？ | [`docs/design/commitments.md`](./docs/design/commitments.md) DC-001 / DC-004 / DC-006 | [`docs/implementation/IMPLEMENTATION_DESIGN.md`](./docs/implementation/IMPLEMENTATION_DESIGN.md) |
| secret / 投资建议 / 写链请求怎么处理？ | [`docs/product/PRD.md`](./docs/product/PRD.md) §7 | [`docs/implementation/IMPLEMENTATION_DESIGN.md`](./docs/implementation/IMPLEMENTATION_DESIGN.md) §3 / §8 |
| Neo N3 和 Neo X 为什么双 adapter？ | [`docs/decision/TECH_PROPOSAL.md`](./docs/decision/TECH_PROPOSAL.md) | [`docs/architecture/ARCHITECTURE.md`](./docs/architecture/ARCHITECTURE.md) / [`docs/implementation/IMPLEMENTATION_DESIGN.md`](./docs/implementation/IMPLEMENTATION_DESIGN.md) |
| 如果今天要实现，API 和技术栈是什么？ | [`docs/implementation/implementation-plan.md`](./docs/implementation/implementation-plan.md) | [`docs/implementation/IMPLEMENTATION_DESIGN.md`](./docs/implementation/IMPLEMENTATION_DESIGN.md) |
| Registry owner / provider / bridge 边界怎么定？ | [`docs/operations/registry-ops-plan.md`](./docs/operations/registry-ops-plan.md) | [`docs/architecture/ARCHITECTURE.md`](./docs/architecture/ARCHITECTURE.md) §5 / §11 |
| 怎么评测这个方案？ | [`eval/eval-prototype.md`](./eval/eval-prototype.md) | [`eval/eval-cases.yaml`](./eval/eval-cases.yaml) / [`eval/eval-fixtures.yaml`](./eval/eval-fixtures.yaml) / [`eval/eval-runner-spec.md`](./eval/eval-runner-spec.md) |
| LLM 非确定，为什么用 mock 跑、指标说明什么？ | [`interview/answers/eval-under-nondeterministic-llm.md`](./interview/answers/eval-under-nondeterministic-llm.md) | [`eval/eval-prototype.md`](./eval/eval-prototype.md) §9 / [`prototype/eval_runner/`](./prototype/eval_runner/) |
| 面试怎么讲？ | [`interview/answers/project-star.md`](./interview/answers/project-star.md) | [`interview/interview-defense-matrix.md`](./interview/interview-defense-matrix.md) |

## Source Of Truth 顺序

当文档冲突时按下面顺序处理：

1. 项目事实：本 README “当前事实” + [`meta.yaml`](./meta.yaml)。
2. 产品范围 / 业务目标 / 上线阶段：[`docs/product/PRD.md`](./docs/product/PRD.md)。
3. 方向取舍：[`docs/decision/TECH_PROPOSAL.md`](./docs/decision/TECH_PROPOSAL.md)。
4. 组件边界 / 数据资产 / 部署：[`docs/architecture/ARCHITECTURE.md`](./docs/architecture/ARCHITECTURE.md)。
5. 字段 / schema / policy / tool / evidence / eval checks：[`docs/implementation/IMPLEMENTATION_DESIGN.md`](./docs/implementation/IMPLEMENTATION_DESIGN.md)。
6. 不变量和校验：[`docs/design/commitments.md`](./docs/design/commitments.md)。
7. 评测状态：[`eval/eval-prototype.md`](./eval/eval-prototype.md) + [`eval/eval-cases.yaml`](./eval/eval-cases.yaml) + [`eval/eval-fixtures.yaml`](./eval/eval-fixtures.yaml) + [`eval/eval-runner-spec.md`](./eval/eval-runner-spec.md)。
8. 决策链复盘：[`eval/decision-trail-full.md`](./eval/decision-trail-full.md)（M0-M13 全周期）+ [`eval/decision-trail-d5-hardening.md`](./eval/decision-trail-d5-hardening.md)（D5 硬化），只作为派生分析，不覆盖以上任何文档。
9. 面试表达：`interview/interview-defense-matrix.md` / `interview/answers/*`，只作为派生表达，不覆盖以上任何文档。

## 当前最重要缺口

| 缺口 | 为什么重要 | 落地位置 |
|---|---|---|
| 真实 Neo owner / production provider 未确认 | 不能把 candidate source 写成生产事实源 | [`docs/operations/registry-ops-plan.md`](./docs/operations/registry-ops-plan.md) |
| Eval runner LLM 模式 | deterministic runner 已实现；`--router llm` 四档横扫(Qwen2.5 7/14/32/72B) + T1 留出集已完成：critical_bypass=0 跨全档成立，14B+ 98/100，heldout_t1 7/7 | [`eval/eval-prototype.md`](./eval/eval-prototype.md) §9.2 |
| Registry production storage / retention 未最终确定 | 影响 attachment、tx/address、conversation、handoff 存储 | [`docs/operations/registry-ops-plan.md`](./docs/operations/registry-ops-plan.md) |
| 端到端服务代码尚未实现 | 已有可运行 eval harness（`prototype/eval_runner/`），但 Chat API / 真实链上 adapter 仍是契约，不是可运行客服系统 | [`docs/implementation/implementation-plan.md`](./docs/implementation/implementation-plan.md) |
| 多语言完整评测未展开 | 当前只有部分 investment / secret adversarial 多语言样例 | [`eval/eval-prototype.md`](./eval/eval-prototype.md) |

## 当前状态

`in-progress`

已完成：产品边界、技术提案、架构、实现设计、implementation plan、registry ops plan、design commitments、100 条 eval cases、eval fixtures、runner spec、面试防御矩阵和单题深答；**可运行的 deterministic eval runner（[`prototype/eval_runner/`](./prototype/eval_runner/)）并在 mocked oracle 模式下跑通 100 条 case**；**LLM router 四档横扫(Qwen2.5 7/14/32/72B) + T1 留出集已完成**：critical_bypass=0 跨全档成立，14B+ 98/100(main)、7/7(heldout_t1)——见 [`eval/eval-prototype.md`](./eval/eval-prototype.md) §9 与 [`eval/results/`](./eval/results/)。

未完成：真实 provider / source owner 生产确认、端到端服务代码（Chat API + 真实链上 adapter）、LLM 自由文本 answer compiler 的 `full_prototype` verifier 压测、D5 短语检测硬化、版本阶梯消融、上线或业务结果。

诚实口径：mocked 模式不代表真实 router 准确率（deny/boundary 启发式对着这 100 条写，含轻度过拟合）；prototype 指标不是业务 KPI，不写成客服降本。
