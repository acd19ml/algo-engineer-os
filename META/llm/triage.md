# INBOX Triage Rules

这个文件定义你如何处理 INBOX/ 中的内容。用户把学习痕迹丢进 INBOX，你负责把它们整理到知识库的正确位置。

---

## 整体流程

```
1. 读 META/REGISTRY.md        → 了解已有内容
2. 读 INBOX/ 所有文件          → 了解待处理内容
3. 对每个 INBOX 项目执行分类    → 判断属于哪一层
4. 执行整理                    → 创建或更新目标文件
5. 更新 META/REGISTRY.md       → 同步索引
6. 标记 INBOX 项目为已处理      → 避免重复处理
```

---

## Step 1: 读取现状

读 `META/REGISTRY.md`，确认：
- 已有哪些 KNOWLEDGE 节点
- 已有哪些 PROBLEMS 页面
- 已有哪些 PROJECTS
- 已有哪些 RAW_SOURCES

**目的：避免重复创建，优先更新已有内容。**

---

## Step 2: 读取 INBOX

读取 INBOX/ 下所有文件。忽略 README.md。

对每个文件，提取：
- 主题是什么
- 内容类型（论文笔记、代码片段、问题、链接、想法、工作经验...）
- 涉及哪些已有节点/问题/项目

---

## Step 3: 分类

对每个 INBOX 项目，按以下决策树判断：

```
这个内容是...

├── 原始资料（论文链接、文档、网页、粗读笔记）
│   → RAW_SOURCES/
│
├── 关于一个可复用的概念/方法/机制的学习
│   ├── 已有对应节点？ → 更新该 KNOWLEDGE 节点
│   └── 没有？ → 判断是否值得新建节点（见粒度判断）
│       ├── 值得 → 新建 KNOWLEDGE 节点（最小结构）
│       └── 不值得 → 作为已有节点的补充内容
│
├── 关于一个问题/挑战/失败模式的思考
│   ├── 已有对应问题页？ → 更新该 PROBLEMS 页面
│   └── 没有？ → 新建 PROBLEMS 页面（最小结构）
│
├── 关于一个具体项目的进展/决策/记录
│   ├── 已有对应项目？ → 更新该 PROJECTS 页面
│   └── 没有？ → 新建 PROJECTS 页面
│
├── 可复用的工程实践/SOP/debug 经验
│   → WORK/
│
├── 简历素材/面试准备/岗位分析
│   → CAREER/
│
├── 外部代码仓库/实验 repo
│   → REPRO_INDEX/
│
└── 无法归类或太碎片
    → 看能否附加到已有节点的 thoughts/README.md
    → 如果完全无法归类，保留在 INBOX 并标注 [待归类]
```

---

## Step 4: 执行整理

### 创建新内容时

- KNOWLEDGE 节点：只创建 README.md + meta.yaml，不要创建空的子目录
- PROBLEMS 页面：只创建 README.md，包含问题定义、候选方案、open questions
- PROJECTS 页面：只创建 README.md，包含目标、范围、状态
- RAW_SOURCES：创建对应目录和 README.md，保留原始链接和关键信息

模板参考 `META/llm/CONTEXT.md` 中的第 4-6 节。

### 更新已有内容时

- 增量添加，不要重写整个文件
- 新的 paper claim 和个人判断要分开标注
- 如果新信息与已有信息冲突，在 open questions 中暴露冲突，不要静默覆盖
- 更新 meta.yaml 中的 last_reviewed_at 日期

### 内容拆分

一个 INBOX 项目可能涉及多个目标：
- 一篇论文笔记 → RAW_SOURCES（原文信息）+ KNOWLEDGE（方法节点）+ PROBLEMS（问题页）
- 一段工作经验 → WORK（SOP）+ CAREER（故事素材）+ KNOWLEDGE（技术点）

按内容本质拆分到各自的正确位置。

---

## Step 5: 更新 REGISTRY.md

每次整理后，把新增/修改的条目更新到 `META/REGISTRY.md`：
- 新建节点 → 加到 KNOWLEDGE nodes 表
- 新建问题页 → 加到 PROBLEMS 表
- 新建项目 → 加到 PROJECTS 表
- 新建原始资料 → 加到 RAW_SOURCES 表

---

## Step 6: 标记已处理

处理完的 INBOX 文件，在文件顶部加一行：

```
<!-- PROCESSED: YYYY-MM-DD -->
```

或者，如果用户允许，直接删除已处理的 INBOX 文件。

默认行为：**加标记，不删除**。除非用户说"处理完可以删"。

---

## 特殊情况处理

### INBOX 项目是纯链接
→ 创建 RAW_SOURCES 条目，记录链接和上下文。如果能判断主题，同时更新对应 KNOWLEDGE 节点的 refs。

### INBOX 项目是一个问题/困惑
→ 判断是已有问题的补充还是新问题。如果是已有节点的 open question，加到该节点的 thoughts/README.md 或 README.md 的 Open Questions 中。

### INBOX 项目内容太碎片无法归类
→ 保留在 INBOX，加标注 `<!-- PENDING: 内容太碎片，待后续补充后再归类 -->`。

### INBOX 项目跨多个主题
→ 拆分内容到各自的正确位置，每个位置只包含与该位置相关的部分。

### 你不确定某内容是否正确
→ 整理时标注 `[待确认]`，放在 open questions 中，不要当成已验证的事实。

### INBOX 项目是与 LLM 的聊天记录
→ 聊天记录本身作为 RAW_SOURCES 保存（保留原始对话上下文）。从中提取的知识点正常 triage 到 KNOWLEDGE/PROBLEMS 等。

### INBOX 项目带有 track 标签（如 `[TML]` `[AI]` `[NLP]`）
��� 这些是临时 track（如 final 备考）的学习痕迹。正常 triage 知识内容，但注意：
- 过程性内容（cheat sheet 策略、做题技巧、考试安排）**不入库**，标记后丢弃
- 只有**值得长期复用的知识点**才整理到 KNOWLEDGE/
- 参考 `TRACKS/` 目录了解当前活跃的 track 和处理规则
