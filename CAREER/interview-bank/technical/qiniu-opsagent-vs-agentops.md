# Q: 你做的项目跟 AgentOps 有什么关系？如果让你 debug 自己的 agent 系统你怎么做？

## 来源

- 出处：基于 AgentOps 报告 §5-9（OpsAgent vs AgentOps 区分 + Agent 自身可观测性）的项目深挖
- 频率：中-高（任何懂 agent 工程的面试官都会问"agent 挂了怎么 debug"）

## 涉及节点

- 主：`PROJECTS/work/qiniu-zeroops-rca-agent/`
- 相关：`PROJECTS/research/awm-mechanism-audit/` + `PROJECTS/research/selective-transfer-memory/`（当前 CV 中的 Agent Memory 自主研究）
- 相关 KNOWLEDGE 节点：`KNOWLEDGE/agent/agentops-vs-opsagent/`（核心概念）+ `KNOWLEDGE/agent/agent-failure-attribution/`（debug agent 系统的核心方法论）+ `KNOWLEDGE/agent/agent-anomaly-taxonomy/`（11 类异常分类）+ `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`（标准化失败轨迹 schema + 6 benchmark + 标注流水线）

## 我的答案（核心：把两段项目连成一条故事线）

### 概念定义（5 秒回答）

> AgentOps 和 OpsAgent 是两个方向：
>
> - **OpsAgent / AgenticOps** = 用 Agent 做传统系统的运维（**我在七牛云做的**）
> - **AgentOps** = 用运维技术管理 Agent 系统本身（新方向，和我后续做 Agent Memory / failure analysis 的研究兴趣相连）

### 我的项目属于哪个

> **七牛云项目是 OpsAgent**——用多智能体做传统微服务系统的根因分析。但**项目过程中我碰到的核心痛点恰好是 AgentOps 问题**：Agent 模块单独跑通了，但端到端联调始终上不去——"**Agent 搭建爽，Debug 火葬场**"（AgentOps 报告里的原话）。

### 当时为什么没意识到要做 AgentOps

> **2025.07-10 那会儿 AgentOps 这个概念在学术界都还没成型**（裴昶华这份报告是 2025 CCF ChinaSoft 的，时间晚于我项目结束）。我们做 OpsAgent 项目时，**Agent 自身的可观测性 / failure attribution / checkpoint rollback 这些工程能力都不在视野里**——我们的整个工程基础设施都是为传统系统设计的。

### 如果今天重做我会补哪些 AgentOps 能力

| 缺什么 | 具体补什么 |
|---|---|
| **Agent 自身可观测性** | 在已有 JSON 结构化输出之上再加：每步 thought / action / observation 的事件流记录、token 消耗 / 延迟 / 工具调用结果的结构化追踪、agent 间消息传递的 trace ID |
| **Anomaly Taxonomy（异常分类的边界）** | 11 类异常 = Intra-Agent 5 类（Reasoning / Planning / Action / Memory / Environment）+ Inter-Agent 6 类（Task Spec / Security / Communication / Trust / Emergent / Termination）；**先有分类才能谈检测和归因**——我们项目当时连"挂在哪一类"都没法系统化标，全靠人肉看（详见 `KNOWLEDGE/agent/agent-anomaly-taxonomy/`） |
| **Failure Attribution** | 端到端跑挂时定位"哪个 agent / 哪一步 / 哪个工具调用首次引入错误"——可参考报告 §9-10 的 Who&When / FAMAS / Echo / Correct 等方法 |
| **Failure Trajectory Dataset（长期改进的基础设施）** | 标准化 schema（mistake_agent / mistake_step / mistake_reason / history / system_prompt）+ 6 benchmark 覆盖（SWE-Bench Pro / Terminal-Bench / WebArena-Verified / OSWorld-Verified / VitaBench / TravelPlanner）+ LLM 预标注 + 人工复核流水线；**单次 debug 是治标，标注好的失败轨迹库才让系统能长期改进**（详见 `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`） |
| **Model Data / Checkpoint Data** | 报告 §8.1 提到的 attention map / logits / memory state / workflow state 等，让 agent 错误后能 replay 而不只是看到最终错误 |
| **Trajectory 异常检测** | Group-wise VAE 对调用链做结构 / 延迟异常检测，可借鉴到 agent trajectory 上（详见 `KNOWLEDGE/agent/agent-failure-attribution/` "AIOps 方法可以迁移" 段） |
| **Resolution 可回滚** | rollback / rerun / A/B test prompt——agent 多步推理失败后能回到具体步骤重跑而不是从头重来 |

### 如果今天重做我会怎么强化 OpsAgent 自身能力（procedural memory 方向）

上面那张表是补**AgentOps 工程化能力**（让 agent 能被调试 / 归因 / 持续改进）。如果要进一步强化 **OpsAgent 本身的智能** 而不是工程化能力——我的判断是：**用 procedural memory 替代当前的短期上下文压缩**。

**核心思路**：模型本身够强、工具也成熟，问题不是"能不能做"而是"重复搜索浪费"；运维的当前拓扑、服务依赖、告警模式是**外部结构**——刚好该用 procedural memory 保留（保留可复用的搜索路径、验证顺序、边界条件）。

**详细延伸思考 + 面试 challenge 答案** → 见 [`main-project-and-research.md`](./main-project-and-research.md) **§E 未来延伸**。

**具体两层架构（Storage partition vs Retrieval filter + Declarative vs Procedural）+ 面试 soundbite + 5 个 challenge 防御** → 见 [`memory-architecture-for-ops.md`](./memory-architecture-for-ops.md)（从资深 SRE 视角反推得到的洞察）。

**面试切入时机**：
- 当面试官问 "**如果重做 OpsAgent 你会怎么变？**"——可以从 AgentOps 工程化（上表）切到 OpsAgent 自身智能强化（procedural memory）形成双维度回答
- 当面试官问 "**拿到优质数据你只能 SFT 吗？**"——直接切到 procedural memory 作为 SFT 之外的另一条路径
- 当面试官问 "**你研究方向 / 你最近在思考什么？**"——从 Agent Memory 自主研究切入，再讲如果重做 OpsAgent 会如何加入 procedural memory

### 关键金句（**面试时拉满学术坐标 + 自我学习路径**）

> "**我七牛云做的是 OpsAgent，但碰到的痛点是 AgentOps**——Agent 单独跑通了端到端联调始终上不去。当时这个概念学术界还没成型，我们的工程基础设施都是为传统系统设计的。后来我做 Agent Memory 自主研究，本质上是在继续追问：Agent 如何从历史轨迹里提取可复用经验、如何判断这些经验什么时候帮忙什么时候误导。"

## 关键金句（备用，更精炼版）

> "**Agent 搭建爽，Debug 火葬场——这是我项目当时的真实痛点，也是 AgentOps 这个新方向要解决的核心问题**。"

## 我答不出的部分（深问准备）

- **"具体某个 agent debug 失败的例子"** → 答：**最让我印象深的是 ReAct 循环不终止**——agent 反复调同样的工具但没有进展，最后我们补了"值班长不获取数据，只做结构化推理 + 智能终止判断"的角色才解决。**这本质上就是 AgentOps 多智能体异常分类里的 Inter-Agent / Termination Anomaly**——11 类异常的具体边界见 `KNOWLEDGE/agent/agent-anomaly-taxonomy/`
- **"你 Agent Memory 研究跟 AgentOps 具体怎么连"** → 答：我研究的是 agent 从历史成功 / 失败 trajectory 里抽出可执行经验，并判断什么时候复用、什么时候不复用。这和 AgentOps 的连接点是 failure trajectory、failure attribution 和 memory policy：不是只 debug 一次，而是让失败轨迹变成长期改进材料
- **"未来你想做 OpsAgent 还是 AgentOps，具体抓哪几个子问题"** → 答：**AgentOps**。理由：(1) OpsAgent 是用 agent 做事，工程问题已经清晰；(2) AgentOps 是工程基础设施层，是 agent 大规模落地的必经环节；(3) 我亲身经历过 OpsAgent 项目卡在 AgentOps 缺位上，这种"用户视角的工程痛点"是 AgentOps 研究者最珍贵的资产。**具体抓三件事**：(a) **异常分类**——先把 11 类异常的边界划清楚（Reasoning vs Action vs Memory vs Communication vs Termination 不能混），不然检测和归因都谈不上；(b) **Failure Attribution**——Who & When 是基础，FAMAS / Echo / Correct 是上层方法；(c) **Failure Trajectory Dataset**——标准化 schema + 多 benchmark + LLM 预标注 + 人工复核的流水线，让系统能从失败里持续改进，而不是每次都重新调一次
- **"如果让你给你的项目补 AgentOps 能力的顺序"** → 答：**异常分类 → 可观测性 → Failure Attribution → Trajectory Dataset**。理由：分类先于检测（不知道有几类异常无法埋点）；可观测性是基础（没事件流谈不上归因）；Failure Attribution 解单次 debug 问题；Trajectory Dataset 是长期改进的底座（**单次 debug 是治标，标注好的失败轨迹库才让系统长期能改进**——这跟传统 AIOps 历史告警库的角色一致）
