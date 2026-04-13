# Math Notes for Transformer

## Scope
本目录用于记录 Transformer 的关键数学结构、符号定义、复杂度理解和推导疑问。

## 1. Core components to formalize
需要逐步写清：

- scaled dot-product attention
- multi-head attention
- positional information injection
- feed-forward network
- residual connection + normalization
- encoder / decoder structure differences

## 2. Key formulas to revisit
### Scaled dot-product attention
需要整理：
- Q, K, V 的定义
- attention score 的计算
- 为什么要除以 sqrt(d_k)

### Multi-head attention
需要整理：
- 为什么拆多个 head
- head 的拼接与线性映射
- 多头带来的表示优势是什么

## 3. Complexity notes
需要理解：
- self-attention 的时间复杂度
- self-attention 的空间复杂度
- 为什么长序列下成本高
- 为什么这会引出后续 long-context 和 sparse attention 路线

## 4. Current questions
- “并行性更强”在数学和计算图层面具体体现在哪里？
- 为什么多头比单头更有表达力，这件事应该怎样直观解释？
- 原论文里的 encoder-decoder attention 在现代 LLM 学习路径中应占多大权重？

## 5. Next steps
- 先补 attention 基础公式
- 再补 Transformer block 的整体结构图
- 再补复杂度分析
