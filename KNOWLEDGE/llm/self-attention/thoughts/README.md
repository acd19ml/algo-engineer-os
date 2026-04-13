# Self-Attention 思考

## 1. Current understanding

我当前对 Self-Attention 的理解，重点不应只是“每个 token 看其它 token”。

更重要的是：

- 它允许信息直接跨远距离位置交互
- 它改变了信息传播路径
- 它把很多原本依赖 recurrence 的建模能力，转到了显式相互作用上

## 2. 为什么这个节点值得独立

如果不把 Self-Attention 拆出来，Transformer 节点很容易变得过大。  
而且后面很多路线都会直接复用它：

- long-context routes
- efficient attention
- KV cache related understanding

## 3. 当前判断

Self-Attention 是最值得优先独立理解的机制之一，  
它甚至比“完整 Transformer 架构”更适合作为很多后续学习路径的机制起点。

## 4. 未决问题

- 在工程实践里，人们真正最常关心的是 attention 本身，还是它在 block 里的组合方式？
- 从学习顺序上，应该先彻底理解 Self-Attention，再看 Transformer，还是交替推进更自然？
