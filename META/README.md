# META

`META/` 是这个仓库的规则层（rule layer）与治理层（governance layer）。

如果 `RAW_SOURCES/` 保存证据，`KNOWLEDGE/` 保存结构化节点，  
那么 `META/` 定义的就是：**这个系统应该如何运作、如何维护、如何避免失控**。

它不直接承载领域知识本身。  
它负责定义知识系统的结构、约束、模板与维护逻辑。

---

## 这个目录是做什么的

`META/` 主要回答以下问题：

- 什么样的页面或目录才是有效对象
- `meta.yaml` 应该包含哪些关键字段
- 仓库里的 source of truth 是什么
- 哪些内容可以被自动更新，哪些必须人工 review
- LLM 应该如何参与维护 Wiki、索引页、关系页
- 命名、目录结构、页面类型如何长期保持一致

没有这一层，仓库也可以继续增长。  
但随着节点、关系、Wiki、外部 repo 索引不断增加，它会逐渐变得不一致、难以判断、难以维护。

---

## 为什么这一层重要

这个仓库的目标不是一次性整理，而是长期积累。

这意味着：

- 节点会越来越多
- 页面之间会有越来越多交叉引用
- 同一主题会反复被重写、扩写、比较
- 外部实验 repo 会不断接入
- 人和 LLM 都会参与维护

当复杂度上升时，只有结构没有治理是不够的。  
`META/` 的作用，就是防止系统在增长中漂移（drift）。

---

## 推荐子结构

```text
META/
├── README.md
├── schema/
├── templates/
├── policies/
└── llm/
```

### `schema/`

定义仓库中各类对象的结构规范。

Examples:

- knowledge node schema
- `meta.yaml` schema
- problem page schema
- wiki page schema
- external repo metadata schema

这一层解决的是 **structural correctness**。

---

### `templates/`

提供可直接复用的模板。

Examples:

- node `README.md`
- node `meta.yaml`
- problem page
- wiki page
- subdirectory `README.md`
- external reproduction entry

这一层解决的是 **consistency and speed**。

---

### `policies/`

定义稳定的、仓库级别的规则。

Examples:

- source-of-truth priority
- naming conventions
- node granularity guidance
- evidence level definitions
- maintenance policy
- deprecation policy

这一层解决的是 **governance and boundary setting**。

---

### `llm/`

定义 LLM 如何参与维护。

Examples:

- system prompt
- editing rules
- update workflows
- review checklist
- uncertainty handling rules

这一层解决的是 **controlled automation**。

LLM 不应该被当成不受约束的作者。  
它更适合被当成**受规则约束的维护者**。

---

## 不应该放什么

`META/` 不应该承载以下内容：

- 具体论文内容或知识点解释
- 某个知识节点的事实性说明
- 项目执行记录
- 一次性实验日志
- 单主题临时笔记

这些内容应该去更合适的层：

- 原始证据放到 `RAW_SOURCES/`
- 结构化主题放到 `KNOWLEDGE/`
- 问题分析放到 `PROBLEMS/`
- 编译型综合页放到 `WIKI/`
- 项目与工作沉淀放到 `PROJECTS/`、`WORK/`

一句话说，`META/` 的目标不是“讲清某个主题”，  
而是“定义整个系统如何稳定地讲清主题”。

---

## 设计目标

### 1. Keep the system stable as it grows

仓库应该随着积累变得更丰富，而不是更混乱。

### 2. Make rules explicit

重要约定不能只存在于记忆里。

### 3. Support both humans and LLMs

人类需要能理解规则，LLM 需要能遵守规则。

### 4. Separate truth, structure, and presentation

- truth lives in raw sources
- structure lives in metadata
- presentation lives in compiled pages

### 5. Make maintenance reproducible

同一类更新，应该尽量走同一类流程，而不是每次重新发明做法。

---

## 推荐优先级

当 `META/` 内部不同文件发生冲突时，建议按下面顺序理解：

1. hard policy
2. schema
3. templates
4. LLM operating rules
5. examples

也就是说：

- `policy` 用来定边界
- `schema` 用来定结构
- `template` 用来提速
- `llm rules` 用来约束维护流程
- examples 只用于说明，不应高于正式规则

---

## Source of Truth 提醒

`META/` 本身不保存领域真值。  
它定义的是“真值、结构、可读层应该如何被管理”。

当信息冲突时，仍应遵守仓库级 source-of-truth 顺序：

1. `RAW_SOURCES/`
2. `KNOWLEDGE/*/meta.yaml`
3. `KNOWLEDGE/*/README.md`
4. `PROBLEMS/`
5. `WIKI/`
6. `DASHBOARDS/`
7. `OUTPUT/`

这意味着：

- `META/` 可以规定更新流程
- `META/` 不应该推翻原始证据
- `META/` 可以要求标注不确定性
- `META/` 不应该凭空制造事实

---

## `META/llm/` 至少应覆盖什么

建议明确写清以下内容：

### allowed actions

- 补全目录级 README
- 按模板创建新页面
- 基于已有 source material 更新摘要页
- 维护交叉链接、索引页、对比页
- 整理 refs 与结构化元数据

### disallowed actions

- 在没有证据时新增事实性结论
- 覆盖原始资料含义
- 擅自修改关键关系字段
- 把猜测写成事实
- 用 Wiki 文本替代底层真值层

### uncertainty handling

- 不确定时显式标注
- 争议内容单列为 open question
- 判断与事实分开写
- 缺少证据时宁可留空，也不要强行补齐

### review triggers

以下场景建议强制人工 review：

- 新建高影响知识节点
- 修改 `meta.yaml` 中的关键关系
- 更新 source-of-truth 相关政策
- 大规模重写 Wiki
- 引入新的 schema 或 template

---

## 如何使用这个目录

### 当你创建一个新节点时

先检查：

- naming rules
- node template
- metadata schema

### 当你新增一种页面类型时

先检查：

- 是否已有 template 可以复用
- 是否需要新增 schema 支持
- 这个页面到底应属于 `WIKI/`、`KNOWLEDGE/` 还是其它层

### 当你更新关系时

先检查：

- 这次修改是否应该写进 `meta.yaml`
- 是否影响 source-of-truth 结构
- 是否需要同步更新相关 Wiki

### 当你让 LLM 帮忙维护时

先让它查看 `META/llm/` 下已经存在的规则文件，至少包括：

- `META/llm/system_prompt.md`
- `META/llm/editing_rules.md`
- `META/llm/update_workflows.md`
- `META/llm/review_checklist.md`

---

## 推荐维护顺序

当一个新主题进入系统时，推荐按下面顺序落地：

1. 先确认原始资料是否进入 `RAW_SOURCES/`
2. 再确认是否需要创建或更新 `KNOWLEDGE/` 节点
3. 如果对应的是待解决问题，再更新 `PROBLEMS/`
4. 如果需要横向整理或对外可读解释，再更新 `WIKI/`
5. 如果沉淀的是规则、模板或维护约束，再回写 `META/`

这个顺序的核心是：

- 先落证据
- 再落结构
- 再落综合说明
- 最后抽象出通用维护规则

---

## 当前阶段的重点

`META/` 的第一阶段建议优先补齐：

- metadata schema definition
- reusable templates
- source-of-truth policy
- LLM maintenance rules
- naming and node granularity conventions

---

## 与其它目录的关系

- `META/` 定义规则
- `RAW_SOURCES/` 保存证据
- `KNOWLEDGE/` 保存结构化知识节点
- `PROBLEMS/` 保存问题空间与方案比较
- `WIKI/` 提供编译后的可读页面

一句话概括：

`META/` 不负责提供答案，  
它负责约束“答案如何被组织、更新、验证与复用”。

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [KNOWLEDGE](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/README.md)
- [PROBLEMS](/Users/mac/studyspace/algo-engineer-os/PROBLEMS/README.md)
