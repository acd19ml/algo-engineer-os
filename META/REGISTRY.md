# Registry

知识库全局索引。LLM 在处理 INBOX 前必须先读，避免重复创建。

> 此文件由 LLM 在每次整理后自动同步。人工也可改。

---

## KNOWLEDGE nodes

| id | 路径 | type | status |
|---|---|---|---|

（暂无节点。Final 结束后从对话 log 长出）

## PROBLEMS

| id | 路径 | status |
|---|---|---|

（暂无。等对话 log 出现"横向对比 N 方案"时由 LLM 触发建议）

## PROJECTS

| id | 路径 | type | status |
|---|---|---|---|

（暂无。`PROJECTS/work/` 下两个待挖掘项目：qiniu-supervisor-agent、neo-deepresearch-and-react-agent）

## RAW_SOURCES

| id | 路径 | type |
|---|---|---|

（暂无）

## CAREER

| 文件 | 作用 | 维护方 |
|---|---|---|
| `CAREER/cv.md` | 简历（过时，待更新） | 你 |
| `CAREER/skill-gap.md` | CV ↔ 目标岗位缺口表 | 你（LLM 建议 diff） |
| `CAREER/target-roles/` | 目标岗位画像（待填：summer-intern-agent-engineer、newgrad-agent-engineer） | 你（或对话长出但你审）|
| `CAREER/interview-bank/technical/` | 技术题（待填：你丢面经触发）| LLM triage |
| `CAREER/interview-bank/behavioral/` | 行为题 + STAR（待填：从 PROJECTS/work 派生）| LLM triage |

## WORK

| 路径 | 状态 |
|---|---|
| `WORK/` | 未来层。等 PROJECTS/work/ 复盘后从中提炼 SOP |

## REPRO_INDEX

（暂无条目。等真有外部 repo 再建）

## TRACKS

| id | 路径 | 类型 | 状态 |
|---|---|---|---|
| final-exam-prep | TRACKS/active/final-exam-prep.md | 临时 | active（4.27 今天 / 4.29 / 5.2）|
| agent-engineer | TRACKS/roadmap/agent-engineer.md | 长期 | **待重写**（等 target-roles 填完）|

---

## Ownership 速查

| 区域 | 维护方 |
|---|---|
| INBOX、TRACKS、CAREER 下用户私有文件、META | 你 |
| KNOWLEDGE、PROBLEMS、PROJECTS、RAW_SOURCES、REPRO_INDEX、CAREER/interview-bank、WORK/playbooks、REGISTRY | LLM 写入 |
| TRACKS 勾选 / skill-gap 更新 / 实习挖掘 / 横向对比 | LLM 在 Triage Report 建议，你执行 |

详见 `README.md` 的 Ownership Matrix。
