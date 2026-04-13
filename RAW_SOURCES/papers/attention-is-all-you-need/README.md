# Attention Is All You Need

## Basic info

- Title: Attention Is All You Need
- Authors: Vaswani et al.
- Year: 2017
- Source: https://arxiv.org/html/1706.03762v7

## Why I am reading this

这是 Transformer 的原始论文，也是后续 LLM、ViT、MLLM 等很多路线的结构起点之一。

这篇论文不只是“介绍一个模型”。  
它更适合作为一条完整闭环的起点：

- source
- problem
- node
- project
- repro asset

## First-pass extraction

这一轮阅读重点不是追求全懂，而是先回答这些问题：

- 论文试图解决什么问题？
- 为什么当时的 RNN / LSTM 路线不够？
- attention 在这里到底扮演什么角色？
- Transformer 的核心结构是什么？
- 哪些内容应该拆成独立 knowledge nodes？

## Related system objects

- [Sequence Modeling Problem](../../../PROBLEMS/modeling/sequence-modeling/README.md)
- [Transformer Node](../../../KNOWLEDGE/llm/transformer/README.md)
- [Self-Attention Node](../../../KNOWLEDGE/llm/self-attention/README.md)
- [Positional Encoding Node](../../../KNOWLEDGE/llm/positional-encoding/README.md)
- [Reading and Reproduction Project](../../../PROJECTS/research/attention-is-all-you-need-reading-and-reproduction/README.md)

## Raw notes

这里先放粗读笔记，不追求结构完美。

- 论文核心问题不只是“能不能用 attention”，而是“如何更好地做 sequence modeling，同时提升长距离依赖建模能力和训练并行性”
- Transformer 的关键转变，是把序列建模的主路径从 recurrent path 转成 attention-based global interaction
- 位置关系没有消失，而是从结构内置变成显式 positional signal
- 这篇论文适合拆出至少三个高复用节点：Transformer、Self-Attention、Positional Encoding

## Next extraction targets

- 提取 problem framing，回写到 `PROBLEMS/modeling/sequence-modeling/`
- 提取结构层信息，回写到 `KNOWLEDGE/llm/transformer/meta.yaml`
- 提取最小实现目标，回写到项目页和 external repo 计划
