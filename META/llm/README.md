# LLM Rules

这个目录定义 LLM 应如何参与维护这个仓库。

这个仓库的设计原则是：  
human-owned, but LLM-assisted。

这意味着 LLM 可以是有用的贡献者，  
但前提是它必须运行在显式规则之下。

这个目录的作用，就是让这种协作变得更安全、更结构化、更可重复。

---

## 这个目录是做什么的

`META/llm/` 主要定义：

- LLM 被允许做什么
- LLM 不能做什么
- LLM 应如何理解仓库分层
- 常见更新 workflow 应如何处理
- 人类应如何 review LLM-generated changes

这些文件的作用，是把 LLM assistance 从 ad hoc prompting，变成 governed maintenance process。

---

## 为什么这一层重要

如果没有明确的 LLM rules，language model 很容易：

- over-generalize
- invent confidence
- blur source and synthesis
- rewrite structure incorrectly
- duplicate pages
- collapse distinctions between layer types

这个仓库的结构已经足够复杂，  
不能依赖 unconstrained generation。

`META/llm/` 的价值，就是给 LLM 一个清楚的 operating model。

---

## 核心文件

### `system_prompt.md`

定义 LLM 在这个仓库中的总体维护角色。

### `editing_rules.md`

定义具体编辑约束与行为规则。

### `update_workflows.md`

定义常见仓库更新的 repeatable workflows。

### `review_checklist.md`

定义人类如何 review LLM-generated updates。

---

## 期望中的 LLM 角色

在这个仓库里，LLM 更适合扮演：

- constrained maintainer
- structured drafting assistant
- synthesis helper
- linking assistant
- consistency helper

它不应扮演：

- unconstrained author
- truth source
- silent resolver of ambiguity
- authority above raw sources and metadata

---

## 设计原则

### 1. LLM 协助维护，但不拥有 truth

truth 来自更低层，尤其是 raw sources。

### 2. LLM 应改善结构与可读性

它的价值不只是生成文字，  
更是降低维护成本，同时保留 trust。

### 3. LLM 更新必须可 review

任何重要更新都应容易检查、容易推理、容易复核。

### 4. 显式 uncertainty 优于伪造 certainty

如果 ambiguity 是真实存在的，LLM 就应保留它。

### 5. Layer boundaries matter

一个好的 LLM maintenance system，必须尊重仓库架构本身。

---

## 什么时候应查看这个目录

在这些场景下，应查看 `META/llm/`：

- 让 LLM 创建新页面时
- 让 LLM 更新 wiki page 时
- 让 LLM 把 source 连接进结构化页面时
- review LLM output 是否安全可保留时
- 定义或微调 LLM 维护行为时

---

## 相关入口

- [Meta](../README.md)
- [Templates](../templates/README.md)
- [Policies](../policies/README.md)
