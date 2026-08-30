# Arithmetic necessity: why the memory bound is a staircase

## 1. The unexpected structure

Write a unit-modulus transition mode as

\[
\lambda=e^{2\pi i\alpha},
\qquad \alpha\in[0,1).
\]

An \(N\)-state deterministic classical cycle can place peripheral eigenvalues only
at roots of unity

\[
e^{2\pi i p/q},\qquad q\le N.
\]

The ability of finite classical memory to mimic \(\lambda\) is therefore controlled
by rational approximation of \(\alpha\).

The original ANANKE angle was chosen simply as \(0.73\) radians. Its phase in turns
is

\[
\alpha=\frac{0.73}{2\pi}
=0.116183108457\ldots
\]

and its continued fraction begins

\[
\boxed{
\alpha=[0;8,1,1,1,1,5,31,1,20,4,2,\ldots].
}
\]

The first convergent denominators are

\[
1,\ 8,\ 9,\ 17,\ 26,\ 43,\ 241,\ 7514,\ldots
\]

That arithmetic sequence explains the visible plateaus and jumps in the
Karpelevič state-count bound.

## 2. The accidental noble shadow

Consider the noble number

\[
\alpha_*
=[0;8,\overline{1}]
=\frac{1}{8+1/\varphi},
\qquad
\varphi=\frac{1+\sqrt5}{2}.
\]

Its angle is

\[
2\pi\alpha_*=0.729074092233\ldots\text{ radians}.
\]

The original \(0.73\)-radian choice differs by only

\[
9.25908\times10^{-4}\text{ radians}
=0.05305^\circ.
\]

So the arbitrarily chosen gate accidentally follows the noble continued-fraction
tail for five consecutive coefficients. Its early memory thresholds consequently
follow the near-Fibonacci recurrence

\[
8,\ 9,\ 17,\ 26,\ 43,\ldots
\]

## 3. Where the current angle eventually fails

The next partial quotient of the current phase is \(5\), producing the unusually
good convergent

\[
\frac{28}{241}.
\]

At maximum cycle order 241, the current phase is only

\[
3.3668\times10^{-6}
\]

away from the corresponding root of unity in the complex plane. The noble target's
nearest available root at the same order is still

\[
8.5742\times10^{-5}
\]

away—about 25.47 times farther.

Thus the current gate is excellent for early finite-state separation but contains a
future arithmetic trap at order 241.

## 4. Experimental-design hypothesis

This suggests a new design principle:

> Do not choose witness transformations merely because they are noncommuting or
> have irrational phases. Choose phases whose continued fractions deliberately
> resist low-denominator rational approximation over the classical-memory range
> one intends to exclude.

Within a fixed near-identity sector, a noble tail

\[
[0;k,\overline{1}]
\]

is the natural asymptotic candidate because continued fractions with bounded small
partial quotients avoid sporadically exceptional rational approximants.

This does **not** yet prove that noble phases maximize the full finite-shot
Karpelevič confidence distance. The complete optimum also depends on:

- the curvature of the stochastic eigenvalue region, not only its unit-circle roots;
- sensitivity of Hankel extraction to the chosen preparation and measurement;
- the spectrum of every controlled transformation jointly;
- shot allocation and estimator bias.

The result is therefore a strong design hypothesis plus an exact arithmetic
diagnosis, not an optimality theorem.

## 5. The more alien interpretation

The extracted transformation does not merely carry a real-valued angle. It carries a
hierarchy of possible finite ontological counterfeits. Each continued-fraction
convergent marks a classical memory size at which a qualitatively better counterfeit
becomes available.

In that sense, the transformation's operational necessity has an **arithmetic
spectrum**:

\[
\boxed{
\text{precision scale}
\longleftrightarrow
\text{minimum counterfeit ontology size}
}
\]

Necessity is not binary. It is a staircase of how much alternative machinery must be
paid to erase the transformation.
