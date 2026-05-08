# 讲义 11 - Optimization（优化）

**课程**: CS5491: Artificial Intelligence

---

## 1. Optimization Problem（优化问题）的定义

**General Form（一般形式）**：

```text
min  f(x)
 x
s.t. x ∈ F
```

| Component（组件） | Symbol（符号） | 描述 |
|------|------|------|
| **Optimization Variable（优化变量）** | `x ∈ ℝⁿ` | 我们要对它进行优化的对象 |
| **Feasible Set / Feasible Region（可行集 / 可行域）** | `F ⊆ ℝⁿ` | `x` 被允许取的所有值 |
| **Objective Function（目标函数）** | `f: F → ℝ` | 想要最小化的函数 |
| **Optimal Solution（最优解）** | `x* = argmin_{x∈F} f(x)` | 在 Feasible Region 中使目标最小的点 |
| **Optimal Value（最优值）** | `f* = min_{x∈F} f(x) = f(x*)` | 目标函数的最小值 |

---

## 2. 按 Variable Type（变量类型）分类

| Variable Type（变量类型） | Domain（定义域） | Problem Category（问题类别） |
|----------|--------|----------|
| **Discrete Variable（离散变量）** | Integers, Finite Set（整数、有限集合） | Combinatorial Optimization（组合优化） |
| **Continuous Variable（连续变量）** | Real Numbers（实数） | Continuous Optimization（连续优化） |
| **Mixed Variable（混合变量）** | 部分 Discrete（离散）、部分 Continuous（连续） | Mixed-Integer Optimization（混合整数优化） |

---

## 3. 按 Feasible Set（可行集）分类

| Type（类型） | Feasible Set（可行集） | 说明 |
|------|--------|------|
| **Unconstrained Optimization（无约束优化）** | `F = ℝⁿ` | 对 `x` 没有任何限制 |
| **Constrained Optimization（有约束优化）** | `F ⊊ ℝⁿ` | 找到一个 Feasible Point（可行点）本身就可能不易 |

---

## 4. 按 Objective Function（目标函数）分类

| Objective Type（目标类型） | 示例 |
|----------|------|
| `f(x) = 1` | **Feasibility Problem（可行性问题）**：只要找到任何一个 Feasible Point（可行点）即可 |
| `f(x) = aᵀx` | **Linear Objective（线性目标）** |
| `f(x)` 为 Convex Function（凸函数） | **Convex Optimization Problem（凸优化问题）** |
| `f(x)` 任意 | **General / Nonlinear Optimization（一般 / 非线性优化）** |

### Minimization vs. Maximization（最小化与最大化）的等价转换

```text
max g(x)   等价于   min -f(x)    其中 g(x) = -f(x)
```

二者 Optimal Solution（最优解）相同，Optimal Value 满足 `g* = -f*`。

---

## 5. Classic Optimization Examples（经典优化示例）

### 5.1 Traveling Salesman Problem, TSP（旅行商问题）

- **Variable `x`（变量）**：城市的 Visiting Order（访问顺序，一个排列）
- **Feasible Set（可行集）**：每个城市恰好访问一次的所有排列
  ```text
  F = {x : x ∈ {1,...,n}ⁿ, 且对每个城市 i 有 Σₖ I(xₖ = i) = 1}
  ```
- **Objective Function（目标函数）**：Total Travel Distance（总旅行距离）
  ```text
  f(x) = Σₖ₌₁ⁿ⁻¹ d(xₖ, xₖ₊₁) + d(xₙ, x₁)
  ```

### 5.2 N-Queens Problem（N 皇后问题）

**Form 1（形式 1，Column as Variable，列为变量）**：
- 变量：`xᵢ` = 第 i 列中皇后所在的行（Row）
- Feasible Region（可行域）：
  ```text
  F = {x : xᵢ ≠ xⱼ 且 |xᵢ - xⱼ| ≠ |i - j|, ∀ i ≠ j}
  ```
- Objective Function（目标函数）：`f(x) = 1`（纯 Feasibility Problem，只要有解即可）

**Form 2（形式 2，Coordinate as Variable，坐标为变量）**：
- 变量：`(xᵢ, yᵢ)` = 第 i 个皇后的坐标
- 约束更复杂，但思路类似

### 5.3 Linear Regression（线性回归）

**问题**：拟合直线 `y ≈ a x`，使其尽量贴合 Data Points（数据点）。

| 点 | `x` | `y` |
|----|-----|-----|
| 1 | 1.0 | 2.1 |
| 2 | 2.0 | 3.98 |
| 3 | 3.0 | 7.0 |

两种常见形式：

- **L1 Loss（L1 损失）**：

```text
minₐ Σᵢ |yᵢ - a xᵢ|
```

- **L2 Loss / Least Squares（L2 损失 / 最小二乘）**：

```text
minₐ Σᵢ (yᵢ - a xᵢ)²
```

---

## 6. 如何求解 Optimization Problem？

> **不存在一个对所有优化问题都适用的 Universal Algorithm（通用算法）。**  
> 通常是针对特定 Problem Class（问题类）设计专门算法。

### Problem Hierarchy（问题层级结构）

```text
General Optimization（一般优化）
└── Convex Optimization, CO（凸优化）
    └── Linear Program, LP（线性规划）
        └── (Mixed) Integer Linear Program, MILP（混合整数线性规划）
    └── Quadratic Program, QP（二次规划）
    └── Semidefinite Program, SDP（半定规划）
    └── Second-Order Cone Program, SOCP（二阶锥规划）
```

### Common Solvers（常见求解器）

| Solver（求解器） | Supported Problem Types（支持问题类型） |
|--------|--------------|
| **Cplex** | LP, MILP, QP |
| **Gurobi** | LP, MILP, MIQP |
| **GLPK** | LP, MILP（开源） |
| **Cvxopt** | 一般 Convex Optimization（Python） |
| **MOSEK** | QP, SOCP |
| **DSDP5** | SDP |

---

## 7. 为什么要把问题表述为 Optimization Problem？

> **"Lazy Mode（懒人模式）" Workflow（工作流）**：
>
> 1. 把实际问题 Formalize（形式化）成 Optimization Problem  
> 2. 判断它属于哪一类（LP、IP、Convex、Non-Convex 等）  
> 3. 调用相应的现成 Solver（求解器）  
> 4. 得到 Numerical Solution（数值解）

**关键收益**：将"如何求解（How to Solve）"与"需要什么（What to Achieve）"解耦。
- 你只需描述 **Objective & Constraints（目标与约束）**（要什么）
- Solver 负责 **Algorithm & Numerical Implementation（算法与数值实现）**（怎么做）

---

## 8. Summary Table（总结表）

| Problem Type（问题类型） | Variables（变量） | Objective（目标函数） | Constraints（约束） | Typical Solver / Method（典型求解器 / 方法） |
|----------|------|----------|------|--------------------|
| LP（线性规划） | Continuous（连续） | Linear（线性） | Linear（线性） | Simplex Method, Interior Point |
| IP / MILP（整数 / 混合整数线性规划） | Integer / Mixed（整数 / 混合） | Linear（线性） | Linear（线性） | Branch & Bound 等 |
| QP（二次规划） | Continuous（连续） | Quadratic（二次） | Linear（线性） | Active Set, Interior Point |
| Convex（凸优化） | Continuous（连续） | Convex（凸） | Convex（凸） | Gradient Descent（梯度下降）、Interior Point |
| General NLP（一般非线性规划） | Continuous（连续） | Arbitrary（任意） | Arbitrary（任意） | 无通用保证，Heuristic Methods（启发式方法） |
| TSP（旅行商） | Discrete（离散） | Distance Sum（距离和） | Permutation Constraint（排列约束） | Heuristics, B&B, Approximation Algorithms |
