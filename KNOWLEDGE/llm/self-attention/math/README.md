# Self-Attention 数学笔记

## Scope

本目录用于记录 Self-Attention 的核心公式、张量关系和复杂度理解。

## 1. Core formulas

优先整理：

- Q, K, V 的定义
- score matrix 的计算
- softmax 的作用
- weighted sum 的输出意义

## 2. 需要重点解释的问题

- 为什么 Q 和 K 的内积可以表达相关性？
- 为什么 softmax 后每个位置会形成对其它位置的注意分布？
- 为什么 attention 可以处理长距离依赖？

## 3. Complexity notes

需要继续写清：

- 时间复杂度
- 空间复杂度
- 为什么序列长度增长会带来明显成本

## 4. Next steps

- 先写出最小版 attention 公式
- 再配一个小型 shape 例子
- 最后回连到 Transformer block
