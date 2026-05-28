# Agent Memory 在运维场景的组织架构（从资深 SRE 视角）

> **派生**：基于 Socratic 讨论（`RAW_SOURCES/dialogues/conversation_01.md` + `PROBLEMS/agent-memory-architecture/` + `PROJECTS/research/awm-mechanism-audit/` + `PROJECTS/research/selective-transfer-memory/`）的核心洞察。
>
> **用途**：面试展示对 agent memory + ops 业务的理解深度。表达"我不只是会做 OpsAgent demo，我真正想清楚了 memory 在 ops 场景该长什么样"。

---

## 触发场景（面试官问以下任一时切入）

- "你做 OpsAgent 时怎么设计 memory？" / "如果重做你会怎么变？"
- "你怎么看 Agent Memory 在 ops 场景的特殊性？"
- "Procedural memory vs Declarative memory 你怎么理解？"
- "Memory 跨用户跨场景能共享吗？"
- "你为什么对 procedural memory 感兴趣？"（→ 接 [[main-project-and-research]] §C）

---

## 核心论点（30 秒电梯版）

> Agent memory 在 ops 场景**不能是单一 partition**——必须区分两个维度：
>
> 1. **Storage Partition** (memory 物理组织维度) ≠ **Retrieval Filter** (query 时筛选维度)
> 2. **Declarative memory**（service-specific facts，service-anchored）+ **Procedural memory**（cross-service diagnostic playbook，symptom-anchored）
>
> 这是从**资深 SRE 真实 mental model 反推**的，不是从理论分类正推。

---

## 第一层论证 · Storage Partition vs Retrieval Filter

### 概念区分

| 概念 | 含义 | 工程后果 |
|---|---|---|
| **Storage partition** | memory 物理按维度分桶 | 跨桶不能复用；决定 **share boundary** |
| **Retrieval filter** | memory 物理不分桶，query 时按维度筛 | 决定 **query latency + 召回精度** |

**两件事的工程含义完全不同**。partition 决定"什么时候可以跨域 share"，filter 决定"怎么在桶内快速 narrow"。

### Storage Partition 应该是 service（不是故障类型）

**4 个理由**：

1. **Service 是稳定边界**——ownership / oncall / postmortem 都按 service 组织；故障类型边界模糊（一个"性能问题"可能是 DB / GC / 网络 / 上游）
2. **Service 是真实的"故障域"**——一个 service 跨集群跨版本，但其根本 architecture / dependencies / 已知 quirks 是 service-level 的，**这才是真正的"同域可复用、跨域强制隔离"**
3. **Long-tail 在 service 内足够密**——核心 service 一年 50-200 个事件可形成统计；跨 service 的故障类型分布稀疏且不可比
4. **匹配 SRE 工作流**——postmortem 库 / runbook / on-call rotation 全部 service-anchored

### Retrieval Filter 是多维并行

| 维度 | 用途 | 触发顺序 |
|---|---|---|
| **change correlation** | recent deploy / config change | **通常第一**（生产事故 60-80% trace to recent change）|
| **symptom pattern** | "P99 飙但无 error" 类 pattern | narrow 候选根因 |
| **time-of-day pattern** | 业务时段 | narrow 业务 context |
| **infra signature** | cluster / region quirks | narrow infra-specific 问题 |
| **service history** | service 历史 issue | retrieve 已知问题 |

**"故障类型"属于 symptom pattern 这一维**，是 retrieval filter，**不是 storage partition**。

---

## 第二层论证 · Procedural vs Declarative 在 SRE 脑子里自然分离

资深 SRE 的"memory"其实是**两套不同的东西并存**：

| 类型 | 存什么 | 组织维度 | 例子 |
|---|---|---|---|
| **Declarative**（service-specific facts）| service 的 quirks / 已知 issue / dependencies | **service-anchored** | "payment-api v2.x 在 50k qps 时 GC 飙高" |
| **Procedural**（投入查 playbook）| 遇到某 pattern 该怎么投入查 | **symptom-pattern-anchored** | "P99 飙 + 无 error → 先查 saturation → GC → 上游" |

**关键判断**：这两套必须 **分开存储 + 分开更新**——

- Declarative 跨 service 不可复用（payment-api 的 quirk 跟 order-api 无关）
- Procedural 跨 service 可复用（"P99 飙但无 error 先查 saturation" 在所有 service 上适用）
- Declarative 的更新触发是 **service 自身变更**（new version / new dependency）
- Procedural 的更新触发是 **诊断 strategy 改进**（一个 playbook 在多个 service 上反复用、积累 success rate）

---

## 为什么"按故障类型划分"这个常见直觉**一半对一半错**

直觉本身很自然，但**当作 storage partition 用就崩了**：

| 维度 | 直觉对 | 直觉错 |
|---|---|---|
| 作为 **procedural memory 的 anchor** | ✅ 对——cross-service playbook 确实按 symptom / failure type 组织（这就是 Hermes Skills / AWM workflow / Runbook 的形态）| —— |
| 作为 **declarative memory 的 storage partition** | —— | ❌ 错——跨 service 的"性能问题"经验复用率极低，因为每个 service 的性能特征都 service-specific |

**"故障类型"是 procedural memory 的合理组织维度，不是 declarative memory 的合理组织维度。** 把两层混在一起谈"按故障类型划分 memory"必然出错。

---

## 工程含义 · 两层架构

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Service-anchored Declarative Store             │
│   - payment-api/  → facts, quirks, known-issues, history│
│   - order-api/    → facts, quirks, known-issues, history│
│   - ...                                                 │
│   Storage partition: service                            │
│   Cross-service: 强制隔离                               │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Symptom-anchored Procedural Playbook           │
│   - "P99 spike no error" → diagnostic sequence          │
│   - "Error rate jump"    → diagnostic sequence          │
│   - "Memory leak"        → diagnostic sequence          │
│   - ...                                                 │
│   Storage partition: symptom pattern / failure type     │
│   Cross-service: 可复用                                 │
└─────────────────────────────────────────────────────────┘
       ↑
  Retrieval (多维并行)
       ↑
  change / symptom / time / infra / service-history
```

**两层独立**：
- L1 由 service owner 维护；写入触发是 service 变更 / postmortem
- L2 由 SRE 团队维护；写入触发是新 playbook 验证有效

**两层协作**：诊断时 L2 先 narrow"该查什么"（cross-service knowledge），L1 提供"这个具体 service 的特殊情况"（service-specific knowledge）。

---

## Interview Soundbite（金句版）

> "我在做 OpsAgent 时一开始的直觉是按故障类型划分 memory，后来反推资深 SRE 的真实 mental model 发现这是错的——但是错得有结构。
>
> Senior SRE 的 memory 是 **service-anchored**（storage partition），故障类型其实是**检索维度**（retrieval filter）。这两件事的工程含义完全不同：partition 决定 share boundary（跨 service 不直接共享），filter 决定 query 精度（service 内多维并行索引）。
>
> 更深一层：SRE 脑子里其实有**两套 memory** 并存——**declarative memory** 是 service-specific facts（service-anchored、跨 service 强制隔离），**procedural memory** 是 cross-service diagnostic playbook（symptom-anchored、跨 service 可复用）。故障类型直觉之所以诱人，是它对应 procedural 那一层；之所以错，是它当作了 declarative 的组织维度。
>
> 工程上这意味着 memory system 不应该是单一 partition，而是**两层结构：service-anchored declarative store + symptom-anchored procedural playbook**。这跟 Hermes Skills 的 SOP 闭环（symptom-anchored procedural）+ Claude Code CLAUDE.md 的 project context（project-anchored declarative）在结构上是对应的——业界顶级实现已经在用这个分层，只是没有显式命名。"

---

## 面试可能 Challenge + 防御

**Q1**：你说 60-80% 故障 trace to recent change 这个数据从哪来？
- A: SRE 圈 folklore，Google SRE Book / Etsy postmortem 文化 / Increment Magazine 这种 SRE 媒体经常引；不是某篇 paper 的硬数据，是行业共识。**我面试时会诚实说"这是行业 folklore 不是 paper 硬数据"**——这反而显得严谨

**Q2**：那 declarative 跟 procedural 的边界你怎么定？有些 facts 像"payment-api 50k qps 时 GC 飙高"——这既是 service-specific fact，也是一个可复用的 pattern
- A: 边界是 **诊断时的检索路径**——如果是 "我先想到这个 service" 就是 declarative；如果是 "我先想到这种 pattern" 就是 procedural。**同一条信息可以在两层各放一份**（declarative 那层是 service-specific instance，procedural 那层是去 instance 化的 pattern）

**Q3**：跨组织 / 跨公司怎么共享？同 service 不同公司可以 share 吗？
- A: Declarative 不能（你的 payment-api 跟我的 payment-api 不是同一个东西）；procedural 可以（"P99 spike no error → 先查 saturation" 跨公司适用）。**这就是开源 runbook / blog 文化的本质**——人们分享的都是 procedural，不分享的都是 declarative

**Q4**：那环境变化（service 升级）的级联更新怎么办？
- A: 在两层架构下，**问题被局部化**到 declarative 层的 service-specific instance——升级 v2 → v3 时 service-anchored 的 declarative facts 需要重新 calibrate，但 procedural playbook 不动。这比单层 partition 时**级联更新爆炸**好得多——这正好对应 [[agent-memory-cascading-update]] 提的 3% 准确率问题：**两层架构能把级联范围控制在 service 内部**

**Q5**：你这套是不是马后炮？做的时候没想到，现在反推 SRE 视角才整理出来？
- A: 诚实承认：**是的，做 OpsAgent 时我用的是直觉拆 SOP + multiagent**，事后做研究 audit 才反推到 service-anchored + symptom-anchored 两层。**但这正是反思价值——把"工程过程中没说清楚的设计直觉"升级成可表达可推广的架构原则**。这是从"会做"到"想清楚为什么这样做"的关键步骤

---

## 与 KB / PROJECTS 衔接

- **[[agent-memory-system]]**：Claude Code 6 层架构其实就是分层 storage partition（managed / user / project / local / auto-memory / team）——但没显式区分 declarative vs procedural
- **[[agent-skills-closed-loop]]**：Hermes Skills 是 procedural memory 的工程实现——symptom-anchored 的 SOP 闭环
- **[[agent-memory-cascading-update]]**：单层 partition 时级联更新只有 3% 准确率；两层架构把级联范围限制在 service 内部，是缓解方向之一
- **[[agent-memory-architecture-thesis]]**：Ledger + Views + Policy 三件套 → service-anchored declarative 是 ledger 维度，symptom-anchored procedural 是 views 维度
- **[[main-project-and-research]] §E**：procedural memory 在运维场景的未来延伸——本卡是更精细的"那个 procedural memory 怎么组织"的展开
- **`PROJECTS/research/awm-mechanism-audit/` + `PROJECTS/research/selective-transfer-memory/`**：当前 CV 中真正可讲的研究项目；它们提供 selective reuse、matched/mismatched 与可执行性边界的方法学基础

---

## 边界承认（诚实）

- 这是**反推**资深 SRE 的 mental model，不是**对接**真实 SRE 调研。可信度依赖于 SRE Book / 行业 folklore，不是直接证据。
- 真实生产中的 memory 可能比"两层"更复杂——还有**第三层**（基础设施层，跨 service 跨 symptom，比如 K8s 平台级 quirks）。本卡先讲两层是为了清晰，工程实现可以扩展。
- "Service" 作为 partition 的颗粒度也可以再分（service × component，比如 payment-api/queue vs payment-api/db）；具体到什么颗粒度看实际故障 distribution。

---

## Open Question（不在面试场合主动抛，被问可以讲）

- 跨 service 的 procedural playbook 是不是真的"跨 service 适用"？还是只在**同 tech stack**（Java vs Go vs Python）内适用？这需要 ablation。
- Service-anchored declarative 的**自动 expire / retire** 机制怎么做？service 升级版本后旧 facts 怎么 retire？人工还是规则？
- L1 ↔ L2 的 **interaction protocol**：L2 procedural 调用过程中产生新发现 → 怎么写回 L1 declarative？这是 cascading update 的具体形态。
