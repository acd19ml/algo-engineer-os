# 讲义 12 - Convex Optimization（凸优化）

**课程**: CS5491: Artificial Intelligence

---

## 1. Convex Optimization Problem（凸优化问题）的定义

**Convex Optimization Problem（凸优化问题）**：

```text
min  f(x)
 x
s.t. x ∈ F
```

其中：
- `f` 是一个 **Convex Function（凸函数）**
- `F` 是一个 **Convex Set（凸集合）**

---

## 2. Convex Combination（凸组合）

对 `x, y ∈ ℝⁿ`，它们的 **Convex Combination（凸组合）** 定义为：

```text
z = θx + (1-θ)y,   θ ∈ [0, 1]
```

- 当 `θ ∈ (0,1)` 时，`z` 严格位于 `x` 和 `y` 之间（Strict Convex Combination，严格凸组合）

---

## 3. Convex Sets（凸集合）

### 定义

集合 `F` 是 **Convex（凸的）**，当且仅当：

```text
∀x, y ∈ F, ∀θ ∈ [0,1]:  z = θx + (1-θ)y ∈ F
```

### 直观理解

> 取集合中任意两点，连 Line Segment（线段），如果整条线段完全位于集合内部，则该集合是 **Convex Set（凸集合）**。

| Set（集合） | Convex?（是否凸？） |
|------|----------|
| `ℝⁿ` | **是** |
| `∅`（Empty Set，空集） | **是**（True by Vacuous Truth，真空成立） |
| Single Point（单点）`{x₀}` | **是** |
| Intersection（两个凸集合的交）`F₁ ∩ F₂` | **是** |
| Union（两个凸集合的并）`F₁ ∪ F₂` | **不一定是** |
| Integer Lattice（整数格点）`ℤⁿ` | **不是**（如 `0.5×0 + 0.5×1 = 0.5 ∉ ℤ`） |

---

## 4. Convex Functions（凸函数）

### 定义

给定一个 Convex Set `F`，若 `f: F → ℝ` 满足：

```text
∀x, y ∈ F, ∀θ ∈ [0,1]:  f(θx + (1-θ)y) ≤ θf(x) + (1-θ)f(y)
```

则称 `f` 在 `F` 上是 **Convex Function（凸函数）**。

### 直观理解

> 在图像上，连接 `(x, f(x))` 和 `(y, f(y))` 的 Chord（弦），总是在函数曲线**上方或重合（Above or On the Curve）**。  
> 可以理解为 "Bowl-Shaped（碗状向上）" 的形状。

### Concave Functions（凹函数）

若 `-f` 为 Convex Function（凸函数），则 `f` 为 **Concave Function（凹函数）**：

```text
f(θx + (1-θ)y) ≥ θf(x) + (1-θ)f(y)
```

> Maximizing a Concave Function（最大化一个凹函数）+ Convex Feasible Set（凸可行集）⇔ Minimizing a Convex Function —— 仍然属于 Convex Optimization（凸优化问题）。

---

## 5. 如何证明一个函数是 Convex（凸的）？

### Method 1（方法 1）：按定义直接验证（By Definition）

直接验证

```text
f(θx + (1-θ)y) ≤ θf(x) + (1-θ)f(y)
```

在许多简单函数上可以用 Algebraic Calculation（代数计算）证明。

### Method 2（方法 2）：利用 Convex Function Properties（凸函数的性质）

| Property（性质） | 说明 |
|------|------|
| **Non-Negative Weighted Sum（非负权重和）** | 若 `fᵢ(x)` 都是凸函数，且 `wᵢ ≥ 0`，则 `Σ wᵢ fᵢ(x)` 也是凸的 |
| **Linear Transformation Preserves Convexity（线性变换保持凸性）** | 若 `g(x)` 凸，则 `f(x) = g(Ax+b)` 也是凸的 |
| **1D Second Derivative Test（一维二阶导数判别）** | 单变量 `f` 在区间 `[a,b]` 上，若 `f''(x) ≥ 0`，则在该区间上凸 |

### Method 3（方法 3）：Hessian Matrix Test（海森矩阵判别，多维）

对二阶连续可导函数 `f: ℝⁿ → ℝ`：

```text
f 在 F 上凸  ⟺  在 F 的内部所有点 x 上，Hessian H(x) 为 PSD（半正定）
```

**Hessian Matrix（海森矩阵）**：

```text
H(x) = [∂²f/∂xᵢ∂xⱼ]   （所有 Second-Order Partial Derivatives（二阶偏导数）组成的矩阵）
```

**Positive Semidefinite, PSD（正半定）**：

```text
∀z ∈ ℝⁿ:  zᵀH(x)z ≥ 0
```

等价说法：所有 Eigenvalues（特征值）均不为负。

### Quiz：常见函数的 Convexity（凸性）

| Function（函数） | Convexity（凸性） | 理由 |
|------|------|------|
| `eᵃˣ, a ∈ ℝ` | **Convex（凸）** | `f''(x) = a² eᵃˣ ≥ 0` |
| `log x, x>0` | **Concave（凹）** | `f''(x) = -1/x² < 0` |
| `‖x‖₂ = √(Σxᵢ²)` | **Convex（凸）** | Norm Convexity（范数凸），可直接应用性质 |
| Bilinear `xᵀAy` | 一般既非凸也非凹 | 在 `(x,y)` 上不满足凸定义 |
| `x³, x ∈ ℝ` | 既非 Global Convex（全局凸）也非全局凹 | `f''(x) = 6x`，在 `x<0` 时为负 |

---

## 6. Key Theorem（关键定理）：Local Optimum = Global Optimum（局部最优 = 全局最优）

> **定理**：在 Convex Optimization Problem（凸优化问题）中，**任意 Local Optimum（局部最优点）都是 Global Optimum（全局最优点）**。

| 概念 | 定义 |
|------|------|
| **Global Optimum（全局最优）** | `x* ∈ F`，使得对所有 `y ∈ F` 有 `f(x*) ≤ f(y)` |
| **Local Optimum（局部最优）** | 存在 Radius（半径）`R>0`，在球 `‖x-y‖ ≤ R` 内所有 Feasible Points（可行点）`y` 满足 `f(x) ≤ f(y)` |

**Significance（重要性）**：
- 对 Non-Convex Problems（非凸问题），Gradient Descent（梯度下降）等方法可能被 **Local Minimum（局部最小值）** 困住
- 对 Convex Problems（凸问题），只要找到一个 Local Minimum，就已经是 Global Minimum → Convergence（收敛）更有保障

---

## 7. Gradient & Gradient Descent（梯度与梯度下降）

### Gradient（梯度）

对 `f: ℝⁿ → ℝ`，其 Gradient（梯度）定义为：

```text
∇f(x) = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]ᵀ
```

- Gradient Direction（梯度方向）是函数值 **Increases Fastest（增长最快）** 的方向
- Negative Gradient（负梯度）`-∇f(x)` 是函数值 **Decreases Fastest（下降最快）** 的方向

### Unconstrained Gradient Descent（无约束梯度下降算法）

```text
Initialize（初始化）：x₀ （例如 x₀ = 0）
Repeat until Convergence（重复直到收敛）：
    x_{t+1} = xₜ - α · ∇f(xₜ)
```

其中：
- `α > 0` 为 **Step Size（步长）/ Learning Rate（学习率）**
- Convergence Condition（收敛条件）示例：`‖x_{t+1} - xₜ‖ ≤ ε`

### Step Size Selection（步长的选择）

- **Too Large（过大）**：可能在 Optimal Point（最优点）附近 Oscillate（震荡）或 Diverge（发散）
- **Too Small（过小）**：Convergence（收敛）非常缓慢
- 常见策略：Fixed Step Size（固定步长）、Decreasing Step Size（递减步长）、或使用 **Line Search（线搜索）** 每步 Adaptive（自适应）选择最佳步长

### Projected Gradient Descent, PGD（投影梯度下降）

针对 Constrained Problem（有约束问题）`min f(x) s.t. x ∈ F`：

```text
x_{t+1} = P_F(xₜ - α · ∇f(xₜ))
```

其中 `P_F(x)` 是将点 `x` Projected（投影）到 Feasible Set `F` 上的算子：

```text
P_F(x) = argmin_{x'∈F} ‖x - x'‖₂
```

---

## 8. Solving Methods Overview（求解方法概览）

| Scenario（场景） | Method（方法） |
|------|------|
| Unconstrained + Differentiable（无约束 + 可微） | Gradient Descent、求解 `∇f=0`、Closed-Form Solution（解析解） |
| Unconstrained + Twice Differentiable（无约束 + 二阶可微） | Newton's Method（Newton 法，未在课上展开） |
| Constrained + Differentiable（有约束 + 可微） | Projected Gradient Descent, PGD 等 |
| General Convex Constraints（一般凸约束） | Interior Point Method（内点法）等 |
| Non-Differentiable（不可微） | ε-Subgradient Method（ε-次梯度法）、Cutting Plane Method（切平面法）等 |

---

## 9. Convex Optimization Practice Workflow（凸优化的实践工作流）

1. **Problem Formulation（建模问题）**：
   - 明确 Variable `x`（变量）、Feasible Set `F`（可行集）、Objective Function `f`（目标函数）
   - 证明或确认 `f` Convex（凸）、`F` Convex（凸）（确保是 Convex Problem（凸问题））
2. **Call Solver（调用求解器）**：
   - Python：`cvxpy`, `cvxopt`
   - MATLAB：`fmincon`, `cvx`
3. **Map Solution Back（将数值解映射回原问题）**，解释其含义

示例（Python + `cvxpy`）：

```python
import cvxpy as cp

x = cp.Variable(n)
objective = cp.Minimize(c.T @ x)
constraints = [A @ x <= b]
problem = cp.Problem(objective, constraints)
problem.solve()
print(x.value)
```

---

## 10. Convex Optimization in AI（凸优化在 AI 中的作用）

| AI Application（AI 应用） | Convex Optimization Form（凸优化形式） |
|---------|------------|
| Linear Regression with L2（线性回归，L2） | Least Squares（最小二乘），Quadratic Convex Optimization（二次凸优化） |
| Support Vector Machine, SVM（支持向量机） | Quadratic Programming, QP（二次规划）问题 |
| Lasso / Ridge Regression（Lasso / Ridge 回归） | Convex Optimization with L1 / L2 Regularization（带 L1 / L2 正则项的凸优化） |
| Neural Network Training（神经网络训练） | **通常为 Non-Convex（非凸）** —— 只保证找到 Local Optimum（局部最优） |
| LP / IP Problems | LP 是 Convex Optimization 的特例；IP 则是带 Integer Constraints（整数约束）的扩展 |

> **关键区分**：许多"经典机器学习"模型可表述为 Convex Optimization，因此有 Global Optimum Guarantee（全局最优保证）；而大部分深度学习模型对应的是 Non-Convex Optimization（非凸优化），只能期望找到"足够好"的 Local Solution（局部解）。

---

## 11. 小结

| 概念 | 关键点 |
|------|--------|
| Convex Set（凸集合） | 任意两点 Line Segment（连线）完全位于集合内 |
| Convex Function（凸函数） | 函数图像总在任意两点 Chord（连线）之下 |
| Hessian PSD（海森矩阵正半定） | 对二阶可微函数，Hessian PSD ⇔ Convex（凸） |
| Local Optimum = Global Optimum（局部最优 = 全局最优） | Convex Optimization 最强大的性质之一 |
| Gradient Descent（梯度下降） | 沿着 `-∇f` 方向迭代，Step Size `α` 控制更新幅度 |
| Projected Gradient Descent, PGD（投影梯度下降） | 每步更新后 Project（投影）回 Feasible Set（可行集） |
