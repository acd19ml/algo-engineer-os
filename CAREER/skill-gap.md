# Skill Gap

> CV (`CAREER/cv.md`) ↔ 目标岗位 (`CAREER/target-roles/*`) 的差异表。
>
> **维护**：你来编辑。LLM 在 Triage Report 里建议 diff，你判断后手动改。

## 用法

每次 LLM triage 完，看 Triage Report 里的 "skill-gap 建议"，如果同意就改这个文件。

## 现状摘要

基于 `cv.md` 提炼出的核心能力点：

- **Agent 工程**：Multi-Agent (Supervisor + Sub-Agents)、ReAct、RAG、语义路由、工具编排
- **训练原理**：PPO / DPO / GRPO / DAPO / LoRA / QLoRA 演进谱系（KB 撑住）
- **推理优化**：KV Cache 工程理解 + Neo 70% 成本降经验
- **工程基础**：Python + Go、微服务、Gin、gRPC、数据库 + 中间件、TDD
- **领导 + 架构**：组长 + 6 步法 + 三类设计文档
- **开源协作**：Neo 260+ stars + 海外社区运营
- **研究深度**（agent memory）：横向对比 + selective transfer 方法学 + 8 类 boundary pattern

## 目标岗位汇总要求

合并 4 份 target-roles 提炼的共同要求：


| 能力                                  | 来自哪份 JD            |
| ----------------------------------- | ------------------ |
| **Coding Agent / SWE-bench**        | A202665            |
| **MCP servers/tools 实现**            | A202665            |
| **业务归因 + 数据挖掘**                     | 业务 Agent           |
| **AI 编程工具重度玩家（Cursor/Claude Code）** | 业务 Agent           |
| **vLLM / 推理优化部署**                   | A202665 + 业务 Agent |
| **DPO / ORPO / RLHF 工程实战**          | A202665 + 腾讯游戏     |
| **AWQ / GPTQ / GGUF 量化**            | A202665            |
| **观测 / 全链路追踪**                      | 业务 Agent           |
| **NPC / TTS / 数字人**                 | 腾讯游戏（独有）           |


## Gap 表（双层结构）

### 层 1：已有但 cv 没体现 ← 解决方案是改 cv（Week 1 已做）


| 能力                                            | 表现                                                                                                 | 是否已写进新 cv                                                   |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| 组长经验 + 架构 6 步法                                | 七牛云实习内容                                                                                            | ✅ 新 cv 七牛云段已加                                               |
| 三类设计文档思考                                      | `KNOWLEDGE/methodology/three-tier-decision-docs/` + `PROJECTS/work/qiniu-zeroops-rca-agent/` 学术坐标段 | ✅ 新 cv 七牛云段已加                                               |
| Neo 海外社区运营                                    | Neo 实际工作内容                                                                                         | ✅ 新 cv Neo 段已加                                              |
| agent memory 框架对比研究                           | 主项目横向对比                                                                                            | ✅ 主项目"横向对比研究" bullet                                        |
| 7B 模型 LoRA + GRPO 全栈训练经验                      | 主项目（进行中）                                                                                           | ✅ 主项目"全链路实现" bullet                                         |
| selective transfer 方法学（matched/mismatched 配对） | 自主研究（HotpotQA→2WikiMultiHopQA 实验）                                                                  | ✅ **新增"Agent Memory 自主研究项目"栏**（独立成项，不写论文名词）                 |
| boundary pattern 检测 + step-level 分析           | 自主研究（AWM 框架复现审计）                                                                                   | ✅ **新增"Agent Memory 自主研究项目"栏**（6-18% 影响窗口 + 8 类失败模式作为已观察结果） |
| Transformer 八股深度                              | KB 32 节点                                                                                           | ⚠️ cv 技能段加了但深度看不出——靠面试 + 横向对比报告体现                           |


### 层 2：真正的 gap ← 需要补齐


| 能力                                       | 目标岗位需要             | 我现状  | 优先级    | 补齐路径                        |
| ---------------------------------------- | ------------------ | ---- | ------ | --------------------------- |
| **SWE-bench / RepoBench 实战**             | A202665            | 未跑过  | **P0** | 主项目 Week 3-7                |
| **Claude Code / OpenClaw / Hermes 源码理解** | 多个 JD              | 没读过  | **P0** | 横向对比 Week 1-2               |
| **GRPO 工程实战**                            | A202665 + 腾讯       | 仅原理  | **P1** | 主项目 Week 6-7                |
| **vLLM 部署经验**                            | A202665 + 业务 Agent | 仅概念  | **P1** | 主项目 Week 8                  |
| **AWQ / GPTQ / GGUF 量化实战**               | A202665            | 仅概念  | P2     | sprint 不补；面试讲原理             |
| **MCP servers/tools 实现**                 | A202665            | 仅概念  | P2     | sprint 不补；用主项目里类似的工具集成讲     |
| **业务归因 / 数据挖掘**                          | 业务 Agent           | 弱    | P2     | sprint 不补；用 Neo 70% 成本归因当例子 |
| **预训练 / 持续预训练实战**                        | A202665 + 数据预训练    | 仅方法论 | P3     | sprint 不补；KB 已撑住面试问题        |
| **NPC / TTS / 数字人**                      | 腾讯游戏               | 完全没有 | P3     | sprint 不补；不主投腾讯游戏           |
| **顶会论文**                                 | 多个加分项              | 没有   | P4     | 短期不解决；研究项目长期可考虑             |


## 已具备（从 gap 移出来的）

> 当某个 gap 经过学习 / 复盘后变为已具备，从上表移到这里。保留路径以便回顾。

- **Transformer 内部机制（QKV / Multi-Head / KV Cache / MHA→MQA→GQA→MLA）**——KB `KNOWLEDGE/transformer/` 3 节点；面试可深聊
- **Agent 工程理论体系（4 件核心事 / Context Engineering 6 层 / Harness 6 关键词 / Multi-Agent 决策框架 / Structured Output 6 层）**——KB `KNOWLEDGE/agent/` 6 节点
- **训练范式演进谱系（RLHF → DPO → GRPO 减法路径）**——KB `KNOWLEDGE/training/rlhf-dpo-grpo/`
- **LoRA 原理 + 显存估算**——KB `KNOWLEDGE/training/lora/`
- **Agent Harness 与模型边界诊断**：KB `model-boundary-probing` / `agent-evaluation-harness` / `tool-call-repair-harness` + `PROBLEMS/agent-harness-boundary-map/`
- **SFT 数据工程与训练策略**：KB `sft-data-sourcing` / `sft-data-quality` / `sft-training-strategy` / `sft-loss-signal-allocation`

## Open Questions

- **量化（AWQ / GPTQ）值不值得在 sprint 里花 1-2 天单独学？**——目前判断不值得；面试问到讲原理够；如果某个 JD 强烈要求实战再回头看
- **MCP servers/tools 实现要不要做一个 demo？**——如果主项目要集成 MCP（agent 可调用外部代码搜索 / git 工具）就顺便做了；不专门做
- **是否应该刷一些 SWE-bench-Lite 上的 Claude Code 跑分？**——如果横向对比时间宽裕，顺手跑一两个 issue 看实际效果，可以增强报告说服力
