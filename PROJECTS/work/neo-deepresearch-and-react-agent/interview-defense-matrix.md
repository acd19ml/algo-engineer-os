# Neo · 面试挑战防御矩阵

> **状态**：基线版（多数 ⚠️/❌），等 README 末段挖掘 brief 答完后会大量升级。
>
> **素材来源**：CV 第 56-59 行 + `CAREER/interview-bank/technical/internships.md` D 段 + `CAREER/skill-gap.md` + `CAREER/target-roles/*.md` 散落引用。
>
> **跟 Qiniu matrix 的差异**：
> - Qiniu matrix 起手时已经有 1700+ 行项目文档支撑，所以 ✅ 居多；
> - Neo matrix 起手时只有 CV + 几行追问骨架，所以大量 ⚠️/❌——**这是诚实的 readiness**，不是缺陷。
>
> **下游链路**（同 Qiniu）：识别 GAP → 按 P0/P1/P2 排产 → P0/P1 GAP 落地为 `interview-bank/technical/neo-*.md` 或 `PROBLEMS/*` 横向页 → 更新本表 readiness。

## Readiness 图例

- ✅ 有现成回答（指向已有材料）
- ⚠️ 部分准备（有素材但需要补充 / 重组）
- ❌ 知识空白（待挖掘 brief 回答 / 待研究）

## 谁会问（缩写）

- **HR**：HR 初面 / 一面（业务背景 + 简历真实性）
- **技**：技术面（架构 + 实现 + 算法）
- **总**：总监 / 高级技术面（取舍 + 反思 + 行业认知）
- **研**：研究方向面（学术坐标 + 横向比较）
- **行**：行为面（协作 + 压力 + 反思）

---

## 1. 业务背景类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| Neo 智能经济是做什么的？业务定位？ | 简历真实性 / HR + 技 | ❌ | **挖掘 brief A1** |
| 你 5 个月（2025.02-07）的总体目标？ | HR / 技 | ❌ | **挖掘 brief A2** |
| 团队结构？report 给谁？4 子项目你时间占比？ | HR / 技 | ❌ | **挖掘 brief A3** |
| 去 Neo 的原因 / 离开 Neo 的原因？ | 转换叙事 / HR + 总 | ❌ | **挖掘 brief A4** + `internships.md` "为什么离开" |
| 4 子项目是同时做还是先后？ | 实习真实性 / 技 | ❌ | 同上 |
| Neo 是 web2 还是 web3 公司？面向哪条 chain？ | 行业 / 技 | ❌ | **挖掘 brief A1** |
| 一段实习同时 4 个项目，怎么避免每个都浅尝辄止？ | 反向挑战 / 总 + 行 | ❌ | 待 D 答完——需要诚实说明哪个深度高、哪些浅参与 |

---

## 2. 产品决策类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| DeepResearch 服务最终面向什么用户场景？ | 业务理解 / 技 | ❌ | **brief B1** |
| ReAct 区块链问答系统用户问什么类型的问题？ | 业务理解 / 技 | ❌ | **brief B2** |
| 子账户系统的具体业务场景？给谁用？ | 业务理解 / 技 | ❌ | **brief B4** |
| 4 个子项目里哪个上线了 / 哪个没上线？ | 诚实度 / 技 + 总 | ❌ | **brief E2-E3** |
| 这些项目商业价值怎么衡量？ | 产品视角 / 总 | ❌ | brief 之后 |

---

## 3. 架构选型类

### 3.1 通用 / 跨子项目

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 为什么 Python 不 Go / Rust？ | 选型 / 技 | ⚠️ | LLM 生态 + 团队栈，待 C1 完善 |
| Pinecone Serverless vs 自建（Weaviate / Milvus）？ | 向量库 / 技 | ⚠️ | `internships.md` D2 部分回答（本地 vs 托管 trade-off）|
| FAISS vs Pinecone 并用为什么不只选一个？ | 向量库 / 技 | ⚠️ | `internships.md` D2 部分回答（短期对话内 vs 长期跨对话 trade-off）|
| mem0 是什么？跟自己设计的记忆区别？ | RAG/记忆 / 技 + 研 | ⚠️ | `internships.md` D2（mem0 是开源 long-term memory framework，对比已有），但**需要重组成 STAR**——GAP-N1 |
| OpenAI text-embedding-3-large 选型？ | embedding / 技 | ⚠️ | `internships.md` D2 已答（原生 3072 维 + 区分度）+ `fundamentals.md` 已列入待对比 |
| ReAct 模式 vs Plan-and-Execute？为什么 ReAct？ | 范式 / 技 | ❌ | **brief C2** |

### 3.2 DeepResearch 子项目

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 用了什么 agent 编排范式（工作流 / agent loop / DAG）？ | 范式 / 技 | ❌ | **brief C1** |
| 跟 OpenAI Deep Research / GPT-Researcher 比？ | 横向 / 总 | ❌ | **GAP-N2（P0）**：DeepResearch 横向页 |
| 跟 LangChain Agent / AutoGen 比？ | 横向 / 技 | ❌ | 同上 |
| 工具集成怎么标准化（tool 抽象层）？ | 工程 / 技 | ⚠️ | `internships.md` D1 已答（`__call__` 接口 + 统一 error/timeout/retry）|

### 3.3 D2 ReAct + 语义路由（CV 金字段）

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| **62 个工具怎么定的？为什么 62 不是 30 / 100**？ | 范围定义 / 技 + 总 | ❌ | **brief C2** |
| **3072 维向量为什么不更小**？ | 工程 / 技 | ✅ | `internships.md` D2 已答（OpenAI 原生 + 区分度 + 内存可接受）|
| **两阶段检索 Top10→Top5**：Top10 用什么相似度？精排用什么模型？ | RAG / 技 | ⚠️ | `internships.md` D2 部分回答（cosine + cross-encoder bge-reranker），需 brief C2 确认具体模型名 |
| **98% 意图匹配怎么测**？测试集多大？谁标注？ | 评测 / 技 + 总 | ❌ | **GAP-N3（P0）**：评测设计——`internships.md` D2 已 flag 为 "Gap: 准备具体数字" |
| **70% 成本降——baseline 是什么**？ | 评测 / 技 + 总 | ✅ | `internships.md` D2 已 confirm（baseline = 塞全部 62 工具）|
| 70% 是 token 节省还是金额节省？相对 / 绝对？ | 评测 / 技 | ❌ | 待 brief C2 / E4 |
| 延迟初始化具体怎么做？ | 工程 / 技 | ⚠️ | `internships.md` D2 部分回答（增量 embedding + 首次请求 build + versioned + 原子切换）|
| 实时批量索引更新具体怎么做？ | 工程 / 技 | ⚠️ | `internships.md` D2 部分回答（事件队列 + 后台 worker + 原子替换）|
| ReAct 收敛慢 / 不停问题怎么解？ | 范式 / 技 | ❌ | 待 brief C2 |
| 失败工具调用（API 404 / 超时）怎么处理？ | 健壮性 / 技 | ❌ | 待 brief C2 |
| 跟 ToolBench / API-Bank 学术工作比？ | 横向 / 研 | ❌ | **GAP-N4（P1）**：tool-routing 学术坐标 |

### 3.4 SDK + 海外社区

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| SDK 仓库链接 / 你贡献的 commit 数 / 具体 PR # ？ | 真实性 / HR + 技 | ❌ | **brief C3** |
| 4 个核心模块的具体作用？ | 工程 / 技 | ⚠️ | CV 列出但缺细节，待 brief C3 |
| 测试用例覆盖率？ | 工程 / 技 | ❌ | 待 brief C3 |
| SDK 设计 vs LangChain / CrewAI / Eliza 框架？ | 横向 / 技 + 总 | ❌ | **GAP-N5（P1）**：agent framework 横向 |
| 海外社区运营具体数字（Issues / PR / Discord）？ | 真实性 / HR | ⚠️ | `internships.md` D3 已列 5 件事，缺数字 |
| 你和海外开发者协作语言？时差怎么处理？ | 跨文化 / HR + 行 | ✅ | `internships.md` D3 已答（英文 + 异步沟通 + 重大决策 Discord 会议）|

### 3.5 子账户系统

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 子账户和主账户的隔离机制？ | 安全 / 技 | ⚠️ | `internships.md` D4 已答（私钥独立 + 多签 + 配额）|
| Turnkey 是什么？为什么选它（vs Fireblocks / Privy / 自建 HSM）？ | 选型 / 技 | ⚠️ | `internships.md` D4 部分答（HSM 级管理 + 不落地 + 合规），需 brief C4 补横向 |
| LLM 驱动自动交易的安全考虑？ | 安全 / 技 + 总 | ✅ | `internships.md` D4 已答（intent vs 签名分离 + 规则引擎 + 子账户隔离 + 全链路审计）|
| 多签 n-of-m 具体配置？ | 工程 / 技 | ❌ | **brief C4** |
| 规则引擎具体实现（产品 / OPA / 自写）？ | 工程 / 技 | ❌ | **brief C4** |

---

## 4. Agent 设计类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| DeepResearch 的核心难点是什么？ | Agent 难点 / 技 | ✅ | `internships.md` D1 已答（意图理解 + 工具编排 + 信息聚合）|
| ReAct 模式具体 trace 长什么样？ | 范式细节 / 技 | ❌ | 待 brief C2 |
| 短期 + 长期记忆怎么协调（mem0 / FAISS / Pinecone 三者）？ | 记忆设计 / 技 + 研 | ⚠️ | `internships.md` D2 提到三者用法，**需要补统一架构图**——GAP-N6 |
| 工具调用失败 / 超时 / 重试策略？ | 工程 / 技 | ⚠️ | `internships.md` D1 答了通用方法（统一 error/timeout/retry），但 D2 / D4 还需要具体 |
| Procedural / Episodic / Semantic memory 区别？ | RAG 理论 / 研 | ✅ | `fundamentals.md` 已列入 + `KNOWLEDGE/agent/context-engineering/` |

---

## 5. 算法 / 评测类（CV 5 硬指标，最容易被打穿）

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| **98% 准确率的测试集**：多大 / 谁标注 / 覆盖什么 | 评测严谨 / 技 + 总 | ❌ | **GAP-N3（P0）** |
| 98% 是 hold-out / k-fold / online A/B？ | 评测 / 技 | ❌ | 同上 |
| **70% 成本降是什么 baseline**？ | 评测 / 技 + 总 | ✅ | `internships.md` D2（baseline = 塞 62 工具全描述）|
| 70% 节省的是 token / 金额 / 调用次数？ | 评测 / 技 | ❌ | 待 brief E4 |
| 怎么保证语义路由不漏召（false negative）？ | 评测 / 技 | ❌ | 待 brief C2——Top10 召回的 floor 保障 |
| Cross-encoder 精排具体哪个模型？ | embedding / 技 | ⚠️ | `internships.md` D2 提 bge-reranker 作为候选，需 brief 确认 |
| Embedding 模型为什么不微调？ | embedding / 技 | ❌ | 待 brief C2——可能因 cold start / 数据不足 |
| 工具描述怎么写得让 embedding 区分度高？ | prompt 工程 / 技 | ❌ | **GAP-N7（P1）**：工具描述编写规范 |

---

## 6. 数据 + 存储类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| Pinecone Serverless 的 cost model？ | 工程 / 技 | ❌ | 待补 |
| FAISS index 类型怎么选（IVF / HNSW / Flat）？ | 向量库 / 技 | ❌ | **GAP-N8（P2）** |
| 索引更新 / 切换的原子性怎么保证？ | 工程 / 技 | ⚠️ | `internships.md` D2 提到 versioned + 原子替换，需 brief C2 补具体 |
| 区块链链上数据查询怎么做（RPC / index service / The Graph）？ | 工程 / 技 + 研 | ❌ | 待 brief C2 / C4 |

---

## 7. 工程实现类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 4 个子项目的工程协作（git workflow / PR review）？ | 工程 / 技 + 行 | ❌ | 待 brief C3 / D2 |
| 部署模式（K8s / Docker / Serverless / Lambda）？ | 工程 / 技 | ❌ | 待补 |
| 监控 / 可观测性怎么做？ | 工程 / 技 | ❌ | 待补 |
| CI/CD 怎么做？ | 工程 / 技 | ❌ | 待 brief C3 |
| 测试覆盖率？单元 / 集成 / E2E ？ | 工程 / 技 | ❌ | 待 brief C3 |
| API rate-limit / 缓存策略？ | 工程 / 技 | ❌ | 待补 |

---

## 8. 复盘 / 反思类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 4 子项目里最大的技术挑战 + 怎么解决？ | 反思深度 / 技 + 总 | ❌ | **brief D1** |
| 海外协作的具体冲突 / 困难故事？ | 跨文化 / HR + 行 | ❌ | **brief D2**——STAR 故事 2 候选 |
| 跟 mentor 的最大分歧？怎么解决？ | 协作 / 行 | ❌ | **brief D3** |
| 项目内部最大的失败 / 踩坑？ | 反思 / HR + 行 | ❌ | **brief D4**——STAR 故事 3 候选 |
| 顶住压力的具体经历？ | 韧性 / HR + 行 | ❌ | **brief D5** |
| 5 个月学到最重要的事？ | 反思 / HR + 总 | ❌ | **brief E1** |
| 跟七牛云比 Neo 给你最大不同收获？ | 转换叙事 / HR + 总 | ⚠️ | `internships.md` 通用追问已有答题骨架（应用层 vs 系统层；工具型 vs 系统型；海外协作 vs 团队协作）|
| 实习中最自豪的设计 / 决策？ | 反思 / 技 + 总 | ⚠️ | `internships.md` 通用追问提示 = 语义路由 70% 成本降，待 D 答完后定 |
| 为什么离开 / 来这边？ | 转换叙事 / HR | ❌ | `internships.md` 通用追问已 flag "需准备 transition story" |

---

## 9. 横向调研类（最值钱，最容易打穿）

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| **vs OpenAI Deep Research / GPT-Researcher**？ | 行业 / 总 | ❌ | **GAP-N2（P0）** |
| **vs LangChain Agent / AutoGen / CrewAI / Eliza**？ | 框架横向 / 技 + 总 | ❌ | **GAP-N5（P1）** |
| **vs ToolBench / API-Bank 学术 tool retrieval 工作**？ | 学术 / 研 | ❌ | **GAP-N4（P1）** |
| MCP 协议出现后，你的语义路由方案还需要吗？| 时代演进 / 总 | ❌ | **GAP-N9（P1）**：MCP 时代的 tool routing 价值 |
| Anthropic Skills / Codex / Cursor Agent 涌现后，你做的 SDK 还有价值吗？ | 时代演进 / 总 | ❌ | **GAP-N10（P2）**：开源 agent SDK 在 Skills 时代的定位 |
| vs Coinbase AgentKit / Privy / Crossmint 这种 AI agent + blockchain 安全方案？ | 横向 / 技 + 研 | ❌ | **GAP-N11（P1）**：AI agent + blockchain 安全栈 |
| 2025 年初到 2026 年中 Web3 + Agent 生态变化？你怎么跟进？ | 行业敏感 / 总 | ❌ | 待补——结合 brief E2 |

---

## 10. 领域知识类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| RAG 系统设计？召回率 vs 精确率 trade-off？ | RAG / 技 | ⚠️ | `fundamentals.md` + `KNOWLEDGE/agent/context-engineering/` |
| 区块链合约调用 / RPC / The Graph 基础？ | 区块链 / 技 | ❌ | **GAP-N12（P2）**：web3 basics 兜底 |
| HSM / 多签 / 私钥管理基础？ | 区块链安全 / 技 | ⚠️ | `internships.md` D4 触及，但深度有限 |
| LLM Function Calling vs MCP 协议？ | LLM 工具调用 / 技 + 研 | ⚠️ | KB 涉及，但 Neo 项目当时还是 FC 时代——需要 framing |
| Embedding 模型横向（OpenAI / Cohere / bge / E5）？ | embedding / 技 | ⚠️ | `fundamentals.md` 已 flag 待对比 |
| 向量库横向（Pinecone / FAISS / Milvus / Weaviate）？ | 向量库 / 技 | ⚠️ | `fundamentals.md` 已 flag 待对比 |

---

## GAP 优先级清单（按落地紧迫度）

### P0 — 必须在 brief 答完后立刻补完

| GAP # | 内容 | 落地位置 |
|---|---|---|
| GAP-N2 | DeepResearch 横向（vs OpenAI Deep Research / GPT-Researcher）| `PROBLEMS/deep-research-paradigm-landscape/`（新建）|
| GAP-N3 | D2 评测设计（98% 测试集 / 标注 / hold-out）| `CAREER/interview-bank/technical/neo-semantic-router-evaluation.md`（新建）|

### P1 — 中等优先

| GAP # | 内容 | 落地位置 |
|---|---|---|
| GAP-N1 | mem0 vs 自己设计的记忆系统 STAR | `CAREER/interview-bank/behavioral/neo-semantic-router-design.md` 部分含 |
| GAP-N4 | tool-routing 学术坐标（vs ToolBench / API-Bank）| 新建 `KNOWLEDGE/agent/semantic-tool-routing/` |
| GAP-N5 | Agent framework 横向（vs LangChain / CrewAI / Eliza）| `PROBLEMS/agent-framework-comparison/`（Qiniu GAP-7/47 已计划）—— Neo 同源合并 |
| GAP-N6 | 短期 + 长期记忆统一架构（mem0 / FAISS / Pinecone）| `subsystem-react-router.md` §X（待建）|
| GAP-N7 | 工具描述编写规范 | 待写 |
| GAP-N9 | MCP 时代下 tool routing 价值（你的项目还需要吗？）| 整合到 GAP-N4 / `KNOWLEDGE/agent/semantic-tool-routing/` |
| GAP-N11 | AI agent + blockchain 安全栈 | `PROBLEMS/ai-blockchain-security-landscape/` 或 `KNOWLEDGE/agent/agent-blockchain-safety/` |

### P2 — 兜底回答

| GAP # | 内容 | 兜底策略 |
|---|---|---|
| GAP-N8 | FAISS index 类型选型 | 承认"默认 IndexFlat / 项目规模没到需要换 IVF/HNSW" |
| GAP-N10 | 开源 agent SDK 在 Skills 时代定位 | 承认时代变化 + 引用 KNOWLEDGE/agent/agent-tool-design 节点 |
| GAP-N12 | web3 basics 兜底 | "项目期间接触到 RPC / 智能合约 / 多签等基础，未深入分布式共识层" |

---

## 维护规则（同 Qiniu）

1. **每次 mock / 正式面试**遇到新问题 → 立刻追加一行
2. **完成一个 GAP** → 升级 readiness（❌ → ⚠️ → ✅）+ 更新深答位置
3. **GAP 优先级动态调整**
4. **季度回顾**

## 不在本文档讨论的内容

- 4 子项目业务背景 / 决策 / 复盘 → `README.md`
- 4 子项目系统视图 → `system-anatomy.md`（待建）
- D2 ReAct + 语义路由深度解剖 → `subsystem-react-router.md`（待建）
- 单题深答 → `CAREER/interview-bank/technical/neo-*.md`（待派生）
- STAR 故事 → `CAREER/interview-bank/behavioral/neo-*.md`（待派生）
