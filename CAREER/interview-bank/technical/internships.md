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
| 你举一个三类文档的实际例子？ | 实训项目里：**技术提案** = "ZeroOps 该做成对话辅助 / 无人替代 / 灰度发布管理 三选哪个？"（团队级方向决策——这一层我们当时缺位是教训）；**架构设计** = "Dify L1/L2/L3 多智能体的边界 + Result Fusion 多模态融合范式选型"；**实现设计** = "告警阈值调整工具的 API + 数据表 ddl + 5 个 agent 的 prompt 结构 + JSON 输出 schema" | ✅ 已对齐新 CV |
| 6 步法里哪一步最难？踩过什么坑？ | "产品定位 → 原型图" 这一步——容易陷入伪需求（某功能用技术手段解决比做成产品功能更合理）；要警惕过度设计（设计了实际不会用的功能）；我们项目三次方向变更全卡在这一步 | KB: `KNOWLEDGE/methodology/architecture-design-six-steps/`（"避免过度设计 + MVP 思想"段） |
| 三类文档现在 AI 都能生成——你怎么看？ | AI 生成不区分类别——容易把"该不该做"和"具体怎么实现"混在一份文档里。**人的工作变成识别 AI 生成的是哪一类、缺哪一类**——所以三类划分反而比 AI 时代之前更重要 | KB: `KNOWLEDGE/methodology/three-tier-decision-docs/`（"AI 生成混合层级文档"段 Open Question） |

### C2. Dify L1/L2/L3 多智能体 + MCP 工具集（取代旧的"Supervisor → Sub Agents"叙事）

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 5 个角色 agent 怎么决定下一步派哪个？ | 任务规划 agent（"运维专家"）解析告警 + 生成 SOP 步骤计划（拓扑定位 → 指标验证 → 日志取证 → 根因推断）+ 调度指令；3 个数据 agent（Metric / Log / Trace）各自处理单一模态；值班长 agent **不获取数据**只对已有证据做结构化推理 + 停止判断；最终输出 agent 生成结构化报告 | KB: `PROJECTS/work/qiniu-zeroops-rca-agent/` "三件套之一"段 + `KNOWLEDGE/agent/multi-agent-rca-paradigm/` |
| 数据 agent 失败时怎么处理？ | (a) 工作流内置重试 + 上下文压缩；(b) 值班长 agent 评估证据充分性，若证据不足或冲突会重构问题表述发起新一轮；(c) 工作流引擎支持循环 + 条件分支 + 超时控制 | KB: `KNOWLEDGE/agent/multi-agent-rca-paradigm/` "ReAct 性能优化路径"段 |
| 工具集（日志 / 指标 / 链路 / CMDB 拓扑）怎么注册？标准化方式？ | **MCP Server**（部署在函数计算上）——每个工具暴露 schema（参数、返回、错误码）；agent 通过 MCP 协议动态调用；这跟"内部 tool registry"思路一致但用标准 MCP 协议 | KB: `KNOWLEDGE/agent/agent-tool-design/` + `KNOWLEDGE/agent/structured-output/` |
| 你为什么选**按职责拆 + Result Fusion**而不是单 agent + 多 tool？ | 三个原因：(a) 上下文爆炸——多模态数据全塞一个 agent 会撑爆 context；(b) 调试黑盒——错了不知道哪步错；(c) 团队中非算法成员要能接手——按职责拆 + JSON 结构化输出便于显式调试。**这跟学术界 Flow-of-Action (WWW 2025) 的 Main/Action/Judge/Ob 角色拆分高度同构** | KB: `KNOWLEDGE/agent/multi-agent-rca-paradigm/` "三件套"段 |
| 你的多智能体设计跟 Cloud Code 那种"按阶段拆（explore/plan/implement/verify）"区别在哪？ | 项目是根因分析任务——主要"信息收集 + 推理"，**没有 implement/verify 阶段**——所以按数据源 + 推理角色拆比按阶段拆更直观。同时类比"人类运维团队"对非算法 mentor 更易理解 | KB: `KNOWLEDGE/agent/agent-role-isolation/`（Cloud Code 按阶段拆）+ `KNOWLEDGE/agent/multi-agent-rca-paradigm/`（按职责拆） |
| Result Fusion / Model Fusion / Feature Fusion 三种范式你为什么选 Result Fusion？ | 工业落地友好：日志/指标/调用链已有成熟工具（SLS / Prometheus / ARMS），转告警事件后 LLM 直接读；Model Fusion 上限更高但需要训练融合模型 + 标注数据，MVP 阶段做不起 | KB: `KNOWLEDGE/agent/multi-agent-rca-paradigm/` "三件套之二"段；技术深问：`CAREER/interview-bank/technical/qiniu-multimodal-fusion-paradigm.md` |

### C3. 为什么选 Dify 工作流而不是 agent loop（取代旧的"RocketMQ 异步事件驱动"叙事——RocketMQ 未真实使用）

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 你为什么选 Dify 工作流而不是 agent loop / coding agent 范式？ | **时代背景**：2025.07-10 当时市面上还没有开源 agent loop 系统（Claude Code / Codex / Cursor Agent 等都是后涌现）+ 上下文工程刚兴起 + 最火是基于 DAG 的 DeepResearch。**项目初期试过 agent loop → 调试困难 → 主动退到工作流**——用工作流可调试性换 agent loop 灵活性的 ROI 取舍 | KB: `CAREER/interview-bank/technical/qiniu-agent-loop-vs-workflow.md`（完整答案 + 金句） |
| 工作流的 ReAct 性能问题怎么解决？ | 四件事：(a) 减少不必要循环——前置数据处理减少无效思考；(b) 上下文压缩 + 精准引用——摘要历史信息；(c) 智能终止判断——值班长 agent 评估证据充分性；(d) 显式总结工具——任务完成时调用总结工具生成结构化报告 | KB: `KNOWLEDGE/agent/multi-agent-rca-paradigm/` "ReAct 性能优化路径"段 |
| 如果今天重做你会改吗？ | 会重新评估 agent loop——Claude Code / Codex / OpenHands 等 harness 这一年涌现成熟，把 agent debug / failure attribution / checkpoint rollback 工程能力都内置了。**但当时退到工作流是对的**——技术坐标决定 | KB: `KNOWLEDGE/agent/agentops-vs-opsagent/`（AgentOps 视角反观自己项目的局限） |
| 你的多 agent 系统当时挂掉怎么 debug？ | 老实承认：当时主要靠 Dify 工作流的可视化 + 每个 agent 的 JSON 结构化输出做事后定位——**没有专门的 failure attribution 机制，连"挂在哪一类异常"都没法系统化标**。**系统化答案 = 三件套**：(a) 11 类 anomaly taxonomy（Intra-Agent 5 + Inter-Agent 6，先有分类才能埋点）；(b) failure attribution（Who&When / FAMAS / Echo / Correct）；(c) failure trajectory dataset（标准化 schema + 多 benchmark + 标注流水线，让单次 debug 升级成长期改进基础设施）。这三件项目当时一件都没有 | KB: `KNOWLEDGE/agent/agent-failure-attribution/` + `KNOWLEDGE/agent/agent-anomaly-taxonomy/` + `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`；技术深问：`CAREER/interview-bank/technical/qiniu-opsagent-vs-agentops.md` |

### C4. 同一服务不同版本动态阈值

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 为什么需要按版本？ | 同一服务发布新版本后，错误率 / 延迟基线可能变化（功能更多或性能不同）——用一套静态阈值会**新版本一上线就大量误报**；按版本动态阈值能让告警跟随版本演化 | ⚠️ 业务理解 |
| 阈值动态调整的具体机制？ | 数据中间层观察新版本上线后的 N 个时间窗口（比如 1h / 6h / 24h）数据 → 用统计方法（均值 ± k 倍标准差，或基于历史版本对比）算新阈值 → 持续更新 | ⚠️ 准备具体算法 |
| 这个设计和告警系统本身的关系？ | 外部告警系统不知道版本概念——我们做的中间层是"加在它前面"的版本感知层：拦截原始指标 → 按版本归一化 → 再喂给告警系统 | 系统设计思考 |

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
| mem0 是什么？和你自己设计的记忆有什么区别？ | mem0 是开源 long-term memory framework，提供 fact extraction + storage + retrieval；我们用它做短期 + 长期对话记忆；自己设计的 procedural memory（主项目）是 **task-level 的工作流记忆**——两者粒度和用途不同 | ⚠️ 准备讲清两者边界 |
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
| 最自豪的设计 / 决策？ | （需要准备：比如 Neo 70% 成本降的语义路由设计 / 七牛云 Dify L1/L2/L3 多智能体 + Result Fusion 范式让根因定位成功率从 20% 迭代到约 70%） |
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
| 自主研究：从 AWM 复现踩到 boundary 边界 → 设计主项目的故事 | 研究能力 + 工程化能力 | 待派生 |
