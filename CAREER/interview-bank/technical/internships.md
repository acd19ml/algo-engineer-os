# 面试深挖题：两段实习

> 对 `cv.md` 实习栏（七牛云 + Neo）每条 bullet 的可能追问派生。

---

## C. 七牛云 — AI 算法工程师 / 项目组长

### C1. 组长 + 架构设计 6 步法 + 三类设计文档

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 你作为组长具体协调什么？6 个人怎么分工？ | 前端 2 + 后端 2 + 运维 1 + 算法 1（我）；我作为算法 + 架构 owner，协调 (a) 各端接口对齐 (b) 数据表设计 review (c) LLM 应用边界（哪些用 LLM、哪些用确定性逻辑兜底） | ⚠️ 准备具体到周例会节奏 |
| 6 步法（产品定位 → 原型图 → API → 数据表 → 模块拆分 → 模块详细设计）的核心动机？ | 每一步在解决上一步留下的、推进不下去的问题：定位决定原型；原型决定 API 形状；API 决定数据表关系；数据表决定模块边界——**避免推倒重来** | 详见 `INBOX/short-term-plan-for-career/qiniu-intern-record.md`（导师写的） |
| 你说的"区分技术提案 / 架构设计 / 实现设计三类决策层级文档"——这三类具体什么区别？ | **技术提案**："该不该做"（动机、替代方案、共识）；**架构设计**："系统怎么组织"（组件、控制流、部署）；**实现设计**："具体怎么落地"（API、schema、状态机）；**决策层级不同，不是详略不同** | 详见 `INBOX/short-term-plan-for-career/want-to-talk-by-myself-during-interview.md` |
| 你举一个三类文档的实际例子？ | 实训项目里：技术提案 = "ZeroOps 该做成全托管还是工具？"（团队级决策）；架构设计 = "Supervisor 与 Sub-Agents 的边界、和 RocketMQ 的关系"；实现设计 = "告警阈值调整工具的 API + 数据表 ddl" | ⚠️ 准备具体故事 |
| 6 步法里哪一步最难？踩过什么坑？ | "产品定位 → 原型图" 这一步——容易陷入伪需求（某功能用技术手段解决比做成产品功能更合理）；要警惕过度设计（设计了实际不会用的功能） | 详见 qiniu-intern-record.md |
| 三类文档现在 AI 都能生成——你怎么看？ | AI 生成不区分类别——容易把"该不该做"和"具体怎么实现"混在一份文档里。**人的工作变成识别 AI 生成的是哪一类、缺哪一类**——所以三类划分反而比 AI 时代之前更重要 | ⚠️ 自己的判断 |

### C2. Supervisor → Sub Agents 架构 + 工具集

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| Supervisor 怎么决定派哪个 Sub Agent？ | 根据告警类型 + 当前已收集的上下文 → LLM 推理出下一步该用哪类工具 → 对应的 Sub Agent 接管 | KB: `agent/multi-agent/`（按工具领域拆分） |
| Sub Agent 失败时 Supervisor 怎么处理？ | (a) 重试（异步 MQ 自动重试）；(b) Supervisor 收到失败信号后切换 Sub Agent 类型（比如"日志查询"失败就改用"指标查询"）；(c) 累计失败超过阈值 → 升级到人工 | KB: `agent/agent-engineer-ability/`（错误恢复——架构级隔离） |
| 工具集（指标 / 日志 / 异常检测 / 上下游关系 / 阈值调整 / 版本回滚）怎么注册？标准化方式？ | 内部 tool registry（类似 MCP 思路）——每个工具暴露 schema（参数、返回、错误码）；Sub Agent 通过 tool_name 调用；Supervisor 看到的不是工具实现，是工具能力描述 | KB: `agent/structured-output/`（第 3 层 + 第 5 层） |
| 这个 Supervisor 架构和 Anthropic / Manus 的 multi-agent 立场（"按工具拆分而不是按角色拆分"）一致吗？ | 一致——我们的 Sub-Agents 是按工具领域（监控工具组 / 修复工具组）拆，**不是按"工程师 / 运维 / 数据分析师" 这种角色拟人化**——避免了拟人化角色分工的反模式 | KB: `agent/multi-agent/`（关键："把子 agent 当作工具来调用而不是同事") |

### C3. RocketMQ 异步事件驱动

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 为什么用 MQ 不用同步 RPC？ | 同步 multi-agent 在 LLM 调用慢 + 工具调用失败时**串行阻塞**——一个 Sub Agent 卡住会拖累整个 Supervisor；MQ 解耦——Supervisor 发任务到 queue 后立即返回，Sub Agent 异步消费 | ⚠️ 标准答案 |
| 同步 Multi-Agent 的"内存雪崩"具体是什么？ | (a) Supervisor 同步等 Sub Agent 时，自身上下文一直驻留在内存；(b) 多个并发 Sub Agent 失败重试时，老的等待任务没释放、新的又叠上；(c) LLM 调用超时叠加 → 等待协程爆 → OOM 或频繁 GC | ⚠️ 实习中实际遇到的 |
| 失败重试 + 优先级队列怎么实现？ | RocketMQ 的延迟消息 + Topic 按优先级分；失败重试用退避策略（exponential backoff）；保留 trace_id 串联整次任务的所有 retry | ⚠️ 准备具体到代码层 |
| 异步设计带来的新问题？ | (a) 状态同步——Supervisor 不知道 Sub Agent 进度；解决：定期 heartbeat + Supervisor 端 timeout；(b) 结果回传顺序——异步导致结果乱序到达；解决：trace_id 关联 + Supervisor 端 reorder buffer | ⚠️ trade-off 思考 |

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
| 最自豪的设计 / 决策？ | （需要准备：比如 Neo 70% 成本降的语义路由设计 / 七牛云 RocketMQ 异步解耦的雪崩防护） |
| 为什么离开 / 来这边？ | （准备 transition story——通常是"想做更前沿的 agent 训练 + 评测，所以来实习更深入的方向"） |

---

## 还需要派生的：STAR 故事

每段实习派生 2-3 个 STAR 故事（背景 / 任务 / 行动 / 结果）放 `interview-bank/behavioral/`：

| 故事 | 适用 |
|---|---|
| 七牛云：6 步法在某个具体功能上的实操 + 踩坑 | 行为面（领导力 / 协作） |
| 七牛云：异步雪崩的发现 + 解决过程 | 技术深度 + 故障排查能力 |
| Neo：3072 维语义路由的设计决策过程 | 系统设计能力 |
| Neo：海外社区某次冲突 / 协作 | 跨文化协作 |
| 自主研究：从 AWM 复现踩到 boundary 边界 → 设计主项目的故事 | 研究能力 + 工程化能力 |

Week 2 完成 STAR 故事派生。
