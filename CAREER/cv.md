# 李勐霄

**联系方式**：13212815337 | [acd19ml@gmail.com](mailto:acd19ml@gmail.com)
**其他信息**：23 岁 | [Github](https://github.com/acd19ml?tab=repositories)

---

## 教育背景

**香港城市大学**，人工智能，*硕士* | 2025.08 - 2026.08

- **主修课程**：生成式人工智能、动态规划与强化学习、自然语言处理、机器学习算法与应用

**谢菲尔德大学**，计算机科学，*本科* | 2021.09 - 2024.06

- **主修课程**：高级算法、软件全栈开发、网络安全团队项目、智能网、数据驱动计算、系统设计与安全等

**比赛奖项**：七牛云第三届 1024 创作节优胜奖

**参与比赛**：阿里云智能 Agent 创新大赛、ThinkInAI MCP 挑战赛 Hackathon、Global AI Conference & Hackathon Tokyo

---

## 项目经历

**Coding Agent + Procedural Memory 全链路开源研究项目** | 2026.05 - 至今 *进行中*
**自主项目** | 开源仓库

- 基于开源 Claude Code 实现扩展 procedural memory 模块，在 SWE-bench-Lite 上设计 matched / mismatched issue 配对评测，验证记忆抽象的可执行性如何决定跨任务复用边界。
- **全链路实现**：业务定义 → 多智能体架构（Supervisor + Sub-Agents + Memory Pool）→ trajectory 数据生产与蒸馏 → Qwen 2.5-7B + LoRA SFT 训练 → GRPO 策略学习 → matched/mismatched 评测体系 → vLLM 部署。
- **评测设计**：构建 matched / mismatched issue 配对评测框架，包含四类指标：(i) 加 memory 模块前后整体 pass@1 / pass@k 对比；(ii) 按 issue 类型分桶（bug fix / feature add / refactor）的成功率影响；(iii) matched / mismatched 配对上的增益比值，量化 memory 模块的 selective 程度；(iv) 对 memory 引入错误的案例做归类，建立可回归的失败模式检测集。
- **横向对比研究**：对 Claude Code（开源 fork）/ OpenClaw / Hermes-Agent 三个主流 agent harness 在记忆机制 / 工具调用 / 上下文管理 / 错误恢复 / 反馈回路五个维度做对比分析，并将 procedural memory 思想拓展到运维诊断场景做思想实验，输出开源研究报告。

**Agent Memory 自主研究项目** | 2026 春
**硕士在读期间个人研究**

- **主流 Web Agent Memory 框架的复现与审计**：在 Mind2Web 上做 step-level 配对实验（baseline vs workflow 同步对照），发现 workflow 实际影响窗口仅 6-18% 且 matched / mismatched 站点效果反向；归类 8 类典型失败模式（strategy redirection / domain misdirection 等），输出可复用的 paired-case 评测方法学。
- **记忆跨任务复用机制实验**（HotpotQA → 2WikiMultiHopQA 近迁移）：以 matched / mismatched 配对框架测试三种记忆形态（None / Episodic / Consolidated），定位"记忆抽象的可执行性"如何决定跨任务复用边界。

---

## 实习经历

**七牛云** | 2025.07 - 2025.10
**AI 算法工程师 / 项目组长** | 上海

- 作为项目组长协调前后端、运维、算法 6 名同学，遵循"明确产品定位 → 定义产品原型与原型图 → 定义功能 API → 完成数据表设计 → 进行模块拆分 → 模块详细设计"的架构设计 6 步法，区分技术提案 / 架构设计 / 实现设计三类决策层级文档，推动项目从需求到上线全流程联调。
- 设计并实现 Supervisor Agent → Sub Agents 架构，在运维告警处理场景下实现自动下钻归因分析与自愈，集成指标 / 日志 / 异常检测 / 上下游关系等查询工具，以及告警阈值调整 / 版本回滚等执行工具。
- 使用 RocketMQ 的发布订阅模式实现异步化 Agent 事件驱动，缓解了同步 Multi-Agent 因失败重试 / 连接超时引发的内存雪崩，支持任务失败自动重试与按优先级的事件驱动。
- 设计外部告警系统与本系统的数据中间层，实现"同一服务不同版本"动态告警阈值调整机制，使问题在更早阶段被发现与解决。

**Neo 智能经济** | 2025.02 - 2025.07
**AI Agent 开发工程师** | 上海

- 构建基于 Python 的 LLM 多智能体工作流 DeepResearch 服务，集成意图识别、任务规划、网页搜索 / 数据抓取 / 代码执行工具。
- 构建 ReAct 模式的 Agent 区块链问答系统：对话管理、短长期记忆（mem0）、本地文档搜索（FAISS）、Pinecone Serverless + OpenAI text-embedding-3-large 集成。**设计区块链 API 语义路由系统**：3072 维向量编码 62 种工具方法描述、延迟初始化动态构建索引、两阶段检索（Top10 初筛 → Top5 精排），达成 **98% 意图匹配准确率，降低 70% 调用成本**，支持实时批量索引更新。
- 参与设计与开发开源 AI Agent 框架 SDK（**260+ stars**）及配套工具集 SDK：集成同步 / 异步执行工具、Graph 工具、链上对象存储工具、钱包加密工具，编写测试用例保障可用性。**维护项目海外全球技术社区**：处理 GitHub Issues、Review 海外开发者 PR、撰写并维护开发者文档，与海外开发者协作推进项目演进。
- 实现 LLM 驱动的自动交易子账户系统：多重签名验证 + 资金配额，在用户托管账户与自动化交易账户之间实施逻辑隔离，通过 Turnkey 对钱包私钥加密存储。

---

## 技能

- **大模型与 Agent**：熟悉 Transformer / Attention 机制（QKV / Multi-Head / KV Cache）、ReAct / Plan-RePlan / SubAgent / Workflow / MCP / A2A 等 Agent 范式；熟悉 Context Engineering / Harness Engineering 工程实践；熟练运用 LangChain / LangGraph 等智能体框架。
- **训练与微调**：熟悉 PPO / DPO / GRPO / DAPO 强化学习算法及其演进谱系；熟练运用 LoRA / QLoRA 高效参数微调；理解 SFT / RLHF / RLAIF 后训练流程及能力激活关系。
- **检索与记忆**：熟悉 RAG 系统设计，熟练运用向量数据库（Pinecone）、嵌入模型与高效检索策略；理解 procedural / episodic memory 的设计权衡。
- **数据库与中间件**：熟练 MongoDB / MySQL / Postgres，以及 Redis / RocketMQ。
- **工程**：熟练 Python，具备 Go 语言基础；熟练 Gin、gRPC、微服务架构，及面向对象 / 接口 / IoC 设计原则；熟练 GitHub 工程化协作，具备测试驱动开发经验；熟练 PRD 编写、MVP 模块拆分与架构设计。

