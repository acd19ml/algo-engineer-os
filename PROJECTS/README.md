# PROJECTS

`PROJECTS/` 是这个仓库把知识连接到真实执行的地方。

如果 `KNOWLEDGE/` 保存可复用的概念与方法，`PROBLEMS/` 保存以挑战为中心的问题视角，  
那么 `PROJECTS/` 的作用就是：**把这些知识和问题真正转成实际产出**。

项目是学习变成实现、研究变成 artifact、经验变成可复用专业材料的地方。

---

## 这一层是做什么的

`PROJECTS/` 用于组织那些具有明确执行边界的工作。

Examples:

- a research reproduction project
- a multimodal learning project
- a side project for experimentation
- a work project with technical design and implementation
- a small tool built to solve a recurring engineering need

没有这一层，知识会越来越完整，  
但很难被稳定地转成真实结果、真实经验和真实能力证明。

---

## 为什么这一层重要

一个强的算法工程师不只需要“知道概念”，  
还需要能够：

- 在具体场景里应用知识
- 把方法放进真实约束中做选择
- 做设计决策
- 排查失败与异常
- 记录 trade-off
- 向别人解释结果与价值

这些能力最清楚地体现在项目里。

这一层帮助你回答：

- 我到底真正做过什么
- 我用了哪些知识
- 我遇到了哪些问题
- 牵涉了哪些代码、实验与 repo
- 哪些经验以后还可以复用
- 哪些内容可以转成 work asset 或 interview story

---

## 什么内容主要属于这里

当一个对象主要是在描述 **有明确目标的 bounded work** 时，它通常属于 `PROJECTS/`。

Examples:

- a Qwen3-VL reading and reproduction effort
- a retrieval system prototype
- a training pipeline experiment
- a model serving optimization project
- a side project for evaluating long-context behavior
- a work project on feature ranking or recommendation

一个项目页不应该只是原始日志。  
它应该成为一份“可复用的执行记忆”。

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- 稳定主题节点与机制说明 -> `KNOWLEDGE/`
- 问题定义与方案空间 -> `PROBLEMS/`
- 编译型综合页 -> `WIKI/`
- 外部 repo 与实验索引 -> `REPRO_INDEX/`
- 日常 SOP、incident notes、复盘套路 -> `WORK/`
- 职业表达与角色准备 -> `CAREER/`

`PROJECTS/` 的重点不是“解释一个概念”，  
而是“保留一次真实执行是如何发生的”。

---

## 推荐子结构

```text
PROJECTS/
├── README.md
├── research/
├── work/
├── side-projects/
└── archived/
```

这些分类只是实践上的分组，不是硬边界。

### `research/`

用于 paper reproductions、technical explorations 和 research-driven investigations。

### `work/`

用于与岗位职责、业务目标或真实交付直接相关的项目。

### `side-projects/`

用于自发发起的实验、工具、小系统或学习型构建。

### `archived/`

用于保存已完成、暂停或不再活跃但仍值得保留的项目。

---

## 一个项目页应包含什么

一个强的项目页通常应覆盖：

### 1. Project summary

项目是什么，目标是什么。

### 2. Motivation

为什么做这个项目，它想解决什么问题。

### 3. Scope

什么在范围内，什么明确不做。

### 4. Related knowledge nodes

这个项目用了哪些 topics、methods、capabilities。

### 5. Related problems

它涉及哪些技术问题或实际问题。

### 6. Related repos

相关 external repos、experiments、scripts 是什么。

### 7. Key decisions

做了哪些关键设计或实验决策。

### 8. Results or current status

已经完成了什么，还剩什么。

### 9. Lessons learned

哪些经验下次应复用，哪些坑应避免。

### 10. Career value

它如何转成简历 bullet、interview story 或 skill proof。

---

## 一个项目页通常应连接什么

一个项目页通常应回链到：

- `KNOWLEDGE/` 中使用到的 nodes
- `PROBLEMS/` 中相关的 challenge pages
- `REPRO_INDEX/` 中相关代码与实验 repos
- `WORK/` 中沉淀出来的 playbooks 或 design notes
- `CAREER/` 中项目表达、岗位匹配与故事页
- `THINKING/` 中更高层的反思、判断与原则

这正是项目页在项目结束后仍然有价值的原因。

---

## 设计原则

### 1. Projects are not just logs

项目页应保留结构，而不只是时间顺序。

### 2. Connect execution back to knowledge

一个有价值的项目，应反过来强化知识图谱。

### 3. Preserve decisions, not just outcomes

很多时候，路径比最终结果更值得保留。

### 4. Make reuse easy

未来的你打开一个项目页时，应能快速知道：

- 它是什么
- 关键点是什么
- 哪些内容可复用

### 5. Preserve unfinished work

项目不必“完全成功”才值得保留。  
partial work 也可能带来 insight、code、validation 和 interview material。

---

## 推荐项目页结构

一个最小可用项目页可以很轻：

- `Title`
- `Goal`
- `Motivation`
- `Scope`
- `Related knowledge`
- `Related problems`
- `Related repos`
- `Status`
- `Key learnings`
- `Next steps`

这样既不会太重，也能保留足够多的上下文。

---

## 这一层如何与其它层协作

### With `KNOWLEDGE/`

projects 把 knowledge nodes 放进真实上下文里使用。

### With `PROBLEMS/`

projects 会暴露哪些问题在实践里真正重要。

### With `REPRO_INDEX/`

projects 往往依赖 external code 和 experiments。

### With `WORK/`

projects 会沉淀出可复用的 SOP、playbooks 和 design notes。

### With `CAREER/`

projects 会变成故事、证据和职业成长信号。

### With `THINKING/`

projects 往往会触发新的问题、比较和设计原则。

---

## 当前阶段的重点

`PROJECTS/` 的第一阶段建议优先：

- creating a small number of meaningful project pages
- linking them to knowledge nodes and problems
- connecting them to external repos
- recording decisions and lessons learned
- turning project memory into reusable professional assets

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [PROBLEMS](/Users/mac/studyspace/algo-engineer-os/PROBLEMS/README.md)
- [REPRO_INDEX](/Users/mac/studyspace/algo-engineer-os/REPRO_INDEX/README.md)
- [CAREER](/Users/mac/studyspace/algo-engineer-os/CAREER/README.md)
- [WIKI](/Users/mac/studyspace/algo-engineer-os/WIKI/README.md)
