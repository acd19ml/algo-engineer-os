# Lecture 03 - Uninformed Search

**Course**: CS5491: Artificial Intelligence
**Reading**: RN Chapter 3.3–3.4

---

## 1. State Space Graphs

A **State Space Graph** is a mathematical representation of a search problem:
- **Nodes**: abstracted world configurations (states)
- **Arcs**: successors (action results)
- **Goal**: a set of goal nodes

> Each state occurs **only once** in the graph.
> In practice, the full graph is too large to build in memory — it is a conceptual tool.

---

## 2. Search Trees

A **Search Tree** is a "what-if" tree of plans and their outcomes:

| Component | Description |
|-----------|-------------|
| Root | Start state |
| Child nodes | Successors of parent state |
| Each node | Represents an **entire path** (plan) in the state space graph |

> Building the whole tree is impossible for most problems — we build it **on demand**.

### State Space Graph vs. Search Tree

| State Space Graph | Search Tree |
|-------------------|-------------|
| Each state appears once | Same state may appear multiple times |
| Compact representation | Exponentially larger |
| Each node = a state | Each node = a **path** to that state |

---

## 3. Tree Search Algorithm

**Key concepts**:
- **Fringe**: set of partial plans (nodes) under consideration
- **Expansion**: generating successor nodes from a fringe node
- **Exploration Strategy**: determines which fringe node to expand next

**Main question**: *Which fringe node to explore next?*

```
function TREE-SEARCH(problem):
    initialize fringe with start state
    loop:
        if fringe is empty: return FAILURE
        node = remove from fringe (per strategy)
        if GOAL-TEST(node.state): return SOLUTION(node)
        add successors of node to fringe
```

---

## 4. Search Algorithm Properties

Four key evaluation criteria:

| Property | Definition |
|----------|-----------|
| **Complete** | Guaranteed to find a solution if one exists? |
| **Optimal** | Guaranteed to find the **least cost** path? |
| **Time Complexity** | How many nodes are generated/expanded? |
| **Space Complexity** | How many nodes are stored in memory? |

### Tree Parameters
- `b` = **branching factor** (max successors per node)
- `m` = **maximum depth** of the tree
- `s` = **depth of shallowest solution**
- Total nodes in tree = `1 + b + b² + ... + b^m = O(b^m)`

---

## 5. Depth-First Search (DFS)

**Strategy**: Expand the **deepest** node first

**Implementation**: Fringe is a **LIFO stack** (Last In, First Out)

### DFS Properties

| Property | Answer | Reason |
|----------|--------|--------|
| **Complete** | No (Yes with cycle prevention) | `m` could be infinite |
| **Optimal** | No | Finds leftmost solution, not cheapest |
| **Time** | `O(b^m)` | May explore entire tree |
| **Space** | `O(bm)` | Only siblings on the current path |

> **DFS Space Advantage**: Only stores the current path + siblings — very memory efficient.

---

## 6. Breadth-First Search (BFS)

**Strategy**: Expand the **shallowest** node first

**Implementation**: Fringe is a **FIFO queue** (First In, First Out)

### BFS Properties

| Property | Answer | Reason |
|----------|--------|--------|
| **Complete** | **Yes** | `s` is finite if a solution exists |
| **Optimal** | **Only if all costs = 1** | Finds shallowest, not cheapest |
| **Time** | `O(b^s)` | Processes all nodes at depth ≤ s |
| **Space** | `O(b^s)` | Must store entire last tier |

> **BFS Space Problem**: Storing an entire level can be exponentially expensive.

---

## 7. DFS vs. BFS Comparison

| Property | DFS | BFS |
|----------|-----|-----|
| Complete | No* | Yes |
| Optimal | No | Only if uniform cost |
| Time | `O(b^m)` | `O(b^s)` |
| Space | `O(bm)` | `O(b^s)` |
| Fringe | Stack (LIFO) | Queue (FIFO) |
| Best for | Deep solutions, limited memory | Shallow solutions, completeness needed |

*With cycle detection: complete when `m` is finite.

---

## 8. Iterative Deepening (IDS)

**Idea**: Combine the **space advantage of DFS** with the **completeness/optimality of BFS**

**Algorithm**:
1. Run DFS with depth limit = 1 → if no solution...
2. Run DFS with depth limit = 2 → if no solution...
3. Run DFS with depth limit = 3 → ...

**Is it wasteful?** No — most work happens at the deepest level, so repeated work at shallower levels is negligible.

| Property | IDS |
|----------|-----|
| Complete | Yes |
| Optimal | Yes (uniform cost) |
| Time | `O(b^s)` |
| Space | `O(bs)` ← best of both worlds |

---

## 9. Cost-Sensitive Search

> **BFS limitation**: finds path with fewest actions, NOT the least-cost path.

We need a search that respects edge costs.

---

## 10. Uniform Cost Search (UCS)

**Strategy**: Expand the **cheapest** node first (by cumulative path cost `g(n)`)

**Implementation**: Fringe is a **priority queue** (priority = cumulative cost)

### UCS Properties

| Property | Answer | Reason |
|----------|--------|--------|
| **Complete** | **Yes** | If min arc cost ε > 0 and optimal cost C* is finite |
| **Optimal** | **Yes** | Always expands cheapest unexplored node |
| **Time** | `O(b^(C*/ε))` | Explores all nodes with cost ≤ C* |
| **Space** | `O(b^(C*/ε))` | Stores last tier of cost-contour |

Where:
- `C*` = cost of optimal solution
- `ε` = minimum arc cost
- `C*/ε` = "effective depth"

### UCS Behavior
- Explores nodes in **increasing cost contours** (like ripples in water)
- Good: complete and optimal
- Bad: explores in **all directions** — no information about where the goal is

---

## 11. Uninformed Search Summary Table

| Algorithm | Complete | Optimal | Time | Space | Fringe |
|-----------|----------|---------|------|-------|--------|
| **DFS** | No* | No | `O(b^m)` | `O(bm)` | Stack |
| **BFS** | Yes | Only if uniform | `O(b^s)` | `O(b^s)` | Queue |
| **IDS** | Yes | Only if uniform | `O(b^s)` | `O(bs)` | Stack (with limit) |
| **UCS** | Yes | Yes | `O(b^(C*/ε))` | `O(b^(C*/ε))` | Priority Queue |

---

## 12. Search and Models

> Search operates over **models** of the world — not the real world.

- The agent does NOT try plans in the real world
- Planning is done **in simulation**
- **Your search is only as good as your model**

This is a critical point: if your transition model is wrong, even optimal search will produce bad plans.

---

## 13. Key Concepts Summary

| Term | Meaning |
|------|---------|
| **Fringe** | Set of nodes to be explored |
| **LIFO stack** | Last-in-first-out → used by DFS |
| **FIFO queue** | First-in-first-out → used by BFS |
| **Priority queue** | Sorted by cost → used by UCS |
| **Branching factor `b`** | Average successors per node |
| **Depth `m`** | Maximum depth of search tree |
| **Shallowest solution `s`** | Depth of the nearest goal |
| **Optimal solution cost `C*`** | Cost of the cheapest solution |
| **Min arc cost `ε`** | Smallest edge weight in the graph |

---

## 14. Looking Ahead

UCS is optimal but **blind** — it wastes effort exploring in all directions.

**Next**: Informed Search (Lecture 04) uses **heuristics** to guide search toward the goal, dramatically improving efficiency.
