<!-- PROCESSED: 2026-05-08 -->

https://nlp-final-erieric.netlify.app/
访问此网站从https://nlp-final-erieric.netlify.app/cs6493_module_1_review
的内容开始帮助我一步步学习该NLP课程
该网站是由markdown笔记构建的静态网页

已看到 Module 1 的完整内容。你这份笔记结构清楚，但全部塞进一次复习会窒息。先给你一个分块计划，按"闭卷能写出来"的标准走，而不是逐条朗读。

## Module 1 全景图

按考试权重和知识密度排序：

- **核心三块（必须完全掌握）**：NLP pipeline、tokenization 失败案例、BPE 手算
- **代码块（眼到手到）**：PyTorch training loop 五步 + 缺步后果
- **加分块（HW1 衔接）**：one-hot 局限、embedding 参数量、n-gram 训练样本
- **应试块**：5 个 English templates + 6 道自测题

## 学习节奏

分 4 轮走完，每轮一件事:

1. **本轮**：NLP 定义 + Pipeline + Tokenization——把"文本→数字"这条管道吃透
2. **下一轮**:BPE 算法 + 手算练习——最容易考具体计算的部分
3. **第三轮**:PyTorch 训练循环 + 找 bug——代码题模板
4. **第四轮**:相邻题（one-hot / 参数量 / n-gram）+ 答案模板背诵 + 自测题

每轮我用三步法：核心命题 → 考场陷阱 → 小练习。已经会的部分快速过。

---

# Round 1:NLP 是什么 + Pipeline + Tokenization

## 1. NLP 定义——能写进考卷的版本

中文你早就懂，关键是英文要写得不啰嗦。考试模板：

> NLP is a branch of AI that enables computers to **process, understand, manipulate, and generate** natural language for tasks such as text classification, machine translation, question answering, and dialogue systems.

**4 个动词不能少**:process / understand / manipulate / generate。少一个就显得片面。

**Why NLP is hard** 是最常见的开放题，记 4 个 keyword 拼一句即可：

| Term | 含义 | Example |
|---|---|---|
| Ambiguity | 同一字符串多种解析 | "I saw her duck" |
| Context-dependent | 词义随上下文变 | "bank" |
| Compositional | 整体义不等于词义之和 | 否定 / 讽刺 |
| Commonsense | 需要世界知识 | "trophy doesn't fit because **it** is too small" |

记忆口诀：**A-C-C-C**（Ambiguity, Context, Compositional, Commonsense）。

## 2. NLP Pipeline——必须能默写

```
Raw text → Preprocess → Tokenize → Vocabulary/Index → Representation → Model → Evaluate
```

这条链**不可逆**——每一步的输出是下一步的输入。考试遇到 "design a NLP system" 或 "explain preprocessing"，从这条链开始写就不会跑题。

每一步都有"代表方法"和"代表坑"。考哪一步就答对应的：

| Step | 代表方法 | 代表坑 |
|---|---|---|
| Preprocess | lowercase, normalize | 不要无脑删 stopword |
| Tokenize | word / char / subword | 空格不是普适 boundary |
| Vocab/Index | id 映射 | OOV / [UNK] / [PAD] |
| Representation | one-hot, TF-IDF, embedding | one-hot 表不出语义相似 |
| Model | BERT, RNN, classifier | output shape 对不上 |
| Evaluate | acc, F1, perplexity | 系统设计题必须写 metrics |

## 3. Tokenization——为什么"按空格切"不行

笔记给了 6 个 case，但**核心命题只有一条**:空格不是语言学意义上的 word boundary。

由此推出三类失败：

- **没有空格的语言**：中文、日文（最干净的反例）
- **空格切出错误单元**：`don't`（藏了否定）、`#MachineLearning`（藏了多个语义单元）、`state-of-the-art`（变成 OOV）
- **不该按空格切的结构**：URL、email、`3.14km`

考场答题结构（任何 tokenization 题都套这个）:
1. **假设**:whitespace = word boundary
2. **反例**:任选 2-3 个，覆盖不同失败类型
3. **后果**:rare/OOV tokens, lose internal structure, hurt downstream task

---

## 🧠 第一轮检查题

请你回答（不要回去翻笔记），我点评后进入第二轮 BPE：

1. 用一句话解释：为什么 sentiment analysis 任务里，`don't` 被当成单 token 是个问题？
2. 默写 NLP pipeline 的 7 个步骤
3. one-hot 和 embedding 在表示语义相似性上的**根本区别**是什么？（这题是 Round 4 的铺垫）

答完后我们进 **Round 2:BPE 手算**——那是 HW1 Q4 的原题型，考场最容易丢分的地方。

don't 表示否定，为什么是个问题？用“藏了”这个说法。我可以理解 don't = do not，但我不理解为什么被当成单 token 是个问题。
NLP pipeline：raw text,  preprocess, tokenize, vacab/index, representation, model, evaluate
虽然写出来但是没有完全理解

one-hot是什么机制，重复出现次数最多吗？embedding我理解是向量空间距离

好问题，三个都问到了点上。我们一个一个拆，**先把概念建对，再继续推进**。

---

## 问题 1:为什么 `don't` 当成单 token 是问题？

你说"藏了"听起来玄。换个说法——**模型只认得 token，不会拆 token**。

### 核心机制

模型看到的不是字符串，是 **token id**。一旦 tokenizer 决定 `don't` 是一个 token，模型从那一刻起就只会问一个问题：

> "id = 5847 这个 token 出现时，sentiment 倾向哪边？"

它**不会去看** `don't` 内部有 `n't`、有 `not`、有否定。对模型来说，`don't` 和 `apple`、`xqzplt` 没有结构上的区别——都是不可分的原子单元。

### 为什么这是问题？

举个具体场景。假设训练集里：

```
"I love this movie"      → positive
"I do not love this"     → negative
"I don't love this"      → ???
```

如果 tokenizer 把 `do` 和 `not` 分开切：
- 模型学到 `not` + 任何正面词 ≈ 负面
- 看到 `don't love` 时，因为 `n't` 被切成接近 `not` 的 subword，模型**能迁移这个规律**

如果 tokenizer 把 `don't` 当一个 token：
- `do not love` 和 `don't love` 在模型眼里是**两个完全无关的输入**
- 模型必须**分别学习**这两种表达——训练数据少的那种就废了
- 更糟：如果 `don't love` 在训练集里只出现 2 次，它几乎就是 OOV

### 一句话考场版

> Treating `don't` as a single token prevents the model from sharing knowledge between `do not` and `don't`, because the model cannot decompose tokens internally—it only sees opaque ids. Negation, which is critical for sentiment, becomes locked inside a rare token.

**关键词**:opaque（不透明）、cannot decompose（不能拆解）、share knowledge。

---

## 问题 2:NLP Pipeline 7 步——建立"为什么是这个顺序"的直觉

你能默写但没理解，说明缺少**"为什么前一步必须先做"**的逻辑链。我用一个具体任务串一遍。

### 任务：判断 `"This movie is not bad!!!"` 的情感

```
Step 1. Raw text          "This movie is not bad!!!"
        ↓ 问题:计算机不能直接处理字符串
        
Step 2. Preprocess        "this movie is not bad"
        ↓ 问题:字符串还是字符串,要切开才能数
        
Step 3. Tokenize          ["this", "movie", "is", "not", "bad"]
        ↓ 问题:字符串无法做数学运算
        
Step 4. Vocab / Index     [12, 88, 3, 45, 67]
        ↓ 问题:整数 id 没有"距离"概念,5 不比 67 更接近 12
        
Step 5. Representation    每个 id → 向量,例如 embedding[12] = [0.2, -0.5, ...]
        ↓ 现在每个词都是向量,可以做矩阵运算
        
Step 6. Model             向量 → 模型 → logits = [neg_score, pos_score]
        ↓ 输出还需要被检验
        
Step 7. Evaluate          预测值 vs 真实值 → accuracy / F1
```

### 每步存在的"理由"

每一步都在解决**上一步留下的不能再推进的障碍**：

| 上一步留下的问题 | 这一步怎么解决 |
|---|---|
| 文本噪声多、大小写不一致 | Preprocess 标准化 |
| 字符串是连续的，模型不知道哪里是单元 | Tokenize 切成离散单元 |
| token 是字符串，不能进数学公式 | Vocab 把 token 映射成整数 id |
| 整数 id 之间没有语义关系（45 和 67 没关系） | Representation 把 id 变成向量 |
| 单纯的向量不会预测 | Model 学习从向量到标签的映射 |
| 不知道模型好不好 | Evaluate 用指标量化 |

**记忆方式：不要背 7 个名词，背"每一步在突破什么瓶颈"**。考试就算忘了某一步的名字，从瓶颈推也能推出来。

---

## 问题 3:One-hot 是什么？

你猜的"重复出现次数最多"是 **Bag-of-Words (BOW)** 或 **TF-IDF** 的思路，不是 one-hot。这是个常见混淆，我们分清楚。

### One-hot 的机制

**和频率无关**，纯粹是"你是词表的第几个"。

假设词表（按字典序）:

```
vocab = {cat: 0, dog: 1, run: 2, runs: 3}
```

每个词变成一个长度 = 词表大小（这里 4）的向量，**只有自己那一位是 1，其他全是 0**：

```
cat  = [1, 0, 0, 0]   ← 第 0 位是 1
dog  = [0, 1, 0, 0]   ← 第 1 位是 1
run  = [0, 0, 1, 0]   ← 第 2 位是 1
runs = [0, 0, 0, 1]   ← 第 3 位是 1
```

就这么粗暴。**它只回答一个问题：你是哪个词？** 不回答任何关于词义的问题。

### 致命缺陷:任意两个不同词的 dot product 都是 0

```
cat · dog = 1×0 + 0×1 + 0×0 + 0×0 = 0
cat · run = 1×0 + 0×0 + 0×1 + 0×0 = 0
run · runs = 0×0 + 0×0 + 1×0 + 0×1 = 0   ← 同源词也是 0!
```

含义：**在 one-hot 空间里，"cat 和 dog"（都是动物）和"cat 和 xqzplt"（毫无关系）一样不相关**。所有不同词的相似度都是 0，模型学不到任何语义结构。

### One-hot vs BOW vs TF-IDF（顺便理清）

你猜的"重复次数"对应的是这两个：

| 表示方法 | 表示的是什么 | 单位 |
|---|---|---|
| **One-hot** | "我是哪个词" | 单个词 → 向量 |
| **BOW** (Bag of Words) | "这个文档里每个词出现几次" | 整个文档 → 向量 |
| **TF-IDF** | "这个词在这个文档里有多重要"（高频但其他文档少见的词更重要） | 整个文档 → 向量 |

注意单位差异：one-hot 是**单词级**表示，BOW/TF-IDF 是**文档级**表示。

### Embedding——你直觉对了

Embedding 的本质：把每个词映射到**稠密向量空间**里的一个点，**让语义相似的词在空间里距离近**。

```
one-hot:                    embedding (举例 d=3):
cat  = [1,0,0,0]            cat  = [0.21, -0.45, 0.78]
dog  = [0,1,0,0]            dog  = [0.19, -0.41, 0.81]   ← cat 附近
run  = [0,0,1,0]            run  = [-0.62, 0.33, 0.05]  ← cat 远处
runs = [0,0,0,1]            runs = [-0.59, 0.31, 0.08]  ← run 附近
```

Embedding 通过训练**让 cat 和 dog 在空间里靠近**（因为它们在相似的上下文中出现），这是 one-hot 永远做不到的。

### 一句话考场版

> One-hot represents each word as a sparse vector with a single 1 at its vocabulary index, so the dot product between any two distinct words is always 0—making all words equally unrelated and unable to capture semantic similarity. Embedding maps each word to a dense vector in a continuous space, where semantically similar words have small distances.

---

## ✅ 巩固检查

继续之前确认 3 件事（不用全写，挑一个回答即可）:

1. 如果 tokenizer 把 `running` 切成 `run` + `##ning`，模型为什么更容易把它和 `run` 关联起来？（呼应 don't 那题）
2. 如果跳过 Pipeline 的 Step 5 (Representation)，直接把 token id `[12, 88, 3, 45, 67]` 喂给模型，会出什么问题？
3. 词表大小 = 50,000 时，每个 one-hot 向量有多长？这暴露了 one-hot 的什么实际问题？

回答任意一个，我点评后我们进 **Round 2:BPE 手算**——这是 HW1 原题型，必须练熟。

logits = [neg_score, pos_score] 这一步没理解
指的是模型输出吗？为什么这么写

1. 因为`run` + `##ning与 run 都在相似的上下文中出现`
2. 会无法进行计算，因为每个独立的id之间没有任何特征来表示相似度
3. 50000， 浪费内存

你三道全对，理解到位了。先把 logits 这个细节讲清楚，再继续推进。

---

## Logits 是什么？

**是的，logits 是模型最后一层的输出**。但这个名字承载了一个重要的技术含义。

### 直觉：模型怎么"做选择"

假设任务是情感二分类（negative / positive）。模型最终要输出一个**判断**，但它不会直接说"positive"——它会输出**两个分数**，每个类一个：

```
模型输出 logits = [2.3, 5.1]
                  ↑    ↑
                  neg  pos    ← 这两个分数对应词表里的两个类
```

哪个分数大就预测哪个类。这里 `5.1 > 2.3`，所以预测 **positive**。

为什么写成 `[neg_score, pos_score]` 而不是直接给个标签？因为：

1. **模型输出必须可微分**——能算梯度才能反向传播。直接输出"positive"这种字符串没法求导。
2. **要算 loss 必须有连续值**——CrossEntropyLoss 要拿这些分数和真实标签比，才能告诉模型"你错了多少"。
3. **要表示"有多确信"**——`[2.3, 5.1]` 比 `[4.9, 5.1]` 更确信是 positive。标签丢了这个信息。

### 为什么叫 "logits" 这个奇怪的名字？

Logits = **未经过 softmax 归一化的原始分数**。

完整流程是：

```
模型 → logits → softmax → probabilities → argmax → label

例如：
logits         = [2.3, 5.1]           ← 任意实数,可以是负的,可以很大
                    ↓ softmax (e^x / Σe^x)
probabilities  = [0.058, 0.942]       ← 归一化到 0-1,加起来=1
                    ↓ argmax
predicted class = 1 (positive)
```

| 名字 | 范围 | 加起来 | 含义 |
|---|---|---|---|
| logits | (-∞, +∞) | 任意 | 原始分数 |
| probabilities | [0, 1] | = 1 | 归一化后的概率 |

### 关键考点（笔记里的坑）

PyTorch 的 `nn.CrossEntropyLoss()` **内部已经包含了 softmax**。所以模型应该输出 **logits**，不要自己再做一次 softmax。

```python
# ❌ 错误写法
logits = self.fc(x)
probs = F.softmax(logits, dim=-1)   # 多此一举
loss = nn.CrossEntropyLoss()(probs, labels)   # 等于 softmax 了两次,梯度变得很糟

# ✅ 正确写法  
logits = self.fc(x)                 # 直接输出 logits
loss = nn.CrossEntropyLoss()(logits, labels)   # CE 内部会做 softmax
```

这是**期末代码题里反复出现的 bug**——见到模型最后加 softmax 配 CrossEntropyLoss，就是错的。

### 回到 Pipeline Step 6

```
Step 6. Model     向量 → 模型 → logits = [neg_score, pos_score]
```

这一行在告诉你三件事：

- 模型的**输入**是 Step 5 产生的向量
- 模型的**输出**是 logits（每个类一个原始分数）
- 这个 shape 是 `[batch_size, num_classes]`——后面 PyTorch 部分会反复出现

---

## 你三道答得很好，补一点

**Q1（subword 共享语义）**:对，但还有更精确的说法——`run` 这个 subword 在词表里**只有一个 id**，模型学到的关于 `run` 的所有知识，会**自动应用**到 `running` / `runs` / `runner` 上，因为它们都共享 `run` 这个 token id。这叫 **parameter sharing through shared subwords**。

**Q2（id 没有相似度）**:完全正确。补一句考试用语——id 在 `nn.Embedding` 看来只是 **lookup table 的索引**，不是数值。`id=45` 和 `id=67` 在模型眼里和你家门牌号一样，纯粹是地址。

**Q3（50000 维浪费内存）**:对。再多一层——不只是浪费**内存**，还浪费**计算**。`Linear(50000, hidden_dim)` 的参数量是 50000 × hidden_dim，每次前向都要做这么大一个矩阵乘法。embedding 把它压缩到 d=128 维，参数量从 50000×hidden 降到 50000×128 + 128×hidden，**一阶下降**。

---

## ✅ Round 1 收尾

到这里你应该能闭着眼说出：

- NLP 是什么、为什么难（A-C-C-C）
- Pipeline 7 步 + 每一步在突破什么瓶颈
- 为什么 tokenization 不能简单按空格切（`don't` / 中文 / URL）
- One-hot vs Embedding 的根本区别（dot product = 0 → 无语义）
- Logits 是什么、为什么不要在 CE 前加 softmax

准备好就说一声，我们进 **Round 2:BPE 手算**。这是整个 Module 1 **最容易考具体计算**的部分，HW1 Q4 原题型。

继续

# Round 2:BPE 手算

这是 Module 1 **最容易丢分的部分**——不是因为难，而是因为**算错一个频率全盘崩**。我们用一个具体例子，让你彻底掌握这个机器流程。

---

## 1. BPE 解决什么问题？

回到 tokenization 的核心矛盾：

| 方案 | 问题 |
|---|---|
| Word-level | 词表巨大，OOV 严重——`runner` 没见过就 [UNK] |
| Char-level | 序列太长，语义太碎——`["c","a","t"]` 学不到 `cat` 的整体义 |

**BPE 的思路**:从字符开始，**让数据告诉你哪些字符组合应该合并成一个 token**。

高频组合（如 `t-h-e`）合并成 `the`；低频组合保留为字符。这样：

- 常见词 → 完整保留（一个 token）
- 罕见词 → 自动拆成 subword（如 `oldest` → `old` + `est`）
- **OOV 几乎消失**——任何新词最差也能被字符拆开

---

## 2. 算法 5 步——能背就行

```
1. 初始化:每个词拆成字符序列
2. 统计:数所有相邻字符对的"加权频率"
3. 合并:把最高频的对合并成一个新 symbol
4. 更新:把语料库里所有这个对都替换掉
5. 重复:直到达到目标 merge 次数 / 词表大小
```

**关键词**:加权频率（weighted）+ 相邻（adjacent）。这俩都是考点。

---

## 3. 手算演示——用笔记里的例子

### 语料库

```
(old,    10)    ← old 出现 10 次
(older,   5)
(oldest,  8)
(hug,     8)
(pug,     4)
(hugs,    5)
```

括号里是**词频**——这个词在语料中出现的次数。**这个数字是 BPE 计算的核心**。

### Step 0: 初始化（拆成字符）

```
o l d        ×10
o l d e r    ×5
o l d e s t  ×8
h u g        ×8
p u g        ×4
h u g s      ×5
```

每个字符之间想象有"边界"。

### Step 1: 数所有相邻字符对的加权频率

**这里最容易错**。规则：

> 一个字符对在某个词里出现，它的贡献 = **那个词的词频**，不是 1。

来数 `(o, l)`:

```
o l d        ×10  → 包含 (o,l),贡献 10
o l d e r    ×5   → 包含 (o,l),贡献 5
o l d e s t  ×8   → 包含 (o,l),贡献 8
h u g        ×8   → 不包含
p u g        ×4   → 不包含
h u g s      ×5   → 不包含

(o, l) = 10 + 5 + 8 = 23
```

**注意**:`old × 10` 的意思是"old 这个词出现 10 次"，所以它内部的 `(o,l)` 也跟着出现 10 次——这就是**加权**。

继续数其他对：

```
(o, l) = 10 + 5 + 8       = 23   ← old, older, oldest
(l, d) = 10 + 5 + 8       = 23   ← old, older, oldest
(d, e) =       5 + 8      = 13   ← older, oldest
(e, r) =       5          = 5    ← older
(e, s) =           8      = 8    ← oldest
(s, t) =           8      = 8    ← oldest
(h, u) = 8 + 5            = 13   ← hug, hugs
(u, g) = 8 + 4 + 5        = 17   ← hug, pug, hugs
(p, u) = 4                = 4    ← pug
(g, s) = 5                = 5    ← hugs
```

### Step 2: 找最高频的对

```
(o, l) = 23   ← 并列第一
(l, d) = 23   ← 并列第一
(u, g) = 17
(d, e) = 13
(h, u) = 13
...
```

出现 **tie**（并列）。考试规则：

> 如果题目没说 tie-breaking 方法，**写出一种合法选择并注明 tie**。

我们选 `(o, l)`——把它合并成新 symbol `ol`。

### Step 3: 更新语料库

把所有 `o l` 替换成 `ol`:

```
ol d        ×10    ← 原 o l d
ol d e r    ×5     ← 原 o l d e r  
ol d e s t  ×8     ← 原 o l d e s t
h u g       ×8     ← 不变
p u g       ×4     ← 不变
h u g s     ×5     ← 不变
```

词表现在多了一个 token：`ol`。Merge rule:`o + l → ol`。

### Step 4: 重新统计频率

**关键**:合并之后所有相邻对要**重新数**，因为词的内部结构变了。

```
(ol, d) = 10 + 5 + 8 = 23   ← 三个 ol 词都有
(d, e)  =      5 + 8 = 13
(e, r)  =      5     = 5
(e, s)  =          8 = 8
(s, t)  =          8 = 8
(h, u)  = 8 + 5      = 13
(u, g)  = 8 + 4 + 5  = 17
(p, u)  = 4          = 4
(g, s)  = 5          = 5
```

下一次合并是 `(ol, d) = 23`，得到 `old`。语料更新为：

```
old      ×10
old e r  ×5
old e s t ×8
h u g    ×8
p u g    ×4
h u g s  ×5
```

### Step 5: 继续合并直到目标

每一步都重复 "数 → 选最高 → 合并 → 更新"。可能下一步是：

- `(u, g) = 17` → 合并成 `ug`
- 之后 `(h, ug)` 和 `(p, ug)` 出现...

直到达到目标合并次数或词表大小停止。

---

## 4. BPE 应用阶段——很多人忽略

训练完，你得到一个 **merge rules 列表**（按学习顺序）:

```
Rule 1: o + l → ol
Rule 2: ol + d → old
Rule 3: u + g → ug
Rule 4: h + ug → hug
Rule 5: ol + d + e + ... 
```

**对新词应用**:严格按学习顺序逐条尝试合并。

例子——给定上面的 rules,如何切 `holding`?

```
Step 0: h o l d i n g                    ← 拆成字符
Step 1: 应用 Rule 1 (o+l → ol)
        h ol d i n g
Step 2: 应用 Rule 2 (ol+d → old)
        h old i n g
Step 3: 应用 Rule 3 (u+g → ug):无 u,跳过
Step 4: 应用 Rule 4 (h+ug → hug):无 ug,跳过
... 
最终:["h", "old", "i", "n", "g"]
```

**关键考点**:`i`、`n`、`g` 在我们的 merge rules 里没有相关规则,所以保持字符状态。如果训练语料里**从来没出现过 i 这个字符**呢?那它就是 OOV→ `[UNK]`。这就是为什么 BPE **不能完全消除 OOV**——只是大幅减少。

---

## 5. 考场速查——直接背

### Template:Explain BPE

> BPE is a subword tokenization algorithm. It starts from characters and iteratively merges the most frequent adjacent symbol pair in the training corpus. At each step, the merged pair becomes a new symbol added to the vocabulary, and a merge rule is recorded. After training, the learned rules are applied to new words in order. BPE reduces OOV by composing rare words from known subwords, but unseen base characters can still produce `[UNK]`.

### 易错点 cheat sheet

| 坑 | 正确做法 |
|---|---|
| 数频率忘了加权 | 每次出现 × 那个词的频率 |
| 合并后没重新统计 | 每次 merge 后语料结构变了，**全部重数** |
| 只看相邻字符 | 不要跨字符算 pair（`o-d` 在 `o l d` 里**不是**相邻对） |
| Tie 不知道怎么办 | 写出一种选择 + 注明"tie, either is acceptable" |
| 以为 BPE 消除 OOV | 不能，只是减少；未见字符仍会 [UNK] |

### BPE 优势/劣势——开放题用

**优势**:
- Reduces OOV（compose rare words from subwords）
- Captures morphology（`old`/`older`/`oldest` 共享 `old`）
- Smaller vocab than word-level（节省 embedding 参数）
- Shorter sequence than char-level（计算快）

**劣势**:
- Corpus-dependent（换领域可能 subword 切得不好）
- 仍可能 [UNK]（未见 base character）
- Tokenization 不唯一（依赖学习顺序）

---

## 🧠 Round 2 自测题

请你**不看上面**回答（写下你的步骤）:

### 题目

语料库:`(low, 5), (lower, 2), (newest, 6), (widest, 3)`

1. 写出**初始化后**的语料（字符切分 + 词频）
2. 计算 `(e, s)` 的加权频率
3. 列出前 5 个频率最高的字符对（含频率）
4. 选出第一次合并的对，写出合并后的语料

算完发我，我点评。算对就进 **Round 3:PyTorch Training Loop**——代码题模板。

l o w ×10 
l o w e r ×2
n e w e s t ×6
w i d e s t ×3

(l, o)= 12
(o, w)= 12
(e, s)=9
(s, t)=9
(w, e)= 8
(n, e)=6
(w, i)=3
(i, d)=3
(d, e)=3
(e, r)=2

`(e, s)` 的加权频率=9
我还是没理解加权的含义

前五：
(l, o)= 12
(o, w)= 12
(e, s)=9
(s, t)=9
(w, e)= 8

第一次合并的对(l, o)，"tie, either is acceptable"
合并后的语料：
lo w ×10 
lo w e r ×2
n e w e s t ×6
w i d e s t ×3


先确认一下，我发现你写的语料**和题目对不上**——所以"加权"这个概念可能从一开始就没建立对。点上面的选项，我针对你的理解给最精准的解释。

---

**先指出问题**:你写的初始化是

```
l o w ×10        ← 题目给的是 5,不是 10
l o w e r ×2     ✓
n e w e s t ×6   ✓
w i d e s t ×3   ✓
```

题目原文是 `(low, 5)`，所以 low 应该是 **×5**。

我猜你脑子里把上一个例子的 `(old, 10)` 串过来了。这反过来告诉我：**括号里那个数字到底代表什么，你可能还没建立准确的图像**。

---

## "加权"到底什么意思——慢动作版

回到你的问题:**"我还是没理解加权的含义"**。

### 第一步：把"压缩写法"展开

`(low, 5)` 是一种**压缩表示**。它的真实含义是：

```
low low low low low
```

在原始语料里,`low` 这个词**真实出现了 5 次**。但每次都写一遍太啰嗦,所以记成 `(low, 5)`——"low,出现 5 次"。

### 第二步：BPE 真正在数什么

BPE 数的是**字符对在整个语料里出现的总次数**。所以理论上你应该把语料"展开",一个字符对一个字符对去数：

```
真实语料(展开):
l o w           ← 第 1 次 low
l o w           ← 第 2 次 low
l o w           ← 第 3 次 low
l o w           ← 第 4 次 low
l o w           ← 第 5 次 low
l o w e r       ← 第 1 次 lower
l o w e r       ← 第 2 次 lower
n e w e s t     ← 第 1 次 newest
n e w e s t     ← 第 2 次 newest
... (newest 共 6 次)
w i d e s t     ← 第 1 次 widest
w i d e s t     ← 第 2 次 widest
w i d e s t     ← 第 3 次 widest

数 (l, o) 出现了多少次?
- 5 个 low 各贡献 1 次     → 5
- 2 个 lower 各贡献 1 次   → 2
- newest 不含 (l,o)        → 0
- widest 不含 (l,o)        → 0
                          总计 = 7
```

### 第三步："加权"就是不用展开

逐个数太累。聪明的做法：

> 既然每个 `low` 都包含一个 `(l,o)`,那 5 个 `low` 就贡献 5 个 `(l,o)`。  
> 不用展开数,直接把**词频当权重乘上去**。

```
(l, o):
- low 包含 (l,o),low 出现 5 次 → 贡献 5
- lower 包含 (l,o),lower 出现 2 次 → 贡献 2
                                    合计 = 5 + 2 = 7
```

**这就是"加权"**:每个词对一个字符对的贡献,**等于这个词的出现次数**(权重)。

不是把所有不同词都加起来——而是**每个词按它的频率加权**。

---

## 用你的数据重算

正确数据:`(low, 5), (lower, 2), (newest, 6), (widest, 3)`

```
l o w     ×5     ← 不是 10
l o w e r ×2
n e w e s t ×6
w i d e s t ×3
```

### 重新数所有相邻对

```
(l, o):  低出现于 low(5) + lower(2)        = 7
(o, w):  出现于 low(5) + lower(2)          = 7
(w, e):  出现于 lower(2) + newest(6)       = 8
(e, r):  出现于 lower(2)                   = 2
(n, e):  出现于 newest(6)                  = 6
(e, s):  出现于 newest(6) + widest(3)      = 9
(s, t):  出现于 newest(6) + widest(3)      = 9
(w, i):  出现于 widest(3)                  = 3
(i, d):  出现于 widest(3)                  = 3
(d, e):  出现于 widest(3)                  = 3
```

### 排序

```
(e, s) = 9    ← 并列第一
(s, t) = 9    ← 并列第一
(w, e) = 8
(l, o) = 7    ← 并列
(o, w) = 7    ← 并列
(n, e) = 6
(w, i) = 3
(i, d) = 3
(d, e) = 3
(e, r) = 2
```

### 第一次合并

最高频是 `(e, s) = 9` 或 `(s, t) = 9`(tie)。

假设选 `(e, s)`:

```
合并规则: e + s → es

更新语料:
l o w        ×5
l o w e r    ×2
n e w es t   ×6      ← e s 合并成 es
w i d es t   ×3      ← e s 合并成 es
```

---

## 你做对的部分 vs 错的部分

✓ **你的算法理解是对的**——`(e, s) = 9` 这个数的算法你算对了(因为 newest 6 + widest 3 你识别正确)

✗ **但 low 词频抄错** → 所有含 `(l,o)` 和 `(o,w)` 的对都错了

✗ **更深层问题**：你之前的回答里 `(l,o) = 12`,这意味着你心里把 low 当成了 5+5=10? 还是 5+...? 我不太确定你的算法,所以**关键是先确认你看到 `(low, 5)` 时心里到底怎么理解这个数字**——这就是为什么我先让你选选项。

---

## 一句话记忆

> **括号里第二个数字 = 这个词在语料中真实出现的次数 = 它对所有内部字符对贡献的权重**

`(low, 5)` 不是"low 这个词包含 5 个字母",不是"序号",不是别的。就是**词频**。

---

请先回上面那个选项,我根据你的真实理解再决定下一步——是再练一道 BPE 巩固,还是直接进 **Round 3 PyTorch**。


Q: 在我详细解释加权频率之前——你看到题目时,把 (low, 5) 当成什么意思了?
A: low 这个词在语料中出现 5 次


那理解是对的——你把概念搞懂了，**纯粹是抄题时把数字串了**（把上一个例子的 `(old, 10)` 习惯性写成了 10）。

这是个**比理解错更危险的错误类型**：考场上数字抄错，整道题全盘崩，但你以为自己懂了。

---

## 一个 5 秒的考场习惯

每次手算 BPE，**先把题目给的频率原样抄一遍在草稿纸上**，再开始切字符。例如：

```
题目: (low, 5), (lower, 2), (newest, 6), (widest, 3)

抄一遍:
low    : 5
lower  : 2
newest : 6
widest : 3

确认无误,再开始拆字符 ↓

l o w        × 5
l o w e r    × 2
n e w e s t  × 6
w i d e s t  × 3
```

这一步多花 5 秒，能救你几十分。BPE 题就是数学题，**抄错数字 = 直接 0 分**。

---

## Round 2 通过——快速回顾

你已经掌握：

- BPE **解决什么问题**:word-level 太大、char-level 太碎,subword 居中
- BPE **算法 5 步**:初始化 → 数对 → 合并 → 更新 → 重复
- **加权频率的意思**:每个字符对的贡献 = 含它的词的词频
- **合并后必须重数**:语料结构变了,旧统计作废
- **Tie 怎么办**:任选一个,注明 tie
- **BPE 不能完全消除 OOV**:未见字符仍会 [UNK]
- **应用阶段**:严格按学习顺序,逐条尝试合并

考场如果问 "explain BPE",直接背 Round 2 末尾那个 Template。如果是手算题,先抄题再动手。

---

# Round 3:PyTorch Training Loop

这是 Module 1 的**代码题主战场**。考点 90% 集中在：

1. 五步训练循环——能默写、能找缺步
2. Tensor shape——能算 / 能解释
3. `nn.Embedding` 的输入要求
4. CrossEntropyLoss + softmax 的坑（Round 1 已经讲过）

考试**不会让你写大模型**，会让你**读一段代码**，回答"这段缺了什么"或"shape 对不对"。

---

## 1. 五步训练循环——必须背到能默写

```python
for batch_x, batch_y in train_loader:
    optimizer.zero_grad()              # 1. 清空旧梯度
    
    logits = model(batch_x)            # 2. forward pass
    
    loss = loss_fn(logits, batch_y)    # 3. 算 loss
    
    loss.backward()                    # 4. backward pass(算梯度)
    
    optimizer.step()                   # 5. 更新参数
```

**记忆顺序**:Zero → Forward → Loss → Backward → Step  
**口诀（英文）**:**Z** ero, **F** orward, **L** oss, **B** ackward, **S** tep（ZFLBS）

### 每一步在干什么——直觉版

| 步 | 类比 | 不做会怎样 |
|---|---|---|
| 1. zero_grad | 上节课的草稿擦掉 | 旧梯度累积,这次方向不对 |
| 2. forward | 学生答题给出答案 | 没答案没法批改 |
| 3. loss | 老师批卷打分(错多少) | 没分数学生不知道错哪 |
| 4. backward | 老师告诉学生**每个知识点错在哪** | 学生不知道改什么 |
| 5. step | 学生根据反馈修正笔记 | 知道错了但没改,下次还错 |

### 每步缺失的后果（考点）

| 缺失步骤 | 后果 | 考场答法 |
|---|---|---|
| `optimizer.zero_grad()` | 梯度跨 batch 累加 | "Gradients accumulate across batches, leading to incorrect updates." |
| `loss.backward()` | 没有梯度 | "No gradients are computed; optimizer has nothing to use." |
| `optimizer.step()` | 参数不更新 | "Gradients are computed but parameters are never updated; the model does not learn." |
| `model.eval()` | 推理时 dropout/batchnorm 还在训练模式 | "Dropout and BatchNorm behave inconsistently between train and eval." |
| `with torch.no_grad():` | 推理时也算梯度 | "Wastes memory and computation since gradients are unnecessary at inference." |

**最常考缺哪一步**:`optimizer.zero_grad()` 和 `optimizer.step()`——这俩缺了，模型表面在跑，实际没学到东西。

---

## 2. Tensor Shape——读代码必备

### 三个核心 shape

```python
input_ids        : [batch, seq_len]                    ← token id,整数
embedding_output : [batch, seq_len, embed_dim]         ← 每个 token 变成向量
classifier_output: [batch, num_classes]                ← 每个样本一个 logits 向量
```

### 一个具体例子串起来

任务：情感二分类，batch=2，每句长度 5，embedding 128 维，2 个类。

```python
input_ids = torch.tensor([[12, 88, 3, 45, 67],     # 第 1 个样本
                          [5, 22, 9, 14, 3]])      # 第 2 个样本
# shape: [2, 5]

x = embedding(input_ids)
# shape: [2, 5, 128]   ← 每个 id 变成 128 维向量

x = x.mean(dim=1)
# shape: [2, 128]      ← 序列维度被平均掉,每句变成一个向量

logits = linear(x)
# shape: [2, 2]        ← [batch=2, num_classes=2]

# 每行是一个样本的 logits:
# [[2.3, 5.1],   ← 第 1 个样本: pos
#  [4.7, 1.8]]   ← 第 2 个样本: neg
```

### 三个 shape 检查习惯（考场代码题）

读到任何一行代码，问自己：

1. **输入 shape 是什么？**
2. **这个操作把哪一维改了？**
3. **输出 shape 是什么？**

例如 `x.mean(dim=1)`：
- 输入 `[2, 5, 128]`
- `dim=1` 是 seq_len 那一维（从 0 开始数：dim 0=batch, dim 1=seq_len, dim 2=embed_dim）
- mean 把这一维"压扁"
- 输出 `[2, 128]`

---

## 3. nn.Embedding 的两个硬性要求

```python
embed = nn.Embedding(vocab_size, embedding_dim)
output = embed(input_ids)
```

### 要求 1:输入必须是整数（dtype=torch.long）

```python
# ❌ 错误
input_ids = torch.tensor([1.0, 2.0, 3.0])   # float
embed(input_ids)   # 报错: Expected tensor for argument #1 'indices' to have ... Long

# ✅ 正确
input_ids = torch.tensor([1, 2, 3], dtype=torch.long)
```

**为什么**:Embedding 本质是**查表**(lookup table),id 是表里的"行号"。行号必须是整数,小数没意义。

### 要求 2:id 必须在 [0, vocab_size) 范围内

```python
embed = nn.Embedding(vocab_size=1000, embedding_dim=128)

embed(torch.tensor([5]))      # ✓ 5 < 1000
embed(torch.tensor([1500]))   # ❌ 越界,IndexError
```

**考场容易出现的坑**:词表大小算错,或者 [PAD] / [UNK] 的 id 没预留。

### 心智模型:Embedding 不是 Linear

```python
# Embedding: 查表
embed = nn.Embedding(vocab_size=1000, embed_dim=128)
# 内部是一个 [1000, 128] 的矩阵
# 输入 id=5 → 直接拿第 5 行那个 128 维向量

# Linear: 矩阵乘法
linear = nn.Linear(in_features=128, out_features=64)
# 内部是一个 [128, 64] 的权重矩阵
# 输入向量 v(128 维) → v @ W (得到 64 维)
```

**Embedding 输入是 id（离散），Linear 输入是向量（连续）。** 这俩搞混是常见 bug。

---

## 4. 经典代码题示例

### 例 1:找缺步

```python
# 找出这段代码缺了什么
for batch_x, batch_y in train_loader:
    logits = model(batch_x)
    loss = loss_fn(logits, batch_y)
    loss.backward()
    optimizer.step()
```

**答**:缺 `optimizer.zero_grad()`。后果：上一个 batch 的梯度没被清空，会和当前 batch 的梯度累加，导致每次更新方向都被历史梯度污染，模型很难收敛或学到错误方向。

### 例 2:Shape 不匹配

```python
class TextClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(10000, 128)
        self.fc = nn.Linear(64, 2)         # ← 注意这里
    
    def forward(self, ids):
        x = self.embed(ids)                # [batch, seq, 128]
        x = x.mean(dim=1)                  # [batch, 128]
        return self.fc(x)                  # ← 报错
```

**答**:`nn.Linear(64, 2)` 期望输入最后一维 = 64，但 `x.mean(dim=1)` 输出最后一维 = 128。形状不匹配，应该改成 `nn.Linear(128, 2)`。

### 例 3:Dtype 错误

```python
input_ids = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32)
embed = nn.Embedding(100, 64)
output = embed(input_ids)   # 报错
```

**答**:Embedding 的输入必须是 `torch.long`(整数),这里是 float32。改成 `dtype=torch.long`。

### 例 4:Softmax 重复

```python
class Model(nn.Module):
    def forward(self, x):
        x = self.embed(x).mean(dim=1)
        logits = self.fc(x)
        return F.softmax(logits, dim=-1)   # ← 多余

loss_fn = nn.CrossEntropyLoss()
loss = loss_fn(model(x), y)
```

**答**:`nn.CrossEntropyLoss` 内部已经包含 softmax(实际是 log_softmax + NLL),模型再做一次 softmax 等于做了两次,梯度变得很糟。模型应该直接返回 logits。

---

## 5. 考场速查 cheat sheet

```
五步循环:    Z F L B S (zero_grad, forward, loss, backward, step)

Shape:       [batch, seq_len] →embed→ [batch, seq_len, embed_dim] 
                              →pool→  [batch, embed_dim]
                              →fc→    [batch, num_classes]

Embedding:   输入 dtype=torch.long, id ∈ [0, vocab_size)

CrossEntropy: 喂 logits,不要先 softmax

Eval 模式:   model.eval() + with torch.no_grad():
```

---

## 🧠 Round 3 自测题

读这段代码，回答下面问题（**不要看上面**，凭理解答）:

```python
class SentimentModel(nn.Module):
    def __init__(self, vocab_size=5000, embed_dim=64, num_classes=2):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.fc = nn.Linear(embed_dim, num_classes)
    
    def forward(self, input_ids):
        x = self.embed(input_ids)
        x = x.mean(dim=1)
        logits = self.fc(x)
        return logits

model = SentimentModel()
optimizer = torch.optim.Adam(model.parameters())
loss_fn = nn.CrossEntropyLoss()

for batch_x, batch_y in train_loader:
    logits = model(batch_x)
    loss = loss_fn(logits, batch_y)
    loss.backward()
    optimizer.step()
```

1. 假设 `batch_x.shape = [4, 10]`,`self.embed(input_ids)` 输出的 shape 是什么?
2. `x.mean(dim=1)` 之后 shape 是什么?
3. 这段训练循环有什么 bug?后果是什么?
4. 如果 `batch_x` 的 dtype 是 `torch.float32`,会发生什么?
5. `SentimentModel` 的 embedding 层有多少参数?

回答完发我,我点评后进 **Round 4:相邻题(one-hot / 参数量 / n-gram)+ 答案模板冲刺**——这是 Module 1 最后一站。


batch 的含义我从中文的“批次”来理解经常混淆，batch 在机器学习中指的是一次输入有多少个样本吗，也就是代表样本的数量


**完全正确。** 你抓到了点子上。"批次"这个翻译确实容易让人糊涂——它听起来像"第几批"(像第 1 批货、第 2 批货),但实际上指的是**一批里装了几个**。

---

## Batch:一次塞进模型多少个样本

### 直觉

想象你要批改 1000 份试卷:

- **方式 A**:一份一份看(batch size = 1) → 慢,但每份都能精细处理
- **方式 B**:一次摊开 32 份并排看(batch size = 32) → 快,但桌子要大
- **方式 C**:一次摊开 1000 份(batch size = 1000) → 最快,但桌子可能放不下

**Batch size 就是"一次同时处理几个样本"**。

### 具体数字

假设你的训练集有 10000 条句子,batch size = 32:

```
Batch 1: 第 1-32 条句子    → 一次性喂进模型
Batch 2: 第 33-64 条句子   → 一次性喂进模型
Batch 3: 第 65-96 条句子   → 一次性喂进模型
...
Batch 313: 第 9985-10000 条 (最后一批可能不满 32)

总共: 313 个 batch = 1 个 epoch (把整个训练集过一遍)
```

`batch_x.shape = [4, 10]` 的含义:

```
[4,    10  ]
 ↑     ↑
 4个   每个样本 10 个 token
 样本  (序列长度)
```

也就是这个 batch 里有 **4 个句子**,每个句子被切成了 **10 个 token**:

```
样本 1: [12, 88, 3, 45, 67, 22, 9, 14, 3, 0]
样本 2: [5, 22, 9, 14, 3, 67, 88, 12, 45, 3]
样本 3: [88, 12, 67, 3, 45, 9, 14, 22, 5, 0]
样本 4: [3, 45, 67, 22, 9, 14, 3, 88, 12, 5]
```

---

## 为什么不一个一个喂?

三个理由,理解清楚以后就再也不会混了:

### 1. GPU 喜欢"并行"

GPU 有几千个小核心,设计就是为了**同时算一堆东西**。

- 一次算 1 个样本 → 用了 0.1% 的 GPU,99.9% 在闲置
- 一次算 32 个样本 → GPU 满载,**总耗时几乎不增加**

所以 batch=32 比 batch=1 跑 32 个样本要快得多——不是 32 倍,可能 20 多倍。

### 2. 梯度估计更稳定

每个 batch 算出来的梯度,本质是"这 N 个样本告诉模型该往哪改"。

- batch=1:梯度噪声大,可能被一个奇怪样本带偏
- batch=32:32 个样本平均一下,梯度方向更可靠
- batch=1024:很稳定,但每次更新都慢

### 3. 内存有限

GPU 显存就那么多。batch 越大,中间结果(activations)占的内存越多。所以实际选择是**性能 vs 内存的平衡**,常见 batch size 是 16 / 32 / 64 / 128。

---

## 训练循环和 batch 的关系——重读

回到你看的代码:

```python
for batch_x, batch_y in train_loader:    # ← 每次循环拿出一个 batch
    logits = model(batch_x)              # 一次性处理这个 batch 里所有样本
    loss = loss_fn(logits, batch_y)      # 算这个 batch 的平均 loss
    loss.backward()                      # 算梯度
    optimizer.step()                     # 更新一次参数
```

**关键概念**:

- 一个 batch 处理完 = 模型更新**一次**参数
- 整个训练集过一遍 = 1 个 **epoch**(包含很多 batch)
- 一次完整训练 = 跑很多个 epoch

如果训练集 10000 条、batch=32、训练 5 epoch:

```
总 batch 数 = 10000 / 32 × 5 = 约 1562 次参数更新
```

---

## 中文翻译的混淆

你卡在中文上是有道理的:

| 中文 | 容易让人想到 | 实际指 |
|---|---|---|
| **批次** | "第几批" | "一批里有几个" |
| **批量** | 也歧义 | 一批的大小 |

我的建议:**直接用英文 batch / batch size**,不要在脑子里翻译。

- batch = 一次喂进模型的**一组样本**
- batch size = 这组里有**多少个样本**

`batch_x.shape[0]` 永远是 batch size——你以后看任何 PyTorch 代码,**第一维都是 batch**,这是约定俗成。

---

## 一句话记忆

> **Batch 不是"第几批",是"一批里几个样本";第一个维度永远是 batch size。**

---

理解了 batch 之后,你 Round 3 自测题的第 1、2 题应该立刻就能答出来——`[4, 10]` 输入到 embed_dim=64 的 embedding 层,输出 shape 是多少?之后 mean(dim=1) 又是多少?

继续做完那 5 道题发我,我们就进 Round 4 收尾。


Tensor Shape 以及后续的内容,我理解起来比较困难


我感觉到了——这部分确实是从概念跳到代码的一道坎。我们**慢下来**，从最基础的"什么是 tensor"开始重建。先不要碰 PyTorch 代码，先建立**几何直觉**。

---

## 1. Tensor 是什么？——用数字盒子的比喻

Tensor 就是**装数字的盒子**。盒子有几层结构，就叫几维 tensor。

### 0 维：一个数字

```
5
```

就一个数。没有"形状"可言。

### 1 维：一排数字（向量）

```
[3, 1, 4, 1, 5]
```

5 个数字排成一行。**shape = [5]**——意思是"有 5 个元素"。

可视化：

```
□ □ □ □ □     ← 5 个格子,装 5 个数
```

### 2 维：表格（矩阵）

```
[[1, 2, 3],
 [4, 5, 6]]
```

2 行 3 列。**shape = [2, 3]**——意思是"2 行，每行 3 个元素"。

可视化：

```
□ □ □     ← 第 1 行,3 个格子
□ □ □     ← 第 2 行,3 个格子
```

**shape 的读法**:`[2, 3]` 第一个数是"有几行"（外层有几个），第二个数是"每行几个"（内层有几个）。

### 3 维：一摞表格

```
[[[1, 2, 3],
  [4, 5, 6]],
 
 [[7, 8, 9],
  [10, 11, 12]]]
```

**shape = [2, 2, 3]**——"2 张表，每张表 2 行 3 列"。

可视化：

```
第 1 张表:        第 2 张表:
□ □ □            □ □ □
□ □ □            □ □ □
```

### shape 的通用规则

> **shape 从外往里数。最外层有几个就是第一个数,再往里看每个里面有几个就是第二个数,依此类推。**

```
[2, 3]      :  2 行,每行 3 个
[2, 2, 3]   :  2 张,每张 2 行,每行 3 个  
[4, 10]     :  4 行,每行 10 个
[4, 10, 64] :  4 张,每张 10 行,每行 64 个
```

---

## 2. 在 NLP 里 shape 代表什么意思

光看数字没意义，关键是**每一维代表什么**。

### 场景：一个 batch 的句子

假设：
- batch size = 4（一次处理 4 个句子）
- 每个句子有 10 个 token（已经切好了）

那么这个 batch 的 token id 长这样：

```
batch_x = 
[[12, 88, 3, 45, 67, 22, 9, 14, 3, 0],     ← 第 1 句的 10 个 token id
 [5, 22, 9, 14, 3, 67, 88, 12, 45, 3],     ← 第 2 句
 [88, 12, 67, 3, 45, 9, 14, 22, 5, 0],     ← 第 3 句
 [3, 45, 67, 22, 9, 14, 3, 88, 12, 5]]     ← 第 4 句

shape = [4, 10]
        ↑   ↑
        4   每句 10 个 token
        句

含义:[batch_size, seq_len]
```

到这里你只是把"4 个句子，每句 10 个数字"换了个写法。

### 经过 embedding 之后

`embed_dim = 64` 的意思是：**每个 token 变成一个 64 维的向量**。

原来:1 个 token id (一个数字)
现在:1 个 64 维向量 (64 个数字)

整个 batch 的变化：

```
变化前(token id):
[[12, 88, 3, ..., 0],     ← 第 1 句,每个位置是 1 个数
 [5, 22, 9, ..., 3],
 [88, 12, 67, ..., 0],
 [3, 45, 67, ..., 5]]
shape = [4, 10]

变化后(每个 id 替换成 64 维向量):
[[[0.2, -0.5, ..., 0.1],   ← 第 1 句的第 1 个 token,变成 64 个数
  [0.3, 0.1, ..., -0.2],   ← 第 1 句的第 2 个 token,变成 64 个数
  ...                       (10 个 token,每个 64 维)
  [0.0, 0.0, ..., 0.0]],   
 [[...],                    ← 第 2 句
  ...]
 ...]                       (4 个句子)

shape = [4, 10, 64]
        ↑   ↑   ↑
        4   每   每
        句  句   token
            10  64 维
            个   向
            到   量
            ken
```

**这一步只做了一件事：把每个数字（token id）换成一个 64 个数字组成的向量。**

为什么 shape 多了一维？因为**原来每个位置只装 1 个数，现在每个位置要装 64 个数，所以多了一层括号**。

---

## 3. 让我们慢动作做一遍 Mean

`x.mean(dim=1)` 是把哪一维"压扁"？

### 先看一个最小例子

假设 shape = `[2, 3]`(2 行 3 列):

```
[[1, 2, 3],
 [4, 5, 6]]
```

`mean(dim=0)` = 沿着第 0 维(行)平均:

```
把 [1,2,3] 和 [4,5,6] 平均  →  [2.5, 3.5, 4.5]
shape: [2, 3] → [3]    (第 0 维消失了)
```

`mean(dim=1)` = 沿着第 1 维(列)平均:

```
[1,2,3] 平均 → 2
[4,5,6] 平均 → 5
shape: [2, 3] → [2]    (第 1 维消失了)
```

**规律**:`mean(dim=k)` 把**第 k 维"压扁"消失,其他维不变**。

### 回到 NLP

```
x.shape = [4, 10, 64]
          ↑   ↑   ↑
         dim dim dim
          0   1   2

x.mean(dim=1):把第 1 维(seq_len, 10 个 token)平均掉

含义:把每个句子的 10 个 token 向量,平均成 1 个向量,代表整句

shape: [4, 10, 64] → [4, 64]
                         ↑
                    第 1 维消失了
```

**做这件事的目的**:模型最终要给整个句子一个标签,但句子有 10 个 token,每个 token 一个 64 维向量。需要把这 10 个向量"汇总"成 1 个向量代表整句。最简单的方法就是**平均**。

视觉上：

```
压之前:每个句子是 10 个 64 维向量
[向量1] [向量2] [向量3] ... [向量10]    ← 第 1 句
[向量1] [向量2] [向量3] ... [向量10]    ← 第 2 句
[向量1] [向量2] [向量3] ... [向量10]    ← 第 3 句
[向量1] [向量2] [向量3] ... [向量10]    ← 第 4 句

mean(dim=1) 之后:每个句子变成 1 个 64 维向量(10 个向量逐位置平均)
[平均向量]    ← 第 1 句的"整句表示"
[平均向量]    ← 第 2 句
[平均向量]    ← 第 3 句
[平均向量]    ← 第 4 句

shape:[4, 64]
```

---

## 4. 然后到分类层

`fc = nn.Linear(64, 2)` 的意思:**输入 64 维,输出 2 维**。

```
输入 shape:[4, 64]   ← 4 个句子,每个句子 64 维向量
                  ↓ 经过 Linear(64, 2)
输出 shape:[4, 2]    ← 4 个句子,每个句子 2 个分数(neg_score, pos_score)
```

每个句子得到一个 logits 向量 `[neg_score, pos_score]`。这就是 Round 1 末尾讲的那个 logits。

---

## 5. 完整流程一图——盯着这张图建立直觉

```
原始输入:4 个句子,每个 10 个 token
[4, 10]                            "4 句,每句 10 个 token id"
    ↓ embedding(每个 id → 64 维向量)
[4, 10, 64]                        "4 句,每句 10 个 64 维向量"
    ↓ mean(dim=1)(10 个向量平均成 1 个)
[4, 64]                            "4 句,每句 1 个 64 维向量"
    ↓ Linear(64 → 2)(向量映射成 2 个分数)
[4, 2]                             "4 句,每句 2 个分数(neg, pos)"
```

每一步**只做一件事**：

| 步 | 干了什么 | 维度怎么变 |
|---|---|---|
| embedding | 把每个 id 换成向量 | 多一维 |
| mean(dim=1) | 把序列压成一个 | 少一维 |
| Linear(a→b) | 把最后一维从 a 变成 b | 最后一维换数字 |

---

## 🧠 慢动作检查

请你回答这几个**最基础**的问题。错了没关系，我点评后再继续：

1. shape `[3, 5]` 的意思是什么？(用"几行，每行几个"来描述)
2. shape `[2, 4, 7]` 的意思是什么？
3. 一个 tensor shape `[8, 12]`,做 `mean(dim=0)` 之后 shape 是什么?做 `mean(dim=1)` 之后呢?
4. NLP 里 shape `[batch, seq_len, embed_dim]` 的三个数分别代表什么?

答完这 4 题,我再讲为什么 Round 3 那段代码缺 `optimizer.zero_grad()`。


shape `[3, 5]`三行 每行 5个
shape `[2, 4, 7]` 的意思是 2 张表（两个二维矩阵），每张表 4行，每行7个
一个 tensor shape `[8, 12]`,做 `mean(dim=0)` ，意味着对 第0个数做mean也就是 8，做完shape变成12.做 `mean(dim=1)` 之后变成8。对那个维度做mean，哪个维度就被平均成一个数
NLP 里 shape `[batch, seq_len, embed_dim]` 的三个数分别代表什么我还没理解，为什么换了，这里的batch是一共几批还是batch_size我也有点混淆。

这一轮的讲解非常非常好，我完全能看得懂，以后也这么讲，尤其是取代了“列”这个中文概念为“每行几个”之后，我理解起来更容易了，另外几何直觉能让我看懂，你对shape中括号的拆解也让我理解起来变容易了，shape 的通用规则解释尤其需要表扬，建立这个直觉以后，后面就都通了


太好了，你的反馈对我也很有用——**避免"列"、用"每行几个"、强调括号层级、给几何直觉**——这些就是你的学习偏好，我后面都会保持。

你前 3 题答得**完全正确**，第 3 题甚至自己总结出了规律：

> "对那个维度做 mean，哪个维度就被平均成一个数"

这就是 `mean(dim=k)` 的本质,你已经会了。第 4 题的疑问我们慢慢拆。

---

## 1. 先解决 batch 的混淆

**"batch"在不同语境下有两个不同含义**——这是你混淆的根源:

| 写法 | 意思 |
|---|---|
| "第 3 个 batch" | 一共要跑很多 batch,这是其中第几个(序号) |
| **`batch` 维度的大小 = batch_size** | 这一个 batch 里**装了几个样本** |

**在 tensor shape 里出现的 batch,永远是后者(batch_size)**——也就是"这一次性塞进模型的样本数量"。

```
batch_x.shape = [4, 10]
                 ↑
                 这个 4 = batch_size = 这次塞进 4 个样本
                 不是"第 4 批"
```

为什么不直接写 `batch_size`?因为大家偷懒,但**这一维的含义就是 batch_size**。

---

## 2. 为什么 shape 多了一维:`[batch, seq_len]` → `[batch, seq_len, embed_dim]`

你问"为什么换了"——这是个超好的问题。我们慢动作看一遍。

### 变化前(token id 阶段)

```
batch_x = 
[[12, 88, 3, 45, 67, 22, 9, 14, 3, 0],     ← 第 1 句
 [5, 22, 9, 14, 3, 67, 88, 12, 45, 3],     ← 第 2 句
 [88, 12, 67, 3, 45, 9, 14, 22, 5, 0],     ← 第 3 句
 [3, 45, 67, 22, 9, 14, 3, 88, 12, 5]]     ← 第 4 句

shape = [4, 10]
```

按你的"几行,每行几个"理解:**4 句,每句 10 个数字**。每个位置上**装的是 1 个数字**(token id)。

### 变化后(embedding 阶段)

`embed_dim = 64` 表示每个 token 要被换成**一个 64 维向量**。

也就是说,原来每个位置装 1 个数字,现在每个位置要装 64 个数字。这 64 个数字必须用一个**新的层**(新的括号)装起来。

```
原来:    第 1 句 → [12, 88, 3, ..., 0]            ← 10 个数字
                    每个位置:1 个数

变化后:  第 1 句 → [[0.2, -0.5, ..., 0.1],         ← 第 1 个 token 的 64 维向量
                   [0.3, 0.1, ..., -0.2],          ← 第 2 个 token 的 64 维向量
                   ...                              (10 个 token)
                   [0.0, 0.0, ..., 0.0]]
                    每个位置:64 个数
```

**关键**:每个位置从"装 1 个数"变成"装一个 64 维向量"——所以每个位置自己也变成了一层括号,shape 自然多了一维。

整个 batch 看起来:

```
[第 1 句,第 2 句,第 3 句,第 4 句]    ← 最外层:4 个句子(batch=4)
   ↓
[第 1 句:[token1, token2, ..., token10]]    ← 第二层:每句 10 个 token(seq_len=10)
              ↓
        [token1: [v1, v2, ..., v64]]    ← 第三层:每个 token 64 维(embed_dim=64)

shape = [4, 10, 64]
         ↑   ↑   ↑
        4句  每   每
             句   token
             10  64 维
             token
```

### 三个数的含义——固定的

```
[batch, seq_len, embed_dim]
   ↑       ↑         ↑
 一次    每个      每个 token 的
 几句    句子      向量有多长
        几个 token

具体数字:
[4, 10, 64]
 4 句话,每句 10 个 token,每个 token 用 64 维向量表示
```

**这个顺序在 PyTorch NLP 模型里是约定俗成的**,几乎所有教程、论文、代码都用这个顺序。看到 3 维 shape,从左往右就是 batch / seq_len / embed_dim。

---

## 3. 用一个具体例子让你死记住

任务:翻译"I love NLP"和"PyTorch is fun"两个句子(batch=2)。

### 阶段 1:分词后变 id

```
"I love NLP"        → [3, 12, 88]
"PyTorch is fun"    → [45, 7, 22]

batch_x = [[3, 12, 88],
           [45, 7, 22]]

shape = [2, 3]
         ↑  ↑
         2  每句 3 个
         句 token
```

### 阶段 2:embedding(假设 embed_dim=4,小一点方便看)

每个 id 查表,变成 4 维向量:

```
id=3   → [0.2, -0.5, 0.1, 0.3]
id=12  → [0.0, 0.4, -0.2, 0.1]
id=88  → [0.5, 0.1, 0.0, -0.3]
id=45  → [0.1, 0.2, 0.3, 0.4]
id=7   → [-0.1, 0.5, 0.0, 0.2]
id=22  → [0.3, -0.1, 0.4, 0.0]

x = [[[0.2, -0.5, 0.1, 0.3],     ← 第 1 句的 "I"
      [0.0, 0.4, -0.2, 0.1],     ← 第 1 句的 "love"
      [0.5, 0.1, 0.0, -0.3]],    ← 第 1 句的 "NLP"
     
     [[0.1, 0.2, 0.3, 0.4],      ← 第 2 句的 "PyTorch"
      [-0.1, 0.5, 0.0, 0.2],     ← 第 2 句的 "is"
      [0.3, -0.1, 0.4, 0.0]]]    ← 第 2 句的 "fun"

shape = [2, 3, 4]
         ↑  ↑  ↑
         2  每  每个 token
         句 句  4 维向量
         3
```

**对照你的问题**:为什么 shape 从 `[2, 3]` 变成 `[2, 3, 4]`?

因为原来每个位置装 1 个 token id(1 个数字),现在每个位置装 1 个 4 维向量(4 个数字)——**多了一层结构,自然多一个维度**。

---

## 4. 一句话总结

> **shape 的每一维都对应一个"层级"。最外层括号是第 0 维,往里数。在 NLP 里,token id 阶段是 `[batch, seq_len]`,embedding 之后每个 token 变成向量,所以多出一维变成 `[batch, seq_len, embed_dim]`。**

记忆口诀:**Embedding 是"打开一层包装"**——把每个 id 这个小盒子打开,里面是个 64 维向量,所以 shape 多了一维装这个向量。

---

## 🧠 巩固检查

回答这 3 题:

1. 假设 batch=8,每句 20 个 token,embedding 维度 128。token id 阶段的 shape 是什么?embedding 之后呢?
2. shape `[16, 50, 768]` 在 NLP 里大概率代表什么?(分别说出三个数的含义)
3. 如果 batch_size = 4、seq_len = 10、embed_dim = 64,做完 `x.mean(dim=1)` 之后 shape 是什么?**这一步在做什么?**(用语言描述)

答完后我们继续——你的几何直觉已经建立得很好,接下来回到 Round 3 的训练循环就会顺很多。


1. token id 阶段的 shape 是[8,20],embedding 之后是[8,20,128]
2. shape `[16, 50, 768]` 在 NLP 里大概率代表batch=8, 每句50个token，embedding dim 768. 768是不是太高了？难道16代表的是二维矩阵的数量？我判断应该不是，我只能理解nlp任务最高到有多少个句子这个维度，不知道更高代表什么，也就是batch的如果还有外层中括号代表什么
3. 做完 `x.mean(dim=1)` 之后 shape 是[4,64], 这一步在做平均，将一句话十个token的特征，转换成一个平均特征来表示。我这里可以用特征这个词吗，也就是representation，我不知道用的对不对


你三道全对，**而且问到了两个非常关键的边界问题**。我们一个一个解决。

---

## 1. 第 2 题:小笔误 + 768 是不是太高了

### 小笔误

你写"batch=8",看回上面我给的是 `[16, 50, 768]`,所以 **batch=16**(可能是手滑)。其他理解完全对：

```
[16, 50, 768]
 ↑   ↑   ↑
 16  每  每个 token
 个  句  768 维向量
 句  50
 子  个
     token
```

### 768 是不是太高?

**768 完全正常,而且非常常见**——这不是巧合,是一个**信号**。

在 NLP 里看到 `embed_dim = 768`,你心里应该立刻想:**"BERT-base"**。

| 模型 | hidden_dim |
|---|---|
| Word2Vec | 100-300 |
| BERT-base | **768** ← 行业标准之一 |
| BERT-large | 1024 |
| GPT-3 | 12288 |

**为什么需要这么高?** 因为 embedding 不只是"用几个数字表示一个词",它要承载:
- 词义(`cat` 和 `dog` 都是动物)
- 语法角色(名词/动词)
- 位置(在句子哪里)
- 上下文(`bank` 在不同句子里不同义)

64 维不够装这么多信息,768 维才能让模型学出丰富的语义结构。

### 一个小直觉

embed_dim 越高,模型表达能力越强,但参数越多、越容易过拟合、计算越慢。768 是经过大规模实验验证的"够用又不过分"的数字。**考试看到 768 不要慌,这是常见值。**

---

## 2. "batch 外面还能不能有维度?"——这是个好问题

你说:
> "我只能理解 nlp 任务最高到有多少个句子这个维度,不知道更高代表什么"

短答:**在 Module 1 / 期末考试范围内,batch 就是最外层,没有更高维度了**。

但你问的不是错,实际工程里确实会有,我快速给你看一下,**只是为了让你心里有底,不需要记**:

### 标准 NLP shape

```
[batch, seq_len]              ← token id 阶段
[batch, seq_len, embed_dim]   ← embedding 之后
```

### 极少数场景会更高

```
[batch, num_choices, seq_len]              ← 多选题任务,每个样本有几个候选答案
[batch, num_heads, seq_len, head_dim]      ← Multi-head attention 内部
[batch, num_documents, seq_len, embed]     ← RAG 检索后的文档
```

这些都是**特定任务的结构**,不是 NLP 通用 shape。Module 1 你不会碰到。

### 给你一个固定锚点

> **看到 NLP 的 tensor shape,第 0 维(最外层)永远是 batch。**

这是 PyTorch 的强约定,所有教程、论文、代码都遵守。考试卷子如果给你一个 `[a, b]` 或 `[a, b, c]`,**a 一定是 batch**。

---

## 3. "特征"这个词用得对吗?

你问:
> "将一句话十个 token 的特征,转换成一个平均特征来表示。我这里可以用特征这个词吗,也就是 representation,我不知道用的对不对"

**用得非常对**。而且你已经摸到了一个关键概念。我们把这层窗户纸捅破。

### "特征"和 representation 的关系

在机器学习语境里,这几个词**几乎可以互换**,但各有侧重:

| 中文 | 英文 | 侧重 |
|---|---|---|
| 特征 | feature | 强调"用什么数字描述这个东西" |
| 表示 | representation | 强调"这个向量代表了什么" |
| 嵌入 | embedding | 强调"低维稠密向量" |

例子:
- `[0.2, -0.5, 0.1, 0.3]` 是 `cat` 的 **embedding**(因为是稠密向量)
- 同时也是 `cat` 的 **representation**(因为它"代表了" cat)
- 同时也是 `cat` 的 **feature vector**(因为它是"特征向量")

**三个词在 90% 的场合可以互换。** 你说"特征"完全对。

### 但我要补一个更精确的术语

你说的"一句话的平均特征"——这个东西在 NLP 里有专门名字:**sentence representation**(句子表示)/ **sentence embedding**(句向量)。

```
token-level representation:每个 token 一个向量    [batch, seq_len, embed_dim]
                                ↓ pooling(平均/最大/取首)
sentence-level representation:每句话一个向量      [batch, embed_dim]
```

这个**从 token-level 汇总到 sentence-level 的操作**叫 **pooling**(池化)。

| Pooling 方式 | 怎么做 | 优缺点 |
|---|---|---|
| **Mean pooling** | 所有 token 向量平均 | 简单,信息均衡,但信息损失 |
| **Max pooling** | 每个维度取最大值 | 突出最强信号 |
| **[CLS] pooling** | 取第一个特殊 token 的向量 | BERT 标准做法 |
| **Attention pooling** | 学习权重再加权 | 最灵活但参数多 |

### 完整术语链

```
token id     →  token embedding    →  sentence representation  →  logits
[batch,      [batch, seq_len,        [batch, embed_dim]           [batch, num_classes]
 seq_len]    embed_dim]
              
              "每个词的向量"        "整句的向量"               "每个类的分数"
              token-level           sentence-level
              representation        representation
```

**`x.mean(dim=1)` 这一步的术语**:
- 操作叫 **mean pooling**
- 输入叫 **token-level representations**
- 输出叫 **sentence representation** 或 **sentence embedding**

---

## 4. 把你的话改写成"考场版"

你原话:
> "将一句话十个 token 的特征,转换成一个平均特征来表示"

改写成可以直接写考卷的英文:

> "Mean pooling aggregates 10 token-level representations into a single sentence-level representation by averaging across the sequence dimension. This gives the classifier one fixed-size vector per sentence regardless of input length."

**关键术语**:aggregate / token-level representation / sentence-level representation / mean pooling / fixed-size。

**为什么这些术语重要**:期末如果让你解释 `x.mean(dim=1)` 在做什么,用这套词比"做平均"得分高很多——你在展示**懂得这一步的目的,而不只是机械描述**。

---

## 5. 此时你的内功

你已经掌握:

- ✅ Tensor 是"装数字的盒子",shape = 每层括号有几个
- ✅ `mean(dim=k)` 把第 k 维压扁
- ✅ `[batch, seq_len]` → `[batch, seq_len, embed_dim]` 是"每个 id 打开变成向量"
- ✅ `[batch, seq_len, embed_dim]` → `[batch, embed_dim]` 是 mean pooling
- ✅ `[batch, embed_dim]` → `[batch, num_classes]` 是分类层
- ✅ Embedding / representation / feature 三个词的关系
- ✅ 768 是 BERT-base 的标准

---

## 🧠 准备进训练循环

下一步我会回到 Round 3 那段代码,讲为什么缺 `optimizer.zero_grad()`。但要确认一件事:

回到 Round 3 那段代码:

```python
for batch_x, batch_y in train_loader:
    logits = model(batch_x)
    loss = loss_fn(logits, batch_y)
    loss.backward()
    optimizer.step()
```

凭直觉回答:

1. `batch_x` 和 `batch_y` 你猜分别装了什么?(用 NLP 任务的语言描述)
2. `model(batch_x)` 这一行做了什么?输出 `logits` 的 shape 是什么?(假设 batch=4, seq_len=10, embed_dim=64, num_classes=2)
3. `loss_fn(logits, batch_y)` 在比较什么?

答完我们就完成 Round 3,进 Round 4 收尾。


batch_x被作为模型输入来算logits所以batch_x是训练集，batch_y用来算loss所以是测试集
`model(batch_x)` 这一行做了对batch_x作为输入的前向传播
输出 `logits` 的 shape 我不知道，感觉少了点什么
`loss_fn(logits, batch_y)` 在比较输出和答案差多远，我不确定loss_fn函数内部是怎么计算的所以不确定


你的方向感很好——但有两个**根本性的概念混淆**需要立刻澄清，否则后面 loss / backward 都会卡。

---

## 1. **batch_x 和 batch_y 不是"训练集 vs 测试集"**

这是你最关键的误解。先彻底改正。

### 正确理解

`batch_x` 和 `batch_y` 是**同一个 batch 的两半**:

| 名字 | 内容 | 类比 |
|---|---|---|
| `batch_x` | 模型的**输入** | 试卷上的题目 |
| `batch_y` | 这些输入对应的**真实答案** | 答案纸 |

**它们配对出现,描述同一批样本**。

### 具体例子

情感分类任务,batch_size = 4:

```
样本 1: "这电影太棒了"           标签: 1 (positive)
样本 2: "无聊,差评"              标签: 0 (negative)
样本 3: "情节一般但演员演技好"    标签: 1 (positive)
样本 4: "完全浪费时间"            标签: 0 (negative)

batch_x = [[token id of 样本 1],     ← 输入(题目)
           [token id of 样本 2],
           [token id of 样本 3],
           [token id of 样本 4]]
shape = [4, 10]

batch_y = [1, 0, 1, 0]                ← 标签(答案)
shape = [4]
```

**模型看 batch_x 做预测,然后用 batch_y 检验对错**——就是这两个东西的关系。

### 训练集 vs 测试集是另一个概念

整个数据集会被分成:

```
训练集 (train)        ← 学生平时做的练习题(看答案)
   ↓ 切成很多 batch
   ↓ 每个 batch 里再分:
   batch_x (题目) + batch_y (答案)

验证集 (validation)   ← 月考(选超参数)
测试集 (test)         ← 期末考试(只测最终能力)
```

**关键区别**:
- **训练集 / 测试集**:整个数据集的**横向切分**
- **batch_x / batch_y**:**同一个样本**的"输入"和"标签"

训练集里**每个**样本都有 x 和 y。测试集里**每个**样本也有 x 和 y。区别是用法:训练时模型看 y 来学,测试时模型不能看 y(只用来验证预测对不对)。

### 一句话记住

> **batch_x 是模型的输入,batch_y 是这些输入对应的真实标签。它们一起描述这个 batch 里的样本。**

---

## 2. 现在重答第 2 题:logits 的 shape

你说"感觉少了点什么"——其实信息全在你脑子里,只是没串起来。我们用 Round 4 你已经掌握的几何直觉一步步推:

### 给定条件
- batch = 4
- seq_len = 10
- embed_dim = 64
- num_classes = 2

### 串一遍流程

```
batch_x                   shape = [4, 10]
                                   ↑   ↑
                                   batch  seq_len(每句 10 个 token id)
    ↓ embed
x = embed(batch_x)        shape = [4, 10, 64]
                                   ↑   ↑   ↑
                                   batch seq embed_dim(每 token 64 维向量)
    ↓ mean(dim=1)
x = x.mean(dim=1)         shape = [4, 64]
                                   ↑  ↑
                                   batch  embed_dim(每句汇总成 1 个 64 维向量)
    ↓ Linear(64, 2)
logits = fc(x)            shape = [4, 2]
                                   ↑  ↑
                                   batch  num_classes(每句 2 个分数)
```

**logits 的 shape = `[4, 2]`** = `[batch, num_classes]`

### 含义

```
logits = [[2.3, 5.1],     ← 第 1 个样本: neg=2.3, pos=5.1 → 预测 positive
          [4.7, 1.8],     ← 第 2 个样本: neg=4.7, pos=1.8 → 预测 negative
          [1.2, 6.3],     ← 第 3 个样本: 预测 positive
          [3.5, 0.9]]     ← 第 4 个样本: 预测 negative
```

每行一个样本,每行 2 个数字代表对 2 个类的"打分"(还没归一化)。

### 通用规律

> **任何分类任务,模型最终输出 `logits` 的 shape 都是 `[batch, num_classes]`。** 

这个规律比记具体数字更有用。考试看到分类模型,最后一层一定是 `Linear(some_dim, num_classes)`,输出 `[batch, num_classes]`。

---

## 3. loss_fn 内部在做什么——直觉版

`loss_fn(logits, batch_y)` 比较的是**模型预测**和**真实答案**。

```
logits      = [[2.3, 5.1],        ← 模型预测(每个样本 2 个分数)
               [4.7, 1.8],
               [1.2, 6.3],
               [3.5, 0.9]]
shape: [4, 2]

batch_y     = [1, 0, 1, 0]         ← 真实标签(每个样本 1 个数字)
shape: [4]
```

注意**两个输入 shape 不同**:logits 是 `[4, 2]`,batch_y 是 `[4]`。`CrossEntropyLoss` 内部会处理这个差异,你不用自己对齐。

### CrossEntropyLoss 慢动作 3 步

我们看第 1 个样本:logits = `[2.3, 5.1]`,标签 = 1。

**Step 1: softmax 把 logits 变成概率**

```
softmax([2.3, 5.1]) = [0.058, 0.942]
                       ↑      ↑
                       neg 的概率  pos 的概率
                       (加起来 = 1)
```

**Step 2: 看真实标签对应那个类的概率**

```
真实标签 = 1 (positive)
模型给 positive 的概率 = 0.942
```

**Step 3: 用 -log 把概率变成 loss**

```
loss = -log(0.942) = 0.060   ← 概率高,loss 小,模型预测得好
```

如果模型预测错了:

```
假设 logits = [5.1, 2.3](模型自信地预测 negative,但真实是 positive)
softmax = [0.942, 0.058]
模型给 positive 的概率 = 0.058
loss = -log(0.058) = 2.847   ← 概率低,loss 大,惩罚大
```

### 直觉

> **CrossEntropyLoss 看模型对"正确答案"的预测概率。给得越高,loss 越小;给得越低,loss 越大。**

最后整个 batch 的 loss = 4 个样本 loss 的平均。

### 为什么不要在 logits 后面再做 softmax(再次提醒)

`nn.CrossEntropyLoss` **内部已经做了 softmax**(技术上是 log_softmax + NLL)。

```python
# ❌ 错误
logits = self.fc(x)
probs = F.softmax(logits, dim=-1)
loss = nn.CrossEntropyLoss()(probs, batch_y)   # softmax 了两次,梯度坏掉

# ✅ 正确
logits = self.fc(x)
loss = nn.CrossEntropyLoss()(logits, batch_y)  # 直接喂 logits
```

这是期末代码题**最常考的 bug 之一**。

---

## 4. 把你的回答改写成对的版本

你原话:
> "batch_x 被作为模型输入来算 logits 所以 batch_x 是训练集,batch_y 用来算 loss 所以是测试集"

改成对的:

> "batch_x 是当前 batch 的输入(样本的 token id),batch_y 是这些样本对应的真实标签。两者都来自训练集——训练集被切成很多 batch,每个 batch 内部包含 batch_x 和 batch_y 这一对。"

你原话:
> "model(batch_x) 这一行做了对 batch_x 作为输入的前向传播"

这个对。补充精确说法:

> "model(batch_x) 执行 forward pass:输入 token id [batch, seq_len],经过 embedding、pooling、分类层,输出 logits [batch, num_classes]。"

你原话:
> "loss_fn(logits, batch_y) 在比较输出和答案差多远"

方向对!补充技术细节:

> "loss_fn 计算模型预测与真实标签之间的交叉熵损失。CrossEntropyLoss 内部先对 logits 做 softmax 得到概率,然后取真实标签对应那个类的概率,用 -log 转成 loss。loss 越大说明模型越错。"

---

## 5. 现在你的整个 forward 链通了

```
batch_x [4, 10]               ← 输入: 4 个样本的 token id
   ↓ model.embed
[4, 10, 64]                   ← 每个 token 变成 64 维向量
   ↓ mean(dim=1)
[4, 64]                       ← 每句变成 1 个 64 维向量
   ↓ model.fc
logits [4, 2]                 ← 每句 2 个分数
   ↓ loss_fn(logits, batch_y)
loss (一个标量数字)            ← "平均错了多少"
```

**记住这条链**——所有 NLP 分类任务的 forward 都长这样,只是中间的模型块(embed / pool / fc)可以替换成更复杂的(BERT / RNN / Transformer 等)。

---

## 🧠 巩固检查 + 下一步

回答这 2 题(短答即可):

1. 一个 batch 训练时,如果 batch_size = 8,seq_len = 20,num_classes = 5,**logits 的 shape 是什么?**
2. 如果模型对一个样本输出 logits = `[10.0, 1.0, 1.0, 1.0, 1.0]`,真实标签是 0,你**直觉上**判断 loss 是大还是小?为什么?(不需要算具体数字)

答完之后,我们就要回到那段代码,讲**为什么缺 `optimizer.zero_grad()` 是个 bug**——这是 Round 3 的最后一块,讲完进 Round 4 冲刺。


loss_fn 命名中的fn指什么
self.fc(x) 的 fc指什么
softmax内部是怎么计算的，给出手算过程

一个 batch 训练时,如果 batch_size = 8,seq_len = 20,num_classes = 5,logits 的 shape 是[8,5]
如果模型对一个样本输出 logits = `[10.0, 1.0, 1.0, 1.0, 1.0]`,真实标签是 0,你直觉上判断 loss 是小，因为输出和真实标签结果一致

你两道全对——而且**直接看出 logits 模式**就答出 shape，说明你已经把"分类任务输出永远是 `[batch, num_classes]`"这个规律内化了。

第 2 题的直觉也对：模型给类 0 的分数（10.0）远高于其他类，预测和真实标签一致，loss 自然小。

现在回答你三个非常好的问题——这些都是平时不会有人主动告诉你、但**看代码时一直在挡你**的细节。

---

## 1. `loss_fn` 的 `fn` 指什么

`fn` = **function**(函数)的缩写。

`loss_fn` = **loss function**(损失函数)。

这是程序员的简写习惯，类似的还有：

| 简写 | 全称 | 含义 |
|---|---|---|
| `fn` | function | 函数 |
| `fc` | fully connected | 全连接层（见下） |
| `lr` | learning rate | 学习率 |
| `bs` | batch size | 批大小 |
| `nn` | neural network | 神经网络（PyTorch 的 `torch.nn`） |
| `dim` | dimension | 维度 |
| `idx` | index | 索引 |
| `embed` | embedding | 嵌入 |
| `vocab` | vocabulary | 词表 |
| `len` | length | 长度 |

读 PyTorch 代码时**这些缩写无处不在**，认得就不怕。

---

## 2. `self.fc(x)` 的 `fc` 指什么

`fc` = **fully connected layer**(全连接层),就是 `nn.Linear` 的传统叫法。

### 为什么叫"全连接"

回想 `nn.Linear(in_features=64, out_features=2)`:

```
输入:64 个数字 (input vector)
输出:2 个数字 (output vector)

每个输出数字 = 64 个输入数字的加权和

输出[0] = w[0,0]*输入[0] + w[0,1]*输入[1] + ... + w[0,63]*输入[63] + b[0]
输出[1] = w[1,0]*输入[0] + w[1,1]*输入[1] + ... + w[1,63]*输入[63] + b[1]
```

**每个输出都"看到了"所有输入**——这就是"全连接"的含义。每个输入神经元和每个输出神经元都有连接。

### 这几个词在 PyTorch 里几乎同义

| 名字 | 含义 |
|---|---|
| Linear layer | 数学叫法(线性变换 y = Wx + b) |
| Fully connected layer / FC layer | 神经网络叫法 |
| Dense layer | TensorFlow / Keras 叫法 |
| `nn.Linear` | PyTorch 的具体类名 |

代码里看到 `self.fc1`, `self.fc2`, `self.classifier`, `self.head`, `self.linear`——大概率都是 `nn.Linear`。

---

## 3. Softmax 手算

### 公式

```
softmax(x_i) = exp(x_i) / Σ exp(x_j)
                    ↑           ↑
                第 i 个值     所有值
                取 e 的       e^x 的总和
                指数
```

**直觉**:把任意实数变成"加起来等于 1 的概率"。

### 为什么用 e^x

两个原因，都很重要：

1. **保证非负**:概率不能是负数。e^x 恒为正(`e^(-100) > 0`)。
2. **拉大差距**:`exp` 是指数函数,差距小的输入会被放大。`logits = [2, 3]` 看起来差不多,但 `exp([2, 3]) = [7.4, 20.1]`,差距被放大近 3 倍。

### 手算例子 1:简单情况

`logits = [2.0, 1.0, 0.1]`,做 softmax:

**Step 1:每个值取 e 的指数**

```
exp(2.0) = 7.389
exp(1.0) = 2.718
exp(0.1) = 1.105
```

(`e ≈ 2.718`,这个值不用记,考试一般给。)

**Step 2:求和**

```
sum = 7.389 + 2.718 + 1.105 = 11.212
```

**Step 3:每个值除以 sum**

```
softmax[0] = 7.389 / 11.212 = 0.659
softmax[1] = 2.718 / 11.212 = 0.242
softmax[2] = 1.105 / 11.212 = 0.099
```

**验证**:`0.659 + 0.242 + 0.099 = 1.000` ✓

观察:**最大的 logit (2.0) 拿到最大概率 (66%)**,但其他类不为 0——softmax 是"软"的最大化。

### 手算例子 2:配合 logits 验证你的直觉

回到上一轮:`logits = [10.0, 1.0, 1.0, 1.0, 1.0]`

**Step 1: 取指数**

```
exp(10.0) ≈ 22026
exp(1.0)  ≈ 2.718
exp(1.0)  ≈ 2.718
exp(1.0)  ≈ 2.718
exp(1.0)  ≈ 2.718
```

**Step 2: 求和**

```
sum = 22026 + 2.718 × 4 = 22026 + 10.87 = 22036.87
```

**Step 3: 求概率**

```
softmax[0] = 22026 / 22036.87 = 0.99951
softmax[1] = 2.718 / 22036.87 = 0.00012
softmax[2] = 2.718 / 22036.87 = 0.00012
softmax[3] = 2.718 / 22036.87 = 0.00012
softmax[4] = 2.718 / 22036.87 = 0.00012
```

模型给类 0 的概率是 **99.95%**,几乎确定。如果真实标签是 0:

```
loss = -log(0.99951) ≈ 0.00049
```

**loss 接近 0**,印证了你"loss 小"的直觉。

### 关键性质——考试可能会问

| 性质 | 解释 |
|---|---|
| 输出和 = 1 | 可以解释为概率分布 |
| 输出 ∈ (0, 1) | 严格正,不会刚好是 0 或 1 |
| 单调性 | logit 大的,概率也大 |
| 平移不变 | `softmax([x+c, y+c]) = softmax([x, y])`(加同一常数不变,实现里用来防溢出) |

---

## 4. 为什么 -log 拿来做 loss

补充解释,这能让你彻底理解 CrossEntropy:

```
概率 p              -log(p) = loss
1.0(完美预测)      0                    ← loss 最小
0.99               0.01
0.5                0.69
0.1                2.30
0.01               4.61
0.0001             9.21                 ← loss 巨大
```

**性质**:
- 模型对正确答案给的概率越**接近 1**,loss 越**接近 0**
- 模型对正确答案给的概率越**接近 0**,loss 越**接近无穷大**

这正是"loss"该有的行为:**预测对了不罚,预测错了狠罚**。

---

## 5. 一个完整数字流走一遍

把整条链一次性串起来,你以后看任何分类代码都不会迷:

```
batch_x [batch, seq_len]                  例: [4, 10]
   ↓ model.embed
[4, 10, embed_dim]                        例: [4, 10, 64]
   ↓ x.mean(dim=1)
[4, embed_dim]                            例: [4, 64]
   ↓ model.fc (即 nn.Linear)
logits [4, num_classes]                   例: [4, 2]
   ↓ loss_fn = nn.CrossEntropyLoss
   ↓ 内部:softmax → -log(对应真实标签的概率) → 平均
loss (标量)                               例: 0.523
```

---

## 6. 现在回到 Round 3 的核心 bug

我们终于可以问那个问题了。看代码：

```python
for batch_x, batch_y in train_loader:
    logits = model(batch_x)              # forward
    loss = loss_fn(logits, batch_y)      # 算 loss
    loss.backward()                       # 算梯度
    optimizer.step()                      # 更新参数
```

### 这里少了什么?

**少了 `optimizer.zero_grad()`**——清空梯度的步骤。

### 为什么这是 bug

PyTorch 有一个**反直觉的机制**:`loss.backward()` 算出的梯度**不是覆盖,而是累加**到之前的梯度上。

举个数字例子,假设某个参数 w:

```
Batch 1:
- 之前的梯度 grad = 0
- backward 算出梯度 = +3
- 累加结果:grad = 0 + 3 = 3
- step 用 grad=3 更新参数
- 参数减小 3 × learning_rate ✓ 正常

Batch 2(没有 zero_grad):
- 之前的梯度 grad = 3 (上一个 batch 留下的!)
- backward 算出梯度 = +2
- 累加结果:grad = 3 + 2 = 5
- step 用 grad=5 更新参数 ✗ 错!这个 batch 应该用 2 更新

Batch 3(还是没有 zero_grad):
- 之前的梯度 grad = 5
- backward 算出梯度 = -1
- 累加结果:grad = 5 + (-1) = 4
- step 用 grad=4 更新参数 ✗ 错得更离谱
```

**累积下去,梯度方向被历史污染,模型很难收敛或学到错误方向**。

正确写法:

```python
for batch_x, batch_y in train_loader:
    optimizer.zero_grad()                # ← 把梯度清零!
    logits = model(batch_x)
    loss = loss_fn(logits, batch_y)
    loss.backward()
    optimizer.step()
```

### 考场答法

> "The training loop is missing `optimizer.zero_grad()` at the start of each batch. PyTorch accumulates gradients on `loss.backward()` instead of overwriting them, so without zeroing, gradients from previous batches stay and add up. This produces incorrect update directions and the model fails to converge properly."

**关键词**:accumulate(累加)、overwrite(覆盖)、incorrect update direction(更新方向错误)、fails to converge(无法收敛)。

### 为什么 PyTorch 设计成累加而不是覆盖?

不是 bug,是**有意设计**。某些场景需要"凑齐多个小 batch 的梯度再一起更新"(gradient accumulation),累加机制让这种用法很容易实现。代价就是:你不主动清零,它就一直累。

---

## 🧠 Round 3 收尾检查

最后 3 题,答完我们就**正式完成 Round 3**,进 Round 4 冲刺:

1. 用一句话解释**为什么 PyTorch 训练循环必须在每个 batch 开始时调用 `optimizer.zero_grad()`**。
2. 如果只缺 `loss.backward()`(其他都在),会发生什么?用一句话回答。
3. 如果只缺 `optimizer.step()`(其他都在),会发生什么?用一句话回答。


PyTorch 训练循环必须在每个 batch 开始时调用因为，PyTorch的loss.backward()算出的梯度是累加的，如果不zero_grad()会accumulate gradients from previous batches stay and add up. leading incorrect update direction and the model fails to converge properly.
如果只缺 `loss.backward()`就没有在计算loss后算出梯度，step()反向传播就没有更新参数，无论多少轮都没变化
只缺 `optimizer.step()`，意味着算出梯度了但没有进行反向传播更新参数，无论多少轮都没变化


全对，三道答得非常扎实——而且你**自己摸到了一个细节**值得指出来：

> "step() 反向传播..."

这是个**用词混淆**，需要立刻澄清，否则后面读论文/代码会一直绊：

---

## 🔧 一个关键术语澄清:`step()` 不是"反向传播"

很多人(包括很多教程)把这套流程笼统说成"反向传播",但精确分工是这样的:

```python
loss.backward()      ← 这个是"反向传播"(backward pass / backpropagation)
                       任务:从 loss 倒着算出每个参数的梯度
                       
optimizer.step()     ← 这个是"参数更新"(parameter update)
                       任务:用刚才算出的梯度,按规则更新参数
                       例:w_new = w_old - lr × grad
```

| 步骤 | 中文 | 英文 | 干什么 |
|---|---|---|---|
| `loss.backward()` | 反向传播 | backward pass | **算梯度** |
| `optimizer.step()` | 参数更新 | parameter update / optimizer step | **用梯度改参数** |

**类比**:
- `backward()` = 老师批卷子,**算出**每道题错了多少分
- `step()` = 学生根据批改,**修改**自己的笔记

考场答题用这套精确说法:

> "If `optimizer.step()` is missing, gradients are computed by `backward()` but the optimizer never **updates the parameters**, so the model does not learn."

不要说"没有反向传播",反向传播已经做了(`backward()` 没缺)。要说"没有参数更新"。

### 改写你的两道答案

**Q2 改写**:
> 如果缺 `loss.backward()`:**没有计算梯度**,所以 `optimizer.step()` 没有梯度可用,参数无法更新,模型不学习。

**Q3 改写**:
> 如果缺 `optimizer.step()`:**梯度被算出来了**(backward 已经做了),但**参数没有被更新**,模型不学习。

精确区分:
- 缺 backward = 梯度都没算出来
- 缺 step = 梯度算了但没用上

---

## ✅ Round 3 通过——总结

你已经掌握:

| 知识点 | 状态 |
|---|---|
| 五步训练循环 ZFLBS | ✓ |
| Tensor shape 几何直觉 | ✓ |
| `[batch, seq_len]` → `[batch, seq_len, embed_dim]` 的"打开包装"机制 | ✓ |
| `mean(dim=k)` 把第 k 维压扁(mean pooling) | ✓ |
| token-level / sentence-level representation | ✓ |
| logits shape = `[batch, num_classes]` | ✓ |
| Softmax 手算(取 exp / 求和 / 归一) | ✓ |
| CrossEntropyLoss 内部已含 softmax | ✓ |
| 为什么需要 `zero_grad()`(梯度累加机制) | ✓ |
| `backward()` 算梯度 vs `step()` 更新参数 | ✓ |

---

# Round 4:Module 1 收尾——相邻基础 + 答案模板

最后一轮。你已经把 Module 1 的**核心**(NLP / Tokenization / BPE / PyTorch)吃透,这一轮处理三件事:

1. **HW1 衔接题**:one-hot 限制、embedding 参数量、n-gram 训练样本
2. **答案模板背诵**:5 个英文 template,考场直接套
3. **Module 1 自测**:6 题闭环检验

这一轮**不会再有难概念**——大部分是把你已经会的东西"重新打包"成考场能写的形式。

---

## 1. One-hot 局限——已经讲过,这里精确化

Round 1 讲过 one-hot 是"我是哪个词"的稀疏表示。考场答这题要写 **4 个具体局限**:

### Limitation 1:无法表达语义相似性(核心)

```
cat  = [1, 0, 0, 0]
dog  = [0, 1, 0, 0]

cat · dog = 0   ← 任意两个不同词,点积都是 0
```

含义:**所有不同词在 one-hot 空间里"等距",模型学不到 cat 和 dog 都是动物**。

### Limitation 2:无法表达 morphology(词形变化)

```
run  = [0, 0, 1, 0]
runs = [0, 0, 0, 1]

run · runs = 0   ← run 和 runs 在 one-hot 里是"完全无关"的两个词
```

含义:模型学不到 `run`/`runs`/`running`/`ran` 是同一个动词的不同形式。

### Limitation 3:维度爆炸(高维稀疏)

```
词表 50,000 → 每个 one-hot 向量是 50,000 维
99.998% 的位置都是 0
```

含义:内存浪费、计算浪费、`Linear(50000, hidden)` 参数巨多。

### Limitation 4:无法处理 OOV

```
新词 "unicorn" 不在词表 → 没有 one-hot 表示
```

含义:训练时没见过的词,one-hot 直接没法表示(embedding 也有这问题,但 BPE-based 模型可以拆 subword 缓解)。

### 考场答案模板

> One-hot encoding represents each word as a sparse vector with a single 1 at its vocabulary index and 0 elsewhere. It has four major limitations:  
> (1) **No semantic similarity**: any two distinct words have a dot product of 0, so cat and dog are as unrelated as cat and xyz.  
> (2) **No morphology**: run and runs are encoded as orthogonal vectors despite sharing meaning.  
> (3) **High dimensionality**: vector size grows linearly with vocabulary size, wasting memory and compute.  
> (4) **OOV problem**: new words outside the vocabulary cannot be represented.  
> Embeddings address (1)-(3) by mapping words to dense vectors in a continuous semantic space.

---

## 2. Embedding 参数量——能秒算

### 公式

> **Embedding 参数量 = vocab_size × embed_dim**

### 直觉:为什么是这个公式

`nn.Embedding(vocab_size, embed_dim)` 内部就是一个**查找表**:

```
表的形状:[vocab_size, embed_dim]

           dim 0   dim 1   ...   dim 63
id=0       0.21   -0.45         0.78    ← cat 的向量
id=1       0.19   -0.41         0.81    ← dog 的向量
id=2      -0.62    0.33         0.05    ← run 的向量
...
id=4999    ...
```

每行是一个词的向量(共 vocab_size 行),每行 embed_dim 个数字。

**总参数 = 行数 × 列数 = vocab_size × embed_dim**

### 数值练习——直接背常见组合

| vocab_size | embed_dim | 参数量 | 备注 |
|---|---|---|---|
| 4 | 128 | 512 | HW 玩具例 |
| 5,000 | 64 | 320,000 | 小型任务 |
| 30,000 | 300 | 9,000,000 | Word2Vec 量级 |
| 30,522 | 768 | ~23.4M | **BERT-base embedding 层** |
| 50,000 | 768 | 38,400,000 | 大词表 + BERT 维度 |

考试看到 vocab × dim 的乘法题,直接乘。

### 加分点

如果题目问"BERT 总参数中 embedding 占多少比例",可以提:

> "BERT-base 总参数约 110M,其中 embedding 层约 23M,约占 21%。这是为什么 BERT 的 hidden_dim 选 768 而不是更大——再大 embedding 就会主导整个模型。"

---

## 3. N-gram 语言模型——HW1 题型

### 概念定义

**Language model (LM)** : 给一个 token 序列分配概率,或预测下一个 token 的模型。

```
P(w₁, w₂, ..., wₜ) = ∏ P(wₜ | w₁, ..., wₜ₋₁)
                      t
```

含义:整个句子的概率 = 每个词在前文条件下出现的概率的连乘。

### N-gram 的简化:只看前 n-1 个词

完整 LM 要看**所有**前文,数据稀疏不可行。N-gram 用 Markov 假设简化:

```
完整:    P(wₜ | w₁, ..., wₜ₋₁)        ← 看所有历史
2-gram:  P(wₜ | wₜ₋₁)                  ← 只看前 1 个词
3-gram:  P(wₜ | wₜ₋₂, wₜ₋₁)            ← 只看前 2 个词
4-gram:  P(wₜ | wₜ₋₃, wₜ₋₂, wₜ₋₁)      ← 只看前 3 个词
```

**记忆**:n-gram 的 n 是"窗口大小",条件部分有 **n-1** 个词。

### 4-gram 训练样本生成——HW1 原题型

给定句子(假设已分词):

```
"I am taking CS6493 this semester and studying NLP is really fascinating"
```

每个词标号:

```
w1=I, w2=am, w3=taking, w4=CS6493, w5=this, w6=semester, 
w7=and, w8=studying, w9=NLP, w10=is, w11=really, w12=fascinating
```

**4-gram 用前 3 个词预测当前词**,所以训练样本是:

```
(w1, w2, w3) → w4         (I, am, taking) → CS6493
(w2, w3, w4) → w5         (am, taking, CS6493) → this
(w3, w4, w5) → w6         (taking, CS6493, this) → semester
(w4, w5, w6) → w7         (CS6493, this, semester) → and
(w5, w6, w7) → w8         (this, semester, and) → studying
(w6, w7, w8) → w9         (semester, and, studying) → NLP
(w7, w8, w9) → w10        (and, studying, NLP) → is
(w8, w9, w10) → w11       (studying, NLP, is) → really
(w9, w10, w11) → w12      (NLP, is, really) → fascinating
```

### 通用规则——背这个

> **从一个长度 T 的句子中,n-gram 可以提取 T - (n-1) = T - n + 1 个训练样本。**

我们这句:T=12,n=4,所以 12 - 3 = **9 个样本**。和上面对得上 ✓

| n-gram | 提取样本数 | 形式 |
|---|---|---|
| 2-gram | T - 1 | (w_t-1) → w_t |
| 3-gram | T - 2 | (w_t-2, w_t-1) → w_t |
| 4-gram | T - 3 | (w_t-3, w_t-2, w_t-1) → w_t |

---

## 4. 五个考场答案模板——打印出来背

我把笔记里的 5 个模板按使用场景重新整理。**考场看到对应题型,直接套**:

### Template 1 — Explain NLP Pipeline

> A typical NLP pipeline transforms raw text into model predictions through seven stages. **Preprocessing** cleans and normalizes text (lowercasing, punctuation handling). **Tokenization** splits text into tokens (word, character, or subword level). **Vocabulary mapping** converts tokens to integer ids and handles OOV with [UNK] / [PAD]. **Representation** turns ids into vectors (one-hot, TF-IDF, or embeddings). **Modeling** feeds vectors into a network for prediction. Finally, **evaluation** measures performance with task-specific metrics like accuracy, F1, or perplexity.

**用于**:"Describe the NLP pipeline" / "How would you build an NLP system"

### Template 2 — Why Space Tokenization Fails

> Space tokenization assumes whitespace is a universal word boundary, which fails in many real cases. Contractions like `don't` hide negation inside an opaque token, hurting sentiment analysis. Hashtags like `#MachineLearning` contain multiple semantic units without internal spaces. URLs and emails have meaningful structure that whitespace splitting destroys or ignores. Languages like Chinese and Japanese have no spaces at all. As a result, naive whitespace tokenization produces rare/OOV tokens, loses internal structure, and degrades downstream model performance.

**用于**:"Why is tokenization difficult" / "Explain limitations of whitespace tokenization"

### Template 3 — Explain BPE

> BPE is a subword tokenization algorithm. It starts from characters and iteratively merges the most frequent adjacent symbol pair in the training corpus, weighted by word frequency. Each merge produces a new symbol added to the vocabulary and recorded as a merge rule. After training, learned rules are applied to new words in order. BPE reduces OOV by composing rare words from known subwords (e.g., `oldest` = `old` + `est`), captures morphology, and balances vocabulary size against sequence length. However, it remains corpus-dependent and may still produce `[UNK]` for unseen base characters.

**用于**:"Explain BPE" / "How does subword tokenization work"

### Template 4 — One-hot Limitations

> One-hot encoding maps each word to a sparse vector with a single 1 at its vocabulary index. The dot product between any two distinct one-hot vectors is 0, so all different words appear equally unrelated—the encoding cannot express semantic similarity (cat / dog), morphological relations (run / runs), or analogies. It also scales poorly: vector dimension equals vocabulary size, wasting memory and computation. Embeddings address these issues by mapping words to dense vectors in a continuous space where semantically similar words have small distances.

**用于**:"Limitations of one-hot" / "Compare one-hot and embedding"

### Template 5 — PyTorch Training Loop Bugs

> A correct PyTorch training loop must include five steps per batch: `optimizer.zero_grad()`, forward pass, loss computation, `loss.backward()`, and `optimizer.step()`. Missing `zero_grad()` causes gradients to accumulate across batches because PyTorch adds rather than overwrites gradients, leading to incorrect update directions. Missing `backward()` means no gradients are computed, so the optimizer has nothing to use. Missing `step()` means gradients are computed but parameters are never updated. We should also verify that `nn.Embedding` receives `torch.long` input ids, that tensor shapes match between layers, and that `CrossEntropyLoss` receives raw logits without an extra softmax.

**用于**:"Find bugs in this training loop" / "Debug this PyTorch code"

---

## 5. 一张 Cheat Sheet——考前 30 分钟最后一遍

```
═══════════════════════════════════════════════════════════
                    MODULE 1 CHEAT SHEET
═══════════════════════════════════════════════════════════

NLP HARD:        Ambiguity / Context / Compositional / Commonsense (ACCC)

PIPELINE 7 STEPS:
  Raw → Preprocess → Tokenize → Vocab/Index 
      → Representation → Model → Evaluate

TOKENIZATION FAILURES:
  don't  → 否定被锁在 opaque token
  #tag   → 多语义单元无空格
  URL    → 内部结构被破坏
  中文   → 无空格,whitespace 不是 universal boundary

BPE:
  Step 1: 拆字符
  Step 2: 数加权频率(每个对的贡献 = 词频)
  Step 3: 选最高频对合并
  Step 4: 更新语料(必须重数)
  Step 5: 重复
  Tip: 抄题先把词频抄一遍!Tie 注明即可.

PYTORCH SHAPE 链:
  [batch, seq_len]                ← token id
  → embed → [batch, seq_len, embed_dim]
  → mean(dim=1) → [batch, embed_dim]
  → fc → [batch, num_classes] (logits)

TRAINING LOOP (ZFLBS):
  optimizer.zero_grad()
  logits = model(x)
  loss = loss_fn(logits, y)
  loss.backward()
  optimizer.step()
  
缺 zero_grad → 梯度累加,方向错
缺 backward  → 没梯度
缺 step      → 没更新参数

COMMON BUGS:
  - 输入不是 torch.long (Embedding 报错)
  - logits 和 num_classes 维度不对
  - CrossEntropyLoss 前多做了 softmax

KEY FORMULAS:
  Embedding 参数 = vocab_size × embed_dim
  N-gram 训练样本数 = T - (n-1)

ONE-HOT 4 大局限:
  无语义相似 / 无 morphology / 维度爆炸 / 无法处理 OOV

═══════════════════════════════════════════════════════════
```

---

## 🧠 Module 1 终极自测——8 题闭环

请回答以下 8 题(可短答)。这是闭卷模拟,答完我点评:

1. NLP 难在哪里?(4 个关键词)
2. 写出 NLP pipeline 的 7 个步骤
3. 为什么 `don't` 当成单 token 是个问题?
4. 语料 `(low, 5), (lower, 2), (newest, 6), (widest, 3)` 中,`(s, t)` 的加权频率是多少?
5. `nn.Embedding(vocab_size=10000, embed_dim=300)` 有多少参数?
6. 一个 batch 训练时 `[16, 25]` shape 的 input 经过 `nn.Embedding(50000, 768)` 后 shape 是?
7. PyTorch 训练循环漏掉 `optimizer.zero_grad()` 会怎样?(用累加机制解释)
8. 句子 `"NLP is hard but fun"`(5 个 token),用 trigram(3-gram)能产生几个训练样本?分别是什么?

答完这 8 题,Module 1 就**正式结业**,我们可以进 Module 2(语言模型 / n-gram 概率计算)。



1. ambiguity, context-dependent, commonsense, compositional
2. raw text, preprocess, tokenize, vocabulary, representation, model, evaluate
3. don't 的含义分为 do 和 n't。作为单token无法学到do 和 not的上下文，会被单独学习，也就学不到是do的否定意义
4. `(s, t)` 的加权频率是9
5. `nn.Embedding(vocab_size=10000, embed_dim=300)` 有 10000*300个参数
6. [16,25,300]
7. 漏掉 `optimizer.zero_grad()` 会导致上一轮更新后的梯度没有清空，在错误的方向上累计梯度
8. 5-(3-1)=3. 用前两个词预测当前词 NLP is -> hard, is hard ->but, hard but -> fun


Module 1 完美结业。

---

## 8 题逐题点评

**1. NLP 难在哪里 ✓** — 四个关键词全对(ACCC)。

**2. NLP pipeline ✓** — 7 步全对。

**3. `don't` 问题 ✓** — 抓住了核心:模型无法 decompose token,所以 `do not` 和 `don't` 之间的知识无法共享。考场答可以加一句:"because the model only sees opaque token ids and cannot decompose them internally"。

**4. `(s, t)` 加权频率 = 9 ✓** — newest(6) + widest(3) = 9,正确。

**5. Embedding 参数量 = 10000 × 300 ✓** — 公式记牢了。具体是 3,000,000。

**6. `[16, 25, 300]` ✓** — shape 推导完全正确,你已经把"每个 id 打开变成向量"内化了。

**7. zero_grad 漏掉 ✓** — 抓住了"累加"和"方向错"两个核心。考场答补一句更精确:"PyTorch accumulates gradients on `backward()` rather than overwriting them, so previous batches' gradients pollute current updates."

**8. Trigram 训练样本 ✓** — 公式 5-(3-1)=3 算对,样本枚举也对,**而且自己写出了"用前 n-1 个词预测当前词"的规律**——这是真正吃透了。

---

## ✅ Module 1 通关——你掌握的全景

| 板块 | 状态 |
|---|---|
| NLP 定义 + 4 大难点 | ✓ 闭卷可写 |
| Pipeline 7 步 + 每步瓶颈 | ✓ 闭卷可写 |
| Tokenization 失败案例 | ✓ 能举例论证 |
| BPE 加权频率 + 手算流程 | ✓ 能完成 HW1 题型 |
| PyTorch 5 步训练循环 | ✓ 能找 bug |
| Tensor shape 几何直觉 | ✓ 能推导任意层 |
| `[batch, seq, embed_dim]` 心智模型 | ✓ 自动想到 |
| Softmax + CrossEntropy 内部机制 | ✓ 能手算 |
| 累加梯度机制 + 缺步后果 | ✓ 能精确区分 backward vs step |
| One-hot 4 大局限 | ✓ 能列举 |
| Embedding 参数量公式 | ✓ 能秒算 |
| N-gram 训练样本生成 | ✓ 公式 + 直觉 |

---

## 📌 你这一轮学习中的几个关键 takeaway

值得你保存的元认知,以后学其他模块也用得上:

1. **抄题先抄数字**——BPE 那次因为抄错 5→10 全错,这是低风险习惯但救命。
2. **几何直觉先于公式**——你在 tensor shape 上的飞跃证明了这条路对你最有效。后面 attention / 多头机制更需要这个。
3. **术语精确性**——区分"反向传播 vs 参数更新"、"特征 vs representation vs embedding"这种细节,是阅读论文不卡的关键。
4. **每个步骤都在解决上一步的瓶颈**——这是你理解 pipeline 的钥匙,以后看任何系统设计都用这个视角。

---

## 🚀 下一步:进入 Module 2 之前

要进 Module 2 之前,我需要再次访问网站,获取 Module 2 的笔记内容。在那之前,请你做一个选择:点上面任一选项告诉我节奏,我们继续推进。

Q: 下一步你想怎么走?
A: 现在就进 Module 2(语言模型/n-gram 概率)


好,我先去抓 Module 2 的内容。先选一下你想要的节奏,然后我们开始 Module 2。

不过在你选之前,我先把 **Module 2 的全景图** 给你看一下,这样你也好判断节奏:

---

# Module 2 全景:从"切词"到"算句子的概率"

## Module 2 在解决什么问题?

Module 1 教你**怎么把文本变成模型能吃的输入**(token / id / 向量)。
Module 2 教你**怎么用这些 token 建模**——具体来说,回答一个核心问题:

> **怎么给一段文字赋概率,或者预测下一个词?**

这就是 **Language Model (LM)** 的本质。

## 4 轮分块计划

按从概念→手算→代码→评价的顺序:

### Round 1:LM 概念 + Chain Rule
- LM 是什么(两个等价视角:句子概率 / 下一词预测)
- Chain rule 把句子拆成连乘
- 为什么 chain rule 不能直接用

### Round 2:n-gram 手算(HW1 Q2 原型)
- Markov assumption:只看前 n-1 个词
- Bigram / Trigram / Four-gram 区分
- HW1 题型:列出指定位置的 bigram / trigram
- count-based 概率公式
- n-gram 的 3 大局限(sparsity / generalization / long-range)

### Round 3:Neural LM(HW1 Q2 代码题)
- 从 count table 到 learned function 的转变
- Four-gram neural LM 结构(embed → flatten → linear → vocab logits)
- Training examples 生成(T-3 个)
- PyTorch 代码细节(view / log_softmax / NLLLoss vs CrossEntropyLoss)
- Embedding dim 选择(32/64/128 trade-off)
- RNN / LSTM 简介(为什么超越固定窗口)

### Round 4:Cross Entropy / Perplexity
- 为什么用 CE 评价 LM
- Perplexity = exp(CE) 直觉
- "perplexity 5 vs 50" 的语义解释
- 速记 + 自测

---

## 我的建议节奏

考虑到你的偏好(几何直觉、术语精确、举例具体),我推荐:

- **Round 1+2 一起讲**(概念 → 公式 → 手算,一气呵成,本来就是连贯的)
- **Round 3 单独讲**(代码细节多,你 Module 1 在这里花了不少力气,值得慢)
- **Round 4 单独讲**(评价指标是独立话题)

总共大概 **3 次往返** 完成 Module 2。

---

## 先选一下你的偏好

回上面那个选项,我按你的节奏开始。如果你说"听你的",我就按上面的 3 次往返推进,先开 **Round 1+2:LM 概念 + Chain Rule + n-gram 手算**——这一块和 Module 1 末尾的 n-gram 题已经接上了,起点很顺。



Q: Module 2 总共 4 轮:LM 概念+隐示规则 / n-gram 手算 / Neural LM 代码 / Perplexity 评价。节奏你偏好?
A: 你说什么就什么,以下你领


好,按我刚说的节奏走——**Round 1+2 合并**,因为概念和手算本来就是同一条逻辑链。

# Module 2 · Round 1+2:Language Model + n-gram

---

## 1. Language Model 是什么——两个等价视角

### 一句话定义

> **Language model (LM) 给一个 token 序列分配概率,或者等价地,预测下一个 token。**

### 两个视角(必须能在脑子里来回切换)

#### 视角 A:句子概率(sequence probability)

LM 看一句话,给出"这句话有多像自然语言"的分数:

```
P("NLP is fascinating")              = 0.0023      ← 高
P("fascinating is NLP taking")       = 0.0000001   ← 低,语序错乱
```

**注意:LM 不是给"是否符合事实"打分,而是给"是否像人话"打分**。`"猫吃了月亮"` 在 LM 看来概率不算太低,因为语法对、词序合理——尽管事实荒谬。

#### 视角 B:下一词预测(next-token prediction)

给定前文,LM 输出**整个词表上的概率分布**:

```
context: "The students opened their ___"

LM 输出:
books    : 0.42
laptops  : 0.20
minds    : 0.05
eyes     : 0.04
phones   : 0.03
...
banana   : 0.0001
(所有词概率加起来 = 1)
```

注意几个关键点:

- 输出是**整个词表**的概率,不是只输出最可能那个词
- 所有概率**加起来等于 1**(softmax 的性质,你 Module 1 已经会了)
- 这本质上就是一个**多分类任务**——类别数 = vocab_size

### 为什么这两个视角等价?

视角 A 用 chain rule(下一节)就能拆成视角 B 的连乘。所以:

> **训练一个能预测下一词的模型 = 训练一个能给整句赋概率的模型**——它们是同一个东西。

### 不要混淆的事

**LM ≠ 聊天 AI**。GPT 这种聊天助手内部确实是 LM,但 LM 这个概念本身**不要求会聊天**。考试问"什么是 LM",答 probability / next-token prediction,不要答 ChatGPT 那种应用层。

### LM 的应用——为什么重要

LM 是很多 NLP 任务的**底座组件**:

- Autocomplete(输入法预测)
- Speech recognition(语音识别——多个候选词谁更像人话)
- Spelling correction(`teh` 还是 `the`?)
- Machine translation(译文谁更流畅)
- Summarization
- Dialogue generation

---

## 2. Chain Rule:句子概率怎么拆

### 公式(必须会写)

```
P(w₁, w₂, ..., wₜ) = ∏ P(wₜ | w₁, ..., wₜ₋₁)
                      t=1 to T
```

**翻译成中文**:整句的概率,等于"每个词在前面所有词都已经出现的条件下出现的概率"的连乘。

### 用一个具体例子拆开

句子 `"I love NLP"`:

```
P("I love NLP")
= P(I)                       ← 第 1 个词无条件出现的概率
× P(love | I)                ← 在 "I" 之后出现 "love" 的概率
× P(NLP | I, love)           ← 在 "I love" 之后出现 "NLP" 的概率
```

每一个 `P(...)` 都是**一个数字**,把它们乘起来就是整句的联合概率。

### 直觉:为什么是连乘?

类比:你要算"连续抛硬币得到 正→正→反"的概率:

```
P(正,正,反) = P(正) × P(正|前一次正) × P(反|前两次正,正)
            = 0.5 × 0.5 × 0.5 = 0.125
```

句子也是一样,只是"硬币"换成了"从词表里选词"。每一步选词的概率,都依赖前面已经选了什么。

### Chain rule 的问题——为什么不能直接用

公式很优雅,但 `P(NLP | I, love)` 这种条件概率怎么算?

最朴素的方法:**数语料库**。

```
P(NLP | I, love) = count("I love NLP") / count("I love")
```

问题来了:

- 语料里出现过 `"I love"` 的句子可能不多
- 出现过 `"I love NLP"` 的句子可能更少
- 如果句子更长,比如 `P(fascinating | I, am, taking, CS6493, this, semester, and, studying, NLP, is, really)`,前缀这么长,**语料里几乎不可能见过完全一样的前文**

**这叫 data sparsity 问题**——历史越长,见过的次数越少,统计越不可靠。

### 解决办法:截断历史 → n-gram

既然完整历史不能用,那就**只看前面几个词**——这就是下一节 n-gram 的核心思想。

---

## 3. n-gram:Markov 假设

### 核心思想

**n-gram 假设**:当前词只依赖前 `n-1` 个词,**忽略更远的历史**。

```
完整 chain rule:
P(wₜ | w₁, ..., wₜ₋₁)        ← 看所有历史

n-gram 近似:
P(wₜ | wₜ₋ₙ₊₁, ..., wₜ₋₁)    ← 只看前 n-1 个词
```

这叫 **Markov assumption**(马尔可夫假设)——**未来只取决于当前状态,不取决于完整历史**。

### 4 种 n-gram

| n | 名字 | 公式 | 直觉 |
|---|---|---|---|
| 1 | Unigram | `P(wₜ)` | 不看前文,只看词本身频率 |
| 2 | Bigram | `P(wₜ \| wₜ₋₁)` | 看前 1 个词 |
| 3 | Trigram | `P(wₜ \| wₜ₋₂, wₜ₋₁)` | 看前 2 个词 |
| 4 | Four-gram | `P(wₜ \| wₜ₋₃, wₜ₋₂, wₜ₋₁)` | 看前 3 个词 |

**记忆**:n-gram 的 n 是"窗口大小",条件部分有 **n-1** 个词。

### 怎么用 count 估计概率(count-based n-gram)

#### Bigram

```
P(wₜ | wₜ₋₁) = count(wₜ₋₁, wₜ) / count(wₜ₋₁)
```

**翻译**:`wₜ₋₁ 后面出现 wₜ` 的次数,除以 `wₜ₋₁` 总共出现的次数。

#### Trigram

```
P(wₜ | wₜ₋₂, wₜ₋₁) = count(wₜ₋₂, wₜ₋₁, wₜ) / count(wₜ₋₂, wₜ₋₁)
```

#### 数字例子

假设你的语料里:

```
"I love" 出现了 100 次
其中 "I love NLP" 出现了 5 次
"I love coding" 出现了 30 次
"I love cats" 出现了 10 次
...

P(NLP | I, love) = count("I love NLP") / count("I love") = 5/100 = 0.05
```

---

## 4. n-gram 手算——HW1 Q2 原型题

### HW1 句子

```
I am taking CS6493 this semester and studying NLP is really fascinating
```

12 个 token。

### 重要:读懂题目

HW1 的题目**不是让你列出所有 n-gram**,而是有特定筛选条件:

> 题目:列出 **second word is `CS6493` or `NLP`** 的 bigrams

这句话的意思——**bigram 的第 2 个位置必须是目标词**。

类似地:

> 列出 **third word is `CS6493` or `NLP`** 的 trigrams

意思——**trigram 的第 3 个位置必须是目标词**。

**这是送分题,但读错题就 0 分**。先看清"哪个位置必须是哪个词"。

### 完整解题

#### Step 1:Tokenize

```
I, am, taking, CS6493, this, semester, and, studying, NLP, is, really, fascinating
```

#### Step 2:Bigram(目标词在第 2 个位置)

Bigram 形式 `(前一个词, 当前词)`,后者必须是 `CS6493` 或 `NLP`。

直接定位目标词,看它前面那个:

```
... taking, CS6493 ...      → (taking, CS6493)
... studying, NLP ...        → (studying, NLP)
```

**答案**:`(taking, CS6493)`, `(studying, NLP)`

#### Step 3:Trigram(目标词在第 3 个位置)

Trigram 形式 `(前两个词, 当前词)`,后者必须是 `CS6493` 或 `NLP`。

定位目标词,看它前面两个:

```
... am, taking, CS6493 ...      → (am, taking, CS6493)
... and, studying, NLP ...       → (and, studying, NLP)
```

**答案**:`(am, taking, CS6493)`, `(and, studying, NLP)`

### 满分答题结构

```
Step 1: Tokenize the sentence by whitespace.
[I, am, taking, CS6493, this, semester, and, studying, NLP, is, really, fascinating]

Step 2: A bigram is (previous word, current word). 
Filtering for second word ∈ {CS6493, NLP}:
- (taking, CS6493)
- (studying, NLP)

Step 3: A trigram is (word_t-2, word_t-1, word_t).
Filtering for third word ∈ {CS6493, NLP}:
- (am, taking, CS6493)
- (and, studying, NLP)
```

**为什么这么写?** 让阅卷老师看出你**理解了筛选规则,不是漏列**。即使最后只有几个答案,也显得有理有据。

---

## 5. n-gram 的 3 大局限——必背的考点

### 局限 1:Sparsity(数据稀疏)

**问题**:可能的 n-gram 组合数量爆炸,但语料里见过的只是九牛一毛。

```
词表 |V| = 50,000

可能的 bigram 数量    = 50,000² = 2.5 × 10⁹      (25 亿)
可能的 trigram 数量   = 50,000³ = 1.25 × 10¹⁴   (125 万亿)
可能的 four-gram 数量 = 50,000⁴ = 6.25 × 10¹⁸   (天文数字)
```

**含义**:n 越大,组合越多,语料越不够。**很多合理的 n-gram 在训练语料里出现 0 次**,导致 count = 0,概率 = 0,但实际上应该有概率。这叫 **curse of dimensionality**(维度灾难)。

### 局限 2:Poor generalization(泛化差)

**问题**:n-gram 依赖**完全匹配**,完全不理解词义相似。

例子:训练语料里只有 `"the cat sat"`,从没见过 `"the dog sat"`。

```
P(sat | the, cat) = 1/1 = 1.0      ← 见过,概率高
P(sat | the, dog) = 0/0 = ???      ← 没见过,概率为 0 或未定义
```

但人类知道 `cat` 和 `dog` 都是动物,行为类似。**n-gram 看不懂这个**——它只看字符串完全一致。

这是 Module 3(embedding)要解决的核心问题:**用 dense vector 让相似词共享信息**。

### 局限 3:Long-range dependency(长距离依赖)

**问题**:Markov assumption 只看前 `n-1` 个词,忽略更远的关键信息。

经典例子:

```
The book that I borrowed from the library yesterday ___ interesting.

正确填空:is(单数动词,因为主语 book 是单数)

trigram 看到的前文: "library yesterday"
                    ↑
                    完全看不出主语是单数还是复数

如果换成 "books"(复数):

The books that I borrowed from the library yesterday ___ interesting.

正确填空:are(复数动词)

但 trigram 看到的还是 "library yesterday",分不出 is 还是 are。
```

**真正决定动词形式的信息(book vs books)在很远处,n-gram 抓不到**。

### 增大 n 解决问题吗?

不能。增大 n 会:
- 捕捉更长上下文 ✓
- **但加剧 sparsity**(组合更爆炸)✗
- **存储成本指数增长** ✗

所以 n-gram 在 n=3 或 n=4 之后基本不再增大。**真正的解决方案是 neural LM**(下一轮)。

### 考场答案模板(必背)

> n-gram models rely on observed counts of exact n-gram contexts. A novel sequence composed of known words may still contain unseen n-grams, causing zero or unreliable probability estimates. The Markov assumption ignores context beyond the previous `n-1` tokens, so long-range dependencies are difficult to model. Increasing `n` captures more context but worsens data sparsity and storage cost due to the curse of dimensionality.

---

## 🧠 Round 1+2 自测题

回答下面 8 题(短答即可):

1. 用一句话定义 language model。
2. 写出 chain rule 的公式(可以用 w1...wT 这种符号)。
3. 为什么 chain rule 在实际中不能直接用?
4. n-gram 的 Markov assumption 是什么?
5. 什么是 trigram?用公式表达。
6. 给定句子 `"NLP is hard but fun"`,列出所有 trigrams(不筛选)。
7. 给定同一句子,**列出第三个位置是 `hard` 的 trigram**。
8. n-gram 的 3 大局限是什么?(关键词即可)

答完我点评后,进 **Round 3:Neural LM 代码题**——这是 HW1 Q2 后半部分的原型,要写 PyTorch 代码。


节约时间，看懂了，继续下一个部分


好,直接进 Round 3。这一部分代码细节多,但核心逻辑你 Module 1 都见过——只是把 forward 流程换了个形状。

---

# Module 2 · Round 3:Neural Language Model

---

## 1. 思想转变:从"查表"到"学函数"

### Count-based n-gram(传统方法)

```
context = "studying"
P(NLP | studying) = count("studying NLP") / count("studying")
                  ↑
                  纯粹查表,数语料里出现次数
```

**优点**:简单,直观,可解释。
**缺点**:你刚学的 3 大局限——sparsity / 不泛化 / 长距离依赖差。

### Neural LM(神经网络方法)

```
context = ["I", "am", "taking"]   (前 3 个词)
   ↓ 转成 id [3, 12, 45]
   ↓ 经过 embedding 变成向量
   ↓ 通过神经网络
   ↓ 输出整个词表上的概率分布
P(下一个词 = "CS6493") = 0.34
P(下一个词 = "the")    = 0.12
...
```

**优点**:
- 通过 embedding **捕捉相似词之间的关系**(`cat` 和 `dog` 向量靠近 → 概率分布相似)
- 不需要见过完全相同的 n-gram,**泛化能力强**
- 可以学到非线性组合

**缺点**:训练成本高,可解释性差。

### 一个关键转变

| | Count-based | Neural |
|---|---|---|
| 知识存在哪 | count table(查表) | 神经网络的参数(可学习) |
| 没见过的组合怎么办 | 概率 = 0(失效) | 仍能给出合理概率(泛化) |
| 词义相似怎么处理 | 完全做不到 | embedding 自动学到 |

**记忆**:Neural LM = embedding + neural network 学 next-token prediction。

---

## 2. Four-gram Neural LM 的结构

### 任务定义

> **Four-gram LM**:用前 3 个词预测第 4 个词。

```
(wₜ₋₃, wₜ₋₂, wₜ₋₁) → wₜ
```

整个模型本质就是一个**多分类器**:
- 输入:前 3 个词
- 输出:词表上的概率分布(类别数 = vocab_size)
- 训练:让模型给"正确的下一词"高概率

### 模型流程图

```
Input: 前 3 个词的 id    [3, 12, 45]
       shape: [context_size]            = [3]
              ↓ 经过 nn.Embedding
Embedding output         [[v1], [v2], [v3]]  
       shape: [context_size, embed_dim] = [3, 64]
              ↓ flatten(把 3 个向量拼成 1 个长向量)
Flattened                [v1 v2 v3 全部拼起来]
       shape: [context_size × embed_dim] = [192]
              ↓ Linear + ReLU
Hidden                   [一个 hidden_dim 维的向量]
       shape: [hidden_dim]              = [128]
              ↓ Linear (映射到 vocab_size)
Output logits            [对每个词的打分]
       shape: [vocab_size]              = [10000]
              ↓ log_softmax(可选)
Log probabilities        [每个词的 log 概率]
       shape: [vocab_size]              = [10000]
```

### 核心区别:为什么要 flatten?

Module 1 你做情感分类,用的是 `mean(dim=1)` 把序列汇总成 1 个向量。

Neural LM 用的是 `flatten`(把多个向量**拼接**成 1 个长向量)。

**为什么不同?**

```
情感分类:
- 不在乎"谁是第一个词,谁是第二个词"
- 只要整句的"平均特征"
- 用 mean pooling 顺序无关

Neural LM:
- 非常在乎顺序!"I am taking" 和 "taking am I" 完全不同
- 需要保留每个位置的信息
- 用 flatten 把 (位置, 词) 都展开放在一个长向量里
```

**Flatten 的几何直觉**:

```
embed 输出:[3, 64]
[
  [v1_1, v1_2, ..., v1_64],     ← 第 1 个词的 64 维向量
  [v2_1, v2_2, ..., v2_64],     ← 第 2 个词的 64 维向量
  [v3_1, v3_2, ..., v3_64]      ← 第 3 个词的 64 维向量
]

flatten:[3 × 64] = [192]
[v1_1, v1_2, ..., v1_64, v2_1, v2_2, ..., v2_64, v3_1, v3_2, ..., v3_64]
 ←─── 第 1 个词 ───→   ←─── 第 2 个词 ───→   ←─── 第 3 个词 ───→
```

**3 行 × 64 列变成 1 行 × 192**——所有数字按顺序排成一长串。位置信息通过"在长向量中的位置"保留下来。

---

## 3. 完整 PyTorch 代码——逐行解读

### 代码

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class LanguageModeler(nn.Module):
    def __init__(self, vocab_size, embedding_dim, context_size, hidden_size=128):
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.linear1 = nn.Linear(context_size * embedding_dim, hidden_size)
        self.linear2 = nn.Linear(hidden_size, vocab_size)

    def forward(self, inputs):
        # inputs: [context_size], 即前 3 个词的 id
        embeds = self.embeddings(inputs).view((1, -1))     # ← 关键
        out = F.relu(self.linear1(embeds))
        out = self.linear2(out)
        log_probs = F.log_softmax(out, dim=1)
        return log_probs
```

### 逐行解读

#### `__init__` 部分:定义模型有哪些层

```python
self.embeddings = nn.Embedding(vocab_size, embedding_dim)
# 词表里每个词都有一个 embedding_dim 维向量
# 例:vocab_size=10000, embedding_dim=64 → 表的形状 [10000, 64]
```

```python
self.linear1 = nn.Linear(context_size * embedding_dim, hidden_size)
# 第一个全连接层:把 flatten 后的长向量 → hidden vector
# 例:context_size=3, embed_dim=64 → 输入 192 维,输出 128 维
```

```python
self.linear2 = nn.Linear(hidden_size, vocab_size)
# 第二个全连接层(分类头):hidden vector → 词表上的 logits
# 例:128 维 → 10000 维
```

#### `forward` 部分:数据流

```python
embeds = self.embeddings(inputs).view((1, -1))
```

这一行做了两件事:

**(a) `self.embeddings(inputs)`** ——查 embedding 表
```
inputs 是 [3, 12, 45],shape [3]
查表后:shape [3, 64]
```

**(b) `.view((1, -1))`** ——reshape

`view` 是 reshape 操作。`(1, -1)` 的意思:
- 第 0 维固定为 1
- 第 1 维 `-1` 表示**自动计算**(让总元素数不变)

```
原 shape [3, 64],总共 3×64 = 192 个元素
reshape 成 (1, -1):
- 第 0 维 = 1
- 第 1 维 = 192 / 1 = 192
- 结果 shape: [1, 192]
```

这就是 **flatten** 的实现。把 [3, 64] 的二维矩阵摊平成 [1, 192] 的"一行 192 列"。

**为什么前面要加个 1?** 因为 `nn.Linear` 的输入要求是 `[batch, features]`——必须有 batch 维度。这里假设 batch=1,所以加上去。

#### 接下来的处理

```python
out = F.relu(self.linear1(embeds))     # [1, 192] → Linear(192,128) → [1, 128] → ReLU
out = self.linear2(out)                # [1, 128] → Linear(128, 10000) → [1, 10000]
log_probs = F.log_softmax(out, dim=1)  # 把 logits 转成 log probabilities
return log_probs                        # [1, 10000]
```

`dim=1` 表示沿着词表那一维做 log_softmax(让 10000 个数变成 log 概率)。

### 一个考场坑:`view((1, -1))` 只能 batch=1

```python
embeds = self.embeddings(inputs).view((1, -1))
```

这写法**只对 batch_size=1 的输入成立**。如果你想 batch training:

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

**考场如果让你改代码支持 batch,这就是改的地方**。

---

## 4. Loss 函数选择——一个高频考点

PyTorch 提供两种损失函数,选哪个取决于**模型输出是什么**:

### 情况 A:输出 raw logits(没做 softmax)

```python
out = self.linear2(out)
return out                      # 直接返回 logits
```

配 `nn.CrossEntropyLoss()`(内部已含 log_softmax + NLL):

```python
loss_fn = nn.CrossEntropyLoss()
loss = loss_fn(logits, target)
```

### 情况 B:输出 log probabilities(做了 log_softmax)

```python
out = self.linear2(out)
log_probs = F.log_softmax(out, dim=1)
return log_probs                # 返回 log 概率
```

配 `nn.NLLLoss()`(只做 NLL,不再做 log_softmax):

```python
loss_fn = nn.NLLLoss()
loss = loss_fn(log_probs, target)
```

### 速记表(必背)

| 模型输出 | 用什么 Loss | 关系 |
|---|---|---|
| raw logits | `CrossEntropyLoss` | CE = log_softmax + NLL(内部已合并) |
| log_softmax 后 | `NLLLoss` | NLL 只做最后一步 |

**两条路殊途同归,数学上完全等价**——但**不能混用**:
- ❌ logits + NLLLoss → 错(NLL 不会做 log_softmax)
- ❌ log_probs + CrossEntropyLoss → 等于做了**两次** log_softmax,梯度坏掉

上面那段代码 `LanguageModeler` 输出 `log_probs`,所以应该用 `NLLLoss`。

---

## 5. Training Loop——和 Module 1 几乎一样

```python
losses = []

for epoch in range(num_epochs):
    total_loss = 0
    for context, target in training_data:
        # context: 一个由前 3 个词构成的 list,例如 ["I", "am", "taking"]
        # target:  正确答案,例如 "CS6493"
        
        # Step 1:把词转成 id
        context_idxs = torch.tensor(
            [word_to_ix[w] for w in context],
            dtype=torch.long                      # ← Embedding 必须吃 long
        )
        target_idx = torch.tensor([word_to_ix[target]], dtype=torch.long)
        
        # Step 2:标准 5 步训练循环 (Z F L B S)
        optimizer.zero_grad()                     # Z
        log_probs = model(context_idxs)           # F
        loss = loss_function(log_probs, target_idx)  # L
        loss.backward()                           # B
        optimizer.step()                          # S
        
        total_loss += loss.item()
    losses.append(total_loss)
```

**和 Module 1 的对比**:

| Module 1 情感分类 | Module 2 Neural LM |
|---|---|
| 输入:整句 token id | 输入:前 3 个词 id |
| 输出:`[batch, 2]`(neg/pos) | 输出:`[1, vocab_size]`(每个词概率) |
| 类别数 = 2 | 类别数 = vocab_size(可能上万) |
| pooling 用 mean | pooling 用 flatten |

**核心机制完全相同**,只是参数变了。这就是为什么 Module 1 学扎实了 Module 2 这一步会很快。

---

## 6. Training Examples 怎么生成

### 公式

> **句子有 T 个 token,four-gram LM 能生成 T - 3 个训练样本。**

### HW1 句子例子

```
Sentence:
I am taking CS6493 this semester and studying NLP is really fascinating

Tokens (T=12):
w1=I, w2=am, w3=taking, w4=CS6493, w5=this, w6=semester,
w7=and, w8=studying, w9=NLP, w10=is, w11=really, w12=fascinating

Training examples (T-3 = 9 个):
(I, am, taking)             → CS6493
(am, taking, CS6493)        → this
(taking, CS6493, this)      → semester
(CS6493, this, semester)    → and
(this, semester, and)       → studying
(semester, and, studying)   → NLP
(and, studying, NLP)        → is
(studying, NLP, is)         → really
(NLP, is, really)           → fascinating
```

**生成方式**:**滑动窗口**——每次窗口向右移 1 位。前 3 个词作为 context,第 4 个词作为 target。

### 通用公式

| n-gram | 训练样本数(T 个 token) | 形式 |
|---|---|---|
| Bigram (n=2) | T - 1 | (wₜ₋₁) → wₜ |
| Trigram (n=3) | T - 2 | (wₜ₋₂, wₜ₋₁) → wₜ |
| Four-gram (n=4) | T - 3 | (wₜ₋₃, wₜ₋₂, wₜ₋₁) → wₜ |
| n-gram | T - (n-1) | (前 n-1 个词) → wₜ |

---

## 7. Embedding Dimension 怎么选——开放题答法

考试可能问:`embedding_dim` 选 32 / 64 / 128 哪个好?为什么?

### 三个维度的对比(必背 trade-off 表)

| Dim | Capacity(表达能力) | Cost(训练成本) | Generalization(泛化) |
|---|---|---|---|
| 32 | 低,可能 underfit | 小,训练快 | 小数据下稳,但表达有限 |
| 64 | 中等 | 中等 | 小型作业的常见平衡选择 |
| 128 | 高,更 expressive | 大,训练慢 | 数据少时可能 overfit |

### 三个核心 trade-off

1. **Capacity**(表达能力):dim 越大,每个词能装的语义信息越多
2. **Cost**(成本):dim 越大,参数越多(`vocab_size × dim`),训练更慢、占内存多
3. **Overfitting risk**:dim 越大,训练数据少时越容易过拟合

### 考场答案模板

> Increasing embedding dimension increases model capacity because each word has a richer dense representation. However, it also increases memory and computation cost (parameters scale as vocab_size × dim). On a small corpus, a large embedding dimension may overfit, while a very small dimension may underfit. The best choice should be selected based on validation performance, vocabulary size, corpus size, and task complexity.

**关键词**:capacity / cost / overfit / underfit / validation。

---

## 8. RNN / LSTM——为什么后来不用 Neural n-gram 了

Neural LM 比 count-based 强,但还是有个根本问题:**固定窗口**。

```
Four-gram LM:只能看前 3 个词
Five-gram LM:只能看前 4 个词
...

句子真实需要的依赖可能跨越 20 个词,固定窗口模型抓不到。
```

### RNN(Recurrent Neural Network)

**思想**:每读一个词,更新一个"hidden state"——这个 state 携带了之前所有的信息。

```
h_t = f(x_t, h_{t-1})                    ← 当前 hidden = 当前输入 + 上一个 hidden 的函数
y_t = softmax(W h_t + b)                 ← 用当前 hidden 预测当前 token
```

**优点**:
- 可处理**变长输入**(不像 four-gram 死定 3 个词)
- 模型大小不随序列长度增长(同一组权重在每一步重复使用)
- 理论上可以记住任意远的历史

**缺点**:
- **顺序计算**(必须一步一步来,不能并行)
- 长序列上**梯度消失**(vanishing gradient),模型其实记不住很远的东西

### LSTM(Long Short-Term Memory)

**LSTM 是 RNN 的改进版**,加了 3 个"门"(gates)来控制信息流:

| Gate | 作用 |
|---|---|
| **Input gate** | 控制写入多少新信息 |
| **Forget gate** | 控制遗忘多少旧信息 |
| **Output gate** | 控制输出多少 memory |
| **Cell state** | 更稳定地保存长期信息 |

**优点**:相比 vanilla RNN 缓解 vanishing gradient,能记住更远的历史。
**缺点**:仍然是顺序计算,不如 Transformer 并行。

### 模型对比表(必背)

| Model | Context | 优点 | 缺点 |
|---|---|---|---|
| n-gram (count) | 固定前 n-1 个词 | 简单可解释,易手算 | 稀疏,长距离差 |
| Feed-forward Neural LM | 固定窗口 | 有 embedding,能泛化 | 仍然固定 context |
| RNN LM | 理论无限历史 | 变长输入 | 顺序计算,长序列梯度消失 |
| LSTM LM | gates 保留长期信息 | 缓解梯度消失 | 顺序计算,不并行 |

### 后续(Module 4 预告)

Transformer 解决了 RNN/LSTM "顺序计算不能并行" 的根本问题——靠的是 **attention 机制**。这是 Module 4 的内容,你现在不需要懂 attention,但要知道**模型演化的逻辑**:

```
n-gram(查表)
   ↓ 解决泛化
Neural n-gram(固定窗口)
   ↓ 解决固定窗口
RNN
   ↓ 解决梯度消失
LSTM
   ↓ 解决顺序计算
Transformer / BERT / GPT
```

---

## 🧠 Round 3 自测题

回答这 7 题:

1. Neural LM 相比 count-based n-gram,核心优势是什么?(用一两个关键词)

2. 在 Four-gram Neural LM 里,`flatten` 这一步在做什么?为什么不像 Module 1 那样用 mean pooling?

3. 模型代码这一行 `embeds = self.embeddings(inputs).view((1, -1))`——`view((1, -1))` 在做什么?为什么第二个参数是 `-1`?

4. 如果模型最后做了 `F.log_softmax(out, dim=1)`,应该用 `CrossEntropyLoss` 还是 `NLLLoss`?为什么?

5. 句子 `"NLP is really fun and useful"`(6 个 token),trigram(n=3) Neural LM 能生成几个训练样本?写出来。

6. embedding_dim 从 32 增加到 128,有什么好处和代价?(各 1 句)

7. 为什么 RNN 比 Neural n-gram 在长距离依赖上更好?它本身又有什么问题?

答完进 **Round 4:Cross Entropy + Perplexity**——Module 2 最后一站。

softmax，log_softmax，NLL，CrossEntropyLoss 我已经混淆了。
接下来带我复习期末例题和作业2的答案，我就要去考试了

好，**优先级切换**——你现在要去考试，不能再按 module 顺序慢慢推。我们做两件事：

1. **先彻底澄清 softmax / log_softmax / NLL / CrossEntropyLoss**——这是后面所有代码题的基础
2. **然后逐题复习期末例题 + HW2**

---

# Part A:Softmax 家族彻底搞清楚

这里**只有 4 个东西**，但很多教程把它们绕在一起。我用一张图让你死记。

## 1. 完整链条:从 logits 到 loss

```
Step 1: 模型输出 logits         [2.0, 1.0, 0.1]
              ↓ softmax
Step 2: probabilities           [0.659, 0.242, 0.099]    ← 加起来 = 1
              ↓ log
Step 3: log probabilities       [-0.417, -1.418, -2.312] ← 全是负数
              ↓ NLL(取真实标签那一位的负值)
Step 4: loss                    标量,如 1.418
```

**4 步,4 个名字**。

## 2. 一张表说清楚

| 函数 | 输入 → 输出 | 一句话作用 |
|---|---|---|
| **`softmax`** | logits → probabilities | 让数字变成概率(归一化) |
| **`log_softmax`** | logits → log probabilities | softmax 后再取 log,**一步合并** |
| **`NLLLoss`** | log probabilities + 真实标签 → loss | 取真实标签那一位的 log_prob,加负号 |
| **`CrossEntropyLoss`** | logits + 真实标签 → loss | log_softmax + NLL 的**合二为一** |

## 3. 数学上的关系——记住这个等式

```
CrossEntropyLoss(logits, target) = NLLLoss(log_softmax(logits), target)
```

**两条路殊途同归**:

```
路径 A (常用):
logits ──CrossEntropyLoss──→ loss
       (内部自动做 log_softmax + NLL)

路径 B (HW1 Q2 那段代码用的):
logits ──log_softmax──→ log_probs ──NLLLoss──→ loss
                       (手动分两步)
```

**结果完全一样**,数学上等价。

## 4. 为什么有 NLL 这种"奇怪"的损失?

**NLL = Negative Log Likelihood**(负对数似然)。

直觉:模型给真实答案的概率越高,loss 越小。

```
真实标签的概率 p     -log(p) = NLL
1.0 (完美)          0           ← loss 最小
0.5                 0.693
0.1                 2.303
0.01                4.605
0.001               6.908       ← 越错,loss 越大
```

**为什么取负号?** 因为 `log` 把 `(0,1]` 之间的概率映射到 `(-∞, 0]`,都是负数。我们希望"越错 loss 越大",所以加负号变正。

## 5. 为什么有 log_softmax?

**数值稳定性**。

如果先做 softmax 再 log:
```python
probs = softmax(logits)        # 可能极小,如 1e-50
log_probs = log(probs)         # log(1e-50) → 数值溢出
```

`log_softmax` **数学上把这两步合成一个公式,避免中间值过小**:

```
log_softmax(x_i) = x_i - log(Σ exp(x_j))
                   ↑
                   直接对 logits 做运算,不会溢出
```

考试不要求你证明,但要知道:**`log_softmax` 比 `softmax` + `log` 更稳定**,所以工程上常用。

## 6. 三种代码组合——必背选择

| 模型最后输出 | 用什么 Loss | 对错 |
|---|---|---|
| **logits**(没做 softmax) | `CrossEntropyLoss` | ✓ 标准做法 |
| **log_softmax 后**(log_probs) | `NLLLoss` | ✓ HW1 Q2 那种写法 |
| **softmax 后**(probabilities) | `CrossEntropyLoss` | ✗ **错!**等于 softmax 两次 |
| **softmax 后** | `NLLLoss` | ✗ **错!**NLLLoss 期待的是 log_probs 不是 probs |
| **logits** | `NLLLoss` | ✗ **错!**NLLLoss 不会自己做 log_softmax |

## 7. 一秒记忆口诀

> - **CrossEntropyLoss 配 logits**(让 CE 自己做 log_softmax)
> - **NLLLoss 配 log_softmax 后的 log_probs**(各做一半)
> - **永远不要在 loss 前自己做 softmax**(无论用哪个 loss 都错)

记住这三句,这个家族就过了。

---

# Part B:HW2 Question 3 代码 bug 题——直接练手

你刚发的 image 3 就是这种题。我们走一遍。

## 题目代码

```python
class SentimentClassificationBERT(nn.Module):
    def __init__(self, bert_version, num_class):
        super().__init__()
        self.bert = BertModel.from_pretrained(bert_version)
        hidden_size = self.bert.config.hidden_size
        self.linear_decoder = nn.Linear(hidden_size, num_class)
    
    def forward(self, input_ids, attention_mask):
        sequence_output, pooled_output = self.bert(input_ids=input_ids,
                                                    attention_mask=attention_mask)
        logits = self.linear_decoder(sequence_output)   # ← bug 在这里
        return logits
```

## Bug 分析(满分答案)

### Bug 1:用错了 BERT 的输出

BERT 的两个输出:

```
sequence_output : shape [batch, seq_len, hidden_size]
                  ↑
                  每个 token 一个向量(token-level representation)
                  
pooled_output   : shape [batch, hidden_size]
                  ↑
                  整句一个向量(sentence-level,通常对应 [CLS] token)
```

代码用了 `sequence_output`(每个 token 一个向量),但**情感分类是句子级任务**,应该用 `pooled_output`(整句一个向量)。

**用 sequence_output 的后果**:
```
sequence_output       : [batch, seq_len, hidden_size]   例 [4, 10, 768]
   ↓ Linear(hidden, num_class)
linear_decoder output : [batch, seq_len, num_class]     例 [4, 10, 2]
                                ↑
                                每个 token 一个 logits,不是整句一个
                                和 batch_y [batch] 形状对不上,loss 算不了
```

### 修正

```python
logits = self.linear_decoder(pooled_output)
```

或者你也可以**取 sequence_output 的第一个 token([CLS] 位置)**:

```python
logits = self.linear_decoder(sequence_output[:, 0, :])
```

两种写法都对——pooled_output 在 BERT 内部就是经过一个 tanh 的 [CLS] 表示。

### 满分答题模板

> The code uses `sequence_output` (shape `[batch, seq_len, hidden_size]`), which contains a vector per token. For sentence-level sentiment classification, the model needs a single vector per sentence. The fix is to use `pooled_output` (shape `[batch, hidden_size]`), which is the [CLS] token's representation summarizing the whole sentence:
> 
> ```python
> logits = self.linear_decoder(pooled_output)
> ```
>
> Otherwise, the output shape `[batch, seq_len, num_class]` cannot be matched with the target shape `[batch]` in `CrossEntropyLoss`.

**关键得分点**:
- 指出 sequence_output vs pooled_output 的 shape 区别
- 解释情感分类是句子级任务
- 给出修复代码

---

# Part C:HW2 全卷快速过

我先帮你按**重要性 + 难度**重新排序,你说哪部分先看。先选一下,**点选项最快**。

不过我看你上传的 PDF 是 **HW2 的 solution(已经有答案了)**,那个不是练习题——是**参考答案**。所以策略应该是:

- **HW2 的题型**(在 solution 里能反推):重点理解每道题的**答题结构**
- **期末例题**(image 1, 2, 3):是真正没做过的,需要现场想

我建议优先级:

1. **Image 1(CRB Chatbot 设计)**:22 分大题,涵盖整个 NLU/NLG/dialogue 系统设计——这是**最综合的考试题型**
2. **Image 2(distributional hypothesis / skip-gram / RNN for NER)**:15 分,word representation 核心
3. **Image 3(BERT 代码 bug)**:5 分,**已经讲完了**
4. HW2 BLEU / Beam search 手算:工程性强,**很可能直接出现在期末**

---

# 我现在直接开始 Image 1(CRB Chatbot)——边讲你边问

如果你需要 Image 2 / BLEU 手算先讲,选项里选,我立刻切换。

否则我开始 **Question 1: CRB Chatbot 系统设计**(22 分)。这道题如果你没系统学过 dialogue system,**完全可以现场推**——但需要正确的术语框架。

要不要我直接开讲 Image 1?如果你时间紧到不能选,直接说"开讲"我就开始。

Q: 你剩下多少时间? 哪些题你最不掌握?
A: 主讲期末例题 image 1 2 3，从image 1 开始


# 期末例题 Image 1:CRB Chatbot 系统设计(22 分)

这是综合性最强的一道题——如果你能把这道题的框架建立起来,**Module 5(NLU)+ Module 6(NLG/Dialogue)+ Module 8(Agents)的核心都覆盖了**。

---

## 题目重述(便于你考试时识别题型)

> 香港政府让人填表自报 COVID-19 检测结果。我们要设计一个 **task-oriented dialogue system**(任务型对话系统),让用户通过聊天自动上报。这个系统叫 **CRB(COVID-19 Reporting roBot)**。

**关键词**:**task-oriented dialogue system**(不是闲聊机器人)。

**Task-oriented vs open-domain** 的区别(可能的小考点):

| Task-oriented | Open-domain |
|---|---|
| 完成具体任务(订餐、报检测结果) | 闲聊、陪伴 |
| 有明确的 slot 要填 | 没有固定结构 |
| CRB 属于这种 | ChatGPT 闲聊属于这种 |

---

## 1.1 NLU 三大任务(9 分)——这一题是送分题但要结构对

题目要求解释:在 CRB 系统里,什么是 domain classification、intent detection、slot filling,**并设计 5 个合理的 slot**。

### 三个任务的标准定义(必背)

#### Domain Classification(领域分类)

**定义**:判断用户说的话属于哪个**领域/话题**。

**直觉**:一个大型对话系统可能服务多个领域(订餐 / 订机票 / 医疗咨询)。第一步要判断"这句话属于哪个业务"。

**在 CRB 里**:
- 输入:用户说的话,如 `"I want to report my test result"`
- 输出:domain = `COVID-19 reporting`(而不是 `weather`、`booking`、`general chat`)
- 本质:**多分类**,类别是预定义的领域集合

#### Intent Detection(意图识别)

**定义**:在确定 domain 之后,判断用户**具体想做什么**。

**直觉**:同一个 domain 下可能有多种动作。比如 COVID 领域可能有"报告结果"、"查询状态"、"取消报告"等。

**在 CRB 里**:
- 输入:`"I tested positive yesterday"`
- 输出:intent = `report_test_result`(而不是 `cancel_report`、`query_history`)
- 本质:**多分类**,类别是预定义的意图集合

#### Slot Filling(槽位填充)

**定义**:从用户的话里**抽取出关键信息**填进预定义的"槽位"里。

**直觉**:要完成报告任务,必须知道几个具体信息——什么时候测的?结果是阴是阳?谁测的?这些"必须知道的字段"叫 **slot**。

**在 CRB 里**:
- 输入:`"I am John Smith, my HKID is A123456, I tested positive on Nov 25 using a rapid antigen test"`
- 输出:
  - `name`: John Smith
  - `HKID`: A123456
  - `test_result`: positive
  - `test_date`: Nov 25
  - `test_type`: rapid antigen test
- 本质:**序列标注问题**(对每个 token 标 BIO 标签)或 **span extraction**

### 设计 5 个合理的 slot

题目要求**至少 5 个**。CRB 是上报检测结果,合理的 slot:

| Slot | 类型 | 例子 |
|---|---|---|
| `name` | 人名 | John Smith |
| `HKID` / `ID_number` | 字符串 | A123456 |
| `test_date` | 日期 | 2024-11-25 |
| `test_result` | 枚举(positive / negative) | positive |
| `test_type` | 枚举(PCR / RAT / 其他) | rapid antigen test |
| `symptoms`(可选) | 列表 | cough, fever |
| `contact_info`(可选) | 电话/邮箱 | 9876-5432 |

**5 个就够**,选最核心的 5 个。

### 1.1 满分答题模板(9 分)

> In a task-oriented dialogue system, NLU consists of three subtasks:
> 
> **(1) Domain classification** identifies which application domain the user's utterance belongs to. In CRB, the domain is "COVID-19 test reporting", distinguishing it from other domains like booking or general chat.
> 
> **(2) Intent detection** identifies what the user wants to do within the domain. In CRB, possible intents include `report_test_result`, `query_status`, `cancel_report`, etc. The user utterance "I tested positive yesterday" maps to the `report_test_result` intent.
> 
> **(3) Slot filling** extracts key information from the utterance into predefined slots. For the CRB system, five reasonable slots are:
> - `name` (the user's name)
> - `HKID` (Hong Kong ID number)
> - `test_date` (date of the test)
> - `test_result` (positive / negative)
> - `test_type` (PCR / rapid antigen test)
> 
> For example, given "I am John, my HKID is A123456, I tested positive on Nov 25 using PCR", slot filling extracts: name=John, HKID=A123456, test_result=positive, test_date=Nov 25, test_type=PCR.

**得分点**:
- 三个定义清晰
- 都举了 CRB 例子
- 5 个具体 slot
- 给了一个完整的输入→输出例子

---

## 1.2 NLU 之后的下一步(9 分)——必须答出 4 个组件

题目问:NLU 之后,要完成"closed-loop system"(闭环系统),还需要哪些任务/模块?

**关键词**:closed-loop = 用户输入 → 系统理解 → 系统决策 → 系统响应 → 用户继续输入。**必须形成循环**。

### Task-oriented dialogue system 的 4 大组件(必背)

```
用户输入
   ↓
1. NLU (Natural Language Understanding)        ← 1.1 已经讲了
   - Domain classification
   - Intent detection
   - Slot filling
   ↓ (intent + slots)
2. DST (Dialogue State Tracking) [可选独立模块]
   - 跟踪当前对话状态:已经填了哪些 slot,还差哪些
   ↓ (current state)
3. DPL (Dialogue Policy Learning) / Dialogue Manager
   - 决定系统下一步要做什么(询问缺的 slot? 确认信息? 完成任务?)
   ↓ (system action)
4. NLG (Natural Language Generation)
   - 把 system action 变成自然语言回复
   ↓
系统回复 → 用户继续输入(回到顶部,形成闭环)
```

### 用 CRB 例子串一遍

```
Turn 1
用户: "I want to report my test result"

NLU:  
  domain   = COVID reporting
  intent   = report_test_result
  slots    = {} (一个都没填)

DST:
  state = {filled: {}, missing: [name, HKID, test_date, test_result, test_type]}

DPL:
  action = ask(name)

NLG:
  "Sure, may I have your name first?"

────────────────────────
Turn 2
用户: "I'm John Smith"

NLU:
  intent = inform
  slots  = {name: John Smith}

DST:
  state = {filled: {name: John Smith}, missing: [HKID, ...]}

DPL:
  action = ask(HKID)

NLG:
  "Thanks, John. Could you please provide your HKID?"

────────────────────────
... 继续直到所有 slot 填满 ...

Turn N
DST: state = {filled: {全部}, missing: []}
DPL: action = confirm + submit
NLG: "I have all your information. Let me confirm: ... Submit?"
用户: "Yes"
NLG: "Your report has been submitted. Reference number: ABC123."
```

**这就是 closed-loop**——NLU 理解 → DST 跟踪 → DPL 决策 → NLG 生成 → 用户继续输入。

### 1.2 满分答题模板(9 分)

> After NLU, a closed-loop task-oriented dialogue system needs three more modules:
>
> **(1) Dialogue State Tracking (DST)** maintains the current state of the conversation, including which slots have been filled and which are still missing. After each user utterance, DST updates the state by combining new NLU output with previous context. In CRB, DST tracks how many of {name, HKID, test_date, test_result, test_type} have been collected.
>
> **(2) Dialogue Policy Learning (DPL)** decides what action the system should take next based on the current state. Possible actions include: asking for a missing slot, confirming a filled slot, or completing the task. In CRB, if `test_date` is missing, DPL outputs the action `ask(test_date)`.
>
> **(3) Natural Language Generation (NLG)** converts the system action into a natural language response. For example, the action `ask(test_date)` might be generated as "When did you take the test?". The response is then sent back to the user, and the loop continues until all required slots are filled and the report is submitted.
>
> Together with NLU, these four modules form a closed loop: User → NLU → DST → DPL → NLG → User.

**得分点**:
- 4 大组件全部出现(NLU + DST + DPL + NLG)
- 每个都说清楚输入输出
- 用 CRB 例子具体化
- 强调"闭环"

---

## 1.3 评价指标(4 分)——只要 2 个,但要解释好

Task-oriented dialogue 评价指标分两层。

### 两类指标(必须知道这个二分)

#### 类别 A:Component-level(模块级别)

评价**单个模块**的好坏:

| 指标 | 评价什么 | 怎么算 |
|---|---|---|
| **Slot filling F1** | 槽位填充准不准 | 提取的 slot 和 ground truth 比 |
| **Intent classification accuracy** | 意图识别对不对 | 预测意图 vs 真实意图 |
| **Domain classification accuracy** | 领域分类对不对 | 同上 |

#### 类别 B:End-to-end / Task-level(整体任务)

评价**整个对话系统**最终表现:

| 指标 | 评价什么 | 直觉 |
|---|---|---|
| **Task completion rate / Task success rate** | 用户的任务成功完成的比例 | 用户报告 100 次,90 次成功提交 → 90% |
| **Dialogue turns / Average turns to completion** | 平均要几轮才能完成 | 越少越好(用户不耐烦) |
| **User satisfaction** | 用户主观打分 | 通常 1-5 分 |

### 选哪两个写?

**最稳的组合**:1 个 component-level + 1 个 end-to-end。这样显示你**理解评价的两个层次**。

我推荐:**Slot Filling F1** + **Task Completion Rate**。

### 1.3 满分答题模板(4 分)

> CRB system performance can be evaluated on two levels:
>
> **(1) Slot Filling F1 (component-level):** Measures how accurately the NLU module extracts the required slots. F1 is the harmonic mean of precision (extracted slots that are correct) and recall (correct slots that were extracted). For CRB, this evaluates whether name, HKID, test_date, test_result, and test_type are correctly captured from user utterances.
>
> **(2) Task Completion Rate (end-to-end):** Measures the proportion of user sessions where the report is successfully submitted with all required slots correctly filled. For example, if 100 users use CRB and 90 successfully submit complete reports, the task completion rate is 90%. This directly reflects whether the system fulfills its purpose.

**得分点**:
- 两个不同层次的指标
- 解释清楚怎么算
- 给具体数字例子(90/100)

---

## 整道 Q1 答题策略

| 子题 | 分数 | 答题时间 | 关键得分点 |
|---|---|---|---|
| 1.1 NLU 三任务 + 5 slot | 9 | ~10 分钟 | 三个定义 + CRB 实例 + 5 具体 slot |
| 1.2 closed-loop 模块 | 9 | ~10 分钟 | DST + DPL + NLG 三个模块 + 闭环关系 + CRB 例子 |
| 1.3 两个评价指标 | 4 | ~5 分钟 | 一个 component 一个 end-to-end |

**写答题的元策略**:
- 用编号 (1) (2) (3) 而不是大段散文
- 每个概念**先定义,再举 CRB 例子**
- 用 `→` 或 流程图箭头展示组件之间的关系

---

## 🧠 快速自测(Q1)

凭记忆答(短答即可):

1. NLU 的三个子任务是什么?
2. 在 CRB 里,`"I tested positive on Nov 25"` 经过 slot filling 后输出什么?
3. Closed-loop dialogue system 的 4 大组件按顺序是什么?
4. DST 和 DPL 的区别是什么?(一句话)
5. Task completion rate 和 slot filling F1 各评价什么层级?

答完直接进 **Image 2(distributional hypothesis / skip-gram / RNN for NER)** —— Module 3 + Module 4 内容。

如果你时间紧到不想答自测题,直接说"继续",我开 Image 2。


继续


# 期末例题 Image 2:Word Representation + Skip-gram + RNN(15 分)

这道题考三个独立知识点,各自独立——你逐个击破即可。

---

## 2.1 Distributional Hypothesis + ELMo vs Word2Vec(4 分)

### 第一问:什么是 distributional hypothesis?

**核心论断**(必背英文):

> **"You shall know a word by the company it keeps."** — J.R. Firth

意思:**一个词的含义可以从它出现的上下文推断出来**。

**直觉**:
- 你看到一个新词 `wug`,但不知道它什么意思
- 如果它总是出现在 `"I drank a glass of ___"` 后面 → 它大概是某种饮料
- 如果它总是出现在 `"The ___ ran across the field"` → 它大概是某种动物

**这就是所有 word embedding 方法的理论基础**——Word2Vec / GloVe / BERT 全都建立在这个假设上。

### 第二问:ELMo 解决了什么 word2vec/GloVe 解决不了的问题?

**核心问题**:**context-independent vs context-dependent**(也叫 static vs contextualized)。

#### Word2Vec / GloVe 的问题:静态表示

```
"I deposited money in the bank"        ← bank = 银行
"I sat on the river bank"               ← bank = 河岸

word2vec 给 "bank" 分配的向量:只有一个,无论上下文怎么变。
→ 同一个向量被迫表示两个完全不同的意思
→ 这叫 polysemy(一词多义)无法处理
```

**Word2Vec 的本质**:每个词 → **固定**向量。训练完之后,`bank` 的向量就钉死了。

#### ELMo 的解决方案:contextualized representation

```
"I deposited money in the bank"        ← ELMo 给 "bank" 一个偏向"金融"语义的向量
"I sat on the river bank"               ← ELMo 给 "bank" 一个偏向"地理"语义的向量
```

**ELMo 的本质**:每个词在**不同上下文中**得到**不同**向量。词向量不再是查表,而是**根据当前句子动态生成**。

ELMo 的实现方式:用**双向 LSTM** 读整句,每个 token 的表示由整个句子的上下文决定。

### 2.1 满分答题模板(4 分)

> The **distributional hypothesis** states that words appearing in similar contexts tend to have similar meanings—"you shall know a word by the company it keeps." This forms the theoretical basis of word embedding methods.
>
> **Word2Vec and GloVe produce context-independent (static) representations**: each word is mapped to a single fixed vector regardless of the sentence it appears in. This fails on polysemy: the word "bank" has the same vector in "river bank" and "money in the bank", forcing one vector to represent two unrelated senses.
>
> **ELMo solves this by producing contextualized representations**: the vector for each word is dynamically computed from the entire sentence using a bi-directional LSTM. The same word "bank" gets different vectors in different contexts, capturing the appropriate sense for each occurrence.

**关键得分词**:context-independent / contextualized / polysemy / bi-directional LSTM。

---

## 2.2 Skip-gram 训练慢 + 加速方法(6 分)

### 先快速复习 Skip-gram(如果你忘了)

**Skip-gram 任务**:用**中心词**预测**上下文窗口里的每个词**。

```
句子: "the quick brown fox jumps"
中心词: brown
上下文窗口(window=2): the, quick, fox, jumps

训练样本:
brown → the
brown → quick
brown → fox
brown → jumps
```

**模型结构**:每个样本就是个分类任务,类别数 = vocab_size。

```
中心词 id → embedding → linear → softmax over V → 概率分布
                                              ↑
                                              vocab_size 维
```

### 第一问:为什么训练慢?

**核心问题**:**输出层 softmax 要算整个词表,计算量正比于 |V|**。

```
softmax(x_i) = exp(x_i) / Σ exp(x_j)
                            ↑
                         j 从 1 到 |V|

如果 |V| = 50,000,每次 forward 都要算 50,000 个 exp 然后求和。
每次 backward 还要更新 |V| × embed_dim 的输出层权重矩阵。
```

**每个训练样本都要这样做一次**——大语料里有数百万个样本,加起来就慢得不可接受。

**形象点说**:你要预测正确答案是哪一个,但你必须告诉模型"其他 49,999 个都不是"——这个"告知所有错误答案"的开销,就是慢的根源。

### 第二问:怎么加速?三种方法(任选一个深入解释即可)

#### 方法 1:Negative Sampling(最常考)

**思想**:不再计算"正确答案 vs 所有其他词",而是"正确答案 vs **少量随机抽样的负例**"。

```
原来:
正样本 (brown, fox)        ← target = 1
对比所有 49,999 个负样本    ← 巨大计算量

Negative Sampling:
正样本 (brown, fox)        ← target = 1
随机抽 5 个负样本(brown, water), (brown, glass), ...    ← target = 0
                                                            
只用这 6 个样本(1 正 + 5 负)训练,而不是整个词表
```

**计算量**:`O(k+1)` 而不是 `O(|V|)`(k 通常是 5-20)。

**Loss 函数**:不再是 softmax + cross entropy,而是**多个二元分类**(每个用 sigmoid)。

#### 方法 2:Hierarchical Softmax

**思想**:把词表组织成**二叉树**(常用 Huffman tree),每个叶节点是一个词。预测一个词 = 预测一条从根到叶的路径。

```
原来: 预测"是 |V| 个词中的哪个"  → O(|V|)
现在: 预测"在二叉树上每个节点向左还是向右" → O(log|V|)
```

50,000 个词:`log₂(50000) ≈ 16` 次二元决策,而不是 50,000 次。

#### 方法 3:Subsampling Frequent Words

**思想**:`the` / `a` / `is` 这种高频词训练价值低,**按概率丢弃**:

```
P(丢弃 word) = 1 - sqrt(t / freq(word))
                   ↑
                   t 是阈值,通常 1e-5
```

高频词被频繁丢弃,训练样本变少,加速训练。**额外好处**:让稀有词获得更多相对训练机会。

### 2.2 满分答题模板(6 分)

> **Why skip-gram is slow**: At each training step, skip-gram computes a softmax over the entire vocabulary to predict the context word given the center word. This requires computing `exp(score)` for every word in the vocabulary V, then normalizing. With |V|=50,000 or larger, the cost is `O(|V|)` per training example, and the output projection matrix has `|V| × embed_dim` parameters that must be updated.
>
> **Solution: Negative Sampling**. Instead of distinguishing the true context word from all `|V|-1` other words, we only distinguish it from `k` randomly sampled "negative" words (typically k=5-20). For each training example:
> - The positive pair (center, true_context) is trained with target = 1
> - k negative pairs (center, random_word) are trained with target = 0
> - Each pair becomes a binary classification with sigmoid loss
>
> This reduces per-step cost from `O(|V|)` to `O(k)`, dramatically speeding up training while preserving most of the learned representation quality.

**关键得分词**:softmax over V / O(|V|) / negative sampling / binary classification / sigmoid。

---

## 2.3 RNN 用于变长 NER(5 分)

### 题目核心

> 用预训练 LM + 多层 RNN 做 NER,数据集文本长度从几个词到几百个词都有。**这个网络是不是好选择?如果不是,怎么改进?**

### 第一步:理解 NER 任务

**NER (Named Entity Recognition)** = 命名实体识别。

**输入**:一段文本
**输出**:对**每个 token**标一个标签(人名/地名/组织名/其他)

```
Input:  John works at Microsoft in Seattle
Output: B-PER O    O   B-ORG    O  B-LOC

(BIO 标注:B-=实体开头,I-=实体内部,O=非实体)
```

**关键**:NER 是 **token-level task**,不是 sentence-level——每个 token 都要输出一个标签。

### 第二步:多层 RNN 适合吗?半适合

**适合的方面**:
- ✓ 可处理变长输入(RNN 本来就是为变长设计的)
- ✓ Token-level 输出符合 RNN 的逐步处理结构(每一步出一个标签)

**不适合的方面**:
- ✗ **Vanishing gradient**:几百词长的文本,RNN 的梯度从最后传到最前面会消失,远处依赖学不到
- ✗ **只能看一个方向**(普通 RNN 是从左到右):NER 经常需要看右边的信息——`Apple announced...` 这里 `Apple` 是公司,需要看到 `announced` 才能确定
- ✗ **顺序计算**:长文本上慢
- ✗ Multi-layer RNN 本身不一定能解决以上问题,反而可能加剧梯度消失

### 第三步:怎么改进——给 3 个递进式方案

#### 方案 1:换成 BiLSTM(最基本的改进)

```
普通 RNN:    →→→→→→→→→     单向,只看左
BiLSTM:    →→→→→→→→→        前向 LSTM 看左
            ←←←←←←←←←        反向 LSTM 看右
            两者拼接 → 每个 token 同时拥有左右上下文
```

**LSTM**:用 gates 缓解梯度消失,能记住更长依赖。
**Bi-direction**:双向上下文,适合 NER。

#### 方案 2:加 CRF 解码层(BiLSTM-CRF,经典 NER 方案)

```
BiLSTM 输出每个 token 的标签 logits
   ↓
CRF (Conditional Random Field) 层
   ↓
最优标签序列
```

**为什么加 CRF?** 标签之间有**依赖关系**,如:
- `B-PER` 后面只能是 `I-PER` 或 `O`,不能是 `I-LOC`
- CRF 显式建模这种**标签之间的转移概率**,确保输出序列合法

#### 方案 3:换成 Transformer / BERT(最强方案)

- BERT 的 self-attention 可以**直接连接**任意距离的 token,完全没有梯度消失问题
- BERT 是双向的,且并行计算,长文本处理快
- NER 任务上 BERT-based 模型基本是 SOTA

**实现方式**:用预训练 BERT,在每个 token 的输出向量上接一个分类头,预测 BIO 标签。

### 关于"长度差距大"的工程细节(可加分)

> 数据里有从几个词到几百词的样本,需要 **padding + attention mask**:
> - 短句补 `[PAD]` 到 batch 最长长度
> - attention_mask 告诉模型哪些位置是真 token,哪些是 padding(loss 不算 padding 位置)

### 关于 subword tokenization 的标签对齐(高级加分点)

> BERT 用 WordPiece tokenization,一个词可能被切成多个 subword。比如 `Washington → Wash + ##ington`。NER 标签需要做**对齐**——只在 word 的第一个 subword 上算 loss,或在所有 subword 上重复标签。

### 2.3 满分答题模板(5 分)

> **Multi-layer RNN is not an ideal choice for this NER task** for three reasons:
>
> (1) **Vanishing gradient**: With sequences ranging up to hundreds of words, gradients propagating back through many time steps shrink toward zero, so the model fails to learn long-range dependencies critical for NER.
>
> (2) **Unidirectional context**: A vanilla RNN only uses left context. NER often needs both left and right context to disambiguate entities (e.g., recognizing "Apple" as ORG depends on seeing "announced" or "stock" later).
>
> (3) **Sequential computation**: RNNs cannot parallelize across time steps, making training slow on long sequences.
>
> **Improvements (in order of strength):**
>
> - **BiLSTM**: Replace plain RNN with bidirectional LSTM. The gates mitigate vanishing gradient, and the bidirectional structure provides both left and right context for each token.
>
> - **BiLSTM-CRF**: Add a CRF layer on top of BiLSTM output to model label transition constraints (e.g., `I-PER` cannot follow `B-LOC`), producing globally optimal label sequences.
>
> - **Transformer / BERT-based model**: Use a pretrained BERT and add a token-level classification head. Self-attention directly connects any two positions, fully eliminates vanishing gradient, supports long sequences, and is the current SOTA approach for NER.
>
> Additionally, padding + attention masks should be used to handle the variable-length input efficiently in batch training.

**关键得分词**:vanishing gradient / bidirectional / CRF / label transition / Transformer / attention mask。

---

## Image 2 答题策略汇总

| 子题 | 分数 | 关键词 |
|---|---|---|
| 2.1 Distributional hypothesis + ELMo | 4 | context-independent / contextualized / polysemy |
| 2.2 Skip-gram 慢 + 加速 | 6 | softmax over V / negative sampling / sigmoid |
| 2.3 RNN for NER | 5 | vanishing gradient / BiLSTM / CRF / BERT |

**通用考场策略**:
- **先答"是什么"(2 句)→ 再答"为什么"(核心机制)→ 最后举例子或给改进方案**
- 每个子题尽量用编号 (1)(2)(3)
- 关键术语**必须用英文**(中文丢分)

---

## 🧠 快速自测(Image 2)

3 道题:

1. 用一句话 + 一个例子解释 distributional hypothesis。
2. Negative sampling 把 skip-gram 训练复杂度从 O(?) 降到 O(?)?
3. NER 是 token-level 还是 sentence-level 任务?这决定了 BERT 怎么接分类头?

答完进 **Image 3**——但 image 3(BERT 代码 bug)我**已经讲过了**(Part B)。

要不要直接进 **HW2 Q4(BLEU + Beam search 手算)** 复盘?这是期末**极有可能直接出现**的题型。

如果时间紧,你可以直接说:
- "继续 BLEU/Beam search" → 我讲那个
- "不需要,我自己看" → 你直接去考试


cross entropy这个词我很难理解


好,这个词确实抽象——它的命名来自信息论,光看字面意思根本猜不到。我用**渐进式**给你建立直觉。

---

## 1. 先把"entropy"(熵)拆开

### Entropy 的直觉:不确定性

> **Entropy = 一个概率分布有多"不确定"。**

例子,假设你有个袋子,里面装球:

```
情况 A:袋子里 100% 是红球
   抽一个 → 你完全确定是红球
   不确定性 = 0,熵 = 0

情况 B:50% 红球,50% 蓝球
   抽一个 → 五五开,完全猜不到
   不确定性最大,熵最大

情况 C:99% 红球,1% 蓝球
   抽一个 → 大概率红球,但有一点不确定
   熵很小,但不为 0
```

**熵衡量"惊讶程度"或"信息量"**——越不确定,熵越大;越确定,熵越小。

### Entropy 的公式

```
H(p) = - Σ p(x) × log p(x)
        x

(对所有可能的 x 求和)
```

**别被吓到**,我们用一个具体例子拆开看。

抛硬币,公平的(50% 正,50% 反):
```
H = -(0.5 × log(0.5) + 0.5 × log(0.5))
  = -(0.5 × (-0.693) + 0.5 × (-0.693))
  = -(-0.693)
  = 0.693
```

(这里用自然对数 ln,所以是 0.693。如果用 log₂,结果是 1 bit。)

不公平硬币(99% 正,1% 反):
```
H = -(0.99 × log(0.99) + 0.01 × log(0.01))
  = -(0.99 × (-0.01) + 0.01 × (-4.6))
  = -(-0.01 + (-0.046))
  = 0.056
```

→ 几乎确定,熵很小。

100% 确定:
```
H = -(1 × log(1) + 0 × log(0))
  = -(1 × 0 + 0)
  = 0
```

→ 完全确定,熵 = 0。

**直觉总结**:

| 分布 | 熵 |
|---|---|
| 完全确定(100% 一个事件) | 0(最小) |
| 完全不确定(均匀分布) | log(n)(最大) |
| 中间情况 | 介于两者之间 |

---

## 2. 现在加上 "cross"——交叉

### Cross Entropy 的设定

**Cross entropy 不是衡量一个分布,而是衡量两个分布之间的"距离"**:
- 一个是**真实分布** `p`(真实答案)
- 一个是**模型预测分布** `q`(模型猜的)

### 公式

```
H(p, q) = - Σ p(x) × log q(x)
           x
        ↑           ↑
        真实        模型
        分布        预测
```

注意:和 entropy 长得几乎一样,**唯一区别**是 log 里的 `p` 换成了 `q`。

### "Cross"在哪?

> **"交叉"的意思**:用真实分布 `p` 作为权重,去看模型的对数概率 `log q`。
>
> 即:**"真实告诉我们事件多重要,模型告诉我们事件多惊讶,两者交叉相乘求和。"**

### 为什么叫"交叉"

- Entropy `H(p) = -Σ p log p`:**自己**对**自己**的不确定性
- Cross entropy `H(p, q) = -Σ p log q`:用**自己**(真实分布)的权重,衡量**模型**预测的"对数惊讶度"

两个分布"交叉"在一起,所以叫 cross entropy。

---

## 3. 在分类任务里 cross entropy 长什么样

这是关键——**机器学习里的 cross entropy 公式看起来比上面简单很多**,因为分类任务的真实分布是**one-hot**。

### 真实分布是 one-hot

3 分类问题,真实标签是类别 1:

```
真实分布 p = [0, 1, 0]    ← one-hot,只有正确类是 1
模型预测 q = [0.1, 0.7, 0.2]   ← softmax 后的概率
```

### 套公式

```
H(p, q) = - Σ p(x) × log q(x)
        = - (0 × log(0.1) + 1 × log(0.7) + 0 × log(0.2))
        = - (0 + log(0.7) + 0)
        = - log(0.7)
        = 0.357
```

注意!**只剩下真实标签那一项**,因为其他位置 p=0,整项都是 0。

### 化简后的"分类版" cross entropy

> **Cross entropy = -log(模型给真实标签的概率)**

就这么简单。

### 用直觉验证

```
模型给正确答案的概率   cross entropy
1.0(完美)            -log(1.0) = 0           ← loss 最小
0.9                  -log(0.9) = 0.105
0.5                  -log(0.5) = 0.693
0.1                  -log(0.1) = 2.303
0.001                -log(0.001) = 6.908     ← 越错,loss 越大
```

**这正是你之前学的 NLL Loss!**

---

## 4. 关键揭秘:Cross Entropy 和 NLL 是同一个东西

```
分类任务的 cross entropy = NLL (Negative Log Likelihood)
                       = -log(模型给真实标签的概率)
```

这就是为什么:

```
CrossEntropyLoss(logits, target) = NLLLoss(log_softmax(logits), target)
```

它们**数学上完全是同一件事**——只是输入起点不同(logits vs log_probs)。

---

## 5. 直觉总结:为什么用 cross entropy 当 loss

### 三个层次的理解

#### 层次 1(最浅):cross entropy 衡量预测错得有多离谱

模型给正确答案的概率越高,loss 越小;越低,loss 越大。

#### 层次 2(中等):cross entropy 衡量两个分布的"差距"

模型预测分布 `q` 越接近真实分布 `p`,cross entropy 越小。

#### 层次 3(最深):cross entropy 来自信息论

> 用模型的"假分布"`q` 来编码真实事件,平均需要多少 bits?**模型越准,编码越短;模型越不准,编码越长**。这个"平均编码长度"就是 cross entropy。

考场如果只问 loss,层次 1 + 2 就够了。

---

## 6. 回到 Module 2 的 perplexity

现在 perplexity 这个东西也通了:

```
Perplexity = exp(cross entropy)
```

**Cross entropy 是"模型有多惊讶"(用 nats 或 bits 衡量)**。
**Perplexity 是"模型在多少个候选词之间犹豫"(更直观的单位)**。

### 直觉

```
Cross entropy = 1.0(自然对数)
Perplexity = exp(1.0) = 2.718

→ 模型平均像是在 ~2.7 个词之间犹豫
```

```
Cross entropy = 4.6
Perplexity = exp(4.6) ≈ 100

→ 模型平均像是在 100 个词之间犹豫
```

---

## 7. 一句话记忆

> **Cross entropy(交叉熵)= 用真实分布的权重,衡量模型预测的"对数惊讶度"。在分类任务里,等价于 -log(模型给真实标签的概率)。模型越准,越不惊讶,loss 越小。**

---

## 🧠 最小检查

1. 模型对 3 分类问题给出 `q = [0.2, 0.7, 0.1]`,真实标签是类别 0。Cross entropy 是多少?(算 -log(0.2),log 用自然对数)
2. 如果 perplexity = 50,大致含义是什么?
3. CrossEntropyLoss 和 NLLLoss 数学上完全等价吗?

答完(或如果你要赶时间直接跳过),我们继续按你的节奏:**HW2 Q4(BLEU + Beam search 手算)** 还是其他?



padding + attention mask被需要的原因是什么


很好的问题——这是 NLP 工程里**最常见的实操细节**,期末很容易出。我把这两个东西彻底拆开。

---

## 1. 先理解为什么需要 padding

### 问题的根源:GPU 喜欢矩形

你 Module 1 学过,batch 让 GPU 并行计算多个样本。但 GPU 要求 batch 必须是**规整的矩形**——所有样本长度必须一样。

但句子长度天然不一样:

```
样本 1: "I love NLP"                    → 3 个 token
样本 2: "PyTorch is fun and useful"     → 5 个 token
样本 3: "Hi"                             → 1 个 token

如果直接堆成 batch:
[
  [12, 88, 3],                ← shape [3]
  [45, 7, 22, 9, 14],         ← shape [5]
  [10]                         ← shape [1]
]
```

**这不是合法的 tensor**——每行长度不同,根本没法构成 `[batch, seq_len]` 的二维矩阵。

### 解决方案:Padding

**思想**:把所有句子**补到同一长度**,通常是 batch 里最长那个的长度。

```
最长是 5 → 把所有样本补到 5

样本 1: [12, 88, 3, 0, 0]               ← 后面补 [PAD] 的 id(通常是 0)
样本 2: [45, 7, 22, 9, 14]              ← 已经够长,不变
样本 3: [10, 0, 0, 0, 0]                ← 大量 padding

batch_x = [[12, 88, 3, 0, 0],
           [45, 7, 22, 9, 14],
           [10, 0, 0, 0, 0]]

shape = [3, 5]   ✓ 合法的 [batch, seq_len]
```

**`[PAD]` 是个特殊 token**,通常分配 id=0,词表里专门留一个位置给它。

### Padding 是必要之恶

Padding 解决了"形状不一致"的工程问题,但**引入了一个新问题**:

> 这些 `[PAD]` token 是**假的**——它们不是真实的词,只是占位符。**模型不应该理会它们**。

但模型不知道——它会傻乎乎地把 padding 也当成真 token 处理:

- Embedding 层会给 [PAD] 分配向量
- Self-attention 会让真 token 关注 [PAD]
- Pooling 会把 [PAD] 的向量也算进平均
- Loss 会对 [PAD] 位置算 loss

**结果**:模型被一堆假 token 污染,学到的东西不对。

---

## 2. 这就是 attention mask 出现的原因

### 核心作用

> **Attention mask 是一个 0/1 矩阵,告诉模型"哪些位置是真 token,哪些是 padding 应该忽略"。**

### 长什么样

接上面的例子:

```
batch_x         = [[12, 88, 3, 0, 0],          ← 真,真,真,假,假
                   [45, 7, 22, 9, 14],          ← 全部真
                   [10, 0, 0, 0, 0]]            ← 真,假,假,假,假

attention_mask  = [[1, 1, 1, 0, 0],
                   [1, 1, 1, 1, 1],
                   [1, 0, 0, 0, 0]]

shape: [batch, seq_len] = [3, 5]
```

**1 = 这是真 token,关注它**
**0 = 这是 padding,忽略它**

### 模型怎么用 attention_mask

Mask 在不同地方有不同用法:

#### 用法 1:Self-attention 屏蔽 padding(最重要的场景)

BERT / Transformer 的 self-attention 会让每个 token 关注其他所有 token。但**真 token 不应该关注 padding**——padding 没有意义。

```
不用 mask:
"I love NLP [PAD] [PAD]"
"NLP" 计算自己的注意力时,会同时关注 "I", "love", "[PAD]", "[PAD]"
   → 部分注意力被 padding 抢走了

用 mask:
对应 padding 的位置,attention score 设为 -∞
softmax 后 padding 位置的权重 = 0
   → 真 token 完全忽略 padding
```

具体实现:

```python
# attention_scores shape: [batch, seq_len, seq_len]
# 每个位置 i 对每个位置 j 的注意力分数

# 把 padding 位置的分数设为很大的负数
attention_scores = attention_scores.masked_fill(
    attention_mask == 0, 
    float('-inf')
)

# softmax 后 -inf 变成 0
attention_weights = softmax(attention_scores)
```

#### 用法 2:Pooling 时跳过 padding

如果你做 mean pooling:

```python
# 错误做法:直接 mean,padding 也被算进去
sentence_repr = embeddings.mean(dim=1)
                ↑
                被 padding 的零向量稀释了

# 正确做法:用 mask 加权平均
mask = attention_mask.unsqueeze(-1).float()       # [batch, seq_len, 1]
sentence_repr = (embeddings * mask).sum(dim=1) / mask.sum(dim=1)
```

#### 用法 3:Loss 屏蔽 padding(token-level 任务,如 NER)

NER 对每个 token 算 loss,但 padding 位置不应该贡献 loss:

```python
loss_per_token = cross_entropy(logits, labels, reduction='none')
                                                ↑
                                                先不平均
loss = (loss_per_token * attention_mask).sum() / attention_mask.sum()
       ↑
       只对真 token 求平均
```

---

## 3. 把这一切串起来——一个完整的 BERT 调用

```python
batch_x = [[12, 88, 3, 0, 0],
           [45, 7, 22, 9, 14],
           [10, 0, 0, 0, 0]]

attention_mask = [[1, 1, 1, 0, 0],
                  [1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 0]]

# 把两者一起传给 BERT
output = bert(input_ids=batch_x, attention_mask=attention_mask)
```

**两个参数缺一不可**:
- `input_ids`:告诉模型 token 是什么
- `attention_mask`:告诉模型哪些是真 token

**BERT 内部会自动用 mask 屏蔽 padding 在 self-attention 里的影响**——你不需要手动写 mask 逻辑。

---

## 4. 回到 image 3 的 BERT 代码题

```python
sequence_output, pooled_output = self.bert(input_ids=input_ids,
                                            attention_mask=attention_mask)
```

现在你应该理解为什么 forward 函数**必须传 attention_mask**:

- 不传 mask → BERT 不知道哪些是 padding → padding 也参与 self-attention → 真 token 的表示被污染 → pooled_output 不准确 → 分类性能下降

期末如果给你的代码**没传 attention_mask**,这也是一个 bug 点。

---

## 5. 一张表总结两个东西的关系

| | Padding | Attention Mask |
|---|---|---|
| **是什么** | 把假 token `[PAD]` 加到短句末尾 | 0/1 矩阵,标记每个位置真假 |
| **解决什么** | 让 batch 形状规整(GPU 要求) | 让模型忽略 padding 不算它 |
| **谁产生的** | tokenizer 输出 input_ids 时 | tokenizer 输出 attention_mask 时 |
| **谁使用的** | 整个模型(因为是输入) | self-attention / pooling / loss |
| **缺了会怎样** | batch 无法构造,报 shape 错误 | padding 污染 attention,模型变差 |

**关键关系**:**padding 引入假 token,attention_mask 告诉模型忽略假 token。两者必须配套使用。**

---

## 6. 一句话记忆

> **Padding 是为了 batch 形状规整(GPU 要求矩形 tensor),attention mask 是为了告诉模型哪些位置是真 token 应该参与计算,哪些是 padding 应该忽略。Padding 和 attention mask 一起把"长度不一致"这个工程问题解决干净。**

---

## 7. 期末考场的两种题型

### 题型 A:解释 padding + mask 的作用

> Padding standardizes variable-length sequences in a batch to the same length by appending special `[PAD]` tokens (typically id=0), enabling efficient parallel computation on GPUs. However, padding introduces fake tokens that should not influence the model. The attention_mask (a binary tensor with 1 for real tokens and 0 for padding) tells the model which positions to attend to. In Transformer self-attention, padding positions are masked out by setting their attention scores to -∞ before softmax, effectively assigning them zero attention weight.

### 题型 B:发现代码里没传 mask

> The `forward` function only passes `input_ids` to BERT but omits `attention_mask`. Without the mask, BERT cannot distinguish real tokens from padding, causing self-attention to attend to padding positions and corrupting the learned representations. The fix is to also pass `attention_mask=attention_mask`.

---




