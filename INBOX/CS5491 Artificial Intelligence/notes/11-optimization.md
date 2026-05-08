# Lecture 11 - Optimization

**Course**: CS5491: Artificial Intelligence

---

## 1. Optimization Problem Definition

**General form**:
```
min  f(x)
 x
s.t. x ∈ F
```

| Component | Symbol | Description |
|-----------|--------|-------------|
| **Optimization variable** | `x ∈ ℝⁿ` | What we optimize over |
| **Feasible set/region** | `F ⊆ ℝⁿ` | Allowed values of `x` |
| **Objective function** | `f: F → ℝ` | What we minimize |
| **Optimal solution** | `x* = argmin_{x∈F} f(x)` | The best feasible point |
| **Optimal value** | `f* = min_{x∈F} f(x) = f(x*)` | The minimum objective value |

---

## 2. Classification of Variables

| Variable Type | Domain | Class |
|---------------|--------|-------|
| **Discrete** | Integers, finite sets | Combinatorial optimization |
| **Continuous** | Real numbers | Continuous optimization |
| **Mixed** | Some discrete, some continuous | Mixed-integer optimization |

---

## 3. Classification of Feasible Sets

| Type | Feasible Set | Notes |
|------|-------------|-------|
| **Unconstrained** | `F = ℝⁿ` | No restrictions |
| **Constrained** | `F ⊊ ℝⁿ` | Finding a feasible point can itself be hard |

---

## 4. Classification of Objectives

| Objective | Type |
|-----------|------|
| `f(x) = 1` | **Feasibility problem** (just find any feasible point) |
| `f(x) = aᵀx` | **Linear** |
| `f(x) = convex function` | **Convex optimization** |
| `f(x) = arbitrary` | **General/Nonlinear** |

### Min ↔ Max Conversion
```
max g(x) = min -f(x)     where g(x) = -f(x)
```
Same optimal solution; optimal values are negatives: `g* = -f*`

---

## 5. Classic Optimization Examples

### 5.1 Traveling Salesman Problem (TSP)

- **Variable** `x`: ordered list of cities (permutation)
- **Feasible set**: `F = {x : each city visited exactly once}`
  - `F = {x : xᵢ ∈ {1,...,n}ⁿ; Σₖ I(xₖ=i)=1, ∀i}`
- **Objective**: total distance
  - `f(x) = Σₖ₌₁ⁿ⁻¹ d(xₖ, xₖ₊₁) + d(xₙ, x₁)`

### 5.2 N-Queens Problem

**Formulation 1** (Column-based):
- Variable `xᵢ` = row of queen in column `i`
- `F = {x : xᵢ ≠ xⱼ, |xᵢ - xⱼ| ≠ |i-j|, ∀i≠j}`
- Objective `f(x) = 1` (feasibility only)

**Formulation 2** (Coordinate-based):
- Variables `(xᵢ, yᵢ)` = row/column of i-th queen
- More complex feasibility constraints

### 5.3 Linear Regression

**Problem**: Find `a` such that `yᵢ ≈ axᵢ` for all data points

| Data | `x` | `y` |
|------|-----|-----|
| Point 1 | 1.0 | 2.1 |
| Point 2 | 2.0 | 3.98 |
| Point 3 | 3.0 | 7.0 |

**Two formulations**:

L1 loss: `min_a Σᵢ |yᵢ - axᵢ|`

L2 loss (least squares): `min_a Σᵢ (yᵢ - axᵢ)²`

---

## 6. How to Solve Optimization Problems?

> **No general algorithm exists.** We use specialized algorithms for specific problem classes.

### Problem Hierarchy

```
General Optimization
└── Convex Optimization (CO)
    └── Linear Program (LP)
        └── (Mixed) Integer Linear Program (MILP)
    └── Quadratic Program (QP)
    └── Semidefinite Program (SDP)
    └── Second-Order Cone Program (SOCP)
```

### Existing Solvers

| Solver | Problem Types |
|--------|--------------|
| **Cplex** | LP, MILP, QP |
| **Gurobi** | LP, MILP, MIQP |
| **GLPK** | LP, MILP (open source) |
| **Cvxopt** | Convex optimization (Python) |
| **MOSEK** | QP, SOCP |
| **DSDP5** | SDP |

---

## 7. Why Formulate as Optimization?

> **"Lazy mode"** workflow:
> 1. Formulate the problem as an optimization problem
> 2. Identify which **class** it belongs to (LP, IP, convex, etc.)
> 3. Call the corresponding **solver**
> 4. Done!

**Key benefit**: Decouple **representation** from **problem solving**.
- You describe *what* you want, the solver figures out *how* to find it.

---

## 8. Summary Table

| Problem | Variables | Objective | Constraints | Solver |
|---------|-----------|-----------|------------|--------|
| LP | Continuous | Linear | Linear | Simplex, Interior Point |
| IP/MILP | Integer/Mixed | Linear | Linear | Branch & Bound |
| QP | Continuous | Quadratic | Linear | Active set, Interior Point |
| Convex | Continuous | Convex | Convex | Gradient descent, Interior Point |
| General NLP | Continuous | Arbitrary | Arbitrary | No guarantee |
| TSP | Discrete | Sum of distances | Permutation | Heuristics, B&B |
