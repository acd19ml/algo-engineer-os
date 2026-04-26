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
