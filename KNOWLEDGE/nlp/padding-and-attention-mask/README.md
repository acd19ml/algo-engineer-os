# Padding and Attention Mask

## 它要解决什么问题

NLP 输入的天然形态是**变长**——一个 batch 里的句子可能从几个词到几百个词。但 GPU 的并行计算要求 **batch 内所有样本是同一形状的张量**——也就是要求一个规则的矩形 `[batch, seq_len]`。

Padding 和 attention mask 是一对配套机制，用来**调和这两个互相矛盾的事实**：

- **Padding**：把短句补齐到 batch 最长长度——解决形状问题
- **Attention mask**：标记哪些位置是真 token、哪些是补出来的假货——告诉模型忽略后者

两者**必须配套**——只 padding 不传 mask，会出大问题。

## 朴素直觉为什么不够：padding 解决一个问题，引入另一个

为什么需要 padding？看一个具体 batch：

```
sample 1: "I love NLP"            (3 个 token)
sample 2: "This movie is great"   (4 个 token)
sample 3: "Hello"                  (1 个 token)
```

**长度不同**——直接堆不成规则的 `[batch, seq_len]` tensor。

最简单的解决方案是**用占位符 `[PAD]` 把短句补齐**到最长句子的长度：

```
sample 1: ["I", "love", "NLP", [PAD]]
sample 2: ["This", "movie", "is", "great"]
sample 3: ["Hello", [PAD], [PAD], [PAD]]
```

现在 shape 统一：`[3, 4]`。形状问题解决了。

**但引入了新问题**：`[PAD]` 不是真实语义输入。如果模型把它和真 token 一样对待，所有依赖序列内容的计算都会被污染：

- self-attention：可能把注意力给到 padding 位置
- pooling：mean pooling 会把 padding 的 0 向量平均进去，**稀释句子表示**
- token-level loss（如 NER）：padding 位置不应该有标签，**不该贡献 loss**

## 反事实：不传 attention_mask 会发生什么

`attention_mask` 通常形状是 `[batch, seq_len]`——**1 表示真 token，0 表示 padding**：

```
sample 1: ["I", "love", "NLP", [PAD]]
mask:     [1,    1,     1,     0   ]
```

模型在处理每个位置时**先看 mask**，对 0 的位置做特殊处理。

如果不传 mask，会发生：

**Self-attention 被污染**。Transformer 的 attention 在每个位置生成一个对所有位置的 softmax 权重分布。如果不告诉模型 padding 位置是假的，那 padding 位置会**正常参与 softmax**——一些 attention 权重会"漏"到 padding 上，真 token 之间的权重被稀释。

工程上的标准做法：**把 padding 位置的 attention score 设成一个很大的负数**（如 `-1e9`），过 softmax 后权重接近 0。这要求模型知道哪些位置是 padding——也就是必须传 mask。

**Mean pooling 被稀释**。

```
没 mask:  pooled = (v1 + v2 + v3 + v_pad) / 4
                                          ↑
                                          padding 的 0 向量被平均进去
```

正确做法是**mask 加权平均**：

```
有 mask:  pooled = (v1 + v2 + v3) / 3    （只算真 token 的平均）
```

不传 mask，第 4 个位置的 padding 向量会**稀释整个句子表示**——句子越短被稀释越严重。

**Token-level 任务（NER）**：每个位置有一个标签，loss 是 token-level cross-entropy。padding 位置**不应该有标签**——loss 应该跳过它们。如果不传 mask，padding 位置会贡献错误的 loss 信号，污染训练。

**调用 BERT 必须传 mask**：

```python
outputs = model(input_ids=input_ids, attention_mask=attention_mask)
```

漏掉 attention_mask，BERT **不能区分真 token 和 padding**——上面所有问题都会出现。

## Padding mask vs Causal mask 的区别

容易混的另一种 mask：causal mask（自回归 mask）。两者都用 0/1 标记位置，但目的完全不同：

| | 标记什么 | 形状 | 何时用 |
|---|---|---|---|
| **Padding mask** | 哪些位置是真 token 哪些是 padding | `[batch, seq_len]` | 任何变长 batch（BERT、NER、分类） |
| **Causal mask** | 当前位置只能看到之前的位置 | `[seq_len, seq_len]`（下三角） | 自回归生成（GPT 训练 / 推理） |

两种 mask 在 GPT 训练时**同时使用**——padding mask 告诉它哪些位置是 PAD（不参与 attention），causal mask 告诉它每个位置只能看左边。

容易踩的坑：把两个 mask 形状搞混（`[batch, seq_len]` vs `[seq_len, seq_len]`）或者只用一个就以为够了。

## 实践：变长输入的标准处理流程

NER 上有非常长的样本（几百词）和短样本（几个词）混杂在一起：

1. **Tokenize**：每个样本切成 token id 列表，长度不同
2. **Padding**：补到 batch 最长长度（通常用 `[PAD]` 的 id，常约定为 0）
3. **生成 attention_mask**：对每个样本，真 token 位置是 1，padding 位置是 0
4. **传入模型**：`model(input_ids, attention_mask=mask)`
5. **计算 loss 时再用一次 mask**：token-level loss 只在 mask=1 的位置算

## Open Questions

- **BERT 的 `[CLS]` 和 `[SEP]` 这类特殊 token 在 mask 里通常算 1**——也就是它们参与 attention。但 `[CLS]` 的 attention 模式和真 token 很不一样（被设计成"全局摘要"位置）。**这些特殊 token 的 mask 处理是否需要更细粒度的区分**？这一节点没展开。
- **变长 padding 的对齐方式**：left-padding vs right-padding。GPT 推理时的 KV cache 通常假设 left-padding（即 padding 放在前面），而 BERT 训练通常 right-padding。混用会出错——这条线和 generation API 的接口设计相关，本节点没碰到。
- **WordPiece 切分后 NER 标签怎么对齐**？比如 `Washington → Wash + ##ington`，原本一个标签 `B-LOC` 现在要怎么分配给两个 subword？这是 NER 上的标准工程坑，详见 `KNOWLEDGE/nlp/ner-sequence-modeling/`。
