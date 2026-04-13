# Self-Attention 代码笔记

## Scope

本目录用于记录 Self-Attention 的最小实现思路、张量流动和实现疑问。

## 1. External repos

- [transformer-from-scratch](https://github.com/yourname/transformer-from-scratch)

## 2. 最小实现目标

先做一个最小版 scaled dot-product attention：

- 输入 `Q`, `K`, `V`
- 算 score
- 做 softmax
- 得到输出

## 3. 实现时重点关注

- shape 是否清楚
- batch 维与 sequence 维的排列
- mask 放在哪一步
- attention weights 是否便于观察

## 4. 当前状态

- minimal attention: planned
- masked attention: planned
- visualization / debugging hooks: planned
