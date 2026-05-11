# 面试深挖题：技术八股 + 系统设计

> 对 `cv.md` 技能段每条 + 公共系统设计题的可能追问派生。
>
> 大部分题目 KB 已覆盖——重点在"能不能用反事实 / 数字 / 类比讲清楚"。

---

## E1. Transformer + Attention 八股

| 追问 | KB 节点 | 答题钩子 |
|---|---|---|
| QKV 三组矩阵为什么必要？不分行不行？ | `transformer/qkv-three-matrix-design/` | 极端方案一（一组都不用，X·X^T）→ 图书馆比喻 → 角色焊死；极端方案二（只 QK 投影、V 不投影）→ The animal didn't cross the street 例子 → 匹配特征 vs 传递内容 |
| 为什么除以根号 dk？不除会怎样？ | （需要补 KB 节点：`transformer/attention-scaling/`）⚠️ | 不除 → 高 d_k 时 softmax 趋近 1-hot → 梯度消失 → "用反事实而非'防止梯度消失'结论" |
| Multi-Head 设计动机？参数量一样为什么表达能力更强？ | `transformer/multi-head-attention/` | 单头瓶颈：一个权重分布承载不了多种关系（"小明把妈妈昨天刚买的苹果吃了"——句法 / 语义 / 局部三种关系）；多头总计算量不变但信息容量翻 N 倍；全科医生 vs 8 个专科医生类比 |
| KV Cache 的核心问题？为什么是核心瓶颈？ | `transformer/kv-cache/` | 自回归不对称性（Q 一次性、K/V 累积）；Prefill compute-bound vs Decode memory-bound；具体数字（40 层 / 32 头 / 4096 长度 / FP16 → 2.5GB / request → 64 用户 → 160GB） |
| MLA / MQA / GQA 区别？为什么 MLA 能省那么多？ | `transformer/kv-cache/`（Open Q 提到）⚠️ 详解需要补 KB | MQA 共享所有头的 KV；GQA 分组共享；MLA 用低秩分解 KV 投影——节省 cache 同时保持表达能力；"selective 性"差异 |
| RoPE vs ALiBi 区别？长上下文怎么外推？ | （需要补 KB 节点：`transformer/positional-encoding/`）⚠️ | RoPE 相对位置编码 + 旋转性质；ALiBi 直接在 attention score 加距离衰减；长上下文外推问题（RoPE 频率外推 / YaRN） |
| Pre-norm vs Post-norm？ | `ml/residual-connections/`（Open Q 提到）⚠️ 详解需要补 KB | Pre-norm 训练稳定（梯度更直接），但表达能力略弱；Post-norm 表达强但训练不稳；大模型主流是 Pre-norm |
| FlashAttention 核心思想？ | （需要补 KB 节点：`transformer/flash-attention/`）⚠️ | 不改公式改数据搬运；SRAM vs HBM 带宽差异；分块计算 softmax 的在线算法；memory-bound 优化 |

---

## E2. 训练 + 微调 + 后训练

| 追问 | KB 节点 | 答题钩子 |
|---|---|---|
| PPO vs GRPO 区别？为什么 GRPO 能省 value model？ | `training/rlhf-dpo-grpo/` | 演进谱系：RLHF + PPO 四模型 → DPO 两模型 offline → GRPO 两模型 online；GRPO 用组内 reward 均值替代 value model；REINFORCE-with-baseline 变体 |
| DPO 数学推导主线？ | `training/rlhf-dpo-grpo/` | KL 约束的闭式解 → reward 等价于策略对数概率比 → 带回 BT 偏好模型常数项消除 → 直接用极大似然优化策略 |
| DPO 的局限？衍生变体在做什么减法？ | `training/rlhf-dpo-grpo/` | offline 分布偏移（"去年考试排名"类比）；Iterative DPO / Online DPO 重新采样；IPO 解过拟合；KTO 不要成对偏好 + 去参考模型；ORPO 合并 SFT 阶段 |
| KL 散度在 PPO 里做什么？为什么要约束？ | `training/rlhf-dpo-grpo/` | 防止策略偏离参考模型太远（导致行为失控）；和 clip 机制配合限制单步策略更新幅度 |
| LoRA 为什么低秩有效？rank 怎么选？ | `training/lora/` | Intrinsic Dimensionality——微调真正影响的方向集中在低维子空间；棱镜类比；rank=8/16/32 经验值；rank > 64 通常不增益 |
| LoRA 显存怎么估算？ | `training/lora/` | 4 部分：模型参数 + 优化器状态 + 梯度 + 激活；7B + LoRA + batch=1 + seq_len=2048 大概 16-20GB；激活值是大头 |
| SFT → RL 时机？什么时候可以做 RL？ | `training/sft-rl-relationship/` | SFT 提供合格起点；RL 探索 SFT 数据外的空间；冰山类比；R1-zero 反例（明确奖励信号 + 强 base model 才能跳过 SFT）|
| 奖励坍缩 / Reward Hacking 怎么防？ | `training/rlhf-dpo-grpo/`（OQ 提到）⚠️ 详解需补 KB | (a) 多源奖励（结果 + 过程）;  (b) 规则奖励 + 模型奖励混用；(c) 动态采样跳过无区分度样本（DAPO）；(d) 定期 ablation 验证 reward 是否仍 align |
| 长对话强化学习 reward 怎么设计？ | `training/long-context-rl/` | 千问 LongRL：从"只看答案"改成"过程+结果都看"；Warm-Up SFT + Curriculum RL + Difficulty-Aware Sampling；GRPO + DAPO 配合 |
| Lost in the Middle 怎么解决？两条路？ | `training/long-context-rl/` + `agent/context-engineering/` | RL 训"翻书"能力（千问 LongRL）vs 偏置注意力（Manus 重写 todo list 到末尾）；两条路在不同层 |
| SFT 数据量怎么选？1000 vs 50 vs 10K？ | `training/sft-data-size/` | 50-100 起步验证方向；格式一致性 > 数量；分布对齐；小模型用精简数据集；4 家共识 |
| Continue pretrain vs Finetune 怎么选？ | `training/continue-pretrain-vs-finetune/` | "知识不够 vs 行为不够" 决策树；困惑度量化方法；继续预训练 4 个坑 |

---

## E3. RAG + 检索 + 记忆

| 追问 | KB 节点 | 答题钩子 |
|---|---|---|
| RAG 流程？从哪些角度优化？ | `agent/context-engineering/`（Just-in-time Context） | (a) Chunking 策略；(b) Embedding 选型；(c) 检索（粗筛 + 精排）；(d) Re-ranker；(e) Query rewriting；(f) Citation tracking |
| 为什么大窗口模型出现后 RAG 还有意义？ | `agent/context-engineering/` | "不是装不装得下，是该不该装进去"；窗口大反而稀释 attention；KV cache 成本随窗口爆炸 |
| Procedural / Episodic / Semantic memory 区别？ | `training/long-context-rl/`（提到）+ 主项目（procedural）+ `agent/context-engineering/` | Procedural = "怎么做"（工作流模板）；Episodic = "什么时候发生了什么"（具体事件）；Semantic = "事实知识" |
| Embedding 模型选型？为什么 OpenAI text-embedding-3-large？ | ⚠️ 准备具体对比 | 性能（MTEB benchmark）+ 维度（3072 与 1536 trade-off）+ 成本 |
| 向量数据库怎么选？Pinecone vs FAISS vs Milvus？ | ⚠️ 准备 trade-off 表 | Pinecone 托管 / FAISS 本地内存 / Milvus 自部署可扩展；按部署模式 + 数据规模 + 团队偏好选 |

---

## E4. Agent 范式 + 工程

| 追问 | KB 节点 | 答题钩子 |
|---|---|---|
| ReAct vs Plan-Act vs ToT 各自的边界？ | `agent/agent-engineer-ability/` | ReAct = 边推理边行动（短任务好）；Plan-Act = 先规划后执行（长任务好，但 plan 错传导）；ToT = 树搜索（开销大但能 backtrack） |
| Context Engineering 6 层是什么？ | `agent/context-engineering/` | Compaction / 外化记忆 / 即时加载 / 上下文隔离 / 工具设计 / 缓存友好架构 |
| Harness Engineering 6 关键词？ | `agent/harness/` | 上下文架构 + 架构约束 + 自验证循环 + 上下文隔离 + 长治理 + 可拆卸性 |
| Multi-Agent 什么时候用？什么时候不用？ | `agent/multi-agent/` | 该用：上下文污染 / 并行探索 / 工具过多；不该用：编码任务 / 简单查询 / 拟人化角色分工 |
| Structured Output 6 层？ | `agent/structured-output/` | 约束解码 → 验证重试 → 工具调用 → logit mask → 多 agent schema → 模式锁定 |
| Skill / Harness / OpenClaw / Hermes 各自优缺点？ | ⚠️ Week 1-2 横向对比报告后补 | 待 4 个项目源码读完——这正是横向对比报告的核心 |
| AI 编程工具用过哪些？Cursor / Claude Code / 月度费用？ | 个人经验 | Claude Code（这个 OS 本身就是 daily 协作 ；KB 32 节点都是 Claude 协作出来的） |
| 业务现象归因 / 数据挖掘怎么做？ | ⚠️ 弱项 | 用 Neo 70% 成本降的例子讲——baseline 是把 62 个工具描述全塞 prompt，归因 = token 成本占大头，所以做语义路由减少塞 prompt 的工具数 |

---

## F. 系统设计高频题

| 追问 | KB / 准备 |
|---|---|
| 二级缓存 + 数据一致性策略（cache aside / read through / write through / write behind）？ | ⚠️ 准备完整 4 种策略对比表 |
| Redis 主从故障 / 主从切换怎么处理？请求量超预期怎么办？ | ⚠️ 准备：（1）哨兵 + 客户端重连；（2）降级到 DB；（3）熔断 + 排队 |
| 高并发下单场景 Redis 故障的应对？ | ⚠️ 准备：（1）本地缓存兜底；（2）请求排队；（3）异步补偿 |
| 带过期时间的 LRU 怎么实现？ | ⚠️ 准备代码：双链表 + hashmap + 惰性删除 + 定时清理 |
| 长对话上下文记忆怎么保持？ | `agent/context-engineering/` + `training/long-context-rl/` |
| 多轮对话微调怎么做？数据格式？ | ⚠️ 准备：messages 数组格式 + role 标注 + masking 策略（assistant token 才算 loss） |
| Agentic RL 设计思路？ | `training/long-context-rl/` |
| 如何评估 Agent 效果？ | `agent/harness-practice/`（评估器设计） + 主项目评测设计 |

---

## G. 编程 + 算法

> 字节面经显示手撕 1 小时无（重视上限 > 手撕）；阿里有手撕（链表 / LRU）。
> 暑期 agent 类岗位手撕权重在下降但仍要保底。

| 题型 | 优先级 |
|---|---|
| 链表（反转 / 合并 / 双指针）| P0 |
| 二叉树（遍历 / DFS / BFS）| P0 |
| 字符串（无重复最长子串 / 滑动窗口）| P0 |
| DP 基础（爬楼梯 / 背包 / 最长公共子序列）| P1 |
| 带过期 LRU / 滑动窗口最大值 | P1 |
| Top K / 堆 | P2 |
| 图论 / 拓扑排序 | P2 |
| 复杂 DP / 贪心 | P3 |

策略：每天 leetcode 1-2 题保底；优先刷高频 + 自己卡过的；不追求覆盖率。

---

## H. 行为面 + HR 面

| 题目 | 准备 |
|---|---|
| 自我介绍（2 分钟） | 标准化版本：教育 → 两段实习 → 自主研究 → 主项目 → 未来方向 |
| 职业规划（3-5 年） | 与目标岗位的成长路径对齐——准备 1 个 generic + 3 个公司定制版 |
| 选择本公司的理由 | 每家公司单独准备；不要套话 |
| 实习期待 / 如何判断公司是否符合 | 准备 3 个具体标准：（1）项目类型；（2）mentor 风格；（3）团队氛围 |
| 你最大的优点 / 缺点 | 准备具体故事支撑，不要泛泛 |
| AI 工具使用月度费用 | 诚实说（Claude / GPT 订阅 + API 费用） |

---

## 优先级建议

**Week 1（投递前）必须能答出**：
- A 全部（主项目）
- B1 + B2（自主研究——475-step 含义 / 6-18% / 8 类失败 / matched-mismatched 细节）
- C1（七牛云组长 + 6 步法 + 三类文档——这是讲故事的支点）
- D2（Neo 语义路由——98% 和 70% 怎么算的）
- E1（Transformer 八股 KB 已支撑）
- E2 中 PPO/GRPO/DPO/LoRA（KB 已支撑）

**Week 2（横向对比报告完成后）需要能答出**：
- A4 + E4 末尾的 Skill/Harness/OpenClaw/Hermes 对比

**Week 3+（主项目 MVP 后）需要能答出**：
- A2 的具体 trade-off（用真实做出来的数字代替"我打算这样"）
- A3 的真实评测结果（用真实 pass@1 / 增益比值代替"我会算"）

---

## Gap 标记（需要新建的 KB 节点）

按优先级排序：

| KB 节点 | 用于 | 优先级 |
|---|---|---|
| `transformer/attention-scaling/`（√dk 缩放） | E1 八股 | P0（这题极高频）|
| `transformer/positional-encoding/`（RoPE/ALiBi/YaRN）| E1 八股 | P0 |
| `transformer/flash-attention/` | E1 八股 | P1 |
| `transformer/mqa-gqa-mla/` | E1 八股 | P1 |
| `ml/pre-norm-vs-post-norm/` | E1 八股 | P2 |
| `agent/comparison-claude-code/` | E4 + A4 | P0（Week 1-2 横向对比时建）|
| `agent/comparison-openclaw/` | 同上 | P0 |
| `agent/comparison-hermes-agent/` | 同上 | P0 |
| `agent/comparison-summary/` | 同上 | P0 |
| `training/reward-hacking/` | E2 高频 | P1 |
| `training/multi-turn-finetune/` | F 系统设计 | P1 |

→ 这些节点会在 sprint Week 1-3 边做项目边补完。
