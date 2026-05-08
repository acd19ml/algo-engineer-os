# 第一周：计算机视觉与自然语言处理中的架构演进

**课程：** CS6487 机器学习专题
**授课教师：** 郭建远博士
**学期：** 香港城市大学计算机科学系，2025-26年度 B 学期

---

## 概述

本周涵盖神经网络架构（Neural Network Architecture）在两大领域——计算机视觉（CV，Computer Vision）与自然语言处理（NLP，Natural Language Processing）——的历史与技术演进。讲座从早期卷积网络（Convolutional Network，1989年）一路追溯至现代基于 Transformer 的大型语言模型（LLM，Large Language Model，2025年），梳理出推动各阶段进步的共同工程原则。

**核心主题：**
- 表征学习（Representation Learning）与神经网络深度的作用
- 通过捷径连接（Shortcut Connection）解决梯度消失/爆炸（Gradient Vanishing/Exploding）问题
- 面向边缘部署（Edge Deployment）的高效神经网络设计
- 混合专家（MoE，Mixture of Experts）范式在大语言模型扩展中的应用
- 超连接（Hyper-Connections）作为残差捷径（Residual Shortcut）的广义形式

---

## 核心概念

### 1. 表征学习（Representation Learning）

表征学习的核心思想是：神经网络能够从原始数据中自动学习有用的特征表示（Feature Representation），而无需依赖人工设计的特征（Hand-crafted Features）。深层网络学习层次化表示（Hierarchical Representation）：

- **浅层（Early Layers）** 捕捉低级特征（Low-level Features）：边缘、纹理
- **中间层（Middle Layers）** 捕捉中级特征（Mid-level Features）：部件、形状
- **深层（Deep Layers）** 捕捉高级语义特征（High-level Semantic Features）：物体、类别

XOR 问题在历史上促成了多层网络（Multi-layer Network）的提出：单层线性网络无法分离 XOR，但加入隐藏层（Hidden Layer）后，网络可以学到一种非线性表示，使问题在该表示空间中线性可分。

**反向传播**（Backpropagation，LeCun 等，1989年）通过链式法则（Chain Rule）高效计算梯度，使多层网络的训练成为可能。

---

### 2. 梯度消失 / 爆炸（Gradient Vanishing / Exploding）问题

随着网络加深，梯度（Gradient）在反向传播过程中可能出现两种极端情况：
- **消失（Vanishing）**：梯度指数级缩小，导致浅层学习极为缓慢
- **爆炸（Exploding）**：梯度指数级增大，训练变得不稳定

这一核心挑战促使研究者提出了更好的初始化（Initialization）策略和架构创新（Architectural Innovation），即残差连接（Residual Connection）。

**前向传播（Forward Pass）与反向传播（Backward Pass）过程中的信号必须保持规范化**，以防止跨多层的尺度误差积累。

---

### 3. 网络初始化（Network Initialization）

良好的初始化能确保训练初期信号不消失、不爆炸。

| 方法 | 适用激活函数 | 公式 | PyTorch API |
|---|---|---|---|
| Xavier 初始化（Xavier Init） | 线性激活（Linear Activation） | `n * Var(w) = 1` | `torch.nn.init.xavier_uniform_()` |
| Kaiming 初始化（Kaiming Init） | ReLU 激活 | `n * Var(w) = 2` | `torch.nn.init.kaiming_uniform_()` |

两种方法均基于分析假设（Analytical Assumption，如高斯权重分布）推导出方差（Variance）在层间的传播规律。Xavier 适用于对称激活函数（Symmetric Activation，tanh、sigmoid），而 Kaiming 则针对 ReLU 的死亡神经元（Dead Neuron）特性（ReLU 平均会将一半输出置零）进行了修正。

**关键参考文献：**
- "Efficient Backprop" — LeCun 等，1998年
- Xavier 初始化："Understanding the difficulty of training deep feedforward neural networks" — Glorot & Bengio，2010年
- Kaiming 初始化："Delving Deep into Rectifiers" — He 等，ICCV 2015年

---

### 4. 归一化（Normalization）模块

归一化层（Normalization Layer）能在训练过程中稳定激活值（Activation）的分布，降低对初始化的敏感性，并支持更高的学习率（Learning Rate）。

- **批归一化**（BN，Batch Normalization）：在批次（Batch）维度上归一化，适用于大批次训练的 CNN。由 Ioffe & Szegedy 提出（ICML 2015年）。
- **层归一化**（LN，Layer Normalization）：在特征（Feature）维度上归一化，是 Transformer 的标准配置。
- **其他变体：** 组归一化（Group Norm）、实例归一化（Instance Norm）等，适用于批次较小或特征具有空间结构的场景。

**核心作用：** BN 通过在整个训练过程中将激活值控制在合理范围内（"减少内部协变量偏移"，Reducing Internal Covariate Shift），使得更深网络的训练成为可能。

---

### 5. 捷径连接（Shortcut Connection）与残差学习（Residual Learning）

捷径（跳跃/残差）连接（Skip/Residual Connection）是实现极深网络（Very Deep Networks）的最重要架构创新。网络不再直接学习映射 `H(x)`，而是学习**残差**（Residual）`F(x) = H(x) - x`，从而使恒等映射（Identity Mapping）变得极易学习。

```
输出 = F(x) + x
     （残差 + 恒等捷径）
```

**为何有效：**
- 梯度可以直接通过恒等路径（Identity Path）流动，绕过非线性变换
- 即使中间层只学习细微的修正，恒等捷径也能保留有用信息
- 支持拥有数百乃至数千层的网络

这一原则远不止于 ResNet：它在 Transformer（LayerNorm + 残差）、超连接以及众多现代架构中普遍存在。

---

### 6. 高效神经网络（Efficient Neural Networks，边缘部署）

三种架构技术可大幅降低移动端/边缘设备（Mobile/Edge Devices）的计算成本：

#### 深度可分离卷积（Depthwise Separable Convolution，MobileNet）
将标准卷积（Standard Convolution）分解为两个更廉价的步骤：
1. **深度卷积（Depthwise Conv）：** 对每个输入通道（Input Channel）单独应用一个滤波器（Filter），独立捕获各通道内的空间模式
2. **逐点卷积（Pointwise Conv，1×1）：** 跨通道（Channel）混合信息

**计算量缩减：** 从 `H*W*Cin*Cout*K*K` 降至 `H*W*Cin*K*K + H*W*Cin*Cout`，约为原始计算量的 `1/Cout + 1/K²`。

---

> 学习进度标记（2026-04-26）：已学到这里。已完成标准卷积、Depthwise Conv、Pointwise Conv、Depthwise Separable Conv 的计算量与表达能力取舍；下次从分组卷积（Group Convolution）和通道混洗（Channel Shuffle）继续。

---

#### 分组卷积（Group Convolution）+ 通道混洗（Channel Shuffle，ShuffleNet）
- **分组卷积：** 将通道分为 G 组，各组内独立进行卷积
- **问题：** 各组之间无法跨边界（Boundary）交换信息
- **通道混洗（Channel Shuffle）：** 在下一次分组卷积前对通道进行重新排列，实现跨组通信

#### 倒置残差（Inverted Residual）与线性瓶颈（Linear Bottleneck，MobileNet V2）
- 传统瓶颈（Bottleneck）：宽→窄→宽（先压缩后扩展）
- 倒置残差：窄→宽→窄（先扩展后压缩）
- 扩展阶段为深度卷积提供更多通道，提升表达能力（Expressiveness）
- 最终线性（无激活，No-activation）瓶颈保留特征的流形结构（Manifold Structure）

#### Ghost 模块（Ghost Module，GhostNet）
- CNN 中许多特征图（Feature Map）存在冗余（Redundancy），一个特征图是另一个的线性变换
- GhostNet 通过普通卷积生成一小组"本征"特征图（Intrinsic Feature Maps），再通过廉价线性运算生成"幽灵"特征图（Ghost Feature Maps）
- 在更低计算量（FLOPs，Floating Point Operations）下实现与全宽网络相当的精度

---

### 7. 混合专家（MoE，Mixture of Experts）

MoE 将 Transformer 中单一的稠密前馈网络（FFN，Feed-Forward Network）层替换为一组 `N` 个专家网络（Expert Networks），并由一个**路由器/门控网络**（Router/Gating Network）决定对每个 token 激活哪些专家。

**稀疏激活（Sparse Activation）：** 对于任意输入，每次只激活一部分专家（例如从16个中选取前2个），因此即使总参数量大幅增加，每个 token 的实际计算量仍保持可控。

**组合灵活性示例（来自 DeepSeekMoE）：**
- 在16个专家中标准 top-2 路由：C(16,2) = **120** 种组合
- 细粒度方案：将每个专家拆分为4个子专家 → 在64个子专家中 top-8 路由：C(64,8) = **4,426,165,368** 种组合

如此巨大的组合数量使模型能够形成更加专业化（Specialized）、更具针对性的表示。

**关键论文：**
- Switch Transformers（Google）：简化的 MoE，每个 token 单一专家路由，参数量扩展至万亿级
- DeepSeekMoE：细粒度专家分割（Fine-grained Expert Segmentation）

---

### 8. 超连接（Hyper-Connections）与 mHC

**超连接**（Hyper-Connections，ByteDance，ICLR 2025年）对标准残差捷径（Residual Shortcut）进行了推广：每层的输出可以是多个前序层（Previous Layers）表示的可学习线性组合（Learnable Linear Combination），而不仅仅是简单的 `x + F(x)`。

- 残差连接（Residual Connection）是超连接在固定系数（Fixed Coefficients）下的特殊情形
- 超连接可以模拟非相邻层（Non-adjacent Layers）之间更丰富的信息流动

**问题：** 引入可学习混合系数（Learnable Mixing Coefficients）后，无法保证映射行为良好——训练过程中范数（Norm）可能无限增长。

**mHC（流形约束超连接，Manifold-Constrained Hyper-Connections，DeepSeek）** 通过对复合映射（Composite Mapping）施加约束来解决这一问题：
- **前向传播约束（Forward Pass Constraint）：** 基于复合映射矩阵行和（Row Sum）绝对值的最大值——控制前向方向的最坏情况扩展
- **反向传播约束（Backward Pass Constraint）：** 基于列绝对值最大值（Maximum Absolute Column Sum）——控制梯度传播

这些约束将表示限制在有界流形（Bounded Manifold）上，在保留超连接表达能力的同时确保训练稳定。

---

### 9. 下一个 Token 预测（NTP，Next Token Prediction）——大语言模型如何生成文本

NTP 是现代大语言模型的基本训练目标（Training Objective）。在每一步，模型根据所有前置 token 预测最可能的下一个 token。

**三步生成过程：**

1. **生成分数**（Logits）：大语言模型读取输入序列，为词表（Vocabulary，通常数以万计）中的每个 token 生成一个分数（Logit）。

2. **转换为概率**（Softmax）：Logits 经 Softmax 函数（Softmax Function）转换为合法的概率分布（Probability Distribution）：
   ```
   P(token_i) = exp(z_i) / sum(exp(z_j) for all j)
   ```
   示例：logit 4.2 → 约36%，logit 4.1 → 约32%，logit 3.9 → 约26%，以此类推。

3. **加权采样（Weighted Sampling）：** 模型不总是选择概率最高的 token（贪婪解码，Greedy Decoding，否则输出会确定且重复），而是按概率分布进行采样。这引入了**受控随机性（Controlled Randomness）**——同一输入在不同运行中可以产生不同输出，对于多样性（Diversity）和创造性（Creativity）至关重要。

**循环往复：** 每个新生成的 token 被追加到输入序列，重复上述过程，直到生成特殊的序列结束 token（EOS，End-of-Sequence Token）。

---

### 10. 门控 FFN（Gated FFN）与 GLU 变体（GLU Variants）

Transformer 中的标准 FFN：`FFN(x) = W2 * ReLU(W1 * x)`

门控变体（Gated Variants）——GLU（Gated Linear Unit）、SwiGLU、GeGLU——增加了乘性门控机制（Multiplicative Gating Mechanism）：

```
GatedFFN(x) = (W1 * x) * gate(W3 * x)
```

其中 `gate` 是激活函数（Activation Function），如 sigmoid（GLU）、GELU（GeGLU）或 Swish（SwiGLU）。

- 门控机制充当软性过滤器（Soft Filter）：能够动态地抑制或放大不同特征维度（Feature Dimension）的信息
- SwiGLU 被用于 LLaMA、PaLM 以及大多数现代开源大语言模型
- 在相同参数量（Parameter Count）下，consistently 优于标准 ReLU-FFN

---

## 重要模型与架构

### 计算机视觉（CV）时间线

| 年份 | 模型 | 核心创新 | 深度 |
|---|---|---|---|
| 1989/1998 | LeNet | 首个实用 CNN；卷积（Convolution）+池化（Pooling）+全连接（FC）+反向传播 | ~5层 |
| 2012 | AlexNet | 大规模深度 CNN；GPU 训练；ImageNet | 8层 |
| 2014 | VGGNet | 系统性深度研究；3×3 卷积堆叠 | 11–19层 |
| 2014 | GoogleNet/Inception | Inception 模块；多尺度（Multi-scale）并行卷积 | 22层 |
| 2015 | ResNet | 残差（捷径）连接；支持1000+层 | 50–1000+ |
| 2016 | DenseNet | 密集连接（Dense Connection）：每层连接所有后续层 | 20–100 |
| 2017 | MobileNet V1 | 面向边缘设备的深度可分离卷积 | — |
| 2018 | ShuffleNet V1/V2 | 分组卷积+通道混洗；实用效率指导原则 | — |
| 2018 | MobileNet V2 | 倒置残差；线性瓶颈 | — |
| 2019–20 | EfficientNet | NAS（Neural Architecture Search）+ 宽度/深度/分辨率复合缩放（Compound Scaling） | — |
| 2020 | GhostNet | 廉价线性运算生成冗余特征图 | — |
| 2020 | ViT | Transformer 应用于图像块（Image Patches） | 12–24 |
| 2021+ | DeiT, PVT, Swin, TNT, ConvNeXt | 混合（Hybrid）及改进的视觉 Transformer | 不定 |

#### 云端（Cloud-side）vs. 边缘端（Edge-side）侧重点
- **云端：** 追求最高精度（Accuracy）；计算成本相对次要（AlexNet → VGG → ResNet → ViT）
- **边缘端：** 最小化 FLOPs、内存（Memory）、延迟（Latency）；同时注重隐私保护（MobileNet → ShuffleNet → GhostNet）
- **知识蒸馏（Knowledge Distillation）：** 大型云端模型为紧凑型（Compact）边缘模型的训练提供指导——大模型为小模型生成标签或软目标（Soft Targets）

---

### NLP / 大语言模型（LLM）时间线

| 年份 | 模型/技术 | 核心创新 |
|---|---|---|
| 2017年前 | RNN、LSTM、GRU | 序列处理（Sequential Processing）；门控机制（Gating Mechanism）捕获长程依赖 |
| 2017 | Transformer | 自注意力（Self-Attention）；完全放弃递归（Recurrence）；可并行化（Parallelizable） |
| 2020 | GPT-3 | 1750亿参数大语言模型；大规模少样本学习（Few-shot Learning） |
| 2020 | 门控 FFN（GLU 变体） | FFN 层中的乘性门控（SwiGLU、GeGLU） |
| 2021 | Switch Transformers | 稀疏 MoE（Sparse MoE）；每个 token 单一专家；万亿参数 |
| 2022 | ChatGPT | 基于 RLHF（Reinforcement Learning from Human Feedback）对齐的对话大语言模型 |
| 2023 | LLaMA | 开源大语言模型；引发开源生态繁荣 |
| 2023 | GPT-4V / Gemini | 多模态大语言模型（Multimodal LLM，文本+图像/视频） |
| 2023 | Qwen-VL | 阿里巴巴多模态大语言模型 |
| 2023 | Phi-2 | 微软小参数量高性能模型 |
| 2024+ | DeepSeekMoE | 细粒度专家分割；超密集 MoE |
| 2025 | 超连接（HC） | 广义捷径连接；字节跳动（ICLR 2025） |
| 2025 | mHC | 流形约束超连接；DeepSeek |

---

### Transformer 架构深度解析

Transformer（Vaswani 等，NeurIPS 2017年）引入了一种根本不同的序列建模（Sequence Modeling）方法：

- **自注意力（Self-Attention）：** 序列中每个 token 可以直接关注其他所有 token——没有 CNN 的局部偏置（Local Bias），也没有 RNN 的序列瓶颈（Sequential Bottleneck）
- **多头注意力**（MHSA，Multi-Head Self-Attention）：多个注意力头（Attention Heads）并行学习不同类型的关系
- **位置编码**（PE，Positional Encoding）：由于自注意力对排列具有等变性（Permutation-equivariant），位置信息必须显式添加
- **前馈网络**（FFN，Feed-Forward Network）：在每个位置（Position）独立应用的逐位置 MLP（Position-wise MLP）
- **残差连接（Residual Connection）+ 层归一化（LayerNorm）：** 围绕每个子层（Sub-layer）应用，保证训练稳定性

**参数层全为线性（等价于 1×1 卷积）：** Q、K、V 投影（Projection）和 MLP 层。注意力（Attention）本身不包含参数——参数存在于投影矩阵（Projection Matrices）中。

**视觉 Transformer**（ViT，Vision Transformer，2020年）：将相同架构应用于图像，方法是：
1. 将图像切分为固定大小的块（Patches，如 16×16 像素）
2. 对每个块进行线性嵌入（Linear Embedding）→ 生成 token 序列
3. 应用标准 Transformer 编码器（Encoder）
4. 使用分类 token（[CLS] Token）进行分类

ViT 表明，一种统一的架构（Unified Architecture）可以在语言、视觉、音频及其他序列/结构化数据中普遍适用。

---

## 关键要点

1. **深度强大，但难以训练。** 计算机视觉架构的历史，很大程度上是一部克服障碍（梯度消失、初始化不当）的历史，正是这些障碍阻止了深层网络有效学习。

2. **残差/捷径连接（Residual/Shortcut Connection）是普适解决方案。** 无论是 ResNet（CV）、Transformer（NLP），还是超连接（两者兼顾），围绕变换块提供梯度高速通道（Gradient Highway）的原则，是深度学习中最一致有效的思想之一。

3. **效率与精度的权衡（Efficiency-Accuracy Trade-off）由架构来管理。** MobileNet、ShuffleNet 和 GhostNet 表明，聪明的架构选择（而非仅仅剪枝或量化）可以在极低成本下恢复大模型的大部分精度。

4. **稀疏计算（Sparse Computation）支撑规模扩展。** MoE 将参数量（Parameter Count）与每个 token 的计算量（Computation per Token）解耦，使得万亿参数模型的训练和服务在经济上可行。

5. **Transformer 是通用架构（General-purpose Architecture）。** 它已在 NLP 中取代了特定任务架构，并在 CV 领域（ViT、Swin）越来越具竞争力。其模块化特性（SA + FFN + 残差 + 归一化）使组件替换（门控 FFN、MoE 层、超连接）变得便捷。

6. **生成中的随机性（Randomness in Generation）是特性，而非缺陷。** 加权采样（Weighted Sampling，而非贪婪的 argmax）可防止大语言模型输出的确定性和重复性，同时赋予模型创造力（Creativity）和多样性（Diversity）。

7. **云端与边缘通过协作共存（Cloud-Edge Collaboration）。** 大型云端模型生成数据、标签和软知识（Soft Knowledge），用于训练紧凑型边缘模型。边缘模型与云端模型也可以在推理时协作（推测解码，Speculative Decoding）。

---

## 参考文献

> 完整引用信息请参见课程目录中的相关阅读文档。本讲座引用的主要论文包括：

- **LeNet（1989/1998）：** LeCun 等——奠基性 CNN 工作
- **AlexNet（NIPS 2012）：** Krizhevsky、Sutskever、Hinton
- **VGGNet（ICLR 2015）：** Simonyan & Zisserman
- **GoogleNet/Inception（CVPR 2015/2016）：** Szegedy 等
- **批归一化（Batch Normalization，ICML 2015）：** Ioffe & Szegedy
- **ResNet（CVPR 2016）：** He、Zhang、Ren、Sun
- **Kaiming 初始化（Kaiming Init，ICCV 2015）：** He 等
- **MobileNet V1：** Howard 等（Google）
- **MobileNet V2（CVPR 2018）：** Sandler 等（Google）
- **ShuffleNet V1（CVPR 2018）：** Zhang 等（旷视）
- **ShuffleNet V2（ECCV 2018）：** Ma 等（旷视）
- **GhostNet（CVPR 2020）：** Han 等（华为）
- **Transformer（NeurIPS 2017）：** Vaswani 等
- **ViT（ICLR 2021）：** Dosovitskiy 等
- **视觉 Transformer 综述（TPAMI 2022）：** Han 等
- **GLU 变体（2020）：** Shazeer
- **Switch Transformers：** Fedus 等（Google）
- **DeepSeekMoE：** DeepSeek 团队
- **超连接（Hyper-Connections，ICLR 2025）：** 字节跳动
- **mHC：** DeepSeek 团队

---

*笔记整理自 CS6487 第一周讲座幻灯片。如需深入阅读，请参考上述原始论文及课程相关阅读文档。*
