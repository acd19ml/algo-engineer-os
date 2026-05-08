# 讲义 06 - 约束满足 II：Backtracking & Improvements（回溯与改进）

**课程**: CS5491: Artificial Intelligence  
**阅读**: RN 第 6 章

---

## 1. Backtracking Search（回溯搜索）

### 核心思想

在 DFS 的基础上针对 CSP 做两点关键改进：

| 思想 | 描述 |
|------|------|
| **一次只给一个变量赋值（One Variable at a Time）** | 固定变量顺序；赋值具有 **Commutativity（可交换性）** —— `[WA=red, NT=green]` 与 `[NT=green, WA=red]` 等价 |
| **Incremental Goal Test（随赋值即时检查约束）** | 只考虑与已有赋值**不冲突（Consistent）**的取值 |

> **Backtracking = DFS + Variable Ordering（变量顺序）+ Failure on Constraint Violation（违反约束立刻回退）**  
> 在实际中已经可以解决 N≈25 的 N-Queens Problem（N 皇后问题）。

### 算法

```text
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

## 2. 提升回溯效率的三大策略

| 策略 | 要回答的问题 |
|------|--------------|
| **Ordering（排序）** | 先给哪个变量赋值？每个变量先尝试哪个取值？ |
| **Filtering（过滤）** | 能否及早发现 Unsolvable Branch（无解分支）？ |
| **Structure（利用结构）** | 能否利用 Constraint Graph Structure（约束图结构）拆分问题？ |

---

## 3. Ordering（排序）

### 3.1 Variable Ordering：MRV, Minimum Remaining Values（最少剩余值）

- 每次选择 **Current Legal Value Count（当前合法取值数）最少** 的变量
- 又称：**Most Constrained Variable（最受限变量）** 或 **"Fail-First（优先失败）"** Heuristic
- **为什么是"最少"？** 因为这些变量最容易导致 Failure（失败），优先尝试能更早发现 Dead-End（死路）

### 3.2 Value Ordering：LCV, Least Constraining Value（最少约束值）

- 对某变量，优先选择**对其他变量约束最少（Least Constraining）**的取值
- **为什么是"最少约束"？** 因为希望给后续变量留下更多合法空间（Flexibility）

> **MRV + LCV 的组合可以让 1000-Queens Problem（1000 皇后问题）也变得可行！**

| Ordering Type（排序类型） | Heuristic（启发式） | 目标 |
|----------|--------|------|
| Variable Ordering（变量排序） | MRV（最少剩余值） | 让 Failure **尽早**暴露（Fail Fast） |
| Value Ordering（取值排序） | LCV（最少约束值） | 让 Success **尽快**出现（Succeed First），保留灵活性 |

---

## 4. Filtering（过滤）

### 4.1 Forward Checking（前向检验）

- 给某变量赋值后，**从其相邻变量的 Domain（取值域）中划去与之冲突的值**
- 可以立刻检测 "Obvious Conflicts（显而易见的矛盾）"

**示例（澳大利亚地图着色）**：
- 赋值 `WA = red` → 从 NT 和 SA 的 Domain 中删除 `red`
- 赋值 `Q = green` → 从 NT, NSW, SA 的 Domain 中删除 `green`
- 若某变量 Domain 被删空 → 立即 Backtrack（回溯）

**局限（Limitation）**：只向前看**一层邻居（One-hop Neighbors）**，无法捕捉更深层的潜在矛盾。

### 4.2 Constraint Propagation（约束传播）：Arc Consistency（弧一致性）

**Arc Consistency（弧一致性）**：Directed Arc（有向弧）`X → Y` 是一致的，当且仅当对 `X` 的 Domain 中的每一个 `x`，在 `Y` 的 Domain 中至少存在一个 `y` 与之满足约束。

- **关键传播规则（Propagation Rule）**：如果 `X` 失去了某个取值，则需要重新检查 `X` 的所有 Neighbors（邻居）
- 通过在 Constraint Graph 上反复传播删值信息来提前识别 Inconsistency（不一致）

**AC-3 Algorithm（AC-3 算法）**：

```text
function AC-3(csp):
    queue = all arcs in csp
    while queue not empty:
        (Xi, Xj) = DEQUEUE(queue)
        if REVISE(csp, Xi, Xj):
            if |domain(Xi)| == 0: return false  # 失败
            for each Xk in neighbors(Xi) - {Xj}:
                ENQUEUE(queue, (Xk, Xi))
    return true
```

**Time Complexity（时间复杂度）**：`O(n² d³)`，可优化至 `O(n² d²)`（`n` 为变量数，`d` 为最大域大小）

| 方法 | 检测范围 | 说明 |
|------|----------|------|
| Forward Checking（前向检验） | Direct Neighbors（仅直接邻居） | 快，但只看一步 |
| Arc Consistency（弧一致性） | All Arcs（图上所有弧） | 更深层传播，但更慢 |

### 4.3 Arc Consistency 的局限

在执行完 Arc Consistency 之后，CSP 可能：
- 只剩下 **Unique Solution（唯一解）**
- 还剩下 **Multiple Solutions（多个解）**（仍需要搜索）
- **No Solution（没有解）**，但局部检查无法发现这一事实

> 因此，Arc Consistency 通常是嵌入在 Backtracking Search 内部作为一种 **Filter（过滤器）** 来使用。

---

## 5. Problem Structure（问题结构）

### 5.1 Independent Subproblems（独立子问题）

现实中的 CSP 通常可以分解成若干 **Disconnected Subproblems（互不相连的子问题）**（在 Constraint Graph 上是不同 Connected Components（连通分量））。

**示例**：Tasmania（塔斯马尼亚岛）在 Constraint Graph 上与澳大利亚大陆部分不相连，可独立求解。

**Efficiency Gain（效率提升）**：

- 不分解：复杂度约为 `O(dⁿ)`
- 若分解为若干规模为 `c` 的子问题：复杂度变为 `O((n/c) · dᶜ)` —— 对 `n` 为线性级

| 场景 | 所需时间 |
|------|----------|
| `n = 80, d = 2`，无分解 | 约 40 亿年 |
| `n = 80, d = 2, c = 20` | 约 0.4 秒 |

### 5.2 Tree-Structured CSPs（树结构 CSP）

> **定理**：若 Constraint Graph 是 **Acyclic Tree Structure（无环树结构）**，则该 CSP 可在 `O(nd²)` 时间内求解。

对比：
- 一般 CSP：Time Complexity（时间复杂度）`O(dⁿ)`（指数）
- Tree-Structured CSP：Time Complexity `O(nd²)`（多项式）

**Tree-Structured CSP Algorithm（树结构 CSP 的算法）**：
1. **Ordering（排序）**：选一个 Root（根结点），对变量排序，使每个结点的 Parent（父亲）排在它前面
2. **Bottom-Up Pruning（自底向上删值）**：从 `i = n` 到 `2`，对每条边应用 `RemoveInconsistent(Parent(Xᵢ), Xᵢ)`
3. **Top-Down Assignment（自顶向下赋值）**：从 `i = 1` 到 `n`，为 `Xᵢ` 赋一个与其 Parent 一致的值

整体 Time Complexity：`O(nd²)`

### 5.3 Cutset Conditioning（割集条件化）

当 Constraint Graph 中存在 Cycle（环）时：
1. 找到一个 **Cutset（割集）** —— 去掉这些变量后，Constraint Graph 变成树
2. Enumerate（枚举）Cutset 变量的所有可能赋值
3. 对于每一种 Cutset Assignment，求解对应的 Tree-Structured CSP

**Complexity（复杂度）**：`O(dᶜ · (n-c) · d²)`，其中 `c` 是 Cutset Size（割集大小）  
当 `c` 很小时，这种方法非常高效。

---

## 6. 小结：CSP 提升技巧

| 技术 | 类型 | 核心思想 |
|------|------|----------|
| Backtracking Search（回溯搜索） | Algorithm（算法） | DFS + Variable Commutativity（可交换性）+ Constraint Check（约束检查） |
| MRV（最少剩余值） | Ordering（排序） | 优先选择"最受限（Most Constrained）"的变量 |
| LCV（最少约束值） | Ordering（排序） | 优先选择"最不妨碍他人（Least Constraining）"的取值 |
| Forward Checking（前向检验） | Filtering（过滤） | 赋值后立刻从邻域中删去 Conflicting Values（冲突值） |
| Arc Consistency / AC-3（弧一致性） | Filtering（过滤） | 在整个图上传播约束，提前 Prune（剪枝） |
| Decomposition（分解） | Structure（结构） | 拆成多个 Independent Subproblems（独立子问题） |
| Tree-Structured Algorithm（树结构算法） | Structure（结构） | 对无环图在 `O(nd²)` 时间内求解 |
| Cutset Conditioning（割集条件化） | Structure（结构） | 通过固定小 Cutset，将有环图变成树结构 |

---

## 7. Complexity Overview（复杂度概览）

| Algorithm / Technique（算法 / 技术） | Time Complexity（时间复杂度） | 说明 |
|-------------|-----------|------|
| Naive Backtracking（朴素回溯） | `O(dⁿ)` | 没有任何改进 |
| MRV + LCV + Forward Checking | 实践中大幅加速 | 理论上难以精确界定上界 |
| AC-3（弧一致性） | `O(n²d³)` | 常用于 Preprocessing（预处理）或搜索中的过滤 |
| Tree-Structured CSP（树结构 CSP） | `O(nd²)` | 需要 Acyclic Constraint Graph（无环约束图） |
| Cutset Conditioning（割集条件化） | `O(dᶜ · (n-c)d²)` | `c` 为 Cutset Size（割集大小） |
