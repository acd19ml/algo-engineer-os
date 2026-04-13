# OUTPUT

`OUTPUT/` 是这个仓库存放派生产出的地方。

如果 `SCRIPTS/` 保存的是工具，  
那么 `OUTPUT/` 保存的就是这些工具运行后的结果。

这一层存在的意义，是把 generated artifacts 和 source content 清楚分开。

---

## 这一层是做什么的

`OUTPUT/` 用于存放那些由脚本或仓库工作流生成的派生文件，例如：

- graph exports
- dashboard snapshots
- path outputs
- summary tables
- generated status pages
- machine-readable indexes

这些文件不是 primary source of truth。  
它们是从真实源层编译、导出或快照出来的视图。

---

## 为什么这一层重要

一个知识系统通常同时包含两类内容。

### Source content

由你直接编写和维护。

Examples:

- node READMEs
- `meta.yaml`
- problem pages
- project pages
- work notes
- career assets

### Derived content

由脚本或流程从 source content 生成。

Examples:

- DAG visualizations
- progress summaries
- auto-generated indexes
- current path rollups
- stale asset reports

如果这两类东西混在一起，仓库会越来越难理解，也越来越难维护。

`OUTPUT/` 的作用，就是把这种区别明确下来。

---

## 什么内容主要属于这里

当一个文件主要是 **generated artifact 或 derived view** 时，它通常属于 `OUTPUT/`。

Examples:

- `dag.svg`
- `graph.json`
- `progress_dashboard.md`
- `path_outputs/`
- `repo_health_report.md`
- `coverage_summary.json`

一个文件通常属于这里，当它满足以下特征：

- 它是从别的文件构建出来的
- 它不是 canonical source
- 它以后可以被重新生成

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- canonical content -> `KNOWLEDGE/`, `PROBLEMS/`, `PROJECTS/` 等
- repository rules -> `META/`
- automation code -> `SCRIPTS/`
- static manually managed images -> `assets/`

`OUTPUT/` 只用于保存 derived artifacts。

---

## 常见 output 类型

### Graph outputs

从 node metadata 和关系生成。

Examples:

- DAG diagrams
- graph JSON exports
- dependency maps
- subgraph views

这类输出主要帮助观察结构。

---

### Dashboard outputs

用于生成或刷新状态汇总。

Examples:

- progress dashboard
- project rollup
- active paths summary
- reproduction coverage summary

这类输出主要帮助观察系统状态和优先级。

---

### Path outputs

用于生成推荐序列的视图。

Examples:

- topologically sorted study paths
- role-based readiness paths
- project preparation sequences

这类输出主要帮助把 graph 转成 navigation。

---

### Health or maintenance reports

用于观察仓库健康状态。

Examples:

- orphan node reports
- missing README reports
- stale repo reports
- invalid metadata reports

这类输出主要帮助保持系统健康。

---

## 推荐子结构

一开始使用轻量结构即可：

```text
OUTPUT/
├── README.md
├── dag.svg
├── graph.json
├── progress_dashboard.md
├── repo_health_report.md
└── path_outputs/
```

当产出体量增加后，再按类型拆子目录也不迟。

---

## 设计原则

### 1. Output is not truth

generated files 不应替代 source content。

### 2. Keep outputs reproducible

一个好的 output 应该可以从 source files 和 scripts 重新生成。

### 3. Prefer clarity over accumulation

不要因为“也许以后有用”就无限保留临时输出。

### 4. Make generated status easy to inspect

output 的目标之一，是让你更快看懂系统当前状态。

### 5. Keep source and derived layers separate

这正是这个目录存在的主要原因。

---

## 这一层应该帮助你回答什么

一个好的 `OUTPUT/` 应该让你快速回答：

- 当前知识图谱长什么样
- 当前有哪些 active paths
- 仓库健康状态如何
- 已经取得了什么进展
- 哪些区域还很浅，或者已经 stale

---

## 这一层如何与其它层协作

### With `SCRIPTS/`

很多文件会由这里的脚本生成或刷新。

### With `DASHBOARDS/`

部分 dashboard 页面可能被生成到 `OUTPUT/`，或从这里镜像过去。

### With `KNOWLEDGE/`

一些 output 会汇总 node relationships、status 与 progress。

### With `REPRO_INDEX/`

一些 output 会汇总 external repo coverage 与 health。

### With `PATHS/`

一些 output 会保存 path views 或 path snapshots。

---

## 版本管理建议

有些 output 很适合提交到 Git，因为它们在浏览器里也有直接价值。

Examples:

- `dag.svg`
- `progress_dashboard.md`

另一些 output 更偏临时或机器使用，可以按需忽略。

Examples:

- intermediate JSON files
- temporary reports
- local-only snapshots

具体是否提交，可以通过 `.gitignore` 按“是否值得长期保留”来判断。

---

## 当前阶段的重点

`OUTPUT/` 的第一阶段建议优先：

- one graph view
- one progress summary
- one repo health summary
- one path output directory

这已经足够在不增加太多复杂度的前提下，让系统更可观察。

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [SCRIPTS](/Users/mac/studyspace/algo-engineer-os/SCRIPTS/README.md)
- [DASHBOARDS](/Users/mac/studyspace/algo-engineer-os/DASHBOARDS/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [PATHS](/Users/mac/studyspace/algo-engineer-os/PATHS/README.md)
