# Lecture 06 - Constraint Satisfaction II: Backtracking & Improvements

**Course**: CS5491: Artificial Intelligence
**Reading**: RN Chapter 6

---

## 1. Backtracking Search

### Core Idea

Basic DFS for CSPs with two key improvements:

| Idea | Description |
|------|-------------|
| **One variable at a time** | Fix an ordering; assignments are **commutative** — `[WA=red, NT=green]` same as `[NT=green, WA=red]` |
| **Check constraints as you go** | Only consider values that don't conflict with previous assignments (incremental goal test) |

> **Backtracking = DFS + variable-ordering + fail-on-violation**
> Can solve N-queens for n ≈ 25.

### Algorithm
```
function BACKTRACKING-SEARCH(csp):
    return BACKTRACK({}, csp)

function BACKTRACK(assignment, csp):
    if assignment is complete: return assignment
    var = SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    for value in ORDER-DOMAIN-VALUES(var, assignment, csp):
        if value is consistent with assignment:
            add {var = value} to assignment
            result = BACKTRACK(assignment, csp)
            if result ≠ failure: return result
            remove {var = value} from assignment
    return failure
```

---

## 2. Improving Backtracking: Three Strategies

| Strategy | Question |
|----------|----------|
| **Ordering** | Which variable/value to try next? |
| **Filtering** | Can we detect failure early? |
| **Structure** | Can we exploit the graph structure? |

---

## 3. Ordering

### 3.1 Variable Ordering: Minimum Remaining Values (MRV)

- **Choose the variable with the fewest legal values** remaining in its domain
- Also called: **"most constrained variable"** or **"fail-first"** heuristic
- **Why minimum?** Variables with fewer options are most likely to cause failure — better to discover failure early

### 3.2 Value Ordering: Least Constraining Value (LCV)

- **Choose the value that rules out the fewest options** for remaining variables
- **Why least?** We want to keep maximum flexibility for future assignments

> **Combining MRV + LCV makes 1000-queens feasible!**

| Ordering | Heuristic | Goal |
|----------|-----------|------|
| Variable | MRV (fewest remaining values) | Fail fast — detect dead ends early |
| Value | LCV (least constraining) | Succeed first — preserve flexibility |

---

## 4. Filtering

### 4.1 Forward Checking

- After assigning a variable, **cross off values in neighbors' domains** that would violate constraints
- Detects immediate failures

**Example** (Map Coloring):
- Assign `WA = red` → remove `red` from NT and SA domains
- Assign `Q = green` → remove `green` from NT, NSW, SA domains
- Detect: if any domain becomes empty → backtrack immediately

**Limitation**: Only looks one step ahead — doesn't catch all failures.

### 4.2 Constraint Propagation (Arc Consistency)

**Arc Consistency**: Arc `X → Y` is consistent iff for every value `x` in `X`'s domain, there exists some value `y` in `Y`'s domain that satisfies the constraint.

- **Key rule**: If `X` loses a value, all neighbors of `X` must be rechecked
- Propagates failure information through the constraint graph

**AC-3 Algorithm**:
```
function AC-3(csp):
    queue = all arcs in csp
    while queue not empty:
        (Xi, Xj) = DEQUEUE(queue)
        if REVISE(csp, Xi, Xj):
            if |domain(Xi)| == 0: return false  # failure
            for each Xk in neighbors(Xi) - {Xj}:
                ENQUEUE(queue, (Xk, Xi))
    return true
```

**Runtime**: `O(n²d³)`, reducible to `O(n²d²)`

| Method | Detection Range | Notes |
|--------|----------------|-------|
| Forward Checking | Direct neighbors | Fast, shallow |
| Arc Consistency | All arcs in graph | Deeper propagation, slower |

### 4.3 Limitations of Arc Consistency

After enforcing arc consistency, the CSP may have:
- Exactly **one solution** left
- **Multiple solutions** left (need more search)
- **No solutions** (but we may not know it yet — only detects local inconsistencies)

> Arc consistency still runs **inside** backtracking search as a filter.

---

## 5. Problem Structure

### 5.1 Independent Subproblems

Real-world CSPs often decompose into **independent subproblems** (connected components of the constraint graph).

**Example**: Tasmania is disconnected from mainland Australia → solve separately.

**Efficiency gain**:
- Without decomposition: `O(dⁿ)`
- With decomposition into subproblems of size `c`: `O((n/c) · dᶜ)` — **linear in n**

| Setup | Cost |
|-------|------|
| n=80, d=2, no decomposition | ~4 billion years |
| n=80, d=2, c=20 | ~0.4 seconds |

### 5.2 Tree-Structured CSPs

> **Theorem**: If the constraint graph has **no loops** (is a tree), the CSP can be solved in `O(nd²)` time.

Compare:
- General CSP: `O(dⁿ)` (exponential)
- Tree-structured CSP: `O(nd²)` (polynomial)

**Algorithm for Tree-Structured CSPs**:
1. **Order**: Choose root, arrange variables so parents precede children
2. **Remove backward**: For `i = n to 2`, apply `RemoveInconsistent(Parent(Xᵢ), Xᵢ)`
3. **Assign forward**: For `i = 1 to n`, assign `Xᵢ` consistently with `Parent(Xᵢ)`

**Runtime**: `O(nd²)`

### 5.3 Cutset Conditioning

For graphs with loops:
1. Find a **cutset** — a small set of variables whose removal makes the graph a tree
2. Try all assignments to cutset variables
3. Solve the resulting tree CSP for each

**Runtime**: `O(dᶜ · (n-c) · d²)` where `c` = cutset size

> Very fast when cutset size `c` is small!

---

## 6. Summary: CSP Improvements

| Technique | Type | Key Idea |
|-----------|------|----------|
| Backtracking | Algorithm | DFS + commutativity + constraint check |
| MRV | Ordering | Choose most constrained variable first |
| LCV | Ordering | Choose least constraining value first |
| Forward Checking | Filtering | Prune domains after assignment |
| Arc Consistency (AC-3) | Filtering | Propagate constraints through graph |
| Decomposition | Structure | Split into independent subproblems |
| Tree Algorithm | Structure | `O(nd²)` for acyclic graphs |
| Cutset Conditioning | Structure | Make graph a tree by fixing cutset |

---

## 7. Complexity Overview

| Algorithm | Time Complexity | Notes |
|-----------|----------------|-------|
| Naive backtracking | `O(dⁿ)` | No improvements |
| With MRV + LCV + FC | Much better in practice | Hard to bound theoretically |
| AC-3 | `O(n²d³)` | Preprocessing |
| Tree CSP | `O(nd²)` | Requires acyclic constraint graph |
| Cutset conditioning | `O(dᶜ · (n-c)d²)` | `c` = cutset size |
