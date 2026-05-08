# Lecture 8: Preconditioning and Adaptive Optimizers (Adam and Muon)

> Source: `CS6487-week8.pdf`
> Format note: this is an annotated near-original version. The lecture flow, key equations, and optimizer definitions follow the PDF rather than the summary style used in earlier weeks.

---

## Opening remark

Original:

- Many modern optimizers used in ML (Adam-family, Shampoo, Muon) can be understood as plain first-order methods, but not under the usual Euclidean geometry.
- They perform steepest descent under carefully chosen norms, often time-varying and sometimes matrix-aware.
- The lecture positions AdaGrad, RMSProp, AdamW, and Shampoo as intermediate designs, with Adam and Muon as two canonical endpoints: diagonal vs operator-norm flavored.

Annotation:

- This remark is the thesis of the whole lecture.
- The lecture is not presenting a list of unrelated optimizers. It is presenting one geometry-based framework.

---

## 1. From GD / momentum to metrized gradient methods

### 1.1 From Taylor to a norm-induced descent step

Original:

- Fix a point `w in R^n` and let `Δw` be a candidate update.
- A second-order Taylor model gives
  `f(w + Δw) ≈ f(w) + g^⊤ Δw + (1 / 2) Δw^⊤ H Δw`, with `g := ∇f(w)`.
- Penalized view:
  `Δw in arg min g^⊤ Δw + (1 / 2eta) ||Δw||_H^2`
  where `||Δw||_H^2 := Δw^⊤ H Δw`.
- The note says `eta > 0` plays two roles:
  as a step size, and as the inverse strength of regularization.

Annotation:

- The optimizer step is derived from a local model plus a geometry-aware movement penalty.
- The geometry matrix `H` does not have to be the exact Hessian. It can be any positive-definite metric we choose.

### 1.2 Constrained view via Lagrange multipliers

Original:

- Equivalent trust-region view:
  `Δw in arg min g^⊤ Δw`
  subject to `||Δw||_H^2 <= 2 rho`
- The lecture forms the Lagrangian and identifies the correspondence
  `lambda = 1 / eta`
- Therefore:
  trust-region radius `rho`  <->  regularization strength `lambda = 1 / eta`

Annotation:

- This is important conceptually: preconditioning can be viewed either as penalized movement or as choosing the steepest admissible step under a norm constraint.

### 1.3 Euclidean geometry gives standard GD

Original:

- If `H = I`, then the penalized problem becomes
  `min g^⊤ Δw + (1 / 2eta) ||Δw||_2^2`
- The minimizer is `Δw = -eta g`, which recovers
  `w_(t+1) = w_t - eta ∇f(w_t)`
- Momentum is written as
  `m_t = beta m_(t-1) + (1 - beta) g_t`
  `w_(t+1) = w_t - eta m_t`
- The lecture states explicitly:
  momentum is a direction filter, while preconditioning is a geometry choice applied to that direction.

Annotation:

- This separation of roles is one of the most useful takeaways in the lecture.

---

## 2. Preconditioning as changing the norm

### 2.1 Steepest descent under a matrix norm

Original:

- Let `P ≻ 0` be SPD and define `||Δw||_P^2 := Δw^⊤ P Δw`.
- Replacing the Euclidean movement cost in the penalized objective gives
  `min g^⊤ Δw + (1 / 2eta) Δw^⊤ P Δw`
- The minimizer is
  `Δw* = -eta P^(-1) g`

Annotation:

- This is the master formula for preconditioning.
- Once `P_t` changes over time, we get adaptive methods.

### 2.2 Diagonal vs matrix preconditioning

Original:

- Diagonal preconditioners `P_t = diag(p_(t,1), ..., p_(t,n))` are cheap and scale each coordinate separately.
- This includes AdaGrad, RMSProp, Adam, and AdamW.
- Matrix-aware preconditioners treat structured parameters as matrices / tensors and adapt along row, column, or operator directions.
- This includes Shampoo and Muon.

Annotation:

- The split is not just implementation detail. It is about what correlations the optimizer is able to model.

---

## 3. Diagonal adaptive methods as preconditioning

Original template:

- In all diagonal methods, the effective update is
  `w_(t+1) = w_t - eta D_t^(-1/2) d_t`
  where `D_t` is diagonal and `d_t` is the direction.

Annotation:

- All diagonal adaptive optimizers differ only in how they build `d_t` and `D_t`.

### 3.1 AdaGrad

Original:

- AdaGrad uses the cumulative coordinate-wise second moment
  `v_t = v_(t-1) + g_t ⊙ g_t`
- It preconditions with `D_t = diag(v_t) + eps I`
- Update:
  `w_(t+1) = w_t - eta g_t / sqrt(v_t + eps)`
- Interpretation from the lecture:
  coordinates that have seen large gradients historically get smaller effective steps.

Annotation:

- AdaGrad is the simplest "history-based diagonal metric" in this family.
- Its main limitation is over-shrinking after long training because the accumulator only grows.

### 3.2 RMSProp

Original:

- RMSProp replaces the cumulative sum by an EMA:
  `v_t = rho v_(t-1) + (1 - rho)(g_t ⊙ g_t)`
- Update:
  `w_(t+1) = w_t - eta g_t / sqrt(v_t + eps)`
- Interpretation:
  the metric tracks recent gradient energy rather than all history.

Annotation:

- RMSProp fixes the main long-horizon issue of AdaGrad.

### 3.3 Adam

Original:

- Adam combines
  `m_t = beta_1 m_(t-1) + (1 - beta_1) g_t`
  `v_t = beta_2 v_(t-1) + (1 - beta_2)(g_t ⊙ g_t)`
- Bias corrections:
  `m_hat_t = m_t / (1 - beta_1^t)`
  `v_hat_t = v_t / (1 - beta_2^t)`
- Update:
  `w_(t+1) = w_t - eta m_hat_t / sqrt(v_hat_t + eps)`
- Preconditioning lens in the lecture:
  Adam is momentum first, geometry second.

Annotation:

- This is one of the most important conceptual reframings in the note:
  Adam is not "mysterious adaptive learning rate magic"; it is momentum plus a diagonal metric.

### 3.4 AdamW

Original:

- AdamW applies weight decay separately:
  `w_(t+1) = (1 - eta lambda) w_t - eta m_hat_t / sqrt(v_hat_t + eps)`
- The lecture says:
  Adam mixes `lambda w_t` into the gradient before preconditioning;
  AdamW decays `w_t` after preconditioning is formed.

Annotation:

- Decoupled weight decay means the adaptive geometry acts on the data gradient, not on the regularizer.

### 3.5 Single diagonal template

Original:

- All four methods can be written as
  `d_t = Dir(g_(1:t))`
  `D_t = DiagMetric(g_(1:t))`
  `w_(t+1) = w_t - eta (D_t + eps I)^(-1/2) d_t`

Annotation:

- This is the clean "family definition" for diagonal adaptive methods.

---

## 4. Matrix-aware preconditioning: Shampoo and Muon

### 4.1 Shampoo

Original:

- For matrix parameter `W in R^(m x n)` with gradient `G_t`, Shampoo maintains
  `L_t = L_(t-1) + G_t G_t^⊤ in R^(m x m)`
  `R_t = R_(t-1) + G_t^⊤ G_t in R^(n x n)`
- Update:
  `W_(t+1) = W_t - eta (L_t + eps I)^(-1/4) G_t (R_t + eps I)^(-1/4)`
- The lecture explains whitening as the goal:
  transform the gradient so its local second moment is closer to isotropic.
- It also explains the `-1/4` exponents by a Kronecker-factor approximation:
  whitening `vec(G_t)` suggests an inverse square root overall, which becomes a two-sided transform in matrix form.

Annotation:

- Shampoo is a structured generalization of the same second-moment idea used in AdaGrad / Adam.
- It is richer than diagonal methods because it can model row and column coupling.

### 4.2 Muon as operator-norm preconditioning

Original:

- Trust region in spectral norm:
  `min <G, ΔW>`
  subject to `||ΔW||_(2->2) <= rho`
- If `G = U Σ V^⊤` is the SVD, the steepest descent direction is
  `ΔW* = -rho U V^⊤`
- The note says:
  keep singular directions, discard singular values.
- This is the core "Muon direction".

Annotation:

- Muon normalizes the worst-case operator size of the step rather than second-moment energy.

### 4.3 Muon algorithm via Newton-Schulz polar orthogonalization

Original:

- Definition 4.1 (Muon, per matrix parameter). Fix learning rate `eta`, momentum `beta`, stability constant `eps`, and a small Newton-Schulz iteration count `K`.
- Initialize `M_0 = 0`.
- For `t = 1, 2, ...`:
  `G_t = ∇_W f(W_t)`
  `M_t = beta M_(t-1) + (1 - beta) G_t`
  `U_t = NS Polar(M_t; K)`
  `W_(t+1) = W_t - eta U_t`
- One practical Newton-Schulz form:
  `X_0 := M_t / (||M_t||_F + eps)`
  `X_(k+1) = (1/2) X_k (3I - X_k^⊤ X_k)`
  output `U_t := X_K`

Annotation:

- The lecture's interpretation:
  Adam-family preconditions with coordinate-wise second moments;
  Shampoo with row/column second moments;
  Muon with operator-norm normalization of a momentum-smoothed direction.

---

## 5. Coherent comparison: spin-offs and design choices

### 5.1 Family tree

Original:

- Start from GD: Euclidean metric.
- Add diagonal metric from second moments: AdaGrad -> RMSProp.
- Add momentum direction: Adam.
- Fix regularization interaction: AdamW.
- Generalize diagonal metric to structured matrix metric: Shampoo.
- Use a different matrix norm constraint: Muon.

Annotation:

- This section is the payoff of the whole lecture: one family tree, one design language.

### 5.2 What differs at a glance

Original lecture table, paraphrased:

- AdaGrad: direction `g_t`, diagonal accumulated metric
- RMSProp: direction `g_t`, diagonal EMA metric
- Adam: EMA direction, diagonal EMA metric
- AdamW: Adam direction and metric, but decoupled decay
- Shampoo: matrix gradient, row/column whitening metric
- Muon: momentum-smoothed matrix gradient, polar factor / operator-norm geometry

Annotation:

- This table is useful because it separates "direction" from "metric / preconditioner" explicitly.

### 5.3 Quadratic sanity check

Original:

- For `f(w) = (1/2) w^⊤ H w`, GD behaves as
  `w_(t+1) = (I - eta H) w_t`
- Preconditioning replaces `H` by `P^(-1) H` in the dynamics, aiming to reduce anisotropy.

Annotation:

- This is the geometric reason preconditioning helps: it reshapes the spectrum seen by the optimizer.

### 5.4 Where momentum fits

Original:

- In both Adam and Muon:
  raw gradient -> momentum smoothing -> geometry / preconditioning -> step
- Adam applies a diagonal second-moment metric to `m_hat_t`.
- Muon applies a polar-factor map to `M_t`.
- Shared theme:
  momentum stabilizes direction; preconditioning stabilizes scale / geometry.

Annotation:

- This line is arguably the best one-sentence summary of the lecture.

---

## 6. Implementation notes and small details that matter

### 6.1 Bias correction

Original:

- Because `m_t` and `v_t` are initialized at zero, early values are biased toward zero.
- Dividing by `(1 - beta_1^t)` and `(1 - beta_2^t)` corrects this.
- The note says bias correction makes the EMA behave like it had a long warm-start history.

Annotation:

- This is why Adam without bias correction behaves differently in early iterations.

### 6.2 The role of `eps`

Original:

- `eps` is primarily for numerical stability.
- Placing `eps` inside vs outside the square root changes behavior when coordinates are nearly zero.
- Conceptually, `eps` sets a floor on how aggressive the preconditioner can become when `v_t` is tiny.

Annotation:

- This is not just an implementation hack. It changes the effective geometry near small estimated variance.

### 6.3 When diagonal is good and when it is not

Original:

- Diagonal preconditioning is often effective because:
  it adapts to gradient-scale heterogeneity,
  it is cheap and robust under stochastic gradients,
  and many parameter groups are only loosely coupled.
- But diagonal methods cannot exploit strong parameter correlations, such as coupled rows / columns in linear layers.

Annotation:

- This is the practical decision rule for when more structured methods might matter.

---

## 7. One unified pseudocode

Original:

- Each iteration can be viewed as:
  compute stochastic gradient `g_t`
  form direction `d_t`
  build geometry object `P_t`
  update `theta_(t+1) = theta_t - eta P_t(d_t)`
- Diagonal methods:
  `P_t(d_t) = (D_t + eps I)^(-1/2) d_t`
- Shampoo:
  `P_t(G_t) = (L_t + eps I)^(-1/4) G_t (R_t + eps I)^(-1/4)`
- Muon:
  `P_t(M_t) ≈ Polar(M_t)`

Annotation:

- Once everything is written as "direction + geometry", Adam and Muon stop looking unrelated.

---

## Takeaway

Original lecture takeaway:

- Adaptive optimizers are different ways to choose a metric.
- Adam is the canonical diagonal second-moment design.
- Muon is the canonical operator-norm flavored matrix-aware design.
- Both are most naturally understood as first-order methods under non-Euclidean geometry.

Annotation:

- This lecture is the conceptual continuation of Lecture 7:
  smoothness and momentum explain first-order methods;
  geometry explains adaptive first-order methods.
