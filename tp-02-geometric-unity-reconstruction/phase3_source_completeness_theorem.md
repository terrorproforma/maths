# Phase 3B — Variational source-completeness theorem

## Statement

A displayed first-order functional does not uniquely determine its Euler–Lagrange operator, Hessian, principal symbol, or propagating degrees of freedom unless every field-dependent map in the functional is typed together with its variation and domain.

For the repaired Geometric Unity branch, write the action schematically as

\[
I_+[\omega,\gimel]
=
\int_Y
\mu_{\gimel}
\left\langle
T_+(\omega,\gimel),
\operatorname{Sh}_{\omega,\gimel}(F_\omega)
\right\rangle_{\gimel}.
\]

The data required to define its linearized dynamics are the tuple

\[
\mathfrak V=
\left(
Y,
\mathcal E_\omega,
\mathcal E_T,
\mathcal E_F,
\mu,
\langle\cdot,\cdot\rangle,
A_0[\gimel],
T_+,
\operatorname{Sh},
F,
\mathcal B
\right),
\]

where \(\mathcal B\) denotes boundary/domain data.

At a background \((\bar\omega,\bar\gimel)\), the first variation contains

\[
D\operatorname{Sh}_{\bar\omega,\bar\gimel}
[\delta\omega,\delta\gimel](F_{\bar\omega}),
\]

\[
\operatorname{Sh}_{\bar\omega,\bar\gimel}
(d_{\bar\omega}\delta\omega),
\]

\[
D A_0|_{\bar\gimel}[\delta\gimel],
\]

and the variations of the measure and pairing. The Hessian additionally requires the corresponding second derivatives.

## Theorem

> **Variational source-completeness theorem.** Suppose a source fixes the names and pointwise types of \(T\), \(F\), and \(\operatorname{Sh}\), but does not uniquely fix the background value of \(\operatorname{Sh}\), its Fréchet derivative, the observation-to-connection derivative \(D A_0\), or the integration-by-parts domain. Then the source does not determine a unique Euler–Lagrange linearization or principal symbol. Consequently it cannot determine a unique physical degree-of-freedom count.

## Proof

The linearized curvature is

\[
\delta F=d_{\bar\omega}\delta\omega.
\]

The Shiab-curvature factor varies as

\[
\delta\bigl(\operatorname{Sh}(F)\bigr)
=
(D\operatorname{Sh})[\delta\omega,\delta\gimel](F_{\bar\omega})
+
\operatorname{Sh}_{\bar\omega,\bar\gimel}
(d_{\bar\omega}\delta\omega).
\]

The leading derivative term in the Hessian therefore contains the leading symbol of

\[
\operatorname{Sh}_{\bar\omega,\bar\gimel}\circ d_{\bar\omega},
\]

as well as any leading derivative contribution induced by

\[
D A_0|_{\bar\gimel}.
\]

Choose two covariant bundle maps \(C_1,C_2:\mathcal E_F\to\mathcal E_T\) with the same declared domain and codomain but different contractions on the image of the symbol of \(d_{\bar\omega}\). Both may satisfy the same verbal description and both give zero on a flat background \(F_{\bar\omega}=0\), yet

\[
\sigma(C_1\circ d_{\bar\omega})(k)
\neq
\sigma(C_2\circ d_{\bar\omega})(k)
\]

for some covector \(k\). The two completions then possess different quadratic kinetic operators and potentially different kernels, characteristic cones, and mode counts.

Likewise, two observation-induced connections agreeing at \(\bar\gimel\) but having different derivatives \(D A_0|_{\bar\gimel}\) give the same background action and different linearized coupling to observation-field perturbations.

Finally, changing the boundary/domain data changes which formal integrations by parts are valid and which directions are gauge, constrained, or physical. Hence the displayed functional without the missing derivatives and domains does not select one linearized theory. ∎

## Application to TP-02

The current reconstruction has fixed:

- the total-space dimension and principal geometric bundles at a preliminary level;
- the right inhomogeneous group law;
- the actual tilted stabilizer;
- a repaired covariant augmented torsion \(T_+\);
- the universal variation of \(T_+\).

It has not yet independently frozen:

1. the exact substitute Shiab of draft eq. (9.3) as a typed bundle map;
2. its dependence on the unified and observation fields;
3. its Fréchet derivative;
4. the complete derivative of the observation-induced connection;
5. the metric dependence of the pairing and measure;
6. the boundary and adjoint domains;
7. a background satisfying the repaired field equations.

Therefore a numerical eigenvalue calculation performed before those items are fixed would diagonalize an investigator's completion, not a uniquely reconstructed source theory.

## Consequence

This is not a terminal theorem that Geometric Unity cannot be completed. It is a terminal theorem about what the current source-typed data can support:

\[
\boxed{
\text{no unique principal symbol or mode count follows yet from the primary presentation.}
}
\]

The project must now either:

1. type the explicit eq. (9.3) substitute and complete the derivative/domain data; or
2. prove that the official source leaves one of those indispensable objects non-unique.

No sympathetic interpolation may be blended into the source branch without a separate model identifier.
