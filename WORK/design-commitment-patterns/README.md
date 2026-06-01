# Design Commitment Patterns

设计承诺 pattern 层。这里放的是**可复用的预沉淀不变量**：当你准备做某个架构选择时，先打开对应 pattern，判断这个项目是否应该把它实例化成项目内 `DC-XXX`。

它接在 runbook 后面、项目 commitment 前面：

```text
KNOWLEDGE 节点（为什么）
  → runbook 症状簇（坏了怎么查）
  → design commitment pattern（设计前有哪些候选不变量）
  → PROJECTS/<project>/design/commitments.md（本项目真的承诺什么）
```

## 和其它层的区别

| 层 | key | 触发时刻 | 放什么 |
|---|---|---|---|
| KNOWLEDGE | 概念 / 机制 | 学习和重学 | 因果叙述、反事实、Open Questions |
| runbook | 症状 | debug / 面试自测 | 当前动作、适用边界、源 |
| design commitment pattern | 设计决策 | 开工前 / 架构草图前 | 可复用不变量、代价、范围、实例化校验 |
| project design commitment | 项目承诺 | 项目采纳后 | 本项目 `DC-XXX`、强度、状态、可执行校验 |

## 何时建

只在下列情况建：

- 多条 runbook 条目的某个方案共享同一条结构性不变量，且该不变量让症状 / 有害后果不可能发生。
- 某条 runbook 中的前瞻预防内容已经能写出可检查的不变量、代价、范围、实例化校验。
- 用户明确要求把某簇 runbook 压成设计前可调用的候选不变量。

不要把运行时恢复流程、诊断 procedure、节点 thesis 写进这里。它们分别留在 runbook 和 KNOWLEDGE。

## 文件组织

```text
WORK/design-commitment-patterns/
├── README.md
└── <domain>/
    └── <decision-or-invariant-slug>.md
```

slug 用设计决策或不变量命名，不用症状命名。

例：

- `agent/respond-single-output-channel.md`：决定让小模型多步工具 agent 只走工具输出通道。

## 写作规则

模板：[`META/templates/design_commitment_pattern.template.md`](../../META/templates/design_commitment_pattern.template.md)。

- pattern 不是项目承诺，不写 `DC-XXX`，不写 `active`。
- 必须写"留在 runbook 的部分"，防止把恢复流程误升格。
- 必须写"实例化成项目 DC 时要补的校验"，否则设计时无法交给 coding agent 执行。
- 源必须指向 KNOWLEDGE 节点和被压缩的 runbook 簇。

## 引用方向

- pattern → KNOWLEDGE / runbook：允许。
- PROJECTS / 项目仓库 → pattern：允许，表示项目参考或采纳后实例化。
- KNOWLEDGE → pattern：禁止，稳定知识层不依赖 WORK。
