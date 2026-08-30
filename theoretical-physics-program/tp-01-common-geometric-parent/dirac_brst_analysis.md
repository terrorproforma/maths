# Dirac and BRST analysis of the compactified parent

## Scope

This file completes the canonical test required by TP-01 v1.0 for the strongest fixed-reference interpretation of the five-dimensional `Spin(4,2)` Chern-Simons/transgression parent. A fully dynamical relative transgression contains two opposite-level bulk Chern-Simons copies plus the transgression boundary coupling; it therefore cannot improve the local degree-of-freedom mismatch. The single-copy analysis is the most favourable case.

The result is complete for the claimed reduction and for a generic regular canonical sector. It is not an atlas of every degenerate or irregular stratum of five-dimensional Chern-Simons phase space.

## 1. Five-dimensional canonical structure

Let `a=1,...,N` label a basis of the gauge algebra, with `N=15` for `so(4,2)`. Split spacetime as `R x Sigma_4`, with spatial indices `I,J=1,...,4`. The Chern-Simons action has the first-order form

\[
I=\int dt\int_{\Sigma_4}
\left[
\ell_a^I(A)\dot A_I^a-A_0^aK_a
\right].
\]

For the rank-three invariant `g_abc`,

\[
K_a=-g_{abc}\epsilon^{IJKL}F^b_{IJ}F^c_{KL},
\]

and

\[
\Omega^{IJ}_{ab}
=\frac{\delta\ell_b^J}{\delta A_I^a}
-\frac{\delta\ell_a^I}{\delta A_J^b}
=-4\epsilon^{IJKL}g_{abc}F^c_{KL}.
\]

The canonical momenta obey the primary constraints

\[
\phi_a^I=p_a^I-\ell_a^I\approx0.
\]

It is useful to replace `K_a` by

\[
G_a=K_a-D_I\phi_a^I,
\]

which generates internal gauge transformations. The bulk brackets are

\[
\{\phi_a^I,\phi_b^J\}=\Omega^{IJ}_{ab},
\qquad
\{\phi_a^I,G_b\}=f^c{}_{ab}\phi_c^I,
\qquad
\{G_a,G_b\}=f^c{}_{ab}G_c.
\]

The identity

\[
\Omega^{IJ}_{ab}F^b_{KJ}=\delta^I_KK_a
\]

implies four null vectors on `K_a=0`. The associated first-class combinations

\[
H_K=F^a_{KJ}\phi_a^J
\]

generate improved spatial diffeomorphisms.

A canonical sector is both:

1. **generic:** `rank Omega=4N-4`; and
2. **regular:** the constraint Jacobian `dK_a/dF` has rank `N`.

For `N=15`, the constraint split is:

- 15 Gauss first-class constraints;
- 4 spatial-diffeomorphism first-class constraints;
- 56 second-class primary constraints.

The local configuration-space degree count is

\[
N_{\rm dof}
=\frac12\left[8N-2(N+4)-(4N-4)\right]
=N-2=13.
\]

The momenta conjugate to `A_0` and their gauge-fixing partners do not alter this count.

## 2. Deterministic regular-sector witness

The verification code uses the vector epsilon invariant

\[
g_{(AB)(CD)(EF)}=\epsilon_{ABCDEF}
\]

for `so(4,2)`. With random seed `0`, it solves the 15 algebraic equations `K_a=0` for 90 independent spatial-curvature components. The resulting point has:

- `||K|| = 3.95e-13`;
- constraint-Jacobian rank `15`;
- symplectic rank `56`;
- four linearly independent diffeomorphism null vectors;
- maximum null-vector residual `1.58e-12`.

This is a local phase-space witness. It establishes that the epsilon invariant admits the open regular/canonical stratum assumed by the degree count. It is not claimed to be a complete global solution with chosen boundary conditions.

## 3. Minimal BRST/BFV complex in a canonical sector

After eliminating the 56 second-class constraints with the Dirac bracket, choose the improved diffeomorphism generator

\[
\bar H_I=H_I+A_I^aG_a,
\]

which generates ordinary spatial Lie derivatives. The first-class algebra is the semidirect product of internal gauge transformations and spatial diffeomorphisms. A minimal BFV charge can be written schematically as

\[
\begin{aligned}
\Omega_{\rm BFV}=\int_{\Sigma_4}\Big[&
 c^aG_a+\xi^I\bar H_I
-\frac12f^a{}_{bc}c^bc^c\mathcal P_a
-(\mathcal L_\xi c)^a\mathcal P_a\\
&-\frac12[\xi,\xi]^I\mathcal P_I
\Big]
+\Omega_{\partial\Sigma}.
\end{aligned}
\]

Here `c^a` and `xi^I` are the gauge and spatial-diffeomorphism ghosts, and `P_a`, `P_I` their ghost momenta. `Omega_boundary` is absent for gauge parameters that vanish at the boundary, and is replaced by the transgression surface charge for admitted asymptotic symmetries.

An equivalent Lagrangian BRST complex is

\[
sA_M=-D_Mc-\mathcal L_\xi A_M,
\]

\[
sc=-\frac12[c,c]-\mathcal L_\xi c,
\qquad
s\xi^M=-\frac12[\xi,\xi]^M.
\]

It is nilpotent on the full field space. In degenerate sectors the diffeomorphism generators can become reducible and ghosts-for-ghosts may be required. The reduction tested here is already rejected in the generic canonical sector, so no conclusion depends on choosing a special reducible stratum.

## 4. Full zero modes on `M4 x S1`

Write the five-dimensional connection as

\[
A(x,y)=B(x,y)+\phi(x,y)\,dy.
\]

For `y`-independent fields,

\[
F=F_B-dy\wedge D_B\phi.
\]

Up to the declared transgression boundary term, fibre integration gives

\[
\int_{S^1}CS_5(B+\phi dy)
=3L_y\int_{M_4}\langle\phi F_B\wedge F_B\rangle.
\]

The full zero mode `phi` is adjoint-valued and has 15 components. The v1.0 Einstein sector is a much smaller restriction. Split `hat A=(A,4)`, with `A in {0,1,2,3,5}`:

\[
B_\mu=\frac12B_\mu^{AB}J_{AB}+C_\mu^AJ_{A4},
\]

\[
\phi=\frac12\varphi^{AB}J_{AB}+\Phi^AJ_{A4}.
\]

The MacDowell-Mansouri surface is

\[
C_\mu^A=0,
\qquad
\varphi^{AB}=0,
\qquad
\Phi^A=v\delta^A{}_5,
\]

with

\[
B^{ab}=\omega^{ab},
\qquad
B^{a5}=\ell_4^{-1}e^a.
\]

This is not a gauge fixing of the full zero-mode theory.

### Adjoint-orbit count

For the full adjoint zero mode `phi=vJ_54`, the adjoint map `ad(J_54)` has rank `8` and a seven-dimensional centralizer. Gauge transformations can move the holonomy along its eight-dimensional conjugacy orbit, but they cannot remove the seven conjugacy-invariant/centralizer directions.

Within the narrower v1.0 `SO(3,2)` vector ansatz, the orbit of `Phi^A=v delta^A_5` is

\[
SO(3,2)/SO(3,1),
\]

of dimension `4`. Four conditions can orient `Phi`; its norm is a gauge-invariant fifth datum.

## 5. Why the fixed norm is not a BRST gauge condition

For zero modes,

\[
s\phi=[\phi,c^{(0)}]
\]

(up to the chosen sign convention). Every invariant polynomial `P(phi)` is BRST closed:

\[
sP(\phi)=0.
\]

Thus the holonomy Casimirs and, in the vector ansatz, `Phi^2`, are physical sector labels. A gauge-fixing fermion can choose a representative on a conjugacy orbit; it cannot fix a conjugacy-invariant value without inserting an additional physical restriction.

The equations of the four-dimensional zero-mode action are

\[
\mathcal E_\phi\equiv\langle T_aF\wedge F\rangle=0,
\]

\[
\mathcal E_B\equiv D\phi\wedge F=0.
\]

Gauge invariance gives the Noether identity

\[
D\mathcal E_B+[\phi,\mathcal E_\phi]=0.
\]

Even if the connection equation holds, this implies only that `E_phi` lies in the centralizer of `phi`. The gauge-invariant radial projection

\[
\mathcal C_\phi
=\langle\phi F\wedge F\rangle
\]

survives. On the fixed MacDowell-Mansouri surface it becomes

\[
\mathcal C_\phi
=v\epsilon_{abcd}F^{ab}\wedge F^{cd}=0.
\]

For a torsionless Einstein solution with cosmological constant, `F^{ab}` equals the Weyl two-form. Generic Einstein solutions, including Schwarzschild-AdS with nonzero mass, violate this equation. The equation is not removed by choosing the orientation of `Phi`.

## 6. Dynamical preservation verdict

The circle component `A_y` is one of the four spatial canonical coordinates of the five-dimensional theory, not a Lagrange multiplier. Its Euler-Lagrange equation is part of the parent evolution. Imposing

\[
A_y=vJ_{54}
\]

and deleting its variation removes a canonical equation. The fixed surface is preserved only on the intersection with the additional condition `C_phi=0` and the omitted-component equations. That intersection is strictly smaller than the Einstein solution space.

Therefore the surface is:

- not a gauge slice of the unconstrained parent;
- not a dynamically invariant truncation containing generic GR;
- not a regular symplectic quotient;
- an externally selected holonomy/symmetry-breaking sector.

## 7. Boundary generators

For the relative transgression, bulk first-class constraints acquire the surface terms already contained in the transgression action. Gauge parameters for the two endpoint connections must agree at the common boundary. Under endpoint Dirichlet data or `Theta=0` matching, the surface variation vanishes. With nontrivial asymptotic symmetries, the boundary term becomes the physical surface charge rather than being silently discarded.

This boundary completion repairs differentiability of the parent generators. It does not remove the bulk holonomy equation or the 13-mode regular spectrum.
