# AWM Mechanism Audit on Mind2Web

> CityU Guided Study Final Report：对 AWM (Agent Workflow Memory, Wang et al. 2024) 做 Mind2Web 复现 + 机制审计 + 失败模式诊断。**不是简单重跑，而是复现加解释**。

## 类型

`research`

## 目标

回答两个研究问题：

1. AWM 在 Mind2Web 上的 paper claim 哪些 hold up、哪些 break down？
2. 当 AWM 帮 / 害的时候，是通过什么机制？是 broad guidance 还是 narrow intervention？

## 动机

Interim report 阶段最初问的是宽泛的 "memory for GUI/web agents" 问题。综述完后把问题收窄到 **procedural memory**：不只是"存历史"，而是"存可复用的 task workflow"。AWM 是这个问题上最清晰的代表方法，因此作为 focal case。

## 范围

### 包含

- **忠实复现**：Mind2Web 上的主 claim（offline gains / online behavior under distribution shift / LM workflows 比 rule workflows 更抽象）
- **机制审计**：超越 aggregate score，做 step-level 配对分析（baseline vs workflow 同任务同站点同 step）
- **失败模式 + 边界条件**：什么时候 AWM 帮、什么时候害、为什么害
- **workflow text 对比**：LM-induced vs rule-induced 的长度、参数化程度、可执行性
- **Final presentation**（speaker notes + slide deck）：13 slides + 18 道 Q&A 准备

### 不包含

- ❌ AWM 框架的实现层改动（只复现 + 诊断，不改源码）
- ❌ 跨 model 泛化测试（受 setting 限制，下一步）
- ❌ Failure-driven revision loop 的实现（只识别 gap，未补）

## 关键发现

### Finding 1 — AWM 不是 uniform effective，而是 condition-dependent

正向 site（kayak / newegg）：workflow 产生 **0 negative interventions**。

负向 site：
- budget：negative 12 / positive 6（**反向**）
- sixflags：negative 6 / positive 3（**反向**）

**Influence window 只有 6-18% step**。AWM 不是通过 broad guidance 影响整段 trajectory，而是通过少数 **decisive interventions** 决定 aggregate outcome。

### Finding 2 — Abstraction is real, but does not guarantee better execution

| 维度 | LM workflows | Rule workflows |
|---|---|---|
| 步数 | 1.7-2.7 步 | 7.8-12.5 步 |
| 具体值 | 已参数化、无具体值 | 大量具体值 |

但 performance：united 上 LM 明显占优；newegg 上 rule 反而 competitive（因为 task pattern 固定，具体值依然可迁移）。**抽象是真实的，但抽象 ≠ 更鲁棒的执行**。

### Finding 3 — Help looks like action-mode redirection

united 案例：baseline click 错误的 package-type control；workflow 条件 `TYPE [10892] [las vegas]` 正确填入。**workflow 的价值不是"加文本"，而是"把动作类型导正"**（点击 → 输入）。

### Finding 4 — Harm looks like workflow-family mismatch

sixflags "申请工作"案例：注入的 workflow 是"选公园"。baseline 正确 click `Jobs`；workflow 条件错误 click `Browse the Parks Below`。**这不是随机错误，是 stored workflow 来自错误任务族，但 procedural bias 强到足以 redirect 第一步行动**。

## 研究判断（CV / 面试用）

AWM 是 procedural memory 的 **partial, condition-dependent** mechanism。

它在三个条件同时满足时才帮：
1. workflow family 具备可复用性
2. retrieved procedure 与当前 task 匹配
3. baseline 仍有改进空间

**缺失的是 failure-driven revision loop**。系统没有稳健机制：detect harmful workflows / revise after failure / suppress when match weak。

## 下一步思考（Discussion，未写进 report 主体）

研究问题应该从"AWM 哪个模块需要改"上抬一层：**procedural memory object 应该长什么样**？

把 Skill / AWM / Gene 视作 experience-object 空间中的不同 design points，而非线性进化：
- Skill：external procedural object，但仍偏 human-readable + prose-heavy
- AWM：context-conditioned workflow templates with action slots；比 plain summary 更 executable，但 selection / boundary / revision 仍弱
- Gene：更 compact 的 runtime control object，trigger / strategy / avoid constraints / validation 显式

实验方向：构建轻量级 **diagnosis structure simulation**（隐藏拓扑 + tool-based queries + 同症状不同根因 + 轻微 environment drift），测试 external procedural memory 是否能降低 repeated search cost 并在 environment drift 下支持 selective reuse。

## 方法学产出（可迁移）

- **Paired-case 评测方法**：同任务同站点 baseline vs workflow 对照，step-level diff
- **Influence window 度量**：实际改变行为的 step 占比（6-18% 是诊断信号）
- **Workflow text comparison**：长度 / 参数化程度 / 具体值数量
- **Positive / Negative intervention 分类**：strategy redirection / domain misdirection / step skipping / workflow-family mismatch

## 简历素材

> 主流 Web Agent Memory 框架的复现与审计（AWM @ Mind2Web）：在 step-level 配对实验下做 baseline vs workflow 同步对照，发现 workflow 实际影响窗口仅 6-18% 且正向 / 负向站点的干预模式反向；归类 workflow 干预的正负机制（strategy redirection / domain misdirection / step skipping 等），并定位"抽象不等于更好执行"边界，输出可复用的 paired-case 评测方法学。

## 相关知识 / 问题

- KNOWLEDGE：可由本项目派生 / 关联的节点
  - `KNOWLEDGE/agent/agent-memory-system/` — 通用 agent memory 设计
  - 候选新节点：`procedural-memory-object-shape`（Skill / AWM / Gene 横向对比，需 PROBLEMS 触发后再判）
- PROBLEMS：候选 `PROBLEMS/procedural-memory-object-design/`（Skill vs AWM vs Gene 横向对比框架页）

## 当前状态

`done`（Final Report + Presentation 已交付）

## 面试故事入口

- "你做过什么 agent memory 方面的研究？" → 用 4 个 finding + 研究判断 + 下一步方向回答
- "AWM 是好的 memory 方案吗？" → partial, condition-dependent 三个条件
- "你的复现和 paper 结果有差异时怎么处理？" → 不是 throw away，而是定位为 *mechanism stronger than performance narrative*

## 关键提交件

原始交付件保存在 `RAW_SOURCES/research-deliverables/awm-mechanism-audit/`：

- `final-report.tex`（2186 行）—— 完整论文写作
- `appendix-content.tex` —— audit trail
- `reference.bib`
- `speaker-note.md` —— 13 slides + 18 道 Q&A（汇报现场用）
