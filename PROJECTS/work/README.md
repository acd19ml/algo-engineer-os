# PROJECTS / work

工作类项目（实习 + 全职）的复盘页。

## 已完成

- ✅ `qiniu-zeroops-rca-agent/` — 七牛云 ZeroOps 1024 实训营：组长 + Dify L1/L2/L3 多智能体根因分析下钻模块 + 架构设计 6 步法实操。**MVP / Mock 阶段未上线**，获七牛云第三届 1024 创作节优胜奖。**4 份文档完整**（README + system-anatomy + agent-subsystem + interview-defense-matrix）

## 挖掘中（⏳ in-progress）

- ⏳ `neo-deepresearch-and-react-agent/` — Neo 智能经济 4 子项目（DeepResearch / ReAct + 语义路由 / 开源 SDK / 子账户系统）。**起手骨架已建**（README + interview-defense-matrix），含 20 题挖掘 brief；`system-anatomy.md` 和 `subsystem-react-router.md` 等 brief 答完后 evolve

## 当前待挖掘

（暂无——所有实习项目已起手）

## 怎么挖掘

1. 开 Claude session，说"我想挖掘 X 实习"
2. 顺序对话：项目背景 → 你的具体职责 → 关键技术决策 → 遇到了什么问题 → 怎么解的 → 量化结果 → 如果重做你会怎么改
3. 对话存到对应的 INBOX dialogue_logs 目录
4. LLM triage：建 `PROJECTS/work/{公司}-{项目}/` 项目页 + 提炼可复用 SOP 到 `WORK/playbooks/` + 提炼面试故事到 `CAREER/interview-bank/behavioral/`

## 项目页结构

参考 `META/templates/project_README.template.md`。`type: work`。

## 命名

`{公司}-{核心项目}/`（如 `qiniu-zeroops-rca-agent/`）。一个公司有多个独立项目就拆成多个目录。
