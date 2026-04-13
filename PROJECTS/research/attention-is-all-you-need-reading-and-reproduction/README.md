# Attention Is All You Need Reading and Reproduction

## 1. Summary

围绕 Transformer 原始论文进行系统阅读、知识拆解和最小复现。

## 2. Goal

- 读懂论文的问题背景、核心设计和结构逻辑
- 拆出高复用知识节点
- 实现最小版 attention 和 Transformer block
- 形成可复用的知识、问题、项目和职业资产

## 3. Motivation

这个项目的目标不是“完整复现论文全部结果”，  
而是用一篇非常典型的论文，把 Algo Engineer OS 真的跑通一次。

它应该同时连接：

- raw source
- problem page
- knowledge nodes
- repro asset
- later career story

## 4. Scope

### In scope

- 阅读原论文
- 建立 Transformer / Self-Attention / Positional Encoding 节点
- 建立 Sequence Modeling 问题页
- 规划并开始 toy implementation
- 形成一版项目总结

### Out of scope

- 大规模训练完整翻译模型
- 完整 reproduction 原论文全部实验
- 一次性覆盖所有后续 Transformer 变体

## 5. Current status

- reading: active
- node building: active
- toy code: planned
- summary writing: planned

## 6. Related knowledge nodes

- [Transformer](../../../KNOWLEDGE/llm/transformer/README.md)
- [Self-Attention](../../../KNOWLEDGE/llm/self-attention/README.md)
- [Positional Encoding](../../../KNOWLEDGE/llm/positional-encoding/README.md)

## 7. Related problems

- [Sequence Modeling](../../../PROBLEMS/modeling/sequence-modeling/README.md)

## 8. Related repos

- [transformer-from-scratch](https://github.com/yourname/transformer-from-scratch)
- [Repro Index Entry](../../../REPRO_INDEX/external-repos.md)

## 9. Key decisions

- 不追求一开始完整复现原论文训练结果
- 先做最小理解闭环：问题 -> 结构 -> 数学 -> toy code
- 先拆高复用节点，不把所有内容塞进 Transformer 一个页面

## 10. Constraints

- time
- compute
- implementation scope
- current node coverage is still sparse

## 11. Results

当前阶段的产出包括：

- 原始资料入口页
- Sequence Modeling 问题页
- Transformer / Self-Attention / Positional Encoding 节点
- planned toy repo entry

## 12. Lessons learned

到目前为止，最重要的经验不是某个公式本身，  
而是：围绕一篇论文建立 source -> problem -> node -> project 的闭环，比只写一个 node 更能让系统真正运转。

## 13. Reusable outputs

- knowledge nodes
- problem page
- project memory
- repro index entry
- later career story material

## 14. Career value

这个项目可以证明：

- 结构化阅读论文的能力
- 把问题拆成 nodes 和 projects 的能力
- 从概念走向实现的执行能力
- 系统化沉淀知识的能力

## 15. Expected outputs

- 3 个知识节点
- 1 个问题页
- 1 个 external toy repo
- 1 个项目总结
- 1 个 career story 草稿

## 16. Next steps

- 先补 Self-Attention 与 Positional Encoding 节点的核心内容
- 再建立 `transformer-from-scratch` 的最小实现计划
- 最后形成一版项目复盘 / summary
