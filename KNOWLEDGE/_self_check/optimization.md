# Self-Check: Optimization

> 日常自检：从上往下看题，能答出来跳下一题；卡住就点链接跳到知识节点重新学。
> 答案不在这里——答案在链接的节点里。

---

## L-Smooth / 梯度下降稳定性

- [浅] `L`-光滑性是不是更好的学习率？`L` 和 `α`（学习率）分别是什么性质的量？ → `KNOWLEDGE/optimization/l-smooth-gradient-descent/`
- [中] 光滑性定义里的 `x, y` 为什么是任意两点而不是当前点和下一点？分析 GD 时为什么可以代入 `y = x - α∇f(x)`？ → `KNOWLEDGE/optimization/l-smooth-gradient-descent/`
- [中] 一维例子 `f(x) = (L/2)x²` 中，`α = 1/L` 时 `1 - Lα/2` 等于多少？为什么不是 0？ → `KNOWLEDGE/optimization/l-smooth-gradient-descent/`
- [中] 下降引理里的线性项 `<∇f(x), y-x>` 什么时候才能保证非正？ → `KNOWLEDGE/optimization/l-smooth-gradient-descent/`

## 非凸 GD 收敛

- [浅] 非凸 vs 凸地形的核心差别是什么？非凸下 GD 的保证对象为什么从"全局最优"降级为"梯度小"？ → `KNOWLEDGE/optimization/nonconvex-gd-convergence/`
- [中] 非凸保证写成 `min_{0<=k<T} ||∇f(x_k)||²`——为什么是 `min` 而不是 `||∇f(x_T)||`？后者代表什么、和理论保证有什么区别？ → `KNOWLEDGE/optimization/nonconvex-gd-convergence/`
- [中] 把每步下降不等式求和后，**telescoping** 在做什么？为什么用到 `f*` 是下界这一假设？ → `KNOWLEDGE/optimization/nonconvex-gd-convergence/`
- [中] T 增大让 `min` 上界变小——这是数学保证变强还是实际行为变好？为什么要警惕这两者的差别？ → `KNOWLEDGE/optimization/nonconvex-gd-convergence/`
- [中] 凸+光滑下 GD 是 `O(1/k)` 收敛——这是什么意思？要把误差缩小 10 倍，需要把步数做什么？ → `KNOWLEDGE/optimization/nonconvex-gd-convergence/`

---

## 跨节点综合

- [深] 把 L-光滑性 + 下降引理 + GD 一步代入，能推出 `f(x - α∇f(x)) <= f(x) - α(1 - Lα/2)||∇f(x)||²`。完整推一遍。 → `KNOWLEDGE/optimization/l-smooth-gradient-descent/`
