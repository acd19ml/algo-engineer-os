# CS5491 AI — Tutorial Exam #1（L01–L04）

**Spring 2026 | Total: 45 pts | Recommended Time: ~2 hours**

**Name:** __________________ **Student ID:** __________________

---

> **Instructions:** This exam is open-book (physical notes only). Point deductions apply for wrong answers in Section 1 (T/F). Show all working. If a question is ambiguous, state your assumptions explicitly — you will be graded on the assumption *and* your reasoning.

---

## Section 1 — True / False with Justification *(10 pts)*

> **Grading:** 2 pts per question: 1 pt for the correct T/F answer, 1 pt for a correct and complete justification. A correct answer with *no or incorrect* justification earns 0.5 pts max. An incorrect answer earns 0 pts regardless of justification.

---

**(a)** (2 pts) **T / F** — The state space graph of any search problem always contains *strictly fewer* nodes than the corresponding search tree.

*Justification:*

 

 

---

**(b)** (2 pts) **T / F** — Breadth-First Search (BFS) is guaranteed to find an optimal (minimum-cost) solution whenever all edge costs are non-negative.

*Justification:* 

---

**(c)** (2 pts) **T / F** — If we set h(n) = 0 for every node n, then A Search is equivalent to Uniform Cost Search (UCS).

*Justification:*

 


| 算法      | 优先级（谁小谁先出队） |
| ------- | ----------- |
| **UCS** | g(n)        |
| **A**   | g(n) + h(n) |


f(n) = g(n) + h(n) = g(n) + 0 = g(n) 

---

**(d)** (2 pts) **T / F** — Iterative Deepening Search (IDS) is strictly worse than BFS in time complexity because IDS re-expands nodes from shallower depths multiple times.

*Justification:*

 

 

---

**(e)** (2 pts) **T / F** — If an admissible heuristic h₁ *dominates* an admissible heuristic h₂ (i.e., h₁(n) ≥ h₂(n) for all n), then A Search with h₁ will always expand a *subset* of the nodes that A with h₂ would expand.

*Justification:*

 

 

---

## Section 2 — Agent Design & Problem Formulation *(12 pts)*

---

### Part A — Environment Classification (6 pts)

You are designing an AI agent for a **Mars rover** that must autonomously collect rock samples from 5 designated sites and return to its base station. Relevant details:

- The rover uses cameras and LiDAR to sense terrain, but cannot see beyond hills or behind obstacles.
- Communication delay with Earth is 15 minutes (so the rover must act independently).
- Dust storms occur randomly and can reshape terrain or bury markers while the rover is deliberating.
- Exact rock sample locations must be found by on-site scanning (not known in advance).
- The rover shares the Mars surface with two other research rovers from other agencies.
- Sample collection order affects which sites remain accessible (driving over certain terrain degrades it).

For **each** of the six dimensions below, circle the correct term and write **one sentence** justifying your choice based on the scenario above.


| #   | Dimension                                     | Your Choice | Justification |
| --- | --------------------------------------------- | ----------- | ------------- |
| i   | Fully Observable **vs.** Partially Observable |             |               |
| ii  | Deterministic **vs.** Stochastic              |             |               |
| iii | Static **vs.** Dynamic                        |             |               |
| iv  | Discrete **vs.** Continuous                   |             |               |
| v   | Single-agent **vs.** Multi-agent              |             |               |
| vi  | Episodic **vs.** Sequential                   |             |               |


*(6 classifications × 1 pt = 6 pts; correct term without justification = 0.5 pt)*

---

### Part B — State Space Formulation (6 pts)

Consider a simpler robot problem: a **cleaning robot** operates in a **2×2 grid** (cells labeled A, B, C, D as shown below). Each cell may be *Dirty* or *Clean*. The robot starts at cell **A**. Available actions: move **Right**, **Down**, **Left**, **Up** (only valid if within the grid), and **Suck** (cleans the current cell, no effect if already clean). All actions cost 1. Goal: all cells are Clean.

```
┌───┬───┐
│ A │ B │
├───┼───┤
│ C │ D │
└───┴───┘
```

**(i) [2 pts]** Define a **minimal** state representation sufficient for planning. State all variables and their domains. How many total distinct states exist?

*State variables and domains:*

 

 

*Total distinct states:*

 

---

**(ii) [2 pts]** Write the **successor function** formally. Describe what state results from each action applied to a general state (robot at position p, dirt configuration d).

 

 

 

---

**(iii) [2 pts]** A classmate proposes representing state as just `(robot_position, dirty_cell_count)` — e.g., `(A, 3)` means "robot at A, 3 cells still dirty". Is this sufficient for planning? If not, give a **concrete example** of two world configurations that this representation cannot distinguish, but which require different actions.

 

 

 

---

## Section 3 — Search Algorithm Traces *(18 pts)*

Consider the following directed graph. You want to find a path from **S** (start) to **G** (goal).

```
         1           1
    S ──────→ A ──────→ C
    │                   │
  2 │                   │ 99
    │         5         │
    └──────→ B ──────→ G
```

**Edge costs and heuristic values:**


| Node | h(n) | Edges out | Cost |
| ---- | ---- | --------- | ---- |
| S    | 7    | S→A       | 1    |
| A    | 1    | S→B       | 2    |
| B    | 5    | A→C       | 1    |
| C    | 1    | B→G       | 5    |
| G    | 0    | C→G       | 99   |


> **Rules for all algorithms:** Use **graph search** (never re-expand a visited node). Break ties **alphabetically** (prefer A before B, B before C, etc.). The goal check is performed when a node is **dequeued/expanded** (not when it is added to the fringe).

---

### (a) Depth-First Search (3 pts)

Show the order in which nodes are **expanded** (visited), and state the **path** and **cost** found.


| Step | Node Expanded | Fringe (after expansion) | Visited Set |
| ---- | ------------- | ------------------------ | ----------- |
| 0    | —             | {S}                      | {}          |
| 1    |               |                          |             |
| 2    |               |                          |             |
| 3    |               |                          |             |
| 4    |               |                          |             |


**Expansion order:** S, _______________

**Path found:** _______________  **Path cost:** _______________

---

### (b) Uniform Cost Search (4 pts)

Show the fringe (as a priority queue sorted by g(n)) and the visited set at each step.


| Step | Node Expanded | g(n) | Fringe after expansion (node: g) | Visited |
| ---- | ------------- | ---- | -------------------------------- | ------- |
| 0    | —             | —    | {S:0}                            | {}      |
| 1    |               |      |                                  |         |
| 2    |               |      |                                  |         |
| 3    |               |      |                                  |         |
| 4    |               |      |                                  |         |
| 5    |               |      |                                  |         |


**Expansion order:** S, _______________

**Path found:** _______________  **Path cost:** _______________

---

### (c) Greedy Best-First Search (3 pts)

Show the fringe sorted by h(n).


| Step | Node Expanded | h(n) | Fringe after expansion (node: h) | Visited |
| ---- | ------------- | ---- | -------------------------------- | ------- |
| 0    | —             | —    | {S:7}                            | {}      |
| 1    |               |      |                                  |         |
| 2    |               |      |                                  |         |
| 3    |               |      |                                  |         |


**Expansion order:** S, _______________

**Path found:** _______________  **Path cost:** _______________

---

### (d) A Search (4 pts)

Show the fringe sorted by f(n) = g(n) + h(n). Include g, h, and f values for each new node.


| Step | Node Expanded | g   | h   | f   | Fringe after expansion (node: f) | Visited |
| ---- | ------------- | --- | --- | --- | -------------------------------- | ------- |
| 0    | —             | —   | —   | —   | {S:7}                            | {}      |
| 1    |               |     |     |     |                                  |         |
| 2    |               |     |     |     |                                  |         |
| 3    |               |     |     |     |                                  |         |
| 4    |               |     |     |     |                                  |         |
| 5    |               |     |     |     |                                  |         |


**Expansion order:** S, _______________

**Path found:** _______________  **Path cost:** _______________

---

### (e) Analysis (4 pts — 2 pts each)

**(i)** Verify whether the heuristic h is **admissible**. You must check every non-goal node. Show your work.


| Node | h(n) | h(n) (true cost to G) | h(n) ≤ h(n)? |
| ---- | ---- | --------------------- | ------------ |
| S    | 7    |                       |              |
| A    | 1    |                       |              |
| B    | 5    |                       |              |
| C    | 1    |                       |              |


Is h admissible? _____ Why is this important for A?

 

 

---

**(ii)** Greedy Search found the path S→A→C→G (cost 101), while A found S→B→G (cost 7). Both used the same admissible heuristic. Explain precisely **why Greedy failed** while **A succeeded**. Your answer must reference the priority functions of both algorithms.

 

 

 

---

## Section 4 — Heuristic Design & Analysis *(5 pts)*

The **8-puzzle** is a 3×3 sliding tile puzzle with tiles 1–8 and one blank. A move slides any tile adjacent to the blank into the blank's position. The goal is to reach a specific target configuration. Consider this specific state N and goal configuration:

```
State N:          Goal:
┌───┬───┬───┐   ┌───┬───┬───┐
│ 1 │ 2 │ 3 │   │ 1 │ 2 │ 3 │
├───┼───┼───┤   ├───┼───┼───┤
│ 4 │ 5 │   │   │ 4 │   │ 5 │
├───┼───┼───┤   ├───┼───┼───┤
│ 7 │ 8 │ 6 │   │ 7 │ 8 │ 6 │
└───┴───┴───┘   └───┴───┴───┘
```

Three heuristics are proposed:

- **h₁(n)** = number of misplaced tiles (not counting the blank)
- **h₂(n)** = sum of Manhattan distances of each tile from its goal position (not counting blank)
- **h₃(n)** = h₁(n) + h₂(n)

---

**(a) [1 pt]** Compute h₁(N), h₂(N), and h₃(N) for State N above.


| Heuristic | Value for State N | Working |
| --------- | ----------------- | ------- |
| h₁(N)     |                   |         |
| h₂(N)     |                   |         |
| h₃(N)     |                   |         |


---

**(b) [1 pt]** Is **h₁** admissible? Justify with a brief argument (not just "yes/no").

 

 

---

**(c) [1 pt]** Is **h₂** admissible? Justify with a brief argument.

 

 

---

**(d) [2 pts]** Is **h₃** admissible? Give a **concrete counterexample** using State N above (or construct another simple state) to prove your answer. Compute h₃ and h for that state.

 

 

 

---

## Section 5 — Conceptual Reasoning *(Bonus — 5 pts)*

> *This section tests deeper understanding. Partial credit is given for correct reasoning even if conclusions are wrong.*

---

**(a) [2 pts]** A Search with an admissible heuristic h is run on a graph and finds path P with cost C. Now suppose we run A again with a **new heuristic h'** where h'(n) = h(n) + 100 for all non-goal nodes, and h'(G) = 0.

Is h' admissible? Does A with h' still find the optimal path? Explain.

 

 

 

---

**(b) [3 pts]** You are given a search problem where the state space is a **tree** (no cycles). Compare DFS, BFS, and UCS in terms of **completeness** and **optimality** for this tree. Do any of the standard guarantees change compared to a general graph?

*(Hint: think carefully about what causes DFS to be incomplete in the general case.)*

 

 

 

---

*End of Exam — Good Luck!*

---

---

# Answer Key

> ⚠️ Attempt the exam above independently before reading this section.

---

## Section 1 — True/False

### (a) FALSE

The search tree can have the *same state appear multiple times* (once per distinct path that leads to it), making the tree potentially infinite for graphs with cycles. The state space graph contains each state exactly once — so the graph is ≤ the tree in node count. However, "**strictly** fewer" fails for acyclic graphs where each state is reachable via exactly one path (graph = tree). The statement is too strong.

### (b) FALSE

BFS finds the path with the **fewest edges** (minimum depth), not minimum total cost. With varying edge costs, a 1-hop path of cost 100 is returned over a 2-hop path of total cost 2. BFS is optimal *only when all edge costs are equal (uniform = 1)*.

### (c) TRUE

With h(n) = 0 for all n: f(n) = g(n) + h(n) = g(n) + 0 = g(n). A's priority function becomes identical to UCS's priority (cumulative path cost g(n)). Both algorithms expand nodes in identical order.

### (d) FALSE

IDS does re-expand nodes, but this is not a net loss asymptotically. The last (deepest) iteration generates O(b^s) nodes. The total across all prior iterations adds only a constant factor b/(b−1). Asymptotic time complexity remains **O(b^s)** — identical to BFS. IDS actually *beats* BFS on **space**: O(bs) vs. O(b^s).

### (e) FALSE

The precise theorem is: every node expanded by A with h₁ is *also* expanded by A with h₂ — making h₁'s expanded set a **subset-or-equal** (⊆) of h₂'s. The "always strictly fewer" claim fails when the two heuristics produce identical results on some problem instances (ties). The correct statement uses ⊆, not ⊊.

---

## Section 2A — Environment Classification


| #   | Answer                   | Key Reasoning                                                                                            |
| --- | ------------------------ | -------------------------------------------------------------------------------------------------------- |
| i   | **Partially Observable** | Cameras cannot see beyond hills; sample locations unknown until on-site scan                             |
| ii  | **Stochastic**           | Dust storms occur with random probability; terrain changes are unpredictable                             |
| iii | **Dynamic**              | Dust storms reshape terrain *while the rover deliberates* (15-min comm delay = extended deliberation)    |
| iv  | **Continuous**           | Terrain elevation, rover position (x,y,z), speed, arm angles — all real-valued                           |
| v   | **Multi-agent**          | Two other rovers share the surface; their movements can affect terrain and site accessibility            |
| vi  | **Sequential**           | Driving over terrain degrades it — each action affects which future actions are available; order matters |


---

## Section 2B — State Space Formulation

### (i) Minimal state representation

State variables:

- **Robot position**: ∈ {A, B, C, D} → 4 values
- **Dirt status of each cell**: ∈ {Dirty, Clean} for each of A, B, C, D → 2⁴ = 16 combinations

**Total distinct states: 4 × 16 = 64**

Note: Facing direction is unnecessary — movement cost is uniform and direction has no effect on future options in this formulation.

### (ii) Successor function

For state s = (pos, dA, dB, dC, dD):


| Action     | Valid when   | New state                                      |
| ---------- | ------------ | ---------------------------------------------- |
| Move Right | pos ∈ {A, C} | pos → B (from A) or D (from C); dirt unchanged |
| Move Down  | pos ∈ {A, B} | pos → C (from A) or D (from B); dirt unchanged |
| Move Left  | pos ∈ {B, D} | pos → A (from B) or C (from D); dirt unchanged |
| Move Up    | pos ∈ {C, D} | pos → A (from C) or B (from D); dirt unchanged |
| Suck       | always       | pos unchanged; d_{pos} → Clean                 |


All valid actions cost 1. Invalid moves (e.g., Move Left from A) produce no successors.

### (iii) Classmate's representation is INSUFFICIENT

The representation `(robot_position, dirty_cell_count)` loses *which specific cells* are dirty.

**Concrete counterexample:**

- **World X**: Robot at A, cells {B, C, D} are dirty → `(A, 3)`
- **World Y**: Robot at A, cells {A, B, C} are dirty → `(A, 3)`

In **World X**: A is already clean; the optimal first action is to move toward a dirty cell (e.g., Right toward B).
In **World Y**: A is dirty and the robot is already there; the optimal first action is **Suck** to immediately clean A.

Same compressed state, different optimal actions — the representation breaks planning.

---

## Section 3 — Search Algorithm Traces

**Graph:** S→A(1), S→B(2), A→C(1), C→G(99), B→G(5)
**Heuristics:** h(S)=7, h(A)=1, h(B)=5, h(C)=1, h(G)=0

---

### (a) DFS

*Push in reverse-alphabetical order so A pops before B; mark visited on expansion.*


| Step | Expanded | Fringe | Visited      |
| ---- | -------- | ------ | ------------ |
| 1    | S        | [B, A] | {S}          |
| 2    | A        | [B, C] | {S, A}       |
| 3    | C        | [B, G] | {S, A, C}    |
| 4    | **G** ✓  | —      | {S, A, C, G} |


**Expansion order:** S, A, C, G
**Path:** S → A → C → G  **Cost: 101** ✗ *(suboptimal)*

---

### (b) UCS

*Priority = g(n); alphabetical tiebreak.*


| Step | Expanded | g   | Fringe (node:g) | Visited         |
| ---- | -------- | --- | --------------- | --------------- |
| 1    | S        | 0   | {A:1, B:2}      | {S}             |
| 2    | A        | 1   | {B:2, C:2}      | {S, A}          |
| 3    | B        | 2   | {C:2, G:7}      | {S, A, B}       |
| 4    | C        | 2   | {G:7}*          | {S, A, B, C}    |
| 5    | **G** ✓  | 7   | —               | {S, A, B, C, G} |


 C→G would put G at cost 2+99=101, but G is already in fringe with g=7 (cheaper) → no update.

> **Tiebreak at Step 3:** B and C both have g=2; B expands first (alphabetical).

**Expansion order:** S, A, B, C, G
**Path:** S → B → G  **Cost: 7** ✓ *(optimal)*

---

### (c) Greedy Best-First Search

*Priority = h(n); alphabetical tiebreak.*


| Step | Expanded | h   | Fringe (node:h) | Visited      |
| ---- | -------- | --- | --------------- | ------------ |
| 1    | S        | 7   | {A:1, B:5}      | {S}          |
| 2    | A        | 1   | {C:1, B:5}      | {S, A}       |
| 3    | C        | 1   | {G:0, B:5}      | {S, A, C}    |
| 4    | **G** ✓  | 0   | —               | {S, A, C, G} |


**Expansion order:** S, A, C, G
**Path:** S → A → C → G  **Cost: 101** ✗ *(suboptimal!)*

---

### (d) A Search

*Priority = f(n) = g(n) + h(n).*


| Step | Expanded | g   | h   | f   | Fringe (node:f) | Visited         |
| ---- | -------- | --- | --- | --- | --------------- | --------------- |
| 1    | S        | 0   | 7   | 7   | {A:2, B:7}      | {S}             |
| 2    | A        | 1   | 1   | 2   | {C:3, B:7}      | {S, A}          |
| 3    | C        | 2   | 1   | 3   | {B:7, G:101}    | {S, A, C}       |
| 4    | B        | 2   | 5   | 7   | {G:7}**         | {S, A, B, C}    |
| 5    | **G** ✓  | 7   | 0   | 7   | —               | {S, A, B, C, G} |


 When B is expanded: G enters with g=2+5=7, f=7. G is already in fringe with f=101. Since 7 < 101, **update G's entry to g=7, parent=B, f=7**.

**Expansion order:** S, A, C, B, G
**Path:** S → B → G  **Cost: 7** ✓ *(optimal)*

---

### (e.i) Admissibility Check

True shortest paths to G: via B costs 2+5=7; via C costs 1+99=100 (from A) or ≥101 (from S). Therefore:


| Node | h(n) | h(n) | h(n) ≤ h(n)?   |
| ---- | ---- | ---- | -------------- |
| S    | 7    | 7    | ✓ (tight)      |
| A    | 1    | 100  | ✓ (very loose) |
| B    | 5    | 5    | ✓ (tight)      |
| C    | 1    | 99   | ✓ (very loose) |


**h is admissible.** Admissibility guarantees A's optimality: the proof shows that any ancestor n of the optimal goal A satisfies f(n) ≤ g(A) ≤ g(B) = f(B) for any suboptimal goal B. So A will always expand an ancestor of the optimal goal before any suboptimal goal.

---

### (e.ii) Why Greedy Failed / A Succeeded

**Greedy** uses priority = h(n) only. It selected A (h=1) over B (h=5) at S because A *looks* closer to the goal by h. It then selected C (h=1) over B (h=5) again. Greedy has **no memory of cost already incurred** — it cannot detect that the h(A)=1 estimate is wildly optimistic (true remaining cost is 100). It blindly follows the locally cheapest h value at each step.

**A** uses priority = f(n) = g(n) + h(n). After expanding C (f=3), it adds G to the fringe with f=2+99+0=101. A then expands B (f=7) and discovers G via B→G at total cost 7. Since 7 < 101, it **updates G's entry** and correctly identifies the optimal path. A succeeds because g(n) penalizes the expensive detour through A→C even when h makes it look attractive.

**Summary:** Greedy is myopic (h only). A is globally aware (g accounts for past cost, h estimates future). Admissibility of h is necessary but not sufficient to make Greedy optimal — it only guarantees A is optimal.

---

## Section 4 — Heuristic Analysis

### (a) Values for State N

Only tile **5** is misplaced: it is at position (row=1, col=2); its goal is (row=1, col=1). Manhattan distance = |1−1| + |2−1| = 1. All other tiles are at their goal positions.


| Heuristic | Value | Working                                                 |
| --------- | ----- | ------------------------------------------------------- |
| h₁(N)     | **1** | Only tile 5 is out of place                             |
| h₂(N)     | **1** | Tile 5: Manhattan distance = 1; all others contribute 0 |
| h₃(N)     | **2** | 1 + 1 = 2                                               |


### (b) h₁ — ADMISSIBLE

Each misplaced tile requires **at least 1 move** to reach its goal position, since each move repositions exactly one tile by one step. Therefore the number of misplaced tiles is a lower bound on the number of moves required: h₁(n) ≤ h(n) for all n.

### (c) h₂ — ADMISSIBLE

Each tile must travel at least its Manhattan distance to reach its goal, since each move shifts exactly one tile by exactly one step. No single move can reduce any tile's Manhattan distance by more than 1. Therefore the sum of Manhattan distances is a lower bound on total moves: h₂(n) ≤ h(n) for all n.

### (d) h₃ — NOT ADMISSIBLE

**Counterexample using State N:**

- h₃(N) = **2**
- h(N) = **1** (one move: slide tile 5 right into the blank at (1,2))

Since h₃(N) = 2 > h(N) = 1, **h₃ overestimates** the true cost at State N. h₃ is **not admissible**.

**Why h₃ fails:** h₃ = h₁ + h₂ double-counts each misplaced tile — once for being out of place and once for its distance. These are not independent lower bounds on *separate* moves; they both measure the same moves. Their sum can exceed h.

---

## Section 5 — Bonus

### (a) h'(n) = h(n) + 100

**Is h' admissible?** No, in general. For any node n where h(n) < 100, we have h'(n) = h(n) + 100 ≥ 100 > h(n). For example, a node 1 step from the goal has h(n) = 1 but h'(n) ≥ 100. h' wildly overestimates for nodes close to the goal.

**Does A with h' find the optimal path?** Not guaranteed. Since h' is inadmissible, the optimality guarantee breaks down. A may assign a very high f-value to nodes near the optimal goal and expand a suboptimal goal node first.

### (b) DFS, BFS, UCS on a Tree (no cycles)


| Algorithm | Completeness (tree)       | Optimality (tree)    | Change vs. graph?             |
| --------- | ------------------------- | -------------------- | ----------------------------- |
| **DFS**   | **Yes** (if finite depth) | No                   | **YES — DFS is now complete** |
| **BFS**   | Yes                       | Only if uniform cost | No change                     |
| **UCS**   | Yes                       | Yes                  | No change                     |


**Key change:** DFS is normally incomplete on general graphs because it can loop forever in cycles. In a **tree**, cycles are impossible by definition — DFS will always terminate and find a solution if one exists at finite depth. Optimality properties are unchanged: DFS still finds the leftmost (not cheapest) solution, so it remains non-optimal with varying costs.

---

## Algorithm Comparison Summary


| Algorithm | Expansion Order | Path    | Cost | Optimal? |
| --------- | --------------- | ------- | ---- | -------- |
| DFS       | S, A, C, G      | S→A→C→G | 101  | ✗        |
| UCS       | S, A, B, C, G   | S→B→G   | 7    | ✓        |
| Greedy    | S, A, C, G      | S→A→C→G | 101  | ✗        |
| A         | S, A, C, B, G   | S→B→G   | 7    | ✓        |


> **Key insight from this graph:** DFS and Greedy both fail because they commit early to the A→C branch (DFS by depth, Greedy by h=1). UCS and A both succeed by accounting for actual path costs. A additionally uses h to expand in a smarter order than UCS, though both find the same optimal path here.

---

*Tutorial #1 — Covers Lectures 01–04*
*Next: Tutorial #2 will cover L05–L08 (CSP, Constraint Propagation, Adversarial Search, Alpha-Beta Pruning)*