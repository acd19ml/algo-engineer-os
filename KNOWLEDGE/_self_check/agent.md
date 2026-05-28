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

## 模型边界探测

- [浅] 为什么 benchmark 分数不能替代 agent 场景里的模型边界图？真实边界至少包含哪四个维度？ → `KNOWLEDGE/agent/model-boundary-probing/`
- [中] 模型上下文更长、推理更快后，为什么 agent 反而更容易暴露长程失控问题？举上下文漂移、缺乏自验证、死循环三个例子。 → `KNOWLEDGE/agent/model-boundary-probing/` + `KNOWLEDGE/agent/context-engineering/`
- [中] SpecLock、辩论机制、熔断器、Skill 提炼、压缩前写记忆分别在补哪类长程失败边界？ → `KNOWLEDGE/agent/model-boundary-probing/` + `KNOWLEDGE/agent/harness/`
- [深] "模型会换，边界会变，但画边界地图的能力不会过时"——这句话和"补偿性工程 vs 系统性工程"是什么关系？ → `KNOWLEDGE/agent/model-boundary-probing/` + `KNOWLEDGE/agent/agent-engineer-ability/`

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

## Agent 评估 Harness

- [浅] 为什么复杂 agent 不能只看最终输出评估？执行轨迹里有哪些最终答案看不到的失败信号？ → `KNOWLEDGE/agent/agent-evaluation-harness/`
- [中] 直接让编码助手"帮我评估这个 agent"会出现哪三类失败？为什么这些失败本质上是缺领域评估知识？ → `KNOWLEDGE/agent/agent-evaluation-harness/`
- [中] 过程性指令、评估模板、实时 API 文档检索三类技能分别解决什么问题？为什么实时文档能显著提高代码跑通率？ → `KNOWLEDGE/agent/agent-evaluation-harness/`
- [深] "规划本身不是价值，有约束的规划才是价值"——这句话在 agent 评估代码生成里怎么体现？ → `KNOWLEDGE/agent/agent-evaluation-harness/` + `KNOWLEDGE/agent/harness/`

## 工具调用修复 Harness

- [浅] 当开源模型工具调用失败时，为什么要先问"它不会推理，还是没记住 schema 格式"？ → `KNOWLEDGE/agent/tool-call-repair-harness/`
- [中] 四类常见工具输入形状错误是什么？为什么这些错误说明 Harness 可以在格式边界上补偿模型？ → `KNOWLEDGE/agent/tool-call-repair-harness/`
- [中] 为什么工具输入修复必须"先校验再修复"，不能先预处理？写文件内容被静默篡改的反例说明什么？ → `KNOWLEDGE/agent/tool-call-repair-harness/`
- [中] Markdown 链接泄露到文件路径这个例子，为什么不是普通幻觉，而是聊天分布污染工具边界？schema 类型该怎么改？ → `KNOWLEDGE/agent/tool-call-repair-harness/` + `KNOWLEDGE/agent/structured-output/`
- [深] "能修复的修复，不能修复的扩展语义"——字段关系不变量（offset / limit）为什么不能靠单字段修复？ → `KNOWLEDGE/agent/tool-call-repair-harness/`

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

## CLAUDE.md 规则设计（用户侧行为合约）

- [浅] CLAUDE.md 三种常见状态（什么都塞 / 完全跳过 / 复制模板就忘）各自的 token 浪费 / 遵循率坑是什么？为什么 200 行是个真实天花板？ → `KNOWLEDGE/agent/claude-md-rule-design/`
- [浅] Karpathy 原版 4 条（先想后写 / 简单至上 / 外科手术式修改 / 目标驱动）各自防什么具体错误？为什么这 4 条只能覆盖 ~40% 失败模式？ → `KNOWLEDGE/agent/claude-md-rule-design/`
- [中] 12 条 vs 4 条 vs 18 条的实测数据——合规率从 78%→76%→52% 但错误率 11%→3%→回升。**新规则的边际价值取决于什么**？什么叫"新规则不在争夺同一份注意力预算，而是形成互补增强"？ → `KNOWLEDGE/agent/claude-md-rule-design/`
- [中] Karpathy 原版的 4 个 limitation（长任务 / 多代码库 / 测试质量 / 生产 vs 原型）各自缺什么？新增 8 条分别补哪个 limitation？ → `KNOWLEDGE/agent/claude-md-rule-design/`
- [中] 规则 5 "模型只做判断不做决策"——为什么调用 Claude 去判断 "503 该不该重试" 的代码会**稳定运行两周后开始漂移**？这跟"确定性逻辑 vs 裁量逻辑"的分工原则有什么关系？ → `KNOWLEDGE/agent/claude-md-rule-design/`
- [中] 规则 9 "测试验证意图而非仅验证行为"——`expect(getUserName()).toBe('John')` 测试为什么形同虚设？写"业务逻辑变更时会失败"的测试的标准是什么？ → `KNOWLEDGE/agent/claude-md-rule-design/`
- [中] 规则 12 "显式失败"——为什么"看起来像成功的失败是最贵的失败"？数据库迁移**悄悄跳过 14% 因约束冲突的记录**为什么 11 天后才被发现？默认原则"主动暴露不确定性"在 CLAUDE.md 里怎么写？ → `KNOWLEDGE/agent/claude-md-rule-design/`
- [深] **试过但放弃的 6 条路径**（Reddit 看来的规则 / 超过 12 条 / 依赖不一定存在的工具 / 在 CLAUDE.md 里放例子 / "小心"类软语言 / 让 Claude "做高级工程师"）——**这 6 条反事实证据各自暴露了 prompt 设计的什么深层错误**？为什么"例子比规则重"是反直觉？ → `KNOWLEDGE/agent/claude-md-rule-design/`
- [深] **两条心智模型**：(1) "CLAUDE.md 是行为合约不是许愿清单"——每条规则必须能回答"预防的是什么错误"；(2) "6 条针对真踩过的坑 > 12 条里有 6 条用不上"。**这两条原则跟 agent-system-prompt 节点的"具体规则 > 抽象原则"是同一回事吗**？用户侧 CLAUDE.md vs Claude Code 内部 system prompt 两层是怎么交互的？ → `KNOWLEDGE/agent/claude-md-rule-design/#open-questions` (open) + `KNOWLEDGE/agent/agent-system-prompt/`

## System Prompt 设计（Claude Code 实操）

- [浅] Cloud Code 的 system prompt 有 900 多行——它的"模块化 + 静态/动态分离"结构是什么样的？ → `KNOWLEDGE/agent/agent-system-prompt/`
- [中] "静态段在前 / 动态段在后" 这个安排和 KV Cache 是什么关系？为什么不能把动态内容放在前面？ → `KNOWLEDGE/agent/agent-system-prompt/` + `KNOWLEDGE/transformer/kv-cache/`
- [中] "请写好代码" vs "不要给你没改的代码加注释"——为什么具体规则比抽象原则更有效？ → `KNOWLEDGE/agent/agent-system-prompt/`
- [中] 行动风险评估框架的两个维度（可逆性 × 影响范围）怎么用？"教模型怎么处理意外状态" 这条设计的价值在哪？ → `KNOWLEDGE/agent/agent-system-prompt/`
- [中] "防说谎"为什么必须同时也"防过度谨慎"？只防一个方向会出什么问题？ → `KNOWLEDGE/agent/agent-system-prompt/`
- [深] "30% 虚假声明率" 这个数字暗示了什么？模型默认的"讨好用户"倾向在哪些场景下危险？ → `KNOWLEDGE/agent/agent-system-prompt/#open-questions` (open)

## RAG / Agentic RAG

- [浅] 面试官问"长上下文会不会淘汰 RAG"时，为什么要先区分"能不能放进去"和"该不该放进去"？ → `KNOWLEDGE/agent/agentic-rag-vs-long-context/`
- [中] 传统 RAG、长上下文、Agentic RAG 三者分别适合什么问题形态？为什么 Agentic RAG 里长上下文反而变成工作空间？ → `KNOWLEDGE/agent/agentic-rag-vs-long-context/` + `KNOWLEDGE/training/long-context-rl/`
- [中] RAG 回答不准时，为什么排查顺序应该是数据源 → chunking → query 理解 → embedding → 排序？每一层分别怎么诊断？ → `KNOWLEDGE/agent/rag-failure-diagnosis/`
- [中] Query rewrite 为什么可能让召回率下降？"怎么开白名单"被改成"访问许可列表"这个例子暴露了什么问题？ → `KNOWLEDGE/agent/rag-query-rewriting/`
- [中] Query rewrite 的五类通用策略（基础改写 / multi-query / subquery / step-back / HyDE）分别解决什么检索问题？为什么必须先分类再改写？ → `KNOWLEDGE/agent/rag-query-rewriting/`
- [中] Agentic RAG 延迟高时，为什么 planning cache 比简单限制迭代次数更接近根因优化？它缓存的到底是什么？ → `KNOWLEDGE/agent/agentic-rag-planning-cache/`
- [深] Planning cache、procedural memory、skills 三者都在复用过去成功经验：它们的边界在哪里？什么时候模板缓存应该升级成显式 skill？ → `KNOWLEDGE/agent/agentic-rag-planning-cache/#open-questions` (open) + `KNOWLEDGE/agent/agent-skills-closed-loop/`

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

## Memory 架构理论框架（Ledger + Views + Policy 三件套）

- [浅] Memory 为什么不是"存储"？"能力来自历史能不能在当前状态下影响决策分布"这句话的反直觉在哪？ → `KNOWLEDGE/agent/memory-architecture-thesis/`
- [浅] (Ledger, Views, Policy) 三件套各自负责什么？三者缺一各自会出现什么具体问题？ → `KNOWLEDGE/agent/memory-architecture-thesis/`
- [中] 一个完整的 ledger event 至少包含哪几个要素？event 序列为什么"是真相来源但不可直接用"？views 和 policy 在中间做什么转换？ → `KNOWLEDGE/agent/memory-architecture-thesis/`
- [中] 为什么需要 System 2 而不是把 memory 能力 RL 训进 System 1 权重？"memory 能力和 LLM 其他 agent 能力相对正交"是什么意思？非正交边界在哪？ → `KNOWLEDGE/agent/memory-architecture-thesis/`
- [中] JitRL 的修正项 `Δ = α · A_est(s, a, M)` 怎么逼近 fine-tune 效果？参数化 vs 非参数化"写入成本"分摊在哪不一样？ → `KNOWLEDGE/agent/memory-architecture-thesis/`
- [中] 三类上限瓶颈（接口带宽 / views 近似误差 / policy 可学习性）各自对应什么可观测指标？怎么用这三类指标定位"当前系统效果差在哪里"？ → `KNOWLEDGE/agent/memory-architecture-thesis/`
- [中] Memory 操作的 6 个工具化动作（LTM: ADD/UPDATE/DELETE + STM: RETRIEVE/SUMMARY/FILTER）分别对应参数化训练里的什么行为？为什么必须 RL 训练而不能 rubrics based？ → `KNOWLEDGE/agent/memory-architecture-thesis/`
- [中] bi-temporal 把 `transaction_time ≠ valid_time` 拆开——为什么 UPDATE/DELETE 的语义不应该是"改旧记录"而是"追加更正事件"？这对"遗忘"的实现有什么启发？ → `KNOWLEDGE/agent/memory-architecture-thesis/`
- [深] TKG 给边加 temporal validity `[t_start, t_end]`——这跟纯语义检索的根本区别是什么？为什么 Zep 在长时序记忆评测能比传统 RAG 提升 18.5%？MAGMA 的 ablation（0.700 → 0.647）证明了什么？ → `KNOWLEDGE/agent/memory-architecture-thesis/`
- [深] 非参数化 Memory 想逼近参数化上限——核心**不是**"塞更多东西进库"，而是什么？为什么 policy 是真正的瓶颈而不是存储后端？ → `KNOWLEDGE/agent/memory-architecture-thesis/#open-questions` (open)

## Heuristic Learning（coding agent 改变维护曲线）

- [浅] HL 和 Deep RL 在 6 个维度（Policy / State / Action / Feedback / Update / Memory）上的差异？最反直觉的一个差异是什么？ → `KNOWLEDGE/agent/heuristic-learning/`
- [浅] Atari Breakout 上从 387 到 864 的提升用什么策略？这个策略包含什么 if-else 之外的内容？ → `KNOWLEDGE/agent/heuristic-learning/`
- [中] 为什么 1980 年代 expert system 失败而 HL 现在可能成立？变化的不是规则本身，变的是什么？纺纱机的类比怎么用？ → `KNOWLEDGE/agent/heuristic-learning/`
- [中] HS（Heuristic System）和单一 `policy.py` 的区别是什么？哪 7 个组成部分都齐才算 HS？ → `KNOWLEDGE/agent/heuristic-learning/`
- [中] HL 怎么处理 Continual Learning？"避免遗忘"怎么转化为"维护一个持续吸收反馈的软件系统"？老能力可以固化为哪 6 类对象？ → `KNOWLEDGE/agent/heuristic-learning/`
- [中] Coupling complexity **不能用代码行数衡量**——什么决定了它的上限？为什么 500 行干净策略可能比 80 行难维护的策略好维护？ → `KNOWLEDGE/agent/heuristic-learning/`
- [中] "只增不压的 HS 最终会变成大泥球"——为什么单调增长就是负资产？健康 HS 必须有的两种操作是什么？ → `KNOWLEDGE/agent/heuristic-learning/`
- [深] Montezuma 在 Atari57 拿 400 分但路径是 86 个 macro-action 的开环执行——这个反例对 HL 的边界给出什么提示？什么样的环境需要"超越纯 `if-else`"的程序形态？ → `KNOWLEDGE/agent/heuristic-learning/`
- [深] 在 Robotics System 1 / System 2 分层里 HL 的定位是什么？joint-level → limb-level → whole-body balance → task-level 分层的逻辑是什么？coding agent 不"懂走路"为什么不影响它当 update pipeline？ → `KNOWLEDGE/agent/heuristic-learning/`
- [深] HL 产物（rules + tests + replays + memory）是不是一种 procedural memory？跟 AWM workflow / Hermes Skill 在 "procedural memory object shape" 这条轴上怎么定位？ → `KNOWLEDGE/agent/heuristic-learning/#open-questions` (open)

## Hermes Skills 闭环（procedural memory 的工程闭环）

- [浅] Hermes Skills 7 步闭环的核心环节是什么？这个闭环跟 LangChain / AutoGen / CrewAI / Claude Code / OpenAI Codex CLI 的关键区别在哪？ → `KNOWLEDGE/agent/agent-skills-closed-loop/`
- [浅] Skill 创建触发条件 `SKILLS_GUIDANCE` 里 "5+ tool calls / fixing a tricky error / don't wait to be asked" 分别在 hint 什么设计判断？"过时 Skill 比没 Skill 更危险"反直觉在哪？ → `KNOWLEDGE/agent/agent-skills-closed-loop/`
- [中] 七道安全关卡的"先写入再扫描"反直觉——为什么**不**"先扫描后写入"？TOCTOU 竞态条件是什么？原子写入 `tempfile + os.replace` 在 AI Agent 工具里罕见，反应了什么工程成熟度？ → `KNOWLEDGE/agent/agent-skills-closed-loop/`
- [中] 两层缓存（L1 进程内 LRU + L2 磁盘快照）的 `cache_key` 五元组为什么必须包含 `available_tools` 和 `platform_hint`？同一个 Skill 在不同配置下显示 / 隐藏靠什么机制？ → `KNOWLEDGE/agent/agent-skills-closed-loop/`
- [中] System Prompt 的 "you MUST load it" 强制措辞背后是什么取舍？"漏加载相关 Skill 的成本 vs 多加载不相关 Skill 的成本" 哪个更大？ → `KNOWLEDGE/agent/agent-skills-closed-loop/`
- [中] 条件激活 4 字段（`fallback_for_toolsets / requires_toolsets / fallback_for_tools / requires_tools`）解决什么问题？`manual-web-search` 在 web toolset 可用时隐藏的例子说明什么设计原则？ → `KNOWLEDGE/agent/agent-skills-closed-loop/`
- [中] 渐进式加载 Tier 0-3 同时解决哪两个矛盾？"Agent 知道有哪些 Skill 可用" + "Skill 内容不占满 context" 分别落在哪一层？ → `KNOWLEDGE/agent/agent-skills-closed-loop/`
- [深] Hermes Skill（Agent 显式 create）vs AWM workflow（task completion 反推）vs Claude Code Skills.md（人写）—— procedural memory 三种 design point 哪个更可持续？这条轴跟 memory-architecture-thesis 三件套怎么连接？ → `KNOWLEDGE/agent/agent-skills-closed-loop/#open-questions` (open)

## Memory 级联更新问题（MeMe 论文 + research direction）

- [浅] "我搬家了" 之后，"健身房在望京"这条记忆应该怎么办？三层更新难度（直接替换 / 级联失效 / 反事实推理）分别是什么？ → `KNOWLEDGE/agent/agent-memory-cascading-update/`
- [浅] MeMe 论文的两个关键数字——级联更新 3% / 反事实推理 1%——意味着什么？为什么"不是某个系统差，是所有系统都差"？ → `KNOWLEDGE/agent/agent-memory-cascading-update/`
- [中] 当前记忆系统为什么做不到级联更新？跟传统数据库的"外键约束 + 级联删除"类比一下——根源差在哪？ → `KNOWLEDGE/agent/agent-memory-cascading-update/`
- [中] 四个候选方向（写入时触发分析 / 显式依赖图 / 置信度衰减 + 主动确认 / 全量上下文）各自为什么不够？四者指向的同一根本矛盾是什么？ → `KNOWLEDGE/agent/agent-memory-cascading-update/`
- [中] 唯一"部分有效"的方案是"全量上下文（70× 成本）"——它证明了什么关于模型推理能力 vs 记忆架构能力的判断？ → `KNOWLEDGE/agent/agent-memory-cascading-update/`
- [中] "写入时粗筛 + 读取时精确验证 + 后台批量扫描" 两阶段方案的成本摊销逻辑是什么？为什么"没有任何开源/商业产品完整实现"是个重要信号？ → `KNOWLEDGE/agent/agent-memory-cascading-update/`
- [深] **级联更新失败可以归到 `memory-architecture-thesis` 三类瓶颈框架里的哪一类？** policy 可学习性 vs views 近似误差 vs 接口带宽——为什么是 policy？这跟用 GRPO 训 memory tool 的数据分布有什么关系？ → `KNOWLEDGE/agent/agent-memory-cascading-update/` + `KNOWLEDGE/agent/memory-architecture-thesis/`
- [深] **"事实被否定" vs "事实变成历史" 的区分**本质是什么？跟 `memory-architecture-thesis` 里 `transaction_time ≠ valid_time` 的 bi-temporal 设计是同一回事吗？如果显式 ledger 记录 valid_time 区间，第 3 层反事实推理能从 1% 提升到多少？ → `KNOWLEDGE/agent/agent-memory-cascading-update/#open-questions` (open)
- [深] **对做 agent 产品的人**："不能假设记忆系统会自动处理依赖关系"——什么场景必须在产品层面设计降级策略（搬家 / 换工作 / 换城市 / 换伴侣）？怎么设计？这跟"AI 记错了"的用户体感和系统责任怎么划分？ → `KNOWLEDGE/agent/agent-memory-cascading-update/`

## Agent Failure Trajectory Dataset（评测基础设施）

- [浅] Who&When 的两个结构性局限是什么？为什么"71% 任务 5-10 步 + 48% 失败偏早"会让简单启发式占便宜？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [浅] 6 个 benchmark（SWE-Bench Pro / Terminal-Bench / WebArena-Verified / OSWorld-Verified / VitaBench / TravelPlanner Bench）的共同特征是什么？为什么是这 6 个而不是其他？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [中] 失败类型分布 wrong_answer 76.6% / budget_exhausted 20.2% / agent_gave_up 2.3% / tool_call_loop 1.0%——这个分布**暗示了 agent 失败的根本形态**是什么？为什么传统 "loop 检测" 解决不了 99% 的失败？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [中] Schema 的核心三件套（mistake_agent / mistake_step / mistake_reason）分别提供什么监督信号？为什么 `system_prompt` 必须保留？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [中] history 用 OpenAI message 格式 `{role, name, content}` 而不是自定义 schema——为什么这是个工程上的正确选择？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [中] LLM 预标注（DeepSeek v4 Pro 首轮 50 条）+ 人工复核——为什么 LLM 预标注**不能作为 ground truth**？预标注的价值在哪？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/`
- [深] 1570 样本 × 11 类 Taxonomy = 平均每类 140 样本——这个规模够用吗？什么样的 attribution 方法会过拟合到这个规模？ → `KNOWLEDGE/agent/agent-failure-trajectory-dataset/#open-questions` (open)

## 小模型 Harness 工程（Forge 案例）

- [浅] 单步准确率 90% 的模型，跑 5 步工作流通过率是多少？跑 10 步呢？为什么这叫"复合概率问题"而不是"模型能力问题"？ → `KNOWLEDGE/agent/small-model-harness-engineering/`
- [浅] Forge 的合成 `respond` 工具解决什么问题？不加它，工作流完成率从 100% 降到多少？ → `KNOWLEDGE/agent/small-model-harness-engineering/`
- [中] 五层防护各自针对什么失败模式？哪一层不是在修格式错误，而是在管"工具调用顺序"？ → `KNOWLEDGE/agent/small-model-harness-engineering/`
- [中] Hard Error vs ToolResolutionError（HTTP 404 类比）——为什么必须区分？混淆两类会出什么问题？ → `KNOWLEDGE/agent/small-model-harness-engineering/`
- [中] Step Enforcer 的升级式纠正消息（礼貌 → 直接 → 强硬）——这个设计在干什么？ → `KNOWLEDGE/agent/small-model-harness-engineering/`
- [中] Tiered Compact 第二阶段删除工具返回结果但保留推理过程——为什么推理比原始数据更不能丢？第三阶段又删掉推理——两次决定的逻辑分别是什么？ → `KNOWLEDGE/agent/small-model-harness-engineering/`
- [中] 同一套模型权重，llama.cpp 原生函数调用 7% vs llama-file 提示注入 83%——这对"这个模型工具调用不行"的结论有什么影响？ → `KNOWLEDGE/agent/small-model-harness-engineering/`
- [深] 消融实验五层缺一不可——这说明复合概率问题里每类失败模式的独立性有多强？能否用"优先修哪一层成本效益最高"的思路来部分部署 Harness？ → `KNOWLEDGE/agent/small-model-harness-engineering/#open-questions` (open)

## 缓存感知 Agent 循环（DeepSeek ReasonX 案例）

- [浅] DeepSeek 缓存命中价格是 miss 的几分之一？把命中率从 30% 提到 99% 能降多少成本？ → `KNOWLEDGE/agent/cache-aware-agent-loop/`
- [浅] 大多数 Agent 框架缓存命中率只有 2–30%——三个主要原因是什么？ → `KNOWLEDGE/agent/cache-aware-agent-loop/`
- [中] 三区域设计（Immutable Prefix / Append-only Log / Volatile Scratch）各自的不变性约束是什么？哪个区域的内容不发送给 API？为什么？ → `KNOWLEDGE/agent/cache-aware-agent-loop/`
- [中] 为什么 Append-only Log 加上"永不回滚"的策略能保证缓存永远命中？如果第 3 轮消息被修改，会发生什么？ → `KNOWLEDGE/agent/cache-aware-agent-loop/`
- [中] Cache Line Fold 和普通压缩（删旧消息/替换旧消息）的根本区别是什么？摘要调用本身为什么也能命中缓存？ → `KNOWLEDGE/agent/cache-aware-agent-loop/`
- [中] Storm 模块的滑动窗口里，写操作为什么要清空读操作记录？不做这个设计，哪种正常工作流会被错误拦截？ → `KNOWLEDGE/agent/cache-aware-agent-loop/`
- [中] Flash-first + Need Pro 自升级——为什么是"模型自己决定"而不是"错误次数超阈值就切换"？ → `KNOWLEDGE/agent/cache-aware-agent-loop/`
- [深] "缓存策略应该是架构约束，不是事后优化"——如果在已有 Agent 框架上事后改造缓存，会遇到哪些结构性阻力？ → `KNOWLEDGE/agent/cache-aware-agent-loop/#open-questions` (open)

## 层级 Agent 记忆（OpenViking 案例）

- [浅] 平面记忆系统（Cloud Code Active Recall 范式）的五个痛点是什么？哪个痛点是 Cloud Code 的设计里根本没有的能力？ → `KNOWLEDGE/agent/hierarchical-agent-memory/`
- [浅] 三层力度（L0/L1/L2）各自大约多少 token？各自在决策链里的作用是什么？ → `KNOWLEDGE/agent/hierarchical-agent-memory/`
- [中] 层级递归检索的四步（全局搜索 → 子节点搜索 → 分数传播 → 收敛检测）里，"分数传播"解决了平面向量搜索的哪个缺陷？ → `KNOWLEDGE/agent/hierarchical-agent-memory/`
- [中] `agent/` 目录的四类（cases / patterns / tools / skills）和 Cloud Code 的四类记忆有什么本质区别？ → `KNOWLEDGE/agent/hierarchical-agent-memory/` + `KNOWLEDGE/agent/agent-memory-system/`
- [中] Session Commit 和 Cloud Code 的 Extract Memories 后台 agent 都是"对话结束后自动提取"——设计理念的核心差异是什么？OpenViking 的八类 vs Cloud Code 的四类划分背后的思路不同在哪？ → `KNOWLEDGE/agent/hierarchical-agent-memory/` + `KNOWLEDGE/agent/agent-memory-system/`
- [中] Working Memory 七段式文档为什么对每个段落做"保持/更新/追加"的决策而不是重写整个文档？ → `KNOWLEDGE/agent/hierarchical-agent-memory/`
- [中] 级联更新问题：所有系统准确率 3%，OpenViking 的层级结构如何部分缓解但不从架构上解决？ → `KNOWLEDGE/agent/hierarchical-agent-memory/` + `KNOWLEDGE/agent/agent-memory-cascading-update/`
- [深] L0 摘要质量是层级检索的关键瓶颈——如果 L0 写得不好，整条检索链会怎么失效？这跟 Cloud Code Active Recall 的"选择模型返回空列表"失败模式有什么结构上的相似和不同？ → `KNOWLEDGE/agent/hierarchical-agent-memory/#open-questions` (open)

---

## 跨节点综合

- [深] **Context Engineering、Harness Engineering、Multi-Agent、Structured Output 是 4 件不同的事吗？** 它们之间的包含关系怎么画？哪些是"补偿性工程"、哪些是"系统性工程"？ → `KNOWLEDGE/agent/agent-engineer-ability/` + `KNOWLEDGE/agent/context-engineering/` + `KNOWLEDGE/agent/harness/` + `KNOWLEDGE/agent/multi-agent/` + `KNOWLEDGE/agent/structured-output/`
- [深] **Anthropic Harness 实践案例的核心认知**：永远不让 agent 自我评估、上游规划只给方向不给路径、组件可拆卸——这三条原则在 multi-agent 系统设计里怎么体现？ → `KNOWLEDGE/agent/harness-practice/` + `KNOWLEDGE/agent/multi-agent/`
- [深] **Cloud Code 全栈拆解串成一条线**：四层压缩 / YOLO 分类器 / 6 agent 按阶段拆 / 工具三原则 / 记忆四存五不存 / 系统提示词模块化——这 6 个子系统都在解决"在概率性的模型周围，构建确定性的工程系统"。每个子系统**编码了什么假设、用什么硬约束兜底、什么软约束补缝**？ → `KNOWLEDGE/agent/agent-context-compaction/` + `KNOWLEDGE/agent/agent-permission-system/` + `KNOWLEDGE/agent/agent-role-isolation/` + `KNOWLEDGE/agent/agent-tool-design/` + `KNOWLEDGE/agent/agent-memory-system/` + `KNOWLEDGE/agent/agent-system-prompt/` + `KNOWLEDGE/agent/harness/`
- [深] **Cloud Code 的整体设计哲学**："不信任模型的自觉性，能用硬约束的地方绝不用软约束"——但有些行为（不加冗余功能、克制抽象）没法编进代码、只能写进 prompt。**硬约束 vs 软约束的边界在哪、判断准则是什么**？这条原则会随着模型变强而演化吗？ → `KNOWLEDGE/agent/agent-role-isolation/` + `KNOWLEDGE/agent/agent-permission-system/` + `KNOWLEDGE/agent/harness/`
- [深] **OpsAgent / AgentOps / Multi-Agent RCA / Failure Attribution 串成一条研究线**：工程师做 OpsAgent 时遇到的痛点"Agent 模块单独跑通但端到端联调上不去"，本质上就是缺 AgentOps 的 Failure Attribution 能力。**这条迁移路径（OpsAgent → AgentOps）跟"研究方向定位"的关系是什么**？怎么用这条迁移路径回答"你未来想做什么"？ → `KNOWLEDGE/agent/agentops-vs-opsagent/` + `KNOWLEDGE/agent/multi-agent-rca-paradigm/` + `KNOWLEDGE/agent/agent-failure-attribution/`
- [深] **Claude Code 6 层 vs OpenClaw 2 层 vs Ledger+Views+Policy 三件套 vs AWM/Hermes Skills 程序性记忆**——同一个问题"Agent 跨会话记忆"的四种 design space。每种方案的 (Ledger, Views, Policy) 三件套对应情况是什么？为什么所有开源系统都没把 policy 显式化为 ADD/UPDATE/DELETE Action 序列？这暴露了什么 gap？ → `KNOWLEDGE/agent/memory-architecture-thesis/` + `KNOWLEDGE/agent/agent-memory-system/` + `KNOWLEDGE/agent/agent-skills-closed-loop/` + `PROBLEMS/agent-memory-architecture/`
- [深] **Heuristic Learning 和 Hermes Skills 闭环都在做"agent 积累经验"，但路线截然不同**——HL 强调代码 + tests + replays + memory 的软件系统、Skills 强调 SOP 文档 + 自动 patch。这两条路线的本质差异是什么？什么场景下 HL 更合适（环境 feedback 清晰可验证）、什么场景下 Skills 更合适（任务可流程化）？两条路线能否共存？ → `KNOWLEDGE/agent/heuristic-learning/` + `KNOWLEDGE/agent/agent-skills-closed-loop/`
- [深] **Procedural Memory Object Shape 这条轴**：Skill（人写 / 偏散文）vs AWM workflow（task 反推 / context-conditioned templates with action slots）vs Hermes Skill（agent 自主 create / 7 步闭环带自动 patch）vs Gene（runtime control object with trigger/strategy/avoid/validation）。把这四种当作 design point 而不是线性进化——在 web agent / 运维 RCA / coding agent 三个场景下哪种最合适？为什么？ → `KNOWLEDGE/agent/agent-skills-closed-loop/` + `KNOWLEDGE/agent/heuristic-learning/` + `KNOWLEDGE/agent/agent-memory-system/` + `PROBLEMS/agent-memory-architecture/`
- [深] **memory-architecture-thesis 的"追加更正事件"不变量 vs cascading-update 的"显式依赖图"方向**——这两个其实是**同一族问题的两个视角**还是两个独立机制？bi-temporal 闭合的是"什么时刻什么是真的"（**fact-level 时序**），cascading 解决的是"一个事实变了哪些事实需要重算"（**cross-fact 依赖传播**）。请论证：(1) 为什么 bi-temporal 是必要条件不是充分条件；(2) 为什么"显式依赖图"是 bi-temporal 不变量的天然延伸（从事件序列升级到事件 + 依赖图）；(3) 它失败的不是设计动机，而是什么——这跟 `memory-architecture-thesis` 的三类瓶颈框架（接口带宽 / views 近似误差 / policy 可学习性）哪个对应？ → `KNOWLEDGE/agent/memory-architecture-thesis/` + `KNOWLEDGE/agent/agent-memory-cascading-update/`
- [深] **复合概率 vs 单模型性能**：Forge 用 5 层外部防护让 8B 模型逼近无防护 Sonnet，Anthropic GAN 三 agent 系统用评估器驱动迭代远超单 agent——两个案例的共同信号是什么？"Agent 性能上限不取决于模型能做什么，而是模型周围搭了什么"这句话对"什么时候该换更强模型 vs 什么时候该加 Harness"的决策怎么指导？ → `KNOWLEDGE/agent/small-model-harness-engineering/` + `KNOWLEDGE/agent/harness-practice/` + `KNOWLEDGE/agent/harness/`
- [深] **Cloud Code Active Recall（平面） vs OpenViking 层级检索 vs memory-architecture-thesis（Ledger+Views+Policy）**——三个记忆系统在 "policy 显式化" 这条轴上怎么定位？OpenViking 的 Session Commit 8 类 + Working Memory 7 段最接近三件套的哪一层？layer 检索的"分数传播"相当于 policy 的什么？ → `KNOWLEDGE/agent/hierarchical-agent-memory/` + `KNOWLEDGE/agent/agent-memory-system/` + `KNOWLEDGE/agent/memory-architecture-thesis/`
- [深] **缓存感知架构（ReasonX Append-only + Cache Line Fold）与 agent-context-compaction（Cloud Code 四层流水线）都在管"长上下文里的经济账"，但设计约束不同**——Cloud Code 对象是单次对话不超限，ReasonX 对象是多次请求间缓存命中率最大化。这两个目标冲突吗？如果用 Cloud Code 的"删旧消息"压缩策略，对 DeepSeek API 缓存命中率的影响是什么？如何设计一个同时满足两个目标的压缩策略？ → `KNOWLEDGE/agent/cache-aware-agent-loop/` + `KNOWLEDGE/agent/agent-context-compaction/`
