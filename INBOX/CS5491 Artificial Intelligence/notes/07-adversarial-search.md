# Lecture 07 - Adversarial Search

**Course**: CS5491: Artificial Intelligence
**Reading**: RN Chapter 5.1–5.5

---

## 1. Game Playing — State of the Art

| Game | Milestone |
|------|-----------|
| **Checkers** | 1950: First computer player; 1994: Chinook beats human champion; 2007: Solved |
| **Chess** | 1997: **Deep Blue** defeats Gary Kasparov (200M positions/sec, up to 40-layer search) |
| **Go** | 2016: **AlphaGo** defeats human champion (Monte Carlo Tree Search + learned eval function; b > 300) |

---

## 2. Types of Games

| Axis | Options |
|------|---------|
| Outcomes | Deterministic vs. Stochastic |
| Players | 1, 2, or more |
| Sum | Zero-sum vs. General |
| Observability | Perfect vs. Imperfect information |

**Goal**: Find a **policy** (strategy) `S → A` that recommends the best action from each state.

---

## 3. Deterministic Game Formalization

| Component | Description |
|-----------|-------------|
| `S` | States (start at `s₀`) |
| `P = {1, ..., N}` | Players (usually alternate turns) |
| `A` | Actions (may depend on player/state) |
| `T: S × A → S` | Transition function |
| `Terminal Test: S → {t, f}` | Is the game over? |
| `Terminal Utilities: S × P → ℝ` | Payoff at terminal states |
| **Solution** | Policy `π: S → A` |

---

## 4. Zero-Sum vs. General Games

| Type | Utilities | Nature |
|------|-----------|--------|
| **Zero-Sum** | Agents have **opposite** utilities | Pure competition — one maximizes, one minimizes |
| **General** | Agents have **independent** utilities | Cooperation, indifference, or competition all possible |

---

## 5. Single-Agent Value

For a single agent:
- **Terminal states**: `V(s)` is known
- **Non-terminal states**: `V(s) = max_{s' ∈ children(s)} V(s')`

The agent always picks the action leading to the highest-value child.

---

## 6. Minimax

### 6.1 Minimax Values

| Node Type | Value Rule |
|-----------|-----------|
| **MAX node** (agent's turn) | `V(s) = max_{s'} V(s')` |
| **MIN node** (opponent's turn) | `V(s) = min_{s'} V(s')` |
| **Terminal** | `V(s)` = given utility |

### 6.2 Adversarial Search (Minimax)
- For **deterministic, zero-sum** games (tic-tac-toe, chess, checkers)
- One player **maximizes**, the other **minimizes**
- Computes each node's **minimax value**: best achievable utility against a **rational adversary**

### 6.3 Minimax Algorithm (Pseudocode)
```
function MINIMAX(state, depth):
    if TERMINAL(state): return UTILITY(state)
    if MAX's turn:
        return max over successors: MINIMAX(s', depth-1)
    else (MIN's turn):
        return min over successors: MINIMAX(s', depth-1)
```

### 6.4 Minimax Properties

| Property | Value |
|----------|-------|
| **Complete** | Yes (if tree is finite) |
| **Optimal** | Yes, against a perfect adversary |
| **Time** | `O(bᵐ)` |
| **Space** | `O(bm)` |

**Chess**: `b ≈ 35`, `m ≈ 100` → exact solution completely infeasible!

---

## 7. Alpha-Beta Pruning

### 7.1 Key Idea

We can skip evaluating subtrees that **cannot affect** the final decision at the root.

### 7.2 How It Works

- `α` = best value MAX can guarantee so far (along current path)
- `β` = best value MIN can guarantee so far (along current path)

**Pruning rules**:
- At a MIN node: if current value ≤ α → prune (MAX won't choose this branch)
- At a MAX node: if current value ≥ β → prune (MIN won't choose this branch)

### 7.3 Alpha-Beta Properties

| Property | Detail |
|----------|--------|
| **Correctness** | No effect on minimax value at the **root** |
| **Intermediate values** | May be wrong (but we only care about the root) |
| **Action selection** | Naïve version may give wrong values to root's children — need care |
| **Child ordering** | Good ordering dramatically improves pruning |
| **Best case (perfect ordering)** | Time: `O(b^(m/2))` — **doubles searchable depth** |

> Alpha-beta with perfect ordering can solve problems twice as deep as minimax alone.
> Even with alpha-beta, full chess search is still impossible.

---

## 8. Depth-Limited Search & Evaluation Functions

**Problem**: Cannot search to terminal nodes in realistic games.

**Solution**:
- Set a **depth limit**
- Replace terminal utilities with an **evaluation function** `Eval(s)` for non-terminal positions

**Evaluation Function Requirements**:
- Should **agree with terminal utilities** on terminal states
- Should be **fast** to compute
- Should **correlate with actual winning probability**

**Example** (chess): `Eval(s)` = weighted sum of piece values + position factors

**Example computation**:
- 100 seconds, 10K nodes/sec → 1M nodes per move
- Alpha-beta reaches depth ~8 → decent chess program

> **More depth = much better play**. Use **iterative deepening** for "anytime" behavior.

---

## 9. Summary: Minimax & Alpha-Beta

| Algorithm | Time | Space | Optimal | Notes |
|-----------|------|-------|---------|-------|
| Minimax | `O(bᵐ)` | `O(bm)` | Yes (vs perfect opp) | Too slow for real games |
| Alpha-Beta | `O(b^(m/2))` best | `O(bm)` | Yes (same as minimax) | Best with good ordering |
| Depth-limited | Bounded | Bounded | No | Uses evaluation function |

---

## 10. Key Concepts

| Term | Definition |
|------|-----------|
| **Zero-sum game** | One player's gain = other's loss |
| **Minimax** | MAX maximizes, MIN minimizes; both play optimally |
| **Alpha-Beta** | Pruning technique — skips provably irrelevant branches |
| `α` | Best MAX value found along current path |
| `β` | Best MIN value found along current path |
| **Evaluation function** | Heuristic estimate of state value for depth-limited search |
| **Metareasoning** | Computing about what to compute (e.g., when to prune) |
