# Self-Check: Training

> 日常自检：从上往下看题，能答出来跳下一题；卡住就点链接跳到知识节点重新学。
> 答案不在这里——答案在链接的节点里。

---

## 自己跑预训练的可行性

- [浅] 7B 模型在单卡 A100 80GB 上能不能训？需要哪些优化技巧才能拉到上限？ → `KNOWLEDGE/training/posttrain-practice-roadmap/`
- [浅] 一个月跑预训练的预算估算——大概多少钱？经验公式 "训练所需 token ≈ 模型参数 × 20" 怎么用？ → `KNOWLEDGE/training/posttrain-practice-roadmap/`
- [中] 第 1 周为什么先做数据工程而不是上 GPU？"数据是预训练的地基" 怎么理解？去重 / 分词 / 数据配比各解决什么问题？ → `KNOWLEDGE/training/posttrain-practice-roadmap/`
- [中] 第 2 周的"故意制造事故"具体做什么？Loss Spike 长什么样、出现时如何分析？为什么 Google 训 PaLM 会有 20+ 次 spike？ → `KNOWLEDGE/training/posttrain-practice-roadmap/`
- [中] 真正"攒到经验"的标准是什么？面试时被问"你训过吗"——能答得出哪些具体问题才算合格？ → `KNOWLEDGE/training/posttrain-practice-roadmap/`

## 继续预训练 vs 微调：何时用

- [浅] 继续预训练（无监督）和微调（有监督）的根本区别是什么？"知识 vs 行为"用一句话说出来。 → `KNOWLEDGE/training/continue-pretrain-vs-finetune/`
- [中] 两个判断方法——"直接问模型" 和 "用困惑度量化"——分别怎么用？什么情况下结论是 "直接微调就够"、什么情况下是 "必须先做继续预训练"？ → `KNOWLEDGE/training/continue-pretrain-vs-finetune/`
- [中] 继续预训练的 4 个经典坑——灾难性遗忘 / 数据质量 / 训练不充分或过度 / 和微调阶段的衔接——各自的解决方案是什么？为什么领域数据占比通常不要超过 50%？ → `KNOWLEDGE/training/continue-pretrain-vs-finetune/`
- [深] 医疗问答系统的例子——为什么"拿医疗问答对去微调"解决不了"模型胡说"的问题？模型背了模板"换个问法就露馅"——这反映了 SFT 的什么本质局限？ → `KNOWLEDGE/training/continue-pretrain-vs-finetune/` + `KNOWLEDGE/training/sft-rl-relationship/`

## SFT 和 RL 的关系

- [浅] "预训练模型的能力是冰山"——SFT 激活的是水面上的部分还是水面下？强化学习的作用呢？ → `KNOWLEDGE/training/sft-rl-relationship/`
- [中] SFT 的天花板在哪？为什么 100 段对话示范不能让模型在第 101 种场景表现好？ → `KNOWLEDGE/training/sft-rl-relationship/`
- [中] 强化学习"激活已有但未被覆盖的能力" 怎么理解？数学题分情况讨论的例子——为什么这种策略 SFT 没教模型却"自己学会了"？ → `KNOWLEDGE/training/sft-rl-relationship/`
- [中] DeepSeek R1-zero 没做 SFT 直接 RL——为什么这条路对它可行？三个条件是什么？ → `KNOWLEDGE/training/sft-rl-relationship/`
- [中] 一般情况下为什么不能跳过 SFT？乒乓球的类比怎么用？"起点太差，探索无效"是什么意思？ → `KNOWLEDGE/training/sft-rl-relationship/`

## LoRA

- [浅] LoRA 的 ABC：B 矩阵为什么初始化为 0？这有什么效果？ → `KNOWLEDGE/training/lora/`
- [中] 为什么"加一个低秩矩阵到原权重上"就能注入新能力？棱镜的类比怎么用？关键的几何直觉——"只在 R 个方向上修正" 是什么意思？ → `KNOWLEDGE/training/lora/`
- [中] R = 8 时只修改了 8 个方向，剩下数千个方向不变——为什么这就能显著改变模型行为？层叠结构的级联放大效应怎么理解？ → `KNOWLEDGE/training/lora/`
- [中] LoRA 比全参微调更抗遗忘的根本原因是什么？不是"权重没动过"，那是什么？ → `KNOWLEDGE/training/lora/`
- [中] Intrinsic Dimensionality 是什么？为什么 ΔW 可以是低秩的？预训练 vs 微调的差异怎么支持这个论点？ → `KNOWLEDGE/training/lora/`
- [中] Rank 怎么选？什么任务用 4-8、16、32？为什么超过 64 基本不会有明显收益？ → `KNOWLEDGE/training/lora/`
- [中] LoRA 加在哪些层？原始论文 vs 后来工程实践的差别是什么？代价怎么权衡？ → `KNOWLEDGE/training/lora/`

## LoRA 显存估算

- [浅] LoRA 微调显存怎么拆成 4 部分？每部分的来源是什么？ → `KNOWLEDGE/training/lora/`
- [中] 7B 模型 + LoRA + batch=1 + seq_len=2048——4 部分各占多少？总计多少？24GB 4090 能不能跑？ → `KNOWLEDGE/training/lora/`
- [中] 激活值的"系数 10-30" 是什么意思？梯度检查点能省多少？代价是什么？ → `KNOWLEDGE/training/lora/`
- [中] 实操技巧：先 batch=1 测，再线性外推——为什么有效？激活值和 batch_size 的关系是什么？ → `KNOWLEDGE/training/lora/`

## 长上下文 RL 训练

- [浅] Lost in the Middle 现象——长上下文模型会出现什么具体行为？为什么 "12 万 token 窗口" 看似够用却仍有问题？ → `KNOWLEDGE/training/long-context-rl/`
- [中] 千问 LongRL 的核心思路——把奖励从"只看答案"改成"过程和结果都看"。具体怎么落地？ → `KNOWLEDGE/training/long-context-rl/`
- [中] 三个核心设计（Warm-up SFT / Curriculum-Guided RL / Difficulty-Aware Sampling）各自解决什么问题？什么是 entropy collapse、为什么渐进式扩展能缓解？ → `KNOWLEDGE/training/long-context-rl/`
- [中] GRPO 比传统 PPO 简化在哪？组内 reward 均值替代了 Value Network 的什么角色？ → `KNOWLEDGE/training/long-context-rl/`
- [中] DAPO 的三个解决（动态采样 / 超长惩罚 / 非对称裁剪）——传统 PPO 的对称裁剪为什么会让模型"过早收敛到局部最优"？ → `KNOWLEDGE/training/long-context-rl/`
- [深] 千问 LongRL-32B 训练后涌现出 4 个行为（信息定位 / 子目标拆解 / 错误回溯 / 答案验证）——这些和 OpenAI o1 / DeepSeek R1 的 reasoning 训练是同一回事吗？ → `KNOWLEDGE/training/long-context-rl/#open-questions` (open)

## RLHF → DPO → GRPO 演进谱系

- [浅] RLHF 标准流程的 4 步 + 4 模型——分别是哪 4 步、4 模型？为什么这套范式"太重"？ → `KNOWLEDGE/training/rlhf-dpo-grpo/`
- [浅] DPO 的核心简化——把 4 模型变成 2 模型——具体砍掉了哪 3 件事？ → `KNOWLEDGE/training/rlhf-dpo-grpo/`
- [中] DPO 的数学推导主线："KL 约束有闭式解 → reward 等价于对数概率比 → 带回 BT 模型常数项消掉"——讲清楚每一步在做什么。 → `KNOWLEDGE/training/rlhf-dpo-grpo/`
- [中] DPO 的核心局限是 **offline 分布偏移**——用 "去年考试排名指导今年学习" 的类比说明。Iterative DPO / Online DPO 怎么缓解？ → `KNOWLEDGE/training/rlhf-dpo-grpo/`
- [中] DPO 衍生（Iterative / Online / IPO / KTO / ORPO）各自做了什么减法？KTO 怎么"连成对偏好都不要"？ → `KNOWLEDGE/training/rlhf-dpo-grpo/`
- [中] GRPO 的核心创新是 **组内 baseline**——它怎么省掉了 value model？为什么"采一组样本的平均奖励当 baseline" 在样本量够大时已经够准？ → `KNOWLEDGE/training/rlhf-dpo-grpo/`
- [中] 演进谱系对比表：RLHF / DPO / GRPO 在 Reward Model / Value Model / 在线采样 / 模型数 4 列上各是什么？为什么 GRPO 同时拥有 DPO 的轻量和 PPO 的在线探索？ → `KNOWLEDGE/training/rlhf-dpo-grpo/`
- [中] GRPO 的适用边界——为什么对数学和代码效果极好、对开放式对话不行？DeepSeek R1 训练里怎么混用 GRPO 和偏好数据？ → `KNOWLEDGE/training/rlhf-dpo-grpo/`
- [深] 整条演进路径的本质——"对齐哪些环节是真正必要的？哪些可以简化"。GRPO 之后这条线还会怎么走？强 LLM-as-judge 替代人类标注是不是终点？ → `KNOWLEDGE/training/rlhf-dpo-grpo/#open-questions` (open)

## SFT 数据量怎么选

- [浅] 四家大厂的起步建议（OpenAI 50 / Anthropic 50-100 / Google 100 / HF 1000+）——为什么差异不矛盾？是面向场景不同。 → `KNOWLEDGE/training/sft-data-size/`
- [中] OpenAI 强调的"格式一致性"——具体哪些细节会拉低学习效率？标注者一致性为什么是模型性能上限？ → `KNOWLEDGE/training/sft-data-size/`
- [中] 数据分布对齐——OpenAI 的"60% 拒答 vs 实际 5%"例子说明什么？为什么这是"最隐蔽的"微调失败原因？ → `KNOWLEDGE/training/sft-data-size/`
- [中] Anthropic 的小数据 vs 大数据超参数发现——什么时候调 batch size 优先于学习率？ → `KNOWLEDGE/training/sft-data-size/`
- [中] Google 的"先在小模型上验证数据"——为什么这个 trick 极其实用？逻辑链是什么？ → `KNOWLEDGE/training/sft-data-size/`
- [中] Hugging Face 的 SmallTalk 不是随便凑的 100 万条——每个子集都有明确目的。10 万条 OpenHermes / 5 万条 MetaMath 各负责什么？为什么小模型用专门的精简版？ → `KNOWLEDGE/training/sft-data-size/`
- [深] "SFT 不教新事实，只教新行为模式"——这条原则怎么影响数据集设计？什么时候应该用 RAG 或继续预训练，而不是 SFT？ → `KNOWLEDGE/training/sft-data-size/` + `KNOWLEDGE/training/continue-pretrain-vs-finetune/`

---

## 跨节点综合

- [深] **训练范式的全景**：预训练（提供能力冰山）→ 继续预训练（补领域知识）→ SFT（激活合格起点）→ RL（扩展能力边界）。每一阶段在做什么、什么时候可以跳过哪一步？ → `KNOWLEDGE/training/posttrain-practice-roadmap/` + `KNOWLEDGE/training/continue-pretrain-vs-finetune/` + `KNOWLEDGE/training/sft-rl-relationship/`
- [深] **微调路线的选择**：全参微调 vs LoRA vs RAG vs 继续预训练——根据"知识 vs 行为"和"任务规模 / 预算"两个维度，怎么决策？ → `KNOWLEDGE/training/lora/` + `KNOWLEDGE/training/continue-pretrain-vs-finetune/` + `KNOWLEDGE/training/sft-data-size/`
- [深] **Lost in the Middle 的两条解决路径**：千问 LongRL 用 RL 训出"翻书"能力 vs Manus 用 to-do list 重写到末尾"偏置注意力"——两条路在解决同一个问题的不同层吗？哪条更根本？ → `KNOWLEDGE/training/long-context-rl/` + `KNOWLEDGE/agent/context-engineering/`
