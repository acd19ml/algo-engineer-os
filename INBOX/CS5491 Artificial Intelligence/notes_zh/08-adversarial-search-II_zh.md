# 讲义 08 - Adversarial Search II（对抗搜索 II）：Expectimax & Utilities（期望极大与效用）

**课程**: CS5491: Artificial Intelligence  
**阅读**: RN 第 16.1–16.3 章

---

## 1. Uncertain Outcomes（不确定结果）：Worst Case vs. Average Case（最坏情况 vs. 平均情况）

| 方法 | 假设 | Node Type（结点类型） |
|------|------|----------|
| **Minimax** | 对手行为 **Optimal / Worst-Case（最优 / 最坏）** | MIN Node |
| **Expectimax** | 结果是 **Stochastic（随机的）** | Chance Node（随机结点） |

> **关键洞见**：Uncertainty（不确定性）并不总是来自对手的恶意，有时 Environment（环境）本身就是随机的。

---

## 2. 为什么结果会不确定（Why Uncertain Outcomes）？

| 来源 | 示例 |
|------|------|
| **Explicit Randomness（显式随机性）** | 掷骰子（Dice）、洗牌（Shuffling） |
| **Unpredictable Opponent（对手不可预测）** | Pac-Man 中鬼 Random Walk（随机走位） |
| **Action Failure / Noise（动作失败 / 噪声）** | 机器人 Wheel Slippage（车轮打滑） |

---

## 3. Expectimax Search（期望极大搜索）

### 3.1 结点类型与计算（Node Types & Computation）

| Node Type（结点类型） | 计算规则 |
|----------|----------|
| **MAX Node（MAX 结点）** | 与 Minimax 相同：`V(s) = max_{s'} V(s')` |
| **Chance Node（随机结点）** | `V(s) = Σ P(outcome) · V(outcome)`（Weighted Average，加权平均） |
| **Terminal Node（终局结点）** | `V(s)` = 给定 Utility（效用） |

### 3.2 算法

```text
function EXPECTIMAX(state, depth):
    if TERMINAL(state): return UTILITY(state)
    if MAX node:
        return max over successors: EXPECTIMAX(s', depth-1)
    if CHANCE node:
        return Σ P(s') * EXPECTIMAX(s', depth-1)
```

### 3.3 示例计算

```text
Chance Node：V = (1/2) × 8 + (1/3) × 24 + (1/6) × (−12)
           = 4 + 8 − 2 = 10
```

### 3.4 Expectimax Pruning（Expectimax 剪枝）

- 比 Minimax 中的 α-β Pruning（剪枝）要困难得多
- 只有在同时有 **Probability Bounds（概率上界 / 下界）** 和 **Value Bounds（值界）** 的情况下才能安全剪枝

---

## 4. Probability Basics（概率基础回顾）

### Random Variables & Distributions（随机变量与分布）

- **Random Variable（随机变量）**：表示一个结果未知的量
- **Probability Distribution（概率分布）**：为所有可能结果分配概率，且总和为 1

**示例**：
- `P(T=none) = 0.25`, `P(T=mild) = 0.50`, `P(T=heavy) = 0.25`

### 基本规律

- `P(outcome) ≥ 0` 对所有结果
- `Σ P(outcome) = 1`
- 在有 Evidence（证据）时更新：如 `P(T=heavy | Hour=8am) = 0.60`

### Expected Value（期望值）

```text
E[f(X)] = Σ P(X=x) · f(x)
```

即在给定 Probability Distribution 下的 **Weighted Average（加权平均）**。

---

## 5. Expectimax 中用什么概率？

在 Expectimax 中，需要对 Environment / Opponent 指定 Probability Model（概率模型）：

| Model Type（模型类型） | 示例 |
|----------|------|
| **Uniform Distribution Model（均匀分布模型）** | 掷公平骰子 —— 各面等可能（Equally Likely） |
| **Learned Model（学习得到的模型）** | 根据对手历史行为训练的 Policy Model（策略模型） |
| **Adversarial Model（对抗性模型）** | 假设对手 Worst-Case Behavior（最坏行为）（→ Minimax 情形） |

> **Chance Node（随机结点）** 可统一表示所有**不受智能体控制的因素（Uncontrolled Factors）**（环境随机性或对手行为）。

---

## 6. Modeling Assumptions（建模假设）的风险

| 错误类型 | 描述 | 后果 |
|----------|------|------|
| **Dangerous Optimism（危险的乐观）** | 把对手当作 Random（随机），却实际上是 Adversarial（对抗性）的 | 容易被对手 Exploit（利用） |
| **Dangerous Pessimism（危险的悲观）** | 把 Random Environment（随机环境）当作 Adversarial | 行为过于 Conservative（保守），浪费机会 |

### Pac-Man 实验结果（示意）

| Ghost Type（鬼类型） | Minimax Pac-Man | Expectimax Pac-Man |
|--------|-----------------|--------------------|
| **Adversarial Ghost（对抗型鬼）** | 5/5 胜，得分约 483 | 1/5 胜，得分约 -303 |
| **Random Ghost（随机鬼）** | 5/5 胜，得分约 493 | 5/5 胜，得分约 **503** |

> **经验教训**：Model 必须尽量贴近现实。Model Error（模型错误）时，即便算法本身正确，也可能表现灾难性。

---

## 7. Mixed Games：Expectiminimax（混合型游戏）

某些博弈同时具有 Adversarial（对抗性）和 Stochastic（随机性）（例如 **Backgammon（双陆棋）**）：
- Environment 相当于一个额外的 **Random Player（随机玩家）**
- 搜索树中同时存在 MAX、MIN、CHANCE 三类结点

**Backgammon 特点**：
- 骰子有 21 种结果 × 每个状态约 20 种 Legal Moves（合法走法）→ `b ≈ 420`
- 深度 2 的树：`20 × (21 × 20)³ ≈ 1.2 × 10⁹` 个结点
- 随着深度增加，到达某个具体结点的 Probability（概率）急剧下降 → 适度 Depth Cutoff（截断深度）的影响相对较小

**TDGammon**：  
使用深度 2 的搜索 + 强大的 Evaluation Function（评估函数）+ **Reinforcement Learning（强化学习）** 训练 → 达到世界冠军水平，是首个在正式比赛中夺冠的 AI 系统。

---

## 8. Utilities（效用）

### 8.1 什么是 Utility（效用）？

- 把 **World Outcomes（世界结果 / 状态）映射到实数** 的函数
- 用于刻画智能体对不同结果的 **Preference（偏好）**

### 8.2 效用从何而来？

- 简单游戏：`+1 / -1`（胜 / 负）
- 复杂领域：需要精心设计 Reward / Utility Function（奖励 / 效用函数）
- 数学上有定理说明：只要 Preference（偏好）满足若干 "Rationality Axioms（理性公理）"，就可以用 Utility Function 表示

### 8.3 Utility Scale（效用的刻度）

| Search Type（搜索类型） | Scale 是否重要？ | 原因 |
|----------|----------------|------|
| **Minimax** | 不重要 | 只依赖于 Ordering（大小关系），单调变换不改变最优策略 |
| **Expectimax** | **重要** | 计算 Expected Value（期望值）时会用到数值大小 |

> 对于 Expectimax，若把所有效用乘以常数，只是把期望整体放大 / 缩小，不改变最优动作；但若做 **Non-Linear Transformation（非线性变换）**，则可能改变最优选择。

### 8.4 Maximum Expected Utility Principle（最大期望效用原则）

> **理性智能体应当选择能最大化其 Expected Utility（期望效用）的行动，前提是给定当前的 Belief（信念 / 概率模型）。**

需要回答的问题：
- Utility Function 应如何设计或学习？
- 为什么要用 Expected Value 而不是其它标尺？（来自一组关于理性偏好的 Axioms（公理））
- 若行为无法用任何 Utility Function 解释，则意味着 Preference（偏好）是 Irrational（不理性）的。

### 8.5 为什么要"硬编码（Hard-code）"效用？

- 不应让智能体自己随意定义效用，否则可能 **Reward Hacking（外道优化）**
- 也不应直接规定 Behavior Rules（行为规则）（太死板）
- 更推荐：**人类设计 / 学习一个合理的 Utility Function，让 "Rational Behavior（理性行为）" 自然产生**

---

## 9. 小结：博弈中的搜索算法

| 场景 | 算法 | 关键特性 |
|------|------|----------|
| Deterministic, Two-Player, Zero-Sum（决定性、双人、零和） | **Minimax** | 对手被视为 Perfectly Rational Adversary（完全理性对抗者） |
| + Pruning（剪枝） | **Alpha-Beta** | 跳过不影响根决策的分支 |
| Stochastic Environment（随机环境） | **Expectimax** | 对 Random Outcomes（随机结果）取期望值 |
| Mixed（Adversarial + Stochastic，混合） | **Expectiminimax** | 同时包含 MAX / MIN / CHANCE 结点 |
| Limited Resources（资源有限） | **Depth-Limited + Evaluation Function（深度限制 + 评估函数）** | 及早截断，用 Heuristic Value 近似 |

---

## 10. 关键公式

| 公式 | 含义 |
|------|------|
| `V(s) = max_{s'} V(s')` | MAX Node 的取值 |
| `V(s) = min_{s'} V(s')` | MIN Node 的取值 |
| `V(s) = Σ P(s') · V(s')` | CHANCE Node（Expectimax）的取值 |
| `E[U] = Σ P(outcome) · U(outcome)` | Expected Utility（期望效用） |
