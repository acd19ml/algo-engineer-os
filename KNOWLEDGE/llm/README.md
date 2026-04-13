# LLM

`KNOWLEDGE/llm/` 用于组织与 large language models 相关的知识节点。

这一层更关注：

- 基础架构
- 训练与推理机制
- 长上下文与效率问题
- 模型变体
- 与多模态系统的连接

这个目录的作用，不是把所有 LLM 内容揉成一页，  
而是逐步拆出可复用、可链接、可被路径与项目反复调用的 nodes。

---

## 这个目录适合放什么

当前优先建立的第一批 nodes：

- [Transformer](./transformer/README.md)
- [Self-Attention](./self-attention/README.md)
- [Positional Encoding](./positional-encoding/README.md)

---

## 维护原则

- 保持 node 粒度清晰
- family overview 尽量放到 `WIKI/`
- 结构关系优先写入 `meta.yaml`
- 数学、实现、资料、个人判断尽量分层

---

## 当前示例

当前目录下的第一批标准样板节点是：

- [Transformer](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/llm/transformer/README.md)
- [Self-Attention](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/llm/self-attention/README.md)
- [Positional Encoding](/Users/mac/studyspace/algo-engineer-os/KNOWLEDGE/llm/positional-encoding/README.md)
