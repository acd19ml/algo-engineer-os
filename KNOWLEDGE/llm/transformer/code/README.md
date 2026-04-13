# Transformer 代码笔记

## Scope
本目录用于记录 Transformer 的实现思路、外部代码仓库、工程拆解方式和实现疑问。

## 1. External repos
- [transformer-from-scratch](https://github.com/yourname/transformer-from-scratch)
- [Project page](../../../../PROJECTS/research/attention-is-all-you-need-reading-and-reproduction/README.md)

## 2. Implementation goals
计划分三步，先跑通最小闭环：

### Step 1
实现最小版 scaled dot-product attention

### Step 2
实现单层 Transformer block
包括：
- multi-head attention
- FFN
- residual
- normalization

### Step 3
实现一个最小可运行的 toy Transformer
重点不是训练出强模型，而是理解张量流动和模块接口

## 3. Implementation questions
- 先用 PyTorch 直接写，还是先用 NumPy 写一个更透明的版本？
- 要不要把 positional encoding 单独模块化？
- decoder mask 最好在第一版就实现，还是后面再补？

## 4. Engineering notes
实现时要特别关注：
- tensor shape 变化
- mask 的位置和广播方式
- head 拆分与拼接
- residual 和 normalization 的位置

## 5. Current status
- toy attention: planned
- single block: planned
- full toy transformer: planned
