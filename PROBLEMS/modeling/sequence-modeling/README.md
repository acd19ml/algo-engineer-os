# Sequence Modeling

## 1. Problem definition

序列建模要求模型理解输入序列中不同位置之间的关系，并在需要时利用长距离依赖信息完成表示或生成任务。

这个问题会在语言建模、机器翻译、语音、时间序列等任务中反复出现。

## 2. Why it matters

很多核心 AI 任务本质上都属于 sequence modeling。  
如果模型难以处理长距离依赖，或者训练效率过低，就会直接限制模型能力和规模扩展。

这个问题之所以关键，是因为它同时连接：

- 表达能力
- 训练并行性
- 长序列效率
- 后续系统扩展性

## 3. Typical failure modes

- 长距离依赖难以捕捉
- 训练不能充分并行
- 序列变长后效率迅速下降
- 信息需要跨很多步传播时容易退化

## 4. Contexts where it appears

- `research`
- `training`
- `inference`
- `evaluation`
- `deployment`

## 5. Candidate solutions

- recurrent architectures（RNN / LSTM 路线）
- [Transformer](../../../KNOWLEDGE/llm/transformer/README.md)

## 6. Comparison dimensions

- 长距离依赖建模能力
- 并行训练能力
- 计算复杂度
- 实现复杂度
- 长序列可扩展性

## 7. Related knowledge nodes

- [Transformer](../../../KNOWLEDGE/llm/transformer/README.md)
- [Self-Attention](../../../KNOWLEDGE/llm/self-attention/README.md)
- [Positional Encoding](../../../KNOWLEDGE/llm/positional-encoding/README.md)

## 8. Related projects or work contexts

- [Attention Is All You Need Reading and Reproduction](../../../PROJECTS/research/attention-is-all-you-need-reading-and-reproduction/README.md)

## 9. Current judgment

从当前视角看，Transformer 真正改变的不只是“效果更好”，  
而是它把 sequence modeling 的主要瓶颈，从 recurrent path 上的信息传播限制，转移到了 attention 的计算与内存成本上。

这意味着它没有消灭问题，只是换了一类更适合扩展和工程化的瓶颈。

## 10. Open questions

- Transformer 真正替代 RNN / LSTM 的最关键原因，到底是表达能力、并行性，还是可扩展性？
- 长距离依赖问题在 Transformer 中是否被真正解决，还是只是换成了长上下文成本问题？

## 11. Next steps

- 继续从原论文提取 problem framing
- 比较 recurrent route 与 attention route 的主要 trade-offs
- 在 toy implementation 中观察 sequence interaction 的实际差异
