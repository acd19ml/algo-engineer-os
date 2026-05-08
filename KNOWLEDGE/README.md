# KNOWLEDGE

结构化知识图谱层。把对话 log 里你真正参与思考的内容沉淀成可复用的节点。

## 这一层是什么

`KNOWLEDGE/` 不是笔记堆放区，也不是百科。它是这个 repo 的 **backbone**：每个节点对应一个稳定、可复用、可被多次引用的主题单元。

它的核心约束：
- **入库源限定** = `INBOX/<topic>/dialogue_logs/` 和 `internalized/`。课件、ppt、tutorial 等参考材料不入库（详见 `META/llm/triage.md`）
- **节点是自含 artifact**：节点 / `meta.yaml` 不引用 INBOX 路径——INBOX 是临时层，可删
- **形态：因果叙述 + 反事实推导**：不是 bullet 摘要。读者完全忘了能从节点重新学回来。详见 `META/policies/node_form.md`
- **稀疏 > 饱满**：节点只写来源材料实际推导/澄清/纠正过的内容
- **自检题独立于节点**：在 `KNOWLEDGE/_self_check/<domain>.md`，浅 → 深排序、链接到节点

## 节点结构

最小（新建只需要这两个）：

```
KNOWLEDGE/{domain}/{node}/
├── README.md     因果叙述形态的节点正文（详见 META/policies/node_form.md）
└── meta.yaml     结构化元数据（不含 INBOX 路径）
```

按需扩展（有内容才建）：

```
├── math/README.md     公式、推导
├── code/README.md     实现笔记、shape、坑
├── refs/README.md     来源链接
└── thoughts/README.md 个人判断、open questions
```

**不要建空文件**。没有内容就不建。

自检题不在节点内——在 `KNOWLEDGE/_self_check/<domain>.md`。

## 形态规则 + 模板

写节点前必读：

- 抽象规则：`META/policies/node_form.md`
- 具体范例：`META/llm/few_shots/node_form.example.md`
- 占位骨架：`META/templates/node_README.template.md`

## 节点和其它层的引用关系

| 引用方向 | 是否允许 |
|---|---|
| KNOWLEDGE → KNOWLEDGE | ✓ 节点之间正常互引 |
| KNOWLEDGE → PROBLEMS | ✓ 写"服务的问题页" |
| KNOWLEDGE → RAW_SOURCES | ✓ 写来源 |
| **KNOWLEDGE → INBOX** | ✗ 禁止（artifact 必须自含，INBOX 可删） |
| **KNOWLEDGE → TRACKS** | ✗ 禁止。tracks 单向引用 knowledge |
| **KNOWLEDGE → CAREER** | ✗ 禁止。CAREER 引用 knowledge |
| **KNOWLEDGE → _self_check** | ✗ 禁止。_self_check 单向链接到 KNOWLEDGE |
| **KNOWLEDGE → PODCAST** | ✗ 禁止。PODCAST 单向 mirror KNOWLEDGE |

> 这个约束是 source-of-truth 设计的一部分：稳定层（KNOWLEDGE）不依赖不稳定层（TRACKS / CAREER / PODCAST / _self_check / INBOX）。

## 节点粒度

参考 `META/policies/node_granularity.md`。简单判断：4 题答 3 个"是"才建独立节点。
1. 有稳定独立 identity？
2. 一句话能说清为什么重要？
3. 会被多个项目/问题/track 引用？
4. 有自己的前置依赖、替代方案、下游用途？

## 命名

lowercase kebab-case。canonical term 优先（`kv-cache`、`rope`、`rag`）。详见 `META/policies/naming_convention.md`。

## 当前域

```
KNOWLEDGE/
├── _self_check/        自检题 deck（按 domain 组织）
├── llm/
├── methodology/        学习 / 答题方法这类 meta-skill
├── ml/
├── nlp/
├── optimization/
├── pytorch/
├── transformer/
└── vision/
```
