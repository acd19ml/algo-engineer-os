# Lecture 09 - Linear Programming

**Course**: CS5491: Artificial Intelligence

---

## 1. Motivation: From Search to Optimization

Search algorithms explore a tree until reaching a goal. Can a similar strategy work for **continuous optimization**?

**Answer**: Yes — LP uses the geometry of constraints to find optimal solutions efficiently.

---

## 2. Motivating Example: The Diet Problem

**Goal**: Find cheapest diet satisfying nutritional constraints.

| Food | Cost | Calories | Sugar | Calcium |
|------|------|----------|-------|---------|
| Stir-fry (per oz) | $1 | 100 cal | 3g | 20mg |
| Boba (per fl oz) | $0.50 | 50 cal | 4g | 70mg |

**Health Constraints**:
- 2000 ≤ Calories ≤ 2500
- Sugar ≤ 100g
- Calcium ≥ 700mg

**Decision variables**: `x₁` = oz of stir-fry, `x₂` = fl oz of boba

---

## 3. Optimization Formulation

### Step 1: Write out constraints
```
100x₁ + 50x₂ ≥ 2000    (min calories)
100x₁ + 50x₂ ≤ 2500    (max calories)
3x₁  + 4x₂  ≤ 100     (sugar)
20x₁ + 70x₂ ≥ 700     (calcium)
```

### Step 2: Convert all to ≤ form (negate ≥ constraints)
```
-100x₁ - 50x₂ ≤ -2000
 100x₁ + 50x₂ ≤  2500
   3x₁ +  4x₂ ≤   100
  -20x₁ - 70x₂ ≤  -700
```

### Step 3: Matrix form
**Standard LP**:
```
min  cᵀx
 x
s.t. Ax ≤ b
```

Where:
```
A = [[-100, -50],      b = [-2000]     c = [1  ]
     [ 100,  50],          [ 2500]         [0.5]
     [   3,   4],          [  100]
     [ -20, -70]]          [ -700]
```

---

## 4. Linear Programming Definition

**Linear Programming (LP)**:
- **Linear objective**: `min cᵀx`
- **Linear constraints**: `Ax ≤ b`

| Form | Formulation |
|------|-------------|
| **Inequality Form** | `min cᵀx` s.t. `Ax ≤ b` |
| **General Form** | `min cᵀx` s.t. `Gx ≤ h`, `Ax = b` |
| **Standard Form** | `min cᵀx` s.t. `Ax ≤ b`, `x ≥ 0` |

As opposed to **general optimization**:
```
min f₀(x)  s.t. fᵢ(x) ≤ 0,  aᵢᵀx = bᵢ
```

---

## 5. Geometric Interpretation

### Shapes in 2D, 3D, N-D

| Dimension | Equality (`ax=b`) | Inequality (`ax≤b`) | System of inequalities |
|-----------|-------------------|--------------------|------------------------|
| 2D | Line | Half-plane | Polygon |
| 3D | Plane | Half-space | Polyhedron |
| N-D | Hyperplane | Half-space | Polytope |

### Key Insight
> **The optimal LP solution is always at a feasible vertex** (intersection of constraint boundaries).

### Algorithms to Find the Vertex
1. **Check all feasible intersections**: enumerate vertices (exponential in worst case)
2. **Simplex**: walk along edges of the polytope toward the optimum (efficient in practice)
3. **Interior Point**: traverse the interior of the feasible region (polynomial time)

---

## 6. Cost Contours

The objective `cᵀx = k` defines **parallel hyperplanes** (lines in 2D) for different values of `k`.

- Moving in direction `-c` decreases the objective
- The optimal solution is the **last feasible point** touched as we sweep in direction `-c`

---

## 7. Solving an LP

**Key theorem**: Optimal solutions lie at **vertices** of the feasible polytope.

**Procedure** (for small problems):
1. Find all intersections of constraint boundaries
2. Check which are feasible
3. Evaluate objective at each feasible intersection
4. Return the minimum

For larger problems, use **Simplex** or **Interior Point** methods.

---

## 8. Connection to CSP and Search

| Problem Type | Goal | Path Matters? |
|-------------|------|---------------|
| Search | Reach goal state | Yes |
| CSP | Satisfy constraints | No |
| **LP** | **Minimize cost** while satisfying linear constraints | No (just the final assignment) |

LP = **CSP + continuous variables + linear objective**

---

## 9. Summary

| Component | Description |
|-----------|-------------|
| Decision variable | `x ∈ ℝⁿ` |
| Objective | `min cᵀx` (linear) |
| Constraints | `Ax ≤ b` (linear) |
| Solution location | Always at a **vertex** of the feasible polytope |
| Algorithms | Simplex (practical), Interior Point (polynomial) |
