# 第三周：Transformer 架构中的位置编码

**课程：** CS6487 机器学习专题
**授课教师：** 郭建远博士
**学期：** 香港城市大学计算机科学系，2025-26年度 B 学期
**参考来源：** NeurIPS 2025 教程（Christopher Curtis、Saiph Savage）

---

## 概述

本讲座探讨 Transformer 架构中的**位置编码（PE）**——为何必要、如何从2017年的正弦固定编码演进至现代的无参数方法（如 RoPE 和 ALiBi），以及未来面向多模态和特定领域任务的发展方向。

### 讲座路线图
1. 自注意力回顾
2. 正弦编码深度解析
3. 位置编码方法的演进
   - 2018–2021：相对位置表示（RPR）方法的概念演进
   - 2021–2025：现代方法 + 多模态/特定领域方法
4. 位置编码的未来

---

## Transformer 基础

### 为何 Transformer 占据主导

Transformer 驱动着几乎所有领域的最先进模型：
- 自然语言处理（NLP）
- 计算机视觉
- 多模态推理
- 科学机器学习
- 智能体 AI

其核心创新——**自注意力（Self-Attention）**——无需递归（Recurrence）即可对 token 间的全局关系建模，赋予其关键优势：

| 特性 | 描述 |
|---|---|
| **全局内容理解** | 每个 token 可以同时关注所有其他 token |
| **并行化** | 去除了顺序递归；支持大规模训练 |
| **灵活性** | 适用于 NLP、视觉、音频、时序、生物等领域 |
| **可扩展性** | 性能随模型规模和数据规模的增加而提升 |

### 代表性 Transformer 模型
- **大语言模型：** LLaMA、GPT、Qwen
- **视觉：** ViT（视觉 Transformer）、Swin Transformer
- **多模态：** CLIP、Flamingo
- **信息检索：** BERT

---

## 自注意力（Self-Attention）：深度回顾

### 关键术语与符号

| 符号 | 含义 |
|---|---|
| $N$ | 序列中的 token 数 |
| $D$ | 嵌入维度 |
| $X$ | 形状为 $N \times D$ 的输入张量 |
| $w$ | 注意力分数 |
| $B$ | 批次大小（通常被抽象掉） |
| $W_Q, W_K, W_V$ | 可学习权重矩阵（$D \times D$） |
| $Q, K, V$ | 查询、键、值张量（$N \times D$） |

### 张量与嵌入

**张量（Tensor）：** 按 $n$ 维组织数字的通用容器：
- 标量（0维）：单个数字
- 向量（1维）：数字列表
- 矩阵（2维）：数字网格
- 3维张量：矩阵的堆叠
- 4维+张量：更高阶的堆叠

**嵌入（Embedding）：** 捕获语义含义（Semantic Meaning）的稠密（Dense）数值表示。含义相似的词被映射到嵌入空间（Embedding Space）中相近的向量：

$$\text{cat} \to [0.6,\ 0.9,\ 0.1,\ 0.4,\ \ldots]$$
$$\text{dog} \to [0.7,\ -0.1,\ 0.4,\ 0.3,\ \ldots]$$
$$\text{house} \to [-0.8,\ -0.4,\ -0.5,\ 0.1,\ \ldots]$$

关键特性：$\text{"cat"}$ 和 $\text{"dog"}$ 相近；$\text{"cat"}$ 和 $\text{"house"}$ 相距较远。嵌入在应用位置编码之前是**固定的**（预训练得到）。

### 计算 Q、K、V

给定输入 $X \in \mathbb{R}^{N \times D}$ 和权重矩阵 $W_Q, W_K, W_V \in \mathbb{R}^{D \times D}$：

$$Q = X W_Q, \quad K = X W_K, \quad V = X W_V$$

每个张量 $Q, K, V \in \mathbb{R}^{N \times D}$ 表示输入在嵌入空间中的增强、可学习编码。具体地，单元 $(i, j)$ 为：

$$Q_{ij} = x_i \cdot W_Q^{(:,j)}$$

即第 $i$ 个 token 与权重矩阵第 $j$ 列在嵌入维度上的点积。

### 注意力分数计算

**注意力分数矩阵（Attention Score Matrix）** $A \in \mathbb{R}^{N \times N}$ 计算如下：

$$A = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{D}}\right)$$

- 每个单元 $A_{ij}$ 量化："token $j$ 与 token $i$ 的相关程度如何？"
- 缩放因子 $\frac{1}{\sqrt{D}}$ 防止点积量级过大导致 softmax 梯度塌陷。
- 此操作也称为**点积注意力（Dot-product Attention）**，因为它以点积（Dot Product）作为相似度度量。

**为何使用点积？**
点积衡量的是按量级缩放的余弦相似度。当结果较大时，向量在嵌入空间中指向相似方向（语义相似性）。由于它对量级也很敏感，这促使了 $\sqrt{D}$ 缩放和精心的嵌入设计。

> 参考：Wang 等，*Non-local Neural Networks*，CVPR 2018（全局注意力类机制的原始动机）。

### 上下文张量（Context Tensor）

最终上下文张量（Context Tensor）$Z$ 为：

$$Z = A V$$

注意力矩阵 $A$ 根据所有 token 之间的相互关联度，对值向量 $V$ 中的信息进行重新分配。

---

## 核心问题：缺乏顺序感知

### 为何位置编码是必要的

自注意力在设计上是**排列等变的（Permutation-equivariant）**：模型无法原生感知相邻关系（Adjacency）、方向性（Directionality）或距离（Distance）。这意味着：

- **"猫追了狗"** 和 **"狗追了猫"** 产生完全相同的注意力分数矩阵（只是排列顺序不同）。
- 时序依赖关系、token 间距离和方向性关系在没有外部位置信息的情况下是不可见的。

这产生了对**位置编码（PE，Positional Encoding）** 的根本需求：一种将顺序（Order）、距离（Distance）和方向性（Directionality）整合到模型中的机制。

### 位置编码必须提供的信息
1. 区分 token 顺序（"猫追狗" vs. "狗追猫"）
2. 对时序依赖关系建模
3. 捕获距离（token 之间的距离）
4. 理解方向（左/右、早/晚、上游/下游）

---

## 位置编码的历史轨迹

### 三个时代

| 时代 | 时期 | 关注点 |
|---|---|---|
| **第一时代** | ~2017年 | 绝对正弦编码（Absolute Sinusoidal Encoding，输入层面） |
| **第二时代** | 2018–2021年 | 相对位置表示（Relative Position Representation）；注意力内部的可学习参数 |
| **第三时代** | 2021年至今 | 最简/无参数方法（Parameter-free，RoPE、ALiBi）；多模态与特定领域 |

---

## 位置嵌入的类型

### 1. 绝对位置编码（正弦编码）— Vaswani 等，2017年

#### 公式（Formulation）

位置编码（Positional Encoding）$P \in \mathbb{R}^{N \times D}$ 直接加到输入（Input）上：

$$X' = U + P$$

其中 $U$ 是 token 内容嵌入（即原来的 $X$），$P$ 是位置信号。

正弦编码定义为：

$$P_{(pos, 2i)} = \sin\!\left(\frac{pos}{10000^{2i/D}}\right)$$

$$P_{(pos, 2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/D}}\right)$$

其中 $pos$ 是 token 位置，$i$ 是维度索引。

#### 加入正弦 PE 后注意力的展开

将 $X$ 替换为 $U + P$ 后，注意力分数 $A_{ij}$ 展开为**四个项**：

$$A_{ij} \propto \underbrace{U_i W_Q W_K^\top U_j^\top}_{\text{(1) 内容–内容}} + \underbrace{U_i W_Q W_K^\top P_j^\top}_{\text{(2) 内容–位置}} + \underbrace{P_i W_Q W_K^\top U_j^\top}_{\text{(3) 位置–内容}} + \underbrace{P_i W_Q W_K^\top P_j^\top}_{\text{(4) 位置–位置}}$$

| 项 | 描述 |
|---|---|
| (1) 内容–内容 | 标准自注意力（语义相似性） |
| (2) 内容–位置 | token $i$ 的内容与绝对位置 $j$ 的关系 |
| (3) 位置–内容 | 绝对位置 $i$ 与 token $j$ 内容的关系 |
| (4) 位置–位置 | token $i$ 与 $j$ 之间的纯位置关系 |

几乎所有后续 PE 方法都强调这四个项中的一个或多个。

#### 通过三角恒等式实现相对编码

利用三角积化和差公式：

$$\sin(\alpha)\sin(\beta) = \frac{1}{2}[\cos(\alpha - \beta) - \cos(\alpha + \beta)]$$
$$\cos(\alpha)\cos(\beta) = \frac{1}{2}[\cos(\alpha - \beta) + \cos(\alpha + \beta)]$$

**位置–位置**项（4）通过**角度差** $(\theta_i - \theta_j)$ 编码相对距离，其中 $\theta \propto pos / 10000^{2i/D}$。

这意味着正弦编码同时捕获：
- **绝对位置：** 每个位置获得唯一的固定向量。
- **相对位置（隐式）：** $P_{pos+k}$ 可以表示为 $P_{pos}$ 的线性函数（通过三角恒等式）。

对于 $N=50, D=128$，这创建了一个在不同频率下振荡的丰富位置信号矩阵。

#### 正弦编码的问题

1. **控制力不足：** 位置信号通过大规模可学习交互隐式编码——难以解释或约束。
2. **噪声：** 学习到的距离属性可能与领域知识相冲突。
3. **泛化性弱：** 绝对编码对未见过的序列长度外推效果差。
4. **无方向性：** 无法区分从左到右和从右到左。
5. **缺乏专用学习：** 既然已经高度依赖学习，为何不引入专用的可学习参数？

> 视觉证据：TENER 论文（Yan 等，2019年）表明正弦 PE 产生嘈杂的相对距离模式。

---

### 2. 绝对可学习位置编码（APE）

#### 公式

与固定正弦不同，学习一个 $N_{\max} \times D$ 的参数矩阵：

$$P \in \mathbb{R}^{N_{\max} \times D} \quad \text{（完全可学习）}$$

每个位置（直到最大上下文长度 $N_{\max}$）都获得一个专用的可学习 $D$ 维向量。

#### 特性

- 实现简单：仅需查表和加法操作。
- 引入 $N_{\max} \times D$ 个新参数（可能很大）。
- 相比正弦编码没有明显性能提升。
- **仍在 BERT 中使用**（固定小上下文长度的仅编码器模型）。

#### APE 的问题

**有效性：**
- 随着网络深度增加，信号影响力减弱（仅在输入时添加一次）。
- 内容–位置和位置–位置项可能并非最理想的编码目标。

**规模：**
- 需要 $N_{\max} \times D$ 个参数——对长上下文来说代价较高。

**泛化性：**
- 无法泛化到长度超过 $N_{\max}$ 的序列。

> **当前使用情况：** BERT 和小型特定任务编码器模型。大多数现代大语言模型不使用 APE。

---

### 3. 相对位置表示（RPR）— Shaw 等，2018年

**论文：** *Self-Attention with Relative Position Representations*，NAACL 2018（Google Brain）

#### 核心洞察

与其在输入中添加位置信息，不如将其作为注意力分数的偏置**直接注入注意力计算**中。

#### 直觉：节点与边

将 token 视为图中的节点，其相对距离视为边权重。目标是在嵌入空间中学习最优的边权重向量，其中每个相对距离（以最大距离 $k$ 截断）都有自己的可学习向量。

#### 公式

单元 $(i, j)$ 的修改后注意力分数变为：

$$e_{ij} = \frac{q_i (k_j + a_{ij}^K)^\top}{\sqrt{D}}$$

其中 $a_{ij}^K \in \mathbb{R}^D$ 是一个可学习向量，由截断相对距离 $\text{clip}(j - i, -k, k)$ 索引。

在张量层面，这将正弦编码的**位置–位置**项替换为精确的可学习相对距离偏置，并通过 $Q$ 张量交互捕获**内容–位置**关系。

#### 相比正弦 PE 的优势

| | 正弦 PE | RPR（Shaw） |
|---|---|---|
| 位置信号位置 | 输入层面 | 注意力内部 |
| 参数量 | 0（固定） | 每层 $2k+1$ 个可学习向量 |
| 方向性 | 无 | 有（有符号距离） |
| 噪声 | 高（隐式） | 低（受控） |
| 分析难度 | 难 | 较容易 |

#### Shaw 的实验

- 任务：带编码器-解码器 Transformer 的神经机器翻译（NMT）。
- 发现：相对位置表示相比正弦绝对编码提升了翻译质量。
- 关键发现：在**每一层**（而非仅在输入处）添加位置信息可以改善性能。
- 将相对信息与绝对信息结合相比仅使用相对信息无显著增益。

---

### 4. Transformer-XL — Dai 等，2019年

**论文：** *Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context*，ACL 2019（Google）

#### 动机

Transformer 受到上下文长度 $N$ 的限制。Transformer-XL 通过段级递归将 Shaw 的相对编码扩展，以建模**超出固定上下文长度的依赖关系**。

#### 核心创新

在 Shaw 的基础上扩展，Transformer-XL 的注意力分数包含**四个项**（重现原始展开注意力表达式的全部四项）：

$$e_{ij} = \underbrace{q_i^\top k_j}_{\text{内容–内容}} + \underbrace{q_i^\top W_{K,R} r_{i-j}}_{\text{内容–位置}} + \underbrace{u^\top k_j}_{\text{全局内容偏置}} + \underbrace{v^\top W_{K,R} r_{i-j}}_{\text{全局位置偏置}}$$

| 项 | Shaw | Transformer-XL |
|---|---|---|
| 内容–内容 | 是 | 是 |
| 内容–位置（基于查询） | 是 | 是 |
| 全局内容偏置 | 否 | 是——$u$（可学习，与查询无关） |
| 全局位置偏置 | 否 | 是——$v$（可学习，与查询无关） |

全局偏置 $u$ 和 $v$ 是**与查询无关的**：它们编码了一种关于内容和距离的均匀先验，无论哪个 token 正在发出查询。这捕获了一种直觉：某些词通常是重要的，无论当前的查询是什么。

---

### 5. 改进的 RPR 方法 — Huang 等，2020年

**论文：** *Improve Transformer Models with Better Relative Position Embeddings*，EMNLP 2020（AWS）

Huang 等认为 Shaw 的方案未能充分利用 $Q$、$K$ 与相对距离之间的交互。他们提出了**四种方法**作为消融研究：

| 方法 | 描述 |
|---|---|
| **M1** | 用绝对距离 $\|i-j\|$ 的可学习标量缩放注意力分数 $(i,j)$ |
| **M2** | 同 M1，但允许方向性（有符号距离 $j - i$） |
| **M3** | 三维可学习张量：按距离逐通道缩放每个 $Q$/$K$ 嵌入维度 |
| **M4** | 类似 Shaw，但对 $Q$ 和 $K$ 张量均加入对称的内容–位置偏置 |

**主要发现：**
- 直接用标量缩放注意力分数（M1、M2）对性能**有害**。
- 对称内容–位置偏置（M4）优于仅基于查询的偏置（Shaw 的方法）。

---

### 6. DA-Transformer — Wu 等，2021年

**论文：** *DA-Transformer: Distance-Aware Transformer*，NAACL 2021（微软亚洲研究院）

核心贡献：
- **多头距离分割：** 跨注意力头分配位置编码，迫使每个头学习不同的距离范围（部分窄/局部，部分宽/全局）。
- **非负约束：** 防止位置信号过度强调负注意力单元值。

---

### 7. Swin Transformer — Liu 等，2021年

**论文：** *Swin Transformer: Hierarchical Vision Transformer Using Shifted Windows*，ICCV 2021（微软亚洲研究院）

在**视觉领域**应用相对位置编码，在局部注意力窗口内使用2D相对位置偏置。证明了 RPR 风格的编码可以自然地迁移到图像块上。

---

### 8. RoPE：旋转位置嵌入 — Su 等，2021年

**论文：** *RoFormer: Enhanced Transformer with Rotary Position Embedding*

#### 划时代影响

RoPE 目前是仅解码器大语言模型的**主流 PE 方法**，被以下模型使用：
- LLaMA、Mistral、Falcon、Qwen、Gemma、DeepSeek

#### 核心思想

RoPE 通过**旋转（Rotation）** 查询（Query）和键（Key）向量的维度对来编码位置。对于位置 $m$ 处的二维情形，旋转矩阵（Rotation Matrix）为：

$$R_m = \begin{pmatrix} \cos(m\theta) & -\sin(m\theta) \\ \sin(m\theta) & \cos(m\theta) \end{pmatrix}$$

对于 $D$ 维向量，RoPE 应用 $D/2$ 个这样的2D旋转，每个旋转使用不同的基频 $\theta_i = 10000^{-2i/D}$。

旋转后的查询和键为：

$$\tilde{q}_m = R_m q_m, \quad \tilde{k}_n = R_n k_n$$

旋转 Q 和 K 的点积自然产生**相对位置** $(m - n)$ 的函数：

$$\tilde{q}_m^\top \tilde{k}_n = q_m^\top R_m^\top R_n k_n = q_m^\top R_{m-n} k_n$$

这是关键特性：注意力分数仅取决于**相对偏移** $(m-n)$，而非绝对位置。

#### 为何 RoPE 占据主导

- **无参数：** 无需额外的可学习参数。
- **数学优雅：** 相对位置自然从旋转结构中涌现。
- **外推性：** 优于 APE；在更长序列上退化更平缓。
- **高效：** 无需实例化 $N \times N$ 位置矩阵即可高效计算。

#### RoPE 扩展（面向长上下文）

RoPE 在极长距离时可能存在困难。扩展方案包括：

| 扩展 | 描述 |
|---|---|
| **YaRN** | 另一种 RoPE 扩展方案（Yet Another RoPE extensioN）——重新缩放频率分量 |
| **LongRoPE** | 通过渐进式重新缩放将 RoPE 扩展至极长上下文 |
| **NTK 感知缩放** | 使用神经切线核理论重新缩放基频 |
| **XPos** | 增加指数衰减以改善长程行为 |

**多模态扩展：**
- **M-RoPE**（Qwen2-VL）：将 RoPE 扩展至2D/3D空间位置，用于视觉语言模型，支持任意分辨率的感知。

---

### 9. ALiBi：线性偏置注意力 — Press 等，2022年

**论文：** *Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation*，ICLR 2022（Meta）

#### 动机问题
- Transformer 能否外推到比训练时更长的序列？
- PE 方法是否是外推失败的根本原因？
- 能否在不增加额外参数、不降低运行速度、不增加内存占用的情况下实现高效外推？

#### 公式

ALiBi 使用**固定的、不可学习的线性偏置（Fixed Non-learnable Linear Bias）** 修改注意力分数（Attention Score）：

$$e_{ij} = q_i k_j^\top - m \cdot |i - j|$$

其中 $m$ 是头特定的斜率（每个注意力头不同），构成等比数列。

在张量层面：

$$A = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{D}} + B\right)$$

其中 $B_{ij} = -m_h \cdot |i - j|$，$h$ 为注意力头编号。

#### 核心特性

- **单调衰减（Monotonic Decay）：** 注意力偏置（Attention Bias）随距离线性递减——较近的 token 自然获得更高的关注。
- **多头多样性（Multi-head Diversity）：** 每个头使用不同的斜率（Slope）$m_h$，捕获不同的局部尺度（Locality Scale）。
- **零参数（Zero Parameters）：** 完全固定——无需任何可学习参数（Learnable Parameters）。
- **长度外推（Length Extrapolation）：** 可以泛化到比训练时长得多的序列。

#### 实验结果

- **使用 ALiBi 在较短序列上训练可以超越使用正弦或 APE 在较长序列上训练的基线。**
- 由于参数固定，提升了速度和内存效率。
- 在**局部依赖**任务上特别有效。

---

### 10. NoPE：无位置编码 — Kazemnejad 等，2023年

**论文：** *The Impact of Positional Encoding on Length Generalization in Transformers*，NeurIPS 2023（麦吉尔大学、IBM、Meta）

#### 核心发现

令人惊讶的是，在某些合成的长度泛化（Length Generalization）任务上，**完全不使用位置编码（NoPE，No Positional Encoding）** 可以匹配甚至超越显式 PE 方法。因果注意力掩码（Causal Attention Mask）本身提供了一些隐式的顺序信号（Ordering Signal）。

#### NoPE 的局限性

- 研究的任务上下文非常短（$\leq 40$–50个 token）。
- 使用干净的合成数据（复制、反转、加法、SCAN、PCFG任务）。
- **不适用于：**
  - 长上下文外推任务
  - 图像、视频、音频或空间推理（需要显式坐标）
  - 代码、图、树、表格（需要位置线索）
  - 双向编码器（没有因果掩码提供顺序信号）

---

## 比较与分析

### PE 方法分类（Taxonomy of PE Methods）

| 方法 | 时代 | 位置（Location） | 可学习（Learnable） | 相对（Relative）? | 外推能力（Extrapolation） |
|---|---|---|---|---|---|
| 正弦编码（Vaswani 2017） | 2017 | 输入 | 否 | 隐式 | 差 |
| APE（BERT风格） | 2018 | 输入 | 是 | 否 | 差 |
| RPR（Shaw 2018） | 2018–2020 | 注意力 | 是 | 是 | 中等 |
| Transformer-XL（Dai 2019） | 2019 | 注意力 | 是 | 是 | 好 |
| ALiBi（Press 2022） | 2021–2025 | 注意力 | 否 | 是 | 很好 |
| RoPE（Su 2021） | 2021–2025 | Q/K 向量 | 否 | 是 | 好 |
| NoPE | 2023 | 无 | N/A | N/A | 取决于任务 |

### 注意力中的四个基本项

任何 PE 方法都可以通过它强调以下四个项中的哪些来刻画：

| 项 | Shaw | XL | ALiBi | RoPE |
|---|---|---|---|---|
| 内容–内容 | 是 | 是 | 是 | 是 |
| 内容–位置 | 是 | 是 | 否 | 是 |
| 全局内容偏置 | 否 | 是 | 否 | 否 |
| 全局位置偏置 | 否 | 是 | 是 | 否 |
| 位置–位置 | 已替换 | 已替换 | 已替换 | 已替换 |

### 应用性能特点

| 方法 | 最适用场景 |
|---|---|
| 正弦编码 | 短序列；可解释性研究 |
| APE | 固定长度编码器任务（BERT、分类） |
| RPR/XL | 长文档；NMT；编码器任务 |
| ALiBi | 局部依赖任务；高效长上下文推理 |
| RoPE | 通用解码器大语言模型；长上下文生成 |
| M-RoPE | 视觉语言多模态任务 |

**特定领域发现**（来自 Gong 等，2025年，基因序列建模）：
- RoPE 在捕获**周期性基序**和外推到长序列方面表现出色。
- ALiBi 在**局部依赖**驱动的任务上表现良好。

---

## 编码器 vs. 解码器：不同的 PE 哲学

### 编码器模型（如 BERT）

- **固定序列长度：** 为固定最大序列长度（通常512个 token）的任务而设计。
- **简单性：** 可学习绝对嵌入实现简单——直接查表相加。
- **特定任务性能：** 学习高效的特定任务位置表示。
- **双向上下文：** 每个 token 可以关注所有其他 token；绝对位置明确定义每个 token 的全局位置。
- **趋势：** 定制化、领域导向的信号；可学习、绝对和相对方法的混合。

### 解码器模型（如 GPT、LLaMA）

- **长度泛化：** 必须外推到可变且可能很长的序列长度。
- **相对距离优先：** 在长文本中，相邻词的关系比绝对位置更重要。
- **避免过拟合：** APE 可能过拟合到特定训练位置；RoPE 和 ALiBi 泛化效果更好。
- **收敛于 RoPE：** RoPE 已成为事实上的标准——不仅因为技术优势，还因为生态系统惯性（大规模预训练成本、共享架构标准）。

---

## 位置编码的未来

### 当前发展趋势

**编码器方向：**
- 高度定制化、特定用例的信号
- 面向特定领域（生物、物理、表格、图数据）
- 注重丰富的位置编码
- 针对较小的 Transformer 模型设计
- 可学习、绝对和相对信号的混合
- 固定的、较小的上下文很常见

**解码器方向：**
- 基于文本的模型已收敛于 RoPE（通常附带长上下文扩展）
- 视觉 Transformer（仅解码器架构）通常仍使用可学习绝对 PE
- 沉重的生态系统惯性倾向于采用、扩展和改造现有方案，而非从头重新设计

### 开放研究问题

1. **特定领域 PE：** 生物、物理、表格和图数据需要独特的结构线索——"位置"在每个领域有不同含义。
2. **多模态 PE：** 如何统一整合1D（文本）、2D（图像）、3D（视频/空间）位置信号（例如 Qwen2-VL 中的 M-RoPE）。
3. **PE 作为结构注入框架：** PE 正从简单的加性信号演进为将结构先验注入注意力的通用机制。
4. **超长上下文：** YaRN、LongRoPE、NTK 感知缩放是活跃研究领域。
5. **NoPE 的限制：** 精确理解无 PE 在何时以及为何有效仍是开放问题。

---

## 关键要点

1. **Transformer 缺乏固有的位置感知**——自注意力是排列等变的，使 PE 对任何序列任务都不可或缺。

2. **向输入添加 PE 会在注意力中产生四个交互项**：内容–内容、内容–位置（×2）和位置–位置。所有后续 PE 方法都在操纵这些项中的一个或多个。

3. **正弦编码**（Vaswani 2017）具有开创性，但存在隐式相对编码噪声大和外推效果差的问题。

4. **该领域从输入层面的 PE 转向了注意力层面的 PE**（自 Shaw 2018年起），提升了控制力、效率和可解释性。

5. **RoPE** 通过向量旋转优雅地实现相对位置编码——产生仅依赖相对偏移的注意力分数，且无需额外参数。

6. **ALiBi** 使用固定线性衰减偏置——零参数，强外推能力，适用于局部依赖任务。

7. **没有单一 PE 方法在所有场景下都占优：** 编码器倾向于可学习绝对 PE；解码器收敛于 RoPE；多模态任务需要空间扩展。

8. **PE 的未来**是特定领域的结构注入——将 PE 视为嵌入结构先验的框架，而非仅仅是顺序信息。

---

## 数学公式汇总

### 正弦 PE
$$P_{(pos, 2i)} = \sin\!\left(\frac{pos}{10000^{2i/D}}\right), \quad P_{(pos, 2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/D}}\right)$$

### 标准自注意力
$$A = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{D}}\right), \quad Z = AV$$

### RPR（Shaw）注意力分数
$$e_{ij} = \frac{(x_i W_Q)(x_j W_K + a_{ij}^K)^\top}{\sqrt{D}}$$

### Transformer-XL 注意力分数
$$e_{ij} = q_i^\top k_j + q_i^\top W_{K,R} r_{i-j} + u^\top k_j + v^\top W_{K,R} r_{i-j}$$

### RoPE 旋转
$$\tilde{q}_m = R_m q_m, \quad \tilde{k}_n = R_n k_n, \quad \tilde{q}_m^\top \tilde{k}_n = q_m^\top R_{m-n} k_n$$

### ALiBi 偏置
$$e_{ij} = q_i k_j^\top - m_h \cdot |i - j|$$

---

## 参考文献

### 主要论文

1. **Vaswani 等（2017）** — *Attention Is All You Need.* NeurIPS 30. [奠基性 Transformer + 正弦 PE]

2. **Shaw、Uszkoreit、Vaswani（2018）** — *Self-Attention with Relative Position Representations.* NAACL. Google Brain. [RPR 方法]

3. **Dai 等（2019）** — *Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context.* ACL. Google. [含全局偏置和段级递归的扩展 RPR]

4. **Wang、Girshick、Gupta、He（2018）** — *Non-Local Neural Networks.* CVPR. [全局注意力/点积相似度的动机]

5. **Yan 等（2019）** — *TENER: Adapting Transformer Encoder for Named Entity Recognition.* [证明正弦 PE 距离属性存在问题]

6. **Huang 等（2020）** — *Improve Transformer Models with Better Relative Position Embeddings.* EMNLP. AWS. [四种 RPR 消融方法]

7. **Wu、Wu、Huang（2021）** — *DA-Transformer: Distance-Aware Transformer.* NAACL. 微软亚洲研究院. [多头距离感知 PE]

8. **Liu 等（2021）** — *Swin Transformer: Hierarchical Vision Transformer Using Shifted Windows.* ICCV. 微软亚洲研究院. [视觉领域的相对 PE]

9. **Press 等（2022）** — *Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation.* ICLR. Meta. [ALiBi]

10. **Kazemnejad 等（2023）** — *The Impact of Positional Encoding on Length Generalization in Transformers.* NeurIPS. 麦吉尔大学、IBM、Meta. [NoPE 研究]

11. **Su 等** — *RoFormer: Enhanced Transformer with Rotary Position Embedding.* [RoPE]

12. **Qwen2-VL 团队** — *Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution.* [多模态的 M-RoPE]

13. **Gong 等（2025）** — *Evaluation of Coding Schemes for Transformer-based Gene Sequence Modeling.* [基因领域 RoPE vs. ALiBi 的应用比较]

### 教程来源

14. **Curtis, Christopher 和 Savage, Saiph（2025）** — NeurIPS 2025 位置编码教程. [本讲座的基础]

### 参考模型家族

- **LLaMA** — Meta 开源大语言模型家族（使用 RoPE）
- **Mistral** — Mistral AI 大语言模型（使用 RoPE）
- **Falcon** — TII 大语言模型（使用 RoPE）
- **Qwen** — 阿里巴巴大语言模型家族（使用 RoPE / M-RoPE）
- **Gemma** — Google DeepMind 大语言模型（使用 RoPE）
- **DeepSeek** — DeepSeek AI 大语言模型（使用 RoPE）
- **BERT** — Google 编码器模型（使用 APE）
- **GPT** — OpenAI 大语言模型家族
- **ViT** — 视觉 Transformer
- **CLIP** — OpenAI 视觉语言模型
- **Flamingo** — DeepMind 多模态模型
