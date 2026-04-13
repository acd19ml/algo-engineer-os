# Transformer 参考资料

## Source entry

- [Attention Is All You Need Raw Source Page](../../../../RAW_SOURCES/papers/attention-is-all-you-need/README.md)

## Core references
### 1. Attention Is All You Need
- Vaswani et al.
- 这是 Transformer 的原始论文
- 重点应看：
  - motivation
  - architecture
  - attention formulation
  - multi-head attention
  - complexity discussion

## Related references to revisit
- 后续 decoder-only 架构资料
- positional encoding 系列资料
- Transformer 在 vision 中的扩展资料
- efficient attention / long-context 相关资料

## What to extract from references
读资料时应重点提取：
- 结构设计动机
- 核心公式
- 为什么替代 RNN/LSTM
- 复杂度瓶颈
- 对后续模型的影响

## Current notes
- 原论文应作为概念起点，但不能把现代 LLM 结构全部等同于原始 Transformer
- 后续应增加一份 “base Transformer vs modern decoder-only LLM” 的补充资料
