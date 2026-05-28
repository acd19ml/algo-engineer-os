# 李勐霄

**联系方式**：13212815337 | [acd19ml@gmail.com](mailto:acd19ml@gmail.com)
**其他信息**：24 岁 | [Github](https://github.com/acd19ml?tab=repositories)

---

## 教育背景

**香港城市大学**，人工智能，*硕士* | 2025.09 - 2027.06

- **主修课程**：生成式人工智能、动态规划与强化学习、自然语言处理、机器学习算法与应用

**谢菲尔德大学**，计算机科学，*本科* | 2021.09 - 2024.06

- **主修课程**：高级算法、软件全栈开发、网络安全团队项目、智能网、数据驱动计算、系统设计与安全等

**比赛奖项**：七牛云第三届 1024 创作节优胜奖

---

## 项目经历

**Agent Memory 自主研究项目** | 2026.01 - 2026.05
**硕士在读期间个人研究**

- **主流 Web Agent Memory 框架的复现与审计**（AWM @ Mind2Web）：通过 step-level paired 配对实验对照 baseline vs workflow，**发现 workflow 影响窗口仅 6-18% 且正/负向站点的干预模式反向**；归类正负机制（strategy redirection / domain misdirection / step skipping 等），定位"抽象不等于更好执行"边界，建立 paired-case 评测方法学。
- **记忆跨任务复用机制实验**（HotpotQA → 2WikiMultiHopQA 近迁移）：在固定经验预算 + matched/mismatched 配对下测试三种记忆形态（None / Episodic / Consolidated），**受控对比证明仅匹配路径在两次修复（源任务重路由 + 算子可执行化）后恢复、不匹配控制组保持不变**，定位"可执行性"是跨任务复用的关键边界。

---

## 实习经历

**七牛云** | 2025.07 - 2025.10
**AI 算法工程师 / 项目组长** | 上海

- 作为项目组长协调前后端、运维、算法 6 名同学，负责 AI 运维项目从产品定位、原型设计、API / 数据表设计到模块拆分与联调推进；经历三次产品形态调整后收敛 MVP，并沉淀技术提案 / 架构设计 / 实现设计决策文档。
- 设计并实现 “指标下钻分析” AI 子系统：基于 Langchain, Langgraph 的三层多智能体架构 — 任务规划 “运维专家” + 日志 / 指标 / 链路三个专门数据 agent + 不主动获取数据的分析决策 “值班长” + 最终输出 “运维专家” 5 个角色 agent，按角色选模型；通过 MCP Server 标准化封装日志 / 指标 / 链路 / CMDB 拓扑工具，使大模型按需动态查询多源运维数据。
- 针对多智能体 ReAct 模式的延迟高 / token 爆炸 / 循环不终止三个痛点做工程优化（上下文压缩与精准引用 + 智能终止判断 + 显式总结工具 + 减少无效循环），**Mock 系统 demo 上根因定位成功率从 20% 迭代提升到约 70%**。
- 设计**运行体检中心**：通过时序异常检测主动巡检全量指标，**把根因分析的触发入口从"告警驱动"扩展为"告警 + 主动巡检"双路径**；在多版本灰度发布场景下进一步设计数据中间层，实现"同一服务不同版本"动态阈值调整机制，使问题先于阈值告警被识别。

**Neo 智能经济** | 2025.02 - 2025.07
**AI Agent 开发工程师** | 上海

- 基于 LangChain / LangGraph 构建 LLM 多智能体 DeepResearch 服务，设计 coordinator / planner / researcher / coder / reporter / human feedback 等状态节点，将复杂研究任务拆解为背景调研、任务规划、网页搜索、数据抓取、代码执行分析与报告生成链路；通过图式编排隔离规划、执行、反馈与汇报职责，提升长链路 research workflow 的可控性与可调试性。
- 设计 ReAct 区块链问答 Agent 的双路 RAG 路由：基于 FAISS 召回技术文档证据，基于 Pinecone + OpenAI
text-embedding-3-large 索引 62 种 API / 工具 schema，形成 Top10 召回 → Top5 精排的候选上下文选择流程；相
较全量文档 / 工具 prompt 注入，达成 98% 工具意图匹配准确率并降低 70% 调用成本。
- 参与设计与开发开源 AI Agent 框架 SDK（**260+ stars**）及配套工具集 SDK：集成同步 / 异步执行、Graph、链上对象存储工具、钱包加密工具，编写测试用例保障可用性。**维护项目海外全球技术社区**：处理 GitHub Issues、Review 海外开发者 PR、撰写并维护开发者文档，与海外开发者协作推进项目演进。

---

## 技能

- **大模型与 Agent**：熟悉 Transformer / Attention 机制（QKV / Multi-Head / KV Cache）、ReAct / Plan-RePlan / SubAgent / Workflow / MCP / A2A 等 Agent 范式；熟悉 Context Engineering / Harness Engineering 工程实践；熟练运用 LangChain / LangGraph 等智能体框架。
- **训练与微调**：熟悉 PPO / DPO / GRPO / DAPO 强化学习算法及其演进谱系；熟练运用 LoRA / QLoRA 高效参数微调；理解 SFT / RLHF / RLAIF 后训练流程及能力激活关系。
- **检索与记忆**：熟悉 RAG 系统设计，熟练运用向量数据库（Pinecone）、嵌入模型与高效检索策略；理解 procedural / episodic memory 的设计权衡。
- **数据库与中间件**：熟练 MongoDB / MySQL / Postgres，以及 Redis。
- **工程**：熟练 Python，具备 Go 语言基础；熟练 Gin、gRPC、微服务架构，及面向对象 / 接口 / IoC 设计原则；熟练 GitHub 工程化协作，具备测试驱动开发经验；熟练 PRD 编写、MVP 模块拆分与架构设计。

