# 讲义 04 - Informed Search（有信息搜索）

**课程**: CS5491: Artificial Intelligence  
**阅读**: RN 第 3.5–3.6, 4.1–4.2 章

---

## 1. Uninformed vs. Informed Search（无信息搜索 vs. 有信息搜索）

| 类型 | 方法 | 类比 |
|------|------|------|
| **Uninformed Search（无信息搜索）** | DFS, BFS, UCS | **闭着眼睛**找路 |
| **Informed Search（有信息搜索）** | Greedy, A\* | **睁着眼睛**找路 |

有信息搜索会利用 **Problem-Specific Knowledge（问题相关的知识，即启发式）** 来引导搜索朝向目标，从而更高效地找到解。

---

## 2. Heuristic Function（启发式函数）

一个 Heuristic Function `h(n)` 是：
- 一个用来估计 **State `n` 距离 Goal（目标）有多近** 的函数
- 为某一个**具体搜索问题**设计

示例：
- **Manhattan Distance（曼哈顿距离）**：`|Δx| + |Δy|`（常用于网格地图）
- **Euclidean Distance（欧式距离）**：`sqrt(Δx² + Δy²)`（直线距离）
- **Pancake Problem（煎饼问题）**：最大那块仍未在正确位置的煎饼的索引

> 启发式是高度 Problem-Specific（问题相关）的 —— **不存在万能启发式（No Universal Heuristic）**。

---

## 3. Greedy Best-First Search（贪心最佳优先搜索）

**策略**：总是扩展**看起来离目标最近（Closest to Goal）**的结点

**Priority（优先级）**：`h(n)` —— 从当前结点到目标的**估计剩余代价（Estimated Remaining Cost）**

### 贪心搜索的问题

- **Best Case（最好情况）**：直奔目标，非常快
- **Worst Case（最坏情况）**：像一个引导很差的 DFS —— 可能迷路很深，甚至找不到解
- **Not Optimal（不最优）**：只看 `h(n)`，忽略已经付出的代价 `g(n)`
- **Incomplete（不完备）**：可能沿某条"坏路径"无限深入

> 示例：在罗马尼亚地图中，贪心搜索可能选了一条中间城市看上去更靠近 Bucharest 的路径，但整体路径却更长。

---

## 4. A\* Search（A\* 搜索）

### 4.1 核心思想：融合 UCS 和 Greedy

| 算法 | Priority（优先级） | 关注点 |
|------|--------|--------|
| **UCS** | `g(n)` | **已走的代价（Past Cost）**（从起点到 n） |
| **Greedy** | `h(n)` | **估计剩余代价（Estimated Future Cost）**（从 n 到目标） |
| **A\*** | `f(n) = g(n) + h(n)` | **估计的总路径代价（Estimated Total Path Cost）** |

- `g(n)` = 从起点到结点 `n` 的 Actual Cost（真实代价）
- `h(n)` = 从 `n` 到目标的 Estimated Cost（估计代价）
- `f(n)` = 经过 `n` 的整条路径的 Estimated Total Cost（估计总代价）

### 4.2 终止条件（Termination Condition）

> **当某个目标结点从 Priority Queue（优先队列）中被取出（Dequeue）时停止** —— 而不是当它第一次被放入队列时。

这是保证 Optimality（最优性）的关键：处于边界上的某个目标结点，其当前路径不一定是最便宜的。

---

## 5. Admissibility（可采纳性）

### 5.1 定义

若对所有状态 `n`，启发式 `h` 满足：

```text
0 ≤ h(n) ≤ h*(n)
```

其中 `h*(n)` 是从 `n` 到最近目标的 **True Minimum Cost（真实最小代价）**，则称 `h` 为 **Admissible（可采纳的）**，也称为 **Optimistic（乐观的）**。

> Admissible Heuristic（可采纳启发式）**从不高估（Never Overestimates）** 到目标的真实代价。

### 5.2 直观理解

| Heuristic Type（启发式类型） | 行为 |
|------------|------|
| **Admissible / Optimistic（可采纳 / 乐观）** | 会拖慢坏计划，但不会压过真实代价 → 保证 Optimality（最优性） |
| **Inadmissible / Pessimistic（不可采纳 / 悲观 / 过大）** | 可能"困住"真正好的计划在边界上 → 破坏最优性 |

---

## 6. A\* Optimality Proof（A\* 最优性证明，树搜索版本）

**设定**：
- `A` = Optimal Goal Node（最优目标结点，真实代价最小）
- `B` = Suboptimal Goal Node（次优目标结点，`g(B) > g(A)`）
- 启发式 `h` 是 Admissible（可采纳的）

**命题**：`A` 会在 `B` 之前从 Fringe（边界）中被取出并扩展。

**证明思路**：
1. 当 `B` 在 Fringe 上时，`A` 的某个 Ancestor（祖先）`n` 也必定在 Fringe 上。
2. 由 Admissibility（可采纳性）：`f(n) = g(n) + h(n) ≤ g(A)`（因为 `h(n) ≤ h*(n)`）
3. 对 Goal Node（目标结点），有 `h = 0`，所以 `f(A) = g(A)`
4. 因 `B` 是次优，`g(A) ≤ g(B)`，因此 `f(A) ≤ f(B)`
5. 结合 2、4：`f(n) ≤ f(A) < f(B)`
6. 根据 A\* 的优先级规则，`n` 会先于 `B` 被扩展 → 进而 `A` 的所有祖先会在 `B` 之前扩展 → **A 在 B 之前被扩展**

**结论**：使用 Admissible Heuristic（可采纳启发式）的 A\* 在树搜索中是 **Optimal（最优）的**。

---

## 7. UCS vs. A\* —— Cost Contour（等高线）比较

| 算法 | Expansion Pattern（探索模式） |
|------|----------|
| **UCS** | 在**所有方向**上均匀扩展（Cost Contours 近似"圆形"） |
| **A\*** | 主要朝 **Goal Direction（目标方向）** 扩展（等高线被"拉长"并指向目标） |

> 当有一个好的 Heuristic（启发式）时，A\* 相比 UCS 能极大提高效率。

---

## 8. 构造 Admissible Heuristic（可采纳启发式）

> 使用 A\* 时，大部分难度其实在于**设计一个好的 Admissible Heuristic（可采纳启发式）**。

### 关键技巧：Relaxed Problems（放宽问题）

- **Relaxed Problem（放宽问题）**：从原问题中**移除（Relax）一些约束**
- 放宽问题的最优解代价，对原问题而言，是一个 Admissible Heuristic

**示例 —— 8-Puzzle（8 拼图）**：

| Heuristic（启发式） | 对应放宽 |
|--------|----------|
| Misplaced Tiles（错位方块数） | 方块可以"跳到任意位置"，不受阻挡 |
| Manhattan Distance Sum（曼哈顿距离之和） | 方块可以"穿过其他方块"，只管走直线 |

> Heuristic 越"强大"（越接近真实代价，同时不超过），A\* 扩展的结点越少，搜索越快。  
> 在实践中，也可以用 Inadmissible Heuristic（不可采纳启发式）（允许少量高估）来换取更快的速度，但会牺牲最优性。

---

## 9. A\* 的典型应用

- 视频游戏中 NPC 的 Path Planning（路径规划）
- Navigation（导航）/ Route Planning（路径规划，如地图应用）
- Robot Motion Planning（机器人运动规划）
- Resource & Task Planning（资源与任务规划）
- 语义分析与 Machine Translation（机器翻译）中的搜索
- 语音识别中的 Hidden State Decoding（隐状态解码）

---

## 10. A\* 小结

| 性质 | A\* |
|------|-----|
| **Complete（完备性）** | 是（在 Heuristic Admissible 且步长下界 > 0 时） |
| **Optimal（最优性）** | 是（Heuristic Admissible 时） |
| **Time Complexity（时间复杂度）** | 依赖于 Heuristic 质量，最坏情况仍接近指数级 |
| **Space Complexity（空间复杂度）** | 指数级（需存储全部 Fringe 结点） |

**关键要点**：
- 同时利用 **Past Cost `g(n)`（已走代价）** 和 **Estimated Future Cost `h(n)`（估计剩余代价）**
- 在 Heuristic **Admissible（可采纳）** 时保证 Optimality（最优性）
- 通过 **Relaxed Problems（放宽问题）** 构造 Heuristic 是工程上非常重要的套路

---

## 11. Heuristic Design（启发式设计）即"搜索问题"

进阶方法：把"如何设计一个好 Heuristic"本身视作一个优化 / 搜索问题：
- 使用 Machine Learning（机器学习）自动学习启发式（如对 Knapsack、Online Bin Packing 等问题）
- 使用 Meta-Heuristics（元启发式）、Neural Networks（神经网络）等方法，学习对状态的"值"或"距离"估计

---

## 12. 总结

| 算法 | `f(n)` | Complete（完备） | Optimal（最优） | 说明 |
|------|--------|------|------|------|
| **Greedy** | `h(n)` | 否 | 否 | 只看离目标的估计距离，可能走"看着近其实远"的路 |
| **A\*** | `g(n) + h(n)` | 是 | 是（h Admissible） | 结合 Past Cost 与 Heuristic，最常用的有信息搜索算法 |
| **UCS** | `g(n)` | 是 | 是 | 完全"盲目（Blind）"，不考虑目标方向 |

> **核心洞见**：A\* 使用 Admissible Heuristic 时既 **Optimal（最优）** 又 **Efficient（高效）**。`h(n)` 越接近真实代价 `h*(n)` 而不超过它，A\* 的表现就越好。
