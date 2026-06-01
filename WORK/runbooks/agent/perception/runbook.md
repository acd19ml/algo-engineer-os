# Agent Runbook · Perception

> 索引和使用方式在 [README.md](../README.md)。模板在 [`META/templates/runbook_entry.template.md`](../../../../META/templates/runbook_entry.template.md)。

---

## P-019：RAG 回答不准，不知道是哪一环坏了

`type: diagnostic-procedure`   `severity: reversible-cheap`

**症状**
- 用户反馈 RAG 答案错 / 不全 / 答非所问
- 第一反应是换 embedding / 调 chunk size / 加 reranker

**根因**

RAG pipeline 长——数据源 → chunking → query 理解 → embedding → 排序——错可能发生在任何一环。上游错会伪装成下游错；没定位就调参，所有优化都可能只是噪声。

**前置条件**
- 能拿到若干 bad case（用户 query、错误回答、期望答案）
- 能查看知识库原文、实际 chunk、检索 TopK / TopN 排名
- 关卡 4 需要一小组标注 query → 应召回文档的 eval set

**当前方案**

*关卡 1：答案到底在不在知识库里*

抽几个 bad case，**人工到知识库里找答案**：
- 找不到 → 修 ingestion / OCR / 文档同步 / 数据源更新
- 找得到 → 进关卡 2

*关卡 2：看 bad case 对应的实际 chunk 长什么样*

不要看配置，看**失败样本实际的 chunk 内容**：
- 答案是否被切断？（chunk size 太小把条件和流程切成两半）
- 是否被淹没？（chunk 太大混了多个话题，相关几句被无关稀释）
- 是否缺标题或上下文？

出问题 → 调 chunk size / overlap / 按标题层级切分 / 保留表格和段落结构。没问题 → 进关卡 3

*关卡 3：检查 query 和 doc 的词面是否错位*

例：用户问"手机发烫怎么办"，文档写"设备温度异常处理方案"。

错位明显 → Query rewrite / Query expansion / HyDE / 混合检索（向量 + 关键词）。不错位 → 进关卡 4

*关卡 4：做小评测集量化 embedding 在领域的表现*

标注每个 query 应召回哪些文档，算 recall@K / MRR / 命中率。

- 大量**领域术语 case** 召回低 → 通用 embedding 在垂直域水土不服。考虑换模型 / 领域微调 / 构造正负样本
- 命中率不低 → 进关卡 5

只有确认不是数据源 / chunk / query 表达问题后，这一步才有解释力。

*关卡 5：召回了但排序在 TopK 外*

把 retrieval 范围放宽到 Top20 / Top50 查正确 chunk 排名：
- 在 Top20 但不在 Top5 → 加 cross-encoder reranker（初始 Top20-50 → reranker 精排 → 最终 Top5）
- 完全没召回 → 回去重审关卡 1-4

reranker 只适合小候选集精排，不适合全库扫描。

**适用与失效**
- 适用：单轮 RAG（一次检索、一次回答）
- 失效：多轮 Agentic RAG——一次回答可能多次检索 + 多次判断，传统 recall@K 不能直接解释"中间哪一步查错了"。需要轨迹级评估

**源**

`[[rag-failure-diagnosis]]`。验证状态：部分验证（结构化思路已被多个生产 RAG 系统验证）。

**See also**
- P-039 Query 改写降低检索效果
- `[[rag-query-rewriting]]` · `[[agentic-rag-vs-long-context]]` · `[[agentic-rag-planning-cache]]`

---

## P-039：Query 改写后检索效果反而下降

`type: remedy-menu`   `severity: reversible-cheap`

**症状**
- 加了 query rewriting 之后，RAG 召回率反而下降
- 用户问"怎么开白名单"，被改写成"如何将特定用户添加到访问许可列表中"；文档里恰好用的是"白名单"这个词
- 业务缩写被通用模型错误扩展（"HP"改写为"Hewlett-Packard"，但业务里 HP 指 Hearing Preparation）
- 或者反过来：简单查询也全部经过改写，成本和延迟上升但效果没改善

**根因**

通用大模型在缺乏业务上下文时，会把业务语言拉回通用语言；而 RAG 检索恰恰需要贴近知识库语言。无条件改写对所有 query 无差别应用，浪费成本且可能降质。

**当前方案**

*方案 1：改写前先路由分类（默认先上）*

- 简单查询（单个明确实体 / 直问直答）→ 直接检索，不经过改写
- 复杂 / 模糊 / 跨域查询 → 进改写流程

不要对所有查询都改写——简单查询改写是纯增加成本。

*方案 2：在改写 prompt 里注入业务术语约束*

对命中的业务术语动态注入解释——用户 query 先检索业务术语库，把命中的几条注入改写 prompt（"HP=Hearing Preparation，指庭审准备阶段"），让模型改写时不改掉业务词。

*方案 3：先做实体识别，再改写*

识别 query 里的产品名 / 缩写 / 内部专有词，锁定这些实体后再改写——只改措辞，不改业务词。

**适用与失效**
- 适用：有领域特定术语 / 缩写 / 内部词汇的业务 RAG 系统
- 失效：通用域（不存在业务术语偏差的场景）；检索效果本来就好时改写是冗余成本
- 失效：方案 3 的实体识别在高度新颖的内部词汇上可能识别不全，需要维护业务词典

**源**

`[[rag-query-rewriting]]`。验证状态：未验证（外部 case，未在本地项目实例化验证）。

**See also**
- P-019 RAG 全链路诊断（先排查本条问题属于哪一层）
- `[[route-before-rewrite]]`（DC pattern）
