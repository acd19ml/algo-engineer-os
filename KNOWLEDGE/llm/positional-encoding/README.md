# Positional Encoding

## 1. 这个节点是什么

Positional Encoding 是在 attention-based architecture 中显式注入位置信息的方法。  
因为 Self-Attention 本身不天然知道序列顺序，所以位置表示成为 Transformer 路线里的关键补充机制。

## 2. 为什么重要

如果没有 position signal，Self-Attention 很难区分：

- 哪个 token 在前
- 哪个 token 在后
- 相对位置关系如何影响语义

这个节点的重要性在于：

- 它解释了 Transformer 如何表达顺序
- 它直接连接后续 RoPE、relative position encoding 等路线
- 它是 long-context 路线的高复用入口

## 3. 节点类型

- concept
- mechanism

## 4. 前置知识

- [Self-Attention](../self-attention/README.md)
- Transformer 的基本结构
- 基本三角函数直觉（用于理解 sinusoidal encoding）

## 5. 相关问题

- [Sequence Modeling](../../../PROBLEMS/modeling/sequence-modeling/README.md)

## 6. 相关节点

- [Transformer](../transformer/README.md)
- [Self-Attention](../self-attention/README.md)

## 7. 替代方案 / 邻近方案

- sinusoidal positional encoding
- learned positional embedding
- relative position encoding
- rotary position encoding（后续再拆）

## 8. 下游用途

Positional Encoding 会反复出现在：

- Transformer 基础理解
- decoder-only LLM
- long-context methods
- multimodal position design

## 9. 相关项目

- [Attention Is All You Need Reading and Reproduction](../../../PROJECTS/research/attention-is-all-you-need-reading-and-reproduction/README.md)

## 10. 外部仓库

- [transformer-from-scratch](https://github.com/yourname/transformer-from-scratch)

## 11. 当前状态

- concept: done
- math: doing
- code: planned
- reproduction: planned
- comparison: planned
- personal insight: doing

## 12. 目录说明

- `math/`：位置表示公式和直觉
- `code/`：最小注入方式与实现记录
- `refs/`：原论文及后续路线资料
- `thoughts/`：个人判断与后续拆分思路

## 13. 未决问题

- Position 应更优先理解为 absolute encoding，还是更优先理解为 relative relation？
- 对学习路径来说，是先理解 base positional encoding，还是直接进入 RoPE 更高效？
- Positional Encoding 这个 node 应保持多宽，才不会和后续 RoPE / MRoPE 路线混层？

## 14. 补充说明

这个节点应保持为高复用入口，不要一开始就把所有 position family 都揉进去。
