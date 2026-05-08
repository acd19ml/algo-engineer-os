# 讲义 09 - Linear Programming, LP（线性规划）

**课程**: CS5491: Artificial Intelligence

---

## 1. Motivation（动机）：从搜索到优化

传统搜索算法在树上扩展结点直到抵达 Goal State（目标状态）。  
类似的思想是否可以用于 **Continuous Optimization Problem（连续优化问题）**？

**答案**：可以。Linear Programming（LP，线性规划）利用约束的几何结构，在连续空间中高效地找到最优解。

---

## 2. Motivating Example：Diet Problem（饮食问题）

**目标**：在满足 Nutritional Constraints（营养约束）的前提下，找到**最便宜的饮食组合（Cheapest Diet）**。

| Food（食物） | Cost（成本） | Calories（热量） | Sugar（糖） | Calcium（钙） |
|------|------|------|----|----|
| 炒菜（每盎司） | \$1 | 100 cal | 3 g | 20 mg |
| 奶茶（每液盎司） | \$0.50 | 50 cal | 4 g | 70 mg |

**Health Constraints（健康约束）**：
- 2000 ≤ Calories（热量） ≤ 2500
- Sugar（糖） ≤ 100 g
- Calcium（钙） ≥ 700 mg

**Decision Variables（决策变量）**：
- `x₁` = 炒菜的盎司数
- `x₂` = 奶茶的液盎司数

---

## 3. Optimization Modeling（优化建模）

### 第一步：写出 Constraints（约束）

```text
100x₁ + 50x₂ ≥ 2000    （Calorie Lower Bound，热量下限）
100x₁ + 50x₂ ≤ 2500    （Calorie Upper Bound，热量上限）
3x₁  + 4x₂  ≤ 100      （Sugar Constraint，糖）
20x₁ + 70x₂ ≥ 700      （Calcium Constraint，钙）
```

### 第二步：将所有约束转为 ≤ 形式（把 ≥ 约束两边乘以 -1）

```text
-100x₁ - 50x₂ ≤ -2000
 100x₁ + 50x₂ ≤  2500
   3x₁ +  4x₂ ≤   100
 -20x₁ - 70x₂ ≤  -700
```

### 第三步：写成 Matrix Form（矩阵形式）

**Standard LP Form（标准 LP 形式）**：

```text
min  cᵀx
 x
s.t. Ax ≤ b
```

其中：

```text
A = [[-100, -50],      b = [-2000]     c = [1  ]
     [ 100,  50],          [ 2500]         [0.5]
     [   3,   4],          [  100]
     [ -20, -70]]          [ -700]
```

---

## 4. Linear Programming, LP（线性规划）的定义

**Linear Programming, LP（线性规划）**：
- **Linear Objective Function（线性目标函数）**：`min cᵀx`
- **Linear Constraints（线性约束）**：`Ax ≤ b`（及变形）

| Form（形式） | 表达 |
|------|------|
| **Inequality Form（不等式形式）** | `min cᵀx` s.t. `Ax ≤ b` |
| **General Form（一般形式）** | `min cᵀx` s.t. `Gx ≤ h`, `Ax = b` |
| **Standard Form（标准形式）** | `min cᵀx` s.t. `Ax ≤ b`, `x ≥ 0` |

与 General Optimization（一般优化）相比：

```text
min f₀(x)  s.t. fᵢ(x) ≤ 0,  aᵢᵀx = bᵢ
```

LP 要求 Objective（目标）和 Constraints（约束）都必须是 Linear（线性的）。

---

## 5. Geometric Interpretation（几何解释）

### 在 2D、3D、N 维中的形状

| Dimension（维度） | Equality `ax = b`（等式） | Inequality `ax ≤ b`（不等式） | 多个不等式 |
|------|---------------|------------------|------------|
| 2D | Line（直线） | Half-Plane（半平面） | Polygon（多边形） |
| 3D | Plane（平面） | Half-Space（半空间） | Polyhedron（多面体） |
| N 维 | Hyperplane（超平面） | Half-Space（半空间） | Polytope（多胞体） |

### 关键洞见

> **LP 的最优解一定出现在 Feasible Region（可行域）的某个 Vertex（顶点）上** —— 即若干 Constraint Boundary（约束边界）的交点。

### 寻找顶点的算法思路

1. **Enumerate All Feasible Vertices（枚举所有可行交点）**：计算所有约束交点并筛选 Feasible Points（可行点）（最坏情况指数复杂度）
2. **Simplex Method（单纯形法）**：沿 Polytope（多面体）的边走向更优 Vertex（顶点）（实践中极其高效）
3. **Interior Point Method（内点法）**：在 Feasible Region（可行域）内部沿 "Central Path（中心路径）" 迭代（可证 Polynomial Time（多项式时间）上界）

---

## 6. Cost Contours（目标等高线）

对于目标 `cᵀx = k`，不同的 `k` 对应一族彼此平行的 **Hyperplanes（超平面）**（在 2D 中是直线）。

- 沿 `-c` 方向移动可以减小目标值
- 最优解是沿 `-c` 方向推进时，最后仍与 Feasible Region 有交的那个 **Boundary Point（边界点）**

---

## 7. 求解一个 LP 的步骤（小规模）

根据"最优解在 Vertex 上"的定理，小规模问题可以这样求：

1. 列出所有 Constraint Boundary（约束边界）的交点
2. 检查每个交点是否满足所有约束（Feasible，可行）
3. 在所有 Feasible Vertices（可行交点）上计算 Objective Value（目标值）
4. 返回目标值最小的交点

大规模问题则通常交给：
- **Simplex Method（单纯形法）**
- **Interior Point Method（内点法）**

---

## 8. 与 CSP 和搜索的联系

| Problem Type（问题类型） | 目标 | 路径是否重要？ |
|----------|------|----------------|
| Search（搜索） | 到达 Goal State（目标状态） | 是 |
| CSP | 满足全部 Constraints（约束） | 否 |
| **LP（线性规划）** | **在满足 Linear Constraints（线性约束）的前提下最小化 Objective Cost（目标代价）** | 否，只关心最终解 |

可以视作：

> LP = **CSP + Continuous Variables（连续变量）+ Linear Objective Function（线性目标函数）**

---

## 9. 小结

| Component（组件） | 描述 |
|------|------|
| Decision Variables（决策变量） | `x ∈ ℝⁿ` |
| Objective Function（目标函数） | `min cᵀx`（Linear，线性） |
| Constraints（约束） | `Ax ≤ b`（Linear，线性） |
| Solution Location（解的位置） | 必定位于 Feasible Polytope（可行多面体）的某个 **Vertex（顶点）** |
| Typical Algorithms（典型算法） | Simplex Method（实践中很快）、Interior Point Method（多项式时间） |
