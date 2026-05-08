# Week 1: Architecture Evolution in CV & NLP

**Course:** CS6487 Topics in Machine Learning
**Instructor:** Dr. Jianyuan Guo
**Term:** SemB 25-26, Dept. CS, CityU

---

## Overview

This week covers the historical and technical evolution of neural network architectures across two major domains: Computer Vision (CV) and Natural Language Processing (NLP). The lecture traces a coherent narrative from early convolutional networks (1989) through modern transformer-based large language models (2025), emphasizing the recurring engineering principles that drove progress at each stage.

**Core themes:**
- Representation learning and the role of depth in neural networks
- Solving the gradient vanishing/exploding problem via shortcut connections
- Efficient neural network design for edge deployment
- The Mixture-of-Experts (MoE) paradigm for scaling LLMs
- Hyper-connections as a generalization of residual shortcuts

---

## Key Concepts

### 1. Representation Learning

Representation learning is the idea that neural networks can automatically learn useful feature representations from raw data, rather than relying on hand-crafted features. Deep networks learn hierarchical representations:

- **Early layers** capture low-level features (edges, textures)
- **Middle layers** capture mid-level features (parts, shapes)
- **Deep layers** capture high-level semantic features (objects, categories)

The XOR problem historically motivated multi-layer networks: a single linear layer cannot separate XOR, but a hidden layer can learn a non-linear representation that makes the problem linearly separable.

**Backpropagation** (LeCun et al., 1989) made training multi-layer networks practical by efficiently computing gradients through the chain rule.

---

### 2. The Gradient Vanishing / Exploding Problem

As networks get deeper, gradients can either:
- **Vanish**: become exponentially small during backpropagation, making early layers learn very slowly
- **Explode**: grow exponentially large, causing unstable training

This is a core challenge that motivated both better initialization strategies and architectural innovations (residual connections).

**Signals during forward and backward pass must be normalized** to prevent accumulation of scale errors across many layers.

---

### 3. Network Initialization

Good initialization ensures signals do not vanish or explode at the start of training.

| Method | Target | Formula | PyTorch API |
|---|---|---|---|
| Xavier Init | Linear activations | `n * Var(w) = 1` | `torch.nn.init.xavier_uniform_()` |
| Kaiming Init | ReLU activations | `n * Var(w) = 2` | `torch.nn.init.kaiming_uniform_()` |

Both methods derive from analytical assumptions (e.g., Gaussian weight distributions) about how variance propagates through layers. Xavier is suited for symmetric activations (tanh, sigmoid), while Kaiming accounts for the dead-neuron behavior of ReLU (which zeroes half the output on average).

**Key references:**
- "Efficient Backprop" — LeCun et al., 1998
- Xavier: "Understanding the difficulty of training deep feedforward neural networks" — Glorot & Bengio, 2010
- Kaiming: "Delving Deep into Rectifiers" — He et al., ICCV 2015

---

### 4. Normalization Modules

Normalization layers stabilize the distribution of activations during training, reducing sensitivity to initialization and enabling higher learning rates.

- **Batch Normalization (BN):** Normalizes over the batch dimension. Effective for CNNs with large batches. Proposed by Ioffe & Szegedy (ICML 2015).
- **Layer Normalization (LN):** Normalizes over the feature dimension. Standard in Transformers.
- **Other variants:** Group Norm, Instance Norm, etc. — useful in settings where batch size is small or features are spatial.

**Key role:** BN allowed training of much deeper networks by keeping activations in a reasonable range throughout training ("reducing internal covariate shift").

---

### 5. Shortcut Connections (Residual Learning)

Shortcut (skip/residual) connections are the single most important architectural innovation for enabling very deep networks. Instead of learning a direct mapping `H(x)`, the network learns the **residual** `F(x) = H(x) - x`, making the identity mapping trivially learnable.

```
Output = F(x) + x
       (residual + identity shortcut)
```

**Why this works:**
- The gradient can flow directly through the identity path, bypassing non-linear transformations
- Even if intermediate layers learn small refinements, the identity shortcut preserves useful information
- Enables networks with hundreds or even thousands of layers

This principle generalizes far beyond ResNet: it appears in Transformers (LayerNorm + residual), Hyper-Connections, and many modern architectures.

---

### 6. Efficient Neural Networks (Edge Deployment)

Three architectural techniques dramatically reduce computation cost for mobile/edge devices:

#### Depthwise Separable Convolution (MobileNet)
A standard convolution is decomposed into two cheaper steps:
1. **Depthwise conv:** Apply one filter per input channel (captures spatial patterns within each channel independently)
2. **Pointwise conv (1x1):** Mix information across channels

**Cost reduction:** From `H*W*Cin*Cout*K*K` to `H*W*Cin*K*K + H*W*Cin*Cout` — roughly `1/Cout + 1/K^2` of the original cost.

#### Group Convolution + Channel Shuffle (ShuffleNet)
- **Group convolution:** Split channels into G groups; convolutions run independently within each group
- **Problem:** Groups cannot exchange information across boundaries
- **Channel Shuffle:** Permute channels before the next group conv to allow cross-group communication

#### Inverted Residual with Linear Bottleneck (MobileNet V2)
- Traditional bottleneck: wide → narrow → wide (compress then expand)
- Inverted residual: narrow → wide → narrow (expand then compress)
- The expansion gives the depthwise conv more channels to work with, improving expressiveness
- The final linear (no-activation) bottleneck preserves the manifold structure of features

#### Ghost Module (GhostNet)
- Many feature maps in CNNs are redundant (one map is a linear transformation of another)
- GhostNet generates a small set of "intrinsic" feature maps with normal convolution, then generates "ghost" maps cheaply via linear operations
- Achieves similar accuracy as full-width networks at much lower FLOPs

---

### 7. Mixture-of-Experts (MoE)

MoE replaces a single dense Feed-Forward Network (FFN) layer in a Transformer with a set of `N` expert networks, and a **router/gating network** that selects which experts to activate for each token.

**Sparse activation:** Only a subset (e.g., top-2 out of 16) of experts are active for any given input, so the total computation per token stays manageable even as the total number of parameters grows.

**Combinatorial flexibility example (from DeepSeekMoE):**
- Standard top-2 routing over 16 experts: C(16,2) = **120** combinations
- Fine-grained: split each expert into 4 sub-experts → top-8 routing over 64 experts: C(64,8) = **4,426,165,368** combinations

This vast increase in combinations allows the model to develop much more specialized, targeted representations.

**Key papers:**
- Switch Transformers (Google): simplified MoE with single expert per token, scaled to trillion parameters
- DeepSeekMoE: fine-grained expert segmentation for better specialization

---

### 8. Hyper-Connections and mHC

**Hyper-Connections** (ByteDance, ICLR 2025) generalize the standard residual shortcut by allowing each layer's output to be a learned linear combination of multiple previous layers' representations, not just a simple `x + F(x)`.

- A residual connection is a special case of a hyper-connection with fixed coefficients
- Hyper-connections can model richer information flow between non-adjacent layers

**Problem:** With learnable mixing coefficients, there is no guarantee that the mapping is well-behaved — norms can grow unboundedly during training.

**mHC (Manifold-Constrained Hyper-Connections, DeepSeek)** addresses this by constraining the composite mapping:
- **Forward pass constraint:** Based on the maximum absolute value of row sums of the composite mapping matrix — controls worst-case expansion in the forward direction
- **Backward pass constraint:** Based on the maximum absolute column sum — controls gradient propagation

These constraints keep the representations on a bounded manifold, making training stable while retaining the expressiveness of hyper-connections.

---

### 9. Next Token Prediction (NTP) — How LLMs Generate Text

NTP is the fundamental training objective of modern LLMs. At each step, the model predicts the most probable next token given all previous tokens.

**Three-step generation process:**

1. **Generate Scores (Logits):** The LLM reads the input sequence and produces a score (logit) for every token in the vocabulary (typically tens of thousands of tokens).

2. **Convert to Probabilities (Softmax):** Logits are passed through the Softmax function to produce a valid probability distribution:
   ```
   P(token_i) = exp(z_i) / sum(exp(z_j) for all j)
   ```
   Example: logit 4.2 → ~36%, logit 4.1 → ~32%, logit 3.9 → ~26%, etc.

3. **Weighted Sampling:** Rather than always selecting the highest-probability token (which would produce deterministic, repetitive output), the model samples according to the probability distribution. This introduces **controlled randomness** — the same input can produce different outputs across runs, which is crucial for diversity and creativity.

**The cycle repeats:** Each newly generated token is appended to the input, and the process repeats until a special end-of-sequence token is generated.

---

### 10. Gated FFN (GLU Variants)

Standard FFN in a Transformer: `FFN(x) = W2 * ReLU(W1 * x)`

Gated variants (GLU, SwiGLU, GeGLU) add a multiplicative gating mechanism:

```
GatedFFN(x) = (W1 * x) * gate(W3 * x)
```

Where `gate` is an activation like sigmoid (GLU), GELU (GeGLU), or Swish (SwiGLU).

- The gate acts as a soft filter: it can suppress or amplify information from different feature dimensions dynamically
- SwiGLU is used in LLaMA, PaLM, and most modern open-source LLMs
- Consistently outperforms standard ReLU-FFN at the same parameter count

---

## Important Models & Architectures

### CV Timeline

| Year | Model | Key Innovation | Depth |
|---|---|---|---|
| 1989/1998 | LeNet | First practical CNN; conv + pool + FC + backprop | ~5 layers |
| 2012 | AlexNet | Deep CNN at scale; GPU training; ImageNet | 8 layers |
| 2014 | VGGNet | Systematic depth study; 3x3 conv stacking | 11–19 layers |
| 2014 | GoogleNet/Inception | Inception module; multi-scale parallel convolutions | 22 layers |
| 2015 | ResNet | Residual (shortcut) connections; enables 1000+ layers | 50–1000+ |
| 2016 | DenseNet | Every layer connects to all subsequent layers | 20–100 |
| 2017 | MobileNet V1 | Depthwise separable convolution for edge devices | — |
| 2018 | ShuffleNet V1/V2 | Group conv + channel shuffle; practical efficiency guidelines | — |
| 2018 | MobileNet V2 | Inverted residuals; linear bottleneck | — |
| 2019–20 | EfficientNet | NAS + compound scaling of width/depth/resolution | — |
| 2020 | GhostNet | Cheap linear operations to generate redundant feature maps | — |
| 2020 | ViT | Transformer applied to image patches | 12–24 |
| 2021+ | DeiT, PVT, Swin, TNT, ConvNeXt | Hybrid and improved vision transformers | varies |

#### Cloud vs. Edge Focus
- **Cloud-side:** Maximize accuracy; compute cost is less critical (AlexNet → VGG → ResNet → ViT)
- **Edge-side:** Minimize FLOPs, memory, latency; privacy preservation (MobileNet → ShuffleNet → GhostNet)
- **Knowledge Distillation:** Large cloud models guide the training of compact edge models — the large model generates labels or soft targets for the small model

---

### NLP / LLM Timeline

| Year | Model/Technique | Key Innovation |
|---|---|---|
| Pre-2017 | RNN, LSTM, GRU | Sequential processing; gating for long-range dependencies |
| 2017 | Transformer | Self-attention; abandons recurrence entirely; parallelizable |
| 2020 | GPT-3 | 175B parameter LLM; few-shot learning at scale |
| 2020 | Gated FFN (GLU variants) | Multiplicative gating in FFN layers (SwiGLU, GeGLU) |
| 2021 | Switch Transformers | Sparse MoE; single expert per token; trillion parameters |
| 2022 | ChatGPT | RLHF-aligned conversational LLM; mainstream breakthrough |
| 2023 | LLaMA | Open-source LLM; triggered open-source ecosystem |
| 2023 | GPT-4V / Gemini | Multimodal LLMs (text + image/video) |
| 2023 | Qwen-VL | Multimodal LLM from Alibaba |
| 2023 | Phi-2 | Microsoft small model with strong performance |
| 2024+ | DeepSeekMoE | Fine-grained expert segmentation; ultra-dense MoE |
| 2025 | Hyper-Connections (HC) | Generalized shortcut connections; ByteDance (ICLR 2025) |
| 2025 | mHC | Manifold-constrained hyper-connections; DeepSeek |

---

### Transformer Architecture Deep Dive

The Transformer (Vaswani et al., NeurIPS 2017) introduced a fundamentally different approach to sequence modeling:

- **Self-Attention:** Every token can directly attend to every other token in the sequence — no locality bias like CNNs, no sequential bottleneck like RNNs
- **Multi-Head Attention (MHSA):** Multiple attention heads learn different types of relationships in parallel
- **Positional Encoding (PE):** Since self-attention is permutation-invariant, positional information must be explicitly added
- **Feed-Forward Network (FFN):** Position-wise MLP applied identically at each position
- **Residual connections + LayerNorm:** Applied around each sub-layer for stability

**Parameter layers are all linear (1x1 conv equivalent):** Q, K, V projections and MLP layers. Attention itself is parameter-free — the parameters live in the projection matrices.

**Vision Transformer (ViT, 2020):** Applied the same architecture to images by:
1. Splitting the image into fixed-size patches (e.g., 16x16 pixels)
2. Linearly embedding each patch → sequence of tokens
3. Applying standard Transformer encoder
4. Using the [CLS] token for classification

ViT showed that a unified architecture can work across language, vision, audio, and other sequential/structured data.

---

## Key Takeaways

1. **Depth is powerful, but hard to train.** The history of CV architectures is largely a story of overcoming the obstacles (vanishing gradients, poor initialization) that prevent deep networks from learning effectively.

2. **Residual/shortcut connections are a universal solution.** Whether in ResNet (CV), Transformer (NLP), or Hyper-Connections (both), the principle of providing a gradient highway around a transformation block is one of the most consistently useful ideas in deep learning.

3. **Efficiency and accuracy are a trade-off managed by architecture.** MobileNet, ShuffleNet, and GhostNet show that smart architectural choices (not just pruning or quantization) can recover most of a large model's accuracy at a fraction of the cost.

4. **Sparse computation enables scale.** MoE decouples the number of parameters from the computation per token, allowing trillion-parameter models to be trained and served economically.

5. **The Transformer is a general-purpose architecture.** It has replaced task-specific architectures in NLP, and is increasingly competitive in CV (ViT, Swin). The modular nature (SA + FFN + residual + norm) makes it easy to swap in improved components (Gated FFN, MoE layers, Hyper-Connections).

6. **Randomness in generation is a feature, not a bug.** Weighted sampling (instead of greedy argmax) prevents deterministic, repetitive LLM output and enables creativity and diversity.

7. **Cloud and edge coexist through collaboration.** Large cloud models generate data, labels, and soft knowledge that train compact edge models. Edge and cloud models can also collaborate at inference time (speculative decoding).

---

## References Mentioned

> See the Related Reading document in the course directory for full citation details. The key papers cited in this lecture are:

- **LeNet (1989/1998):** LeCun et al. — foundational CNN work
- **AlexNet (NIPS 2012):** Krizhevsky, Sutskever, Hinton
- **VGGNet (ICLR 2015):** Simonyan & Zisserman
- **GoogleNet/Inception (CVPR 2015/2016):** Szegedy et al.
- **Batch Normalization (ICML 2015):** Ioffe & Szegedy
- **ResNet (CVPR 2016):** He, Zhang, Ren, Sun
- **Kaiming Init (ICCV 2015):** He et al.
- **MobileNet V1:** Howard et al. (Google)
- **MobileNet V2 (CVPR 2018):** Sandler et al. (Google)
- **ShuffleNet V1 (CVPR 2018):** Zhang et al. (Face++)
- **ShuffleNet V2 (ECCV 2018):** Ma et al. (Face++)
- **GhostNet (CVPR 2020):** Han et al. (Huawei)
- **Transformer (NeurIPS 2017):** Vaswani et al.
- **ViT (ICLR 2021):** Dosovitskiy et al.
- **Vision Transformer Survey (TPAMI 2022):** Han et al.
- **GLU Variants (2020):** Shazeer
- **Switch Transformers:** Fedus et al. (Google)
- **DeepSeekMoE:** DeepSeek team
- **Hyper-Connections (ICLR 2025):** ByteDance
- **mHC:** DeepSeek team

---

*Notes compiled from CS6487 Week 1 lecture slides. For deeper reading, refer to the original papers listed above and the course's Related Reading document.*
