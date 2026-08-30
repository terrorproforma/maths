# Strengthened restricted no-go theorem - TP-01 v1.1

## Theorem

Consider a five-dimensional Chern-Simons or fixed-reference transgression theory on `M4 x S1` with gauge group locally `Spin(4,2)`, defined by a nondegenerate rank-three invariant polynomial. Assume:

1. the theory is local, polynomial and contains finitely many five-dimensional fields;
2. the operational bulk dynamics is pure connection Chern-Simons/transgression dynamics;
3. the compactification is regular and retains every zero mode of the connection;
4. the reduced theory is obtained by an invertible field map or a genuine gauge/symplectic quotient;
5. the parent gauge/BRST symmetry is not explicitly broken by external compensator data;
6. the relevant parent background lies in a regular constant-rank canonical sector;
7. omitted fields and nonzero Kaluza-Klein modes are removed only by a proved consistent truncation or controlled decoupling limit;
8. the endpoint connections live in a declared common bundle/cobordism sector and no unmentioned global structure-group reduction is imposed.

Then the theory cannot reduce to pure four-dimensional Einstein-Cartan/Einstein-Hilbert gravity with cosmological constant and only two local graviton polarizations.

## Proof

### 1. The circle component survives

The full zero mode of the connection contains an adjoint scalar `phi=A_y`. Fibre integration gives, up to the declared boundary term,

\[
S_0=3kL_y\int_{M_4}\langle\phi F\wedge F\rangle.
\]

Retaining all zero modes therefore retains `phi` and its Euler-Lagrange equation.

### 2. Fixing the compensator is not pure gauge

The adjoint element `vJ_54` has an eight-dimensional gauge orbit and a seven-dimensional centralizer in `so(4,2)`. In the narrower vector ansatz, `Phi^A` has a four-dimensional `SO(3,2)` orbit but one gauge-invariant norm. The conjugacy class of the Wilson line is physical; for the vector representation,

\[
\operatorname{tr}W=4+2\cosh(L_yv).
\]

Thus fixing the complete value of `phi` or `Phi` imposes gauge-invariant data and cannot be an ordinary BRST gauge choice.

### 3. A gauge-invariant equation remains

The radial projection of the scalar equation,

\[
\mathcal C_\phi=\langle\phi F\wedge F\rangle=0,
\]

is gauge invariant. In the MacDowell-Mansouri sector it becomes

\[
\epsilon_{abcd}F^{ab}\wedge F^{cd}=0.
\]

Generic Einstein solutions such as Schwarzschild-AdS violate it. Deleting this equation is a change of theory.

### 4. The regular degree counts mismatch

A regular five-dimensional `Spin(4,2)` Chern-Simons sector has

\[
N_{\rm dof}=15-2=13
\]

local configuration degrees of freedom. Four-dimensional GR has two. A regular invertible reduction or symplectic quotient cannot delete eleven physical modes without new constraints or a decoupling mechanism.

### 5. The maximally symmetric escape is singular

At the Chern-Simons AdS root, `F=0`, the symplectic matrix and ordinary quadratic graviton operator vanish. This is a degenerate and irregular stratum, not a healthy two-helicity phase.

### 6. The first KK level cannot repair closure

The non-Abelian Fourier modes form a loop algebra with mode addition. The set `{0,+/-1}` is not closed because brackets generate `+/-2`; any exact finite truncation containing a nonzero mode generates an infinite tower. At quadratic order on a regular `y`-independent background, the first conjugate pair carries 26 additional real degrees of freedom. No positive decoupling gap is supplied by the pure Chern-Simons action.

### 7. The symplectic pullback is not a reduction

The fixed-holonomy surface has the correct pulled-back Einstein-Cartan plus Euler covariant symplectic potential. However, it is not invariant under the parent equations and is not obtained by quotienting a first-class gauge orbit. Correct coefficients on a non-invariant surface do not establish dynamical equivalence.

### 8. Global data are additional assumptions

A global compensator requires a chosen holonomy conjugacy class and a reduction of the parent bundle to the Lorentz stabilizer. These are extra data excluded by assumptions 5 and 8.

The assumptions therefore contradict the requirements for a pure Einstein daughter. At least one must be abandoned. QED.

## Known escape routes

- **Stelle-West/constrained compensator:** adds a norm constraint and changes the canonical system.
- **Plebanski/BF:** adds two-form fields and simplicity constraints.
- **Boundary gWZW sector:** retains physical edge/group fields.
- **Holographic/induced gravity:** is effective and nonlocal from the daughter viewpoint.
- **Singular AdS stratum:** abandons regular constant-rank dynamics.
- **Orbifold or projected KK theory:** changes the loop algebra and needs a new consistency proof.
- **Dynamical phase transition:** adds a potential/sector-selection mechanism and must show decoupling.

These are legitimate model-building directions. They are not counterexamples to the theorem because each violates an explicit assumption.
