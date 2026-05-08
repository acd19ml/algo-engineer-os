# CS5491 AI — Tutorial Exam #3（L09–L12）

**Spring 2026 | Total: 45 pts | Recommended Time: ~2 hours**

**Name:** __________________ **Student ID:** __________________

---

> **Instructions:** Open-book (physical notes only). Show all algebraic working — answers without justification earn 0. State any additional assumptions clearly.

---

## Section 1 — True / False with Justification *(10 pts, 2 pts each)*

---

**(a)** (2 pts) **T / F** — For a **minimization** Integer Programming (IP) problem, the optimal value of the LP relaxation is always **≤** the optimal IP objective value. (i.e., the LP relaxation provides a lower bound on the IP optimum.)

*Justification:*

&nbsp;

&nbsp;

---

**(b)** (2 pts) **T / F** — To find the optimal IP solution, it is always sufficient to round the LP relaxation solution to the nearest integer values and check feasibility.

*Justification:*

&nbsp;

&nbsp;

---

**(c)** (2 pts) **T / F** — Every local minimum of a convex function, minimized over a convex feasible set, is also a global minimum.

*Justification:*

&nbsp;

&nbsp;

---

**(d)** (2 pts) **T / F** — The intersection of any two convex sets is always a convex set.

*Justification:*

&nbsp;

&nbsp;

---

**(e)** (2 pts) **T / F** — Gradient descent with a sufficiently small fixed step size α is guaranteed to converge to the **global** minimum of any continuously differentiable function f.

*Justification:*

&nbsp;

&nbsp;

---

## Section 2 — Linear Programming & Branch and Bound *(14 pts)*

A factory uses **Machine 1** and **Machine 2** to fulfil production orders. Let:
- x₁ = hours scheduled on Machine 1
- x₂ = hours scheduled on Machine 2

**Production rates** (units per hour):

| Machine | Product A | Product B | Cost ($/hr) |
|---------|-----------|-----------|-------------|
| M1 | 2 | 1 | **$3** |
| M2 | 1 | 2 | **$2** |

The factory must meet **minimum daily orders**: ≥ 12 units of Product A and ≥ 8 units of Product B. Both x₁ and x₂ must be non-negative.

---

### (a) LP Formulation (3 pts)

Write the linear program in standard form. Clearly state the decision variables, objective function, and all constraints.

**Decision variables:**

**Objective** (minimize):

**Subject to:**

---

### (b) Feasible Region and Vertices (3 pts)

The feasible region lives in the first quadrant (x₁ ≥ 0, x₂ ≥ 0). The constraints define two boundary lines.

**(i)** For each constraint (excluding non-negativity), find the two points where it intersects the axes. Describe how to draw the feasible region.

*Constraint 1 axis intercepts:*

*Constraint 2 axis intercepts:*

**(ii)** Find the **three vertices** of the feasible region by computing all pairwise intersections of constraint boundaries. Show all algebra.

| Vertex | Coordinates (x₁, x₂) | Feasibility check |
|--------|----------------------|-------------------|
| V1 (C1 ∩ x₁=0) | | |
| V2 (C2 ∩ x₂=0) | | |
| V3 (C1 ∩ C2) | | |

---

### (c) Optimal LP Solution (2 pts)

Evaluate the objective function at each vertex. Identify the LP optimal solution.

| Vertex | Objective value 3x₁ + 2x₂ |
|--------|---------------------------|
| V1 (0, 12) | |
| V2 (8, 0) | |
| V3 | |

**LP optimal:** x₁\* = ___ x₂\* = ___ **Objective\* =** ___

Is the LP solution integer-valued? ___

---

### (d) LP Relaxation as a Lower Bound (2 pts)

**(i)** Now require x₁, x₂ ∈ ℤ⁺ (non-negative integers). Explain in **one sentence** why the LP optimal value you found in (c) is a **lower bound** on the optimal IP objective.

&nbsp;

**(ii)** Is it valid to simply round the LP solution to the nearest integers to find the IP optimum? Check whether rounding x₁ down (⌊x₁\*⌋) and x₂ down (⌊x₂\*⌋) gives a feasible integer point. Show the constraint check.

&nbsp;

&nbsp;

---

### (e) Branch and Bound (4 pts)

Run one level of Branch and Bound on x₁ (the first fractional variable).

**Root LP solution:** x₁\* = 16/3, x₂\* = 4/3, objective = 56/3 ≈ 18.67

**Left branch** — add constraint x₁ ≤ ⌊16/3⌋ = **5**:

Solve the sub-LP. What is the new feasible point and objective value? (Hint: with x₁=5, find the minimum feasible x₂ from each constraint.)

&nbsp;

&nbsp;

**Right branch** — add constraint x₁ ≥ ⌈16/3⌉ = **6**:

Solve the sub-LP. What is the new feasible point and objective value?

&nbsp;

&nbsp;

**Which branch gives the better (lower cost) integer solution?**

**Optimal IP solution:** x₁ = ___ x₂ = ___ **Objective =** ___

**Is the right branch pruned after the left branch is solved? Why or why not?**

&nbsp;

---

## Section 3 — Optimization Classification & Convexity *(12 pts)*

---

### (a) Problem Classification (4 pts)

For each optimization problem below, state: (i) variable type (continuous/integer/binary), (ii) objective type (linear/quadratic/convex/nonlinear), and (iii) which **class** it belongs to from {LP, IP, BIP, MILP, Convex, General NLP}.

**(i)** min_{x₁,x₂ ∈ ℝ} 3x₁ + 5x₂  subject to  x₁ + x₂ ≤ 10,  x₁ - x₂ ≥ 2,  x₁,x₂ ≥ 0

&nbsp;

**(ii)** min_{x ∈ {0,1}³} 4x₁ + 3x₂ + x₃  subject to  x₁ + x₂ + x₃ ≥ 2

&nbsp;

**(iii)** min_{a,b ∈ ℝ} Σᵢ (yᵢ − axᵢ − b)²  (Least squares regression)

&nbsp;

**(iv)** min_{x ∈ ℝ²} x₁x₂  (minimizing a product of two real variables)

&nbsp;

---

### (b) Convexity of a Univariate Function (5 pts)

Consider the function **f(x) = x⁴ − 4x² + 4** defined on ℝ.

**(i) [1 pt]** Compute f'(x) and f''(x).

&nbsp;

**(ii) [1 pt]** Is f''(x) ≥ 0 for all x ∈ ℝ? Find the exact values of x where f''(x) = 0 and the sign of f''(x) on each interval.

&nbsp;

&nbsp;

**(iii) [1 pt]** Is f convex on ℝ? State your conclusion clearly and cite the test you used.

&nbsp;

**(iv) [2 pts]** Find **all critical points** of f (where f'(x) = 0). Classify each as a local minimum, local maximum, or neither. What is the **global minimum** value of f and where is it achieved?

*(Hint: f(x) can be written as a perfect square.)*

&nbsp;

&nbsp;

---

### (c) Convexity and the Local = Global Theorem (3 pts)

**(i) [1 pt]** If gradient descent is applied to f(x) = x⁴ − 4x² + 4 starting at x₀ = 1 with step size α = 0.1, compute f'(1) and determine the direction of the first gradient step (left or right on the number line). Which critical point does the algorithm converge toward?

&nbsp;

&nbsp;

**(ii) [2 pts]** Now consider a different function g(x) = x⁴ − 4x² (also non-convex) which has:
- a local minimum at x = 0 with g(0) = 0
- local minima at x = ±√2 with g(±√2) = −4

Gradient descent starting near x = 0.1 converges to x = 0 (the local minimum with value 0), **not** to x = ±√2 (the global minima with value −4). Does this violate the **local = global theorem** for convex optimization? Explain precisely.

*(Note: actually g(0)=0 and g'(0)=0 but x=0 is a LOCAL MAXIMUM not minimum for g. Use this to guide your answer.)*

&nbsp;

&nbsp;

&nbsp;

---

## Section 4 — Gradient Descent *(9 pts)*

Consider the function:

$$f(x_1, x_2) = 2x_1^2 + x_2^2 - 2x_1 x_2$$

---

### (a) Gradient Computation and Manual Descent (4 pts)

**(i) [1 pt]** Compute the gradient ∇f(x₁, x₂) = (∂f/∂x₁, ∂f/∂x₂).

&nbsp;

**(ii) [2 pts]** Starting at **x⁰ = (2, 1)** with step size **α = 0.1**, perform **two** gradient descent steps. Fill in the table.

| Step | Current x | ∇f(x) | x_{new} = x − 0.1 · ∇f(x) | f(x_{new}) |
|------|-----------|--------|---------------------------|------------|
| 0 → 1 | (2, 1) | | | |
| 1 → 2 | | | | |

*(For f(x₁,x₂): use f(a,b) = 2a² + b² − 2ab)*

**(iii) [1 pt]** Find the **exact global minimum** by setting ∇f = 0 and solving the system of equations.

&nbsp;

---

### (b) Convexity via Hessian (3 pts)

**(i) [2 pts]** Write the Hessian matrix H of f(x₁, x₂). Then compute:
- det(H)
- The leading principal minor H₁₁

Use these to determine whether H is **positive definite** (PD), positive semidefinite (PSD), or neither. Conclude whether f is convex.

**Hessian H =**

&nbsp;

det(H) = ___, H₁₁ = ___

**H is:** ___  **f is:** ___

**(ii) [1 pt]** Because f is convex (as confirmed above), what does this guarantee about gradient descent starting from **any** initial point x⁰?

&nbsp;

---

### (c) Step Size Analysis (2 pts)

The convergence of gradient descent requires the step size α < 2/λ_max, where λ_max is the largest eigenvalue of the Hessian H.

Given that the eigenvalues of H are λ₁ = 3 − √5 ≈ 0.76 and λ₂ = 3 + √5 ≈ 5.24:

**(i)** What is the maximum safe step size α_max?

&nbsp;

**(ii)** Is our step size α = 0.1 within this safe range? ___

**(iii)** Describe what would happen (qualitatively) if we used α = 5 instead of 0.1.

&nbsp;

---

## Section 5 — Conceptual Synthesis *(Bonus — 5 pts)*

---

**(a) [2 pts] — B&B as Informed Search**

The notes draw an analogy between the LP relaxation in Branch and Bound and **admissible heuristics in A\* search**. Explain this analogy precisely. In particular:
- What does the LP relaxation correspond to in the A\* framework?
- Why must the LP relaxation be a **lower** bound (for minimization) for this analogy to hold?

&nbsp;

&nbsp;

&nbsp;

---

**(b) [3 pts] — Problem Hierarchy**

The course presents a hierarchy: **General NLP ⊇ Convex ⊇ LP ⊇ (no hierarchy with IP)**.

Answer the following:

**(i)** Why is an LP always a convex optimization problem? (Hint: is the LP objective convex? Are the LP constraints defining a convex set?)

&nbsp;

**(ii)** Why is an IP problem generally **not** a convex optimization problem, even though its objective is linear?

&nbsp;

**(iii)** A friend argues: "Since IP is harder than LP, we should just model everything as LP." What is wrong with this argument? Give one real-world scenario that **requires** integer variables.

&nbsp;

&nbsp;

---

*End of Exam — Good Luck!*

---

---

# Answer Key

> ⚠️ Attempt the exam independently before reading.

---

## Section 1 — True / False

### (a) TRUE

The LP relaxation **removes** the integer constraint, making its feasible set a **superset** of the IP feasible set (every integer-feasible point is also LP-feasible, but not vice versa). A larger feasible set can only help minimization — the minimum over a larger set is ≤ the minimum over a smaller set. Therefore y\*\_LP ≤ y\*\_IP. The LP relaxation is a **lower bound** on the IP optimum.

*Analogy from notes:* LP relaxation plays the same role as an admissible heuristic in A\* — it underestimates the true (integer) cost.

### (b) FALSE

The LP relaxation solution (a vertex of the LP polytope) may be far from any integer-feasible point. Rounding to the nearest integer can produce:
1. An **infeasible** point (violates constraints), or
2. A **suboptimal** integer point far from the true IP optimum.

*Example:* If LP optimum is (5.33, 1.33), rounding down to (5, 1) might violate a constraint, and the true IP optimum might be (5, 2) — not adjacent to (5, 1).

### (c) TRUE

This is the **fundamental theorem of convex optimization**. Proof by contradiction: suppose x is a local minimum of f over convex set F but not global. Then ∃ y ∈ F with f(y) < f(x). Since F is convex, the point z = θy + (1−θ)x ∈ F for all θ ∈ (0,1). By convexity of f: f(z) ≤ θf(y) + (1−θ)f(x) < f(x) for any θ ∈ (0,1). But z can be made arbitrarily close to x (take θ → 0), contradicting x being a local minimum.

### (d) TRUE

Let F₁ and F₂ be convex sets. Let x, y ∈ F₁ ∩ F₂ and θ ∈ [0,1]. Since x, y ∈ F₁ and F₁ is convex: θx+(1−θ)y ∈ F₁. Since x, y ∈ F₂ and F₂ is convex: θx+(1−θ)y ∈ F₂. Therefore θx+(1−θ)y ∈ F₁ ∩ F₂. The intersection is convex. ✓

*Note:* The **union** of two convex sets is generally NOT convex (e.g., two disjoint discs — a point between them is in neither).

### (e) FALSE

Gradient descent with small α is guaranteed to converge to the global minimum **only for convex functions**. For non-convex differentiable functions, gradient descent converges to a **local minimum** (or a saddle point), which may not be the global minimum. Example: f(x) = x⁴ − 4x² has two local minima and gradient descent converges to whichever basin of attraction the starting point is in.

---

## Section 2 — LP & Branch and Bound

### (a) LP Formulation

**Decision variables:** x₁ = hours on M1, x₂ = hours on M2 (x₁, x₂ ∈ ℝ⁺)

**Objective:** minimize 3x₁ + 2x₂

**Subject to:**
```
2x₁ + x₂  ≥ 12     (Product A demand)
x₁  + 2x₂ ≥ 8      (Product B demand)
x₁, x₂    ≥ 0      (non-negativity)
```

---

### (b) Feasible Region and Vertices

**Constraint 1** (2x₁ + x₂ = 12):
- x₁=0 → x₂=12: point **(0, 12)**
- x₂=0 → x₁=6: point **(6, 0)**

**Constraint 2** (x₁ + 2x₂ = 8):
- x₁=0 → x₂=4: point **(0, 4)**
- x₂=0 → x₁=8: point **(8, 0)**

*Feasible region:* The region **above** (or on) both lines, combined with x₁,x₂ ≥ 0. It is unbounded toward the upper-right.

**Vertex V3** — intersection of C1 and C2:

From C1: x₂ = 12 − 2x₁. Substitute into C2:
x₁ + 2(12 − 2x₁) = 8 → x₁ + 24 − 4x₁ = 8 → −3x₁ = −16 → **x₁ = 16/3**

x₂ = 12 − 2(16/3) = 12 − 32/3 = 4/3. → **x₂ = 4/3**

| Vertex | Coordinates | Feasibility check |
|--------|-------------|-------------------|
| V1 | (0, 12) | 2×0+12=12≥12✓; 0+24=24≥8✓ |
| V2 | (8, 0) | 2×8+0=16≥12✓; 8+0=8≥8✓ |
| V3 | (16/3, 4/3) | 32/3+4/3=36/3=12✓; 16/3+8/3=24/3=8✓ |

---

### (c) Optimal LP Solution

| Vertex | Objective 3x₁ + 2x₂ |
|--------|----------------------|
| V1 (0, 12) | 0 + 24 = **24** |
| V2 (8, 0) | 24 + 0 = **24** |
| V3 (16/3, 4/3) | 3×16/3 + 2×4/3 = 16 + 8/3 = **56/3 ≈ 18.67** |

**LP optimal: x₁\* = 16/3 ≈ 5.33, x₂\* = 4/3 ≈ 1.33, Objective\* = 56/3 ≈ 18.67**

**Not integer-valued** — both variables are fractional.

---

### (d) LP Relaxation as Lower Bound

**(i)** The LP feasible set includes all real-valued (x₁,x₂) satisfying the constraints, which is a superset of the IP feasible set (integer points only). Since we minimize over a larger set, the LP minimum ≤ IP minimum — making LP an optimistic lower bound.

**(ii)** Round x₁\* = 16/3 ≈ 5.33 down to 5, x₂\* = 4/3 ≈ 1.33 down to 1. Check (5, 1):
- C1: 2×5 + 1 = 11 < 12 ✗ **INFEASIBLE**

Rounding down gives an infeasible point. This confirms rounding is **not sufficient** for finding the IP optimum — it can violate constraints.

---

### (e) Branch and Bound

**Root:** x₁\* = 16/3, x₂\* = 4/3, obj = 56/3. Branch on x₁ (first fractional variable).

**Left branch — add x₁ ≤ 5:**

With x₁ = 5 (at the new boundary):
- C1: 2×5 + x₂ ≥ 12 → x₂ ≥ 2
- C2: 5 + 2x₂ ≥ 8 → x₂ ≥ 1.5

Binding: x₂ ≥ 2. Minimizing cost: set x₂ = 2 (smallest feasible).
**Sub-LP solution: x₁=5, x₂=2. Objective = 15+4 = 19. ✓ Integer!**

**Right branch — add x₁ ≥ 6:**

With x₁ = 6 (at the new boundary):
- C1: 2×6 + x₂ ≥ 12 → x₂ ≥ 0
- C2: 6 + 2x₂ ≥ 8 → x₂ ≥ 1

Binding: x₂ ≥ 1. Minimizing cost: set x₂ = 1.
**Sub-LP solution: x₁=6, x₂=1. Objective = 18+2 = 20. ✓ Integer!**

**Optimal IP solution: x₁ = 5, x₂ = 2, Objective = 19**

**Is right branch pruned?** After the left branch gives objective = 19 (best known integer solution), we explore the right branch. The right branch's LP gives 20 > 19. Since 20 ≥ best known (19), the right branch **cannot improve** the solution. It is **pruned** by the bounding condition: *if LP objective ≥ best known IP objective, discard this branch*.

*Verification:* 2×5+2=12≥12✓, 5+4=9≥8✓, obj=15+4=19. ✓

---

## Section 3 — Classification & Convexity

### (a) Problem Classification

**(i)** min 3x₁+5x₂ s.t. linear constraints, x ∈ ℝ:
- Variables: **continuous** | Objective: **linear** | Class: **LP**

**(ii)** min 4x₁+3x₂+x₃ s.t. x₁+x₂+x₃≥2, x ∈ {0,1}³:
- Variables: **binary** | Objective: **linear** | Class: **BIP (Binary Integer Program)**

**(iii)** min Σ(yᵢ−axᵢ−b)²:
- Variables: **continuous** (a, b ∈ ℝ) | Objective: **quadratic** (sum of squares of linear functions) | Class: **Convex (QP)**

**(iv)** min x₁x₂:
- Variables: **continuous** | Objective: **bilinear** (product of two variables) | Class: **General NLP** (bilinear is neither convex nor concave over ℝ²; e.g., fix x₂=1 it's linear in x₁, but it's not jointly convex)

---

### (b) Convexity of f(x) = x⁴ − 4x² + 4

**(i)**
```
f(x)  = x⁴ − 4x² + 4
f'(x) = 4x³ − 8x = 4x(x² − 2)
f''(x)= 12x² − 8
```

**(ii)** f''(x) ≥ 0 requires 12x² ≥ 8, i.e., x² ≥ 2/3, i.e., |x| ≥ √(2/3) ≈ 0.816.

**f''(x) = 0 at:** x = ±√(2/3) = ±√6/3 ≈ ±0.816

Sign of f''(x):
- x ∈ (−∞, −√(2/3)): f'' > 0 (convex region)
- x ∈ (−√(2/3), +√(2/3)): f'' < 0 (**concave region**)
- x ∈ (+√(2/3), +∞): f'' > 0 (convex region)

In particular: **f''(0) = −8 < 0**.

**(iii)** **f is NOT convex on ℝ.** By the second derivative test for 1D functions: f is convex on an interval if and only if f''(x) ≥ 0 throughout that interval. Since f''(0) = −8 < 0, the test fails at x = 0. Therefore f is not convex on ℝ.

*Geometric check:* f(x) = (x² − 2)² — this is a "W-shaped" curve with a local maximum in the middle and two valleys, which is clearly not bowl-shaped (not convex).

**(iv)** Critical points where f'(x) = 4x(x² − 2) = 0:
- x = 0: f''(0) = −8 < 0 → **local MAXIMUM**. f(0) = 4.
- x = +√2: f''(√2) = 12×2 − 8 = 16 > 0 → **local minimum**. f(√2) = 4−8+4 = 0.
- x = −√2: f''(−√2) = 16 > 0 → **local minimum**. f(−√2) = 0.

**Global minimum value = 0**, achieved at x = **±√2** (two global minima).
*(Note: f ≥ 0 for all x since f(x) = (x²−2)² ≥ 0, so 0 is indeed the global minimum.)*

---

### (c) Local = Global Theorem

**(i)** f'(1) = 4×1×(1−2) = **−4** < 0.

Gradient descent step: x\_new = 1 − α×(−4) = 1 + 4α > 1. The step moves **right** (increasing x).

Gradient descent from x₀=1 rolls toward x=+√2 ≈ 1.414 (the nearest local/global minimum to the right). It converges to **x=√2**.

**(ii)** g(x) = x⁴ − 4x² has g'(x) = 4x³ − 8x = 4x(x²−2), g''(x) = 12x²−8.
At x=0: g''(0)=−8<0 → x=0 is a **local MAXIMUM** of g, not a local minimum.

Therefore, the scenario described ("gradient descent converges to x=0, a local minimum") is **incorrect** — x=0 is a local maximum of g, not a minimum. Gradient descent never converges to a local maximum from a generic starting point (it moves away from maxima).

The **local = global theorem** states: *for convex f, every local minimum is a global minimum*. This theorem:
1. **Does not apply** here because g is non-convex.
2. **Is not violated** in any case, because x=0 is a local MAXIMUM of g (not a local minimum). The theorem makes no claim about local maxima.

The real issue: for non-convex functions, gradient descent can converge to **different local minima** depending on the starting point. Starting near x=0.1 (where g'(0.1)<0), gradient descent moves right toward x=+√2 (global minimum). Starting near x=−0.1, it moves left toward x=−√2 (also global minimum). In this particular case, both local minima happen to be global, so no problem. But in general, non-convex functions can have local minima that are strictly worse than global — gradient descent provides **no guarantee** in that case.

---

## Section 4 — Gradient Descent

### (a) Gradient and Steps

**(i)**
```
∂f/∂x₁ = 4x₁ − 2x₂
∂f/∂x₂ = 2x₂ − 2x₁

∇f(x₁, x₂) = (4x₁ − 2x₂,  2x₂ − 2x₁)
```

**(ii) Gradient Descent Trace:**

**Step 0 → 1:** x⁰ = (2, 1)
- ∇f(2, 1) = (4×2 − 2×1, 2×1 − 2×2) = (8−2, 2−4) = **(6, −2)**
- x¹ = (2, 1) − 0.1×(6, −2) = (2−0.6, 1+0.2) = **(1.4, 1.2)**
- f(1.4, 1.2) = 2(1.96) + (1.44) − 2(1.4)(1.2) = 3.92 + 1.44 − 3.36 = **2.00**

**Step 1 → 2:** x¹ = (1.4, 1.2)
- ∇f(1.4, 1.2) = (4×1.4 − 2×1.2, 2×1.2 − 2×1.4) = (5.6−2.4, 2.4−2.8) = **(3.2, −0.4)**
- x² = (1.4, 1.2) − 0.1×(3.2, −0.4) = (1.4−0.32, 1.2+0.04) = **(1.08, 1.24)**
- f(1.08, 1.24) = 2(1.1664) + (1.5376) − 2(1.08)(1.24) = 2.3328 + 1.5376 − 2.6784 ≈ **1.19**

| Step | Current x | ∇f(x) | x_new | f(x_new) |
|------|-----------|--------|-------|----------|
| 0→1 | (2, 1) | (6, −2) | (1.4, 1.2) | 2.00 |
| 1→2 | (1.4, 1.2) | (3.2, −0.4) | (1.08, 1.24) | ≈ 1.19 |

**(iii) Global minimum:** Set ∇f = 0:

System: 4x₁ − 2x₂ = 0 and 2x₂ − 2x₁ = 0

From eq 1: x₂ = 2x₁. Substitute into eq 2: 2(2x₁) − 2x₁ = 4x₁ − 2x₁ = 2x₁ = 0 → **x₁ = 0, x₂ = 0**.

**Global minimum: x\* = (0, 0), f\* = 0.**

---

### (b) Hessian Analysis

**(i)**

$$H = \begin{bmatrix} \frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} \\ \frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} \end{bmatrix} = \begin{bmatrix} 4 & -2 \\ -2 & 2 \end{bmatrix}$$

- **det(H)** = 4×2 − (−2)×(−2) = 8 − 4 = **4 > 0**
- **H₁₁** = 4 > 0

Since det(H) > 0 AND H₁₁ > 0, all leading principal minors are positive → H is **Positive Definite (PD)**.

**H is: Positive Definite (PD) → f is: strictly convex**

**(ii)** Since f is convex (strictly), **the local = global theorem guarantees that any local minimum found by gradient descent is the global minimum**. Therefore, gradient descent starting from **any** initial point x⁰ will converge to x\* = (0, 0) with f\* = 0, regardless of where it starts.

---

### (c) Step Size Analysis

**(i)** Maximum safe step size: α_max = 2/λ_max = 2/(3+√5) ≈ 2/5.24 ≈ **0.382**

**(ii)** Our step size α = 0.1 < 0.382. **Yes, α=0.1 is within the safe range.** ✓

**(iii)** With α = 5 >> α_max ≈ 0.38: the gradient descent step **overshoots** the minimum. Instead of moving toward (0,0), the update x_{t+1} = x_t − 5∇f(x_t) jumps far past the minimum to the other side of the bowl. In subsequent iterations, it continues to overshoot back and forth with **increasing distance** from the minimum → **gradient descent diverges** (does not converge).

---

## Section 5 — Bonus

### (a) B&B Analogy to A\*

| A\* Search | Branch and Bound |
|-----------|-----------------|
| **Heuristic h(n)** — estimated cost to goal | **LP relaxation value** — estimated minimum cost from this subproblem |
| **Admissibility**: h(n) ≤ h\*(n) | **Lower bound property**: LP ≤ IP (LP is optimistic, relaxes integer constraints) |
| **Pruning**: skip node n if f(n) ≥ best known | **Pruning**: skip branch if LP objective ≥ best known integer solution |
| **Correctness**: admissible h guarantees optimal solution found | **Correctness**: LP bound guarantees B&B finds optimal IP solution |

The LP relaxation must be a **lower** bound (for minimization) because:
1. The LP feasible set ⊇ IP feasible set (integer constraint removed = more freedom)
2. More freedom → can only do at least as well in minimization
3. Therefore LP objective ≤ IP objective at all corresponding points

If the LP relaxation **overestimated** the IP optimum, pruning based on it could discard the optimal IP solution (same as an inadmissible heuristic in A\* could bypass the optimal path). The lower bound property is essential for correctness.

### (b) Problem Hierarchy

**(i) LP ⊆ Convex:** An LP has objective f(x) = cᵀx (linear = convex: second derivative is 0 ≥ 0) and constraints Ax ≤ b (each linear inequality defines a half-space, which is convex; their intersection is convex by Section 1d). Therefore LP = minimize convex function over convex set = convex optimization. ✓

**(ii) IP ⊄ Convex:** An IP has feasible set F = {x ∈ ℤⁿ : Ax ≤ b}. The integer lattice ℤⁿ is **not convex**: for example, 0 ∈ ℤ and 1 ∈ ℤ, but 0.5 × 0 + 0.5 × 1 = 0.5 ∉ ℤ. The feasible set of an IP is a discrete set of points, not a convex set. Even though the LP objective is convex, optimizing over a non-convex feasible set disqualifies it as a convex optimization problem.

**(iii) Why LP can't replace IP:** The argument conflates problem *difficulty* with model *expressibility*. Many real decisions are inherently discrete and cannot be fractionalized:

- **Scheduling:** You cannot assign "0.7 of a nurse" to a shift — you need exactly 0 or 1 nurses.
- **Network design:** Build a road or not — you can't build 0.6 of a road.
- **Knapsack:** Take a whole item or leave it — fractional items are physically meaningless.

Modeling these as LP would give meaningless fractional solutions (e.g., "hire 2.3 pilots"). Integer constraints are necessary to get valid, implementable solutions. The IP formulation correctly captures the combinatorial nature of these decisions.

---

## Summary Tables

### Optimization Problem Classes

| Class | Variables | Objective | Constraints | Solver | Complexity |
|-------|-----------|-----------|-------------|--------|------------|
| LP | ℝⁿ | Linear | Linear | Simplex, Interior Point | Polynomial |
| IP | ℤⁿ | Linear | Linear | Branch & Bound | NP-hard |
| BIP | {0,1}ⁿ | Linear | Linear | B&B | NP-hard |
| QP | ℝⁿ | Quadratic | Linear | Active set | Polynomial (convex case) |
| Convex | ℝⁿ | Convex | Convex | Gradient descent, IPM | Polynomial |
| General NLP | ℝⁿ | Arbitrary | Arbitrary | Heuristics | No guarantee |

### Convexity Reference

| Test | Method | Condition |
|------|--------|-----------|
| 1D second derivative | Compute f''(x) | f''(x) ≥ 0 everywhere on domain |
| Hessian (nD) | Compute H = [∂²f/∂xᵢ∂xⱼ] | H is positive semidefinite (all eigenvalues ≥ 0) |
| Definition | Verify inequality | f(θx+(1−θ)y) ≤ θf(x)+(1−θ)f(y) |
| Composition rules | Non-neg. weighted sum, linear transform | Preserve convexity (see notes) |

### Gradient Descent Step Size

| Step size α | Behavior |
|-------------|----------|
| α < 2/λ_max | Converges (rate depends on condition number κ = λ_max/λ_min) |
| α = 2/λ_max | Boundary — may oscillate |
| α > 2/λ_max | **Diverges** |
| α → 0 | Converges but **infinitely slowly** |

---

*Tutorial #3 — Covers Lectures 09–12 (all 12 lectures complete)*

*Full coverage: Tutorial #1 (L01–L04) + Tutorial #2 (L05–L08) + Tutorial #3 (L09–L12)*
