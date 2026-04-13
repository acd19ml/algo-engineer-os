# Source of Truth Policy

这个文档定义仓库的 source-of-truth hierarchy。

目标很简单：  
当不同页面之间出现冲突时，我们要知道应该先信哪一层。

---

## 真值优先级

这个仓库遵循下面的优先顺序：

1. `RAW_SOURCES/`
2. `KNOWLEDGE/*/meta.yaml`
3. `KNOWLEDGE/*/README.md`
4. `PROBLEMS/`
5. `WIKI/`
6. `DASHBOARDS/`
7. `OUTPUT/`

---

## 每一层分别意味着什么

### 1. `RAW_SOURCES/`

这是首要证据层。

Examples:

- papers
- docs
- books
- course material
- raw notes copied from original sources

当你在问这些问题时，应优先看这一层：

- 原始资料到底怎么说
- 原始上下文到底是什么
- 当前总结是否已经偏离证据

---

### 2. `KNOWLEDGE/*/meta.yaml`

这是首要结构层。

它主要定义：

- dependencies
- node type
- related problems
- alternatives
- progress
- external repo links

当你在问这些问题时，应优先看这一层：

- 官方关系结构是什么
- 这个 node 依赖什么
- 这个 node 连到哪些 problems

如果 prose 与 metadata 在“结构关系”上冲突，以 metadata 为准。

---

### 3. `KNOWLEDGE/*/README.md`

这是首要节点解释层。

它主要定义：

- 这个 node 是什么
- 它为什么重要
- 它在概念上如何连接到其它对象

当你在问这些问题时，应优先看这一层：

- 系统目前如何解释这个主题
- 读者应该先理解什么

---

### 4. `PROBLEMS/`

这是问题 framing 层。

它主要定义：

- 系统如何表述 challenge space
- 哪些 solution families 相关
- 哪些 trade-offs 值得关注

当你在问这些问题时，应优先看这一层：

- 为什么这个方法重要
- 我们当前处在什么问题空间里

---

### 5. `WIKI/`

这是 compiled synthesis 层。

它主要提升：

- readability
- comparison
- cross-node understanding

但它不是底层真值层。

当你在问这些问题时，适合优先看这一层：

- 全局图景是什么
- 哪里能快速看到一个综合总结

不要用这一层去静默覆盖更低层。

---

### 6. `DASHBOARDS/`

这是 observability 层。

它展示当前视图与优先级，但不是 authoritative truth。

---

### 7. `OUTPUT/`

这是 derived artifact 层。

它保存生成文件，不应被当成根真值。

---

## 冲突处理规则

### Rule 1

如果 wiki page 与 raw sources 冲突，以 raw sources 为准。

### Rule 2

如果 node README 与 `meta.yaml` 在 dependency structure 上冲突，以 `meta.yaml` 为准。

### Rule 3

如果 dashboard 与 source layer 冲突，以 source layer 为准。

### Rule 4

如果底层本身存在歧义，不要发明确定性。  
应该显式记录这种歧义。

### Rule 5

如果一个页面依赖的是 interpretation 而不是 direct evidence，要明确标注。

---

## 实际含义

### 当你更新 wiki page 时

先检查：

- raw sources
- node metadata
- node README

再改 synthesis。

### 当你新增一个关系时

把关系写进 `meta.yaml`，不要只写在 prose 里。

### 当你记录个人判断时

如果没有验证，不要把它写成 source-backed fact。

### 当你让 LLM 更新内容时

LLM 也应遵守这套 source-of-truth hierarchy。

---

## 总结

这个仓库是刻意分层的。

- truth 不等于 summary
- structure 不等于 explanation
- explanation 不等于 synthesis
- synthesis 不等于 dashboard

保持这些层的区分，是这个系统能够长期扩展的重要前提。
