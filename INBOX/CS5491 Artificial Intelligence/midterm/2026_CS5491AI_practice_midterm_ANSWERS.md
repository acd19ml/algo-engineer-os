# CityU CS5491 AI — Practice Midterm: Complete Answers

**(Spring 2026)**

> All answers cite the course notes. References are written as `[Lecture XX, §Y]`.

---

## 1 — Multiple Choice Questions

---

### (a) Identity

*(Fill in name and student ID on the cover page.)*

---

### (b) Types of Agents — Crossword Puzzle Environment

> **Background**: The environment's nature dictates which AI technique to use.
> *"The characteristics of Percepts, Environment, and Action space dictate which AI technique to use."*
> — [Lecture 01, §5.2]


| #   | Choice                                        | Answer               | Reasoning                                                                                                         |
| --- | --------------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------- |
| i   | fully observable **vs.** partially observable | **Fully observable** | The entire puzzle grid is visible at all times; the agent can see every filled and empty cell. No hidden state.   |
| ii  | single agent **vs.** multi-agent              | **Single agent**     | Only one agent fills in words. There is no opponent or competing agent modifying the board.                       |
| iii | stochastic **vs.** deterministic              | **Deterministic**    | Placing a word in a slot always produces exactly that result with certainty—no randomness involved.               |
| iv  | discrete **vs.** continuous                   | **Discrete**         | States (partially completed grids) and actions (placing a specific word in a specific slot) are countable/finite. |


*Source: Environment classification framework — [Lecture 01, §5.2]*

---

### (c) True or False

#### i) A search with a heuristic that is not completely admissible may still find the shortest path.

**Answer: TRUE**

Admissibility is a *sufficient* condition for optimality in A, not a *necessary* one. An inadmissible heuristic breaks the optimality *guarantee*, but in specific problem instances the algorithm can still happen to return the optimal path.

> *"Inadmissible heuristics can also be useful in practice (sacrifice optimality for speed)."*
> — [Lecture 04, §8]

Optimality proof for A requires `h(n) ≤ h*(n)` everywhere; violating this *can* cause suboptimal results but does not *always* do so.

---

#### ii) Doubling computer speed allows you to double the depth of tree search.

**Answer: FALSE**

Tree search is **exponential** in depth: the number of nodes at depth `m` is `O(b^m)`. Doubling speed doubles the node count explored, but depth gain is only `log_b(2)`, which is tiny for realistic branching factors.

Example: with `b = 35` (chess), doubling speed adds only `log₃₅(2) ≈ 0.18` more depth — far from doubling.

> *"Total nodes in tree = 1 + b + b² + ... + b^m = O(b^m)"*
> — [Lecture 03, §4]

> *"Chess: b ≈ 35, m ≈ 100 → exact solution completely infeasible!"*
> — [Lecture 07, §6.4]

---

#### iii) Backtracking search on CSPs still requires exponential time in the worst case.

**Answer: TRUE**

Backtracking is DFS with constraint checking. Without structure exploitation, the naive worst case is `O(d^n)`.

> *"Naive backtracking: O(d^n) — No improvements"*
> — [Lecture 06, §7]

Even with MRV + LCV + Forward Checking, the worst case remains exponential; improvements only help average-case performance.

---

#### iv) A Minimax agent may achieve a better score against a suboptimal adversary than against an optimal one.

**Answer: TRUE**

Minimax is designed for worst-case play (optimal adversary). Against a suboptimal adversary who makes mistakes, the Minimax agent will gain at least as much as it would against a perfect player—often more.

> *"Minimax: Optimal, Yes, against a perfect adversary."*
> — [Lecture 07, §6.4]
>
> *"Pac-Man experiment: Random ghosts vs. Adversarial ghosts — Minimax Pacman wins 5/5 in both cases but scores higher against random opponents."*
> — [Lecture 08, §6]

The minimax value is a **lower bound** on what the agent can achieve; suboptimal opponents let the agent exceed this bound.

---

#### v) For an IP problem, it is sufficient to consider integer points around the LP solution.

**Answer: FALSE**

Rounding the LP solution to nearby integers is **not** guaranteed to yield the optimal—or even a feasible—integer solution. The optimal integer point can be far from the LP vertex.

> *"Why Not Just Round the LP Solution? Answer: **No!** The optimal integer solution can be far from the rounded LP solution."*
> — [Lecture 10, §4]

This is why Branch and Bound must be used instead of simple rounding.

---

## 2 — Informed Search

**Graph summary** (reconstructed):


| Edge | Cost | Heuristic h(n) |
| ---- | ---- | -------------- |
| S→A  | 1    | h(S)=9, h(A)=8 |
| A→B  | 1    | h(B)=9         |
| A→D  | 3    | h(D)=5         |
| A→E  | 8    | h(E)=4         |
| B→C  | 1    | h(C)=10        |
| D→E  | 1    |                |
| D→F  | 3    | h(F)=3         |
| E→H  | 2    | h(H)=2         |
| H→F  | 1    |                |
| F→G  | 3    | h(G)=0         |


> All three algorithms use a **priority queue** (fringe). Goal check is performed **on expansion** (dequeue), not on generation.
> — [Lecture 03, §3] and [Lecture 04, §4.2]

---

### (a) Uniform Cost Search (UCS)

> **Strategy**: Expand the node with the lowest cumulative cost `g(n)`.
> — [Lecture 03, §10]


| Step | Action                                    | g(n) | Fringe after expansion                     |
| ---- | ----------------------------------------- | ---- | ------------------------------------------ |
| 1    | **Visit S**                               | 0    | {A(1)}                                     |
| 2    | **Visit A**                               | 1    | {B(2), D(4), E(9)}                         |
| 3    | **Visit B**                               | 2    | {C(3), D(4), E(9)}                         |
| 4    | **Visit C**                               | 3    | {D(4), E(9)} — C is dead end               |
| 5    | **Visit D**                               | 4    | {E(5), F(7)} — E updated from 9 to 5 via D |
| 6    | **Visit E**                               | 5    | {F(7), H(7)}                               |
| 7    | **Visit F** *(F before H alphabetically)* | 7    | {H(7), G(10)}                              |
| 8    | **Visit H**                               | 7    | {G(10)} — F already visited                |
| 9    | **Visit G**                               | 10   | GOAL                                       |


**Visited order:** S, A, B, C, D, E, F, H, G

**Path:** S → A → D → F → G

**Path length (cost):** 1 + 3 + 3 + 3 = **10**

---

### (b) Greedy Search

> **Strategy**: Expand the node with the lowest heuristic `h(n)` (estimated forward cost). Ignores `g(n)`.
> — [Lecture 04, §3]


| Step | Action      | h(n) | Fringe after expansion |
| ---- | ----------- | ---- | ---------------------- |
| 1    | **Visit S** | 9    | {A(8)}                 |
| 2    | **Visit A** | 8    | {E(4), D(5), B(9)}     |
| 3    | **Visit E** | 4    | {H(2), D(5), B(9)}     |
| 4    | **Visit H** | 2    | {F(3), D(5), B(9)}     |
| 5    | **Visit F** | 3    | {G(0), D(5), B(9)}     |
| 6    | **Visit G** | 0    | GOAL                   |


**Visited order:** S, A, E, H, F, G

**Path:** S → A → E → H → F → G

**Path length (cost):** 1 + 8 + 2 + 1 + 3 = **15**

> Note: Greedy found a valid path but not the optimal one (15 > 10). This illustrates that Greedy is **not optimal** because it ignores the cost already incurred.
> — [Lecture 04, §3]

---

### (c) A Search (`f(n) = g(n) + h(n)`)

> **Strategy**: Combine UCS (backward cost `g`) and Greedy (forward cost `h`).
> A is **complete and optimal** when `h` is admissible (`h(n) ≤ h*(n)`).
> — [Lecture 04, §4, §5–§6]


| Step | Action                                                | f=g+h   | Fringe after expansion                                            |
| ---- | ----------------------------------------------------- | ------- | ----------------------------------------------------------------- |
| 1    | **Visit S**                                           | 0+9=9   | {A(1+8=9)}                                                        |
| 2    | **Visit A**                                           | 1+8=9   | {D(4+5=9), B(2+9=11), E(9+4=13)}                                  |
| 3    | **Visit D** *(tie at f=9, D before E alphabetically)* | 4+5=9   | {E(5+4=9), F(7+3=10), B(11)} — E updated from 13 to 9             |
| 4    | **Visit E**                                           | 5+4=9   | {H(7+2=9), F(10), B(11)}                                          |
| 5    | **Visit H**                                           | 7+2=9   | {F(7+3=10), B(11)} — F via H would be g=8, f=11 > 10; not updated |
| 6    | **Visit F**                                           | 7+3=10  | {G(10+0=10), B(11)}                                               |
| 7    | **Visit G**                                           | 10+0=10 | GOAL                                                              |


**Visited order:** S, A, D, E, H, F, G

**Path:** S → A → D → F → G

**Path length (cost):** 1 + 3 + 3 + 3 = **10** ✓ (optimal)

> A found the optimal path (cost 10) while visiting fewer nodes than UCS (7 vs. 9).
> This efficiency comes from the heuristic guiding search toward the goal.
> — [Lecture 04, §7]

---

## 3 — Course Scheduling (CSP)

> **CSP formulation**: Variables + Domains + Constraints.
> *"A CSP specifies: Variables X₁,...,Xₙ; Domains D₁,...,Dₙ; Constraints on allowable combinations."*
> — [Lecture 05, §2]

### (a) CSP Formulation

**Variables:** One per class (which professor teaches it):

`C₁, C₂, C₃, C₄, C₅`

**Domains** (professors qualified for each class):


| Variable                  | Domain |
| ------------------------- | ------ |
| C₁ (Intro to Programming) | {A, C} |
| C₂ (Intro to AI)          | {A}    |
| C₃ (NLP)                  | {B, C} |
| C₄ (Computer Vision)      | {B, C} |
| C₅ (Machine Learning)     | {A, B} |


**Constraints** (a professor can only teach one class at a time — no simultaneous scheduling conflicts):

Overlapping class times:

- Class 1 (8:00–9:00) overlaps Class 2 (8:30–9:30) → **C₁ ≠ C₂**
- Class 2 (8:30–9:30) overlaps Class 3 (9:00–9:30) → **C₂ ≠ C₃**
- Class 2 (8:30–9:30) overlaps Class 4 (9:00–9:30) → **C₂ ≠ C₄**
- Class 3 (9:00–10:00) and Class 4 (9:00–10:00) are simultaneous → **C₃ ≠ C₄**

Class 5 (10:30–11:30) does not overlap any other class, so **C₅ is unconstrained** by timing.

> These are **binary constraints** (each relates exactly two variables), as defined in [Lecture 05, §7].
> Note: C₁ ≠ C₂ is valid *only when* the professors' domains intersect — since D(C₁) ∩ D(C₂) = {A}, this is the critical constraint to check.

---

### (b) Constraint Graph

> *"Binary CSP: each constraint relates exactly two variables. Constraint Graph: nodes = variables, arcs = constraints."*  
> — [Lecture 05, §5]

Nodes: C₁, C₂, C₃, C₄, C₅

Edges (constraints):

- C₁ — C₂  (overlap: 8:00–9:00 and 8:30–9:30)
- C₂ — C₃  (overlap: 8:30–9:30 and 9:00–10:00)
- C₂ — C₄  (overlap: 8:30–9:30 and 9:00–10:00)
- C₃ — C₄  (simultaneous: both 9:00–10:00)

C₅ is an isolated node (no time overlap with others).

> **Valid solution** (verify by inspection):
>
> - C₁ = C (Prof C teaches Class 1)
> - C₂ = A (only Prof A qualifies)
> - C₃ = B (Prof B teaches NLP; C₂=A≠B ✓)
> - C₄ = C (Prof C teaches CV; C₂=A≠C ✓, C₃=B≠C ✓)
> - C₅ = B or A (no conflict; e.g., C₅ = B)

---

## 4 — Adversarial Search (Minimax + Alpha-Beta)

> **Minimax rule**: MAX nodes take the maximum of children's values; MIN nodes take the minimum.
> — [Lecture 07, §6.1]

### (a) Fill in Minimax Values

**Bottom-up computation** (level 3 → level 2 → level 1 → root):

**Level 3 (MIN nodes):**


| Node | Children (leaves) | Value = min |
| ---- | ----------------- | ----------- |
| L3_1 | 20, 11            | **11**      |
| L3_2 | 5, 13             | **5**       |
| L3_3 | 12, 15            | **12**      |
| L3_4 | 9, 34             | **9**       |
| L3_5 | 10, 6             | **6**       |
| L3_6 | 20, 2             | **2**       |
| L3_7 | 5, 9              | **5**       |
| L3_8 | 23, 13            | **13**      |


**Level 2 (MAX nodes):**


| Node | Children (L3 values) | Value = max |
| ---- | -------------------- | ----------- |
| L2_1 | 11, 5                | **11**      |
| L2_2 | 12, 9                | **12**      |
| L2_3 | 6, 2                 | **6**       |
| L2_4 | 5, 13                | **13**      |


**Level 1 (MIN nodes):**


| Node | Children (L2 values) | Value = min |
| ---- | -------------------- | ----------- |
| L1_1 | 11, 12               | **11**      |
| L1_2 | 6, 13                | **6**       |


**Root (MAX):**


| Node | Children (L1 values) | Value = max |
| ---- | -------------------- | ----------- |
| Root | 11, 6                | **11**      |


---

### (b) Alpha-Beta Pruning

> **α** = best value MAX can guarantee so far; **β** = best value MIN can guarantee so far.
> Pruning rules: at MIN node prune if `v ≤ α`; at MAX node prune if `v ≥ β`.
> — [Lecture 07, §7]

**Trace (left to right, α=-∞, β=+∞ at root):**

```
ROOT (MAX): α=-∞, β=+∞
│
├── L1_1 (MIN): α=-∞, β=+∞
│   ├── L2_1 (MAX): α=-∞, β=+∞
│   │   ├── L3_1 (MIN): → sees 20 then 11 → returns 11
│   │   │   α updated to 11 at L2_1
│   │   └── L3_2 (MIN): α=11, β=+∞
│   │       ├── leaf 5: v=5 ≤ α=11 → ✂ PRUNE leaf 13
│   │       └── returns ≤5 (< 11, won't improve L2_1)
│   │   L2_1 = 11; β updated to 11 at L1_1
│   │
│   └── L2_2 (MAX): α=-∞, β=11
│       ├── L3_3 (MIN): α=-∞, β=11 → sees 12, 15 → returns 12
│       │   L2_2 current = 12 ≥ β=11 → ✂ PRUNE L3_4 (both leaves 9, 34)
│       └── L2_2 returns ≥12 (won't help L1_1)
│   L1_1 = min(11, ≥12) = 11
│   α updated to 11 at ROOT
│
└── L1_2 (MIN): α=11, β=+∞
    ├── L2_3 (MAX): α=11, β=+∞
    │   ├── L3_5 (MIN): α=11, β=+∞
    │   │   ├── leaf 10: v=10 ≤ α=11 → ✂ PRUNE leaf 6
    │   │   └── returns ≤10
    │   └── L3_6 (MIN): α=11, β=+∞ → sees 20, 2 → returns 2
    │   L2_3 = max(≤10, 2) ≤ 10
    │   L1_2 current = ≤10 ≤ α=11 → ✂ PRUNE entire L2_4
    └── L1_2 returns ≤10

ROOT = max(11, ≤10) = 11 ✓
```

**Summary of pruned branches:**


| Cut # | Location | Pruned                                                    | Reason                                          |
| ----- | -------- | --------------------------------------------------------- | ----------------------------------------------- |
| ✂ 1   | L3_2     | Leaf **13**                                               | After seeing leaf 5 (v=5 ≤ α=11 at parent L2_1) |
| ✂ 2   | L2_2     | Entire **L3_4** (leaves 9, 34)                            | L2_2 got ≥12 ≥ β=11 at parent L1_1              |
| ✂ 3   | L3_5     | Leaf **6**                                                | After seeing leaf 10 (v=10 ≤ α=11 at L2_3)      |
| ✂ 4   | L1_2     | Entire **L2_4** subtree (L3_7, L3_8, leaves 5, 9, 23, 13) | L1_2 got ≤10 ≤ α=11 at ROOT                     |


> With perfect ordering, Alpha-Beta reduces time from `O(b^m)` to `O(b^(m/2))`, effectively **doubling the searchable depth**.
> — [Lecture 07, §7.3]

---

## 5 — Expectimax (Tic Tac Toe)

> **Expectimax**: Replace MIN nodes with **Chance nodes** when the opponent is random.
> `V(chance node) = Σ P(outcome) · V(outcome)`
> — [Lecture 08, §3]

**Current board** (X to move):

```
_ | O | X
O | X | _
O | X | _
```

Empty squares: **(0,0)** [top-left, row 1], **(1,2)** [middle-right, row 2], **(2,2)** [bottom-right, row 3]

**Olivia's probability model**: Let P(top square) = t. Then P(middle square) = 3t, P(bottom square) = 9t.

> Key threat: O already occupies column 0 at rows 1 and 2 — if O plays (0,0), **O wins** by completing column 0.

---

### Move X1: X plays middle-right (1,2)

Board becomes:

```
_ | O | X
O | X | X
O | X | _
```

Remaining empty: **(0,0)** (top, weight t) and **(2,2)** (bottom, weight 9t)

$$P(O \to (0,0)) = \frac{t}{t+9t} = \frac{1}{10}, \quad P(O \to (2,2)) = \frac{9}{10}$$


| O's move | Result                            | Score |
| -------- | --------------------------------- | ----- |
| O→(0,0)  | O completes column 0 → **O wins** | −1    |
| O→(2,2)  | X must play (0,0) → **Draw**      | 0     |


$$E(\text{X1}) = \frac{1}{10}(-1) + \frac{9}{10}(0) = -\frac{1}{10}$$

---

### Move X2: X plays bottom-right (2,2)

Board becomes:

```
_ | O | X
O | X | _
O | X | X
```

Remaining empty: **(0,0)** (top, weight t) and **(1,2)** (middle, weight 3t)

$$P(O \to (0,0)) = \frac{t}{t+3t} = \frac{1}{4}, \quad P(O \to (1,2)) = \frac{3}{4}$$


| O's move | Result                                                         | Score |
| -------- | -------------------------------------------------------------- | ----- |
| O→(0,0)  | O completes column 0 → **O wins**                              | −1    |
| O→(1,2)  | X plays (0,0) → X wins diagonal (0,0)-(1,1)-(2,2) → **X wins** | +1    |


$$E(\text{X2}) = \frac{1}{4}(-1) + \frac{3}{4}(+1) = -\frac{1}{4} + \frac{3}{4} = \boxed{\frac{1}{2}}$$

---

### Move X3: X plays top-left (0,0)

Board becomes:

```
X | O | X
O | X | _
O | X | _
```

X now **blocks** O's column-0 threat!

Remaining empty: **(1,2)** (middle, weight 3t) and **(2,2)** (bottom, weight 9t)

$$P(O \to (1,2)) = \frac{3t}{3t+9t} = \frac{1}{4}, \quad P(O \to (2,2)) = \frac{3}{4}$$


| O's move | Result                                                         | Score |
| -------- | -------------------------------------------------------------- | ----- |
| O→(1,2)  | X plays (2,2) → X wins diagonal (0,0)-(1,1)-(2,2) → **X wins** | +1    |
| O→(2,2)  | X plays (1,2) → **Draw**                                       | 0     |


$$E(\text{X3}) = \frac{1}{4}(+1) + \frac{3}{4}(0) = \frac{1}{4}$$

---

### Comparison and Answer


| Move | Description            | Expected Score     |
| ---- | ---------------------- | ------------------ |
| X1   | Middle-right (1,2)     | −1/10 = −0.10      |
| X2   | **Bottom-right (2,2)** | **+1/2 = +0.50** ✓ |
| X3   | Top-left (0,0)         | +1/4 = +0.25       |


**Answer: Circle position (2,2) — bottom-right.**

**Justification:**

- Move X2 yields the highest expected score (+0.5) by exploiting Olivia's strong preference for the bottom row.
- After X2, Olivia is 3× more likely to play the middle-right square than the top-left. Playing middle-right lets X complete the main diagonal (0,0)-(1,1)-(2,2) for a win (+1).
- Move X3 blocks O's column threat but scores lower (0.25) because Olivia strongly prefers the bottom row, which after X3 leads to a draw rather than a win.
- Move X1 is worst (−0.1) because Olivia heavily favors the bottom row, leaving the lethal top-left square to O with high probability.

> *"A rational agent should choose the action that maximizes its expected utility, given its knowledge."* (Principle of Maximum Expected Utility)
> — [Lecture 08, §8.4]

---

## 6 — Linear Programming

> **LP formulation**: linear objective function + linear constraints.
> — [Lecture 09, §4]

### (a) Linear Programming Formulation

**Decision variables:**

- `x` = number of blouses produced per day
- `y` = number of skirts produced per day

**Objective function** (maximize profit):

$$\text{Maximize} \quad P = 8x + 6y$$

**Subject to:**


| Constraint      | Expression                | Reason                                                |
| --------------- | ------------------------- | ----------------------------------------------------- |
| Ann's time      | $x + y \leq 7$            | Each blouse uses 1h of Ann; each skirt uses 1h of Ann |
| Margaret's time | $x + \frac{1}{2}y \leq 5$ | Each blouse uses 1h of Margaret; each skirt uses 0.5h |
| Non-negativity  | $x \geq 0, y \geq 0$      | Cannot make negative items                            |
| Integrality     | $x, y \in \mathbb{Z}$     | Partial blouse/skirt not allowed                      |


> The integrality constraint makes this an **Integer Programming** problem; we first solve the LP relaxation.
> — [Lecture 10, §3]

---

### (b) Draw Constraints and Identify Feasible Region

> *"The optimal LP solution is always at a feasible vertex (intersection of constraint boundaries)."*
> — [Lecture 09, §5]

**Step 1 — Define the two constraint lines:**

**Line 1** (Ann's constraint): `x + y = 7`

- When x=0: y=7 → point **A = (0, 7)**
- When y=0: x=7 → point **B = (7, 0)**
- Draw a solid line from (0,7) to (7,0)
- Feasible side: below-left (shaded region where x+y ≤ 7)

**Line 2** (Margaret's constraint): `x + 0.5y = 5`  (equivalently: `2x + y = 10`)

- When x=0: y=10 → point **C = (0, 10)**
- When y=0: x=5 → point **D = (5, 0)**
- Draw a solid line from (0,10) to (5,0)
- Feasible side: below-left (shaded region where x + 0.5y ≤ 5)

**Step 2 — Find intersection of the two constraint lines:**

Solve simultaneously:

```
x + y   = 7     ... (1)
x + 0.5y = 5    ... (2)
```

Subtract (2) from (1): `0.5y = 2` → `y = 4`, then `x = 3`

→ Intersection point **E = (3, 4)**

**Step 3 — Mark feasible region and corner points:**

The feasible region is the polygon bounded by:

- x-axis (y=0): from origin to (5,0)
- y-axis (x=0): from origin to (0,7)
- Line 1 (Ann): from (0,7) to E=(3,4)
- Line 2 (Margaret): from E=(3,4) to (5,0)

**Corner points of the feasible region:**


| Corner Point | Constraints satisfied                       |
| ------------ | ------------------------------------------- |
| O = (0, 0)   | Both slack                                  |
| A' = (0, 7)  | Ann binding, Margaret slack (0+3.5=3.5≤5 ✓) |
| E = (3, 4)   | Both binding                                |
| D = (5, 0)   | Margaret binding, Ann slack (5+0=5≤7 ✓)     |


> Draw the shaded feasible region as the quadrilateral O → A' → E → D → O (first quadrant).

---

### (c) Solve the Linear Programming Problem

> **Procedure**: Evaluate the objective at each feasible vertex; the maximum is optimal.
> — [Lecture 09, §7]


| Corner Point   | P = 8x + 6y                               |
| -------------- | ----------------------------------------- |
| O = (0, 0)     | 8(0) + 6(0) = **$0**                      |
| A' = (0, 7)    | 8(0) + 6(7) = **$42**                     |
| **E = (3, 4)** | 8(3) + 6(4) = 24 + 24 = **$48** ← maximum |
| D = (5, 0)     | 8(5) + 6(0) = **$40**                     |


**Solution:**


|                           | Value   |
| ------------------------- | ------- |
| Number of **blouses** (x) | **3**   |
| Number of **skirts** (y)  | **4**   |
| Maximum daily **profit**  | **$48** |


**Verification:**

- Ann's time: 3 + 4 = **7 hours** ≤ 7 ✓ (exactly saturated)
- Margaret's time: 3 + 0.5(4) = 3 + 2 = **5 hours** ≤ 5 ✓ (exactly saturated)
- x=3, y=4 are both integers → no rounding needed; the LP optimum is also the IP optimum.

> **Working (cost-contour intuition):** The objective `8x + 6y = k` defines parallel lines with slope −4/3. Sweeping these lines upward-right through the feasible region, the last feasible vertex touched is E=(3,4), giving maximum profit $48. — [Lecture 09, §6]

---

## Reference Index


| Topic                     | Source Note                                       |
| ------------------------- | ------------------------------------------------- |
| Agent & environment types | [Lecture 01 — Introduction, §5]                   |
| Search tree complexity    | [Lecture 03 — Uninformed Search, §4–§10]          |
| UCS algorithm             | [Lecture 03 — Uninformed Search, §10]             |
| A and admissibility       | [Lecture 04 — Informed Search, §4–§6]             |
| Greedy search             | [Lecture 04 — Informed Search, §3]                |
| CSP formulation           | [Lecture 05 — Constraint Satisfaction, §2–§5]     |
| Backtracking search       | [Lecture 06 — Constraint Satisfaction II, §1, §7] |
| Minimax & alpha-beta      | [Lecture 07 — Adversarial Search, §6–§7]          |
| Expectimax & utilities    | [Lecture 08 — Adversarial Search II, §3, §8]      |
| Linear programming        | [Lecture 09 — Linear Programming, §4–§7]          |
| Integer programming       | [Lecture 10 — Integer Programming, §3–§4]         |


