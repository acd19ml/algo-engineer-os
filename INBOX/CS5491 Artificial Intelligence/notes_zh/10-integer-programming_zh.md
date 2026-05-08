# 讲义 10 - Integer Programming, IP & Branch and Bound（整数规划与分支定界）

**课程**: CS5491: Artificial Intelligence

---

## 1. 从 LP 到 Integer Programming, IP（整数规划）

- **LP**：变量可以取任意 Real Number（实数值）→ 例如可以买 3.7 盎司炒菜
- **IP**：变量必须为 **Integer（整数）** → 只能买整碗 / 整杯

**示例**：
- LP：选择炒菜和奶茶的"连续数量"（盎司），变量是实数
- IP：选择炒菜碗数、奶茶杯数，变量必须是**整数（Integer）**

---

## 2. Integer Programming, IP（整数规划）的形式化

```text
min  cᵀx
 x
s.t. Ax ≤ b
     x ∈ ℤᴺ      ← Integer Constraint（整数约束）
```

### Common Variants（常见变体）

| Type（类型） | Constraint（约束） | Typical Use（典型用途） |
|------|------|----------|
| **LP** | `x ∈ ℝᴺ` | Continuous Quantity Decisions（连续数量决策） |
| **IP** | `x ∈ ℤᴺ` | All-Integer Decisions（全部为整数） |
| **Binary IP, BIP（二值整数规划）** | `x ∈ {0,1}ᴺ` | Yes/No, Select/Skip Decisions（是 / 否、选 / 不选类型决策） |
| **Mixed Integer LP, MILP（混合整数线性规划）** | 部分变量为整数，部分为实数 | Mixed Discrete & Continuous Decisions（既有离散决策又有连续决策） |

---

## 3. LP Relaxation（LP 松弛）

**LP Relaxation（LP 松弛）**：把 Integer Programming 中的 Integer Constraint（整数约束）去掉，当作普通 Linear Programming 来解。

```text
min  cᵀx          ← 与 IP 相同
 x
s.t. Ax ≤ b       ← 与 IP 相同
                  ← 不再要求 x 为整数
```

### 关键性质（针对 **Minimization Problem，最小化问题**）

记 `y*_IP` 为 IP 的 Optimal Objective Value（最优目标值），`y*_LP` 为相应 LP Relaxation 的最优目标值。

| Proposition（命题） | Correct?（正确性） | 理由 |
|------|--------|------|
| `x*_IP = x*_LP` | **一般错误** | LP Optimal Solution（最优解）往往是 Non-Integer（非整数） |
| `y*_IP ≤ y*_LP` | **错误** | IP Constraints（约束）更严格，最优值一般更大 |
| `y*_IP ≥ y*_LP` | **正确** | LP Feasible Region（可行域）是 IP 的 Superset（超集） |

> 对于 Minimization Problem（最小化问题），LP Relaxation 给出了 IP 最优值的一个 **Lower Bound（下界）**。

**类比 A\***：LP Relaxation 的最优值类似于一个 **Admissible Heuristic（可采纳启发式）**，它 Underestimates（低估）真实整数解的代价，因此可用于 Pruning（剪枝）。

---

## 4. 直接对 LP 解"取整（Round）"可以吗？

**问题**：把 LP 的 Optimal Real Solution（最优实数解）就地"四舍五入（Round）"为整数，是否总是 Feasible（可行）/ 接近最优？

**答案**：**不可靠（Unreliable）**。

- Rounding（取整）后可能**违反约束（Violate Constraints）**，变成 Infeasible Solution（不可行解）
- 即便可行，也可能远离真正的 Integer Optimal Solution（整数最优解）

在二维几何图中，经常可以看到 LP Optimal Vertex（最优解所在顶点）与最近的 Feasible Integer Point（可行整数点）距离很远。

---

## 5. Branch and Bound, B&B（分支定界算法）

**核心思想**：对 LP Relaxation 解中带小数（Fractional）的变量，逐个添加约束进行 "Branch（分支）"，并用 LP 解的 Lower Bound（下界）来 "Bound / Prune（定界 / 剪枝）"。

### Algorithm Framework（算法框架）

```text
function BRANCH_AND_BOUND(LP):
    solve LP relaxation → 得到解 x*_LP
    if x*_LP 是 Integer Solution（整数解）: return x*_LP  （可行整数解）
    if LP 无可行解: return ∞

    找到某个使得 x*_LP[i] 为 Fractional（非整数）的下标 i
    left_LP  = 在 LP 上加约束 {xᵢ ≤ floor(x*_LP[i])}
    right_LP = 在 LP 上加约束 {xᵢ ≥ ceil(x*_LP[i])}

    left_val  = BRANCH_AND_BOUND(left_LP)
    right_val = BRANCH_AND_BOUND(right_LP)

    return min(left_val, right_val)
```

### Pruning Rules（剪枝 / 定界规则）—— 可以停止向下搜索的情况：

1. **LP Solution is Integer（LP 解为整数）** → 已找到一个 Feasible IP Solution（可行 IP 解），可作为当前 Candidate（候选）
2. **LP Objective ≥ Current Best Integer Solution（LP 目标值 ≥ 已知最好整数解）** → 此分支不可能更优，直接 Prune（剪掉）
3. **LP Infeasible（LP 无可行解）** → 该分支没有任何解

### 直观图示

```text
                     LP Relaxation（根结点）
                    /                 \
          xᵢ ≤ ⌊x*ᵢ⌋                   xᵢ ≥ ⌈x*ᵢ⌉
             /                               \
        解子 LP                          解子 LP
   （Prune or Branch）              （Prune or Branch）
```

---

## 6. B&B 示例：整数版饮食问题

**目标**：在饮食问题中要求 `x₁, x₂` 都是 Integer（整数）。

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | 解 LP Relaxation | 得到 Non-Integer Solution（非整数解，如 `x₁=3.5`） |
| 2 | 在 `x₁` 上 Branch（分支）：`x₁≤3` 和 `x₁≥4` | 得到两个子问题 |
| 3 | 分别解两个 Sub-LPs（子 LP） | 得到两个 Lower Bounds（下界）或整数解 |
| 4 | 利用 Lower Bound 与当前 Best Integer Solution（最优整数解）比较 Prune（剪枝） | 去掉不可能更优的子树 |
| 5 | 在剩余子树中继续 Branch / Prune | 直到遍历完所有必要分支 |

最终返回所有 **Feasible Integer Solutions（可行整数解）** 中目标值最小的那一个。

---

## 7. Complexity Comparison（复杂度比较）

| Problem Type（问题类型） | Complexity（复杂度） | 说明 |
|----------|--------|------|
| LP | Polynomial Time（多项式时间，内点法等） | 在实践中相当高效 |
| IP | 一般为 NP-Hard | 最坏情况下指数复杂度 |
| IP + Branch & Bound | 最坏仍为指数，但实践中通常较快 | Commercial Solvers（商业求解器）广泛采用 |

---

## 8. 小结

| 概念 | 要点 |
|------|------|
| **IP（整数规划）** | 在 Linear Constraints（线性约束）下增加 Integer Constraint（整数约束） |
| **BIP（二值整数规划）** | 变量只取 0/1，用于 Binary Selection Problems（选择问题） |
| **MILP（混合整数线性规划）** | 部分变量整数，部分连续 |
| **LP Relaxation（LP 松弛）** | 去掉 Integer Constraint，给出 IP 目标的 Lower Bound（下界，对最小化） |
| **Branch and Bound, B&B（分支定界）** | Recursively Branch（递归分支）Non-Integer Variables（非整数变量），并用 LP Lower Bound 进行 Pruning（剪枝） |
| **Pruning Conditions（剪枝条件）** | LP 目标值 ≥ 当前最佳整数解，或 LP Infeasible（不可行） |

> **关键洞见**：LP Relaxation 在 Integer Programming 中扮演的角色类似于 A\* 搜索中的 Admissible Heuristic（可采纳启发式） —— 它提供了一个 **Optimistic Lower Bound（乐观下界）**，帮助我们有效地 Prune（剪枝）次优分支。
