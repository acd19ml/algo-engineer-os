# 讲义 07 - Adversarial Search（对抗搜索）

**课程**: CS5491: Artificial Intelligence  
**阅读**: RN 第 5.1–5.5 章

---

## 1. Game Playing（博弈）现状


| 游戏 | 里程碑 |
| ---------------- | ------------------------------------------------------------ |
| **Checkers（跳棋）** | 1950：首个计算机玩家；1994：Chinook 击败人类冠军；2007：被 "Solved（解出）" |
| **Chess（国际象棋）** | 1997：**Deep Blue** 击败棋王 Garry Kasparov（每秒 2 亿 Positions（局面），搜索深度可达 40 层） |
| **Go（围棋）** | 2016：**AlphaGo** 击败世界冠军（Monte Carlo Tree Search（蒙特卡洛树搜索）+ Learned Evaluation Function（学习得到的评估函数）；Branching Factor（分支因子）b > 300） |


---

## 2. Game Types（游戏类型）


| 维度 | 取值 |
| ------ | -------------------------------------- |
| 结果 | Deterministic（决定性） vs. Stochastic（随机性） |
| 玩家数 | 1、2 或多玩家 |
| 和 / 零和 | Zero-Sum（零和） vs. General-Sum（一般和） |
| 可观测性 | Perfect Information（完全信息） vs. Imperfect Information（不完全信息） |


**目标**：为每个状态 `S` 找到推荐最佳动作的 **Policy（策略）** `π: S → A`。

---

## 3. 决定性游戏的形式化（Formalization of Deterministic Games）


| 组件 | 描述 |
| ------------------------------- | ------------------ |
| `S` | States（所有状态，起始于 `s₀`） |
| `P = {1, ..., N}` | Players（玩家集合，通常 Alternating（轮流）行动） |
| `A` | Actions（动作集合，可能依赖于玩家 / 状态） |
| `T: S × A → S` | Transition Function（状态转移函数） |
| `Terminal Test: S → {t, f}` | 判断游戏是否结束 |
| `Terminal Utilities: S × P → ℝ` | Terminal State（终局）时每个玩家的收益 |
| **解** | Policy（策略）`π: S → A` |


---

## 4. Zero-Sum vs. General-Sum（零和博弈 vs. 一般博弈）


| 类型 | 效用 | 特点 |
| ---------------------- | ------------ | ---------------- |
| **Zero-Sum Game（零和游戏）** | 各方效用**正好相反（Opposite）** | 纯 Competitive（竞争）：一方最大化，另一方最小化 |
| **General-Sum Game（一般和游戏）** | 各方有各自的 Utility Function（效用函数） | 可能 Cooperative（合作）、无关或竞争 |


---

## 5. Single-Agent State Value（单智能体的状态价值）

单智能体情形下：

- **Terminal State（终局状态）**：`V(s)` 由 Objective Function（目标函数）给出
- **Non-Terminal State（非终局状态）**：  
`V(s) = max_{s' ∈ children(s)} V(s')`

智能体总是选择能通向**最高价值子结点（Highest-Value Child）**的动作。

---

## 6. Minimax（极大极小）

### 6.1 Minimax Value（Minimax 值定义）


| Node Type（结点类型） | 取值规则 |
| ---------------- | ----------------------- |
| **MAX Node（MAX 结点，我方回合）** | `V(s) = max_{s'} V(s')` |
| **MIN Node（MIN 结点，对手回合）** | `V(s) = min_{s'} V(s')` |
| **Terminal Node（终局结点）** | `V(s)` = 既定 Utility（效用值） |


### 6.2 Adversarial Search（对抗搜索，Minimax）

- 用于 **Deterministic, Zero-Sum（确定性、零和）** 博弈（Tic-Tac-Toe（井字棋）、Chess（国际象棋）、Checkers（跳棋）等）
- 一方尝试 **Maximize（最大化）**，另一方尝试 **Minimize（最小化）**
- 为每个结点计算其 **Minimax Value**：在对手 **Rational & Worst-Case（理性且最坏行为）** 下仍能保证的最好效用

### 6.3 Minimax Algorithm（Minimax 算法，伪代码）

```text
function MINIMAX(state, depth):
    if TERMINAL(state): return UTILITY(state)
    if MAX's turn:
        return max over successors: MINIMAX(s', depth-1)
    else (MIN's turn):
        return min over successors: MINIMAX(s', depth-1)
```

### 6.4 Minimax Properties（Minimax 性质）


| 性质 | 数值 |
| --------- | ---------- |
| **Complete（完备性）** | 是（若 Game Tree（博弈树）有限） |
| **Optimal（最优性）** | 是（对 Perfectly Rational（完美理性）对手） |
| **Time Complexity（时间复杂度）** | `O(bᵐ)` |
| **Space Complexity（空间复杂度）** | `O(bm)` |


以 Chess（国际象棋）为例：`b ≈ 35`，`m ≈ 100` → 精确搜索整棵树完全不可行。

---

## 7. Alpha-Beta Pruning（α-β 剪枝）

### 7.1 核心思想

跳过那些不可能影响 Root Node（根节点）最终决策的 Subtrees（子树），即 **在保证根结点 Minimax Value 不变的前提下剪枝**。

### 7.2 工作原理

- `α` = 当前路径上，MAX 至少能保证的最好值（**Lower Bound for MAX**）
- `β` = 当前路径上，MIN 至少能保证的最好值（**Upper Bound for MIN**）

**Pruning Rules（剪枝规则）**：

- 在 MIN Node：若当前值 ≤ α → Prune（剪枝，MAX 不会选择这个分支）
- 在 MAX Node：若当前值 ≥ β → Prune（剪枝，MIN 不会选择这个分支）

### 7.3 Alpha-Beta Properties（Alpha-Beta 性质）


| 性质 | 说明 |
| -------------- | ---------------------------------- |
| **Correctness（正确性）** | 不改变根结点的 Minimax Value |
| **Intermediate Node Values（中间结点值）** | 可能不准确（但我们只关心根结点的决策） |
| **Child Expansion Order（子结点展开顺序）** | 越接近真实最优顺序，Pruning（剪枝）效果越好 |
| **Best Case（最优情况，Perfect Ordering）** | Time Complexity 可降为 `O(b^(m/2))` —— 相当于搜索深度翻倍 |


> 在 Perfect Ordering（完美子结点排序）下，Alpha-Beta 能够在相同计算资源下搜索深度约为原来两倍。  
> 即便有 Alpha-Beta，对国际象棋完全搜索仍然是不可能的。

---

## 8. Depth-Limited Search & Evaluation Function（深度限制搜索与评估函数）

**问题**：实际游戏中，很难把搜索做到 Terminal State（终局状态）。

**解决思路**：

- 设置一个 **Depth Limit（搜索深度上限）**
- 用一个 **Evaluation Function `Eval(s)`（评估函数）** 来对 Non-Terminal State（非终局局面）进行估值，代替真实 Terminal Utility

**Evaluation Function 要求**：

- 在 Terminal State 上应与真实 Utility（效用）一致
- 计算要 **Fast（足够快）**
- 对真实 Win Rate（胜率）要有**较强相关性（Strong Correlation）**

**示例**（Chess / 国际象棋）：  
`Eval(s)` = 各棋子价值的加权和（Weighted Sum of Piece Values）+ 若干位置 / 布局特征

**算力估算示例**：

- 100 秒一手棋，每秒 1 万个结点 → 一手约 100 万结点
- 配合 Alpha-Beta 可达到深度约 8 → 已能实现较强水平

> **更深的 Search Depth（搜索深度）通常意味着更强的棋力（Playing Strength）**。  
> 常结合 **Iterative Deepening（迭代加深）** 实现 "Anytime（随时可中断）" 行为。

---

## 9. 小结：Minimax 与 Alpha-Beta


| 算法 | Time（时间） | Space（空间） | Optimal（最优性） | 备注 |
| ------------------ | ----------------- | ------- | --------------- | -------- |
| Minimax | `O(bᵐ)` | `O(bm)` | 是（对 Perfect Opponent） | 对复杂游戏过慢 |
| Alpha-Beta | 最好情况 `O(b^(m/2))` | `O(bm)` | 是（与 Minimax 相同） | 需良好 Child Ordering |
| Depth-Limited Minimax / α-β | 受限 | 受限 | 否 | 借助 Evaluation Function 近似 |


---

## 10. 关键概念


| 术语 | 定义 |
| ---------------------- | ------------------------ |
| **Zero-Sum Game（零和游戏）** | 一方收益等于另一方损失，总和为常数（通常为 0） |
| **Minimax** | MAX 取最大，MIN 取最小，假设双方都 Optimal（最优） |
| **Alpha-Beta Pruning（α-β 剪枝）** | 通过 α, β 界限跳过不可能影响根决策的分支 |
| `α`（Alpha） | 沿当前路径，MAX 已知**能保证的最好值（Best Guaranteed Value）** |
| `β`（Beta） | 沿当前路径，MIN 已知**能保证的最好值（Best Guaranteed Value）** |
| **Evaluation Function `Eval(s)`（评估函数）** | 在 Depth-Limited 时，对中间局面给出 Heuristic Estimate（启发式数值估计） |
| **Metareasoning（元推理）** | 对"该算什么、算到多深"进行的 Rational Thinking（理性思考） |
