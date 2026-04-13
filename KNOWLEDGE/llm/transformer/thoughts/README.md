# Transformer 思考

## 1. Current understanding
我当前对 Transformer 的理解，不应只停留在“它用了 attention”。

更重要的是：
- 它把序列建模从递归路径切换到了全局交互路径
- 它更适合并行训练
- 它把“位置关系如何表达”这个问题从结构里拆出来，交给显式位置编码处理
- 它因此也把一些新的问题暴露出来，比如长上下文复杂度问题

## 2. Why this node matters in my system
Transformer 应该是一个高复用节点，因为它会被这些路径反复引用：
- LLM 路径
- MLLM 路径
- ViT 路径
- long-context 路径
- inference optimization 路径
- [Attention Is All You Need Reading and Reproduction 项目](../../../../PROJECTS/research/attention-is-all-you-need-reading-and-reproduction/README.md)

如果这个节点写得太差，后面很多路径都会模糊。

## 3. Current concerns
- 这个节点很容易写得过大，最后把 self-attention、positional encoding、decoder-only 变体都混进去
- 如果粒度控制不好，Transformer 节点会变成一个“什么都有一点”的入口页，而不是一个清晰的 reusable node

## 4. Current judgment
我更倾向于把 Transformer 保持为“架构级入口节点”，然后把这些内容拆出去：
- self-attention
- positional encoding
- decoder-only LLM structure
- efficient attention / long-context routes

这样后续复用会更强。

## 5. Open questions
- 对于职业成长来说，理解 Transformer 到什么程度才算“够用”？
- 是需要完整手推，还是做到能讲清结构 + 写 toy code + 理解关键 trade-off 就可以？
- 在面试和工作里，最常被真正问到的 Transformer 深度到底是什么层次？
