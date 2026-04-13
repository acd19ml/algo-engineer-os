# Algo Engineer OS

一个用于学习、研究、实践、工作与成长的算法工程师个人操作系统。

这个仓库不只是笔记集合，也不只是论文阅读仓库。  
它是一个连接**长期知识积累、项目执行、工作沉淀与职业成长**的系统。

它服务于五类核心活动：

| Activity | Focus |
| --- | --- |
| **learning** | concepts, math, code, papers, experiments |
| **research** | methods, comparisons, open questions, reproductions |
| **work** | playbooks, design notes, debugging notes, reusable patterns |
| **projects** | research projects, side projects, work projects |
| **career** | resume stories, interview prep, skill gap analysis, growth planning |

---

## Quick Start

如果你第一次打开这个仓库，先不要试图把整套结构一次看完。

建议按下面顺序开始：

1. 先看 [如何使用这个仓库](#如何使用这个仓库)
2. 再看 [META](./META/README.md)，确认规则、模板和 source-of-truth
3. 然后跳到 [入口](#入口)，按你当前任务进入对应目录

如果你此刻最常见的任务是“接入论文 / 学习主题 / 做项目 / 做求职准备”，完整导航都放在后面的 [入口](#入口) 区块。

---

## 推荐阅读路径

根据你这次打开仓库的目的不同，推荐顺序不同：

### 1. 先建立整体理解

建议顺序：

1. [如何使用这个仓库](#如何使用这个仓库)
2. [入口](#入口)
3. [META](./META/README.md)
4. [KNOWLEDGE](./KNOWLEDGE/README.md)
5. [PROBLEMS](./PROBLEMS/README.md)
6. [PROJECTS](./PROJECTS/README.md)

### 2. 你正在接入一篇新论文

建议顺序：

1. [RAW_SOURCES](./RAW_SOURCES/README.md)
2. [Paper Ingestion Prompt Template](./META/templates/paper_ingestion_prompt.template.md)
3. [KNOWLEDGE](./KNOWLEDGE/README.md)
4. [PROBLEMS](./PROBLEMS/README.md)
5. [PROJECTS](./PROJECTS/README.md)
6. [REPRO_INDEX](./REPRO_INDEX/README.md)

默认不要一开始就写 `WIKI/`。
优先先把 `source -> structure -> execution` 这条链跑通。

### 3. 你想从一个主题开始构建

建议顺序：

1. [KNOWLEDGE](./KNOWLEDGE/README.md)
2. [META/policies/node_granularity.md](./META/policies/node_granularity.md)
3. [META/templates/node_README.template.md](./META/templates/node_README.template.md)
4. [PROBLEMS](./PROBLEMS/README.md)
5. [PROJECTS](./PROJECTS/README.md)

### 4. 你想把已有工作转成可复用资产

建议顺序：

1. [PROJECTS](./PROJECTS/README.md)
2. [WORK](./WORK/README.md)
3. [CAREER](./CAREER/README.md)
4. [THINKING](./THINKING/README.md)
5. [WIKI](./WIKI/README.md)

---

## 这个仓库是什么

这个仓库按照 **Knowledge Graph + LLM Wiki + Execution Index** 的方式构建。

它不是单纯按文件夹堆内容，也不是每次都从原始资料重新检索答案。  
它希望把知识持续沉淀为一个可以长期复用、持续更新、支持行动的系统。

系统的三个核心理念是：

### 1. Knowledge is stored as reusable nodes
每个主题都可以成为一个可复用的知识单元，而不是散落在不同笔记里的碎片。

### 2. Relationships are explicit
前置依赖、相关问题、替代方案、下游用途等关系，需要显式表达，而不是靠记忆维持。

### 3. Readable pages are compiled from structured knowledge
原始资料和节点页保持精确，Wiki 页负责综合与可读性。  
也就是说，这个系统同时追求：
- **truthfulness**
- **structure**
- **readability**
- **reusability**

---

## 系统分层

这个仓库有四个核心层次：

### 1. `RAW_SOURCES/` — 原始资料层
保存原始材料与引用来源，尽量保留上下文，不轻易重写。

Examples:
- papers
- books
- docs
- course notes
- web clippings
- rough reading notes

这一层解决的问题是：  
**不要让知识系统脱离原始证据。**

---

### 2. `KNOWLEDGE/` — 结构化知识图谱层
这是系统的核心层。

每个主题被视为一个知识节点，通常包含：
- `README.md`
- `meta.yaml`
- `math/README.md`
- `code/README.md`
- `refs/README.md`
- `thoughts/README.md`

Examples:
- transformer
- rope
- kv-cache
- distributed training
- multimodal modeling

这一层解决的问题是：  
**知识不仅要被记录，还要能被组织、连接、追踪与复用。**

---

### 3. `WIKI/` — 编译后的可读层
这一层不是原始真值层，而是从 `RAW_SOURCES/`、`KNOWLEDGE/`、`PROBLEMS/` 等层编译得到的综合页面。

Examples:
- concept overviews
- comparison pages
- problem syntheses
- model overviews
- project overviews
- career guides

这一层解决的问题是：  
**让复杂知识可以被快速理解、横向比较和长期查阅。**

---

### 4. `REPRO_INDEX/` — 执行索引层
这个仓库不要求包含所有实验代码。  
实验 repo 可以独立存在于外部，而这里维护它们的索引、状态和用途。

Examples:
- toy implementations
- reproduction repos
- analysis repos
- environment notes

这一层解决的问题是：  
**把知识和真实实验、代码资产重新连接起来。**

---

## 问题驱动层

除了知识节点，这个系统还用 `PROBLEMS/` 来组织“问题”。

### `PROBLEMS/`
Examples:
- training instability
- long-context degradation
- multimodal position encoding
- evaluation mismatch
- deployment bottlenecks
- interview storytelling

问题层的作用是：

- 让知识不只是“主题列表”
- 把方法放回它们要解决的问题中
- 支持同一问题下的方案比较
- 让学习路径更接近真实研究与工作过程

---

## 项目、工作与职业层

为了让知识真正服务现实，这个系统还包含三类更高层的结构：

### `PROJECTS/`
项目连接知识与产出。

Examples:
- research projects
- work projects
- side projects

### `WORK/`
用于沉淀日常工程实践中的可执行资产。

Examples:
- playbooks
- incident notes
- design notes
- recurring task SOPs

### `CAREER/`
用于职业成长、求职准备与能力表达。

Examples:
- resume
- interview prep
- target roles
- skill gap analysis
- project stories
- personal brand notes

---

## LLM Wiki 规则层

为了让这个仓库不仅能被人维护，也能被 LLM 辅助维护，系统包含专门的规则层：

### `META/`
这个目录存放：
- schema
- templates
- policies
- llm maintenance rules

其中 `META/llm/` 负责告诉 LLM：

- 什么是 source of truth
- 哪些页面可以更新
- 哪些关系不能擅自改动
- 如何处理新论文、新节点、新项目
- 如何区分事实、判断和猜测
- 如何维护 Wiki 而不污染底层真值层

这一层的作用是：  
**让 LLM 成为受约束的维护者，而不是随意发挥的生成器。**

---

## 真值来源（Source of truth）

当信息冲突时，按以下优先级判断：

1. `RAW_SOURCES/`
2. `KNOWLEDGE/*/meta.yaml`
3. `KNOWLEDGE/*/README.md`
4. `PROBLEMS/`
5. `WIKI/`

这意味着：

- raw sources preserve original context
- metadata defines structure and relationships
- node READMEs explain individual topics
- problem pages frame the question space
- wiki pages are compiled summaries, not base truth

---

## 设计原则

### 1. Directory structure does not represent dependency
目录用于组织内容，不用于表达前置依赖逻辑。

### 2. Dependencies live in metadata
知识之间的关系应当显式表达。

### 3. Every directory has a `README.md`
每个目录都应该说明：
- what it contains
- why it exists
- how to use it

### 4. Keep facts and opinions separate
- facts go to sources / refs / structured pages
- judgments go to thoughts / comparisons / open questions

### 5. Prefer reusable knowledge units
每个节点都应尽量小而清晰，便于跨项目复用。

### 6. Prefer accumulation over repeated rediscovery
不要每次都从零重新整理知识。  
应当通过增量更新，让系统持续变厚、变清晰、变可靠。

### 7. Wiki is compiled, not primary
Wiki 页应该可读、可综合，但不能替代底层真值层。

### 8. The system must support real work
这个仓库不只服务于理论学习。  
它也应帮助你提升执行效率、沟通质量与职业进展。

---

## 顶层结构

```text
algo-engineer-os/
├── META/
├── RAW_SOURCES/
├── KNOWLEDGE/
├── PROBLEMS/
├── PROJECTS/
├── WIKI/
├── REPRO_INDEX/
├── WORK/
├── CAREER/
├── THINKING/
├── PATHS/
├── DASHBOARDS/
├── SCRIPTS/
├── OUTPUT/
└── assets/
```

---

## 如何使用这个仓库

这个仓库最容易用错的地方，不是“写得不够多”，而是**一开始放错层**。

建议每次新增内容前，先回答一个问题：

> 这次新增的对象，最本质上是什么？

### 第一步：先判断应该放哪一层

- 原始论文、网页、文档、粗读笔记 -> `RAW_SOURCES/`
- 稳定、可复用的主题 / 方法 / 机制 -> `KNOWLEDGE/`
- 想解决的问题、失败模式、方案比较 -> `PROBLEMS/`
- 一次有明确目标和边界的执行 -> `PROJECTS/`
- 跨多个对象的综合说明或对比页 -> `WIKI/`
- 外部 repo、toy 实现、实验索引 -> `REPRO_INDEX/`
- 可反复执行的 SOP、playbook、design note -> `WORK/`
- 简历、面试、岗位准备、职业表达 -> `CAREER/`
- 个人判断、疑问、方向、反思 -> `THINKING/`
- 面向目标的学习 / 成长顺序 -> `PATHS/`
- 当前状态视图和优先级视图 -> `DASHBOARDS/`
- 自动化和校验脚本 -> `SCRIPTS/`
- 脚本生成产物 -> `OUTPUT/`
- 共享静态图片和图示 -> `assets/`

如果一时拿不准，优先使用这条默认判断：

- source evidence -> `RAW_SOURCES/`
- reusable topic -> `KNOWLEDGE/`
- challenge space -> `PROBLEMS/`
- bounded execution -> `PROJECTS/`
- compiled synthesis -> `WIKI/`

### 第二步：按常见场景使用

#### 当你学习一个新主题时

1. 先判断它是不是一个值得长期复用的 node，而不是某个更大主题里的小节。
2. 在 `KNOWLEDGE/` 下创建节点目录。
3. 最小结构通常包括：
   - `README.md`
   - `meta.yaml`
   - `math/README.md`
   - `code/README.md`
   - `refs/README.md`
   - `thoughts/README.md`
4. 先补 `meta.yaml` 和 `refs/README.md`，再补节点解释。
5. 把它连接到相关 `PROBLEMS/`、`PROJECTS/` 和外部 repo。

#### 当你读到一篇新论文时

1. 不要直接从论文跳到 `WIKI/` 或“总结页”。
2. 先把原文入口、原始链接或粗笔记接入 `RAW_SOURCES/`。
3. 再按这个顺序增量更新：
   - `KNOWLEDGE/*/refs`
   - 需要补充的 `KNOWLEDGE` 节点与 `meta.yaml`
   - 相关 `PROBLEMS/`
   - 相关 `PROJECTS/`
   - 相关 `REPRO_INDEX/`
   - 最后才是 `WIKI/`（如果真的需要）
4. 如果只有论文链接，也应先创建或补全对应的 `RAW_SOURCES` 页面。
5. 和 LLM 协作时，优先使用这个模板：
   - [META/templates/paper_ingestion_prompt.template.md](/Users/mac/studyspace/algo-engineer-os/META/templates/paper_ingestion_prompt.template.md)

#### 当你启动一个项目时

1. 在 `PROJECTS/` 下创建项目页。
2. 写清目标、范围、约束、当前状态和关键决策。
3. 链接所依赖的 `KNOWLEDGE` 节点和 `PROBLEMS` 页面。
4. 把相关外部 repo 记到 `REPRO_INDEX/`。
5. 把可复用经验沉淀到 `WORK/`，把个人判断和方向变化沉淀到 `THINKING/`。

#### 当你准备求职或面试时

1. 在 `CAREER/` 中维护目标岗位、skill gap 和项目故事。
2. 把项目页里的真实经历转成 resume bullets 和 interview stories。
3. 在 `PATHS/` 里建立 role-based 或 interview-based 路径。
4. 如果需要高层速查页，再把它们编译成 `WIKI/` 下的 career guide。

### 第三步：与 LLM 协作时怎么用

LLM 最适合做的是**受规则约束的维护**，不是“自由发挥的作者”。

建议这样协作：

1. 先告诉 LLM 这次任务的输入是什么：
   - 一个原论文链接
   - 一个 `RAW_SOURCES/.../README.md`
   - 一个已有 node / problem / project
2. 再告诉它这次允许更新到哪一层：
   - 只处理 source
   - 更新到 refs
   - 更新到 nodes / problems / projects
   - 是否允许写 `WIKI/`
3. 明确要求它遵守 source-of-truth 顺序：
   - `RAW_SOURCES/`
   - `KNOWLEDGE/*/meta.yaml`
   - `KNOWLEDGE/*/README.md`
   - `PROBLEMS/`
   - `WIKI/`
4. 要求它显式区分：
   - paper claim
   - current judgment
   - open question
5. 对这些内容做人工 review：
   - 新建 node 是否真的值得存在
   - `meta.yaml` 关系是否改对
   - problem framing 是否清楚
   - 有没有把猜测写成事实

### 一个推荐的最小闭环

如果你想让这个系统真正运转，而不是只多一篇笔记，最推荐的闭环是：

1. 从一篇论文或一个主题开始
2. 先接入 `RAW_SOURCES/`
3. 拆出 1 到 3 个高复用 `KNOWLEDGE` 节点
4. 建一个相关 `PROBLEMS` 页面
5. 建一个小 `PROJECTS` 页面
6. 如果有代码或计划写代码，把它记到 `REPRO_INDEX/`
7. 只有在需要更高可读性时，再补 `WIKI/`

一个简单判断是：

- 不要一开始就追求“全”
- 优先追求“source -> structure -> execution” 这条链先跑通一次

---

## 当前目标
- build a durable knowledge graph for algorithm engineering
- connect theory, implementation, execution, and career growth
- support paper reading and experiment reproduction
- accumulate reusable work knowledge
- turn projects into reusable professional assets
- improve job readiness and long-term growth over time

---

## 长期愿景

这个仓库应逐步成为：

- a learning system
- a research system
- a work support system
- a project memory system
- a career growth system

换句话说：

一个帮助你持续成长为更强算法工程师的个人操作系统。

---

## 入口

如果你是第一次打开这个仓库，建议按下面顺序进入：

1. 先看 [如何使用这个仓库](#如何使用这个仓库)
2. 再看 [META](./META/README.md)，确认规则和边界
3. 然后根据你当前任务进入对应目录

### 按任务导航

| 我现在要做什么 | 应该先看哪里 |
| --- | --- |
| 我在接入一篇新论文 | [RAW_SOURCES](./RAW_SOURCES/README.md)<br>[Paper Ingestion Prompt Template](./META/templates/paper_ingestion_prompt.template.md) |
| 我在学习一个新主题，想沉淀成可复用节点 | [KNOWLEDGE](./KNOWLEDGE/README.md) |
| 我在整理一个问题空间，想比较方案和 trade-off | [PROBLEMS](./PROBLEMS/README.md) |
| 我在推进一个有明确边界的项目 | [PROJECTS](./PROJECTS/README.md) |
| 我想看这个主题对应的外部代码、toy 实现或 reproduction repo | [REPRO_INDEX](./REPRO_INDEX/README.md) |
| 我想把反复出现的工程做法沉淀成 SOP / playbook / design note | [WORK](./WORK/README.md) |
| 我在准备简历、面试或目标岗位 | [CAREER](./CAREER/README.md) |
| 我想记录当前判断、疑问、方向和反思 | [THINKING](./THINKING/README.md) |
| 我想规划下一步学习或成长顺序 | [PATHS](./PATHS/README.md) |
| 我想快速看综合说明、对比页或 overview | [WIKI](./WIKI/README.md) |
| 我想看当前系统状态、优先级或活跃路径 | [DASHBOARDS](./DASHBOARDS/README.md) |
| 我想看仓库规则、模板和 LLM 维护方式 | [META](./META/README.md) |

### 按目录导航

| 目录 | 作用 |
| --- | --- |
| [META](./META/README.md) | 规则层。定义 source of truth、模板、命名、LLM 维护规则。 |
| [RAW_SOURCES](./RAW_SOURCES/README.md) | 原始资料层。论文、文档、粗读笔记先落这里。 |
| [KNOWLEDGE](./KNOWLEDGE/README.md) | 结构化知识图谱层。沉淀稳定、可复用的 nodes。 |
| [PROBLEMS](./PROBLEMS/README.md) | 问题驱动层。组织 challenge、失败模式、候选方案和 trade-off。 |
| [PROJECTS](./PROJECTS/README.md) | 项目层。把知识和问题真正连接到执行与产出。 |
| [REPRO_INDEX](./REPRO_INDEX/README.md) | 执行索引层。管理外部 repo、toy 实现、复现状态与环境说明。 |
| [WIKI](./WIKI/README.md) | 编译后的可读层。提供 overview、comparison、synthesis。 |
| [WORK](./WORK/README.md) | 工作资产层。沉淀 playbook、incident notes、design notes、recurring tasks。 |
| [CAREER](./CAREER/README.md) | 职业资产层。组织 resume、interview、job target、skill gap、stories。 |
| [THINKING](./THINKING/README.md) | 反思层。记录判断、疑问、方向和认知变化。 |
| [PATHS](./PATHS/README.md) | 路径层。把 graph 变成面向目标的行动顺序。 |
| [DASHBOARDS](./DASHBOARDS/README.md) | 状态视图层。帮助你看清当前 focus、progress 和 readiness。 |
| [SCRIPTS](./SCRIPTS/README.md) | 自动化层。放校验、生成、索引和 dashboard 脚本。 |
| [OUTPUT](./OUTPUT/README.md) | 派生产物层。保存脚本生成的 graph、summary、health report 等。 |
| [assets](./assets/README.md) | 共享静态资源层。保存可复用图片、图示、截图和图标。 |

---

## 当前状态

这个系统正在持续建设中。

第一阶段聚焦于：

- building the core directory structure
- defining metadata conventions
- creating initial knowledge nodes
- establishing problem pages
- linking external experiment repos
- setting up reusable templates
- defining LLM maintenance rules
- making the system incrementally updatable

---
