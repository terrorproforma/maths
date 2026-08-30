# TP-02 Phase 2 summary — inhomogeneous gauge-group sign audit

## Verdict

\[
\boxed{\text{The printed formulas in draft sections 6–7 are not mutually consistent.}}
\]

The right action, semidirect-product law, and tilted map

\[
\tau_-(h)=\left(h,-h^{-1}d_{A_0}h\right)
\]

are mutually consistent and make \(\tau_-\) the stabilizer of \(A_0\). But the printed augmented torsion

\[
T_-=a-\varepsilon^{-1}d_{A_0}\varepsilon
\]

obeys

\[
T_-(g\tau_-(h))=h^{-1}T_-(g)h-2h^{-1}d_{A_0}h,
\]

not the claimed equivariance law.

## Exact executable result

- Semidirect associativity: **PASS**
- Affine right action: **PASS**
- Tilted-map homomorphism: **PASS**
- \(A_0\) stabilization: **PASS**
- Printed torsion equivariance: **FAIL**
- Analytic failure term \(-2h^{-1}d_{A_0}h\): **PASS**
- Plus-sign torsion repair: **PASS**

## Repaired branch

\[
\widetilde T=a+\varepsilon^{-1}d_{A_0}\varepsilon.
\]

This is equivalent to reversing the ordered affine-difference map while keeping the source's right action and stabilizer.

## Scope

This is a repairable source-level algebraic inconsistency. It is not yet a no-go theorem against Geometric Unity as a model class.

## Next calculation

Independently vary the first-order bosonic action in both the literal printed branch and the repaired branch, retaining the full observation dependence of \(A_0\). Then compare their gauge identities, deformation operators, and principal symbols.
