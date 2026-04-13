# SCRIPTS

`SCRIPTS/` 是这个仓库存放自动化脚本的地方。

如果 `KNOWLEDGE/`、`PROBLEMS/`、`PROJECTS/` 等目录保存的是系统内容，  
那么 `SCRIPTS/` 保存的就是：**帮助这个系统长期保持可维护、可验证、可生成、可观察的工具**。

这一层是仓库的自动化运维层（operational automation layer）。

---

## 这一层是做什么的

`SCRIPTS/` 用于承接那些不应长期依赖手工完成的仓库级重复任务。

Examples:

- validating metadata
- checking broken references
- checking missing READMEs
- building graph outputs
- generating path views
- generating dashboards
- checking orphan nodes
- summarizing status across directories

没有这一层，仓库仍然能工作。  
但随着系统变大，维护成本会迅速上升。

---

## 为什么这一层重要

一个大型个人知识系统，不只是内容集合。  
它还需要：

- structure
- consistency
- observability

随着仓库增长，你会越来越频繁地想回答这些问题：

- 有没有节点缺少 metadata
- 有没有 dependency 写坏了
- 有没有 orphan nodes 没有任何引用
- 哪些 knowledge nodes 没有连到任何 problems
- 哪些 external repos 已经 stale
- 当前学习或 reproduction progress 到底是什么状态
- 能不能直接生成 dashboard，而不是每次手工整理

`SCRIPTS/` 的作用，就是让这些任务变得可重复、可验证、可依赖。

---

## 什么内容主要属于这里

当一个对象主要是在做 **maintenance、validation、generation 或 indexing** 时，它通常属于 `SCRIPTS/`。

Examples:

- metadata validators
- graph builders
- topo sort utilities
- stale asset checkers
- dashboard builders
- repo sync tools
- reference checkers
- coverage summaries

这一层不是用来保存领域知识本身的。  
它保存的是帮助你管理这些知识的程序。

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- repository rules -> `META/`
- generated views -> `OUTPUT/`
- static diagrams -> `assets/`
- domain knowledge -> `KNOWLEDGE/`
- personal reflections -> `THINKING/`

`SCRIPTS/` 是自动化层，不是内容层。

---

## 常见脚本类别

### Validation scripts

用于发现不一致或结构错误。

Examples:

- missing `README.md` checker
- invalid `meta.yaml` checker
- unknown dependency checker
- schema compliance checker
- broken link checker

这些脚本主要保护系统质量。

---

### Graph and path scripts

用于从 metadata 构建结构视图。

Examples:

- DAG builder
- topology sorter
- path generator
- node relationship exporter

这些脚本的作用，是把结构变成可用导航。

---

### Dashboard scripts

用于生成可观察性视图。

Examples:

- progress dashboard generator
- project status rollup
- skill gap summary builder
- external repo status summary

这些脚本的作用，是降低 steering 与 prioritization 成本。

---

### Sync or indexing scripts

用于连接本仓库与外部资产。

Examples:

- sync external repo metadata
- refresh experiment index
- collect last-checked dates
- summarize external implementation coverage

这些脚本的作用，是加强知识与执行资产之间的连接。

---

## 推荐子结构

一开始保持简单即可：

```text
SCRIPTS/
├── README.md
├── validate_meta.py
├── build_dag.py
├── topo_sort.py
├── check_orphans.py
├── build_dashboards.py
└── sync_external_repos.py
```

脚本数量增多以后，再按子目录拆分也不迟。

---

## 设计原则

### 1. Scripts should support the repository, not dominate it

这是一个知识系统优先的仓库，不是一个为了写工具而写工具的项目。

### 2. Prefer useful automation over excessive automation

优先自动化那些重复、易错、手工维护成本高的任务。

### 3. Keep scripts understandable

未来的你应该能快速理解一个脚本做什么、为什么存在。

### 4. Separate source content from generated output

脚本应从源内容读取，并把结果写到 `OUTPUT/` 或明确约定的目标文件。

### 5. Prefer idempotent behavior where possible

同一个脚本多跑一次，不应制造混乱的重复或额外漂移。

---

## 一个好脚本应该降低什么成本

一个值得留下来的脚本，通常应显著降低以下至少一种成本：

- maintenance cost
- validation cost
- navigation cost
- observability cost
- consistency cost

如果一个脚本没有明确降低其中任何一种成本，它大概率还不值得长期保留。

---

## 这一层如何与其它层协作

### With `META/`

脚本应尊重 schema、templates 和 repository policies。

### With `KNOWLEDGE/`

脚本可以验证 node 结构，也可以生成 graph views。

### With `PROBLEMS/`

脚本可以汇总 problem coverage 或缺失连接。

### With `PROJECTS/`

脚本可以汇总 project status 或检查缺失链接。

### With `REPRO_INDEX/`

脚本可以刷新或汇总 external repo metadata。

### With `DASHBOARDS/`

部分 dashboard 页面可以由脚本生成或刷新。

### With `OUTPUT/`

大多数生成型 artifacts 应写到这里，而不是混进 source content。

---

## 当前阶段的重点

`SCRIPTS/` 的第一阶段建议优先：

- metadata validation
- orphan node checking
- basic DAG generation
- simple path generation
- lightweight dashboard generation

这已经足够显著提升整个系统的可维护性。

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [META](/Users/mac/studyspace/algo-engineer-os/META/README.md)
- [DASHBOARDS](/Users/mac/studyspace/algo-engineer-os/DASHBOARDS/README.md)
- [OUTPUT](/Users/mac/studyspace/algo-engineer-os/OUTPUT/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [REPRO_INDEX](/Users/mac/studyspace/algo-engineer-os/REPRO_INDEX/README.md)
