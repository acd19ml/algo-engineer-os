# PROJECTS / work

工作类项目（实习 + 全职）的复盘页。

## 已完成

- ✅ `qiniu-zeroops-rca-agent/` — 七牛云 ZeroOps 1024 实训营：组长 + Dify L1/L2/L3 多智能体根因分析下钻模块 + 架构设计 6 步法实操。**MVP / Mock 阶段未上线**，获七牛云第三届 1024 创作节优胜奖。**4 份文档完整**（README + system-anatomy + agent-subsystem + interview-defense-matrix）

## 挖掘中（⏳ in-progress）

- ⏳ `neo-official-support-agent/` — Neo 官网智能客服：2025.02-2025.07 一人负责产品方案，从“官网无独立客服、依赖 Discord 社区和全球开发者维护”的业务问题出发，收敛为官网安全支持入口：官方资源导航、Neo N3 / Neo X 只读链上诊断、安全拦截和人工升级摘要。当前已按目录分层：根入口 `README.md` + `meta.yaml`，`docs/` 放 PRD / 技术提案 / 架构 / 实现 / 运维 / 设计承诺，`eval/` 放 100 cases / fixtures / runner spec，`prototype/` 承接未来可运行代码，`interview/` 放面试派生表达。

## 当前待挖掘

（暂无——所有实习项目已起手）

## 怎么挖掘

1. 开 Claude session，说"我想挖掘 X 实习"
2. 顺序对话：项目背景 → 你的具体职责 → 关键技术决策 → 遇到了什么问题 → 怎么解的 → 量化结果 → 如果重做你会怎么改
3. 对话存到对应的 INBOX dialogue_logs 目录
4. LLM triage：建 `PROJECTS/work/{公司}-{项目}/` 项目页 + 提炼可复用 SOP 到 `WORK/playbooks/` + 提炼面试材料到项目本地 `interview-defense-matrix.md`

## 项目页结构

参考 `META/templates/project_README.template.md`。`type: work`。

## 命名

`{公司}-{核心项目}/`（如 `qiniu-zeroops-rca-agent/`）。一个公司有多个独立项目就拆成多个目录。
