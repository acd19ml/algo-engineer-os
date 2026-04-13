# Transformer

## 1. 这个节点是什么
Transformer 是一种基于注意力机制的神经网络架构，用于高效建模序列中的依赖关系。它是现代 LLM、很多多模态模型，以及大量序列建模系统的核心基础。

## 2. 为什么重要
Transformer 之所以重要，不只是因为它“效果好”，更因为它改变了序列建模的主流范式。

它的重要性主要体现在：
- 用注意力替代了纯递归结构
- 更适合并行训练
- 更容易扩展到大规模数据和参数
- 成为了 LLM、ViT、MLLM 等很多后续系统的共同基础

如果不理解 Transformer，后面很多模型结构都只能停留在“记模块名字”的层面。

## 3. 节点类型
- concept
- architecture

## 4. 前置知识
- [Self-Attention](../self-attention/README.md)
- [Positional Encoding](../positional-encoding/README.md)
- neural network basics

## 5. 相关问题
- [Sequence Modeling](../../../PROBLEMS/modeling/sequence-modeling/README.md)

## 6. 相关节点
- [Self-Attention](../self-attention/README.md)
- [Positional Encoding](../positional-encoding/README.md)

## 7. 替代方案 / 邻近方案
- recurrent architectures（RNN / LSTM 路线）
- decoder-only LLM 是重要后续变体，但不是 base Transformer 本身

## 8. 下游用途
Transformer 是很多后续系统的结构基础，例如：
- decoder-only LLM
- encoder-only representation models
- encoder-decoder generation models
- vision transformers
- multimodal large models

## 9. 相关项目
- [Attention Is All You Need Reading and Reproduction](../../../PROJECTS/research/attention-is-all-you-need-reading-and-reproduction/README.md)

## 10. 外部仓库
- [transformer-from-scratch](https://github.com/yourname/transformer-from-scratch)
- [Repro Index Entry](../../../REPRO_INDEX/external-repos.md)

## 11. 当前状态
- concept: done
- math: doing
- code: todo
- reproduction: todo
- comparison: todo
- personal insight: todo

## 12. 目录说明
- `math/`：公式、结构推导、复杂度分析
- `code/`：从零实现思路、外部代码仓库
- `refs/`：论文、文档、补充资料
- `thoughts/`：个人理解、局限、疑问

## 13. 未决问题
- base Transformer 和现代 decoder-only LLM 的差异应该拆成单独节点，还是在 Transformer 页里概述后链接出去？
- positional encoding 应该作为 Transformer 的子部分理解，还是单独作为更高复用性的节点？
- 从学习路径角度，self-attention 是否值得先拆成独立节点再回到 Transformer？

## 14. 补充说明
这个节点应该作为很多后续路径的起点之一，但不应该试图容纳所有 Transformer 变体。
