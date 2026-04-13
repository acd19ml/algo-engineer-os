# WIKI

`WIKI/` 是这个仓库的编译后的可读层（compiled readable layer）。

如果 `RAW_SOURCES/` 保存证据，`KNOWLEDGE/` 保存结构化节点，  
那么 `WIKI/` 的作用就是：**把底层内容编译成更容易阅读、比较、回顾和重访的页面**。

Wiki page 不是基础真值层。  
它是一个 **compiled synthesis layer**，建立在更低层的证据、节点、问题页与项目页之上。

---

## 这一层是做什么的

`WIKI/` 主要服务这些需求：

- 我不想来回打开五个节点页，只想先看一个清晰 overview
- 我想在一个地方比较多种方法
- 我想快速理解一个问题空间
- 我想看一个模型或系统的整体图景
- 我想把分散的项目、工作或职业材料编译成可复用页面

没有这一层，仓库可以很精确。  
但它会越来越难被快速导航、快速比较、快速复习。

---

## 这一层为什么特殊

`WIKI/` 不是另一个普通笔记目录。

它遵循一个核心原则：

> **Wiki pages are compiled, not primary.**

这意味着：

- 它们建立在更底层页面之上
- 它们提升的是 readability 与 synthesis
- 它们必须保持可追溯性
- 它们不应该替代 source of truth

一个好的 wiki page 应该帮助你更快思考，  
而不是模糊“事实、结构化描述、综合总结”之间的边界。

---

## 什么内容主要属于这里

当一个页面主要是在做 **cross-node synthesis** 时，它通常属于 `WIKI/`。

Examples:

- concept overviews
- problem syntheses
- comparison pages
- model overviews
- project overviews
- career guides
- open question summaries

一个 wiki page 通常会从这些层吸收内容：

- `RAW_SOURCES/`
- `KNOWLEDGE/`
- `PROBLEMS/`
- `PROJECTS/`
- `WORK/`
- `CAREER/`

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- 原始证据与阅读摘录 -> `RAW_SOURCES/`
- 稳定主题节点 -> `KNOWLEDGE/`
- 问题定义与方案空间 -> `PROBLEMS/`
- 具体项目执行记录 -> `PROJECTS/`
- 日常工作 SOP 与 incident notes -> `WORK/`
- 职业资产原件 -> `CAREER/`

`WIKI/` 更适合做“编译与整合”，而不是做第一落点。

---

## 常见 wiki page 类型

### `concepts/`

高层概念总览页。

Examples:

- transformer overview
- rope family overview
- multimodal training overview

这类页面帮助回答：

- 这个领域的整体版图是什么
- 关键组件有哪些
- 它们之间如何拼起来

---

### `problem-syntheses/`

重要问题空间的综合页。

Examples:

- long context in LLMs
- multimodal position encoding
- evaluation reliability

这类页面帮助回答：

- 问题空间长什么样
- 主流方案有哪些
- 哪些 trade-off 最重要

---

### `comparisons/`

方法、系统或设计选择的对比页。

Examples:

- rope vs alibi
- mrope vs interleaved-mrope
- navit vs fuyu vs vit

这类页面帮助回答：

- 这些选项哪里相似
- 哪里不同
- 在什么前提下应选哪一个

---

### `model-overviews/`

完整系统或模型的结构化总览。

Examples:

- qwen3-vl overview
- llama inference stack overview
- a production recommendation system overview

这类页面帮助回答：

- 系统由哪些主要组件构成
- 关键设计选择是什么
- 接下来该看哪些节点或问题页

---

### `project-overviews/`

项目层面的高层总结页。

Examples:

- a multimodal reproduction project
- a work project architecture summary
- a side project learning summary

这类页面帮助回答：

- 做了什么
- 用了哪些知识
- 学到了什么
- 哪些部分可复用

---

### `career-guides/`

支持职业成长的编译页。

Examples:

- interview preparation guide
- algorithm engineer skill map
- project storytelling guide

这类页面帮助回答：

- 哪些能力最重要
- 当前缺什么
- 如何把技术工作转成 career assets

---

### `open-questions/`

跨主题的未决问题汇总页。

Examples:

- unresolved questions in multimodal token organization
- open questions in long-context evaluation
- what I still do not understand about training stability

这类页面帮助回答：

- 目前到底还不清楚什么
- 下一步值得调查什么

---

## 一个 wiki page 应包含什么

一个强的 wiki page 通常至少应覆盖：

### 1. Scope

这页到底覆盖什么，不覆盖什么。

### 2. Compiled sources

它是从哪些 lower-level pages 或材料编译出来的。

### 3. Main synthesis

这页最核心的 takeaway 是什么。

### 4. Structure or comparison

主要维度、方案、组件或比较轴是什么。

### 5. Caveats

哪些部分仍不确定、不完整、或者证据还弱。

### 6. Related pages

读者接下来应该跳去哪些 nodes、problems、projects。

---

## 这一层的写作原则

### 1. Readability over fragmentation

wiki page 的目标，是降低理解成本。

### 2. Traceability over convenience

写得顺手不能代替可追溯性。

### 3. Synthesis over duplication

不要把多个节点原样拷贝后拼在一起。

### 4. Uncertainty should remain visible

综合不完整时，要明确写出来。

### 5. Compiled does not mean authoritative

wiki page 很有用，但它不是根真值层。

---

## 推荐目录结构

```text
WIKI/
├── README.md
├── concepts/
├── problem-syntheses/
├── comparisons/
├── model-overviews/
├── project-overviews/
├── career-guides/
└── open-questions/
```

这些分类只是帮助导航。  
不要把分类本身误当成知识依赖或问题依赖。

---

## Frontmatter 建议

为了让这一层更可维护、也更适合 LLM 参与维护，  
建议 wiki page 在 frontmatter 中至少标注：

- `title`
- `page_type`
- `compiled_from`
- `last_compiled_at`
- `confidence`

例如：

```yaml
title: Multimodal Position Encoding
page_type: problem_synthesis
compiled_from:
  - ../../PROBLEMS/position-encoding-for-multimodal/README.md
  - ../../KNOWLEDGE/multimodal/rope/README.md
  - ../../KNOWLEDGE/multimodal/mrope/README.md
last_compiled_at: 2026-04-14
confidence: mixed
```

这有两个好处：

- 方便人类回溯编译来源
- 方便 LLM 判断应该更新什么、不该越权改什么

---

## 这一层应如何维护

### 手工维护时

适合用 `WIKI/` 来：

- 总结一个节点簇
- 比较几个 alternatives
- 形成复用型 review page
- 为后续学习或面试准备提供速查入口

### LLM 辅助维护时

LLM 可以帮助：

- 跨多个节点页做 synthesis
- 改善内部链接
- 更新 comparison tables
- 归纳 open questions

但 LLM 不应该：

- invent evidence
- silently override structured truth
- turn guesses into established facts

所有 LLM-assisted updates 都应遵守 `META/llm/` 下的规则。

---

## Source of Truth 提醒

`WIKI/` 的价值在于综合，不在于“定案”。

当 Wiki 与更底层页面冲突时，应优先相信：

1. `RAW_SOURCES/`
2. `KNOWLEDGE/*/meta.yaml`
3. `KNOWLEDGE/*/README.md`
4. `PROBLEMS/`
5. `WIKI/`

因此，wiki page 应尽量：

- 显式指出 compiled-from 来源
- 避免替代底层结构页
- 避免把综合判断写成未经确认的事实

---

## 这一层如何与其它层协作

### With `RAW_SOURCES/`

wiki page 应保持对 source material 的 grounded connection。

### With `KNOWLEDGE/`

wiki page 常常是从多个 nodes 编译出来的。

### With `PROBLEMS/`

wiki page 往往会整合整个 problem space。

### With `PROJECTS/`

wiki page 可以把项目经验转成可复用总结。

### With `CAREER/`

wiki page 可以支撑 interview prep 和 skill development。

---

## 当前阶段的重点

`WIKI/` 的第一阶段建议优先：

- a small number of high-value overview pages
- a few comparison pages
- a few problem synthesis pages
- explicit `compiled_from` metadata
- clear separation from source-of-truth layers

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [META](/Users/mac/studyspace/algo-engineer-os/META/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [PROBLEMS](/Users/mac/studyspace/algo-engineer-os/PROBLEMS/README.md)
