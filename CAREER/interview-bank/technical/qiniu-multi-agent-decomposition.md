# Q: 你的多智能体根因分析系统具体怎么拆 agent？跟 Flow-of-Action 比有什么差距？

## 来源

- 出处：项目深挖（自挖）+ AgentOps 报告 §4 Flow-of-Action 是同期工作
- 频率：高（"多智能体怎么拆"是 agent 方向最高频技术题）

## 涉及节点

- 主：`PROJECTS/work/qiniu-zeroops-rca-agent/`
- 相关 KNOWLEDGE 节点：`KNOWLEDGE/agent/multi-agent/` / `KNOWLEDGE/agent/multi-agent-rca-paradigm/` / `KNOWLEDGE/agent/agent-role-isolation/` / `KNOWLEDGE/agent/structured-output/`
- 学术参考：Flow-of-Action (WWW 2025, 中科院 + 清华 + 字节)——已沉淀到 `KNOWLEDGE/agent/multi-agent-rca-paradigm/` "对照 Flow-of-Action" 段

## 我的答案

### 我具体怎么拆的（5 个角色 agent + 工作流 + SOP）

按"人类运维团队类比"拆 5 个角色：

| Agent 角色 | 模型 | 职责 | 类比人类 |
|---|---|---|---|
| 运维专家（任务规划） | qwen-plus-latest | 解析告警 + 生成 SOP 步骤计划 + 调度下游 agent | 一线 SRE |
| Metric Agent | qwen3-coder-plus | 时序指标查询 + 异常波动分析 | 指标专员 |
| Log Agent | qwen3-coder-plus | 自然语言转 SLS 查询 + 日志分析 | 日志专员 |
| Trace Agent | qwen3-coder-plus | 调用链查询 + 拓扑分析 | 链路专员 |
| 值班长（分析决策） | qwen-plus-latest | **不获取数据**，只对已有证据做结构化推理 + 判断停止条件 | 值班 SRE Lead |
| 最终输出 | qwen-plus-latest | 结构化报告生成 | 运营专家 |

**拆分轴**：**按职责拆**（每个 agent 负责一个清晰可独立调试的环节）。

**SOP**：跟运维高工 mentor 共定的"**拓扑定位 → 指标验证 → 日志取证 → 根因推断**"，嵌入运维专家 agent 的 system prompt。每个数据 agent 内部还有"严格按 5 步执行，一步都不能跳过"的固定排查流程。

**Agent 间通信**：JSON 结构化（agent_type / status / summary / data / plan / step_id），不是自由文本。

### 跟 Flow-of-Action (WWW 2025) 的对照（**这是关键的金句产出**）

> 我做的项目按学术分类属于 **OpsAgent / AgenticOps 方向**。Flow-of-Action 是这个方向的代表工作，发表在 WWW 2025。我的角色拆分跟它高度同构——**运维专家 ≈ MainAgent / 数据 agent ≈ Action Set / 值班长 ≈ JudgeAgent + ObAgent**——但我的 SOP 是 prompt 内嵌的，**Flow-of-Action 的 SOP 是一个 5 个子工具组成的动态系统**：`match_sop`（匹配历史 SOP）/ `generate_sop`（无匹配时生成新 SOP）/ `generate_sop_code`（把 SOP 转成可执行代码）/ `run_sop`（执行代码并收集结果）/ `match_observation`（结果回灌匹配下一步）。比我多的不只是"动态生成代码"，而是**把 SOP 从静态规则升级成可匹配 / 可生成 / 可执行 / 可回灌的闭环**。这是诚实的差距。

### 对照表（详细）

| 维度 | Flow-of-Action | 我做的 |
|---|---|---|
| Agent 角色 | MainAgent + ActionAgent + JudgeAgent + ObAgent | 运维专家 + 3 个数据 agent + 值班长 + 输出 agent（结构同构） |
| **SOP 机制** | **5 子工具闭环**：match_sop / generate_sop / generate_sop_code / run_sop / match_observation——SOP 是可匹配 / 可生成 / 可执行 / 可回灌的动态系统 | **prompt 内嵌 + 工作流约束**——SOP 是静态规则（差一层） |
| 多模态融合 | Result Fusion | Result Fusion（同范式） |
| 评测 | LA / TA / APL 量化指标 | 根因定位成功率 20% → 70%（迭代中） |
| 数据来源 | benchmark + 真实部署 | Mock 系统 |

## 关键金句

> "**我的多 agent 设计跟 Flow-of-Action 高度同构，但 SOP 机制差一层——他们的 SOP 是 5 子工具的闭环（match_sop → generate_sop → generate_sop_code → run_sop → match_observation），可匹配 / 可生成 / 可执行 / 可回灌；我做到 prompt 内嵌 + 工作流约束**。"

> "**5 个 agent 是按职责拆**——这种拆法对应 Result Fusion 多模态融合范式：每个数据源单独 agent 处理，最后由综合 agent 融合判断。**这是当时学术界主流方向的工业实现**。"

## 我答不出的部分（深问准备）

- **"为什么按职责拆而不是按阶段拆（explore / plan / implement / verify）"** → 答：项目是根因分析任务，**没有 implement / verify 这种生产性阶段**——主要做"信息收集 + 推理"，所以按数据源拆比按阶段拆更直观。同时类比"人类运维团队"对非算法 mentor / 团队成员更易理解。**这是当时的合理选择，但今天回看按阶段拆可能有利于 trajectory 异常检测和 failure attribution**
- **"5 个 agent 之间的 token 消耗 / 延迟数据"** → 没具体量化（**面试时诚实承认是工程感知层面的优化而非严格实验**）
- **"如果用单 agent + 多 tool 而不是多 agent，区别在哪"** → 答：单 agent 上下文累积压力大、不利于团队分工调试 / 多 agent 可独立调试单独 prompt 但 inter-agent 通信开销大。**这跟"拆函数 vs 不拆函数"的工程权衡是一样的**
