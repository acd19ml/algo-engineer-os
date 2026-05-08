# Lecture 10 - Integer Programming & Branch and Bound

**Course**: CS5491: Artificial Intelligence

---

## 1. From LP to Integer Programming

**LP**: variables can be any real values → buy 3.7 oz of stir-fry
**IP**: variables must be **integers** → must buy whole bowls/glasses

**Example**:
- LP: choose amount of stir-fry (ounces) and boba (fluid ounces) — continuous
- IP: choose number of bowls of stir-fry and glasses of boba — **discrete**

---

## 2. Integer Programming (IP) Formulation

```
min  cᵀx
 x
s.t. Ax ≤ b
     x ∈ ℤᴺ      ← integer constraint
```

### Variants

| Type | Constraint | Use Case |
|------|-----------|---------|
| **LP** | `x ∈ ℝᴺ` | Continuous quantities |
| **IP** | `x ∈ ℤᴺ` | Whole numbers only |
| **Binary IP (BIP)** | `x ∈ {0,1}ᴺ` | Yes/no decisions |
| **Mixed Integer LP (MILP)** | Some `xᵢ ∈ ℤ`, others `xᵢ ∈ ℝ` | Mixed decisions |

---

## 3. LP Relaxation

**LP Relaxation**: drop the integer constraint and solve as a regular LP.

```
min  cᵀx        ← same as IP
 x
s.t. Ax ≤ b     ← same as IP
                ← integer constraint REMOVED
```

### Key Properties (for minimization)

Let `y*_IP` = optimal IP objective, `y*_LP` = optimal LP relaxation objective.

| Claim | True? | Reason |
|-------|-------|--------|
| `x*_IP = x*_LP` | **False** | LP solution often non-integer |
| `y*_IP ≤ y*_LP` | **False** | IP is more constrained → higher cost |
| `y*_IP ≥ y*_LP` | **True** | LP feasible set ⊇ IP feasible set |

> **LP relaxation gives a lower bound** on the IP optimal value.

**Connection to A* heuristics**: LP relaxation is like an admissible heuristic — it underestimates the true (integer) cost.

---

## 4. Why Not Just Round the LP Solution?

**Question**: Is it sufficient to round the LP solution to nearby integers?

**Answer**: **No!** The optimal integer solution can be far from the rounded LP solution.

Example: In 2D, the LP optimal vertex might be far from any integer point in the feasible region.

---

## 5. Branch and Bound Algorithm

**Idea**: Recursively split the problem into subproblems by constraining one fractional variable at a time.

### Algorithm

```
function BRANCH_AND_BOUND(LP):
    solve LP relaxation → get solution x*_LP
    if x*_LP is integer: return x*_LP  (feasible integer solution)
    if LP is infeasible: return ∞

    find i such that x*_LP[i] is non-integer
    left_LP  = LP + constraint {xᵢ ≤ floor(x*_LP[i])}
    right_LP = LP + constraint {xᵢ ≥ ceil(x*_LP[i])}

    left_val  = BRANCH_AND_BOUND(left_LP)
    right_val = BRANCH_AND_BOUND(right_LP)

    return min(left_val, right_val)
```

### Pruning (Bounding) Rules — Stop going deeper when:
1. **LP gives an integer solution** → feasible IP solution found
2. **LP objective ≥ best known IP objective** → this branch cannot improve
3. **LP is infeasible** → this branch has no solution

### Visual Intuition
```
                    LP relaxation (root)
                   /                    \
     xᵢ ≤ ⌊x*ᵢ⌋                    xᵢ ≥ ⌈x*ᵢ⌉
      /                                      \
  solve sub-LP                          solve sub-LP
  (prune or branch)                     (prune or branch)
```

---

## 6. Branch and Bound Example

**Diet Problem (Integer version)**:

| Step | Action | Result |
|------|--------|--------|
| 1 | Solve LP relaxation | Get non-integer solution (e.g., x₁=3.5) |
| 2 | Branch on x₁: left (x₁≤3), right (x₁≥4) | Two subproblems |
| 3 | Solve each sub-LP | Get bounds or integer solutions |
| 4 | Prune branches worse than best found | Reduce search |
| 5 | Return best integer solution found | Optimal IP solution |

---

## 7. Complexity Comparison

| Problem | Complexity | Notes |
|---------|-----------|-------|
| LP | Polynomial (Interior Point) | Efficient |
| IP | NP-hard in general | Exponential worst case |
| IP with B&B | Exponential worst case, fast in practice | Most commercial solvers use B&B |

---

## 8. Summary

| Concept | Key Point |
|---------|-----------|
| **IP** | LP + integer constraints |
| **BIP** | IP with binary variables (0/1) |
| **MILP** | Mix of integer and continuous variables |
| **LP Relaxation** | Lower bound on IP objective (for minimization) |
| **Branch and Bound** | Recursively split on fractional variables + prune with LP bounds |
| **Pruning condition** | LP objective ≥ best known IP objective |

> **Key insight**: LP relaxation plays the same role as an admissible heuristic in A* — it gives a lower bound that enables pruning of suboptimal branches.
