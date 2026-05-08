# Lecture 05 - Constraint Satisfaction Problems (CSP)

**Course**: CS5491: Artificial Intelligence
**Reading**: RN Chapter 6

---

## 1. Search vs. CSP: Two Modes of Thinking

| Mode | Focus | Path Matters? |
|------|-------|--------------|
| **Planning** (search) | Sequence of actions to reach a goal | **Yes** — path has cost/depth |
| **Identification** (CSP) | Assignment to variables that satisfies all constraints | **No** — only the final assignment matters |

> Assumption: single agent, deterministic actions, fully observed, discrete state space.

---

## 2. What Are CSPs?

### Standard Search Problems
- State = "black box" (arbitrary data structure)
- Goal test = any function
- Successor = any function

### Constraint Satisfaction Problems (CSPs)
A special class of search where:
- **Variables**: `X₁, X₂, ..., Xₙ`
- **Domains**: each variable `Xᵢ` takes values from domain `Dᵢ`
- **Constraints**: specify allowable combinations of values for subsets of variables
- **Goal**: find a **complete assignment** that satisfies **all constraints**

> CSPs allow powerful general-purpose algorithms that exploit structure.

---

## 3. CSP Formulation

| Component | Description |
|-----------|-------------|
| **States** | Partial assignments of values to variables |
| **Initial State** | Empty assignment `{}` |
| **Successor Function** | Assign a value to an unassigned variable |
| **Goal Test** | Assignment is complete AND satisfies all constraints |

---

## 4. Classic Example: Map Coloring (Australia)

| Component | Value |
|-----------|-------|
| **Variables** | WA, NT, Q, NSW, V, SA, T |
| **Domains** | `{red, green, blue}` |
| **Constraints** | Adjacent regions must have different colors |

**Constraint forms**:
- **Implicit**: `WA ≠ NT`
- **Explicit**: `(WA, NT) ∈ {(red,green), (red,blue), (green,red), ...}`

**Example solution**: `{WA=red, NT=green, Q=red, NSW=green, V=red, SA=blue, T=green}`

---

## 5. Constraint Graphs

- **Binary CSP**: each constraint relates exactly **two** variables
- **Constraint Graph**: nodes = variables, arcs = constraints

> Graph structure reveals **independent subproblems** (e.g., Tasmania is disconnected from the mainland).

---

## 6. Example: N-Queens Problem

### Formulation 1 (Grid-based)
- Variables: `Xᵢⱼ` ∈ `{0, 1}` (queen present or not)
- Constraints: no two queens in same row, column, or diagonal; exactly N queens total

### Formulation 2 (Compact)
- Variables: `Qₖ` = column position of queen in row k
- Domain: `{1, 2, ..., N}`
- Constraints: `∀(i,j)` queens are non-threatening

---

## 7. Varieties of CSPs

### Variable Types

| Type | Example | Notes |
|------|---------|-------|
| **Finite discrete** | Map coloring, Boolean SAT | `O(dⁿ)` assignments; SAT is NP-complete |
| **Infinite discrete** | Job scheduling (integers) | Linear: solvable; Nonlinear: undecidable |
| **Continuous** | Telescope scheduling | Linear: solvable in poly time (LP) |

### Constraint Types

| Type | Description | Example |
|------|-------------|---------|
| **Unary** | Restricts single variable | `SA = green` |
| **Binary** | Restricts pair of variables | `SA ≠ WA` |
| **Higher-order** | Restricts 3+ variables | Cryptarithmetic |
| **Soft (preferences)** | Preferred values with costs | `red` better than `green` → constrained optimization |

---

## 8. Real-World CSP Applications

- Scheduling (meeting times, class timetabling)
- Assignment (who teaches what)
- Hardware configuration
- Transportation scheduling
- Factory scheduling
- Circuit layout
- Fault diagnosis

---

## 9. Solving CSPs with Standard Search

A naive approach:
- **BFS**: explores many equivalent orderings → inefficient
- **DFS**: similar issue

**Problem**: Both are too slow due to redundant exploration of the same assignment in different orders.

---

## 10. Looking Ahead

The next lecture (06) introduces **Backtracking Search** and improvements:
- Filtering (Forward Checking, Arc Consistency)
- Ordering (MRV, LCV)
- Problem Structure exploitation
