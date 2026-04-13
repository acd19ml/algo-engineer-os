# WORK

`WORK/` 是这个仓库沉淀日常工程工作可执行资产的地方。

如果 `KNOWLEDGE/` 帮你理解，`PROJECTS/` 帮你完成有边界的工作，  
那么 `WORK/` 的作用就是：**让你在反复出现的真实工作场景里执行得更稳定、更高效、更可复用**。

这一层承接的是：  
知识如何变成可重复实践（repeatable practice）。

---

## 这一层是做什么的

`WORK/` 主要服务那些会反复出现、带有约束、而且经常伴随时间压力的工程工作。

Examples:

- recurring engineering tasks
- debugging workflows
- design patterns
- deployment checklists
- incident handling notes
- team communication templates
- evaluation and reporting routines

没有这一层，有价值的工作知识通常会散落在记忆、聊天记录和临时笔记里。  
结果就是：每次都像第一次做。

---

## 为什么这一层重要

一个强的算法工程师不只需要懂方法，  
还需要知道如何：

- execute reliably
- debug efficiently
- communicate clearly
- reuse what worked before
- avoid repeating avoidable mistakes
- turn one-off experience into repeatable leverage

这正是 `WORK/` 存在的原因。

这一层帮助你回答：

- 这个任务下次怎么再做一遍
- 这类事情通常会在哪里出错
- 上线前我应该检查什么
- 我该如何向队友解释状态、风险和 trade-off
- 上一次在压力下学到的东西，这次如何不再重新发现

---

## 什么内容主要属于这里

当一个对象主要是在描述 **reusable operational or execution knowledge** 时，它通常属于 `WORK/`。

Examples:

- playbooks
- incident notes
- design notes
- recurring task SOPs
- evaluation runbooks
- debugging checklists
- deployment notes
- experiment review templates
- meeting or reporting templates

这一层不是原始项目历史。  
它更适合存放从项目和工作经验中抽出来的 **可复用工作模式**。

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- raw learning material -> `RAW_SOURCES/`
- concept and method explanations -> `KNOWLEDGE/`
- challenge-centered synthesis -> `PROBLEMS/`
- bounded project history -> `PROJECTS/`
- personal reflections -> `THINKING/`
- job-targeted positioning -> `CAREER/`

当然，这些层仍然应该在需要时回链到相关 work assets。

---

## 推荐子结构

```text
WORK/
├── README.md
├── playbooks/
├── incident-notes/
├── design-notes/
├── recurring-tasks/
└── templates/
```

### `playbooks/`

用于可复用的 step-by-step 执行指南。

Examples:

- how to investigate a training instability issue
- how to evaluate a new model checkpoint
- how to onboard a new experiment repo
- how to prepare a model comparison report

---

### `incident-notes/`

用于记录 operational issues、失败案例与从中提炼出来的经验。

Examples:

- deployment rollback notes
- silent data issue postmortem
- model collapse debugging summary
- inference latency spike investigation

---

### `design-notes/`

用于更偏工作面的技术设计文档。

Examples:

- data pipeline design note
- model serving design note
- evaluation framework note
- feature store usage note

---

### `recurring-tasks/`

用于那些应该逐步变成 routine 的重复性流程。

Examples:

- weekly experiment review
- monthly model performance audit
- dataset quality checklist
- benchmark refresh workflow

---

### `templates/`

用于通用模板与沟通结构。

Examples:

- experiment summary template
- design review template
- postmortem template
- status update template

---

## 一个强的 work asset 应包含什么

一个强的 work asset 的目标，是降低未来执行成本。

一个好页面通常会包含：

### 1. Context

它在什么情境下有用。

### 2. Trigger

什么时候应该打开这页。

### 3. Steps

应该按什么顺序执行。

### 4. Common pitfalls

最常见的问题和误区是什么。

### 5. Inputs and outputs

输入是什么，预期产出是什么。

### 6. Related tools or repos

涉及哪些系统、脚本、环境或 repo。

### 7. Related knowledge

它依赖哪些 concepts、methods 或 nodes。

### 8. Review notes

下一次应该改进什么。

---

## 设计原则

### 1. Prefer reuse over reinvention

如果一个任务会出现不止一次，它大概率就值得有一份可复用页面。

### 2. Keep pages operational

一个好的 work page 应帮助你行动，而不只是帮助你回顾。

### 3. Extract patterns from projects

projects 产生一次性经验，  
`WORK/` 要把这些经验转成可重复实践。

### 4. Keep failure knowledge visible

incident notes 和 postmortems 不是杂物，  
它们是高价值资产。

### 5. Support communication, not just execution

工作不只是做事，也包括清楚地同步状态、解释决策和沟通 trade-off。

---

## 这一层如何与其它层协作

### With `KNOWLEDGE/`

work assets 往往依赖知识节点中的技术理解。

### With `PROBLEMS/`

反复出现的 operational issues 可能逐步升级成正式 problem pages。

### With `PROJECTS/`

projects 是可复用 work patterns 的重要来源。

### With `REPRO_INDEX/`

一些工作任务会依赖 external repos、scripts 或 environments。

### With `CAREER/`

强的 work assets 往往能成为 ownership、execution ability 和 maturity 的证据。

### With `THINKING/`

反思与 decision logs 之后常常会被提炼成 playbooks、checklists 或 templates。

---

## 当前阶段的重点

`WORK/` 的第一阶段建议优先：

- recording recurring tasks
- creating a few high-value playbooks
- capturing failure handling notes
- preserving useful templates
- extracting reusable patterns from ongoing projects

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [PROBLEMS](/Users/mac/studyspace/algo-engineer-os/PROBLEMS/README.md)
- [PROJECTS](/Users/mac/studyspace/algo-engineer-os/PROJECTS/README.md)
- [CAREER](/Users/mac/studyspace/algo-engineer-os/CAREER/README.md)
- [THINKING](/Users/mac/studyspace/algo-engineer-os/THINKING/README.md)
- [REPRO_INDEX](/Users/mac/studyspace/algo-engineer-os/REPRO_INDEX/README.md)
