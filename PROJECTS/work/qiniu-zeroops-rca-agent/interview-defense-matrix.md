# 七牛云 ZeroOps · 面试挑战防御矩阵

> **目的**：把这个项目所有可能被面试官挑战的角度建成一个 catalog——每条记录 readiness + 深答位置 + GAP 行动项。这是 living document，每次 mock 或正式面试遇到新问题就追加一行 + 标记。
>
> **跟谁不同**：
> - `README.md` 是**叙事**（决策复盘）
> - `system-anatomy.md` / `agent-subsystem.md` 是**系统是什么**
> - `interview-answers/*.md`（项目本地深答，5-10 页/篇）是**单题深答**
> - **本文档是 catalog**——只索引 + 追缺口，深答进项目本地 `interview-answers/`
>
> **下游链路（闭环）**：识别 GAP → 按 P0/P1/P2 排产 → ① 落地为 `interview-answers/` 深答或 `PROBLEMS/` 横向页；② **若暴露项目本身的不足 → 回写改进项目设计 / 复盘；若是方法论问题 → 回 `KNOWLEDGE/methodology/` 节点** → 更新本表 readiness。

## Readiness 图例

- ✅ **有现成回答**——指向 technical bank / KNOWLEDGE 节点 / 项目文档，可直接背诵或现场表达
- ⚠️ **部分准备**——有素材或大方向，但需要重组 / 横向调研 / 补具体证据才能挡住深问
- ❌ **知识空白**——还没研究过；被问到时要么诚实承认要么给一个"假设性回答方向"兜底

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
| 为什么 MVP 没上线？ | 诚实度 / HR + 技 | ✅ | `README.md` "结果（坦诚的现状）" |
| 为什么基于 Mock 不接生产？ | 工程严谨 / 技 | ✅ | `README.md` "结果" + "问题 3" |
| Mock 系统怎么模拟数据？故障注入策略？ | 工程细节 / 技 | ⚠️ | **GAP-1**：补 mock 数据生成 + 故障注入策略说明 |
| 三个月做了什么？时间分配？ | 产出 / HR + 技 | ✅ | `README.md` "团队角色" + `system-anatomy.md` §7（6 步法产物清单）|
| 团队人数 + 你的实际占比？ | 协作度量 / HR + 技 | ✅ | `README.md` "团队角色" |
| 项目本来打算解决什么真实业务问题？ | 业务理解 / 技 | ✅ | `README.md` "动机" + `agent-subsystem.md` §1（数据接入业务痛点）|
| 项目结束时哪些指标算成功？业务侧 KPI？ | 评测意识 / 技 + 总 | ⚠️ | 仅 20%→70% 是技术 KPI，**缺业务侧成功定义**——GAP-2 |
| 你怎么界定"项目结束"的？ | 边界意识 / 总 | ✅ | 1024 实训营 3 个月制 + milestone 路演 |
| 项目获奖（1024 优胜奖）意味着什么？ | 评价 / HR + 技 | ✅ | `README.md` "结果"+`cv.md` 末段 |

---

## 2. 产品决策类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 为什么变更场景而不是线上运行场景？ | MVP 思维 / 技 + 总 | ✅ | `README.md` "关键决策" 行 1 |
| **双路径（告警 + 体检中心）的具体业务价值？** | 架构创新论证 / 技 | ⚠️ | **GAP-3（P0）**：体检中心 vs 告警的覆盖差异、命中率差异——需量化或至少给定性论证 |
| 体检中心多久巡检一次？过载怎么办？ | 工程深度 / 技 | ❌ | **GAP-4**：未量化巡检频率 vs 系统负担 trade-off |
| 体检中心调用 AI 的成本怎么估？ | 工程深度 / 技 | ❌ | **GAP-5**：每次 RCA 的 token 成本未沉淀 |
| 三次产品形态调整的具体过程？ | 协作 / HR + 行 | ✅ | README.md（决策复盘） |
| 如果再做你会怎么定产品形态？ | 反思深度 / 总 | ✅ | `README.md` "复盘 §1" |
| 你怎么知道变更场景方向是对的？ | 验证意识 / 技 | ⚠️ | 基于 CEO 拍板 + mentor 业务判断，**缺数据驱动验证**——GAP-6 |
| 一开始想做"对话辅助 SRE"为什么不做？ | 决策回溯 / 行 | ✅ | README.md（决策复盘） |
| 一开始想做"无人替代 SRE"为什么不做？ | 决策回溯 / 行 | ✅ | 同上 |
| 谁是用户？运维工程师 vs 业务方？ | 用户定位 / 技 + 总 | ✅ | `README.md` "动机" |

---

## 3. 架构选型类（横向调研高频）

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 为什么选 LangGraph StateGraph 而不是自由 Agent Loop？ | 横向调研 / 技 + 总 | ✅ | `README.md` "真实选型路径" + `interview-answers/qiniu-agent-loop-vs-workflow.md` |
| 为什么选 LangGraph 不选 Dify 可视化方案？ | ROI 取舍 / 技 | ✅ | 同上；核心：ops safety + HITL interrupt 是代码层需要，Dify 可视化是 SaaS 约束 |
| 为什么不用 coding agent 范式？ | 时代背景 / 技 + 总 | ✅ | 同上 |
| **为什么 MCP 不是直接 Function Calling？** | 协议选型 / 技 | ⚠️ | **GAP-8（P1）**：MCP vs FC 取舍未沉淀 |
| 为什么 fox / Gin 不是 Echo？ | 公司栈 / 技 | ✅ | `system-anatomy.md` §1.2（公司内部包装） |
| 为什么 Postgres 不是 MySQL？ | 选型 / 技 | ✅ | `system-anatomy.md` §1.2 + §3.3（ARRAY 类型）|
| 为什么 zerolog 不是 logrus / zap？ | 日志栈 / 技 | ❌ | **GAP-9（P2）**：日志库横向缺位 |
| 为什么 Vue 不是 React？ | 前端栈 / 技 | ✅ | 团队栈，弱化即可 |
| ReAct 模式具体是 Original 还是 PDL-based？ | 范式细节 / 技 | ✅ | `agent-subsystem.md` §3 |
| 如果今天重做你会选什么？ | 时代意识 / 总 | ✅ | `README.md` "复盘 §2" |
| 工作流 vs Agent Loop 各自适用场景？ | 范式认知 / 技 | ✅ | `interview-answers/qiniu-agent-loop-vs-workflow.md` |
| 函数计算 vs K8s Job 部署 MCP Server 的取舍？ | 部署选型 / 技 | ❌ | **GAP-10（P2）** |
| 灰度发布编排自己写还是用 Argo Rollouts / Flagger？ | 工具调研 / 技 | ⚠️ | **GAP-11（P1）**：项目自实现，缺横向对比 |

---

## 4. Agent 设计类（最容易深问的区域）

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 5 个 agent 为什么这么拆？ | 拆分理由 / 技 | ✅ | `interview-answers/qiniu-multi-agent-decomposition.md` |
| 按职责拆 vs 按阶段拆（Claude Code 式）？ | 多智能体范式 / 技 + 研 | ✅ | 同上 + `KNOWLEDGE/agent/multi-agent/` |
| 值班长为什么不主动取数据？ | 设计哲学 / 技 | ✅ | `agent-subsystem.md` §5.5 |
| **5 个 prompt 是怎么演进的？v1→v2→v3 改了什么？** | 迭代历史 / 技 | ❌ | **GAP-12（P1）**：prompt 演进案例缺位，是工程深度铁证 |
| **上下文压缩具体方法是什么？** | 工程深度 / 技 | ⚠️ | **GAP-13（P1）**：`agent-subsystem.md` §3.3 只到 framework，缺具体策略（摘要 vs 抽取关键片段 vs window slide）|
| Agent 间 JSON schema 怎么定的？演化过程？ | schema 设计 / 技 | ⚠️ | **GAP-14（P1）**：schema 演化过程未沉淀 |
| 为什么有 L3 通用专家 + 语言专家？ | 角色冗余 / 技 | ⚠️ | `agent-subsystem.md` §1.1 提到角色但 §2 工作流细节未给职责区分——GAP-15 |
| 工具调用失败 / 超时怎么处理？ | 健壮性 / 技 | ❌ | **GAP-16（P1）**：失败重试 + 降级策略缺位 |
| Agent trajectory 如何调试？ | AgentOps 视角 / 总 + 研 | ✅ | `README.md` "复盘 §7" + `KNOWLEDGE/agent/agentops-vs-opsagent/`（缺位是事后审视）|
| 模型按角色选具体怎么选的？ | 选型 / 技 | ✅ | `agent-subsystem.md` §2.1 |
| qwen 系列模型对比 / 为什么不用 GPT-4？ | 选型 / 技 | ⚠️ | **GAP-17**：内网 / 合规 / 成本理由可加固 |
| 多个 agent 怎么避免无限循环？ | 终止判断 / 技 | ✅ | `agent-subsystem.md` §3.3 #3（智能终止判断）|
| 值班长 + 运营专家是不是角色冗余？ | 角色合理性 / 技 | ⚠️ | **GAP-18**：值班长 = 决策仲裁，运营专家 = 报告生成；独立的工程理由（输出结构差异）需补 |
| Result Fusion vs Model Fusion vs Feature Fusion？ | 多模态范式 / 技 + 研 | ✅ | `interview-answers/qiniu-multimodal-fusion-paradigm.md` |
| Trace agent 为什么严禁截断 stack trace？ | 数据完整性 / 技 | ✅ | `agent-subsystem.md` §5.3（5 条行动铁律 #2）|
| 知识库怎么切片？ chunk size 选多少？ | RAG 工程 / 技 | ⚠️ | `agent-subsystem.md` §6 提到"切片优化"但缺具体参数——GAP-19 |
| Embedding 模型为什么选 text-embedding-v3？ | 选型 / 技 | ⚠️ | `agent-subsystem.md` §2.1 仅列出未给理由——GAP-20 |
| Agent 间 context 怎么传？全量 vs 摘要？ | 工程深度 / 技 | ✅ | `agent-subsystem.md` §3.3 #2（上下文压缩与精准引用）|

---

## 5. 算法 / 评测类（最容易被打穿）

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| **时序异常检测具体什么算法？** | 算法 / 技 | ⚠️ | `system-anatomy.md` 提 STL+百分位但**深问会穿** |
| **STL + 百分位数能解决什么 / 不能解决什么？** | 算法局限 / 技 | ❌ | **GAP-21（P0）**：必须建对比表（STL / Z-score / 孤立森林 / RPCA / Group-wise VAE / 季节性分解）|
| 为什么不用 Group-wise VAE 这类深度方法？ | 算法前沿 / 技 + 研 | ❌ | 同 GAP-21 |
| 时序数据预处理怎么做？缺失值 / 异常点平滑？ | 算法基础 / 技 | ❌ | **GAP-22**：算法预处理细节未沉淀 |
| 时序异常检测的滑动窗口怎么设？ | 算法工程 / 技 | ❌ | 同上 |
| **20% → 70% 怎么测的？标注谁做的？** | 评测严谨性 / 技 + 总 | ⚠️ | **GAP-23（P0）**：评测设计细节 / 标注来源 / 根因匹配标准 |
| Precision / Recall 是多少？ | 指标知识 / 技 | ❌ | **GAP-24（P0）**：内部 demo 数据，需诚实回答 + 解释为何只用 success rate |
| "根因定位成功"具体怎么定义？ | 评测设计 / 技 | ❌ | 同 GAP-23 |
| 70% 的 baseline 是什么？相对什么提升？ | 评测意识 / 技 | ⚠️ | `agent-subsystem.md` §7 有路径但缺评测设计——GAP-23 |
| 召回率精确率为什么不分开报？ | 评测意识 / 技 | ❌ | 同上 |
| 怎么避免根因分析 hallucination？ | LLM 缺陷 / 技 | ⚠️ | `agent-subsystem.md` §5（限制行为）+`agent-subsystem.md` §5.3（数据完整性铁律）有部分回答 |
| 你做了多少 test case？覆盖什么场景？ | 测试覆盖 / 技 | ❌ | **GAP-25**：测试用例数据未沉淀 |
| ARMS 火焰图分析的实际效果如何？ | 算法落地 / 技 | ❌ | **GAP-26（P2）**：火焰图 agent 实际效果未量化 |
| 端到端延迟是多少？P50 / P95 / P99？ | 性能 / 技 | ❌ | **GAP-27**：延迟数据未沉淀 |
| 单次 RCA 的 token 消耗 / 成本？ | 工程 / 技 | ❌ | 同 GAP-5 |

---

## 6. 数据 + 存储类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| Postgres ARRAY 为什么不拆中间表？ | 选型 / 技 | ✅ | `system-anatomy.md` §3.3 |
| ARRAY 类型查询性能 / 索引怎么处理？ | 数据库深度 / 技 | ❌ | **GAP-28（P2）**：GIN 索引未沉淀 |
| event_log 怎么不打爆表？ | 工程 / 技 | ❌ | **GAP-29（P2）**：分区 / 归档策略缺位 |
| correlation_id 怎么贯穿的？ | 设计 / 技 | ✅ | `system-anatomy.md` §3.3 |
| alert_rule_metas 为什么单独拆表？ | 设计 / 技 | ✅ | `system-anatomy.md` §3.3 |
| 同一告警的多级阈值为什么用两条规则？ | 设计 / 技 | ✅ | `system-anatomy.md` §3.3 |
| 数据库 schema 演化怎么管理？migration 工具？ | 工程 / 技 | ❌ | **GAP-30（P2）** |
| 向量数据库（VectorDB）选型理由？ | 选型 / 技 | ⚠️ | `agent-subsystem.md` §1.1 出现但选型理由缺——GAP-31 |
| Redis 用在哪？怎么避免缓存击穿 / 雪崩？ | 中间件 / 技 | ⚠️ | `agent-subsystem.md` §1.1 出现但具体场景缺——GAP-32 |

---

## 7. 工程实现类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| **为什么 Go 主流程 + Python 异常检测，不全 Go？** | 工程取舍 / 技 | ⚠️ | CV 已删但仍可能被问；准备答案："算法生态 + 模块独立迭代" |
| LangGraph service K8s 部署方案？ | 部署 / 技 | ⚠️ | **GAP-33（P2）**：Python FastAPI/uvicorn 容器化 + K8s Deployment；具体细节待补 |
| LangGraph service 高可用怎么做？ | 工程 / 技 | ❌ | 同上；MVP 阶段未深究 |
| 灰度发布逻辑是否真自动？冲突检测怎么做？ | 实现深度 / 技 | ⚠️ | `system-anatomy.md` §5 描述策略缺实现细节——GAP-34 |
| 服务依赖关系（CMDB）怎么获得？ | Mock 体系 / 技 | ❌ | **GAP-35**：CMDB mock 来源未沉淀 |
| MCP Server 部署在函数计算的具体原因？ | 部署选型 / 技 | ⚠️ | `agent-subsystem.md` §1.2 原则二提到但缺工程细节 |
| 函数计算冷启动问题怎么解决？ | FaaS / 技 | ❌ | **GAP-36（P2）**：冷启动 / 预留实例策略 |
| CI/CD 怎么做的？ | 工程 / 技 | ❌ | **GAP-37**：项目 CI/CD 未沉淀 |
| 代码规模？技术债怎么管？ | 工程 / 技 | ❌ | **GAP-38**：诚实回答即可（MVP 阶段未做形式化技术债管理）|
| 端到端测试怎么做的？ | 测试 / 技 | ❌ | **GAP-39**：MVP 阶段大概率没做完整 E2E 测试，需诚实回答 |
| 监控告警自己怎么监控？（meta-observability）| 可观测元 / 技 + 总 | ❌ | **GAP-40**：项目自身可观测性未沉淀——这正是"AgentOps 视角缺位"的具体表现 |
| 项目代码开源吗？仓库结构？ | 工程 / 技 | ❌ | **GAP-41**：仓库结构 / 是否公开未沉淀 |
| 团队 git 协作模式？PR review 流程？ | 协作 / 技 + 行 | ⚠️ | `RAW_SOURCES/qiniu-internship-artifacts/复盘文档.md` 提到"加强 GitHub 协作培训" / "养成 PR 习惯"——GAP-42 |

---

## 8. 复盘 / 反思类（已经准备充分）

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| 你最后悔什么？ | 反思深度 / HR + 总 | ✅ | `README.md` "复盘 §1"（技术提案缺位）|
| 如果重做你会换什么？ | 时代意识 / 总 | ✅ | `README.md` "复盘 §2" |
| 你学到的最重要的事？ | 顿悟 / 任何面 | ✅ | `README.md` "复盘" |
| 端到端没跑通根本原因？ | 诚实 + 技术深度 / 技 | ✅ | `README.md` "复盘 §7"（缺 AgentOps 视角）|
| 协作上遇到的最大挑战？ | 协作 / HR + 行 | ✅ | README.md（决策复盘） |
| 压力大的时刻？ | 韧性 / HR + 行 | ✅ | README.md（决策复盘） |
| 算法 / 产品 / 团队冲突怎么处理？ | 多元 / 行 | ✅ | 三 STAR 故事综合 |
| 跟 CEO 直接共事是什么感受？ | 高 stake 协作 / 总 | ✅ | README.md（决策复盘） |
| 跟 mentor 之间最大分歧？怎么解决？ | 师徒协作 / 行 | ⚠️ | **GAP-43**：mentor 分歧场景未沉淀（可能是设计时讨论 vs 拍板）|

---

## 9. 横向调研类（最容易打穿 / 最值钱）

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| vs Flow-of-Action (WWW 2025)？ | 学术坐标 / 总 + 研 | ✅ | `README.md` "学术坐标" + `KNOWLEDGE/agent/multi-agent-rca-paradigm/` |
| vs Claude Code？ | 选型 / 技 | ✅ | `agent-subsystem.md` §8（三方比较：LangGraph StateGraph vs 自由 Agent Loop vs Claude Code harness）|
| vs 阿里云 AIOps 产品？ | 行业 / 技 | ⚠️ | `KNOWLEDGE/agent/agentops-vs-opsagent/` 有素材待整理——GAP-44 |
| **vs Datadog APM / Splunk Observability？** | 商业产品 / 总 | ❌ | **GAP-45（P0）**：商业 AIOps 产品矩阵 |
| **vs OpsAgent 后续出的开源（OpenAIOps 等）？** | 时代演进 / 总 + 研 | ❌ | **GAP-46（P0）**：2025.10 后的项目横向 |
| **vs LangGraph？** | 编排框架 / 技 | ⚠️ | **GAP-47（P0）**：补 LangGraph 对比段（合并到 GAP-7）|
| vs CrewAI / AutoGen？ | 多智能体框架 / 技 | ❌ | **GAP-48（P1）**：补主流框架横向 |
| 业界做根因分析的开源项目（OpsMind / robusta / Kepler / OpenAIOps）？ | 行业认知 / 技 + 研 | ❌ | **GAP-49（P1）**：开源 RCA 项目横向 |
| 学术界 RCA 主流方法？ | 学术 / 研 | ✅ | `KNOWLEDGE/agent/multi-agent-rca-paradigm/` |
| MCP 协议演进现状？2026 年生态？ | 行业 / 技 | ⚠️ | 2026 年 MCP 适配更广，需更新认知——GAP-50 |
| Anthropic Skills / OpenAI Assistants / Google Gemini Function Calling 横向？ | 工具 / 技 | ❌ | **GAP-51（P1）**：LLM 厂商 agent 工具栈对比 |
| 当下（2026）做相同项目怎么做？ | 时代演进 / 总 | ⚠️ | `README.md` "复盘 §2"+"学术坐标 §最后一段"有方向，缺具体技术栈——GAP-52 |

---

## 10. 领域知识类

| 挑战角度 | 测什么 / 谁问 | Readiness | 深答位置 / 行动 |
|---|---|---|---|
| AIOps 核心难点是什么？ | 领域 / 技 | ⚠️ | `KNOWLEDGE/agent/agentops-vs-opsagent/` AIOps 痛点段——GAP-53 |
| SRE 实际工作模式？on-call / playbook / postmortem？ | 领域 / 技 | ⚠️ | 项目里运维 mentor 经验，需整理——GAP-54 |
| 灰度发布业界做法（蓝绿 / 金丝雀 / Feature flag）？ | 领域 / 技 | ⚠️ | **GAP-55（P1）**：补三种灰度策略对比 |
| 黄金四指标来源（Google SRE）？ | 基础 / 技 | ✅ | 标准 SRE 概念（延迟 / 流量 / 错误 / 饱和度，Google SRE Book）|
| 微服务可观测性三大支柱？ | 基础 / 技 | ✅ | Metrics + Logs + Traces 是标准 |
| Prometheus 查询语法基础？ | 工具 / 技 | ⚠️ | 项目有 PromQL 接触但深度有限——GAP-56 |
| SLO / SLI / SLA 区别？ | SRE 基础 / 技 | ⚠️ | 概念知道但项目没显式用——GAP-57 |
| 故障的 MTTD / MTTR 行业平均？ | 行业数字 / 技 | ❌ | **GAP-58**：未沉淀行业数字 |
| OpenTelemetry 现状 + 与本项目关系？ | 工具 / 技 | ❌ | **GAP-59**：OTel 与项目 Prometheus / ARMS 栈关系未沉淀 |

---

## GAP 优先级清单（按落地紧迫度）

### P0 — 最高深问概率，2 周内补完

| GAP # | 内容 | 落地位置 |
|---|---|---|
| GAP-3 | 双路径（告警 + 体检）业务价值的定性 / 定量论证 | 加到 `interview-answers/qiniu-dual-trigger-rca.md`（新建）|
| ~~GAP-7 / GAP-47~~（已解决）| 已采用 LangGraph；原"vs Dify"问题不再成立；转为补充 **Agent Loop vs LangGraph StateGraph vs Claude Code 三方对比**（已在 `agent-subsystem.md` §8 落地）| —— |
| GAP-21 | 时序异常检测算法对比表（STL / Z-score / 孤立森林 / RPCA / Group-wise VAE / 季节性分解）| `interview-answers/qiniu-anomaly-detection-algos.md`（新建）|
| GAP-23 / GAP-24 | 20%→70% 评测设计细节（标注 / 匹配标准 / Precision-Recall / baseline） | `interview-answers/qiniu-rca-evaluation.md`（新建）|
| GAP-45 | 商业 AIOps 产品对比（Datadog / Splunk / New Relic / Dynatrace / Honeycomb）| `PROBLEMS/aiops-product-landscape/`（新建）|
| GAP-46 | 开源 OpsAgent 项目横向（OpenAIOps / robusta / Kepler / OpsMind）| 同上 |

### P1 — 中等深问概率，1 个月内

| GAP # | 内容 | 落地位置 |
|---|---|---|
| GAP-8 | MCP vs Function Calling 协议对比 | 补到 `agent-subsystem.md` §4 前或新建 `KNOWLEDGE/agent/mcp-vs-function-calling/` |
| GAP-11 | 灰度发布编排自实现 vs Argo Rollouts / Flagger 横向 | `PROBLEMS/canary-release-tooling/` |
| GAP-12 | Prompt 演进案例（v1→v3 改了什么解决了什么）| `agent-subsystem.md` 新增 §9 |
| GAP-13 | 上下文压缩具体策略（摘要 vs 关键片段 vs window slide）| 同上 |
| GAP-14 | Agent 间 JSON schema 演化过程 | 同上 |
| GAP-16 | Agent 工具调用失败 / 超时重试 / 降级策略 | `agent-subsystem.md` 新增 §10 |
| GAP-48 | CrewAI / AutoGen 横向 | 合并到 GAP-7/47 横向页 |
| GAP-49 | 开源 RCA 项目横向 | 合并到 GAP-45/46 横向页 |
| GAP-51 | LLM 厂商 agent 工具栈对比（Anthropic Skills / OpenAI Assistants / Google FC）| `PROBLEMS/llm-agent-tooling-landscape/` |
| GAP-55 | 蓝绿 / 金丝雀 / Feature flag 三种灰度策略对比 | `system-anatomy.md` §5 扩充或起 `KNOWLEDGE/methodology/canary-strategies/` |

### P2 — 低概率，兜底回答 / 被问时承认

| GAP # | 内容 | 兜底策略 |
|---|---|---|
| GAP-1 | Mock 数据生成 + 故障注入策略 | 项目里有相应 mock 设计，问到时回忆即可 |
| GAP-2 / GAP-6 | 业务侧 KPI / 数据驱动验证 | 承认"MVP 阶段以技术 KPI 为主，业务 KPI 未定义" |
| GAP-4 / GAP-5 | 巡检频率 + token 成本 | 承认"MVP 阶段未量化" |
| GAP-9 | zerolog 选型 | 团队栈，弱化 |
| GAP-10 / GAP-36 | 函数计算 vs K8s Job / 冷启动 | 承认"团队 mentor 推荐函数计算 + MVP 阶段未深究冷启动" |
| GAP-15 / GAP-18 | 角色冗余讨论 | 给"输出结构差异"的论证骨架 |
| GAP-17 | 模型选型公司理由 | "内网 + 合规 + 成本" 三段论 |
| GAP-19 / GAP-20 | chunk size + embedding 模型选型 | 团队默认 + 项目未做消融 |
| GAP-22 / GAP-25 / GAP-27 | 算法预处理 / test case 数量 / 延迟数据 | 承认"MVP 阶段未做严格量化" |
| GAP-26 | 火焰图实际效果 | 承认"展示性大于实际效果" |
| GAP-28 / GAP-29 / GAP-30 | ARRAY 索引 / event_log 分区 / schema migration | 承认"MVP 阶段未到工程优化" |
| GAP-31 / GAP-32 | VectorDB / Redis 选型理由 | 团队栈或现成基础设施 |
| GAP-33 / GAP-34 / GAP-35 | K8s 部署 / 灰度自动化 / CMDB mock 来源 | 承认"实现细节遗忘"或查阅资料 |
| GAP-37 — GAP-42 | CI/CD / 代码规模 / E2E 测试 / 自监控 / 仓库结构 / git 协作 | 承认"MVP 阶段未到完整工程化"——这是 GAP-40 同时关联到"AgentOps 视角缺位" |
| GAP-43 | 跟 mentor 分歧场景 | 准备 1-2 个具体场景兜底（设计讨论 vs 拍板 vs SOP 设计协作）|
| GAP-44 / GAP-50 / GAP-52 | 阿里云 AIOps / MCP 生态 / 当下重做技术栈 | 项目有素材，被问时整合即可 |
| GAP-53 / GAP-54 / GAP-56 / GAP-57 / GAP-58 / GAP-59 | AIOps 难点 / SRE 工作模式 / PromQL / SLO / MTTD / OTel | 领域知识类，深度按需而定 |

---

## 维护规则（living document）

1. **每次 mock / 正式面试**遇到新问题 → 立刻追加一行（写挑战 + 测什么 + 当时回答的 readiness 评级 + 是否要补 GAP）
2. **完成一个 GAP** → 把对应行的 readiness 升级（❌ → ⚠️ → ✅）+ 更新深答位置
3. **GAP 优先级动态调整**——某个角度被反复问到，从 P2 升 P1，从 P1 升 P0
4. **季度回顾**——检查所有 ⚠️ 是否可以推到 ✅，所有 ❌ 是否还需要 / 还相关
5. **新增类别**——如果出现一个挑战角度不属于现有 10 类，新建第 11/12 类（不要硬塞）

---

## 不在本文档讨论的内容

- 决策叙事 / 时代背景 / 复盘 → `README.md`
- 系统 6 层架构 / API / DB / 流程图 → `system-anatomy.md`
- Agent 5 角色 prompt / MCP / 工作流 / 20%→70% 路径 → `agent-subsystem.md`
- 单题深答（每篇 5-10 页）→ `CAREER/interview-answers/qiniu-*.md`
- 行为题 STAR 故事 → README.md 决策复盘（STAR 卡已退场）
- 学术坐标 / 工业范式 / Failure Attribution → `KNOWLEDGE/agent/agentops-vs-opsagent/` + `multi-agent-rca-paradigm/` + `agent-failure-attribution/`
