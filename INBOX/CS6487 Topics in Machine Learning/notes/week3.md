# Week 3: Position Embedding in Transformer Architecture

**Course:** CS6487 Topics in Machine Learning
**Instructor:** Dr. Jianyuan Guo
**Semester:** SemB 2025-2026, Dept. CS, CityU
**Based on:** NeurIPS 2025 Tutorial (Christopher Curtis, Saiph Savage)

---

## Overview

This lecture explores **Positional Encoding (PE)** in Transformer architectures — why it is necessary, how it has evolved from sinusoidal fixed encodings in 2017 to modern parameter-free methods like RoPE and ALiBi, and where it is heading for multimodal and domain-specific tasks.

### Lecture Roadmap
1. Self-Attention Review
2. Sinusoidal Encoding Deep-Dive
3. Evolution of Positional Encoding Methods
   - 2018–2021: Conceptual Evolution of RPR (Relative Position Representation) methods
   - 2021–2025: Modern methods + Multi-Modal / Domain-Specific approaches
4. Future of Positional Encoding

---

## Transformer Fundamentals

### Why Transformers Dominate

Transformers power nearly every state-of-the-art model in:
- Natural Language Processing (NLP)
- Computer Vision
- Multimodal Reasoning
- Scientific ML
- Agentic AI

Their core innovation — **self-attention** — models global relationships between tokens without recurrence, giving them key advantages:

| Property | Description |
|---|---|
| **Global Content Understanding** | Every token can attend to every other token simultaneously |
| **Parallelization** | Removes sequential recurrence; enables training at scale |
| **Flexibility** | Works across NLP, Vision, Audio, Time-Series, Biology, etc. |
| **Scalability** | Performance empirically improves with model and data size |

### Notable Transformer-Based Models
- **LLMs:** LLaMA, GPT, Qwen
- **Vision:** ViT (Vision Transformer), Swin Transformer
- **Multimodal:** CLIP, Flamingo
- **Information Retrieval:** BERT

---

## Self-Attention: A Deep Review

### Key Terms and Notation

| Symbol | Meaning |
|---|---|
| $N$ | Number of tokens in the sequence |
| $D$ | Embedding dimension |
| $X$ | Input tensor of shape $N \times D$ |
| $w$ | Attention scores |
| $B$ | Batch size (often abstracted away) |
| $W_Q, W_K, W_V$ | Learnable weight matrices ($D \times D$) |
| $Q, K, V$ | Query, Key, Value tensors ($N \times D$) |

### Tensors and Embeddings

**Tensor:** A generalized container for numbers organized in $n$ dimensions:
- Scalar (0-D): a single number
- Vector (1-D): a list of numbers
- Matrix (2-D): a grid of numbers
- 3-D tensor: a stack of matrices
- 4-D+ tensor: higher-order stacking

**Embedding:** A dense numerical representation that captures semantic meaning. Words with similar meaning are mapped to nearby vectors in the embedding space:

$$\text{cat} \to [0.6,\ 0.9,\ 0.1,\ 0.4,\ \ldots]$$
$$\text{dog} \to [0.7,\ -0.1,\ 0.4,\ 0.3,\ \ldots]$$
$$\text{house} \to [-0.8,\ -0.4,\ -0.5,\ 0.1,\ \ldots]$$

Key property: $\text{"cat"}$ and $\text{"dog"}$ are close; $\text{"cat"}$ and $\text{"house"}$ are far apart. Embeddings are **fixed** (pretrained) before positional encoding is applied.

### Computing Q, K, V

Given input $X \in \mathbb{R}^{N \times D}$ and weight matrices $W_Q, W_K, W_V \in \mathbb{R}^{D \times D}$:

$$Q = X W_Q, \quad K = X W_K, \quad V = X W_V$$

Each tensor $Q, K, V \in \mathbb{R}^{N \times D}$ represents an enriched, learnable encoding of the input in embedding space. Specifically, cell $(i, j)$ is:

$$Q_{ij} = x_i \cdot W_Q^{(:,j)}$$

i.e., the dot product of the $i$-th token with the $j$-th column of the weight matrix across the embedding dimension.

### Attention Score Computation

The **attention score matrix** $A \in \mathbb{R}^{N \times N}$ is computed as:

$$A = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{D}}\right)$$

- Each cell $A_{ij}$ quantifies: *"How relevant is token $j$ to token $i$?"*
- The scaling factor $\frac{1}{\sqrt{D}}$ prevents large dot-product magnitudes from collapsing the softmax gradient.
- This operation is also called **dot-product attention** because it relies on the dot product as a similarity measure.

**Why the dot product?**
The dot product measures the cosine similarity scaled by magnitude. When the result is large, vectors point in similar directions in embedding space (semantic similarity). Because it is also magnitude-sensitive, this motivates the $\sqrt{D}$ scaling and careful embedding design.

> Reference: Wang et al., *Non-local Neural Networks*, CVPR 2018 (original motivation for global attention-like mechanisms).

### Context Tensor

The final context tensor $Z$ is:

$$Z = A V$$

The attention matrix $A$ redistributes information from the value vectors $V$ across all tokens, weighted by their mutual relevance.

---

## The Core Problem: No Sense of Order

### Why Positional Encoding is Necessary

Self-attention is **permutation-equivariant** by design: the model cannot natively detect adjacency, directionality, or distance. This means:

- **"The cat chased the dog"** and **"The dog chased the cat"** produce identical attention score matrices (just permuted).
- Temporal dependencies, token distances, and directional relationships are invisible without external positional information.

This creates the fundamental need for **Positional Encoding (PE):** a mechanism to integrate ordering, distance, and directionality into the model pipeline.

### What Positional Encoding Must Provide
1. Distinguish token order ("cat chased dog" vs. "dog chased cat")
2. Model temporal dependencies
3. Capture distance (how far tokens are from one another)
4. Understand direction (left/right, earlier/later, upstream/downstream)

---

## Historical Trajectory of Positional Encoding

### Three Eras

| Era | Period | Focus |
|---|---|---|
| **Era 1** | ~2017 | Absolute sinusoidal encoding (input-level) |
| **Era 2** | 2018–2021 | Relative position representations; learnable parameters inside attention |
| **Era 3** | 2021–Present | Minimal/parameter-free methods (RoPE, ALiBi); multimodal & domain-specific |

---

## Types of Position Embeddings

### 1. Absolute Positional Encoding (Sinusoidal) — Vaswani et al., 2017

#### Formulation

Positional encoding $P \in \mathbb{R}^{N \times D}$ is added directly to the input:

$$X' = U + P$$

where $U$ is the token content embedding (formerly $X$) and $P$ is the positional signal.

The sinusoidal encoding is defined as:

$$P_{(pos, 2i)} = \sin\!\left(\frac{pos}{10000^{2i/D}}\right)$$

$$P_{(pos, 2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/D}}\right)$$

where $pos$ is the token position and $i$ is the dimension index.

#### Expansion of Attention with Sinusoidal PE

Replacing $X$ with $U + P$ in the attention formula expands the attention score $A_{ij}$ into **four terms**:

$$A_{ij} \propto \underbrace{U_i W_Q W_K^\top U_j^\top}_{\text{(1) Content–Content}} + \underbrace{U_i W_Q W_K^\top P_j^\top}_{\text{(2) Content–Pos}} + \underbrace{P_i W_Q W_K^\top U_j^\top}_{\text{(3) Pos–Content}} + \underbrace{P_i W_Q W_K^\top P_j^\top}_{\text{(4) Pos–Pos}}$$

| Term | Description |
|---|---|
| (1) Content–Content | Standard self-attention (semantic similarity) |
| (2) Content–Pos | How token content $i$ relates to absolute position $j$ |
| (3) Pos–Content | How absolute position $i$ relates to token content $j$ |
| (4) Pos–Pos | Purely positional relationship between tokens $i$ and $j$ |

Nearly all subsequent PE methods emphasize one or more of these four terms.

#### Relative Encoding via Trigonometry

By trigonometric product-to-sum identities:

$$\sin(\alpha)\sin(\beta) = \frac{1}{2}[\cos(\alpha - \beta) - \cos(\alpha + \beta)]$$
$$\cos(\alpha)\cos(\beta) = \frac{1}{2}[\cos(\alpha - \beta) + \cos(\alpha + \beta)]$$

The **Pos–Pos** term (4) encodes relative distances through **differences in angles** $(\theta_i - \theta_j)$, where $\theta \propto pos / 10000^{2i/D}$.

This means Sinusoidal Encoding captures both:
- **Absolute position:** each position gets a unique fixed vector.
- **Relative position (implicit):** $P_{pos+k}$ can be represented as a linear function of $P_{pos}$ (via trigonometric identities).

For $N=50, D=128$, this creates a rich matrix of oscillating positional signals at different frequencies.

#### Problems with Sinusoidal Encoding

1. **Loss of control:** The positional signal is implicitly encoded through a massive learnable interaction — hard to interpret or constrain.
2. **Noise:** Learned properties of distance may conflict with domain knowledge.
3. **Weak generalization:** Absolute encodings extrapolate poorly to unseen sequence lengths.
4. **No directionality:** Cannot distinguish left-to-right from right-to-left.
5. **No dedicated learning:** Since learning is relied upon heavily, why not introduce dedicated learnable parameters?

> Visual evidence: TENER paper (Yan et al., 2019) showed sinusoidal PE produces noisy relative distance patterns.

---

### 2. Absolute Learnable Positional Encoding (APE)

#### Formulation

Instead of fixed sinusoids, learn an $N_{\max} \times D$ matrix of parameters:

$$P \in \mathbb{R}^{N_{\max} \times D} \quad \text{(fully learnable)}$$

Each position up to the maximum context length $N_{\max}$ gets a dedicated learnable $D$-dimensional vector.

#### Properties

- Simple to implement: just a lookup and addition operation.
- Introduces $N_{\max} \times D$ new parameters (potentially large).
- No clear performance gains over sinusoidal encoding.
- **Still used in BERT** (encoder-only models with fixed, small context lengths).

#### Problems with APE

**Effectiveness:**
- Signal loses influence as network depth increases (added only once at input).
- Content–Pos and Pos–Pos terms may not be the most desirable things to encode.

**Size:**
- Requires $N_{\max} \times D$ parameters — expensive for long contexts.

**Generalization:**
- Cannot generalize to sequences longer than $N_{\max}$.

> **Usage today:** BERT and small task-specific encoder models. Most modern LLMs do not use APE.

---

### 3. Relative Position Representations (RPR) — Shaw et al., 2018

**Paper:** *Self-Attention with Relative Position Representations*, NAACL 2018 (Google Brain)

#### Key Insight

Rather than adding position information to the input, inject it **directly into the attention computation** as a bias on the attention scores.

#### Intuition: Nodes and Edges

Think of tokens as nodes in a graph, and their relative distances as edge weights. The goal is to learn optimal edge-weight vectors in embedding space, where each relative distance (clipped at max distance $k$) gets its own learnable vector.

#### Formulation

The modified attention score for cell $(i, j)$ becomes:

$$e_{ij} = \frac{q_i (k_j + a_{ij}^K)^\top}{\sqrt{D}}$$

where $a_{ij}^K \in \mathbb{R}^D$ is a learnable vector indexed by the clipped relative distance $\text{clip}(j - i, -k, k)$.

At the tensor level, this replaces the **Pos–Pos** term of sinusoidal encoding with a precise, learnable relative distance bias, and captures **Content–Position** via the $Q$ tensor interaction.

#### Advantages over Sinusoidal PE

| | Sinusoidal PE | RPR (Shaw) |
|---|---|---|
| Position signal location | Input level | Inside attention |
| Parameter count | 0 (fixed) | $2k+1$ learnable vectors per layer |
| Directionality | No | Yes (signed distances) |
| Noise | High (implicit) | Low (controlled) |
| Analysis | Hard | Easier |

#### Shaw's Experiment

- Task: Neural Machine Translation (NMT) with encoder-decoder Transformers.
- Finding: Relative position representations improve translation quality vs. sinusoidal absolute encodings.
- Key finding: Adding positional information at **each layer** (not just input) improves performance.
- Combining relative and absolute information yielded no significant gains over relative-only.

---

### 4. Transformer-XL — Dai et al., 2019

**Paper:** *Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context*, ACL 2019 (Google)

#### Motivation

Transformers are limited by their context length $N$. Transformer-XL extends Shaw's relative encoding to model **dependencies beyond a fixed context length** using segment-level recurrence.

#### Key Innovations

Expanding on Shaw, Transformer-XL's attention score contains **four terms** (recreating all four of the original expanded attention expression):

$$e_{ij} = \underbrace{q_i^\top k_j}_{\text{Content–Content}} + \underbrace{q_i^\top W_{K,R} r_{i-j}}_{\text{Content–Pos}} + \underbrace{u^\top k_j}_{\text{Global Content Bias}} + \underbrace{v^\top W_{K,R} r_{i-j}}_{\text{Global Pos Bias}}$$

| Term | Shaw | Transformer-XL |
|---|---|---|
| Content–Content | Yes | Yes |
| Content–Pos (Query-based) | Yes | Yes |
| Global Content Bias | No | Yes — $u$ (learnable, query-agnostic) |
| Global Pos Bias | No | Yes — $v$ (learnable, query-agnostic) |

The global biases $u$ and $v$ are **query-agnostic**: they encode a uniform prior over content and distance regardless of which token is querying. This captures the intuition that some words are generally important, regardless of the current query.

---

### 5. Improved RPR Methods — Huang et al., 2020

**Paper:** *Improve Transformer Models with Better Relative Position Embeddings*, EMNLP 2020 (AWS)

Huang et al. argued that Shaw's formulation under-utilizes the interaction between $Q$, $K$, and relative distance. They proposed **four methods** as an ablation study:

| Method | Description |
|---|---|
| **M1** | Scale attention score $(i,j)$ by a learnable scalar for absolute distance $\|i-j\|$ |
| **M2** | Same as M1 but allow directionality (signed distance $j - i$) |
| **M3** | 3D learnable tensor: scale each $Q$/$K$ embedding dimension channel-wise by distance |
| **M4** | Like Shaw but with symmetric content–position bias for both $Q$ and $K$ tensors |

**Key findings:**
- Scaling attention scores directly by scalars (M1, M2) is **damaging** to performance.
- Symmetric content–position biases (M4) outperform query-only bias (Shaw's approach).

---

### 6. DA-Transformer — Wu et al., 2021

**Paper:** *DA-Transformer: Distance-Aware Transformer*, NAACL 2021 (MSRA)

Key contributions:
- **Multi-head distance split:** Distribute positional encoding across attention heads, forcing each head to learn different distance ranges (some narrow/local, others wide/global).
- **Non-negative constraint:** Prevents position signal from overemphasizing negative attention cell values.

---

### 7. Swin Transformer — Liu et al., 2021

**Paper:** *Swin Transformer: Hierarchical Vision Transformer Using Shifted Windows*, ICCV 2021 (MSRA)

Applies relative positional encoding in the **vision domain**, using 2D relative position biases within local attention windows. Demonstrates that RPR-style encodings transfer naturally to image patches.

---

### 8. RoPE: Rotary Position Embedding — Su et al., 2021

**Paper:** *RoFormer: Enhanced Transformer with Rotary Position Embedding*

#### Game-Changing Impact

RoPE is now the **dominant PE method** for decoder-only LLMs. It is used in:
- LLaMA, Mistral, Falcon, Qwen, Gemma, DeepSeek

#### Core Idea

RoPE encodes position by **rotating** the query and key vectors in pairs of dimensions. For a 2D case, the rotation matrix at position $m$ is:

$$R_m = \begin{pmatrix} \cos(m\theta) & -\sin(m\theta) \\ \sin(m\theta) & \cos(m\theta) \end{pmatrix}$$

For a $D$-dimensional vector, RoPE applies $D/2$ such 2D rotations, each with a different base frequency $\theta_i = 10000^{-2i/D}$.

The rotated query and key are:

$$\tilde{q}_m = R_m q_m, \quad \tilde{k}_n = R_n k_n$$

The dot product of rotated Q and K naturally yields a function of **relative position** $(m - n)$:

$$\tilde{q}_m^\top \tilde{k}_n = q_m^\top R_m^\top R_n k_n = q_m^\top R_{m-n} k_n$$

This is the key property: the attention score depends only on the **relative offset** $(m-n)$, not on absolute positions.

#### Why RoPE is Dominant

- **Parameter-free:** No extra learnable parameters.
- **Mathematically elegant:** Relative positions naturally emerge from the rotation structure.
- **Extrapolation:** Better than APE; degrades gracefully on longer sequences.
- **Efficient:** Can be computed efficiently without materializing an $N \times N$ position matrix.

#### RoPE Extensions (for Long-Context)

RoPE can struggle with extremely long distances. Extensions include:

| Extension | Description |
|---|---|
| **YaRN** | Yet Another RoPE extensioN — rescales frequency components |
| **LongRoPE** | Extends RoPE to very long contexts with progressive rescaling |
| **NTK-Aware Scaling** | Rescales base frequency using Neural Tangent Kernel theory |
| **XPos** | Adds exponential decay for better long-range behavior |

**Multimodal Extension:**
- **M-RoPE** (Qwen2-VL): Extends RoPE to 2D/3D spatial positions for vision-language models, enabling perception at any resolution.

---

### 9. ALiBi: Attention with Linear Biases — Press et al., 2022

**Paper:** *Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation*, ICLR 2022 (Meta)

#### Motivating Questions
- Can Transformers extrapolate to longer sequences than seen in training?
- Is the PE method the root cause of extrapolation failure?
- Can extrapolation be achieved efficiently — without extra parameters, slower runtime, or higher memory?

#### Formulation

ALiBi modifies the attention score with a **fixed, non-learnable linear bias**:

$$e_{ij} = q_i k_j^\top - m \cdot |i - j|$$

where $m$ is a head-specific slope (different for each attention head), forming a geometric sequence.

At the tensor level:

$$A = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{D}} + B\right)$$

where $B_{ij} = -m_h \cdot |i - j|$ for attention head $h$.

#### Key Properties

- **Monotonic decay:** Attention bias decreases linearly with distance — closer tokens are naturally favored.
- **Multi-head diversity:** Each head uses a different slope $m_h$, capturing different locality scales.
- **Zero parameters:** Entirely fixed — no learnable parameters needed.
- **Length extrapolation:** Can generalize to sequences much longer than seen during training.

#### Experimental Results

- Training on **shorter sequences with ALiBi can beat longer-sequence baselines** (with sinusoidal or APE).
- Improves speed and memory efficiency due to fixed parameters.
- Particularly effective on tasks with **local dependencies**.

---

### 10. NoPE: No Positional Encoding — Kazemnejad et al., 2023

**Paper:** *The Impact of Positional Encoding on Length Generalization in Transformers*, NeurIPS 2023 (McGill, IBM, Meta)

#### Core Finding

Surprisingly, using **no positional encoding at all** (NoPE) can match or outperform explicit PE methods on certain synthetic length-generalization tasks. The causal attention mask itself provides some implicit ordering signal.

#### Limitations of NoPE

- Tasks studied use very short contexts ($\leq 40$–50 tokens).
- Clean synthetic data (Copy, Reverse, Addition, SCAN, PCFG tasks).
- Does **not** apply to:
  - Long-context extrapolation tasks
  - Images, video, audio, or spatial reasoning (require explicit coordinates)
  - Code, graphs, trees, tables (require positional clues)
  - Bidirectional encoders (no causal mask to provide ordering)

---

## Comparison & Analysis

### Taxonomy of PE Methods

| Method | Era | Location | Learnable | Relative? | Extrapolation |
|---|---|---|---|---|---|
| Sinusoidal (Vaswani 2017) | 2017 | Input | No | Implicit | Poor |
| APE (BERT-style) | 2018 | Input | Yes | No | Poor |
| RPR (Shaw 2018) | 2018–2020 | Attention | Yes | Yes | Moderate |
| Transformer-XL (Dai 2019) | 2019 | Attention | Yes | Yes | Good |
| ALiBi (Press 2022) | 2021–2025 | Attention | No | Yes | Very Good |
| RoPE (Su 2021) | 2021–2025 | Q/K vectors | No | Yes | Good |
| NoPE | 2023 | None | N/A | N/A | Task-dependent |

### Four Fundamental Terms in Attention

Any PE method can be characterized by which of these four terms it emphasizes:

| Term | Shaw | XL | ALiBi | RoPE |
|---|---|---|---|---|
| Content–Content | Yes | Yes | Yes | Yes |
| Content–Pos | Yes | Yes | No | Yes |
| Global Content Bias | No | Yes | No | No |
| Global Pos Bias | No | Yes | Yes | No |
| Pos–Pos | Replaced | Replaced | Replaced | Replaced |

### Applied Performance Characteristics

| Method | Best For |
|---|---|
| Sinusoidal | Short sequences; interpretability research |
| APE | Fixed-length encoder tasks (BERT, classification) |
| RPR/XL | Long documents; NMT; encoder tasks |
| ALiBi | Local-dependency tasks; efficient long-context inference |
| RoPE | General-purpose decoder LLMs; long-context generation |
| M-RoPE | Vision-language multimodal tasks |

**Domain-Specific Findings** (from Gong et al., 2025 on gene sequence modeling):
- RoPE excels at capturing **periodic motifs** and extrapolating to long sequences.
- ALiBi performs well on tasks driven by **local dependencies**.

---

## Encoder vs. Decoder: Different PE Philosophies

### Encoder Models (e.g., BERT)

- **Fixed Sequence Lengths:** Designed for tasks with fixed maximum sequence lengths (typically 512 tokens).
- **Simplicity:** Learned absolute embeddings are simple to implement — straightforward lookup and addition.
- **Task-Specific Performance:** Learns highly effective task-specific positional representations.
- **Bidirectional Context:** Every token can attend to all others; absolute positions explicitly define each token's global location.
- **Trend:** Custom, domain-oriented signals; mixture of learned, absolute, and relative.

### Decoder Models (e.g., GPT, LLaMA)

- **Length Generalization:** Must extrapolate to variable and potentially very long sequence lengths.
- **Relative Distance Priority:** Nearby word relationships are more important than absolute position in long texts.
- **Avoiding Overfitting:** APE can overfit to specific training positions; RoPE and ALiBi generalize better.
- **Convergence on RoPE:** RoPE has become the de facto standard — not just for technical merit but also due to ecosystem inertia (large pretraining costs, shared architectural standards).

---

## Future of Positional Encoding

### Current Trajectory

**Encoder direction:**
- Highly tailored, use-case-specific signals
- Domain-oriented (biology, physics, tabular, graph data)
- Emphasis on rich positional encodings
- Designed for smaller transformer models
- Mixture of learned, absolute, and relative signals
- Fixed, smaller contexts are common

**Decoder direction:**
- Text-based models have converged on RoPE (often with extensions for long context)
- Vision Transformers (decoder-only architectures) often still use learned absolute PE
- Heavy ecosystem inertia favors adoption, extension, and repurposing over bottom-up redesign

### Open Research Questions

1. **Domain-specific PE:** Biology, physics, tabular, and graph data require unique structural cues — "position" means something different in each domain.
2. **Multimodal PE:** How to unify 1D (text), 2D (image), 3D (video/spatial) position signals coherently (e.g., M-RoPE in Qwen2-VL).
3. **PE as a structural injection framework:** PE is evolving from a simple additive signal into a general mechanism for injecting structural priors into attention.
4. **Ultra-long context:** YaRN, LongRoPE, NTK-Aware Scaling are active areas.
5. **NoPE limits:** Understanding precisely when and why no PE works is still an open question.

---

## Key Takeaways

1. **Transformers lack inherent positional awareness** — self-attention is permutation-equivariant, making PE essential for any sequence task.

2. **Adding PE to the input creates four interaction terms** in attention: Content–Content, Content–Pos (x2), and Pos–Pos. All subsequent PE methods manipulate one or more of these terms.

3. **Sinusoidal encoding** (Vaswani 2017) was groundbreaking but suffers from noisy implicit relative encoding and poor extrapolation.

4. **The field shifted from input-level to attention-level PE** (Shaw 2018 onward), improving control, efficiency, and interpretability.

5. **RoPE** achieves relative position encoding elegantly through vector rotation — yielding attention scores that depend only on relative offset, with no extra parameters.

6. **ALiBi** uses a fixed linear decay bias — zero parameters, strong extrapolation, works well for local-dependency tasks.

7. **No single PE method dominates all settings:** Encoders favor learned absolute PE; decoders converged on RoPE; multimodal tasks require spatial extensions.

8. **The future of PE** is domain-specific structural injection — treating PE as a framework for embedding structural priors, not just sequential order.

---

## Mathematical Formulas Summary

### Sinusoidal PE
$$P_{(pos, 2i)} = \sin\!\left(\frac{pos}{10000^{2i/D}}\right), \quad P_{(pos, 2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/D}}\right)$$

### Standard Self-Attention
$$A = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{D}}\right), \quad Z = AV$$

### RPR (Shaw) Attention Score
$$e_{ij} = \frac{(x_i W_Q)(x_j W_K + a_{ij}^K)^\top}{\sqrt{D}}$$

### Transformer-XL Attention Score
$$e_{ij} = q_i^\top k_j + q_i^\top W_{K,R} r_{i-j} + u^\top k_j + v^\top W_{K,R} r_{i-j}$$

### RoPE Rotation
$$\tilde{q}_m = R_m q_m, \quad \tilde{k}_n = R_n k_n, \quad \tilde{q}_m^\top \tilde{k}_n = q_m^\top R_{m-n} k_n$$

### ALiBi Bias
$$e_{ij} = q_i k_j^\top - m_h \cdot |i - j|$$

---

## References Mentioned

### Primary Papers

1. **Vaswani et al. (2017)** — *Attention Is All You Need.* Advances in Neural Information Processing Systems 30 (NeurIPS). [Foundational Transformer + Sinusoidal PE]

2. **Shaw, Uszkoreit, Vaswani (2018)** — *Self-Attention with Relative Position Representations.* NAACL. Google Brain. [RPR method]

3. **Dai et al. (2019)** — *Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context.* ACL. Google. [Extended RPR with global biases and segment recurrence]

4. **Wang, Girshick, Gupta, He (2018)** — *Non-Local Neural Networks.* CVPR. [Motivation for global attention / dot-product similarity]

5. **Yan et al. (2019)** — *TENER: Adapting Transformer Encoder for Named Entity Recognition.* [Demonstrated problems with sinusoidal PE distance properties]

6. **Huang et al. (2020)** — *Improve Transformer Models with Better Relative Position Embeddings.* EMNLP. AWS. [Four RPR ablation methods]

7. **Wu, Wu, Huang (2021)** — *DA-Transformer: Distance-Aware Transformer.* NAACL. MSRA. [Multi-head distance-aware PE]

8. **Liu et al. (2021)** — *Swin Transformer: Hierarchical Vision Transformer Using Shifted Windows.* ICCV. MSRA. [Relative PE in vision domain]

9. **Press et al. (2022)** — *Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation.* ICLR. Meta. [ALiBi]

10. **Kazemnejad et al. (2023)** — *The Impact of Positional Encoding on Length Generalization in Transformers.* NeurIPS. McGill, IBM, Meta. [NoPE study]

11. **Su et al.** — *RoFormer: Enhanced Transformer with Rotary Position Embedding.* [RoPE]

12. **Qwen2-VL Team** — *Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution.* [M-RoPE for multimodal]

13. **Gong et al. (2025)** — *Evaluation of Coding Schemes for Transformer-based Gene Sequence Modeling.* [Applied comparison of RoPE vs. ALiBi in biology]

### Tutorial Sources

14. **Curtis, Christopher and Savage, Saiph (2025)** — NeurIPS 2025 Tutorial on Positional Encoding. [Basis for this lecture]

### Model Families Referenced

- **LLaMA** — Meta's open LLM family (uses RoPE)
- **Mistral** — Mistral AI LLM (uses RoPE)
- **Falcon** — TII LLM (uses RoPE)
- **Qwen** — Alibaba LLM family (uses RoPE / M-RoPE)
- **Gemma** — Google DeepMind LLM (uses RoPE)
- **DeepSeek** — DeepSeek AI LLM (uses RoPE)
- **BERT** — Google encoder model (uses APE)
- **GPT** — OpenAI LLM family
- **ViT** — Vision Transformer
- **CLIP** — OpenAI vision-language model
- **Flamingo** — DeepMind multimodal model
