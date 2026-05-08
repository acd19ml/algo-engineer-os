# Self-Check: ML

> 日常自检：从上往下看题，能答出来跳下一题；卡住就点链接跳到知识节点重新学。
> 答案不在这里——答案在链接的节点里。

---

## 表征学习 / XOR

- [浅] 单层线性模型为什么解决不了 XOR？ → `KNOWLEDGE/ml/representation-learning-xor/`
- [中] 如果把多层网络的激活函数全部去掉，能解决 XOR 吗？为什么？ → `KNOWLEDGE/ml/representation-learning-xor/`
- [深] 表征学习的核心动机是什么？为什么说"深度本身不是关键，非线性表示能力才是"？ → `KNOWLEDGE/ml/representation-learning-xor/`

## 梯度流（Gradient Flow）

- [浅] "梯度消失" 准确说是参数变小，还是梯度变小？两者区别是什么？ → `KNOWLEDGE/ml/gradient-flow-deep-networks/`
- [浅] 反向传播为什么是连乘不是连加？ → `KNOWLEDGE/ml/gradient-flow-deep-networks/`
- [中] 一个 20 层网络，每层局部导数 ≈ 0.5。第一层收到的梯度量级估算是多少？ → `KNOWLEDGE/ml/gradient-flow-deep-networks/`
- [中] 前向传播也是逐层计算，为什么前向稳定不等于反向稳定？ → `KNOWLEDGE/ml/gradient-flow-deep-networks/`
- [中] sigmoid 前向输出是有界的 [0, 1]，看起来很稳，为什么反传时还会有梯度消失？ → `KNOWLEDGE/ml/gradient-flow-deep-networks/`
- [深] 梯度消失 / 梯度爆炸 / 梯度裁剪三者的关系是什么？哪两个是同一机制的两个方向，哪一个是另一种思路？ → `KNOWLEDGE/ml/gradient-flow-deep-networks/`

## 初始化和归一化

- [浅] Kaiming 把 Xavier 守的 `n · Var(w) ≈ 1` 改成了 `≈ 2`，为什么？ → `KNOWLEDGE/ml/initialization-and-normalization/`
- [中] 只有初始化没有归一化，为什么训练过程中尺度还是会跑？ → `KNOWLEDGE/ml/initialization-and-normalization/`
- [中] BN 和 LN 的区别用 "固定谁、沿谁收集" 怎么说？把 `[B, F]` 张量当成表格，BN 看哪些数？LN 看哪些数？ → `KNOWLEDGE/ml/initialization-and-normalization/`
- [中] 归一化里 "1" 指的是中心还是尺度？中心和尺度分别接近什么？ → `KNOWLEDGE/ml/initialization-and-normalization/`
- [中] 给三组数 `[1,2]`、`[10,20]`、`[100,200]`，**只减均值**得到什么？再除以标准差呢？为什么"只减均值"还不够？ → `KNOWLEDGE/ml/initialization-and-normalization/`
- [深] BN 训练时沿 batch 收集统计量，**推理时这个 batch 不存在**——通常用 running mean/var 替代。这两个统计量对齐与否对最终行为影响多大？为什么 BN 在小 batch 下表现不稳？ → `KNOWLEDGE/ml/initialization-and-normalization/#open-questions` (open)

## 残差连接

- [浅] 残差连接最直观的设计动机是什么？（不要从 ResNet 论文背） → `KNOWLEDGE/ml/residual-connections/`
- [中] 为什么说残差是给梯度提供 "一条不经过非线性的旁路"？identity 路径上局部导数是多少？ → `KNOWLEDGE/ml/residual-connections/` + `KNOWLEDGE/ml/gradient-flow-deep-networks/`

---

## 跨节点综合

- [深] 初始化、归一化、残差三种方法都缓解梯度问题，但解决的是同一问题在不同时刻 / 不同路径上的表现。说出每种方法管什么时刻 / 什么路径。 → `KNOWLEDGE/ml/gradient-flow-deep-networks/` + `KNOWLEDGE/ml/initialization-and-normalization/` + `KNOWLEDGE/ml/residual-connections/`
- [深] 梯度裁剪是否破坏方向信息？clip-by-norm vs clip-by-value 的选择依据？ → `KNOWLEDGE/ml/gradient-flow-deep-networks/#open-questions` (open)
