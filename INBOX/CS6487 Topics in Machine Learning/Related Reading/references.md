# CS6487 Topics in Machine Learning — Related Reading

> 本文档汇总了课程 6 周讲义中提到的所有相关阅读材料，包括论文、教程、视频和链接。
> 每条记录注明了**来源周次与背景说明**，方便与笔记对照查阅。

---

## 目录

- [Week 1: Architecture Evolution in CV & NLP](#week-1-architecture-evolution-in-cv--nlp)
- [Week 2: Efficient Deep Learning & Distributed Training](#week-2-efficient-deep-learning--distributed-training)
- [Week 3: Position Embedding in Transformer](#week-3-position-embedding-in-transformer)
- [Week 4: Multi-Objective Optimization in Deep Learning](#week-4-multi-objective-optimization-in-deep-learning)
- [Week 5: Graph Machine Learning (Part 1)](#week-5-graph-machine-learning-part-1)
- [Week 6: Graph Machine Learning (Part 2)](#week-6-graph-machine-learning-part-2)
- [按类型索引](#按类型索引)

---

## Week 1: Architecture Evolution in CV & NLP

> 对应笔记：`notes/week1.md` | 讲师：Dr. Jianyuan Guo

### 论文

| # | 引用 | 页码 | 背景说明 |
|---|------|------|---------|
| W1-P1 | LeCun et al. **"Backpropagation applied to handwritten zip code recognition."** 1989. | p.9, p.13 | LeNet 的奠基工作，证明反向传播可用于 CNN 训练 |
| W1-P2 | LeCun et al. **"Gradient-based learning applied to document recognition."** 1998. | p.9, p.13 | LeNet 完整论文，引入 MNIST 数据集，建立 CNN 体系 |
| W1-P3 | LeCun et al. **"Efficient Backprop."** 1998. | p.22 | 权重初始化与信号归一化的早期方法论文 |
| W1-P4 | Glorot & Bengio. **"Understanding the difficulty of training deep feedforward neural networks."** 2010. | p.22 | Xavier 初始化来源，适用于线性激活函数 |
| W1-P5 | Krizhevsky, Sutskever, Hinton. **"ImageNet Classification with Deep Convolutional Neural Networks."** *NIPS 2012.* | p.14 | AlexNet 论文，开启深度学习时代，ImageNet Top-5 错误率降至 15.3% |
| W1-P6 | Simonyan & Zisserman. **"Very deep convolutional networks for large-scale image recognition."** *arXiv 2014 (ICLR 2015).* | p.17–18 | VGGNet，系统性研究网络深度，使用 3×3 卷积堆叠 |
| W1-P7 | He et al. **"Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification."** *ICCV 2015.* | p.22 | Kaiming（He）初始化，针对 ReLU 激活函数 |
| W1-P8 | Szegedy et al. **"Going deeper with convolutions."** *arXiv 2014 (CVPR 2015).* | p.23 | GoogleNet/Inception V1，多尺度并行卷积 Inception 模块 |
| W1-P9 | Szegedy et al. **"Rethinking the Inception Architecture for Computer Vision."** *arXiv 2015 (CVPR 2016).* | p.24 | Inception V2/V3，因式分解卷积 |
| W1-P10 | Ioffe & Szegedy. **"Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift."** *ICML 2015.* | p.25 | Batch Normalization 原论文，稳定深度网络训练 |
| W1-P11 | He et al. **"Deep Residual Learning for Image Recognition."** *arXiv 2015 (CVPR 2016).* | p.27–32 | ResNet，引入 identity shortcut connection，使 1000+ 层网络成为可能 |
| W1-P12 | Howard et al. **"MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications."** Google, 2017. | p.33–34 | MobileNet V1，深度可分离卷积，大幅降低计算量 |
| W1-P13 | Zhang et al. **"ShuffleNet: An Extremely Efficient Convolutional Neural Network for Mobile Devices."** *CVPR 2018.* | p.35–36 | ShuffleNet V1，分组卷积 + Channel Shuffle |
| W1-P14 | Sandler et al. **"MobileNetV2: Inverted Residuals and Linear Bottlenecks."** *CVPR 2018.* | p.37–38 | MobileNet V2，倒置残差块 + 线性瓶颈 |
| W1-P15 | Ma et al. **"ShuffleNet V2: Practical Guidelines for Efficient CNN Architecture Design."** *ECCV 2018.* | p.41–42 | ShuffleNet V2，超越 FLOPs 的实际效率准则（内存访问代价、分支并行度等）|
| W1-P16 | Han et al. **"GhostNet: More Features from Cheap Operations."** *CVPR 2020.* Huawei. | p.43 | GhostNet，用廉价线性操作生成冗余特征图 |
| W1-P17 | Vaswani et al. **"Attention is all you need."** *NeurIPS 2017.* | p.44 | Transformer 原论文，自注意力机制奠基 |
| W1-P18 | Dosovitskiy et al. **"An image is worth 16x16 words: Transformers for image recognition at scale."** *arXiv 2020 (ICLR 2021).* | p.45 | Vision Transformer (ViT)，将 Transformer 应用于图像 Patch 序列 |
| W1-P19 | Shazeer. **"Glu variants improve transformer."** *arXiv:2002.05202, 2020.* | p.60 | GLU 变体（SwiGLU、GeGLU）改进 Transformer FFN 层 |
| W1-P20 | Google. **"Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity."** [arXiv:2101.03961](https://arxiv.org/abs/2101.03961) | p.61–62 | Switch Transformer，简单稀疏 MoE 路由，扩展至万亿参数 |
| W1-P21 | DeepSeek. **"DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models."** [arXiv:2101.03961](https://arxiv.org/abs/2101.03961) | p.63 | 细粒度专家分割策略，大幅提升组合灵活性 |
| W1-P22 | ByteDance. **"Hyper-Connections."** *ICLR 2025.* [arXiv:2409.19606](https://arxiv.org/pdf/2409.19606) | p.64 | Hyper-Connections，将残差连接推广为多层表示的可学习线性组合 |
| W1-P23 | DeepSeek. **"mHC: Manifold-Constrained Hyper-Connections."** | p.71–75 | mHC，在有界流形约束下稳定 Hyper-Connections 训练，解决范数爆炸问题 |
| W1-P24 | Han et al. **"A survey on vision transformer."** *IEEE TPAMI 45.1 (2022): 87–110.* | p.6 | ViT 变体综述（DeiT、PVT、TNT、Swin 等）|

### 视频

| # | 链接 | 页码 | 背景说明 |
|---|------|------|---------|
| W1-V1 | [Bilibili 视频：What's Next 演示](https://www.bilibili.com/video/BV1S1mXBEEvQ/?spm_id_from=333.337.search-card.all.click&vd_source=c8040ef26040b063f7023f1fa2ed819c) | p.78 | Week 1 末尾"What's Next"部分的补充演示视频 |

### 博客 / 链接

| # | 链接 | 页码 | 背景说明 |
|---|------|------|---------|
| W1-L1 | [HuggingFace: Mixture of Experts Explained](https://huggingface.co/blog/moe) | p.61 | MoE 架构的通俗介绍博客，作为 Switch Transformer 的入门读物引用 |

---

## Week 2: Efficient Deep Learning & Distributed Training

> 对应笔记：`notes/week2.md` | 讲师：Dr. Jianyuan Guo

### 论文

| # | 引用 | 页码 | 背景说明 |
|---|------|------|---------|
| W2-P1 | Dally. **"Efficient Methods for Deep Neural Networks."** *NIPS 2016 Workshop.* | p.3 | 引用以说明模型规模快速增长的历史趋势（图像识别→语音识别→LLM，至 761B 参数）|
| W2-P2 | Karpathy et al. **"Deep Visual-Semantic Alignments for Generating Image Descriptions."** 2015. | p.17 | 以 LSTM 图像描述生成模型为例，演示 90–95% 稀疏度剪枝后仍能生成合理描述 |
| W2-P3 | Walsh. **"Peter Huttenlocher (1931–2013)."** *Nature 502.7470 (2013): 172.* | p.19 | 用人脑突触剪枝（出生时 ~1000 万亿 → 青少年期 ~500 万亿）为 NN 剪枝提供生物学类比 |
| W2-P4 | Qiu et al. **"Going Deeper with Embedded FPGA Platform for Convolutional Neural Network."** *FPGA 2016.* | p.36 | CNN 在 FPGA 上的量化实验结果，展示精度 vs. 位宽权衡 |
| W2-P5 | Zhang et al. **"Efficient and Accurate Approximations of Nonlinear Convolutional Networks."** *CVPR 2015.* | p.38 | 低秩近似（矩阵分解）应用于卷积层的高效推理 |
| W2-P6 | Zhu, Han, Mao, Dally. **"Trained Ternary Quantization."** *ICLR 2017.* | p.41–43 | TTQ，在训练中学习三元权重 {−1, 0, +1}，而非后处理量化 |
| W2-P7 | Han et al. **"EIE: Efficient inference engine on compressed deep neural network."** *ACM SIGARCH 44.3, 2016.* | p.51 | EIE 硬件加速器，专为稀疏量化网络设计，跳过零值计算 |

---

## Week 3: Position Embedding in Transformer

> 对应笔记：`notes/week3.md` | 讲师：Dr. Jianyuan Guo
> 部分内容来自：NeurIPS 2025 Tutorial (Christopher Curtis · Saiph Savage)

### 教程

| # | 引用 | 页码 | 背景说明 |
|---|------|------|---------|
| W3-T1 | Curtis & Savage. **NeurIPS 2025 Tutorial on Positional Encoding.** | p.1 | Week 3 讲义的主要来源之一 |

### 论文

| # | 引用 | 页码 | 背景说明 |
|---|------|------|---------|
| W3-P1 | Vaswani et al. **"Attention is all you need."** *NeurIPS 2017.* | p.36–37 | Transformer 原论文，提出正弦位置编码（APE） |
| W3-P2 | Wang et al. **"Non-local neural networks."** *CVPR 2018.* | p.26 | 引用以说明注意力中点积作为相似度度量的合理性 |
| W3-P3 | Yan et al. **"TENER: Adapting Transformer Encoder for Named Entity Recognition."** 2019. | p.46 | 图示来源，展示正弦编码距离噪声问题 |
| W3-P4 | Shaw, Uszkoreit, Vaswani (Google Brain). **"Self-attention with relative position representations."** *NAACL 2018.* | p.53, p.58 | 提出 RPR，将相对位置直接注入注意力计算 |
| W3-P5 | Dai et al. (Google). **"Transformer-XL: Attentive language models beyond a fixed-length context."** *ACL 2019.* | p.60–64 | 扩展 RPR，加入全局内容/位置偏置和段级递归，支持超长上下文 |
| W3-P6 | Huang et al. (AWS). **"Improve transformer models with better relative position embeddings."** *EMNLP 2020.* | p.65–69 | 提出 M1–M4 四种 RPR 变体，探索 Q、K 与相对距离的不同交互 |
| W3-P7 | Wu et al. (MSRA). **"Da-transformer: Distance-aware transformer."** *NAACL 2021.* | p.70 | 跨注意力头分割位置编码 + 非负约束 |
| W3-P8 | Liu et al. (MSRA). **"Swin Transformer: Hierarchical vision transformer using shifted windows."** *ICCV 2021.* | p.71 | 在视觉领域应用 2D 相对位置偏置，局部窗口内计算 |
| W3-P9 | Su et al. **"RoFormer: Enhanced Transformer with Rotary Position Embedding."** | p.74 | RoPE，旋转位置编码，现为主流解码器 LLM 标准方案（LLaMA、Mistral、DeepSeek 等）|
| W3-P10 | Press et al. (Meta). **"Train short, test long: Attention with linear biases enables input length extrapolation."** *ICLR 2022.* | p.77 | ALiBi，在注意力分数上加固定线性偏置，零参数长度外推 |
| W3-P11 | Kazemnejad et al. (McGill/IBM/Meta). **"The impact of positional encoding on length generalization in transformers."** *NeurIPS 2023.* | p.84 | 研究 NoPE（无位置编码）在短序列合成任务上的效果 |
| W3-P12 | Wang et al. **"Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution."** | p.74 | 将 RoPE 扩展为 M-RoPE，支持多模态 2D/3D 空间位置 |
| W3-P13 | Gong et al. **"Evaluation of Coding Schemes for Transformer-based Gene Sequence Modeling."** 2025. | p.93 | 对比 RoPE 与 ALiBi 在基因序列建模中的表现 |

---

## Week 4: Multi-Objective Optimization in Deep Learning

> 对应笔记：`notes/week4.md` | 讲师：Zhichao Lu (CityUHK)
> 来源：IJCAI 2025 Tutorial on Gradient-based MO DL；CVPR 2023 Tutorial on MOO for DL

### 教程

| # | 引用 | 页码 | 背景说明 |
|---|------|------|---------|
| W4-T1 | **IJCAI 2025 Tutorial on Gradient-based Multi-Objective Deep Learning.** | p.1 | Week 4 讲义主要来源 |
| W4-T2 | **CVPR 2023 Tutorial on Multi-Objective Optimization for Deep Learning.** | p.1 | Week 4 讲义主要来源 |

### 论文

| # | 引用 | 页码 | 背景说明 |
|---|------|------|---------|
| W4-P1 | Arrieta et al. **"Explainable artificial intelligence (XAI): Concepts, taxonomies, opportunities and challenges."** *Information Fusion, 2020.* | p.6 | 准确性 vs. 可解释性的多目标权衡示例 |
| W4-P2 | Gu et al. **"Jet-Nemotron: Efficient language model with post neural architecture search."** *arXiv:2508.15884, 2025.* | p.7 | LLM 性能-速度权衡，实现 21–47× 加速 |
| W4-P3 | Zhong et al. **"Panacea: Pareto alignment via preference adaptation for LLMs."** *NeurIPS 2024.* | p.8 | LLM 对齐作为 MOO：有用性 vs. 无害性冲突 |
| W4-P4 | Luukkonen et al. **"Artificial intelligence in multi-objective drug design."** *Current Opinion in Structural Biology, 2023.* | p.9 | AI 驱动的多目标分子设计 |
| W4-P5 | Liu et al. **"End-to-end multi-task learning with attention."** *CVPR 2019.* | p.25 | DWA（Dynamic Weight Average）损失平衡方法 |
| W4-P6 | Kendall et al. **"Multi-task learning using uncertainty to weigh losses for scene geometry and semantics."** *CVPR 2018.* | p.26 | UW（Uncertainty Weighting），利用不确定性加权各任务损失 |
| W4-P7 | Liu et al. **"Towards impartial multi-task learning."** *ICLR 2021.* | p.27 | IMTL-L（损失平衡）与 IMTL-G（梯度平衡）|
| W4-P8 | Lin et al. **"Dual-balancing for multi-task learning."** *arXiv:2308.12029, 2023.* | p.27 | 证明 IMTL-L 等价于最优不确定性参数下的 log 变换 |
| W4-P9 | Ye et al. **"Multi-objective meta learning."** *NeurIPS 2021.* | p.28 | MOML，双层优化，通过验证集性能自适应学习任务权重 |
| W4-P10 | Liu et al. **"Auto-Lambda: Disentangling dynamic task relationships."** *TMLR 2022.* | p.29 | Auto-λ，MOML 的高效扩展 |
| W4-P11 | Ye et al. **"A first-order multi-gradient algorithm for multi-objective bi-level optimization."** *ECAI 2024.* | p.29 | FORUM，MOML 的一阶高效扩展 |
| W4-P12 | Lin et al. **"Reasonable effectiveness of random weighting: A litmus test for multi-task learning."** *TMLR 2022.* | p.30 | Random Weighting，出奇有效的简单 MTL 基线 |
| W4-P13 | Lin et al. **"Smooth Tchebycheff scalarization for multi-objective optimization."** *ICML 2024.* | p.31 | STCH，Tchebycheff 标量化的平滑近似 |
| W4-P14 | Sener & Koltun. **"Multi-task learning as multi-objective optimization."** *NeurIPS 2018.* | p.35 | MGDA，多梯度下降算法，求解 Pareto 最优解 |
| W4-P15 | Liu et al. **"Conflict-averse gradient descent for multi-task learning."** *NeurIPS 2021.* | p.36 | CAGrad，将更新方向约束在平均梯度附近 |
| W4-P16 | Yu et al. **"Gradient surgery for multi-task learning."** *NeurIPS 2020.* | p.39 | PCGrad，通过投影到冲突梯度法平面解决梯度冲突 |
| W4-P17 | Navon et al. **"Multi-task learning as a bargaining game."** *ICML 2022.* | p.42 | 周期性权重更新加速策略 |
| W4-P18 | Liu et al. **"FAMO: Fast adaptive multitask optimization."** *NeurIPS 2023.* | p.43 | FAMO，无梯度 MGDA 加速，利用损失差异更新权重 |
| W4-P19 | Zhang & Li. **"MOEA/D: A multiobjective evolutionary algorithm based on decomposition."** *IEEE TEVC 11.6 (2007): 712–731.* | p.49 | MOEA/D，基于分解的多目标进化算法框架 |
| W4-P20 | Zitzler & Thiele. **"Multiobjective optimization using evolutionary algorithms."** *PPSN 1998.* | p.56 | Hypervolume 作为 Pareto 前沿近似集的质量指标 |
| W4-P21 | Lin et al. **"Few for many: Tchebycheff set scalarization for many-objective optimization."** *ICLR 2025.* | p.61 | Few for Many（CityUHK），处理目标数 m >> K 的情形 |
| W4-P22 | Ding et al. **"Efficient algorithms for sum-of-minimum optimization."** *ICML 2024.* | p.63 | Sum of Minimal（UCLA），多目标设置下的高效算法 |
| W4-P23 | Chen & Kwok. **"Pareto merging: Multi-objective optimization for preference-aware model merging."** *ICML 2025.* | p.71 | Pareto Merging，模型合并的 MOO 形式化 |
| W4-P24 | Li et al. **"MAP: Low-compute model merging with amortized Pareto fronts via quadratic approximation."** *arXiv:2406.07529, 2024.* | p.75 | MAP，用二次近似高效计算 Pareto 前沿的模型合并 |
| W4-P25 | Yu et al. **"Meta-World: A benchmark and evaluation for multi-task and meta reinforcement learning."** *CoRL 2020.* | p.78 | Meta-World，10/50 目标机器人操控的 MORL 基准 |
| W4-P26 | Rame et al. **"Rewarded soups: Towards Pareto-optimal alignment by interpolating weights fine-tuned on diverse rewards."** *NeurIPS 2023.* | p.84 | Rewarded Soups，插值独立微调权重实现 Pareto 最优 LLM 对齐 |
| W4-P27 | Shi et al. **"Decoding-time language model alignment with multiple objectives."** *NeurIPS 2024.* | p.84 | MOD，在解码时的 logit 空间进行多目标对齐 |
| W4-P28 | Rafailov et al. **"Direct preference optimization: Your language model is secretly a reward model."** *NeurIPS 2023.* | p.87 | DPO，闭合式 RLHF 解法，为 GenARM 提供理论基础 |
| W4-P29 | Xu et al. **"GenARM: Reward guided generation with autoregressive reward model for test-time alignment."** *ICLR 2025.* | p.87 | GenARM，用自回归奖励模型在测试时对齐 LLM |
| W4-P30 | Wang et al. **"Efficient evolutionary search over chemical space with large language models."** *ICLR 2025.* | p.93 | MOLLEO，LLM 驱动的多目标分子设计进化搜索 |
| W4-P31 | Ran et al. **"MOLLM: Multi-objective large language model for molecular design."** *arXiv:2502.12845, 2025.* | p.95 | MO-LLM，通用 LLM 多目标优化平台 |
| W4-P32 | Han et al. **"Training-free multi-objective diffusion model for 3d molecule generation."** *ICLR 2024.* | p.100 | 多目标扩散后验采样，无需重训练生成 3D 分子 |
| W4-P33 | Zhu et al. **"Sample-efficient multi-objective molecular optimization with GFlowNets."** *NeurIPS 2023.* | p.103 | HN-GFN，超网络 GFlowNet 用于多目标分子优化 |
| W4-P34 | Jain et al. **"Multi-objective GFlowNets."** *ICML 2023.* | p.103 | MO-GFlowNet，将 GFlowNet 扩展到多目标设置 |
| W4-P35 | Zhang et al. **"LibMOON: A gradient-based multiobjective optimization library in PyTorch."** *NeurIPS 2024.* | p.109 | LibMOON，开源 PyTorch MOO 库（笔记中 Week 4 > 开源工具 小节）|
| W4-P36 | Lin & Zhang. **"LibMTL: A Python library for deep multi-task learning."** *JMLR 24.209 (2023): 1–7.* | p.115 | LibMTL，开源 PyTorch MTL 库，含 26 种优化策略 |

### 链接

| # | 链接 | 页码 | 背景说明 |
|---|------|------|---------|
| W4-L1 | [RDT (Reversible Data Transforms)](https://github.com/sdv-dev/RDT) | p.91 | 计算分子属性（QED、LogP 等）的工具库 |

---

## Week 5: Graph Machine Learning (Part 1)

> 对应笔记：`notes/week5.md` | 讲师：Zhichao Lu (CityUHK)
> 来源：Stanford CS224W by Prof. Jure Leskovec

### 教程 / 课程

| # | 引用 | 页码 | 背景说明 |
|---|------|------|---------|
| W5-T1 | Leskovec, Jure. **Stanford CS224W: Machine Learning with Graphs.** | p.1 | Week 5 & 6 讲义的主要来源 |

### 论文

| # | 引用 | 页码 | 背景说明 |
|---|------|------|---------|
| W5-P1 | Ying et al. **"Graph Convolutional Neural Networks for Web-Scale Recommender Systems."** *KDD 2018.* | p.33 | PinSage，Pinterest 基于图的推荐系统，边级预测任务 |
| W5-P2 | Zitnik et al. **"Modeling Polypharmacy Side Effects with Graph Convolutional Networks."** *Bioinformatics 2018.* | p.35–36 | 药物-药物相互作用副作用的生物医学图链接预测 |
| W5-P3 | Stokes et al. **"A Deep Learning Approach to Antibiotic Discovery."** *Cell 180.4 (2020): 688–702.* | p.44 | GNN 图分类模型预测有前途的抗生素分子 |
| W5-P4 | Sanchez-Gonzalez et al. **"Learning to simulate complex physics with graph networks."** *ICML 2020.* | p.46–47 | 图网络学习复杂物理模拟（节点=粒子，边=交互）|
| W5-P5 | Konaklieva. **"Molecular targets of β-lactam-based antimicrobials."** *Antibiotics 3.2 (2014): 128–142.* | p.43 | 抗生素分子结构参考（节点=原子，边=化学键）|
| W5-P6 | Shervashidze et al. **"Efficient graphlet kernels for large graph comparison."** *AISTATS 2009.* | p.118 | Graphlet Kernel，图级特征中的图核方法 |
| W5-P7 | Shervashidze et al. **"Weisfeiler-Lehman graph kernels."** *JMLR 12.9, 2011.* | p.118 | WL Kernel，颜色精化算法，判断图同构（笔记中 Week 5 > 图级特征 小节）|
| W5-P8 | Stage et al. **2015.** | p.36 | 证据：Pyrimethamine + Aliskiren → Sarcoma（de novo 药物副作用预测）|
| W5-P9 | Bicker et al. **2017.** | p.36 | 证据：Tolcapone + Pyrimethamine → Breast disorder |
| W5-P10 | Russo et al. **2016.** | p.36 | 证据：Omeprazole + Amoxicillin → Renal tubular acidosis |
| W5-P11 | Banakh et al. **2017.** | p.36 | 证据：Atorvastatin + Amlodipine → Muscle inflammation |
| W5-P12 | Parving et al. **2012.** | p.36 | 证据：Aliskiren + Tioconazole → Breast inflammation |

---

## Week 6: Graph Machine Learning (Part 2)

> 对应笔记：`notes/week6.md` | 讲师：Zhichao Lu (CityUHK)
> 来源：Stanford CS224W by Prof. Jure Leskovec

### 论文

| # | 引用 | 页码 | 背景说明 |
|---|------|------|---------|
| W6-P1 | Perozzi et al. **"DeepWalk: Online Learning of Social Representations."** *KDD 2014.* | p.11, p.47–48 | DeepWalk，最简单随机游走策略，无偏固定长度游走；图示来源（Zachary 空手道俱乐部）|
| W6-P2 | Grover & Leskovec. **"node2vec: Scalable Feature Learning for Networks."** *KDD 2016.* | p.49–50 | node2vec，有偏游走插值 BFS（同质性）与 DFS（结构等价）|
| W6-P3 | Dong et al. **2017.** | p.59 | 基于节点属性的有偏随机游走（异质图 / metapath2vec）|
| W6-P4 | Abu-El-Haija et al. **2017.** | p.59 | 基于可学习权重的有偏随机游走 |
| W6-P5 | Tang et al. **"LINE."** 2015. | p.59 | 直接优化 1-hop 和 2-hop 随机游走概率 |
| W6-P6 | Ribeiro et al. **"struct2vec."** 2017. | p.59 | 在修改后的网络上进行随机游走，捕捉结构身份 |
| W6-P7 | Chen et al. **"HARP."** 2016. | p.59 | 层次化表示学习，在游走方法前对图进行预处理 |
| W6-P8 | Duvenaud et al. **2016.** | p.63 | Approach 1 图级嵌入：节点嵌入求和，应用于分子图分类 |
| W6-P9 | Li et al. **2016.** | p.64 | Approach 2 图级嵌入：引入虚拟超节点连接所有节点 |
| W6-P10 | **"Anonymous Walk Embeddings."** *ICML 2018.* [arXiv:1805.11921](https://arxiv.org/pdf/1805.11921.pdf) | p.65 | Approach 3 图级嵌入：基于匿名游走的图嵌入 |
| W6-P11 | Goyal & Ferrara. **2017 survey.** | p.78 | 节点嵌入方法对比综述（node2vec 在节点分类上更优，其他方法在链接预测上更优）|

### 链接

| # | 链接 | 页码 | 背景说明 |
|---|------|------|---------|
| W6-L1 | [Noise Contrastive Estimation (NCE)](https://arxiv.org/pdf/1402.3722.pdf) | p.41 | 负采样是 NCE 的一种近似形式，作为补充阅读链接提供 |

---

## 按类型索引

### 论文（共 ~100 篇）

按重要性/被引频次排序的核心论文（所有论文已在上方各周次章节列出）：

**基础架构**
- ResNet (He et al., CVPR 2016) → W1-P11
- Transformer / Attention is All You Need (Vaswani et al., NeurIPS 2017) → W1-P17, W3-P1
- Vision Transformer / ViT (Dosovitskiy et al., ICLR 2021) → W1-P18

**高效神经网络**
- MobileNet V1/V2 → W1-P12, W1-P14
- ShuffleNet V1/V2 → W1-P13, W1-P15
- GhostNet → W1-P16

**位置编码**
- RoPE / RoFormer → W3-P9
- ALiBi (Press et al., ICLR 2022) → W3-P10
- Transformer-XL (Dai et al., ACL 2019) → W3-P5
- Swin Transformer (Liu et al., ICCV 2021) → W3-P8

**多目标优化**
- MGDA (Sener & Koltun, NeurIPS 2018) → W4-P14
- PCGrad (Yu et al., NeurIPS 2020) → W4-P16
- DPO (Rafailov et al., NeurIPS 2023) → W4-P28

**图神经网络**
- DeepWalk (Perozzi et al., KDD 2014) → W6-P1
- node2vec (Grover & Leskovec, KDD 2016) → W6-P2
- WL Kernel (Shervashidze et al., JMLR 2011) → W5-P7

### 教程 / 课程

| ID | 资源 | 对应课程内容 |
|----|------|------------|
| W3-T1 | NeurIPS 2025 Tutorial on Positional Encoding | Week 3 |
| W4-T1 | IJCAI 2025 Tutorial on Gradient-based MO DL | Week 4 |
| W4-T2 | CVPR 2023 Tutorial on MOO for DL | Week 4 |
| W5-T1 | Stanford CS224W: Machine Learning with Graphs | Week 5 & 6 |

### 视频

| ID | 资源 | 对应课程内容 |
|----|------|------------|
| W1-V1 | [Bilibili 演示视频](https://www.bilibili.com/video/BV1S1mXBEEvQ/) | Week 1 末尾 |

### 博客 / 网页链接

| ID | 资源 | 对应课程内容 |
|----|------|------------|
| W1-L1 | [HuggingFace MoE Blog](https://huggingface.co/blog/moe) | Week 1: MoE 入门 |
| W4-L1 | [GitHub: sdv-dev/RDT](https://github.com/sdv-dev/RDT) | Week 4: 分子属性计算 |
| W6-L1 | [NCE 论文 arXiv](https://arxiv.org/pdf/1402.3722.pdf) | Week 6: 负采样原理 |

---

*最后更新：2026-02-28*
