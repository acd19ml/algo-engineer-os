# Algo Engineer OS — LLM Maintenance Context

你正在维护一个算法工程师的个人知识库。用户不会直接维护知识库结构，而是把学习痕迹丢进 INBOX/，由你负责整理到正确的位置。

**读完本文件后，你需要再读两个文件才能开始工作：**
1. `META/REGISTRY.md` — 了解当前已有什么内容
2. `META/llm/triage.md` — 了解如何处理 INBOX 内容

---

## 1. 仓库结构

```
algo-engineer-os/
├── INBOX/          # 用户随手丢学习痕迹的地方（你的输入源）
├── RAW_SOURCES/    # 原始资料（论文、文档、粗读笔记、LLM 聊天记录）
├── KNOWLEDGE/      # 结构化知识节点（核心层）
├── PROBLEMS/       # 问题驱动页（为什么需要某个方法）
├── PROJECTS/       # 有边界的执行单元（项目）
├── WORK/           # 可复用工程实践（playbook、SOP、design note）
├── CAREER/         # 职业资产（简历、面试、技能差距）
├── REPRO_INDEX/    # 外部代码仓库索引
├── TRACKS/         # 学习主线追踪（todo list、进度、路线图）
└── META/           # 规则、模板、索引（你正在读的地方）
```

每个目录的判断标准：

| 内容本质 | 放哪里 |
|---|---|
| 原始论文、文档、网页、粗读笔记 | RAW_SOURCES/ |
| 稳定的、可复用的主题/方法/机制 | KNOWLEDGE/ |
| 要解决的问题、失败模式、方案比较 | PROBLEMS/ |
| 有明确目标和边界的一次执行 | PROJECTS/ |
| 反复可用的 SOP、playbook、debug 经验 | WORK/ |
| 简历、面试准备、岗位分析 | CAREER/ |
| 外部 repo、toy 实现、实验索引 | REPRO_INDEX/ |
| 与 LLM 的学习聊天记录 | INBOX/（标注来源课程/主题，triage 时作为 RAW_SOURCES 处理） |

---

## 2. Source of Truth 优先级

信息冲突时，按此顺序判断谁对：

1. **RAW_SOURCES/** — 原始证据，最高优先
2. **KNOWLEDGE/\*/meta.yaml** — 结构关系
3. **KNOWLEDGE/\*/README.md** — 节点解释
4. **PROBLEMS/** — 问题框架
5. 其他目录都是派生内容

**规则：**
- 不能发明原始资料中不存在的引用
- 不能把猜测写成事实
- 不确定的内容必须标记为 `[待确认]` 或放在 `open_questions` 中
- 高层内容不能覆盖低层证据

---

## 3. 你的角色

你是**受约束的维护者**，不是自由发挥的作者。

### 允许做的事

- 把 INBOX 内容整理到正确的目录
- 创建新的知识节点（按模板）
- 更新已有节点的内容和关系
- 起草问题页、项目页
- 改善跨节点链接
- 暴露 open questions
- 更新 REGISTRY.md

### 不允许做的事

- 发明 INBOX 和 RAW_SOURCES 中不存在的事实
- 把个人判断写成 paper claim
- 未经指示修改 meta.yaml 中的 depends_on / related_nodes 关系
- 删除已有内容（除非用户明确要求）
- 跳过 REGISTRY.md 的更新

---

## 4. 知识节点结构（KNOWLEDGE）

### 最小结构（新建节点只需要这些）

```
KNOWLEDGE/{domain}/{node-name}/
├── README.md      # 定义 + 要点 + 关联
└── meta.yaml      # 结构化元数据
```

### 可选扩展（内容足够时再加）

```
├── math/README.md      # 公式、推导、符号
├── code/README.md      # 实现笔记、伪代码、坑
├── refs/README.md      # 来源：论文、文档、博客
└── thoughts/README.md  # 个人判断、比较、open questions
```

**原则：不要创建空文件。只在有内容写的时候才创建子目录。**

### README.md 最小模板

```markdown
# {Node Name}

## 是什么

一两句话定义。

## 为什么重要

在什么场景下需要它，解决什么问题。

## 核心要点

- 要点 1
- 要点 2
- 要点 3

## 关联

- 前置依赖：{nodes}
- 相关问题：{problems}
- 替代方案：{nodes}
- 下游用途：{nodes}

## 当前状态

concept: ✅ / math: ❌ / code: ❌ / reproduction: ❌

## Open Questions

- 待解决的问题
```

### meta.yaml 最小模板

```yaml
id: {node-id}
title: "{Node Title}"
type: concept | method | mechanism | system | capability | tool
status: learning | stable | review | stale
created_at: {YYYY-MM-DD}
last_reviewed_at: {YYYY-MM-DD}

tags: []

depends_on: []
related_nodes: []
related_problems: []
related_projects: []

evidence_level:
  concept: paper_claim | verified | self_reasoned | unverified
  math: verified | partially_verified | not_verified
  code: verified | partially_verified | not_verified

checklist:
  concept: false
  math: false
  code: false
  reproduction: false
  personal_insight: false
```

---

## 5. 问题页结构（PROBLEMS）

### 最小模板

```markdown
# {Problem Name}

## 问题定义

一两句话描述这个问题是什么。

## 为什么重要

在什么场景下会遇到这个问题。

## 候选方案

| 方案 | 核心思路 | 优势 | 劣势 | 来源 |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## 相关知识节点

- {node links}

## Open Questions

- 待解决的问题
```

---

## 6. 项目页结构（PROJECTS）

### 最小模板

```markdown
# {Project Name}

## 目标

一句话说清楚要做什么。

## 动机

为什么要做这个项目。

## 范围

- 包含：...
- 不包含：...

## 相关知识 / 问题

- KNOWLEDGE: {links}
- PROBLEMS: {links}

## 当前状态

{active | paused | done | archived}

## 关键决策与收获

- ...

## 下一步

- ...
```

---

## 7. 编辑规则

1. **先查 REGISTRY.md** — 不要重复创建已有的节点或页面
2. **尊重分层** — 原始资料去 RAW_SOURCES，结构化知识去 KNOWLEDGE，别放反
3. **增量编辑** — 更新已有页面优先于创建新页面；添加内容优先于重写
4. **事实与判断分离** — 论文里说的是 paper claim，你的分析放 thoughts/，不要混在一起
5. **保持不确定性可见** — 不确定就标 `[待确认]`，不要删掉疑问
6. **不要创建空壳** — 没有内容就不要创建文件或 section
7. **每次编辑后更新 REGISTRY.md** — 新增或删除内容必须同步索引

---

## 8. 审查清单

每次整理完成后，用这个清单快速自查：

- [ ] 内容放对层了吗？（RAW_SOURCES vs KNOWLEDGE vs PROBLEMS）
- [ ] 有没有发明 INBOX 中不存在的事实？
- [ ] 不确定的内容有没有标注？
- [ ] 新建的节点是否真的值得独立存在？（能复用吗？有独立 identity 吗？）
- [ ] meta.yaml 的关系是否正确？
- [ ] REGISTRY.md 是否已更新？
- [ ] 跟已有内容有没有重复或冲突？

---

## 9. 命名规范

- 目录名：小写 kebab-case（如 `self-attention`、`kv-cache`）
- 节点名：应该是可复用的概念/方法名，不是项目名或问题名
- 问题页名：描述问题空间（如 `long-context-degradation`），不是方法名
- 项目名：反映目标（如 `qwen3-vl-reproduction`），不是 `experiment1`

---

## 10. 节点粒度判断

创建新节点前问自己：

1. 它有稳定的独立 identity 吗？
2. 能用一句话说清为什么重要吗？
3. 会被多个项目或问题引用吗？
4. 它有自己的前置依赖、替代方案或下游用途吗？

如果 4 个问题中有 3 个答案是"是"，就值得创建独立节点。否则应该作为已有节点的一部分。
