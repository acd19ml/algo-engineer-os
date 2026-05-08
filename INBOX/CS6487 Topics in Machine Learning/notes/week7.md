# Lecture 7: Smoothness, Gradient Descent Convergence, and Momentum

> Source: `CS6487-week7.pdf`
> Format note: this file follows the original lecture-note order and keeps the original definitions / lemmas / propositions as closely as possible, with short annotations added after each block.

---

## 1. Preliminaries: norms, inequalities, and quadratic forms

### 1.1 Inner products and norms

Original:

- We use the standard inner product `⟨x, y⟩ := x^⊤ y` and Euclidean norm `||x|| := sqrt(x^⊤ x)`.
- Recall the Cauchy-Schwarz inequality:
  `|⟨x, y⟩| <= ||x|| ||y||`
- Recall the triangle inequality:
  `||x + y|| <= ||x|| + ||y||`

Annotation:

- This is the geometric language used throughout the proof.
- Every later bound on descent, stability, and rates is built by combining these basic norm inequalities with smoothness.

### 1.2 Useful inequalities for analysis

Original:

- Young's inequality (scalar form). For any `a, b in R` and `eta > 0`,
  `ab <= (eta / 2) a^2 + (1 / 2eta) b^2`
- Completing the square (vector form). For any `u, v in R^d` and `eta > 0`,
  `||u - v||^2 = ||u||^2 - 2⟨u, v⟩ + ||v||^2`
  hence
  `-2⟨u, v⟩ <= eta ||u||^2 + (1 / eta) ||v||^2`
- The lecture remark says these are the same inequality in disguise and let us trade cross-terms for squared norms.

Annotation:

- "Trade cross-terms for squared norms" is the key proof move.
- Whenever a proof produces a mixed term like `⟨gradient, error⟩`, these inequalities convert it into something summable.

### 1.3 Convexity and strong convexity (quick review)

Original:

- Definition 1.1 (Convexity). A differentiable function `f` is convex if for all `x, y in R^d`,
  `f(y) >= f(x) + ⟨∇f(x), y - x⟩`
- Definition 1.2 (`mu`-strong convexity). For `mu > 0`, `f` is `mu`-strongly convex if for all `x, y`,
  `f(y) >= f(x) + ⟨∇f(x), y - x⟩ + (mu / 2) ||y - x||^2`
- Remark 1.1. Strong convexity implies a unique minimizer `x*` and gives geometric (linear) convergence rates for GD with proper step sizes. In modern ML, objectives are often nonconvex, but these results remain highly informative and are exactly correct for quadratic models.

Annotation:

- Convexity gives a first-order lower bound.
- Strong convexity adds quadratic curvature from below, which is why it upgrades `O(1/k)` to geometric convergence.

---

## 2. Taylor's theorem and the descent lemma

### 2.1 Taylor expansion with remainder

Original:

- Theorem 2.1 (Taylor's theorem, multivariate second order). Let `f` be twice continuously differentiable. For any `x` and step `s`,
  `f(x + s) = f(x) + ⟨∇f(x), s⟩ + (1 / 2) s^⊤ ∇^2 f(x + tau s) s`
  for some `tau in (0, 1)`.
- The lecture note: if we can upper bound the Hessian along the segment `x + tau s`, we get a usable upper bound on `f(x + s)`. This is the technical bridge from local geometry (curvature) to global algorithmic progress.

Annotation:

- Taylor expansion tells us exactly what information is missing from a pure first-order model.
- Smoothness will be used to bound that second-order remainder term uniformly.

### 2.2 L-smoothness and the descent lemma

Original:

- Definition 2.1 (L-smoothness / Lipschitz gradient). We say `f` is `L`-smooth on a set `X` if
  `||∇f(x) - ∇f(y)|| <= L ||x - y||` for all `x, y in X`.
- Lemma 2.1 (Descent lemma). If `f` is differentiable and `L`-smooth on a convex set containing the segment between `x` and `y`, then
  `f(y) <= f(x) + ⟨∇f(x), y - x⟩ + (L / 2) ||y - x||^2`
- Proof sketch in the lecture:
  define `phi(t) = f(x + t(y - x))`, write
  `phi(1) - phi(0) = integral phi'(t) dt`,
  add and subtract `⟨∇f(x), y - x⟩`,
  then apply Cauchy-Schwarz and `L`-smoothness.
- Remark 2.1. The descent lemma is the single most-used inequality in first-order method analysis. It gives a quadratic upper model:
  `f(y) ≲ f(x) + (linear term) + (L / 2) ||y - x||^2`

Annotation:

- This is the core lemma of the lecture.
- It says smoothness turns the unknown function into something we can safely upper bound by a tractable quadratic surrogate.

### 2.3 Equivalent characterization

Original:

- When `f` is twice differentiable, `L`-smoothness is equivalent to the uniform Hessian bound
  `∇^2 f(x) ⪯ L I` for all `x`.

Annotation:

- This is the curvature interpretation of smoothness: no direction curves upward faster than `L`.

---

## 3. Consequences of smoothness

### 3.1 A basic inequality for one step

Original:

- Plug `y = x - alpha ∇f(x)` into the descent lemma:
  `f(x - alpha ∇f(x)) <= f(x) - alpha (1 - L alpha / 2) ||∇f(x)||^2`
- Hence any step size `alpha in (0, 2 / L)` gives descent:
  `f(x - alpha ∇f(x)) <= f(x)`

Annotation:

- This is the first rigorous step-size rule.
- It explains why `alpha <= 1 / L` is a standard conservative choice: it keeps the coefficient in front of `||∇f(x)||^2` clearly positive.

### 3.2 Smooth + convex implies gradient is well-behaved

Original:

- Lemma 3.1 (Co-coercivity of the gradient). If `f` is convex and `L`-smooth, then for all `x, y`,
  `⟨∇f(x) - ∇f(y), x - y⟩ >= (1 / L) ||∇f(x) - ∇f(y)||^2`
- Remark 3.1. This lemma is central in advanced analyses such as proximal methods, operator splitting, and monotone operators.

Annotation:

- Co-coercivity is stronger than plain Lipschitz continuity.
- It is the reason convex + smooth objectives behave much more regularly than arbitrary nonconvex objectives.

---

## 4. Notions of convergence and rates

### 4.1 What does "converge" mean?

Original:

- Function-value convergence: `f(x_k) -> f*`
- Iterate convergence: `x_k -> x*`
- Stationarity in nonconvex optimization: `||∇f(x_k)|| -> 0` or `min_{0 <= t < k} ||∇f(x_t)|| -> 0`
- The lecture note states that in nonconvex ML, the standard deterministic guarantee for GD is convergence to a first-order stationary point.

Annotation:

- This section is clarifying the target before proving rates.
- For nonconvex objectives, "small gradient" is the basic guarantee; global optimality is generally not promised.

### 4.2 Rates: sublinear vs linear

Original:

- Definition 4.1. Let `(a_k)` be a nonnegative sequence decreasing to `0`.
- Sublinear rate: `a_k = O(1/k)` or `O(1/sqrt(k))`
- Linear (geometric) rate: `a_k <= C rho^k` for some `rho in (0, 1)`
- Remark 4.1. In ML, "linear convergence" means geometric decay, not a straight line.

Annotation:

- This terminology matters because later propositions compare GD in nonconvex, convex, and strongly convex regimes.

---

## 5. Gradient Descent: algorithm and convergence

### 5.1 Algorithm

Original:

- Gradient Descent with constant step size `alpha > 0`:
  `x_(k+1) = x_k - alpha ∇f(x_k)`
- The lecture interprets GD as repeatedly minimizing the local quadratic model
  `m_k(y) := f(x_k) + ⟨∇f(x_k), y - x_k⟩ + (1 / 2alpha) ||y - x_k||^2`
  whose minimizer is exactly `x_k - alpha ∇f(x_k)`.

Annotation:

- This explains why GD is not just a heuristic step along `-∇f`; it is the optimizer of a local surrogate.

### 5.2 Nonconvex guarantee: small gradient norm

Original:

- Assume `f` is `L`-smooth and bounded below by `f* > -infinity`.
- Using the one-step inequality with `alpha in (0, 1 / L]`:
  `f(x_(k+1)) <= f(x_k) - (alpha / 2) ||∇f(x_k)||^2`
- Summing from `k = 0` to `T - 1` yields
  `min_{0 <= k <= T-1} ||∇f(x_k)||^2 <= 2(f(x_0) - f*) / (alpha T)`
- Proposition 5.1. With `alpha = 1 / L`,
  `min_{0 <= k <= T-1} ||∇f(x_k)|| <= sqrt(2L(f(x_0) - f*) / T)`
- Hence to make `min ||∇f(x_k)|| <= epsilon`, it suffices that
  `T = O(L(f(x_0) - f*) / epsilon^2)`

Annotation:

- This is the standard deterministic complexity bound for smooth nonconvex optimization.
- The guarantee is on the best iterate among the first `T`, not necessarily the last iterate.

### 5.3 Convex guarantee: `O(1/k)` in function value

Original:

- Now assume `f` is convex and `L`-smooth, and a minimizer `x*` exists.
- With `alpha = 1 / L`, one can show
  `f(x_k) - f* <= (L / 2k) ||x_0 - x*||^2`
- Proposition 5.2. If `f` is convex and `L`-smooth and GD uses `alpha = 1 / L`, then
  `f(x_k) - f* = O(1/k)`

Annotation:

- Convexity upgrades the guarantee from "some iterate has small gradient" to "function value converges at rate `O(1/k)`".

### 5.4 Condition number remark

Original:

- Remark 5.2. Define the condition number `kappa := L / mu`.
- Then `(1 - mu / L)^k ≈ exp(-k / kappa)` for large `kappa`.
- Ill-conditioning (large `kappa`) slows GD dramatically.

Annotation:

- This is the bridge to momentum and preconditioning.
- Large curvature disparity is exactly what causes zig-zagging and slow progress.

---

## 6. Step-size choices in practice

### 6.1 Constant steps based on smoothness

Original:

- If you know an `L` such that `f` is `L`-smooth, the safest deterministic choice is
  `alpha = 1 / L`
- If `f` is also `mu`-strongly convex and `mu` is known, an often-better tuned choice is
  `alpha = 2 / (L + mu)`

Annotation:

- `1 / L` is the clean theory choice.
- `2 / (L + mu)` is more aggressive and tuned to the quadratic/strongly convex setting.

### 6.2 Backtracking line search

Original:

- If `L` is unknown, backtracking starts from a trial step size and shrinks by `beta in (0, 1)` until
  `f(x - alpha ∇f(x)) <= f(x) - (alpha / 2) ||∇f(x)||^2`
- The note says this behaves like `1 / L` locally.

Annotation:

- The lecture explicitly notes that exact line search is rare in deep learning because mini-batches make function values noisy.

### 6.3 Diminishing step sizes

Original:

- For deterministic smooth optimization, constant steps are typically best.
- Diminishing steps `alpha_k ↓ 0` are more relevant for stochastic gradient methods.

Annotation:

- This separates classical deterministic GD theory from stochastic optimization practice.

---

## 7. Momentum: why and how

### 7.1 Motivation: oscillations and ill-conditioning

Original:

- Consider a quadratic objective `f(x) = (1/2) x^⊤ H x` with eigenvalues in `[mu, L]`.
- In eigen-coordinates, GD decouples into scalar recursions
  `z_(k+1) = (1 - alpha lambda) z_k`
- Stability requires `alpha in (0, 2 / L)`.
- When `kappa = L / mu` is large, `alpha ≈ 1 / L` makes progress along small-curvature directions very slow, and GD can zig-zag.

Annotation:

- This is the clean quadratic picture behind the phrase "ill-conditioned optimization".

### 7.2 Heavy-ball (Polyak) momentum

Original:

- Definition 7.1. Given step size `alpha > 0` and momentum parameter `beta in [0, 1)`,
  `x_(k+1) = x_k - alpha ∇f(x_k) + beta (x_k - x_(k-1))`
- Equivalent velocity form:
  `v_(k+1) = beta v_k + ∇f(x_k)`, `x_(k+1) = x_k - alpha v_(k+1)`
- Remark 7.1:
  if gradients keep pointing in a consistent direction, momentum accumulates them and effectively increases the step;
  if gradients oscillate, momentum acts like a low-pass filter and damps sign changes.

Annotation:

- These two intuitions are exactly the ones used in practical deep-learning explanations of momentum.

### 7.3 Stability picture on quadratics

Original:

- Along an eigen-direction with curvature `lambda`, heavy-ball becomes
  `z_(k+1) = (1 - alpha lambda + beta) z_k - beta z_(k-1)`
- The lecture explains that:
  steep directions can be stabilized by the feedback term `-beta z_(k-1)`,
  while flat directions can move faster because the larger admissible `alpha` is no longer limited as severely by the steep modes.
- Proposition 7.1. For a quadratic with eigenvalues in `[m, L]` and condition number `kappa = L / m`, there exist parameter choices `(alpha, beta)` such that
  `||e_k||_2 <= C ((sqrt(kappa) - 1) / (sqrt(kappa) + 1))^k ||e_0||_2`

Annotation:

- This is the main quantitative payoff: heavy-ball can improve the condition-number dependence from `kappa` to `sqrt(kappa)`.

### 7.4 Nesterov momentum (lookahead)

Original:

- Nesterov's accelerated gradient is written as
  `y_k = x_k + beta (x_k - x_(k-1))`
  `x_(k+1) = y_k - alpha ∇f(y_k)`
- Compared to heavy-ball, the gradient is evaluated at the lookahead point `y_k`.
- Theorem 7.1 (informal). For convex `L`-smooth objectives, Nesterov-type schemes can achieve
  `f(x_k) - f* = O(1 / k^2)`

Annotation:

- The lecture notes that the proof is more involved and uses estimate sequences or Lyapunov functions.
- In deep-learning libraries, many "momentum" implementations are closer to heavy-ball than exact Nesterov acceleration.

### 7.5 Parameter heuristics

Original:

- Deterministic quadratic model:
  `alpha = 4 / (sqrt(L) + sqrt(mu))^2`
  `beta = ((sqrt(L) - sqrt(mu)) / (sqrt(L) + sqrt(mu)))^2`
- Deep-learning heuristics:
  common defaults are `beta in {0.9, 0.95, 0.99}` with a tuned learning rate.
- Remark 7.3. In SGD, momentum can smooth noise and speed optimization, but it can also amplify bias or cause overshooting if the learning rate is too large.

Annotation:

- The lecture is careful to separate the exact quadratic theory from practical stochastic training.

---

## 8. Summary and what to remember

Original:

- `L`-smoothness implies the descent lemma, which gives rigorous decrease bounds for GD.
- With `alpha <= 1 / L`, GD is a descent method and achieves:
  `nonconvex: min_{t < T} ||∇f(x_t)|| = O(1 / sqrt(T))`
  `convex: f(x_T) - f* = O(1 / T)`
  `strongly convex: geometric rate with factor about 1 - 1 / kappa`
- Step size is the main stability knob.
- Momentum introduces inertia that can mitigate zig-zagging and improve conditioning effects.

Annotation:

- This lecture is building the first-order optimization toolkit used again in Lectures 8 and 9.
