# BPE Tokenization

## 它要解决什么问题

Tokenization 的根本矛盾：

| 方案 | 问题 |
|---|---|
| **Word-level** | 词表巨大，OOV 严重——`runner` 没见过就变 `[UNK]` |
| **Char-level** | 序列太长，语义太碎——`["c","a","t"]` 学不到 `cat` 的整体义 |

BPE（Byte Pair Encoding）的核心思路：**从字符开始，让数据告诉你哪些字符组合应该合并成一个 token**。

高频组合（如 `t-h-e`）合并成 `the`，低频组合保留为字符。这样：

- 常见词 → 完整保留（一个 token）
- 罕见词 → 自动拆成 subword（如 `oldest` → `old` + `est`）
- **OOV 几乎消失**——任何新词最差也能被字符拆开

## 朴素直觉为什么不够：先看 BPE 算法 5 步

```
1. 初始化:每个词拆成字符序列
2. 统计:数所有相邻字符对的"加权频率"
3. 合并:把最高频的对合并成一个新 symbol
4. 更新:把语料库里所有这个对都替换掉
5. 重复:直到达到目标 merge 次数 / 词表大小
```

**关键词**：**加权**频率 + **相邻**——两个都是考点。

## 反事实：什么叫"加权频率"——为什么不能简单数次数

最容易错的地方是 Step 2 的 "加权"。看一个语料库：

```
(low, 5)        ← low 出现 5 次
(lower, 2)
(newest, 6)
(widest, 3)
```

括号里第二个数字是**词频**——这个词在语料中真实出现的次数。

**BPE 数的是字符对在整个语料里出现的总次数**。如果你只数"在多少个不同词里出现"，那是错的——`low` 出现了 5 次，每次都包含一个 `(l, o)`，所以 `(l, o)` 在 `low` 里贡献 **5 次**，不是 1 次。

理论上你应该把语料"展开"逐个数：

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
... (newest 共 6 次)
w i d e s t     ← 第 1 次 widest
... (widest 共 3 次)

数 (l, o) 出现了多少次?
- 5 个 low 各贡献 1 次     → 5
- 2 个 lower 各贡献 1 次   → 2
- newest 不含 (l,o)        → 0
- widest 不含 (l,o)        → 0
                          总计 = 7
```

逐个数太累。聪明的做法：**既然每个 `low` 都包含一个 `(l,o)`，那 5 个 `low` 就贡献 5 个 `(l,o)`——直接把词频当权重乘上去**。

```
(l, o):
- low 包含 (l,o), low 出现 5 次   → 贡献 5
- lower 包含 (l,o), lower 出现 2 次 → 贡献 2
                                    合计 = 7
```

**这就是"加权"**：每个词对一个字符对的贡献 = **这个词的词频**（权重）。

> **括号里第二个数字 = 这个词在语料中真实出现的次数 = 它对所有内部字符对贡献的权重**

最容易踩的坑就是抄错词频——后面所有数字全错。**手算题第一步应该先把题目给的词和频率原样抄一遍**，确认无误再开始拆字符。

## 反事实：BPE 一定要"相邻"才算

`(o, d)` 在 `o l d` 里**不是**相邻对——中间隔了一个 `l`。BPE 只数**直接相邻**的字符对。

这一点在初始化阶段容易踩——记住每个字符之间想象有"边界"，只看左右紧挨的两个字符。

## 用例子算一遍

语料库：

```
l o w     ×5
l o w e r ×2
n e w e s t ×6
w i d e s t ×3
```

数所有相邻对的加权频率：

```
(l, o) = 5 + 2           = 7    ← low(5) + lower(2)
(o, w) = 5 + 2           = 7
(w, e) = 2 + 6           = 8    ← lower(2) + newest(6)
(e, r) = 2               = 2
(n, e) = 6               = 6
(e, s) = 6 + 3           = 9    ← newest(6) + widest(3)
(s, t) = 6 + 3           = 9
(w, i) = 3               = 3
(i, d) = 3               = 3
(d, e) = 3               = 3
```

最高频是 `(e, s) = 9` 和 `(s, t) = 9`——**tie**。

考试规则：**如果题目没说 tie-breaking 方法，写出一种合法选择并注明 tie**。

假设选 `(e, s)`，合并成新 symbol `es`。**Merge rule**：`e + s → es`。

更新语料（把所有 `e s` 替换成 `es`）：

```
l o w        ×5
l o w e r    ×2
n e w es t   ×6      ← e s 合并成 es
w i d es t   ×3      ← e s 合并成 es
```

**关键**：合并之后所有相邻对要**重新数**——因为词的内部结构变了，旧统计作废。

继续这个流程，直到达到目标 merge 次数或词表大小。

## 应用阶段：严格按学习顺序

训练完得到一个 merge rules 列表（按学习顺序）：

```
Rule 1: e + s → es
Rule 2: ...
Rule 3: ...
```

对新词应用：**严格按学习顺序逐条尝试合并**。

例：训练得到的 rules 是 `o+l→ol`, `ol+d→old`, `u+g→ug`, `h+ug→hug`。给一个新词 `holding`：

```
Step 0: h o l d i n g                    ← 拆成字符
Step 1: 应用 Rule 1 (o+l → ol)
        h ol d i n g
Step 2: 应用 Rule 2 (ol+d → old)
        h old i n g
Step 3: 应用 Rule 3 (u+g → ug):无 u,跳过
Step 4: 应用 Rule 4 (h+ug → hug):无 ug,跳过
最终:["h", "old", "i", "n", "g"]
```

`i`、`n`、`g` 在我们的 merge rules 里没有相关规则，所以保持字符状态。

## 反事实：为什么 BPE 不能完全消除 OOV

如果训练语料里**从来没出现过某个字符**呢？那它就是 OOV → `[UNK]`。

具体说：BPE 的最小单位是**字符**，而字符表来自训练语料。如果在 Unicode 全集中**未出现于训练**的字符（比如训练全是英文，测试出现中文字符），仍然变成 `[UNK]`。

所以：**BPE 大幅减少 OOV，但不能完全消除**——只是把 "未见词" 推到了 "未见字符" 这个更小的集合。

## BPE 的优势 / 劣势

**优势**：

- Reduces OOV（compose rare words from subwords）
- Captures morphology（`old` / `older` / `oldest` 共享 `old`）
- Smaller vocab than word-level（节省 embedding 参数）
- Shorter sequence than char-level（计算快）

**劣势**：

- Corpus-dependent（换领域可能 subword 切得不好）
- 仍可能 [UNK]（未见 base character）
- Tokenization 不唯一（依赖学习顺序）

## Open Questions

- **WordPiece 和 BPE 的严格差异**是什么？BERT 用 WordPiece，GPT 用 BPE，但具体细节差异（比如选择 merge 时的目标函数、prefix 标记 `##` 等）这一节点没碰到，需要单独节点。
- **SentencePiece** 进一步支持没有空格的语言（中文 / 日文），它是 BPE 的扩展还是不同算法？工程上很常用但本节点未覆盖。
- BPE 训练时的 **merge 数量**（也就是最终词表大小）如何选？经验上 vocab_size = 30K-50K 是常见，但选 10K 和 100K 的区别在哪？这条线和 embedding 参数量、序列长度的 trade-off 有关。
