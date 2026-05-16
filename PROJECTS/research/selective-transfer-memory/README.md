# Selective Transfer in Memory-Augmented LLM Agents

> 团队课程项目（4 人）。固定经验预算下做 matched / mismatched 配对设计，测试"记忆是否帮助 structure-matched target，且不伤害 structure-mismatched target"。Near-transfer pilot：HotpotQA → 2WikiMultiHopQA。

## 类型

`research`

## 目标

回答一个比"记忆平均上有没有帮助"更严格的问题：**在固定经验预算下，记忆能否帮助结构匹配的目标任务，同时不伤害结构不匹配的任务？**

## 动机

只看 average benchmark gain 不足以判断 memory 是否真起作用。两个干扰：

1. 更多上下文本身可能提升表现 —— 不等于 memory 起作用
2. 粗粒度相关性标签可能误判 —— 大类别"相关"的源任务在算子层可能 mismatched

因此需要 paired controlled comparison，让 *match path 提升、mismatch control 不变* 成为唯一可信号。

## 团队 & 我的贡献

| 成员 | 主要分工 |
|---|---|
| Li Mengxiao（我） | 研究框架 + pilot 实验设置 |
| Cheng Zhaoyang | workflow + observability 框架设计 |
| Jiang Yuchen | 诊断分析 + 匹配修复 |
| Ye Hengrui | 算子抽象 + 选择性分析 + 最终总结 |

## 实验设置

- **任务**：HotpotQA（源，构建记忆材料） → 2WikiMultiHopQA（目标，被回答）
- **模型**：Qwen3.5-9B，本地部署，**greedy decoding**（减少 sampling 噪声）
- **预算固定**：每个条件都获得相同 5 个已解决源任务作为经验
- **三种记忆条件**：
  - None（仅 context + question）
  - Episodic（5 个源任务轨迹分别提供）
  - Consolidated（5 个源任务压缩成一个抽象经验）
- **匹配 / 不匹配并列报告**：差异可解释为记忆形式或结构匹配带来的影响，不被模型能力或数据预算混淆

## 共享 Prompt 框架（关键设计）

所有条件下模型看到的部分相同：`Context / Question / Past Experience / Instructions / Reasoning / Final Answer`。让：

- 输出可解析、可评分
- 模型如何使用记忆变得可观察（明确使用 / 拒绝 / 忽略）
- 结果差异能归因到记忆形式 vs 结构匹配，而非格式或工具性因素

## 指标分两类

| 类别 | 指标 |
|---|---|
| 结果指标 | Exact Match、token-level F1、matched / mismatched 对照 |
| 过程指标 | 推理过程是否可见 / 最终答案是否可解析 / 过去经验被明确使用、拒绝或忽略 |

## 核心诊断案例：wiki_dev_2639

**问题**：Harriet Pelham-Holles, Duchess of Newcastle-upon-Tyne 的 sibling-in-law 是谁？  
**Gold**：Henry Pelham  
**关系路径**：wife → husband → brother

最初 pilot 结果：

- No-memory baseline：**正确**
- 两个 "relevant memory" 条件（episodic / consolidation）：**都失败**

表面看像"记忆造成负迁移"。但**真正原因**：目标是 *relation-chain bridge* 案例，源记忆只按粗粒度 bridge 标签被标 relevant。源任务大类别相关，但没保留目标所需的算子结构。

**结论**：原来的 matched 标签比想象中更弱。看起来像 negative transfer 的结果，可能来自 *目标推理路径 ↔ 源任务匹配粒度* 的不一致。

## 修复 1：匹配粒度（Source Rerouting）

只改变 matched source set，其它一切固定（目标问题、模型、prompt 框架、评分、mismatched control）。

- Before：matched source 来自 attribute-bridge 集合
- After：matched source 来自 relation-chain 集合（同亲属关系算子模式）

**量化结果**：matched episodic 从 **0 → 1**，mismatched control **仍为 0**。

结论不止是"记忆有帮助"，更强是：**匹配粒度本身就是结果的一部分**。粗粒度 bridge 标签对此案例太宽泛；只有源任务保留正确算子模式，episodic 路径才恢复。

## 修复 2：可执行算子抽象（Operator Repair）

修复 1 后 matched episodic 恢复，但 matched consolidation 仍错。

原因：之前的抽象 *偏描述性*——提到怎样思考 spouse branches，但没以模型可执行的 ordered operator path 形式保留算子结构。

修改 Past Experience block 中的 heuristic：把 sibling-in-law **规范化为 ordered operator path**——`spouse-of → sibling`，或 `sibling → spouse-of`。

**量化结果**：matched consolidation 从 **0 → 1**，mismatched control **仍为 0**。

结论：**抽象本身不够；抽象必须以可执行形式保留算子结构**。

## 选择性信号汇总

| 设置 | matched episodic | matched consolidation | mismatched control |
|---|---|---|---|
| 粗粒度 matching（初始） | 0 | 0 | 0 |
| + 修复 1（Source Rerouting） | **1** | 0 | 0 |
| + 修复 2（Operator Repair） | **1** | **1** | 0 |

**Pattern**：matched 路径提升，mismatched 控制组始终保持 0。这是 selective transfer 的受控特征，可与 general context 效应区分。

## 关键结论（三句话）

1. 只有当 matched / mismatched 共享相同预算 + 相同 prompt 框架时，selective transfer 才可见
2. **匹配粒度很重要**：粗粒度相关标签可能掩盖目标案例真正的推理结构
3. **整合记忆必须保留可执行的算子结构**，尤其在 relation-chain 推理路径中

## 局限

- 最强修复证据集中在一个 anchor diagnostic case（wiki_dev_2639）
- 所有实验仅一个 Qwen3.5-9B 配置
- 定位为 **诊断性 pilot**，不是最终 benchmark 结论

## 下一步

- 在更多 relation-chain targets 上做修复后扩展评估
- 测试是否能跨模型成立
- 探索 *applicability judgment + memory-form design* 联合学习

## 方法学产出（可迁移）

- **Matched / mismatched paired evaluation design**（防止 general context 效应混淆 selective transfer 信号）
- **共享 prompt 框架**（结果差异可归因到记忆形式 vs 结构匹配）
- **结果 + 过程双指标**（不只问"答对没"，问"记忆是不是被正确使用"）
- **anchor diagnostic case + 受控修复链**（暴露 → 重路由 → 算子抽象 → 重验证）

## 简历素材

> 记忆跨任务复用机制实验（HotpotQA → 2WikiMultiHopQA 近迁移）：在固定经验预算 + 共享 prompt 框架下以 matched / mismatched 配对设计测试三种记忆形态（None / Episodic / Consolidated），通过受控前后对比验证仅匹配路径在两次修复（源任务重路由 + 算子可执行化）后恢复、不匹配控制组始终保持不变，定位"记忆抽象的可执行性"如何决定跨任务复用边界。

## 相关知识 / 问题

- KNOWLEDGE：`KNOWLEDGE/agent/agent-memory-system/`（通用 memory 系统）
- 候选关联：episodic vs consolidation memory 形态对比（暂未单独建节点；可在 PROBLEMS 触发）

## 当前状态

`done`（Final Presentation + Report 已交付）

## 面试故事入口

- "你们和 baseline 比怎么 design 实验？" → matched / mismatched 配对 + 共享 prompt 框架
- "你怎么知道修复 1 真的造成了提升而不是巧合？" → 只改 matched source set，其它五项变量固定，前后对照
- "为什么 anchor case 够支撑结论？" → 不声称大规模 benchmark 提升，声称"暴露了一个 evaluation 问题 + 两次受控修复 + matched 恢复 / mismatched 不变"
- "和 AWM 那个项目什么关系？" → 这是 small memory-transfer pilot，发现"主题相关但缺执行结构"会失效，启发了 AWM 项目对 procedural memory object shape 的进一步思考

## 关键提交件

原始交付件保存在 `RAW_SOURCES/research-deliverables/selective-transfer-memory/`：

- `final-report.tex`（331 行）
- `appendix.tex`
- `speaker-note.md` —— 10 分钟英文汇报中文版 + 18 题 Q&A 准备
