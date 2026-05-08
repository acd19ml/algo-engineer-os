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

---

## INBOX 文件夹约定

```
INBOX/<topic>/
├── dialogue_logs/    ← ✅ KNOWLEDGE 入库源（用户和 LLM 对话学习的 log）
├── internalized/     ← ✅ KNOWLEDGE 入库源（用户从视频 / 播客 / 资料主动消化过的内容）
├── notes/            ← ⚠️ 参考材料。可读，不入库
├── notes_zh/, ppts/, tutorials/ ← 同上
└── *.pdf / 杂物      ← 看内容判断（论文 → RAW_SOURCES，面经 → CAREER/interview-bank/）
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
4. 按需加载 stage（见上）       再做整理
5. 创建 / 更新目标文件          仅在写入区内
6. 更新 META/REGISTRY.md
7. 标记已处理 INBOX 项目        文件顶加 <!-- PROCESSED: YYYY-MM-DD -->（用户可能直接删，标记是 courtesy）
8. 输出 Triage Report
```

---

## 分类决策树

```
INBOX 项目是...

├── dialogue_logs/*.md / internalized/*.md
│   → 加载 stage 1 → 提炼 KNOWLEDGE 节点
│   → 节点写完后加载 stage 2 → 更新对应 _self_check/<domain>.md
│   → 检测是否有 "横向对比 N 方案" → 加载 stage 4 触发 PROBLEMS 建议
│   → 检测是否项目复盘 → 触发 PROJECTS 建议
│
├── 论文 / 完整文档（PDF / 长 .md）
│   → RAW_SOURCES/<type>/<slug>/（建条目，保留 URL + 元信息）
│   → 不直接生成 KNOWLEDGE 节点
│
├── 面经 / 面试题
│   → 加载 stage 5 → CAREER/interview-bank/{technical,behavioral}/
│   → 链回 KNOWLEDGE 节点（如已存在）；不存在则在题目里标 [未学]
│
├── 外部 repo URL / 实验代码
│   → REPRO_INDEX/ 加条目
│
├── 课件 / 笔记 / cheat sheet / tutorial
│   → 留在 INBOX 不动。Triage Report 提一句 "这些是参考材料，未入库"
│
├── 用户讨论目标岗位 / JD 的 dialogue log
│   → CAREER/target-roles/{role}.md
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

## 跨层联动检测（Triage Report 的输入）

整理过程中持续记录这 4 类信号：

### 1. TRACKS 进度建议
对于本次新建/更新的 KNOWLEDGE 节点，扫 `TRACKS/active/*` 和 `TRACKS/roadmap/*`，找出可能被本次入库覆盖的 checkbox，列入 Report。**不要自己勾**。

### 2. skill-gap 更新建议
对照 `CAREER/skill-gap.md`，看本次入库的能力是否能从 gap 移到 "已具备"。给出 diff 形式建议。**不要自己改**。

### 3. 实习挖掘 nudge
检查 `PROJECTS/work/` 是否有 README 已列但还没建项目页的实习。如果距上次提醒已过一段时间或本次 INBOX 涉及相关技术，提醒用户开对话挖掘。

### 4. 横向对比触发
检测本次内容是否包含 N 个方案的横向对比（关键词：vs、比较、trade-off、几种方案、A 还是 B）。如有，加载 stage 4，建议建对应 `PROBLEMS/x` 页。

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

### 2. 建议改 skill-gap
- ...

### 3. 实习挖掘 nudge
- ...

### 4. 横向对比触发
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
