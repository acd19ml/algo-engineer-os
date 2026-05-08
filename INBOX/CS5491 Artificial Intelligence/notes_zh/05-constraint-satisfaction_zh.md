# 讲义 05 - Constraint Satisfaction Problems, CSP（约束满足问题）

**课程**: CS5491: Artificial Intelligence  
**阅读**: RN 第 6 章

---

## 1. Search vs. CSP（搜索 vs. CSP）：两种思维模式

| 模式 | 关注点 | 路径是否重要？ |
|------|--------|----------------|
| **Planning / Search（规划 / 搜索）** | 通过一系列动作到达目标 | **是** —— Path Cost（路径长度 / 代价）重要 |
| **Identification / CSP（识别 / CSP）** | 找到一个满足所有约束的 Variable Assignment（变量赋值） | **否** —— 只关心最终赋值是否可行 |

> 典型假设：Single Agent（单智能体）、Deterministic（确定性）动作、Fully Observable（完全可观测）、Discrete State Space（离散状态空间）。

---

## 2. 什么是 CSP？

### General Search Problem（一般搜索问题）

- State（状态）= 任意"黑盒"数据结构
- Goal Test（目标测试）= 任意布尔函数
- Successor Function（后继函数）= 任意函数

### Constraint Satisfaction Problems, CSP（约束满足问题）

是一类结构化的搜索问题：
- **Variables（变量）**：`X₁, X₂, ..., Xₙ`
- **Domains（取值域）**：每个 `Xᵢ` 的取值来自域 `Dᵢ`
- **Constraints（约束）**：对某些变量子集给出允许的 **Value Combinations（取值组合）**
- **Goal（目标）**：找到一个 **Complete Assignment（完整赋值）**，使得**所有约束都被满足**

> 由于结构明确，CSP 可以使用通用而强大的算法来利用 Problem Structure（问题结构）。

---

## 3. CSP 的形式化

| 组件 | 描述 |
|------|------|
| **States（状态）** | Partial Assignment（对变量的部分赋值） |
| **Initial State（初始状态）** | Empty Assignment（空赋值）`{}` |
| **Successor Function（后继函数）** | 给一个 Unassigned Variable（未赋值变量）赋上一个值 |
| **Goal Test（目标测试）** | 赋值是 Complete（完整）的 **且** 满足所有 Constraints（约束） |

---

## 4. 经典示例：Map Coloring（地图着色，澳大利亚）

| 组件 | 内容 |
|------|------|
| **Variables（变量）** | WA, NT, Q, NSW, V, SA, T |
| **Domains（取值域）** | `{red, green, blue}` |
| **Constraints（约束）** | Adjacent Regions（相邻区域）颜色必须不同 |

**约束的两种表达方式**：
- **Implicit（隐式）**：`WA ≠ NT`
- **Explicit（显式）**：`(WA, NT) ∈ {(red,green), (red,blue), (green,red), ...}`

**示例解（Example Solution）**：
```text
{WA=red, NT=green, Q=red, NSW=green, V=red, SA=blue, T=green}
```

---

## 5. Constraint Graph（约束图）

- **Binary CSP（二元 CSP）**：每个 Constraint（约束）只涉及**两个**变量
- **Constraint Graph（约束图）**：结点 = 变量，边 = 存在约束

> 约束图的结构可以揭示 **Independent Subproblems（相互独立的子问题）**（例如 Tasmania（塔斯马尼亚）与大陆部分相互独立）。

---

## 6. 示例：N-Queens Problem（N 皇后问题）

### 形式化 1（Grid Representation，网格表示）

- 变量：`Xᵢⱼ ∈ {0, 1}`（是否在网格 (i, j) 放皇后）
- 约束：同一 Row（行）、同一 Column（列）、同一 Diagonal（对角线）上不能有两个皇后；总皇后数为 N

### 形式化 2（更紧凑表示）

- 变量：`Qₖ` = 第 k 行皇后所在的列编号
- 取值域：`{1, 2, ..., N}`
- 约束：对所有 `(i, j)`，任意两皇后 **Non-Attacking（互不攻击）**

---

## 7. CSP 的类型

### Variable Types（变量类型）

| 类型 | 示例 | 说明 |
|------|------|------|
| **Finite Discrete（有限离散）** | Map Coloring（地图着色）、Boolean SAT（布尔可满足性） | `O(dⁿ)` 种赋值；SAT 是 NP-Complete（NP 完全） |
| **Infinite Discrete（无限离散）** | 作业调度中的整数时间 | 线性情况可解；非线性可能不可判定 |
| **Continuous（连续）** | Telescope Scheduling（望远镜排程）、Resource Allocation（资源分配） | Linear Case（线性情形）可用 Linear Programming（线性规划）在多项式时间内求解 |

### Constraint Types（约束类型）

| 类型 | 描述 | 示例 |
|------|------|------|
| **Unary（一元）** | 限制单个变量 | `SA = green` |
| **Binary（二元）** | 限制两个变量的关系 | `SA ≠ WA` |
| **Higher-order（高阶）** | 涉及 3 个及以上变量 | Cryptarithmetic（字谜）、Sudoku（数独）等 |
| **Soft / Preference（软约束 / 偏好）** | 包含偏好及代价 | 偏好 red 胜于 green → 转为 Constraint Optimization Problem（约束优化问题） |

---

## 8. CSP 的实际应用

- Scheduling（排程，会议时间安排、课程时间表）
- Assignment（分配，谁教哪门课，谁做哪个任务）
- Hardware Configuration（硬件配置）
- Transportation / Flight Scheduling（交通 / 航班排程）
- Factory Production Scheduling（工厂生产排程）
- Circuit Layout（电路布局）
- Fault Diagnosis（故障诊断）

---

## 9. 使用常规搜索来解 CSP？

一种朴素做法：
- **BFS（广度优先搜索）**：会穷举许多变量赋值的不同顺序 → 大量 Equivalent States（等价状态）被重复访问
- **DFS（深度优先搜索）**：问题类似

**问题**：这些方法效率非常低，大量时间浪费在不同顺序的 **Equivalent Assignments（等价赋值）** 上。

> 这就是为什么需要专门针对 CSP 的算法（如 Backtracking Search（回溯搜索）、Forward Checking（前向检验）、Arc Consistency（弧一致性）等）。

---

## 10. 展望

下一讲（Lecture 06）将进一步介绍在 CSP 上的 **Backtracking Search（回溯搜索）及其改进**：
- Filtering（过滤）：Forward Checking（前向检验）、Arc Consistency（弧一致性）
- Ordering（变量 / 取值排序）：MRV（最少剩余值）、LCV（最少约束值）
- Problem Structure（利用问题结构）
