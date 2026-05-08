# 第二周：高效深度学习与大规模分布式训练

**课程：** CS6487 机器学习专题
**授课教师：** 郭建远博士
**学期：** 香港城市大学计算机科学系，2025-26年度 B 学期

---

## 概述

深度学习从根本上改变了众多领域（自动驾驶、机器翻译、AlphaGo、智能机器人）。然而，随着模型规模（Model Scale）不断扩大——从数千亿到数万亿参数——三个基本的工程挑战随之涌现：**模型大小（Model Size）**、**训练速度（Training Speed）** 和 **能源效率（Energy Efficiency）**。本讲座综述了共同构成*高效深度学习（Efficient Deep Learning）*领域的算法（Algorithm）与硬件（Hardware）技术，涵盖推理时的模型压缩（Model Compression）与大规模分布式训练（Large-scale Distributed Training）两个方面。

统一框架是**算法-硬件协同设计（Algorithm-Hardware Co-Design）**：高效系统需要在两个维度上对算法（压缩、并行）和硬件（加速器、存储层次）进行联合优化：

- **推理（Inference）维度：** 对已训练模型进行压缩/优化，实现快速、低成本部署。
- **训练（Training）维度：** 使训练过程本身更快、更具扩展性（Scalable）。

---

## 核心概念

### 1. 大规模深度学习的三大挑战

#### 1.1 模型大小（Model Size）
- 大模型难以通过无线方式（Over-the-air）分发更新，例如在移动设备（Mobile Devices）上。
- 大语言模型的参数量（Parameter Count）已达数千亿：Deepseek（761B MoE）、LLaMA 3（405B 稠密模型）。
- 计算需求（Compute Requirement）惊人：现代大语言模型每个 Token 需消耗 250–2448 GFLOP。

#### 1.2 速度（Speed）
- 训练时间随模型深度线性增长。在四块 M40 GPU 上的基准测试数据如下：

| 模型 | 错误率 | 训练时间 |
|-----------|-----------|---------------|
| ResNet18 | 10.76% | 2.5 天 |
| ResNet50 | 7.02% | 5 天 |
| ResNet101 | 6.21% | 1 周 |
| ResNet152 | 6.16% | 1.5 周 |

- 漫长的训练时间直接制约了机器学习研究人员的生产力（Productivity）和迭代速度（Iteration Speed）。

#### 1.3 能源效率（Energy Efficiency）
- AlphaGo 需要 1,920 颗 CPU 和 280 块 GPU，每局棋的电费约 3,000 美元。
- 在移动端：大模型会迅速耗尽电池（Battery）。
- 在数据中心（Data Center）：能耗提高了总拥有成本（TCO，Total Cost of Ownership）。
- 关键洞察：**模型越大 → 内存访问（Memory Access）越多 → 能耗越高。** 内存访问的能耗是算术运算（Arithmetic Operation）的100倍以上，因此内存效率（Memory Efficiency）至关重要。

---

### 2. 高效推理算法（Algorithms for Efficient Inference）

压缩和加速推理（Inference Acceleration）的五种主要算法方法：

1. **剪枝（Pruning）**
2. **权重共享（Weight Sharing）**
3. **量化（Quantization）**
4. **低秩近似（Low-Rank Approximation）**
5. **二值/三值网络（Binary/Ternary Networks）**

#### 2.1 剪枝（Pruning）

**核心思想：** 移除已训练神经网络中的冗余权重（Redundant Weights，即突触），类似于人类大脑在发育过程中修剪突触连接（Synaptic Connections）（从出生时约1000万亿个突触减少到青少年时期的约500万亿个）。

**标准三步流程：**
1. **训练（Train）** — 正常训练完整的稠密网络（Dense Network）。
2. **剪枝（Prune）** — 移除低于阈值（Threshold）的权重（例如将小量级权重置零）。剪枝后权重分布（Weight Distribution）发生变化：剪枝前呈以零为中心的钟形曲线；剪枝后接近零的权重被移除。
3. **再训练/微调（Retrain/Fine-tune）** — 通过对稀疏网络（Sparse Network）进行微调，恢复因剪枝损失的精度。

**对权重分布（Weight Distribution）的影响：**
- 剪枝前：权重呈以近零值为中心的钟形分布（Bell-curve Distribution）。
- 剪枝后：接近零的权重消失，形成双峰分布（Bimodal Distribution）。
- 再训练后：分布重新调整，剩余权重向两侧扩散。

**对 RNN/LSTM/大语言模型的剪枝（Pruning）：**
- 即使在90%的稀疏率（Sparsity）下，剪枝后的语言模型仍能生成语义等价的图像描述/文本
- 在95%稀疏率时，生成文本开始出现一定程度的退化（Degradation）

**生物学类比（Biological Analogy）：** 人类突触剪枝（Synaptic Pruning）是一个灵感来源——大脑在修剪不使用的连接的同时保留关键通路（Critical Pathways），在不牺牲能力的情况下提升效率。

#### 2.2 权重共享（Weight Sharing）

**核心思想：** 强制一组权重共享一个代表值（Representative Value），从而减少需要存储的独立参数（Independent Parameters）数量。

**机制：**
1. 将权重聚类（Cluster）为 K 组（例如使用 k-means 聚类）。
2. 用每组的聚类中心（Cluster Centroid）值替换该组中的每个权重。
3. 只存储码本（Codebook，K 个中心值）和每个权重对应的索引（Index）。
4. 示例：权重 {2.09, 2.12, 1.92, 1.87} 全部映射到共享值 2.0。

**可视化：** 采用权重共享训练后，权重分布变为离散（Discrete）形态——聚集为少量不同的值，而非连续分布（Continuous Distribution）。

**比特效率（Bit Efficiency）：** 存储聚类索引所需的比特数（Bits）少于存储原始浮点权重。所需比特数取决于聚类数 K：每个权重索引需要 log₂(K) 比特。

#### 2.3 量化（Quantization）

**核心思想：** 将权重（Weights）和激活值（Activations）的数值精度（Numerical Precision）从32位浮点（FP32，32-bit Floating Point）降低到更低位宽（Bit-width，例如8位整数 INT8、FP16）。

**工作流程：**
1. 以完整的 float32 精度训练模型。
2. 收集权重和激活值分布的统计数据（Statistics）。
3. 执行量化（将浮点值映射到固定精度的离散值）。
4. 以浮点格式进行微调（Fine-tune）以恢复精度。
5. 转换为定点格式（Fixed-point Format）用于部署。

**示例（8位量化，8-bit Quantization）：**
- 权重映射到256个离散值（2⁸）。
- 激活值同样进行量化。
- 相比 FP32，内存占用（Memory Footprint）减少4倍（8位 vs. 32位）。

**结果（Qiu 等，FPGA'16）：** 8位量化的 CNN 可以匹配或接近其 float32 版本的精度，同时大幅降低计算（Compute）和内存需求。

#### 2.4 低秩近似（Low-Rank Approximation）

**核心思想：** 利用奇异值分解（SVD，Singular Value Decomposition）等技术，将大型权重矩阵（Weight Matrix，尤其是卷积层中的）分解为较小矩阵（Smaller Matrices）的乘积。

**对卷积层（Convolutional Layers）的处理：**
- 大型卷积核（Convolution Kernel）可以分解为一系列更小的卷积核的组合。
- 同时减少参数量（Parameter Count）和计算量（Computation）。
- Zhang 等（CVPR'15）证明这可以高效应用于非线性卷积网络。

#### 2.5 二值/三值网络（Binary/Ternary Networks）

**核心思想：** 将量化推向极限——将权重限制为仅2个值 {-1, +1}（二值，Binary）或3个值 {-1, 0, +1}（三值，Ternary）。

**训练三值量化（TTQ，Trained Ternary Quantization）— Zhu、Han、Mao、Dally，ICLR'17：**
- 权重在训练过程中被学习为三值（而非事后量化）。
- 同时学习两个缩放因子（Scale Factors，分别对应正权重和负权重）。
- 相比 FP32，权重内存减少约16倍。
- 训练过程中权重演化（Weight Evolution）：权重从分布式开始，随着训练的推进逐渐收敛到三值。
- TTQ 卷积核的可视化显示出清晰的三值聚类（Ternary Clusters）。

---

### 3. 高效推理硬件（Hardware for Efficient Inference）

#### 3.1 专用推理加速器（Specialized Inference Accelerators）

| 加速器 | 研发机构 | 核心特性 |
|-------------|-----------|-------------|
| Eyeriss | MIT | RS（行静止，Row Stationary）数据流（Dataflow） |
| DaDiannao | 中科院 | 片上 eDRAM（Embedded DRAM）存储 |
| TPU | Google | 8位整数运算（8-bit Integer Arithmetic） |
| NPU | 华为 | 神经网络处理单元（Neural Processing Unit） |

#### 3.2 Google TPU（张量处理单元，Tensor Processing Unit）

TPU 专为8位整数运算的神经网络推理而构建：
- **矩阵单元（Matrix Unit）：** 65,536（256×256）个8位乘加单元（MAC，Multiply-Accumulate Units）
- **时钟频率（Clock Rate）：** 700 MHz
- **峰值吞吐量（Peak Throughput）：** 92 TOPS（万亿次运算/秒）= 65,536 × 2 × 700M
- **MAC 优势：** MAC 数量比 GPU 多25倍以上，比 CPU 多100倍以上
- **片上内存（On-chip Memory）：**
  - 4 MiB 累加器内存（Accumulator Memory）
  - 24 MiB 统一缓冲区（Unified Buffer，比 GPU 多3.5倍）
- **片外（Off-chip）：** 8 GiB DDR3 DRAM（两通道，2133 MHz）

#### 3.3 屋顶线模型（Roofline Model）

屋顶线模型（Roofline Model）用于判断计算是**计算受限（Compute-bound）** 还是**内存带宽受限（Memory Bandwidth-bound）**：
- **计算受限：** FLOPS/秒是瓶颈 → 需要更快的计算单元（Compute Units）。
- **内存受限：** 内存带宽（Memory Bandwidth）是瓶颈 → 需要更好的数据复用（Data Reuse）或压缩。

**模型性能通常低于屋顶线的原因：**
- 低延迟（Low Latency）要求阻止使用大批次（Large Batch Size）→ 低运算密度（Operational Intensity，每字节运算次数）。
- **解决方案：** 压缩模型以减小内存占用（Memory Footprint）。
- **挑战：** 硬件必须能够高效执行压缩（稀疏，Sparse）模型。

#### 3.4 EIE：高效推理引擎（Efficient Inference Engine）

**EIE（Han 等，ACM SIGARCH 2016）** 是专为运行压缩（稀疏+量化，Sparse + Quantized）网络而设计的专用硬件加速器（Specialized Hardware Accelerator）：
- 同时利用权重（Weights）和激活值（Activations）的稀疏性（Sparsity）。
- 经验法则：`0 * A = 0` 且 `W * 0 = 0` → 跳过所有零乘法（Zero Multiplications）。
- 自定义数据流（Dataflow）直接在硬件上跳过零计算。
- **结果：** 与压缩模型上的 CPU/GPU 相比，显著提升吞吐量（Throughput）和能源效率（Energy Efficiency）。

---

### 4. 高效训练算法（Algorithms for Efficient Training）

三种主要方法：

1. **并行化（Parallelization）**（跨多个 GPU/节点）
2. **混合精度训练（Mixed Precision Training）**（FP16 + FP32）
3. **模型蒸馏（Model Distillation）**（知识迁移，Knowledge Transfer）

#### 4.1 并行化策略（Parallelization Strategies）

现代大语言模型训练集群（Training Cluster）规模庞大。以 Meta 的 Llama 3 集群为例：
- **GPU：** H100，片上带宽（On-chip Bandwidth）3,352 GB/秒
- **服务器（Server）：** 8块 GPU，GPU 间带宽 900 GB/秒（NVLink）
- **机架（Rack）：** 2台服务器 = 16块 GPU
- **Pod：** 192个机架 = 3,072块 GPU，服务器间带宽 50 GB/秒
- **集群（Cluster）：** 8个 Pod = **24,576块 GPU**
- **总计：** 1.875 PB GPU 内存，4.15亿 FP32 核心，1300万张量核心（Tensor Cores），24.3 EFLOP/秒

拥有 L 层的模型操作形状为 `(Batch, Sequence, Dim)` 的张量（Tensor）。四种并行策略各自切分不同维度：

| 策略 | 缩写 | 切分维度 |
|----------|-------------|-----------------|
| 数据并行（Data Parallelism） | DP | 批次（Batch）维度 |
| 上下文并行（Context Parallelism） | CP | 序列（Sequence）维度 |
| 流水线并行（Pipeline Parallelism） | PP | 层（Layer，L）维度 |
| 张量并行（Tensor Parallelism） | TP | 隐藏（Hidden，Dim）维度 |

##### 4.1.1 数据并行（DP，Data Parallelism）

**思路：** 使用大小为 M×N 的 minibatch，分配给 M 块 GPU。由于梯度（Gradient）是线性的，每块 GPU 独立计算梯度，然后取平均（Averaging）。

**逐步工作流程：**
1. 每块 GPU 拥有完整的模型副本（Model Replica）和优化器（Optimizer）。
2. 每块 GPU 加载自己的 N 个数据样本（Data Samples）。
3. 每块 GPU 执行前向传播（Forward Pass）计算损失（Loss）Lᵢ。
4. 每块 GPU 执行反向传播（Backward Pass）计算梯度（Gradient）dLᵢ/dWⱼ。
5. 对所有 M 块 GPU 的梯度取平均（Gradient Averaging）：dL/dWⱼ = (1/M) Σ dLᵢ/dWⱼ。
6. 每块 GPU 使用平均梯度更新自己的权重（Weights）。

**优化（Optimization）：** 第4步（反向传播）和第5步（梯度同步，Gradient Sync）可以重叠（Overlap）——在计算第 j-1 层梯度的同时，开始传输第 j 层的梯度（梯度分桶，Gradient Bucketing）。

**关键限制：** 每块 GPU 必须在内存（Memory）中保存完整模型。使用 Adam 优化器时，每个权重需要4个数值（权重、梯度、一阶矩 β₁、二阶矩 β₂），每个数值占用2字节（FP16）：
- 10亿参数 → 8 GB
- 100亿参数 → 80 GB（刚好填满一块 H100 GPU）
- 700亿+参数 → 需要模型分片（Model Sharding）

**解决方案：** 全分片数据并行（FSDP，Fully Sharded Data Parallelism）。

##### 4.1.2 全分片数据并行（FSDP，Fully Sharded Data Parallelism）

**思路：** 跨 GPU 切分（Shard）模型权重。每个权重 Wᵢ 由且仅由一块 GPU"拥有"，该 GPU 同时存储其梯度（Gradients）和优化器状态（Optimizer States）。

**FSDP 算法（前向+反向传播）：**
1. **第 i 层前向传播前：** 拥有者 GPU（Owner GPU）将 Wᵢ 广播（Broadcast）到所有其他 GPU。
2. **所有 GPU** 使用 Wᵢ 执行第 i 层的前向传播，然后**删除**本地的 Wᵢ 副本（节省内存）。
3. **第 i 层反向传播前：** 拥有者 GPU 再次广播 Wᵢ。
4. **所有 GPU** 执行第 i 层的反向传播以计算本地 dL/dWᵢ，然后删除本地的 Wᵢ。
5. **第 i 层反向传播后：** 每块 GPU 将本地的 dL/dWᵢ 发送（Reduce）给拥有者 GPU，然后删除本地梯度。
6. **拥有者 GPU** 执行梯度更新（Gradient Update）（Wᵢ += -lr × dL/dWᵢ）。

**优化措施：**
- **预取（Prefetching）：** 在使用 Wᵢ 进行前向传播的同时，在后台预取 Wᵢ₊₁。
- **前向传播末尾优化：** 不删除前向传播结束时最后一个获取的权重，以避免立即重新获取它用于反向传播。
- **流水线重叠（Pipeline Overlap）：** 在使用 Wᵢ 进行反向传播的同时，同步发送/更新 Wᵢ₊₁ 的梯度并获取 Wᵢ₋₁。
- **数据预取（Data Prefetch）：** 在当前批次的前向+反向传播期间预取（Prefetch）下一批数据。

##### 4.1.3 混合分片数据并行（HSDP，Hybrid Sharded Data Parallelism）

**思路：** 使用 GPU 的二维网格（2D Grid）将 FSDP 与 DP 结合：
- 将 N = M × K 块 GPU 分为 M 组，每组 K 块 GPU。
- 每组 K 块 GPU 内部：使用 FSDP（权重分片，Weight Sharding）。
- M 组之间：使用标准 DP（梯度平均，Gradient Averaging）。

**通信模式（Communication Pattern）：**
- 每组**内部**进行3次高带宽（High-bandwidth）通信：Wᵢ（前向）、Wᵢ（反向）、dL/dWᵢ（反向）。将同组 GPU 保持在同一节点/Pod 中。
- **跨组**进行1次低带宽（Low-bandwidth）通信：仅在反向传播时传输 dL/dWᵢ。可以使用较慢的 Pod 间链路（Inter-pod Links）。

##### 4.1.4 上下文并行（CP，Context Parallelism）

**思路（针对 Transformer）：** 跨多块 GPU 处理单个长序列（Long Sequence），对序列（Sequence）维度进行切分。

**组件处理：**
- **归一化（Normalization）和残差连接（Residual Connection）：** 轻松实现并行化（无权重，序列切分范围内无跨 token 依赖）。
- **MLP 层（MLP Layers）：** 每块 GPU 保存 MLP 权重的副本；激活值（Activations）按序列位置切分；梯度同步方式与 DP 相同。
- **QKV 投影（QKV Projection）：** 与 MLP 相同——序列并行化，梯度同步。
- **注意力算子（Attention Operator）：** 由于全局注意力（Global Attention）依赖关系，处理最为复杂。两个选项：

**选项1——环形注意力（Ring Attention）：**
- 将 Q、K、V 分块（Block）并分布在各 GPU 上。
- 内层循环遍历键/值块（Key/Value Blocks，通过环形拓扑，Ring Topology 传递）。
- 外层循环遍历查询块（Query Blocks，本地）。
- 实现复杂，但可扩展到任意长度的序列。

**选项2——Ulysses 注意力（Ulysses Attention）：**
- 在多头注意力（Multi-head Attention）的注意力头（Attention Heads）维度上并行化。
- 不尝试分布注意力矩阵（Attention Matrix）本身。
- 实现更简单。
- 限制：最大并行度 = 注意力头数（Number of Attention Heads）。

##### 4.1.5 流水线并行（PP，Pipeline Parallelism）

**思路：** 将模型的 L 层分配给各 GPU，每块 GPU 处理一组层。激活值（Activations）在层边界处在 GPU 间传递（复制）。

**问题：** 顺序依赖关系（Sequential Dependencies）产生空闲时间（"气泡"，Bubbles）。一块 GPU 在收到前一块 GPU 的激活值之前无法处理下一层。对于 N 路 PP，朴素最大模型 FLOPS 利用率（MFU，Model FLOPS Utilization）为 1/N。

**解决方案——微批次（Microbatching）：**
- 将每个批次分成多个较小的微批次（Microbatches）。
- 通过 GPU 对微批次进行流水线（Pipeline）处理，保持 GPU 持续工作。
- **示例：** 4路 PP 配合4个微批次，MFU 从 1/4 = 25% 提升到 8/14 ≈ 57.1%。
- 更多微批次 → 更高 MFU → 但也意味着更大的有效批次和更多内存占用。

##### 4.1.6 张量并行（TP，Tensor Parallelism）

**思路：** 跨 GPU 切分单个层的权重矩阵（Weight Matrices），并使用分块矩阵乘法（Block Matrix Multiplication）。

**朴素方法的问题：** 计算 XW = Y 后，每块 GPU 持有 Y 的一部分。在进入下一层之前需要一次全规约（All-reduce）操作——此通信无法与计算重叠。

**技巧——配对连续 TP 层：**
- 按列分片（Column-wise Sharding）第一层 W：每块 GPU 计算 XWᵢ = Yᵢ（部分输出）。
- 按行分片（Row-wise Sharding）第二层 U：每块 GPU 计算 YᵢUᵢ = Zᵢ（最终结果的部分输出）。
- 最终结果：Z = Z₁ + Z₂ + Z₃ + Z₄（全规约求和，All-reduce Sum）。
- 两层之间无需通信！只需在配对之后进行一次全规约。

**4路 TP 示例（2个连续层）：**
- 第1层：XW = Y，W 按列切分 [1×1][1×4]——每块 GPU i 计算 XWᵢ = Yᵢ。
- 第2层：YU = Z，U 按行切分 [4×1][1×1]——每块 GPU i 计算 YᵢUᵢ（Z 的部分结果）。
- 最终：Z = Y₁U₁ + Y₂U₂ + Y₃U₃ + Y₄U₄（全规约）。

##### 4.1.7 N 维（ND，N-Dimensional）并行

对于最大规模的模型（如 LLaMA 3 405B），同时使用全部四种并行策略：
- 将 GPU 组织在一个**四维网格（4D Grid）** 中，每块 GPU 的网格坐标给出其在 TP、CP、PP 和 DP 各维度上的等级（Rank）。
- 配置经过优化以最大化模型 FLOPS 利用率（MFU，Model FLOPS Utilization）。

#### 4.2 混合精度训练（Mixed Precision Training）

**核心思想：** 大部分计算使用16位浮点（FP16，16-bit Floating Point）以提升吞吐量（Throughput）、减少内存占用，同时保留一份32位浮点（FP32）的主权重（Master Weights）副本，用于数值稳定（Numerically Stable）的梯度累积（Gradient Accumulation）和优化器更新（Optimizer Update）。

**工作流程：**
1. 以 FP32 保存主权重（Master Weights）。
2. 将权重转换（Cast）为 FP16 用于前向和反向传播。
3. 以 FP16 计算梯度（Gradients）。
4. 将梯度转换回 FP32 用于优化器更新。
5. 以 FP32 更新主权重。

**优势：**
- 激活值（Activations）和梯度（Gradients）的内存减少约2倍。
- 在原生支持 FP16 的张量核心（Tensor Cores）上获得更高吞吐量。
- 使用损失缩放（Loss Scaling）防止 FP16 小梯度下溢（Underflow）。

**结果——精度保持（Accuracy Preservation）：**

| 模型 | 模式 | Top-1 精度 | Top-5 精度 |
|-------------|--------------------------|-----------|-----------|
| AlexNet | FP32 | 58.62% | 81.25% |
| AlexNet | 混合精度（Mixed Precision） | 58.12% | 80.71% |
| Inception V3 | FP32 | 71.75% | 90.52% |
| Inception V3 | 混合精度 | 71.17% | 90.10% |
| ResNet-50 | FP32 | 73.85% | 91.44% |
| ResNet-50 | 混合精度 | 73.60% | 91.11% |

混合精度训练仅造成极小的精度损失（Top-1 约下降0.3–0.6%），同时大幅减少内存占用并提升吞吐量。

#### 4.3 知识蒸馏（Knowledge Distillation，模型蒸馏 Model Distillation）

**核心思想：** 训练一个小"学生"模型（Student Model）来模仿大"教师"模型（Teacher Model）的行为，而非从头在硬标签（Hard Labels）上训练学生模型。

**关键洞察——软标签（Soft Labels）包含更多信息：**
- 硬标签（Hard Labels，独热编码，One-hot Encoding）："这是一只猫" — 仅提供1比特信息。
- 软标签（Soft Labels，教师输出概率）："80%的概率是猫，15%是狗，5%是狐狸" — 提供关于数据相似性结构（Similarity Structure）的丰富信息。

**温度缩放（Temperature Scaling）：**
- 在应用 softmax 之前将教师的 logits 除以"温度"T。
- T 越高 → 概率分布越软（Softer Distribution）→ 迁移的信息越多（More Information Transferred）。
- 学生不仅学习*答案是什么*，还学习*不同类别之间的相似程度（Inter-class Similarity）*。

**结果：** 仅使用教师软标签在3%的数据上训练的学生模型，收敛精度达到57.0%，而教师的精度为58.9%。用97%更少的标注数据（Labeled Data）达到了相当的精度。

---

### 5. 高效训练硬件（Hardware for Efficient Training）

#### 5.1 CPU（中央处理单元，Central Processing Unit）

**英特尔 Xeon Emerald Rapids（2023年）：**
- 最多约64核（Cores）/128线程（Threads）
- DDR5-5600 内存接口（Memory Interface）
- 约350W TDP（热设计功耗，Thermal Design Power）
- 支持 FP16/BF16 的 Intel AMX 和 AVX-512 指令集（Instruction Set）
- Intel 7 工艺节点（Process Node）

CPU 为通用处理器（General-purpose Processor），在深度神经网络训练核心的稠密矩阵乘法（Dense Matrix Multiplication）方面远落后于 GPU 和 TPU。

#### 5.2 GPU（图形处理单元，Graphics Processing Unit）

**英伟达 Ampere A100（2020年）：**
- 19.5 TFLOPS FP32
- 312 / 624 TFLOPS FP16 张量核心（Tensor Core，稠密/稀疏）
- 80 GB HBM2e（高带宽内存，High Bandwidth Memory，约2.0 TB/s）
- 400W TDP
- 600 GB/s NVLink（第3代）

**英伟达 Hopper H100（2022年）：**
- 约67 TFLOPS FP32
- 约1,979 TFLOPS FP16 张量核心（稀疏）
- 80 GB HBM3（约3.35 TB/s 内存带宽）
- 700W TDP
- 900 GB/s NVLink（第4代）

**Hopper vs. Ampere 性能提升：**
- FP16 张量核心吞吐量（Tensor Core Throughput）约提升6倍（1,979 vs. 312 TFLOPS）
- 内存带宽（Memory Bandwidth）提升约68%（3.35 vs. 2.0 TB/s）
- 互联带宽（Interconnect Bandwidth）提升约50%（900 vs. 600 GB/s NVLink）

#### 5.3 Google Cloud TPU

- **Cloud TPU v7（Ironwood）：** 单芯片峰值 FP8 性能约4,614 TFLOPS。
- **TPU Pod（9,216块 Ironwood TPU）：** FP8 性能可扩展至约42.5 **EFLOPS**——远超早期 TPU Pod 的总量，支持下一代 AI 工作负载（Workloads）。

---

## 技术总结

### 推理压缩技术（Inference Compression Techniques）

| 技术 | 移除/改变的内容 | 内存节省 | 计算节省 | 精度影响 |
|-----------|------------------------|---------------|----------------|-----------------|
| 剪枝（Pruning） | 将小权重归零 | 高（稀疏存储，Sparse Storage） | 高（跳过零，Skip Zeros） | 低（配合微调） |
| 权重共享（Weight Sharing） | 将权重聚类为共享值 | 中等（码本，Codebook） | 低 | 低 |
| 量化（Quantization，INT8） | 降至8位精度 | 相比 FP32 节省4倍 | 高（整数 MAC） | 极低 |
| 低秩近似（Low-Rank Approx.） | 矩阵分解（SVD） | 中等 | 中等 | 低 |
| 二值/三值网络（Binary/Ternary） | 将权重限制为 {-1,0,+1} | 相比 FP32 约16倍 | 极高 | 中等 |

### 并行策略比较（Parallelism Strategies Comparison）

| 策略 | 切分维度 | 内存收益 | 通信模式 | 最佳适用场景 |
|----------|----------------|----------------|-----------------------|---------------|
| DP（数据并行） | 批次（Batch） | 无（每块 GPU 保存完整模型） | 梯度全规约（Gradient All-reduce，1次） | 中小型模型 |
| FSDP（全分片） | 无（权重分片） | 随 GPU 数量线性增长 | 3次全聚集（All-gather）+规约（Reduce） | 大模型（100亿+） |
| HSDP（混合分片） | 混合 | 组内线性增长 | 3次本地+1次全局 | 超大模型 |
| CP（上下文并行） | 序列（Sequence） | 无 | 注意力键/值环形（Ring）传递 | 长上下文（Long-context）模型 |
| PP（流水线并行） | 层（Layers） | 随 GPU 数量线性增长 | 激活值点对点（Point-to-point）传递 | 层数多的模型 |
| TP（张量并行） | 隐藏维度（Hidden Dim） | 无（张量分片） | 每对 TP 层2次全规约 | 宽度大的模型 |

### 硬件比较（Hardware Comparison）

| 硬件 | 峰值 FLOPS | 内存带宽（Memory BW） | 互联带宽（Interconnect BW） | 功耗 |
|----------|-----------|-----------|-----------------|-------|
| A100 80GB | 312 TFLOPS FP16 | 2.0 TB/s | 600 GB/s | 400W |
| H100 80GB | 1,979 TFLOPS FP16 | 3.35 TB/s | 900 GB/s | 700W |
| TPU v7 | 4,614 TFLOPS FP8 | — | — | — |

---

## 关键要点

1. **内存主导能耗（Memory Dominates Energy）：** 内存访问所消耗的能量是算术运算的100倍以上。因此，压缩（剪枝、量化）具有双重收益——既减少计算（Compute），又减少内存访问（Memory Access）。

2. **压缩流程（Compression Pipeline）：** 对于推理，标准配方是 训练（Train）→ 剪枝（Prune）→ 再训练（Retrain）→ 量化（Quantize）→ 部署（Deploy）。组合多种压缩技术（如剪枝+量化+权重共享）可获得乘法级别（Multiplicative）的节省。

3. **稀疏性（Sparsity）需要硬件支持：** 压缩模型只有在能够利用稀疏性（如 EIE）或量化（如 TPU 的 INT8 单元）的硬件上才能实现真实的加速。通用 CPU/GPU 在没有专用内核（Specialized Kernels）的情况下可能无法从中受益。

4. **FSDP 支持训练超过单 GPU 内存的模型：** 通过在多块 GPU 之间分片（Shard）权重、梯度和优化器状态，FSDP 随 GPU 数量线性降低每块 GPU 的内存占用。这是训练700亿至4000亿+参数模型的关键。

5. **并行化是多维的（Multi-dimensional Parallelism）：** 现代大语言模型训练同时使用全部四种并行策略（TP + CP + PP + DP），以四维 GPU 网格（4D GPU Grid）进行组织。每种策略都利用不同的硬件拓扑（Hardware Topology）。

6. **流水线气泡（Pipeline Bubbles）是 PP 效率的天敌：** 微批次（Microbatching）是主要解决方案。更多微批次 → 更高 MFU，但也意味着更大的批次大小。理想数量是一个硬件与模型架构联合设计问题（Hardware-Architecture Co-design）。

7. **混合精度（Mixed Precision）几乎是"免费的"：** 从 FP32 切换到混合精度 FP16/FP32 训练，内存大约减半，主要架构的 Top-1 精度下降不超过0.6%。

8. **知识蒸馏利用"暗知识"（Dark Knowledge）：** 教师输出的软概率分布（Soft Probability Distribution）编码了硬标签所丢弃的类间相似性结构（Inter-class Similarity Structure）。在教师软标签仅3%数据上训练的学生模型可以接近教师精度。

9. **算法-硬件协同设计（Algorithm-Hardware Co-Design）至关重要：** 单纯的算法改进或硬件改进都不够。最大效率来自于算法和硬件的协同设计（例如，EIE 专为剪枝+量化模型设计）。

10. **未来指向脑启发式计算（Brain-inspired Computing）：** 从 PC 时代 → 移动优先（Mobile-first）→ AI 优先（AI-first）→ 脑启发/认知计算（Brain-inspired/Cognitive Computing）的演进，反映了向原生支持 AI 工作负载并具备高能源效率的架构转型的趋势。

---

## 参考文献

- **Dally，NIPS'2016 高效深度神经网络方法研讨会** — 展示图像识别（Image Recognition）、语音识别（Speech Recognition）和大语言模型任务中模型规模增长的历史趋势。

- **Karpathy 等，"Deep Visual-Semantic Alignments for Generating Image Descriptions"，2015年** — 作为用于展示90%稀疏率（Sparsity）下剪枝仍能保持图像描述质量的基础 RNN/LSTM 模型。

- **Christopher A Walsh. Peter Huttenlocher（1931–2013）. Nature，502(7470):172–172，2013年** — 为人脑突触剪枝（Synaptic Pruning）的生物学基础提供依据（新生儿1000万亿个突触 → 1岁500万亿 → 青少年50万亿）。

- **Qiu 等，"Going Deeper with Embedded FPGA Platform for Convolutional Neural Network"，FPGA'16** — 展示 CNN 在 FPGA 上的量化结果（精度与位宽权衡）。

- **Zhang 等，"Efficient and Accurate Approximations of Nonlinear Convolutional Networks"，CVPR'15** — 演示卷积层的低秩近似（Low-rank Approximation）。

- **Zhu、Han、Mao、Dally，"Trained Ternary Quantization"，ICLR'17** — TTQ 方法：训练期间学习三值权重（Ternary Weights）、权重演化可视化和卷积核（Kernel）可视化。

- **Han、Song 等，"EIE: Efficient Inference Engine on Compressed Deep Neural Network"，ACM SIGARCH Computer Architecture News 44.3 (2016)** — 专为高效运行稀疏、量化神经网络而设计的 EIE 硬件加速器（Hardware Accelerator）。

---

*笔记整理自 CS6487 第二周讲座幻灯片，2025-2026年度 B 学期。*
