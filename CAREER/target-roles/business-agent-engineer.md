# 业务 Agent 工程师 / Agent 应用落地岗

> **优先级**：★★★★★ 主投
>
> **方向**：业务场景 → AI 原生系统架构 → Agent 工程落地（不强调训练）

## 目标公司 / 类型

- 阿里 / 字节 / 腾讯等大厂业务部门 AI Agent 落地团队
- 中型公司或独角兽的 Agent 应用方向

## JD 核心要求（按权重）

### 必须会

| 类别 | 要求 |
|---|---|
| 需求理解与归因 | 数据挖掘 + 特征分析 + 业务现象归因；把模糊业务痛点转成明确 AI 解决目标 |
| AI 原生架构设计 | Agent 系统核心模块规划：记忆管理 / 推理策略 / 工具编排 |
| 知识与环境构建 | API 接入 + RAG 知识库 + 记忆方案 + 召回质量 + 上下文注入策略 |
| Agent 关键模块 | 意图识别 / 任务拆解 / 反思纠错闭环 |
| 系统观测 | 标准化 SDK/API + 全链路追踪 + 多维归因分析 |
| 自动评测与回测 | 调优 + Case 分析 → 收敛效果与性能 |
| 高并发性能 | 异步 + 降级策略 + 低侵入观测 |

### 必须特质

| 特质 | 关键词 |
|---|---|
| AI 编程工具重度玩家 | Cursor / Claude Code 顶级玩家 + 极强 Prompt 调优 + 完整项目级开发经验 |
| 大模型能力理解 | LLM 能力 / 局限 / 任务拆解 / 确定性逻辑兜底 / 主流应用范式（Context Engineering / Prompt / Agent / 工具调用） / 主流框架（LangChain）/ 幻觉 + Prompt 注入风险工程化应对 |
| 扎实代码与工程能力 | 数据结构 / 算法 / 网络 / 操作系统 / 至少一种主流语言（Java / Python / JS）深度实践 |

### 优先会 / 加分项

- AI 应用 / Agent 实际落地经验（RAG / 多智能体 / MCP / Skill）
- 开源贡献（GitHub 高质量 AI 项目）
- AI Infra 基础理解（vLLM / Ollama 推理框架原理 + 延迟优化 + KV cache 优化 + 流式输出）
- NLP / CV 训练经验（SFT / RL）

## 我的对照

### 已具备 ✅

| JD 要求 | 我的支撑 |
|---|---|
| **AI 原生架构 + Agent 模块规划** | 七牛云 Supervisor + 主项目 Memory Pool 设计 |
| **意图识别 + 任务拆解** | Neo 98% 意图匹配 + 七牛云下钻 |
| **RAG + 记忆方案** | Neo 语义路由 + 主项目 procedural memory |
| **工具编排** | 七牛云 + Neo 都做了多工具编排 |
| **高并发性能** | 七牛云 RocketMQ 异步 + Neo 70% 成本降 |
| **AI 编程工具重度玩家** | 我和 LLM 协作开发已是日常（这个 OS 本身就是证明） |
| **LangChain / MCP** | cv 技能栈 + KB |
| **开源贡献** | Neo 150+ stars + 主项目即将开源 |
| **vLLM / KV cache 工程理解** | KB `KNOWLEDGE/transformer/kv-cache/` + 主项目 vLLM 部署 |
| **代码 / 算法 / 网络 / 操作系统基础** | 谢菲尔德本科 + 双语言（Python + Go） |

### 缺口 ⚠️

| JD 要求 | 我的状态 | 补齐路径 |
|---|---|---|
| **业务现象归因 / 数据挖掘** | 弱（实习中没碰过太多 BI 视角） | sprint 不补；面试时把 Neo 的成本归因（70% 降）当例子讲 |
| **完整 Cursor / Claude Code 项目级使用** | 已用，但没有产出物展示 | 主项目本身就是"用 Claude Code 协作开发的产物"——可以讲 |
| **NLP / CV 训练经验** | NLP 有（KB 6 个 nlp 节点）；CV 弱 | sprint 不补 |

### 优势项

- **agent memory 这个具体领域的深度**（cv 上独一份）
- **生产级多 agent 工程**（不是 demo）
- **运维场景思想实验**——展示业务理解
- **架构 6 步法 + 三类设计文档**——产品工程协同能力

## 典型面试问题（参考阿里淘宝闪购面经）

| 类别 | 题目 |
|---|---|
| 项目深挖 | LangGraph 节点设计 / 代码生成自修复机制 / 项目最大挑战 |
| 系统 | 二级缓存 + 数据一致性（cache aside / read through / write through / write behind 区别） |
| 高并发 | Redis 故障 + 主从切换 / 请求量超预期 |
| AI Coding | 带过期时间的 LRU |
| 开放 | RAG 流程 / 优化角度 / 评测指标 / 模型选择 / AI 工具使用 |
| 行为 | 职业规划 / 对公司期待 / 选择本公司理由 |

参考阿里高德面经：

| 类别 | 题目 |
|---|---|
| AI 实践 | AI 工具有哪些使用 + 对比 + 月度费用 |
| 系统 | skill / harness / openclaw / hermes 介绍及优缺点举例 |

→ skill harness openclaw hermes 这道题正是横向对比报告的硬通货。

## 投递时机

- 第 1 周末 cv 重写后即可投
- **优先级**：和 A202665 并列第一

## 参考来源

- JD 原文：`INBOX/short-term-plan-for-career/jd.md`（业务 Agent 段）
- 面经：`INBOX/short-term-plan-for-career/shared-interview.md`（阿里淘宝闪购 + 阿里高德段）
- HR 抱怨简历的诊断：`INBOX/short-term-plan-for-career/post.md`——避雷
