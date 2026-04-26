# PROJECTS / work

工作类项目（实习 + 全职）的复盘页。

## 当前待挖掘（LLM 在 Triage Report 里会主动 nudge 你）

- [ ] `qiniu-supervisor-agent/` — 七牛云：Supervisor-Sub Agents 架构、RocketMQ 异步事件驱动、协调 6 人推进上线
- [ ] `neo-deepresearch-and-react-agent/` — Neo：DeepResearch 多智能体工作流、ReAct 区块链问答系统、3072 维向量 62 工具的语义路由

> 这些项目目前只在 `CAREER/cv.md` 的 bullet 里有。需要扩展成完整复盘页（背景 / 决策 / 问题 / 解法 / 结果 / 复盘）。

## 怎么挖掘

1. 开 Claude session，说"我想挖掘 X 实习"
2. 顺序对话：项目背景 → 你的具体职责 → 关键技术决策 → 遇到了什么问题 → 怎么解的 → 量化结果 → 如果重做你会怎么改
3. 对话存到 `INBOX/internships/qiniu/dialogue_logs/{date}.md`（或 neo/）
4. LLM triage：建 `PROJECTS/work/qiniu-supervisor-agent/` 项目页 + 提炼可复用 SOP 到 `WORK/playbooks/` + 提炼面试故事到 `CAREER/interview-bank/behavioral/`

## 项目页结构

参考 `META/templates/project_README.template.md`。`type: work`。

## 命名

`{公司}-{核心项目}/`（如 `qiniu-supervisor-agent/`）。一个公司有多个独立项目就拆成多个目录。
