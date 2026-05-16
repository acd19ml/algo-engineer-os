# Memory 架构本质：(Ledger, Views, Policy) 三件套 + System 1/2 + 三个上限瓶颈

## 它要解决什么问题

Agent memory 是个长得最像"做对了"的失败领域——所有人都在堆向量库 + RAG，但没人能解释清楚 **Memory 到底是什么**。一个看似干净的提问就能戳穿：

> "Memory = 存储 + 检索吗？"

不是。**存了很多历史不等于能力**。能力来自"历史能不能在当前状态下影响决策分布"。Memory 的价值不在于"存了多少"，而在于**从历史到当前决策的通道是否有效**。

这个节点把作者的 Memory 三命题、System 1+2 分工、以及非参数化方案的三类上限瓶颈连起来，作为理解所有 memory 工作（RAG / agentic memory / KV 注入 / 时序图谱）的统一底座。

## 三个核心命题

### 命题 A：Memory 不是"存储"，而是可被决策利用的外部状态（external state）

把 agent 看成 input → output 函数。**仅仅"存了很多历史"并不构成能力**——能力来自：在当前状态下，历史能否以某种形式影响决策分布。

Memory 系统的工作是从历史中提取**当前可用**的信息（证据 / 摘要 / 子图 / 可执行技能），把它提供给推理层共同产生决策。它的输出要么进入上下文（证据 / 摘要 / 子图），要么直接参与决策（对输出分布做调制）。

> Memory 不等于历史本身，而是"把历史转成当前可用信息"的通道。

### 命题 B：Memory 的最小闭包是 (Ledger, Views, Policy) 三件套

只要系统要满足**可溯源 / 可回滚 / 可观测**这三个硬约束，Memory 的最小形态就不可能是"一个向量库 + 若干 prompt"。它必须是一个能被审计的状态机：

1. **Raw Ledger（权威记录）**：append-only 记录每次写入 / 更新 / 删除发生了什么（输入、时间、scope）。
2. **Derived Views（派生视图）**：面向检索 / 推理的派生状态——向量索引 / keyword/hybrid / KG/TKG / timeline / skill index。Views 可以多、可以 lossy，**但必须可回指 Raw Ledger**。
3. **Policy（控制层）**：决定何时读 / 读多少 / 何时写 / 怎么更新 / 怎么遗忘。这些决策必须**显式化为可记录 / 可回放的 Action 序列**（ADD/UPDATE/DELETE/NONE），而不是"靠 prompt 里一句话暗示"。

类比：Raw Ledger 像账本 / 黑匣子；views 像缓存 + 索引 + 物化视图；policy 像调度器 / 控制回路。**三者缺一**：

- 没账本 → 不可治理
- 没索引 / 抽象 → 不可用
- 没可训练 / 可 A/B 的控制点 → 不可持续迭代

### 命题 C：Memory 的基本单位是 event 序列，但直接用 event 流 ≠ 可用系统

把 Raw Ledger 建模成 event 序列是合理的，因为所有可审计性都依赖"事件闭包"。一个最通用的 ledger 事件至少包含：

- **作用域（scope）**：哪个用户 / 会话 / 任务
- **时间戳**：事件发生的时刻
- **输入观测**：当时的 messages / 环境状态片段
- **系统动作**：包括对外输出，也包括 Memory Tool 的动作
- **记忆变更**：ADD / UPDATE / DELETE / NONE
- **反馈信号**（可选）：reward / 用户评分 / 任务成败
- **决策元数据**（可选）：候选集合 candidate_set / 命中证据 provenance / early stop 阈值

但 event 太底层。如果只存 event 你得到"可审计的历史"，不是"可用的记忆能力"。真正把历史变成能力的是 **views（重组织 / 压缩 / 索引 / 时序化 / 技能化）+ policy（决定什么时候触发哪些 view、怎么更新 view）**。

> event 是 Ledger 的数据形态；views/policy 是能力形态。

## 由此推出闭环系统形态

三个命题合起来得到：

```text
Raw Ledger（权威）→ Views（可用）→ Policy（控制）→ Commit（回写）→ Provenance（可回放）
```

Memory 的本质不是一个组件，而是一个闭环系统。

## 接下来的问题：System 1 + System 2 分工

如果 System 2 不发挥作用，记忆能力只能通过 RL post-training 固化到 System 1（LLM 权重）。这种设定下很难保证记忆特化训练后仍保持通用泛化能力——所以**需要一个非空的 System 2**，承担记忆的写入 / 检索 / 更新，并把决策**显式化为可观测可回放的过程**。

**Memory 能力和 LLM 其他 agent 能力是"相对正交"的**：

> Answer = f_θ(x, r_φ(x, H))

θ 表示通用 LLM/Agent（推理 / 规划 / 工具调用），φ 表示 memory 系统（写入 / 索引 / 检索 / 过滤 / 摘要 / 时序化）。这个接口形式意味着：可以在不动 θ 的前提下通过改 φ 获得增益，也可以反过来。

经验现象支持这点：同一个 base model 不做 memory 特化训练，接入不同 RAG / 长期记忆策略就能显著改变长程任务表现；同一套 memory infra（raw_ledger + views + 检索策略）也常能服务多种 base model。**"跨模型可复用"通常意味着能力更多绑定在接口与外部状态上，而非某个特定模型权重上**。

非正交边界：检索噪声 / 错检 / 时序冲突会直接破坏推理（导致幻觉）；何时检索 / 检索多少 / 何时写入更新等策略也依赖 agent 的自我评估。所以更准确说法是 **"相对正交 + 存在可控交叉项"**，System 2 的 observability / provenance / sandbox A/B 的意义就在于把交叉项显式化、可诊断、可迭代。

System 2 的构型：

```text
                               (final answer / action)
+-------------------+      +---------------------------+      +------------------+
|   User / Env IO   | ---> | System 1: General Agent   | ---> | Output / Effect  |
+-------------------+      | (LLM + tools + planner)   |      +------------------+
                           +------------+--------------+
                                        ^
                                        |  retrieved_context + provenance
                                        |
                                        |  memory_tool(query, ctx)
                                        v
+-----------------------------------------------------------------------------------+
|                         System 2: Agentic Memory (Slow Loop)                      |
|                                                                                   |
|  PreThink --> Retrieve (loop) --> Evidence Accumulate --> Early Stop(conf >= tau) |
|    |             |                     |                      |                  |
|    |             v                     |                      |                  |
|    |       +----------------------+    |                      |                  |
|    |       | Memory Infra         |<---+----------------------+                  |
|    |       |  - Raw Ledger        |        Write / Update (ADD/UPDATE/DELETE,    |
|    |       |  - Derived Views     |        SUMMARY/FILTER, ... )                 |
|    |       |    * Vector / Hybrid |                                              |
|    |       |    * Keyword / BM25  |   Guarantee: 100% provenance (trace to Raw)  |
|    |       |    * KG / Timeline   |   Sandbox: run N strategies in parallel      |
|    |       +----------------------+   Observability: trace / log / metrics       |
|    |                                                                            |
|    +--------------------------- control feedback loop ---------------------------+
+-----------------------------------------------------------------------------------+
```

## 参数化 vs 非参数化：在线适应的两种载体

- **参数化记忆**：经验被写进模型权重；训练 / 微调把历史数据编译进权重；推理时直接用更新后的模型，不需要额外检索
- **非参数化记忆**：经验被写在外部状态里（ledger + views + skill pool + 索引）；写入由 policy 决定写哪些 / 怎么写；推理时通过检索 / 汇聚 / 注入让外部状态影响输出

**差别不在"有没有存储"，而在适应算子写在哪里**。参数化把写入成本前置到训练；非参数化把写入成本分摊到在线 commit + 推理 retrieve+inject。System 2 的意义就是：**把在线适应的主战场从模型权重挪到外部记忆状态与控制策略上，并让它可观测、可回放、可 A/B**。

## 记忆对决策的调制：修正项 Δ

如果把 agent 一步决策写成 logits，最通用的"记忆影响决策"表达方式：**外部记忆对模型输出施加一个可控的修正项 Δ**。System 1 的权重提供基线能力（通用性），Δ 来自外部记忆，负责个性化 / 任务特化 / 时序修正 / 经验复用。

JitRL 给出了这种调制的一个具体形式（用 advantage 做加性调制）：

$$
\text{Logits}_{new}(a \mid s)
=
\text{Logits}_{old}(a \mid s)
+
\alpha \cdot A_{est}(s, a, M)
$$

**只需要维护一个动态的非参数化经验库**（每步决策前检索与当前状态相似的历史轨迹估计 A_est 并对 logits 做加性调制；每个 task/episode 结束把新轨迹 (s,a,r,G) 写回入库），即可实现类似梯度下降的效果。逼近的是 fine-tune 的效果。

这也解释了为什么前文强调 policy 的工具化：**如果 Δ 的来源不可审计（隐式写在 prompt 里），系统无法做到 provenance / rollback / sandbox**。协议要求的正是把 Δ 的来源（命中证据、候选集合、写入动作）显式化。

## 非参数化方案的上限由什么决定：三类瓶颈

参数化的上限来自"权重可以把大量经验压缩进一个可快速前向的函数"；非参数化想逼近它，核心**不是把更多东西塞进库**，而是让 Δ 逼近"如果我真的 fine-tune 了会发生什么"。

| 瓶颈 | 典型可观测指标 | 直觉 |
|---|---|---|
| **接口带宽**（Memory → System 1 注入容量） | 单次注入的有效 token 数 / 信息密度（注入证据被 System 1 实际采纳的比例）/ latency budget 占比 | 注入了很多但 System 1 没用上→带宽浪费；注入太少答错→带宽不够。记忆固化 / 分层记忆 / latent token 都是在提高单位预算的信息密度 |
| **views 近似误差**（views 的逼近误差） | 召回精度（precision@K）/ 漏召回率（recall gap）/ 时序冲突率（返回证据中过期 / 被纠正的比例） | 只要不是把 ledger 全量塞模型，views 就一定近似——错检 / 漏检 / 时序冲突 / 语义漂移会直接污染 Δ。上限不仅取决于"存了多少"，更取决于 views 的误差是否被治理住 |
| **policy 可学习性**（什么时候写 / 读、写什么、信谁） | Action 序列的事后回报 / UPDATE/DELETE 误操作率 / 不必要检索比例 | **真正的上限瓶颈往往不是存储后端，而是 policy**：写多了污染、写少了学不到；召回多了噪声、召回少了信息不够；UPDATE/DELETE 做错一次长期就滚雪球。所以 policy 必须既能学习（RL 训练范式），又能治理（protocol 的候选集合约束 + provenance 闭包 + sandbox 回放 A/B） |

> 在 sandbox / A/B 环境里，三类瓶颈分别对应一组可观测 action-level 指标，用于定位"当前系统的效果差在哪里"。实际迭代中往往先通过 sandbox 回放定位"最疼的那个瓶颈"，再针对性改进。

## Memory 操作的工具化：让 model 像控制手臂一样控制 memory

打破 rubrics-based policy 的禁锢——基于预定义规则控制记忆读写是不可持续的。两种方案：训一个外部 NN（学术界探索为主，难度大），或 Prompt/SFT/RL 一个 LM 来做（更可行，至少 GRPO 训练大家公认）。

**Agentic Memory 概念**：把记忆操作彻底工具化，整合进 Agent 动作空间。让模型像控制手臂一样控制 memory，而非被动接收上下文。参数落在 LLM Agent 上，依赖 LLM 的泛化和迁移能力。

| 记忆工具分类 | 具体操作 | 功能描述 | 对应参数化行为 |
|---|---|---|---|
| 长期记忆（LTM） | ADD | 存储新知识 | 梯度更新（Training） |
| 长期记忆（LTM） | UPDATE | 修正旧知识 | 权重调整（Fine-tuning） |
| 长期记忆（LTM） | DELETE | 移除过时信息 | 灾难性遗忘管理 / 剪枝 |
| 短期记忆（STM） | RETRIEVE | 语义搜索并注入 | 激活相关神经元 |
| 短期记忆（STM） | SUMMARY | 压缩对话历史 | 抽象表征形成 |
| 短期记忆（STM） | FILTER | 移除无关 Context | 注意力机制（Attention Masking） |

## 时序：从"发生过什么"到"何时为真 / 何时被相信"

LLM 对时间天然不敏感（尤其是隐含 / 相对 / 跨时区）。纯语义检索会把"过去的高相似事实"当成"现在仍为真"，导致"过时事实复活"和"被纠正的事实仍反复召回"。

**解决方案不是更强 prompt**，而是把时序提升到架构骨架层：

- **Raw Ledger** 加入双时态：`transaction_time`（系统何时写入 / 更正）≠ `valid_time`（事实在世界中何时为真）。两者不等价——你可以在今天纠正上周发生的事实
- **Views** 不是"相关即可"，而是"在某个查询时间语境下成立"。没有 time slice，语义相似检索会把旧事实当作当前事实
- **Policy** 默认 `time_scope=current`（宁可漏不可错）；需要历史时显式触发 `historical/all`，让 EvidencePack 承载"冲突并存"的证据结构，让 System 1 决策

**关键不变量**：CAS 已锁定时的 UPDATE/DELETE 语义不应是"把旧记录改掉"，而是**"追加一个更正事件"**，让 recall 在 query_time 下选择生效版本。"遗忘 = tombstone commit + 抑制"也兼容这个不变量——tombstone 本质也是一种可审计的 state change。

**这条不变量解决的边界**：bi-temporal + "追加更正事件" 只解决**单个 fact_key 的时序冲突**（fact-level temporal correctness）。它能让 "我住在北京" → "我住在上海" 的两个版本共存于 ledger，由 query_time 选择生效版本。但它**不会自动给依赖事实追加任何事件**——`location` 变了，依赖 `location` 的 `commute=bike-15min` / `gym=望京邮乐` / `social-security=北京` 这些事实的 `valid_time` 不会被任何机制触动，recall 仍会取出它们当作"现在仍为真"。

也就是说，bi-temporal 是 **必要条件，不是充分条件**——它闭合了"什么时刻什么是真的"的**记账问题**，但**没闭合"一个事实变了，哪些事实的真值需要重算"的传播问题**。后者是 [[agent-memory-cascading-update]] 节点专门讨论的级联更新难题（MeMe 论文实测所有主流系统 3% / 1% 准确率）——可以看作本不变量的**未完成续集**。

Zep / Graphiti 用 TKG 给边加入 `[t_start, t_end]` temporal validity，把"曾经为真"和"当前为真"结构化分离——而不是交给 LLM 去"记得别搞混"。在他们的长时序评测上报告比传统 RAG 提升 18.5% 准确率。MAGMA 论文（2026）提出四正交图架构（语义 / 时间 / 因果 / 实体），ablation 显示移除时间骨干后评判分数从 0.700 降到 0.647，证明时间排序提供了不可替代的推理轴。

## Open Questions

- **何时 retrieve 多少 evidence**：early stopping 的 confidence threshold 怎么训？InfMem 用 RL 训出了一个 3.9× 推理加速的 policy 网络，但跨 domain 的泛化怎么样？
- **"状态类事实"（职位 / 住址 / 关系）是否应该形成"默认连续区间"不变量**（同一 fact_key 在 current 下尽量单值），还是完全允许重叠并交给 System 1 处理？
- **memory specialization 训练后 base capability 退化**：如何在 GRPO 训 memory tool 使用策略时不破坏通用 reasoning？跟 `KNOWLEDGE/training/sft-rl-relationship/` 里讨论的"能力激活 vs 能力压缩"是同一条轴。
