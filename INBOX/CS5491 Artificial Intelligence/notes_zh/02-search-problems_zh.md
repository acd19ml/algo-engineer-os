# 讲义 02 - 搜索问题（Search Problems）

**课程**: CS5491: Artificial Intelligence  
**阅读**: RN 第 3.1–3.4 章

---

## 1. 回顾：Rational Agent（理性智能体）

- **Agent（智能体）**：能 **Perceive（感知）** 并 **Act（采取行动）** 的实体
- **Rational Agent（理性智能体）**：选择能最大化其（期望）效用的行为
- Percepts（感知）、Environment（环境）和 Action Space（动作空间）的特性共同决定应当采用哪种 AI 技术

### 关于理性智能体的关键问题

| 问题 | 回答 |
|------|------|
| 理性智能体是 Omniscient（全知）的吗？ | **不是** —— 受限于它能感知到的信息 |
| 理性智能体有 Clairvoyant（预知能力）吗？ | **没有** —— 不知道环境 Dynamics（动力学）的全部细节 |
| 理性智能体会 Explore & Learn（探索和学习）吗？ | **会** —— 在未知环境中这是必须的 |

> **结论**：理性智能体不一定总是"成功"，但必须是 **Autonomous（自治）的**。

---

## 2. PEAS 框架

**PEAS** = **P**erformance Measure（性能度量） · **E**nvironment（环境） · **A**ctuators（执行器） · **S**ensors（传感器）

### 示例 1：Pac-Man 智能体

| PEAS 组件 | 说明 |
|-----------|------|
| **Performance Measure（性能度量）** | 每个时间步 -1；吃到食物 +10；胜利 +500；死亡 -500；撞到害怕的鬼 +200 |
| **Environment（环境）** | Pac-Man 游戏 Dynamics（动力学）+ 鬼的行为 |
| **Actuators（执行器）** | 向北、向西、向东、向南、原地不动（Stop） |
| **Sensors（传感器）** | 整个游戏状态完全可见 |

### 示例 2：RoboTaxi（无人出租车）智能体

| PEAS 组件 | 说明 |
|-----------|------|
| **Performance Measure（性能度量）** | 收入、乘客满意度、车辆成本、罚单、保险等 |
| **Environment（环境）** | 道路、其他司机、乘客、交通规则等 |
| **Actuators（执行器）** | 方向盘、刹车、油门、显示屏 / 扬声器 |
| **Sensors（传感器）** | 摄像头（Camera）、LiDAR、雷达（Radar）、超声波（Ultrasonic）、加速度计（Accelerometer）、麦克风等 |

---

## 3. 环境分类（Environment Types）

| 属性 | Pac-Man | RoboTaxi |
|------|---------|----------|
| 可观测性 | **Fully Observable（完全可观测）** | **Partially Observable（部分可观测）** |
| 智能体数量 | **Multi-Agent（多智能体）** | **Multi-Agent（多智能体）** |
| 决定性 | **Deterministic（确定性）** | **Stochastic（随机性）** |
| 动态性 | **Static（静态）** | **Dynamic（动态）** |
| 空间 | **Discrete（离散）** | **Continuous（连续）** |

### 定义

- **Fully Observable（完全可观测）**：智能体在任意时刻都能看到完整状态
- **Partially Observable（部分可观测）**：智能体只能获得有限 / 含噪的观测
- **Deterministic（确定性）**：给定状态和动作，结果是唯一确定的
- **Stochastic（随机性）**：动作结果存在不确定性
- **Static（静态）**：智能体思考期间环境不会变化
- **Dynamic（动态）**：即使智能体不动，环境也可能发生变化
- **Discrete（离散）**：状态和动作集合是有限的
- **Continuous（连续）**：状态 / 动作可以取连续实数

---

## 4. Agent Types（智能体类型）

### 4.1 Reflex Agent（反射型智能体）

- 仅根据**当前观测**（以及可能的少量记忆）来选择动作
- 可以维护一个对世界当前状态的 Internal Model（内部模型）
- **不会考虑未来后果**，不显式规划
- 关注世界现在**是什么样**
- 问题：*反射型智能体能是理性的吗？*
  - 只有在环境**完全可观测且确定性**时才可能是理性的

### 4.2 Planning Agent（规划型智能体）

- 决策基于对**行动未来后果**的预测
- 需要一个 **Transition Model（状态转移模型）**：动作如何改变世界
- 需要明确的 **Goal（目标）**
- 关注世界将来**会变成什么样**

#### Deliberation（深思熟虑程度）的谱系

| 方法 | 描述 |
|------|------|
| **Offline Planning（离线规划）** | 先生成一条完整、最优的计划，再执行 |
| **Online Planning（在线规划）** | 先生成简单 / 贪心计划，边执行边 **Replan（重新规划）** |

---

## 5. Search Problems（搜索问题）

### 5.1 形式化定义

一个搜索问题由以下部分构成：

| 组件 | 描述 |
|------|------|
| **State Space（状态空间）** | 所有可能状态的集合 |
| **Successor Function（后继函数）** | 给定当前状态 → 返回若干三元组 `(action, next_state, cost)` |
| **Start State（起始状态）** | 智能体的初始状态 |
| **Goal Test（目标测试）** | 判断某个状态是否为目标状态的函数 |

> **Solution（解）**：一串动作序列（即一条 **Plan（计划）**），能把起始状态转换为某个目标状态。

### 5.2 关键洞见：搜索问题是"模型"

- 搜索问题是对真实问题的 **Abstract Model（抽象模型）**
- 我们有意丢弃与规划无关的细节，只保留与决策相关的部分

---

## 6. 示例：在罗马尼亚旅行

**目标**：从 Arad 城市出发，到达 Bucharest

| 组件 | 取值 |
|------|------|
| **State Space（状态空间）** | 罗马尼亚各个城市 |
| **Successor Function（后继函数）** | 城市之间的道路（代价 = 距离） |
| **Start State（起始状态）** | Arad |
| **Goal Test（目标测试）** | 当前城市是否为 Bucharest？ |

- 解是一条**城市序列**，构成从 Arad 到 Bucharest 的最短 / 最优路径。

---

## 7. World State vs. Search State（世界状态 vs. 搜索状态）

| 概念 | 描述 |
|------|------|
| **World State（世界状态）** | 包含环境的**所有**细节 |
| **Search State（搜索状态）** | 只保留为规划决策**必要**的细节 |

### 示例：Pac-Man 的状态空间

#### 问题 1：Path Planning（路径规划，只要到达某个位置）

| 组件 | 取值 |
|------|------|
| State（状态） | 位置 `(x, y)` |
| Actions（动作） | N, E, W, S |
| Successor（后继） | 更新位置 |
| Goal Test（目标测试） | `(x, y) == END` |

#### 问题 2：Eat-All-Dots（吃完所有豆子）

| 组件 | 取值 |
|------|------|
| State（状态） | `(x, y)` + 每个豆子是否还存在的 Boolean（布尔量） |
| Actions（动作） | N, E, W, S |
| Successor（后继） | 更新位置 + 更新各豆子的布尔标记 |
| Goal Test（目标测试） | 所有豆子对应的布尔值都为 `False` |

---

## 8. State Space Size（搜索空间大小）

以 Pac-Man 为例的**世界状态变量（World State Variables）**：

| 变量 | 数量 |
|------|------|
| 智能体位置数（Agent Positions） | 120 |
| 食物（豆子）数量（Food/Dots） | 30 个 |
| 鬼的位置数（Ghost Positions） | 12 |
| 智能体朝向（Agent Direction） | 4（NEWS） |

**State Space Size（状态空间大小）**：

| 问题 | 公式 | 含义 |
|------|------|------|
| 全部世界状态 | `120 × 2^30 × 12 × 4` | 天文数字 |
| 仅路径规划（Path Planning only） | `120` | 只考虑位置 |
| 吃完所有豆子（Eat-All-Dots） | `120 × 2^30` | 位置 + 还剩哪些豆子 |

> **关键洞见**：合理的 State Abstraction（状态抽象）可以极大缩小搜索空间。只保留会影响后续决策的变量。

---

## 9. 小结

| 概念 | 要点 |
|------|------|
| Rational Agent（理性智能体） | 最大化 Expected Utility（期望效用）；Autonomous（自治）但不全知 |
| PEAS | 用于规范化描述一个智能体设计的框架 |
| Reflex Agent（反射型智能体） | 只对当前状态做出反应，不做未来规划 |
| Planning Agent（规划型智能体） | 利用 Transition Model（状态转移模型）预测行动后果并规划 |
| Search Problem（搜索问题） | （State Space, Successor Function, Start State, Goal Test）四元组 |
| Solution（解） | 从 Start State（起始状态）到 Goal State（目标状态）的一串动作 |
| State Abstraction（状态抽象） | 丢弃与规划无关的细节，减少状态空间规模 |

---

## 10. 阅读

- **本次讲义**：RN 第 3.1–3.4 章  
- **下一次讲义**：RN 第 3.1–3.4 章（续 —— Uninformed Search（无信息搜索）算法）
