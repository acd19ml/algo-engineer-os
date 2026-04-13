# DASHBOARDS

`DASHBOARDS/` 是这个仓库存放系统当前状态视图的地方。

如果 `KNOWLEDGE/` 保存结构，`PROJECTS/` 保存执行，`PATHS/` 保存方向，  
那么 `DASHBOARDS/` 的作用就是回答：

- 现在什么是活跃的
- 现在缺什么
- 什么在推进
- 什么需要注意
- 这个系统此刻到底长什么样

这一层存在的意义，是让仓库变得可观察（observable）。

---

## 这一层是做什么的

`DASHBOARDS/` 提供一组 summary views，帮助你把这个仓库当作一个活系统来观察和管理。

Examples:

- knowledge map
- current focus
- skill progress
- job readiness
- project status
- active paths
- open gaps
- stale repos or outdated pages

没有这一层，系统可能会长得很好，  
但会越来越难被“看清”和“转向”。

---

## 为什么这一层重要

一个大型仓库可以非常有价值，  
但也可能越来越难一眼看清。

你可能同时拥有：

- 很多 nodes
- 很多 projects
- 很多未完成的想法
- 多个 external repos
- 不完整的 comparisons
- 不断变化的 priorities

如果这些都埋在目录里，就很难回答一些简单但重要的问题：

- 我这周到底该重点做什么
- 我已经真正做成了什么
- 我最大的 gap 在哪里
- 哪些东西已经 stale
- 哪些最接近变成高价值资产

`DASHBOARDS/` 的作用，就是让系统更容易被观察、被优先级化、被维护。

---

## 什么内容主要属于这里

当一个页面主要是在提供 **state view** 而不是 source layer 时，它通常属于 `DASHBOARDS/`。

Examples:

- current focus page
- skill progress summary
- project status page
- active path tracker
- repo health overview
- stale asset tracker
- learning coverage summary

这一层关心的是可见性，不是细节本身。

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- 事实与结构定义 -> `KNOWLEDGE/`
- 真实执行记录 -> `PROJECTS/`
- 职业资产原件 -> `CAREER/`
- path 本身 -> `PATHS/`
- 外部 repo 状态原始索引 -> `REPRO_INDEX/`
- 反思、判断与方向变化 -> `THINKING/`

dashboard 应该是 view，而不是唯一真值来源。

---

## 推荐子结构

一个轻量结构通常就足够：

```text
DASHBOARDS/
├── README.md
├── knowledge-map.md
├── current-focus.md
├── skill-progress.md
├── job-readiness.md
├── project-status.md
└── active-paths.md
```

一开始尽量简单。  
后续需要时再扩展。

---

## 常见 dashboard 页面

### `knowledge-map.md`

用于高层观察知识覆盖度。

可以总结：

- major domains
- foundational gaps
- mature clusters
- areas with strong project linkage
- areas that are still shallow

---

### `current-focus.md`

用于近周期优先级管理。

它应帮助回答：

- 我现在在聚焦什么
- 哪些 nodes、problems、projects 正在活跃
- 这周有哪些事情不该分散注意力

这通常是最有价值的 dashboard 之一。

---

### `skill-progress.md`

用于追踪能力成长。

可以观察：

- theory understanding
- implementation skill
- systems awareness
- evaluation maturity
- communication readiness
- role-specific capability growth

---

### `job-readiness.md`

用于观察目标岗位准备度。

它应帮助回答：

- 我现在瞄准哪些 roles
- 我离它们还有多远
- 还缺哪些关键点
- 哪些当前项目最能支撑 readiness

这类页面和 `CAREER/` 配合会很强。

---

### `project-status.md`

用于汇总 active、paused 和 archived projects。

它应帮助回答：

- 什么在 active
- 什么被 block 住了
- 什么正在 drift
- 什么该 revive，什么该 close

---

### `active-paths.md`

用于汇总当前正在推进的路径。

它可以跟踪：

- current topic paths
- role-based paths in progress
- interview paths if needed
- reached / pending milestones

---

## 设计原则

### 1. Dashboards are views, not truth layers

dashboard 是对底层信息的总结，  
不应成为事实唯一存在的地方。

### 2. Prefer clarity over completeness

一个有用的 dashboard 应帮助决策，而不是增加压迫感。

### 3. Keep dashboards actionable

dashboard 应帮助你决定下一步做什么。

### 4. Separate active attention from full inventory

不是所有重要内容都需要同时出现在每个 dashboard 里。

### 5. Allow a mix of manual and generated views

有些 dashboard 一开始适合手工维护，  
有些以后可以部分脚本生成。两种都没问题，只要目的清楚。

---

## 这一层如何与其它层协作

### With `KNOWLEDGE/`

dashboard 可以总结 node coverage 与成熟度。

### With `PROJECTS/`

dashboard 可以显示哪些项目 active、blocked 或 done。

### With `CAREER/`

dashboard 可以反映 readiness 与 skill-gap progress。

### With `PATHS/`

dashboard 可以跟踪当前活跃 path 的进度和焦点。

### With `REPRO_INDEX/`

dashboard 可以显示 implementation coverage 或 stale external repos。

### With `THINKING/`

dashboard 也可以反映被反思和决策影响后的当前优先级。

---

## 手工与生成式 dashboard

一些 dashboard 页面在早期更适合手工维护。

Examples:

- `current-focus.md`
- `job-readiness.md`

另一些页面以后可以部分由 metadata 或 scripts 生成。

Examples:

- node coverage summaries
- reproduction status summaries
- stale asset reports
- path progress rollups

这种混合模式是刻意保留的灵活性。

---

## 当前阶段的重点

`DASHBOARDS/` 的第一阶段建议优先：

- one `current-focus.md` page
- one `skill-progress.md` page
- one `project-status.md` page
- one `job-readiness.md` page
- a lightweight overview of active paths

通常这几页就足以让整个系统更容易被驾驶。

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [PROJECTS](/Users/mac/studyspace/algo-engineer-os/PROJECTS/README.md)
- [CAREER](/Users/mac/studyspace/algo-engineer-os/CAREER/README.md)
- [PATHS](/Users/mac/studyspace/algo-engineer-os/PATHS/README.md)
- [THINKING](/Users/mac/studyspace/algo-engineer-os/THINKING/README.md)
- [REPRO_INDEX](/Users/mac/studyspace/algo-engineer-os/REPRO_INDEX/README.md)
