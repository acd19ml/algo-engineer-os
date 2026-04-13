# Self-Attention 参考资料

## Core reference

### Attention Is All You Need

- Vaswani et al.
- Self-Attention 是理解这篇论文的最核心入口之一
- 重点应回看：
  - attention formulation
  - scaled dot-product attention
  - multi-head attention connection

## What to extract

读资料时重点提取：

- 自注意力到底如何建模位置间交互
- 为什么它比纯递归路径更适合并行化
- 它带来的新瓶颈是什么

## Current notes

- 这个节点应保持比 Transformer 更机制级
- 需要避免把 multi-head attention 的全部内容都提前塞进来
