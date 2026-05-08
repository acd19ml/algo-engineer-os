# Week 5: Machine Learning on Graphs (Part 1)

> Source credits to Stanford CS224W by Prof. Jure Leskovec.
> Lecture by Zhichao Lu, Department of Computer Science, CityUHK.

---

## Overview

This week introduces **Machine Learning on Graphs**, covering the motivation for graph-structured data, graph representations, traditional graph feature engineering, and a preview of Graph Neural Networks. The lecture is structured into three major sections:

1. Introduction to Graph Machine Learning
2. Traditional Graph Machine Learning (node, link, and graph-level features)
3. Graph Neural Networks (deep learning on graphs)

**Core theme:** Graphs are a general language for describing and analyzing entities with relations/interactions. By explicitly modeling relational structure, we achieve better predictive performance than flat (grid/sequence) representations.

---

## Introduction to Graph ML

### Why Graphs?

- A **graph** is a general language for describing and analyzing entities with relations/interactions.
- Modern ML methods (CNNs, RNNs, Transformers) are designed for simple sequences and grids. **Not everything can be represented as a sequence or a grid.**
- Complex real-world domains have rich relational structures that are naturally represented as graphs.
- Graphs are one of the **hottest sub-fields in ML**, with rapidly growing presence at venues like ICLR.

### Many Types of Data are Graphs

| Domain | Graph Type |
|--------|-----------|
| Social networks | Friendship, professional, sexual networks |
| Information networks | Citation networks, WWW, internet |
| Biological networks | Protein-protein interaction, disease pathways, regulatory networks |
| Technology networks | Computer networks, underground transport |
| Other | Knowledge graphs, scene graphs, code graphs, molecules, 3D shapes, particle networks, food webs |

**Key question:** How do we take advantage of relational structure for better prediction?

### Why is Graph ML Hard?

- **Arbitrary size and complex topological structure** — no spatial locality like grids
- **No fixed node ordering or reference point** — nodes are not indexed
- **Often dynamic** and have **multimodal features**

### Representation Learning on Graphs

**Goal:** Map nodes to $d$-dimensional embeddings such that similar nodes in the network are embedded close together.

Traditional ML lifecycle:
```
Raw Data --> Feature Engineering (manual) --> ML Model --> Prediction
```

Representation Learning automates feature extraction:
```
Raw Graph --> Representation Learning --> Embeddings --> Downstream Tasks
```

Methods covered in this course:
- **Traditional methods:** Graphlets, Graph Kernels
- **Node embeddings:** DeepWalk, Node2Vec
- **Graph Neural Networks:** GCN, GraphSAGE, GAT
- **Applications:** Biomedicine, Science, Industry

---

### Applications of Graph ML

#### Task Types

| Task Type | Description | Example |
|-----------|-------------|---------|
| Node-level | Predict a property of a node | Protein function, user categorization |
| Edge-level | Predict missing/new links between nodes | Recommender systems, drug interactions |
| Subgraph-level | Classify/predict communities or regions | Traffic prediction, route ETA |
| Graph-level | Classify or generate entire graphs | Drug discovery, molecule property prediction |

#### Application Examples

**1. Protein Folding (Node-level)**
- **AlphaFold** by DeepMind solves the protein folding problem computationally.
- **Graph representation:** Nodes = amino acids, Edges = proximity between residues ("spatial graph").
- Impact: Accurately predicts 3D protein structure from amino acid sequence alone; transformative for drug discovery and biological science.

**2. Recommender Systems (Edge-level)**
- **PinSage** (Pinterest): Graph Convolutional Neural Networks for Web-Scale Recommender Systems (Ying et al., KDD 2018).
- Nodes = users and items, Edges = user-item interactions.
- Goal: Learn node embeddings $Z_i$ such that $d(Z_{cake1}, Z_{cake2}) < d(Z_{cake1}, Z_{sweater})$.
- Predict whether two nodes in the graph are related.

**3. Drug Side Effects (Edge-level)**
- **Decagon** (Zitnik et al., Bioinformatics 2018): Modeling Polypharmacy Side Effects with Graph Convolutional Networks.
- Nodes = Drugs and Proteins, Edges = Interactions.
- Task: Given a pair of drugs, predict adverse side effects (polypharmacy).
- Important because 46% of people ages 70-79 take more than 5 drugs; many take 20+.

**4. Traffic Prediction (Subgraph-level)**
- **Predicting Time of Arrival (ETA)** with GNNs — deployed in Google Maps.
- Nodes = Road segments, Edges = Connectivity between road segments.
- Significantly reduced negative ETA outcomes in several major cities.

**5. Drug Discovery (Graph-level)**
- **Stokes et al., Cell 2020:** A Deep Learning Approach to Antibiotic Discovery.
- Antibiotics are small molecular graphs: Nodes = Atoms, Edges = Chemical bonds.
- A GNN graph classification model predicts promising molecules from a pool of candidates.
- **Molecule generation/optimization:** Generate novel molecules with high drug-likeness, or optimize existing molecules for desirable properties.

**6. Physics Simulation (Graph-level)**
- **Sanchez-Gonzalez et al., ICML 2020:** Learning to Simulate Complex Physics with Graph Networks.
- Nodes = Particles, Edges = Interactions between particles.
- Graph evolution task: predict how a graph will evolve over time.

---

### Graph Representation

#### Components of a Network

- **Nodes (vertices)** $N$: the objects/entities
- **Edges (links)** $E$: the interactions/relations
- **Graph** $G(N, E)$: the system

#### Choosing a Proper Representation

The choice of representation determines the nature of the questions you can study:
- Connect individuals who work together → **professional network**
- Connect individuals with sexual relationships → **sexual network**
- Connect papers that cite each other → **citation network**

Key questions when building a graph:
- What are the **nodes**?
- What are the **edges**?

#### Types of Graphs

**Directed vs. Undirected:**
| | Undirected | Directed |
|--|------------|----------|
| Links | Symmetric, reciprocal | Directed arcs |
| Examples | Collaborations, Facebook friendship | Phone calls, Twitter following |

**Node Degree:**
- **Undirected:** $k_i$ = number of edges adjacent to node $i$; Average degree $\bar{k} = \frac{2E}{N}$
- **Directed:** in-degree $k_i^{in}$, out-degree $k_i^{out}$; Source: $k^{in}=0$; Sink: $k^{out}=0$
- $\sum_i k_i^{in} = \sum_i k_i^{out} = E$ (total number of edges)

**Bipartite Graph:**
- Nodes divided into two disjoint sets $U$ and $V$; every edge connects a node in $U$ to one in $V$.
- $U$ and $V$ are independent sets (no edges within $U$ or within $V$).
- Examples: Authors-to-Papers, Actors-to-Movies, Users-to-Movies, Recipes-to-Ingredients.
- **Folded/Projected:** Project onto one set (e.g., author collaboration networks, movie co-rating networks).

#### Graph Representations

**Adjacency Matrix:**
$$A_{ij} = 1 \text{ if there is a link from node } i \text{ to node } j, \quad A_{ij} = 0 \text{ otherwise}$$

- Undirected: $A_{ij} = A_{ji}$ (symmetric), $A_{ii} = 0$
- Directed: $A_{ij} \neq A_{ji}$ in general, $A_{ii} = 0$
- Degree: $k_i = \sum_j A_{ij}$ (row sum for undirected), $k_i^{out} = \sum_j A_{ij}$, $k_i^{in} = \sum_i A_{ij}$
- Most real-world networks are **sparse**: $E \ll E_{max}$; adjacency matrix filled with zeros (e.g., WWW density $= 1.51 \times 10^{-5}$, MSN IM density $= 2.27 \times 10^{-8}$).

**Edge List:** Represent graph as a list of (source, target) pairs. Simple but hard to query neighbors.

**Adjacency List:** For each node, store a list of its neighbors. Preferred for large, sparse graphs; allows quick neighbor retrieval.

**Node and Edge Attributes:**
- Weight (e.g., communication frequency)
- Ranking (best friend, second best friend, ...)
- Type (friend, relative, co-worker)
- Sign (Trust vs. Distrust)
- Structural properties (number of common friends)

**More Graph Types:**
| Type | Description | Example |
|------|-------------|---------|
| Unweighted | $A_{ij} \in \{0,1\}$ | Friendship, Hyperlink |
| Weighted | $A_{ij} \in \mathbb{R}$ | Collaboration, Internet, Roads |
| Self-loops | $A_{ii} \neq 0$ | Proteins |
| Multigraph | Multiple edges between same pair | Communication, Collaboration |

#### Connectivity

**Undirected Graphs:**
- **Connected:** Any two vertices can be joined by a path.
- **Disconnected:** Made up of two or more connected components.
- **Giant Component:** Largest connected component.
- **Isolated node:** Node with no edges.
- Adjacency matrix of a disconnected graph has **block-diagonal form**.

**Directed Graphs:**
- **Strongly connected:** Has a path from each node to every other node and vice versa.
- **Weakly connected:** Connected if edge directions are disregarded.
- **Strongly Connected Components (SCCs):** Maximal subsets that are mutually reachable.
  - **In-component:** Nodes that can reach the SCC.
  - **Out-component:** Nodes reachable from the SCC.

---

## Traditional Graph ML

### Overview

Traditional ML pipeline for graphs:
1. **Design features** for nodes/links/graphs (hand-crafted, $d$-dimensional vectors $\in \mathbb{R}^D$)
2. **Obtain features** for all training data
3. **Train an ML model** (Random Forest, SVM, Neural Network)
4. **Apply the model:** Given new node/link/graph, obtain features and make prediction

The quality of hand-crafted features is the key to achieving good model performance.

---

### Node-Level Features

**Goal:** Characterize the structure and position of a node in the network.

#### 1. Node Degree

$$k_v = \text{number of edges adjacent to node } v$$

- Simple count of neighboring nodes.
- Treats all neighboring nodes equally (does not capture importance).

#### 2. Node Centrality

**Eigenvector Centrality:**
- A node $v$ is important if surrounded by important neighbors.
- Recursive definition:
$$c_v = \frac{1}{\lambda} \sum_{u \in N(v)} c_u$$
- In matrix form: $\lambda \mathbf{c} = A\mathbf{c}$ — centrality $\mathbf{c}$ is the **eigenvector** of $A$.
- By the **Perron-Frobenius Theorem**, the largest eigenvalue $\lambda_{max}$ is always positive and unique.
- The eigenvector $\mathbf{c}$ corresponding to $\lambda_{max}$ is used as centrality.

**Betweenness Centrality:**
- A node is important if it lies on many shortest paths between other nodes.
$$c_v = \sum_{s \neq v \neq t} \frac{\#(\text{shortest paths between } s \text{ and } t \text{ containing } v)}{\#(\text{shortest paths between } s \text{ and } t)}$$
- Example: In a chain A-C-D-E with B branching off C, node C has high betweenness.

**Closeness Centrality:**
- A node is important if it has small shortest path lengths to all other nodes.
$$c_v = \frac{1}{\sum_{u \neq v} \text{shortest path length between } u \text{ and } v}$$

#### 3. Clustering Coefficient

Measures how connected $v$'s neighboring nodes are:
$$e_v = \frac{\#(\text{edges among neighboring nodes})}{\binom{k_v}{2}} \in [0, 1]$$

- Denominator = number of possible edges among $k_v$ neighbors.
- Counts triangles in the ego-network of $v$.

#### 4. Graphlets (图元)

**Key idea:** Count the number of pre-specified subgraph structures (graphlets) that a node participates in.

**Definitions:**
- **Induced subgraph:** Formed from a subset of vertices and ALL edges connecting those vertices in the original graph.
- **Graph Isomorphism:** Two graphs with the same number of nodes connected in the same way.
- **Graphlet:** Rooted connected induced non-isomorphic subgraphs.

There are **73 different graphlets** on up to 5 nodes (positions 0–72).

**Graphlet Degree Vector (GDV):**
- A count vector of graphlets rooted at a given node.
- For graphlets of sizes 2–5, GDV has 73 coordinates.
- Example: GDV $= [2, 1, 0, 2]$ for graphlets $a, b, c, d$.

**Analogy:**
- Degree → counts #(edges) a node touches
- Clustering coefficient → counts #(triangles) a node touches
- GDV → counts #(graphlets) a node touches for many graphlet types

#### Node-Level Features Summary

| Category | Features | Use Case |
|----------|----------|----------|
| **Importance-based** | Node degree, Eigenvector centrality, Betweenness centrality, Closeness centrality | Predicting influential nodes (e.g., celebrity users in social networks) |
| **Structure-based** | Node degree, Clustering coefficient, Graphlet Degree Vector | Predicting role in graph (e.g., protein functionality in PPI networks) |

---

### Link-Level Features

**Goal:** Design features for a pair of nodes to predict new links.

**Two formulations of link prediction:**
1. **Links missing at random:** Remove a random set of links and aim to predict them.
2. **Links over time:** Given $G[t_0, t_0']$, predict links that appear in $G[t_1, t_1']$.

#### 1. Distance-Based Features

- **Shortest-path distance** between two nodes.
- Limitation: Does not capture the degree of neighborhood overlap.

#### 2. Local Neighborhood Overlap

Captures the number of neighboring nodes shared between $v_1$ and $v_2$:

| Metric | Formula |
|--------|---------|
| **Common Neighbors** | $\|N(v_1) \cap N(v_2)\|$ |
| **Jaccard's Coefficient** | $\frac{\|N(v_1) \cap N(v_2)\|}{\|N(v_1) \cup N(v_2)\|}$ |
| **Adamic-Adar Index** | $\sum_{u \in N(v_1) \cap N(v_2)} \frac{1}{\log(k_u)}$ |

**Limitation:** Metric is always zero if the two nodes have no common neighbors, even if they could be connected in the future.

#### 3. Global Neighborhood Overlap

Uses the **entire graph structure** to score two nodes.

**Katz Index:** Count the number of walks of all lengths between a given pair of nodes.

**Key insight — Powers of the Adjacency Matrix:**
- $A_{uv}^{(1)}$ = #walks of length 1 (direct neighborhood) between $u$ and $v$ = $A_{uv}$
- $A_{uv}^{(2)}$ = #walks of length 2 = $(A^2)_{uv}$
- $A_{uv}^{(l)}$ = #walks of length $l$ = $(A^l)_{uv}$

Derivation:
$$P_{uv}^{(2)} = \sum_i A_{ui} \cdot P_{iv}^{(1)} = \sum_i A_{ui} \cdot A_{iv} = (A^2)_{uv}$$

**Katz Index Formula:**
$$S_{uv} = \sum_{l=1}^{\infty} \beta^l A_{uv}^l, \quad 0 < \beta < 1 \text{ (discount factor)}$$

**Closed-form computation** (geometric series of matrices):
$$S = \sum_{i=1}^{\infty} \beta^i A^i = (I - \beta A)^{-1} - I$$

#### Link-Level Features Summary

| Method | Description | Limitation |
|--------|-------------|-----------|
| Distance-based | Shortest path length | Does not capture neighborhood overlap |
| Local neighborhood overlap | Common neighbors, Jaccard, Adamic-Adar | Zero when no common neighbors |
| Global (Katz Index) | Counts all walks between two nodes | Computationally more expensive |

---

### Graph-Level Features and Graph Kernels

**Goal:** Features that characterize the structure of an entire graph.

#### Kernel Methods (核方法)

- **Kernel** $K(G, G') \in \mathbb{R}$: measures similarity between two graphs.
- **Kernel matrix** $\mathbf{K} = (K(G, G'))_{G,G'}$ must be positive semidefinite.
- There exists a feature representation $\phi(\cdot)$ such that $K(G, G') = \phi(G)^T \phi(G')$.
- Once the kernel is defined, off-the-shelf models (e.g., **kernel SVM**) can be used.

**Key idea — Bag-of-* for graphs:**

Naïve approach: Bag-of-Words (BoW) using node counts — fails because two different graphs can have the same node count vector.

Better: Use **node degrees** as "words." Even better: use **graphlets** or **color refinement**.

#### Graphlet Kernel

**Idea:** Count the number of different graphlets in a graph.

Note: Graphlets for graph-level features differ from node-level graphlets:
- Nodes in graphlets **do not need to be connected** (isolated nodes allowed)
- Graphlets are **not rooted**

For $k=3$, there are 4 graphlets ($g_1, g_2, g_3, g_4$).
For $k=4$, there are also 4 graphlets.

**Graphlet Count Vector:**
$$f_G = ((f_G)_1, (f_G)_2, \ldots, (f_G)_{n_k}) \text{ where } (f_G)_i = \#(g_i \subseteq G)$$

**Graphlet Kernel:**
$$K(G, G') = h_G^T h_{G'}, \quad h_G = \frac{f_G}{\text{Sum}(f_G)} \text{ (normalized)}$$

Normalization handles graphs of different sizes.

**Limitation:** Counting size-$k$ graphlets takes $O(n^k)$ time by enumeration; subgraph isomorphism is **NP-hard**. If node degree is bounded by $d$, an $O(nd^{k-1})$ algorithm exists.

#### Weisfeiler-Lehman (WL) Kernel

**Goal:** An efficient graph feature descriptor $\phi(G)$.

**Idea:** Use neighborhood structure to iteratively enrich node vocabulary — a generalized Bag of node degrees.

**Algorithm: Color Refinement**

1. Assign initial color $c^{(0)}(v)$ to each node $v$.
2. Iteratively refine node colors:
$$c^{(k+1)}(v) = \text{HASH}\left(\{c^{(k)}(v),\ \{c^{(k)}(u)\}_{u \in N(v)}\}\right)$$
   where HASH maps different inputs to different colors.
3. After $K$ steps, $c^{(K)}(v)$ summarizes the structure of the $K$-hop neighborhood of $v$.

**Color Refinement Example (2 steps):**
- Step 0: All nodes get color 1.
- Step 1: Aggregate neighboring colors → hash → new colors (e.g., $\{1,11\} \to 2$, $\{1,111\} \to 3$, etc.)
- Step 2: Aggregate and hash again → more refined colors (e.g., colors 6–13 in the example).

**WL Graph Features:**
- After color refinement, count the number of nodes with each color.
- Represents graph as a **Bag-of-Colors** vector $\phi(G)$.

**WL Kernel:**
$$K(G, G') = \phi(G)^T \phi(G')$$

**Computational Complexity:**
- Color refinement at each step: **linear in #(edges)** (aggregate neighboring colors).
- Only colors that appear in both graphs need to be tracked → at most total #(nodes) colors.
- Counting colors: linear in #(nodes).
- **Total: linear in #(edges)** — much more efficient than Graphlet Kernel.

**Connection to GNNs:** WL kernel is closely related to Graph Neural Networks (message passing aggregates neighbor information, analogous to color refinement).

#### Graph-Level Features Summary

| Method | Representation | Complexity | Key Property |
|--------|---------------|------------|--------------|
| Graphlet Kernel | Bag-of-graphlets | $O(n^k)$ per graph | Expressive but slow |
| WL Kernel | Bag-of-colors | Linear in #(edges) | Efficient; related to GNNs |
| Random-walk Kernel | Based on random walks | — | Uses path statistics |
| Shortest-path Kernel | Based on shortest paths | — | Uses path length statistics |

---

## Graph Neural Networks

### Motivation

Traditional graph ML uses **hand-crafted features**:
- Time-consuming to design
- Not adaptive (features are fixed, not learned)
- May miss important structural patterns

**Graph Neural Networks (GNNs)** learn features automatically from the graph structure and node/edge attributes.

### The Representation Learning Paradigm

$$f: N \to \mathbb{R}^d$$

Learn a function mapping each node to a $d$-dimensional embedding, such that similar nodes in the network are embedded close together.

### Methods Covered in This Course

- **GCN (Graph Convolutional Network):** Applies convolution-like operations on graphs.
- **GraphSAGE:** Samples and aggregates features from local neighborhoods.
- **GAT (Graph Attention Network):** Uses attention mechanisms to weight neighbor contributions.

> **Note:** The detailed GNN section (GCN, GraphSAGE, GAT, message passing framework) will be covered in subsequent lectures. The connection between WL color refinement and message passing GNNs is a key insight: both iteratively aggregate neighborhood information.

---

## Key Takeaways

1. **Graphs are everywhere.** Social, biological, information, and physical systems all exhibit relational structure that is naturally represented as graphs.

2. **Graph ML is challenging** due to arbitrary size, no fixed node ordering, and complex topology — unlike images or sequences.

3. **Graph representation matters.** The choice of nodes, edges, and directionality determines what questions can be studied.

4. **Real-world graphs are sparse.** The adjacency matrix is mostly zeros; use edge lists or adjacency lists in practice.

5. **Three levels of graph ML tasks:** node-level, edge-level (link prediction), and graph-level prediction.

6. **Node features:**
   - *Importance-based:* Degree, Eigenvector centrality, Betweenness, Closeness.
   - *Structure-based:* Degree, Clustering coefficient, Graphlet Degree Vector (GDV).

7. **Link features:**
   - *Local:* Common neighbors, Jaccard coefficient, Adamic-Adar.
   - *Global:* Katz index (counts walks of all lengths via powers of adjacency matrix).

8. **Graph kernels** enable graph-level classification:
   - **Graphlet Kernel:** Expressive but NP-hard to compute.
   - **WL Kernel:** Efficient color refinement; linear in #(edges); closely related to GNNs.

9. **Powers of the adjacency matrix:** $(A^k)_{uv}$ counts walks of length $k$ between nodes $u$ and $v$ — fundamental to both link prediction (Katz index) and graph neural networks.

10. **The WL kernel foreshadows GNNs:** Both iteratively aggregate neighborhood information to build richer representations. GNNs learn this aggregation; WL kernel uses a fixed hash.

---

## References Mentioned

| Reference | Type | Context |
|-----------|------|---------|
| Stanford CS224W by Prof. Jure Leskovec | Course | Source credit for lecture content |
| Ying et al., "Graph Convolutional Neural Networks for Web-Scale Recommender Systems," KDD 2018 | Paper | PinSage recommender system |
| Zitnik et al., "Modeling Polypharmacy Side Effects with Graph Convolutional Networks," Bioinformatics 2018 | Paper | Drug side effects prediction |
| Stokes et al., "A Deep Learning Approach to Antibiotic Discovery," Cell 2020 | Paper | GNN for drug discovery |
| Sanchez-Gonzalez et al., "Learning to Simulate Complex Physics with Graph Networks," ICML 2020 | Paper | Physics simulation with GNNs |
| AlphaFold by DeepMind | System/Paper | Protein folding via spatial graphs |
| Konaklieva, Monika I., "Molecular targets of β-lactam-based antimicrobials: beyond the usual suspects," Antibiotics 3.2 (2014): 128-142 | Paper | Antibiotic molecular structure |
| Shervashidze, Nino, et al., "Efficient graphlet kernels for large graph comparison," Artificial Intelligence and Statistics 2009 | Paper | Graphlet Kernel [1] |
| Shervashidze, Nino, et al., "Weisfeiler-Lehman graph kernels," Journal of Machine Learning Research 12.9 (2011) | Paper | WL Kernel [2] |
| Google Maps GNN (DeepMind) | System | Traffic prediction / ETA with GNNs |
