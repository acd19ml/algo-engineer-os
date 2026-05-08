# Self-Check: Agent

> 日常自检：从上往下看题，能答出来跳下一题；卡住就点链接跳到知识节点重新学。
> 答案不在这里——答案在链接的节点里。

---

## Agent 工程师核心能力

- [浅] Agent 工程师的 4 件核心事是什么？它们各自对应传统软件工程的什么概念？ → `KNOWLEDGE/agent/agent-engineer-ability/`
- [浅] "补偿性工程" 和 "系统性工程" 的根本差别是什么？哪一类会随着模型变强而消失？ → `KNOWLEDGE/agent/agent-engineer-ability/`
- [中] 为什么说 "上下文不是数据，上下文就是程序本身"？这和传统后端的 Service + Redis 模式有什么根本不同？ → `KNOWLEDGE/agent/agent-engineer-ability/`
- [中] Agent 控制流和传统流程编排的差别——"你写死 A→B→C" vs "你设计棋盘让模型在棋盘内决策"——具体怎么落地？计划机制 / 任务依赖图 / 自主认领举一个例子。 → `KNOWLEDGE/agent/agent-engineer-ability/`
- [中] OpenAI Codex 团队的"agent 出错时不应该让它再试一次"——为什么 retry 在传统开发是合理策略，在 agent 智能故障上是错的？ → `KNOWLEDGE/agent/agent-engineer-ability/`
- [深] "模型越强就不需要 agent 工程"——这个论点为什么错？用 CPU/操作系统的类比说明。 → `KNOWLEDGE/agent/agent-engineer-ability/`

## 上下文工程

- [浅] Context Engineering 和 Prompt Engineering 的根本区别是什么？为什么单轮问答两者差别不大、agent 场景差别巨大？ → `KNOWLEDGE/agent/context-engineering/`
- [中] 上下文工程的目标是 "用最小的高信噪比 token 集合最大化期望结果概率"——这句话反直觉在哪？ → `KNOWLEDGE/agent/context-engineering/`
- [中] Compaction、Structured Note Taking、Just-in-time Context 三层各自解决什么问题？为什么 "外化记忆到文件系统" 是核心组件而不是辅助工具？ → `KNOWLEDGE/agent/context-engineering/`
- [中] 为什么"动态增删工具"会破坏 KV Cache？Manus 用 logit masking 替代怎么解决这个问题？ → `KNOWLEDGE/agent/context-engineering/` + `KNOWLEDGE/transformer/kv-cache/`
- [中] "为什么不应该擦除 agent 执行过程中的失败"——失败信号在 agent 学习里扮演什么角色？ → `KNOWLEDGE/agent/context-engineering/`
- [深] Lost in the Middle 现象——agent 长任务里目标会被埋在上下文中间。为什么"重写 to-do list 到末尾"能缓解这个问题？这利用了模型的什么特性？ → `KNOWLEDGE/agent/context-engineering/` + `KNOWLEDGE/training/long-context-rl/`

## Harness Engineering

- [浅] LangChain 的 Coding Agent 在 Terminal Bench 上从 30 名外冲到前 5——他们改了什么？这件事说明什么？ → `KNOWLEDGE/agent/harness/`
- [浅] "Agent = Model + Harness" 的公式怎么解读？模型 / agent / harness 在车的比喻里分别是什么？ → `KNOWLEDGE/agent/harness/`
- [中] Harness 的 6 个关键词是什么？"上下文架构 + 架构约束 + 自验证循环 + 上下文隔离 + 长治理 + 可拆卸性"——每个解决什么具体问题？ → `KNOWLEDGE/agent/harness/`
- [中] Vercel 移除 80% 的工具反而提升性能——这和"约束架构 vs 提示约束"有什么关系？ → `KNOWLEDGE/agent/harness/`
- [中] "推理三明治"策略——为什么不是全程最高推理强度？规划/执行/验证三阶段各用什么强度？ → `KNOWLEDGE/agent/harness/`
- [深] "Harness 投入是复利"和"避免过度工程化"听起来矛盾——什么时候该投入 Harness、什么时候该等模型变强自然解决？ → `KNOWLEDGE/agent/harness/#open-questions` (open)

## Harness 实践（GAN-Inspired）

- [浅] Anthropic 的同 prompt 实验：单 agent vs Harness——核心功能能不能用 / 产品范围 / 成本各自怎样？ → `KNOWLEDGE/agent/harness-practice/`
- [浅] 三 agent 系统（规划器 / 生成器 / 评估器）借鉴了 GAN 的什么思想？ → `KNOWLEDGE/agent/harness-practice/`
- [中] 规划器为什么"故意只写高层产品设计、不写技术实现细节"？这和 multi-agent 的"上游粒度要克制"是同一原则吗？ → `KNOWLEDGE/agent/harness-practice/`
- [中] 上下文焦虑（context anxiety）是什么？为什么 Compaction 解决不了？Context Reset 怎么解决？ → `KNOWLEDGE/agent/harness-practice/`
- [中] 评估器为什么必须独立于生成器？为什么"自评"几乎一定会偏向自我表扬？ → `KNOWLEDGE/agent/harness-practice/`
- [中] 让评估器变严格的两件事——"主观维度可打分化" + "few-shot 校准"——具体怎么落地？设计质量 / 原创性的权重为什么比工艺 / 功能性高？ → `KNOWLEDGE/agent/harness-practice/`
- [中] Iteration Contract（迭代合同）解决什么问题？它在"高层规格"和"可测试实现"之间是怎么搭桥的？ → `KNOWLEDGE/agent/harness-practice/`
- [深] "Harness 中的每一个组件本质上都编码了一个假设"——这句话怎么指导 harness 的演进？Anthropic 在 Opus 4.6 之后移除了什么、保留了什么？为什么保留？ → `KNOWLEDGE/agent/harness-practice/`

## Multi-Agent: 何时用 / 不用

- [浅] Multi-agent 的代价——token 消耗是普通 agent 的几倍？这意味着判断该用与否的根本标准是什么？ → `KNOWLEDGE/agent/multi-agent/`
- [中] 三个该用的场景（上下文污染 / 并行探索 / 工具过多）各自怎么诊断？多 agent 怎么解决？ → `KNOWLEDGE/agent/multi-agent/`
- [中] 三个不该用的场景（编码任务 / 简单查询 / 拟人化角色分工）各自的反模式是什么？为什么"按角色分工"是反模式？ → `KNOWLEDGE/agent/multi-agent/`
- [中] "通过通信共享上下文，不通过共享上下文通信"——Manus 的这条原则怎么理解？调试 agent 是不是例外？ → `KNOWLEDGE/agent/multi-agent/`
- [深] "并行不是万能要"——OpenCode 在同一会话内串行执行的设计选择背后的考量是什么？什么场景下并行真的更好？ → `KNOWLEDGE/agent/multi-agent/#open-questions` (open)

## 结构化输出

- [浅] 模型为什么倾向自由文本？"加 JSON Schema 还会乱输出"的根本原因是什么？ → `KNOWLEDGE/agent/structured-output/`
- [中] 约束解码的代价是什么？为什么"格式 100% 正确不保证内容正确"？什么场景下基础模型受益、指令微调模型反而退化？ → `KNOWLEDGE/agent/structured-output/`
- [中] 验证 + 重试循环为什么是约束解码的"互补层"而不是替代品？schema 中的字段取值范围怎么落到验证器里？ → `KNOWLEDGE/agent/structured-output/`
- [中] "工具调用即结构化输出" 是什么思路？把虚拟工具的 schema 当作输出契约——这种方案的好处是什么？ → `KNOWLEDGE/agent/structured-output/`
- [中] Logit masking 替代动态工具增删——为什么不能直接增删工具？工具命名前缀（browser_、shell_）的设计和 KV Cache 怎么联动？ → `KNOWLEDGE/agent/structured-output/` + `KNOWLEDGE/transformer/kv-cache/`
- [中] Schema 字段的 description 是 "写给人看" 还是 "写给模型看"？好描述 vs 差描述的差别有多大？ → `KNOWLEDGE/agent/structured-output/`
- [深] Bitter Lesson 视角下"过度结构化的警惕"——agent 的控制机制怎么会反过来限制性能？怎么知道一个约束已经"成了瓶颈"？ → `KNOWLEDGE/agent/structured-output/#open-questions` (open)

---

## 跨节点综合

- [深] **Context Engineering、Harness Engineering、Multi-Agent、Structured Output 是 4 件不同的事吗？** 它们之间的包含关系怎么画？哪些是"补偿性工程"、哪些是"系统性工程"？ → `KNOWLEDGE/agent/agent-engineer-ability/` + `KNOWLEDGE/agent/context-engineering/` + `KNOWLEDGE/agent/harness/` + `KNOWLEDGE/agent/multi-agent/` + `KNOWLEDGE/agent/structured-output/`
- [深] **Anthropic Harness 实践案例的核心认知**：永远不让 agent 自我评估、上游规划只给方向不给路径、组件可拆卸——这三条原则在 multi-agent 系统设计里怎么体现？ → `KNOWLEDGE/agent/harness-practice/` + `KNOWLEDGE/agent/multi-agent/`
