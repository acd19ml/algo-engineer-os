# Design Commitment Pattern Template

`WORK/design-commitment-patterns/<domain>/<slug>.md` 的条目形态。

design commitment pattern 是**项目承诺的预沉淀层**：它从 runbook 症状簇里抽出可复用的结构性不变量，让你在开工前能按设计决策调用；但它还不是某个项目的 `DC-XXX`，不能被运行中的系统直接违反。

真实项目采纳时，再从 pattern 实例化到项目仓库或 `PROJECTS/<project>/design/commitments.md`，按 `META/templates/design_commitment.template.md` 写成可违反、可校验的承诺。

---

## 升级判据

只有结构性不变量能进入 pattern：

- **可以进入**：让一簇症状，或它们的有害后果，从设计上不可能发生的约束。
- **不能进入**：运行时恢复流程、诊断 procedure、节点 thesis、纯经验口诀。

同一条 runbook 里如果既有过程又有不变量，只抽不变量；过程继续留在 runbook。

---

## 字段

```markdown
# <Pattern 名称>

`status: candidate | stable | stale`   `instantiates-to: project-design-commitment`

## 何时打开

当你做什么设计决策时打开；不适合什么场景。

## 结构性不变量

一句话写清这个 pattern 的不变量。用"系统必须 / 不得"表达，但不要伪装成某个项目已经采纳。

## 它预防的症状簇

- P-XXX：症状一句话 → 不变量如何让它 / 它的有害后果不发生
- P-YYY：...

## 留在 runbook 的部分

哪些相关方案只是恢复 / 诊断过程，不进入 pattern。

## 代价 / 范围

- 代价：关掉了什么、多了什么成本
- 适用：什么前提下值得
- 失效：什么场景下会过度工程或与其它 pattern 冲突

## 实例化成项目 DC 时要补的校验

- 架构 / 静态检查
- eval / CI / lint
- 暂不能自动化时的人工 review TODO

## 前沿问题

什么一旦被解决，会让这个 pattern 降级、退役或改写。

## 源

`[[node-name]]` + P-XXX..P-YYY。
验证状态：未验证 / 部分验证 / 已验证。

## 演进日志

- `YYYY-MM`：从哪簇症状抽出 / 因什么项目验证升级 / 因什么前沿进展降级
```

---

## 写作要点

- pattern 是**设计前调用卡片**，key 是设计决策，不是症状。
- 不复述 KNOWLEDGE 的因果机制；只写不变量、代价、范围、实例化校验。
- 不写项目事实；项目事实属于 `PROJECTS/<project>/design/commitments.md`。
- 如果"校验"完全写不出来，它还不是 design commitment pattern，先回 runbook / KNOWLEDGE。
