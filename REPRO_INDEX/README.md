# REPRO_INDEX

外部代码 / 实验 repo 的索引层。

## 这层是什么

主仓库不存所有代码。代码住在外部 repos，这里只维护它们的索引：连到哪个节点、什么类型、什么状态、怎么跑。

## 当前状态

空。等你有真实的外部 repo（toy 实现、论文复现、实验代码）再建条目。

## 触发条件

- 你做了一个 toy 实现 → 在这里登记
- 你 fork 了某 repo 做了改动 → 登记
- 复现了某篇论文 → 登记

LLM 在 triage 时如果检测到 INBOX 内容里出现了 GitHub URL / 实验代码相关讨论，会建议在这里加条目。

## 推荐字段（建条目时）

```yaml
- name: <repo-name>
  url: https://github.com/...
  type: toy-implementation | paper-reproduction | benchmark | analysis | sandbox
  status: planned | toy | partial | reproduced | validated | stale | archived
  linked_nodes: [...]
  linked_projects: [...]
  purpose: <一句话>
  environment: <语言/框架>
  last_checked: YYYY-MM-DD
```

## 引用方向

KNOWLEDGE / PROJECTS 可以引用这里。这里不向上引用。
