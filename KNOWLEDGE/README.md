# KNOWLEDGE

`KNOWLEDGE/` 是这个仓库的结构化知识图谱层。

它不是原始资料堆放区，也不是单纯为了好读而写的 Wiki。  
它是仓库的核心层（core layer / backbone），负责把主题沉淀成可复用的知识节点（knowledge nodes）。

一个节点不是普通笔记。  
它应该能支持：

- learning
- explanation
- comparison
- implementation
- project reuse
- career reuse

---

## 这一层是做什么的

`KNOWLEDGE/` 的目标，是把专业知识组织成：

- explicit
- reusable
- accumulative
- project-relevant
- career-relevant

它解决的问题不是“把资料存起来”，  
而是“把主题变成长期可调用的节点，并显式连接起来”。

Examples:

- `transformer`
- `rope`
- `kv-cache`
- `distributed-training`
- `multimodal-modeling`
- `evaluation-metrics`
- `inference-optimization`

---

## 为什么这一层重要

普通笔记系统可以记录信息。  
结构化知识图谱可以做得更多：

- show prerequisites
- connect methods to problems
- connect concepts to projects
- connect theory to code
- connect work experience to reusable knowledge
- connect projects to interview stories

这就是为什么 `KNOWLEDGE/` 是整个仓库的 backbone。

---

## 什么算一个知识节点

一个知识节点通常是“稳定、可复用、可被多次引用”的主题单元。

它可以是：

- concept
- method
- mechanism
- component
- system pattern
- evaluation concept
- implementation pattern
- capability

它通常不应该是：

- 一篇论文标题本身
- 一次性实验记录
- 太宽泛的大主题
- 只在单个项目中出现的一次性命名

一个实用判断是：

如果这个主题未来会在多个问题、项目、文章、讨论中反复出现，  
它就值得成为一个节点。

---

## 一个节点通常长什么样

推荐结构：

```text
KNOWLEDGE/
└── transformer/
    ├── README.md
    ├── meta.yaml
    ├── math/
    │   └── README.md
    ├── code/
    │   └── README.md
    ├── refs/
    │   └── README.md
    └── thoughts/
        └── README.md
```

### `README.md`

节点主入口。

它应该回答：

- what this topic is
- why it matters
- what it depends on
- what problems it helps solve
- what it connects to

推荐包含：

- concise definition
- mental model
- key ideas
- typical use cases
- important tradeoffs
- related nodes
- links to `math/` `code/` `refs/` `thoughts/`

---

### `meta.yaml`

结构化关系层。

推荐字段可以包括：

- node id
- canonical name
- aliases
- node type
- status
- prerequisites
- related nodes
- related problems
- alternatives
- downstream uses
- linked projects
- external repos
- checklist / progress
- primary sources

`meta.yaml` 负责回答“系统应如何理解这个节点”，  
`README.md` 负责回答“人应如何读懂这个节点”。

---

### `math/README.md`

用于公式、推导、符号和数学理解。

适合放：

- derivations
- notation mapping
- proofs or proof sketches
- scaling analysis
- theoretical limits

---

### `code/README.md`

用于实现视角与工程理解。

适合放：

- pseudocode
- implementation notes
- tensor shape conventions
- external code links
- performance pitfalls
- debugging heuristics

---

### `refs/README.md`

用于保存来源与引用索引。

适合放：

- papers
- docs
- blogs
- talks
- repos
- benchmark references

这里尽量保持可追溯性。  
没有来源的结论，至少要明确它是经验判断而不是事实摘录。

---

### `thoughts/README.md`

用于保存判断、解释、疑问与限制。

适合放：

- interpretation
- tradeoff analysis
- comparison notes
- open questions
- hypotheses
- limitations

这里可以主观，但必须与事实层分开。

---

## 什么内容主要属于这里

当一个对象主要是“可复用主题或能力”时，它通常属于 `KNOWLEDGE/`。

Examples:

- attention
- transformer
- batch-normalization
- rope
- quantization
- beam-search
- distributed-training
- a-b-testing
- feature-engineering
- model-evaluation

---

## 什么内容不应首先放在这里

以下内容更适合先落到其它层：

- raw paper highlights -> `RAW_SOURCES/`
- problem framing -> `PROBLEMS/`
- project execution notes -> `PROJECTS/`
- operational SOPs -> `WORK/`
- interview prep assets -> `CAREER/`
- compiled overviews -> `WIKI/`

当然，这些层仍然应该回链到相关知识节点。

---

## 命名与组织原则

### 节点命名原则

建议目录名满足以下要求：

- 尽量稳定，不随一时表述变化
- 尽量使用领域内常见术语
- 尽量短而清晰
- 避免把多个主题硬塞进一个名字
- 别名放到 `meta.yaml`，不要塞进目录名

推荐倾向：

- 使用 canonical term
- 目录名尽量可搜索
- 多词节点使用 `kebab-case`

Examples:

- `kv-cache`
- `long-context-training`
- `retrieval-augmented-generation`

### 目录分组原则

`KNOWLEDGE/` 可以按大类分组以提升可读性，  
但 **directory grouping does not represent dependency**。

例如：

```text
KNOWLEDGE/
├── foundations/
├── machine-learning/
├── deep-learning/
├── llm/
├── multimodal/
├── systems/
├── infra/
├── data/
├── engineering/
└── product-sense/
```

这些分组只用于组织。  
真实依赖关系应该始终写在 `meta.yaml` 或正文关系区块里。

---

## 何时新建节点，何时扩展旧节点

### 适合新建节点的情况

- 主题已经能独立讨论
- 未来会被多个项目或问题复用
- 它有自己独立的机制、术语或实现边界
- 当前页面已经因为混合多个主题而变得难以维护

### 适合继续扩展原节点的情况

- 新内容只是已有节点的子方面
- 独立出去会导致强重复
- 这个内容还没有形成稳定边界

一个简单判断：

如果你写着写着发现“这个小节已经像另一篇独立页面”，  
那通常就是该拆节点的时候。

---

## 节点设计原则

### 1. Keep nodes small enough to reuse

节点不能大到难以维护。

### 2. Keep nodes meaningful enough to matter

节点也不能碎到只剩噪音。

### 3. Separate topic from problem

节点通常是 topic、method、concept、capability。  
问题页是另一种对象。

### 4. Separate fact from judgment

事实优先进入 `refs/` 与结构化页面。  
判断优先进入 `thoughts/`。

### 5. Prefer explicit links

不要依赖记忆在未来重建关系。

---

## 推荐写法与不推荐写法

推荐：

- 开头先给稳定定义
- 尽快说明它解决什么问题或服务什么目标
- 区分机制、实现、证据、判断
- 让读者快速知道该去哪里看 `math/` `code/` `refs/`
- 重要结论能追到来源
- 与其它节点的关系是显式的

不推荐：

- 把节点写成资料堆
- 把 README 写成长篇论文笔记
- 把不同层级主题混在同一页
- 把猜测写成结论
- 把实现细节、数学推导、主观判断揉在一个文件里
- 用目录深度表达概念依赖关系

---

## 如何创建一个新节点

1. 先确认它是不是一个值得复用的稳定主题
2. 选择清晰的 node boundary
3. 创建节点目录
4. 添加标准文件：`README.md`、`meta.yaml`、`math/README.md`、`code/README.md`、`refs/README.md`、`thoughts/README.md`
5. 优先补 `meta.yaml` 与 `refs/README.md`
6. 再写 `README.md` 的定义、机制、关系与用途
7. 需要时补 `math/` 与 `code/`
8. 把判断与疑问放到 `thoughts/`
9. 把它连接到 related nodes、related problems、related projects，以及需要时的 external repos

---

## 这一层如何与其它层协作

### With `RAW_SOURCES/`

raw sources 提供证据与原始上下文。

### With `PROBLEMS/`

problem pages 提供动机、比较空间与真实约束。

### With `PROJECTS/`

projects 提供真实使用场景与产出。

### With `WIKI/`

wiki pages 会跨多个知识节点做编译型整合。

### With `REPRO_INDEX/`

external experiment repos 把理论连接到代码与验证。

---

## 与 `PROBLEMS/` 和 `WIKI/` 的区别

可以用一句话区分：

- `KNOWLEDGE/` 讲“这个东西是什么、怎么工作”
- `PROBLEMS/` 讲“我们到底在解决什么问题、有哪些方案”
- `WIKI/` 讲“把多个节点与问题编译成更容易阅读的综合页”

例如：

- `rope/` 适合放在 `KNOWLEDGE/`
- `long-context-degradation/` 适合放在 `PROBLEMS/`
- “long context methods overview” 适合放在 `WIKI/`

---

## 当前阶段的重点

`KNOWLEDGE/` 的第一阶段建议优先：

- creating foundational nodes
- defining stable node patterns
- linking nodes to problems
- connecting nodes to external code repos
- forming the first reusable knowledge graph

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [META](/Users/mac/studyspace/algo-engineer-os/META/README.md)
- [PROBLEMS](/Users/mac/studyspace/algo-engineer-os/PROBLEMS/README.md)
