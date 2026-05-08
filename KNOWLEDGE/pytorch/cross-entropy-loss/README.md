# Cross Entropy Loss

## 它要解决什么问题

分类模型最后一层输出 logits（原始打分），但训练需要一个**可微分的 loss**——告诉模型"预测错了多少"。

PyTorch 提供了一组互相纠缠的工具：`logits`、`softmax`、`log_softmax`、`NLLLoss`、`CrossEntropyLoss`。它们之间的**正确组合**是高频踩坑点——用错组合的代码看起来能跑，但**梯度坏掉**，模型悄悄学不到东西。

要避坑，得搞清楚：

- 每个东西**输入是什么、输出是什么**
- 哪两组工具**等价**、哪两组**不能混用**

## 五个工具：先把每一个的角色钉死

### Logits

**定义**：模型最后一层输出的**原始类别分数**——还没经过 softmax。

```
logits = [2.3, 5.1]
         ↑    ↑
         neg  pos
```

性质：

- 范围 `(-∞, +∞)`——任意实数，可以是负的，可以很大
- **不要求和为 1**

为什么模型不直接输出概率或标签？

1. 输出**必须可微分**——能算梯度才能反向传播。直接输出 "positive" 字符串没法求导
2. 算 loss 必须有**连续值**——CrossEntropyLoss 要拿这些分数和真实标签比
3. 要表示 "**有多确信**"——`[2.3, 5.1]` 比 `[4.9, 5.1]` 更确信是 positive。标签丢了这个信息

### Softmax

把 logits **变成概率分布**：

```
softmax(x_i) = exp(x_i) / Σ exp(x_j)
                    ↑           ↑
                第 i 个值     所有值的 e^x 总和
```

例：`softmax([2.0, 1.0, 0.1])`：

```
Step 1: exp(2.0)=7.389, exp(1.0)=2.718, exp(0.1)=1.105
Step 2: sum = 7.389 + 2.718 + 1.105 = 11.212
Step 3: 各除以 sum → [0.659, 0.242, 0.099]
```

性质：

- 输出 ∈ (0, 1)，加起来 = 1 → 可以解释为概率分布
- **单调**：logit 大的，概率也大
- **平移不变**：`softmax([x+c, y+c]) = softmax([x, y])`（实现里用来防溢出）

为什么用 `e^x` 而不是其他正函数？两个原因：

1. **保证非负**：概率不能负数，`e^x` 恒为正
2. **拉大差距**：`logits=[2, 3]` 看起来差不多，但 `exp([2,3]) = [7.4, 20.1]`，差距被放大近 3 倍

### Log_softmax

`log(softmax(x))`——softmax 后取 log 的**数值稳定合并版**。

为什么单独有这个？因为 softmax 之后再取 log 在数值上容易**下溢**（softmax 输出接近 0 时，log 接近 -∞）。`log_softmax` 内部用对数变换合并这两步，数值更稳。

输出范围 `(-∞, 0]`——log 概率，不是概率。

### NLLLoss

**Negative Log-Likelihood Loss**。期望输入是 **log probabilities**。

直觉：取真实标签对应那个类的 log 概率，**取负数**：

```
target = 1
input = [log_p_0, log_p_1, log_p_2]
loss = -input[1] = -log_p_1
```

它**不做 softmax，也不取 log**——只是简单的 "取对应位置 + 取负"。

### CrossEntropyLoss

期望输入是 **raw logits**——内部包含 `log_softmax + NLL`：

```
CrossEntropyLoss(logits, target) = NLLLoss(log_softmax(logits), target)
```

也就是说：CrossEntropyLoss = log_softmax + NLLLoss 一起做完。

## 反事实：错误组合分别会怎样

PyTorch 提供两条**等价**路径：

| 模型输出什么 | 用什么 Loss | 数学上等价吗 |
|---|---|---|
| **raw logits** | `nn.CrossEntropyLoss` | ✓ 推荐 |
| **log_softmax 之后** | `nn.NLLLoss` | ✓ 推荐 |

**两条路殊途同归，但不能混用**：

### 错误组合 1：softmax 后再喂 CrossEntropyLoss

```python
# ❌ 错
logits = self.fc(x)
probs = F.softmax(logits, dim=-1)
loss = nn.CrossEntropyLoss()(probs, labels)
```

`CrossEntropyLoss` 内部还会再做一次 log_softmax——等于做了 **softmax 两次**，梯度会**坏掉**。

更糟的是这种 bug **不会报错**——loss 看起来在动，模型表面在训练，但**梯度信号是错的**，收敛差或学不动。这是期末代码题里反复出现的 bug。

**正确**：

```python
# ✓ 对
logits = self.fc(x)
loss = nn.CrossEntropyLoss()(logits, labels)
```

### 错误组合 2：logits 直接喂 NLLLoss

```python
# ❌ 错
logits = self.fc(x)
loss = nn.NLLLoss()(logits, labels)
```

`NLLLoss` **不做 softmax 也不取 log**——它假设输入已经是 log 概率。直接喂 raw logits，相当于把任意实数当成 log 概率处理——**完全错位**。

### 错误组合 3：probabilities 喂 NLLLoss

```python
# ❌ 错
logits = self.fc(x)
probs = F.softmax(logits, dim=-1)
loss = nn.NLLLoss()(probs, labels)
```

`NLLLoss` 期望 log 概率，喂 probability（不带 log）——少了一步取 log，**整个量级都错了**。

## 正确组合记忆口诀

> **CE 吃 logits，NLL 吃 log_softmax**——两条路要选一条走到底。

或者更简单的做法：**默认用 CrossEntropyLoss，模型直接输出 logits**——不要手动加 softmax 或 log_softmax。这是最不容易出错的方案。

## Cross Entropy 的几何意义

数学上：

```
CE(p, q) = -Σ p_i · log(q_i)
```

- `p` 是真实分布
- `q` 是模型预测分布

意义：**真实分布 p 加权下，模型分布 q 的"对数惊讶度"**。

在分类任务里，`p` 通常是 **one-hot** —— 真实标签那一项是 1、其他全是 0。代入：

```
CE = -log(q[true_label])
```

也就是 **`-log(模型给真实标签的概率)`**——只剩下"模型对正确答案给了多大概率"那一项的贡献。

具体性质：

```
概率 q[true]      -log(q)
1.0(完美预测)    0           ← loss 最小
0.99              0.01
0.5               0.69
0.1               2.30
0.01              4.61
0.0001            9.21        ← loss 巨大
```

性质很自然：

- 模型对正确答案给的概率越接近 1，loss 越接近 0
- 模型对正确答案给的概率越接近 0，loss 越接近无穷大

这正是 "loss" 该有的行为：**预测对了不罚，预测错了狠罚**。

## 一个具体计算例子

3 分类中 `q = [0.2, 0.7, 0.1]`，真实标签是类别 0：

```
CE = -log(q[0]) = -log(0.2) ≈ 1.609
```

如果模型给类 0 的概率从 0.2 提到 0.9：

```
CE = -log(0.9) ≈ 0.105
```

**模型 self-correction 的方向：让真实类别的概率变大，CE 自然下降**——这就是训练在做的事。

## Perplexity：cross entropy 的指数

在语言模型里常用的评价指标：

```
perplexity = exp(cross entropy)
```

直觉解读：**模型平均在多少个候选之间犹豫**。

- 完美预测（CE=0）→ perplexity = 1（"零犹豫"）
- 词表大小 V 的纯随机预测 → CE = log(V)，perplexity = V（"在 V 个候选里随便猜"）

所以 perplexity 越接近 1 越好。LM 评价中，**比较两个模型用 perplexity 比直接看 CE 直觉**——它直接对应 "犹豫程度"。

## Open Questions

- **Label smoothing**：把 one-hot 真实分布软化（比如 `[0.9, 0.05, 0.05]` 而不是 `[1, 0, 0]`），让 CE 不要把过多的概率推给单一类。这是常见正则化技巧但本节点未展开。
- **多标签分类（multi-label）** 用的是 `BCEWithLogitsLoss`（每个标签独立 sigmoid + BCE），不是 CrossEntropyLoss。两者形式很像但**不是同一个东西**——一个标签可以多类、一个标签必须互斥。这条线本节点未展开。
- 为什么 `log_softmax + NLL` 这条路在数值上比 `softmax 后再 log` 更稳？这涉及到 log-sum-exp trick 的具体细节——本节点提到了概念但没展开数值推导。
