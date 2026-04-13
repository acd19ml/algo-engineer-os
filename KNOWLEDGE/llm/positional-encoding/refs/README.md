# Positional Encoding 参考资料

## Core reference

### Attention Is All You Need

- Vaswani et al.
- 这是 position signal 在 Transformer 中的原始入口之一
- 应重点回看：
  - positional encoding 的设计动机
  - 为什么要补顺序信息

## Later references to revisit

- learned positional embedding 路线
- relative position encoding
- rotary position encoding（RoPE）
- long-context 相关位置表示路线

## Current notes

- 这个节点必须保持比 RoPE 更上层
- 它的价值不在于“只解释原论文做法”，而在于成为 position family 的稳定入口
