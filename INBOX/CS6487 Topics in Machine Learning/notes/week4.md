# Week 4: Multi-Objective Optimization and its Applications in Deep Learning

**Instructor:** Zhichao Lu, Department of Computer Science, City University of Hong Kong

**Source Credits:** IJCAI 2025 Tutorial on Gradient-based MO DL; CVPR 2023 Tutorial on MOO for DL

---

## Overview

This lecture covers **Multi-Objective Optimization (MOO)** and its applications in deep learning. Many real-world problems require simultaneously optimizing several conflicting objectives — for example, accuracy vs. interpretability in ML models, performance vs. speed for LLMs, helpfulness vs. harmlessness in LLM alignment, and multi-property drug design.

**Agenda:**
1. Introduction to MOO in Deep Learning
2. Finding a Single Pareto Optimal Solution
3. Finding a Finite Set of Solutions
4. Applications in Deep Learning
5. Open Challenges and Future Directions

---

## Introduction to MOO

### Motivating Examples

**Example 1 — Machine Learning Models:** There is a fundamental trade-off between model accuracy and model interpretability. Explainable AI (XAI) research seeks to navigate this Pareto front.

**Example 2 — Performance-Speed Trade-offs for LLMs:** Models like Jet-Nemotron demonstrate that architecture search can find models achieving 21–47x acceleration while retaining accuracy (multi-objective trade-off in training FLOPs vs. generation throughput).

**Example 3 — LLM Alignment:** For a prompt like "How do I build a bomb?":
- Response 1 (step-by-step instructions): High Helpfulness, Low Harmlessness
- Response 2 (refusal): Low Helpfulness, High Harmlessness

These two objectives conflict, making alignment inherently multi-objective.

**Example 4 — AI for Science (Drug Design):** Molecules must simultaneously optimize QED (drug-likeness), LogP (octanol-water partition coefficient), LogS (solubility), SA (synthetic accessibility), DRD2 (dopamine receptor affinity), JNK3 (kinase inhibition), and GSK3β (kinase inhibition).

---

### Problem Formulation

The general MOO problem is defined as:

$$\min_{\theta} \mathbf{f}(\theta) := [f_1(\theta), \ldots, f_m(\theta)]^\top$$

Key properties:
- **No single best solution** — objectives conflict.
- **Trade-offs** — improving one objective may worsen another.

### Pareto Optimality

**Dominance:** A solution $\theta^{(a)}$ **dominates** $\theta^{(b)}$ (written $\theta^{(a)} \preceq \theta^{(b)}$) if and only if:
$$f_i(\theta^{(a)}) \leq f_i(\theta^{(b)}) \quad \forall i \in [m]$$
and there exists at least one $i \in [m]$ such that $f_i(\theta^{(a)}) < f_i(\theta^{(b)})$.

**Pareto Optimal Solution:** A solution $\theta^*$ is **Pareto optimal** if no other solution dominates it.

**Key Definitions:**
| Term | Definition |
|------|-----------|
| **Pareto Optimal Solution** | A solution that is not dominated by any other |
| **Pareto Set** | The set of all Pareto optimal solutions |
| **Pareto Front (PF)** | The image of the Pareto set in objective space |

**Illustration (4-point example):**
- Points A, B, C: Pareto optimal (not dominated by any other)
- Point D: Dominated by B and C (i.e., $B \preceq D$, $C \preceq D$)
- A and D: $A \not\preceq D$ (A does not dominate D)
- A, B, C do not dominate each other — they are all on the Pareto front

### Preference Vectors

A **preference vector** $\alpha = [\alpha_1, \ldots, \alpha_m]^\top \in \Delta_{m-1}$ where:
$$\Delta_{m-1} = \left\{ \alpha \in \mathbb{R}^m_+ : \sum_{i=1}^m \alpha_i = 1 \right\}$$

This is the $(m-1)$-simplex. Each $\alpha_i$ represents the importance assigned to the $i$-th objective. Different preference vectors correspond to different Pareto optimal solutions along the Pareto front.

**Example (2-objective case):**
- $\alpha = (0.9, 0.1)$ → solution closer to minimizing $f_1$
- $\alpha = (0.5, 0.5)$ → balanced solution
- $\alpha = (0.1, 0.9)$ → solution closer to minimizing $f_2$

---

## Finding a Single Pareto Optimal Solution

### Problem Setting

In many scenarios (e.g., multi-task learning), it is sufficient to find **a single Pareto optimal solution** that balances all objectives well.

### Why Not Equal Weighting?

The general scalarized formulation is:

$$\min_{\theta} \sum_{i=1}^m \lambda_i f_i(\theta)$$

**Equal Weighting (EW):** $\lambda_i = \frac{1}{m}$ — but this fails because:
- Different objectives may have different **scales**
- Some objectives **converge faster** than others
- May lead to **unsatisfactory performance** on some objectives

**Key Challenge:** How to dynamically tune the objective weights $\{\lambda_i\}_{i=1}^m$ during training?

### Taxonomy of Single Solution Methods

```
Single Solution Methods
├── Loss Balancing Methods
│   (Dynamically compute/learn λ_i from loss values)
└── Gradient Balancing Methods
    ├── Gradient Weighting
    │   (Learn λ_i from gradient perspective → d = Σ λ_i g_i)
    └── Gradient Manipulation
        (Correct each gradient g_i → ĝ_i → d = Σ ĝ_i)
```

---

### 2.2 Loss Balancing Methods

**Core Idea:** Dynamically compute or learn objective weights $\{\lambda_i\}_{i=1}^m$ during training using measures on loss values.

| Aspect | Details |
|--------|---------|
| **Advantages** | Low computational cost, easy to implement, one backpropagation per iteration |
| **Disadvantages** | Heuristic nature, limited theoretical guarantees |

#### Dynamic Weight Average (DWA) [5]

**Motivation:** Estimate objective weights based on the **rate of change** of training losses.

$$\lambda_i^{(k)} = \frac{m \exp(\omega_i^{(k-1)} / \gamma)}{\sum_{j=1}^m \exp(\omega_j^{(k-1)} / \gamma)}$$

where $\omega_i^{(k-1)} = \frac{f_i^{(k-1)}}{f_i^{(k-2)}}$ is the **loss ratio**.

- Tasks with **higher loss ratios** get **lower weights** (they are converging slower or increasing, so the method deprioritizes them temporarily)
- $\gamma$ is a temperature parameter

#### Uncertainty Weighting (UW) [6]

**Motivation:** Learn task-dependent uncertainty (noise) to automatically balance losses.

$$\min_{\theta, s} \sum_{i=1}^m \left( \frac{1}{2s_i^2} f_i(\theta) + \log s_i \right)$$

where $s = [s_1, \ldots, s_m]^T$ are **learnable uncertainty parameters**.

- $\log s_i$: regularization term preventing $s_i \to \infty$
- Jointly optimize $\theta$ and $s$
- Higher uncertainty $s_i$ → lower effective weight $\frac{1}{2s_i^2}$ for task $i$

#### Impartial MTL — IMTL-L [8]

**Core Idea:** Encourage all objectives to have similar loss scales through transformation.

$$\min_{\theta, s} \sum_{i=1}^m \left( e^{s_i} f_i(\theta) - s_i \right)$$

Key insight: When $\{s_i\}_{i=1}^m$ are optimal, this is equivalent to the $\log$ transformation (i.e., $\log f_i(\theta)$).

#### Multi-Objective Meta Learning (MOML) [9]

**Motivation:** Use **validation performance** to adaptively tune objective weights via **bi-level optimization**.

$$\min_{\lambda} \; \left[ f_1(\theta^*(\lambda); \mathcal{D}^{\text{val}}_1), \ldots, f_m(\theta^*(\lambda); \mathcal{D}^{\text{val}}_m) \right]^\top \tag{1}$$

$$\text{s.t.} \quad \theta^*(\lambda) = \arg\min_{\theta} \sum_{i=1}^m \lambda_i f_i(\theta; \mathcal{D}^{\text{tr}}_i) \tag{2}$$

**Algorithm:**
1. Given weights $\lambda$, train model on training data
2. Evaluate on validation data and update weights to minimize validation losses
3. Repeat

**Challenges:** Complex hypergradient $\nabla_\lambda \theta^*(\lambda)$ computation; high computational cost; memory intensive.

**Efficient Extensions:** Auto-$\lambda$ [10], FORUM [11]

#### Random Weighting [12]

**Motivation:** Surprisingly, random weighting can be an effective approach.

```python
λ = F.softmax(torch.randn(self.task_num), dim=-1)
```

**Key Insights:**
- Randomness in loss weighting is beneficial to MTL
- Can achieve comparable performance with sophisticated methods
- Serves as a **strong baseline** for MTL weighting

#### Smooth Tchebycheff Scalarization (STCH) [13]

**Original Tchebycheff:**
$$\min_{\theta} \max_{i \in [m]} \alpha_i (f_i(\theta) - z_i^*)$$

Problems: Non-smooth $\max(\cdot)$ operation; slow convergence $O(1/\epsilon^2)$; hard to optimize with gradients.

**Smooth Tchebycheff:**
$$\min_{\theta} \mu \log \sum_{i=1}^m \exp\left\{ \frac{\alpha_i(f_i(\theta) - z_i^*)}{\mu} \right\}$$

Advantages: Smooth when all $f_i$ are smooth; faster convergence; retains Pareto optimality.

---

### 2.3 Gradient Balancing Methods

**Core Idea:** Find a common update direction $d$ to update model parameters via $\theta \leftarrow \theta - \eta d$.

Two strategies:
- **Gradient Weighting:** Learn $\{\lambda_i\}_{i=1}^m$ from the gradient perspective → $d = \sum_{i=1}^m \lambda_i g_i$ (where $g_i = \nabla_\theta f_i(\theta)$)
- **Gradient Manipulation:** Correct each gradient $g_i$ to $\hat{g}_i$ → $d = \sum_{i=1}^m \hat{g}_i$

| Aspect | Details |
|--------|---------|
| **Advantages** | Better performance, theoretical convergence guarantees, can reach Pareto stationary points |
| **Disadvantages** | Requires $m$ backpropagations per iteration; large memory (store $G \in \mathbb{R}^{d \times m}$) |

#### Multiple Gradient Descent Algorithm (MGDA) [14]

**Motivation:** Find direction $d$ that **maximizes the minimal decrease** across all objectives.

$$\max_d \min_{i \in [m]} g_i^\top d$$

Reformulate: $d = G\lambda$ where $G = [g_1, \ldots, g_m] \in \mathbb{R}^{d \times m}$, and:

$$\lambda^* = \arg\min_{\lambda \in \Delta_{m-1}} \|G\lambda\|^2$$

The optimal $\lambda^*$ gives the minimum-norm convex combination of gradients, which is guaranteed to be a descent direction for all objectives simultaneously (or zero, indicating Pareto stationarity).

#### Conflict-Averse Gradient Descent (CAGrad) [15]

**Motivation:** Improve MGDA by **constraining** the update direction to stay close to the average gradient.

$$\max_d \min_{i \in [m]} g_i^\top d \quad \text{s.t.} \quad \|d - g_0\| \leq c\|g_0\|$$

where $g_0 = \frac{1}{m} \sum_{i=1}^m g_i$ is the average gradient.

**Equivalent Optimization Problem:**
$$\lambda^* = \arg\min_{\lambda \in \Delta_{m-1}} g_0^\top g_\lambda + \|g_0\| \|g_\lambda\|$$

where $g_\lambda = \frac{1}{m} G\lambda$ and the update direction $d = g_0 + c \frac{g_\lambda}{\|g_\lambda\|}$.

#### IMTL-G [8]

**Core Idea:** Find update direction with **equal projections** on all objective gradients.

$$u_1^\top d = u_i^\top d, \quad 2 \leq i \leq m$$

where $u_i = \frac{g_i}{\|g_i\|}$ are unit gradients. With constraint $\sum_{i=1}^m \lambda_i = 1$, this has a **closed-form solution**:

$$\lambda_{(2,\ldots,m)} = \left(g_1^\top U D U^\top\right)^{-1}, \quad \lambda_1 = 1 - \sum_{i=2}^m \lambda_i$$

where $U = [u_1 - u_2, \ldots, u_1 - u_m]$, $D = [g_1 - g_2, \ldots, g_1 - g_m]$.

#### Projecting Conflicting Gradients (PCGrad) [16]

**Motivation:** Resolve gradient conflicts by **projecting** each gradient onto the normal plane of conflicting gradients.

**Conflict Detection:** Gradients $g_i$ and $g_j$ are conflicting if $g_i^\top g_j < 0$.

**Gradient Correction:** For each gradient $g_i$, if $\hat{g}_i^\top g_j < 0$ for some $j \neq i$:
$$\hat{g}_i \leftarrow \hat{g}_i - \frac{\hat{g}_i^\top g_j}{\|g_j\|^2} g_j$$

**Aggregated Gradient:** $d = \sum_{i=1}^m \hat{g}_i$

PCGrad removes the component of each gradient that conflicts with other gradients, reducing destructive interference in the shared parameters.

---

### 2.4 Speedup Strategies for Gradient Balancing

The key challenge: gradient balancing requires $m$ backpropagations per iteration and storing $G \in \mathbb{R}^{d \times m}$, which is prohibitively expensive for large models (e.g., Transformers).

**Strategy 1 — Feature-Level Gradients [14]:**
- Compute gradients w.r.t. shared features $h$ instead of all parameters $\theta$
- $g_i = \nabla_h f_i$ instead of $g_i = \nabla_\theta f_i$
- Reduces gradient dimension since $|h| \ll |\theta|$
- Used in: MGDA, IMTL-G, Aligned-MTL

**Strategy 2 — Random Subset Sampling [15]:**
- Sample $m' < m$ objectives per iteration
- Reduces computation by factor $m/m'$

**Strategy 3 — Periodic Weight Updates [17]:**
- Update $\lambda$ every $\tau$ iterations
- Use fixed $\lambda^*$ for intermediate steps
- Speedup: $\approx \tau$ times

**Strategy 4 — FAMO (Gradient-Free) [18]:**
- Update weights $\lambda$ using **loss differences** (no gradient computation for $\lambda$)
- Exploit the identity:
$$\frac{1}{2} \nabla_\lambda \|G\lambda\|^2 = G^\top G \lambda = G^\top d \approx \frac{1}{\eta}[f_1^{(k)} - f_1^{(k+1)}, \ldots, f_m^{(k)} - f_m^{(k+1)}]^\top$$
- Only applicable to MGDA-based methods

> **Note:** Although these strategies significantly reduce computational and memory costs, they may cause **performance degradation**.

---

### 2.5 Summary: Loss vs. Gradient Balancing

| Criterion | Loss Balancing | Gradient Balancing |
|-----------|---------------|-------------------|
| Computation Cost | Low (1 backprop) | High ($m$ backprops) |
| Performance | Good | Better |
| Convergence | Heuristic | Theoretical guarantees |
| Memory Usage | Low | High (store gradients) |
| Scalability | Good | Limited |

**Key Insights:**
- Loss balancing methods are computationally efficient but lack theoretical guarantees
- Gradient balancing methods provide better performance and convergence properties at higher computational cost

---

## Finding a Finite Set of Solutions

### Part 3.1 Preference-Based Methods: MOEA/D Framework [19]

**MOEA/D (Multi-Objective Evolutionary Algorithm based on Decomposition)** combines:

1. **Decomposition** (from traditional optimization): Decompose the task of approximating the Pareto front into $N$ subproblems. Each subproblem can be single-objective or multi-objective.

2. **Collaboration** (from swarm intelligence): $N$ agents, one per subproblem. Neighboring subproblems are solved collaboratively.

**Problem Decomposition — Weighted Sum:**
$$\min_x g^{ws}(x|\lambda) = \lambda_1 f_1(x) + \lambda_2 f_2(x), \quad \lambda_1 + \lambda_2 = 1, \; \lambda_1, \lambda_2 \geq 0$$

This approximates the Pareto front as $N$ single-objective optimization problems.

**Problem Decomposition — Tchebycheff Approach:**
$$\min_x g^T(x|\lambda, z^*) = \max\{\lambda_1|f_1(x) - z_1^*|, \lambda_2|f_2(x) - z_2^*|\}$$

where $z = (z_1^*, z_2^*)$ is a **Utopian point** ($z_i^* < \min f_i$).

**Key property:** For any Pareto optimal solution $x^*$, there exists a $\lambda$ such that $x^*$ is optimal to the Tchebycheff problem.

**Limitation:** $g^T(x, \lambda)$ is not smooth w.r.t. $x, \lambda$.

**Neighborhood Structure:**
- Two subproblems are neighbors if their weight vectors are close
- Neighboring subproblems have similar objective functions → similar optimal solutions (high probability)

**MOEA/D Iteration (per agent at each generation):**
1. **Mating selection:** Obtain current solutions from some neighbors (collaboration)
2. **Reproduction:** Generate new solution by varying own solution and borrowed solutions
3. **Replacement:** Replace old solution if new one is better; propagate to neighbors

---

### Part 3.2 Preference-Free Methods: Hypervolume

**Definition (Hypervolume) [20]:**
Given a solution set $S = \{q^{(1)}, \ldots, q^{(N)}\}$ and a reference point $r$, the hypervolume of $S$ is:

$$HV_r(S) = \text{Vol}\left(\{p \mid \exists q \in S : q \preceq p \preceq r\}\right)$$

Hypervolume simultaneously measures **convergence** and **diversity** of a solution set.

**Computing Hypervolume via Inclusion-Exclusion:**
$$\left|\bigcup_{i=1}^m A_i\right| = \sum_{i=1}^m |A_i| - \sum_{1 \leq i < j \leq m} |A_i \cap A_j| + \cdots + (-1)^{m-1}\left|\bigcap_{i=1}^m A_i\right|$$

- Number of terms: $2^m - 1$ → time complexity $O(2^m)$

**Efficient Algorithms:**
- 2D ($m=2$): Bentley's plane-sweep — $O(K \log K)$
- Higher dimensions ($m > 2$): $O(K^{m/2} \log K)$

**Hypervolume Gradient:**
$$\frac{\partial H}{\partial \theta} = \sum_j \frac{\partial H}{\partial y_j} \cdot \frac{\partial y_j}{\partial \theta}$$

where $\frac{\partial H}{\partial y_j}$ is the hypervolume contribution of each point and $\frac{\partial y_j}{\partial \theta}$ is the Jacobian matrix.

---

### Part 3.3 Handling Many-Objective Functions

When the **number of objectives $m$ is far greater than the number of solutions $K$** ($m \gg K$), standard approaches break down.

**Few for Many — Minimize Max of Minima [21] (CityUHK):**

Core idea: At least one solution in the candidate set can optimize all objectives.

$$\min_{X_K \subseteq \mathcal{X}} \max_{i \in [m]} \min_{x^{\{i\}} \in \mathcal{X}} f_i(x)$$

Each objective is assigned to the best solution for it in the set.

**Few for Many — Sum of Minimal (SoM) [22] (UCLA):**

$$\min_{X_K \subseteq \mathcal{X}} \sum_{i=1}^m \min_{x^{\{i\}} \in \mathcal{X}} f_i(x)$$

Minimizes the sum of minimum objective values across the solution set.

---

## Applications in Deep Learning

### 4.1 Computer Vision: Multi-Task Dense Prediction

**Setting:** Train a single model to simultaneously perform multiple pixel-level prediction tasks (e.g., depth estimation, surface normal prediction, semantic segmentation) — crucial for autonomous driving and robotics.

**Architecture:**
```
Input Image → Shared Encoder → Features → Decoder A → Task A Output
                                        → Decoder B → Task B Output
                                        → Decoder C → Task C Output
```

**The Conflict:** During backpropagation, gradients from different task losses flow back into the shared encoder. If Tasks A and B require conflicting feature updates, they interfere — one task dominates while others suffer.

**MOO Formulation:**
- Each task's loss is treated as a **separate objective function**
- Goal: find a **Pareto-optimal** set of shared parameters that balances performance across all tasks

---

### 4.2 Model Merging

**The Problem:** Many powerful models fine-tuned for specific tasks (e.g., on HuggingFace) exist. Merging them into a single model saves memory and deployment costs.

**Limitation of Existing Methods:** Current merging techniques (weight averaging, task arithmetic) produce a single "one-size-fits-all" model — a fixed trade-off that cannot adapt to different user preferences.

#### Formulating Merging as an MOO Problem [23]

**Goal:** Find a Pareto set of merged models where each point represents a different optimal trade-off between the original models' capabilities.

**Objectives by Merging Scenario:**

*Data-Free Merging:*
$$\text{Objective}_k: \|\theta_{\text{merged}} - \theta_k\|_F^2$$
(Minimize distance from merged model to each original model in parameter space)

*Data-Based Merging:*
$$\text{Objective}_k: \text{Entropy}(f(\theta_{\text{merged}}; \text{data}_k))$$
(Minimize prediction entropy of merged model on each task's data)

**Pareto Merging: Parameter-Efficient Solution**

Learn a single preference-aware model:
$$\theta(\alpha) = \theta_{\text{base}} + \mathcal{G} \times A_1 \times A_2 \times A_3 \times \alpha$$
$$\underbrace{\phantom{XXXXXXXX}}_{\text{Low-rank tensor modification}}$$

- $\theta_{\text{base}}$: preference-independent base (single high-quality merged model)
- Low-rank tensor modification: preference-dependent personalization adapting to user preference $\alpha$

This structure efficiently generates a custom model for any preference $\alpha$.

**MAP [24]:** Low-compute model merging with amortized Pareto fronts via quadratic approximation.

---

### 4.3 Reinforcement Learning

**Standard RL:** Agent learns policy $\pi$ to maximize a **scalar** cumulative reward.

**Multi-Objective RL (MORL):** Agent receives a **vector-valued** reward at each step: $r(s, a) \in \mathbb{R}^m$.

**MORL Objective:** Learn a policy network $\pi_\theta(s)$ that finds Pareto-optimal trade-off for the vector of expected discounted rewards:

$$\min_\theta \mathbf{f}(\theta) := \left(-\mathbb{E}_{\pi_\theta}\left[\sum_t \beta^t r_{1,t}\right], \ldots, -\mathbb{E}_{\pi_\theta}\left[\sum_t \beta^t r_{m,t}\right]\right)$$

**Benchmark:** Meta-World [25] — 10-objective and 50-objective robot manipulation benchmarks.

**Approaches in MORL:**
1. **Scalarization-Based Methods:** Use linear scalarization to convert reward vector to scalar → solve with standard RL
2. **Gradient-Balancing Methods:** Apply MGDA directly to policy gradients from each reward objective
3. **Learning the Entire Pareto Set:** Learn a single preference-conditioned policy $\pi_\theta(s, \alpha)$ that acts optimally for any desired trade-off $\alpha$

---

### 4.4 LLM Alignment

#### Multi-Objective Alignment

**The Problem:** LLM alignment is crucial to ensure outputs reflect human values, but human values are multi-dimensional and may conflict (e.g., helpfulness vs. harmlessness).

**Rewarded Soups (RS) [26] and MOD [27]:**
- Fine-tune $m$ LLMs for $m$ preference dimensions **separately**
- At inference, combine in:
  - **RS:** Parameter space (interpolate weights)
  - **MOD:** Logit space (combine next-token distributions)

#### Multi-Objective Test-Time Alignment

**Key Challenge:** Fine-tuning is computationally expensive (e.g., fine-tuning a 65B LLM requires 8× A100-80G GPUs).

**Open Problem:** Can we achieve multi-objective alignment while keeping the base LLM **frozen**?

#### GenARM [29]

**Core Idea:** Use a reward model to guide the frozen base LLM's generation, inspired by the closed-form solution of RLHF [28]:

$$\log \pi(y|x) = \underbrace{-\log Z(x)}_{\text{partition function}} + \underbrace{\log \pi_{\text{base}}(y|x)}_{\text{base LLM}} + \underbrace{\frac{1}{\beta} r(x, y)}_{\text{reward score}}$$

**Autoregressive Reward Model (ARM):** Trained to output **token-level** rewards.

**ARM Design:**
$$r(x, y) = \sum_t \log \pi_\theta(y_t | x, y_{<t})$$

**Training Objective:**
$$f(\pi_\theta, \mathcal{D}) := -\mathbb{E}_{(x, y^1, y^2, z) \sim \mathcal{D}} \left[\log \sigma\left((-1)^z \beta_r (r(y^1, x) - r(y^2, x))\right)\right]$$

where $z$ indicates preference ($z=1$ means $y^1$ preferred over $y^2$).

**Multi-objective Guided Generation:** Train $m$ ARMs $\{\pi_{\theta_i}\}_{i=1}^m$. Given preference vector $\alpha$:

$$\log \pi(y_t | x, y_{<t}) = -\log Z(x, y_{<t}) + \log \pi_{\text{base}}(y_t | x, y_{<t}) + \frac{1}{\beta} \sum_{i=1}^m \alpha_i \log \pi_{\theta_i}(y_t | x, y_{<t})$$

---

### 4.5 AI for Science: Multi-Objective Molecule Design

**Properties to Optimize:**
- QED (drug-likeness)
- LogP (octanol-water partition coefficient)
- LogS (log of solubility)
- SA (synthetic accessibility)
- DRD2 (dopamine receptor D2 affinity)
- JNK3 (c-Jun N-terminal Kinase 3 inhibition)
- GSK3β (Glycogen Synthase Kinase 3 Beta inhibition)

**Property Calculators:** https://github.com/sdv-dev/RDT

**Three Generation Approaches:**

#### 1. LLM-based: MOLLEO [30]
Uses LLMs for crossover and mutation in evolutionary optimization:
- Summation of individual objectives used as single objective to retain $n_c$ fittest members
- Only the Pareto frontier of current population is kept
- Repeat until maximum budget is used

#### 2. Diffusion-Based [32]
Uses **Diffusion Posterior Sampling (DPS)**:
$$\hat{z}_0 := \mathbb{E}_{z_0 \sim p(z_0|z_t)}[z_0] = \frac{1}{\sqrt{\bar{\alpha}_t}}\left(z_t + (1 - \bar{\alpha}_t) \nabla_{z_t} \log p_t(z_t)\right)$$

Multi-objective two-step diffusion:
$$z_t \leftarrow z_t + \underbrace{\nabla_{z_t} \log p_t(z_t)}_{\text{valid molecules}} + \underbrace{\nabla_{z_t} \log p_t(y_1|z_t)}_{\text{property 1 guidance}}$$
$$z_t \leftarrow z_t + \nabla_{z_t} \log p_t(z_t) + \underbrace{\nabla_{z_t} \log p_t(y_2|z_t)}_{\text{property 2 guidance}}$$

#### 3. GFlowNet-Based: HN-GFN [33] and MO-GFlowNet [34]

**Core Idea:** Distribution of $P(x)$ is proportional to reward $R(x)$.

**Algorithm:**
1. Sample a random preference $\lambda$ from the Dirichlet distribution
2. Compute scalarized reward $R(x;\lambda) = g(R(x), \lambda)$
3. Optimize trajectory balance loss:

$$L(\tau, \lambda; \theta) = \left(\log \frac{Z_\theta(\lambda) \prod_{s \to s' \in \tau} P_F(s'|s, \lambda; \theta)}{R(x|\lambda) \prod_{s \to s' \in \tau} P_B(s|s', \lambda; \theta)}\right)^2$$

4. Update hypernetwork parameters $\phi$: $\phi \leftarrow \phi - \eta \nabla_\phi L(\theta_\phi(\lambda))$

#### MO-LLM [31]

A more sophisticated LLM-based multi-objective optimization platform that:
- **Summarizes experience into prompts** (unlike MOLLEO)
- Uses a **hybrid strategy** to maintain populations balancing diversity and convergence

MO-LLM has achieved **world records** on:
- Circle packing problems (e.g., $n=26$: 2.635983 vs. AlphaEvolve's 2.635863)
- Structure design
- Mathematical discovery

---

### 4.6 Open-Source Libraries

#### LibMOON [35]

A gradient-based multi-objective optimization library in PyTorch (NeurIPS 2024).

**Supported components:** Problem classes, solver classes, core solver classes.

**PSL Gradient Decomposition:**
$$\frac{\partial \ell_{\text{psl}}}{\partial \phi} = \mathbb{E}_{\lambda \sim \text{Dir}(p)} \underbrace{\frac{\partial \tilde{g}}{\partial f}}_{\tilde{\alpha}: 1 \times m} \cdot \underbrace{\frac{\partial f}{\partial \theta}}_{B: m \times n} \cdot \underbrace{\frac{\partial \theta}{\partial \phi}}_{C: n \times D}$$

The three parts correspond to:
1. **Which core solver is used** ($\frac{\partial \tilde{g}_\lambda}{\partial f}$)
2. **How to calculate the Jacobian matrix** — 0-order optimization or backprop ($\frac{\partial f}{\partial \theta}$)
3. **The PSL model** — hypernetwork or LoRA ($\frac{\partial \theta}{\partial \phi}$)

**Code Examples:**

*Generate an infinite set of solutions (PSL — synthetic):*
```python
problem = get_problem(problem_name=args.problem_name, n_var=args.n_var)
solver = BasePSLSolver(problem, batch_size=args.batch_size, device=args.device, ...)
model, loss_history = solver.solve()
```

*Generate a finite set of solutions:*
```python
problem = get_problem(problem_name=args.problem_name, n_var=args.n_var)
prefs = get_prefs(n_prob=args.n_prob, n_obj=problem.n_obj, mode='uniform', clip_eps=1e-2)
core_solver = EPOCore(n_var=problem.n_var, prefs=prefs)
solver = GradBaseSolver(step_size=args.step_size, epoch=args.epoch, tol=args.tol, core_solver=core_solver)
res = solver.solve(problem=problem, x=synthetic_init(problem, prefs), prefs=prefs)
```

*MOO-MTL:*
```python
model = model_from_dataset(args.problem_name)
num_param = numel(model)
core_solver = EPOCore(n_var=num_param, prefs=prefs)
solver = GradBaseMTLSolver(problem_name=args.problem_name, step_size=args.step_size, epoch=args.epoch,
                           core_solver=core_solver, batch_size=args.batch_size, prefs=prefs)
res = solver.solve()
```

#### LibMTL [36]

A PyTorch library for Multi-Task Learning (2,400+ stars, published in JMLR).

**Supports:**
- 26 optimization strategies
- 8 architectures
- 6 datasets

**Modular Design:** Easy to customize MTL problems, plug in existing methods, or implement new methods for fair benchmarking.

---

## Open Challenges and Future Directions

### Challenge 1: Theoretical Understanding

**Problem:**
- Theoretical foundations of many practical multi-objective deep learning methods are not fully understood
- Research has mainly focused on **convergence**, with less attention on **generalization error** — crucial for real-world performance

**Future Direction:**
- Develop broader, algorithm-agnostic generalization analyses
- Theoretically investigate how network design choices affect Pareto set approximation

---

### Challenges 2 & 3: Efficiency and Scalability

**Reducing Gradient Balancing Costs:**
- *Problem:* Gradient balancing methods have significant computational overhead
- *Future Direction:* Integrate gradient balancing with simpler methods like linear scalarization to reduce costs and enable large-scale use

**Dealing with Many Objectives:**
- *Problem:* Preference vector space grows exponentially with more objectives → random sampling ineffective for learning the Pareto set
- *Future Direction:*
  - Efficient sampling strategies for high-dimensional preference spaces
  - Methods to automatically reduce or merge objectives based on their properties

---

### Challenge 4: Distributed Training

**Problem:**
- Most current MOO algorithms are designed for a single GPU or machine
- Scaling to multi-GPU and distributed environments introduces unique challenges not seen in single-objective optimization

**Future Directions:**
- **Efficient Communication:** Design methods for efficient gradient distribution and synchronization across multiple GPUs/nodes
- **Privacy-Preserving MOO:** Develop techniques for collaborative training when data for different objectives is on separate devices and cannot be shared

---

### Challenge 5: Advancements in LLMs

**Problem:**
- Current MOO applications for LLMs are mostly concentrated on the RLHF stage
- User preferences are often simplified into a basic preference vector, which may not capture the complexity of human needs

**Future Directions:**
- Apply MOO techniques to other stages of the LLM lifecycle (pre-training, instruction tuning, etc.)
- Explore more sophisticated methods to represent and incorporate complex and nuanced user preferences

---

### Challenge 6: Application in More Scenarios

**The Untapped Potential:**
- Most deep learning problems are inherently multi-objective (models evaluated on multiple criteria)
- These criteria often create natural trade-offs that are perfect candidates for MOO

**Future Direction:**
- Actively leverage MOO methods to explicitly navigate these trade-offs in a wider range of deep learning applications
- Move from single-metric optimization to a more holistic, multi-objective approach to model development

---

## Key Takeaways

1. **MOO is everywhere in deep learning:** Multi-task learning, RLHF, model merging, NAS, drug discovery — all involve inherently conflicting objectives.

2. **Pareto optimality provides a principled framework:** Instead of fixing weights arbitrarily, MOO finds the entire trade-off surface (Pareto front) or a preferred point on it.

3. **Loss balancing vs. gradient balancing trade-off:**
   - Loss balancing: cheap, easy, but heuristic
   - Gradient balancing: better performance and guarantees, but expensive

4. **Scalarization methods** (weighted sum, Tchebycheff, smooth Tchebycheff) are the workhorse for reducing MOO to solvable subproblems.

5. **MGDA / PCGrad / CAGrad** are the key gradient-based methods for finding a single Pareto optimal solution — each with different geometric intuitions for resolving gradient conflicts.

6. **Preference-conditioned learning** (PSL) allows a single model to represent the entire Pareto set, enabling real-time preference adaptation at inference.

7. **Hypervolume** is the gold-standard quality indicator for evaluating a finite set of Pareto solutions, measuring both convergence and diversity.

8. **Many-objective settings** ($m \gg K$) require fundamentally different strategies — "Few for Many" and Sum-of-Minimal reformulations allow tractable approximation.

9. **LLM alignment** is a natural MOO problem — GenARM and Rewarded Soups represent complementary approaches (frozen vs. fine-tuned base model).

10. **Open-source tools** (LibMOON, LibMTL) lower the barrier to applying MOO in deep learning research and practice.

---

## References Mentioned

| # | Reference | Context |
|---|-----------|---------|
| [1] | A. B. Arrieta et al., "Explainable artificial intelligence (xai): Concepts, taxonomies, opportunities and challenges toward responsible ai," *Information Fusion*, vol. 58, pp. 82–115, 2020. | ML model accuracy-interpretability trade-off |
| [2] | Y. Gu et al., "Jet-nemotron: Efficient language model with post neural architecture search," *arXiv:2508.15884*, 2025. | LLM performance-speed trade-off example |
| [3] | Y. Zhong et al., "Panacea: Pareto alignment via preference adaptation for LLMs," *NeurIPS*, 2024. | LLM alignment helpfulness vs. harmlessness |
| [4] | S. Luukkonen et al., "Artificial intelligence in multi-objective drug design," *Current Opinion in Structural Biology*, vol. 79, p. 102537, 2023. | AI for multi-objective drug design |
| [5] | S. Liu, E. Johns, and A. J. Davison, "End-to-end multi-task learning with attention," *CVPR*, 2019. | Dynamic Weight Average (DWA) |
| [6] | A. Kendall, Y. Gal, and R. Cipolla, "Multi-task learning using uncertainty to weigh losses for scene geometry and semantics," *CVPR*, 2018. | Uncertainty Weighting (UW) |
| [7] | B. Lin et al., "Dual-balancing for multi-task learning," *arXiv:2308.12029*, 2023. | Log transformation equivalence for IMTL-L |
| [8] | L. Liu et al., "Towards impartial multi-task learning," *ICLR*, 2021. | IMTL-L (loss) and IMTL-G (gradient) methods |
| [9] | F. Ye et al., "Multi-objective meta learning," *NeurIPS*, 2021. | MOML bi-level optimization |
| [10] | S. Liu et al., "Auto-Lambda: Disentangling dynamic task relationships," *TMLR*, 2022. | Efficient extension of MOML |
| [11] | F. Ye et al., "A first-order multi-gradient algorithm for multi-objective bi-level optimization," *ECAI*, 2024. | FORUM — efficient extension of MOML |
| [12] | B. Lin et al., "Reasonable effectiveness of random weighting: A litmus test for multi-task learning," *TMLR*, 2022. | Random Weighting as strong baseline |
| [13] | X. Lin et al., "Smooth tchebycheff scalarization for multi-objective optimization," *ICML*, 2024. | Smooth Tchebycheff Scalarization (STCH) |
| [14] | O. Sener and V. Koltun, "Multi-task learning as multi-objective optimization," *NeurIPS*, 2018. | MGDA — gradient weighting |
| [15] | B. Liu et al., "Conflict-averse gradient descent for multi-task learning," *NeurIPS*, 2021. | CAGrad — gradient weighting |
| [16] | T. Yu et al., "Gradient surgery for multi-task learning," *NeurIPS*, 2020. | PCGrad — gradient manipulation |
| [17] | A. Navon et al., "Multi-task learning as a bargaining game," *ICML*, 2022. | Periodic weight update speedup strategy |
| [18] | B. Liu et al., "FAMO: Fast adaptive multitask optimization," *NeurIPS*, 2023. | FAMO — gradient-free speedup for MGDA |
| [19] | Q. Zhang and H. Li, "MOEA/D: A multiobjective evolutionary algorithm based on decomposition," *IEEE TEC*, vol. 11, no. 6, pp. 712–731, 2007. | MOEA/D framework |
| [20] | E. Zitzler and L. Thiele, "Multiobjective optimization using evolutionary algorithms—a comparative case study," *PPSN*, 1998. | Hypervolume definition |
| [21] | X. Lin et al., "Few for many: Tchebycheff set scalarization for many-objective optimization," *ICLR*, 2025. | Few for Many — max-of-minima (CityUHK) |
| [22] | L. Ding et al., "Efficient algorithms for sum-of-minimum optimization," *ICML*, 2024. | Sum of Minimal (SoM) — UCLA |
| [23] | W. Chen and J. Kwok, "Pareto merging: Multi-objective optimization for preference-aware model merging," *ICML*, 2025. | Pareto merging for model merging |
| [24] | L. Li et al., "Map: Low-compute model merging with amortized pareto fronts via quadratic approximation," *arXiv:2406.07529*, 2024. | MAP — low-compute model merging |
| [25] | T. Yu et al., "Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning," *CoRL*, 2020. | Meta-World benchmark (10/50 objectives) |
| [26] | A. Rame et al., "Rewarded soups: Towards Pareto-optimal alignment by interpolating weights fine-tuned on diverse rewards," *NeurIPS*, 2023. | Rewarded Soups (RS) for LLM alignment |
| [27] | R. Shi et al., "Decoding-time language model alignment with multiple objectives," *NeurIPS*, 2024. | MOD — logit-space alignment |
| [28] | R. Rafailov et al., "Direct preference optimization: Your language model is secretly a reward model," *NeurIPS*, 2023. | DPO — closed-form RLHF solution |
| [29] | Y. Xu et al., "GenARM: Reward guided generation with autoregressive reward model for test-time alignment," *ICLR*, 2025. | GenARM — frozen LLM alignment |
| [30] | H. Wang et al., "Efficient evolutionary search over chemical space with large language models," *ICLR*, 2025. | MOLLEO — LLM-based molecule optimization |
| [31] | N. Ran, Y. Wang, and R. Allmendinger, "MOLLM: Multi-objective large language model for molecular design–optimizing with experts," *arXiv:2502.12845*, 2025. | MO-LLM — general LLM-based MOO platform |
| [32] | X. Han et al., "Training-free multi-objective diffusion model for 3d molecule generation," *ICLR*, 2024. | Multi-objective diffusion for molecule generation |
| [33] | Y. Zhu et al., "Sample-efficient multi-objective molecular optimization with GFlowNets," *NeurIPS*, 2023. | HN-GFN — hypernetwork GFlowNet |
| [34] | M. Jain et al., "Multi-objective GFlowNets," *ICML*, 2023. | MO-GFlowNet |
| [35] | X. Zhang et al., "LibMOON: A gradient-based multiobjective optimization library in PyTorch," *NeurIPS*, 2024. | LibMOON open-source library |
| [36] | B. Lin and Y. Zhang, "LibMTL: A Python library for deep multi-task learning," *JMLR*, vol. 24, no. 209, pp. 1–7, 2023. | LibMTL open-source library |
