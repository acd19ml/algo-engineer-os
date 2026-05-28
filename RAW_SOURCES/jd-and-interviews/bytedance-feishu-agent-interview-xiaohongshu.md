# 字节 / 飞书 Agent 面经汇总（小红书分享）

> 来源：用户粘贴的小红书面经摘录。
> 时间：2026-05-17。
> 用途：支撑 `CAREER/applications/active/2026-05-17_bytedance-feishu_agent-backend-intern.md` 的面试准备。
> 说明：本文做结构化整理，不直接作为事实预测；不同部门 / 面试官会有差异。

## 来源 A：飞书质量效能工程部 Agent 面经

### 技术追问

| 主题 | 具体问题 |
|---|---|
| MCP API 封装 | 基于 MCP 协议封装 API 具体怎么做；做了哪些参数校验；举例说明；工具调用失败如何处理 |
| LangGraph state | LangGraph 的 state 机制是什么；在项目里如何做分布式状态管理；状态存储使用什么 key / value |
| Agent evaluation | 项目评测环节怎么做；是否存在函数多调用 / 少调用；是否存在参数多传 / 少传；需要举具体例子 |
| 鉴权 | 函数调用鉴权怎么做 |
| MCP 协议理解 | MCP 协议具体做什么 |

### 场景题

有一个错误日志系统，日志里包含人员、负责人等信息。需要做一个 AI Agent 识别日志风险等级，如何设计评级方案。

### 反思信号

分享者提到大部分问题只能答一两个点，没法把原因、前因后果说清楚。对本仓库的启发是：准备时不能只背关键词，要准备“场景 → 设计 → 失败 case → 指标 → 取舍”的完整链条。

## 来源 B：飞书 Agent 面经

### 面试流程与问题

| 阶段 | 问题 |
|---|---|
| 开场 | 自我介绍 |
| 项目差异 | QA 业务型 Agent 和 DeepSearch / DeepResearch Agent 的差别 |
| 项目模式 | 解释项目 1 Agent 的工作模式 |
| MCP | MCP schema 格式；MCP 协议大概包含哪些内容 |
| Evaluation | 业务 Agent evaluation 流程；每个指标代表什么；如果 tools 被多调用但不影响结果，如何设计指标描述 |
| RAG chunk | RAG 文档如何 chunk；如果预输入不是 Markdown，且不同文档类别上下文格式不同，如何处理 |
| Retrieval | embedding 模型选型原则；稠密检索算法原理；rerank 算法原理 |
| RAG 诊断 | 如何判断 RAG 某个环节是检索出问题还是生成出问题 |
| 手撕 | 原生库 / NumPy 手写 multi-head attention |

### 反问与反思

分享者反问了本次哪里需要改善以及部门业务。个人反思是：做深的项目应该放前面；面试不能太多停顿；手撕时要记住公式和张量形状。

## 来源 C：字节飞书 AI 工程开发实习生面经

### 背景信号

分享者背景是双非本科 + 211 硕士研二，有一年 TOP2 交叉领域课题组实习，方向偏大模型应用，包括 RAG、提示词和 Agent。

### 一面

| 类型 | 问题 |
|---|---|
| 项目介绍 | 自我介绍；介绍两段实习项目 |
| RAG 深挖 | 实习 RAG 项目具体怎么做；是否用 GraphRAG；GraphRAG 原理、优势、知识库如何构建 |
| 微调 | 微调怎么做；微调数据集大小；数据集如何构建；用什么模型 |
| 具体工程问题 | 使用 reportlab 生成 PDF 时，表格跨页错误如何处理 |
| Transformer 项目 | 手写 Transformer / 红楼梦续写项目；词表构建、模型架构、自回归生成怎么做 |
| 代码 / 场景考核 | 多维表格数据获取 → 用 Dify 处理 → 保存回多维表格，20 分钟给完整解决方案 |

### 二面

| 类型 | 问题 |
|---|---|
| 项目介绍 | 介绍项目 |
| 大模型知识图谱 | 从 Transformer / GPT 到最新大模型的发展历程 |
| 训练评测流程 | 从模型训练、评测整体流程，把涉及知识点分门别类讲清楚 |
| CS 课程串讲 | 假设对方是计算机学院老师，串讲相关课程和工作原理 |
| 代码 / 系统设计 | 设计并实现一个基于大模型的长篇小说生成框架，可参考 LangChain，涉及 models、chain、memory 等类 |

### HR 面

- 个人信息
- 如果发生分歧怎么处理
- 上一段实习最大的挑战和收获
- 是否有其它 offer

## 对本岗位准备的高频主题

| 优先级 | 主题 | 准备要求 |
|---|---|---|
| P0 | MCP 协议和工具封装 | 能讲 schema、参数校验、鉴权、失败处理、重试、超时、错误返回 |
| P0 | LangGraph state | 能讲 state object、节点间状态传递、checkpoint / store、分布式场景下 key-value 设计 |
| P0 | Agent evaluation | 能讲 task success、tool precision / recall、参数正确率、多调用 / 少调用 / 多参数 / 少参数如何计量 |
| P0 | RAG 诊断 | 能拆 query、chunk、embedding、retrieval、rerank、generation 六层，并给 failure case |
| P1 | 后端系统设计 | 能设计 AI 能力调用框架、日志风险评级 Agent、多维表格 + Dify 处理链路 |
| P1 | Transformer / attention 手撕 | 至少能写出 NumPy multi-head attention 的 QKV、mask、softmax、concat、projection |
| P1 | GraphRAG / 知识库构建 | 能解释什么时候需要图结构、实体关系如何构建、优势和成本 |
| P2 | 微调和训练评测 | 能说数据构建、SFT / RL / eval 基本流程，不必强行包装成实战 |
