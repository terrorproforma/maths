# Finite-Temperature Tensor-Basis Specification - v1.9

**Author:** Angus Muffatti  
**Status:** Frozen component spaces for the pilot  
**Date:** 24 August 2026

## Declared state symmetry

- Homogeneous plasma with a preferred time-like four-vector u^mu.
- CP-even and parity-even background; no chiral chemical potential.
- Electroweak-symmetric phase and exact color/weak covariance.
- Angular anisotropy is carried by spherical-harmonic dependence of form factors, not by adding a fixed anisotropy vector.

At generic kinematics, the pilot evolves a **complete component space** compatible with the declared symmetries. Ward or Slavnov-Taylor identities fix longitudinal components; orthogonal transverse components remain dynamical. Symmetry relations are imposed as constraints, not used to delete components before the evolution demonstrates redundancy.

## Object catalogue

| Object | Raw components | Evolved basis | Constraints | Comment |
| --- | --- | --- | --- | --- |
| gauge propagator D_G^{mu nu} | 16 | 4 | Background gauge condition and STI monitor; physical self-energy transverse subspace has two dressings in equilibrium. | The fourth mixed structure is retained as a truncation/gauge diagnostic. |
| fermion inverse propagator S^{-1} | 16 | 3 | Chiral projector removes the scalar term for Q_L; vectorlike D retains it. | Additional CP-odd structures are excluded by the declared state symmetry. |
| fermion-gauge vertex Gamma^mu | 64 | 16 L + 48 T | Longitudinal 16-component matrix fixed by STI; transverse 48-component subspace evolved. | This replaces the four-tensor seed used only for v1.8 initialization. |
| scalar-gauge or ghost-gauge vertex Gamma^mu | 4 | 1 L + 3 T | Longitudinal component fixed by Ward/ST identity. | Complete for a Lorentz vector at generic non-null Q. |
| Yukawa H-Q-D vertex | 16 | 4 | Gauge representation and chirality. | Four complex components per chiral orientation at generic kinematics. |
| matter-ghost kernel H(P,Q) | 16 | 16 | Color/group tensor factored; matrix form factors are evolved or reconstructed. | This removes the v1.8 common-scalar-kernel limitation. |
| three-gauge vertex Gamma^{mu nu rho} | 64 |  | Longitudinal/STI completion plus Bose/color permutation constraints. | The 27 fully transverse amplitudes are evolved; permutation symmetry is enforced as a linear projector. |
| H-dagger-H Bethe-Salpeter vertex | 1 | 1 | Kernel K=delta Sigma_H/delta G_H from the identical truncation. | Primary gauge-invariant spectral control. |

## Complete Clifford space

\[
\left\{\mathbf 1,\gamma^\mu,\sigma^{\mu\nu},\gamma^5\gamma^\mu,\gamma^5\right\}
\]

has numerical rank

\[
\boxed{16}.
\]

## Fermion-gauge vertices

A generic vector-Dirac vertex contains \(4\times16=64\) complex components. At nonzero transfer momentum,

\[
64 = 16_{\rm longitudinal}+48_{\rm transverse}.
\]

The STI reconstructs the longitudinal matrix sector. The solver evolves the full 48-component transverse null-space basis. Validation gives

\[
\operatorname{rank}\Gamma_T=48,
\qquad
\max\frac{\|Q_\mu\Gamma_T^\mu\|}{\|Q\|\,\|\Gamma_T\|}=1.556e-17.
\]

## Scalar/ghost-gauge and Yukawa vertices

A scalar- or ghost-gauge vector has one longitudinal and three transverse components. For one chiral portal orientation, the projected Clifford basis \(P_R\Gamma_A P_L\) has rank four; the conjugate orientation is stored separately.

## Matter-ghost kernels

All 16 Clifford components are allocated for each required matter-ghost scattering kernel. The STI has the schematic form

\[
Q_\mu\Gamma_A^\mu=gT^AF(Q^2)\left[S^{-1}(P+Q)H-\overline H S^{-1}(P)\right].
\]

## Three-gauge vertex

For \(P+Q+R=0\), each Lorentz leg has a three-dimensional transverse component space. Before Bose/color/permutation reduction, the complete fully transverse component basis has

\[
3^3=27
\]

components. Validation gives

\[
\operatorname{rank}=27,
\qquad
\max\mathcal R_T=4.445e-16.
\]

The number 27 is a component-space dimension, not a claim that 27 independent physical scalar form factors survive all symmetry identities.

## Singular kinematics

At zero transfer or exceptional collinear configurations, the generic projector basis is non-unique. The solver must approach these cells continuously, use singular-value decomposition, and report rank loss rather than silently switching basis.

## Verdict

All declared generic component spaces have the expected rank and transversality. Dynamical sufficiency remains a pilot convergence question tested by basis enlargement and identity scans.
