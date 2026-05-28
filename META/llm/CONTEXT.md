# Algo Engineer OS — LLM Maintenance Context

> **Stage-1 必读**（在写/改 KNOWLEDGE 时由 `META/llm/triage.md` 引用过来）。
>
> 这一文件主要给 LLM 看 **ownership matrix**——谁拥有什么、你能不能动。
>
> - 节点形态规则在 `META/policies/node_form.md`
> - INBOX 处理流程在 `META/llm/triage.md`
> - 自检题规则在 `META/policies/self_check.md`
> - 播客脚本规则在 `META/policies/podcast_script.md`

---

## 1. Ownership Matrix（最重要 —— 必须严格遵守）

### 🧑 用户纯私有 surface（你只读，绝不写）

- `INBOX/` 下所有内容
- `TRACKS/active/*` 和 `TRACKS/roadmap/*`（结构 + 勾选都用户来）
- `CAREER/cv.md`
- `CAREER/skill-gap.md`
- `CAREER/target-roles/*.md`（用户填，或对话长出但最终编辑权属于用户）
- `CAREER/applications/` 中的投递状态、联系人、结果等事实字段（以用户确认为准）
- `META/` 下所有规则文件（CONTEXT、policies、templates、triage、few_shots、README）

### 🤖 你的写入区（从对话 log / 用户 drop 的内容触发）

- `KNOWLEDGE/<domain>/<node>/` — 全自动从 `INBOX/<topic>/dialogue_logs/` 或 `internalized/` 长出
- `KNOWLEDGE/_self_check/<domain>.md` — 节点新建/大改后同步更新
- `PROBLEMS/*` — 当 log 出现 "横向对比 N 方案" 时触发
- `PROJECTS/*` — 当 log 是项目复盘 / 实习挖掘 / 论文复现时触发
- `RAW_SOURCES/*` — 当 INBOX 出现论文 / 完整文档时
- `REPRO_INDEX/*` — 当 INBOX 出现外部 repo 信息时
- `CAREER/interview-bank/*` — 用户丢面经到 INBOX，你 triage
- `CAREER/applications/*` — 用户明确请求整理投递工作时，可辅助创建 / 更新投递记录
- `WORK/playbooks/*` — 当用户和你对话明确说 "这个流程要沉淀成 SOP" 时
- `PODCAST/*` — 用户明确请求 "做成播客脚本" 或 "intro 一下未学的 X" 时（**不自动触发**）
- `META/REGISTRY.md` — 每次 triage 后同步

### 🔔 你只建议、用户执行（写进 Triage Report，不直接动文件）

- TRACKS 里 "建议勾掉" 的 checkbox
- `CAREER/skill-gap.md` 的更新建议（diff 形式）
- 实习挖掘 nudge
- 横向对比触发

### 用户编辑 = ground truth

如果用户手动改了你写的文件，下次读时把它当事实，**不要覆盖**。冲突时在 Triage Report 里暴露，让用户决定。

---

## 2. 节点是自含 artifact

`KNOWLEDGE/*` 下任何节点（README、meta.yaml）**不能引用 INBOX 路径**——INBOX 是临时 scratch，用户随时可删。节点必须可以独立存在。

LLM 在 triage 时仍然只从 INBOX 用户参与过的内容（`dialogue_logs/` 或 `internalized/`）提炼，**但这是 process discipline，不在 artifact 中追踪路径**。

---

## 3. 引用方向规则（tracks → knowledge 单向）

| 方向 | 允许 |
|---|---|
| TRACKS → KNOWLEDGE | ✓ tracks 可以写"完成此项对应 KNOWLEDGE/x" |
| **KNOWLEDGE → TRACKS** | ✗ 禁止。knowledge 不感知 tracks 存在 |
| CAREER → KNOWLEDGE | ✓ |
| **KNOWLEDGE → CAREER** | ✗ |
| PROBLEMS ↔ KNOWLEDGE | ✓ 双向 |
| KNOWLEDGE ↔ KNOWLEDGE | ✓ |
| _self_check → KNOWLEDGE | ✓（每题链接到节点）|
| **KNOWLEDGE → _self_check** | ✗ 禁止 |
| PODCAST → KNOWLEDGE | ✓（review 型 mirror）|
| **KNOWLEDGE → PODCAST** | ✗ |

理由：稳定层（KNOWLEDGE）不依赖不稳定层（TRACKS / CAREER / PODCAST / _self_check）。

---

## 4. Source of Truth 优先级

冲突时按此判断：

1. `INBOX/<topic>/dialogue_logs/` 和 `internalized/` —— 用户实际学习痕迹（**临时层，可删**）
2. `RAW_SOURCES/` —— 原始证据
3. `KNOWLEDGE/*/meta.yaml` —— 结构关系
4. `KNOWLEDGE/*/README.md` —— 节点解释
5. `PROBLEMS/` —— 问题框架
6. 派生层（CAREER stories、WORK playbooks、PODCAST reviews、_self_check）

不能发明 INBOX / RAW_SOURCES 中不存在的事实。不确定标 `[待确认]`。

详细规则：`META/policies/source_of_truth.md`。

---

## 5. 你的角色边界

### 允许做

- 把 INBOX 内容整理到正确目录（在你的写入区内）
- 创建 / 更新 KNOWLEDGE 节点（按 `META/policies/node_form.md` + few-shot）
- 起草 PROBLEMS / PROJECTS 页（按触发条件）
- 暴露 open questions（按 node_form 规则——必须从正文自然引出）
- 更新 `_self_check/<domain>.md`（按 `META/policies/self_check.md`）
- 写 PODCAST 脚本（仅当用户请求）
- 在 Triage Report 里给用户建议
- 同步 `META/REGISTRY.md`

### 禁止做

- 写入用户私有 surface（看 §1）
- **在 KNOWLEDGE artifact 里引用 INBOX 路径**（看 §2）
- 发明 INBOX / RAW_SOURCES 中不存在的事实
- 拍脑袋生成自检题或面试题
- 自动勾掉 TRACKS 的 checkbox
- 自动改 `CAREER/skill-gap.md`
- 自动建 PODCAST 脚本（必须用户明确请求）
- 删除已有内容（除非用户明确要求）
- 跳过 REGISTRY 更新

---

## 6. 节点结构

最小：

```
KNOWLEDGE/{domain}/{node}/
├── README.md     按 META/policies/node_form.md
└── meta.yaml     结构化关系
```

按需扩展（**有内容才建**）：`math/`、`code/`、`refs/`、`thoughts/` 各自的 README.md。

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

evidence_level:
  concept: paper_claim | verified | self_reasoned | unverified
  math: verified | partially_verified | not_verified
  code: verified | partially_verified | not_verified

checklist:
  concept: false
  math: false
  code: false
  reproduction: false
```

注意：

- 不再有 `source_dialogue_logs` 字段（节点是自含 artifact，不引用 INBOX）
- 不再有 `self_check_questions` checklist 项（自检题在 `_self_check/`，不属于节点完成度）

---

## 7. 命名

- 目录 / 文件：lowercase kebab-case
- 节点：canonical 领域术语（`kv-cache`、`rope`、`rag`）
- 问题页：问题空间名（`long-context-degradation`），不是方法名
- 项目：反映目标（`qiniu-supervisor-agent`）

详细规则：`META/policies/naming_convention.md`。

---

## 8. 编辑规则

1. 先查 `META/REGISTRY.md` —— 不重复创建
2. 尊重 ownership matrix —— 不写用户私有 surface
3. 增量编辑 > 重写 —— 更新已有页面优先
4. 事实与判断分离 —— paper claim 进主体，个人判断进 `thoughts/`
5. 保持不确定性可见 —— `[待确认]` 不要删
6. 不创建空壳
7. 每次编辑后更新 REGISTRY
8. 整理结束输出 Triage Report

---

## 9. 审查清单

每次整理完自查：

- [ ] 内容放对层了？
- [ ] **没在 KNOWLEDGE artifact 里引用 INBOX 路径？**
- [ ] 引用方向合规（tracks → knowledge 单向）？
- [ ] 节点形态是因果叙述，不是 bullet 摘要？（详见 `META/policies/node_form.md`）
- [ ] 节点稀疏度合理（没"为完整性"补内容）？
- [ ] 节点内**没有**自检题（移到 `_self_check/`）？
- [ ] 节点内**没有**"来源" section（在 meta.yaml）？
- [ ] Open Questions 从正文自然引出、可行动、高质量？
- [ ] 没发明 INBOX 中不存在的事实？
- [ ] REGISTRY 已更新？
- [ ] Triage Report 输出了 4 类联动建议？
