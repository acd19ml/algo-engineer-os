# Naming Convention Policy

这个文档定义目录、节点、文件和页面标题的命名规则。

目标是让仓库保持：

- readable
- consistent
- searchable
- easy to link
- easy to maintain

---

## 总体原则

### 1. 优先清晰，而不是花哨

名字应说明“它是什么”。

### 2. 优先稳定，而不是临时

除非确实必要，不要按短期上下文给对象命名。

### 3. 目录和文件优先使用 lowercase kebab-case

Examples:

- `interleaved-mrope`
- `long-context-extension`
- `skill-gap-analysis`

### 4. 优先明确，而不是缩写堆叠

只有在缩写本身已经是领域标准时，才使用缩写。

Good:

- `kv-cache`
- `rope`

Less good:

- `ctx-opt-final`
- `misc2`

---

## 目录命名规则

目录统一使用 lowercase kebab-case。

Examples:

- `multimodal`
- `distributed-training`
- `project-overviews`
- `career-guides`

不要使用：

- spaces
- camelCase
- `misc`、`other`、`temp` 这类模糊名字

---

## 文件命名规则

### README 文件

每个目录都应有一个 `README.md`。

### 模板文件

模板统一以 `.template.md` 结尾。

Examples:

- `node_README.template.md`
- `wiki_page.template.md`

### 规则文件

规则文件使用清晰、可描述的名字。

Examples:

- `source_of_truth.md`
- `naming_convention.md`
- `node_granularity.md`

---

## 节点命名规则

一个 node 的名字通常应对应这些对象之一：

- concept
- method
- system
- capability
- metric
- workflow
- tool

Examples:

- `transformer`
- `rope`
- `kv-cache`
- `beam-search`
- `distributed-training`

避免这些问题：

- 过宽
- 过泛
- 只对当前临时表述成立

Bad examples:

- `important-stuff`
- `notes-about-attention`
- `stuff-i-need-later`

---

## 问题页命名规则

problem page 应命名为 problem space，而不是简单 topic label。

Good:

- `multimodal-position-encoding`
- `long-context-degradation`
- `training-instability`
- `evaluation-mismatch`

Less good:

- `rope-problem`
- `context`
- `evaluation-notes`

---

## 项目命名规则

project 目录名应清楚反映项目目标。

Good:

- `qwen3-vl-reproduction`
- `retrieval-system-prototype`
- `latency-reduction-study`

Less good:

- `experiment1`
- `new-project`
- `my-test`

---

## Wiki 页命名规则

wiki page 文件名应描述页面内容，而不是只写主题名。

Good:

- `rope-family-overview.md`
- `multimodal-position-encoding.md`
- `navit-vs-fuyu-vs-vit.md`
- `qwen3-vl-overview.md`

---

## 资源文件命名规则

assets 应使用可描述的名字。

Good:

- `knowledge-graph-overview.png`
- `project-architecture-v1.svg`

Bad:

- `img1.png`
- `final-final-2.png`
- `newnew.png`

---

## 标题与目录名的区别

目录名 / 文件名 应尽量 machine-friendly。  
页面标题可以更 human-friendly。

Example:

- directory: `interleaved-mrope`
- title: `Interleaved M-RoPE`

---

## 重命名规则

当更清晰时，可以重命名；但要谨慎执行。

重命名前至少检查：

- links
- metadata references
- wiki references
- external repo references（如果相关）

尽量追求“更少但更好的名字”，避免频繁 churn。

---

## 总结

好的命名会降低几乎所有环节的摩擦：

- writing
- linking
- searching
- scripting
- browsing
- maintenance

如果一个名字现在就觉得模糊，之后通常只会更糟。
