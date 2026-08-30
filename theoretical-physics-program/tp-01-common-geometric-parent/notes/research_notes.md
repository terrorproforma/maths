# Research notes - TP-01 v1.1

## Decisive correction

The named follow-up calculation does not rescue the strong parent claim. It makes the failure sharper:

- The parent has a perfectly consistent generic canonical sector, but it is a 13-mode theory.
- The Einstein surface has the correct pulled-back Einstein-Cartan symplectic coefficients.
- Nevertheless the surface is not invariant under the parent equations and is not a BRST gauge slice.
- The gauge-invariant holonomy norm/conjugacy class is external physical data.
- Adding the first nonzero KK level cannot be done as an exact finite nonlinear truncation; the loop algebra generates the full tower.
- At quadratic order the first KK pair adds 26 real regular-sector modes.

The distinction is now:

\[
\boxed{
\text{correct action and symplectic pullback}
\neq
\text{consistent dynamical reduction}.
}
\]

## What unexpectedly passed

The local covariant symplectic pullback is not the problem. On the fixed surface,

\[
\theta_{\rm pull}
=2\alpha\epsilon_{abcd}\delta\omega^{ab}
\left(R^{cd}+\ell^{-2}e^ce^d\right),
\]

which is exactly the Euler potential plus the Einstein-Cartan potential. After the Euler transgression boundary completion, the bulk daughter phase-space form is the expected one.

This is useful because it localizes the obstruction. The failure lies in deleted equations, non-invariance, gauge-invariant holonomy data and extra parent modes - not in a missing coefficient of the GR kinetic term on the restricted surface.

## What failed hardest

The fixed norm cannot be gauge. In the narrow vector description, `SO(3,2)` has a four-dimensional orbit through a nonzero timelike vector, leaving one norm invariant. In the full adjoint compactification, `ad(J_54)` has rank 8 and a seven-dimensional centralizer. The conjugacy class of

\[
W=\exp(L_yvJ_{54})
\]

is physical, with

\[
\operatorname{tr}_{\bf6}W=4+2\cosh(L_yv).
\]

The radial equation

\[
\langle\phi F\wedge F\rangle=0
\]

is gauge invariant. It is exactly the equation that generic Einstein solutions fail.

## Publication position

The result is now suitable for a preprint as a mathematical-physics clarification. The strongest paper is not a claim of a new ultimate action. It is a theorem about the difference between:

- exact cohomological descent;
- correct symplectic pullback;
- BRST gauge fixing;
- consistent truncation;
- and spectrum-preserving reduction.

An independent expert should still verify the global integral normalization and the treatment of exotic degenerate strata before journal submission.
