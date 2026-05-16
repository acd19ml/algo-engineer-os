# Harness Engineering 规范形态 + 实证数据保留

> 这是 thoughts/ 形态——不是节点主体内容（主体讲 GAN-inspired 三 agent 系统），而是从三篇媒体文章蒸馏出的 **Harness Engineering 的规范形态 + 工程化落地证据**，供面试 / CV 引用。三篇分别是：
> - 阿里实战《Harness Engineering：耗时一周，AI Coding 率提升至 90%》
> - 腾讯《Harness Engineering 即控制论》
> - 腾讯《Harness Engineering 如何工程化落地》（JK Launcher 12 章实战）

## 三次范式跃迁（隐喻坐标）

| 阶段 | 时间 | 关注点 | Tobi Lutke 隐喻 |
|---|---|---|---|
| Prompt Engineering | 2022-2024 | 单次交互的优化 | "写好一封邮件" |
| Context Engineering | 2025 | 给 Agent 看什么 | "给邮件附上所有正确的附件" |
| Harness Engineering | 2026 | 跨会话 / 跨 agent / 跨阶段的完整系统 | "Agents aren't hard; the Harness is hard." (Ryan Lopopolo, OpenAI) |

> Mitchell Hashimoto（HashiCorp）的操作性定义：**"Every time you discover an agent has made a mistake, you take the time to engineer a solution so that it can never make that mistake again."** Harness 不是一次性 prompt 优化，是持续演进的系统工程闭环。

## Anthropic 总结的 Agent 四种失败模式

1. **One-shot Syndrome（试图一步到位）**：复杂需求倾向一窗口内完成；上下文消耗大半后开始 Hallucination / 循环输出 / 格式错误 Tool Call。Anthropic 经验数据：**上下文窗口 Sweet Spot 在 40% 以下；超过此阈值，输出质量快速衰退**
2. **Premature Victory Declaration（过早宣布胜利）**：完成部分工作就宣布任务结束，核心功能未实现或未验证——输出"编码完成"，实际编译都过不了
3. **Premature Feature Completion（过早标记功能完成）**：功能已实现但未做端到端测试，部署后才发现关键路径不通。Anthropic 的解决方案：引入 Browser Automation（Puppeteer MCP）做自动化端到端截图
4. **Cold Start Problem（环境启动困难）**：多会话间缺持久化记忆，新会话花大量 token 重新理解项目结构，真正用于编码的 token budget 严重被挤压

**共同根源**：Agent 缺乏外部的结构化约束（Structured Constraints）和反馈机制（Feedback Mechanisms）。进一步：**"Agents are incapable of accurately evaluating their own work"**——Harness 的作用是用外部化控制系统弥补这一缺陷。

## 四根支柱（Anthropic 长时间运行 Agent 工程实践 + OpenAI Codex 团队百万行实战）

OpenAI 团队数据：**3→7 人团队，产出 ~1M LOC，1,500 PRs，人均 3.5 PRs/天，效率提升约 10 倍**。

| 支柱 | 内容 | 关键经验 |
|---|---|---|
| **1. 上下文架构（Context Architecture）** | 让 Agent 恰好获得当前任务所需上下文——不多不少 | OpenAI 早期把 AGENTS.md 写成百科全书——"所有内容都重要 = 没有内容重要"。后来改为 **~100 行作为索引和地图（Index & Map）**，指向更深层 Design Docs / Architecture Specs / Quality Criteria |
| **2. Agent 专业化（Agent Specialization）** | 受限工具集的专业 Agent 优于全权通用 Agent | Anthropic 明确分离三种角色：**Planner（规划）/ Generator（实现）/ Evaluator（验证）**。核心发现："将做事的 Agent 和评判的 Agent 分开，是一个强有力的杠杆" |
| **3. 持久化记忆（Persistent Memory）** | 进度持久化在文件系统上，而非上下文窗口 | Anthropic 标准化启动序列：**检查 cwd → 读 Git Log + progress.md → 定位优先级最高的未完成任务 → 开始工作**。使跨越数十个会话的长时间任务成为可能 |
| **4. 结构化执行（Structured Execution）** | 永远不让 Agent 在未经审查和批准书面计划之前写代码 | 理想执行流：**理解 → 规划 → 执行 → 验证**，每个阶段之间有明确质量门禁。OpenAI 经验：用 Custom Linter + Structure Tests + Taste Invariants 构建机械化约束，完全替代文档层面的"建议"和"最佳实践"。原则："**Waiting is expensive, fixing is cheap**" |

## JK Launcher 实战：24.86% → 90.54% AI Coding Rate

**项目背景**：企业级 Java 应用（**10 万+ 行**，Java 1.8 / Spring Boot / LiteFlow / HSF / Diamond / Tair），从零构建 Harness 体系。

### 四要素架构

| 要素 | 回答 | 形态 |
|---|---|---|
| **Rules** | 标准是什么 | 工程结构约束、编码规范、分层架构约定（**Invariant Constraints**） |
| **Skills** | 应该怎么做 | 需求分析 SOP / 编码分层规范 / 评审清单 / 单元测试方法（**Reusable Workflows**） |
| **Wiki** | 系统是什么样的 | 链路梳理 / 数据模型 / 核心业务流程文档化（**Domain Context**） |
| **Changes** | 做了什么 | 每个需求从分析到部署的全过程文档，构成 **Audit Trail** |

### `.harness/` 目录结构（物理载体）

```text
.harness/
├── agents/          # Agent 角色定义
├── rules/           # 规则体系
│   ├── 工程结构.md
│   ├── 开发流程规范.md
│   └── 项目编码规范.md
├── skills/          # 技能体系（9 个 Skill）
│   ├── request-analysis/      # 需求分析
│   ├── coding-skill/          # 编码实现
│   ├── expert-reviewer/       # 专家评审
│   ├── unit-test-write/       # 单元测试编写
│   ├── unit-test-ci/          # CI 流水线验证
│   ├── deploy-verify/         # 部署验证
│   ├── code-review/           # 代码检查
│   ├── project-analysis/      # 项目分析
│   └── aone-ci-generate/      # CI 配置生成
├── changes/         # 变更管理目录
├── mcp/             # 外部工具集成配置（MCP Servers）
└── (wiki/ 位于项目根目录)
```

### Application Owner Agent（编排中枢）

定义文件 **约 400 行**——信息密度最高的文件，承担 Anthropic 所说的 "Index & Map" 职责。它**不是百科全书，是一张精心设计的地图**，告诉 Agent 在什么阶段该去哪里找什么知识。

五个核心模块：

1. **角色与项目背景**（Role & Project Context）——20-30 行 "刚好够用" 的项目视野
2. **配置中枢索引**（Configuration Hub Index）——结构化表格列 Rules / Skills / Wiki / MCP 四大组件的路径、职责、触发场景、更新频率
3. **七项核心职责**——需求理解 / 任务拆解 / 任务分发 / 任务验收 / 质量把关 / 文档维护 / 知识问答
4. **工作流程调度指令**（10 阶段流程的完整调度逻辑）
5. **沟通原则与硬性约束**——两张清单："必须做到" + "禁止做的"

### 10 阶段开发流程（10-Stage Pipeline）

```text
需求分析 → 需求评审 → 编码实现 → 编码评审 → 单元测试编写
    → 单元测试评审 → 代码推送 → CI 验证 → 部署验证 → 用户确认
```

每个阶段三要素：**Entry Criteria（触发条件）/ Skill Injection（Skill 加载指令）/ Quality Gate（质量门禁）**。

**精确回退路径**（避免"出问题只能从头来"）：
- CI 失败 + 测试 0/0 → 回退阶段 5（测试编写）
- 编译错误 → 回退阶段 3（编码实现）
- 需求不符 → 回退阶段 1（需求分析）

**循环上限**（防 Infinite Self-correction Loop）：需求评审最多 3 轮、编码/测试评审最多 2 轮，超出升级到人工决策。

**5 个 Human-in-the-Loop 确认点**：需求待决议 / 计划评审后 / 编码评审后 / 部署环境参数 / 最终交付。

### 上下文三层加载

| 层 | 加载时机 | 内容 |
|---|---|---|
| **L1 — 会话常驻**（Always Loaded） | 整个会话都加载 | Agent 定义文件（~420 行 Index & Map） + 三份 Rules 文件。**总量严格控制，避免上下文窗口填充率 > 40%** |
| **L2 — 阶段触发**（Phase-triggered） | 进入对应阶段 | 需求分析 → request-analysis Skill；编码 → coding-skill + 8 份分层编码 Spec（Controller→Service→Domain→DAO→Adapter 全链路）；评审 → expert-reviewer |
| **L3 — 按需查询**（On-demand） | Agent 自主查阅 | Wiki 知识库的业务文档不主动加载 |

核心考量：**让 Agent 在任何时刻都拥有"刚好够用"的上下文（Just-enough Context）**。中间件繁多的企业级应用尤其关键——把 RPC / 流程引擎 / 配置中心规范一次性塞给 Agent，信息过载反而导致注意力分散和幻觉。

### Coding-skill 的分层规范（8 份）

| 层级 | 规范文件 | 核心内容 |
|---|---|---|
| 表现层 | Controller 实现 Spec | RPC Provider 实现模式、参数校验、异常处理 |
| 应用层 | 接口定义 / 实现 Spec | RPC 接口定义规范、DTO 设计原则 |
| 业务层 | 业务逻辑 Spec | 核心业务逻辑封装、流程编排组件写法 |
| 数据层 | 建表 / 持久化 Spec | DDL 设计规范、Mapper 编写方式 |
| ... | ... | ... |

### Entropy Garbage Collection

OpenAI 在百万行实践中提出的概念：**Agent 写代码时会模仿代码库中已有的 Pattern，包括 Suboptimal 的 Pattern**。每次生成都可能引入少量风格不一致 / 冗余 / 次优实现——累积起来让代码库逐渐腐化（Code Rot）。

OpenAI 早期尝试每周五手动清理"AI 产物"，发现无法持续。最终方案是将 **"Golden Principles"** 编码化（如"优先使用共享工具包而非手写辅助函数"、"结构化日志格式统一"），让后台 Agent **自动扫描违规并提交修复 PR**，形成自动化的 Entropy Garbage Collection 机制。

### 开发者角色范式转移（Paradigm Shift）

| 模式 | 核心工作 |
|---|---|
| 传统模式 | 写代码 / 调 Bug / 做 Code Review |
| Agent-First 模式 | **设计 Agent 的工作环境**（Working Environment Design） / **编写规范文档**（Specification Authoring） / **管理任务拆分与验收**（Task Orchestration & Acceptance） |

**文档从"给人看的参考资料"变成"Agent 认识世界的唯一窗口"**。架构约束不再是"大团队才需要"的奢侈品，而是 Agent 能高效工作的前置条件。**发现 Bug 不再只是修代码，而是修 Harness**——从根源上防止同类问题再次出现。

> The agent's knowledge boundary equals the repository's file boundary. （Agent 的知识边界等于代码库的文件边界）—— 如果某条架构约定不在代码库中以机器可读的形式存在，对 Agent 来说它就不存在。

## 控制论坐标（Cybernetics 视角）

Harness Engineering 本质是控制论在编码世界的工程实现——1948 年维纳《控制论》关注"系统如何通过接收外界和内部的信息来调整自身状态以达到预定目标"。AI 的"输入-输出-修正"回路与之同构。

Mitchell Hashimoto 的定义 "Every time you discover an agent has made a mistake, engineer a solution so it can never make that mistake again" 是一个标准的**控制反馈环**：

```text
Reference (期望产出) → Plant (Agent + 模型) → Output (实际产出)
                              ↑                     ↓
                          Corrector ← Sensor (失败检测：CI / 测试 / Review)
                              ↑
                         Engineering Action (修 Harness → Rules / Skills / Wiki / Gates)
```

## 核心概念区分（JK Launcher 第 1 章速览表）

| 概念 | 主要回答 | 在工程里的角色 |
|---|---|---|
| **Rule** | 什么事绝对不能乱来 | 基础规矩 / 红线 / 底线（**软约束**，模型可能忘 / 觉得无关 / 偷懒） |
| **Skill** | 这件事具体应该怎么做 | 固定动作的标准操作手册 |
| **Sub Agent** | 复杂任务由谁分工处理 | 不同阶段的专业角色 |
| **Workflow** | 这些角色按什么顺序接力 | 前进 / 暂停 / 打回 / 重跑规则 |
| **Scripts** | 最后谁来判断到底做没做好 | 统一门禁和事后验证（**硬门禁**，可执行验证） |
| **MCP** | AI 怎么安全接上外部工程系统 | 外接能力与工具链（含 Unity 等宿主） |

**关键判断**：Rule 是软约束（AI 可能违反），Scripts 是硬门禁（机器执行不可绕过）——这对决定哪些约束放在 Rule、哪些放在 Scripts 至关重要。

## 这跟主节点的关系

主节点 `KNOWLEDGE/agent/harness-practice/README.md` 讲的是 **GAN-inspired 三 agent 系统**（Planner / Generator / Evaluator）——这是 Anthropic 的 toy 案例形态。

本 thoughts 文件保留的是 **企业级落地的规范形态**：四要素架构 / `.harness/` 目录 / 10 阶段 pipeline / 上下文三层加载 / Entropy GC。两者是**同一套思想的 toy 形态和企业级落地形态**。

## 面试 / CV 用法

- 问 "Harness Engineering 是什么" → 用三次范式跃迁 + Hashimoto 定义 + 四根支柱回答
- 问 "你怎么提高 AI Coding 率" → 拿 JK Launcher 24.86% → 90.54% 数据 + 四要素架构回答
- 问 "Agent 怎么避免幻觉" → 用 Sweet Spot < 40% + 四种失败模式 + 外部化反馈机制回答
