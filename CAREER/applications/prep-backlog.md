# Interview Prep Backlog

> 从 active JD / 面经反推的短期学习清单。它替代 `skill-gap.md` 作为日常备面入口。
>
> 使用方式：每次新增 active 岗位或面经，先把暴露的空白加到这里；学完后再决定是否沉淀到 `KNOWLEDGE/` 和 `_self_check`。

## 当前主线


| 方向       | 说明                                                                   | 对应岗位                 |
| -------- | -------------------------------------------------------------------- | -------------------- |
| Agent 开发 | MCP、LangGraph、RAG、工具调用、后端系统设计、Agent evaluation                       | 华为集团 IT、字节飞书         |
| Agent 算法 | Transformer / Attention、embedding / rerank、SFT / RLHF / GRPO、微调与评测流程 | 华为 AI 模型工程师方向、飞书面经二面 |


## P0：本周必须补到能答


| 主题                                       | 来源             | 要能答到什么粒度                                                                                                   | 当前材料                                                                                     | 补完后去向                                                             |
| ---------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| MCP schema / API 封装 / 鉴权 / 失败处理          | 飞书质量效能面经、华为 JD | 拿七牛云一个日志 / 指标工具举例：schema、必填/可选参数、权限校验、超时、重试、错误码、返回结构                                                       | `CAREER/interview-bank/technical/internships.md` C2；`KNOWLEDGE/agent/agent-tool-design/` | 稳定后新建 `KNOWLEDGE/agent/mcp-tool-schema-and-auth/`                 |
| LangGraph state / checkpoint / key-value | 飞书面经           | 能讲 state object、节点读写、checkpoint key、thread_id / task_id、分布式存储边界                                            | Neo DeepResearch CV bullet；`PROJECTS/work/neo-deepresearch-and-react-agent/`             | 稳定后新建 `KNOWLEDGE/agent/langgraph-state/`                          |
| Agent evaluation 指标                      | 飞书面经           | 区分 task success、tool precision / recall、parameter accuracy、redundant call rate、latency、cost；能解释多调用但答案对怎么扣分 | `PROBLEMS/agent-harness-boundary-map/`；`KNOWLEDGE/agent/agent-evaluation-harness/`       | 可派生 `CAREER/interview-bank/technical/agent-evaluation-metrics.md` |
| RAG 非 Markdown 文档处理与诊断                   | 飞书面经           | 不同文档类型先解析成统一中间表示；保留标题、表格、metadata；能判断 query / chunk / embedding / rerank / generation 哪层错                  | Neo router working draft；`KNOWLEDGE/agent/rag-failure-diagnosis/`                        | 稳定后新建 `KNOWLEDGE/agent/rag-document-processing/`                  |
| NumPy 手写 multi-head attention            | 飞书面经           | 能写 Q/K/V projection、reshape heads、scaled dot-product、mask、softmax、concat、output projection                 | `KNOWLEDGE/transformer/multi-head-attention/`                                            | 若公式不稳，补 `KNOWLEDGE/transformer/attention-scaling/`                |


## P1：有余力补


| 主题                                        | 来源          | 要能答到什么粒度                                      | 当前材料                    | 补完后去向                                  |
| ----------------------------------------- | ----------- | --------------------------------------------- | ----------------------- | -------------------------------------- |
| GraphRAG / 知识库构建                          | 飞书面经        | 什么时候需要图；实体 / 关系抽取；相比普通 RAG 的优势和维护成本           | 暂无稳定节点                  | 按出现频率决定是否建 `KNOWLEDGE/agent/graphrag/` |
| AI Agent 后端系统设计                           | 飞书 JD / 面经  | API 层、任务编排、模型调用、工具层、状态存储、异步队列、观测、降级           | 飞书 application 记录       | 可派生 technical 题                        |
| 大模型训练评测流程串讲                               | 飞书二面、华为模型方向 | 从 pretrain / SFT / RLHF / eval / deploy 串成一张图 | `KNOWLEDGE/training/*`  | `fundamentals.md` 已覆盖，按需补题             |
| Attention scaling / RoPE / FlashAttention | 飞书手撕、通用八股   | 能讲公式、反事实和工程意义                                 | `fundamentals.md` gap 表 | 建 transformer 节点                       |


## 判断规则

- 只被一个岗位问、且很场景化：留在对应 `applications/active/<岗位>.md`。
- 多个岗位都问，且能复用：进入 `interview-bank/technical/`。
- 已经学成稳定知识：进入 `KNOWLEDGE/`，并同步 `_self_check`。
- 和个人经历强相关：优先补 `PROJECTS/work/` 或 `interview-bank/behavioral/`，不要只写抽象知识。
