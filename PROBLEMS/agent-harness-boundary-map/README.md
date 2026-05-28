# Agent Harness 边界图：Context / Evaluation / Tool Repair / Memory

> Harness 不是一个单点工具，而是一组围绕模型边界建立的工程控制层。这个页用来回答一个面试高频问题：什么时候该加 Harness，什么时候该信模型，什么时候该把问题改成检索、记忆或评估系统？

## 问题定义

Agent 失控时，表面现象可能都是"模型没做好"：上下文漂移、工具参数错、评估写偏、同类错误反复出现。但不同失败对应的干预点完全不同。

这个问题的核心是：**如何按失败信号选择 Harness 类型，并判断它是在补模型短板，还是在构建长期可复用的系统能力。**

## 为什么重要

面试官问 Harness、Context Engineering、Agent Memory、RAG 评估时，常常不是要听一个名词定义，而是在测试你能不能把开放的 LLM 行为拆成可观测、可修复、可复用的工程边界。

如果只说"加 prompt / 加 RAG / 加校验"，回答会显得散。更好的回答是先画边界：这个失败发生在输入上下文、工具接口、评估生成、还是跨任务经验复用？每一层的控制手段和风险都不同。

## 候选方案

| 方案 | 核心思路 | 优势 | 劣势 | 适用场景 | 来源 |
|---|---|---|---|---|---|
| **Context Harness** | 控制模型在当前任务看到什么、按什么顺序看、哪些信息必须持续锚定 | 直接影响推理质量；能降低上下文噪声、漂移和 lost-in-the-middle 风险 | 过度压缩会丢关键证据；过度注入会把长上下文变成噪声池 | 长链路 research、coding、RAG、多轮计划执行 | `KNOWLEDGE/agent/context-engineering/`、`KNOWLEDGE/agent/agent-context-compaction/`、`KNOWLEDGE/agent/agentic-rag-vs-long-context/` |
| **Evaluation Harness** | 用过程指令、评估模板、实时文档和轨迹输入约束"让模型写评估代码"这件事 | 把一次性成败变成可诊断指标；减少指标泛滥、计划实现漂移、过度工程化 | 指标仍需项目定制；LLM-as-judge 可能偏好表面完整的轨迹 | Agent 评测、回归测试、工具轨迹质量分析 | `KNOWLEDGE/agent/agent-evaluation-harness/` |
| **Tool Call Repair Harness** | 先 schema 校验，再只沿失败字段做有限修复，并记录错误分布 | 对可枚举格式错误非常有效；正常路径零改写；能释放弱模型工具调用能力 | 过度宽容会掩盖真实语义错误；修复规则强模型 / 工具相关 | function calling、文件工具、API 工具、结构化输出 | `KNOWLEDGE/agent/tool-call-repair-harness/`、`KNOWLEDGE/agent/structured-output/`、`KNOWLEDGE/agent/agent-tool-design/` |
| **Memory / Skill Harness** | 把可复用知识、偏好、失败经验、procedural workflow 外化为可检索 / 可调用的长期状态 | 解决经验不积累；跨会话复用；能把隐性组织知识变成 Agent 可用资源 | 写入策略、召回策略、遗忘策略难；错误记忆会造成长期污染 | 长期个人助手、代码库 Agent、工作流复用、团队规范注入 | `KNOWLEDGE/agent/agent-memory-system/`、`KNOWLEDGE/agent/agent-skills-closed-loop/`、`PROBLEMS/agent-memory-architecture/` |
| **Boundary Probing Harness** | 用真实任务探针持续测模型在上下文、工具、长程行为上的能力曲线 | 不绑定某个模型；能决定哪些 Harness 该保留、哪些可删 | 需要持续维护探针；容易退化成另一个过拟合 benchmark | 新模型接入、模型升级、Agent 平台选型 | `KNOWLEDGE/agent/model-boundary-probing/`、`KNOWLEDGE/agent/harness/` |

## 比较维度

### 1. 失败信号：先看坏在哪里

| 失败信号 | 更可能的 Harness | 判断依据 |
|---|---|---|
| 模型跑着跑着忘目标、证据被淹没、计划和执行脱节 | Context Harness | 失败随上下文长度、信息顺序、压缩策略变化 |
| 最终答案错，但轨迹里不知道是调错工具、漏证据、还是恢复失败 | Evaluation Harness | 只有结果标签，没有中间行为指标 |
| 工具调用参数类型错、字段多传 `null`、数组字符串化、路径被格式化 | Tool Call Repair Harness | 错误集中在可枚举 schema 形状，不是业务推理错误 |
| 同一个偏好、规范、踩坑在不同会话反复解释 | Memory / Skill Harness | 信息对单次任务不是必需知识，但对长期行为稳定性重要 |
| 换模型后旧补丁失效，或不知道新模型能不能吃掉旧工程 | Boundary Probing Harness | 需要能力曲线，而不是一次 benchmark 分数 |

### 2. 干预点：输入、过程、接口、长期状态

Context Harness 改的是**当前输入分布**：把任务目标、证据、约束、历史摘要组织成更适合模型利用的上下文。

Evaluation Harness 改的是**评估生成过程**：让模型先按结构理解 agent，再写少量可跑、可比较的指标。

Tool Call Repair Harness 改的是**模型输出和工具 schema 的接口边界**：不改变任务语义，只修复可确定的格式错位。

Memory / Skill Harness 改的是**跨任务状态**：让下一次任务不从零开始。

Boundary Probing Harness 改的是**工程决策依据**：决定哪些失败是模型边界，哪些是系统设计没给足结构。

### 3. 确定性 vs 模型参与

Tool Call Repair 最适合确定性：schema 校验、有限修复、二次校验都应该尽量不让模型参与。

Context 和 Memory 介于中间：检索、压缩、排序可以确定性实现，但"哪些信息重要"经常需要模型判断。

Evaluation 和 Boundary Probing 更依赖模型，但必须被模板、指标数量、测试场景和人工审查约束。否则它们会把开放性带进本来应该提高确定性的环节。

### 4. 观测指标：Harness 本身也要被评估

| Harness | 主要观测指标 |
|---|---|
| Context Harness | 任务成功率、证据命中率、上下文 token、压缩后信息保真、长链路漂移次数 |
| Evaluation Harness | 评估代码一次跑通率、指标数量、指标和轨迹相关性、计划实现一致性 |
| Tool Call Repair Harness | 原始 schema 失败率、修复成功率、二次校验失败率、误修复率、按模型 / 工具分布的错误地图 |
| Memory / Skill Harness | 召回命中率、错误记忆率、跨任务复用收益、写入噪声、遗忘 / 合并成本 |
| Boundary Probing Harness | 探针覆盖面、模型版本间差异、Harness 删除 / 保留决策的准确性 |

### 5. 什么时候该删除 Harness

Harness 不是越多越专业。模型升级后，如果某类错误稳定消失，旧 Harness 可能变成复杂度债务。

可以删除或弱化的信号：

- 修复层长期没有触发，且新模型在 shadow eval 中 schema 失败率接近 0
- context 压缩带来的收益低于信息丢失风险
- memory 召回经常引入过期信息，净收益为负
- evaluation 指标长期不能解释真实故障，只是在报告里占位置

应该保留的信号：

- 它保护的是业务不变量、安全边界、权限边界，而不是单个模型弱点
- 它沉淀了组织内部知识、项目规范、合规约束
- 它能产生遥测，持续画出模型和系统的错误地图

## 推荐回答框架

面试时可以用这条主线：

> 我会先把 Agent 失败分到四个边界：上下文边界、工具接口边界、评估边界、长期经验边界。上下文问题用 Context Harness 控制信息形态；工具格式问题用 schema-first repair；评估问题用模板和轨迹约束；重复经验问题用 Memory / Skill。最后用 Boundary Probing 定期重测模型能力，决定哪些补偿层该保留、哪些该删。

这个回答比单独说"我会加 RAG / 加 prompt / 加校验"更强，因为它把每个工程动作绑定到了可观测的失败信号。

## 相关知识节点

- `KNOWLEDGE/agent/context-engineering/`
- `KNOWLEDGE/agent/agent-context-compaction/`
- `KNOWLEDGE/agent/agentic-rag-vs-long-context/`
- `KNOWLEDGE/agent/agent-evaluation-harness/`
- `KNOWLEDGE/agent/tool-call-repair-harness/`
- `KNOWLEDGE/agent/model-boundary-probing/`
- `KNOWLEDGE/agent/agent-memory-system/`
- `KNOWLEDGE/agent/agent-skills-closed-loop/`
- `PROBLEMS/agent-memory-architecture/`

## Open Questions

- Boundary probing 的探针如何设计，才能覆盖真实任务而不是变成另一个固定 benchmark？
- Tool repair 的宽容度如何设定，才能修格式错而不掩盖语义错？
- Memory / Skill Harness 如何把"可复用经验"和"过期偏见"区分开？
- Evaluation Harness 里的 LLM-as-judge 如何校准，避免奖励长而复杂但无效的执行轨迹？
