# A202665 — AI Agents 算法实习生

> **优先级**：★★★★★ 主投
>
> **方向**：Coding Agent 全流程（数据 → 训练 → 推理 → 部署 → 评测）

## 目标公司 / 类型

- 一线大厂代码智能体团队（具体公司从 JD 编号 A202665 反查；JD 风格判断为头部）

## JD 核心要求（按权重）

### 必须会

| 类别 | 要求 |
|---|---|
| Coding Agent 系统全流程 | 数据构建（代码语料清洗、代码 / 对话 / 工具轨迹标注）→ 预训练 / 持续预训练 → SFT → 后训练（DPO/ORPO/RLHF/RLAIF） → 评测 |
| Benchmark | HumanEval / MBPP / SWE-bench / RepoBench |
| Agent 框架实战 | LangChain / AutoGen / Agno（至少一个） |
| MCP 协议 | 设计与实现 MCP servers/tools；标准化接入代码搜索 / 编译 / CI/CD / Issue/PR 等 |
| 推理策略 | ReAct / Plan-Act / Tree-of-Thought + Function Calling + RAG（向量 + 结构化 + 代码图） |
| 推理优化 | 蒸馏与量化（AWQ/GPTQ/GGUF）+ 图编译（vLLM / TGI / TensorRT-LLM）+ 缓存（PagedAttention / speculative decoding / prompt caching） |
| 工程化 | Python + 强类型语言（Go / Java / C++ / Rust）+ Git / Linux / 容器 |
| 评测体系 | 执行成功率 / 修复成功率 / TTFR / TTFX；合成数据与轨迹蒸馏管线 |

### 优先会

- 安全沙箱执行与资源隔离
- 鉴权 / 灰度 / 监控告警 / 回滚
- 提示注入 / 越权工具调用防护
- IDE 集成（VSCode / JetBrains）

### 加分项

- 顶会论文
- 大型项目调试与优化经验
- 开源贡献

## 我的对照

### 已具备 ✅

| JD 要求 | 我的支撑 |
|---|---|
| Agent 框架实战 | Neo: ReAct + LangChain + Pinecone；七牛云: Supervisor + Sub-Agents |
| MCP / Function Calling / RAG | 简历技能栈 + KB `KNOWLEDGE/agent/structured-output/` |
| 推理优化（KV cache 工程理解）| KB `KNOWLEDGE/transformer/kv-cache/` 节点 + Neo 70% 成本降经验 |
| ReAct / Plan-Act 推理策略 | Neo 区块链问答 + 七牛云 supervisor |
| Python + 强类型（Go） | cv 技能栈 |
| **评测体系（matched/mismatched 配对 + boundary patterns）** | **自主研究项目两条已交付**：(1) Web agent memory 框架复现 + step-level 分析（6-18% 影响窗口 + 8 类失败模式 + 475-step paired-case 分析）；(2) HotpotQA → 2WikiMultiHopQA 跨任务复用实验（subtype-aware rerouting + operator-level repair） |
| **跨任务记忆迁移方法学** | 自主研究项目（matched/mismatched 配对 + memory 抽象的可执行性边界）|

### 缺口 ⚠️

| JD 要求 | 我的状态 | 补齐路径 |
|---|---|---|
| **SWE-bench / RepoBench 实战** | 未跑过 | 主项目 Week 3-7 |
| **预训练 / 持续预训练** | 未实战 | KB `KNOWLEDGE/training/posttrain-practice-roadmap/` 已有方法论；当前 sprint 不实战，面试时讲方法论 |
| **DPO / ORPO / RLHF / RLAIF** | 原理熟（KB `rlhf-dpo-grpo`），缺工程实战 | 主项目 GRPO 阶段 |
| **AWQ / GPTQ / GGUF 量化** | 概念熟，未跑过 | sprint 不补，**Q&A 时讲原理 + 已知量化对 KV cache 的影响（KB 已支撑）** |
| **vLLM / TGI / TensorRT-LLM** | 主项目要部署 vLLM | 主项目 Week 8 |

### 优势项（同竞争者比）

- **agent memory 研究深度**——主项目 + 横向对比报告 + selective transfer 方法学
- **生产级多 agent 工程经验**——七牛云 supervisor + RocketMQ 异步 + 动态阈值
- **真实开源协作**——Neo 海外社区 + 主项目开源仓库
- **组长 + 架构思考**——七牛云 6 步法 + 三类设计文档

## 典型面试问题（参考字节面经）

| 类别 | 题目 |
|---|---|
| 项目深挖 | reward 怎么设计 / 后续改进思路 |
| 八股 | PPO / GRPO 区别 + critic 训练 + KL 散度作用 |
| KV Cache | KV cache 工程实现 / MLA |
| Transformer | QKV / Multi-Head / Position Encoding |
| Agentic RL | reward hacking / GRPO 改进算法 |
| 开放 | 长对话强化学习 reward / 模型 vs 规则奖励 / 奖励坍缩与 hacking 防范 / 长对话工程方法 / 多轮对话微调 / 上下文记忆保持 / agentic RL 设计思路 / SFT → RL 时机 / 评估方法 |
| 系统 | harness / Hermes / 最新论文 |
| 手撕 | 链表相加（双指针）类基础题 |

→ 这些题已派生到 `interview-bank/technical/`（Week 2 完成）

## 参考来源

- JD 原文：`INBOX/short-term-plan-for-career/jd.md`（A202665 段）
- 同公司面经：`INBOX/short-term-plan-for-career/shared-interview.md`（字节相关段——风格高度相近）

## 投递时机

- **第 1 周末** 简历重写完成即可投
- **第 2 周** 横向对比报告做完后追加 GitHub 链接到 cv，可二次投递

## 面试准备节奏

- Week 1：八股部分用 KB self-check 过一遍
- Week 2：横向对比报告完成后，"最新论文 / harness / Hermes" 这类题有硬通货
- Week 3+：主项目 SFT 跑通后，"SFT → RL 时机 / GRPO 改进 / 奖励坍缩" 这类题有亲身实战
