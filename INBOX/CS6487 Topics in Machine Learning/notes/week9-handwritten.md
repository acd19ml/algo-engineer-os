Lecture 9: Landscapes

1. Critical Points in Multivariate Optimization

1.1 Definition of critical point

Let us study a function

f:\mathbb{R}^n \to \mathbb{R}.

A critical point of this function, denoted by \hat{x}, is defined as a point satisfying

\nabla f(\hat{x})=0.

In the notes, a one-dimensional landscape is drawn. The curve contains several points where the derivative is zero:

* a local maximum,
* a local minimum,
* a saddle point,
* another critical point on a nearly flat region.

The red box marks one point on the curve and labels it as a saddle.

From a dynamical-systems / control perspective:

A critical point is an equilibrium point.

That is, if the gradient is zero, gradient-based dynamics stop moving.

⸻

1.2 Types of critical points

A critical point \hat{x} can be classified as follows.

⸻

Local minimum

\hat{x} is a local minimum if there exists a region R around \hat{x} such that

f(x)\geq f(\hat{x}), \qquad \forall x\in R.

This means all nearby points have function value at least as large as the function value at \hat{x}.

⸻

Local maximum

\hat{x} is a local maximum if there exists a region R around \hat{x} such that

f(x)\leq f(\hat{x}), \qquad \forall x\in R.

This means all nearby points have function value no larger than the value at \hat{x}.

⸻

Saddle point

If a critical point is neither a local minimum nor a local maximum, then it is a saddle point.

In the notes:

\text{saddle point otherwise.}

⸻

2. Local Expansion Around a Critical Point

Now expand f around a critical point \hat{x}.

Using Taylor expansion,

f(\hat{x}+h)
=
f(\hat{x})
+
\nabla f(\hat{x})^\top h
+
\frac{1}{2}h^\top \nabla^2 f(\hat{x})h
+
\cdots

Since \hat{x} is a critical point,

\nabla f(\hat{x})=0.

The first-order term disappears:

\nabla f(\hat{x})^\top h = 0.

So the local behavior is mainly controlled by the Hessian term:

f(\hat{x}+h)
\approx
f(\hat{x})
+
\frac{1}{2}h^\top \nabla^2 f(\hat{x})h.

The red annotation on the page emphasizes that the gradient term is zero at a critical point.

⸻

3. Hessian-Based Classification

Proposition 1.1

The notes give the following classification rules.

⸻

Case 1: Positive definite Hessian

If

\nabla^2 f(\hat{x}) \succ 0,

then \hat{x} is a strict local minimum.

Here, positive definite means all eigenvalues are positive.

⸻

Case 2: Negative definite Hessian

If

\nabla^2 f(\hat{x}) \prec 0,

then \hat{x} is a strict local maximum.

⸻

Case 3: Mixed positive and negative eigenvalues

If

\nabla^2 f(\hat{x})

has both positive and negative eigenvalues, then \hat{x} is a saddle point.

This corresponds to the geometric idea that in some directions the function curves upward, while in other directions it curves downward.

⸻

4. Strict Saddle Property

4.1 Why saddle points are algorithmically friendly

The notes then ask:

Why are saddle points algorithmically friendly?

A saddle point is called strict if the Hessian has at least one strictly negative eigenvalue.

That is, at a saddle point \hat{x},

\lambda_{\min}\left(\nabla^2 f(\hat{x})\right)<0.

This means there exists at least one direction of negative curvature.

In that direction, moving slightly away from the saddle decreases the function value.

⸻

4.2 Definition: strict-saddle property

A function f is said to satisfy the strict-saddle property if every critical point \hat{x} is either:

1. a local minimum, or
2. has a Hessian with a negative eigenvalue:

\lambda_{\min}\left(\nabla^2 f(\hat{x})\right)<0.

So there are no “flat” non-minimum critical points.

⸻

4.3 Informal theorem

The notes state the following informal theorem:

Any algorithm that contains random perturbation at each gradient step will reach a local minimum of any strict-saddle function in polynomial time.

In Markdown form:

\text{Random perturbation} + \text{gradient-based method}
\quad
\Longrightarrow
\quad
\text{escape strict saddles efficiently}.

The idea is:

* At a strict saddle, there is a direction of negative curvature.
* Random perturbation has a nonzero chance of moving the iterate into that escaping direction.
* Once the algorithm moves in that direction, the function value decreases.
* Therefore, strict saddle points are not stable traps for perturbed gradient methods.

⸻

5. Matrix Sensing as a Landscape Model

The lecture then shifts to matrix sensing.

5.1 Problem setup

Let

M^\star \in \mathbb{R}^{d_1\times d_2}

be an unknown low-rank matrix.

Assume

\operatorname{rank}(M^\star)=r.

We observe linear measurements of the form

y_i = \langle A_i, M^\star\rangle,
\qquad i=1,\ldots,m.

The red annotations explain the relationship:

* y_i: what we observe;
* A_i: known sensing matrix;
* M^\star: the unknown target matrix we want to recover.

Here

A_i\in\mathbb{R}^{d_1\times d_2}

is known, and the matrix inner product is

\langle A,B\rangle
=
\operatorname{tr}(A^\top B)
=
\operatorname{vec}(A)^\top \operatorname{vec}(B)
=
\langle \operatorname{vec}(A),\operatorname{vec}(B)\rangle.

⸻

5.2 Sensing operator

Define the sensing operator

\mathcal{A}:\mathbb{R}^{d_1\times d_2}\to \mathbb{R}^m.

It maps a matrix M to a vector of linear measurements:

\mathcal{A}(M)
=
\left[
\langle A_1,M\rangle,
\langle A_2,M\rangle,
\ldots,
\langle A_m,M\rangle
\right]^\top.

We know

y=
[y_1,\ldots,y_m]^\top

and

\mathcal{A}=\{A_1,\ldots,A_m\}.

The goal is to recover M^\star.

⸻

5.3 Matrix sensing optimization problem

The goal is to find a low-rank matrix M such that

\mathcal{A}(M)=y=\mathcal{A}(M^\star),

with

\operatorname{rank}(M)\leq r.

This leads to the constrained optimization problem

\min_M
\|\mathcal{A}(M)-y\|_2^2
\quad
\text{s.t.}
\quad
\operatorname{rank}(M)\leq r.

This is the standard matrix sensing problem.

⸻

5.4 Burer–Monteiro factorized form

To make the rank constraint disappear, the notes factorize M.

In the symmetric case,

M=XX^\top,

where

X\in\mathbb{R}^{n\times r}.

The notes indicate the symmetric case:

d_1=d_2=n.

Then the optimization problem becomes

\min_{X\in\mathbb{R}^{n\times r}}
\frac{1}{2m}
\sum_{i=1}^m
\left(
\langle A_i,XX^\top\rangle-y_i
\right)^2.

This is called the Burer–Monteiro factorized form of matrix sensing.

Important relation:

M=XX^\top

automatically has rank at most r, so the rank constraint is embedded into the parameterization.

⸻

6. Connection Between Matrix Sensing and Neural Networks

6.1 Fully connected MLP example

The notes ask:

How does matrix sensing connect to NN?

A red-annotated diagram shows a two-layer fully connected neural network:

* Input layer:

x\in\mathbb{R}^n.

* Hidden layer:

r \text{ hidden neurons} \in \mathbb{R}^r.

* Output layer:

\text{output} \in \mathbb{R}.

The red notes label:

* input x\in\mathbb{R}^n,
* hidden neurons \in\mathbb{R}^r,
* output \in\mathbb{R},
* fully connected MLP,
* hidden layers have activation \sigma(\cdot)=(\cdot)^2.

So the hidden activation is quadratic.

⸻

6.2 First hidden neuron

Let

u_1\in\mathbb{R}^n

be the weights that connect input x to the first hidden neuron.

The input to the first hidden neuron is

u_1^\top x.

Because the activation is quadratic,

\sigma(u_1^\top x)=(u_1^\top x)^2.

⸻

6.3 Network output

For r hidden neurons with weights

u_1,u_2,\ldots,u_r,

the network output is

y(x,U)
=
\sum_{j=1}^r (u_j^\top x)^2.

This can be rewritten as

y(x,U)
=
x^\top UU^\top x.

Equivalently,

y(x,U)=x^\top Mx,

where

M=UU^\top.

The notes circle the expression:

x^\top Mx.

The matrix

U=[u_1,u_2,\ldots,u_r]\in\mathbb{R}^{n\times r}

contains the hidden-layer weights.

⸻

6.4 Teacher model and empirical risk

Assume data points

(x_i,y_i)

are generated by a teacher weight matrix

M^\star.

Then

y_i=x_i^\top M^\star x_i.

Since

x_i^\top M^\star x_i
=
\langle x_ix_i^\top,M^\star\rangle,

we can identify

A_i=x_ix_i^\top.

Therefore training this network corresponds to solving

\min_{U\in\mathbb{R}^{n\times r}}
\frac{1}{2m}
\sum_{i=1}^m
\left(
\langle x_ix_i^\top,UU^\top-M^\star\rangle
\right)^2.

The notes state:

m \text{ is the number of datapoints.}

So a quadratic-activation two-layer neural network can be viewed as a special matrix sensing problem.

⸻

7. Restricted Isometry Property RIP

The next major topic is the Restricted Isometry Property, abbreviated as RIP.

7.1 Motivation

In matrix sensing, one key property describes the quality of the data:

\text{RIP}.

RIP measures whether the sensing operator approximately preserves distances / norms of low-rank matrices.

⸻

7.2 Definition 3.1: RIP

The sensing operator

\mathcal{A}

satisfies the RIP of rank r with constant \delta_r\in(0,1) if, for every matrix M with

\operatorname{rank}(M)\leq r,

we have

(1-\delta_r)\|M\|_F^2
\leq
\frac{1}{m}\|\mathcal{A}(M)\|_2^2
\leq
(1+\delta_r)\|M\|_F^2.

The notes annotate:

\mathcal{A}(M)

as “a kind of linear function matrix.”

Interpretation:

* If \delta_r\to 0, RIP is good.
* If \delta_r\to 1, RIP is bad.

The red notes explicitly say:

\delta_r \to 0 \quad \text{good}

and

\delta_r \to 1 \quad \text{bad}.

⸻

7.3 Random Gaussian sensing and expectation

The notes consider

\Phi\in\mathbb{R}^{m\times N}

and

x\in\mathbb{R}^N.

If \Phi is Gaussian, then

\mathbb{E}\left[\|\Phi x\|_2^2\right]
=
\|x\|_2^2.

The notes explain this as:

\|x\|_2^2
\longrightarrow
\Phi
\longrightarrow
\|y\|_2^2.

So a Gaussian random linear map approximately preserves squared norms in expectation.

⸻

7.4 Concentration bound

The notes give a probability bound:

\Pr\left(
\left|
\|\Phi x\|_2^2-\|x\|_2^2
\right|
\geq
\epsilon \|x\|_2^2
\right)
\leq
2e^{-m c_0(\epsilon)}.

This says the norm preservation concentrates exponentially in m.

Then the notes write a sample complexity statement:

\[
m \gtrsim O\left(\delta^{-2} r \log\left(\frac{N}{r}\right)\right).
\]

The circled m indicates the number of measurements.

Interpretation:

Higher m gives a better RIP constant.

This is also highlighted in blue:

\text{Higher the }m,\text{ better the RIP constant.}

⸻

8. Case Study of Landscape / Critical Points

8.1 Simplified matrix sensing objective

The notes consider the simplified objective

\min_{x\in\mathbb{R}^n}
\frac{1}{2}
\|xx^\top-M^\star\|_F^2.

Here

r=1.

For rank-one M^\star,

M^\star

has rank 1, so RIP constant \delta_r=0 in this simplified identity-sensing setting.

The notes ask:

Where are its critical points?

Define

f(x)
=
\frac{1}{2}
\operatorname{tr}
\left[
(xx^\top-M^\star)^\top
(xx^\top-M^\star)
\right].

Expanding the gradient:

\nabla f(x)
=
(xx^\top-M^\star)x.

Since

xx^\top x = \|x\|_2^2 x,

we have

\nabla f(x)
=
\|x\|_2^2x-M^\star x.

Critical points satisfy

\nabla f(x)=0.

Therefore,

M^\star x
=
\|x\|_2^2 x.

This means x must be an eigenvector of M^\star, with eigenvalue \|x\|_2^2.

⸻

8.2 Critical points expressed by eigenpairs

Let the eigen-decomposition of M^\star be

M^\star u_i=\lambda_i u_i,

with

\lambda_1\geq \lambda_2\geq \lambda_3\geq \cdots \geq \lambda_n.

Then the critical points are

\hat{x}
\in
\left\{
0,
\pm\sqrt{\lambda_1}u_1,
\pm\sqrt{\lambda_2}u_2,
\ldots,
\pm\sqrt{\lambda_n}u_n
\right\}.

The red annotation labels:

\lambda_i,u_i

as the eigenvalue and eigenvector of M^\star.

⸻

9. Hessian Analysis of the Simplified Landscape

9.1 Verification for one eigen-direction

If

x=\sqrt{\lambda_i}u_i,

then

M^\star x
=
\sqrt{\lambda_i}M^\star u_i
=
\sqrt{\lambda_i}\lambda_i u_i.

Also,

\|x\|_2^2x
=
\|\sqrt{\lambda_i}u_i\|_2^2\sqrt{\lambda_i}u_i
=
\lambda_i\sqrt{\lambda_i}u_i.

So the critical point condition holds:

M^\star x=\|x\|_2^2x.

⸻

9.2 Hessian formula

The gradient is

\nabla f(x)=\|x\|_2^2x-M^\star x.

The Hessian is

\nabla^2 f(x)
=
2xx^\top+\|x\|_2^2I_n-M^\star.

In the notes, there is a slightly different scaling due to the \frac{1}{2} convention, but the structure is the same:

\nabla^2 f(x)
=
4xx^\top
+
2\|x\|_2^2 I_n
-
2M^\star.

The factor of 2 does not change whether the Hessian is positive or has mixed signs.

⸻

9.3 Hessian at x=0

If

\hat{x}=0,

then

\nabla^2 f(\hat{x})
=
-2M^\star.

If M^\star\succeq 0 and nonzero, then -2M^\star\preceq 0.

The notes state:

\nabla^2 f(\hat{x})=-2M^\star<0.

So x=0 is not a local minimum; it is a local maximum or a saddle depending on the rank / definiteness of M^\star.

⸻

9.4 Hessian at \hat{x}=\pm\sqrt{\lambda_i}u_i

For

\hat{x}=\pm\sqrt{\lambda_i}u_i,

the Hessian becomes

\nabla^2 f(\hat{x})
=
4\lambda_i u_iu_i^\top
+
2\sum_{j\neq i}(\lambda_i-\lambda_j)u_ju_j^\top.

The notes list eigenvalues of the Hessian:

\left\{
4\lambda_i,
2(\lambda_i-\lambda_1),
2(\lambda_i-\lambda_2),
\ldots,
2(\lambda_i-\lambda_n)
\right\}.

More precisely, along direction u_i, the eigenvalue is

4\lambda_i.

Along direction u_j, j\neq i, the eigenvalue is

2(\lambda_i-\lambda_j).

⸻

9.5 Classification

Assume

\lambda_1\geq\lambda_2\geq\lambda_3\geq\cdots\geq\lambda_n.

Case 1: i=1

If

i=1,

then

4\lambda_1>0,

and for all j\neq 1,

2(\lambda_1-\lambda_j)\geq 0.

If the top eigenvalue is strictly larger than the others, then all these are positive.

Therefore,

\nabla^2 f(\hat{x})\succ 0,

so

\hat{x}=\pm\sqrt{\lambda_1}u_1

are local minima.

These are also global minima in the rank-one case.

⸻

Case 2: i\neq 1

If

i\neq 1,

then the Hessian contains:

4\lambda_i>0,

but also

2(\lambda_i-\lambda_1)<0,

because

\lambda_i<\lambda_1.

So the Hessian contains both positive and negative eigenvalues.

Therefore,

\nabla^2 f(\hat{x})

has mixed eigenvalues, and the point is a saddle.

⸻

10. Why Small RIP Improves the Landscape

The notes state:

In the previous example, r=1, \delta_r=0.

Therefore:

Only two local minima, and they are also global minima with the same function value.

Those two global solutions are:

+\sqrt{\lambda_1}u_1

and

-\sqrt{\lambda_1}u_1.

The sign ambiguity is natural because

xx^\top=(-x)(-x)^\top.

⸻

10.1 From exact sensing to approximate sensing

The exact objective is

\min_x
\frac{1}{2}\|xx^\top-M^\star\|_F^2.

The general matrix sensing objective is

f(x)
=
\frac{1}{2m}
\|\mathcal{A}(xx^\top)-y\|_2^2.

When

\delta\to 0,

the matrix sensing objective becomes close to the exact objective:

f(x)
\approx
\frac{1}{2}
\|xx^\top-M^\star\|_F^2.

The notes write “closer as \delta\to 0.”

⸻

10.2 Informal theorem

The notes state:

Suppose the sensing operator \mathcal{A} satisfies (2r,\delta)-RIP for a sufficiently small \delta. Then every local minimum of matrix sensing is global.

In notation:

\mathcal{A}\text{ satisfies }(2r,\delta)\text{-RIP}
\quad
\Longrightarrow
\quad
\text{every local minimum is global}.

The notes also phrase this as:

A benign landscape is a landscape where all local minima correspond to global solutions.

This is highlighted in blue:

\text{A benign landscape is a landscape where all local minima correspond to global solution.}

And:

\text{Small RIP} \Rightarrow \text{benign landscape}.

⸻

11. Proof Sketch for Benign Landscape

The final pages give a proof sketch, and the notes explicitly mark it as:

Not responsible!!!

So this is likely not required for exam or homework in full rigor, but the core relationship is still written down.

⸻

11.1 General objective

Consider

f(x)
=
\frac{1}{2m}
\|\mathcal{A}(xx^\top-M^\star)\|_2^2.

Let

E=xx^\top-M^\star.

Then

f(x)
=
\frac{1}{2m}
\|\mathcal{A}(E)\|_2^2.

The gradient is written as

\nabla f(x)
=
\left[
\frac{1}{m}\mathcal{A}^\ast\mathcal{A}(E)
\right]x.

Here

\mathcal{A}^\ast

is the adjoint / transpose operator of \mathcal{A}.

The notes write:

\frac{1}{m}\mathcal{A}^\ast\mathcal{A}\approx I

under small RIP, which is an approximate isometry condition.

⸻

11.2 Hessian directional form

For a perturbation direction \Delta, the Hessian quadratic form is written approximately as

\nabla^2 f(x)[\Delta,\Delta]
=
\frac{1}{m}
\|\mathcal{A}(x\Delta^\top+\Delta x^\top)\|_2^2
+
2\left\langle
\frac{1}{m}\mathcal{A}^\ast\mathcal{A}(E),
\Delta\Delta^\top
\right\rangle.

The notes annotate:

* The first term is always positive.
* The second term can be negative.

Using RIP / approximate isometry,

\frac{1}{m}\mathcal{A}^\ast\mathcal{A}
\approx I,

so

\nabla^2 f(x)[\Delta,\Delta]
\approx
\|x\Delta^\top+\Delta x^\top\|_F^2
+
2\langle E,\Delta\Delta^\top\rangle.

⸻

11.3 Define optimal distance

The notes define \Delta(x) to be the optimal distance between x and x^\star.

Because the factorization is not unique, we have rotational/sign symmetry:

(XR)(XR)^\top=XX^\top

for any orthogonal matrix R.

In the rank-one case, this corresponds to the sign ambiguity:

x
\quad \text{and} \quad
-x.

So the distance should account for this equivalence.

The notes write this symmetry in a red box:

(XR)(XR)^\top=XX^\top
\quad
\text{for any }R.

⸻

11.4 Error decomposition

The notes define

E=xx^\top-M^\star.

Using a perturbation / alignment variable \Delta, one writes

E
=
x\Delta^\top+\Delta x^\top-\Delta\Delta^\top.

Equivalently,

x\Delta^\top+\Delta x^\top
=
E+\Delta\Delta^\top.

This identity is boxed in blue in the notes.

⸻

11.5 Critical point condition

For any critical point \hat{x},

\nabla f(\hat{x})=0.

Therefore,

E\hat{x}=0

approximately / under the exact-isometry version.

The notes write:

\nabla f(\hat{x})=0 \Rightarrow E\hat{x}=0.

This means

\langle E,\Delta\hat{x}^\top\rangle=0

and similarly,

\langle E,\hat{x}\Delta^\top\rangle=0.

Therefore,

\langle E,\hat{x}\Delta^\top+\Delta\hat{x}^\top\rangle=0.

Using

\hat{x}\Delta^\top+\Delta\hat{x}^\top
=
E+\Delta\Delta^\top,

we get

0
=
\langle E,E+\Delta\Delta^\top\rangle
=
\|E\|_F^2+\langle E,\Delta\Delta^\top\rangle.

Thus,

\langle E,\Delta\Delta^\top\rangle
=
-\|E\|_F^2.

This is the key relationship used in the proof sketch.

⸻

11.6 Hessian becomes negative away from the solution

Substitute

\langle E,\Delta\Delta^\top\rangle
=
-\|E\|_F^2

into the Hessian expression:

\nabla^2 f(\hat{x})[\Delta,\Delta]
\approx
\|E+\Delta\Delta^\top\|_F^2
-
2\|E\|_F^2.

Expanding / simplifying as written in the notes gives approximately

\nabla^2 f(\hat{x})[\Delta,\Delta]
=
\|\Delta\Delta^\top\|_F^2
-
3\|E\|_F^2.

The notes state:

\|E\|_F = O(\|\Delta\|_F).

So when \Delta is small,

\nabla^2 f(\hat{x})[\Delta,\Delta]
\approx
-3\|\hat{x}\Delta^\top+\Delta \hat{x}^\top\|_F^2
<0.

If \Delta is large, the notes also conclude

\nabla^2 f(\hat{x})[\Delta,\Delta]
\leq 0.

Therefore, away from the global solution, the Hessian has a negative curvature direction.

⸻

11.7 Final conclusion

The Hessian only becomes positive definite when

\Delta=0.

But

\Delta=0

means

x=x^\star

up to the equivalence class, for example sign or rotation.

Therefore:

\nabla^2 f(\hat{x})
\text{ only becomes positive definite when }
\Delta=0.

So:

x=x^\star
\quad
\Longrightarrow
\quad
\text{global solution}.

This proves the intuition that, under small RIP, any non-global critical point has a negative curvature direction, while local minima must be global.