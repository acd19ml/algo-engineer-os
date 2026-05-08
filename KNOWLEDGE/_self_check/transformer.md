# Self-Check: Transformer

> 日常自检：从上往下看题，能答出来跳下一题；卡住就点链接跳到知识节点重新学。
> 答案不在这里——答案在链接的节点里。

---

## QKV 三组矩阵设计

- [浅] 朴素自注意力（一组参数都不用，直接 X · X^T）有什么根本问题？同一个向量被迫扮演了哪三个角色？ → `KNOWLEDGE/transformer/qkv-three-matrix-design/`
- [浅] 用图书馆检索系统的比喻，搜索词 / 索引标签 / 书的内容分别对应 Q / K / V 的哪个？ → `KNOWLEDGE/transformer/qkv-three-matrix-design/`
- [中] 如果只给 Q 和 K 投影、V 不投影，问题是什么？用 "The animal didn't cross the street because it was too tired" 这个例子说出来。 → `KNOWLEDGE/transformer/qkv-three-matrix-design/`
- [中] W_Q^T · W_K 这个乘积是几乘几的矩阵？秩最多多少？为什么这是"双重收益"？ → `KNOWLEDGE/transformer/qkv-three-matrix-design/`
- [中] 既然 W_Q^T · W_K 是以乘积出现的，为什么不直接学一个矩阵 W = W_Q^T · W_K 省一组参数？ → `KNOWLEDGE/transformer/qkv-three-matrix-design/`
- [深] 低秩论证依赖 d_k << d_model。如果 d_k 接近 d_model，QKV 分离的设计动机还剩什么？还能 justify 双倍参数吗？ → `KNOWLEDGE/transformer/qkv-three-matrix-design/#open-questions` (open)

## Multi-Head Attention

- [浅] 单头注意力的根本瓶颈是什么？为什么一个 softmax 权重分布承载不了多种关系？ → `KNOWLEDGE/transformer/multi-head-attention/`
- [浅] 用 "小明把妈妈昨天刚买的那个又大又红的苹果吃了" 举例：`吃了` 这个 token 同时需要关注哪三种不同层面的关系？ → `KNOWLEDGE/transformer/multi-head-attention/`
- [中] 多头从 d_model=512 拆成 8 个 d_k=64 的子空间。**总计算量怎么变？信息容量怎么变**？ → `KNOWLEDGE/transformer/multi-head-attention/`
- [中] 拆成多个低维头每个头的表达能力变弱，**为什么换来的远大于失去的**？用全科医生 vs 专科医生的类比说明。 → `KNOWLEDGE/transformer/multi-head-attention/`
- [中] 为什么是在 d_model 维度上拆成多个 d_k 子空间，**而不是直接复制 8 个完整的 512 维头**？回答两点。 → `KNOWLEDGE/transformer/multi-head-attention/`
- [深] BERT 的 attention head 可视化显示**很多头是冗余的**——可以剪枝大量头而性能不显著下降。如果是这样，为什么训练不出更高效的稀疏多头结构？ → `KNOWLEDGE/transformer/multi-head-attention/#open-questions` (open)

## KV Cache

- [浅] 为什么缓存的是 K 和 V，**不是 Q**？自回归生成的不对称性是什么？ → `KNOWLEDGE/transformer/kv-cache/`
- [中] 一个请求的 KV Cache 有多大？给定 40 层 / 32 头 / 头维度 128 / 序列 4096 / FP16，估算结果是多少 GB？ → `KNOWLEDGE/transformer/kv-cache/`
- [中] 大模型推理分 prefill 和 decode 两阶段——**两个阶段分别是 compute-bound 还是 memory-bound**？为什么？ → `KNOWLEDGE/transformer/kv-cache/`
- [中] 为什么说 KV Cache 大小直接决定了能同时服务多少用户？ → `KNOWLEDGE/transformer/kv-cache/`
- [中] 列出 4 种主流 KV Cache 优化方案（MQA / GQA / 量化 / PagedAttention），**它们的核心目标是什么**？ → `KNOWLEDGE/transformer/kv-cache/`
- [深] **为什么 KV Cache 这么"耐量化"**？INT8/INT4 量化对 attention 输出影响很小——这暗示了 attention 的什么性质？ → `KNOWLEDGE/transformer/kv-cache/#open-questions` (open)

---

## 跨节点综合

- [深] QKV 三矩阵的**低秩**正则化和多头的**多子空间**设计在数学上嵌套在一起——它们怎么共同服务于"控制模型复杂度 + 同时捕捉多种关系" 这一目标？ → `KNOWLEDGE/transformer/qkv-three-matrix-design/` + `KNOWLEDGE/transformer/multi-head-attention/`
- [深] **MQA / GQA 让多头共享 K/V**——按 multi-head 的论证，这应该明显损害表达能力，但实际效果损失很小。这暗示什么？是不是多头的真正价值更多在 Q 投影的分化而非 K/V 的分化？ → `KNOWLEDGE/transformer/multi-head-attention/#open-questions` (open) + `KNOWLEDGE/transformer/kv-cache/#open-questions` (open)
