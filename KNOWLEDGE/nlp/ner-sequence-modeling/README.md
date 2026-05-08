# NER Sequence Modeling

## 它要解决什么问题

NER（Named Entity Recognition）是命名实体识别——给一段文本，**对每个 token 标一个标签**（人名 / 地名 / 组织名 / 其他）：

```
Input:  John works at Microsoft in Seattle
Output: B-PER O    O   B-ORG    O  B-LOC

(BIO 标注: B-=实体开头, I-=实体内部, O=非实体)
```

NER 是 **token-level task**——每个 token 都要输出一个标签。这和 sentence-level 任务（如情感分类，整句一个标签）的根本不同决定了模型选择的考量也不同。

考典型问题：用预训练 LM + 多层 RNN 做 NER，**数据集长度从几个词到几百词都有**——这个网络是不是好选择？如果不是，怎么改进？

## 朴素直觉为什么不够：多层 RNN 是半适合

直觉上 RNN 适合做 NER——它本来就是为变长设计的，并且每一步出一个 hidden state，**天然对应 token-level 标签**。

但**只看"半适合"是不够的**——还要看哪些方面不适合。

**适合的方面**：

- ✓ 可处理变长输入
- ✓ Token-level 输出符合 RNN 的逐步处理结构（每一步出一个标签）

**不适合的方面**：

- ✗ **Vanishing gradient**：几百词长的文本，RNN 的梯度从最后传到最前面会消失，**远处依赖学不到**
- ✗ **只能看一个方向**：普通 RNN 是从左到右；NER 经常需要看右边——`Apple announced a new product` 里的 `Apple`，要看到 `announced` 才能确定是公司而不是水果
- ✗ **顺序计算**：长文本上慢，无法并行
- ✗ Multi-layer 反而可能加剧梯度消失

也就是说：**多层 RNN 不仅没解决根本问题，还放大了某些问题**。

## 正确路径：三层递进的改进方案

### 方案 1：BiLSTM —— 最基本的改进

普通 RNN 只看左边：

```
→→→→→→→→→     单向,只看左
```

BiLSTM 用两个方向的 LSTM：

```
→→→→→→→→→     前向 LSTM 看左
←←←←←←←←←     反向 LSTM 看右
两者拼接 → 每个 token 同时拥有左右上下文
```

两个改进合在一起：

- **LSTM**：用 gates（input / forget / output）缓解梯度消失，能记住更长依赖
- **Bi-direction**：双向上下文，特别适合 NER 这种需要看右边消歧的任务

### 方案 2：BiLSTM-CRF —— 经典 NER 方案

BiLSTM 的输出是**每个 token 独立预测**的标签 logits。但 NER 的标签**之间有依赖关系**——比如：

- `B-PER` 后面可以是 `I-PER` 或 `O`，**但不能是 `I-LOC`**（地点不能在人名之后开始延续）
- `I-` 标签前面**必须有相同实体类型的 B- 或 I-**

如果只让模型独立预测每个 token，可能预测出**不合法的标签序列**——比如 `O B-PER I-LOC O`。

**CRF（Conditional Random Field）层**的作用就是显式建模这种**标签之间的转移概率**：

```
BiLSTM 输出每个 token 的标签 logits
   ↓
CRF (Conditional Random Field) 层
   ↓
最优标签序列(满足转移约束)
```

CRF 用 Viterbi 解码找出**全局最优合法标签序列**，确保输出不违反 BIO 转移约束。

### 方案 3：Transformer / BERT —— 当前最强方案

BERT-based 模型的优势：

- **Self-attention 直接连接任意距离的 token**——完全没有 vanishing gradient
- **天然双向**——一次性看到整个句子
- **并行计算**——长文本处理快
- **预训练已经学到通用语言理解**——只需 fine-tune

实现方式：用预训练 BERT，在每个 token 的输出向量上接一个分类头，预测 BIO 标签。

NER 任务上 BERT-based 模型基本是 **SOTA**。

## 实践细节：变长输入的工程处理

数据集从几个词到几百词都有，**必须 padding + attention mask**（详见 `KNOWLEDGE/nlp/padding-and-attention-mask/`）：

- 短句补 `[PAD]` 到 batch 最长长度
- attention_mask 告诉模型哪些位置是真 token，哪些是 padding
- **loss 不算 padding 位置**——padding 不应贡献错误的训练信号

## 反事实：BERT subword tokenization 的标签对齐问题

容易踩的高级坑：BERT 用 WordPiece tokenization，**一个词可能被切成多个 subword**：

```
Washington → Wash + ##ington
```

但 NER 的标注是**词级别**的——`Washington` 整体标 `B-LOC`，被切开后变成两个 subword。**标签该怎么对齐**？

两种主流方案：

- **只在 word 的第一个 subword 上算 loss**——其它 subword 标 `[ignore]`，loss 不参与
- **所有 subword 重复标签**——`Wash` 和 `##ington` 都标 `B-LOC`（或者 `B-LOC` + `I-LOC`）

两种方案各有 trade-off，但**都比"忘记对齐"好得多**——后者会直接让 loss 对应错位置。

## 为什么这道题考的是模型选择能力

把这道题从答题角度看，**它不是在问 "RNN 是不是不好"**，而是在问 "**你能不能根据任务特性（token-level、变长、长距离依赖）系统性地分析模型适合度，并给出递进的改进方案**"。

最优的答题结构：

1. **指出 NER 是 token-level**——这是任务特性，决定后续讨论
2. **指出多层 RNN 的三个具体问题**——vanishing gradient / 单向 / 顺序计算
3. **给三个递进方案**：BiLSTM → BiLSTM-CRF → BERT
4. **加分点**：padding + attention mask、subword 标签对齐

## Open Questions

- **CRF 解码算法（Viterbi）**的具体推导——动态规划在标签序列上的最优解搜索。这是经典算法但和当前 BERT-based NER 的关系是什么？现在还需要 CRF 吗？
- BERT 做 NER 时分类头是简单的 `Linear(hidden_dim, num_labels)`——**有没有人在 BERT 上加 CRF 层**？理论上 BERT-CRF 是 BERT-only 的严格更强模型（仍能建模标签转移），但实践里见到的不多——是因为 BERT 已经隐式学到了？
- **subword 标签对齐的两种方案**（first-subword-only vs all-subword）的具体精度差异是多少？什么场景偏好哪个？这条线本节点没展开。
