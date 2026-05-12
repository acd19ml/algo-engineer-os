# Q: 你的多智能体根因分析为什么选 Dify 工作流 + ReAct 而不是 Agent Loop / Coding Agent 范式？

## 来源

- 出处：基于七牛云 ZeroOps 项目可能被深挖的技术选型问题（自挖）
- 频率：高（任何看过你 CV 的 agent 方向面试官都会问）

## 涉及节点

- 主：`PROJECTS/work/qiniu-zeroops-rca-agent/`
- 相关：`KNOWLEDGE/agent/multi-agent/`、`KNOWLEDGE/agent/context-engineering/`
- 相关问题页：`PROBLEMS/multi-agent-decomposition-axis/`（建议建）

## 我的答案（高密度三段式 + 时代锚点）

**第一段：时代背景（关键！决定项目"看起来过时"还是"当时合理"）**

> 项目时间是 2025 年 7 月到 10 月。**当时市面上还没有开源的 agent loop 系统**——Claude Code / Codex / Cursor Agent / OpenHands / SWE-agent 这些都是 2025 年下半年到 2026 年才陆续涌现的。**上下文工程是刚兴起的概念**，当时最火的开源 agent 项目是基于 DAG 的 DeepResearch。Coding Agent / Harness Engineering / Skills 等概念都是项目结束后才系统化。
>
> 评判我的选型必须放在 2025 年 7 月的技术坐标里，而不是用 2026 年的标准回评。

**第二段：我的真实选型路径（不是 naive 选 workflow）**

> 我**项目初期试过编排 agent loop**——类 coding agent 式 / human-in-the-loop 风格。但调试困难：
>
> 1. 当时没有开源 agent loop 参考实现可借鉴
> 2. 多 agent 协同的失败模式（trajectory 错误传播、context 累积、循环不终止）没有标准化可观测性工具
> 3. 团队需要快速搭建可演示原型 + 非算法成员要能接手 → agent loop 黑盒程度太高
>
> 所以**主动从 agent loop 退到 Dify 工作流 + ReAct 模式**。具体收益：
>
> - 可视化工作流便于团队（含非算法成员）理解和调试
> - 每个 agent 的输入输出 JSON 结构化记录、可追溯
> - 每个节点单独可调试，prompt 级别可热替换
> - 内置 MCP 工具集成支持
>
> **本质是用工作流的可调试性换 agent loop 的灵活性，这是当时技术坐标下的合理 ROI 取舍**。

**第三段：今天回看的不足（不假装完美）**

> 今天如果重做，coding agent / Harness / Skills 这些概念都成熟了，**可以重新考虑 agent loop 方向**——特别是用 Claude Code 这类 harness 把 agent debug / failure attribution / checkpoint rollback 这些工程能力都内置。我的工作流方案在表达力（特别是面对真实复杂故障的灵活推理）上不如 agent loop，**但在 MVP 阶段 + 团队需要快速可演示 + 非算法成员要能接手的约束下，工作流仍然是对的选择**。

## 关键金句（背下来）

> "**我不是不知道 agent loop，是 2025 年 7 月那会儿试过然后退下来的**。"

> "**用工作流的可调试性换 agent loop 的灵活性——是当时技术坐标下的合理 ROI 取舍**。"

## 我答不出的部分（深问准备）

- **"你具体试 agent loop 时是怎么调试的、踩了什么坑"** → 我可能记不全具体细节。**面试时诚实承认"具体某个 trajectory 失败的复盘记不清了，但整体感受是失败模式难以收敛"**，比编故事强
- **"如果今天让你重做，你会选哪个 harness"** → 可以提：Claude Code（adopt-built-in skills 思路适合 SOP 嵌入）/ OpenHands（更通用）/ SWE-agent（更专精）。但要诚实承认"具体哪个更适合 AIOps 场景需要做技术调研，不是拍脑袋"
- **"DAG 和 agent loop 和工作流 ReAct 的本质区别是什么"** → 这题如果被问到要拆得开：
  - DAG = 静态、预定义、节点间数据流死板
  - 工作流 + ReAct = 半静态（结构定）+ 半动态（ReAct 循环 + 条件分支）
  - Agent loop = 完全动态（每步由模型自主决定下一步动作）
