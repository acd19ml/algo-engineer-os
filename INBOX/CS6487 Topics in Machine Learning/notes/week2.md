# Week 2: Efficient Deep Learning and Large-Scale Distributed Training

**Course:** CS6487 Topics in Machine Learning
**Instructor:** Dr. Jianyuan Guo
**Semester:** SemB 2025-2026, Dept. CS, CityU

---

## Overview

Deep learning has fundamentally transformed many domains (self-driving cars, machine translation, AlphaGo, smart robotics). However, as models grow ever larger — from hundreds of billions to trillions of parameters — three fundamental engineering challenges emerge: **model size**, **training speed**, and **energy efficiency**. This lecture surveys the algorithmic and hardware techniques that together constitute the field of *efficient deep learning*, covering both inference-time compression and large-scale distributed training.

The unifying framework is **Algorithm-Hardware Co-Design**: efficient systems require co-optimizing algorithms (compression, parallelism) and hardware (accelerators, memory hierarchies) together, across two axes:

- **Inference axis:** compress/optimize a trained model for fast, cheap deployment.
- **Training axis:** make the training process itself faster and more scalable.

---

## Key Concepts

### 1. The Three Challenges of Deep Learning at Scale

#### 1.1 Model Size
- Large models are difficult to distribute for over-the-air updates (e.g., on mobile devices).
- LLMs have grown to hundreds of billions of parameters: Deepseek (761B MoE), LLaMA 3 405B dense.
- Compute requirements are staggering: 250 GFLOP/Token to 2448 GFLOP/Token for modern LLMs.

#### 1.2 Speed
- Training time scales with model depth. Benchmarks on four M40 GPUs show:

| Model     | Error Rate | Training Time |
|-----------|-----------|---------------|
| ResNet18  | 10.76%    | 2.5 days      |
| ResNet50  | 7.02%     | 5 days        |
| ResNet101 | 6.21%     | 1 week        |
| ResNet152 | 6.16%     | 1.5 weeks     |

- Long training times directly limit ML researcher productivity and iteration speed.

#### 1.3 Energy Efficiency
- AlphaGo required 1,920 CPUs and 280 GPUs, costing ~$3,000 per game in electricity.
- On mobile: large models drain batteries quickly.
- In data centers: energy usage increases Total Cost of Ownership (TCO).
- Key insight: **larger model → more memory references → more energy consumed.** Memory access energy is >100x the energy of arithmetic operations, making memory efficiency paramount.

---

### 2. Algorithms for Efficient Inference

The five main algorithmic approaches for compressing and accelerating inference are:

1. **Pruning**
2. **Weight Sharing**
3. **Quantization**
4. **Low Rank Approximation**
5. **Binary / Ternary Networks**

#### 2.1 Pruning

**Core Idea:** Remove redundant weights (synapses) from a trained neural network, similar to how the human brain prunes synaptic connections during development (from ~1,000 trillion synapses at birth to ~500 trillion in adolescence).

**The standard 3-step pipeline:**
1. **Train** — Train the full, dense network normally.
2. **Prune** — Remove weights below a threshold (e.g., set small-magnitude weights to zero). The weight distribution shifts: before pruning there is a bell curve around zero; after pruning those near-zero weights are removed.
3. **Retrain (Fine-tune)** — Recover accuracy lost due to pruning by fine-tuning the sparse network.

**Effect on Weight Distribution:**
- Before pruning: weights follow a bell-curve distribution centered near zero.
- After pruning: the near-zero weights are gone, leaving a bimodal distribution.
- After retraining: the distribution re-adjusts with remaining weights spreading out.

**Pruning RNNs/LSTMs/LLMs:**
- Even at 90% sparsity, pruned language models generate semantically equivalent captions/descriptions:
  - "a basketball player in a white uniform is playing with a ball" → (90% pruned) → "a basketball player in a white uniform is playing with a basketball"
  - "a brown dog is running through a grassy field" → (90% pruned) → "a brown dog is running through a grassy area"
- At 95% sparsity, some degradation begins to appear in generated text.

**Biological Analogy:** Human synaptic pruning is an inspiration — the brain prunes unused connections while retaining critical pathways, improving efficiency without sacrificing capability.

#### 2.2 Weight Sharing

**Core Idea:** Force groups of weights to share a single representative value, reducing the effective number of distinct parameters that need to be stored.

**Mechanism:**
1. Cluster weights into K groups (e.g., using k-means clustering).
2. Replace each weight with its cluster centroid value.
3. Store only the codebook (K centroid values) and an index per weight.
4. Example: weights {2.09, 2.12, 1.92, 1.87} all map to the shared value 2.0.

**Visualization:** After training with weight sharing, the weight distribution becomes discrete — clustering into a small number of distinct values rather than a continuous distribution.

**Bit Efficiency:** Fewer bits are needed to represent the cluster index than the original floating point weight. The number of bits required depends on the number of clusters K: log2(K) bits per weight index.

#### 2.3 Quantization

**Core Idea:** Reduce numerical precision of weights and activations from 32-bit floating point to lower bit-widths (e.g., 8-bit integers, FP16).

**Workflow:**
1. Train the model in full float32 precision.
2. Gather statistics on weight and activation distributions.
3. Perform quantization (map float values to fixed-point discrete values).
4. Fine-tune in float format to recover accuracy.
5. Convert to fixed-point format for deployment.

**Example (8-bit quantization):**
- Weights are mapped to 256 discrete values (2^8).
- Activations are similarly quantized.
- Memory footprint reduced by 4x vs FP32 (8-bit vs 32-bit).

**Results (Qiu et al., FPGA'16):** 8-bit quantized CNNs can match or closely approximate the accuracy of their float32 counterparts while significantly reducing compute and memory requirements.

#### 2.4 Low Rank Approximation

**Core Idea:** Decompose large weight matrices (especially in convolutional layers) into products of smaller matrices using techniques like Singular Value Decomposition (SVD).

**For Conv Layers:**
- A large convolution kernel can be decomposed into a sequence of smaller kernels.
- Reduces both parameter count and computation.
- Zhang et al. (CVPR'15) showed this can be done efficiently for nonlinear convolutional networks.

#### 2.5 Binary / Ternary Networks

**Core Idea:** Push quantization to the extreme — restrict weights to only 2 values {-1, +1} (Binary) or 3 values {-1, 0, +1} (Ternary).

**Trained Ternary Quantization (TTQ) — Zhu, Han, Mao, Dally, ICLR'17:**
- Weights are learned to be ternary during training (not just post-hoc quantized).
- Two scale factors (for positive and negative weights) are also learned.
- Reduces weight memory by ~16x vs FP32.
- Weight evolution during training: weights start distributed, then gradually converge to ternary values as training progresses.
- Visualization of TTQ kernels shows clear separation into three value clusters.

---

### 3. Hardware for Efficient Inference

#### 3.1 Specialized Inference Accelerators

| Accelerator | Developer | Key Feature |
|-------------|-----------|-------------|
| Eyeriss     | MIT       | RS (Row Stationary) Dataflow |
| DaDiannao   | CAS       | eDRAM on-chip memory |
| TPU         | Google    | 8-bit integer arithmetic |
| NPU         | Huawei    | Neural Processing Unit |

#### 3.2 Google TPU (Tensor Processing Unit)

The TPU is purpose-built for neural network inference with 8-bit integer arithmetic:
- **Matrix Unit:** 65,536 (256×256) 8-bit multiply-accumulate units
- **Clock rate:** 700 MHz
- **Peak throughput:** 92 TOPS (tera-operations per second) = 65,536 × 2 × 700M
- **MAC advantage:** >25x more MACs than a GPU, >100x more than a CPU
- **On-chip memory:**
  - 4 MiB of Accumulator memory
  - 24 MiB of Unified Buffer (3.5x more than GPU)
- **Off-chip:** 8 GiB DDR3 DRAM (two channels at 2133 MHz)

#### 3.3 Roofline Model

The Roofline model identifies whether a computation is **compute-bound** or **memory-bandwidth-bound**:
- **Compute bound:** FLOPS/second is the bottleneck → need faster compute units.
- **Memory bound:** Memory bandwidth is the bottleneck → need better data reuse or compression.

**Why models often fall below the roofline:**
- Low latency requirements prevent large batch sizes → low operational intensity (ops/byte).
- **Solution:** Compress the model to reduce memory footprint.
- **Challenge:** Hardware must be able to efficiently execute on the compressed (sparse) model.

#### 3.4 EIE: Efficient Inference Engine

**EIE (Han et al., ACM SIGARCH 2016)** is a specialized hardware accelerator designed to run compressed (sparse + quantized) networks:
- Exploits sparsity in both weights and activations.
- Rule of thumb: `0 * A = 0` and `W * 0 = 0` → skip all zero multiplications.
- Custom dataflow skips zero computations directly in hardware.
- **Result:** Significant throughput and energy efficiency improvements vs CPU/GPU on compressed models.

---

### 4. Algorithms for Efficient Training

Three major approaches:

1. **Parallelization** (across multiple GPUs/nodes)
2. **Mixed Precision Training** (FP16 + FP32)
3. **Model Distillation** (knowledge transfer)

#### 4.1 Parallelization Strategies

Modern LLM training clusters are enormous. Meta's Llama 3 cluster:
- **GPU:** H100 with 3,352 GB/sec on-chip bandwidth
- **Server:** 8x GPUs, 900 GB/sec GPU-to-GPU (NVLink)
- **Rack:** 2 servers = 16 GPUs
- **Pod:** 192 racks = 3,072 GPUs, 50 GB/sec between servers
- **Cluster:** 8 pods = **24,576 GPUs**
- **Total:** 1.875 PB GPU memory, 415M FP32 cores, 13M Tensor Cores, 24.3 EFLOP/sec

A model with L layers operates on tensors of shape `(Batch, Sequence, Dim)`. The four parallelism strategies each split a different dimension:

| Strategy | Abbreviation | Dimension Split |
|----------|-------------|-----------------|
| Data Parallelism | DP | Batch dimension |
| Context Parallelism | CP | Sequence dimension |
| Pipeline Parallelism | PP | Layer (L) dimension |
| Tensor Parallelism | TP | Hidden (Dim) dimension |

##### 4.1.1 Data Parallelism (DP)

**Idea:** Use a minibatch of size M×N, split over M GPUs. Since gradients are linear, each GPU computes gradients independently, then they are averaged.

**Step-by-step workflow:**
1. Each GPU has its own complete copy of the model and optimizer.
2. Each GPU loads its own batch of N data samples.
3. Each GPU runs forward pass to compute loss Li.
4. Each GPU runs backward pass to compute gradients dLi/dWj.
5. Average gradients across all M GPUs: dL/dWj = (1/M) Σ dLi/dWj.
6. Each GPU updates its own weights using the averaged gradient.

**Optimization:** Steps 4 (backward) and 5 (gradient sync) can be overlapped — begin communicating gradients for layer j while still computing gradients for layer j-1 (gradient bucketing).

**Key limitation:** Each GPU must hold the entire model in memory. With the Adam optimizer, each weight requires 4 numbers (weight, gradient, first moment β1, second moment β2), and each number uses 2 bytes (FP16):
- 1B parameters → 8 GB
- 10B parameters → 80 GB (fills a single H100 GPU)
- 70B+ parameters → requires model sharding

**Solution:** Fully Sharded Data Parallelism (FSDP).

##### 4.1.2 Fully Sharded Data Parallelism (FSDP)

**Idea:** Split model weights across GPUs. Each weight Wi is "owned" by exactly one GPU, which also stores its gradients and optimizer states.

**FSDP Algorithm (forward + backward pass):**
1. **Before forward for layer i:** The owner GPU broadcasts Wi to all other GPUs.
2. **All GPUs** run the forward pass for layer i using Wi, then **delete** their local copy of Wi (to save memory).
3. **Before backward for layer i:** The owner GPU broadcasts Wi again.
4. **All GPUs** run backward for layer i to compute local dL/dWi, then delete their local Wi.
5. **After backward for layer i:** Each GPU sends its local dL/dWi to the owner GPU, then deletes its local gradient.
6. **Owner GPU** performs the gradient update (Wi += -lr × dL/dWi).

**Optimizations:**
- **Prefetching:** While computing forward with Wi, pre-fetch Wi+1 in the background.
- **End-of-forward optimization:** Don't delete the last weight fetched at the end of forward to avoid immediately re-fetching it for backward.
- **Pipeline overlap:** While doing backward with Wi, simultaneously send/update Wi+1 gradients and fetch Wi-1.
- **Data prefetch:** Next batch data can be pre-fetched during forward + backward of current batch.

##### 4.1.3 Hybrid Sharded Data Parallelism (HSDP)

**Idea:** Combine FSDP with DP using a 2D grid of GPUs:
- Split N = M × K GPUs into M groups of K GPUs.
- Within each group of K GPUs: use FSDP (weight sharding).
- Across the M groups: use standard DP (gradient averaging).

**Communication pattern:**
- 3× high-bandwidth communication **inside** each group: Wi (forward), Wi (backward), dL/dWi (backward). Keep same-group GPUs on same node/pod.
- 1× lower-bandwidth communication **across** groups: only dL/dWi in backward. Can use slower inter-pod links.

##### 4.1.4 Context Parallelism (CP)

**Idea (for Transformers):** Process a single long sequence across multiple GPUs, splitting the sequence dimension.

**Component handling:**
- **Normalization and residual connections:** Trivially parallelizable (no weights, no cross-token dependencies beyond the sequence split).
- **MLP layers:** Each GPU holds a copy of MLP weights; activations are split by sequence position; gradients synced as in DP.
- **QKV Projection:** Same as MLP — parallelize over sequence, sync gradients.
- **Attention operator:** Hardest due to global attention dependencies. Two options:

**Option 1 — Ring Attention:**
- Divide Q, K, V into blocks and distribute over GPUs.
- Inner loop iterates over key/value blocks (communicated via a ring topology).
- Outer loop iterates over query blocks (local).
- Complex to implement but scales to arbitrarily long sequences.

**Option 2 — Ulysses Attention:**
- Parallelize over attention heads in multi-head attention.
- Don't try to distribute the attention matrix itself.
- Simpler to implement.
- Limitation: maximum parallelism = number of attention heads.

##### 4.1.5 Pipeline Parallelism (PP)

**Idea:** Split the L layers of the model across GPUs. Each GPU handles a subset of layers. Activations are passed (copied) between GPUs at layer boundaries.

**Problem:** Sequential dependencies create idle time ("bubbles"). A GPU cannot process the next layer until it receives activations from the previous GPU. With N-way PP, the naive maximum Model FLOPS Utilization (MFU) is 1/N.

**Solution — Microbatching:**
- Split each batch into multiple smaller microbatches.
- Pipeline microbatches through GPUs so that GPUs stay busy.
- **Example:** 4-way PP with 4 microbatches raises MFU from 1/4 = 25% to 8/14 ≈ 57.1%.
- More microbatches → higher MFU → but also larger effective batch size and more memory.

##### 4.1.6 Tensor Parallelism (TP)

**Idea:** Split the weight matrices of individual layers across GPUs and use block matrix multiplication.

**Naive approach issue:** After computing XW = Y, GPUs each hold a partition of Y. A gather (all-reduce) operation is needed before the next layer — this communication cannot be overlapped with computation.

**Trick — Pair consecutive TP layers:**
- Shard the first layer W over columns: each GPU computes XWi = Yi (a partial output).
- Shard the second layer U over rows: each GPU computes YiUi = Zi (a partial output of the final result).
- Final result: Z = Z1 + Z2 + Z3 + Z4 (all-reduce sum).
- No communication is needed between the two layers! Only one all-reduce after the pair.

**4-way TP example (2 consecutive layers):**
- Layer 1: XW = Y, where W is split column-wise [1×1][1×4] — each GPU i computes XWi = Yi.
- Layer 2: YU = Z, where U is split row-wise [4×1][1×1] — each GPU i computes YiUi (partial Z).
- Final: Z = Y1U1 + Y2U2 + Y3U3 + Y4U4 (all-reduce).

##### 4.1.7 N-Dimensional (ND) Parallelism

For the largest models (e.g., LLaMA 3 405B), all four parallelism strategies are used simultaneously:
- Organize GPUs in a **4D grid** where each GPU's grid index gives its rank along each of the TP, CP, PP, and DP dimensions.
- The configuration is optimized to maximize Model FLOPS Utilization (MFU).

#### 4.2 Mixed Precision Training

**Core Idea:** Use 16-bit floating point (FP16) for most computations to increase throughput and reduce memory, but maintain a master copy of weights in 32-bit float (FP32) for numerically stable gradient accumulation and optimizer updates.

**Workflow:**
1. Keep master weights in FP32.
2. Cast weights to FP16 for forward and backward passes.
3. Compute gradients in FP16.
4. Cast gradients back to FP32 for optimizer update.
5. Update master weights in FP32.

**Benefits:**
- ~2x reduction in memory for activations and gradients.
- Higher throughput on Tensor Cores (which operate on FP16 natively).
- Loss scaling is used to prevent FP16 underflow of small gradients.

**Results — Accuracy preservation:**

| Model       | Mode                     | Top-1 Acc | Top-5 Acc |
|-------------|--------------------------|-----------|-----------|
| AlexNet     | FP32                     | 58.62%    | 81.25%    |
| AlexNet     | Mixed Precision          | 58.12%    | 80.71%    |
| Inception V3 | FP32                    | 71.75%    | 90.52%    |
| Inception V3 | Mixed Precision         | 71.17%    | 90.10%    |
| ResNet-50   | FP32                     | 73.85%    | 91.44%    |
| ResNet-50   | Mixed Precision          | 73.60%    | 91.11%    |

Mixed precision training incurs only minimal accuracy loss (~0.3-0.6% top-1) while dramatically reducing memory and increasing throughput.

#### 4.3 Knowledge Distillation (Model Distillation)

**Core Idea:** Train a small "student" model to mimic the behavior of a large "teacher" model, rather than training the student from scratch on hard labels.

**Key insight — Soft labels carry more information:**
- Hard labels (one-hot): "this is a cat" — provides only 1 bit of information.
- Soft labels (teacher output probabilities): "80% cat, 15% dog, 5% fox" — provides rich information about the similarity structure of the data.

**Temperature Scaling:**
- Divide the teacher's logits by a "temperature" T before applying softmax.
- Higher T → softer probability distribution → more information transferred.
- The student learns not just *what* the answer is, but *how similar* different classes are.

**Result:** A student model trained on only 3% of the data using soft labels from the teacher converges to 57.0% accuracy, vs. the teacher's 58.9%. Achieving comparable accuracy with 97% less labeled data.

---

### 5. Hardware for Efficient Training

#### 5.1 CPUs

**Intel Xeon Emerald Rapids (2023):**
- Up to ~64 cores / 128 threads
- DDR5-5600 memory interface
- ~350W TDP
- Intel AMX & AVX-512 with FP16/BF16 support
- Intel 7 process node

CPUs are general-purpose but fall far behind GPUs and TPUs for the dense matrix multiplications at the core of DNN training.

#### 5.2 GPUs

**Nvidia Ampere A100 (2020):**
- 19.5 TFLOPS FP32
- 312 / 624 TFLOPS FP16 Tensor Core (dense / sparse)
- 80 GB HBM2e (~2.0 TB/s memory bandwidth)
- 400W TDP
- 600 GB/s NVLink (3rd Gen)

**Nvidia Hopper H100 (2022):**
- ~67 TFLOPS FP32
- ~1,979 TFLOPS FP16 Tensor Core (sparse)
- 80 GB HBM3 (~3.35 TB/s memory bandwidth)
- 700W TDP
- 900 GB/s NVLink (4th Gen)

**Hopper vs Ampere improvements:**
- ~6x FP16 Tensor Core throughput (1,979 vs 312 TFLOPS)
- ~68% more memory bandwidth (3.35 vs 2.0 TB/s)
- ~50% more interconnect bandwidth (900 vs 600 GB/s NVLink)

#### 5.3 Google Cloud TPU

- **Cloud TPU v7 (Ironwood):** up to ~4,614 TFLOPS peak FP8 per chip.
- **TPU Pod (9,216 Ironwood TPUs):** scales to ~42.5 **exaflops** of FP8 performance — exceeding earlier TPU pod totals by a large margin and supporting next-generation AI workloads.

---

## Techniques Summary

### Inference Compression Techniques

| Technique | What is Removed/Changed | Memory Saving | Compute Saving | Accuracy Impact |
|-----------|------------------------|---------------|----------------|-----------------|
| Pruning | Zero out small weights | High (sparse storage) | High (skip zeros) | Low (with fine-tuning) |
| Weight Sharing | Cluster weights to shared values | Moderate (codebook) | Low | Low |
| Quantization (INT8) | Reduce precision to 8-bit | 4x vs FP32 | High (integer MACs) | Very low |
| Low Rank Approx. | Decompose matrices (SVD) | Moderate | Moderate | Low |
| Binary/Ternary Nets | Restrict weights to {-1,0,+1} | ~16x vs FP32 | Very high | Moderate |

### Parallelism Strategies Comparison

| Strategy | Dimension Split | Memory Benefit | Communication Pattern | Best Use Case |
|----------|----------------|----------------|-----------------------|---------------|
| DP | Batch | None (full model on each GPU) | Gradient all-reduce (1x) | Small-medium models |
| FSDP | N/A (weight sharding) | Linear with GPU count | 3x all-gather + reduce | Large models (10B+) |
| HSDP | Hybrid | Linear within group | 3x local + 1x global | Very large models |
| CP | Sequence | None | Attention key/value ring | Long-context models |
| PP | Layers | Linear with GPU count | Activation point-to-point | Layer-heavy models |
| TP | Hidden dim | None (tensor sharded) | 2x all-reduce per TP pair | Wide models |

### Hardware Comparison

| Hardware | Peak FLOPS | Memory BW | Interconnect BW | Power |
|----------|-----------|-----------|-----------------|-------|
| A100 80GB | 312 TFLOPS FP16 | 2.0 TB/s | 600 GB/s | 400W |
| H100 80GB | 1,979 TFLOPS FP16 | 3.35 TB/s | 900 GB/s | 700W |
| TPU v7 | 4,614 TFLOPS FP8 | — | — | — |

---

## Key Takeaways

1. **Memory dominates energy:** Over 100x more energy is spent on memory access than arithmetic. Compression (pruning, quantization) is thus doubly beneficial — less compute AND less memory access.

2. **The compression pipeline:** For inference, the standard recipe is Train → Prune → Retrain → Quantize → Deploy. Combining multiple compression techniques (e.g., pruning + quantization + weight sharing) gives multiplicative savings.

3. **Sparsity requires hardware support:** Compressed models only yield real-world speedups on hardware that can exploit sparsity (like EIE) or quantization (like TPU's INT8 units). Generic CPUs/GPUs may not benefit without specialized kernels.

4. **FSDP enables training models that exceed single-GPU memory:** By sharding weights, gradients, and optimizer states across many GPUs, FSDP linearly reduces per-GPU memory with GPU count. Key to training 70B–400B+ parameter models.

5. **Parallelism is multidimensional:** Modern LLM training uses all four parallelism strategies simultaneously (TP + CP + PP + DP) organized in a 4D GPU grid. Each strategy exploits different hardware topology (fast NVLink for TP, slower inter-pod for DP).

6. **Pipeline bubbles are the enemy of PP efficiency:** Microbatching is the primary solution. More microbatches → higher MFU, but also larger batch sizes. The ideal number is a hardware and model-architecture co-design problem.

7. **Mixed precision is nearly free:** Switching from FP32 to mixed precision FP16/FP32 training cuts memory roughly in half with <0.6% top-1 accuracy degradation across major architectures.

8. **Knowledge distillation leverages "dark knowledge":** Soft probability distributions from a teacher encode inter-class similarity structure that hard labels discard. A student trained on soft labels from 3% of data can approach teacher accuracy.

9. **Algorithm-hardware co-design is essential:** Neither algorithmic improvements nor hardware improvements alone are sufficient. Maximum efficiency comes from designing algorithms and hardware in tandem (e.g., EIE designed specifically for pruned + quantized models).

10. **The future points toward brain-inspired computing:** The progression from PC-era → Mobile-first → AI-first → Brain-inspired/Cognitive computing reflects a shift toward architectures that natively handle AI workloads with high energy efficiency.

---

## References Mentioned

- **Dally, NIPS'2016 workshop on Efficient Methods for Deep Neural Networks** — cited on slide 3 (page 3) to show the historical trend of growing model sizes across image recognition, speech recognition, and LLM tasks.

- **Karpathy et al., "Deep Visual-Semantic Alignments for Generating Image Descriptions," 2015** — cited on slide 17 (page 17) as the base RNN/LSTM model used to demonstrate that pruning even at 90% sparsity preserves caption quality.

- **Christopher A Walsh. Peter Huttenlocher (1931–2013). Nature, 502(7470):172–172, 2013** — cited on slide 19 (page 19) to provide the biological basis for synaptic pruning in the human brain (newborn 1,000T → 1-year-old 500T → adolescent 50T synapses).

- **Qiu et al. "Going Deeper with Embedded FPGA Platform for Convolutional Neural Network," FPGA'16** — cited on slide 36 (page 36) to show quantization results (accuracy vs bit-width trade-off) for CNNs on FPGA.

- **Zhang et al. "Efficient and Accurate Approximations of Nonlinear Convolutional Networks," CVPR'15** — cited on slide 38 (page 38) to demonstrate low-rank approximation of convolutional layers.

- **Zhu, Han, Mao, Dally. "Trained Ternary Quantization," ICLR'17** — cited on slides 41–43 (pages 41–43) for the TTQ method: learned ternary weights during training, weight evolution visualization, and kernel visualization.

- **Han, Song, et al. "EIE: Efficient Inference Engine on Compressed Deep Neural Network," ACM SIGARCH Computer Architecture News 44.3 (2016)** — cited on slide 51 (page 51) for the EIE hardware accelerator designed to efficiently run sparse, quantized neural networks.

---

*Notes compiled from CS6487-Week2 lecture slides, SemB 2025-2026.*
