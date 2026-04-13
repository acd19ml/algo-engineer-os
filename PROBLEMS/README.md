# PROBLEMS

`PROBLEMS/` 是这个仓库的问题驱动层（problem layer）。

如果 `KNOWLEDGE/` 保存可复用节点，  
那么 `PROBLEMS/` 解释的就是：**这些节点为什么重要，它们分别在解决什么问题**。

问题页不是在解释一个概念本身。  
它更关注问题定义、症状、约束、原因、方案、trade-off 与评估。

---

## 这一层是做什么的

`PROBLEMS/` 主要回答以下问题：

- 这个方法到底在解决什么问题
- 这个问题为什么重要
- 有哪些候选方案
- 不同方案之间的 trade-off 是什么
- 哪些知识节点与这个问题相关
- 这个问题在 research、work、projects、interviews 里如何出现

没有这一层，仓库很容易退化成“主题列表”，  
但缺少动机、缺少比较、缺少真实决策语境。

---

## 为什么这一层重要

真实学习和真实工作往往不是从概念开始，而是从问题开始。

通常你先遇到的是：

- a bottleneck
- a failure mode
- a design challenge
- an implementation difficulty
- a product requirement
- an interview question

所以一个强的知识系统，不应该只回答：

> What is X?

它也应该回答：

> What problem does X solve?  
> What else solves the same problem?  
> Why choose one path over another?

这就是 `PROBLEMS/` 存在的原因。

---

## 什么算一个 problem

一个值得进入 `PROBLEMS/` 的对象，通常具备这些特征：

- 它是反复出现的难题，而不是一次性小 bug
- 它有明确目标、约束或失败表现
- 它通常存在多个候选方案
- 它值得持续积累证据、比较与经验

Examples:

- `training-instability`
- `long-context-degradation`
- `multimodal-position-encoding`
- `evaluation-mismatch`
- `deployment-bottlenecks`
- `debugging-model-collapse`
- `interview-storytelling`

这说明 problem 不一定只属于研究。  
它也可以是工程问题、工作问题、沟通问题或职业问题。

---

## 什么内容主要属于这里

当一个页面主要是在做 **problem framing** 时，它通常属于 `PROBLEMS/`。

一个好的问题页通常会连接：

- multiple knowledge nodes
- multiple candidate approaches
- trade-offs and limitations
- open questions

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- concept explanations -> `KNOWLEDGE/`
- raw paper notes -> `RAW_SOURCES/`
- project execution details -> `PROJECTS/`
- compiled narrative summaries -> `WIKI/`
- career assets -> `CAREER/`

但这些层通常都应回链到相关 problem pages。

---

## 推荐目录结构

最小标准：

```text
PROBLEMS/
└── long-context-degradation/
    ├── README.md
    ├── meta.yaml
    └── refs/
        └── README.md
```

当问题规模变大时，可以扩展为：

```text
PROBLEMS/
└── long-context-degradation/
    ├── README.md
    ├── meta.yaml
    ├── causes/
    │   └── README.md
    ├── approaches/
    │   └── README.md
    ├── evaluation/
    │   └── README.md
    ├── cases/
    │   └── README.md
    ├── refs/
    │   └── README.md
    └── open_questions/
        └── README.md
```

不要求每个问题页一开始就建全。  
应按复杂度逐步长出来。

---

## 一个问题页应包含什么

一个好问题页通常应覆盖：

### 1. Problem definition

这个问题是什么。

### 2. Why it matters

为什么值得关心。

### 3. Typical failure modes

如果处理不好，通常会出现什么症状或后果。

### 4. Candidate solutions

有哪些方法、模式或技术路线在处理它。

### 5. Comparison dimensions

应该按什么维度比较不同方案。

### 6. Related knowledge nodes

理解这个问题需要哪些节点。

### 7. Related projects or work contexts

它在什么实际场景中出现。

### 8. Open questions

哪些部分仍不清楚、仍有争议、仍需验证。

---

## `meta.yaml` 可以记录什么

问题页的 `meta.yaml` 建议更偏“追踪与关系”：

- canonical name
- aliases
- problem type
- status
- severity or impact
- contexts where it appears
- related knowledge nodes
- known approaches
- evaluation metrics
- linked projects
- primary references

如果 `KNOWLEDGE/` 的 `meta.yaml` 更像“节点关系定义”，  
那么 `PROBLEMS/` 的 `meta.yaml` 更像“问题地图与跟踪面板”。

---

## 推荐拆页方式

当一个问题积累到一定规模时，建议把信息拆到更稳定的子页：

### `causes/`

记录成因、机制解释、原因假设与证据强弱。

### `approaches/`

记录方案家族、适用前提、优缺点、失败模式与 trade-off。

### `evaluation/`

记录评估维度、指标、数据集、判定标准与常见误判。

### `cases/`

记录具体案例、项目中的出现方式、调试过程、复盘结论。

### `refs/`

记录论文、文档、issue、博客、经验帖等证据入口。

### `open_questions/`

记录尚未确认的问题、存在争议的解释、待验证假设。

---

## 分组与分类

`PROBLEMS/` 可以按实践域分组，但这些分组只是组织方式，不表示依赖边界。

例如：

```text
PROBLEMS/
├── modeling/
├── training/
├── inference/
├── evaluation/
├── deployment/
├── debugging/
└── career/
```

一个 problem 往往会跨多个域连接节点与项目。  
不要把目录层级误当成问题边界本身。

---

## 何时新建问题页

适合新建的情况：

- 你在多个场景下反复遇到同类问题
- 这个问题已经出现多个方案或多个失败案例
- 你希望长期跟踪它的证据与结论
- 它连接了多个知识节点、项目或工作情境

不适合新建的情况：

- 只是某次开发中的临时排错点
- 你还说不清问题边界
- 内容量太少，只能写一句话

如果问题还不稳定，可以先在 `WORK/`、项目页或临时笔记里记。  
等它反复出现、值得复用时，再升格到 `PROBLEMS/`。

---

## 如何创建一个新问题页

1. 先把 problem statement 写清，而不是先堆方案
2. 记录主要出现上下文，例如 research、implementation、system design、work execution、interview prep
3. 链接相关 `KNOWLEDGE/` 节点
4. 链接候选方法或 alternatives
5. 写清 trade-offs
6. 明确 evaluation dimensions
7. 不确定的内容放进 `open_questions/`

---

## 问题页设计原则

### 1. Start from the challenge, not from the method

不要把问题页写成另一篇 topic summary。

### 2. Preserve multiple approaches

不要把不同方法压扁成一个模糊答案。

### 3. Make trade-offs visible

一个有用的问题页应该帮助做选择。

### 4. Stay connected to execution

尽量把问题连接到真实项目、实验或工作场景。

### 5. Keep uncertainty visible

如果比较还不完整，就明确写出来。

---

## 问题页与知识节点的区别

两层解决的问题不同。

`KNOWLEDGE/` 更像“知识对象库”：

- what is RoPE
- how KV cache works
- what FlashAttention changes

`PROBLEMS/` 更像“问题求解空间”：

- why long context quality drops
- how to stabilize training
- which latency bottlenecks matter most in serving

前者偏对象、机制、概念。  
后者偏症状、目标、约束、方案比较。

---

## 这一层如何与其它层协作

### With `KNOWLEDGE/`

problem pages 连接 topic nodes 与 solution methods。

### With `RAW_SOURCES/`

problem pages 应被 papers、docs、notes 等证据支撑。

### With `PROJECTS/`

projects 会暴露哪些问题在真实系统里最重要。

### With `WORK/`

operational issues 往往会沉淀成可复用问题页。

### With `CAREER/`

很多面试题和岗位要求，本质上围绕问题而不是定义。

### With `WIKI/`

wiki pages 可以把多个问题页编译成更大的综述。

---

## LLM 维护时的注意事项

问题页很容易被 LLM 写得“看起来完整，但证据很弱”。  
因此这一层要更严格：

- 不要凭空生成成因
- 不要把经验观察写成普遍规律
- 不要把单项目案例外推成通用结论
- 不要省略适用前提与失败边界
- 不确定时，把内容放进 `open_questions/`

问题页最重要的不是文风流畅，  
而是问题定义清晰、证据可追、方案比较真实。

---

## 当前阶段的重点

`PROBLEMS/` 的第一阶段建议优先：

- creating a small set of high-value problem pages
- linking them to foundational nodes
- making alternatives explicit
- using problem pages to guide learning order and project relevance

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [META](/Users/mac/studyspace/algo-engineer-os/META/README.md)
