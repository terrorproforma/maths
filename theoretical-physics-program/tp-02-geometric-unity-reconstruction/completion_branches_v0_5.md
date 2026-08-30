# TP-02 convention and completion branches v0.5

This file prevents source claims, source repairs and independent completions from being blended.

| Branch | Tilted map | Augmented torsion | Shiab / propagation choice | Status |
|---|---|---|---|---|
| `OXFORD` | \(+h^{-1}d_{A_0}h\) | minus | lecture/slide family | Historical official branch; not the 2021 stabiliser convention |
| `DRAFT_LITERAL` | minus | minus | draft eq. (9.3) | Rejected: torsion covariance and first-order action covariance fail |
| `R_PLUS` | minus | plus | unspecified | Stabiliser-compatible repair; kinematic covariance passes |
| `R_PLUS_EIN_ALG` | minus | plus | exact mixed Clifford Einstein completion | Passes algebraic and full-adjoint codomain checks |
| `R_PLUS_EIN_FULL_Y` | minus | plus | local propagation on all of signature-\((7,7)\) \(Y\) | Rejected: fatal `PERT-02` hyperbolicity failure |
| `R_PLUS_EIN_OBS4` | minus | plus | dynamically projected rank-four Lorentzian characteristics | Open; projector, constraints and two-helicity count not yet derived |

## Governing rule

No independent completion is called “Geometric Unity” without qualification.

The source-faithful reconstruction terminates at a precise incompleteness result. Every later branch is a project-selected model whose extra choices are stated explicitly.

## Exact algebraic completion

`R_PLUS_EIN_ALG` fixes:

\[
\Phi_1=e^A\otimes\Gamma_A,
\qquad
\Phi_2=\frac12e^A\wedge e^B\otimes\Gamma_{AB},
\]

with an exact real \(\mathrm{Cl}(7,7)\) representation and split spinor form of signature \((64,64)\).

Its full-adjoint Einstein map is

\[
\mathcal E_d(X)
=
[\Gamma^c,X_{cd}]
+
\frac14
\left\{
\left\{\Gamma^{cd},X_{cd}\right\},
\Gamma_d
\right\}.
\]

## Physical branch condition

A successor branch must derive a rank-four Lorentzian characteristic distribution before any claim of four-dimensional propagation. External restriction of allowed momenta or initial data is not a dynamical reduction.

The next branch must therefore provide:

1. a rank-four projector;
2. gauge/BRST invariance;
3. propagation of the projector constraint;
4. a strongly hyperbolic reduced system;
5. exactly two graviton helicities;
6. compatible Standard Model characteristics.
