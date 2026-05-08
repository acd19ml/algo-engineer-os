# Lecture 04 - Informed Search

**Course**: CS5491: Artificial Intelligence
**Reading**: RN Chapter 3.5–3.6, 4.1–4.2

---

## 1. Uninformed vs. Informed Search

| Type | Methods | Analogy |
|------|---------|---------|
| **Uninformed** | DFS, BFS, UCS | Searching with **eyes closed** |
| **Informed** | Greedy, A* | Searching with **eyes open** |

Informed search uses **problem-specific knowledge** (heuristics) to guide search toward the goal more efficiently.

---

## 2. Heuristics

A **heuristic** `h(n)` is:
- A function that **estimates how close** a state is to a goal
- Designed for a **specific** search problem
- Examples:
  - **Manhattan distance**: `|Δx| + |Δy|` (for grid problems)
  - **Euclidean distance**: `sqrt(Δx² + Δy²)` (straight-line distance)
  - **Pancake problem**: index of the largest pancake still out of place

> Heuristics are problem-specific — there is no universal heuristic.

---

## 3. Greedy Search

**Strategy**: Expand the node that appears **closest to the goal**

**Priority**: `h(n)` — estimated forward cost to goal

### Greedy Search Issues

- **Best case**: Goes straight to the goal (very fast)
- **Worst case**: Like a badly-guided DFS — can get stuck or find suboptimal paths
- **Not optimal**: Greedy ignores the cost already incurred (`g(n)`)
- **Not complete**: Can go down infinite paths

> Example: In Romania routing, greedy may take a longer route because a closer intermediate city *looks* nearer to Bucharest.

---

## 4. A* Search

### 4.1 Key Idea: Combine UCS and Greedy

| Algorithm | Priority | Focus |
|-----------|----------|-------|
| **UCS** | `g(n)` | Backward cost (cost so far) |
| **Greedy** | `h(n)` | Forward cost (estimated remaining) |
| **A*** | `f(n) = g(n) + h(n)` | **Total estimated cost** |

- `g(n)` = actual cost from start to node `n`
- `h(n)` = estimated cost from `n` to goal
- `f(n)` = estimated total cost of the path through `n`

### 4.2 Termination Condition

> **Stop when a goal node is DEQUEUED** — NOT when it is enqueued.

This is critical for optimality: a goal in the fringe might not have the cheapest path yet.

---

## 5. Admissibility

### 5.1 Definition

A heuristic `h` is **admissible** (optimistic) if:

```
0 ≤ h(n) ≤ h*(n)
```

Where `h*(n)` is the **true cost** to the nearest goal.

> An admissible heuristic **never overestimates** the cost to reach the goal.

### 5.2 Intuition

| Heuristic Type | Behavior |
|----------------|---------|
| **Admissible** (optimistic) | Slows down bad plans but never outweighs true costs → preserves optimality |
| **Inadmissible** (pessimistic) | Traps good plans on the fringe → breaks optimality |

---

## 6. Optimality Proof for A* (Tree Search)

**Setup**:
- `A` = optimal goal node (lowest true cost)
- `B` = suboptimal goal node (`g(B) > g(A)`)
- `h` is admissible

**Claim**: A will exit the fringe (be expanded) before B.

**Proof**:

1. Suppose B is on the fringe. Some ancestor `n` of A is also on the fringe.
2. By **admissibility**: `f(n) = g(n) + h(n) ≤ g(A)` (since `h(n) ≤ h*(n)`)
3. At goal nodes, `h = 0`, so `f(A) = g(A)`
4. Since B is suboptimal: `g(A) ≤ g(B)`, thus `f(A) ≤ f(B)`
5. Combining: `f(n) ≤ f(A) < f(B)`
6. Therefore `n` is expanded before B → all ancestors of A expand before B → **A expands before B**

**Conclusion**: A* with admissible heuristics is **optimal**.

---

## 7. UCS vs. A* — Contour Comparison

| Algorithm | Exploration Pattern |
|-----------|---------------------|
| **UCS** | Expands equally in **all directions** (circular contours) |
| **A*** | Expands mainly **toward the goal** (elliptical contours pointed at goal) |

> A* is much more efficient than UCS when a good heuristic is available.

---

## 8. Creating Admissible Heuristics

> **Most of the work in A* is designing a good admissible heuristic.**

### Key Technique: Relaxed Problems
- A **relaxed problem** removes constraints from the original problem
- The optimal solution cost of a relaxed problem is an admissible heuristic for the original

**Example — 8-puzzle**:
| Heuristic | Relaxation |
|-----------|-----------|
| Number of misplaced tiles | Tiles can move anywhere (ignore blocking) |
| Manhattan distance | Tiles can move through other tiles |

> More powerful heuristics = fewer nodes expanded = faster search
> Inadmissible heuristics can also be useful in practice (sacrifice optimality for speed)

---

## 9. A* Applications

- Video games (path planning for NPCs)
- Navigation / routing (Google Maps)
- Robot motion planning
- Resource planning
- Language analysis, machine translation
- Speech recognition

---

## 10. A* Summary

| Property | A* |
|----------|-----|
| **Complete** | Yes (with admissible h) |
| **Optimal** | Yes (with admissible h) |
| **Time** | Depends on heuristic quality |
| **Space** | Exponential (stores all fringe nodes) |

**Key facts**:
- Uses both **backward costs** `g(n)` and **estimated forward costs** `h(n)`
- Optimal with **admissible** heuristics
- Heuristic design (via relaxed problems) is the key engineering challenge

---

## 11. Heuristic Design as a Search Problem

Advanced technique: use machine learning / automated search to design heuristics for hard problems (e.g., online bin packing).

---

## 12. Summary

| Algorithm | f(n) | Complete | Optimal | Notes |
|-----------|------|----------|---------|-------|
| **Greedy** | `h(n)` | No | No | Fast but can fail |
| **A*** | `g(n) + h(n)` | Yes | Yes (admissible h) | Best of both worlds |
| **UCS** | `g(n)` | Yes | Yes | Blind to goal direction |

> **Core insight**: A* is optimal and efficient when `h(n)` is admissible. The closer `h(n)` is to the true cost `h*(n)` without exceeding it, the better A* performs.
