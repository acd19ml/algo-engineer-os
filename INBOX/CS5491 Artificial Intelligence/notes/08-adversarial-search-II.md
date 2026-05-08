# Lecture 08 - Adversarial Search II: Expectimax & Utilities

**Course**: CS5491: Artificial Intelligence
**Reading**: RN Chapters 16.1–16.3

---

## 1. Uncertain Outcomes: Worst Case vs. Average Case

| Approach | Assumption | Method |
|----------|------------|--------|
| **Minimax** | Adversary plays **optimally** (worst case) | MIN node |
| **Expectimax** | Outcomes are **random** (average case) | Chance node |

> **Key insight**: Not all uncertainty comes from an adversary. Sometimes the environment is random, not adversarial.

---

## 2. Why Outcomes Are Uncertain

| Source | Example |
|--------|---------|
| **Explicit randomness** | Rolling dice |
| **Unpredictable opponents** | Ghosts move randomly in Pac-Man |
| **Action failure** | Robot wheels slip |

---

## 3. Expectimax Search

### 3.1 Structure

| Node Type | Computation |
|-----------|-------------|
| **MAX node** | Same as minimax: `V(s) = max_{s'} V(s')` |
| **Chance node** | `V(s) = Σ P(outcome) · V(outcome)` (weighted average) |
| **Terminal** | `V(s)` = given utility |

### 3.2 Algorithm
```
function EXPECTIMAX(state, depth):
    if TERMINAL(state): return UTILITY(state)
    if MAX node:
        return max over successors: EXPECTIMAX(s', depth-1)
    if CHANCE node:
        return Σ P(s') * EXPECTIMAX(s', depth-1)
```

### 3.3 Example Calculation
```
Chance node: V = (1/2) × 8 + (1/3) × 24 + (1/6) × (−12) = 4 + 8 − 2 = 10
```

### 3.4 Expectimax Pruning
- Pruning is harder than in minimax (α-β doesn't directly apply)
- Can prune only with **known probability bounds** and **value bounds**

---

## 4. Probability Primer

### Random Variable & Distribution
- **Random variable**: represents an event with unknown outcome
- **Probability distribution**: assigns weights to all outcomes; must sum to 1

**Example**:
- `P(T=none) = 0.25`, `P(T=mild) = 0.50`, `P(T=heavy) = 0.25`

### Laws
- `P(outcome) ≥ 0` for all outcomes
- `Σ P(outcome) = 1`
- Probabilities update with evidence: `P(T=heavy | Hour=8am) = 0.60`

### Expected Value
```
E[f(X)] = Σ P(X=x) · f(x)
```
The **weighted average** of outcomes under the probability distribution.

---

## 5. What Probabilities to Use?

In expectimax, we need a probabilistic model of the environment/opponent:

| Model Type | Example |
|------------|---------|
| **Uniform** | Roll a fair die — all outcomes equally likely |
| **Learned model** | Trained on opponent behavior data |
| **Adversarial model** | Assumes worst-case behavior (→ minimax) |

> **Chance nodes** represent anything **out of the agent's control** (opponent OR environment).

---

## 6. Modeling Assumptions: Dangers

| Error | Description | Consequence |
|-------|-------------|-------------|
| **Dangerous Optimism** | Assume random when opponent is adversarial | Agent gets exploited |
| **Dangerous Pessimism** | Assume adversarial when opponent is random | Agent plays too conservatively |

### Pac-Man Experiment Results

| Ghost Type | Minimax Pacman | Expectimax Pacman |
|------------|---------------|-------------------|
| **Adversarial** | Won 5/5, Score: 483 | Won **1/5**, Score: -303 |
| **Random** | Won 5/5, Score: 493 | Won 5/5, Score: **503** |

> **Lesson**: Match your model to reality. Using the wrong model can be disastrous.

---

## 7. Mixed Agent Games (Expectiminimax)

Some games have both adversarial and random elements (e.g., **Backgammon**):
- Environment acts as an extra **random agent**
- Tree has MAX, MIN, and CHANCE nodes
- Each node computes the appropriate combination

**Backgammon**:
- 21 possible dice rolls × ~20 legal moves → `b ≈ 420`
- Depth 2: `20 × (21 × 20)³ ≈ 1.2 × 10⁹` nodes
- As depth increases, probability of reaching a node decreases → limiting depth is less damaging

**TDGammon**: Depth-2 search + excellent evaluation function + **reinforcement learning** → world champion level. First AI world champion in any game!

---

## 8. Utilities

### 8.1 What Are Utilities?
- Functions from **outcomes (world states) to real numbers**
- Describe an agent's **preferences**

### 8.2 Where Do Utilities Come From?
- Simple games: `+1/-1` (win/lose)
- Complex domains: carefully designed reward functions
- **Theorem**: Any "rational" preferences can be represented as a utility function

### 8.3 Scale of Utilities

| Search Type | Scale Matters? | Reason |
|-------------|----------------|--------|
| **Minimax** | No | Only ordering matters (monotonic transformation invariant) |
| **Expectimax** | **Yes** | Magnitudes affect expected value computation |

> For expectimax, doubling all utilities doubles the expected value — but the best action remains the same. However, **non-linear** transformations can change the optimal action.

### 8.4 Principle of Maximum Expected Utility

> **A rational agent should choose the action that maximizes its expected utility, given its knowledge.**

**Key questions**:
- Where do utilities come from? → Design or learn them
- Why average? → Follows from axioms of rational preference
- What if behavior can't be described by utilities? → That implies irrational preferences

### 8.5 Why Hard-Wire Utilities?
- Don't let agents pick their own utilities (they might optimize for wrong things)
- Don't prescribe behaviors directly (too rigid)
- Instead: **specify utility, let rational behavior emerge**

---

## 9. Summary: Search Algorithms for Games

| Scenario | Algorithm | Key Feature |
|----------|-----------|-------------|
| Deterministic, 2-player, zero-sum | **Minimax** | Perfect adversary |
| + Pruning | **Alpha-Beta** | Skip irrelevant branches |
| Stochastic environment | **Expectimax** | Expected value over chance |
| Mixed (adversary + random) | **Expectiminimax** | Combine all node types |
| Resource-limited | **Depth-limited + Eval** | Stop early, estimate value |

---

## 10. Key Formulas

| Formula | Meaning |
|---------|---------|
| `V(s) = max_{s'} V(s')` | MAX node value |
| `V(s) = min_{s'} V(s')` | MIN node value |
| `V(s) = Σ P(s') · V(s')` | CHANCE node (expectimax) value |
| `E[U] = Σ P(outcome) · U(outcome)` | Expected utility |
