# PyTorch Classification Training Loop

## 它要解决什么问题

PyTorch 训练分类模型有一个**最小可运行模板**——按 batch 重复五步。这五步看似简单，但**漏一步、错一步都会让模型表面在跑、实际没学到东西**——而且 bug 不会报错，loss 看起来在动，但训练完发现模型没收敛。

要看懂这个 loop，关键不是背步骤名字，而是**理解每一步在干什么、缺一步会怎样**。

## 朴素直觉为什么不够：五步循环必须按这个顺序

```python
for batch_x, batch_y in train_loader:
    optimizer.zero_grad()              # 1. 清空旧梯度
    logits = model(batch_x)            # 2. forward pass
    loss = loss_fn(logits, batch_y)    # 3. 算 loss
    loss.backward()                    # 4. backward pass(算梯度)
    optimizer.step()                   # 5. 更新参数
```

记忆：**Z F L B S**（Zero / Forward / Loss / Backward / Step）。

每一步在干什么——用类比理解：

| 步 | 类比 | 不做会怎样 |
|---|---|---|
| 1. zero_grad | 上节课的草稿擦掉 | 旧梯度累积，这次方向不对 |
| 2. forward | 学生答题给出答案 | 没答案没法批改 |
| 3. loss | 老师批卷打分（错多少） | 没分数学生不知道错哪 |
| 4. backward | 老师告诉学生**每个知识点错在哪** | 学生不知道改什么 |
| 5. step | 学生根据反馈修正笔记 | 知道错了但没改，下次还错 |

## 反事实：缺每一步分别会怎样

**最常考的 bug**——缺 `optimizer.zero_grad()`。这是 PyTorch 一个**反直觉的设计**：

PyTorch 的 `loss.backward()` 算出的梯度**不是覆盖，而是累加**到之前的梯度上。

举个数字例子。某参数 w：

```
Batch 1:
- 之前的梯度 grad = 0
- backward 算出梯度 = +3
- 累加结果: grad = 0 + 3 = 3
- step 用 grad=3 更新 ✓

Batch 2 (没有 zero_grad):
- 之前的梯度 grad = 3 (上一个 batch 留下的!)
- backward 算出梯度 = +2
- 累加结果: grad = 3 + 2 = 5    ← 错!这个 batch 应该用 2
- step 用 grad=5 更新 ✗

Batch 3:
- grad = 5 + (-1) = 4    ← 错得更离谱
```

**累积下去，梯度方向被历史污染**——模型很难收敛或学到错误方向。

为什么 PyTorch 设计成累加而不是覆盖？**有意设计**——某些场景需要"凑齐多个小 batch 的梯度再一起更新"（gradient accumulation），累加机制让这种用法很容易实现。代价就是：你不主动清零，它就一直累。

| 缺的步骤 | 后果 |
|---|---|
| `optimizer.zero_grad()` | 梯度跨 batch 累加，**方向错** |
| `loss.backward()` | **没有梯度**——optimizer 没东西可用 |
| `optimizer.step()` | 梯度算了**但没用上**——参数不更新 |
| `model.eval()` (推理时) | dropout / BN 还在训练模式，输出不一致 |
| `with torch.no_grad():` (推理时) | 算了不必要的梯度，**浪费内存和时间** |

## 一个关键术语澄清：backward ≠ "整个反向传播"

很多教程笼统把 `backward + step` 都叫 "反向传播"，但精确分工是：

```python
loss.backward()      ← 这个是"反向传播"(backward pass / backpropagation)
                       任务: 从 loss 倒着算出每个参数的梯度

optimizer.step()     ← 这个是"参数更新"(parameter update)
                       任务: 用刚才算出的梯度,按规则更新参数
                       例: w_new = w_old - lr × grad
```

类比：

- `backward()` = 老师批卷子，**算出**每道题错了多少分
- `step()` = 学生根据批改，**修改**自己的笔记

考场答题的精确说法：

- 缺 backward → "没有计算梯度，optimizer 没东西可用"
- 缺 step → "梯度被算出来了，但参数没有被更新"

不要把两者混成 "反向传播没做"——**反向传播只指 backward**。

## batch_x vs batch_y：同一 batch 的两半

容易踩的概念坑：`batch_x` 和 `batch_y` 是**同一 batch 的两半**，**不是训练集 vs 测试集**。

| 名字 | 内容 | 类比 |
|---|---|---|
| `batch_x` | 模型的**输入** | 试卷上的题目 |
| `batch_y` | 这些输入对应的**真实答案** | 答案纸 |

**它们配对出现，描述同一批样本**。

具体例子（情感分类，batch_size=4）：

```
样本 1: "这电影太棒了"           标签: 1 (positive)
样本 2: "无聊,差评"              标签: 0 (negative)
样本 3: "情节一般但演员演技好"    标签: 1 (positive)
样本 4: "完全浪费时间"            标签: 0 (negative)

batch_x = [[token id of 样本 1], ...]    shape: [4, 10]    ← 输入
batch_y = [1, 0, 1, 0]                    shape: [4]        ← 标签
```

**模型看 batch_x 做预测，然后用 batch_y 检验对错**——这就是两者的关系。训练集 / 测试集是另一个层级的概念（数据集的横向切分）。

## Tensor Shape 链：从 token id 到 logits

NLP 分类任务的标准 forward 链：

```
batch_x [batch, seq_len]                  例: [4, 10]
   ↓ embed(每个 id 换成 64 维向量)
[batch, seq_len, embed_dim]               例: [4, 10, 64]
   ↓ x.mean(dim=1)(每句汇总成 1 个向量)
[batch, embed_dim]                        例: [4, 64]
   ↓ Linear(embed_dim, num_classes)
logits [batch, num_classes]               例: [4, 2]
```

**通用规律**：分类任务的 logits shape 永远是 `[batch, num_classes]`。

每一步**只做一件事**：

| 步 | 干了什么 | 维度怎么变 |
|---|---|---|
| embedding | 把每个 id 换成向量 | 多一维 |
| mean(dim=1) | 把序列压成一个 | 少一维 |
| Linear(a→b) | 把最后一维从 a 变成 b | 最后一维换数字 |

**为什么 embedding 后多一维**：原来每个位置装 1 个数字（token id），现在每个位置装一个 64 维向量（64 个数字）——多了一层结构，shape 自然多一维。

## nn.Embedding 的两个硬性要求

```python
embed = nn.Embedding(vocab_size, embedding_dim)
```

**要求 1：输入必须是整数（dtype=torch.long）**

```python
# ❌ 报错: float32
input_ids = torch.tensor([1.0, 2.0, 3.0])

# ✓ 正确
input_ids = torch.tensor([1, 2, 3], dtype=torch.long)
```

**为什么**：Embedding 本质是**查表**——id 是表里的"行号"。行号必须是整数。

**要求 2：id 必须在 `[0, vocab_size)` 范围内**

```python
embed = nn.Embedding(vocab_size=1000, embedding_dim=128)
embed(torch.tensor([5]))      # ✓ 5 < 1000
embed(torch.tensor([1500]))   # ❌ IndexError
```

考场容易出现的坑：词表大小算错、`[PAD]` / `[UNK]` 的 id 没预留。

## 心智模型：Embedding 不是 Linear

```python
# Embedding: 查表
embed = nn.Embedding(vocab_size=1000, embed_dim=128)
# 内部是 [1000, 128] 矩阵
# 输入 id=5 → 直接拿第 5 行的 128 维向量

# Linear: 矩阵乘法
linear = nn.Linear(in_features=128, out_features=64)
# 内部是 [128, 64] 矩阵
# 输入向量 v(128 维) → v @ W(得到 64 维)
```

**Embedding 输入是 id（离散），Linear 输入是向量（连续）**。这俩搞混是常见 bug。

## CrossEntropyLoss + softmax 的关键坑

PyTorch 的 `nn.CrossEntropyLoss()` **内部已经包含 softmax**（实际是 `log_softmax + NLL`）。所以模型应该输出 **logits**，不要自己再做一次 softmax：

```python
# ❌ 错误
logits = self.fc(x)
probs = F.softmax(logits, dim=-1)
loss = nn.CrossEntropyLoss()(probs, labels)   # softmax 了两次, 梯度坏掉

# ✓ 正确
logits = self.fc(x)                 # 直接输出 logits
loss = nn.CrossEntropyLoss()(logits, labels)
```

详见 `KNOWLEDGE/pytorch/cross-entropy-loss/`。

## Open Questions

- **DataLoader 的 `num_workers` / `pin_memory` / `persistent_workers`** 这些工程细节对训练速度的影响很大，但本节点没碰到。这条线和 GPU 利用率、CPU-GPU 数据搬运瓶颈相关。
- **Mixed precision training**（fp16 / bf16）和 gradient scaling——本节点的 loop 假设 fp32，工业训练中混合精度是标准做法。这条线相对独立，待单独节点。
- **Gradient accumulation 模式**：故意不调 zero_grad、累积 N 个 batch 的梯度再 step——用来模拟更大的 batch_size。本节点提到了 PyTorch 的累加设计是为了支持这个，但具体使用模板没展开。
