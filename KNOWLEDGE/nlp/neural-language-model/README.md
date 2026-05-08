# Neural Language Model

## 它要解决什么问题

Language model（LM）的目标是 **给一个 token 序列分配概率，或等价地预测下一个 token**。最朴素的实现是 count-based n-gram——直接数语料里出现的次数。但 n-gram 有三大根本局限（详见 `KNOWLEDGE/nlp/bpe-tokenization/` 的 OOV 讨论思路）：

- **Sparsity**：很多合理的 n-gram 在训练语料里出现 0 次 → count = 0、概率 = 0
- **No generalization**：n-gram 只看完全匹配，不理解 `cat` 和 `dog` 都是动物、行为类似
- **Long-range dependency 抓不到**：Markov 假设只看前 n-1 个词

Neural LM 的核心思想：**不再查表，而是学一个从上下文到下一词分布的函数**——通过 embedding 把相似词的向量拉近，让相似上下文得到相似的概率分布。

## 朴素直觉为什么不够：从 count 到 neural 的根本转变

| | Count-based | Neural |
|---|---|---|
| 知识存在哪 | count table（查表） | 神经网络的参数（可学习） |
| 没见过的组合怎么办 | 概率 = 0（失效） | 仍能给出合理概率（泛化） |
| 词义相似怎么处理 | 完全做不到 | embedding 自动学到 |

最关键的转变：**把"知识 = 计数"换成 "知识 = 学到的参数"**——参数可以泛化、可以表达词义相似性，是查表做不到的。

## Four-gram Neural LM 的结构：本质是一个多分类器

任务：用前 3 个词预测第 4 个词。

```
(w_{t-3}, w_{t-2}, w_{t-1})  →  w_t
```

整个模型本质就是一个**多分类器**——类别数 = vocab_size。

模型流程：

```
Input: 前 3 个词的 id            shape: [3]
   ↓ nn.Embedding 查表
Embedding output                  shape: [3, 64]
   ↓ flatten (拼成 1 个长向量)
Flattened                         shape: [192]
   ↓ Linear + ReLU
Hidden                            shape: [128]
   ↓ Linear (映射到 vocab_size)
Output logits                     shape: [10000]
   ↓ log_softmax (可选)
Log probabilities                 shape: [10000]
```

## 反事实：为什么用 flatten 而不是 mean pooling

情感分类（参见 `KNOWLEDGE/pytorch/classification-training-loop/`）用的是 `mean(dim=1)` 把序列汇总成一个向量。Neural LM 用的是 **flatten**——把多个向量**拼接**成一个长向量。

为什么不同？

- **情感分类**：不在乎"谁是第一个词、谁是第二个词"，只要整句的"平均特征"——用 mean pooling，**顺序无关**
- **Neural LM**：**非常在乎顺序**——`"I am taking"` 和 `"taking am I"` 完全不同的下一词分布。需要保留每个位置的信息——用 flatten **把(位置, 词)都展开放在一个长向量里**

flatten 的几何直觉：

```
embed 输出 [3, 64]:
[
  [v1_1, v1_2, ..., v1_64],     ← 第 1 个词的 64 维向量
  [v2_1, v2_2, ..., v2_64],     ← 第 2 个词的 64 维向量
  [v3_1, v3_2, ..., v3_64]      ← 第 3 个词的 64 维向量
]

flatten 后 [192]:
[v1_1, ..., v1_64, v2_1, ..., v2_64, v3_1, ..., v3_64]
 ←─── 第 1 个词 ───→ ←─── 第 2 个词 ───→ ←─── 第 3 个词 ───→
```

3 行 × 64 列变成 1 行 × 192——所有数字按顺序排成一长串。**位置信息通过"在长向量中的位置"保留下来**——后续 Linear 层可以学出"第 1 个词的第 17 维"和"第 3 个词的第 17 维"应该如何不同地影响输出。

## PyTorch 实现：逐行解读

```python
class LanguageModeler(nn.Module):
    def __init__(self, vocab_size, embedding_dim, context_size, hidden_size=128):
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.linear1 = nn.Linear(context_size * embedding_dim, hidden_size)
        self.linear2 = nn.Linear(hidden_size, vocab_size)

    def forward(self, inputs):
        embeds = self.embeddings(inputs).view((1, -1))     # ← 关键
        out = F.relu(self.linear1(embeds))
        out = self.linear2(out)
        log_probs = F.log_softmax(out, dim=1)
        return log_probs
```

`self.embeddings(inputs)` 是查表，把 `[3]` 形状的 id 序列变成 `[3, 64]` 形状的向量序列。

`.view((1, -1))` 是 reshape：

- 第 0 维固定为 1
- 第 1 维 `-1` 表示**自动计算**（让总元素数不变）

`[3, 64]` 共 192 个元素 → `[1, 192]`。这就是 **flatten 的实现**。

> 为什么前面要加个 1？因为 `nn.Linear` 的输入要求是 `[batch, features]`——必须有 batch 维度。这里假设 batch=1，所以加 1 上去。

## 反事实：`view((1, -1))` 只对 batch=1 安全

容易踩的坑：上面这种写法**只对 batch_size=1 的输入成立**。如果想 batch training：

```python
# inputs shape: [batch, context_size]
# embeds shape after lookup: [batch, context_size, embed_dim]

# ❌ 错:强行 view (1, -1) 会把 batch 全混在一起
embeds.view((1, -1))

# ✓ 对:保持 batch 维度
embeds.view(embeds.size(0), -1)   # [batch, context_size × embed_dim]
# 或
embeds.reshape(embeds.size(0), -1)
```

考场如果让你改代码支持 batch，**就是改这一行**。

## Loss 函数选择：取决于模型输出什么

PyTorch 提供两种损失函数，**选哪个取决于模型最后一层是 raw logits 还是 log_softmax 之后**：

| 模型输出 | 用什么 Loss | 关系 |
|---|---|---|
| **raw logits** | `nn.CrossEntropyLoss` | CE = log_softmax + NLL（内部已合并） |
| **log_softmax 后** | `nn.NLLLoss` | NLL 只做最后一步 |

两条路殊途同归，数学上完全等价——**但不能混用**：

- ❌ logits + NLLLoss → 错（NLL 不会做 log_softmax）
- ❌ log_probs + CrossEntropyLoss → 等于做了**两次** log_softmax，梯度坏掉

上面那段 `LanguageModeler` 输出 `log_probs`，所以应该用 `NLLLoss`。详见 `KNOWLEDGE/pytorch/cross-entropy-loss/`。

## Training Loop：和情感分类几乎一样

```python
for context, target in training_data:
    # context: 前 3 个词,target: 第 4 个词
    context_idxs = torch.tensor(
        [word_to_ix[w] for w in context], dtype=torch.long
    )
    target_idx = torch.tensor([word_to_ix[target]], dtype=torch.long)

    optimizer.zero_grad()                    # Z
    log_probs = model(context_idxs)          # F
    loss = loss_function(log_probs, target_idx)  # L
    loss.backward()                          # B
    optimizer.step()                         # S
```

**核心机制完全和情感分类相同**（详见 `KNOWLEDGE/pytorch/classification-training-loop/`），只是参数变了：

| Module 1 情感分类 | Module 2 Neural LM |
|---|---|
| 输入：整句 token id | 输入：前 3 个词 id |
| 输出：`[batch, 2]` (neg/pos) | 输出：`[1, vocab_size]` |
| 类别数 = 2 | 类别数 = vocab_size（可能上万） |
| pooling 用 mean | pooling 用 flatten |

## 训练样本生成：滑动窗口

> **句子有 T 个 token，four-gram LM 能生成 T - 3 个训练样本。**

例：

```
Tokens (T=12): I, am, taking, CS6493, this, semester, and, studying, NLP, is, really, fascinating

Training examples (T-3 = 9 个):
(I, am, taking)             → CS6493
(am, taking, CS6493)        → this
(taking, CS6493, this)      → semester
... (滑动窗口往右移 1 位)
(NLP, is, really)           → fascinating
```

通用公式：n-gram 在长度 T 的句子里能提取 **T - (n-1)** 个样本。

## Embedding Dimension 的 trade-off

`embedding_dim` 的选择是**三方权衡**：

| Dim | Capacity | Cost | Generalization |
|---|---|---|---|
| 32 | 低，可能 underfit | 小，训练快 | 小数据下稳，但表达有限 |
| 64 | 中等 | 中等 | 小型作业的常见平衡 |
| 128 | 高，更 expressive | 大，训练慢 | 数据少时可能 overfit |

三个核心 trade-off：

1. **Capacity**：dim 越大，每个词能装的语义信息越多
2. **Cost**：dim 越大，参数越多（`vocab_size × dim`），训练更慢、占内存多
3. **Overfitting risk**：dim 越大，训练数据少时越容易过拟合

最佳选择应基于 **validation 性能 + vocab 大小 + 语料大小 + 任务复杂度**——没有 universal best。

## Open Questions

- **N-gram neural LM 的固定窗口**是这个范式的根本局限——再大的 n 都解决不了真正的长距离依赖。RNN 解决了变长输入但有梯度消失问题。Transformer 用 self-attention 直接连接任意位置——这条演进线本节点未展开，但为什么 RNN 也走完了它的历史使命这一点值得单独节点处理。
- **Smoothing**（如 Laplace、Kneser-Ney）是 count-based n-gram 缓解 sparsity 的工程手段——它和 neural LM 的"自动泛化"在精神上是不同路线，但 smoothing 能不能从 neural LM 的角度被理解？这个对比本节点未触及。
- **BLEU、Perplexity** 这些 LM 评价指标的具体含义和差别没有展开——尤其 perplexity 的直觉（"模型平均在多少候选之间犹豫"）和 cross entropy 的关系。详见 `KNOWLEDGE/pytorch/cross-entropy-loss/`，但这条线还需要单独节点。
