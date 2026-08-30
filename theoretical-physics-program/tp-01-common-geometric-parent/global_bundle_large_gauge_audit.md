# Global bundle, holonomy and large-gauge audit

## 1. What the relative connection assumes

The difference

\[
\Theta=A-\bar A
\]

is globally an `ad(P)`-valued one-form only when `A` and `Abar` are connections on the same principal bundle `P -> M5`, or when an explicit bundle isomorphism has been chosen. The affine interpolation

\[
A_t=\bar A+t\Theta
\]

therefore lives within a fixed bundle component. If the endpoint bundles have different characteristic classes, the cylinder interpolation used by the parent does not exist without additional cobordism/bundle data.

The exact genealogy is consequently global only inside the declared bundle sector. This is enough for the construction, but it is not a sum over all topological sectors.

## 2. Circle reduction and the true zero-mode observable

A global decomposition

\[
A=B+\phi\,dy
\]

requires a circle action, an equivariant connection and a compatible local trivialization. On a nontrivial bundle over `M4 x S1`, the gauge-invariant object is not a chosen Lie-algebra logarithm `phi`; it is the conjugacy class of the Wilson line

\[
W(x)=\mathcal P\exp\left(\oint_{S^1}A_y(x,y)\,dy\right).
\]

For a periodic gauge transformation,

\[
W(x)\mapsto g(x,0)^{-1}W(x)g(x,0).
\]

Thus the conjugacy class, its characteristic polynomial and representation traces are gauge invariant. A global logarithm `phi=L_y^{-1}\log W` need not exist uniquely.

## 3. The v1.0 fixed holonomy is physical data

For the Lorentzian generator `H=J_54` in the six-dimensional vector representation,

\[
W=\exp(L_yvH)
\]

has eigenvalues `e^{+L_yv}`, `e^{-L_yv}` and four unit eigenvalues. Therefore

\[
\boxed{\operatorname{tr}_{\mathbf 6}W=4+2\cosh(L_yv).}
\]

This trace is a dimensionless, gauge-invariant conjugacy-class observable. Changing `v` changes the sector. The generator is noncompact, so the parameter is not periodically identified by this one-parameter subgroup. In the compact Euclidean continuation the corresponding formula becomes `4+2 cos(L_yv)` and periodic identifications can arise.

Fixing `Phi^A=v delta^A_5` therefore chooses:

1. a particular holonomy conjugacy class;
2. a reduction of the `SO(3,2)` structure group to the Lorentz stabilizer;
3. a nowhere-vanishing fixed-norm section of the associated vector bundle.

Existence of that global section is additional bundle data and is not guaranteed for an arbitrary parent bundle.

## 4. Large gauge transformations and level normalization

The relative transgression is strictly invariant under simultaneous finite gauge transformations of both connections. Classical gauge invariance of the relative action therefore does not rely on cancelling a Chern-Simons winding shift.

Two different questions remain:

### Standalone Chern-Simons daughter

If `Abar` is frozen and the theory is treated as a standalone `CS5` action, a large gauge transformation or a change of six-dimensional extension can shift the action by the integral of the characteristic six-form. The exponentiated action is well defined only after choosing an integral lift of the invariant polynomial and a compatible level.

For a compact oriented rank-six vector bundle, the Euler normalization is

\[
e(E)=\frac{1}{2^3 3!(2\pi)^3}
\epsilon_{ABCDEF}F^{AB}F^{CD}F^{EF}.
\]

With this normalization, its integral on a closed six-manifold is an integer. If the action is `2 pi k` times that class, extension independence follows for integer `k`.

### Lorentzian `Spin(4,2)` parent

The minimal allowed level depends on:

- the global form of the gauge group and its centre quotient;
- which principal bundles are admitted;
- the integral lift represented by the chosen `P3` normalization;
- spin versus vector-associated bundles;
- and the boundary conditions.

The present epsilon polynomial has a natural Euler-class candidate through the vector representation, but the package does not prove the minimal integral lattice for every Lorentzian `Spin(4,2)` bundle. It therefore records a conditional quantization rule rather than inventing a universal integer.

This does not affect the negative dynamical result. Even a quantized level does not remove the Wilson-line equation, the 13-mode regular spectrum or the first-KK tower.

## 5. Boundary topology

The transgression boundary form makes the variational principle and surface generators differentiable for the declared endpoint data. Nontrivial boundary topology may support edge modes and nonzero charges. Those modes are additional physical content; they cannot be counted as a mechanism that deletes unwanted bulk modes while leaving pure four-dimensional GR.

## 6. Global verdict

The exact common genealogy survives globally only after the following are declared:

- one bundle/cobordism sector containing both endpoints;
- a circle-equivariant reduction structure;
- a chosen holonomy conjugacy class;
- a structure-group reduction admitting the compensator section;
- an integral normalization if a standalone quantum Chern-Simons daughter is claimed;
- boundary data and admitted asymptotic symmetries.

These declarations make the construction well defined. They also make clear that the Einstein daughter is selected by extra global data rather than derived as the unrestricted low-energy phase of the parent.
