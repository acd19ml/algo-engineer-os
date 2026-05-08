# Week 6: Machine Learning on Graphs (Part 2)

> Source: CS6487 Topics in Machine Learning, CityU HK. Instructor: Zhichao Lu.
> Content draws heavily from Stanford CS224W (Machine Learning with Graphs).

---

## Overview / Recap

### From Hand-Crafted Features to Learned Representations

Traditional machine learning on graphs follows a two-stage pipeline:

1. **Feature Engineering** — manually design node-level, edge-level, and graph-level features based on mathematical concepts (variance, sparsity, translation, rotation, scale, etc.)
2. **Downstream Model** — train an SVM or neural network that maps those hand-crafted features to labels

The limitation is that feature engineering must be re-done for every new task and every new graph.

**Timeline of feature representation methods** (as shown in the lecture slides):
- 1901 – early statistical methods
- 1936 – classical learning models
- 1996–2005 – SVM, kernel methods
- 2012 – deep learning / learnable features (e.g., AlexNet era)

### Traditional ML for Graphs (Recap from Previous Weeks)

```
Input Graph  -->  Feature Engineering  -->  Structured Learning Algorithm  -->  Prediction
                  (node/edge/graph-level)
```

Feature engineering is a bottleneck: it is manual, task-specific, and requires domain expertise.

---

## Representation Learning

### Graph Representation Learning: Motivation

**Graph Representation Learning** eliminates the need to manually engineer features. Instead of fixed features, the system *automatically learns* a mapping from nodes (or the entire graph) into a low-dimensional vector space.

```
Input Graph  -->  [Representation Learning]  -->  Feature Embeddings  -->  Downstream Task
```

**Goal**: Efficient, *task-agnostic* feature learning for machine learning with graphs.

Formally, we seek a mapping:

```
f : u  -->  R^d
```

where `u` is a node and `R^d` is a d-dimensional embedding space.

### Why Embedding?

Embeddings allow:
- **Similarity encoding**: Proximity in embedding space reflects similarity in the network (e.g., two nodes connected by an edge should have similar embeddings).
- **Multi-task applicability**: A single embedding can be reused for many downstream tasks without re-engineering features.

**Downstream tasks enabled by node embeddings:**
- Node classification
- Link prediction
- Graph classification
- Anomalous node detection
- Clustering

**Classic example**: 2D embedding of nodes in Zachary's Karate Club network (Perozzi et al., DeepWalk, KDD 2014) — nodes from the same community cluster together in embedding space.

---

### Encoder-Decoder Framework

The general framework for learning node embeddings has four components:

1. **Encoder** — maps each node `v` to a low-dimensional vector:
   ```
   ENC(v) = z_v  ∈ R^d
   ```

2. **Node Similarity Function** — defines what it means for two nodes to be "similar" in the original graph (this is the key design choice).

3. **Decoder** — maps pairs of embeddings to a similarity score:
   ```
   DEC(z_v, z_u) = z_v^T · z_u   (dot product)
   ```

4. **Optimization Objective** — adjust encoder parameters so that:
   ```
   similarity(u, v)  ≈  z_v^T · z_u
   ```
   i.e., the dot product of embeddings approximates true node similarity.

#### Setup

Given a graph `G = (V, E)`:
- `V` = vertex set
- `A` = adjacency matrix (assumed binary)
- No additional node features are assumed (the embedding is learned purely from graph structure)

---

### "Shallow" Encoding (Embedding Lookup)

The simplest encoder is an **embedding lookup table**:

```
ENC(v) = Z · v
```

where:
- `Z ∈ R^{d × |V|}` — the embedding matrix (one column per node); this is what we **learn/optimize**
- `v ∈ {0,1}^|V|` — a one-hot indicator vector for node `v` (all zeros except a 1 in the column for node `v`)

Each node is assigned a unique, independently optimized embedding vector. This approach is used by **DeepWalk** and **node2vec**.

**Key parameters to optimize**: the matrix `Z`, which contains embedding `z_u` for every node `u`.

**Note**: Shallow encoding is **unsupervised / self-supervised**:
- No node labels are used
- No node features are used
- Goal: directly estimate coordinates (embeddings) of nodes such that some structural property (captured by the decoder) is preserved
- The resulting embeddings are **task-agnostic**

---

### How to Define Node Similarity?

The central design question is: *when should two nodes have similar embeddings?*

Possible definitions:
- **Direct connection** — nodes are linked by an edge
- **Shared neighborhood** — nodes share many common neighbors
- **Structural roles** — nodes play similar structural roles in the graph (e.g., both are hub nodes)

This lecture focuses on **random walk-based** similarity.

---

## Random Walk Approaches for Node Embeddings

### Notation

| Symbol | Meaning |
|--------|---------|
| `z_u` | Embedding of node `u` (what we optimize) |
| `P(v | u)` | Model-predicted probability of visiting `v` on a random walk starting from `u` |
| `N_R(u)` | Neighborhood of `u` obtained by random walk strategy `R` |
| `σ(z_i)` | Softmax: `exp(z_i) / Σ_j exp(z_j)` |
| `S(x)` | Sigmoid: `1 / (1 + exp(-x))` |

### What is a Random Walk?

Given a graph and a starting node, at each step:
1. Select a neighbor uniformly at random
2. Move to that neighbor
3. Repeat

The sequence of nodes visited is the **random walk**. This produces a stochastic exploration of the graph's neighborhood structure.

### Random Walk Embeddings: Core Idea

```
z_v^T · z_u  ≈  P(v and u co-occur on a random walk over the graph)
```

**Why random walks?**

1. **Expressivity** — Flexible stochastic definition of similarity that captures both *local* and *higher-order* neighborhood information. If a random walk from `u` visits `v` with high probability, `u` and `v` are considered similar.

2. **Efficiency** — No need to consider all `O(|V|^2)` node pairs; only consider pairs that actually co-occur on walks.

### Feature Learning as Optimization

Given `G = (V, E)`, learn `f : u → R^d` (i.e., `f(u) = z_u`) by solving:

```
max_f  Σ_{u ∈ V}  log P(N_R(u) | z_u)
```

where `N_R(u)` is the multiset of nodes visited on random walks starting from `u` under strategy `R`. Nodes can appear multiple times (it is a multiset).

**Intuition**: Given node `u`, learn embeddings that are *predictive* of the nodes likely to appear in `u`'s random walk neighborhood.

### Random Walk Optimization

**Step-by-step procedure:**

1. Run short fixed-length random walks starting from each node `u` in the graph using strategy `R`
2. For each node `u`, collect `N_R(u)` — the multiset of visited nodes
3. Optimize embeddings using the loss:

```
L = Σ_{u ∈ V}  Σ_{v ∈ N_R(u)}  -log P(v | z_u)
```

Parameterize `P(v | z_u)` using **softmax**:

```
P(v | z_u) = exp(z_u^T · z_v) / Σ_{n ∈ V} exp(z_u^T · z_n)
```

Putting it all together:

```
L = Σ_{u ∈ V}  Σ_{v ∈ N_R(u)}  -log [ exp(z_u^T · z_v) / Σ_{n ∈ V} exp(z_u^T · z_n) ]
```

**Problem**: The nested sum over all nodes gives `O(|V|^2)` complexity — prohibitively expensive for large graphs.

---

### Negative Sampling

**Solution**: Approximate the softmax normalization using **Negative Sampling** (a form of Noise Contrastive Estimation, NCE):

```
log [ exp(z_u^T · z_v) / Σ_{n ∈ V} exp(z_u^T · z_n) ]

≈  log σ(z_u^T · z_v)  -  Σ_{i=1}^{K} log σ(z_u^T · z_{n_i})
```

where:
- `σ` is the sigmoid function
- `n_i ~ P_V` — `K` negative samples drawn proportionally to node degree
- This replaces expensive full normalization with `K` random "negative" comparisons

**Choosing K:**
- Higher `K` → more robust estimates
- Higher `K` → higher bias on negative events
- **In practice: K = 5 to 20**

**Note**: Negative samples can technically be any node; for correctness, they should be nodes not on the walk, but any node is used in practice for efficiency.

**Reference**: Noise Contrastive Estimation paper — https://arxiv.org/pdf/1402.3722.pdf

---

### Stochastic Gradient Descent (SGD)

After forming the objective `L`, minimize it using **Stochastic Gradient Descent**:

**Full Gradient Descent:**
1. Initialize `z_u` randomly for all nodes `u`
2. Iterate until convergence:
   - Compute gradient `∂L/∂z_u` for all `u`
   - Update: `z_u ← z_u - η · ∂L/∂z_u`  (where `η` is the learning rate)

**Stochastic Gradient Descent (SGD)** — more practical:
1. Initialize `z_u` randomly for all nodes
2. For each training example (node `u`):
   - Compute per-node loss: `L^u = Σ_{v ∈ N_R(u)} -log P(v | z_u)`
   - Compute gradient `∂L^u/∂z_j` for all dimensions `j`
   - Update: `z_j ← z_j - η · ∂L^u/∂z_j`

SGD evaluates gradients on individual training examples rather than the entire dataset, making it much more scalable.

### Random Walk Summary

```
Algorithm: Random Walk Node Embedding

1. Run short fixed-length random walks from each node u
2. For each node u, collect N_R(u) = multiset of visited nodes
3. Optimize using SGD:
   L = Σ_{u ∈ V} Σ_{v ∈ N_R(u)} -log P(v | z_u)
   (approximate with Negative Sampling for efficiency)
```

---

## Advanced GNN Topics

### DeepWalk

**DeepWalk** (Perozzi et al., KDD 2014) uses the simplest random walk strategy:
- Run **fixed-length, unbiased** random walks from each node
- Each step selects a neighbor uniformly at random

**Limitation**: The resulting notion of similarity is too constrained — it only captures a simple, uniform local view of the neighborhood.

---

### node2vec: Biased Random Walks

**node2vec** (Grover and Leskovec, KDD 2016) generalizes DeepWalk with a *flexible, biased* second-order random walk strategy that can interpolate between two extremes:

| Strategy | Type | View |
|----------|------|------|
| **BFS** (Breadth-First Search) | Local exploration | Micro-view of neighborhood (structural equivalence) |
| **DFS** (Depth-First Search) | Global exploration | Macro-view of neighborhood (homophily) |

**Two hyperparameters:**

- `p` — **Return parameter**: controls the probability of returning to the previous node
- `q` — **In-out parameter**: controls the ratio of BFS-like vs. DFS-like behavior
  - Low `q` → DFS-like (explores farther outward)
  - Low `p` → BFS-like (stays close to source)

#### Biased 2nd-Order Random Walk Mechanics

When the walker has just traversed edge `(S1, w)` and is currently at node `w`, transition probabilities to neighbors of `w` are:

| Next node `t` | Distance from `S1` | Unnormalized probability |
|---------------|--------------------|--------------------------|
| `S1` (back to previous) | 0 | `1/p` |
| Nodes at distance 1 from `S1` (shared neighbors) | 1 | `1` |
| Nodes at distance 2 from `S1` (farther away) | 2 | `1/q` |

This is a **second-order** walk because the transition depends on the *previous* node (not just the current node). The walker "remembers" where it came from.

**Walk types:**
- **BFS-like**: Low `p` → high chance to go back → stays local
- **DFS-like**: Low `q` → high chance to go far → explores globally

#### node2vec Algorithm

```
1. Compute random walk transition probabilities (using p and q)
2. Simulate r random walks of length l starting from each node u
3. Optimize the node2vec objective using SGD (with Negative Sampling)
```

**Complexity**: Linear time in the number of nodes. All three steps are individually parallelizable.

---

### Other Random Walk Variants

| Method | Key Idea |
|--------|----------|
| **DeepWalk** (Perozzi et al., 2014) | Fixed-length unbiased walks |
| **node2vec** (Grover & Leskovec, 2016) | Biased 2nd-order walks (p, q parameters) |
| **metapath2vec** (Dong et al., 2017) | Walks based on node attributes/types (heterogeneous graphs) |
| **Watch Your Step** (Abu-El-Haija et al., 2017) | Walks based on learned weights |
| **LINE** (Tang et al., 2015) | Directly optimizes 1-hop and 2-hop walk probabilities |
| **struct2vec** (Ribeiro et al., 2017) | Runs walks on modified network; captures structural identity |
| **HARP** (Chen et al., 2016) | Hierarchical graph preprocessing before walks |

---

### Choosing a Method

No single method dominates in all cases (Goyal and Ferrara, 2017 survey):
- **node2vec** performs better on **node classification**
- Other methods may perform better on **link prediction**
- **Random walk approaches** are generally more **computationally efficient**
- Key principle: choose the node similarity definition that matches your downstream application

---

## Graph Transformer / Modern Approaches

### Embedding Entire Graphs

Beyond node embeddings, we often need to embed an **entire graph or subgraph** into a single vector `z_G`.

**Use cases:**
- Classifying molecules as toxic vs. non-toxic
- Identifying anomalous graphs
- Drug discovery / molecular property prediction

Three approaches are covered:

---

#### Approach 1: Sum/Average of Node Embeddings

Simple but effective:
1. Run any graph embedding technique to get node embeddings `z_v` for each `v ∈ G`
2. Aggregate:

```
z_G = Σ_{v ∈ G} z_v
```

or use the average. Used by **Duvenaud et al. (2016)** for molecular graph classification.

---

#### Approach 2: Virtual Node

1. Introduce a **virtual "super-node"** that is connected to all nodes in the (sub)graph
2. Run a standard embedding technique — the super-node's embedding becomes `z_G`

Proposed by **Li et al. (2016)** as a general technique for subgraph embedding.

---

#### Approach 3: Anonymous Walk Embeddings

Reference: *Anonymous Walk Embeddings*, ICML 2018 (https://arxiv.org/pdf/1805.11921.pdf)

**Key idea**: Anonymous walks remove node identity — only the *pattern* of revisits matters.

**Anonymous Walk Definition**: In an anonymous walk, each position is labeled by the **index of the first time that node was visited**.

**Example:**
- Walk: A → B → C → B → C
- Anonymous walk: 1 → 2 → 3 → 2 → 3

Two different concrete walks over different nodes that have the same pattern produce the **same anonymous walk**.

**Number of anonymous walks grows exponentially:**
- Length 3: 5 anonymous walks — `{111, 112, 121, 122, 123}`
- Length 7: 877 anonymous walks

**Idea 1: Simple Frequency-Based Representation**

- Simulate `m` anonymous walks of length `l`
- Represent graph as a probability distribution over walk types:
  ```
  z_G[i] = fraction of times anonymous walk w_i occurred
  ```
- This gives a fixed-dimensional histogram vector

**How many walks do we need?**
```
m ≥ (η / ε²) · (log(2/δ) - log(δ))
```
where:
- `η` = number of distinct anonymous walks of length `l`
- `ε` = max acceptable error
- `δ` = failure probability

Example: For `l = 7`, `ε = 0.1`, `δ = 0.01` → need `m = 122,500` random walks.

---

**Idea 2: Learned Walk Embeddings**

Rather than representing walks by frequencies, **learn** embeddings `z_i` for each anonymous walk type `w_i`, as well as an overall graph embedding `z_G`.

**Objective**: Embed walks so that the next walk can be predicted from the context (analogous to word2vec):

```
max_{z_G, z_i}  (1/T) Σ_{t=Δ+1}^{T}  log P(w_t | w_{t-Δ}, ..., w_{t-1}, z_G)
```

where `T` is the total number of sampled walks and `Δ` is the context window size.

**Probability model:**

```
P(w_t | w_{t-Δ}, ..., w_{t-1}, z_G) = exp(y(w_t)) / Σ_{i=1}^{η} exp(y(w_i))

y(w_t) = b + U · cat( (1/Δ) Σ_{i=1}^{Δ} z_i , z_G )
```

where:
- `cat(·, ·)` = concatenation
- `(1/Δ) Σ z_i` = average of walk embeddings in the window
- `b ∈ R`, `U ∈ R^d` are learnable parameters (linear layer)
- `η` = number of all possible anonymous walk types (requires negative sampling)

**After optimization**: `z_G` is a separately optimized learnable parameter that encodes the entire graph.

**Downstream use of `z_G`:**
- **Option 1**: Inner product kernel — `z_G1^T · z_G2` (graph-level similarity)
- **Option 2**: Feed `z_G` into a neural network for graph classification

---

### Hierarchical Embeddings (Preview)

A more advanced approach (covered in Lecture 8): **hierarchically cluster** nodes in the graph, then sum/average node embeddings within each cluster. This produces a hierarchical pooling that captures multi-scale graph structure.

---

## Applications

### How to Use Node Embeddings

Given node embeddings `{z_i}`, downstream applications:

#### Clustering / Community Detection
- Cluster the vectors `{z_i}` directly (e.g., k-means in embedding space)

#### Node Classification
- Predict label of node `i` based on `z_i`

#### Link Prediction
- Predict edge `(i, j)` based on a function of `(z_i, z_j)`:

| Method | Formula |
|--------|---------|
| Concatenate | `f(z_i, z_j) = g([z_i, z_j])` |
| Hadamard (element-wise product) | `f(z_i, z_j) = g(z_i * z_j)` |
| Sum / Average | `f(z_i, z_j) = g(z_i + z_j)` |
| L2 Distance | `f(z_i, z_j) = g(‖z_i − z_j‖₂)` |

#### Graph Classification
- Use graph embedding `z_G` (via node aggregation or anonymous walks) to predict graph-level labels

---

## Key Takeaways

1. **Graph Representation Learning** removes the bottleneck of manual feature engineering by learning task-agnostic node and graph embeddings from raw graph structure.

2. The **Encoder-Decoder framework** is the unifying abstraction:
   - Encoder (shallow lookup): `ENC(v) = Z · v`
   - Decoder (dot product): `DEC(z_u, z_v) = z_u^T · z_v`
   - Objective: maximize dot product similarity for nodes co-occurring on random walks

3. **Random walks** provide a flexible and efficient definition of node similarity, capturing multi-hop neighborhood information without requiring all `O(|V|^2)` pair comparisons.

4. **DeepWalk**: Unbiased fixed-length random walks — simple baseline.

5. **node2vec**: Biased second-order random walks with parameters `p` (return) and `q` (walk-away). Interpolates between BFS (local, structural) and DFS (global, community) views.

6. **Negative Sampling** (NCE approximation) reduces the `O(|V|^2)` softmax normalization cost to `O(K)` per update, making training feasible.

7. **Graph-level embeddings** can be constructed via: node aggregation (sum/avg), virtual super-node, or Anonymous Walk Embeddings.

8. **Anonymous Walk Embeddings** are identity-agnostic and capture the structural pattern of walks — useful for graph classification where node identities are irrelevant.

9. No single method is universally best: the choice of node similarity definition should be driven by the downstream task and application.

10. Future direction (Lecture 8): **Hierarchical / pooling-based** graph embeddings using Graph Neural Networks (deep encoders), which overcome the limitations of shallow embedding lookup.

---

## References Mentioned

### Core Papers

| Paper | Venue | Notes |
|-------|-------|-------|
| Perozzi et al. **"DeepWalk: Online Learning of Social Representations"** | KDD 2014 | Introduced DeepWalk; first random-walk-based node embedding; used Karate Club example |
| Grover & Leskovec. **"node2vec: Scalable Feature Learning for Networks"** | KDD 2016 | Biased 2nd-order random walk (p, q parameters); BFS/DFS interpolation |
| Duvenaud et al. **"Molecular Graph Convolutions"** (2016) | NeurIPS 2016 | Used sum of node embeddings for molecular graph classification |
| Li et al. (2016) | — | Proposed virtual super-node for subgraph embedding |
| Ivanov & Burnaev. **"Anonymous Walk Embeddings"** | ICML 2018 | Anonymous walk-based graph-level embeddings; https://arxiv.org/pdf/1805.11921.pdf |
| Dong et al. **"metapath2vec"** (2017) | — | Biased walks based on node attributes/types (heterogeneous graphs) |
| Abu-El-Haija et al. (2017) | — | Walks based on learned weights |
| Tang et al. **"LINE: Large-scale Information Network Embedding"** (2015) | WWW 2015 | Directly optimizes 1-hop and 2-hop random walk probabilities |
| Ribeiro et al. **"struc2vec"** (2017) | — | Walks on modified network; structural identity-based embeddings |
| Chen et al. **"HARP: Hierarchical Representation Learning for Networks"** (2016) | — | Hierarchical graph preprocessing before applying walk-based methods |
| Goyal & Ferrara. Survey (2017) | — | Survey comparing node embedding methods; shows no single method wins universally |

### Background / Methods

| Reference | Context |
|-----------|---------|
| Noise Contrastive Estimation (NCE) — https://arxiv.org/pdf/1402.3722.pdf | Theoretical basis for Negative Sampling approximation |
| Zachary's Karate Club network | Classic benchmark graph for visualizing node embeddings |

### Art / Image Credits (from slides)

| Credit | Page |
|--------|------|
| Marie-Antoinette by Elisabeth Vigee Le Brun, 1778 | Pages 3–5 |
| Marie-Antoinette by Jacques-Louis David, 1793 | Page 4 |
| Marie-Antoinette by Hippolyte Louis Emile Pauquet | Page 6 |

### Source Course

- **Stanford CS224W**: Machine Learning with Graphs — primary source for this material
- **CityU CS6487**: Topics in Machine Learning, Instructor: Zhichao Lu (SS26)
