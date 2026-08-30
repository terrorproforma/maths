# TP-02 status

**Author:** Angus Muffatti  
**Version:** 0.4.0  
**Status date:** 31 August 2026  
**Project state:** **ACTIVE — source-faithful reconstruction reaches a precise incompleteness result; repaired completion proceeds separately**

## Phase ledger

### Phase 1 — primary-source reconstruction

Completed:

- frozen official source manifest;
- typed initial theory tuple;
- source-definition and claim ledgers;
- exact representation-dimension bookkeeping;
- separation of source claims from independent checks.

### Phase 2 — inhomogeneous gauge-group sign audit

Completed:

\[
T_-\bigl(g\tau_-(h)\bigr)
=
h^{-1}T_-(g)h
-
2h^{-1}d_{A_0}h.
\]

The printed augmented torsion is not equivariant under the printed tilted stabiliser.

A reversible stabiliser-compatible repair was frozen:

\[
T_+
=
a+\varepsilon^{-1}d_{A_0}\varepsilon.
\]

### Phase 3A — first-order action covariance

Completed:

\[
I_-^h-I_-=14,
\qquad
I_+^h-I_+=0.
\]

The literal branch fails its claimed invariant action form. The repaired branch passes the exact kinematic test.

### Phase 3B — official Oxford source and explicit Shiab

Completed:

- classified the official Oxford page as a composite primary source;
- indexed the 2013 lecture, 2020 presentation context and supplementary PowerPoint separately;
- identified the cross-version sign pair
  \[
  \tau_+,\ T_-;
  \]
- typed draft eq. (9.3) as
  \[
  \Omega^2(Y,\operatorname{ad}P_H)\to\Omega^{13}(Y,\operatorname{ad}P_H);
  \]
- derived the relevant Hodge-star degree and signature signs;
- proved the Clifford–Einstein selection lemma;
- verified exact annihilation of an independently constructed algebraic Weyl tensor;
- established the \(n=14\) Riemann-sector benchmark
  \[
  \operatorname{rank}=105,\qquad\dim\ker=3080;
  \]
- derived the universal \(\varepsilon\)-, curvature- and metric-slot variations of the displayed operator.

## Terminal source-faithful result

\[
\boxed{
\begin{array}{c}
\text{The explicit substitute is mathematically meaningful on the}\\
\text{geometric Riemann-curvature subspace.}\\[1mm]
\text{The official corpus does not define its unique full adjoint extension,}\\
\text{complete observation derivative, boundary domain or physical Hessian.}
\end{array}
}
\]

Therefore:

\[
\boxed{
\text{no unique full principal symbol or degree-of-freedom count can be attributed to the source alone.}
}
\]

## Current gate status

- `ALG-01`: **1 — PARTIAL / SOURCE-INCOMPLETE**. The explicit substitute is typed, but the full theory tuple and observable/domain data are incomplete.
- Literal branch `ALG-02`: **0 — FAIL** for the claimed covariant first-order action.
- Repaired branch `ALG-02`: **1 — PARTIAL** pending deformation/BRST closure.
- `ALG-05`, `ALG-06`, `PERT-01` through `PERT-05`, and recovery gates remain unresolved for the independent completion branch.
- `REP-01`: **1 — PARTIAL**, with exact executable audits but no complete executable theory.

No aggregate score is used.

## Active next phase — \(\mathsf{R}_+\)-EIN

The project now moves from reconstruction to an explicitly labelled completion:

1. build exact \(Cl(7,7)\) gamma representatives;
2. construct explicit \(\Phi_1,\Phi_2\);
3. choose and document the full adjoint product extension;
4. declare metric, orientation, reality and boundary domains;
5. derive the repaired quadratic action;
6. compute the principal symbol and gauge complex;
7. count physical modes.

A fatal zero on closure, kinetic rank, hyperbolicity or physical degrees of freedom terminates that candidate branch.

## Reproduction

```bash
make verify
```
