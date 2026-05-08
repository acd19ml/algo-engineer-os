# CS5491 AI — Tutorial Exam #2（L05–L08）

**Spring 2026 | Total: 45 pts | Recommended Time: ~2 hours**

**Name:** __________________ **Student ID:** __________________

---

> **Instructions:** Open-book (physical notes only). Show all working. Justify every T/F answer — unsupported answers earn at most 0.5 pts. State any additional assumptions clearly.

---

## Section 1 — True / False with Justification *(10 pts, 2 pts each)*

---

**(a)** (2 pts) **T / F** — Forward Checking can detect all constraint failures that Arc Consistency (AC-3) is able to detect.

*Justification:*

&nbsp;

&nbsp;

---

**(b)** (2 pts) **T / F** — Alpha-Beta pruning may change the minimax value at the **root** node compared to plain Minimax search.

*Justification:*

&nbsp;

&nbsp;

---

**(c)** (2 pts) **T / F** — In a Minimax game, the optimal action chosen at the root is preserved when **all** terminal utilities are multiplied by the same positive constant k > 0.

*Justification:*

&nbsp;

&nbsp;

---

**(d)** (2 pts) **T / F** — In an Expectimax game, the optimal action chosen at the root is preserved under **any** monotone increasing transformation of the terminal utilities (e.g., squaring all values).

*Justification:*

&nbsp;

&nbsp;

---

**(e)** (2 pts) **T / F** — A tree-structured CSP with n variables and domain size d can be solved in O(nd²) time, which is exponentially faster than the O(dⁿ) worst-case of general backtracking.

*Justification:*

&nbsp;

&nbsp;

---

## Section 2 — Constraint Satisfaction Problems *(12 pts)*

A university must assign **rooms** to four simultaneous-exam sessions: **A**lgebra, **B**iology, **C**hemistry, **D**atabases. Available rooms: **{1, 2, 3}**. Two exams that share student groups must be in **different rooms**. The conflict pairs are:

> A conflicts with B, A conflicts with C, B conflicts with C, B conflicts with D, C conflicts with D.
> *(There is **no** conflict between A and D — they draw from different student populations.)*

---

### (a) CSP Formulation (2 pts)

State the CSP formally.

**Variables:**

**Domains:**

**Constraints** (list all, using ≠ notation):

---

### (b) Constraint Graph (2 pts)

Draw or fully describe the constraint graph. List: (i) all nodes, (ii) all edges, (iii) the degree of each node.

*(Space for graph / description)*

&nbsp;

&nbsp;

Is any single variable connected to **all** other variables? _______________

---

### (c) Backtracking with MRV + Forward Checking + LCV (4 pts)

Run backtracking on this CSP. Use **MRV** to select variables (alphabetical tiebreak) and **LCV** to order values (ties broken by smallest value first). Apply **Forward Checking** after each assignment.

Show the full trace in the table below. A blank row means no action; add or remove rows as needed.

| Step | Variable Chosen | MRV (domain sizes) | Value Assigned | Domain updates after FC |
|------|-----------------|-------------------|----------------|------------------------|
| Init | — | A:3, B:3, C:3, D:3 | — | — |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

**Final assignment:** A = ___ B = ___ C = ___ D = ___

**Did any backtracking occur?** _______________

---

### (d) Arc Consistency — REVISE (2 pts)

Suppose you have just assigned **A = 1** and **B = 2** (in that order, with Forward Checking applied after each). Write out the current domain of each variable at this point:

| Variable | Domain after A=1, B=2 |
|----------|----------------------|
| A | {1} |
| B | {2} |
| C | |
| D | |

Now apply the **REVISE** procedure to arc **(D, C)** — i.e., check whether D's domain needs to be pruned given the constraint D ≠ C. Show each step:

For each value d ∈ domain(D): does there exist c ∈ domain(C) such that d ≠ c?

| d | Supported? (∃ c ∈ domain(C) s.t. d ≠ c) | Keep or Remove? |
|---|------------------------------------------|-----------------|
| | | |
| | | |
| | | |

**D's domain after REVISE(D, C):** _______________

**Did the domain change?** _______________

---

### (e) Problem Structure (2 pts)

**(i)** Is the constraint graph a **tree** (acyclic)? If not, identify one cycle in the graph.

&nbsp;

&nbsp;

**(ii)** Identify a **minimum-size cutset** (set of variables whose removal makes the remaining graph a tree). What is the cutset size c? Write the time complexity of solving the full CSP using cutset conditioning with this cutset.

**Minimum cutset:** _______________  **Size c =** ___

**Time complexity:** _______________

---

## Section 3 — Adversarial Search *(18 pts)*

---

### Part A — Minimax & Alpha-Beta (14 pts)

Consider the Minimax tree below. The **root is a MAX node**. Children are explored **left to right**. Leaf values are given; all internal nodes at level 3 are MIN nodes, at level 2 are MAX nodes, at level 1 are MIN nodes.

**Tree structure** (described systematically; draw your own diagram to assist):

```
ROOT (MAX)
├── L (MIN)
│   ├── LL (MAX)
│   │   ├── A (MIN) → leaves: 3, 12
│   │   └── B (MIN) → leaves: 8, 2
│   └── LR (MAX)
│       ├── C (MIN) → leaves: 14, 5
│       └── D (MIN) → leaves: 2, 4
└── R (MIN)
    ├── RL (MAX)
    │   ├── E (MIN) → leaves: 5, 10
    │   └── F (MIN) → leaves: 7, 11
    └── RR (MAX)
        ├── G (MIN) → leaves: 9, 3
        └── H (MIN) → leaves: 15, 6
```

---

#### (a.i) Minimax Values (5 pts)

Fill in the minimax value for **every** non-leaf node. Show all working.

| Node | Children values | Minimax value |
|------|----------------|---------------|
| A (MIN) | 3, 12 | |
| B (MIN) | 8, 2 | |
| C (MIN) | 14, 5 | |
| D (MIN) | 2, 4 | |
| E (MIN) | 5, 10 | |
| F (MIN) | 7, 11 | |
| G (MIN) | 9, 3 | |
| H (MIN) | 15, 6 | |
| LL (MAX) | A, B | |
| LR (MAX) | C, D | |
| RL (MAX) | E, F | |
| RR (MAX) | G, H | |
| L (MIN) | LL, LR | |
| R (MIN) | RL, RR | |
| ROOT (MAX) | L, R | |

**Optimal action at root:** Go ___ (L / R)

---

#### (a.ii) Alpha-Beta Pruning (6 pts)

Run Alpha-Beta pruning on the same tree (left to right). For **each** internal node visited, record the α and β values when it is **first entered** and when it **returns**. Indicate any node/subtree that is **pruned** (not visited) and explain **why** (which cutoff condition triggered, and at which ancestor).

Use the table below. Add rows for every node visited.

| Node | Type | α when entered | β when entered | Value returned | Pruning? (reason) |
|------|------|----------------|----------------|----------------|-------------------|
| ROOT | MAX | −∞ | +∞ | | |
| L | MIN | | | | |
| LL | MAX | | | | |
| A | MIN | | | | |
| B | MIN | | | | |
| LR | MAX | | | | |
| C | MIN | | | | |
| D | MIN | | | | **PRUNED?** |
| R | MIN | | | | |
| RL | MAX | | | | |
| E | MIN | | | | |
| F | MIN | | | | |
| RR | MAX | | | | |
| G | MIN | | | | |
| H | MIN | | | | |

**Which subtree(s) / leaf node(s) are never evaluated?** _______________

**Which pruning condition triggered (α-cutoff or β-cutoff), and at which node?**

&nbsp;

&nbsp;

---

#### (a.iii) Depth-Limited Minimax Reflection (3 pts)

Suppose you are building a chess engine and can evaluate 10⁷ nodes per second. You have 5 seconds per move (so 5 × 10⁷ = 5×10⁷ nodes total). The branching factor is b = 35.

**(i)** With plain Minimax (no pruning), what is the maximum depth d you can reach? Show the calculation.

&nbsp;

&nbsp;

**(ii)** With Alpha-Beta pruning under **perfect move ordering**, what is the maximum depth reachable? (Use the best-case complexity O(b^(d/2)).)

&nbsp;

&nbsp;

**(iii)** Briefly explain why good move ordering is critical for Alpha-Beta, and give one heuristic for move ordering in a chess-like game.

&nbsp;

&nbsp;

---

### Part B — Expectimax (4 pts)

You are a robot choosing a maintenance strategy (Left branch or Right branch). The environment is uncertain. The tree is:

```
ROOT (MAX)
├── Left → CHANCE node
│   ├── prob 1/2 → MAX node → children {10, 6}
│   ├── prob 1/4 → MAX node → children {2, 8}
│   └── prob 1/4 → terminal: 0
└── Right → CHANCE node
    ├── prob 2/3 → MAX node → children {4, 12}
    └── prob 1/3 → terminal: 3
```

Compute the Expectimax value at the root. Show all sub-calculations. Fill in the table:

| Node | Type | Computation | Value |
|------|------|-------------|-------|
| Left's MAX child 1 | MAX | max(10, 6) | |
| Left's MAX child 2 | MAX | max(2, 8) | |
| Left | CHANCE | | |
| Right's MAX child | MAX | max(4, 12) | |
| Right | CHANCE | | |
| ROOT | MAX | max(Left, Right) | |

**Optimal strategy:** Choose ___ (Left / Right)

---

## Section 4 — Conceptual Analysis *(5 pts)*

---

**(a) [2 pts]** — **Utility Scales and Game Algorithms**

Consider a two-player game where the Minimax values at the root's two children are 4 (Left) and 7 (Right). Now suppose someone squares all terminal utilities: all leaf values are replaced by their squares.

**(i)** Does the optimal Minimax action change? Explain using the invariance property of Minimax.

&nbsp;

&nbsp;

**(ii)** Suppose this is instead an **Expectimax** game. The Left chance node has leaf values {2, 6} with equal probability (1/2 each), and Right has leaf values {1, 9} with equal probability. Compute E[Left] and E[Right] before and after squaring. Does the optimal Expectimax action change? Explain why Expectimax is NOT invariant to squaring.

&nbsp;

&nbsp;

&nbsp;

---

**(b) [3 pts]** — **Choosing the Right Model**

A Pac-Man ghost has two modes: (A) in "scatter" mode it moves completely randomly, and (B) in "chase" mode it uses a fixed rule to move toward Pac-Man. You don't know which mode the ghost is in — you estimate it's in scatter mode with probability 0.8.

**(i)** Should Pac-Man use **Minimax** or **Expectimax** to plan its next move? Justify with reference to the underlying assumptions of each algorithm.

&nbsp;

&nbsp;

**(ii)** If you model the ghost as a **Minimax adversary** when it is actually in scatter mode 80% of the time, what mistake does your agent make? (Use the terms "Dangerous Optimism" or "Dangerous Pessimism" and explain the consequence.)

&nbsp;

&nbsp;

**(iii)** Propose a better model for this situation (one sentence).

&nbsp;

---

*End of Exam — Good Luck!*

---

---

# Answer Key

> ⚠️ Attempt the exam independently before reading.

---

## Section 1 — True / False

### (a) FALSE

Forward Checking (FC) only propagates constraint failures to the **direct neighbors** of the most recently assigned variable. Arc Consistency (AC-3) propagates failures **through the entire constraint graph**: when a variable loses a value, AC-3 re-examines all of that variable's neighbors, potentially triggering further eliminations across the graph. FC is strictly weaker — every failure FC detects, AC-3 also detects, but not vice versa.

*Example:* Consider a chain X→Y→Z. After assigning X=1, FC removes conflicting values from Y. But FC does not then re-examine Z based on Y's updated domain. AC-3 would continue and might further prune Z.

### (b) FALSE

Alpha-Beta pruning is provably **equivalent** to Minimax at the root. Pruned subtrees are those whose values cannot possibly affect the root outcome — they are provably irrelevant to the root's minimax value. The root value and the optimal action are identical to what plain Minimax would produce. (Note: intermediate node values may appear incorrect in alpha-beta, but the **root** value is always correct.)

### (c) TRUE

Minimax is determined by the **ordering** of terminal utilities, not their magnitudes. Multiplying all values by k > 0 applies a monotone increasing transformation: if A > B before scaling, then kA > kB after scaling. Since max and min preserve order, the entire tree's argmax/argmin structure is unchanged. The root's optimal action is therefore unaffected.

*Formal argument:* For any positive k, max(ka, kb) = k·max(a, b) and min(ka, kb) = k·min(a, b), so the tree values scale uniformly and the argmax at the root is unchanged.

### (d) FALSE

Expectimax computes **weighted averages** (expected values), which are sensitive to the magnitude of values, not just their ordering. Non-linear monotone transformations like squaring change relative expected values and can reverse the ordering between options.

*Counterexample:* Left has leaves {1, 9} each with prob 1/2: E[Left] = 5. Right has leaves {4, 6} each with prob 1/2: E[Right] = 5. Both equal. After squaring: E[Left²] = (1 + 81)/2 = 41. E[Right²] = (16 + 36)/2 = 26. Now Left is preferred — the optimal action changed from a tie to a clear preference for Left.

The correct statement: Expectimax is invariant only to **linear** transformations (af + b with a > 0).

### (e) TRUE

For a **tree-structured** CSP (acyclic constraint graph), the algorithm proceeds in two passes — backward arc-consistency elimination and forward assignment — each touching each variable-value pair at most once. The total work is O(nd²): n variables × d values × d-size domain comparisons. This is **polynomial**, vs. O(dⁿ) for naive backtracking (exponential). The speedup is exponential in n.

---

## Section 2 — CSP

### (a) Formulation

**Variables:** A, B, C, D
**Domains:** {1, 2, 3} for each variable
**Constraints:** A ≠ B, A ≠ C, B ≠ C, B ≠ D, C ≠ D

---

### (b) Constraint Graph

Nodes: A, B, C, D
Edges (one per constraint): A–B, A–C, B–C, B–D, C–D → **5 edges total**

Degrees:
- A: connected to B, C → degree **2**
- B: connected to A, C, D → degree **3**
- C: connected to A, B, D → degree **3**
- D: connected to B, C → degree **2**

Both **B and C** are connected to all other variables (degree 3 = n−1 in a 4-variable problem). Yes — B and C are each connected to every other variable.

```
    A
   / \
  B - C
   \ /
    D
```

---

### (c) Backtracking Trace

**Initial:** A={1,2,3}, B={1,2,3}, C={1,2,3}, D={1,2,3}

**Step 1 — MRV:** All have domain size 3. Alphabetical tiebreak → **A**.
**LCV for A:** Each value (1, 2, or 3) eliminates exactly 1 value from B and 1 from C = 2 total eliminations. All tied → assign **A = 1** (smallest).
**FC after A=1:** B ≠ A → remove 1 from B: B={2,3}. C ≠ A → remove 1 from C: C={2,3}. D unaffected: D={1,2,3}.

| After Step 1 | A={1} | B={2,3} | C={2,3} | D={1,2,3} |

**Step 2 — MRV:** B and C have 2 values; D has 3. Tie on B, C → alphabetical → **B**.
**LCV for B (from {2,3}):**
- B=2: FC removes 2 from C → C={3} (1 elimination); removes 2 from D → D={1,3} (1 elimination). Total: 2.
- B=3: FC removes 3 from C → C={2} (1 elimination); removes 3 from D → D={1,2} (1 elimination). Total: 2.
Tied → assign **B = 2** (smallest).
**FC after B=2:** C ≠ B → C={3}. D ≠ B → D={1,3}.

| After Step 2 | A={1} | B={2} | C={3} | D={1,3} |

**Step 3 — MRV:** C has 1 value (most constrained) → **C**.
C = **3** (forced — only value).
**FC after C=3:** A ≠ C: 3 ∉ {1}, no change. B ≠ C: 3 ∉ {2}, no change. D ≠ C: remove 3 from D → D={1}.

| After Step 3 | A={1} | B={2} | C={3} | D={1} |

**Step 4 — MRV:** D has 1 value → **D**.
D = **1** (forced).
**FC after D=1:** B ≠ D: 1 ∉ {2}, no change. C ≠ D: 1 ∉ {3}, no change.

**Final assignment: A=1, B=2, C=3, D=1**

Verification: A≠B(1≠2)✓, A≠C(1≠3)✓, B≠C(2≠3)✓, B≠D(2≠1)✓, C≠D(3≠1)✓

**No backtracking occurred.** MRV+FC+LCV navigated directly to a solution.

---

### (d) REVISE(D, C)

After A=1 (FC: B loses 1, C loses 1): C={2,3}, D={1,2,3}.
After B=2 (FC: C loses 2, D loses 2): C={3}, D={1,3}.

Current domains: C = {3}, D = {1, 3}.

**REVISE(D, C):** Constraint D ≠ C. For each d ∈ D, check if ∃ c ∈ C s.t. d ≠ c:

| d | c values in C = {3} | d ≠ c? | Supported? |
|---|----------------------|---------|------------|
| 1 | 3 | 1 ≠ 3 ✓ | **YES** — keep |
| 3 | 3 | 3 ≠ 3 ✗ | **NO** — remove |

**D's domain after REVISE(D, C): {1}**
**Domain changed: YES** (3 was removed). REVISE returns TRUE.

*Note:* This is consistent with what FC would have done in Step 3 after assigning C=3 — both methods eliminate d=3 from D.

---

### (e) Problem Structure

**(i)** **Not a tree.** The graph contains cycles. One cycle: **A – B – C – A** (triangle). Another: **B – C – D – B** (triangle). Both share the B–C edge.

**(ii)** A minimum cutset of size **c = 1**. Removing either **B** or **C** breaks both triangles:
- Remove B: remaining edges are A–C and C–D → path A–C–D (tree ✓)
- Remove C: remaining edges are A–B and B–D → path A–B–D (tree ✓)

**Minimum cutset: {B} (or {C}), size c = 1**

Time complexity with cutset conditioning:
O(d^c × (n − c) × d²) = O(3¹ × 3 × 3²) = **O(3 × 3 × 9) = O(81)**, or equivalently **O(d · nd²) = O(nd³)**.

Formally written: **O(dᶜ · (n−c) · d²)** with c=1, n=4, d=3.

---

## Section 3 — Adversarial Search

### Part A — Minimax Values

#### (a.i) Node Values

| Node | Children | Value |
|------|----------|-------|
| A (MIN) | 3, 12 | **3** |
| B (MIN) | 8, 2 | **2** |
| C (MIN) | 14, 5 | **5** |
| D (MIN) | 2, 4 | **2** |
| E (MIN) | 5, 10 | **5** |
| F (MIN) | 7, 11 | **7** |
| G (MIN) | 9, 3 | **3** |
| H (MIN) | 15, 6 | **6** |
| LL (MAX) | A=3, B=2 | **3** |
| LR (MAX) | C=5, D=2 | **5** |
| RL (MAX) | E=5, F=7 | **7** |
| RR (MAX) | G=3, H=6 | **6** |
| L (MIN) | LL=3, LR=5 | **3** |
| R (MIN) | RL=7, RR=6 | **6** |
| ROOT (MAX) | L=3, R=6 | **6** |

**Optimal action at root: Go R (Right)** — value 6 > 3.

---

#### (a.ii) Alpha-Beta Pruning Trace

| Node | Type | α entered | β entered | Value returned | Pruning? |
|------|------|-----------|-----------|----------------|----------|
| ROOT | MAX | −∞ | +∞ | **6** | No |
| L | MIN | −∞ | +∞ | **3** | No |
| LL | MAX | −∞ | +∞ | **3** | No |
| A | MIN | −∞ | +∞ | **3** | No |
| B | MIN | 3 | +∞ | **2** | α-cut triggers after leaf 2 (2 ≤ α=3), but B has no more children — no actual savings |
| LR | MAX | −∞ | **3** | **5** | No (itself not pruned, but triggers β-cut) |
| C | MIN | −∞ | 3 | **5** | No |
| **D** | MIN | −∞ | 3 | — | **PRUNED** — see below |
| R | MIN | **3** | +∞ | **6** | No |
| RL | MAX | 3 | +∞ | **7** | No |
| E | MIN | 3 | +∞ | **5** | No |
| F | MIN | **5** | +∞ | **7** | No |
| RR | MAX | 3 | **7** | **6** | No |
| G | MIN | 3 | 7 | **3** | α-cut triggers after leaf 3 (3 ≤ α=3), but G has no more children |
| H | MIN | 3 | 7 | **6** | No |

**Detailed explanation of D's pruning:**

After LL returns 3: L (MIN) updates β ← min(+∞, 3) = 3. Now β = 3 at L.

L then explores LR (MAX) with inherited α = −∞, **β = 3**.

Inside LR: after C (MIN) returns 5, LR's value v = max(−∞, 5) = 5. Check: v = 5 ≥ β = 3? **YES → β-cutoff at LR!** LR returns 5 immediately.

**Subtree D (and its two leaves: 2 and 4) is NEVER EVALUATED.**

**Pruned:** Node D and its leaves **{2, 4}** — two leaf nodes never evaluated.

**Cutoff type:** β-cutoff (at MAX node LR), because LR's value ≥ the inherited β from its MIN ancestor L.

*Intuition:* MIN player (L) has already secured a value of 3 from the LL branch. MAX player (LR) has found a value of 5 — but MIN would never choose LR (5 > 3, worse for MIN). So LR's remaining children are irrelevant.

---

#### (a.iii) Depth-Limited Minimax

**(i) Plain Minimax depth:**
Nodes per depth d = 35^d. Solve 35^d = 5×10⁷:
d = log₃₅(5×10⁷) = ln(5×10⁷)/ln(35) = 17.73/3.56 ≈ **4.98 → depth 4**.

**(ii) Alpha-Beta with perfect ordering:**
Best-case: O(b^(d/2)) = 35^(d/2). Solve 35^(d/2) = 5×10⁷:
d/2 ≈ 4.98 → **d ≈ 9–10 (roughly double plain Minimax).**

Alpha-Beta with perfect ordering effectively **doubles the searchable depth** for the same computation budget — a massive improvement (chess at depth 4 is weak; depth 10 is strong).

**(iii) Good ordering matters** because Alpha-Beta prunes more when the best moves are explored first. At MAX nodes, exploring the highest-value child first makes β-cutoffs more likely; at MIN nodes, the lowest-value child first triggers α-cutoffs.

**Heuristic for chess:** Order moves by *most valuable victim / least valuable attacker* (MVV-LVA): examine captures of high-value pieces first, since they tend to produce high values early and maximize pruning.

---

### Part B — Expectimax

| Node | Type | Computation | Value |
|------|------|-------------|-------|
| Left's MAX child 1 | MAX | max(10, 6) | **10** |
| Left's MAX child 2 | MAX | max(2, 8) | **8** |
| Left | CHANCE | 1/2 × 10 + 1/4 × 8 + 1/4 × 0 = 5 + 2 + 0 | **7** |
| Right's MAX child | MAX | max(4, 12) | **12** |
| Right | CHANCE | 2/3 × 12 + 1/3 × 3 = 8 + 1 | **9** |
| ROOT | MAX | max(7, 9) | **9** |

**Optimal strategy: Choose Right** (expected value 9 > 7).

---

## Section 4 — Analysis

### (a) Utility Scales

**(i) Minimax — squaring does NOT change the action.**

Original children values: Left = 4, Right = 7. MAX chooses Right.

After squaring all terminal utilities, the min/max propagation still preserves order since squaring is a monotone increasing function on non-negative values. Max node: max(a², b²) = (max(a, b))² when a, b ≥ 0. The relative ordering at every node is preserved. **Action unchanged: still Right.**

*Minimax only requires the ordering of values to be preserved. Any monotone increasing transformation (not just linear) preserves minimax decisions — as long as all values are in a domain where the transformation is monotone.*

**(ii) Expectimax — squaring DOES change the action.**

Before squaring:
- E[Left] = 1/2 × 2 + 1/2 × 6 = **4**
- E[Right] = 1/2 × 1 + 1/2 × 9 = **5**
Optimal: **Right** (5 > 4).

After squaring all leaves (2→4, 6→36, 1→1, 9→81):
- E[Left²] = 1/2 × 4 + 1/2 × 36 = **20**
- E[Right²] = 1/2 × 1 + 1/2 × 81 = **41**
Optimal: **Right** (41 > 20) — same action here, but the magnitude ratio changed drastically.

*Different counterexample showing action change:* Left = {0, 10}, Right = {4, 6} (all prob 1/2). E[Left]=5, E[Right]=5 (tied). After squaring: E[Left²]=(0+100)/2=50, E[Right²]=(16+36)/2=26. Now Left wins. **Tie broken by squaring** → action changed.

**Why:** Expected value is a linear operator. Squaring violates linearity (E[X²] ≠ (E[X])²). The non-linear transformation changes expected values non-uniformly, potentially reversing preferences.

---

### (b) Ghost Modeling

**(i)** Use **Expectimax**. Minimax assumes the opponent plays *optimally against you* (worst case). This ghost moves *randomly* 80% of the time — that is not adversarial behavior. Expectimax models the opponent as a probabilistic agent: the chance node computes a weighted average over the ghost's possible moves. This better reflects the actual distribution of ghost behavior and allows Pac-Man to take calculated risks.

**(ii)** Using Minimax against a predominantly random ghost commits **Dangerous Pessimism**: Minimax assumes the worst-case adversarial behavior even when the ghost is likely to move randomly. This causes Pac-Man to be overly conservative — it avoids moves that would be profitable on average against a random ghost, because Minimax plans for the ghost to always choose the move that hurts Pac-Man most. Result: Pac-Man scores lower than it could.

*(Reference: Pac-Man experiment from notes — Minimax Pac-Man vs. random ghosts: won 5/5 but scored 493; Expectimax Pac-Man vs. random ghosts: won 5/5 and scored 503.)*

**(iii)** Use **Expectiminimax** (or a probabilistic Expectimax) that models the ghost as a chance node with probability 0.8 of choosing a random move and 0.2 of choosing the optimal adversarial move, capturing the mixed nature of the ghost's behavior.

---

## Summary Tables

### CSP Techniques

| Technique | Strength | Complexity | Best for |
|-----------|----------|------------|----------|
| Backtracking (naive) | Baseline | O(dⁿ) worst case | Small problems |
| + MRV | Better variable ordering | — | Fail-first benefit |
| + LCV | Better value ordering | — | Succeed-first benefit |
| + FC | Prunes direct neighbors | O(nd) per assignment | Most practical |
| + AC-3 | Prunes entire graph | O(n²d³) | Tighter propagation |
| Tree CSP | Polynomial exact | O(nd²) | Acyclic graphs |
| Cutset conditioning | Hybrid | O(dᶜ · nd²) | Small cutsets |

### Game Algorithms

| Scenario | Algorithm | Root optimality |
|----------|-----------|-----------------|
| Rational adversary | Minimax | Yes vs. perfect player |
| Random environment | Expectimax | Yes (in expectation) |
| Mixed | Expectiminimax | Yes with correct model |
| Resource-limited | Depth-limited + Eval | Approximate |

### Alpha-Beta Complexity

| Move ordering | Time complexity | Equivalent Minimax depth |
|---------------|----------------|--------------------------|
| Random | O(b^(3d/4)) | ~1.33× |
| Good | O(b^(d/2)) | **2×** (doubles depth) |

---

*Tutorial #2 — Covers Lectures 05–08*
*Next: Tutorial #3 will cover L09–L12 (Linear Programming, Integer Programming, Optimization, Convex Optimization)*
