# Neo 智能经济 · 多智能体区块链平台（4 子项目）

> Neo 智能经济 2025.02-07 AI Agent 开发工程师实习。5 个月内同时参与 **4 个独立子项目**：
> 1. **DeepResearch 多智能体工作流**
> 2. **ReAct 区块链问答 + 3072 维语义路由**（CV 金字段，含 98% 意图匹配 + 70% 成本降）
> 3. **开源 AI Agent 框架 SDK + 海外社区运营**（260+ stars）
> 4. **LLM 驱动的自动交易子账户系统**
>
> ⚠️ 项目目录命名（`neo-deepresearch-and-react-agent/`）只覆盖了 1/2 子项目的名字，是早期占位。实际仓内涵盖全 4 子项目。

## 项目挖掘状态：⏳ 挖掘中

参考 [Qiniu 项目](../qiniu-zeroops-rca-agent/README.md) 的 4 份文档结构作为终态。**当前 Neo 素材仅 CV 4 条 bullet + `CAREER/interview-bank/technical/internships.md` D 段 17 个追问骨架**——立刻填 4 份文件会大量占位符，所以按 2 + 2 的节奏分阶段建：

| 文档 | 焦点 | 状态 |
|---|---|---|
| **本页 `README.md`** | 4 子项目导航 / 决策复盘骨架 / 时代背景 / 复盘 / 简历素材 / 面试故事入口 / **挖掘 brief（Q1-Q20）** | ✅ 已建 |
| **`interview-defense-matrix.md`** | 10 类×30+ 行 readiness 矩阵（多数 ⚠️/❌，作为起手 baseline）| ✅ 已建 |
| `system-anatomy.md` | 4 子项目系统视图（架构 + 数据流 + 集成关系）| ⏳ 等 Block B+C 答完 |
| `subsystem-react-router.md` | D2 ReAct + 语义路由深度解剖（CV 5 个硬指标的工程实现 + design rationale）—— **面试最值钱** | ✅ 已建 working draft，等 Block C2 补齐 |

## 类型

`work`

## 目标

⏳ Block A 待回答

## 动机

⏳ Block A 待回答（公司业务 + 这个项目要解决什么）

## 范围（4 子项目）

### 子项目 1：DeepResearch 多智能体工作流

**CV 原文**（bullet 1）：

> 构建基于 Python 的 LLM 多智能体工作流 DeepResearch 服务，集成意图识别、任务规划、网页搜索 / 数据抓取 / 代码执行工具。

**已知线索**（from `internships.md` D1）：
- 核心难点是意图理解 + 工具编排 + 信息聚合
- 工具集成有 tool 抽象层（`__call__(input) -> output`），统一 error handling + timeout + retry

⏳ 待挖掘：B1 / C1（完整业务场景 / 编排范式 / 跟 GPT-Researcher / OpenAI Deep Research 的横向对比）

### 子项目 2：ReAct 区块链问答 + 语义路由 ⭐（CV 金字段）

**CV 原文**（bullet 2）：

> 构建 ReAct 模式的 Agent 区块链问答系统：对话管理、短长期记忆（mem0）、本地文档搜索（FAISS）、Pinecone Serverless + OpenAI text-embedding-3-large 集成。设计区块链 API 语义路由系统：3072 维向量编码 62 种工具方法描述、延迟初始化动态构建索引、两阶段检索（Top10 初筛 → Top5 精排），达成 **98% 意图匹配准确率，降低 70% 调用成本**，支持实时批量索引更新。

**已知线索**（from `internships.md` D2 + 你之前的对话）：
- **5 个 CV 硬指标**：62 工具 / 3072 维 / Top10→Top5 / 98% / 70%——这是面试官最容易精确深挖的几个数字
- **3 类 memory 并用**：mem0 = 对话 long-term；FAISS = 对话内短期文档；Pinecone = 跨对话长期 API 工具描述
- **70% 成本降的 baseline 已确认**：原方案 = 把 62 个工具描述一次性塞 prompt 让 LLM 选 → token 成本高 + 60+ 工具中决策准确率下降；新方案 = embedding 召回 Top10 → cross-encoder 精排 Top5 → 只塞 5 个工具描述
- **3072 维选型理由已确认**：OpenAI text-embedding-3-large 原生 3072 维 + 工具描述语义细微差异多 + 62 工具规模可接受
- **延迟初始化策略已确认**：工具描述变更触发增量 embedding / 索引第一次请求才 build / 索引 versioned 原子切换

⏳ 待挖掘：B2 / C2（5 个硬指标的具体来源 + 评测设计 + Pinecone 用法 + cross-encoder 选型 + 实时批量更新工程实现）

### 子项目 3：开源 AI Agent 框架 SDK + 海外社区运营

**CV 原文**（bullet 3）：

> 参与设计与开发开源 AI Agent 框架 SDK（**260+ stars**）及配套工具集 SDK：集成同步 / 异步执行工具、Graph 工具、链上对象存储工具、钱包加密工具，编写测试用例保障可用性。**维护项目海外全球技术社区**：处理 GitHub Issues、Review 海外开发者 PR、撰写并维护开发者文档，与海外开发者协作推进项目演进。

**已知线索**（from `internships.md` D3）：
- 4 个核心模块（同步异步执行 / Graph / 链上对象存储 / 钱包加密）
- 海外社区运营 5 件事：Issues 24h 响应 / PR review / 开发者文档 / Discord+Telegram / 多语言 README
- 沟通用英文为主 / 时差异步沟通 / 重大决策开 Discord 会议
- 国际用户主要是欧洲+北美的 web3 开发者

⏳ 待挖掘：B3 / C3（SDK 仓库链接 + 你贡献的 commit 数 + 社区运营具体数字 + 是 Neo 主仓还是某个 fork）

### 子项目 4：LLM 驱动的自动交易子账户系统

**CV 原文**（bullet 4）：

> 实现 LLM 驱动的自动交易子账户系统：多重签名验证 + 资金配额，在用户托管账户与自动化交易账户之间实施逻辑隔离，通过 Turnkey 对钱包私钥加密存储。

**已知线索**（from `internships.md` D4）：
- 子账户与主账户隔离：私钥独立 / 多重签名 n-of-m / 资金配额（单笔 + 单日上限）
- Turnkey = wallet infrastructure 提供商，提供 HSM 级私钥管理；选它的原因：私钥不落地 + API 触发签名 + 合规审计
- LLM 决策与签名分离——LLM 只产生 intent，签名前必须过规则引擎（金额上限 / 黑名单 / 频率）

⏳ 待挖掘：B4 / C4（具体 n-of-m / 规则引擎实现 / vs Fireblocks / Privy 选型）

## 团队与角色

⏳ Block A3 待回答（report 给谁 / mentor 是谁 / 团队规模 / 4 子项目时间占比）

## 时代背景（2025.02-07 Web3 + Agent 生态）

⏳ Block A5 待回答——参考 [Qiniu README 的"时代背景"段](../qiniu-zeroops-rca-agent/README.md) 那种锚点表。

候选锚点（待你确认 / 补充）：
- 2025 Q1-Q2 **DeepResearch 类项目正热**（基于 DAG 的 GPT-Researcher / OpenAI Deep Research 都在这段时间涌现）
- **LangChain / LangGraph 生态成型** but agent loop 范式还没普及
- **MCP 协议未发布**（2025 年底才出）—— 当时工具集成主流是 Function Calling
- **mem0 还是早期项目**（你用 mem0 时它可能 1.0 都没到）
- **Pinecone Serverless 刚推出**（2024 年底，2025 上半年还在早期生产实践阶段）
- Anthropic Skills / Codex / Cursor Agent 都没出现

## 真实的技术选型路径（按子项目）

⏳ 待挖掘——每子项目"为什么选 X 不选 Y"

候选挖掘方向：
- **DeepResearch**：为什么用自研多智能体不直接用 GPT-Researcher / LangChain Agent / 当时火的 AutoGen？
- **D2**：为什么 ReAct 不是 Plan-And-Execute？为什么不直接全塞 prompt 让 GPT-4o 决策？语义路由是不是被业务现场逼出来的（成本太高）？
- **SDK**：为什么参与 Neo 主仓而不是分支 fork？
- **子账户**：为什么 Turnkey 不 Fireblocks / Privy / 自建？

## 关键决策（按子项目分）

⏳ 待挖掘后填——参考 Qiniu README 12 条决策表的格式（决策 / 候选 / 选了什么 / 理由）

## 学术坐标 / 行业坐标

⏳ 待挖掘后填——4 子项目分别属于什么学术/行业 paradigm。

候选锚点：
- D2 ReAct + 语义路由 → 这是 **"工具描述 embedding + 两阶段 retrieval"** 范式，可能可以挂在 RAG-for-tools 或者最近的 ToolBench / API-Bank 学术线上
- DeepResearch → 多智能体研究助手范式（OpenAI Deep Research / GPT-Researcher 是参照）
- SDK → 开源 agent framework 范式（vs LangChain / LangGraph / CrewAI / Eliza）
- 子账户 → AI agent + blockchain 安全范式（vs Coinbase AgentKit / Privy / Crossmint）

## 遇到的问题与解决

⏳ Block D 待回答（参考 Qiniu README 3 个 problem 段的写法——情境 + 解决 + 学到的具体一件事）

## 结果

### 量化数字（CV 显式提到的硬指标）

- ✅ **98% 意图匹配准确率**（D2 语义路由）—— 待挖测试集 / 标注来源
- ✅ **70% 调用成本降低**（D2 语义路由）—— baseline 已确认
- ✅ **260+ GitHub stars**（D3 SDK）—— CV 已 confirm 准确（同步修 skill-gap / target-roles 的 150+ stale 引用）

### 待诚实表述的内容

⏳ Block E2-E3 待回答——Neo 4 子项目分别上线了 / 没上线？开源 vs 内部？

## 复盘 / Lessons learned

⏳ Block E 待回答——参考 Qiniu README 7 条 lessons 的层次

## 相关知识（候选）

- ✅ `KNOWLEDGE/agent/structured-output/`（已被 internships.md D4 引用——LLM intent → 规则引擎验证）
- ⏳ 候选：`KNOWLEDGE/agent/multi-agent/`（D1 DeepResearch 适合）
- ⏳ 候选：**新建** `KNOWLEDGE/agent/semantic-tool-routing/`——把"工具描述 embedding + 两阶段 retrieval"做成可复用知识节点（参考 Qiniu 把 AgentOps 报告内化为 KNOWLEDGE 的做法）—— 等 C2 答完后建

## 当前状态

`in-progress`（挖掘中——README + matrix + `subsystem-react-router.md` working draft 已建，`system-anatomy.md` 等 brief 答完后产出）

## 简历素材（CV 当前 4 条 bullet）

参见 `CAREER/cv.md` 第 56-59 行。

## 面试故事 STAR（候选场景，待派生）

| # | 候选场景 | 适合的考察方向 | 状态 |
|---|---|---|---|
| 1 | **3072 维语义路由的设计决策过程**（D2）| 系统设计能力 / 量化数字捍卫 | ⏳ 待 C2 答完后派生 |
| 2 | **海外社区某次冲突 / 协作**（D3）| 跨文化协作 / ownership | ⏳ 待 D2 答完后派生 |
| 3 | **Neo 项目中最大的失败 / 踩坑**（D4）| 反思深度 / 学习能力 | ⏳ 待 D4 答完后派生 |

派生后落地为 `CAREER/interview-bank/behavioral/neo-*.md`，对标 Qiniu 已有的 3 个 STAR 文件。

## 数据核对项

| 数字 | CV 现状 | 历史冲突 | 决定 |
|---|---|---|---|
| GitHub stars | 260+ | `skill-gap.md` / `target-roles/business-agent-engineer.md` 写 150+ | ✅ CV 准；同步修 stale 引用为 260+ |
| 工具数量 | 62 种 | 无冲突 | ✅ |
| 意图匹配准确率 | 98% | 无冲突 | ✅ 但**待挖测试集来源** |
| 成本降低 | 70% | 无冲突 | ✅ baseline 已 confirm |

---

# 挖掘 brief（请你按 block 分批回答）

每答完一个 block 通知我，我会立刻更新 README 对应段 + 升级 matrix 对应行 readiness。**预计动作链**：

- Block A+B 答完 → README 80% 完成
- Block C 答完 → `system-anatomy.md` 可写，`subsystem-react-router.md` 从 working draft 升级为可防御版
- Block D 答完 → 3 个 STAR 故事可派生
- Block E 答完 → README 复盘段补齐 + technical bank 4 个单题深答可派生

## Block A：业务背景 + 你的位置（5 问）

- **A1**：Neo 智能经济是什么公司？业务定位（给非技术朋友也能理解的一句话）？面向 C 端 / B 端？做哪条 chain（Ethereum / Solana / Neo 链 / 多链 / Layer2）？
- **A2**：5 个月（2025.02-07）总体目标？你被招进来主要做什么？职位描述是什么？
- **A3**：团队结构？你 report 给谁？mentor / leader 是谁？团队规模？**4 个子项目你各花了多少时间（粗略百分比）**？
- **A4**：去 Neo 的原因？离开 Neo 的原因？
- **A5**：**时代锚点**——2025 年 2-7 月的 Web3 + Agent 生态当时是什么样子？参考 Qiniu README "时代背景"段那种锚点表。我已经给出候选锚点（DeepResearch 热 / LangChain 生态 / MCP 未发布 / mem0 早期 / Pinecone Serverless 早期生产 / Anthropic Skills 未出），你确认 / 补充 / 删减。

## Block B：4 子项目的边界（4 问，每子项目 1 个）

- **B1（DeepResearch）**：完整业务场景？面向什么用户？最终怎么对外露出（API / 前端 / 内部）？你做的是哪部分？团队里谁还做？是你主导吗？
- **B2（ReAct + 语义路由）**：完整业务场景？用户问什么样的问题？系统回答什么类型的答案（链上数据 / 合约调用 / 投研 / 教学）？这是不是你最深入的项目？你独立做还是团队？
- **B3（SDK + 海外社区）**：什么 SDK？面向什么开发者？解决什么问题？是 Neo 自己开源还是参与社区 fork？你"参与"具体含义（核心贡献者 / contributor / maintainer）？海外社区运营独立做还是团队都参与？
- **B4（子账户）**：什么场景下需要子账户？给 DeFi 用户 / market-makers / 其他？设计这个的业务驱动？你做了哪部分（设计 / 实现 / 都参与）？

## Block C：关键设计决策（按子项目分）

### C1：DeepResearch
- 用了什么 agent 编排范式？工作流 / agent loop / DAG / 其他？
- 为什么 Python？为什么选这 3 类工具（搜索 / 抓取 / 代码执行）？
- 跟当时最火的 OpenAI Deep Research / GPT-Researcher / AutoGen 比有什么差异？为什么不直接用现成方案？

### C2：D2 ReAct + 语义路由（**最关键，CV 5 个硬指标必须各自定钉**）
- **62 个工具是怎么定的**？大类是哪些（合约调用 / 链上数据查询 / 投研 / 其他）？为什么是 62 个不是 30 或 100？
- **3072 维向量为什么用 OpenAI text-embedding-3-large** 不用其他（bge / Cohere / E5 / 自己微调）？
- **两阶段检索 Top10 → Top5**：Top10 用什么相似度（cosine / dot product）？Top5 用什么模型做 rerank（cross-encoder / 自己 fine-tune / LLM 做 judge）？精排的具体模型名（bge-reranker / 其他）？
- **98% 意图匹配率怎么测的**？测试集多大？谁标注？覆盖了 62 工具的多少种 query 模式？是 hold-out test set 还是交叉验证？
- **70% 调用成本怎么算的**？baseline 是"塞全部 62 个工具"还是其他？省的是 prompt token / 模型调用费 / 还是 embedding 费用？省的是绝对金额（每月省多少）还是相对比例？
- **延迟初始化 / 动态构建 / 实时批量更新**——这三个分别解决什么问题？具体工程实现？
- **mem0 vs FAISS vs Pinecone**：三个为什么并用？分别负责什么不同的 memory 维度？切换 / 写入 / 一致性怎么协调？

### C3：SDK + 海外社区
- **真的是 260+ stars**？仓库链接？你贡献的 commit 大概多少？你写的具体 PR # 是？
- 4 个核心模块（同步异步执行 / Graph / 链上对象存储 / 钱包加密）—— 是不是只有这 4 个？团队里其他人做了什么模块？
- **海外社区运营的具体数字**：处理 Issues N 个？Review PR N 个？写过多少文档？Discord+Telegram 多少活跃？月度新增 stars N？
- 国际用户主要是欧美 / 亚太？什么类型的开发者（DeFi / GameFi / Infra / 普通 dApp）？

### C4：子账户系统
- 多重签名 n-of-m 具体数字？多少 signer？签名规则按金额 / 操作类型 / 时间？
- 资金配额怎么实现？查询 + 扣减是哪一层？拒绝时返回什么 error？
- Turnkey 选型理由（vs Fireblocks / Privy / 自建 HSM）？
- LLM 决策与签名分离的"规则引擎"具体是什么（rule engine 产品 / 自写 if-else / OPA / 其他）？

## Block D：遇到的问题 + 怎么解的（覆盖 3 个 STAR 候选）

- **D1**：4 子项目里最大的技术挑战？怎么解决的？（要具体故事，参考 Qiniu CEO 拍板那种细节度）
- **D2**：海外协作的冲突 / 困难——具体故事（哪个 PR / Issue / Discord 对话引发的）？语言 / 时差 / 文化 / 技术分歧分别遇到过什么？
- **D3**：跟 mentor / leader 的最大分歧？怎么解决？
- **D4**：项目内部最大的失败 / 踩坑？必须具体故事
- **D5**：顶住压力的具体经历？（对标 Qiniu 路演加班补救）

## Block E：结果 + 复盘

- **E1**：5 个月学到最重要的事？
- **E2**：现在回看哪些技术选择对 / 错了？（参考 Qiniu README "复盘 §2" 时代意识那种维度）
- **E3**：跟七牛云比，Neo 给你的最大不同收获是什么？（这是 `internships.md` 通用追问的高频题）
- **E4**：CV 上哪个数字（98% / 70% / 260+）最容易被深问？你怎么准备的？

---

## 不在本文档讨论的内容

- 4 子项目的系统视图 / 数据流 / 集成关系 → `system-anatomy.md`（待建）
- D2 ReAct + 语义路由的深度解剖（5 硬指标 + 设计细节）→ `subsystem-react-router.md`（working draft，待 C2 补齐）
- 60+ 挑战角度的 readiness 矩阵 + GAP 清单 → `interview-defense-matrix.md`
- 单题深答（每篇 5-10 页）→ `CAREER/interview-bank/technical/neo-*.md`（待派生 4 篇）
- 行为题 STAR 故事 → `CAREER/interview-bank/behavioral/neo-*.md`（待派生 3 篇）
