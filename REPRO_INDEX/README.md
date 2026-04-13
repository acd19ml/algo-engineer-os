# REPRO_INDEX

`REPRO_INDEX/` 是这个仓库的执行索引层（execution index layer）。

如果 `KNOWLEDGE/` 解释一个主题是什么，`WIKI/` 帮你更快理解它，  
那么 `REPRO_INDEX/` 负责回答：

- 真正的实现在哪里
- 哪个 repo 在验证这个想法
- 哪些内容已经被复现
- 哪些还停留在概念层
- 运行这些实现需要什么环境与上下文

这一层存在的原因很简单：  
真正的算法工程理解，不能停留在笔记与总结页。

---

## 这一层是做什么的

`REPRO_INDEX/` 是与本仓库相关的外部代码与实验资产注册表。

这个仓库不需要把所有代码都存进来。  
代码可以存在外部 repos，而这里负责维护它们的索引、状态、用途与连接关系。

它主要记录：

- repo 是什么
- 它对应哪个 topic 或 project
- 它属于哪类实现
- 当前状态如何
- 应该如何运行、理解、复用

这样做的好处是：

- 主仓库保持聚焦和轻量
- 理论与执行资产之间仍然保持强连接

---

## 为什么这一层重要

一个没有代码索引的知识系统会越来越抽象。  
一个没有知识链接的代码集合会越来越碎片化。

`REPRO_INDEX/` 的作用，就是把这两者重新接起来。

它帮助你连接：

- concept ↔ implementation
- method ↔ reproduction
- project ↔ repo
- learning ↔ validation
- work knowledge ↔ reusable engineering assets

---

## 什么内容主要属于这里

当一个对象主要是在描述 **external code / experiment registry** 时，它通常属于 `REPRO_INDEX/`。

Examples:

- external reproduction repo index
- toy implementation catalog
- experiment status tracker
- environment notes
- runbook for specific repos
- validation notes tied to implementation

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- 概念解释与机制说明 -> `KNOWLEDGE/`
- 问题定义与方法比较 -> `PROBLEMS/`
- 编译型总览页 -> `WIKI/`
- 项目计划与执行记录 -> `PROJECTS/`
- 日常工作 SOP -> `WORK/`

`REPRO_INDEX/` 关心的不是“把代码解释清楚本身”，  
而是“让代码资产可发现、可追踪、可连接”。

---

## 常见内容形态

### `external-repos.md`

外部 repo 总索引。

它应帮助回答：

- 有哪些 repo
- 它们各自是做什么的
- 分别连到哪些 nodes 或 projects
- 类型和状态是什么

---

### `reproduction-status.md`

按状态组织的视图。

它应帮助回答：

- 哪些主题已经有代码
- 哪些只有 toy code
- 哪些已有 partial reproduction
- 哪些仍缺实现或验证

这类页面很适合长期追踪。

---

### `experiment-catalog.md`

更偏 experiment-centered 的视图。

它应帮助回答：

- 做过哪些实验
- 它们分别在哪个 repo
- 它们想回答什么问题

---

### `environments.md`

与外部 repo 相关的环境与工具说明。

它应帮助回答：

- 使用什么 language / framework
- 需要什么环境
- 常见 setup 问题是什么
- 哪些 repo 当前可运行

当外部 repos 积累变多后，这部分会非常有价值。

---

## 外部 repo 的常见类型

一个 repo 可以属于以下类型之一：

- `toy-implementation`
- `paper-reproduction`
- `analysis`
- `visualization`
- `benchmark`
- `project-code`
- `work-asset`
- `sandbox`

这些类型的价值在于：  
区分“用于快速理解的小 repo”和“真正承载项目或验证的工程资产”。

---

## 外部 repo 条目的推荐元数据

每个 external repo entry 建议至少包含：

- repo name
- URL
- linked node(s)
- linked project(s)
- type
- status
- purpose
- environment
- last checked date

例如：

```yaml
- repo: toy-interleaved-mrope
  url: https://github.com/yourname/toy-interleaved-mrope
  linked_nodes:
    - interleaved-mrope
  type: toy-implementation
  status: planned
  purpose: understand the core position transformation logic
  environment: python / pytorch
  last_checked: 2026-04-14
```

---

## 这一层应该帮助你看见什么

一个好的 `REPRO_INDEX/` 应该让你快速回答：

- 这个主题我到底有没有真正的代码资产
- 这个主题只是概念理解，还是已经做过实现或验证
- 哪些 repos 值得重看
- 哪些 repos 已经过时
- 哪些 experiments 支撑了哪些 claim
- 当前学习或项目链路里还缺什么执行资产

---

## 设计原则

### 1. Keep the main repo lightweight

不要强迫所有代码都放在这里。

### 2. Keep code discoverable

所有重要 external repos 都应能从相关 node 或 project 被找到。

### 3. Track implementation maturity

建议明确区分：

- `planned`
- `toy`
- `partial`
- `reproduced`
- `validated`
- `stale`
- `archived`

### 4. Link code back to knowledge

没有上下文的 repo 链接，价值会大幅下降。

### 5. Prefer explanation over mere linking

只有链接不够。  
要说明它存在的目的与状态。

---

## 这一层如何与其它层协作

### With `KNOWLEDGE/`

knowledge nodes 应链接到相关 external repos，尤其是 `code/README.md`。

### With `PROJECTS/`

projects 往往依赖多个 repos，应在这里形成聚合索引。

### With `WORK/`

部分 work assets、脚本或分析仓库也可能需要在这里被索引。

### With `WIKI/`

wiki page 在讨论验证、工程 trade-off、实现路径时，可以引用这里的 repos。

### With `THINKING/`

open questions 往往会触发新的 external experiments。

---

## 推荐维护流程

### 当你创建一个新的 external repo 时

1. 把它加入 `external-repos.md`
2. 从相关 node 的 `code/README.md` 回链过去
3. 如果它支撑某个 project，也从项目页链接它
4. 更新 `reproduction-status.md`

### 当你显著更新一个 repo 时

1. 重新确认它的 purpose 和 status
2. 需要时更新 environment notes
3. 标注它是否改变了你对相关 topic 的 confidence

### 当一个 repo 逐渐失效时

不要立刻删除。  
优先把它标为：

- `stale`
- `archived`
- `superseded`

这样可以保留项目记忆与演化路径。

---

## 当前阶段的重点

`REPRO_INDEX/` 的第一阶段建议优先：

- registering all external experiment repos
- linking repos back to knowledge nodes
- tracking implementation status
- recording minimal environment notes
- making theory-to-code transitions explicit

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [WIKI](/Users/mac/studyspace/algo-engineer-os/WIKI/README.md)
