# Interview Bank

面笔试题库。**LLM 不自动生成题目**，所有内容来自你丢进 INBOX 的真实面经、JD 提取、学长分享。

## 结构

```
interview-bank/
├── technical/      技术题（每题链回 KNOWLEDGE 节点）
└── behavioral/     行为题（每题链回 PROJECTS/work/<实习>/ 的 STAR 故事）
```

## 题目页结构

### `technical/{question-slug}.md`

```markdown
# Q: {question}

## 来源
- 出处：{某厂 / 某面经平台 / 某学长}
- 频率：高 / 中 / 低

## 涉及节点
- 主：`KNOWLEDGE/x/`
- 相关：`KNOWLEDGE/y/`
- 相关问题页：`PROBLEMS/z/`（如有横向比较）

## 我的答案
（用对话 log 里你和 LLM 推过的版本，不是 LLM 单独写）

## 我答不出的部分
- ...（这部分回 INBOX 找 dialogue 学）
```

### `behavioral/{question-slug}.md`

```markdown
# Q: {question, e.g. "讲一段你的实习经历"}

## STAR
- Situation: ...
- Task: ...
- Action: ...
- Result: ...

## 关联项目
- `PROJECTS/work/<实习名>/`

## 可强调的能力信号
- 决策能力 / ownership / 技术深度 / 沟通
```

## 工作流

1. 找面经 → 丢进 `INBOX/<topic>/` 任意位置（甚至直接放原文 .md）
2. LLM triage：拆题 → 建 `interview-bank/technical/` 或 `behavioral/` 条目 → 链回 KNOWLEDGE / PROJECTS
3. 你打开题，对照答案。答不出 → 这一题对应的 KNOWLEDGE 节点是真没学懂，回去和 LLM 对话补

## 当前推荐复习顺序

不要从 `KNOWLEDGE/` 全量扫起。求职准备时按三层走：

1. **岗位层**：先看 `CAREER/applications/active/` 里当前 active 岗位的 JD / 面经准备表，确定本周最可能被问什么。
2. **题库层**：再看 `CAREER/interview-bank/technical/` 和 `behavioral/`，把这些问题练成 1-2 分钟可答的口径。
3. **知识层**：最后用 `KNOWLEDGE/_self_check/` 做查漏补缺。答不出 self-check 时，回对应 `KNOWLEDGE/<domain>/<node>/` 重新学。

## 新知识补洞规则

当 active JD / 面经暴露新空白时，先判断它属于哪一类：

| 空白类型 | 放哪里 | 例子 |
|---|---|---|
| 单岗位临时口径 | `CAREER/applications/active/<岗位>.md` | 某个团队问“多维表格 → Dify → 写回表格”的场景题 |
| 多个岗位都会问的技术题 | `CAREER/interview-bank/technical/<question>.md` | MCP schema / LangGraph state / Agent evaluation 指标 |
| 已经学透、可复用的稳定知识 | `KNOWLEDGE/<domain>/<node>/` + `_self_check` | RAG 文档 chunk、工具鉴权、attention scaling |
| 项目经历追问 | `PROJECTS/work/` 或 `CAREER/interview-bank/behavioral/` | 七牛云 MCP 工具封装具体 case |

`skill-gap.md` 仍可保留，但不再适合作为每日复习入口。它更像长期战略盘点；当前实战准备以 `applications/active` 为入口。
