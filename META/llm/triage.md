# INBOX Triage Rules

> **Stage-0 入口**：LLM 启动后必读。
>
> 只有这个文件 + `META/REGISTRY.md` 是 stage-0 必读。其它规则文件按下方"分阶段加载"在需要时读。

---

## Stage 0：启动必读

读完本文件 + `META/REGISTRY.md`，你就有了：

- INBOX 处理流程
- 决策树（看到什么类型的内容做什么）
- Triage Report 输出格式
- 已有内容索引

如果只是回答 "现在仓库里有什么" 或 "我能不能跑 triage" 这种问题，stage 0 够了。**真要建/改文件再读后续 stage**。不要一次性全读——读了用不上的规则会反过来污染输出。

---

## 两条入口，都受同一套纪律

本仓库有两条工作入口，规则对两条都生效：

1. **INBOX triage**（本文件其余部分）：整理 INBOX → 派生 artifact。
2. **直接设计 / 项目 session**：用户直接让你读某个 `PROJECTS/*` 或 `WORK/*` 文件并就地修改（设计文档、design commitment、项目复盘）。**不经 INBOX，但同样受 ownership、分层、REGISTRY 同步约束。** 设计 session 的标准路由（methodology → pattern → DC）见根 `README.md`「工作流 B」。

无论走哪条，**session 收尾前必须跑自审脚本**：

```bash
bash TOOL/script/self_audit.sh
```

它自动核 6 项：A 节点计数(REGISTRY 单源) · B 节点自含 · C meta.yaml 卫生 · D WORK↔PROJECT 边界 · E ownership 单源 · F README 无硬编计数。**有 FAIL 必须修掉再收尾**；WARN 评估后处理。用法 / 何时跑见脚本头注释。

脚本查不到的（属行为意图，靠你把关）：

- 守 ownership matrix（权威定义见 `META/llm/CONTEXT.md` §1）：没写 META / 用户私有 surface。
- 本次新建 / 改动的 artifact 已同步进 `META/REGISTRY.md`。

### WORK ↔ PROJECT 硬边界（不可违反，self_audit D 会扫）

- **`WORK/` 整层（runbooks / design-commitment-patterns / playbooks）是跨项目可复用资产**：只写通用症状 / 不变量 / SOP，**零项目事实**——不把公司名、产品名、具体场景、占位数值当内容写进去。可用 `[[link]]` 引用来源项目做 provenance（WORK→PROJECTS 允许），但不嵌其具体事实。
- 项目具体的场景、naive 反例、采纳决策、占位值，**只写进 `PROJECTS/<project>/`**（通常是 `design/commitments.md`）。
- **即使标注「示例」，也不得把项目场景写进通用 pattern。**
- 新增项目时，把它的专有名补进 `TOOL/script/self_audit.sh` 的 `PROJECT_TERMS`，D 检查才覆盖它。

---

## 分阶段加载

按触发条件读对应文件：

| Stage | 触发条件 | 必读文件 |
|---|---|---|
| **1. 写/改 KNOWLEDGE 节点** | 决策树判定要建/改 KNOWLEDGE 节点 | `META/llm/CONTEXT.md` · `META/policies/node_form.md` · `META/llm/few_shots/node_form.example.md` |
| **2. 写/改 self-check deck** | 新建节点或节点形态大改后，更新 `KNOWLEDGE/_self_check/<domain>.md` | `META/policies/self_check.md` · `META/templates/self_check.template.md` |
| **3. 写播客脚本** | 用户明确请求 "做成播客脚本" / "我还没学 X 给我讲一遍" | `META/policies/podcast_script.md` · `META/llm/few_shots/podcast_script.example.md` |
| **4. 检测到横向对比 N 方案** | 内容出现 vs / trade-off / 几种方案 | `META/templates/problem_README.template.md` |
| **5. 处理面经 / 项目复盘** | INBOX 出现面经文件 / 实习经历对话 | `CAREER/README.md` + 相关模板 |
| **6. 节点粒度纠结** | 不确定该建独立节点还是并入 | `META/policies/node_granularity.md` |
| **7. 命名纠结** | 不确定 slug / 路径 | `META/policies/naming_convention.md` |
| **8. Source of truth 冲突** | 多处描述不一致 | `META/policies/source_of_truth.md` |
| **9. 写/改 WORK runbook** | 新建/大改 KNOWLEDGE 节点后，出现可操作的工程症状；或 INBOX 是真实 debug 经验 | `WORK/README.md` · `WORK/runbooks/<domain>/README.md` · `META/templates/runbook_entry.template.md` |
| **10. 写/改 design commitment pattern** | runbook 症状簇暴露出可复用结构性不变量 | `WORK/README.md` · `WORK/design-commitment-patterns/README.md` · `META/templates/design_commitment_pattern.template.md` |
| **11. 写/改项目 design commitment** | 用户确认某个项目要采纳 / 起草一条设计承诺 | `META/templates/design_commitment.template.md` · 目标项目 README / design 文档 · 相关 pattern / runbook / KNOWLEDGE 源 |

---

## INBOX 文件夹约定

```
INBOX/<topic>/
├── dialogue_logs/    ← ✅ KNOWLEDGE 入库源（用户和 LLM 对话学习的 log）
├── internalized/     ← ✅ KNOWLEDGE 入库源（用户从视频 / 播客 / 资料主动消化过的内容）
├── notes/            ← ⚠️ 参考材料。可读，不入库
├── notes_zh/, ppts/, tutorials/ ← 同上
└── *.pdf / 杂物      ← 看内容判断（论文 → RAW_SOURCES）
```

**关键约束**：

- ✅ 只有 `dialogue_logs/` 和 `internalized/` 能产出 KNOWLEDGE 节点
- ❌ 不要从 `notes/`、`ppts/`、`tutorials/` 提取知识入 KNOWLEDGE
- ❌ KNOWLEDGE 节点 / `meta.yaml` **不能引用 INBOX 路径**——INBOX 是临时 scratch，用户随时可删，artifact 必须自含

`dialogue_logs/` 和 `internalized/` 的差异是来源不同（对话 vs 自学消化），但 KNOWLEDGE 入库待遇相同。

---

## 流程

```
1. 读 META/REGISTRY.md         了解已有内容
2. 扫 INBOX/                   识别每个文件的类型
3. 按决策树分类
4. 按需加载 stage（见上）       再做整理；落笔前读目标层 README / template / 示例
5. 创建 / 更新目标文件          仅在写入区内
6. 更新 META/REGISTRY.md
7. 标记已处理 INBOX 项目        文件顶加 <!-- PROCESSED: YYYY-MM-DD -->（用户可能直接删，标记是 courtesy）
8. 输出 Triage Report
```

---

## 落笔前示例加载

确定要写入某一层时，不要只读抽象规则。先读：

1. 目标层 README（这一层从哪里长出来、服务哪个工作时刻）
2. 对应 template / policy
3. 同层 1-2 个已有示例（如果存在）

然后在动笔前明确一句内部判断：

```text
这个文件从哪里长出来？它服务哪个触发时刻？它的密度应该留在哪一层？
```

例：写 `WORK/runbooks/agent/` 时，先读 `WORK/README.md`、`WORK/runbooks/agent/README.md`、`META/templates/runbook_entry.template.md`，再看已有 P 条目。确认它是从 KNOWLEDGE 节点或真实 debug 经验纵向投影出的症状条目；机制密度留在 KNOWLEDGE，runbook 只放动作与回链。

---

## 分类决策树

```
INBOX 项目是...

├── dialogue_logs/*.md / internalized/*.md
│   → 加载 stage 1 → 提炼 KNOWLEDGE 节点
│   → 节点写完后加载 stage 2 → 更新对应 _self_check/<domain>.md
│   → 若节点含可操作工程症状 → 加载 stage 9，检查是否投影到 WORK/runbooks
│   → 若 runbook 投影暴露结构性不变量 → 加载 stage 10，沉淀 WORK/design-commitment-patterns
│   → 检测是否有 "横向对比 N 方案" → 加载 stage 4 触发 PROBLEMS 建议
│   → 检测是否项目复盘 → 触发 PROJECTS 建议
│
├── 论文 / 完整文档（PDF / 长 .md）
│   → RAW_SOURCES/<type>/<slug>/（建条目，保留 URL + 元信息）
│   → 不直接生成 KNOWLEDGE 节点
│
├── 外部 repo URL / 实验代码
│   → REPRO_INDEX/ 加条目
│
├── 课件 / 笔记 / cheat sheet / tutorial
│   → 留在 INBOX 不动。Triage Report 提一句 "这些是参考材料，未入库"
│
├── 用户讨论实习经历的 dialogue log
│   → PROJECTS/work/{company}-{project}/
│
└── 太碎片 / 无法归类
    → 保留在 INBOX，加 <!-- PENDING: 待补充 -->
```

---

## 创建 KNOWLEDGE 节点的硬规则（速查）

> 详细规则在 stage 1 的 `META/policies/node_form.md` + few-shot example。

1. **形态**：因果叙述 + 反事实推导，不是 bullet 摘要
2. **稀疏 > 饱满**：只写来源材料实际推导/澄清/纠正过的内容
3. **节点是自含 artifact**：不引用 INBOX 路径
4. **自检题不放节点内**：移到 `KNOWLEDGE/_self_check/<domain>.md`，详见 stage 2
5. **不动用户私有 surface**：详见 stage 1 的 CONTEXT.md ownership

## 更新已有节点

- 增量添加，不重写
- paper claim 与个人判断分开：前者进主体，后者进 `thoughts/`
- 冲突显式暴露：与已有节点冲突 → 在 Open Questions 暴露，不静默覆盖
- 更新 `meta.yaml` 的 `last_reviewed_at`

---

## KNOWLEDGE → runbook 投影

runbook 是从 KNOWLEDGE 节点或真实 debug 经验长出来的**症状索引**，不是节点摘要。只有当材料能回答"读者看到什么现象、下一步做什么"时才投影。

投影流程：

1. 读 `WORK/README.md`、对应 domain runbook README、`META/templates/runbook_entry.template.md`。
2. 查现有 runbook 症状索引。去重 key 是**症状**，不是来源节点。
3. 已有症状命中：
   - `remedy-menu`：新增方案后重排"当前方案"，按期望解决成本排序。
   - `diagnostic-procedure`：新增关卡后插入正确拓扑位置。
   - 历史变化写入"演进日志"，不要把历史方案堆进当前方案。
4. 没有症状命中：新建 P-XXX，编号全局递增。
5. 外部 claim 默认验证状态为"未验证"；只有本地实操后才能改为部分验证 / 已验证。

runbook 条目必须薄：机制密度留在 KNOWLEDGE；runbook 只放症状、最小定位因果、当前动作、适用边界、源和回链。

### runbook → design commitment pattern

新建或大改 KNOWLEDGE 节点后，检查是否有可操作工程症状能投影到 `WORK/runbooks/`。对每条投影下来的修法，先判定它是：

- **运行时恢复 / 一段过程**：症状仍发生，事后补救或定位。例如 rescue parse、注入工具列表、重试纠正、后端 ablation。它留在 runbook。
- **结构性不变量**：让该类症状，或它的有害后果，从设计上不可能发生。例如 dispatcher 在前置未满足时拒绝执行终端工具。它才是候选 design commitment pattern。

同一条 runbook 里可能两者并存：只把不变量当候选，过程留 runbook。节点的 thesis（"为什么"）不作为候选，因为它不可校验，留在 KNOWLEDGE。

仅当**同一条结构性不变量同时使多个症状不可能发生**时，加载 stage 10，创建 / 更新 `WORK/design-commitment-patterns/*`。pattern 必须附：它消除哪簇 / 实例化时可执行校验是什么 / 代价与范围 / 前沿问题。不要创建 `WORK/design-commitments/*`。

项目采纳是下一步：只有用户确认某个项目要采用 pattern 时，才加载 stage 11，落到项目仓库或 `PROJECTS/<project>/design/commitments.md`。

---

## 跨层联动检测（Triage Report 的输入）

整理过程中持续记录这 4 类信号：

### 1. TRACKS 进度建议
对于本次新建/更新的 KNOWLEDGE 节点，扫 `TRACKS/active/*` 和 `TRACKS/roadmap/*`，找出可能被本次入库覆盖的 checkbox，列入 Report。**不要自己勾**。

### 2. 实习挖掘 nudge
检查 `PROJECTS/work/` 是否有 README 已列但还没建项目页的实习。如果距上次提醒已过一段时间或本次 INBOX 涉及相关技术，提醒用户开对话挖掘。

### 3. 横向对比触发
检测本次内容是否包含 N 个方案的横向对比（关键词：vs、比较、trade-off、几种方案、A 还是 B）。如有，加载 stage 4，建议建对应 `PROBLEMS/x` 页。

### 4. runbook / pattern / project commitment 联动
新建或大改 KNOWLEDGE 节点后，检查是否有可操作工程症状能投影到 WORK/runbooks/。
对每条投影下来的修法，先判定它是：
  (a) 运行时恢复 / 一段过程（症状仍发生、事后补救）→ 留在 runbook；
  (b) 结构性不变量（让该类症状或其有害后果从设计上不可能发生）→ 候选 design commitment pattern。
注意：同一条目里可能 (a)(b) 并存——只把其中的不变量当候选，过程留 runbook。
仅当【同一条结构性不变量同时使多个症状不可能发生】时，加载 stage 10，创建 / 更新
WORK/design-commitment-patterns/*，并在 Report 里说明它如何实例化成项目 DC：
它消除哪簇 / 实例化校验是什么 / 代价·范围 / 前沿问题。
项目采纳等待用户确认，不自动创建。节点的 thesis（"为什么"）不作为候选——它不可校验，留在节点。

---

## Triage Report 模板

```markdown
# Triage Report — {YYYY-MM-DD HH:MM}

## ✅ 已建 / 已改

### 新建
- `KNOWLEDGE/<domain>/<node>/` — 形态：因果叙述；覆盖范围：...

### 更新
- `KNOWLEDGE/_self_check/<domain>.md` — 加 N 题
- `META/REGISTRY.md` — 同步

### 留在 INBOX 不动（参考材料）
- `INBOX/<topic>/notes/...` 等

---

## 🔔 建议你执行（4 类联动）

### 1. 建议勾 TRACKS
- ...

### 2. 实习挖掘 nudge
- ...

### 3. 横向对比触发
- ...

### 4. runbook / pattern / project commitment 联动
- ...

---

## ⚠️ 冲突 / 待确认

- ...

---

## 📊 本次整理统计

- 新建节点：N 个
- 更新节点：M 个
- 处理 INBOX 文件：K 个
- 留在 INBOX 不动：J 个
```

---

## 标记已处理

每个被处理的 INBOX 文件顶部加：

```
<!-- PROCESSED: YYYY-MM-DD -->
```

参考材料文件（ppts、notes、tutorials）**不加**这个标记。

注：用户可能直接删 INBOX——标记只是 courtesy，artifact 不依赖它存在。

---

## 特殊情况

### 用户编辑了你写过的文件
当作 ground truth，不覆盖。如果与新内容冲突，在 Triage Report "冲突 / 待确认" 段暴露。

### 内容冲突
保留双方观点 + 标 `[待确认]`，让用户决定。

### dialogue log / internalized 太短或没有实质内容
不建节点。在 Report 中说明 "INBOX/.../x.md 内容不足以建节点，建议补充对话后再处理"。

### 用户标注 `[未来再处理]` 的 INBOX 项
跳过。

### 不确定是否该建独立节点
加载 stage 6 看粒度规则。不确定就先并入相关节点，等内容积累再拆。
