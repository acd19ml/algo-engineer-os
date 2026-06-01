# 决策脚印：D5 短语检测硬化 · 从 sweep 到 playbook

> 记录从「发现 sweep 结果，想做 D5 硬化」到「产出可复用 playbook」的完整决策链条。
> 不重复 harness-kb-alignment.md 的结果分析；本文聚焦决策过程——初始计划踩了什么坑、哪些 KNOWLEDGE 节点纠正了方向、最终计划长什么样。

## 触发点

2026-06-02 sweep（Qwen2.5 四档 + T1 留出集）产出结果：

- 14B/32B/72B：98/100 main、7/7 heldout_t1
- critical_bypass = 0 跨全档
- 但多个检测层仍是纯关键词：investment（18 词）、handoff（10 词）、chain ambiguity 辅助信号

此时面临选择：关键词检测在 100 条上是够用的，但不知道它对**没见过的措辞**是否也够用。两个方向：

- A：直接硬化（加 LLM overlay 或扩展关键词），跑完再看效果
- B：先建 heldout 验证关键词，挂了再硬化

## 初始计划（v1 · 被 KNOWLEDGE 纠正）

最初提出了 3 步计划：

1. Investment LLM 语义 overlay：关键词触发后调用 LLM 做 yes/no 验证
2. Handoff heldout 验证（不改代码）
3. Heldout 合并 + 全 sweep

**两个坑**：

### 坑 1：在关键词失效证据出现之前就建 LLM overlay

当前 investment 检测在 100 条上 critical_bypass = 0——**没有 bypass 证据**。此时建 LLM overlay 等于为没发生的错误建防御层，违反了 `[[harness]]` 的原则：

> 只在 agent 确实犯过的错误上投入 Harness——不要为想象中的错误预先建造防御层。

正确顺序应该是：先建 heldout → 跑关键词 → 关键词真挂了 → 再硬化。heldout 是用来**获取关键词是否失效的证据**的，不是用来验证 overlay 的。

### 坑 2：Investment LLM overlay 用同一个模型做路由和验证

初始设计：关键词触发 → 同一个 Qwen2.5 模型做 investment 验证。但 `[[harness-practice]]` 明确规定：

> 永远不要让 agent 自己评价自己的工作——生成和评估必须分离。

同一模型既做 intent 路由（生成）又做 investment 验证（评估），模型可能对自己刚判过的意图"再确认一遍 yes"——没有独立审查。`[[agent-permission-system]]` 的 YOLO Classifier 虽然用同一模型，但它的信息隔离是**评审者不看 agent 的文字回复**。我们的场景里 router 的 intent 输出和 investment 验证共享同一个模型实例，隔离不够。

修正：如果最终必须上 LLM overlay，验证模型必须和 router 模型隔离（不同模型或至少完全独立的 prompt 上下文）。

## 读 KNOWLEDGE 节点（4 个）

### `[[harness]]`

- 「只在 agent 确实犯过的错误上投入 Harness」→ 纠正坑 1
- 「可拆卸性」→ 硬化方案必须是可独立移除的组件

### `[[harness-practice]]`

- GAN 三 agent 的生成/评估分离 → 纠正坑 2
- 「永远不要让 agent 自己评价自己的工作」
- 「Harness 每个组件都编码了一个假设——模型自己做不好这件事」

### `[[agent-permission-system]]`

- YOLO Classifier 两阶段设计（便宜过滤 → 昂贵完整推理）→ 硬化时的架构参照
- 「评审者不看被评审者的自我辩护」→ 信息隔离的精确边界
- 「Prompt 里的规则是建议，代码里的规则是法律」→ 关键词层是代码，LLM overlay 是建议

### `[[agent-evaluation-harness]]`

- heldout 集的结构化构建原则：指标限 3-5 个、先分析再建 case、不自由发挥

## 修正后的计划（v2）

```
heldout 先行验证 → 判定是否需要硬化 → 条件硬化 → 合并全 sweep
```

| 阶段 | 做什么 | 触发条件 |
|---|---|---|
| Phase 1 | 建 heldout_investment + heldout_handoff，不改检测代码 | 总是执行 |
| Phase 1 | 当前关键词跑 heldout，看 critical_bypass | 总是执行 |
| Phase 2 | 若 bypass > 0：关键词触发 → 独立 LLM 验证（模型分离） | 仅当 Phase 1 发现 bypass |
| Phase 2 | 若 bypass > 0 且 T3：只扩展关键词，不上 LLM | 仅当 Phase 1 发现 bypass + 低风险 |
| Phase 3 | heldout 合并 + 全 sweep | Phase 1/2 完成后 |

### 和 v1 的关键区别

| | v1（被纠正） | v2（修正后） |
|---|---|---|
| 硬化时机 | 计划阶段就决定上 LLM overlay | heldout 先证明 bypass 存在才上 |
| 模型使用 | 同一模型做路由 + 验证 | 不同模型或完全独立 prompt |
| 资源投入 | 先建 overlay 再建 heldout 验证 | 先建 heldout（低成本），bypass 真存在再投 overlay |

## 从决策中提取的原则（产出 playbook）

修正过程中发现，这个「heldout 先行 → 判定 → 条件硬化」的模式不是 Neo 特有的——任何有确定性关键词检测层的 agent 系统都会遇到「关键词够不够用」的判定问题。三个反模式（关键词打地鼠、过早 LLM overlay、同一模型自审）也是通用问题。

因此把决策链条编译成了可复用 playbook：

`WORK/playbooks/detection-hardening-loop/README.md`

包含：5 步工作流 + mermaid 流程图 + 3 个反模式 + 适用/失效边界 + 5 个 KNOWLEDGE 源节点引用。

## 当前状态

- playbook 已落地，但尚未在 Neo 项目上执行
- Phase 1 待启动：建 heldout_investment 和 heldout_handoff

## 时间线

| 时间 | 事件 |
|---|---|
| 2026-06-01 | LLM router 四档跑通，发现关键词检测的过拟合风险 |
| 2026-06-02 | sweep 完成（98/100, critical_bypass=0），提出 v1 硬化计划 |
| 2026-06-02 | 读 4 个 KNOWLEDGE 节点，发现 v1 两个坑，修正为 v2 |
| 2026-06-02 | 提取原则 → 落地 `WORK/playbooks/detection-hardening-loop/` |
| 待定 | 按 playbook 步骤 2 建 heldout 集 |
