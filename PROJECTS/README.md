# PROJECTS

把知识连接到真实执行的层。每个项目 = 有明确边界的 bounded work。

## 子结构

```
PROJECTS/
├── research/       论文复现、技术探索（当前为空）
├── work/           实习 / 全职项目（当前为空，待挖掘 qiniu + neo）
└── side-projects/  自发的小项目（按需建）
```

## 模板

`META/templates/project_README.template.md`。

## 这一层和 LLM 的关系

- **触发**：你和 LLM 对话挖掘某个项目（实习复盘 / 论文复现 / side project）→ 对话 log 进 INBOX → triage 时 LLM 创建项目页
- LLM 写完项目页后会在 Triage Report 提示：是否要继续从这个项目派生出 KNOWLEDGE 节点 / WORK playbook / CAREER stories

## 当前重点

`work/` 下两个待挖掘项目（见 `work/README.md`）。这是接下来准备实习面试最高 ROI 的事。

## 引用关系

| 方向 | 允许 |
|---|---|
| PROJECTS → KNOWLEDGE | ✓ 项目用了哪些节点 |
| PROJECTS → PROBLEMS | ✓ 项目涉及哪些问题 |
| PROJECTS → 项目本地 interview-defense-matrix / interview-answers | ✓ 派生出的故事 |
| PROJECTS → WORK | ✓ 派生出的 playbook |
| KNOWLEDGE → PROJECTS | ✓ 节点可以写"被哪些项目用过" |
