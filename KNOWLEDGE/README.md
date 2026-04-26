# KNOWLEDGE

结构化知识图谱层。把对话 log 里你真正参与思考的内容沉淀成可复用的节点。

## 这一层是什么

`KNOWLEDGE/` 不是笔记堆放区，也不是百科。它是这个 repo 的 **backbone**：每个节点对应一个稳定、可复用、可被多次引用的主题单元。

它的核心约束：
- **入库源唯一** = `INBOX/<topic>/dialogue_logs/*.md`。课件、ppt、tutorial 等参考材料不入库
- **稀疏 > 饱满**：节点只写对话 log 实际覆盖到的部分。论文里写但你没在对话里推导/纠正/澄清过 ≠ 你学过
- **自检题来源限定**：来自对话 log 中你**实际卡住/问错/被纠正/被要求复述**的位置。LLM 不许拍脑袋出题

## 节点结构

最小（新建只需要这两个）：

```
KNOWLEDGE/{domain}/{node}/
├── README.md     定义 + 要点 + 自检问题 + 关联 + 来源
└── meta.yaml     结构化元数据
```

按需扩展（有内容才建）：

```
├── math/README.md     公式、推导
├── code/README.md     实现笔记、shape、坑
├── refs/README.md     来源链接
└── thoughts/README.md 个人判断、open questions
```

**不要建空文件**。没有内容就不建。

## 模板

参考 `META/templates/node_README.template.md`。

## 节点和其它层的引用关系

| 引用方向 | 是否允许 |
|---|---|
| KNOWLEDGE → KNOWLEDGE | ✓ 节点之间正常互引 |
| KNOWLEDGE → PROBLEMS | ✓ 写"服务的问题页" |
| KNOWLEDGE → RAW_SOURCES | ✓ 写来源 |
| KNOWLEDGE → INBOX/dialogue_logs | ✓ 必填来源 |
| **KNOWLEDGE → TRACKS** | ✗ 禁止。tracks 单向引用 knowledge，knowledge 不感知 tracks |
| **KNOWLEDGE → CAREER** | ✗ 禁止。CAREER 引用 knowledge |

> 这个约束是 source-of-truth 设计的一部分：稳定层（KNOWLEDGE）不依赖不稳定层（TRACKS / CAREER）。

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
└── llm/    （目前为空，等 final 结束后从对话 log 长出来）
```
