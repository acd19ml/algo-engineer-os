# RAW_SOURCES / articles

公众号 / 博客 / 技术文章原文存档。这些是 Memory 系统 + Harness Engineering + Heuristic Learning 主题的二手分析文章——大部分内容已蒸馏到 `KNOWLEDGE/agent/` 节点 + `PROBLEMS/agent-memory-architecture/`，**这里保留原文以备未来回查或重新提取**。

## 已蒸馏（KB 内容自含，原文仅备份）

| 文件 | 蒸馏到 |
|---|---|
| `claudecode-memory.md` | `PROBLEMS/agent-memory-architecture/`（7 层防御金字塔表 + 限制 50k/400k/200k + Auto Dream 五道门控 + 9 段全压缩摘要 + 4 类记忆 + 反馈三件套 + Agent Pattern × Memory Scope 双矩阵）|
| `openclaw-memory.md` | `PROBLEMS/agent-memory-architecture/`（三层架构 mermaid + SQLite 4 表 schema + Memory Flush prompt + Hybrid Fusion 0.7/0.3 代码 + 72h 实验数据）|
| `openclaw-claudecode-memory.md` | `PROBLEMS/agent-memory-architecture/`（横向对比骨架 + 6 层 vs 2 层 + LLM 路由 vs SQLite 双索引 + "梦境 vs 临终遗言"对照）|
| `memory.md` | `KNOWLEDGE/agent/memory-architecture-thesis/`（三件套 + System 1/2 + JitRL + 三类瓶颈 + bi-temporal + Memory tool 工具化）|
| `heuristic-learning.md` | `KNOWLEDGE/agent/heuristic-learning/`（HL/HS 定义 + Deep RL 对照表 + Atari 387→864 / MuJoCo Ant 6000+ / HalfCheetah 11836.7 / VizDoom 557/440 / Atari57 342 trajectories + coupling complexity + Montezuma 反例 + Robotics 分层）|
| `harness.md` | `KNOWLEDGE/agent/harness-practice/thoughts/canonical-form-evidence.md`（三次范式跃迁 + 四种失败模式 + Sweet Spot < 40% + 四根支柱 + JK Launcher 24.86%→90.54% + 四要素架构 + `.harness/` 目录 + 10 阶段 pipeline + 三层上下文加载 + Entropy GC + 范式转移）|
| `harness2.md` | 同上（控制论坐标 + 维纳 1948 + Hashimoto 反馈环） |
| `hermes2.md` | `KNOWLEDGE/agent/agent-skills-closed-loop/`（7 步闭环 mermaid + SKILLS_GUIDANCE + 七道安全关卡 + 原子写入 + TOCTOU + Skill frontmatter + 两层缓存 + L1/L2/L3 性能 + 条件激活 + 渐进式加载 Tier 0-3）|

## 部分蒸馏（章 1 已蒸馏，章 2-12 待补）

| 文件 | 已蒸馏 | 未蒸馏（如做主题节点回头读） |
|---|---|---|
| `harness-practice.md` | 第 1 章 6 概念速览（Rule/Skill/SubAgent/Workflow/Scripts/MCP）→ `harness-practice/thoughts/canonical-form-evidence.md` | 章 2-12：具体 Rule 文件写法 / Workflow YAML 配置 / Skills 模板 / Unity 场景接入。若做 "如何从 0 搭 Harness" 节点回头读 |

## 未蒸馏（话题暂未对接到 KB 节点，原文备份待用）

| 文件 | 内容 | 触发条件（什么时候回头读）|
|---|---|---|
| `claudecode.md` | Claude Code 5 大模块（入口与启动链路 / 多模式宿主 / 工具面 / 权限 / 多 Agent 扩展） | 跟现有 harness / agent-tool-design / agent-permission-system / agent-role-isolation / agent-context-compaction 节点重叠较多。若要把"启动三段链路（入口分流→进程级初始化→会话级准备）+ AppState 与 process state 分层 + GrowthBook 远程开关"补到 harness 节点 thoughts/，回头读 |
| `hermes.md` | 阿里云 Hermes 可观测插件（process observability for ReAct） | 若做 "Agent 可观测性" 主题节点，回头读：可观测 4 类问题（过程不可见 / 成本归因 / 工具调用真伪 / 数据泄露）+ 调用链结构化 + Token 归因 |
| `deer-flow2.0-sandbox.md` | DeerFlow 2.0 Sandbox 三层架构（SandboxMiddleware / SandboxProvider / Sandbox 接口）+ DIP/SRP + 懒加载/饿加载 + Docker 容器级隔离 + 与 AutoGen/CrewAI 对比 | 若做 "Agent 沙箱化执行" 节点，回头读：三层架构表 + DIP 解耦设计 + 懒加载缓解资源开销 + AgentMiddleware before_agent/after_agent 钩子模式 |

## 来源（公开材料，可补 URL）

所有文章为公开发表的微信公众号 / 博客内容。如需补 URL：
- claudecode.md / harness.md / memory.md / hermes.md — 阿里妹 / 阿里云开发者公众号
- claudecode-memory.md — X 上 @troyhua（CMU 博士）的 thread 中文化整理
- openclaw-memory.md / openclaw-claudecode-memory.md / harness2.md / harness-practice.md / hermes2.md — 腾讯云开发者公众号
- heuristic-learning.md — Jiayi Weng 个人博客（https://trinkle23897.github.io/learning-beyond-gradients/）
- deer-flow2.0-sandbox.md — 字节跳动开源团队
