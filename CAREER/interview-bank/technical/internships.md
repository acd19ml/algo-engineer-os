# 面试深挖题：两段实习

> 对 `cv.md` 实习栏（七牛云 + Neo）每条 bullet 的可能追问派生。

---

## C. 七牛云 — AI 算法工程师 / 项目组长

### C1. 组长 + 架构设计 6 步法 + 三类设计文档

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 你作为组长具体协调什么？6 个人怎么分工？ | 团队 = 算法 1（我）+ Agent 设计 1 + Mock 系统 2 + 时序检测 1 + 1 mentor 运维专家；我作为组长 + Agent 设计 + 后端联调（后期）的主 owner，每日晨会推进 + 协调前后端 + 联调 Mock 系统 + 路演 PPT | ⚠️ 准备具体到周例会节奏 |
| 6 步法（产品定位 → 原型图 → API → 数据表 → 模块拆分 → 模块详细设计）的核心动机？ | 每一步在解决上一步留下的、推进不下去的问题：定位决定原型；原型决定 API 形状；API 决定数据表关系；数据表决定模块边界——**避免推倒重来** | KB: `KNOWLEDGE/methodology/architecture-design-six-steps/` |
| 你说的"区分技术提案 / 架构设计 / 实现设计三类决策层级文档"——这三类具体什么区别？ | **技术提案**："该不该做"（动机、替代方案、共识）；**架构设计**："系统怎么组织"（组件、控制流、部署）；**实现设计**："具体怎么落地"（API、schema、状态机）；**决策层级不同，不是详略不同** | KB: `KNOWLEDGE/methodology/three-tier-decision-docs/` |
| 你举一个三类文档的实际例子？ | 实训项目里：**技术提案** = "ZeroOps 该做成对话辅助 / 无人替代 / 灰度发布管理 三选哪个？"（团队级方向决策——这一层我们当时缺位是教训）；**架构设计** = "LangGraph StateGraph L1/L2/L3 多智能体的边界 + Result Fusion 多模态融合范式选型"；**实现设计** = "告警阈值调整工具的 API + 数据表 ddl + 5 个 agent 的 prompt 结构 + JSON 输出 schema" | ✅ 已对齐新 CV |
| 6 步法里哪一步最难？踩过什么坑？ | "产品定位 → 原型图" 这一步——容易陷入伪需求（某功能用技术手段解决比做成产品功能更合理）；要警惕过度设计（设计了实际不会用的功能）；我们项目三次方向变更全卡在这一步 | KB: `KNOWLEDGE/methodology/architecture-design-six-steps/`（"避免过度设计 + MVP 思想"段） |
| 三类文档现在 AI 都能生成——你怎么看？ | AI 生成不区分类别——容易把"该不该做"和"具体怎么实现"混在一份文档里。**人的工作变成识别 AI 生成的是哪一类、缺哪一类**——所以三类划分反而比 AI 时代之前更重要 | KB: `KNOWLEDGE/methodology/three-tier-decision-docs/`（"AI 生成混合层级文档"段 Open Question） |

### C2. LangGraph StateGraph L1/L2/L3 多智能体 + MCP 工具集（取代旧的"Supervisor → Sub Agents"叙事）

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 5 个角色 agent 怎么决定下一步派哪个？ | 任务规划 agent（"运维专家"）解析告警 + 生成 SOP 步骤计划（拓扑定位 → 指标验证 → 日志取证 → 根因推断）+ 调度指令；3 个数据 agent（Metric / Log / Trace）各自处理单一模态；值班长 agent **不获取数据**只对已有证据做结构化推理 + 停止判断；最终输出 agent 生成结构化报告 | KB: `PROJECTS/work/qiniu-zeroops-rca-agent/` "三件套之一"段 + `KNOWLEDGE/agent/multi-agent-rca-paradigm/` |
| 数据 agent 失败时怎么处理？ | (a) 工作流内置重试 + 上下文压缩；(b) 值班长 agent 评估证据充分性，若证据不足或冲突会重构问题表述发起新一轮；(c) 工作流引擎支持循环 + 条件分支 + 超时控制 | KB: `KNOWLEDGE/agent/multi-agent-rca-paradigm/` "ReAct 性能优化路径"段 |
| 工具集（日志 / 指标 / 链路 / CMDB 拓扑）怎么注册？标准化方式？ | **MCP Server**（部署在函数计算上）——每个工具暴露 schema（参数、返回、错误码）；agent 通过 MCP 协议动态调用；这跟"内部 tool registry"思路一致但用标准 MCP 协议 | KB: `KNOWLEDGE/agent/agent-tool-design/` + `KNOWLEDGE/agent/structured-output/` |
| 你为什么选**按职责拆 + Result Fusion**而不是单 agent + 多 tool？ | 三个原因：(a) 上下文爆炸——多模态数据全塞一个 agent 会撑爆 context；(b) 调试黑盒——错了不知道哪步错；(c) 团队中非算法成员要能接手——按职责拆 + JSON 结构化输出便于显式调试。**这跟学术界 Flow-of-Action (WWW 2025) 的 Main/Action/Judge/Ob 角色拆分高度同构** | KB: `KNOWLEDGE/agent/multi-agent-rca-paradigm/` "三件套"段 |
| 你的多智能体设计跟 Cloud Code 那种"按阶段拆（explore/plan/implement/verify）"区别在哪？ | 项目是根因分析任务——主要"信息收集 + 推理"，**没有 implement/verify 阶段**——所以按数据源 + 推理角色拆比按阶段拆更直观。同时类比"人类运维团队"对非算法 mentor 更易理解 | KB: `KNOWLEDGE/agent/agent-role-isolation/`（Cloud Code 按阶段拆）+ `KNOWLEDGE/agent/multi-agent-rca-paradigm/`（按职责拆） |
| Result Fusion / Model Fusion / Feature Fusion 三种范式你为什么选 Result Fusion？ | 工业落地友好：日志/指标/调用链已有成熟工具（SLS / Prometheus / ARMS），转告警事件后 LLM 直接读；Model Fusion 上限更高但需要训练融合模型 + 标注数据，MVP 阶段做不起 | KB: `KNOWLEDGE/agent/multi-agent-rca-paradigm/` "三件套之二"段；技术深问：`CAREER/interview-bank/technical/qiniu-multimodal-fusion-paradigm.md` |

### C3. 为什么选 LangGraph StateGraph 而不是 agent loop（取代旧的"RocketMQ 异步事件驱动"叙事——RocketMQ 未真实使用）

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 你为什么选 LangGraph StateGraph 而不是 agent loop / coding agent 范式？ | **三段式**：(1) **运维场景特殊性**——重启/回滚不可逆，自由 loop 自主执行不可接受，必须有显式 HITL plan approval；(2) **真实选型路径**——项目初期先试 LangChain AgentExecutor 自由 ReAct loop → 主动放弃（三问题：①HITL 缺位、②多 agent trajectory 错误传播/上下文失控/循环不终止、③agent loop + ops safety 组合 2025.07 不完善）→ 转向 LangGraph StateGraph；(3) **LangGraph 具体收益**——显式节点边界 + State 类持久化 + interrupt HITL 检查点 + 单节点可单测。**与字节跳动 DeerFlow 1.0（2025.05）同架构**：Coordinator→Researcher×N→Reporter + HITL interrupt。**金句**："运维跟 coding agent 的本质区别是动作不可逆——重启/回滚不能让 agent 自己决定，必须有 HITL" | KB: `CAREER/interview-bank/technical/qiniu-agent-loop-vs-workflow.md`（完整答案 + 金句） |
| DAG / StateGraph / 自由 loop 本质区别？ | DAG = 完全静态，节点数据流预定义；**LangGraph StateGraph = 半静态（节点固定）+ 半动态（ReAct 循环 + conditional edge）**；自由 Agent Loop = 完全动态，每步由模型自主决定。本项目选 StateGraph = 在运维严肃场景下用结构化可控性换灵活性 | KB: `CAREER/interview-bank/technical/qiniu-agent-loop-vs-workflow.md` "我答不出的部分" 段 |
| **ReAct 模式三大痛点怎么解决？量化效果？** | 三痛点：延迟高 / token 爆炸 / 循环不终止。四件事：(a) **显式总结工具 ExplicitSummary**——agent 判断"证据充分"时主动调用终止循环；(b) **智能终止**——连续 2 轮 Observation 语义相似度 >0.92 → 强制终止；(c) **上下文压缩**——Observation >500 token 时 mini-model 压缩到 <150 token 摘要；(d) **减少无效循环**——prompt 禁止连续调同一工具超过 2 次 + max_turns=12 兜底。**量化**：平均轮次 8.3→4.1，token 降 38%，P50 75s→28s | KB: `PROJECTS/work/qiniu-zeroops-rca-agent/mock-system-design.md` §四 步骤7 |
| **20%→70% 是怎么测的？"成功"怎么定义？** | **10 个 test case（3类）**，成功 = **根因服务 + 故障类型双命中**。例："RDS-Order 的 DB 连接池耗尽"✓ / "订单服务有数据库问题"✗（类型模糊）。评测人：实习生 + 队友独立打分，mentor 王昶敏仲裁争议 case。**20% baseline**：2/10（单信号直接命中）；4 个多跳 case 全失败（无CMDB）；3 个灰度 case 全失败（无pod→version映射） | KB: `PROJECTS/work/qiniu-zeroops-rca-agent/mock-system-design.md` §三 |
| **7 步优化里哪步提升最大？** | 步骤 1 **CMDB 集成 +20%**（质变：多跳从"必然失败"→"有可能成功"）；步骤 2 **时间中心化 +12%**（消灭硬错误：心算时间 → 工具空返回 → 必然失败；修了就通）。步骤 3-7 各 +1-8%（量变）。**金句**："CMDB 是从瞎猜到有依据的质变，时间中心化是消灭硬错误" | KB: `PROJECTS/work/qiniu-zeroops-rca-agent/mock-system-design.md` §四 |
| 如果今天重做你会改吗？ | 会重新评估 agent loop——Claude Code / OpenHands harness 体系成熟，agent loop + 内置 HITL + failure attribution 三件套完整。**但 2025.07 技术坐标下，LangGraph StateGraph 在运维严肃场景仍是正确选择**——StateGraph 的结构化可控性在 HITL 硬约束 + 多 agent 可调试要求下是合理取舍 | KB: `KNOWLEDGE/agent/agentops-vs-opsagent/`（AgentOps 视角反观自己项目的局限） |
| 你的多 agent 系统当时挂掉怎么 debug？ | 老实承认：当时主要靠 **LangGraph StateGraph 节点边界**（每个节点显式 typed input/output）+ 每个 agent 的 JSON 结构化输出做事后定位——**没有专门的 failure attribution 机制，连"挂在哪一类异常"都没法系统化标**。**系统化答案 = 三件套**：(a) 11 类 anomaly taxonomy（Intra-Agent 5 + Inter-Agent 6，先有分类才能埋点）；(b) failure attribution（Who&When / FAMAS / Echo / Correct）；(c) failure trajectory dataset（标准化 schema + 多 benchmark + 标注流水线，让单次 debug 升级成长期改进基础设施）。这三件项目当时一件都没有 | KB: `KNOWLEDGE/agent/agent-failure-attribution/` + `KNOWLEDGE/agent/agent-anomaly-taxonomy/` + `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`；技术深问：`CAREER/interview-bank/technical/qiniu-opsagent-vs-agentops.md` |

### C4. 体检中心 + 双路径 + 同一服务不同版本动态阈值

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 为什么需要按版本？ | 同一服务发布新版本后错误率/延迟基线可能变化——静态阈值导致 v1.2 一上线就大量误报（功能更多本来就占更多内存）。按版本动态阈值让告警跟随版本演化，精准区分"v1.1 正常 / v1.2 异常" | ✅ |
| **动态阈值调整的具体机制？** | 数据中间层是 **`alert_rule_metas` 表**（service + version + metric + threshold + original_threshold + adjusted_at）。流程：体检中心（Go）定时巡检 → Python 微服务 STL 分解 + 百分位数检测 → 发现异常但绝对告警未触发 → 更新 `alert_rule_metas.threshold` → 监控 Adapter 下次推送告警规则时读表 → Prometheus 更新规则 → 阈值生效。**灰度场景用灰度机 vs 稳定机百分位数对比**（不依赖历史数据），稳定服务用 STL（需历史数据） | KB: `PROJECTS/work/qiniu-zeroops-rca-agent/mock-system-design.md` §五 |
| **双路径是两个 AI 入口吗？** | **不是**。路径 1（告警驱动）：Prometheus 阈值触发 → 直接进 AI 分析。路径 2（主动巡检）：体检中心发现趋势异常 → 调低阈值 → 问题**提前触发**路径 1 的告警 → 再走路径 1 进 AI。**两条路径最终走同一个 AI 入口**，路径 2 的价值是把"问题被发现"时间窗口提前（Mock 验证：C9 v1.2 内存泄漏提前 15 分钟发现） | KB: `PROJECTS/work/qiniu-zeroops-rca-agent/mock-system-design.md` §五 |
| **STL 对新版本没有历史数据怎么处理？** | 踩过的真实坑：v1.2 刚灰度 5% 时，STL 无法收敛（数据点不足一个完整周期）。**解决**：新版本头 24 小时只用灰度机 vs 稳定机百分位数比较（不依赖历史数据），24 小时后 STL 接管。这是项目实现里真实的冷启动处理 | KB: `PROJECTS/work/qiniu-zeroops-rca-agent/mock-system-design.md` §五 "冷启动坑" |
| 这个设计和告警系统本身的关系？ | 外部告警系统（Prometheus）不知道版本概念——我们做的 `alert_rule_metas` 是"加在它前面"的版本感知层。体检中心修改阈值 → Adapter 同步给 Prometheus → 原有告警机制照跑，对 Prometheus 透明 | ✅ |

---

## D. Neo 智能经济 — AI Agent 开发工程师

### D1. DeepResearch 多智能体

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| DeepResearch 的核心难点是什么？ | (a) 意图理解——用户问题往往含糊；(b) 工具编排——什么时候搜索、什么时候抓取、什么时候执行代码；(c) 信息聚合——多源信息怎么合并、避免重复 | KB: `agent/agent-engineer-ability/`（4 件核心事） |
| 工具集成的标准化方式？ | tool 抽象层——每个 tool 实现 `__call__(input) -> output` 接口；统一的 error handling + timeout + retry；tool 调用由 LLM 决策 | ⚠️ |

### D2. ReAct + mem0 + FAISS + 区块链问答 + 3072 维语义路由

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| mem0 是什么？和你研究里的记忆有什么区别？ | mem0 是开源 long-term memory framework，偏 fact extraction + storage + retrieval；Neo 中可讲作对话长期记忆。自主研究里的 procedural / workflow memory 更关注“怎么执行任务”的可复用步骤，两者粒度和用途不同：一个偏事实与偏好，一个偏可执行过程。 | `CAREER/interview-bank/technical/main-project-and-research.md` |
| FAISS 选型理由？为什么不用 Pinecone（你也用了 Pinecone）？ | FAISS 是本地内存索引——用于**对话内**短期文档；Pinecone 是托管 vector DB——用于**跨对话**长期 API 工具描述（62 种工具的 3072 维向量）；本地 vs 托管的 trade-off | ⚠️ |
| 3072 维向量编码 62 种工具方法描述——为什么 3072 维？为什么不用更小？ | 用的是 OpenAI text-embedding-3-large，原生 3072 维；可以 truncate 到更小但 (a) 工具方法描述语义细微差异多，3072 维区分度更好 (b) 一次性 62 个工具的小规模索引，3072 维内存可以接受 | KB: `transformer/qkv-three-matrix-design/`（低秩约束相关） |
| 延迟初始化动态构建索引具体怎么做？ | (a) 工具方法描述变更触发增量 embedding；(b) 索引在第一次请求时才 build（避免冷启动慢）；(c) 索引 versioned——更新时新旧并存、切换原子 | ⚠️ 准备具体 |
| 两阶段检索 Top10 → Top5 精排——精排用什么模型？ | Top10 用 cosine similarity 粗筛；Top5 用 cross-encoder（小模型如 bge-reranker）做精排；精排捕获 query-tool 交互信号而不只是相似度 | ⚠️ |
| **98% 意图匹配准确率怎么算的？ground truth 从哪来？** | 测试集 = 人工标注的 (用户 query, 正确工具) 对；准确率 = 系统选中正确工具的比例；测试集多大？覆盖率怎样？这是关键 | ⚠️ **Gap: 准备具体数字** |
| **70% 成本降——baseline 是什么？** | **baseline = 把所有工具（62 种）描述一次性塞进 prompt 让 LLM 选** → token 成本高且 LLM 在 60+ 工具中决策准确率下降；优化后 = 先用 embedding 召回 Top10 → cross-encoder 精排 Top5 → 只把 5 个工具描述塞进 prompt → token 数大幅下降，成本降 70% | ✅ 已 confirm |
| 实时批量索引更新具体怎么做？ | (a) 工具变更触发事件 → 入队列；(b) 后台 worker 批量消费 → 重新 embedding；(c) 新索引 build 完后原子替换；(d) 期间用旧索引继续服务，避免 downtime | ⚠️ |

### D3. 开源 SDK 260+ stars + 海外社区运营

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 你贡献了哪些核心模块？具体几个 commit？ | 同步 / 异步执行工具、Graph 工具、链上对象存储工具、钱包加密工具——主要在 tool integration 层；commit 数量 ⚠️ 准备数字 | ⚠️ 准备具体 |
| 海外社区运营具体做什么？ | (a) 处理 GitHub Issues（响应时间 24h 内）；(b) Review PR（每周 N 个）；(c) 撰写开发者文档；(d) 在 Discord / Telegram 回复用户问题；(e) 撰写多语言 README | ⚠️ 准备具体数字（Issues N 个、PR N 个） |
| 你怎么和海外开发者协作？沟通用什么语言？ | 英文为主——文档、Issues、PR review 都英文；时差通过异步沟通解决（Issue 留言 + PR review comments）；遇到重大决策开 Discord 会议 | 不需要 KB |
| 这个项目的国际用户主要是哪些？ | 区块链开发者社区——主要是欧洲 + 北美的 web3 开发者 | ⚠️ |

### D4. 子账户系统（多签 + 资金配额）

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 子账户和主账户的隔离机制？ | (a) 子账户私钥独立（不能从主账户私钥推出）；(b) 多重签名（n-of-m 才能动用大额）；(c) 资金配额（子账户单笔 + 单日上限） | ⚠️ |
| Turnkey 是什么？为什么用它？ | Turnkey 是 wallet infrastructure 提供商——提供 private key 的 HSM 级管理；选它的原因：(a) 私钥不落地（在 Turnkey 端加密），(b) 我们只通过 API 触发签名，(c) 满足合规审计要求 | ⚠️ |
| LLM 驱动自动交易的安全考虑？ | (a) LLM 决策与签名分离——LLM 只产生 intent，签名前必须过规则引擎（金额上限 / 黑名单 / 频率）；(b) 子账户隔离——LLM 错了也不能动主账户；(c) 全链路审计 trace | KB: `agent/structured-output/`（约束解码 + 验证重试） |

---

## 通用追问（适用于两段实习）

| 追问 | 答题要点 |
|---|---|
| 你两段实习的最大区别是什么？ | Neo 是开源应用层（工具集 + ReAct），偏 framework / 工具型；七牛云是企业内部全栈（架构 + 多 agent + 中间件），偏系统型 + 协作型——两段经验互补：Neo 让我对工具集成 + 海外协作有 feel，七牛云让我对生产级系统设计 + 异步架构 + 业务流程有 feel |
| 实习中最大的失败 / 踩坑是什么？ | （需要准备一个具体故事——非泛泛而谈） |
| 最自豪的设计 / 决策？ | （需要准备：比如 Neo 70% 成本降的语义路由设计 / 七牛云 LangGraph StateGraph L1/L2/L3 多智能体 + Result Fusion 范式让根因定位成功率从 20% 迭代到约 70%；或者 CMDB 集成 + 时间中心化这两步一共 +32% 的两大跳跃点叙事） |
| 为什么离开 / 来这边？ | （准备 transition story——通常是"想做更前沿的 agent 训练 + 评测，所以来实习更深入的方向"） |

---

## 还需要派生的：STAR 故事

每段实习派生 2-3 个 STAR 故事（背景 / 任务 / 行动 / 结果）放 `interview-bank/behavioral/`：

| 故事 | 适用 |
|---|---|
| 七牛云：CEO 拍板 / 团队共识失败的复盘 | 行为面（领导力 / 协作） | ✅ 已派生 `CAREER/interview-bank/behavioral/qiniu-ceo-pivot-decision.md` |
| 七牛云：人员动荡 + 接手前后端联调 + 算法调优取舍 | ownership / 工程取舍 | ✅ 已派生 `CAREER/interview-bank/behavioral/qiniu-team-turbulence-handoff.md` |
| 七牛云：路演前进度不达预期 + 加班补救让最终路演超预期 | 极限交付 / 优先级判断 | ✅ 已派生 `CAREER/interview-bank/behavioral/qiniu-roadshow-emergency-rescue.md` |
| Neo：3072 维语义路由的设计决策过程 | 系统设计能力 | 待派生 |
| Neo：海外社区某次冲突 / 协作 | 跨文化协作 | 待派生 |
| 自主研究：从 AWM 复现踩到 boundary 边界 → 形成 Agent Memory 评测方法论 | 研究能力 + 工程化能力 | 待派生 |
