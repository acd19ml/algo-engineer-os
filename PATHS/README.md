# PATHS

`PATHS/` 是这个仓库存放学习路径与成长路径的地方。

如果 `KNOWLEDGE/` 保存可复用节点，`PROBLEMS/` 帮你理解这些节点为什么重要，  
那么 `PATHS/` 的作用就是回答一个更实际的问题：**我下一步应该学什么、做什么、准备什么**。

这一层把一个静态仓库变成可导航的系统。

---

## 这一层是做什么的

`PATHS/` 用于组织带有目标的行动序列。

Examples:

- topic-based learning paths
- role-based growth paths
- project-based preparation paths
- interview-based preparation paths

没有这一层，仓库可能已经包含了你需要的一切内容，  
但仍然无法清楚回答：

- 我应该从哪里开始
- 我下一步该做什么
- 什么顺序更合理
- 为了某个具体目标，我到底该学哪些东西

---

## 为什么这一层重要

knowledge graph 很强，但 graph 不等于 plan。

一个 graph 更擅长告诉你：

- 什么东西彼此相关
- 什么依赖什么
- 什么属于同一空间

而 path 帮你决定的是：

- 什么应该先做
- 什么可以后做
- 针对某个目标，什么最重要
- 什么样的进展已经算 “good enough”

这正是 `PATHS/` 的作用。

---

## 什么内容主要属于这里

当一个对象主要是在描述 **为达成某个目标而设计的行动序列** 时，它通常属于 `PATHS/`。

Examples:

- a path for learning multimodal modeling
- a path for becoming more effective at model serving
- a path for preparing for algorithm engineer interviews
- a path for moving from research-heavy to engineering-heavy work
- a path for building enough system understanding to work on deployment

一个 path 不应只是主题清单。  
它应当有明确目标，并且在顺序上足够清晰，以减少决策负担。

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- stable topic definitions -> `KNOWLEDGE/`
- broad challenge framing -> `PROBLEMS/`
- ongoing execution notes -> `PROJECTS/`
- operational playbooks -> `WORK/`
- personal reflections -> `THINKING/`
- summarized high-level views -> `WIKI/`

不过，path 在需要时应连接到这些所有层。

---

## 推荐子结构

```text
PATHS/
├── README.md
├── topic-based/
├── role-based/
├── project-based/
└── interview-based/
```

### `topic-based/`

按技术主题组织的路径。

Examples:

- transformer foundations
- long-context modeling
- evaluation systems
- multimodal learning

---

### `role-based/`

按目标岗位或能力画像组织的路径。

Examples:

- algorithm engineer
- machine learning engineer
- research engineer
- multimodal engineer
- infra-aware model engineer

---

### `project-based/`

围绕“做成某个东西”组织的路径。

Examples:

- reproduce a paper end-to-end
- build a small retrieval system
- deploy a model service
- create an evaluation pipeline

---

### `interview-based/`

围绕招聘、转岗或面试准备组织的路径。

Examples:

- algorithm interview prep
- systems-heavy ML interview prep
- project storytelling prep
- multimodal role preparation

---

## 一个强的 path 应包含什么

一个好的 path 通常至少应覆盖：

### 1. Goal

这条路径到底想帮助你达成什么。

### 2. Entry assumptions

开始前你最好已经具备什么基础。

### 3. Ordered steps

建议按什么顺序推进。

### 4. Related knowledge nodes

哪些 nodes 最关键。

### 5. Related problems

哪些 problem pages 值得优先理解。

### 6. Related projects

应该做、复现或练习什么。

### 7. Milestones

怎样判断自己在前进。

### 8. Exit criteria

到什么程度就可以先认为“目前够用了”。

这样可以避免 path 退化成模糊的阅读清单。

---

## 常见 path 类型示例

### 一个 topic-based path

例如：

- 先学 Transformer
- 再学 RoPE family
- 再学 multimodal position encoding
- 对比 alternatives
- 做一个 toy implementation
- 读一个 model overview
- 用自己的话说明 trade-offs

这类路径的目标，是逐步掌握一个技术领域。

---

### 一个 role-based path

例如：

- 先定义目标岗位
- 分析所需能力
- 评估当前 gaps
- 把 gaps 映射到 knowledge nodes 和 projects
- 选择一两个最能证明 readiness 的项目
- 准备 interview stories

这类路径的目标，是让你逐步具备岗位准备度。

---

### 一个 project-based path

例如：

- 定义 build target
- 学习 prerequisite nodes
- 阅读相关 problems
- 配置 external repos
- 先做一个 minimal version
- 记录哪些有效、哪些失败
- 把结果转成可复用的 work 和 career assets

这类路径的目标，是把知识稳定地转成产出。

---

## 设计原则

### 1. Paths are goal-oriented

path 应绑定结果，而不只是绑定一组主题。

### 2. Paths should reduce decision fatigue

一个好的 path 应让你更容易决定下一步，而不是更迷茫。

### 3. Paths can be incomplete

path 不需要完美才有用。  
先有一个能用的版本，比等完整更重要。

### 4. Paths should connect multiple layers

一个强的 path 往往会跨越：

- knowledge
- problems
- projects
- work
- career

### 5. Paths should evolve

随着理解变化，path 本身也应该允许调整。

---

## 这一层如何与其它层协作

### With `KNOWLEDGE/`

paths 负责选择并排序相关 nodes。

### With `PROBLEMS/`

paths 会帮助你决定哪些 problems 应优先理解。

### With `PROJECTS/`

很多 path 最终要通过 project 才变得具体。

### With `WORK/`

一些 path 应明确包含 operational 或 engineering practice。

### With `CAREER/`

role-based 和 interview-based paths 应直接连接职业目标。

### With `THINKING/`

反思与判断会不断改变 path 的形状和优先级。

### With `DASHBOARDS/`

dashboard 可以跟踪当前活跃 path 的进度与里程碑。

---

## 当前阶段的重点

`PATHS/` 的第一阶段建议优先：

- a small number of high-value topic paths
- at least one role-based path
- at least one interview-based path
- simple milestone definitions
- strong links back to nodes, problems, and projects

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [PROBLEMS](/Users/mac/studyspace/algo-engineer-os/PROBLEMS/README.md)
- [PROJECTS](/Users/mac/studyspace/algo-engineer-os/PROJECTS/README.md)
- [WORK](/Users/mac/studyspace/algo-engineer-os/WORK/README.md)
- [CAREER](/Users/mac/studyspace/algo-engineer-os/CAREER/README.md)
- [THINKING](/Users/mac/studyspace/algo-engineer-os/THINKING/README.md)
- [DASHBOARDS](/Users/mac/studyspace/algo-engineer-os/DASHBOARDS/README.md)
