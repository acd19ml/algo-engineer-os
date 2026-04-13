# Positional Encoding 代码笔记

## Scope

本目录用于记录位置编码在 toy Transformer 里的最小实现与工程观察。

## 1. External repos

- [transformer-from-scratch](https://github.com/yourname/transformer-from-scratch)

## 2. 最小实现目标

- 先实现 sinusoidal positional encoding
- 把它接到 toy Transformer 的输入表示里
- 观察 shape 与 broadcast 方式

## 3. 实现问题

- position signal 是在 embedding 前后加？
- absolute positional encoding 的实现是否需要单独缓存？
- 后面如果切到 RoPE，接口应怎样保持清晰？

## 4. 当前状态

- sinusoidal encoding: planned
- toy integration: planned
- later comparison hooks: planned
