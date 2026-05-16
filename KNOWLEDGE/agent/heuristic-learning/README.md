# Heuristic Learning：coding agent 接管 rule-based system 的维护曲线

## 它要解决什么问题

Continual Learning 一直难，主要原因是 NN 的灾难性遗忘——学新任务会覆写旧能力。所有 paradigm shift（pretraining → RLHF → 大规模 RL/RLVR）都没真正解决这个问题。

但一个反常的现象出现了：**当 coding agent 在 loop 里"读失败 → 改代码 → 加测试 → 看 replay"时，整个系统在变强，但模型权重一动没动**。在 Atari Breakout 上，Codex 写出的纯规则策略从 387 分爬到 507 → 839 → 864（接近理论上限）；在 MuJoCo Ant 上没有 NN 也能到 6000+，HalfCheetah 五局均分 11836.7——都在常见 Deep RL 区间。在 VizDoom D3 Battle 上，cv2 + NumPy 写的视觉控制策略 10 个种子下 `mean=557.0 / min=440.0`，没有任何 NN 训练。

这不是"反对深度学习"，是**对启发式策略的维护曲线被 coding agent 改变了**这件事的判断——曾经太贵不值得维护的一类启发式，现在可能值得长期持有了。

## 朴素直觉为什么不够

一个直觉是："那就用 Codex 写规则，让规则越来越好就行"。如果你真这么做，几个月内系统会变成：

> "今天加一条规则修 case A，明天 case B 坏了，后天再加一个 if-else，再后天没人敢删任何东西。"

这就是 1980 年代 expert system 失败的形态。问题从来不是规则没用，是**人维护不动**——多增一条规则就要把它和已有规则在脑子里跑一遍，加 10 条还能撑住，加 100 条系统就开始烂。

所以单纯"用 agent 写规则"是错觉。**真正起作用的不是规则本身，是规则 + 测试 + 日志 + 回放 + 记忆 + 失败方向记录被组织成一个 software system**，让 coding agent 在维护这个 system，而不是维护一条条孤立规则。作者把这个对象叫做 **Heuristic System (HS)**，学习过程叫 **Heuristic Learning (HL)**。

一个 HS 至少包含：programmatic policy / state representation / feedback channels / experiment records / replays or tests / memory / coding agent 执行的 update mechanism。**只有一条 `policy.py` 不算 HS**。

## HL 和 Deep RL 的对照

| Axis | Deep RL | HL |
|---|---|---|
| Policy | NN 参数 | 代码：rules / state machines / controllers / MPC / macro-actions |
| State | 通常是显式 observations | 显式变量 / detectors / caches / 可读表示 |
| Action | NN forward pass | 执行代码逻辑 |
| Feedback | 主要是固定 reward | tests / 环境 feedback / logs / replays 都算 feedback（被 coding agent 消费） |
| Update | 梯度下降更新 NN 参数 | coding agent 直接改代码 |
| Memory | on-policy 几乎没有；off-policy 有 replay buffer | 可以显式存 trials / summaries / failure reasons / replays / version diffs |

读这张表的一个不对称之处：**HL 没有 "梯度更新"，更新是 coding agent 编辑代码**。这听起来像退步，但带来五个性质：

- **可解释性**：NN 难解释；HL 策略经常可以翻译成自然语言
- **样本效率**：一次有效的代码改动可以直接跳到新策略，不用慢慢调 learning rate 爬升
- **可回归测试**：旧能力变成 tests / replays / golden cases
- **过拟合可约束**：HL 也会对 seed / 环境细节 / 测试漏洞过拟合，但 simplification + regression check + multi-seed eval 提供了工程形态的 regularization
- **能避一部分灾难性遗忘**：旧能力不必只活在权重里，可以写进 rule set 和 tests

## 为什么之前没起飞

不是因为启发式不行，而是**人维护不起**。维护 expert system 像工业革命前的手工纺织——一个人能转，量上来就崩。**纺纱机改变了生产曲线；coding agent 改变了启发式的维护曲线**。

今天 agentic feedback loop 长这样：

```text
feature request → agent writes code → tests pass → human feedback → next patch
```

随着模型变强，人介入应该缩小。在边界清晰的系统里，这个 loop 可以自动闭合，HL 就能批量产出 HS：

```text
环境反馈 / 测试失败 / 日志异常
  → coding agent 读 context
  → 改 policy / test / memory
  → 重跑
  → 把结果写回 trials 和 summaries
  → 进入下一轮
```

## HL 怎么处理 Continual Learning

HL 也会"遗忘"，但形态更工程：新规则修了一个 failure mode、坏了另一个旧场景；新记忆反复把 agent 引向错方向；测试太窄、policy 学会绕过它；patch 改了共享接口、老调用方静默崩了。

所以 HL **没自动解决 Continual Learning**，它把"避免遗忘"转化为更工程化的问题。在 HL 里旧能力可以固化为：regression tests / fixed-seed replays / golden traces / failure videos / version diffs / 显式写下的失败方向。

这和把经验压进 NN 权重完全不一样——**HL 历史是显式的、可读的、可删的、可重构的**。它既要记得，也要把一堆 local patch 折回更简单的表示。

> 一个只增不压的 HS 最终会变成大泥球。它"记住了很多事"，但记忆形态太差导致没人敢动，系统就腐烂了。

因此一个健康的 HS 至少需要两种操作：

1. **吸收反馈**（write new failures / logs / rewards back into the system）
2. **压缩历史**（把 local patch 折回更简单更可维护的表示）

Continual Learning 的问题从"怎么更新参数"变成"怎么维护一个持续吸收反馈的软件系统"。

## Coupling Complexity：决定一个 HS 能维护到多大

**Coupling complexity** = coding agent 能维护多复杂的策略才能支持 HL。**不能用代码行数衡量**：500 行干净模块边界、好测试、可复现状态、清晰日志的策略可能很好维护；80 行每行影响每行、没日志没 replay 的策略可能是定时炸弹。

代码侧的 coupling 上限由：模块边界 / 接口稳定性 / 测试覆盖率 / 可观测性 / 回滚成本 / 状态可复现性决定。Coding-agent 侧由：模型能力 / context length / 记忆质量 / 工具质量 / 迭代速度决定。

由此推出几条 working hypothesis：

- **更清晰的反馈** 提升了固定 agent 智能能维护的 coupling complexity
- 同样工具反馈下，更强的模型能维护更高 coupling
- 模块化 / tests / replays 把一部分 coupling 移到环境里
- 记忆和工具扩展 agent 的有效 context
- 一个只增不压的 HS coupling 会失控

**Breakout 拿到 864 不只是规则简单**，更因为失败可以视频回放、本地复现、回归测试。Ant 复杂得多，但能分解成 rhythm / posture / contact / 残差 MPC 模块。**Montezuma 是反例**：Atari57 里某次无人值守跑到 400，但路径是 86 个 macro-action 的开环执行——说明有些环境需要更强的程序形态（可组合 macro-action / 可恢复的搜索状态 / 长期记忆），纯 `if-else` 解决不了一切。

## 由此引出 HL 在 Robotics 中的可能定位

把 System 1 / System 2 的语言借过来，可能的分工：

- **专用 shallow NN**：System 1 一部分，快 + 便宜，做感知 / 分类 / 物体状态估计
- **HL**：也属 System 1，做新鲜数据处理 / rules / tests / replays / memory / safety boundary / local recovery
- **LLM agent**：System 2，给 HL 反馈 / 改进 data / 周期性从 HL 生成的数据里抽提取来更新自己

进一步分层：

```text
joint-level HL → limb-level HL → whole-body balance HL → task-level HL
```

下层管低延迟控制和安全；中层管步态和触觉；上层管任务、recovery、长期记忆。**Coding agent 不需要"懂走路"**，它是插入系统里的 update pipeline：持续把失败视频 / 传感器流 / 仿真结果 / 测试结果喂回系统，再把反馈重写成代码、参数、guard rule 和 memory。

## 边界承认

HL 不能做 NN 能做的一切，受限于"代码能表达什么"——特别是复杂感知和长程泛化。**用今天的认知，无法想象一个 agent 写纯 Python（不用 NN）解决 ImageNet**。

真正的开放问题是：怎么让 NN 和 HL 一起解决 Online Learning 和 Continual Learning。最有希望的方向看起来是：**用 HL 快速处理在线数据，把在线经验变成可训练、可回归测试、可过滤的数据，然后周期性更新 NN**。

LLM agent 可以共享学到的东西，也可以在 robotics 里以隔离分支学习。开放问题：HL 产生的 *特定数据分布* 怎么避免破坏 LLM 周期更新的稳定性？这是经典 post-training 问题，已经有不少成熟经验。

## Open Questions

- HL 在 long-horizon generalization 上能爬到哪个上限？Montezuma 类环境是不是"必须用 NN" 的硬边界，还是只需要更强的 macro-action 抽象？
- HL 数据怎么 filter 才能不污染 LLM 的 periodic update？这跟 SFT / RL 的数据质量问题同构。
- HL 产物（rules + tests + replays + memory）本身是不是一种 procedural memory？跟 `PROJECTS/research/awm-mechanism-audit/` 里讨论的"procedural memory object shape"（Skill / AWM / Gene）是同一条轴吗？
