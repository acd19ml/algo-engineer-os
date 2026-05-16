# 面试深挖题：主项目 + 自主研究

> 对 `cv.md` 项目栏（主项目 + 自主研究）每条 bullet 的可能追问派生。
>
> 每题 → 链 KB 节点（已有）/ 标记需要新建 KB / 准备答题要点。
>
> 用法：投递前过一遍，每题都能 1-2 分钟答出；模拟面试时反向更新这个文件。

---

## A. 主项目：Coding Agent + Procedural Memory 全链路

### A1. 整体定位类

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 为什么选 claw-code 做 base 而不是从零写 / 也不是 fork 别的项目？ | (1) claw-code 是开源 Claude Code 实现，可以直接挂载扩展模块；(2) 不重新发明轮子，把研究价值聚焦到 memory 模块本身；(3) "站在巨人肩膀上做 incremental contribution" 是开源生态的正确姿势 | KB: `agent/harness-practice/` |
| 为什么是 procedural memory 而不是 episodic / semantic memory？ | procedural memory 编码"如何执行任务"的程序性技能——天然适合 coding agent 这种"任务序列"场景；episodic 适合对话历史回忆；semantic 适合事实知识 | KB: `training/long-context-rl/`（提到 procedural / episodic 划分） + `agent/context-engineering/`（外化记忆即 procedural 思路） |
| 这个项目和 Claude Code 比有什么不同？为什么不只是"做一个更弱的 Claude Code"？ | 我不是做产品——是基于 claw-code 做**研究维度的延伸**：在一个具体 sub-problem 上（procedural memory 的 selective transfer）做 incremental contribution + 评测方法学 | KB: `agent/harness-practice/`（Anthropic 立场：harness 模块化迭代） |

### A2. 全链路环节追问

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 业务定义环节具体怎么做？"业务"是模拟还是真实？ | SWE-bench-Lite 上的 issue 即"业务"——每个 issue 是真实 GitHub repo 的真实 bug fix 需求；用其原生的 pass@1 作为成功判断 | ⚠️ Gap: SWE-bench-Lite 具体 issue 结构等做完才知道 |
| Multi-agent 架构里 Supervisor + Sub-Agents + Memory Pool 三者怎么通信？ | Supervisor 用 LLM 分析任务后**派单**给 Sub-Agent；Sub-Agent 执行时从 Memory Pool **按需检索** procedural memory；执行完成后由 Supervisor 决定是否把新 trajectory **回写** Memory Pool；通信通过结构化消息（schema-defined）非自然语言 | KB: `agent/multi-agent/`（Anthropic 立场 + Manus 通信原则） + `agent/structured-output/`（第 5 层：多 agent 通信） |
| 数据生产环节：trajectory 怎么生成？oracle 用什么模型？ | 用强 LLM（GPT-4 / Claude）作 oracle，对 SWE-bench-Lite 的 issue 跑出标准解决轨迹（含工具调用、推理链、最终 patch）作为训练 trajectory | ⚠️ Gap: oracle 选什么取决于预算（预算紧用 Claude Sonnet） |
| 从 trajectory 怎么蒸馏成 procedural memory？ | 不直接存原始 trajectory（太长）——按 "成功步骤的 strategy + trigger condition + avoid constraint" 三元组做压缩；类似 AWM 的 workflow 提取，但加上 "可执行性约束"（必须能被 agent 直接调用而非散文描述） | KB: `agent/context-engineering/`（外化记忆） + `training/long-context-rl/`（千问 LongRL 的 trajectory→memory） |
| SFT 用什么数据训什么？label 是什么？ | 数据 = (context + retrieved memory) → (next action)；label = oracle trajectory 的下一步动作；用 Qwen 2.5-7B + LoRA | KB: `training/lora/` + `training/sft-data-size/` |
| GRPO 的 reward 怎么定义？rollout 怎么采？ | 主 reward = issue 的 pass@1（test 通过率）；辅助 reward = 步骤效率（用尽量少的步数解决） + memory 调用恰当性；rollout 在 SWE-bench-Lite 上一次 sample 多个解决路径，用组内 baseline 做 advantage 估计 | KB: `training/rlhf-dpo-grpo/`（GRPO 详解） + `training/long-context-rl/`（DAPO 优化） |
| 评测：matched / mismatched 怎么定义？什么是"结构相似"？ | matched = source memory 的 issue 与 target issue 在**任务结构上相似**（相似的 bug 类型 / 相似的修复模式）；mismatched = source 和 target 任务结构差异大；具体判定可以用 (a) 人工标注一小批 (b) 用 LLM 判定 (c) 基于元数据（issue label / file type） | ⚠️ Gap: 具体方法等 SWE-bench-Lite 数据上手再定 |
| 部署：vLLM 上线的关键考虑？ | (1) KV cache 管理（PagedAttention）；(2) 工具调用的 server-side 沙箱（Docker 隔离）；(3) memory pool 的检索作为外部 API 调用，避免与推理路径耦合 | KB: `transformer/kv-cache/`（memory-bound 论述） |

### A3. 评测设计的四个指标

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| pass@1 vs pass@k 的区别？为什么用 SWE-bench-Lite？ | pass@1 = 一次采样的通过率（贴近真实使用）；pass@k = k 次采样里至少一次通过（衡量上限能力）；SWE-bench-Lite 是 SWE-bench 的精简子集，issue 数量适中、社区标准评测、有 leaderboard 对比基础 | ⚠️ Gap: 还没跑过 SWE-bench 实测 |
| issue 类型分桶（bug fix / feature add / refactor）的意义？ | 不同类型 issue 对 memory 的依赖程度不一样：bug fix 是 pattern matching 强（memory 可能有效）；feature add 是 novel reasoning 强（memory 可能拖累）；refactor 是 structural（memory 看是否捕获了结构模式）——分桶能定位"memory 在哪种任务上真有用" | 链 KB: `training/long-context-rl/`（千问 LongRL 的 difficulty-aware sampling 思路类似） |
| matched / mismatched 增益比值具体怎么算？ | gain_ratio = (matched 上加 memory 的 pass@1 提升) / (mismatched 上加 memory 的 pass@1 退化)；> 1 表示 selective 有效；< 1 表示 memory 没有 selectivity（反而误伤）；理论上想要 >> 1（高度 selective） | ⚠️ 这是自主研究项目方法学的延伸 |
| 失败模式归类怎么避免主观？ | 用 paired-case 配对法（baseline vs workflow 同步、按 positive/negative/ineffective/redundant 四类）；归类时做双盲（先两人独立标注、再合并）；归类后形成可回归的自动检测规则——后续每次跑评测就能自动产出 boundary pattern 分布 | 自主研究项目里的方法学 |

### A4. 横向对比研究

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| Claude Code / OpenClaw / Hermes 三个项目的记忆机制核心差异？ | **Claude Code**：CLAUDE.md（固定前缀）+ Skills（渐进加载）+ sessions（短期）；**OpenClaw**：Brain & Hands 解耦、Gateway 协议层；**Hermes**：（看完源码再补） | ⚠️ Gap: Week 1-2 横向对比时填充 → 新建 `KNOWLEDGE/agent/comparison-*` 节点 |
| 你的"运维场景思想实验"具体怎么做？ | 不搭真实运维环境——基于七牛云实习经验提出："故障域聚合记忆 + subagent 并行验证不同方向 + 失败轨迹按原因分类"作为对 procedural memory 在运维下钻场景应用的设计假设；思想实验不要求 deliverable，但展示对该方向的深度思考 | KB: `agent/multi-agent/`（subagent 并行设计） |
| 五维度（记忆 / 工具 / 上下文 / 错误恢复 / 反馈）你最关注哪个？为什么？ | 记忆机制——这是 4 个项目差异最大的维度，也是 procedural memory 这条主题最相关的；其它 4 维度作对照 | KB: 全部 `agent/*` 6 节点 |

---

## B. 自主研究项目

### B1. AWM 复现 + 475-step paired-case 分析

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| **475 step-pair 具体是怎么算出来的？是 475 个独立题目吗？** | **不是**——是 7 个站点、52 个 task 展开后的 step-pair 总数。每个 paired case = 同站点、同 task_id、同 step_idx 下，baseline (no_workflow) vs offline_wf 的对比；52 个 task 的所有 ground-truth step 加起来 = 475 step-pair。**独立性不强**，是嵌套结构——适合机制分析，不适合外推强普适性结论 | ⚠️ **关键追问点**——一定要准备好诚实表述 |
| 你说的 6-18% 影响窗口具体怎么算？ | 一个 paired case 的 4 类标签：(0,1) positive、(1,0) negative、(0,0) ineffective、(1,1) redundant；workflow "实际影响" 的 step = positive + negative 占该站点 step-pair 总数的比例；7 个站点该比例分布在 6-18%——意味着 workflow 在大部分 step 上没改变 baseline 行为 | ⚠️ 准备讲清楚 |
| 4 类标签 positive/negative/ineffective/redundant 各占比？哪类最多？ | redundant 通常最多——说明 baseline 在大部分 step 已能做对，workflow 没必要贡献；positive + negative 加起来 6-18%（实际影响窗口）；**ineffective 单独占 45-65%**——这是 "workflow 存在但对输出无实质影响" 的占比 | ✅ 数字已对齐 |
| **8 类典型失败模式具体是哪 8 类？** | **结构 = 6 个步骤级机制 + 2 个轨迹现象**（来自 final-report.tex 的 Interpretive Framework 图）。**Matched 上 3 个机制**：(1) strategy redirection（策略重定向），(2) value format correction（数值 / 索引与可读标签等格式纠偏，如 Newegg P-3），(3) premature termination prevention（防过早停步 / 空输出，如 Kayak P-1）。**Mismatched 上 3 个机制**：(4) domain misdirection（领域误导），(5) template step-skipping（模板化跳步），(6) apparent workflow-first behavior（错配场景下优先跟 workflow 而非独立推理）。**2 个轨迹现象**：(7) Ineffective（多数步上对输出无实质影响，占 45-65%），(8) Accumulation（轨迹后半段累积差异——matched +13% / mismatched −11%）。**重要细节**：§Failure Taxonomy 还有另一套 8 行表格（Workflow mismatch / Target-site first-run underperformance / Limited coverage 等），命名体系不同——**回答时主线选"6 机制 + 2 轨迹现象"这套，源自摘要 + Figure（Interpretive framework）；如果面试官追问 Failure Taxonomy 那张表，说明那是另一个维度的分类（按"原论文未讨论的边界条件 pattern"组织）**。 | ✅ 已对齐 final-report.tex L132-141 + L1496-1514 |
| 为什么 6 机制要分 matched / mismatched 各 3 个？这种分类的 evidence 是什么？ | 在配对实验中，matched 站点（task 与 workflow 语义对齐）和 mismatched 站点表现出**完全相反的影响方向**——同一个步骤级机制只在某一类站点上常发；6 个机制按"出现在哪种 site" 分类，让"workflow 在哪种情境下帮 / 哪种情境下害" 的因果链清晰可读 | ✅ 自主研究方法学的核心贡献 |
| Accumulation 现象怎么算的 13% / −11%？ | 把 trajectory 切成前半 / 后半，分别看 paired-case 中 (positive − negative) 的累积净增益。matched 站点后半段净增益 +13%，mismatched 站点后半段净减损 −11%——说明 workflow 影响**不是均匀分布在 step 上**，而在轨迹后半段被放大 | ✅ |
| 复现用的什么模型？和原论文有什么差异？ | 用 GPT-4o + Qwen-3.5-9B（原论文是 GPT-4 + GPT-3.5）——所以**结果应理解为 setting-specific 而非 model-agnostic**——这正是为什么"不外推强普适性结论"很重要 | ⚠️ 准备讲诚实边界 |
| 为什么说 step-level 证据丰富但 site-level 覆盖有限？怎么应对？ | step-level 有 475 个观察、足够定位 8 类机制；但 site 只有 7 个，统计意义弱——所以**站点级的 win/loss 分布只能说"在这 7 站点上观察到 mixed"，不能说"AWM 普适地不行"**。应对：(1) 主项目的 SWE-bench-Lite 上扩 issue 数到几百，(2) 跨数据集 cross-validation | ⚠️ 关键边界说明 |
| 这个复现 study 发表了吗？是不是已经被知名机构做过了？ | 没有发表——这是个人研究项目，不是 paper。原论文是 ICLR 2025 的 AWM；我的复现 study 是基于该论文做 boundary 审计 + setting-specific 评测——和原论文研究问题相邻但不同 | ⚠️ 诚实表述——没发 paper 不丢人 |
| 这个研究的意义是什么？你想说明什么？ | 不是说 AWM 不行——而是揭示 "**AWM 的实际影响窗口比论文 aggregate 评分让人以为的小得多**" + "**workflow 的有效性高度依赖 task-workflow 匹配度**"——这条结论直接推动了主项目里的 matched/mismatched 评测设计 | 主项目的方法学起源 |

### B2. selective transfer 实验 (HotpotQA → 2WikiMultiHopQA)

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 为什么选 HotpotQA → 2WikiMultiHopQA？ | 两者都是多跳 QA、但 reasoning 结构稍异——是典型的 near-transfer 场景；近似但不同的两个 benchmark 比"同一 benchmark 内部 train/test split"更能测试 memory 的真实迁移能力 | ⚠️ |
| 三种条件（No Memory / Episodic Trace / Cross-Episode Consolidation）具体怎么实现？ | **No Memory**：模型只看 target question + context；**Episodic Trace**：注入 5 条 source 任务的解决轨迹（保留细节）；**Cross-Episode Consolidation**：把 5 条 source 压缩成一个抽象 lesson 注入（保留 pattern 丢细节）；source budget 固定为 5 | ⚠️ |
| 5 个 source episode budget 怎么定的？为什么不是 10 或 100？ | 5 是 pilot 阶段的实用选择——足够展示 selective 现象，又不至于让 context 过长干扰评测；这条研究是 pilot 不是 production scale，所以 budget 故意小 | ⚠️ |
| matched / mismatched 怎么定义？基于 reasoning pattern 吗？ | 是。原本用粗粒度 "bridge" label，但 pilot 中发现太粗——后细化为 attribute_bridge（film→director→birthplace）和 relation_chain_bridge（wife→husband→brother）两类；matched/mismatched 基于这两个细粒度的对齐情况 | ⚠️ 关键细化 |
| subtype-aware rerouting 是修复什么？怎么实现的？ | 原 pilot 中匹配的 source episode 反而拉低 target 表现——细化 subtype（attribute vs relation_chain）后重新 route source-target pairing，匹配条件下的迁移收益恢复了 | ⚠️ |
| operator-level repair 是修复什么？ | 匹配条件下的 cross-episode consolidation 失效——原因是 consolidated lesson 抽象到不再 executable；refactor 为"保留 operator 序列 + 抽象触发条件"后，consolidation 条件下的收益也恢复 | ⚠️ |
| 这个 pilot 的结论是什么？ | 不是 "selective transfer 不存在"——而是 "selective-transfer evidence 取决于：(1) relevance 怎么操作化、(2) memory 抽象的可执行性"；**方法学层面的贡献 > benchmark 数字层面** | 主项目的 selective 指标设计起源 |
| 这个 pilot 用的什么模型？怎么处理 reproducibility？ | Qwen-3.5-9B + greedy decoding；source budget 固定 5；matched/mismatched split 预定义；evidence 都在 6 个 target case 上（1 主诊断 + 1 process sanity + 4 边界审计） | ⚠️ |

### B3. 两个研究合起来的方法学贡献

| 追问 | 答题要点 | KB 链接 / Gap |
|---|---|---|
| 这两个研究合起来你想说明什么？ | **agent memory 不是"加 vs 不加"二元问题——而是 selective 问题**：在哪些情境下加（matched）、加多深（抽象的 executable 程度）、加错了怎么诊断（boundary pattern detection）——主项目就是把这套方法学带到 coding agent 上验证一遍 | 主项目 + 两个自主研究的因果链 |
| 为什么没去投论文？ | 一是时间——找暑期实习窗口紧；二是规模——pilot 规模不到 paper publishable level；三是论文不是我目标——这两个研究是为了**对 agent memory 系统设计建立自己的方法学直觉**，工程落地比 paper 重要 | 诚实表述 |
| 你和 AWM 原作者交流过吗？ | 没有——但读过他们后续的 follow-up paper，知道他们已经在 workflow refinement + larger model 方向迭代 | ⚠️ 诚实 |

---

## C. 研究方向延伸：从 memory 实验到运维场景 procedural memory

> **这是从 memory 实验 → 运维落地的桥梁思考，是我的 signature insight**。面试中切入时机选对——以下是 cheat sheet。
>
> **核心判断**：拿到少量优质数据，除了 SFT 之外，**memory 是另一条选择路径**——并且在**环境频繁变化**的场景下，memory 比微调更合适。

### C1. 触发场景（哪些问题适合切入）

| 面试官问题 | 切入方式 |
|---|---|
| "你最近在思考什么？" / "你未来的研究方向？" | 直接整段讲（C2 整段 90s 口语稿） |
| "你的两个 memory 项目对工程实践有什么启发？" | 从 AWM revision loop 缺失 → selective transfer 抽象可执行 → 落到 procedural memory for ops |
| "你为什么对 procedural memory 感兴趣？" | 从研究路径切，再延伸到运维场景 |
| **"拿到优质数据你会怎么用？"** | **最适合切入** — memory 是 SFT 之外的另一条路径，尤其在变化场景下更合适 |
| "如果重做 OpsAgent / ZeroOps 你会怎么变？" | 把这个洞察作为"如果重做我会用 procedural memory"的具体方案 |
| "你对 RAG / memory 的区别认知？" | procedural memory vs RAG 的本质对比（可执行结构 vs 知识片段） |

### C2. 讲述链路（约 90 秒口语稿）

1. **起点**：在 AWM 复现里发现核心 gap——**revision loop 缺失**。AWM 能保留 workflow，但发现失败后不会回滚，一旦匹配错就持续误导。
2. **第二步**：selective transfer 实验进一步定位——**单纯抽象不够，记忆抽象必须保留可执行结构**才能真正跨任务复用（要到算子级别的对齐而非主题相关）。
3. **关键认知**：拿到优质数据除了 SFT，**memory 是另一条路径，尤其在环境频繁变化、每次都微调成本太高的场景**。这个判断后来和七牛云的 mentor 交流过，他的回应是"memory 弥补了微调更新太慢的问题"——业界 senior 同样的视角。
4. **落地场景**：运维下钻分析——模型本身够强、工具也成熟，问题不是"能不能做"而是"重复搜索浪费"；当前拓扑、服务依赖、告警模式都是**外部结构**，刚好该用 procedural memory 保留——保留可复用的搜索路径、验证顺序、边界条件。
5. **下一步实验设想**：轻量图结构环境（隐藏拓扑 + 工具查询 + 同症状不同根因 + 环境漂移），先在仿真上验证 "external procedural memory 能否降低重复搜索成本 + 是否支持环境漂移下的 selective reuse"。

### C3. 能扛的面试 challenge

| Challenge | 答 |
|---|---|
| "为什么不微调？" | 环境频繁变化场景下微调成本不可控；每次变更（新拓扑 / 新服务依赖 / 新告警模式）都重训一次代价过高；memory 可热更新且单次更新代价小 |
| "为什么不直接用 RAG？" | procedural memory 保留的是**可执行结构**（搜索路径 / 验证顺序 / 边界条件），不是知识片段；RAG 给的是"应该看什么"，procedural memory 给的是"应该按什么顺序做什么" |
| "携程 → 去哪儿那个例子说明什么？" | 单条成功 / 失败轨迹改记忆决策粒度太细——同范围（旅行订票）但实例间细节差异会让经验互相干扰；解法：分层 + 故障域聚合 + 不在经验层面同一槽位反复修改 |
| "失败轨迹怎么办？" | 按失败原因分类入库，**不用于复用**，但保留作为后续 subagent 并行验证的"已走过的路"——避免无效重试 |
| "拿到优质数据你只能做 SFT 吗？" | 不是。memory 是另一条路径——尤其变化场景下更合适；和 SFT 不是替代关系而是**互补**（base 能力靠 SFT，环境结构靠 memory） |
| "故障域聚合记忆怎么聚？" | 按故障域（service / topology cluster / 业务模块）做记忆 namespace；同一故障域内允许复用，跨故障域强制隔离；故障域之间的失败轨迹用于"反向参考"（这条没走通） |
| "subagent 并行验证不同方向怎么设计？" | 同故障域内调多个 subagent，每个 subagent 拿一条历史成功路径作引；都没排查出来时，**主 agent 主动跳出已有经验、查新方向**（避免老路反复跑） |
| "为什么 ZeroOps 项目里没用 procedural memory？" | ZeroOps 当时还没意识到这个方向；那时主线是 Dify workflow + ReAct + MCP 工具调用，记忆机制相对简陋（只在 agent 内做短期上下文压缩）；这是**事后回看的"如果重做"方案** |

### C4. 边界（别讲大）

- 这是**研究方向 + 思想实验**，不是已做完的项目。讲时要明确说"我在思考 / 我设想"，**不要说"我做了"**。
- 轻量图结构环境**还没搭**，被追问"你怎么实现这个仿真"时要诚实说"还没动手，目前是设计阶段"。
- mentor 同意 ≠ 方向被验证；只是说"业界 senior 觉得合理"。

### C5. 数据飞轮的延伸思考（更上游的问题）

- 程序性记忆**需要同模型一起构建**——base model 能解决的问题不需要召回经验，召回反而增加开销。
- 从一条成功 / 失败轨迹就改 memory 是**不严谨的决定**——记忆系统需要根据业务场景定制 + 分层设计。
- 系统不成熟时，可能需要**工程师对经验标注**才能驱动迭代——这就是我想学的"数据飞轮"。
- 我可能需要**专门训练一个对轨迹分析、生产记忆的模型**——这是训练方面要累积经验的方向。

> **这一段在面试官问 "数据飞轮 / 好数据是什么 / 你想学什么" 时讲，不要主动塞**。
