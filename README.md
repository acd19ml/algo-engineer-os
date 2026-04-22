# Algo Engineer OS

算法工程师个人知识操作系统。

---

## 核心理念

**你只负责学习，知识库由 LLM 维护。**

学习时把任何形式的痕迹丢进 `INBOX/`，然后把 `META/llm/` 目录交给 LLM，LLM 自动将内容整理到知识库的正确位置。你只需要 review 结果。

---

## 使用方式

### 1. 学习时：丢进 INBOX

在 `INBOX/` 里放任何东西——一段话、一个链接、一张截图、一段代码、一个问题、粗读笔记。零结构要求。

### 2. 整理时：交给 LLM

把以下内容交给 LLM：
- `META/llm/CONTEXT.md` — 系统指令
- `META/REGISTRY.md` — 当前索引
- `META/llm/triage.md` — 分流规则
- `INBOX/` 中待处理的内容

LLM 会自动判断每条内容属于哪一层，创建或更新对应的页面，并同步索引。

### 3. Review

检查 LLM 的整理结果：
- 内容放对层了吗
- 有没有发明不存在的事实
- 新建的节点是否值得独立存在
- 不确定的内容是否有标注

---

## 仓库结构

```
algo-engineer-os/
├── INBOX/          # 随手丢学习痕迹（你的唯一入口）
├── RAW_SOURCES/    # 原始资料（论文、文档、粗读笔记、LLM 聊天记录）
├── KNOWLEDGE/      # 结构化知识节点（核心层）
├── PROBLEMS/       # 问题驱动页（方案比较、trade-off）
├── PROJECTS/       # 有边界的项目
├── WORK/           # 可复用工程实践（playbook、SOP）
├── CAREER/         # 职业资产（简历、面试、技能差距）
├── REPRO_INDEX/    # 外部代码仓库索引
├── TRACKS/         # 学习主线追踪（todo list、路线图）
└── META/           # 规则、模板、索引、LLM 上下文
```

### 内容放哪里（LLM 自动判断，你不需要记）

| 内容本质 | 目录 |
|---|---|
| 原始论文、文档、网页 | RAW_SOURCES/ |
| 可复用的概念/方法/机制 | KNOWLEDGE/ |
| 要解决的问题、失败模式 | PROBLEMS/ |
| 有明确目标的项目 | PROJECTS/ |
| 反复可用的 SOP/debug 经验 | WORK/ |
| 简历、面试准备 | CAREER/ |
| 外部 repo、实验代码 | REPRO_INDEX/ |

---

## Source of Truth

信息冲突时，按此优先级：

1. RAW_SOURCES/（原始证据）
2. KNOWLEDGE/\*/meta.yaml（结构关系）
3. KNOWLEDGE/\*/README.md（节点解释）
4. PROBLEMS/（问题框架）
5. 其他目录（派生内容）

---

## 关键文件

| 文件 | 作用 |
|---|---|
| [META/llm/CONTEXT.md](./META/llm/CONTEXT.md) | LLM 的完整操作指令 |
| [META/llm/triage.md](./META/llm/triage.md) | INBOX 分流规则 |
| [META/REGISTRY.md](./META/REGISTRY.md) | 全局内容索引 |
| [INBOX/README.md](./INBOX/README.md) | 临时入口说明 |

---

## 当前状态

系统正在建设中。已有内容：

- 3 个知识节点（transformer、self-attention、positional-encoding）
- 1 个问题页（sequence-modeling）
- 1 个项目（attention-is-all-you-need-reading-and-reproduction）
- 1 个原始资料（attention-is-all-you-need）
