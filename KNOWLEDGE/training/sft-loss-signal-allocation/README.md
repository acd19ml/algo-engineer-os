# SFT Loss Signal Allocation

## 它要解决什么问题

SFT 数据格式看起来只是工程模板：System、User、Assistant 多轮对话，prompt 部分 label 设成 `-100`，loss 只算 assistant 输出。

但这只是第一层。真正的问题不是数据长什么样，而是**训练信号往哪里流**：哪些 token 贡献梯度、不同回复长度怎么分配权重、同一回复里的 token 是否都同等重要。每一层默认值都会改变模型实际看到的数据分布。

## 角色 mask 是最低层：通常只训练 assistant

标准做法是把 system prompt、用户问题、角色标记这些位置的 label 设成 `-100`，利用 PyTorch Cross Entropy Loss 的 ignore 机制跳过它们。模型只在 assistant 回复位置上计算 loss。

这有明确动机：SFT 想教模型 "在给定指令和上下文时怎么回答"，不是让模型学习复述用户问题或系统提示词。

如果不 mask prompt，模型会被迫预测用户输入和系统提示。这会把训练目标混成语言建模，而不是行为模仿。对聊天模型来说，这通常不是想要的信号。

但 "prompt 完全不算 loss" 也不是绝对真理。

## Prompt loss weight：短回复场景下，0 不一定最优

Prompt Loss Weight (PLW) 把 prompt 是否计算 loss 从二元选择变成 0 到 1 的连续权重。`PLW = 0` 是标准做法，完全不算 prompt；`PLW = 1` 是 prompt 和 assistant 全算；中间值给 prompt 一个很小的梯度贡献。

关键观察是：当 assistant 回复很长时，`PLW = 0` 通常没问题，因为回答本身已经提供了足够训练信号。

但当回复很短时，比如只有几个 token，assistant 部分的梯度信号太少，模型容易过拟合到少量输出 token。给 prompt 一个很小的非零权重，比如 0.1，可能像正则化一样增加约束，让模型不要只盯着短答案表面。

所以第一层取舍是：标准聊天 SFT 默认只算 assistant；如果数据里大量短回复，可以把 prompt loss 当成一个需要实验的正则项，而不是死规则。

## 多轮对话里，loss 聚合方式会改变样本权重

第二层更隐蔽：多轮对话里每一轮 assistant 回复长度不同，loss 应该怎么聚合？

Per-token 等权最常见。每个 token 对 loss 的贡献一样，所以 200 token 的长回复天然比 20 token 的短回复重要 10 倍。它的直觉是：长回复包含更多信息，应该贡献更多梯度。

Per-turn 等权先对每轮回复内部按 token 平均，再让每一轮权重相同。这样短但重要的一轮不会被长回复淹没。它适合你认为 "每轮交互都是一个行为单元" 的场景。

Per-sample 等权让每条对话样本总权重相同，再在样本内部拆分。它适合你关心不同对话之间的公平性，不希望轮数多的样本抢走训练资源。

具体例子：数据 A 是一轮长回复，数据 B 是三轮短回复。Per-token 下，A 可能主导梯度；per-turn 下，B 的三轮会拿到更多总权重；per-sample 下，A 和 B 各占一半，B 内部三轮再平分。

同一批数据，三种聚合方式会产生三种不同训练分布。很多框架默认 per-token，不是因为它一定最好，而是实现最简单。

## Token 级加权：不是每个输出 token 都同样值得学

第三层更细：同一轮 assistant 回复里，每个 token 是否都该等权？

传统 SFT 默认全 token 学习，但回复里有些 token 承载核心逻辑，有些只是可替换表达。比如 "因此" 换成 "所以"，通常不改变推理；但数学推导里的关键关系词、步骤结构、变量绑定更重要。

Profit 这类方法的直觉是利用模型概率区分 token 价值：高概率 token 往往承载稳定的语义框架，低概率 token 更可能是风格性或随机表达选择。选择性 mask 低价值 token，可以减少模型拟合表面措辞的压力，把信号集中到核心逻辑。

DFT 的路线不同，不直接 mask，而是按 token 概率缩放 loss，让梯度估计更均匀稳定。两者共同指向一个趋势：SFT 的 loss 计算从 "哪些角色算" 走向 "哪些轮次怎么算"，再走向 "每个 token 给多少学习信号"。

这层还不是所有工程团队都会马上用的默认技巧，但它提醒你：全 token loss 不是中性选择，它也在表达一种假设，即所有输出 token 同等重要。

## Packing 会悄悄改变有效分布

工程上为了提高 GPU 利用率，经常把多条短样本 packing 成一个长序列。很多实现只关注 attention mask，确保不同样本之间互相看不到，却忽略了 loss 权重是否保持一致。

如果 packing 前你想要 per-sample 等权，packing 后却按整个长序列做 token 平均，短样本可能被长样本淹没。训练能跑，loss 也会降，但有效数据分布已经变了。

所以 packing 后必须显式保留原来的权重语义：每条样本、每轮对话、每个 token 的权重在 packing 前后应该一致。否则 packing 不只是吞吐优化，而是在无意中改训练目标。

## 这道题的核心回答

SFT 数据格式的表层答案是 ChatML / Llama chat template、多轮角色标记、prompt label 设 `-100`。

更深的答案是：SFT 格式本质上定义了 loss 信号分配。第一层决定 prompt 是否贡献梯度；第二层决定多轮、多样本之间怎么分配梯度；第三层决定同一回复内部哪些 token 值得学；packing 则要求这些权重在工程优化后不被破坏。

一句话概括：SFT 数据格式不是文件格式问题，而是训练信号路由问题。

## Open Questions

- Prompt loss weight、per-turn/per-sample weighting、token-level weighting 之间可能互相耦合。短回复数据里，PLW 的收益是否会被 per-turn 等权放大或抵消，需要实验确认。
- Profit / DFT 这类 token 级方法在开放式对话、工具调用、代码生成上的收益是否一致？如果高概率 token 代表 "模型本来就会"，那强调高概率 token 和学习新行为之间的张力需要更清楚的边界。
