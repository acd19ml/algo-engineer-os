# Algo Engineer OS — LLM Maintenance Context

你正在维护一个算法工程师的个人知识库。用户不直接维护知识库结构，而是把学习痕迹丢进 INBOX，由你整理到正确位置。

**读完本文件后，再读这两个：**
1. `META/REGISTRY.md` — 当前已有什么
2. `META/llm/triage.md` — INBOX 处理流程 + Triage Report 模板

---

## 1. Ownership Matrix（最重要 —— 必须严格遵守）

### 🧑 用户纯私有 surface（你只读，绝不写）

- `INBOX/` 下所有内容
- `TRACKS/active/*` 和 `TRACKS/roadmap/*`（结构 + 勾选都用户来）
- `CAREER/cv.md`
- `CAREER/skill-gap.md`
- `CAREER/target-roles/*.md`（用户填，或他和你对话后从 dialogue_log 走 triage 长出来——但**最终编辑权属于用户**）
- `META/` 下所有规则文件（CONTEXT、policies、templates、triage、README）

### 🤖 你的写入区（从对话 log / 用户 drop 的内容触发）

- `KNOWLEDGE/*` — 全自动从 `INBOX/<topic>/dialogue_logs/*.md` 长出
- `PROBLEMS/*` — 当 log 出现"横向对比 N 方案"时触发
- `PROJECTS/*` — 当 log 是项目复盘 / 实习挖掘 / 论文复现时触发
- `RAW_SOURCES/*` — 当 INBOX 出现论文 / 完整文档时
- `REPRO_INDEX/*` — 当 INBOX 出现外部 repo 信息时
- `CAREER/interview-bank/*` — 用户丢面经到 INBOX，你 triage
- `WORK/playbooks/*` 等 — 当用户和你对话明确说"这个流程要沉淀成 SOP"时
- `META/REGISTRY.md` — 每次 triage 后同步

### 🔔 你只建议、用户执行（写进 Triage Report，不直接动文件）

- TRACKS 里"建议勾掉"的 checkbox
- `CAREER/skill-gap.md` 的更新建议（diff 形式）
- 实习挖掘 nudge（"PROJECTS/work/qiniu-... 还没建，要不要开对话挖掘？"）
- 横向对比触发（"本次 log 出现 N 方案对比，建议建 PROBLEMS/x 页"）

### 用户编辑 = ground truth

如果用户手动改了你写的文件，下次读时把它当作事实，**不要覆盖**。如果你的整理结果和用户编辑冲突，在 Triage Report 里指出冲突，让用户决定。

---

## 2. 入库源唯一规则

**`INBOX/<topic>/dialogue_logs/*.md` 是唯一的知识入库源**。

- 课件（`ppts/`）、笔记（`notes/`、`notes_zh/`）、tutorial（`tutorials/`）、cheat sheet 等都是**参考材料**。你可以读它们做事实核对，**但不从这里提取知识入 KNOWLEDGE**。
- 论文 / 完整文档可能 triage 到 `RAW_SOURCES/`，但即使如此，KNOWLEDGE 节点也只能从对话 log 长出来，不能从 RAW_SOURCES 直接生成。
- 例外：用户丢面经到 INBOX → 进 `CAREER/interview-bank/`（这是用户的真实输入，不是参考材料）

理由：用户哲学是"学习的痕迹是和 LLM 的对话过程，不是 LLM 给的整理成品"。看了/抄了 ≠ 学会了。

---

## 3. 节点稀疏度规则

**节点宁稀疏不饱满**：

- KNOWLEDGE 节点只写对话 log 实际覆盖到的部分
- 论文 / 课件里写但用户没在对话里推导/纠正/澄清过的内容 ≠ 用户学过，**不要补全**
- 如果对话 log 只覆盖了 self-attention 的 QKV 计算但没涉及 multi-head，节点里就只写 QKV，不要"为完整性"补 multi-head
- 节点的状态可以反映稀疏度（status: learning，checklist 大多数 false）

不要用 README 模板的 section 数量作为强制目标。section 没内容就删掉，不要凑。

---

## 4. 自检题来源限定

KNOWLEDGE 节点的"自检问题" section 来源**严格限定**：

- ✅ 对话 log 中用户**实际卡住**的位置（用户问了 2 次以上、被纠正过、要求复述过）
- ✅ 用户在对话里主动说"这部分我还不熟"的点
- ❌ 你拍脑袋出的"标准考点"
- ❌ 论文 / 课件目录里看起来该问的题

`CAREER/interview-bank/` 同理：题目来源是用户丢进 INBOX 的真实面经，不是你生成。

---

## 5. 引用方向规则（tracks → knowledge 单向）

| 方向 | 允许 |
|---|---|
| TRACKS → KNOWLEDGE | ✓ tracks 可以写"完成此项对应 KNOWLEDGE/x" |
| **KNOWLEDGE → TRACKS** | ✗ 禁止。knowledge 不感知 tracks 存在 |
| CAREER → KNOWLEDGE | ✓ |
| **KNOWLEDGE → CAREER** | ✗ |
| PROBLEMS ↔ KNOWLEDGE | ✓ 双向 |
| KNOWLEDGE ↔ KNOWLEDGE | ✓ |

理由：稳定层（KNOWLEDGE）不依赖不稳定层（TRACKS / CAREER）。tracks 增删改不能污染 knowledge。

---

## 6. Source of Truth 优先级

冲突时按此判断：

1. `RAW_SOURCES/` — 原始证据，最高
2. `INBOX/<topic>/dialogue_logs/` — 用户实际学习痕迹
3. `KNOWLEDGE/*/meta.yaml` — 结构关系
4. `KNOWLEDGE/*/README.md` — 节点解释
5. `PROBLEMS/` — 问题框架
6. 其它派生层（CAREER stories、WORK playbooks 等）

不能发明 INBOX / RAW_SOURCES 中不存在的事实。不确定的内容标 `[待确认]`。

---

## 7. 你的角色边界

### 允许做

- 把 INBOX 内容整理到正确目录（在你的写入区内）
- 创建 / 更新 KNOWLEDGE 节点（按模板 + 稀疏原则）
- 起草 PROBLEMS / PROJECTS 页（按触发条件）
- 暴露 open questions
- 在 Triage Report 里给用户建议
- 同步 `META/REGISTRY.md`

### 禁止做

- 写入用户私有 surface（看 §1）
- 发明 INBOX / RAW_SOURCES 中不存在的事实
- 拍脑袋生成自检题或面试题
- 自动勾掉 TRACKS 的 checkbox
- 自动改 `CAREER/skill-gap.md`
- 删除已有内容（除非用户明确要求）
- 跳过 REGISTRY 更新

---

## 8. 节点结构

最小：

```
KNOWLEDGE/{domain}/{node}/
├── README.md     按 META/templates/node_README.template.md
└── meta.yaml     结构化关系
```

按需扩展（有内容才建）：`math/`、`code/`、`refs/`、`thoughts/` 各自的 README.md。

**不创建空文件。**

### meta.yaml 最小字段

```yaml
id: {node-id}
title: "{Node Title}"
type: concept | method | mechanism | system | capability | tool
status: learning | stable | review | stale
created_at: YYYY-MM-DD
last_reviewed_at: YYYY-MM-DD

tags: []
depends_on: []
related_nodes: []
related_problems: []

source_dialogue_logs:
  - INBOX/.../dialogue_logs/xxx.md   # 必填，节点的真实来源

evidence_level:
  concept: paper_claim | verified | self_reasoned | unverified
  math: verified | partially_verified | not_verified
  code: verified | partially_verified | not_verified

checklist:
  concept: false
  math: false
  code: false
  reproduction: false
  self_check_questions: false
```

---

## 9. 命名

- 目录 / 文件：lowercase kebab-case
- 节点：canonical 领域术语（`kv-cache`、`rope`、`rag`）
- 问题页：问题空间名（`long-context-degradation`），不是方法名
- 项目：反映目标（`qiniu-supervisor-agent`）

详细规则：`META/policies/naming_convention.md`。

---

## 10. 节点粒度

新建前问 4 个问题（`META/policies/node_granularity.md`）：

1. 有稳定独立 identity？
2. 一句话能说清为什么重要？
3. 会被多个项目 / 问题 / track 引用？
4. 有自己的前置依赖、替代方案、下游用途？

3 个"是"才建独立节点。

---

## 11. 编辑规则

1. 先查 `META/REGISTRY.md` —— 不重复创建
2. 尊重 ownership matrix —— 不写用户私有 surface
3. 增量编辑 > 重写 —— 更新已有页面优先
4. 事实与判断分离 —— paper claim 进主体，个人判断进 `thoughts/`
5. 保持不确定性可见 —— `[待确认]` 不要删
6. 不创建空壳
7. 每次编辑后更新 REGISTRY
8. 整理结束输出 Triage Report（格式见 `triage.md`）

---

## 12. 审查清单

每次整理完自查：

- [ ] 内容放对层了？
- [ ] 引用方向合规（tracks → knowledge 单向）？
- [ ] 节点稀疏度合理（没"为完整性"补内容）？
- [ ] 自检题来源是 dialogue_log 中用户卡住/被纠正的位置？
- [ ] 没发明 INBOX 中不存在的事实？
- [ ] REGISTRY 已更新？
- [ ] Triage Report 输出了 4 类联动建议？
