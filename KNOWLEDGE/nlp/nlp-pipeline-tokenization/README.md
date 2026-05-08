# NLP Pipeline and Tokenization

## 它要解决什么问题

NLP 任务输入是字符串，模型计算的对象是张量。**这两者之间不可能一步跳过去**——必须经过一条管道，每一步突破上一步留下的障碍。

要看懂这条管道，关键不是背 7 个步骤的名字，而是理解 **每一步在突破上一步的什么瓶颈**。背名字考试容易漏一步，懂瓶颈即使忘了某一步的名字也能从瓶颈推回来。

## 朴素直觉为什么不够：管道的每一步都不可省

整条管道：

```
Raw text → Preprocess → Tokenize → Vocab/Index → Representation → Model → Evaluate
```

每一步都在解决**上一步留下的、再也推进不下去的障碍**：

| 上一步留下的问题 | 这一步在解决 |
|---|---|
| 文本噪声、大小写、特殊字符 | **Preprocess** 标准化（lowercase / 去标点 等） |
| 字符串还是连续的，模型不知道哪里是单元 | **Tokenize** 切成离散单元 |
| token 是字符串，不能进数学公式 | **Vocab** 把 token 映射成整数 id |
| 整数 id 之间**没有语义距离**（`id=45` 和 `id=67` 没关系） | **Representation** 把 id 变成向量 |
| 单纯的向量不会预测 | **Model** 学习从向量到标签的映射 |
| 不知道模型好不好 | **Evaluate** 用指标量化 |

中间任何一步跳过，**下一步就无路可走**——这就是管道的强约束。

跑一个具体任务串一遍：判断 `"This movie is not bad!!!"` 的情感。

```
Step 1. Raw text          "This movie is not bad!!!"
        ↓ 计算机不能直接处理字符串
Step 2. Preprocess        "this movie is not bad"
        ↓ 字符串还是字符串,要切开才能数
Step 3. Tokenize          ["this", "movie", "is", "not", "bad"]
        ↓ 字符串无法做数学运算
Step 4. Vocab / Index     [12, 88, 3, 45, 67]
        ↓ 整数 id 没有"距离"概念,5 不比 67 更接近 12
Step 5. Representation    每个 id → embedding 向量
        ↓ 现在每个词都是向量,可以做矩阵运算
Step 6. Model             向量 → logits = [neg_score, pos_score]
        ↓ 输出还需要被检验
Step 7. Evaluate          预测值 vs 真实值 → accuracy / F1
```

## 反事实：为什么"按空格切"不是 universal tokenization

Tokenization 这一步看起来最简单——空格不就是天然的词边界吗？

不对。**空格不是语言学意义上的 word boundary**。这是这条管道里最容易踩坑的位置。

由此推出**三类失败**：

1. **没有空格的语言**：中文、日文（最干净的反例）——空格根本不存在
2. **空格切出错误单元**：
   - `don't` → 藏了否定（`n't` 是 `not`）
   - `#MachineLearning` → 藏了多个语义单元
   - `state-of-the-art` → 变成 OOV
3. **不该按空格切的结构**：URL、email、`3.14km`——内部结构会被破坏

## 为什么 `don't` 被当成单 token 是问题

最容易讲不清楚但最经典的反例。

**模型只认 token id，不会自己拆 token**。一旦 tokenizer 决定 `don't` 是一个 token，模型从那一刻起只会问一个问题："**id = 5847 这个 token 出现时，sentiment 倾向哪边**？"

它**不会去看**这个 token 内部有 `n't`、有 `not`、有否定。对模型来说，`don't` 和 `apple`、`xqzplt` 没有结构上的区别——都是不可分的原子单元。

为什么这是问题？看一个具体场景：

```
"I love this movie"      → positive
"I do not love this"     → negative
"I don't love this"      → ???
```

如果 tokenizer 把 `do` 和 `not` 分开切，那么模型学到 `not` + 任何正面词 ≈ 负面这个规律之后，**看到 `don't love` 时（如果切成 `do` + `n't` + `love`）能迁移这个规律**。

如果 tokenizer 把 `don't` 当一个 token：

- `do not love` 和 `don't love` 在模型眼里是**两个完全无关的输入**
- 模型必须**分别学习**这两种表达——训练数据少的那种就废了
- 更糟：如果 `don't love` 在训练集里只出现 2 次，它几乎就是 OOV

**关键词**：opaque（不透明）、cannot decompose（不能拆解）、share knowledge。否定信息**被锁在了一个 rare token 里**。

## Vocab 和 Representation：两件不同的事

容易混的两步：从 token 到模型输入需要**两步**，不是一步。

```
token "cat"  →  id = 5  →  vector [0.21, -0.45, ..., 0.78]
            (Vocab)        (Representation / Embedding)
```

- **Vocab**：把字符串映射成整数 id。id 只是**词表里的行号 / lookup 地址**，没有语义距离。
- **Representation**：把 id 进一步映射成稠密向量，**这一步才让 id 之间有距离**。

如果跳过 Representation，把 id `[12, 88, 3, 45, 67]` 直接喂给模型，**模型会把这些数字当成"有距离的实数"处理**——但 id 在 `nn.Embedding` 看来只是表里的行号，不是数值。`id=45` 和 `id=67` 在模型眼里和你家门牌号一样纯粹是地址。**结果就是模型学到的关系完全错位**。

## One-hot vs Embedding：根本区别在 dot product

`Representation` 的早期方案是 one-hot：每个词变成一个长度等于词表大小的向量，**只有自己那一位是 1，其他全是 0**。

```
vocab = {cat: 0, dog: 1, run: 2, runs: 3}

cat  = [1, 0, 0, 0]
dog  = [0, 1, 0, 0]
run  = [0, 0, 1, 0]
runs = [0, 0, 0, 1]
```

**致命缺陷**：任意两个不同词的 dot product 都是 0。

```
cat · dog  = 0
cat · run  = 0
run · runs = 0    ← 同源词也是 0
```

含义：**在 one-hot 空间里，"cat 和 dog"（都是动物）和 "cat 和 xqzplt"（毫无关系）一样不相关**。所有不同词的相似度都是 0，模型学不到任何语义结构。

Embedding 是**稠密向量**——把每个词映射到低维连续空间里的一个点，**让语义相似的词在空间里距离近**。

```
embedding 举例 (d=3):
cat  = [0.21, -0.45, 0.78]
dog  = [0.19, -0.41, 0.81]    ← cat 附近
run  = [-0.62, 0.33, 0.05]    ← cat 远处
runs = [-0.59, 0.31, 0.08]    ← run 附近
```

通过训练，相似词的向量自动靠近——这是 one-hot 永远做不到的。

容易混的旁支：one-hot / BOW / TF-IDF 是不同的概念：

- **One-hot**：单词级表示——"我是哪个词"
- **BOW** (Bag of Words)：文档级表示——"这个文档里每个词出现几次"
- **TF-IDF**：文档级表示——"这个词在这个文档里有多重要"

不要混。

## Logits：模型最后一层的原始分数

Pipeline Step 6 的输出叫 **logits**——**未经过 softmax 归一化的原始分数**。

```
模型 → logits → softmax → probabilities → argmax → label

例：
logits        = [2.3, 5.1]           ← 任意实数,可以是负的,可以很大
probabilities = [0.058, 0.942]       ← softmax 后归一化到 [0,1],加起来=1
predicted     = 1 (positive)         ← argmax
```

为什么模型不直接输出标签？

1. 模型输出**必须可微分**——能算梯度才能反向传播。直接输出 "positive" 字符串没法求导。
2. 算 loss 必须有连续值——`CrossEntropyLoss` 要拿这些分数和真实标签比。
3. 要表示 "**有多确信**"——`[2.3, 5.1]` 比 `[4.9, 5.1]` 更确信是 positive。标签丢了这个信息。

**重要工程坑**：PyTorch 的 `nn.CrossEntropyLoss()` **内部已经包含 softmax**——所以模型应输出 logits，**不要自己再做一次 softmax**（详见 `KNOWLEDGE/pytorch/cross-entropy-loss/`）。

## Open Questions

- **跨语言的 tokenization 设计**——中文、日文这种没有空格的语言，业界除了 BPE 还有什么主流方案？jieba 等工具的语言学规则 vs 神经 tokenizer 的对比，这一节点没碰到。
- **token 数量和模型质量**之间的关系是怎样的？vocab 太小（更碎）或太大（OOV 多）都不好——是否有一个理论最优？这条线和 BPE merge 数量、scaling laws 联通。
