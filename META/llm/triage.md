# INBOX Triage Rules

定义你如何处理 INBOX 内容并输出 Triage Report。

> 前置：先读 `CONTEXT.md`（含 ownership matrix、入库源唯一规则、引用方向、节点稀疏度），再读 `REGISTRY.md`（当前已有什么），再来这里。

---

## 流程

```
1. 读 META/REGISTRY.md         了解已有内容
2. 读 INBOX/                   识别每个文件的类型（dialogue_log / 参考材料 / 论文 / 面经 / repo / ...）
3. 对每个 INBOX 项目分类       按下方决策树
4. 执行整理                    创建 / 更新目标文件（仅在你的写入区，看 CONTEXT §1）
5. 更新 META/REGISTRY.md
6. 标记已处理 INBOX 项目       文件顶加 <!-- PROCESSED: YYYY-MM-DD -->
7. 输出 Triage Report          固定 4 个 section（见末尾模板）
```

---

## INBOX 文件夹约定（强制）

```
INBOX/<topic>/
├── dialogue_logs/        ← ✅ 入库主源。从这里提炼 KNOWLEDGE 节点 + 自检题
├── notes/                ← ⚠️ 参考材料。可读，不入库
├── notes_zh/             ← ⚠️ 同上
├── ppts/                 ← ⚠️ 课件，参考材料
├── tutorials/            ← ⚠️ 教程，参考材料
└── *.pdf / *.md          ← 看内容判断，论文 → RAW_SOURCES，杂物保留
```

**关键约束**：

- ✅ 只有 `dialogue_logs/*.md` 能产出 KNOWLEDGE 节点
- ❌ 不要从 `notes/`、`ppts/`、`tutorials/` 提取知识入 KNOWLEDGE。这些是用户学习辅助材料，"看了 ≠ 学会了"
- ❌ 即使 `notes/` 里有完整的概念解释，也不能据此建节点。节点必须有 `source_dialogue_logs` 字段指向真实对话

---

## 分类决策树

```
INBOX 项目是...

├── 对话 log（dialogue_logs/*.md）
│   → 提炼 KNOWLEDGE 节点（按稀疏原则） + 自检题（来源限定）
│   → 检测是否有"横向对比 N 方案"内容 → 触发 PROBLEMS 建议
│   → 检测是否项目复盘 → 触发 PROJECTS 建议
│
├── 论文 / 完整文档（PDF / 长 .md）
│   → RAW_SOURCES/<type>/<slug>/（建条目，保留 URL + 元信息）
│   → 不直接生成 KNOWLEDGE 节点
│
├── 面经 / 面试题（用户标注 [面经] 或内容明显是题）
│   → CAREER/interview-bank/technical/ 或 behavioral/
│   → 链回相关 KNOWLEDGE 节点（如已存在）；不存在则在题目里标 [未学]
│
├── 外部 repo URL / 实验代码
│   → REPRO_INDEX/ 加条目
│
├── 课件 / 笔记 / cheat sheet / tutorial
│   → 留在 INBOX 不动。Triage Report 提一句"这些是参考材料，未入库"
│
├── 用户讨论目标岗位 / JD / 找工作的对话 log
│   → CAREER/target-roles/{role}.md（如已存在则 update；否则建草稿，注明"待用户审"）
│
├── 用户讨论实习经历的对话 log
│   → PROJECTS/work/{company}-{project}/
│   → 提示用户是否要派生 interview-bank/behavioral/ STAR 故事
│
└── 太碎片 / 无法归类
    → 保留在 INBOX，加 <!-- PENDING: 待补充 --> 标注
```

---

## 创建 KNOWLEDGE 节点的硬规则

1. **来源必填**：`meta.yaml` 的 `source_dialogue_logs` 必须指向具体 `INBOX/.../dialogue_logs/*.md` 路径
2. **稀疏 > 饱满**：只写对话 log 实际覆盖到的部分。论文里有但对话没碰到的内容，**留白** + 在 Open Questions 里标"对话未覆盖"
3. **自检题来源限定**：从对话 log 中用户**卡住 / 问错 / 被纠正 / 被要求复述**的位置提炼。不允许：从课件目录推断、按"标准考点"出题、自己编一个看起来合理的问题
4. **粒度判断**：4 题 3 是才建独立节点（`META/policies/node_granularity.md`）。不够格的内容并入相关节点的 thoughts/ 或 README 补充段
5. **不动用户私有 surface**：不在节点里写 "用于完成 TRACKS/x"。引用方向 tracks → knowledge 单向

---

## 更新已有节点

- 增量添加，不重写
- paper claim 与个人判断分开：前者进主体（标来源），后者进 `thoughts/`
- 冲突显式暴露：新对话 log 与已有节点冲突 → 在 Open Questions 暴露，不静默覆盖
- 更新 `meta.yaml` 的 `last_reviewed_at`

---

## 跨层联动检测（Triage Report 的输入）

整理过程中持续记录这 4 类信号：

### 1. TRACKS 进度建议
对于本次新建/更新的 KNOWLEDGE 节点，扫描 `TRACKS/active/*` 和 `TRACKS/roadmap/*`，找出可能被本次入库覆盖的 checkbox，列入 Report。**不要自己勾**。

### 2. skill-gap 更新建议
对照 `CAREER/skill-gap.md` 的 Gap 表，看本次入库的能力是否能从 gap 移到"已具备"。给出 diff 形式建议。**不要自己改**。

### 3. 实习挖掘 nudge
检查 `PROJECTS/work/` 是否有 README 已列但还没建项目页的实习（如 `qiniu-supervisor-agent/`、`neo-deepresearch-and-react-agent/`）。如果距上次提醒已过一段时间或本次 INBOX 涉及相关技术，提醒用户开对话挖掘。

### 4. 横向对比触发
检测本次对话 log 是否包含 N 个方案的横向对比（关键词：vs、比较、trade-off、几种方案、A 还是 B）。如有，建议建对应 `PROBLEMS/x` 页。

---

## Triage Report 模板（每次整理结束必须输出）

```markdown
# Triage Report — {YYYY-MM-DD HH:MM}

## ✅ 已建 / 已改

### 新建
- `KNOWLEDGE/llm/x/` — 来源：`INBOX/.../dialogue_logs/y.md`，覆盖范围：...
- ...

### 更新
- `KNOWLEDGE/llm/z/README.md` — 加了 self-check Q3-Q5
- `META/REGISTRY.md` — 同步
- ...

### 留在 INBOX 不动（参考材料）
- `INBOX/CS6487.../ppts/*.pdf` — 参考材料，不入库
- `INBOX/CS6487.../notes/week3.md` — 参考材料，不入库

---

## 🔔 建议你执行（4 类联动）

### 1. 建议勾 TRACKS
- `TRACKS/active/final-exam-prep.md` 的 "Topics in ML > 用对话 log 把每周关键概念问透" — 本次覆盖了 week3 (`KNOWLEDGE/llm/x/`)
- ...

### 2. 建议改 skill-gap
- 把 "长程记忆系统" 从 Gap 移到"已具备"，理由：本次入库 `KNOWLEDGE/llm/long-term-memory/` 已有自检题且你都答出了
- diff:
  ```
  - | 长程记忆系统 | summer-intern-agent | 用过 mem0 未深入 | P1 | ... |
  + （移到"已具备"段）长程记忆系统 — KNOWLEDGE/llm/long-term-memory/
  ```

### 3. 实习挖掘 nudge
- `PROJECTS/work/qiniu-supervisor-agent/` 还没建。本次 log 涉及了 supervisor agent 概念，是开对话挖掘的好时机。建议下次开 session 时说"挖掘七牛云实习"
- `PROJECTS/work/neo-deepresearch-and-react-agent/` 同上

### 4. 横向对比触发
- 本次 log 第 N 段出现了 "RoPE vs ALiBi vs StreamingLLM" 三种方案对比，建议建 `PROBLEMS/long-context-degradation/`
- （如无，写 "本次未检测到横向对比"）

---

## ⚠️ 冲突 / 待确认

- 用户编辑了 `KNOWLEDGE/x/README.md` 的 Open Questions，与本次入库内容冲突。建议你审：...
- 本次 log 第 X 段提到的 "Y 算法复杂度是 O(n)"，但已有节点写的是 O(n log n)。我标了 [待确认]，请确认
- （如无，写 "无冲突"）

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

参考材料文件（ppts、notes、tutorials）**不加**这个标记，因为它们不算"被处理"，只是被读过。

默认行为：加标记，不删除。除非用户明确说"处理完可以删"。

---

## 特殊情况

### 用户编辑了你写过的文件
当作 ground truth，不覆盖。如果与新对话 log 冲突，在 Triage Report "冲突 / 待确认" 段暴露。

### 对话 log 信息冲突
保留双方观点 + 标 `[待确认]`，让用户决定。

### 对话 log 太短或没有实质内容
不建节点。在 Report 中说明 "INBOX/.../x.md 内容不足以建节点，建议补充对话后再处理"。

### 用户标注 `[未来再处理]` 的 INBOX 项
跳过，不处理。

### 你不确定是否该建独立节点
按粒度判断（4 题 3 是）。不确定就**先并入相关节点**，等内容积累再拆。
