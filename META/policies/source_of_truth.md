# Source of Truth Policy

定义这个 repo 的真值优先级。冲突时按此顺序判断谁对。

## 真值优先级

1. `RAW_SOURCES/` — 原始证据
2. `INBOX/<topic>/dialogue_logs/` — 用户实际学习痕迹
3. `KNOWLEDGE/*/meta.yaml` — 结构关系
4. `KNOWLEDGE/*/README.md` — 节点解释
5. `PROBLEMS/` — 问题框架
6. 派生层（`WORK/playbooks/` SOP、项目本地 interview-answers/defense-matrix 等）

## 每层意味着什么

### 1. `RAW_SOURCES/`
首要证据层。论文、文档、官方资料。原文怎么说就是怎么说。

### 2. `INBOX/<topic>/dialogue_logs/`
**这一项是这个系统特有的**。用户的真实学习过程在这里。当 KNOWLEDGE 节点和对话 log 冲突时，对话 log 优先（因为它是节点的实际来源）。

### 3. `KNOWLEDGE/*/meta.yaml`
结构关系层。dependencies、type、relations。如果 README 与 meta.yaml 在结构关系上冲突，以 meta.yaml 为准。

### 4. `KNOWLEDGE/*/README.md`
节点解释层。"这个东西是什么、怎么工作"。

### 5. `PROBLEMS/`
问题 framing 层。"我们在解决什么、有哪些方案"。

### 6. 派生层
`WORK/playbooks/`、项目本地面试材料 等都是从底层提炼出的。它们不是真值来源，是真值的二次表达。

## 冲突处理规则

### Rule 1
如果派生层（CAREER stories / WORK playbooks）与 KNOWLEDGE / RAW_SOURCES 冲突，以底层为准。

### Rule 2
如果 node README 与 meta.yaml 在 dependency 上冲突，以 meta.yaml 为准。

### Rule 3
如果 KNOWLEDGE 节点内容与 INBOX dialogue_logs 冲突，以 dialogue_logs 为准（因为节点是从 log 长出来的）。

### Rule 4
如果用户手动编辑了 LLM 写的文件，编辑内容 = ground truth。LLM 下次读时不要覆盖。

### Rule 5
如果底层本身存在歧义，不要发明确定性。用 `[待确认]` 显式标注。

## 实际含义

- 不能发明 INBOX / RAW_SOURCES 中不存在的事实
- 不确定的内容用 `[待确认]`
- 高层不能静默覆盖低层
- 用户编辑覆盖 LLM 输出
