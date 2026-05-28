# 字节跳动飞书 · Agent 后端实习

## 投递状态

| 字段 | 内容 |
|---|---|
| 状态 | 已投递 |
| 投递日期 | 2026-05-17 |
| 渠道 | 待补 |
| 联系人 | 待补 |
| 材料版本 | CV 主版本 |
| 下一步 | 等回复；优先补 MCP / LangGraph state / Agent eval / RAG 诊断 / Attention 手撕 |
| 跟进日期 | 2026-05-20 至 2026-05-22 |
| 详情来源 | JD：`RAW_SOURCES/jd-and-interviews/bytedance-feishu-agent-backend-intern.md`；面经：`RAW_SOURCES/jd-and-interviews/bytedance-feishu-agent-interview-xiaohongshu.md` |

## JD 快照

ByteIntern 面向 2027 届毕业生，符合岗位要求可提供转正机会。团队是飞书，字节跳动旗下 B 端企业协作平台，覆盖即时沟通、日历、视频会议、云文档、企业邮箱、服务台，以及 OKR、招聘、绩效等组织管理产品。

岗位职责聚焦飞书业务场景下 Agent 产品 / 功能的后端系统设计与开发，构建高性能、可扩展服务架构；参与 Agent 系统后端架构设计与瓶颈治理，确保稳定性、高并发和大数据能力；优化系统性能、架构升级和服务器资源管理；设计实现 AI 能力调用框架，推动 AI Agent 工程化落地。

## 匹配判断

### 强匹配

- **B 端 Agent 场景**：七牛云 AI 运维 Agent 和华为目标方向一样，都能证明你理解企业内部复杂业务场景中的 Agent 落地。
- **Agent 工程化**：Neo DeepResearch / ReAct Agent、七牛云多智能体 RCA 系统都能支撑工具调用、工作流编排和 AI 能力调用框架相关追问。
- **后端工程基础**：CV 里有 Python、Go、Gin、gRPC、微服务、数据库和中间件经验，可以对应后端系统设计与高可用服务。
- **AI Coding / GitHub 信号**：Neo 开源 AI Agent 框架 SDK 260+ stars + 海外社区协作，对应 JD 的 GitHub 贡献和个人技术项目优先项。
- **产品思维**：七牛云项目中做过产品定位、MVP 收敛、API 定义、数据表设计、模块拆分和联调，可以对应飞书业务场景下的产品功能开发。

### 风险点

- 这条比华为更偏后端工程，不是纯算法 Agent；面试会更可能问服务架构、瓶颈治理、性能优化、资源管理。
- JD 明确提到高并发、大数据、稳定性，需要准备系统设计和工程细节，不能只讲 LangGraph / RAG。
- 飞书是成熟 B 端协作产品，面试可能更看重产品迭代速度、工程可靠性和跨团队协作。

### 一句话定位

> B 端企业协作 Agent 后端岗位，适合用“多智能体应用落地 + 后端工程 + AI 能力调用框架”来投，不适合只按算法岗讲。

## 本岗位使用材料

| 材料 | 内容 |
|---|---|
| CV 版本 | CV 主版本 |
| 打招呼话术 | 您好，我是港城大 AI 硕士，做过企业级多智能体 Agent、LangGraph 工作流和 RAG 工具路由，也有 Python / Go / gRPC / 微服务工程经验，和飞书 Agent 后端工程化方向比较匹配，想进一步沟通实习机会。 |
| 重点强调项目 | 七牛云 AI 运维 Agent；Neo DeepResearch / ReAct RAG 路由；Neo 开源 SDK；工程技能段 |
| 不主动强调内容 | 过深的 Web3 业务细节；过研究化的 Agent Memory 实验，除非对方问 |

## 面试准备

### 小红书面经高频信号

| 优先级 | 主题 | 典型追问 | 当前准备策略 |
|---|---|---|---|
| P0 | MCP / 工具封装 | MCP 协议做什么；schema 格式；如何封装 API；参数校验；工具失败处理；函数鉴权 | 用七牛云 MCP Server + Neo 工具 schema 路由讲，必须准备一个具体 API 工具例子 |
| P0 | LangGraph state | state 机制；分布式状态怎么管；key / value 怎么设计 | 用 DeepResearch 节点状态讲 typed state、checkpoint、thread / task id、node output |
| P0 | Agent evaluation | 业务 Agent evaluation 流程；指标含义；多调用 / 少调用工具；多参数 / 少参数 | 结合 `PROBLEMS/agent-harness-boundary-map/`，准备 tool precision / recall / parameter accuracy |
| P0 | RAG 诊断 | chunk 非 Markdown 文档；embedding 选型；dense retrieval；rerank；检索错还是生成错 | 用 Neo RAG 路由六层 failure map：query / chunk / description / recall / rerank / generation |
| P1 | 场景系统设计 | 日志风险评级 Agent；多维表格数据 → Dify 处理 → 写回表格；长篇小说生成框架 | 按输入源、任务编排、模型调用、工具调用、状态存储、评测闭环回答 |
| P1 | 基础手撕 | 原生库 / NumPy 手写 multi-head attention | 复习 QKV shape、mask、softmax、head concat、output projection |
| P1 | GraphRAG / 知识库构建 | GraphRAG 原理、优势、知识库如何构建 | 准备“实体关系强、多跳问题强时用图；成本是抽取和维护” |
| P2 | 微调 / 训练评测 | 数据集大小、构建方式、模型选择、训练评测流程 | 诚实讲方法论 + KB，不包装成已有大规模实战 |

### JD 定向准备

| 可能追问 | 准备材料 |
|---|---|
| Agent 产品后端系统怎么设计？ | API 层、任务编排层、模型调用层、工具层、状态存储、异步队列、观测与降级 |
| AI 能力调用框架要解决什么？ | 多模型接入、prompt / tool schema 管理、上下文构造、调用限流、重试、fallback、成本与日志 |
| 高并发和稳定性怎么保证？ | 缓存、异步化、限流、熔断、降级、幂等、超时重试、任务队列、可观测指标 |
| 七牛云项目里哪些能证明后端能力？ | MCP Server 工具封装、多源数据查询、模块拆分、API 定义、联调、主动巡检数据中间层 |
| 你熟悉 LLM 应用开发体现在哪里？ | LangChain / LangGraph、ReAct、RAG、工具调用、上下文注入、Agent 评估与失败诊断 |
| 你有 AI Coding 实践吗？ | 这个 OS 和项目文档 / 代码协作流程；强调能用 AI 工具提升工程效率，但仍由自己做架构判断 |
| QA 业务型 Agent 和 DeepSearch Agent 的差别？ | QA 业务 Agent 目标是业务流程闭环和准确调用工具；DeepSearch / DeepResearch 目标是多步信息获取、证据整合和报告生成 |
| RAG 文档不是 Markdown 怎么处理？ | 不说“默认一样”；按文档类型解析成统一中间表示，保留标题层级、表格、字段、metadata，再分类型 chunk |
| 工具多调用但结果对，怎么评估？ | 最终任务成功之外增加 tool precision、冗余调用率、成本、延迟；不能只用 answer correctness |

## 沟通记录

| 日期 | 对象 | 内容 | 下一步 |
|---|---|---|---|
| 2026-05-17 | 待补 | 已投递 | 等回复；3-5 天无回应再跟进 |

## 复盘

### 面试问题

- 待补。

### 暴露缺口

- MCP schema / 鉴权 / 参数校验需要准备到具体 API 例子级别。
- LangGraph state 不能只讲概念，需要讲 key / value、checkpoint 和分布式状态边界。
- RAG 非 Markdown 文档处理不能再说默认一样，需要准备文档解析与 chunk 策略。
- Attention 手撕需要复习公式、张量 shape 和 NumPy 写法。

### 后续动作

- 准备一个“Agent 后端系统设计”口径：入口 API、任务状态、模型调用、工具调用、异步队列、观测与降级。
- 准备高并发稳定性基础题：缓存、限流、熔断、幂等、重试、消息队列。
- 准备一个 MCP API 工具例子：schema、必填 / 可选参数、鉴权、校验、错误码、重试和超时。
- 准备一页 LangGraph state 讲稿：state 字段、节点输入输出、checkpoint key、分布式部署时的存储边界。
- 准备 Agent evaluation 指标表：task success、tool precision / recall、parameter accuracy、redundant call rate、latency、cost。
- 复习 NumPy multi-head attention 手撕。
- 如果进入面试，优先把七牛云经历从“算法 Agent”重讲成“企业级 AI 子系统后端工程”。
