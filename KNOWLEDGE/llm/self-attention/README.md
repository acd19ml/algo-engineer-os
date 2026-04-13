# Self-Attention

## 1. 这个节点是什么

Self-Attention 是一种让序列中每个位置都能直接与其它位置交互的机制。  
它是 Transformer 的核心机制之一，也是后续很多长上下文与高效注意力路线的起点。

## 2. 为什么重要

如果说 Transformer 是架构级转变，那么 Self-Attention 就是其中最关键的机制级转变。

它的重要性主要在于：

- 允许全局位置之间直接交互
- 不再依赖纯递归路径传播信息
- 更适合并行计算
- 为后续 long-context、KV cache、efficient attention 等路线打基础

## 3. 节点类型

- method
- mechanism

## 4. 前置知识

- attention 的基本概念
- 矩阵乘法与向量相似度
- softmax

## 5. 相关问题

- [Sequence Modeling](../../../PROBLEMS/modeling/sequence-modeling/README.md)

## 6. 相关节点

- [Transformer](../transformer/README.md)
- [Positional Encoding](../positional-encoding/README.md)

## 7. 替代方案 / 邻近方案

- recurrent state propagation
- convolutional sequence modeling
- efficient attention variants（后续再拆）

## 8. 下游用途

Self-Attention 通常会出现在：

- Transformer blocks
- decoder-only LLM
- encoder-only models
- vision transformer family
- many multimodal architectures

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

- `math/`：公式、注意力计算、复杂度
- `code/`：最小 attention 实现与 shape 记录
- `refs/`：论文和补充资料
- `thoughts/`：个人判断、直觉和疑问

## 13. 未决问题

- Self-Attention 真正的优势，更多来自全局交互能力，还是来自更适合并行计算？
- 单头 attention 和 multi-head attention 的能力差异，应在这个节点解释多少，何时拆出去？
- 在学习路径上，Self-Attention 是否应先于完整 Transformer node 理解？

## 14. 补充说明

这个节点应保持为机制级页面，不要把整个 Transformer 架构都揉进来。
