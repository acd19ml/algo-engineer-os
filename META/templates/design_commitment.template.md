# Design Commitment Template

一条**设计承诺**的形态。设计承诺 = "为了让一簇症状或它的有害后果不发生，**这个系统**从 day-1 起必须满足的约束"。

实例住在项目仓库或 `PROJECTS/<project>/design/commitments.md`，**不在 KNOWLEDGE，也不作为 WORK 的项目承诺实例**。WORK 里可以有 `design-commitment-patterns/` 作为预沉淀候选；本模板描述的是项目采纳后的真实 `DC-XXX`。它的执行机制（校验）绑在代码和项目边界上，代码在项目里，承诺随项目生死。

> 形态参考底部 few-shot。光看抽象规则写出来的会形似神不似。

---

## 这一层为什么和别的层不同

- **它是唯一能被运行中的系统"违反"的 artifact。** 节点 / runbook 不会被违反，承诺会。判据：一条承诺是真的，当且仅当系统能被"抓到违反它"。抓不到违反的承诺 = 一个愿望。
- **所以最承重的字段是 `校验`，最强形态是可执行的。** 优先写 CI 门禁 / architecture fitness function / 会 fail 的 eval case。暂时不能自动化，也要写明"人工 review + TODO 转 check"。
- **它是一个选择，所以有代价和范围。** 只记好处不记代价的承诺，会被原样抄进下一个代价不可接受的项目。

---

## 实例化判据

项目 design commitment 通常从 `WORK/design-commitment-patterns/*` 实例化而来。写入前先确认：

1. **项目确实采纳**：用户确认这个项目要用这条 pattern，而不是只把它当参考。
2. **能抓到违反**：本项目能写出架构检查、eval、CI、lint 或明确的人工 review TODO。
3. **代价在本项目可接受**：pattern 的范围条件在当前项目成立；冲突 pattern 已被裁决。

如果还停留在"这条以后可能有用"，不要写进项目 DC；先留在 `WORK/design-commitment-patterns/`。

---

## 字段

```markdown
## DC-XXX：<一句话祈使式承诺>

`strength: inviolable | default`

**承诺**
系统 MUST / MUST NOT 的那条约束，写成可证伪的系统不变量，精确到能写校验。

**来源簇**
为溶掉哪簇症状而采纳：`P-aaa` · `P-bbb` · `P-ccc`。
此栏为空 = 这条承诺是 import 的 fashion，不是你从自己的症状里挣到的。

**代价 / 范围**
- 关掉了什么 / 多了什么成本（它买到症状簇消失，也付出代价）
- 可接受的条件：在什么前提下这个代价划算；什么情况不归这条管

**校验**（最承重）
系统怎么证明它成立。优先可执行：CI 检查 / lint / fitness function / eval 用例。
暂不能自动化 → 写明人工 review 步骤 + 标 `TODO: 转 check`。

**前沿问题**
什么一旦被解决，会改写或退役这条承诺（= review 触发器 / 过期条件）。
链到某个节点的 Open Question、某篇 paper、某个 ablation。

**源（为什么这样）**
`[[node-name]]`。理解住在节点。本记录不复述机制，只记选择 / 代价 / 校验 / 前沿。

**状态 + 演进日志**
`active | relaxed | retired | superseded-by DC-YYY`
- `YYYY-MM`：采纳，因 <来源簇> / 强度改为 X，因 Y / 退役，因前沿问题 Z 已解
```

---

## 字段写作要点

| 字段 | 关键 | 反例 |
|---|---|---|
| `strength` | 从来源簇的 `severity` 继承：irreversible 簇 → `inviolable` → 阻断式校验；reversible-cheap 簇通常 → `default` | 给安全相关承诺设 `default` |
| 承诺 | 可证伪、精确到能写校验 | "应尽量保证安全"（无法校验） |
| 来源簇 | 空 = 没挣到，是 import 的 fashion | 凭"大家都说好"采纳，不链症状 |
| 代价 / 范围 | 记下关掉了什么 + 可接受条件 | 只写好处 |
| 校验 | 最强可执行；没有 = 会烂的散文 | 留空 / "靠 code review 把关"含糊带过 |
| 前沿问题 | 让承诺暂定、可演进 | 当成铁律，无退役条件 |
| 源 | 机制回链节点，本记录不重讲 why | 把节点的因果叙述抄进承诺 |

## 薄 vs 厚

承诺记录**不重讲"机制为什么有效"**，那在 `源` 节点里一份。它只记**这个项目的选择 + 代价 + 校验 + 前沿**。

薄判据：删掉所有解释"为什么这招在原理上成立"的句子后，这条承诺还能被照着实现和校验吗？能 → 合适；不能 → 你把 KNOWLEDGE 节点搬进来了。

---

## 它怎么被消费 / 怎么和别层连

- **消费视图 = design checklist**：按**设计决策**索引的视图（"决定用小模型 → 触发 DC-003 / DC-007 / DC-011"）。承诺是**单元**，checklist 是**索引**。开工时 / 交给 coding agent 当约束时，走 checklist。
- **入口（从 pattern 实例化）**：`WORK/design-commitment-patterns/*` 里的候选不变量被某个项目采纳 → 写成项目内 DC，并补齐本项目的校验、状态和演进日志。
- **出口（毕业到 KB）**：同一条承诺的模式在多个项目里反复出现 → 它的**泛化原则**结晶成一个领域级 KNOWLEDGE 节点（durable）。具体承诺仍随项目死，原则留在 KB。
- **退役**：前沿问题被解决 → 据演进日志改 `strength` 或置 `retired / superseded-by`。承诺会死，这正常。

---

## Few-shot

```markdown
## DC-001：Agent 只有一个输出通道——文本经 respond 工具走，模型永不在"文本/工具"间选择

`strength: default`

**承诺**
Agent 的输出只有一条通道：工具调用。文本回复通过合成的 `respond` 工具发出（文字进 `content` 参数）。模型不在"输出文本"和"调工具"之间做模式选择，因为这个选择不存在。

**来源簇**
P-008（模式选择，Forge 实测完成率 100% → 4%）· P-001 方案 3（同一机制的格式兜底入口）。

**代价 / 范围**
- 代价：所有文本输出包一层工具调用，可读性 / token 略增，调试多一层。
- 可接受条件：模型模式选择不稳定时（≤30B / 量化 / 模式选择完成率显著低于"格式问题"能解释的范围）。前沿模型模式选择稳定时这条是冗余开销，该项目可降为 off。

**校验**（最承重）
- 架构：agent loop 只有一个出口 = 工具分发；不存在"直接 return 文本给用户"的代码路径。静态检查定位任何绕过 `respond` 的输出点。
- eval：含"该输出最终答复"与"该调工具"混合的用例；模型走非工具通道即 fail。

**前沿问题**
模型能力到什么程度后，单通道的收益 < 它的开销？是否有"软单通道"（默认工具模式、特定情况允许直出）能兼顾？

**源（为什么这样）**
`WORK/design-commitment-patterns/agent/respond-single-output-channel.md` + `[[small-model-harness-engineering]]`（复合概率：单步误差经多步连乘指数放大；`respond` 消除"模式选择"这一独立认知任务）

**状态 + 演进日志**
`active`
- `2026-05`：采纳，因 P-008 模式选择簇。
```
