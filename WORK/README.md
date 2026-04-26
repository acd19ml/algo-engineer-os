# WORK

可复用工程实践层。**未来层** —— 等 `PROJECTS/work/<实习>/` 复盘做完后，从中提炼出的可复用 SOP / playbook 才放这里。

## 这一层是什么

WORK 不是"工作记录"。"工作记录"是 `PROJECTS/work/<实习>/` 的项目页（背景 / 决策 / 结果 / 复盘）。

WORK 是从那些项目页中**二次提炼**出的"下次再做这类事的可复用资产"：

- `playbooks/` — 可复用 step-by-step 执行指南（如：怎么排查 supervisor agent 任务超时）
- `incident-notes/` — 失败案例 + postmortem
- `design-notes/` — 偏工作面的技术设计（如：消息队列异步化的设计选型笔记）
- `templates/` — 沟通模板（status update / postmortem / design review）

## 当前状态

空。**这是预期的**。等你把 `PROJECTS/work/qiniu-supervisor-agent/` 和 `PROJECTS/work/neo-deepresearch-and-react-agent/` 挖出来后，自然会有 SOP 沉到这里。

## 不要做的事

- 不要现在就建空的 `playbooks/` 子目录占位
- 不要把项目页内容直接搬过来——这层是**提炼**，不是搬运
- 不要让 LLM 主动建 SOP——只在你和 LLM 对话时明确说"这个流程下次还会做，提炼成 SOP"才建

## 引用关系

| 方向 | 允许 |
|---|---|
| WORK → KNOWLEDGE | ✓ playbook 引用相关节点 |
| WORK → PROJECTS | ✓ 提炼来源 |
| PROJECTS → WORK | ✓ 项目页可以写"沉淀出 X playbook" |
