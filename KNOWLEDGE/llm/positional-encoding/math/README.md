# Positional Encoding 数学笔记

## Scope

本目录用于记录位置编码的基础公式、直觉和后续扩展问题。

## 1. First target

优先写清原始 Transformer 中的 sinusoidal positional encoding：

- 为什么用正弦 / 余弦
- 为什么不同维度用不同频率
- 这种设计想保留什么性质

## 2. Questions to formalize

- 位置编码到底是在补什么信息？
- 为什么 attention 本身不足以表达顺序？
- absolute encoding 和 relative encoding 的核心差别是什么？

## 3. Next steps

- 先把原始公式写清
- 再补几组小维度可视化直觉
- 最后为后续 RoPE 路线留接口
