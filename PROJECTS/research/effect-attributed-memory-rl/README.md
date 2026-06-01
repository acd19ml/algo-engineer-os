# Tier 1 技术提案：Effect-Attributed Memory Policy with Trajectory-Level RL @ Coding Agent

> **形态**：PEP / RFC 风格技术提案——回答 "这个变化该不该做"，不是 "怎么做"。
> **来源依据**：`PROBLEMS/agent-memory-architecture/` + `KNOWLEDGE/agent/memory-architecture-thesis/` + `RAW_SOURCES/dialogues/conversation_01.md` + `PROJECTS/research/awm-mechanism-audit/` + `PROJECTS/research/selective-transfer-memory/`
> **方法论**：每个技术决策 → 自我 challenge → mitigation → 保底退路。**真实场景代价 first-class**。

---

## ✦ Research Scope & Framing Declaration

> **本项目通过 Socratic + 第一性 audit 已锁定的研究范围。任何后续 framing 偏离都要回这里重 audit**。

### 研究层级：Mechanism Layer，不是 Content Layer

| 层 | 含义 | 本项目范围 |
|---|---|---|
| **机制层 (Mechanism)** | 怎么 trigger / patch / retrieve / attribute effect / detect drift | ✅ **研究目标** |
| **内容层 (Content)** | 具体存什么 SOP / 哪些事实 / 哪些规则 | ❌ **不研究**（内容必然 domain-bound）|
| **评估层 (Evaluation)** | 什么算 success / effect 怎么测 | ⚠️ 部分研究——attribution method (logits Δ / counterfactual) 是 mechanism，success 定义是 content |

### Mechanism Cluster 聚焦：C1（Effect-aware Lifecycle）

本项目研究 procedural memory 6 个 mechanism gap 中的一个 cluster，**不是全部**：

| Cluster | 包含 invariant | 共同 mechanism | 本项目状态 |
|---|---|---|---|
| **C1 · Effect-aware Lifecycle** | a (drift) + d (distribution) + j (attribution) | 都是"知道 memory 当前价值"——drift 是价值衰减，attribution 是价值归因，distribution 是价值随机性 | ✅ **主线** |
| C2 · Prior-informed Retrieval | b (frequency prior) + i (multi-index) | 都是"用什么 prior 选 memory" | Future work |
| C3 · Bootstrap & Cold-start | g (new env cold start) | 新 domain 无 memory 时如何起步 | Future work |

### Test Bed：Coding Agent，不是 Ops 代理

OpenClaw fork 作 **mechanism exerciser**——存在 procedural memory layer + 多 step task + 可 attribution 的 reward signal——能 exercise C1 机制即可。**不声明 coding agent 是 ops 的代理**。

### Transfer 声明（诚实边界 · 反复 audit 不变量）

| 项 | 声明 | 论证依据 |
|---|---|---|
| ✅ **机制 Transfer** | trigger / revision / attribution / lifecycle policy 可以迁移到 ops 等其他 domain | Hermes Skills 同一套机制在 devops / data-science / mlops work + Claude Code 同一套机制在 coding / 知识库管理 / research agent 都 work——已有先例 |
| ❌ **内容 Transfer** | 在 coding agent 训练得到的具体 memory items **不能**直接迁移到 ops | 内容必须根据 target domain 重做——这是任何 domain 应用的常态，不是项目缺陷 |
| ⚠️ **机制有效性 Transfer** | "在 coding 上 work 的机制，在 ops 上也 work" 是 **hypothesis 不是 fact** | 受 procedural memory 在 ops vs coding 中的权重不对称影响（ops procedural-rich, coding procedural-thin）；机制设计原则 transfer，但参数 / 触发阈值要重新 calibrate |

### Out-of-scope（明确不做）

- ❌ 内容层 SOP 设计（这是 Hermes Skills authors 做的事，不是研究 contribution）
- ❌ C2 + C3 cluster（虽然是真 mechanism gap，但 Phase 1 scope 不包含）
- ❌ Memory 在非平稳生产 ops env 的实际部署（需要真实可观测基础设施）
- ❌ Declarative memory layer 的 policy 训练（D2 patch 已声明：declarative policy 留 Phase 2）

### 给面试官 / mentor 的一句话 summary

> "**这是 procedural memory 机制层的研究，聚焦 effect-aware lifecycle (drift detection + distribution-aware reward + attribution method)，用 coding agent 作 mechanism exerciser，不声明内容迁移到 ops——但机制设计原则是 transferable，已有 Hermes Skills / Claude Code 跨 domain 应用作先例。**"

---

## 0. 问题陈述

外部记忆系统的核心矛盾是：**记忆的价值只能从未来才能验证，但写入决策必须在当下做出**。

业界两条路：

- **Claude Code / OpenClaw**（详见 `PROBLEMS/agent-memory-architecture/`）把写入决策交给 LLM 自决或 Pre-compaction Flush → policy 不可回放、不可训练、上限被 prompt 工程封顶
- **Memory-R1 / Mem-α**（`memory-architecture-thesis` § Memory 操作工具化）把 ADD/UPDATE/DELETE/NONE 建模为 RL action → 训练范式打通，但 reward 仍是**步骤级 task pass**：一次操作只看当前 step → eyeing 当下，忽略累积效应

`conversation_01.md` 提炼的核心论点（综述 Section 5.3 + Karpathy autoresearch 例证）：**记忆决策的真实价值需要从下游 N 个 task 的累积成功率才能显现**。步骤级 reward 反馈回路太短。

同时，`selective-transfer-memory` 已证明：**记忆抽象的可执行性（不是形态）决定跨任务复用边界**。

合起来：业界缺一个**"轨迹级 reward + memory 效果归因 + 可执行性 gate"** 三件事都做对的 memory policy 训练范式。

---

## 1. 核心命题（一句话）

> **把 procedural memory 的 ADD/UPDATE/DELETE/NONE 决策建模为 trajectory-level RL action（属于 C1 · Effect-aware Lifecycle 机制层研究），reward 来自下游 N 个相关任务的累积效果归因（而非单步 task pass），policy 在 SFT 冷启动 + GRPO 微调下学会在不同 task 上下文中选择最优 memory operation，并用最小化可执行 schema gate 约束写入形态。**

**C1 三件事映射**：
- **a (drift detection)** → policy 学到的 UPDATE/DELETE 决策是 drift response
- **d (distribution-aware reward)** → trajectory-level reward + group-wise advantage 让 success/failure 以分布形态参与训练
- **j (effect attribution)** → logits Δ + counterfactual ablation + GRPO group-wise contrast 三轴归因

**与 Memory-R1 / Mem-α 的关键差异**：它们做的是 step-level reward（C1 的 a 和 d 都缺失），本项目的 contribution 在 **把 reward 信号扩展到 trajectory-level 并显式建模 effect attribution**。

---

## 2. 为什么必须做（每条都对应真实代价）

| 缺什么 | 真实代价 |
|---|---|
| Policy 不可回放 | 生产 memory 出错时无法 debug "为什么这条 memory 当时被写下" |
| Step-level reward | policy 在首个 task work，下游 cascade 失败时无法归因 |
| Effect 不可观测 | 不知道"哪条 memory 真有用 vs 浪费 context"，无法做 retire / pruning |
| 可执行性无 gate | 写入的 memory 在 retrieve 时被 LLM ignore，召回浪费（你 selective-transfer 实验已实证）|

---

## 2.5 · 落地具体效果：4-week case study

> **目的**：用一个具象场景验证 §2 抽象代价 + Part B 每个技术贡献。**你后续分析这套系统真实价值的依据**。
>
> **Setup**：个人 SaaS 项目（Next.js 14 + tRPC v10 + Prisma 4 + Vercel）+ OpenClaw 维护 + 同步运行 baseline OpenClaw（无本系统，只用默认 Hermes Skills 自决触发）做对照。

### Week 1

#### Task 1（day 1）· 用户头像上传 silently fail，没 error

**Baseline** (无本系统)：
```
Agent 探索路径:
  1. read upload component (src/components/avatar/upload.tsx)
  2. read API route (src/app/api/avatar/route.ts)
  3. check Cloudinary SDK
  4. run integration test → 没 error 但失败
  5. read middleware / next.config.js / ...
  发现 NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME 在 Vercel preview 没设
30 tool calls, 25 min
```

**本系统**：与 baseline 相同（memory pool 为空，冷启动状态）。**但 task 完成后** policy 决定 ADD memory（**D2/D5 触发**）：

```yaml
skill: vercel-preview-env-var-missing-silent-fail
trigger: "feature silently fails on Vercel preview but works locally"
action:
  - Check Vercel dashboard env vars (not just .env.local)
  - Verify NEXT_PUBLIC_* in correct env (preview/production)
  - vercel env pull to compare
validation: "curl deployment URL, check 200 + correct response"
avoid: "DON'T assume .env.local same as Vercel preview"
```

**D5 schema gate** 自动 sandbox dry-run，pass.

#### Task 2（day 4）· Stripe checkout 在 preview 报 'API key not configured'

**Baseline**：25 tool calls, 20 min（重新探索）。

**本系统**：
```
Retrieve memory (D3 multi-index): 
  Top match: vercel-preview-env-var-missing-silent-fail (trigger 部分 match)
Agent 直接执行 memory action sequence:
  Step 1: vercel env pull --environment=preview → 看到 STRIPE_* 缺失
  Step 2: Vercel dashboard 加 env var
  Step 3: 重新 deploy + validation 通过
5 tool calls, 3 min, SUCCESS
```

**GRPO group-wise** 同时跑 with/without memory 两条 rollout（**D3**），logits Δ 在 step 1 显著（带 memory 时直接选 `vercel env pull`，不带时 read 多 file）。**Effect attribution** 记录：这次 memory 贡献 +22 min saved.

### Week 2

#### Task 3（day 8）· ESLint 报 'cannot find module @types/react-dom'

**Baseline**：15 min（删 node_modules + npm i）。

**本系统**：
```
Retrieve memory: vercel-env memory (trigger 不匹配，drop); 其他候选 score < threshold
No memory retrieved → fallback baseline path
15 min 解决
```

Task 完成后，**policy 决定 NONE**——不写 memory。

为什么？policy 学到的（**D1 RL trained 关键价值**）：
- 这是 one-off problem（不是 systematic pattern）
- 解决步骤已经在 base model pretrained knowledge 里——写 memory 浪费 retrieve budget
- Logits Δ 在 baseline path 上很小（model 本来就知道）

**这是 D1 的关键 deliver**：Hermes 默认会**强制**写 memory（"5+ tool calls + tricky error → 写"）；RL policy 学会 **何时不写**——避免 pool noise 累积。

#### Task 4（day 10）· Prisma migrate: JSON column → relation

**Baseline**：50+ tool calls, 1.5 hour（试 --create-only, 手动 SQL, 数据丢失一次, 重试）。

**本系统**：同 baseline（pool 没有相关项）。Task 完成后 ADD：

```yaml
skill: prisma-json-to-relation-migration
trigger: "migrating Prisma JSON column to relation while preserving data"
action:
  - Create new relation model with FK column
  - prisma migrate dev --create-only --name <descriptive>
  - 手动 add data transformation SQL in migration.sql (UPDATE...JOIN before DROP)
  - Apply with prisma migrate dev
validation:
  - prisma migrate diff (should show no diff)
  - SELECT count from new relation = SELECT count from old JSON
avoid:
  - DON'T just drop column and add relation in single migration—data lost
  - DON'T edit production migrations.sql after deploy
```

**Schema gate dry-run** 在 toy Prisma project sandbox，pass.

### Week 3 · Drift detection

#### Day 18 · 升级 Prisma 4 → 5

升级后，memory `prisma-json-to-relation-migration` **悄悄发生 drift**：
- `--create-only` flag 行为微调
- 新 migration file 默认 header 格式不同

但 memory 不知道——直到下一次相关 task。

#### Task 5（day 20）· 另一个 JSON → relation 迁移

**带 memory 跑**：
```
Step 1: Create relation model → OK
Step 2: prisma migrate dev --create-only → 行为不同，生成的 .sql 结构变了
Step 3: 手动 SQL 不再 fit 新文件结构 → ERROR
Agent 自适应，read Prisma 5 changelog 重新 figure out
25 tool calls, 25 min（比 memory-aided 慢，但比 from scratch 快）
```

**Effect attribution module 检测**（**D3 三轴归因**）：
- Trajectory-level reward：比 task 4 当时低
- Logits Δ：step 1-2 时 memory 仍 steer 模型——但 step 3 **divergence**
- Group-wise contrast：这次 with-memory 在 step 3 后**比 without-memory 慢**

**这是 drift 信号**。Policy 决定 UPDATE（**D2 a-invariant 触发**）：

```yaml
patched skill: prisma-json-to-relation-migration
new context: "For Prisma 5+, --create-only generates different migration structure"
prepended action:
  - First check prisma --version
  - If >=5.0, use approach A (modify SQL after generation)
  - If <5.0, use approach B (original action)
```

**没有本系统**：memory 静默错误，下次还会让 agent 多花 20 min 才发现。

### Week 4 · Cross-user 转移

#### Day 25 · 新 developer 加入项目

**Baseline (新人 + 默认 OpenClaw)**：
```
新人 + agent 探索:
  read schema, auth flow, decide email arch, implement
  踩 Vercel preview env var 坑 (task 1 同根因, 新人不知道)
  踩 Prisma migration 坑
共 2 天
```

**本系统 (team-shared memory pool, 你 4 周累积 ~12 skills)**：
```
Task 开始时 retrieve:
  - vercel-preview-env-var-missing-silent-fail
  - prisma-add-field-with-default
  - email-sending-resend-pattern
  - prisma-json-to-relation-migration

Agent + 新人:
  - Skip env var 坑 (memory 主动提醒)
  - Skip Prisma migration 坑
  - 复用 Resend pattern
共 6 hours
```

**Value**: 4× faster onboarding + 不重复你踩过的坑。

### 4 周总账

| 维度 | Baseline | 本系统 |
|---|---|---|
| 总 task 时间 | ~6 hours | ~2.5 hours |
| Memory pool size | 不存在 | 12 skills（all with effect scores） |
| Drift detected/handled | 0 | 1（Prisma 升级） |
| Noise memory 累积 | N/A | 0（policy 学会 NONE） |
| Cross-user transfer | 不存在 | 1 次（新人 onboard） |
| Pool degradation 风险 | N/A | low（attribution + drift 持续维护） |

**60% 时间节省**。但更重要的：
- **没有 silent fail**（drift 自动检测，不是用户撞墙后才发现）
- **没有 pool degradation**（policy 学会拒绝低价值 memory）
- **knowledge 沉淀到 team**（不是个人 in-context 知识）

### 哪些 tech 是 essential（不是 nice-to-have）

| Tech | 关键 demo 时刻 | 没有它会怎样 |
|---|---|---|
| **D4 SFT 冷启动** | Task 1 完成后 ADD memory，schema 4 字段格式正确 | 纯 RL → 写出 garbage schema，schema gate 全 fail，policy 训不出来 |
| **D1 RL trained policy (GRPO)** | Task 3：学会 NONE | Hermes 默认规则强制写 → noise 累积 → 几月后 pool 不可用 |
| **D2 Trajectory-level reward** | Week 3 drift 检测：reward 信号让 policy 看到"任务虽 pass 但更慢" | Step-level → 只看 task pass，drift 隐藏 |
| **D3 Logits Δ + GRPO group-wise** | Task 5 step 3 divergence 检测 | 没有 → drift 要等 catastrophic failure 才发现 |
| **D3 Effect attribution** | Week 4: pool 12 条都有 effect score | 没有 → 不知道哪条真有用，无法 retire |
| **两层架构** (D2/D5 patch) | 本 case demo procedural 层；"Prisma 当前版本"作为 declarative fact 独立维护 | 没有 → "事实变化" 和 "playbook 变化" 混淆，attribution 不干净 |
| **D5 Schema gate** | Task 1: ADD 时自动 sandbox dry-run | 没有 → 写出 "应该检查 env vars" 这种 generic memory，retrieve 无法精确匹配 |

### 诚实 caveats

1. **不是所有数字都可信**：60% 时间节省是**理想情况**——真实 deploy 会被 corner case 拖累。30-40% 节省是合理预期。
2. **Hermes Skills 已经能做约 50% 的事**：写入触发 / patch / retrieve 已存在。本项目真正 delta 在：
   - RL trained policy 替换 prompt-based 触发（在线改进 vs 固定规则）
   - **Effect attribution**（Hermes 完全没有，真 gap）
   - **Drift detection**（Hermes 靠 agent 跑挂才发现）
   - **两层架构**（Hermes 把所有 memory 当 Skill，混了 declarative facts）
3. **"60%"对照基线很容易被 Hermes 拿走 30%**——本方法在 Hermes 基础上的增量价值约 30%。
4. **Drift detection 是最 unique 价值**——Hermes / Claude Code 都没有，业界没人做。这是 contribution 最实在的点。

---

## 3. Proposed Solution（high-level，详细架构留 Tier 2）

五个组件：

1. **Memory Schema**——最小可执行四字段（trigger / action sequence / validation / avoid_constraint），沿用 Hermes Skills 形态（见 `agent-skills-closed-loop`），不做 schema 创新
2. **Policy Network**——输入 (task state, candidate memory set, retrieved memory)，输出 (op ∈ {ADD, UPDATE, DELETE, NONE}, target_memory_id, payload)
3. **Effect Attribution Module**——logits Δ + GRPO group-wise advantage + prioritized counterfactual ablation
4. **Reward Composer**——`R = α·R_traj + β·R_step_proxy + γ·R_executable + δ·R_audit_penalty`
5. **Training Loop**——SFT 冷启动（弱监督）→ GRPO 微调（trajectory-level reward）

---

## 4. 关键技术决策 × 自我 Challenge × 保底退路（10 个）

### D1 · Memory Policy 用 RL 训而非 prompt

**为什么这样选**：Prompt-based policy 不可回放，且上限被 LLM in-context learning 封顶；学术（Memory-R1 / Mem-α）已经证明 RL action 路径可走。

**Challenge**：
- 真实场景 RL trained policy 易在 OOD task 上崩——它学到了训练 task distribution 上的规律，但真实用户 distribution 完全不同
- Memory-R1 在通用 QA 上 work，但 coding agent 是 multi-turn + tool-use + 长 horizon，policy 复杂度上一个量级
- 训练数据来源单一（SWE-bench-Lite）→ policy 对单一 codebase / 单一 bug type 过拟合

**Mitigation**：
- SFT 冷启动数据加多 source（SWE-bench + OpsAgent trajectory + Hermes Skills 公开 examples）
- RL 阶段保留 prompt-based policy 作 ensemble fallback（policy 输出 confidence 低时回退到 prompt 决策）
- 评测**显式报告 ID vs OOD 退化曲线**，不只报训练分布上的指标

**保底**：RL 不稳定 → 退化到 SFT-only。SFT-only baseline 仍是 contribution（首次系统化轨迹级标注 + 弱监督方法学）

---

### D2 · Reward 用 trajectory-level（不是 step-level Memory-R1）

**为什么这样选**：步骤级 reward 反馈回路太短（你 conversation_01 已论证），记忆决策真实价值是累积的。

**Challenge**：
- Trajectory-level reward 极度稀疏（binary pass/fail）→ credit assignment 困难
- 真实 SWE-bench-Lite task 跑 1-2 小时，单 trajectory rollout 代价巨大
- 100h GPU 预算 → 满规模 trajectory ≈ 100 条，根本不够 GRPO 收敛
- **"下游 N 个相关任务的累积成功率"** 自身是 ill-posed：N 多大？什么算"相关"？相关性判定本身是另一个 ill-posed 子问题

**Mitigation**：
- **混合 reward**：trajectory-level (主，权重 α=0.5-0.7) + step-level proxy (辅，logits Δ × 召回-使用一致性) → 缓解稀疏
- **task 选择缩到可快速 eval**：SWE-bench-Lite 中挑**单 issue + 单文件 fix** 的 5-15 分钟 task，让 rollout 数量上得去（100h → 300-600 条 rollout）
- **"相关任务"先用人工 cluster**：同 repo + 同 module + 同 bug type；Layer 2 才考虑 unsupervised 聚类
- GRPO 同 task sample N=4-8 条 trajectory，其中部分带 memory 部分不带 → contrast 自动给 effect 信号

**保底**：trajectory-level 不收敛 → 退化到 step-level + 后处理统计相关任务集合的累积效果（事后报告而非训练信号）。轨迹级 vs 步骤级的对比本身仍可作为 paper contribution。

**⚠️ 两层架构下的修正**（来自 senior SRE 反推洞察）：

D2 原版假设 memory items 同质，单一 trajectory-level reward。**两层架构下应分开**：

- **Declarative memory policy 的 reward** = **factual correctness + currency**（事实正不正确 + 是否过期），**不是 task pass rate**——一个 fact 写错了就是错了，跟"它被用在哪个 task"无关
- **Procedural memory policy 的 reward** = **cross-task success rate**（一个 playbook 在多个 task 上累积有效率）——**这才是真正的 trajectory-level reward**

**Phase 1 范围内只训 procedural memory policy**（与 trajectory-level reward 自然对接），declarative memory policy 留 Phase 2。这是相比原版 scope 的**正向缩减**：从"训一个通用 memory policy"缩到"训 procedural playbook 调度 policy"——主线更清晰、attribution 更干净。

---

### D3 · 效果测量用 logits Δ + GRPO group-wise（训练）+ prioritized ablation（最终评测）

**为什么这样选**：
- Logits Δ 直接观察 memory 对决策的瞬时调制幅度（`memory-architecture-thesis` § 修正项 Δ 给的 JitRL 公式），免消融
- GRPO group-wise 自然 ablation，训练 + 测量一体（最优雅）
- 完整 ablation 代价高，只在最终评测时对 top-k 可疑 memory 做

**Challenge**：
- **Logits Δ 测瞬时调制幅度 ≠ 真帮忙**——可能改了决策但导致失败（Δ 大但 success rate 低 = reward hacking 嫌疑）
- Logits Δ 在闭源 API 模型完全不可用（无 logit 访问）→ 生产部署不通用
- GRPO group-wise 的 with/without 随机化让 advantage 估计噪声大
- Prioritized ablation 的"优先级"依赖 logits Δ → 如果 Δ 信号不准，整套排序失效（recursive dependency）

**Mitigation**：
- Logits Δ 仅训练时用（本地 Qwen），生产部署改用 **action-level proxy**（执行分歧度 / 召回-使用一致性 / 使用频次 × success 共变）
- GRPO group-wise 把 with/without 当**两个独立 group**分开估 advantage 再 contrast，不混在同一 group
- Prioritized ablation 加 **ensemble 优先级**（logits Δ + 召回频次 + reward 方差三轴，不单押 Δ）

**保底**：logits Δ 不可靠 → 退化到 GRPO group-wise + 周期完整 ablation（代价高但更可靠）。即使全套 effect attribution 失效，pure trajectory reward 训出的 policy 仍可作为 baseline 报。

---

### D4 · SFT 冷启动数据从哪来

**为什么这样选**：直接 RL 训不稳，需要 SFT 给 policy 起点。

**Challenge**：
- SFT 需要 (state, ground-truth memory op) pairs，但 **ground truth op 本身是 ill-defined**——没人知道"正确"写入决策是什么
- LLM-as-judge 标注 → bias 传递（LLM 的判断本身就是要学的对象）
- 人工标注 → 不可扩展且主观

**Mitigation**：
- SFT 数据用**弱监督**：
  - **正例**：从成功 trajectory 中观察 "LLM 在哪些 step 自己决定写 memory"
  - **负例**：从失败 trajectory 中观察 "哪些 step 没写但应该写 / 写了但导致失败"
- 不强求"正确答案"，只学 **success pattern vs failure pattern**
- 加入 `conversation_01` 中你已经 articulated 的写入策略（故障域聚合 / 分层记忆 / 失败按原因分类）作为人工 seed
- SFT 数据规模目标 1-3k 条（参考 `training/sft-data-size`）

**保底**：弱监督质量太差 → 退化到 BC (behavior cloning) on Claude Code 的实际 `extractMemories` 输出（虽 noisy 但是 production-grade signal）

---

### D5 · 可执行性作为 schema gate，不作为研究 dimension

**为什么这样选**：你 selective-transfer 实验已证可执行性决定跨任务复用边界，形态不重要。

**Challenge**：
- "可执行" 的形式化定义是什么？没有定义就没法做 gate
- 即使不研究 schema 创新，仍需一个最小可执行 schema 作 baseline——这个 baseline 本身就是 nontrivial 设计
- "Hermes Skills schema" 沿用是否过于依赖某个特定开源系统

**Mitigation**：
- **最小化 schema**：`{trigger_condition, action_sequence, validation, avoid_constraint}` 四字段（参考 `agent-skills-closed-loop` 的 4 要素）
- 可执行性 gate 用**自动 dry-run 测试**：write 完一条 memory 后，在 sandbox 用 similar task 试 retrieve + 执行，能完整执行（trigger 命中 + action 可执行 + validation 通过）则 pass
- 不绑定 Hermes Skills，schema 设计原则可移植

**保底**：dry-run gate 不可靠 → 退化到人工 review schema validity（Phase 1 task 数小，可承受）

**⚠️ 两层架构下的修正**：

D5 原版假设"可执行性"是单一概念。**两层架构下两种 executability 不同**：

| 层 | 可执行性定义 | 验证方式 |
|---|---|---|
| **Declarative facts** | **retrieval-executable**——能被 retrieve + 注入 prompt + LLM 在 reasoning 中真引用 | 召回精度 + 引用一致性（D3 logits Δ 信号能直接复用） |
| **Procedural playbook** | **execution-executable**——能按步骤执行 + verification 通过 | trigger 命中 + action sequence 跑通 + validation gate（Hermes Skills 4 字段） |

**Phase 1 先做 procedural 那层的 execution-executable gate**（沿用 Hermes Skills 4 字段：trigger / action / validation / avoid_constraint）。Declarative 那层 retrieval-executable gate 留 Phase 2——与 D2 的两层 reward 分层呼应。

---

### D6 · Harness 选 OpenClaw fork

**为什么这样选**：必须深度修 memory 写入触发点 + retrieve 逻辑；纯 prompt 改不够。

**Challenge**：
- Claude Code 闭源 → 只能用 community fork（claw-code），upstream 跟进困难
- OpenClaw 开源但小众 → 社区资源少
- 两者 memory hook 位置不同，portability 差
- Fork 改造完，paper / 项目 contribution 是否绑定具体 harness？通用性怎么说

**Mitigation**：
- 优先 **OpenClaw**：
  - (a) 真开源，code 可读 + 可改
  - (b) Memory Flush 设计模块化便于改 hook
  - (c) SQLite + embedding 检索路径工程化，便于训练 reward 接入
- Fork 后建立 **upstream patch 序列**，方便 rebase
- 在 paper / report 中明确"contribution 是 harness-agnostic 的 policy 训练范式"，但 phase 1 只验证一个

**保底**：OpenClaw 太小众 → 回退 claw-code（Claude Code fork）

---

### D7 · Phase 1 限定 Layer 1（受控）而不做 Layer 2（杂乱无标记）

**为什么这样选**：Layer 2 难点在数据预处理（自动聚类 + 自动评测 + 自动蒸馏），不在 effect measurement framework——这些预处理需数月工程，超 Phase 1 范围。

**Challenge**（**这是你最关心的点**）：
- 你明确说"不能假设完美实验环境"——只做 Layer 1 = 假设完美环境
- 受控实验 work 不代表真实场景 work
- matched/mismatched 配对是人工标的，真实任务相似性未知
- 面试官追问"那真实部署会怎样" → 没答案就崩

**Mitigation**：
- **Phase 1 Layer 1 内必须包含 stress test**：
  - 注入 **noisy memory**（10-20% memory 是无关或错误的）
  - 注入 **OOD task**（训练时没见过的 repo / bug type）
  - **标签 ablation**：去掉部分 matched/mismatched 标注模拟 unsupervised 情境
- **报告退化曲线**，不只报 best-case——OOD task 上 policy 退化多少？noisy memory 注入多少时 policy 开始崩？
- Phase 1 report 开 1 章 "Layer 2 scaling considerations"，从 Layer 1 结果推断 Layer 2 瓶颈

**保底**：stress test 暴露 fatal 失败 → Phase 1 改方向，做更窄的 sub-question（如"仅在固定 task family 内的 memory revision"），保留诚实边界。

---

### D8 · 数据集 = SWE-bench-Lite 子集 + 多 session 模拟

**为什么这样选**：业界标准 + 真实 GitHub bug fix + 自动 pass/fail 评测。

**Challenge**：
- 30-50 task 子集**统计意义弱**，paper-level 不够
- "挑有重复 pattern 的"本身是 selection bias → cherry-pick 嫌疑
- SWE-bench task 隔离独立，**没有真实 user 多 session 连续性** → 不能完整测 memory 跨 session 价值
- 单 task 1-2h，100h GPU 预算下 rollout 数量受限

**Mitigation**：
- 子集挑选 criteria **公开**（同 repo / 同 module / 同 bug type）+ 提供**随机 baseline 子集**对比，证明非 cherry-pick
- **加入 multi-session 模拟**：把 task 序列化（先做 task_a 再做 task_b，task_b 时 memory 池含 task_a 写入），模拟 session 间复用
- 单 task 选 **5-15 分钟可跑完** 的（不是全 SWE-bench-Lite），保留预算可行性
- Report 明确 boundary："this is a pilot study, not a full benchmark"

**保底**：SWE-bench-Lite 不够 → 加 **MetaR / MLE-bench** 作辅助 dataset，covers ML 实验类任务（也命中 procedural memory 跨任务复用语义）

---

### D9 · Reward Composer 怎么组合各信号

**为什么这样选**：纯 trajectory-level 稀疏，纯 step-level 短视，纯可执行 gate 不带 task signal——必须组合。

**Challenge**：
- 权重 α/β/γ/δ 怎么定？是否 sensitive？
- Step-level proxy 信号有偏（logits Δ 测瞬时调制非真实帮助），加权可能引入 bias
- 如何避免 reward hacking？policy 可能学到"加 memory 让 logits Δ 大"而不是"真帮忙"

**Mitigation**：
- Reward 形式：
  ```
  R = α · R_traj          # 下游 N 个相关任务累积 pass rate (主)
    + β · R_step_proxy    # logits Δ × 召回-使用一致性 (辅，避免 Δ 大但 LLM 没用)
    + γ · R_executable    # 可执行 schema gate 是否 pass (binary)
    + δ · R_audit_penalty # 审计者发现 reward hacking 时扣分
  ```
- 权重 **sensitivity analysis 必报**：跑 α/β/γ/δ 的 grid search 摘要
- **审计者作为独立组件**：用独立 LLM 在 trajectory 后扫描"memory 信息含量是否低但 logits Δ 大"——典型 reward hacking 信号
- 审计 prompt 用 `agent-failure-attribution` + `agent-anomaly-taxonomy` 的 11 类异常分类作 reference

**保底**：组合 reward 不收敛 → 回退 pure trajectory-level + 后处理统计 step-level（事后报告而非训练信号）

---

### D10 · 实验报告必须做"真实场景投影"

**为什么这样选**：你最强诉求："实验数据集可能是一个投影，但不能假设完美实验环境、一到真实任务就崩"。**这是整个 Phase 1 的核心健康性约束**。

**Challenge**：
- SWE-bench-Lite 投影到真实 coding agent task 的 gap 在哪？
- Policy 训练 + eval 都在 controlled，真实场景 failure mode 在 lab 测不到
- 实验做完，怎么 argue "这个 work 真实场景能 work"？
- 即使 in-lab 90% pass，到真实场景可能 < 30%

**Mitigation · 三层投影报告**（必须全做，不能省）：

1. **In-distribution**：SWE-bench-Lite 训练子集上的指标（**lab grade**）
2. **OOD-controlled**：训练时没见过但同分布的 task（同 repo 不同 file / 同 bug type 不同 repo）（**generalization grade**）
3. **Real-world projection**：取 1 个 production coding agent 的真实失败轨迹 sample（OpenClaw GitHub issues / claude-code-related bug reports），**让训出的 policy 重跑这些 trajectory，定性观察 + 量化使用率**（**real grade**）

报告中**显式承认 boundary**：哪些 failure mode 没测、哪些假设没 verify。

**保底**：real-world projection 暴露 policy 完全不可用 → Phase 1 report 改为 **"负面结果 + 失败模式分析"**——这本身就是有价值的研究 contribution（业界刚起步，负面结果稀缺，CityU 学术 mentor 也认可这种诚实 paper）。

---

## 5. 已考虑的替代方案

| 方案 | 为什么不选 |
|---|---|
| Pure prompt-engineered policy (no training) | 上限被 LLM 封顶；不可回放；与你诉求"必须有训练经验"冲突 |
| Memory-R1 直接复刻 | 步骤级 reward 已被你识别为局限；复刻不是创新 |
| G2 declarative × procedural 共存 | scope 过大，Phase 1 不可能完成；作为 future work |
| Schema 创新（候选 3 原版） | 你已明确形态不重要 |
| OpsAgent + procedural memory (Dir-B) | 无 public benchmark；说服力打折；与 mentor 学术方向不匹配 |
| 候选 1（不引 trajectory-level） | 不解决 conversation_01 指出的步骤级回路太短问题 |

---

## 6. 真实场景风险表

| # | 风险 | 概率 | 严重度 | Mitigation 摘要 | 保底 |
|---|---|---|---|---|---|
| R1 | RL 不收敛 | 中 | 高 | SFT-only baseline | SFT-only paper |
| R2 | Trajectory reward 稀疏训不动 | 高 | 中 | 混合 reward + step proxy | step-level + 后处理 |
| R3 | OOD 退化严重 | 高 | 高 | Stress test + 报告退化曲线 + ensemble fallback | 缩 scope 到 fixed task family |
| R4 | Logits Δ 信号噪声大 | 中 | 中 | Ensemble 优先级 + 周期完整 ablation | 全 ablation |
| R5 | 100h GPU 预算超 | 高 | 高 | 小模型 1.5B 先验证 + 缩 task scope | Qwen 1.5B 出 Phase 1 |
| R6 | OpenClaw harness 改造过深 upstream 跟不上 | 中 | 低 | upstream patch 序列 | 维护静态 fork |
| R7 | Reward hacking 暴露 paper 不严谨 | 中 | 高 | 审计者组件 + 主动报告 | 改为 reward design analysis paper |
| R8 | 数据集 cherry-pick 嫌疑 | 中 | 中 | 公开 criteria + random baseline | 加 MetaR 辅助 |
| R9 | Real-world projection 完全不 work | 中 | 高 | 改为负面结果 + 失败模式分析 paper | 见 D10 保底 |

---

## 7. 成功标准（Phase 1）

### 必须达成（show-stopper if missed）

- **S1**：训出的 policy 在 in-distribution 测试集上比 **prompt-only baseline** 高 ≥ 5% trajectory-level pass rate
- **S2**：Effect attribution 框架在 prioritized ablation 验证下，**logits Δ 与 counterfactual pass 差呈 ≥ 0.4 相关**
- **S3**：Stress test 下退化曲线**平滑**（OOD task pass rate 退化 < 30%）

### 应当达成

- **S4**：Reward hacking 审计未发现严重 bias
- **S5**：Real-world projection（OpenClaw issues 真实失败 trajectory）定性观察到 policy 给出合理 op 建议

### Bonus

- **S6**：复现 selective-transfer 的 matched/mismatched 差异（说明可执行性 gate 起作用）

---

## 8. 时间表（8-12 周，项目 + 实习并行，CityU mentor 随时请教）

| Week | 内容 | Deliverable |
|---|---|---|
| 1-2 | OpenClaw fork + memory hook 改造 + 最小 schema 实现 + SWE-bench-Lite 子集筛选 | code repo + dataset spec |
| 3-4 | SFT 冷启动数据生产（弱监督）+ 第一版 SFT policy + logits Δ 测量 pipeline | SFT checkpoint + measurement code |
| 5-6 | GRPO 训练（先 Qwen 1.5B 验证收敛性，再 7B 跑最终）+ 混合 reward + 自然 ablation | GRPO checkpoint + reward log |
| 7-8 | Effect attribution module + prioritized ablation + audit 组件 | 完整 effect measurement pipeline |
| 9-10 | Stress test + OOD eval + **real-world projection (OpenClaw issues)** | 完整评测报告 v1 |
| 11-12 | Paper / blog 撰写 + 开源 release + selective-transfer 对接验证 | 最终 deliverable |

---

## 9. Open Questions（不在 Phase 1 解决）

### Mechanism Cluster 未覆盖部分（按 Scope Declaration）

- **C2 · Prior-informed Retrieval (b + i)**：frequency-weighted ranking + multi-dim retrieval policy——Phase 1 用简单 retrieval baseline，正经研究留 Phase 2
- **C3 · Bootstrap & Cold-start (g)**：新 domain 无 memory 时的 bootstrap 机制——Phase 1 用 LLM-as-judge 蒸馏弱监督，正经研究（meta-learning / synthetic data / human seed protocol）留 Phase 2

### 其他延伸方向

- **Layer 2 杂乱无标记轨迹的处理**：聚类质量 / 自动评测 / 蒸馏小模型——Phase 2
- **跨 user / 跨场景 namespace 隔离**：故障域聚合记忆设计（故障域聚合两层架构设计）——Phase 2
- **Declarative memory policy 训练**：D2/D5 patch 已声明两层架构下 declarative layer 独立——Phase 2 主线
- **元认知"审计者"递归层数**：`conversation_01` 中"审计者-执行者"二到三层架构——Phase 3
- **Procedural × declarative 共存**：G2 方向——独立项目

### 跨 domain 机制有效性验证（最深 open question）

- **声明的"机制 transfer"在 ops 上是否真 work？**：scope declaration 承认这是 hypothesis 不是 fact。Phase 1 不验证，但 Phase 2+ 应该有 minimal ops case study（拿 1 个真实 ops trace + postmortem，看机制是否能 apply 即使不能完整 evaluate）

---

## 10. 与已有研究的衔接（机制层视角）

每一条衔接都在**机制层**——本项目不延续他人的内容，而是延续 / 补全他们的机制设计。

- **AWM mechanism audit** (`PROJECTS/research/awm-mechanism-audit/`)：识别 AWM 缺失的 **机制 gap** = revision loop + abstraction-execution gap → 本项目的 policy 训练补 revision **机制**；可执行性 gate 补 abstraction-execution **机制**——不复用 AWM 的具体 workflow 内容
- **selective-transfer** (`PROJECTS/research/selective-transfer-memory/`)：识别的**机制原则** = "记忆抽象的可执行性决定跨任务复用边界" → 本项目用其作 schema gate + matched/mismatched 评测设计——是**评测方法学** transfer 不是任务内容 transfer
- **memory-architecture-thesis**：理论**机制框架** (Ledger + Views + Policy) → 本项目把 **Policy 机制**显式化为 RL trained policy（Ledger + Views 用 OpenClaw 已有实现）
- **conversation_01**：人类元认知三层 + 后果回写 + Karpathy autoresearch → 本项目实现"**后果回写**" **机制层**（trajectory-level reward + effect attribution 即此层的工程化）；"审计者-执行者" 第三层留 Phase 3 future work
- **PROBLEMS/agent-memory-architecture**：5 个 Open Questions 中 G1 (Policy 显式化) → 本项目核心命题——**显式化的是 policy 机制**，不是 policy 决策内容
- **agent-skills-closed-loop (Hermes Skills)**：现成的 **procedural memory 闭环机制范本**——本项目在它的 patch / 触发 / 渐进加载机制基础上，把"agent 自决"prompt-based 决策升级为 RL trained policy；schema 直接沿用 Hermes 的 trigger / action / validation / avoid 4 字段
- **agent-memory-cascading-update**：揭示当前 memory 系统 3% / 1% 级联更新准确率——本项目两层架构（[[memory-architecture-for-ops]]）把级联范围限制在 service 内部是缓解方向之一，但**本项目 Phase 1 不直接解决级联更新**（留 Phase 2）
- **heuristic-learning**：HL 范式 = coding agent 维护 software system 的 update mechanism——本项目的"RL trained memory policy"是 HL 范式中"更新机制"的一种具体实现（用 NN policy 代替 coding agent 编辑代码这个更新算子）

> **机制层衔接的共同 pattern**：本项目把这些 reference 中识别 / 提出 / 隐含的**机制原则**显式化、可训练化、可归因化。Content 不衔接（每条 reference 的具体内容 / 任务都 domain-bound）。

---

## 11. CV 上的挂法（项目敲定后才上）

```
**Effect-Attributed Procedural Memory Policy with Trajectory-Level RL @ Coding Agent**
| 2026.05 - 进行中 · 开源研究项目

- 基于两层 memory 架构（service/codebase-anchored declarative facts + symptom-anchored
  procedural playbook，从资深 SRE mental model 反推得到）聚焦后者，扩展 OpenClaw harness
  把 ADD/UPDATE/DELETE/NONE 决策建模为 RL action。
- 引入轨迹级延迟 reward + memory 效果归因机制（logits Δ + GRPO group-wise advantage +
  prioritized counterfactual ablation 三轴），超越 Memory-R1 / Mem-α 的步骤级 reward 局限。
- Procedural playbook 用 execution-executable schema gate（trigger / action / validation /
  avoid），沿用前期 selective-transfer 实验"可执行性 = 跨任务复用边界" 的洞察并精化
  为两种 executability。
- 三层投影报告：in-distribution / OOD-controlled / real-world projection（OpenClaw GitHub
  issues 真实失败轨迹），不假设完美实验环境。
```

**等到 Phase 1 Week 4 SFT checkpoint 出且 logits Δ measurement pipeline 可用时**，CV 上挂"进行中"。

> **挂 CV 的版本和上面 D1-D10 的内部论证版本不同**：CV bullet 是 30 秒 elevator pitch（强调"做了什么 + contribution"）；内部论证是 PEP 风格（强调"为什么 + trade-off + 保底"）。两者不冲突，受众不同。

---

## Appendix · 你最关心的点的对应章节

| 你的关注 | 对应章节 |
|---|---|
| 形态不重要、可执行性重要 | D5 |
| 回写时机 | D2 (trajectory-level) + D3 (effect-triggered via GRPO group-wise) |
| memory 效果定义和测量 | D3 + D9 + D10 |
| 受控 vs 真实场景 | D7 + D10 + 风险 R3/R9 |
| 杂乱无标记轨迹 | Open Question §9 |
| 不能假设完美实验环境 | D7 + D10 + 三层投影报告 |
| SFT + RL 必须用 | D1 + D2 + D4 + D9 |
| Claude Code / Hermes / OpenClaw 源码理解 | D6 + 前置依赖 `PROBLEMS/agent-memory-architecture/` |
| 数据飞轮 | D4 (SFT 弱监督 = 飞轮起点) + Open Question §9 (Phase 2 闭环) |
| 后果回写 (conversation_01) | D2 + §10 (与 conversation_01 衔接) |
