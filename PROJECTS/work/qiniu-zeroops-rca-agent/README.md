# 七牛云 ZeroOps · 多智能体根因分析下钻模块

> 七牛云 1024 实训营 ZeroOps 智能运维项目（CEO 许式伟亲带 + mentor 王昶敏带教）。我作为项目组长 + Agent 设计负责人协调 6 人推进，核心交付是"指标下钻分析"子系统——基于 LangGraph StateGraph 编排的 L1/L2/L3 多智能体 + MCP 工具集成。

## 五份文档的分工

| 文档 | 焦点 | 用在哪 |
|---|---|---|
| **本页 `README.md`**（决策复盘） | 时代背景 / 关键决策 / 真实选型路径 / SOP 实情 / 学术坐标 / 复盘 / Lessons learned / 简历素材 / 面试故事入口 | 面试前 1 小时快速过 / 写 STAR / 投递 |
| [`system-anatomy.md`](./system-anatomy.md)（系统解剖） | 6 层架构 / 5 大类 REST API + JSON schema / 8 张数据表 + 7 类查询 / 关键流程图（告警去重处理 / 体检中心 / 灰度发布回退 / 异常检测微服务）/ 6 步法实操产物清单 | 被追问技术细节时打开 / 重温自己做过的东西 |
| [`agent-subsystem.md`](./agent-subsystem.md)（Agent 子系统解剖） | LangGraph StateGraph 工作流 + 模型选型 / ReAct PDL 改造 / MCP 工具集 schema / 5 个角色 agent 的 prompt 主体 + JSON 输出 schema / 4 类知识库设计 / **20%→70% 优化路径（含分段数字）** / LangGraph StateGraph vs 自由 Agent Loop vs Claude Code 三方对比 | 面试官追问"你 agent 怎么设计的"时打开 |
| [`mock-system-design.md`](./mock-system-design.md)（**Mock 系统定稿** · 数字地基） | **5 服务 + 2 DB + 10 test case 定义 / 成功标准 / 基线故事 / 7 步分段数字 / 体检中心双路径详解** | 被追问"20% 怎么测的" / "mock 跑了几个服务" / "哪步提升最大"时打开；是所有量化数字的唯一权威来源 |
| [`interview-defense-matrix.md`](./interview-defense-matrix.md)（挑战防御矩阵 · living document） | 10 类挑战 × 60+ 条具体角度 × Readiness 评级 × 深答位置 + P0/P1/P2 GAP 清单 | 准备面试时定位"哪些角度已经准备好 / 哪些是空白 / 下一步该补什么" |

## 类型

`work`

## 目标

为七牛云内部"变更场景的多版本灰度发布管理"系统提供 AI 驱动的故障根因分析能力。在灰度发布过程中检测到异常指标后，由多智能体协作完成跨数据源（指标 / 日志 / 链路 / 拓扑）的关联分析，定位根因并输出可执行的修复建议或自动化动作（重启 / 回滚）。

## 动机

- 七牛云 2025 年 1024 实训营议题。CEO 许式伟立项，AIOps 是 CEO 高度重视的方向
- 传统运维痛点：告警风暴 / 故障定位严重依赖个人经验 / 监控数据孤岛 / 应急响应流程僵化 / 故障经验沉淀难
- 项目初期没有 PRD——团队组建即是产品 0→1 阶段，产品形态经历三次重大调整后由 CEO 拍板收敛到"变更场景的多版本灰度发布管理 + AI 根因下钻 + 简单自愈（重启 / 回滚）"

## 范围

### 包含

- **整体 ZeroOps 系统设计**：6 层架构（View / Controller / Model / 指标分析 / 基础设施 / 外部 mock）+ 5 大类 REST API（服务信息 / 发布任务 / 服务指标 / 告警事件 / 系统变更）+ 数据表设计 + 7 类查询路径
- **多智能体根因分析下钻子系统（我的核心交付）**：基于 LangGraph StateGraph 编排 L1（运维专家：文档检索 + 问题类别 + 决策）/ L2（专门 agent：日志查询分析 / Metric 指标查询分析 / Tracing 查询分析）/ L3（通用专家 + 语言专家）的三层 agent 协作架构。所有工具通过 MCP Server 封装在函数计算上动态调用（日志 / 指标 / 链路 / CMDB 拓扑）
- **灰度发布场景的多版本并行策略**：v1.0 / v1.1 / v1.2 三阶段灰度（5% → 30% → 100%）+ 异常时优先回退最近稳定版本的逐层回溯逻辑
- **运行体检中心**：Go 主流程 + Python 异常检测微服务（STL 分解 + 百分位数检测的 MVP 算法）
- **架构设计 6 步法实操**：产品定位 → 原型图 → API → 数据表 → 模块拆分 → 模块详细设计（mentor 王昶敏带教 + CEO 直接参与决策）
- **组长职责**：每日晨会 / 每日领导汇报 / 公司周报 / milestone 路演 / 前后端联调 / 算法效果（后期人员动荡时接手大量后端联调工作）

### 不包含

- ❌ **未上线生产**：三个月内停留在 MVP，**没真正接入生产环境，全部基于 Mock 系统**
- ❌ Agent 模块独立完成但因产品设计反复调整 + 联调困难导致**未真正接入主链路完整跑通端到端**
- ❌ 复杂时序异常检测（MVP 简化为 STL + 百分位数）
- ❌ 任意场景下的全自动自愈（MVP 治愈动作限定为重启 + 回滚）

## 团队与角色

| 成员 | 职责 |
|---|---|
| **李勐霄（我）** | 组长 + Agent 设计 + 团队任务推进 + 前后端联调（后期） |
| 王辉 | Agent 设计 |
| 程也 | Mock 系统设计 + 时序检测数据配合 |
| 丁楠加 | Mock 系统设计 |
| 王青云 | 时序检测算法 |
| mentor 王昶敏 | 1024 实训营带教导师，架构设计 6 步法的提出者 |
| mentor（运维工程师） | 业务专家，灰度发布 / 告警机制专业指导 |
| 许式伟（CEO） | 项目立项 + milestone 拍板 + 架构细节关键决策 |

**时间投入分配**：算法 30% / 产品设计 + 架构设计 + 协调 + 联调 70%。

## 时代背景（面试时最关键的一段——决定项目"看起来过时"还是"当时合理"）

项目时间是 **2025.07-10**。当时的开源生态：

| 维度 | 2025 年 7 月（项目进行时） | 2026 年 5 月（现在回看时） |
|---|---|---|
| Agent loop 系统 | **市面上还没有开源的 agent loop 系统** | Claude Code / Codex / Cursor Agent / OpenHands / SWE-agent 等遍地开花 |
| 上下文工程 | **概念刚刚兴起** | 已成主流工程范式 |
| Coding Agent | 概念未成型 | 成熟方向 |
| Harness Engineering | 概念未成型 | 成熟方向 |
| Skills | Anthropic 还没推出 | "Skills = 岗位说明书 + SOP + 工具包"已成共识 |
| 最火的开源 agent 项目 | **基于 DAG 的 DeepResearch** | 基于 agent loop 的 coding agent |

**这意味着**：项目时段的技术选项远比现在窄。**评判项目选型必须放在 2025.07 的技术坐标里看，不能用 2026 的标准回评**。

## 真实的技术选型路径（不是"naive 选了 StateGraph"）

项目初期，我**先用 LangChain AgentExecutor 试过自由 ReAct loop**——类 coding agent 式 / multi-agent 协同风格的实现。

**结果**：**主动放弃**。原因（事后反思）：

1. **运维场景安全性**：重启 / 回滚是不可逆动作，自由 loop 的自主执行在运维场景下不可接受——必须有显式的计划审批节点（HITL interrupt）；agent loop 路径在 2025.07 还没有成熟的 ops safety 配套
2. **多 agent 协同失败模式**：trajectory 错误传播、context 累积失控、循环不终止，没有标准化的可观测性工具
3. **整体工程成熟度**：agent loop + ops safety + 多 agent 可观测性这套组合当时尚不完善——不像现在已有 Claude Code、OpenHands 等成熟框架

**取舍**：**主动转向 LangGraph StateGraph**——显式节点边界 + State 类跨节点持久化 + HITL interrupt（值班长作为系统侧 HITL 检查点在每轮循环后裁决，阻止循环失控）。这是与字节跳动同期开源的 DeerFlow 1.0 同一套思路的工业落地：Coordinator/Planner → Researcher × N（并行）→ Reporter，配合 human-in-the-loop 的计划审批节点。

这是有意识的架构取舍——**用 StateGraph 的结构化可控性换自由 loop 的灵活性**，是运维这类严肃场景下的合理工程选择。

## 真实的 SOP 实情（不是缺位 SOP）

**SOP 是跟运维高级工程师 mentor 密切合作共同商定的，不是 prompt 拍脑袋写出来的**。

具体表现在三层：

1. **总体 SOP**（嵌入"运维专家 agent"的 system prompt）：**"拓扑定位 → 指标验证 → 日志取证 → 根因推断"** 的固定步骤
2. **数据 agent 内置阈值排查流程**（每个数据 agent 在 prompt 内规定**"请严格按照以下五个步骤执行，一步都不能跳过或合并"**）：
   - Metric Agent：分析与准备 → 翻译查询 → 执行 → 分析结果 → 输出
   - Log Agent：提取查询信息 → 自然语言转 SLS 查询 → 执行 → 分析 → 输出
3. **值班长 agent 的"不获取数据只判断"原则**——强制约束（"不得忽略 CMDB 提供的上下文 / 不得输出模糊结论 / 不得重复已有分析步骤 / 不得连续调用同一工具超过 2 次"）

**对比 Flow-of-Action (WWW 2025)**：Flow-of-Action 的 SOP 是"可匹配 / 可生成代码 / 可执行 / 可观察"的行动流；**我做的 SOP 是嵌入式 prompt + 工作流约束**，没到"动态生成代码并执行"那一步——这是诚实的差距，但**SOP 本身真实存在且经过运维高工 mentor 把关**。

## 关键决策

| 决策 | 候选 | 选了什么 | 理由 |
|---|---|---|---|
| 产品场景（CEO 拍板） | (a) 对话入口辅助 SRE / (b) 无人化完全替代 SRE / (c) 变更场景的多版本灰度发布管理 | (c) | 团队三次方向变更卡在"产品形态共识"上，前两个选项要么太轻（只是对话框）要么太重（无人化目标不可达），CEO 在 milestone 汇报后拍板收敛到变更场景——既有明确边界（灰度发布过程）又有真实价值（故障早发现） |
| 第一次路演失败后的 MVP 共识 | 继续做完整运维平台 / 收敛到只做变更场景 | 只做变更场景 | 路演时 5 位导师批评"产品形态不清"，团队复盘后明确"先思考 MVP 形态再做模块"——故障治愈只做重启 + 回滚，时序检测只做 STL + 百分位数 |
| **Agent 编排范式**（最容易被追问） | **(a) LangChain AgentExecutor 自由 ReAct loop / (b) DAG 工作流（DeepResearch 式）/ (c) LangGraph StateGraph + ReAct** | **(c) LangGraph StateGraph + ReAct** | **先试了 (a) → 放弃**。运维场景安全性要求显式 HITL（重启/回滚不可逆）；多 agent trajectory 失败模式难以收敛；agent loop + ops safety 组合当时不完善（不像现在有 Claude Code / OpenHands）。**用 StateGraph 的结构化可控性换自由 loop 灵活性，是运维严肃场景下的合理工程选择** |
| Agent 编排平台 | LangChain AgentExecutor / LangGraph StateGraph / Dify / 自建 | **LangGraph StateGraph (K8s)** | 显式节点边界 + State 类跨节点持久化 / 每个 agent 节点可单独单元测试和调试 / HITL interrupt 支持计划审批 / 与 MCP 工具调用集成 / 与 DeerFlow 1.0 同套架构思路 |
| 工具调用协议 | 直接 Function Calling / MCP / 自建 RPC | **MCP（封装在函数计算上）** | 标准化协议解耦大模型与底层运维系统 / 工具集合灵活扩展 / 函数计算便于独立部署和迭代 |
| 多智能体职责切分 | 单 agent + 多 tool / 多个对等 agent / 分层 agent | **运维专家 + 3 个数据 agent + 值班长 + 最终输出 agent**（即 L1/L2/L3 分层的具体落地） | 类比"人类运维团队"——运维专家做任务规划 + 调度 / 三个数据 agent 各自专精 Metric / Log / Trace / 值班长做证据评估和停止判断（不获取数据） / 最终输出做结构化报告。**职责拆分透明化工作流**——每个 agent 输入输出可追溯（JSON 结构化），便于团队调试 |
| **多模态融合范式** | Result Fusion / Model Fusion / Feature Fusion | **Result Fusion** | 每种数据源（Log/Metric/Trace）先单独 agent 分析转结构化告警事件，再交综合 agent 融合判断。**原因**：(1) 日志 / 指标 / 调用链已有成熟工具，没必要重做 embedding；(2) 转结构化事件后 LLM 可直接读，工业落地友好；(3) Agent 天然适合多工具输出综合判断 |
| **SOP 嵌入方式** | (a) 纯 ReAct 自由 plan / (b) prompt 内嵌 SOP / (c) 可执行 Flow（生成代码并执行） | **(b) prompt 内嵌 SOP + 工作流约束** | 跟运维高工 mentor 共同商定"拓扑定位 → 指标验证 → 日志取证 → 根因推断"主流程 + 每个数据 agent 内部固定排查步骤 + 值班长有约束规则。**没做到 Flow-of-Action 的"动态生成代码并执行"层** |
| ReAct 性能优化 | 不优化 / 工程优化 / 模型优化 | **工程优化**：减少循环 + 上下文压缩 + 智能终止判断 + 显式总结工具 | 多轮 ReAct 端到端延迟高 + 历史 Observation 累积导致 token 爆炸 + 易丢关键信息。**MVP 阶段先做工程优化，模型层优化后续迭代** |
| 模型选型 | 全用一个模型 / 按角色选模型 | **按角色选**：运维专家 + 值班长用 qwen-plus-latest，3 个数据 agent 用 qwen3-coder-plus | 数据 agent 需要写 SLS 查询语句 / 处理结构化数据 → coder 模型更强；规划和判断 agent 需要综合推理 → plus 模型够用 |
| 异常检测语言栈 | 纯 Go / 纯 Python / Go + Python 微服务 | **Go 主流程 + Python 异常检测微服务** | 主流程在 Go（与团队后端栈一致）/ 异常检测算法在 Python（生态优势）/ 通过 HTTP API 解耦，**算法模块独立迭代** |
| 数据库 | MySQL / Postgres | **Postgres** | 支持 ARRAY 类型简化告警 labels / metrics 等结构化数据存储，减少拆表 |
| 后端框架 | Gin / Echo / fox | **fox（Gin 的七牛云内部包装）** | 团队内部标准栈 / mentor 推荐 |

## 学术坐标（项目 vs Flow-of-Action / OpsAgent vs AgentOps）

> 这一段让你能在面试时**把自己的项目放进学术研究地图里说话**。完整学术框架已沉淀在 `KNOWLEDGE/agent/agentops-vs-opsagent/`、`KNOWLEDGE/agent/multi-agent-rca-paradigm/`、`KNOWLEDGE/agent/agent-failure-attribution/` 三个节点。

### 我做的项目属于哪个方向

**OpsAgent / AgenticOps 方向**——用 Agent 做传统运维系统的根因分析。**不是 AgentOps**（AgentOps 是运维 Agent 系统本身，是新方向）。详见 `KNOWLEDGE/agent/agentops-vs-opsagent/`。

### 跟 Flow-of-Action (WWW 2025) 的对照

| 维度 | Flow-of-Action（中科院+清华+字节，WWW 2025） | 我做的 |
|---|---|---|
| Agent 分工 | MainAgent + ActionAgent + JudgeAgent + ObAgent | 运维专家 + 3 个数据 agent + 值班长 + 最终输出（结构同构） |
| **SOP 机制** | **可匹配 / 可生成代码 / 可执行的 Flow** | **prompt 内嵌 + 工作流约束**（差一层，未做到动态生成代码并执行） |
| 工具集 | Data Analysis Tools + SOP Flow Tools + Other Tools | MCP 工具集（Log / Metric / Trace / CMDB） |
| 多模态融合范式 | Result Fusion（每模态先转告警事件） | Result Fusion（同一范式） |
| ReAct 优化 | 论文级实验 | 工程级（减少循环 + 上下文压缩 + 智能终止 + 显式总结） |
| 评测 | LA / TA / APL 量化指标 | 根因定位成功率（迭代中 20% → 70%） |
| 数据来源 | benchmark + 真实部署 | **Mock 系统** |
| 验证 | WWW 2025 论文级 | 内部 MVP / 未上线 |

### Result Fusion 范式选型的可辩护逻辑

报告 §3 明确**演讲人偏向 Result Fusion**，理由跟我做的项目逻辑一致：

1. 日志 / 指标 / 调用链各自有成熟工具
2. 转文本事件后 LLM 可以直接处理
3. Agent 天然适合把多个工具输出放在一起综合判断

**这意味着我的多智能体设计不是 naive choice，而是当时学术界主流方向的工业实现**。

### 我的项目当时没意识到的事（事后用 AgentOps 视角审视）

报告 §5.3 + §8 提出"Agent 搭建爽，Debug 火葬场"——这正是我项目"Agent 模块单独跑通但端到端联调困难"的本质。

如果当时知道 AgentOps 视角，应该补：

1. **Agent 自己的可观测性**：Model Data（attention map / logits）+ Checkpoint Data（memory / workflow state）的记录
2. **Trajectory 异常检测**：可借鉴 Group-wise VAE 这类方法对 agent 调用链做结构 / 延迟异常检测
3. **Failure Attribution 机制**：当端到端失败时定位是哪个 agent / 哪一步 / 哪个工具调用首次引入错误

这条**事后审视**给了项目复盘一个学术坐标——**MVP 没上线不只是产品问题，更是因为缺 AgentOps 视角导致 debug 成本不可控**。

## 遇到的问题与解决

### 问题 1：产品形态三次大调整，团队卡在共识上几周

**情境**：项目初期没有 PRD。产品形态从"对话辅助 SRE"调整到"无人替代 SRE"再调整到"多版本灰度发布管理"。每次调整都触发原型图重画 / API 重设 / 数据表重新设计的连锁返工。团队 6 人对 MVP 形态褒贬不一，**几周陷入'设计停摆'**。

**第一次路演当场暴露问题**——5 位导师集中批评：

- 产品形态前端还是后端不清晰
- 选择 Agent 框架没有调研过程
- 路演堆砌专业名词、听众听不懂
- 没思考为什么联调失败
- 演示文档准备不足、缺整体流程演示

**解决**：

1. **CEO milestone 汇报后亲自拍板**——敲定"变更场景的多版本灰度发布管理"为 MVP 唯一形态，同时辅助验收数据表 / API / 架构设计
2. **团队复盘文档明确 MVP 共识清单**——"先思考 MVP 形态再做模块、把功能串起来再细化"
3. **复盘后产出新版完整设计文档**——重新走完 6 步法（产品定位 → 原型图 → API → 数据表 → 模块拆分 → 模块详细设计）

**学到的具体一件事**：技术提案缺位是根本原因——三次方向变更没有 1-2 页的论证文档让团队达成共识就直接跳到架构设计层反复返工。**这是组长应该担起来的，而我当时没有意识到**。

### 问题 2：人员动荡（有人离职 + 团队信心不足）+ 联调任务量爆炸

**情境**：项目中期有人离职，团队整体对产品形态反复调整失去信心，路演压力同时压上来。我作为组长不得不接手大量前后端联调工作。

**取舍**：先放弃了**算法效果调优**——把算法停在"能跑"的 MVP 状态，把时间挪去做联调和团队协调。

**解决**：

1. 主动接手前后端联调（每天和后端联调接口、和前端联调展示、和算法联调 mock 数据格式）
2. 路演前进度不达预期，**加班补救** + 紧急做 PPT 和录屏 → 最终路演呈现超出所有人预期

**反事实复盘**：如果重做，我会——

1. **让每个同学每天都有产出**，不能让团队卡在一个点不动
2. **尽早找领导帮助**——可以多寻求帮助，不要试图一个人扛
3. **意见不统一时立刻开会沟通达成一致**，不要拖

### 问题 3：Agent 模块单独跑通但端到端联调困难

**情境**：基于 LangGraph StateGraph 的 L1/L2/L3 多智能体根因分析模块单独可以跑通，**但因为产品设计反复调整 + Mock 系统接口持续变更 + 时序检测数据格式不稳定，端到端主链路始终联调不顺**。

**坦诚结果**：**Agent 模块没有真正接入主链路完整跑通**——三个月内 Agent 单独的根因分析逻辑设计完整、LangGraph StateGraph 工作流配通、MCP 工具调用通了，**但与外部告警 / 体检中心 / 发布系统的串联停在 Mock 阶段**。

## 结果

### 量化数字（可面试讲）

- **Agent 单独 demo 上根因定位成功率**：**迭代过程中从 20% 优化到约 70%**（项目内部技术总结，Mock 系统数据非生产 A/B）
- **优化路径**：开发集成 CMDB 服务 + 拆分知识库（系统架构 / 历史故障案例 / 运维流程三类）+ 动态注入上下文 + 时间通过中心化函数统一 + 重写提示词结构 + 加入缓存机制
- **ReAct 性能优化**：减少循环次数 + 上下文压缩 + 智能终止判断 + 显式总结工具（具体延迟 / token 节省数据：未量化，**面试时可承认是工程感知层面的优化而非严格 A/B 实验**）

### 坦诚的现状（投递简历 / 面试时必须讲清楚）

- ✅ **完整走完架构设计 6 步法**——产出完整设计文档（原型图 + API + 数据表 + 6 层架构 + 模块详细设计）+ 复盘文档
- ✅ **多智能体根因分析下钻模块独立 demo 跑通**——5 个角色 agent + LangGraph StateGraph 工作流 + MCP 工具集成 + ReAct 迭代收敛
- ✅ **SOP 真实存在**——跟运维高工 mentor 共定的"拓扑定位 → 指标验证 → 日志取证 → 根因推断"主流程嵌入 system prompt
- ✅ **真实数字结果**——根因定位成功率迭代中 20% → 70%
- ✅ **第一次路演失败后的恢复**——加班补救 + PPT + 录屏让最终路演呈现超预期
- ✅ **作为组长协调 6 人 + 完整经历三类决策层级文档实操**（架构设计 + 实现设计 + 复盘——技术提案是缺失的，这是教训）
- ❌ **未上线生产**：三个月内停留在 MVP 阶段
- ❌ **基于 Mock 系统**：未真正接入生产告警 / 监控 / 发布系统
- ❌ **端到端主链路未跑通**：Agent 模块单独可用，但与其它模块的串联停在 Mock 接口

**注**：CV「比赛奖项」里的「七牛云第三届 1024 创作节优胜奖」属于另一条经历（创作节内容类活动），**与本 ZeroOps 项目无关**——写简历素材 / 面试故事时不要 inline 到本项目 bullet。

## 复盘 / Lessons learned

### 1. 技术提案缺位是根本原因（产品决策层）

三次方向变更（对话辅助 → 无人替代 → 灰度发布管理）每次都直接跳进架构设计层返工，**应该先写 1-2 页技术提案让团队达成方向共识**。CEO 最后拍板的本质是替我们补了那个缺位的"技术提案 + 共识"环节。

**下次实操**：每次重大方向变更前，组长应该主导一份技术提案（问题 / 替代方案 / 选择 / 共识范围），让团队在方向层达成一致再动架构。

### 2. 技术选型必须放在"当时技术坐标"里看（防止用未来标准回评自己）

我做的 LangGraph StateGraph + ReAct + Result Fusion 多智能体在 **2026 年回看**会被人问"为什么不用更自由的 coding agent / agent loop"——但 agent loop + ops safety 这套组合在 **2025.07** 还不完善。

**反思**：我**主动从 LangChain AgentExecutor 自由 loop 转向 LangGraph StateGraph** 是运维严肃场景下的合理工程取舍——不是技术能力不够，而是 ops safety + HITL + multi-agent 可观测性三件套在当时的工程成熟度不支撑自由 loop 路径。

**面试金句**：

> 这个项目在 2025 年 7 月开始时，我先用 LangChain AgentExecutor 试了自由 ReAct loop，但有三个问题：运维场景要求 HITL（重启/回滚不可逆，不能让 agent 自主决定）、多 agent trajectory 失败模式难以收敛、agent loop + ops safety 这套组合当时还不完善。所以**主动转向 LangGraph StateGraph**——显式节点边界 + State 持久化 + 值班长作为系统侧 HITL 检查点，这跟字节跳动同期开源的 DeerFlow 1.0 是同一套思路。这不是不了解 agent loop，是运维场景的主动选择。今天 Claude Code、OpenHands 都成熟了，但我的 LangGraph StateGraph 设计仍能挂在 OpsAgent + Result Fusion 这条主流方向上。

**下次实操**：技术选型决策要写时间戳——"这个选型是 X 时刻基于 Y 技术坐标做出的，核心约束是 Z"。给未来的自己和面试官留一个时代背景的锚点，特别是 ops safety 这类 domain-specific 约束要显式记录。

### 3. 团队架构设计讨论不是"所有人参与都好"

mentor 6 步法说"团队参与越多越好"是有前提的：参与的人需要在相关领域有 context。**算法同学被拉去参与后端架构设计既帮不上忙也不一定能理解，还浪费了他调优算法的时间**。

**下次实操**：架构设计时**按子系统的领域专家小组讨论**，不是 6 人全员讨论。Agent 设计由算法 + 一名后端，发布系统由后端 + 运维 mentor，前端由前端独立设计后跟其他模块对齐接口。需要"一锤定音的人"在每次讨论卡住时拍板。

### 4. 组长 + 算法双角色的时间分配陷阱

实际比例算法 30% / 协调 70%。我后期接手前后端联调时，算法效果调优直接被搁置。**这不是个好状态**——如果重做我会主动把联调任务在团队内重新分发而不是自己扛。

### 5. 路演必须从听众反推

第一次路演失败的核心是"成员对产品完整形态把握不充分 + 没思考听众知识储备"。导师们的反馈极尖锐：**"如果上下文太长，模型能否抓取到最核心的内容？" "汇报时最重要的是让观众听懂"**。

**下次实操**：路演 PPT 第一页就是"我们解决的问题 + MVP 边界 + 核心 demo"，技术细节延后到 Q&A 才展开。

### 6. Agent 模块在产品需求反复调整下注定难以收敛

Agent 设计依赖明确的输入输出契约（什么数据进来 / 输出给谁用 / 边界是什么）。**产品形态调整三次，每次 Agent 的输入输出契约都跟着变，导致 Agent 内部架构（角色 + SOP）也要不断调整**。

**下次实操**：Agent 模块开发应该在产品形态明确后才启动详细设计，**或者先做一个 toy demo 不绑定具体产品形态，等产品确定后再做生产级实现**。

### 7. 缺 AgentOps 视角是端到端联调失败的隐藏原因（事后审视）

详见 `KNOWLEDGE/agent/agentops-vs-opsagent/` + `KNOWLEDGE/agent/agent-failure-attribution/`——我做的是 **OpsAgent**（用 agent 做运维），但 agent 自己挂掉时**没有 AgentOps 视角去 debug agent 系统本身**。

**具体缺什么**：

- Agent trajectory 的可观测性（每步 thought / action / observation 的结构化记录虽有，但没做异常检测）
- Failure Attribution 机制（端到端跑挂了，定位是哪个 agent / 哪一步首次引入错误的能力）
- Checkpoint / rollback 能力（agent 多步推理失败后没法回滚到具体步骤重跑）

**下次实操**：做 OpsAgent 时就要 co-design AgentOps——agent 系统本身需要可观测、可归因、可回滚的运行时支持。**这是我后续做 Claude Code procedural memory 研究的起点之一**——从"用 agent 做运维"转向"运维 agent 系统本身"。

## 相关知识

- KNOWLEDGE 节点：
  - `KNOWLEDGE/agent/multi-agent/`——multi-agent 何时该用何时不该用（你做的 5 个角色 agent 是按职责拆 + 类比"人类运维团队"，对照 Cloud Code 的"按阶段拆"）
  - `KNOWLEDGE/agent/agent-role-isolation/`——按阶段拆 + 三维隔离（Cloud Code 实操，你的项目按职责拆是另一种拆法）
  - `KNOWLEDGE/agent/context-engineering/`——上下文工程 6 层（你的 MCP 动态查询 = Just-in-time Context）
  - `KNOWLEDGE/agent/agent-tool-design/`——工具设计三原则（你的 MCP 工具集 = 按需发现）
  - `KNOWLEDGE/agent/structured-output/`——你的 agent 间用 JSON 结构化传递信息（demo.md 里每个 agent 的输出 schema 都定义了 agent_type / status / summary / data / plan）
- 学术沉淀节点（关键内容已内化到 KNOWLEDGE，本页是工业实践案例）：
  - `KNOWLEDGE/agent/agentops-vs-opsagent/`——两个方向的本质区分（OpsAgent / AgentOps）
  - `KNOWLEDGE/agent/multi-agent-rca-paradigm/`——本项目对应的工业范式（三件套：角色拆分 + Result Fusion + SOP 嵌入）
  - `KNOWLEDGE/agent/agent-failure-attribution/`——本项目当时缺失但应该有的能力
- 方法论沉淀节点：
  - `KNOWLEDGE/methodology/architecture-design-six-steps/`——本项目走的 6 步法 SOP
  - `KNOWLEDGE/methodology/three-tier-decision-docs/`——本项目缺失的"技术提案"层在哪
- 相关问题页（建议建）：
  - `PROBLEMS/multi-agent-decomposition-axis/`——你的"按职责（运维专家 / 数据 agent / 值班长 / 输出）拆"vs Cloud Code"按阶段（explore / plan / implement / verify）拆"vs Flow-of-Action"按工作流角色（Main / Action / Judge / Ob）拆"——多智能体拆分轴的横向对比页（高频面试题）
  - `PROBLEMS/multimodal-fusion-paradigms/`——Result Fusion / Model Fusion / Feature Fusion 的工业落地 vs 学术上限对比

## 当前状态

`done`（实习已结束，复盘完成）

## 简历素材（建议替换 CV 当前的七牛云段）

> ⚠️ **重要提示**：CV 当前的七牛云 bullet 包含两处需要修正——
>
> 1. **删除 RocketMQ 内容**（你确认未设计进去，没真实做过）
> 2. **加上 MVP / Mock / 未上线的真相**——投递层面可以保持工作量描述，但面试深问必须如实

**建议替换为**：

- 作为项目组长协调前后端、运维、算法 6 名同学，遵循"明确产品定位 → 定义产品原型与原型图 → 定义功能 API → 完成数据表设计 → 进行模块拆分 → 模块详细设计"的架构设计 6 步法，**经历产品形态三次重大调整后由 CEO 拍板收敛 MVP**，区分技术提案 / 架构设计 / 实现设计三类决策层级文档，推动项目从立项到 milestone 路演的全流程联调。
- 负责"指标下钻分析"AI 子系统的设计与实现：基于 **LangGraph StateGraph** 编排的 **L1（任务规划 + 类别判断 + 决策）/ L2（日志 / 指标 / Tracing 三个专门 agent）/ L3（通用专家 + 语言专家）三层多智能体架构**，通过 **MCP Server（部署在函数计算）** 标准化封装日志 / 指标 / 链路 / CMDB 拓扑等工具，使大模型按需动态查询多源运维数据。
- 在灰度发布场景下设计了**多版本并行灰度策略（5% → 30% → 100% 三阶段 + 异常时逐层回溯到最近稳定版本）**，并设计外部告警系统与本系统的数据中间层，实现"同一服务不同版本"动态告警阈值调整机制。
- 设计 **Go + Python 微服务架构**——Go 主流程 + Python 异常检测微服务（STL 分解 + 百分位数检测），通过 HTTP API 解耦，使算法模块独立迭代和部署。**MVP 阶段基于 Mock 系统验证完整闭环逻辑，未接入生产环境**。

## 面试故事（STAR 派生）

行为题（讲经历）：

- `CAREER/interview-bank/behavioral/qiniu-ceo-pivot-decision.md`——CEO 拍板那一刻 / 产品形态共识失败的复盘
- `CAREER/interview-bank/behavioral/qiniu-team-turbulence-handoff.md`——人员动荡 + 接手前后端联调 + 算法调优取舍
- `CAREER/interview-bank/behavioral/qiniu-roadshow-emergency-rescue.md`——路演前进度不达预期、加班补救让最终路演超预期

技术题（讲选型 / 反思）：

- `CAREER/interview-bank/technical/qiniu-agent-loop-vs-workflow.md`——为什么选 LangGraph StateGraph 而不是自由 agent loop
- `CAREER/interview-bank/technical/qiniu-multi-agent-decomposition.md`——为什么这样拆 agent + 对照 Flow-of-Action
- `CAREER/interview-bank/technical/qiniu-multimodal-fusion-paradigm.md`——Result Fusion vs Model Fusion vs Feature Fusion
- `CAREER/interview-bank/technical/qiniu-opsagent-vs-agentops.md`——OpsAgent vs AgentOps + 你做的项目缺什么
