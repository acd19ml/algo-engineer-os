# Node Granularity Policy

这个文档定义 knowledge node 应该拆多大、合多小。

目标是避免两个常见问题：

1. node 太大，大到难以维护
2. node 太小，小到没有独立价值

一个好的 node 应该是：

- reusable
- understandable
- worth linking to

---

## 什么是一个 node

node 是一个可复用的专业知识单元。

它不是任意一段文字。  
它通常应对应这些对象之一：

- concept
- method
- system
- capability
- workflow
- tool
- metric

---

## 粒度原则

### 1. node 应足够小，便于复用

一个好的 node 应能跨这些场景复用：

- multiple projects
- multiple problems
- multiple learning paths

如果一页内容只在某个超长页面内部才有意义，它往往缠得太紧了。

### 2. node 应足够大，值得存在

如果一个 node 小到没有独立身份，那它可能太碎了。

一个 node 至少应能回答：

- what is this?
- why does it matter?
- what does it connect to?

### 3. 区分 topic 与 problem

node 通常表示 topic 或 method。  
problem page 表示 challenge space。

如果对象本质上是问题陈述，就不要硬塞成 node。

### 4. 需要时区分 family 与 member

有时一个 family 值得有一页，而具体成员也值得各自独立。

Example:

- `rope-family` 更适合作为 wiki overview
- `rope`、`mrope`、`interleaved-mrope` 通常更适合作为独立 nodes

### 5. 当内部小节已经可独立复用时，应考虑拆分

如果某一部分内容经常被单独引用，它可能已经值得成为独立 node。

---

## 什么时候一个 node 太大

一个 node 很可能太大，如果它出现这些情况：

- 同时塞了多个本应单独比较的方法
- 把 concept、family overview、system integration 混在一页
- 不同项目只会用到其中完全不同的小节
- 作为单一对象已经很难维护
- 同一页里出现多条彼此独立的 dependency chains

Examples:

- `llm-training-everything`
- `video-modeling-all-methods`
- `transformer-and-all-variants`

这类情况通常应拆成更小 nodes。

---

## 什么时候一个 node 太小

一个 node 很可能太小，如果它出现这些情况：

- 不打开另外三个 tiny nodes 就完全看不懂
- 它没有独立动机
- 它只是另一页里的一个小标题
- 它没有自己的关系网络
- 它几乎不可能成为一个有价值的 link target

Examples:

- `qk-dot-product-only`
- `the-second-step-of-this-one-workflow`
- `one-symbol-definition`

这类情况通常应并回更大的 node。

---

## 新建 node 前的实用检查

在创建新 node 之前，先问自己：

1. 这个对象有没有稳定身份？
2. 我能不能用一段话说清它为什么重要？
3. 它未来会不会跨页面或项目复用？
4. 它有没有自己的 dependencies、alternatives 或 downstream uses？
5. 我以后会不会想直接链接到它？

如果答案大多是 yes，它大概率值得成为一个 node。

---

## 好的例子

大概率适合作为独立 node 的对象：

- `transformer`
- `rope`
- `kv-cache`
- `distributed-training`
- `beam-search`
- `quantization`
- `interleaved-mrope`

大概率暂时不适合作为独立 node 的对象：

- 一个单独的符号定义
- 一个没有更广身份的微小实现技巧
- 一个只存在于某个 workflow 内部的小节

---

## 默认分层模式

如果不确定对象该落哪层，优先按这个模式判断：

- stable reusable topic -> node
- challenge framing -> problem page
- broad synthesis -> wiki page
- bounded execution -> project page
- recurring operational pattern -> work page
- personal uncertainty or interpretation -> thinking page

这套模式能显著减少类别混淆。

---

## 拆分规则

在这些情况下，应考虑拆 node：

- 一页里包含多个独立有意义的想法
- 不同部分值得各自拥有 alternatives 或 comparisons
- 不同部分的 prerequisites 已明显不同
- 维护单页成本已经很高

拆分时建议：

- 如果需要，保留一个更高层入口页
- 显式写清 parent / child links
- 更新 metadata references

---

## 合并规则

在这些情况下，应考虑合并 node：

- 区分本身是人为的
- 小 node 很少能独立发挥作用
- 维护成本已经高于清晰收益
- 读者几乎总是需要两页一起看

不要只为了减少文件数而合并。  
只有在“合并后更清晰”时才这么做。

---

## 总结

一个好的 node 应该是：

- reusable
- meaningful
- linkable
- maintainable
- distinct

目标不是无限碎片化。  
目标是构建一个既容易学习、又容易继续增长的系统。
