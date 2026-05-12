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

## Context Compaction（Claude Code 实操）

- [浅] Cloud Code 的 25 万次 API 调用浪费事故是什么？三行代码修复的是什么问题？ → `KNOWLEDGE/agent/agent-context-compaction/`
- [浅] 四层压缩流水线分别是什么？为什么需要分四层而不是一层？ → `KNOWLEDGE/agent/agent-context-compaction/`
- [中] 微压缩的两条路径（Cached Micro Compact vs Time-Based）各自适用什么场景？为什么要区分？ → `KNOWLEDGE/agent/agent-context-compaction/`
- [中] 完整压缩的 `<Analysis>` 标签机制是什么？为什么 Analysis 部分会被剥离不进入最终上下文？ → `KNOWLEDGE/agent/agent-context-compaction/`
- [中] "压缩请求本身可能超长" 是怎么发生的？Cloud Code 的解法是什么？ → `KNOWLEDGE/agent/agent-context-compaction/`
- [深] "微压缩对主线程隔离、子 agent 不进全局清理状态"——这个设计避免了什么 bug？换一种实现方式可能怎么踩坑？ → `KNOWLEDGE/agent/agent-context-compaction/`

## 权限系统（Claude Code 实操）

- [浅] "确认框太多用户会无脑点 / 太少拦不住" 这个矛盾，Cloud Code 怎么破？ → `KNOWLEDGE/agent/agent-permission-system/`
- [浅] 三种规则（禁止 / 需要确认 / 允许）的优先级是什么？这和 binary 开关有什么本质区别？ → `KNOWLEDGE/agent/agent-permission-system/`
- [中] YOLO Classifier 两阶段架构是什么？为什么大部分操作能在第一阶段直接放行？ → `KNOWLEDGE/agent/agent-permission-system/`
- [中] "评审者不看 agent 的文字回复" 这个设计切断了什么攻击路径？这条原则可以推广到什么场景？ → `KNOWLEDGE/agent/agent-permission-system/`
- [深] "不可绕过的安全底线"（修改 .zshrc / git config）即使在最高信任模式也要确认——这种 "破坏触发频繁 / 副作用持久 / 检测成本高" 的操作有哪些共同特征？怎么识别？ → `KNOWLEDGE/agent/agent-permission-system/`
- [深] "Prompt 是建议，代码是法律"——这条原则的边界在哪？什么样的规则应该升级到代码、什么样的可以留在 prompt？ → `KNOWLEDGE/agent/agent-permission-system/#open-questions` (open)

## Agent 角色按阶段拆（Claude Code 实操）

- [浅] "改 bug 顺手重构 / 加功能加三层抽象" 这些病症的根源是什么？为什么不是模型问题？ → `KNOWLEDGE/agent/agent-role-isolation/`
- [中] "按功能拆（前端 / 后端 / 测试）" vs "按阶段拆（探索 / 规划 / 实现 / 验证）" 的本质区别是什么？为什么按阶段拆才能真正解决角色冲突？ → `KNOWLEDGE/agent/agent-role-isolation/`
- [中] 三维隔离（工具集 / prompt / 权限）分别管什么？为什么光 prompt 隔离不够？ → `KNOWLEDGE/agent/agent-role-isolation/`
- [中] Explore agent 用 Haiku、Verify agent 用大模型——这背后的"推理三明治"思路是什么？ → `KNOWLEDGE/agent/agent-role-isolation/` + `KNOWLEDGE/agent/harness/`
- [深] "硬约束兜底，软约束补缝" 这条原则在 Cloud Code 里具体怎么落地？哪些规则编进代码、哪些写进 prompt？判断依据是什么？ → `KNOWLEDGE/agent/agent-role-isolation/`

## 工具设计（Claude Code 实操）

- [浅] "你给 agent 接了命令行 + 文件读取 + 搜索，结果模型什么都用命令行做" 是为什么？ → `KNOWLEDGE/agent/agent-tool-design/`
- [中] "万能工具让位" 怎么落地？为什么这条规则要写在工具自己的描述里、不在 system prompt 里？ → `KNOWLEDGE/agent/agent-tool-design/`
- [中] 两级加载（核心工具 + 延迟工具）+ `tool_search` 是怎么工作的？search_hint 字段为什么单独存在、不和工具说明合并？ → `KNOWLEDGE/agent/agent-tool-design/`
- [中] 工具输出预算超限怎么处理？为什么 `read` 工具的上限是无穷大？ → `KNOWLEDGE/agent/agent-tool-design/`
- [深] "工具设计的三个原则都指向同一个核心——工具设计本质上也是上下文工程"。这三条原则各自在管上下文的什么维度？ → `KNOWLEDGE/agent/agent-tool-design/` + `KNOWLEDGE/agent/context-engineering/`

## 记忆系统（Claude Code 实操）

- [浅] "记忆是代码的补给" 这条核心哲学是什么意思？哪些信息绝对不该存进记忆？ → `KNOWLEDGE/agent/agent-memory-system/`
- [浅] 四种该存的记忆类型是什么？反馈记忆为什么必须包含 "规则 + 原因 + 适用场景" 三层？ → `KNOWLEDGE/agent/agent-memory-system/`
- [中] "只记纠正信号、不记肯定信号" 会让 agent 出什么问题？为什么肯定信号更难捕捉？ → `KNOWLEDGE/agent/agent-memory-system/`
- [中] Active Recall 的四步（扫描 / 摘要 / 选择 / 注入）各自做什么？为什么用便宜模型做选择、不用主模型？ → `KNOWLEDGE/agent/agent-memory-system/`
- [中] "选择模型宁缺勿滥" + "后效应代码兜底" 各自防止什么问题？ → `KNOWLEDGE/agent/agent-memory-system/`
- [中] 过期警告（超过两天的记忆自动加提醒）防止什么问题？背后的真实事故是什么？ → `KNOWLEDGE/agent/agent-memory-system/`
- [中] Extract Memories 后台 agent 的四个细节（权限锁死 / 两轮策略 / 互斥 / 游标）各自防什么？ → `KNOWLEDGE/agent/agent-memory-system/`
- [深] "自动化 ≠ 不受控"——后台自动 agent 任务怎么同时做到自动化和可控？这条原则可以推广到哪些其他场景？ → `KNOWLEDGE/agent/agent-memory-system/`
- [深] Active Recall 是两阶段检索（粗筛 + 精选），它和传统 RAG（向量搜索）的根本区别是什么？什么场景下两阶段检索胜过向量？ → `KNOWLEDGE/agent/agent-memory-system/`

## System Prompt 设计（Claude Code 实操）

- [浅] Cloud Code 的 system prompt 有 900 多行——它的"模块化 + 静态/动态分离"结构是什么样的？ → `KNOWLEDGE/agent/agent-system-prompt/`
- [中] "静态段在前 / 动态段在后" 这个安排和 KV Cache 是什么关系？为什么不能把动态内容放在前面？ → `KNOWLEDGE/agent/agent-system-prompt/` + `KNOWLEDGE/transformer/kv-cache/`
- [中] "请写好代码" vs "不要给你没改的代码加注释"——为什么具体规则比抽象原则更有效？ → `KNOWLEDGE/agent/agent-system-prompt/`
- [中] 行动风险评估框架的两个维度（可逆性 × 影响范围）怎么用？"教模型怎么处理意外状态" 这条设计的价值在哪？ → `KNOWLEDGE/agent/agent-system-prompt/`
- [中] "防说谎"为什么必须同时也"防过度谨慎"？只防一个方向会出什么问题？ → `KNOWLEDGE/agent/agent-system-prompt/`
- [深] "30% 虚假声明率" 这个数字暗示了什么？模型默认的"讨好用户"倾向在哪些场景下危险？ → `KNOWLEDGE/agent/agent-system-prompt/#open-questions` (open)

## OpsAgent vs AgentOps（两个方向的本质区分）

- [浅] OpsAgent / AgenticOps 和 AgentOps 是什么？区分这两者解决什么问题？ → `KNOWLEDGE/agent/agentops-vs-opsagent/`
- [浅] AgentOps 跟传统 AIOps 的四维差异是什么（监控数据 / 数据可靠性 / 故障类别 / 修复方式）？ → `KNOWLEDGE/agent/agentops-vs-opsagent/`
- [中] 报告用 BGP 反例论证 AgentOps 必须原生纳入——这个反例的核心力量是什么？类比到 agent 系统怎么用？ → `KNOWLEDGE/agent/agentops-vs-opsagent/`
- [中] Trustworthy Level Agreement (TLA) 是什么？它和传统 guardrail 的区别在哪？ → `KNOWLEDGE/agent/agentops-vs-opsagent/`
- [深] "Agent 搭建爽，Debug 火葬场"——这条痛点跟 OpsAgent 项目工程师亲身碰到的"端到端联调上不去"是什么关系？为什么说"碰到了痛点不等于解决了"？ → `KNOWLEDGE/agent/agentops-vs-opsagent/` + `KNOWLEDGE/agent/agent-failure-attribution/`

## 多智能体根因分析范式（工业实现三件套）

- [浅] 多智能体 RCA 系统的三件套是什么？三件套之间怎么互相约束、形成因果链？ → `KNOWLEDGE/agent/multi-agent-rca-paradigm/`
- [浅] 按职责拆 agent 的五个角色是什么？为什么"分析决策 agent 不主动获取数据"是关键约束？ → `KNOWLEDGE/agent/multi-agent-rca-paradigm/`
- [中] Result Fusion / Model Fusion / Feature Fusion 三种多模态融合范式的本质差异？为什么工业偏 Result Fusion？什么场景下 Model Fusion 上限更高？ → `KNOWLEDGE/agent/multi-agent-rca-paradigm/`
- [中] SOP 嵌入的三个层级是什么（规划 agent / 数据 agent / 决策 agent）？纯 ReAct 不嵌 SOP 的三种失败模式？ → `KNOWLEDGE/agent/multi-agent-rca-paradigm/`
- [中] ReAct 性能优化的四件事（减循环 / 上下文压缩 / 智能终止 / 显式总结）——这些是工程层优化而不是模型层优化，为什么这样选？ → `KNOWLEDGE/agent/multi-agent-rca-paradigm/`
- [深] 多 agent 拆分有三种轴：按职责拆（七牛云 / Flow-of-Action）/ 按阶段拆（Cloud Code）/ 按数据源拆（demo.md L2 内部）——这三种轴的适用场景区别是什么？怎么选？ → `KNOWLEDGE/agent/multi-agent-rca-paradigm/` + `KNOWLEDGE/agent/agent-role-isolation/` + `KNOWLEDGE/agent/multi-agent/`

## Agent Failure Attribution（AgentOps 的核心问题）

- [浅] "Which agent causes task failures and when?"——Failure Attribution 的本质问题是什么？为什么传统 stack trace 不够用？ → `KNOWLEDGE/agent/agent-failure-attribution/`
- [浅] 76.6% 的 agent 失败是 wrong_answer——这个数字说明什么？跟传统系统的 crash 失败有什么本质不同？ → `KNOWLEDGE/agent/agent-failure-attribution/`
- [中] Who&When / FAMAS / Echo / Correct 四种方法各自的本质思路（论证基础 / 频谱分析 / LLM-as-Judge / Retrieval-based）和适用场景？为什么"没有银弹"？ → `KNOWLEDGE/agent/agent-failure-attribution/`
- [中] Who&When 数据集的两个局限（轨迹太短 71% 只有 5-10 步 + 失败位置偏早 48% 在前 1/3）怎么导致简单启发式也能拿高分？ → `KNOWLEDGE/agent/agent-failure-attribution/`
- [中] Group-wise VAE 从 AIOps trace 异常检测迁移到 agent trajectory——迁移的对应关系是什么（Service ↔ Agent / Latency ↔ token/time/cost）？为什么加 VAE 既提准确率又降成本？ → `KNOWLEDGE/agent/agent-failure-attribution/`
- [深] Agent trajectory 的"合理多样性 vs 真实异常"边界怎么划？同一任务两次跑选不同工具——是合理还是异常？这条边界的判断准则可能跟什么有关？ → `KNOWLEDGE/agent/agent-failure-attribution/#open-questions` (open)

## 结构化输出

- [浅] 模型为什么倾向自由文本？"加 JSON Schema 还会乱输出"的根本原因是什么？ → `KNOWLEDGE/agent/structured-output/`
- [中] 约束解码的代价是什么？为什么"格式 100% 正确不保证内容正确"？什么场景下基础模型受益、指令微调模型反而退化？ → `KNOWLEDGE/agent/structured-output/`
- [中] 验证 + 重试循环为什么是约束解码的"互补层"而不是替代品？schema 中的字段取值范围怎么落到验证器里？ → `KNOWLEDGE/agent/structured-output/`
- [中] "工具调用即结构化输出" 是什么思路？把虚拟工具的 schema 当作输出契约——这种方案的好处是什么？ → `KNOWLEDGE/agent/structured-output/`
- [中] Logit masking 替代动态工具增删——为什么不能直接增删工具？工具命名前缀（browser_、shell_）的设计和 KV Cache 怎么联动？ → `KNOWLEDGE/agent/structured-output/` + `KNOWLEDGE/transformer/kv-cache/`
- [中] Schema 字段的 description 是 "写给人看" 还是 "写给模型看"？好描述 vs 差描述的差别有多大？ → `KNOWLEDGE/agent/structured-output/`
- [深] Bitter Lesson 视角下"过度结构化的警惕"——agent 的控制机制怎么会反过来限制性能？怎么知道一个约束已经"成了瓶颈"？ → `KNOWLEDGE/agent/structured-output/#open-questions` (open)

## Agent Anomaly Taxonomy（11 类异常）

- [浅] AgentOps 报告里"异常"的定义跟传统系统挂掉有什么不同？为什么要扩展到 pre-execution / post-execution？ → `KNOWLEDGE/agent/agent-anomaly-taxonomy/`
- [浅] Intra-Agent 5 类 + Inter-Agent 6 类，分别对应 agent 系统的哪些组件 / 层面？ → `KNOWLEDGE/agent/agent-anomaly-taxonomy/`
- [中] 为什么 "wrong_answer" 单一标签不够用？11 类拆分对 attribution / detection / recovery 三个下游各带来什么不同？ → `KNOWLEDGE/agent/agent-anomaly-taxonomy/`
- [中] Termination Anomaly 同时包含 Unstoppable Task 和 Premature Stop 两种相反方向——这两类共同的"异常本质"是什么？ → `KNOWLEDGE/agent/agent-anomaly-taxonomy/`
- [中] Emergent Behavioral Anomalies 为什么"无法在单 agent 层面检测"？这给 multi-agent 系统监控提了什么具体要求？ → `KNOWLEDGE/agent/agent-anomaly-taxonomy/`
- [深] 11 类边界在工程实操中是否真的清晰？一个失败同时触发 Reasoning + Termination 该归哪类？为什么多标签可能比单标签更合适？ → `KNOWLEDGE/agent/agent-anomaly-taxonomy/#open-questions` (open)

## Agent Failure Trajectory Dataset（评测基础设施）

- [浅] Who&When 的两个结构性局限是什么？为什么"71% 任务 5-10 步 + 48% 失败偏早"会让简单启发式占便宜？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [浅] 6 个 benchmark（SWE-Bench Pro / Terminal-Bench / WebArena-Verified / OSWorld-Verified / VitaBench / TravelPlanner Bench）的共同特征是什么？为什么是这 6 个而不是其他？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [中] 失败类型分布 wrong_answer 76.6% / budget_exhausted 20.2% / agent_gave_up 2.3% / tool_call_loop 1.0%——这个分布**暗示了 agent 失败的根本形态**是什么？为什么传统 "loop 检测" 解决不了 99% 的失败？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [中] Schema 的核心三件套（mistake_agent / mistake_step / mistake_reason）分别提供什么监督信号？为什么 `system_prompt` 必须保留？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [中] history 用 OpenAI message 格式 `{role, name, content}` 而不是自定义 schema——为什么这是个工程上的正确选择？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [中] LLM 预标注（DeepSeek v4 Pro 首轮 50 条）+ 人工复核——为什么 LLM 预标注**不能作为 ground truth**？预标注的价值在哪？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [深] 1570 样本 × 11 类 Taxonomy = 平均每类 140 样本——这个规模够用吗？什么样的 attribution 方法会过拟合到这个规模？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/#open-questions` (open)

---

## 跨节点综合

- [深] **Context Engineering、Harness Engineering、Multi-Agent、Structured Output 是 4 件不同的事吗？** 它们之间的包含关系怎么画？哪些是"补偿性工程"、哪些是"系统性工程"？ → `KNOWLEDGE/agent/agent-engineer-ability/` + `KNOWLEDGE/agent/context-engineering/` + `KNOWLEDGE/agent/harness/` + `KNOWLEDGE/agent/multi-agent/` + `KNOWLEDGE/agent/structured-output/`
- [深] **Anthropic Harness 实践案例的核心认知**：永远不让 agent 自我评估、上游规划只给方向不给路径、组件可拆卸——这三条原则在 multi-agent 系统设计里怎么体现？ → `KNOWLEDGE/agent/harness-practice/` + `KNOWLEDGE/agent/multi-agent/`
- [深] **Cloud Code 全栈拆解串成一条线**：四层压缩 / YOLO 分类器 / 6 agent 按阶段拆 / 工具三原则 / 记忆四存五不存 / 系统提示词模块化——这 6 个子系统都在解决"在概率性的模型周围，构建确定性的工程系统"。每个子系统**编码了什么假设、用什么硬约束兜底、什么软约束补缝**？ → `KNOWLEDGE/agent/agent-context-compaction/` + `KNOWLEDGE/agent/agent-permission-system/` + `KNOWLEDGE/agent/agent-role-isolation/` + `KNOWLEDGE/agent/agent-tool-design/` + `KNOWLEDGE/agent/agent-memory-system/` + `KNOWLEDGE/agent/agent-system-prompt/` + `KNOWLEDGE/agent/harness/`
- [深] **Cloud Code 的整体设计哲学**："不信任模型的自觉性，能用硬约束的地方绝不用软约束"——但有些行为（不加冗余功能、克制抽象）没法编进代码、只能写进 prompt。**硬约束 vs 软约束的边界在哪、判断准则是什么**？这条原则会随着模型变强而演化吗？ → `KNOWLEDGE/agent/agent-role-isolation/` + `KNOWLEDGE/agent/agent-permission-system/` + `KNOWLEDGE/agent/harness/`
- [深] **OpsAgent / AgentOps / Multi-Agent RCA / Failure Attribution 串成一条研究线**：工程师做 OpsAgent 时遇到的痛点"Agent 模块单独跑通但端到端联调上不去"，本质上就是缺 AgentOps 的 Failure Attribution 能力。**这条迁移路径（OpsAgent → AgentOps）跟"研究方向定位"的关系是什么**？怎么用这条迁移路径回答"你未来想做什么"？ → `KNOWLEDGE/agent/agentops-vs-opsagent/` + `KNOWLEDGE/agent/multi-agent-rca-paradigm/` + `KNOWLEDGE/agent/agent-failure-attribution/`
