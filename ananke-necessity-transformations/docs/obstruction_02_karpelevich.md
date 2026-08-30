# Obstruction 02: finite classical memory from noisy invariant spectra

## 1. From an exact infinity claim to a finite-data lower bound

The v0 obstruction used an exact peripheral eigenvalue whose phase was not a root
of unity. That excludes every exact finite stochastic realization, but finite data
cannot establish either exact modulus one or irrational phase.

V1 asks a weaker question that finite data can answer:

> How many hidden states must any exact classical stochastic realization have before
> its allowed eigenvalue region reaches the confidence set of the extracted mode?

## 2. Spectral inheritance

Let an \(N\)-state classical realization use a row-stochastic transition matrix
\(M_a\) for operation \(a\). Restricting to its reachable space and quotienting by
its unobservable invariant subspace produces the minimal linear transition
\(T_a\). Consequently, the characteristic polynomial of the quotient divides that
of the relevant restriction, and every eigenvalue of \(T_a\) must occur in
\(M_a\).

Thus an invariant eigenvalue of the minimal behavioural process is a legitimate
constraint on every larger finite classical realization.

## 3. The Karpelevič region

Define

\[
\Theta_N
=
\left\{
\lambda\in\mathbb C:
\lambda\text{ is an eigenvalue of some }N\times N
\text{ stochastic matrix}
\right\}.
\]

The regions are nested:

\[
\Theta_1\subseteq\Theta_2\subseteq\cdots\subseteq\{z:|z|\le1\}.
\]

Their intersections with the unit circle are roots of unity of orders no greater
than \(N\). Between Farey-neighbour roots, the boundary follows algebraic
Karpelevič/Ito arcs.

V1 implements the radial boundary characterization from Stephen Kirkland, Thomas
Laffey and Helena Šmigoc, *The Karpelevič Region Revisited* (2020):

<https://arxiv.org/abs/2005.02452>

As a regression test, the implementation reproduces their example

\[
z=0.9e^{7\pi i/12},
\]

for which

\[
\rho_5(7\pi/12)=0.8675221205<0.9,
\qquad
\rho_6(7\pi/12)=0.9114159453>0.9.
\]

Therefore \(z\notin\Theta_5\) but \(z\in\Theta_6\).

## 4. Analytic certificate

A necessary Dmitriev–Dynkin tangent-wedge condition for an eigenvalue
\(\lambda=x+iy\) of an \(N\)-state stochastic matrix is

\[
|y|\le \cot\!\left(\frac{\pi}{N}\right)(1-x).
\]

The Euclidean distance of the estimated mode from this half-plane is computed
exactly in floating arithmetic. If that distance exceeds the bootstrap-disk radius,
the entire disk lies outside the necessary region and every \(N\)-state model is
excluded.

For the baseline noisy-qubit run, this excludes all classical models with
\(N\le8\), hence

\[
\boxed{N_{\mathrm{classical}}\ge9}
\]

at the declared 99% bootstrap level, conditional on selected rank four and the
sequential interface.

## 5. Full-region numerical certificate

The sharper test minimizes Euclidean distance from the point estimate to the full
boundary of \(\Theta_N\). It uses:

1. a global angular grid;
2. refinement of several best candidate intervals by golden-section search;
3. independent coarse and doubled-resolution runs;
4. a conservative convergence penalty based on their disagreement.

If the convergence-guarded distance exceeds the confidence-disk radius, the disk is
reported numerically disjoint from \(\Theta_N\).

For the baseline run, the 99% disk is disjoint through \(\Theta_{15}\), giving

\[
\boxed{N_{\mathrm{classical}}\ge16}
\]

under the full-region numerical test.

This sharper number is not presented as a formal interval-arithmetic proof. The
analytic lower bound of nine has the cleaner theorem-level geometry; the bound of
sixteen additionally depends on floating-point global boundary minimization and the
bootstrap approximation.

## 6. Calibration against a known classical boundary model

A three-state deterministic cycle has the mode

\[
e^{2\pi i/3}\in\partial\Theta_3.
\]

V1 generated 100 independent datasets from that model, each with 10,000 shots per
word, and used a nominal 99% confidence disk. The test falsely excluded
\(\Theta_3\) once. A damped cycle with eigenvalue

\[
0.88e^{2\pi i/3}\in\operatorname{int}\Theta_3
\]

was also retained.

## 7. Relation to prior work

The use of observable Hankel dynamics and stochastic eigenvalue regions to separate
classical and quantum dimensions has direct precedent in Michael Wolf and David
Pérez-García, *Assessing dimensions from evolution* (2009):

<https://arxiv.org/abs/0901.2542>

Finite-dimensional processes without finite classical realizations, including noisy
memory lower bounds for related quantum processes, are developed by Fanizza et al.:

<https://arxiv.org/abs/2209.11225>

ANANKE v1's candidate contribution is not the Karpelevič theorem or the existence of
classical/quantum dimension gaps. It is the integrated operational pipeline:

\[
\text{finite word counts}
\rightarrow
\text{held-out Hankel rank}
\rightarrow
\text{bootstrap invariant mode}
\rightarrow
\text{finite classical-memory lower bound},
\]

extended to a controlled multi-operation process and accompanied by explicit
false-positive calibration.
