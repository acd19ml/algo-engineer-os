# 讲义 03 - Uninformed Search（无信息搜索）

**课程**: CS5491: Artificial Intelligence  
**阅读**: RN 第 3.3–3.4 章

---

## 1. State Space Graph（状态空间图）

**State Space Graph（状态空间图）** 是对一个搜索问题的数学表示：
- **Nodes（结点）**：抽象后的世界配置（状态）
- **Arcs / Edges（边 / 弧）**：Successor（后继，即动作结果）
- **Goal（目标）**：一组目标结点

> 在状态空间图中，每个状态在图里**只出现一次**。  
> 实际实现中，完整图往往过大，无法全部构建在内存中，更多是**概念上的工具（Conceptual Tool）**。

---

## 2. Search Tree（搜索树）

**Search Tree（搜索树）** 是"假如……会怎样"的计划树，表示不同行动序列及其结果：

| 组件 | 描述 |
|------|------|
| Root（根结点） | Start State（起始状态） |
| Children（子结点） | 父状态的 Successor（后继） |
| 每个结点 | 表示状态空间图中一条**完整路径（Path / Plan）** |

> 对大多数问题来说，构建整棵搜索树是不可行的 —— 我们只在需要时 **On-Demand Expansion（按需扩展）**。

### State Space Graph vs. Search Tree（状态空间图 vs. 搜索树）

| State Space Graph（状态空间图） | Search Tree（搜索树） |
|----------------------------------|------------------------|
| 每个状态只出现一次 | 同一状态可能多次出现 |
| 表示紧凑 | 规模呈指数增长 |
| 结点 = "一个状态" | 结点 = "到该状态的一条路径" |

---

## 3. Tree Search（树搜索算法）

**关键概念**：
- **Fringe（边界）**：当前在考虑的一组"部分计划"（结点）
- **Expansion（展开）**：从某个边界结点生成其 Successor（后继结点）
- **Exploration Strategy（探索策略）**：决定下一步从边界中取出哪个结点来展开

**核心问题**：*下一个要扩展的是哪一个 Fringe Node（边界结点）？*

```text
function TREE-SEARCH(problem):
    initialize fringe with start state
    loop:
        if fringe is empty: return FAILURE
        node = remove from fringe (per strategy)
        if GOAL-TEST(node.state): return SOLUTION(node)
        add successors of node to fringe
```

---

## 4. 搜索算法的性质（Properties of Search Algorithms）

四个评价维度：

| 性质 | 含义 |
|------|------|
| **Complete（完备性）** | 若解存在，是否一定能找到？ |
| **Optimal（最优性）** | 是否一定能找到 **Least-Cost Path（代价最小）** 的路径？ |
| **Time Complexity（时间复杂度）** | 会生成 / 展开多少结点？ |
| **Space Complexity（空间复杂度）** | 会在内存中存储多少结点？ |

### Tree Parameters（树的参数）

- `b` = **Branching Factor（分支因子）**：每个结点最多有多少个后继
- `m` = **Maximum Depth（最大深度）**：搜索树可能的最大深度
- `s` = **Depth of Shallowest Solution（最近解的深度）**
- 整棵树结点数：`1 + b + b² + ... + b^m = O(b^m)`

---

## 5. Depth-First Search, DFS（深度优先搜索）

**策略**：总是优先展开**最深的结点（Deepest Node）**

**实现**：Fringe 使用 **LIFO Stack（后进先出栈）**

### DFS 性质

| 性质 | 结论 | 原因 |
|------|------|------|
| **Complete（完备性）** | 否（若避免循环且 `m` 有限则是） | `m` 可能是无穷 |
| **Optimal（最优性）** | 否 | 返回最左边的那个解，不一定是最便宜的 |
| **Time Complexity（时间复杂度）** | `O(b^m)` | 可能遍历整棵树 |
| **Space Complexity（空间复杂度）** | `O(bm)` | 只需存当前路径及其兄弟结点 |

> **DFS 的空间优势（Space Advantage）**：只需要存储当前路径和同层的少量结点，内存占用非常小。

---

## 6. Breadth-First Search, BFS（广度优先搜索）

**策略**：总是优先展开**最浅的结点（Shallowest Node）**

**实现**：Fringe 使用 **FIFO Queue（先进先出队列）**

### BFS 性质

| 性质 | 结论 | 原因 |
|------|------|------|
| **Complete（完备性）** | **是** | 若存在解，则最近解深度 `s` 有限 |
| **Optimal（最优性）** | **仅当所有边代价都为 1 时成立** | 否则只保证最浅，不保证最便宜 |
| **Time Complexity（时间复杂度）** | `O(b^s)` | 需要遍历深度 ≤ s 的所有结点 |
| **Space Complexity（空间复杂度）** | `O(b^s)` | 需存储最深一层的所有结点 |

> **BFS 的空间问题（Space Issue）**：某一层的结点数呈指数级增长，需要大量内存。

---

## 7. DFS vs. BFS 对比

| 性质 | DFS | BFS |
|------|-----|-----|
| Complete（完备性） | 否* | 是 |
| Optimal（最优性） | 否 | 仅在单位代价时是 |
| Time Complexity（时间复杂度） | `O(b^m)` | `O(b^s)` |
| Space Complexity（空间复杂度） | `O(bm)` | `O(b^s)` |
| Fringe Structure（边界结构） | Stack（LIFO） | Queue（FIFO） |
| 适用场景 | 解很深 / 内存有限 | 解较浅 / 需要完备性 |

\* 带"Loop Detection（循环检测）"且最大深度有限时，DFS 可以是完备的。

---

## 8. Iterative Deepening Search, IDS（迭代加深搜索）

**核心想法**：结合 DFS 的**空间优势（Space Advantage）**和 BFS 的**Complete / Optimal（完备 / 最优）**特性。

**算法**：
1. 先运行一次 Depth Limit = 1 的 DFS → 若无解…
2. 再运行一次 Depth Limit = 2 的 DFS → 若无解…
3. 再运行一次 Depth Limit = 3 的 DFS → 以此类推

### 是否很浪费（Wasteful）？

并不。大部分工作都发生在最深一层；对浅层的重复探索在整体中占比很小。

| 性质 | IDS |
|------|-----|
| Complete（完备性） | 是 |
| Optimal（最优性） | 是（在 Unit Cost（单位代价）情形） |
| Time Complexity（时间复杂度） | `O(b^s)` |
| Space Complexity（空间复杂度） | `O(bs)` ← 同时具备 DFS 的低空间占用 |

---

## 9. Cost-Sensitive Search（代价敏感的搜索）

> **BFS 的局限**：找到的是"动作数最少（Fewest Actions）"的路径，而不是 **Least-Cost Path（代价最小的路径）**。

在边代价（Edge Cost）不全相同的情况下，我们需要一种真正考虑路径代价的搜索方法。

---

## 10. Uniform Cost Search, UCS（一致代价搜索）

**策略**：总是优先展开**当前累计路径代价 `g(n)` 最小**的结点

**实现**：Fringe 使用 **Priority Queue（优先队列）**，优先级 = 累计代价 `g(n)`

### UCS 性质

| 性质 | 结论 | 原因 |
|------|------|------|
| **Complete（完备性）** | **是** | 若最小边代价 ε > 0，且最优解代价 C\* 有限 |
| **Optimal（最优性）** | **是** | 总是先扩展代价最小的未探索结点 |
| **Time Complexity（时间复杂度）** | `O(b^(C*/ε))` | 会扩展所有代价 ≤ C\* 的结点 |
| **Space Complexity（空间复杂度）** | `O(b^(C*/ε))` | 需存储该"代价等高线"上的最后一层结点 |

其中：
- `C*` = Optimal Cost（最优解的代价）
- `ε` = Minimum Edge Cost（单条边的最小代价）
- `C*/ε` = Effective Depth（有效深度）

### UCS 的行为

- 按 **Cost Contours（代价等高线）** 由低到高依次扩展结点（好像水波扩散）
- 优点：Complete（完备）、Optimal（最优）
- 缺点：**对 Goal（目标）位置一无所知**，会向所有方向盲目扩展

---

## 11. Uninformed Search（无信息搜索）小结

| 算法 | Complete（完备） | Optimal（最优） | Time | Space | Fringe Structure（边界结构） |
|------|------|------|------|------|----------|
| **DFS** | 否* | 否 | `O(b^m)` | `O(bm)` | Stack（LIFO） |
| **BFS** | 是 | 仅单位代价时 | `O(b^s)` | `O(b^s)` | Queue（FIFO） |
| **IDS** | 是 | 仅单位代价时 | `O(b^s)` | `O(bs)` | Depth-Limited Stack（有深度限制的栈） |
| **UCS** | 是 | 是 | `O(b^(C*/ε))` | `O(b^(C*/ε))` | Priority Queue（优先队列） |

---

## 12. 搜索与"模型"

> 搜索是在对世界的 **Model（模型）** 上进行的 —— 而不是直接在真实世界上进行。

- 智能体不会在真实世界中直接尝试所有计划
- 规划是在 **Simulated Environment（模拟环境）**（模型）中完成的
- **搜索质量取决于模型质量（Search Quality Depends on Model Quality）**

如果 Transition Model（状态转移模型）不准确，即便使用最优搜索算法，也可能得到很差的真实行为效果。

---

## 13. 关键概念总结

| 术语 | 含义 |
|------|------|
| **Fringe（边界）** | 有待扩展的结点集合 |
| **LIFO Stack（后进先出栈）** | Last In First Out → DFS 使用 |
| **FIFO Queue（先进先出队列）** | First In First Out → BFS 使用 |
| **Priority Queue（优先队列）** | 按代价排序 → UCS 使用 |
| **Branching Factor `b`（分支因子）** | 平均每个结点的后继结点数 |
| **Maximum Depth `m`（最大深度）** | 搜索树可能的最大深度 |
| **Shallowest Solution Depth `s`（最浅解深度）** | 最近目标结点所在的深度 |
| **Optimal Cost `C*`（最优解代价）** | 成本最小那条路径的总代价 |
| **Minimum Edge Cost `ε`（最小边代价）** | 所有边中最小的权重 |

---

## 14. 展望

UCS 能找到最优解，但仍然是 **"Blind（盲目的）"** —— 它不知道目标大致在哪个方向，会在所有方向上浪费探索。

**下一讲（Lecture 04）**：Informed Search（有信息搜索），通过 **Heuristic Function（启发式函数）** 引导搜索朝着目标前进，大幅提升效率。
