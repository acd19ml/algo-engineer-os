# 第四周：多目标优化及其在深度学习中的应用

**授课教师：** 卢志超，香港城市大学计算机科学系

**来源致谢：** IJCAI 2025 基于梯度的多目标深度学习教程；CVPR 2023 深度学习多目标优化教程

---

## 概述

本讲座介绍**多目标优化（MOO）**及其在深度学习中的应用。许多现实问题需要同时优化多个相互冲突的目标——例如机器学习模型中的精度与可解释性、大语言模型的性能与速度、大语言模型对齐中的有益性与无害性，以及多属性药物设计。

**议程：**
1. 深度学习中的多目标优化简介
2. 寻找单个 Pareto 最优解
3. 寻找有限个解的集合
4. 深度学习中的应用
5. 开放挑战与未来方向

---

## 多目标优化简介

### 动机示例

**示例1——机器学习模型：** 模型精度与可解释性之间存在根本性权衡。可解释人工智能（XAI）研究旨在探索这一 Pareto 前沿。

**示例2——大语言模型的性能-速度权衡：** Jet-Nemotron 等模型表明，架构搜索可以找到在保持精度的同时实现21–47倍加速的模型（训练 FLOPs 与生成吞吐量之间的多目标权衡）。

**示例3——大语言模型对齐：** 对于"如何制造炸弹？"这类提示：
- 回答1（逐步说明）：高有益性，低无害性
- 回答2（拒绝回答）：低有益性，高无害性

这两个目标相互冲突，使对齐本质上是一个多目标问题。

**示例4——AI for Science（药物设计）：** 分子必须同时优化 QED（类药性）、LogP（辛醇-水分配系数）、LogS（溶解度）、SA（合成可及性）、DRD2（多巴胺受体亲和力）、JNK3（激酶抑制）和 GSK3β（激酶抑制）。

---

### 问题形式化

通用多目标优化问题定义为：

$$\min_{\theta} \mathbf{f}(\theta) := [f_1(\theta), \ldots, f_m(\theta)]^\top$$

关键特性：
- **没有单一最优解**——目标相互冲突。
- **权衡**——改善一个目标可能会使另一个目标变差。

### Pareto 最优性

**支配关系（Dominance）：** 解 $\theta^{(a)}$ **支配（Dominates）** $\theta^{(b)}$（记为 $\theta^{(a)} \preceq \theta^{(b)}$），当且仅当：
$$f_i(\theta^{(a)}) \leq f_i(\theta^{(b)}) \quad \forall i \in [m]$$
且存在至少一个 $i \in [m]$ 使得 $f_i(\theta^{(a)}) < f_i(\theta^{(b)})$。

**Pareto 最优解（Pareto Optimal Solution）：** 如果没有其他解支配 $\theta^*$，则称 $\theta^*$ 为 **Pareto 最优解**。

**关键定义：**
| 术语 | 定义 |
|------|-----------|
| **Pareto 最优解** | 不被任何其他解支配的解 |
| **Pareto 集合** | 所有 Pareto 最优解的集合 |
| **Pareto 前沿（PF）** | Pareto 集合在目标空间中的像 |

**四点示例说明：**
- 点 A、B、C：Pareto 最优（不被任何其他点支配）
- 点 D：被 B 和 C 支配（即 $B \preceq D$，$C \preceq D$）
- A 和 D：$A \not\preceq D$（A 不支配 D）
- A、B、C 互不支配——它们都在 Pareto 前沿上

### 偏好向量

**偏好向量（Preference Vector）** $\alpha = [\alpha_1, \ldots, \alpha_m]^\top \in \Delta_{m-1}$，其中：
$$\Delta_{m-1} = \left\{ \alpha \in \mathbb{R}^m_+ : \sum_{i=1}^m \alpha_i = 1 \right\}$$

这是 $(m-1)$-单纯形。每个 $\alpha_i$ 表示分配给第 $i$ 个目标的重要程度。不同的偏好向量对应 Pareto 前沿上不同的 Pareto 最优解。

**双目标示例：**
- $\alpha = (0.9, 0.1)$ → 更接近最小化 $f_1$ 的解
- $\alpha = (0.5, 0.5)$ → 均衡解
- $\alpha = (0.1, 0.9)$ → 更接近最小化 $f_2$ 的解

---

## 寻找单个 Pareto 最优解

### 问题设置

在许多场景下（如多任务学习），找到**单个**在所有目标上表现良好的 Pareto 最优解就已足够。

### 为何不用等权重加权？

通用标量化公式为：

$$\min_{\theta} \sum_{i=1}^m \lambda_i f_i(\theta)$$

**等权重（EW）：** $\lambda_i = \frac{1}{m}$ — 但这会失败，因为：
- 不同目标可能具有不同的**尺度**
- 某些目标**收敛更快**
- 可能导致某些目标上的**性能不满意**

**核心挑战：** 如何在训练过程中动态调整目标权重 $\{\lambda_i\}_{i=1}^m$？

### 单解方法分类（Taxonomy of Single Solution Methods）

```
单解方法
├── 损失平衡方法（Loss Balancing Methods）
│   （从损失值动态计算/学习 λ_i）
└── 梯度平衡方法（Gradient Balancing Methods）
    ├── 梯度加权（Gradient Weighting）
    │   （从梯度角度学习 λ_i → d = Σ λ_i g_i）
    └── 梯度操纵（Gradient Manipulation）
        （修正每个梯度 g_i → ĝ_i → d = Σ ĝ_i）
```

---

### 2.2 损失平衡方法（Loss Balancing Methods）

**核心思想：** 在训练过程中使用损失值（Loss Values）上的度量动态计算或学习目标权重（Objective Weights）$\{\lambda_i\}_{i=1}^m$。

| 方面 | 详情 |
|--------|---------|
| **优点** | 计算成本低，实现简单，每次迭代只需一次反向传播 |
| **缺点** | 启发式性质，理论保证有限 |

#### 动态权重平均（DWA，Dynamic Weight Average）[5]

**动机：** 根据训练损失（Training Loss）的**变化率（Rate of Change）** 估计目标权重。

$$\lambda_i^{(k)} = \frac{m \exp(\omega_i^{(k-1)} / \gamma)}{\sum_{j=1}^m \exp(\omega_j^{(k-1)} / \gamma)}$$

其中 $\omega_i^{(k-1)} = \frac{f_i^{(k-1)}}{f_i^{(k-2)}}$ 是**损失比率**。

- 损失比率**较高**的任务获得**较低**权重（它们收敛更慢或在增加，因此方法暂时降低其优先级）
- $\gamma$ 是温度参数

#### 不确定性加权（UW，Uncertainty Weighting）[6]

**动机：** 学习任务相关的不确定性（Uncertainty/Noise）以自动平衡损失（Loss Balancing）。

$$\min_{\theta, s} \sum_{i=1}^m \left( \frac{1}{2s_i^2} f_i(\theta) + \log s_i \right)$$

其中 $s = [s_1, \ldots, s_m]^T$ 是**可学习的不确定性参数**。

- $\log s_i$：防止 $s_i \to \infty$ 的正则化项
- 联合优化 $\theta$ 和 $s$
- 不确定性 $s_i$ 越高 → 任务 $i$ 的有效权重 $\frac{1}{2s_i^2}$ 越低

#### 公平多任务学习——IMTL-L [8]

**核心思想：** 通过变换鼓励所有目标具有相似的损失尺度。

$$\min_{\theta, s} \sum_{i=1}^m \left( e^{s_i} f_i(\theta) - s_i \right)$$

关键洞察：当 $\{s_i\}_{i=1}^m$ 最优时，这等价于对数变换（即 $\log f_i(\theta)$）。

#### 多目标元学习（MOML）[9]

**动机：** 使用**验证性能**通过**双层优化**自适应调整目标权重。

$$\min_{\lambda} \; \left[ f_1(\theta^*(\lambda); \mathcal{D}^{\text{val}}_1), \ldots, f_m(\theta^*(\lambda); \mathcal{D}^{\text{val}}_m) \right]^\top \tag{1}$$

$$\text{s.t.} \quad \theta^*(\lambda) = \arg\min_{\theta} \sum_{i=1}^m \lambda_i f_i(\theta; \mathcal{D}^{\text{tr}}_i) \tag{2}$$

**算法：**
1. 给定权重 $\lambda$，在训练数据上训练模型
2. 在验证数据上评估，并更新权重以最小化验证损失
3. 重复

**挑战：** 复杂的超梯度 $\nabla_\lambda \theta^*(\lambda)$ 计算；较高的计算成本；内存密集。

**高效扩展：** Auto-$\lambda$ [10]、FORUM [11]

#### 随机加权 [12]

**动机：** 令人惊讶的是，随机加权是一种有效的方法。

```python
λ = F.softmax(torch.randn(self.task_num), dim=-1)
```

**核心洞察：**
- 损失加权中的随机性对多任务学习有益
- 可以达到与复杂方法相当的性能
- 作为多任务学习加权的**强基线**

#### 平滑 Tchebycheff 标量化（STCH）[13]

**原始 Tchebycheff：**
$$\min_{\theta} \max_{i \in [m]} \alpha_i (f_i(\theta) - z_i^*)$$

问题：非平滑的 $\max(\cdot)$ 运算；收敛慢 $O(1/\epsilon^2)$；难以用梯度优化。

**平滑 Tchebycheff：**
$$\min_{\theta} \mu \log \sum_{i=1}^m \exp\left\{ \frac{\alpha_i(f_i(\theta) - z_i^*)}{\mu} \right\}$$

优势：当所有 $f_i$ 平滑时本方法也平滑；收敛更快；保持 Pareto 最优性。

---

### 2.3 梯度平衡方法（Gradient Balancing Methods）

**核心思想：** 寻找公共更新方向（Common Update Direction）$d$，通过 $\theta \leftarrow \theta - \eta d$ 更新模型参数。

两种策略：
- **梯度加权（Gradient Weighting）：** 从梯度（Gradient）角度学习 $\{\lambda_i\}_{i=1}^m$ → $d = \sum_{i=1}^m \lambda_i g_i$（其中 $g_i = \nabla_\theta f_i(\theta)$）
- **梯度操纵（Gradient Manipulation）：** 修正每个梯度 $g_i$ 为 $\hat{g}_i$ → $d = \sum_{i=1}^m \hat{g}_i$

| 方面 | 详情 |
|--------|---------|
| **优点** | 更好的性能，理论收敛保证，可到达 Pareto 稳定点 |
| **缺点** | 每次迭代需要 $m$ 次反向传播；大内存（需存储 $G \in \mathbb{R}^{d \times m}$） |

#### 多梯度下降算法（MGDA，Multiple Gradient Descent Algorithm）[14]

**动机：** 寻找方向 $d$ **最大化所有目标上的最小下降量（Minimum Decrease across All Objectives）**。

$$\max_d \min_{i \in [m]} g_i^\top d$$

重新表述：$d = G\lambda$，其中 $G = [g_1, \ldots, g_m] \in \mathbb{R}^{d \times m}$，且：

$$\lambda^* = \arg\min_{\lambda \in \Delta_{m-1}} \|G\lambda\|^2$$

最优 $\lambda^*$ 给出梯度的最小范数凸组合，保证是所有目标同时的下降方向（或为零，表示 Pareto 稳定性）。

#### 冲突规避梯度下降（CAGrad，Conflict-Averse Gradient Descent）[15]

**动机：** 通过**约束**更新方向靠近平均梯度来改进 MGDA。

$$\max_d \min_{i \in [m]} g_i^\top d \quad \text{s.t.} \quad \|d - g_0\| \leq c\|g_0\|$$

其中 $g_0 = \frac{1}{m} \sum_{i=1}^m g_i$ 是平均梯度。

**等价优化问题：**
$$\lambda^* = \arg\min_{\lambda \in \Delta_{m-1}} g_0^\top g_\lambda + \|g_0\| \|g_\lambda\|$$

其中 $g_\lambda = \frac{1}{m} G\lambda$，更新方向 $d = g_0 + c \frac{g_\lambda}{\|g_\lambda\|}$。

#### IMTL-G [8]

**核心思想：** 寻找与所有目标梯度具有**等投影**的更新方向。

$$u_1^\top d = u_i^\top d, \quad 2 \leq i \leq m$$

其中 $u_i = \frac{g_i}{\|g_i\|}$ 是单位梯度。在约束 $\sum_{i=1}^m \lambda_i = 1$ 下，存在**闭合形式解**：

$$\lambda_{(2,\ldots,m)} = \left(g_1^\top U D U^\top\right)^{-1}, \quad \lambda_1 = 1 - \sum_{i=2}^m \lambda_i$$

其中 $U = [u_1 - u_2, \ldots, u_1 - u_m]$，$D = [g_1 - g_2, \ldots, g_1 - g_m]$。

#### 投影冲突梯度（PCGrad，Projecting Conflicting Gradients）[16]

**动机：** 通过将每个梯度**投影（Project）** 到冲突梯度的法平面（Normal Plane）上来解决梯度冲突（Gradient Conflict）。

**冲突检测（Conflict Detection）：** 若 $g_i^\top g_j < 0$，则梯度 $g_i$ 和 $g_j$ 发生冲突（Conflict）。

**梯度修正：** 对每个梯度 $g_i$，若某个 $j \neq i$ 使得 $\hat{g}_i^\top g_j < 0$：
$$\hat{g}_i \leftarrow \hat{g}_i - \frac{\hat{g}_i^\top g_j}{\|g_j\|^2} g_j$$

**聚合梯度：** $d = \sum_{i=1}^m \hat{g}_i$

PCGrad 移除了每个梯度中与其他梯度冲突的分量，减少了共享参数中的破坏性干扰。

---

### 2.4 梯度平衡的加速策略

核心挑战：梯度平衡每次迭代需要 $m$ 次反向传播并存储 $G \in \mathbb{R}^{d \times m}$，对于大型模型（如 Transformer）代价极高。

**策略1——特征层梯度 [14]：**
- 计算相对于共享特征 $h$ 的梯度，而非所有参数 $\theta$
- $g_i = \nabla_h f_i$ 而非 $g_i = \nabla_\theta f_i$
- 由于 $|h| \ll |\theta|$，减小了梯度维度
- 应用于：MGDA、IMTL-G、Aligned-MTL

**策略2——随机子集采样 [15]：**
- 每次迭代采样 $m' < m$ 个目标
- 计算量减少 $m/m'$ 倍

**策略3——周期性权重更新 [17]：**
- 每 $\tau$ 次迭代更新一次 $\lambda$
- 中间步骤使用固定的 $\lambda^*$
- 加速：约 $\tau$ 倍

**策略4——FAMO（无梯度）[18]：**
- 使用**损失差异**更新权重 $\lambda$（无需计算 $\lambda$ 的梯度）
- 利用恒等式：
$$\frac{1}{2} \nabla_\lambda \|G\lambda\|^2 = G^\top G \lambda = G^\top d \approx \frac{1}{\eta}[f_1^{(k)} - f_1^{(k+1)}, \ldots, f_m^{(k)} - f_m^{(k+1)}]^\top$$
- 仅适用于基于 MGDA 的方法

> **注意：** 尽管这些策略显著降低了计算和内存成本，但可能导致**性能下降**。

---

### 2.5 总结：损失平衡 vs. 梯度平衡

| 标准 | 损失平衡 | 梯度平衡 |
|-----------|---------------|-------------------|
| 计算成本 | 低（1次反向传播） | 高（$m$ 次反向传播） |
| 性能 | 良好 | 更好 |
| 收敛性 | 启发式 | 理论保证 |
| 内存使用 | 低 | 高（存储梯度） |
| 可扩展性 | 好 | 有限 |

**核心洞察：**
- 损失平衡方法计算高效，但缺乏理论保证
- 梯度平衡方法以更高的计算成本换来更好的性能和收敛特性

---

## 寻找有限个解的集合

### 第3.1部分 基于偏好的方法：MOEA/D 框架 [19]

**MOEA/D（基于分解的多目标进化算法，Multi-objective Evolutionary Algorithm based on Decomposition）** 结合了：

1. **分解**（来自传统优化）：将逼近 Pareto 前沿的任务分解为 $N$ 个子问题。每个子问题可以是单目标或多目标的。

2. **协作**（来自群体智能）：$N$ 个智能体，每个对应一个子问题。相邻子问题协作求解。

**问题分解——加权求和：**
$$\min_x g^{ws}(x|\lambda) = \lambda_1 f_1(x) + \lambda_2 f_2(x), \quad \lambda_1 + \lambda_2 = 1, \; \lambda_1, \lambda_2 \geq 0$$

将 Pareto 前沿近似为 $N$ 个单目标优化问题。

**问题分解——Tchebycheff 方法：**
$$\min_x g^T(x|\lambda, z^*) = \max\{\lambda_1|f_1(x) - z_1^*|, \lambda_2|f_2(x) - z_2^*|\}$$

其中 $z = (z_1^*, z_2^*)$ 是**乌托邦点**（$z_i^* < \min f_i$）。

**关键特性：** 对于任意 Pareto 最优解 $x^*$，存在某个 $\lambda$ 使得 $x^*$ 是 Tchebycheff 问题的最优解。

**局限性：** $g^T(x, \lambda)$ 关于 $x, \lambda$ 不平滑。

**邻域结构：**
- 权重向量相近的两个子问题互为邻居
- 相邻子问题的目标函数相似 → 最优解也相似（高概率）

**MOEA/D 迭代（每代每个智能体）：**
1. **交配选择：** 从部分邻居处获取当前解（协作）
2. **繁殖：** 通过变异自身解和借来的解生成新解
3. **替换：** 若新解更好则替换旧解；向邻居传播

---

### 第3.2部分 无偏好方法：超体积（Hypervolume）

**定义（超体积，Hypervolume）[20]：**
给定解集（Solution Set）$S = \{q^{(1)}, \ldots, q^{(N)}\}$ 和参考点（Reference Point）$r$，$S$ 的超体积为：

$$HV_r(S) = \text{Vol}\left(\{p \mid \exists q \in S : q \preceq p \preceq r\}\right)$$

超体积（Hypervolume）同时衡量解集的**收敛性（Convergence）** 和**多样性（Diversity）**。

**通过容斥原理计算超体积：**
$$\left|\bigcup_{i=1}^m A_i\right| = \sum_{i=1}^m |A_i| - \sum_{1 \leq i < j \leq m} |A_i \cap A_j| + \cdots + (-1)^{m-1}\left|\bigcap_{i=1}^m A_i\right|$$

- 项数：$2^m - 1$ → 时间复杂度 $O(2^m)$

**高效算法：**
- 二维（$m=2$）：Bentley 平面扫描 — $O(K \log K)$
- 更高维（$m > 2$）：$O(K^{m/2} \log K)$

**超体积梯度：**
$$\frac{\partial H}{\partial \theta} = \sum_j \frac{\partial H}{\partial y_j} \cdot \frac{\partial y_j}{\partial \theta}$$

其中 $\frac{\partial H}{\partial y_j}$ 是每个点的超体积贡献，$\frac{\partial y_j}{\partial \theta}$ 是 Jacobian 矩阵。

---

### 第3.3部分 处理多目标函数

当**目标数 $m$ 远大于解的数量 $K$**（$m \gg K$）时，标准方法会失效。

**少对多——最小值的最大值最小化 [21]（香港城市大学）：**

核心思想：候选集中至少有一个解能优化所有目标。

$$\min_{X_K \subseteq \mathcal{X}} \max_{i \in [m]} \min_{x^{\{i\}} \in \mathcal{X}} f_i(x)$$

每个目标被分配给集合中对它最好的解。

**少对多——最小值之和（SoM）[22]（加州大学洛杉矶分校）：**

$$\min_{X_K \subseteq \mathcal{X}} \sum_{i=1}^m \min_{x^{\{i\}} \in \mathcal{X}} f_i(x)$$

最小化解集中所有最小目标值之和。

---

## 深度学习中的应用

### 4.1 计算机视觉：多任务密集预测（Multi-task Dense Prediction）

**设置：** 训练单个模型同时执行多个像素级预测任务（如深度估计、表面法向预测、语义分割）——对自动驾驶和机器人至关重要。

**架构：**
```
输入图像 → 共享编码器 → 特征 → 解码器A → 任务A输出
                                → 解码器B → 任务B输出
                                → 解码器C → 任务C输出
```

**冲突问题：** 在反向传播过程中，来自不同任务损失的梯度流回共享编码器。如果任务A和B需要相互冲突的特征更新，它们会相互干扰——一个任务主导而其他任务受损。

**多目标优化公式：**
- 每个任务的损失被视为**独立的目标函数**
- 目标：找到在所有任务上平衡性能的**Pareto 最优**共享参数集

---

### 4.2 模型合并（Model Merging）

**问题：** 许多针对特定任务微调的强大模型（例如在 HuggingFace 上）已经存在。将它们合并为单个模型可以节省内存和部署成本。

**现有方法的局限性：** 当前合并技术（权重平均、任务算术）产生单一的"一刀切"模型——固定的权衡，无法适应不同用户偏好。

#### 将合并形式化为多目标优化问题 [23]

**目标：** 找到合并模型的 Pareto 集，其中每个点代表原始模型能力之间不同的最优权衡。

**按合并场景划分的目标：**

*无数据合并：*
$$\text{目标}_k: \|\theta_{\text{合并}} - \theta_k\|_F^2$$
（在参数空间中最小化合并模型与每个原始模型之间的距离）

*基于数据的合并：*
$$\text{目标}_k: \text{Entropy}(f(\theta_{\text{合并}}; \text{data}_k))$$
（最小化合并模型在每个任务数据上的预测熵）

**Pareto 合并：参数高效解决方案**

学习单个偏好感知模型：
$$\theta(\alpha) = \theta_{\text{base}} + \mathcal{G} \times A_1 \times A_2 \times A_3 \times \alpha$$
$$\underbrace{\phantom{XXXXXXXX}}_{\text{低秩张量修正}}$$

- $\theta_{\text{base}}$：与偏好无关的基础（单个高质量合并模型）
- 低秩张量修正：根据用户偏好 $\alpha$ 进行偏好相关的个性化调整

该结构可高效为任意偏好 $\alpha$ 生成定制模型。

**MAP [24]：** 通过二次近似的摊销 Pareto 前沿实现低计算成本模型合并。

---

### 4.3 强化学习（Reinforcement Learning）

**标准强化学习：** 智能体学习策略 $\pi$ 以最大化**标量**累积奖励。

**多目标强化学习（MORL，Multi-objective Reinforcement Learning）：** 智能体（Agent）在每步收到**向量值（Vector-valued）** 奖励：$r(s, a) \in \mathbb{R}^m$。

**多目标强化学习目标：** 学习策略网络 $\pi_\theta(s)$，寻找期望折扣奖励向量的 Pareto 最优权衡：

$$\min_\theta \mathbf{f}(\theta) := \left(-\mathbb{E}_{\pi_\theta}\left[\sum_t \beta^t r_{1,t}\right], \ldots, -\mathbb{E}_{\pi_\theta}\left[\sum_t \beta^t r_{m,t}\right]\right)$$

**基准：** Meta-World [25]——10目标和50目标机器人操作基准。

**多目标强化学习方法：**
1. **基于标量化的方法：** 使用线性标量化将奖励向量转换为标量 → 用标准强化学习求解
2. **梯度平衡方法：** 将 MGDA 直接应用于每个奖励目标的策略梯度
3. **学习整个 Pareto 集合：** 学习单个偏好条件策略 $\pi_\theta(s, \alpha)$，对任意期望权衡 $\alpha$ 都能最优行动

---

### 4.4 大语言模型对齐（LLM Alignment）

#### 多目标对齐

**问题：** 大语言模型对齐对于确保输出反映人类价值观至关重要，但人类价值观是多维的且可能相互冲突（例如有益性 vs. 无害性）。

**奖励汤（RS）[26] 和 MOD [27]：**
- 针对 $m$ 个偏好维度分别微调 $m$ 个大语言模型
- 在推理时在以下空间中组合：
  - **RS：** 参数空间（插值权重）
  - **MOD：** Logit 空间（组合下一个 token 分布）

#### 多目标测试时对齐

**核心挑战：** 微调计算成本高昂（例如微调65B大语言模型需要8×A100-80G GPU）。

**开放问题：** 能否在保持基础大语言模型**冻结**的情况下实现多目标对齐？

#### GenARM [29]

**核心思想：** 使用奖励模型引导冻结的基础大语言模型的生成，受 RLHF 闭合形式解 [28] 启发：

$$\log \pi(y|x) = \underbrace{-\log Z(x)}_{\text{分区函数}} + \underbrace{\log \pi_{\text{base}}(y|x)}_{\text{基础大语言模型}} + \underbrace{\frac{1}{\beta} r(x, y)}_{\text{奖励分数}}$$

**自回归奖励模型（ARM）：** 训练输出**token 级**奖励。

**ARM 设计：**
$$r(x, y) = \sum_t \log \pi_\theta(y_t | x, y_{<t})$$

**训练目标：**
$$f(\pi_\theta, \mathcal{D}) := -\mathbb{E}_{(x, y^1, y^2, z) \sim \mathcal{D}} \left[\log \sigma\left((-1)^z \beta_r (r(y^1, x) - r(y^2, x))\right)\right]$$

其中 $z$ 表示偏好（$z=1$ 表示 $y^1$ 优于 $y^2$）。

**多目标引导生成：** 训练 $m$ 个 ARM $\{\pi_{\theta_i}\}_{i=1}^m$。给定偏好向量 $\alpha$：

$$\log \pi(y_t | x, y_{<t}) = -\log Z(x, y_{<t}) + \log \pi_{\text{base}}(y_t | x, y_{<t}) + \frac{1}{\beta} \sum_{i=1}^m \alpha_i \log \pi_{\theta_i}(y_t | x, y_{<t})$$

---

### 4.5 AI for Science：多目标分子设计（Multi-objective Molecule Design）

**需要优化的属性：**
- QED（类药性）
- LogP（辛醇-水分配系数）
- LogS（溶解度对数）
- SA（合成可及性）
- DRD2（多巴胺受体D2亲和力）
- JNK3（c-Jun N 端激酶3抑制）
- GSK3β（糖原合酶激酶3β抑制）

**属性计算器：** https://github.com/sdv-dev/RDT

**三种生成方法：**

#### 1. 基于大语言模型：MOLLEO [30]
使用大语言模型在进化优化中进行交叉和变异：
- 将各目标之和作为单一目标，保留 $n_c$ 个最优个体
- 只保留当前种群的 Pareto 前沿
- 重复直到用完最大预算

#### 2. 基于扩散模型 [32]
使用**扩散后验采样（DPS）**：
$$\hat{z}_0 := \mathbb{E}_{z_0 \sim p(z_0|z_t)}[z_0] = \frac{1}{\sqrt{\bar{\alpha}_t}}\left(z_t + (1 - \bar{\alpha}_t) \nabla_{z_t} \log p_t(z_t)\right)$$

多目标两步扩散：
$$z_t \leftarrow z_t + \underbrace{\nabla_{z_t} \log p_t(z_t)}_{\text{有效分子}} + \underbrace{\nabla_{z_t} \log p_t(y_1|z_t)}_{\text{属性1引导}}$$
$$z_t \leftarrow z_t + \nabla_{z_t} \log p_t(z_t) + \underbrace{\nabla_{z_t} \log p_t(y_2|z_t)}_{\text{属性2引导}}$$

#### 3. 基于 GFlowNet：HN-GFN [33] 和 MO-GFlowNet [34]

**核心思想：** $P(x)$ 的分布与奖励 $R(x)$ 成正比。

**算法：**
1. 从 Dirichlet 分布中采样随机偏好 $\lambda$
2. 计算标量化奖励 $R(x;\lambda) = g(R(x), \lambda)$
3. 优化轨迹平衡损失：

$$L(\tau, \lambda; \theta) = \left(\log \frac{Z_\theta(\lambda) \prod_{s \to s' \in \tau} P_F(s'|s, \lambda; \theta)}{R(x|\lambda) \prod_{s \to s' \in \tau} P_B(s|s', \lambda; \theta)}\right)^2$$

4. 更新超网络参数 $\phi$：$\phi \leftarrow \phi - \eta \nabla_\phi L(\theta_\phi(\lambda))$

#### MO-LLM [31]

一个更复杂的基于大语言模型的多目标优化平台，具有以下特点：
- **将经验总结为提示**（与 MOLLEO 不同）
- 使用**混合策略**维护种群，平衡多样性和收敛性

MO-LLM 已在以下问题上创造**世界纪录**：
- 圆的填充问题（例如 $n=26$：2.635983 vs. AlphaEvolve 的 2.635863）
- 结构设计
- 数学发现

---

### 4.6 开源库

#### LibMOON [35]

PyTorch 中的基于梯度的多目标优化库（NeurIPS 2024）。

**支持的组件：** 问题类、求解器类、核心求解器类。

**PSL 梯度分解：**
$$\frac{\partial \ell_{\text{psl}}}{\partial \phi} = \mathbb{E}_{\lambda \sim \text{Dir}(p)} \underbrace{\frac{\partial \tilde{g}}{\partial f}}_{\tilde{\alpha}: 1 \times m} \cdot \underbrace{\frac{\partial f}{\partial \theta}}_{B: m \times n} \cdot \underbrace{\frac{\partial \theta}{\partial \phi}}_{C: n \times D}$$

三个部分分别对应：
1. **使用哪个核心求解器**（$\frac{\partial \tilde{g}_\lambda}{\partial f}$）
2. **如何计算 Jacobian 矩阵**——零阶优化或反向传播（$\frac{\partial f}{\partial \theta}$）
3. **PSL 模型**——超网络或 LoRA（$\frac{\partial \theta}{\partial \phi}$）

**代码示例：**

*生成无限个解（PSL——合成数据）：*
```python
problem = get_problem(problem_name=args.problem_name, n_var=args.n_var)
solver = BasePSLSolver(problem, batch_size=args.batch_size, device=args.device, ...)
model, loss_history = solver.solve()
```

*生成有限个解：*
```python
problem = get_problem(problem_name=args.problem_name, n_var=args.n_var)
prefs = get_prefs(n_prob=args.n_prob, n_obj=problem.n_obj, mode='uniform', clip_eps=1e-2)
core_solver = EPOCore(n_var=problem.n_var, prefs=prefs)
solver = GradBaseSolver(step_size=args.step_size, epoch=args.epoch, tol=args.tol, core_solver=core_solver)
res = solver.solve(problem=problem, x=synthetic_init(problem, prefs), prefs=prefs)
```

*多目标优化多任务学习：*
```python
model = model_from_dataset(args.problem_name)
num_param = numel(model)
core_solver = EPOCore(n_var=num_param, prefs=prefs)
solver = GradBaseMTLSolver(problem_name=args.problem_name, step_size=args.step_size, epoch=args.epoch,
                           core_solver=core_solver, batch_size=args.batch_size, prefs=prefs)
res = solver.solve()
```

#### LibMTL [36]

用于深度多任务学习的 PyTorch 库（2400+星，发表于 JMLR）。

**支持：**
- 26种优化策略
- 8种架构
- 6个数据集

**模块化设计：** 便于自定义多任务学习问题、插入现有方法或实现新方法以进行公平基准测试。

---

## 开放挑战与未来方向

### 挑战1：理论理解

**问题：**
- 许多实用的多目标深度学习方法的理论基础尚未完全理解
- 研究主要集中于**收敛性**，而对**泛化误差**的关注较少——这对实际性能至关重要

**未来方向：**
- 开发更广泛的、与算法无关的泛化性分析
- 从理论上研究网络设计选择如何影响 Pareto 集合近似

---

### 挑战2和3：效率与可扩展性

**降低梯度平衡成本：**
- *问题：* 梯度平衡方法有显著的计算开销
- *未来方向：* 将梯度平衡与线性标量化等简单方法整合，以降低成本并支持大规模使用

**处理多目标：**
- *问题：* 目标更多时偏好向量空间呈指数增长 → 随机采样对学习 Pareto 集合无效
- *未来方向：*
  - 高维偏好空间的高效采样策略
  - 基于目标属性自动减少或合并目标的方法

---

### 挑战4：分布式训练

**问题：**
- 大多数当前多目标优化算法是为单 GPU 或单机设计的
- 扩展到多 GPU 和分布式环境引入了单目标优化中未见的独特挑战

**未来方向：**
- **高效通信：** 设计跨多个 GPU/节点高效分布和同步梯度的方法
- **隐私保护多目标优化：** 当不同目标的数据分散在不同设备上且无法共享时，开发协作训练技术

---

### 挑战5：大语言模型的发展

**问题：**
- 当前大语言模型的多目标优化应用大多集中在 RLHF 阶段
- 用户偏好通常被简化为基本的偏好向量，可能无法捕捉人类需求的复杂性

**未来方向：**
- 将多目标优化技术应用于大语言模型生命周期的其他阶段（预训练、指令微调等）
- 探索更复杂的方法来表示和整合复杂而细致的用户偏好

---

### 挑战6：更多场景中的应用

**未被充分挖掘的潜力：**
- 大多数深度学习问题本质上是多目标的（模型在多个标准上被评估）
- 这些标准往往产生自然的权衡，非常适合多目标优化

**未来方向：**
- 积极利用多目标优化方法在更广泛的深度学习应用中显式地探索权衡
- 从单一指标优化转向更全面的、多目标的模型开发方式

---

## 关键要点

1. **多目标优化无处不在：** 多任务学习、RLHF、模型合并、神经架构搜索、药物发现——所有这些都涉及本质上相互冲突的目标。

2. **Pareto 最优性提供了原则性框架：** 与其任意固定权重，多目标优化找到整个权衡曲面（Pareto 前沿）或其上的偏好点。

3. **损失平衡 vs. 梯度平衡的权衡：**
   - 损失平衡：廉价、简单，但启发式
   - 梯度平衡：更好的性能和保证，但代价高昂

4. **标量化方法**（加权求和、Tchebycheff、平滑 Tchebycheff）是将多目标优化化简为可求解子问题的主要工具。

5. **MGDA / PCGrad / CAGrad** 是寻找单个 Pareto 最优解的关键基于梯度的方法——每种方法对解决梯度冲突都有不同的几何直觉。

6. **偏好条件学习（PSL）** 允许单个模型表示整个 Pareto 集合，支持在推理时实时调整偏好。

7. **超体积** 是评估有限个 Pareto 解集合的黄金质量指标，同时衡量收敛性和多样性。

8. **多目标场景**（$m \gg K$）需要根本不同的策略——"少对多"和最小值之和重新公式化允许可处理的近似。

9. **大语言模型对齐**是一个自然的多目标优化问题——GenARM 和奖励汤代表了互补的方法（冻结 vs. 微调基础模型）。

10. **开源工具**（LibMOON、LibMTL）降低了将多目标优化应用于深度学习研究和实践的门槛。

---

## 参考文献

| # | 参考文献 | 背景 |
|---|-----------|---------|
| [1] | A. B. Arrieta 等，"Explainable artificial intelligence (xai): Concepts, taxonomies, opportunities and challenges toward responsible ai"，*Information Fusion*，2020。 | 机器学习模型精度-可解释性权衡 |
| [2] | Y. Gu 等，"Jet-nemotron: Efficient language model with post neural architecture search"，*arXiv:2508.15884*，2025。 | 大语言模型性能-速度权衡示例 |
| [3] | Y. Zhong 等，"Panacea: Pareto alignment via preference adaptation for LLMs"，*NeurIPS*，2024。 | 大语言模型对齐中有益性 vs. 无害性 |
| [4] | S. Luukkonen 等，"Artificial intelligence in multi-objective drug design"，*Current Opinion in Structural Biology*，2023。 | 多目标药物设计中的 AI |
| [5] | S. Liu、E. Johns、A. J. Davison，"End-to-end multi-task learning with attention"，*CVPR*，2019。 | 动态权重平均（DWA） |
| [6] | A. Kendall、Y. Gal、R. Cipolla，"Multi-task learning using uncertainty to weigh losses for scene geometry and semantics"，*CVPR*，2018。 | 不确定性加权（UW） |
| [7] | B. Lin 等，"Dual-balancing for multi-task learning"，*arXiv:2308.12029*，2023。 | IMTL-L 的对数变换等价性 |
| [8] | L. Liu 等，"Towards impartial multi-task learning"，*ICLR*，2021。 | IMTL-L（损失）和 IMTL-G（梯度）方法 |
| [9] | F. Ye 等，"Multi-objective meta learning"，*NeurIPS*，2021。 | MOML 双层优化 |
| [10] | S. Liu 等，"Auto-Lambda: Disentangling dynamic task relationships"，*TMLR*，2022。 | MOML 的高效扩展 |
| [11] | F. Ye 等，"A first-order multi-gradient algorithm for multi-objective bi-level optimization"，*ECAI*，2024。 | FORUM——MOML 的高效扩展 |
| [12] | B. Lin 等，"Reasonable effectiveness of random weighting: A litmus test for multi-task learning"，*TMLR*，2022。 | 随机加权作为强基线 |
| [13] | X. Lin 等，"Smooth tchebycheff scalarization for multi-objective optimization"，*ICML*，2024。 | 平滑 Tchebycheff 标量化（STCH） |
| [14] | O. Sener、V. Koltun，"Multi-task learning as multi-objective optimization"，*NeurIPS*，2018。 | MGDA——梯度加权 |
| [15] | B. Liu 等，"Conflict-averse gradient descent for multi-task learning"，*NeurIPS*，2021。 | CAGrad——梯度加权 |
| [16] | T. Yu 等，"Gradient surgery for multi-task learning"，*NeurIPS*，2020。 | PCGrad——梯度操纵 |
| [17] | A. Navon 等，"Multi-task learning as a bargaining game"，*ICML*，2022。 | 周期性权重更新加速策略 |
| [18] | B. Liu 等，"FAMO: Fast adaptive multitask optimization"，*NeurIPS*，2023。 | FAMO——MGDA 的无梯度加速 |
| [19] | Q. Zhang、H. Li，"MOEA/D: A multiobjective evolutionary algorithm based on decomposition"，*IEEE TEC*，2007。 | MOEA/D 框架 |
| [20] | E. Zitzler、L. Thiele，"Multiobjective optimization using evolutionary algorithms"，*PPSN*，1998。 | 超体积定义 |
| [21] | X. Lin 等，"Few for many: Tchebycheff set scalarization for many-objective optimization"，*ICLR*，2025。 | 少对多——最大最小值（香港城市大学） |
| [22] | L. Ding 等，"Efficient algorithms for sum-of-minimum optimization"，*ICML*，2024。 | 最小值之和（SoM）——加州大学洛杉矶分校 |
| [23] | W. Chen、J. Kwok，"Pareto merging: Multi-objective optimization for preference-aware model merging"，*ICML*，2025。 | 模型合并的 Pareto 合并 |
| [24] | L. Li 等，"Map: Low-compute model merging with amortized pareto fronts via quadratic approximation"，*arXiv:2406.07529*，2024。 | MAP——低计算成本模型合并 |
| [25] | T. Yu 等，"Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning"，*CoRL*，2020。 | Meta-World 基准（10/50目标） |
| [26] | A. Rame 等，"Rewarded soups: Towards Pareto-optimal alignment by interpolating weights fine-tuned on diverse rewards"，*NeurIPS*，2023。 | 大语言模型对齐的奖励汤（RS） |
| [27] | R. Shi 等，"Decoding-time language model alignment with multiple objectives"，*NeurIPS*，2024。 | MOD——Logit 空间对齐 |
| [28] | R. Rafailov 等，"Direct preference optimization: Your language model is secretly a reward model"，*NeurIPS*，2023。 | DPO——RLHF 闭合形式解 |
| [29] | Y. Xu 等，"GenARM: Reward guided generation with autoregressive reward model for test-time alignment"，*ICLR*，2025。 | GenARM——冻结大语言模型对齐 |
| [30] | H. Wang 等，"Efficient evolutionary search over chemical space with large language models"，*ICLR*，2025。 | MOLLEO——基于大语言模型的分子优化 |
| [31] | N. Ran、Y. Wang、R. Allmendinger，"MOLLM: Multi-objective large language model for molecular design"，*arXiv:2502.12845*，2025。 | MO-LLM——通用大语言模型多目标优化平台 |
| [32] | X. Han 等，"Training-free multi-objective diffusion model for 3d molecule generation"，*ICLR*，2024。 | 分子生成的多目标扩散模型 |
| [33] | Y. Zhu 等，"Sample-efficient multi-objective molecular optimization with GFlowNets"，*NeurIPS*，2023。 | HN-GFN——超网络 GFlowNet |
| [34] | M. Jain 等，"Multi-objective GFlowNets"，*ICML*，2023。 | MO-GFlowNet |
| [35] | X. Zhang 等，"LibMOON: A gradient-based multiobjective optimization library in PyTorch"，*NeurIPS*，2024。 | LibMOON 开源库 |
| [36] | B. Lin、Y. Zhang，"LibMTL: A Python library for deep multi-task learning"，*JMLR*，2023。 | LibMTL 开源库 |
