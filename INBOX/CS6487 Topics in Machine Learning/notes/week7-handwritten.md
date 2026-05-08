Lecture 7: Gradient Descent / Convergence

1. Preliminary Math

Inner product and norm

For x, y \in \mathbb{R}^n,

\langle x, y \rangle = x^\top y = y^\top x \in \mathbb{R}.

Vector norm:

\|x\|_2 = \sqrt{x^\top x}.

⸻

Cauchy–Schwarz inequality

|\langle x, y\rangle| \leq \|x\|_2 \|y\|_2.

Geometric interpretation:

\langle x, y\rangle = \|x\|_2 \|y\|_2 \cos \theta,

where \theta is the angle between x and y.

⸻

Young’s inequality

For scalars a,b \in \mathbb{R}, and \eta > 0,

ab \leq \frac{\eta}{2}a^2 + \frac{1}{2\eta}b^2.

For vectors u, v \in \mathbb{R}^n,

\|u-v\|_2^2
= \|u\|_2^2 - 2\langle u,v\rangle + \|v\|_2^2.

Using Young’s inequality,

-2\langle u,v\rangle
\leq \eta \|u\|_2^2 + \frac{1}{\eta}\|v\|_2^2.

⸻

2. Convexity

Geometric intuition

The notes draw two curves:

1. A convex curve, where the tangent line lies below the function curve.
2. A non-convex curve, where a tangent line may cross the function curve.

The red arrows on the convex curve emphasize that the function graph stays above its tangent approximation.

⸻

First-order definition of convexity

A differentiable function f is convex if, for all x,y \in \mathbb{R}^d,

f(y) \geq f(x) + \langle \nabla f(x), y-x\rangle.

This means:

For a convex differentiable function, the first-order Taylor approximation at x is always a global lower bound of f.

⸻

Strong convexity

A function f is \mu-strongly convex if

f(y) \geq f(x)
+ \langle \nabla f(x), y-x\rangle
+ \frac{\mu}{2}\|y-x\|_2^2.

The blue bracket in the notes highlights the ordinary convexity part:

f(x)+\langle \nabla f(x),y-x\rangle,

while the additional quadratic term

\frac{\mu}{2}\|y-x\|_2^2

is what makes the condition stronger.

⸻

3. Taylor’s Theorem / Descent Lemma

3.1 Taylor’s theorem with remainder

Let

f:\mathbb{R}^n \to \mathbb{R}

be a twice continuously differentiable function.

For any x and direction s, where x,s \in \mathbb{R}^n,

f(x+s)
=
f(x)
+
\langle \nabla f(x),s\rangle
+
\frac{1}{2}s^\top \nabla^2 f(x+\tau s)s,

for some unknown

\tau \in [0,1].

The red box highlights the second-order remainder term:

\frac{1}{2}s^\top \nabla^2 f(x+\tau s)s.

The blue note says \tau “may be” some value in [0,1], not necessarily known.

⸻

Quick reminder: Hessian positive semidefinite

For convex twice-differentiable functions, Hessians are positive semidefinite:

\[
\nabla^2 f(x) \succeq 0.
\]

Equivalently, for all a \in \mathbb{R}^n,

a^\top \nabla^2 f(x)a \geq 0.

This also means all eigenvalues satisfy

\lambda(\nabla^2 f(x)) \geq 0.

⸻

4. Smoothness

Definition of smoothness

We say f is L-smooth if

\|\nabla f(x)-\nabla f(y)\|_2
\leq
L\|x-y\|_2,
\qquad
\forall x,y \in \mathbb{R}^d.

Here L is a scalar constant.

Intuition from the diagrams:

* A ReLU-like function has a sharp corner and may fail differentiability/smoothness at the kink.
* Smoothness controls how quickly the slope/gradient can change.

⸻

5. Descent Lemma

Lemma: Descent Lemma

If f is differentiable and L-smooth, then

f(y)
\leq
f(x)
+
\langle \nabla f(x),y-x\rangle
+
\frac{L}{2}\|y-x\|_2^2.

The notes box this inequality in red.

This is the key upper-bound counterpart to the first-order convexity lower bound.

⸻

Proof sketch

Define

\phi(t)=f(x+t(y-x)), \qquad t\in(0,1).

Then

\phi'(t)
=
\left\langle
\nabla f(x+t(y-x)), y-x
\right\rangle.

Now,

\phi(1)-\phi(0)
=
\int_0^1 \phi'(t)\,dt.

Insert and subtract \nabla f(x):

\phi(1)-\phi(0)
=
\int_0^1
\left\langle
\nabla f(x),y-x
\right\rangle dt
+
\int_0^1
\left\langle
\nabla f(x+t(y-x))-\nabla f(x),y-x
\right\rangle dt.

The first term becomes

\left\langle
\nabla f(x),y-x
\right\rangle.

For the second term, use Cauchy–Schwarz:

\left|
\left\langle
\nabla f(x+t(y-x))-\nabla f(x),y-x
\right\rangle
\right|
\leq
\|\nabla f(x+t(y-x))-\nabla f(x)\|_2
\|y-x\|_2.

Using L-smoothness,

\|\nabla f(x+t(y-x))-\nabla f(x)\|_2
\leq
L\|x+t(y-x)-x\|_2.

Since

x+t(y-x)-x=t(y-x),

we get

\|\nabla f(x+t(y-x))-\nabla f(x)\|_2
\leq
Lt\|y-x\|_2.

Therefore,

\phi(1)-\phi(0)
\leq
\langle \nabla f(x),y-x\rangle
+
\int_0^1 Lt\|y-x\|_2^2\,dt.

Since

\int_0^1 Lt\,dt = \frac{L}{2},

we obtain

f(y)-f(x)
\leq
\langle \nabla f(x),y-x\rangle
+
\frac{L}{2}\|y-x\|_2^2.

Thus,

f(y)
\leq
f(x)
+
\langle \nabla f(x),y-x\rangle
+
\frac{L}{2}\|y-x\|_2^2.

⸻

6. Smoothness and Hessian eigenvalues

When f is twice differentiable,

L\text{-smoothness}
\quad
\Longleftrightarrow
\quad
\lambda_{\max}(\nabla^2 f(x)) \leq L.

That is, the largest eigenvalue of the Hessian is bounded by L.

⸻

7. Consequences of Smoothness for Gradient Descent

Gradient descent update:

x_{k+1}=x_k-\alpha \nabla f(x_k).

Here \alpha is the learning rate / step size.

⸻

Apply the descent lemma

Let

y=x_{k+1}=x_k-\alpha \nabla f(x_k).

Then

y-x_k=-\alpha \nabla f(x_k).

Using the descent lemma,

f(x_{k+1})
=
f(x_k-\alpha \nabla f(x_k))

\leq
f(x_k)
+
\left\langle
\nabla f(x_k),
-\alpha \nabla f(x_k)
\right\rangle
+
\frac{L}{2}
\left\|
-\alpha \nabla f(x_k)
\right\|_2^2.

Compute each term:

\left\langle
\nabla f(x_k),
-\alpha \nabla f(x_k)
\right\rangle
=
-\alpha \|\nabla f(x_k)\|_2^2.

And

\frac{L}{2}
\left\|
-\alpha \nabla f(x_k)
\right\|_2^2
=
\frac{L}{2}\alpha^2
\|\nabla f(x_k)\|_2^2.

Therefore,

f(x_{k+1})
\leq
f(x_k)
-
\alpha \|\nabla f(x_k)\|_2^2
+
\frac{L}{2}\alpha^2
\|\nabla f(x_k)\|_2^2.

Factor out:

f(x_{k+1})
\leq
f(x_k)
-
\alpha
\left(
1-\frac{L\alpha}{2}
\right)
\|\nabla f(x_k)\|_2^2.

For descent, we want

\alpha
\left(
1-\frac{L\alpha}{2}
\right)>0.

Since \alpha>0, this requires

1-\frac{L\alpha}{2}>0.

Thus,

\alpha < \frac{2}{L}.

So for any step size

\alpha \in \left(0,\frac{2}{L}\right),

we have

f(x_{k+1}) < f(x_k),

assuming \nabla f(x_k)\neq 0.

This guarantees descent.

⸻

8. Notions of Convergence

Assume we are optimizing a function that is bounded below and has a global minimizer x^\star, such that

f(x) \geq f^\star,
\qquad
f(x^\star)=f^\star.

The notes list three major ways to describe convergence.

⸻

8.1 Function-value convergence

f(x_k) \to f^\star,
\qquad
k\to\infty.

This means the objective value approaches the optimal value.

⸻

8.2 Iterate convergence

x_k \to x^\star,
\qquad
k\to\infty.

This means the actual points generated by the algorithm converge to the optimizer.

⸻

8.3 Stationarity

\|\nabla f(x_k)\| \to 0.

This means the gradients vanish asymptotically.

⸻

Landscape recap

The notes draw a non-convex landscape with multiple valleys.

Important idea:

* A point can be a local minimum but not a global minimum.
* In non-convex optimization, stationarity does not necessarily imply global optimality.

⸻

9. Stationary / Critical Points

A stationary point, also called a critical point, satisfies

\|\nabla f(x)\|=0.

There are three types of stationary points shown:

1. Local minimum.
2. Saddle point.
3. Local maximum.

The notes ask:

Rates: gradient or function value?

This indicates that convergence rates can be measured either by the gradient norm or by the objective-value gap.

⸻

10. Rates of Convergence

Let

\{a_k\}_{k=0}^{\infty}

be a nonnegative sequence such that

a_k \to 0.

Two types of rates are written.

⸻

10.1 Linear rate / geometric rate

a_k \leq C\rho^k,

for some

\rho \in (0,1).

This is fast convergence.

⸻

10.2 Sublinear rate

Examples:

a_k = O(1/k)

or

a_k = O(1/\sqrt{k}).

Equivalently,

a_k \leq \frac{C}{k}

or

a_k \leq \frac{C}{\sqrt{k}}.

The sketch compares:

* \rho^k: decays very fast.
* 1/k: slower.
* 1/\sqrt{k}: even slower.

⸻

11. Convergence of Gradient Descent

11.1 Non-convex guarantee

Assume f is L-smooth and bounded below:

f^\star > -\infty.

Use step size

\alpha = \frac{1}{L}.

From the previous descent inequality:

f(x_{k+1})
\leq
f(x_k)
-
\alpha
\left(
1-\frac{L\alpha}{2}
\right)
\|\nabla f(x_k)\|_2^2.

Plug in

\alpha=\frac{1}{L}.

Then

\alpha\left(1-\frac{L\alpha}{2}\right)
=
\alpha
\left(
1-\frac{1}{2}
\right)
=
\frac{\alpha}{2}.

Therefore,

f(x_{k+1})
\leq
f(x_k)
-
\frac{\alpha}{2}
\|\nabla f(x_k)\|_2^2.

Equivalently,

\frac{\alpha}{2}
\|\nabla f(x_k)\|_2^2
\leq
f(x_k)-f(x_{k+1}).

⸻

Sum from k=0 to T-1

Summing both sides,

\frac{\alpha}{2}
\sum_{k=0}^{T-1}
\|\nabla f(x_k)\|_2^2
\leq
\sum_{k=0}^{T-1}
\left(
f(x_k)-f(x_{k+1})
\right).

The right side telescopes:

\sum_{k=0}^{T-1}
\left(
f(x_k)-f(x_{k+1})
\right)
=
f(x_0)-f(x_T).

Because f(x_T)\geq f^\star,

f(x_0)-f(x_T)
\leq
f(x_0)-f^\star.

Thus,

\frac{\alpha}{2}
\sum_{k=0}^{T-1}
\|\nabla f(x_k)\|_2^2
\leq
f(x_0)-f^\star.

The red annotation says this is the “average of all the gradients.”

Divide both sides by T:

\frac{1}{T}
\sum_{k=0}^{T-1}
\|\nabla f(x_k)\|_2^2
\leq
\frac{2(f(x_0)-f^\star)}{\alpha T}.

Since the minimum is no larger than the average,

\min_{0\leq k\leq T-1}
\|\nabla f(x_k)\|_2^2
\leq
\frac{1}{T}
\sum_{k=0}^{T-1}
\|\nabla f(x_k)\|_2^2.

Therefore,

\min_{0\leq k\leq T-1}
\|\nabla f(x_k)\|_2^2
\leq
\frac{2(f(x_0)-f^\star)}{\alpha T}.

Taking square roots,

\min_{0\leq k\leq T-1}
\|\nabla f(x_k)\|_2
\leq
\sqrt{
\frac{2(f(x_0)-f^\star)}{\alpha T}
}.

⸻

Theorem: non-convex GD convergence

With

\alpha=\frac{1}{L},

gradient descent satisfies

\min_{0\leq k\leq T-1}
\|\nabla f(x_k)\|
\leq
\sqrt{
\frac{2L(f(x_0)-f^\star)}{T}
}.

For all L-smooth functions

f:\mathbb{R}^n\to\mathbb{R}.

This gives a sublinear convergence rate:

\min_k \|\nabla f(x_k)\|
=
O\left(\frac{1}{\sqrt{T}}\right).

Important interpretation:

In non-convex optimization, GD is guaranteed to find an approximately stationary point, not necessarily a global minimum.

⸻

11.2 Convex case: faster convergence to function value

Assume f is convex and L-smooth.

Gradient descent update:

x_{k+1}=x_k-\alpha \nabla f(x_k).

Consider the squared distance to the optimizer:

\|x_{k+1}-x^\star\|^2.

Expand:

\|x_{k+1}-x^\star\|^2
=
\|x_k-\alpha \nabla f(x_k)-x^\star\|^2.

=
\|x_k-x^\star\|^2
-
2\alpha
\langle
\nabla f(x_k),x_k-x^\star
\rangle
+
\alpha^2
\|\nabla f(x_k)\|^2.

Using convexity,

\langle
\nabla f(x_k),x_k-x^\star
\rangle
\geq
f(x_k)-f^\star.

This gives a first notion / metric of convergence:

f(x_k)-f^\star
\leq
\frac{L}{2k}\|x_0-x^\star\|^2.

So the convex case gives function-value convergence at rate

O(1/k).

⸻

12. Momentum: Why and How?

12.1 Motivation

Consider a quadratic objective:

f(x)=\frac{1}{2}x^\top Hx.

Here H is a positive semidefinite matrix.

The notes state that the eigenvalues of H are in an interval, likely

[\mu,L].

Gradient:

\nabla f(x)=Hx.

The global solution/minimum is

x^\star=0.

We track how quickly

x\to 0.

⸻

Diagonalization

Diagonalize

H=U\Lambda U^\top,

where

\Lambda=
\begin{bmatrix}
\lambda_1 & 0\\
0 & \lambda_2
\end{bmatrix}

in the two-dimensional example.

Assume H is diagonalizable.

The notes define a coordinate transformation:

z_k = U^\top x_k.

Gradient descent update:

x_{k+1}
=
x_k-\alpha \nabla f(x_k).

For this quadratic,

x_{k+1}
=
x_k-\alpha Hx_k.

Multiply both sides by U^\top:

U^\top x_{k+1}
=
U^\top x_k-\alpha U^\top Hx_k.

Since z_k=U^\top x_k, this becomes

z_{k+1}
=
z_k-\alpha U^\top H U z_k.

Because

U^\top H U=\Lambda,

we get

z_{k+1}=z_k-\alpha \Lambda z_k.

This is now a vector equation.

For two dimensions:

\begin{bmatrix}
z_{k+1,1}\\
z_{k+1,2}
\end{bmatrix}
=
\begin{bmatrix}
z_{k,1}\\
z_{k,2}
\end{bmatrix}
-
\alpha
\begin{bmatrix}
\lambda & 0\\
0 & \mu
\end{bmatrix}
\begin{bmatrix}
z_{k,1}\\
z_{k,2}
\end{bmatrix}.

Therefore,

z_{k+1,1}=z_{k,1}-\alpha\lambda z_{k,1},

z_{k+1,2}=z_{k,2}-\alpha\mu z_{k,2}.

Equivalently,

z_{k+1,1}=(1-\alpha\lambda)z_{k,1},

z_{k+1,2}=(1-\alpha\mu)z_{k,2}.

The red note says these are “two scalar equations.”

⸻

Stability / convergence requirement

For convergence, we need

|1-\alpha L|<1.

Thus,

\alpha < \frac{2}{L}.

If we plug in

\alpha=\frac{1}{L},

then for the second coordinate,

z_{k+1,2}
=
\left(1-\frac{\mu}{L}\right)z_{k,2}.

If \mu\ll L, for example

L=10000,\qquad \mu=0.1,

then

1-\frac{\mu}{L}
=
1-\frac{0.1}{10000}
\approx 1.

Therefore,

z_{k+1,2}\approx z_{k,2}.

This means progress in the small-eigenvalue direction is extremely slow.

Red annotation:

Ideally, you want L\approx \mu.

This means the condition number should be good. If L is much larger than \mu, gradient descent becomes slow.

⸻

13. Momentum / Heavy-ball / Polyak

Momentum update:

x_{k+1}
=
x_k
-
\alpha \nabla f(x_k)
+
\beta(x_k-x_{k-1}).

The notes annotate:

* \beta controls how much history is retained.
* This is another form for writing momentum.
* The method actually uses a two-step process.

Equivalent two-step form:

m_k=\beta m_{k-1}+(1-\beta)\nabla f(x_k),

x_{k+1}=x_k-\alpha m_k.

The notes emphasize:

This is not equivalent to Nesterov momentum.

Nesterov momentum evaluates the gradient at a look-ahead point, commonly written as something like

x_k+\beta(x_k-x_{k-1}),

rather than simply using \nabla f(x_k).

⸻

14. Why Momentum Accelerates

Use the same quadratic example:

f(x)=\frac{1}{2}x^\top Hx,
\qquad
x\in\mathbb{R}^2.

Assume

\[
H\succeq 0.
\]

The eigenvalues satisfy

\lambda(H)=\{\mu,\ldots,L\}.

Using similar derivation rules, but applying momentum-GD:

z_{k+1,i}
=
(1-\alpha\lambda_i+\beta)z_{k,i}
-
\beta z_{k-1,i}.

Here:

* i denotes an arbitrary dimension.
* \lambda_i denotes an eigenvalue.
* \lambda_i \in [\mu,L].

For ordinary GD, the update was

z_{k+1,i}=(1-\alpha\lambda_i)z_{k,i}.

⸻

14.1 Ratio of contraction

Define the ratio of contraction:

r_{k,i}
=
\frac{z_{k+1,i}}{z_{k,i}}.

For GD,

r_{k,i}=1-\alpha\lambda_i.

For momentum / heavy-ball GD, use

z_{k+1,i}
=
(1+\beta-\alpha\lambda_i)z_{k,i}
-
\beta z_{k-1,i}.

Divide by z_{k,i}:

r_{k,i}^{HB}
=
1+\beta-\alpha\lambda_i
-
\frac{\beta}{r_{k-1,i}^{HB}}.

This equation is boxed in red in the notes.

⸻

14.2 Interpretation

Here x_k,z_k\in\mathbb{R}^n, and x_{k,i} is the i-th entry of vector x_k.

The notes discuss two cases.

⸻

Case 1: Steep direction, large \lambda_i

If \lambda_i is large, then

1+\beta-\alpha\lambda_i

can become negative because of the larger step size \alpha.

Then the term

-\frac{\beta}{r_{k-1,i}^{HB}}

serves as a counter-balance.

The notes say:

\text{Goal: }
\left|
1+\beta-\alpha\lambda_i
-
\frac{\beta}{r_{k-1,i}^{HB}}
\right|
\approx 0.

Assuming

r_{k-1,i}^{HB}

and

r_{k,i}^{HB}

have the same sign, the

-\frac{\beta}{r_{k-1,i}^{HB}}

term will decrease the magnitude of

\left|
1+\beta-\alpha\lambda_i
-
\frac{\beta}{r_{k-1,i}^{HB}}
\right|.

Interpretation:

Momentum can stabilize or damp oscillation in steep directions.

⸻

Case 2: Flat direction, small \lambda_i

If \lambda_i is small, then in the unfortunate event/set,

r_{k,i}\approx 1.

Then

1+\beta-\alpha\lambda_i-\frac{\beta}{r_{k-1,i}}
\approx
1+\beta-\alpha\lambda_i-\beta
=
1-\alpha\lambda_i.

The notes end by saying:

7.4 and 7.5 are not covered.

This means the lecture stops before the next sections.