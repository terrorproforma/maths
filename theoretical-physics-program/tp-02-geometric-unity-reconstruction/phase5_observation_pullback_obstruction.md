# Phase 5 — Pullback is not dynamical reduction

**Project:** TP-02 — Independent Reconstruction of Geometric Unity  
**Branch:** \(\mathsf R_+\)-EIN-OBS4-PULLBACK  
**Status:** **REJECTED**

## 1. Source-motivated question

The primary construction supplies:

1. an observation map
   \[
   \iota:X^4\hookrightarrow Y^{14};
   \]
2. a pullback metric
   \[
   g_X=\iota^*g_Y;
   \]
3. a normal bundle of rank ten;
4. a split along the observed section
   \[
   \iota^*(T^*Y)
   =
   T^*X\oplus N_\iota^*;
   \]
5. fields native to \(Y\) whose observed values on \(X\) are obtained by pullback.

The missing physical question is not whether the pullback exists. It does.

The question is:

> Does pullback turn the ambient fourteen-dimensional field equation into an autonomous four-dimensional evolution equation for the pulled-back field?

The answer is no for a generic local second-order ambient operator.

## 2. Kinematics versus dynamics

For an embedding \(\iota:X\to Y\), the cotangent pullback

\[
d\iota^*:T^*Y|_{\iota(X)}\to T^*X
\]

is canonical and surjective. Once a metric and normal splitting are selected, one may also decompose ambient covectors into tangential and normal pieces.

This is a kinematic statement.

It does not imply

\[
\iota^*(L_Y\Phi)
=
L_X(\iota^*\Phi)
\]

for some autonomous operator \(L_X\) on \(X\).

The right-hand side knows only the pulled-back field. The left-hand side generally depends on normal derivatives of the ambient field that pullback does not retain.

## 3. Descent criterion

Define the vanishing ideal

\[
I_\iota
=
\{f\in C^\infty(Y):\iota^*f=0\}.
\]

### Proposition

An ambient linear differential operator \(L_Y\) descends to a well-defined operator on field values along \(X\),

\[
L_X:C^\infty(X)\to C^\infty(X),
\]

with

\[
\iota^*L_Y=L_X\iota^*,
\]

only if

\[
\boxed{
L_Y(I_\iota)\subseteq I_\iota.
}
\]

Conversely, preservation of the ideal defines an operator on the quotient

\[
C^\infty(Y)/I_\iota
\cong
C^\infty(X).
\]

### Proof

Suppose \(f\in I_\iota\). Then \(\iota^*f=0\). If a descended operator exists,

\[
\iota^*(L_Yf)
=
L_X(\iota^*f)
=
L_X(0)
=
0.
\]

Hence \(L_Yf\in I_\iota\).

Conversely, if \(I_\iota\) is invariant, \(L_Y\) induces an operator on the quotient by assigning

\[
[f]\mapsto[L_Yf].
\]

The assignment is independent of the chosen extension because differences lie in the invariant ideal. ∎

For systems and bundle-valued fields, the same statement applies componentwise to the corresponding submodule of sections vanishing along the embedding.

## 4. Exact normal-jet counterexample

Choose adapted coordinates

\[
(x^\mu,z^a)
\]

near the observed section, with

\[
\iota(X)=\{z^a=0\}.
\]

Take the ambient principal operator

\[
L_Y
=
g^{AB}\partial_A\partial_B+\text{lower-order terms}.
\]

For any non-null normal coordinate \(z^a\), define

\[
f_a=(z^a)^2.
\]

Then

\[
\iota^*f_a=0
\]

and all first derivatives of \(f_a\) also vanish on the section. Nevertheless,

\[
\left.\partial_{z^a}^2f_a\right|_{X}=2,
\]

so

\[
\boxed{
\iota^*(L_Yf_a)=2g^{aa}\neq0.
}
\]

No operator acting only on \(\iota^*f_a=0\) can reproduce this value.

Therefore:

\[
\boxed{
L_Y(I_\iota)\not\subseteq I_\iota.
}
\]

The ambient second-order equation does not descend to an autonomous equation on pulled-back field values.

This is a normal-jet obstruction, not a coordinate artefact.

## 5. Application to the Einsteinian Observerse

The declared dimensions and signatures are

\[
\dim X=4,
\qquad
\dim Y=14,
\qquad
\operatorname{rank}N_\iota=10,
\]

and, in the convention recording negative then positive directions,

\[
\operatorname{sig}Y=(7,7),
\qquad
\operatorname{sig}X=(1,3),
\qquad
\operatorname{sig}N_\iota=(6,4).
\]

Every one of the ten normal directions is non-null in the source's nondegenerate split metric.

The verifier supplies ten exact witnesses:

\[
\iota^*f_a=0,
\qquad
\iota^*(L_Yf_a)=
\begin{cases}
-2,&a=1,\ldots,6,\\
+2,&a=7,\ldots,10.
\end{cases}
\]

Thus neither the bundle split nor ordinary pullback removes the normal principal derivatives.

## 6. Consequence for the OBS4 branch

The natural pullback candidate

\[
\mathsf R_+\text{-EIN-OBS4-PULLBACK}
\]

does not solve the Phase 4 hyperbolicity problem.

The full ambient equation still contains the split-signature normal derivatives. Restricting its solutions after evolution is not the same as constructing a four-dimensional Cauchy problem.

Therefore:

\[
\boxed{
\texttt{PERT-02}=0
\quad
\text{for the pullback-only OBS4 branch}.
}
\]

The source's algebraic split

\[
\iota^*(T^*Y)
=
T^*X\oplus N_\iota^*
\]

is useful for decomposing observed field components. It does not by itself supply a dynamically preserved characteristic projector.

## 7. What would actually be required

A viable completion must add at least one of the following:

### Tangential principal operator

The principal symbol must annihilate every normal covector:

\[
\sigma(L_Y)(n)=0
\qquad
\forall n\in N_\iota^*.
\]

Then the ambient operator is effectively degenerate/tangential along the observed section.

### Propagated normal-jet constraints

All normal derivatives needed by the ambient equation must be fixed by constraints

\[
\mathcal C_r
\left(
\iota^*\Phi,
\iota^*\nabla_n\Phi,
\ldots,
\iota^*\nabla_n^r\Phi
\right)=0
\]

whose consistency and propagation are proved.

### Induced effective dynamics

One may solve or integrate out the normal dynamics with declared boundary/state data and derive a generally nonlocal effective operator on \(X\).

### Localization or boundary dynamics

Fields may be dynamically localized to the observed section by a potential, defect, brane, phase transition, or boundary action. Its stability and backreaction must be calculated.

None of these mechanisms is fixed in the primary corpus.

## 8. Strongest terminal TP-02 conclusion

The complete source-faithful audit now establishes:

\[
\boxed{
\begin{array}{c}
\text{The geometric architecture is substantial and partially typeable.}\\
\text{The literal printed first-order covariance fails.}\\
\text{A repaired Einstein-like algebraic completion exists.}\\
\text{Local propagation on full }Y^{7,7}\text{ is non-hyperbolic.}\\
\text{Observation pullback alone does not produce autonomous }4D\text{ dynamics.}
\end{array}
}
\]

Accordingly, the official primary corpus does not define a complete healthy successor theory.

Any continuing physical model must introduce new normal-dynamics data not supplied by the source. Such work is legitimate as independent model building, but it is no longer a source-faithful reconstruction of Geometric Unity.

## 9. Project status

TP-02 has reached its terminal source-audit outcome:

\[
\boxed{
\textbf{SOURCE-INCOMPLETE AS A PHYSICAL THEORY, WITH TWO EXPLICIT FAILED BRANCHES.}
}
\]

The failed branches are:

1. literal printed first-order branch — covariance failure;
2. repaired local full-\(Y\) branch — split-signature hyperbolicity failure;
3. repaired pullback-only OBS4 branch — normal-jet descent failure.

The algebraic \(\mathrm{Cl}(7,7)\) and Einstein-contraction results remain valid mathematical components.

## 10. Reproduction

```bash
python code/verify_observation_pullback.py --root .
python -m unittest code.tests.test_observation_pullback -v
```

or

```bash
make verify
```
