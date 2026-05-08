# Lecture 12 - Convex Optimization

**Course**: CS5491: Artificial Intelligence

---

## 1. Convex Optimization Definition

**Convex Optimization Problem**:
```
min  f(x)
 x
s.t. x ∈ F
```

Where:
- `f` is a **convex function**
- `F` is a **convex set**

---

## 2. Convex Combinations

**Convex combination** of points `x, y ∈ ℝⁿ`:
```
z = θx + (1-θ)y,   θ ∈ [0, 1]
```
- When `θ ∈ (0,1)`: **strict** convex combination (point strictly between x and y)

---

## 3. Convex Sets

### Definition

A set `F` is **convex** if any convex combination of two points in `F` is also in `F`:
```
∀x, y ∈ F, ∀θ ∈ [0,1]:  z = θx + (1-θ)y ∈ F
```

### Intuition
> Draw a line segment between any two points — the segment stays **inside** the set.

| Set | Convex? |
|-----|---------|
| `ℝⁿ` | **Yes** |
| `∅` | **Yes** (vacuously) |
| Single point `{x₀}` | **Yes** |
| Intersection `F₁ ∩ F₂` of convex sets | **Yes** |
| Union `F₁ ∪ F₂` of convex sets | **Not necessarily** |
| `ℤⁿ` (integers) | **No** (e.g., `0.5 × 0 + 0.5 × 1 = 0.5 ∉ ℤ`) |

---

## 4. Convex Functions

### Definition

A function `f: F → ℝ` is **convex** on convex set `F` if:
```
∀x, y ∈ F, ∀θ ∈ [0,1]:  f(θx + (1-θ)y) ≤ θf(x) + (1-θ)f(y)
```

### Intuition
> The function value at a point between `x` and `y` is **at most** the weighted average of `f(x)` and `f(y)`.
> The function **curves upward** (bowl shape).

### Concave Functions
A function `f` is **concave** if `-f` is convex:
```
f(θx + (1-θ)y) ≥ θf(x) + (1-θ)f(y)
```
> Maximizing a concave function over a convex set = convex optimization.

---

## 5. How to Prove Convexity

### Method 1: By Definition
Verify `f(θx + (1-θ)y) ≤ θf(x) + (1-θ)f(y)` algebraically.

### Method 2: Properties of Convex Functions

| Property | Statement |
|----------|-----------|
| **Non-negative weighted sum** | If `fᵢ(x)` are convex and `wᵢ ≥ 0`, then `Σᵢ wᵢfᵢ(x)` is convex |
| **Linear transformation** | If `g(x)` is convex, then `f(x) = g(Ax+b)` is convex |
| **1D second derivative test** | `f` is convex on `[a,b]` iff `f''(x) ≥ 0` on `[a,b]` |

### Method 3: Hessian Matrix (n-D)

For twice continuously differentiable `f: ℝⁿ → ℝ`:

```
f is convex on F  ⟺  Hessian H(x) is positive semidefinite on interior of F
```

**Hessian matrix**:
```
H(x) = [∂²f/∂xᵢ∂xⱼ]  (matrix of second partial derivatives)
```

**Positive semidefinite (PSD)**: `∀z ∈ ℝⁿ: zᵀH(x)z ≥ 0`
- Equivalently: all eigenvalues of `H(x)` are **non-negative**

### Quiz: Common Convex Functions

| Function | Convex? | Reason |
|----------|---------|--------|
| `eᵃˣ, a ∈ ℝ` | **Yes** | `f'' = a²eᵃˣ ≥ 0` |
| `log x, x>0` | **No** (concave) | `f'' = -1/x² < 0` |
| `‖x‖₂ = √(Σxᵢ²)` | **Yes** | By definition |
| `xᵀAy` (bilinear) | **No** (neither) | Not convex in `(x,y)` jointly |
| `x³, x ∈ ℝ` | **No** | `f'' = 6x` (negative for `x<0`) |

---

## 6. Key Theorem: Local Optima = Global Optima

> **Theorem**: For a convex optimization problem, **every local optimum is a global optimum**.

| Term | Definition |
|------|-----------|
| **Global optimum** | `x* ∈ F` s.t. `∀y ∈ F: f(x*) ≤ f(y)` |
| **Local optimum** | `x ∈ F` s.t. `∃R>0` where `∀y ∈ F` with `‖x-y‖ ≤ R: f(x) ≤ f(y)` |

**Why this matters**: Gradient-based methods can get stuck in local optima for **non-convex** problems. For convex problems, any local minimum found is guaranteed to be the global minimum.

---

## 7. Gradient Descent

### Gradient Definition

For `f: ℝⁿ → ℝ`, the **gradient** is:
```
∇f(x) = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]ᵀ
```
- Points in the direction of **steepest increase** in `f`
- Negative gradient `-∇f(x)` points in direction of steepest **decrease**

### Gradient Descent Algorithm (Unconstrained)

```
Initialize: x₀ (e.g., x₀ = 0)
Repeat until convergence:
    x_{t+1} = xₜ - α · ∇f(xₜ)
```

Where:
- `α > 0` = **step size** (learning rate)
- **Convergence**: `‖x_{t+1} - xₜ‖ ≤ ε`

### Choosing Step Size `α`
- **Too large**: may overshoot, diverge
- **Too small**: converges very slowly
- Methods: fixed, decreasing schedule, **line search** (find best α at each step)

### Projected Gradient Descent (Constrained)

For constrained optimization `min f(x) s.t. x ∈ F`:
```
x_{t+1} = PF(xₜ - α · ∇f(xₜ))
```
Where `PF(x) = argmin_{x'∈F} ‖x - x'‖₂` is the **projection** onto `F`.

---

## 8. Solving Methods Summary

| Setting | Method |
|---------|--------|
| Unconstrained + differentiable | Gradient descent, Set `∇f=0`, Closed form |
| Unconstrained + twice differentiable | Newton's Method (not covered) |
| Constrained + differentiable | Projected gradient descent (not covered) |
| Constrained | Interior Point Method (not covered) |
| Non-differentiable | ε-Subgradient Method, Cutting Plane Method (not covered) |

---

## 9. Practical Workflow for Convex Optimization

1. **Model the problem**:
   - Define variable `x`, feasible set `F`, objective `f`
   - Prove `f` is convex and `F` is convex

2. **Solve using a solver**:
   - Python: `cvxpy`, `cvxopt`
   - MATLAB: `fmincon`, `cvx`

3. **Map solution back** to the original problem

```python
# Example with cvxpy
import cvxpy as cp

x = cp.Variable(n)
objective = cp.Minimize(c.T @ x)
constraints = [A @ x <= b]
problem = cp.Problem(objective, constraints)
problem.solve()
print(x.value)
```

---

## 10. Why Convex Optimization Matters in AI

| AI Application | Convex Formulation |
|----------------|-------------------|
| Linear Regression (L2) | Least squares — quadratic (convex) |
| SVM | Quadratic program (convex) |
| Lasso/Ridge Regression | Convex with L1/L2 regularization |
| Neural Network Training | **Non-convex** — gradient descent finds local optima |
| LP/IP problems | Special cases of convex (LP) |

> **Key distinction**: Deep learning is typically **non-convex** — no guarantee of finding global minimum. Classical ML often uses convex formulations with global optimality guarantees.

---

## 11. Summary

| Concept | Key Fact |
|---------|----------|
| Convex set | Any line segment between two points stays in the set |
| Convex function | Function lies below any chord |
| Hessian PSD | Necessary and sufficient for convexity (differentiable case) |
| Local = Global | Most powerful property of convex optimization |
| Gradient descent | Move in direction of `-∇f` with step size `α` |
| Projected GD | Same but project back onto feasible set each step |
