# Docs Layer

本目录是真值层和工程设计层，不放 eval runner 代码或面试稿。

| 子目录 | 职责 |
|---|---|
| `product/` | 产品 source of truth：用户、问题、范围、非目标、上线阶段。 |
| `decision/` | 方向取舍：为什么做、为什么不是 FAQ / 泛 RAG / 开放 ReAct。 |
| `architecture/` | 系统结构：组件、数据流、模块边界、部署视图。 |
| `implementation/` | 落地契约：schema、policy、tool contract、API、build plan。 |
| `operations/` | source governance：registry owner、SLA、provider policy、bridge 边界。 |
| `design/` | 不变量：项目采纳的 design commitments。 |

未来新增规则：如果文档产生项目事实或工程约束，放这里；如果只是评测、结果或面试表达，不放这里。
