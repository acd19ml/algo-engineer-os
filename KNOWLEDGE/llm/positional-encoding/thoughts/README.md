# Positional Encoding 思考

## 1. Current understanding

Positional Encoding 在我当前系统里很重要，因为它把一个容易被忽略的问题单独暴露出来：

attention 很强，但顺序并不会自动出现。

也就是说，Transformer 把“如何建模顺序”从结构里剥离出来了。

## 2. 为什么值得独立成节点

如果不把这个对象独立出来，后面很多路径会混掉：

- base Transformer
- RoPE
- multimodal position design
- long-context routes

这个节点的高复用性很强，不适合只作为 Transformer 的一个小节。

## 3. 当前判断

Positional Encoding 应作为一个中等抽象层级的入口节点：

- 不要太窄，只讲原论文的 sinusoidal version
- 也不要太宽，一开始就吞掉所有 rotary / relative / multimodal variants

## 4. 未决问题

- 从学习顺序上，是先掌握原始 sinusoidal encoding，再扩展到 RoPE，还是可以直接跳？
- 在实际工作和面试里，人们更关心“为什么需要位置表示”，还是更关心“具体哪种方案更好”？
