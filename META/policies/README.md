# Policies

仓库级稳定规则。减少长期维护中的漂移。

## 形态规则（LLM 在写各类内容前必读）

| 文件 | 作用 |
|---|---|
| [node_form.md](./node_form.md) | KNOWLEDGE 节点的因果叙述形态规则 + Open Questions 规则（**写节点前必读**） |
| [self_check.md](./self_check.md) | `_self_check/<domain>.md` 自检题 deck 的格式、来源、答案规则 |
| [podcast_script.md](./podcast_script.md) | PODCAST 播客脚本的听觉形态规则 |

## 结构规则

| 文件 | 作用 |
|---|---|
| [source_of_truth.md](./source_of_truth.md) | 信息冲突时的优先级 |
| [naming_convention.md](./naming_convention.md) | 目录、文件、节点的命名规则 |
| [node_granularity.md](./node_granularity.md) | 节点该拆多细、合多大 |

## 配套 few-shots

形态规则之后还有具体范例，在 `META/llm/few_shots/`：

| 范例 | 配套规则 |
|---|---|
| `META/llm/few_shots/node_form.example.md` | node_form.md |
| `META/llm/few_shots/podcast_script.example.md` | podcast_script.md |

抽象规则 + 具体范例两边都读，写出来的内容才不会形似神不似。
