Lecture 8: Preconditioning and Adaptive Optimizers

1. From Gradient Descent to Metric Methods

The lecture starts from the idea that gradient descent can be generalized into metric methods.

In ordinary gradient descent, the update direction is the negative gradient:

\Delta w \approx -g,

where

g = \nabla f(w).

The local second-order approximation of f around the current point w is

f(w+\Delta w)
\approx
f(w)
+
g^\top \Delta w
+
\frac{1}{2}\Delta w^\top H \Delta w.

Here:

H = \nabla^2 f(w),

g=\nabla f(w),

and \Delta w is the update.

The handwritten notes annotate:

* f(w): current value / current point.
* g^\top \Delta w: first-order update effect.
* \frac{1}{2}\Delta w^\top H\Delta w: second-order / curvature influence.

We want the update direction to satisfy

\langle g,\Delta w\rangle = -\|g\|^2.

This is achieved by

\Delta w=-g.

So ordinary GD chooses the update direction that directly opposes the gradient.

⸻

1.1 A Penalized View

The notes then introduce a penalized formulation. One way to transform the local perturbation equation into an update rule is

\Delta w
\leftarrow
\arg\min_{\Delta w}
\left\{
g^\top \Delta w
+
\frac{1}{2\eta}
\|\Delta w\|_H^2
\right\}.

Here,

\|\Delta w\|_H^2
=
\Delta w^\top H\Delta w.

The notes write that:

1. \eta controls how much we care about Hessian influence.
2. \eta^{-1} controls the strength of regularization.

A related constrained view is boxed:

\Delta w
\in
\arg\min_{\|\Delta w\|_H^2\leq \rho}
g^\top \Delta w.

This means:

Choose the direction that decreases the linearized objective the most, subject to a constraint on the size of the update measured under the H-norm.

The red/arrow annotation says this is an important perspective.

⸻

1.2 Euclidean Geometry

If we simplify the metric by setting

H=I,

then the penalized update becomes

\min_{\Delta w}
\left\{
g^\top \Delta w
+
\frac{1}{2\eta}\|\Delta w\|_2^2
\right\}.

Take derivative with respect to \Delta w:

\frac{d}{d\Delta w}
\left(
g^\top \Delta w
+
\frac{1}{2\eta}\|\Delta w\|_2^2
\right)
=
g+\frac{1}{\eta}\Delta w.

Set it to zero:

g+\frac{1}{\eta}\Delta w=0.

Therefore,

\Delta w^\star=-\eta g.

This recovers ordinary gradient descent:

w_{t+1}=w_t-\eta g_t.

The notes write:

This motivates GD.

⸻

1.3 Momentum as Temporal Smoothing

Momentum adds temporal smoothing to this algorithm.

The momentum update written in the notes is

m_t=\beta m_{t-1}+(1-\beta)g_t,

w_{t+1}=w_t-\eta m_t.

The notes say:

This recovers the classic momentum GD.

So momentum is presented as ordinary GD where the raw gradient g_t is replaced by a smoothed gradient estimate m_t.

⸻

2. Preconditioning as Changing the Norm

The second major idea is:

Preconditioning can be interpreted as changing the norm used to measure update size.

The pseudo-code for most modern optimizers is described as:

1. Calculate the gradient:

g_t=\nabla f(w_t)

or in backpropagation form,

g_t=\nabla_w f(w_t).

2. Apply momentum:

m_t=\beta m_{t-1}+(1-\beta)g_t.

3. Apply preconditioning:

w_{t+1}=w_t-\eta P_t^{-1}m_t.

The red box highlights the preconditioned direction:

P_t^{-1}m_t.

The notes label P_t as a preconditioning matrix from history.

⸻

2.1 General Preconditioned Local Update

Let

P>0,

meaning P is positive definite. Therefore P is invertible.

Define a P-norm:

\|\Delta w\|_P^2
=
\Delta w^\top P \Delta w.

This is scalar-valued.

Solve the local update problem:

\min_{\Delta w}
\left\{
g^\top \Delta w
+
\frac{1}{2\eta}\Delta w^\top P\Delta w
\right\}.

Take derivative:

g+\frac{1}{\eta}P\Delta w=0.

Therefore,

P\Delta w=-\eta g.

Hence,

\Delta w^\star=-\eta P^{-1}g.

This boxed result is central:

\boxed{
\Delta w^\star=-\eta P^{-1}g
}

So preconditioning changes the geometry of the update.

⸻

2.2 Diagonal Preconditioners

If P is a diagonal matrix, then the update rescales coordinates independently.

The notes write:

Diagonal preconditioners \Rightarrow Adam.

In this case, every coordinate has its own scaling factor.

⸻

2.3 Matrix Preconditioners

If P is a full matrix, the optimizer can mix coordinates.

The notes write:

Matrix preconditioners \Rightarrow Muon.

There is also a handwritten side note:

use strictly better

The intended meaning is that full-matrix preconditioners can be more expressive than diagonal ones, because they model cross-coordinate interactions, not only coordinate-wise scaling.

⸻

3. Diagonal Preconditioners

The lecture then lists a progression:

\text{Adagrad}
\rightarrow
\text{RMSProp}
\rightarrow
\text{Adam}
\rightarrow
\text{AdamW}.

For all diagonal methods, the generic update is

w_{t+1}
=
w_t
-
\eta D_t^{-1/2} d_t.

The diagonal matrix is written as

D_t
=
\begin{bmatrix}
D_1 & 0 & \cdots & 0\\
0 & D_2 & \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & D_n
\end{bmatrix}.

Then

D_t^{-1/2}
=
\begin{bmatrix}
D_1^{-1/2} & 0 & \cdots & 0\\
0 & D_2^{-1/2} & \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & D_n^{-1/2}
\end{bmatrix}.

The idea is:

Each coordinate is divided by a scale estimated from past gradients.

⸻

3.1 Adagrad

Adagrad uses a cumulative coordinate-wise second moment.

The notes define

v_t=v_{t-1}+g_t\odot g_t.

Here,

g_t=\nabla f(w_t),

and

\odot

means element-wise product.

The notes annotate this as:

cumulative coordinate-wise second moment.

Then

D_t=\operatorname{diag}(v_t)+\epsilon I,

or equivalently, coordinate-wise,

D_{t,i}=v_{t,i}+\epsilon.

The update is

w_{t+1}
=
w_t
-
\eta
\frac{g_t}{\sqrt{v_t+\epsilon}},

where division and square root are element-wise.

The handwritten page writes this coordinate-wise idea as:

w_{t+1}
=
w_t
-
\eta
\frac{g_t}{\sqrt{v_t+\epsilon}}.

Interpretation:

* If one coordinate has received large historical gradients, v_{t,i} becomes large.
* Then its effective step size becomes smaller.
* If one coordinate rarely receives large gradients, it keeps a relatively larger step size.

⸻

3.2 RMSProp

RMSProp is described as almost identical to Adagrad, but with exponential moving average.

The update is

v_t
=
\beta v_{t-1}
+
(1-\beta)(g_t\odot g_t).

The notes label this as:

\text{EMA}

meaning exponential moving average.

Then

D_t=\operatorname{diag}(v_t)+\epsilon I.

The direction is still

d_t=g_t.

The update is

w_{t+1}
=
w_t
-
\eta
\frac{g_t}{\sqrt{v_t+\epsilon}}.

Main difference from Adagrad:

* Adagrad accumulates all past squared gradients.
* RMSProp uses an exponential moving average, so old gradients gradually decay.

⸻

3.3 Adam

Adam combines RMSProp and momentum.

The first moment / momentum estimate is

m_t
=
\beta_1 m_{t-1}
+
(1-\beta_1)g_t.

This is labeled as EMA.

The second moment estimate is

v_t
=
\beta_2 v_{t-1}
+
(1-\beta_2)(g_t\odot g_t).

This is also labeled as EMA.

The notes put a red box around the v_t equation and annotate:

identical to RMSProp.

Then

D_t=\operatorname{diag}(v_t)+\epsilon I.

The direction is

d_t=m_t.

The Adam update is

w_{t+1}
=
w_t
-
\eta
\frac{m_t}{\sqrt{v_t+\epsilon}}.

All operations in the fraction are element-wise.

The notes ask:

How is it related to metricized updates?

This question is answered on the next page.

⸻

4. Relation Between Adam and Metricized Updates

Assume no EMA is applied:

\beta_1=\beta_2=0.

Then

m_t=g_t,

and

v_t=g_t\odot g_t.

Adam becomes

w_{t+1}
=
w_t
-
\eta
\frac{g_t}{\sqrt{g_t\odot g_t}}.

Coordinate-wise, this is

\frac{g_t}{|g_t|}
=
\operatorname{sign}(g_t).

So the update becomes

w_{t+1}
=
w_t
-
\eta \operatorname{sign}(g_t).

Thus,

\Delta w
=
-\operatorname{sign}(g).

The notes explicitly write:

\text{The update of Adam without EMA: }
\Delta w=-\operatorname{sign}(g).

This is related to the local update model

\Delta w
=
\arg\min_{\|\Delta w\|_\infty\leq 1}
g^\top \Delta w.

Solving this gives

\Delta w^\star=-\operatorname{sign}(g).

So Adam without EMA corresponds to a local update model using an \ell_\infty-type constraint.

⸻

4.1 AdamW

The notes describe AdamW as:

A version of Adam tailored to L2 regularization.

Core idea:

weight decay.

The AdamW update written is

w_{t+1}
=
(1-\eta\lambda)w_t
-
\eta
\frac{m_t}{\sqrt{v_t+\epsilon}}.

The notes annotate:

* (1-\eta\lambda)w_t: only difference.
* -\eta \frac{m_t}{\sqrt{v_t+\epsilon}}: same as Adam.

So AdamW decouples weight decay from Adam’s adaptive gradient scaling.

⸻

5. Matrix Preconditioning

The lecture then moves from diagonal preconditioning to matrix preconditioning.

The notes write:

\text{Shampoo} / \text{Muon}.

Unlike previous optimizers, which mostly optimize vectors, matrix preconditioning works for matrix-shaped parameters.

Suppose

W\in\mathbb{R}^{m\times n}

instead of

w\in\mathbb{R}^n.

The update is performed directly on matrix parameters.

⸻

5.1 Shampoo: Upgrade from Adagrad

Shampoo is introduced as an upgrade from Adagrad.

Assume the matrix parameter is

W\in\mathbb{R}^{m\times n},

and its gradient is

G_t\in\mathbb{R}^{m\times n}.

Shampoo maintains two smaller second-moment accumulators:

L_t\in\mathbb{R}^{m\times m},

R_t\in\mathbb{R}^{n\times n}.

The updates are

L_t
=
L_{t-1}
+
G_tG_t^\top,

R_t
=
R_{t-1}
+
G_t^\top G_t.

The notes draw boxes around

G_tG_t^\top

and

G_t^\top G_t.

Then the Shampoo update is

W_{t+1}
=
W_t
-
\eta
(L_t+\epsilon I)^{-1/4}
G_t
(R_t+\epsilon I)^{-1/4}.

The power -1/4 appears because preconditioning is applied from both the left and the right.

⸻

5.2 Why Shampoo Is More Than a Diagonal Rule

The notes say Shampoo is almost identical to the diagonal update rule, except for two key differences.

Difference 1: The matrix is broken into two parts

Instead of one diagonal matrix D_t, Shampoo uses two matrices:

L_t
\quad\text{and}\quad
R_t.

This is because the parameter is rectangular:

W\in\mathbb{R}^{m\times n}.

So one matrix handles row-space information and the other handles column-space information.

⸻

Difference 2: L_t and R_t are not diagonal anymore

The notes emphasize:

L_t / R_t are not diagonal anymore.

They now contain subspace / eigenvector information.

This means Shampoo does not merely scale each coordinate independently. It can rotate or transform coordinates according to the accumulated gradient geometry.

⸻

5.3 Geometric Interpretation: Whitening

The notes provide a diagram with coordinates w_1,w_2. A gradient vector points diagonally.

For a diagonal matrix, the update only rescales each axis. For example, the notes show:

D_t=
\begin{bmatrix}
3 & 0\\
0 & 3
\end{bmatrix}

or similar diagonal examples.

Then

D_t^{-1/2}g_t

only changes the coordinate-wise magnitude.

For non-diagonal L_t,R_t, a coordinate transformation is first applied.

The notes draw a rotated coordinate system \tilde{w}_1,\tilde{w}_2, where the gradient is represented in the new coordinate system.

The idea is:

Shampoo performs whitening.

In stochastic optimization, g_t is a random vector or G_t is a random matrix.

The goal is to transform the gradient so that the whitened gradient becomes isotropic:

\mathbb{E}[\tilde{g}_t\tilde{g}_t^\top]=I.

The notes write:

g_t
\longrightarrow
\tilde{g}_t

and label this as:

whiten.

So matrix preconditioning aims to remove anisotropy in the gradient distribution.

⸻

6. Muon: Non-direct Upgrade of Adam

The notes then introduce Muon as a non-direct upgrade of Adam.

Unlike simply extending Adam’s diagonal v_t to a full matrix, Muon uses a different matrix-state formulation.

The notes first write a direct Shampoo-like momentum extension:

M_t
=
\beta_1 M_{t-1}
+
(1-\beta_1)G_t.

Then

L_t
=
L_{t-1}
+
M_tM_t^\top,

R_t
=
R_{t-1}
+
M_t^\top M_t.

These are boxed in red.

However, the notes mark a problem:

Problem!!! Now we need to store
M_t\in\mathbb{R}^{m\times n},
L_t\in\mathbb{R}^{m\times m},
R_t\in\mathbb{R}^{n\times n}.
All three matrices are optimizer states.

This is expensive in memory.

⸻

6.1 Muon Goes Back to the Local Update Model

Muon goes back to the local update model.

We solve for a matrix update

\Delta W\in\mathbb{R}^{m\times n}

through

\Delta W
=
\arg\min_{\|\Delta W\|_{\sigma}\leq \rho}
\langle G,\Delta W\rangle.

The handwritten norm notation is difficult to read, but the notes explain it as a special norm / operator norm.

They write:

\|\Delta W\|_{\sigma}

or equivalently the spectral/operator norm. The notes state:

\|\Delta W\|_{\sigma}
\text{ is the largest singular value.}

So the constraint is based on the largest singular value of the update matrix.

The red note says:

Use special norm / operator norm.

⸻

6.2 Solution of the Spectral-Norm-Constrained Problem

Question written in the notes:

What is the solution to the above equation?

If

G=U\Sigma V^\top,

then

\Delta W^\star
=
-UV^\top.

This means:

The update has the same singular vectors as G, but all singular values are equalized to 1.

The notes explicitly write:

\Delta W^\star
\text{ is } G \text{ but singular values equalized to } 1.

So Muon is essentially using an orthogonalized / normalized matrix direction.

⸻

6.3 Why Newton–Schulz Iteration Is Used

The notes say:

Issue is that SVD is expensive!!!

Instead of computing SVD directly, use Newton–Schulz iteration.

The note writes:

NS(A)\approx UV^\top
\quad
\text{if}
\quad
A=U\Sigma V^\top.

So

NS(A)

is used as a fast approximation to the polar factor

UV^\top.

⸻

6.4 Muon Algorithm

The Muon algorithm is written as:

1. Gradient:

G_t=\nabla_W f(W_t).

2. Momentum:

M_t
=
\beta M_{t-1}
+
(1-\beta)G_t.

3. Newton–Schulz:

U_t
=
NS(M_t)
\approx
UV^\top,

where if

M_t=U\Sigma V^\top,

then NS(M_t)\approx UV^\top.

4. Update:

W_{t+1}
=
W_t
-
\eta U_t.

The notes emphasize:

Now we only need to store M_t.

This is the major memory advantage.

⸻

7. Summary

7.1 Taxonomy

The notes summarize optimizers by geometry / metric:

* GD is Euclidean metric.
* Adagrad / RMSProp / Adam use \ell_\infty-type metric.
* Muon uses spectral norm metric.

More precisely:

\text{GD}
\quad\rightarrow\quad
\text{Euclidean metric}.

\text{Adagrad / RMSProp / Adam}
\quad\rightarrow\quad
\ell_\infty\text{ metric}.

\text{Muon}
\quad\rightarrow\quad
\text{spectral norm metric}.

⸻

7.2 Sanity Check

The notes use a quadratic function:

f(w)=\frac{1}{2}w^\top Hw.

For ordinary GD,

w_{t+1}
=
(I-\eta H)w_t.

In the quadratic case, replace

H

with something like

P^{-1}H.

Then

w_{t+1}
=
(I-\eta P^{-1}H)w_t.

If

P^{-1}H\approx I,

then choosing

\eta=1

gives very fast convergence.

This explains the goal of preconditioning:

Choose P so that P^{-1}H is close to identity.

If the preconditioner perfectly matches curvature, optimization becomes much easier.

⸻

8. Bias Correction in Adam

The last page discusses bias correction in Adam.

The notes write:

\mathbb{E}[m_t]
\approx
(1-\beta_1^t)\mathbb{E}[g_t].

Similarly,

\mathbb{E}[v_t]
\approx
(1-\beta_2^t)\mathbb{E}[g_t\odot g_t].

Because the moving averages are initialized from zero, usually

m_t

and

v_t

start from zero.

The handwritten note says:

usually m_t and v_t start from 0.

Therefore, early estimates are biased toward zero.

To correct this, Adam uses bias-corrected estimates:

\hat{m}_t
=
\frac{m_t}{1-\beta_1^t},

\hat{v}_t
=
\frac{v_t}{1-\beta_2^t}.

Then the Adam update is usually written as

w_{t+1}
=
w_t
-
\eta
\frac{\hat{m}_t}{\sqrt{\hat{v}_t}+\epsilon}.