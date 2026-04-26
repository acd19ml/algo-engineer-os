# PROBLEMS

问题对比框架层。**不是开放问题跟进、不是面试题库、不是知识自检**——这三个分别由 `KNOWLEDGE/x/Open Questions`、`CAREER/interview-bank/`、`KNOWLEDGE/x/自检题` 承担。

## 这一层的真实作用

把 **"我们到底在解决什么、有哪些候选方案、各自 trade-off"** 沉淀成可复用的横向对比页。

它和 KNOWLEDGE 的区别：

| 层 | 答的问题 | 形状 |
|---|---|---|
| `KNOWLEDGE/x` | "RoPE 是什么、怎么工作" | 单一对象的解释 |
| `PROBLEMS/x` | "长上下文这问题，业界 N 种方案各自 trade-off" | 跨对象横向对比 |

## 触发条件（关键）

**只有当你在某次对话 log 里出现"对比 N 种方案"的内容时，LLM 才在 triage 时建议建一个 PROBLEMS 页**。

如果你的 INBOX 内容是单点学习（单概念、单方法），这一层不该被激活。所以新装系统看到这层是空的，是**对的**。

## 你以后会真用到的场景示例

- `long-context-degradation/` — 长上下文质量退化。候选：RoPE 外推 / YaRN / StreamingLLM / 长上下文 SFT
- `agent-memory-design/` — agent 长程记忆怎么做。候选：context stuffing / mem0 / vector store / episodic
- `tool-selection-at-scale/` — 工具数量多时怎么选。候选：retrieval over tools / hierarchical routing / 你 Neo 那个 3072 维向量 62 工具的方案
- `eval-design-for-long-trace-agent/` — agent 长 trace 怎么评。候选：outcome reward / process reward / partial credit / pairwise

每一项都是面试官常问的"系统设计 / 技术选型"题型。秋招前如果你建了 5-10 个这种页，技术面基本不慌。

## 模板

参考 `META/templates/problem_README.template.md`。

## 引用关系

| 引用方向 | 是否允许 |
|---|---|
| PROBLEMS → KNOWLEDGE | ✓ 每个候选方案对应一个节点 |
| PROBLEMS → INBOX/dialogue_logs | ✓ 来源必填 |
| KNOWLEDGE → PROBLEMS | ✓ 节点可以写"我服务的 problem 页" |
| **PROBLEMS → TRACKS** | ✗ 禁止 |
