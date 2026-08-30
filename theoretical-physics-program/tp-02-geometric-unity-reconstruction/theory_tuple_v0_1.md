# Geometric Unity theory tuple — source reconstruction v0.1

This file translates the official 2021 draft into a typed research object. It is deliberately incomplete where the source is incomplete. Mechanical aliases are listed in `symbol_typing_issues.md`.

## 1. Base data

The draft starts from an oriented smooth four-manifold with a unique spin structure:

\[
X^4.
\]

No metric, symplectic form, complex structure or volume form is initially imposed. The source treats the Lorentzian signature choice as additional/anthropic data rather than something derived at this stage.

**Typing status:** clear locally; global existence of a unique spin structure is an initial assumption, not a consequence.

## 2. Observerse

The source defines an `Observerse` as a triple

\[
(X^n,Y^d,\{\iota\}),
\]

with local maps

\[
\iota:U_x^n\rightarrow Y^d
\]

that act as local Riemannian or semi-Riemannian embeddings and induce

\[
g_X=\iota^*g_Y.
\]

The three source cases are trivial, Einsteinian and ambient. TP-02 studies the Einsteinian case:

\[
Y=\operatorname{Met}(X),
\]

the bundle of pointwise nondegenerate metric tensors. For `dim X=4`,

\[
\dim\operatorname{Sym}^2(T_x^*X)=10,
\qquad
\dim Y=4+10=14.
\]

The observation field/section is denoted by the source's Hebrew `gimel` symbol. It is the one field described as truly native to `X`; most other fields are native to `Y` and become `invasive` on `X` by pullback.

**Unresolved typing:** whether the allowed section space includes all signatures globally, how degeneracy boundaries are excluded, and the precise global topology of `Met(X)` used in the dynamics.

## 3. Horizontal, vertical and Chimeric bundles

Viewing `Y` as a fibre bundle over `X` gives the vertical bundle

\[
V=\ker \pi_*\subset TY.
\]

The source defines a horizontal-dual bundle

\[
H^*=\pi^*T^*X\hookrightarrow T^*Y,
\]

and its dual `H`. The `Chimeric Bundle` is

\[
C=V\oplus H^*,
\qquad
C^*=V^*\oplus H.
\]

The source equips `V` with a Frobenius-type metric derived from the point of `Y`, and `H^*` with the pulled-back base metric. For the four-dimensional Lorentzian branch the resulting rank-14 chimeric metric is stated to have signature `(7,7)`.

A section/observation and its induced Levi-Civita connection provide an isomorphism between the chimeric and tangent/cotangent structures in the observed sector.

**Unresolved typing:** a global proof of the stated signature on every chosen component; exact dependence of the horizontal splitting on the distinguished connection; behaviour across signature-changing or degenerate loci.

## 4. Spinors and the main principal bundle

The source constructs spinors for the metric chimeric bundle. In the Lorentzian four-dimensional branch:

\[
\operatorname{Spin}(7,7)
\]

has complex Dirac-spinor dimension `128` and chiral dimension `64`. The source embeds the spin representation into

\[
U(64,64),
\]

and defines a principal bundle over `Y` by extending the chimeric spin-frame bundle through that representation. We record the intended objects as

\[
P_H\rightarrow Y,
\qquad
H_{\rm finite}=U(64,64),
\]

with associated bundles

\[
\operatorname{Ad}(P_H),
\qquad
\operatorname{ad}(P_H),
\qquad
\mathcal S=P_H\times_\rho \mathbb C^{64,64}.
\]

**Unresolved typing:** the draft overloads `H` for the finite-dimensional structure group and the infinite-dimensional gauge group; the exact real/complex and Majorana/Weyl conditions in Lorentzian signature require independent reconstruction.

## 5. Infinite-dimensional field spaces and symmetries

Let

\[
\mathcal A=\operatorname{Conn}(P_H)
\]

be the affine space of connections, modeled on

\[
N=\Omega^1(Y,\operatorname{ad}P_H).
\]

The gauge group is reconstructed as

\[
\mathcal H=\Gamma^\infty(\operatorname{Ad}P_H).
\]

The source defines the inhomogeneous gauge group

\[
\mathcal G=\mathcal H\ltimes N,
\]

with elements

\[
g=(\varepsilon,a),
\]

where `varepsilon` is gauge-group-valued and `a` is an adjoint-valued one-form. The source gives explicit left and right actions on `A` and a tilted embedding

\[
\tau_{A_0}:\mathcal H\hookrightarrow\mathcal G
\]

associated with a distinguished connection `A_0`.

**Typing status:** the semidirect-product law and affine actions are explicit enough to re-derive. Their smooth infinite-dimensional Lie-group category and functional-analytic domains remain undeclared.

## 6. Distinguished connection and observation dependence

An observation/metric section on `X` induces a Levi-Civita connection and then a spin connection on the relevant bundle over `Y`. The source calls this the distinguished connection

\[
A_0\simeq \nabla_0.
\]

It is used to identify the affine connection space with `N`, define the tilted gauge subgroup and compare two connections.

**Conceptual fork:** `A_0` is not a fixed universal background independent of the observation field. The reconstruction must keep track of its functional dependence on the metric section. Treating it as fixed while varying the observation field would change the theory.

## 7. Fields

The source's unified field is reconstructed as

\[
\omega=(\beta,\chi),
\]

with

\[
\beta=(\varepsilon,a)\in\mathcal G,
\]

and fermionic content

\[
\chi=(\nu,\zeta),
\qquad
\nu\in\Omega^0(Y,\mathcal S),
\qquad
\zeta\in\Omega^1(Y,\mathcal S).
\]

The draft sometimes treats barred variables independently at the classical level in anticipation of a fermionic functional integral.

The observation section on `X` is separate and is the only primary field native to `X` in the stated architecture.

**Unresolved typing:** Grassmann parity, reality conditions, functional measure, ghost sector, mass dimensions, engineering dimensions on `Y`, and whether `zeta` is a genuine spin-3/2 field after constraints or merely a spinor-valued one-form.

## 8. Augmented torsion

The source maps an inhomogeneous gauge-group element to a difference of two connections. In stable aliases,

\[
T_\omega
=
 a-\varepsilon^{-1}d_{A_0}\varepsilon
\in\Omega^1(Y,\operatorname{ad}P_H).
\]

It is equivariant under the tilted gauge subgroup. This formula is sufficiently explicit for an independent covariance check.

**Unresolved typing:** how the source's `B_omega` and `A_omega` bi-connections are selected in every action formula, and which connection differentiates each field when the observation section varies.

## 9. Shiab family

The `Shiab` is a source-defined family of metric-dependent contraction/projection operators intended to generalize Einstein's curvature contraction while restoring gauge covariance through dependence on the inhomogeneous field. We denote a selected member by

\[
\operatorname{Sh}_\omega.
\]

The source gives an explicit Einstein-like contraction on adjoint-valued two-forms using the observation-induced soldering data and Hodge star, but also discusses a family of choices and pure-trace modifications.

**Unresolved typing:** the project must freeze one operator branch, specify domain/codomain and all index contractions, and prove covariance before a principal symbol is unique.

## 10. Bosonic dynamics

The first-order bosonic action is source-equation `9.4`, schematically

\[
I_{B,1}(\omega;g_X)
=
\left\langle
T_\omega,
*\left[
\operatorname{Sh}_\omega\left(
F_{B_\omega}
+\frac12 d_{B_\omega}T_\omega
+\frac13[T_\omega,T_\omega]
\right)
+\frac{\kappa_1}{2}T_\omega
\right]
\right\rangle_Y.
\]

The bracket denotes the source's metric pairing/integration over `Y` with the observation-induced metric. The source packages the first-order equation into a field denoted `Upsilon_omega`.

The second-order bosonic action is

\[
I_{B,2}=\|\Upsilon_\omega^B\|^2,
\]

with a compact source equation of motion written as

\[
D_\omega^*\Upsilon_\omega=0.
\]

**Unresolved typing:** exact boundary conditions, integrations by parts, gauge-fixing, functional dependence of `Sh_omega`, the independent variables in the first variation, and the relation between the first- and second-order solution spaces.

## 11. Fermionic dynamics

The source proposes a matrix first-order operator coupling spinor zero-forms and spinor one-forms, with `Shiab`, covariant derivatives and blocks of the inhomogeneous connection. It then seeks a Dirac-square relation between first-order Einstein/Dirac-like equations and second-order Yang-Mills/Higgs-like equations.

**Current status:** not yet reconstructed as a unique closed operator. The primary draft does not provide a stabilized quantum action, BRST gauge fixing or measure.

## 12. Deformation complex

The source proposes operators

\[
\delta_\omega^1:
\Omega^0(\operatorname{ad})
\rightarrow
\Omega^1(\operatorname{ad})\oplus\Omega^0(\operatorname{ad}),
\]

\[
\delta_\omega^2:
\Omega^1(\operatorname{ad})\oplus\Omega^0(\operatorname{ad})
\rightarrow
\Omega^{d-1}(\operatorname{ad}),
\]

with the intended relation

\[
\delta_\omega^2\circ\delta_\omega^1=0
\]

on solutions. The displayed mixed boson/fermion diagram is explicitly marked by the source as potentially inconsistent until stabilized.

**Current status:** a proposal, not an accepted complex. TP-02 must calculate the composition after fixing the operator branch and background.

## 13. Observed field content

Under observation, topological spinors on `Y` are pulled back to `X` and decomposed into spacetime spinors tensored with normal/internal spinors. For the stated `Spin(1,3) x Spin(6,4)` branch, the draft claims:

- a `64`-dimensional spin-1/2 sector;
- a `192`-dimensional sector involving four-dimensional vector-spinor multiplicity;
- a `576`-dimensional sector involving a `144`-dimensional gamma-traceless internal vector-spinor;
- total chiral gamma-traceless vector-spinor dimension `832`.

The arithmetic identity

\[
64+192+576=832
\]

is verified in code. The representation branching, gauge charges, kinetic constraints and decoupling interpretation are not yet proved.

The source further proposes:

- two ordinary `true` generations plus one effective `imposter` generation;
- emergent rather than fundamental chirality;
- additional spin-3/2 matter;
- dark matter and dark gauge sectors.

These remain source claims pending explicit low-energy decomposition, anomaly cancellation, dynamics and mass generation.

## 14. Observables and state data

The source emphasizes observation by pullback, but a complete gauge-invariant observable algebra is not yet specified. Neither a quantum state space nor a cosmological initial-state measure is supplied in the draft.

**Tuple status:** incomplete.

## 15. Current reconstructed tuple

\[
\boxed{
\mathfrak G_{0.1}=
\left(
X^4,
Y^{14}=\operatorname{Met}(X),
C^{7,7},
P_H,
\mathcal G=\mathcal H\ltimes\Omega^1(\operatorname{ad}P_H),
\omega=(\varepsilon,a;\nu,\zeta),
g_X,
I_{B,1},I_{B,2},I_F?,
\mathcal O?,
\mathcal I?,\mathcal B?
\right).
}
\]

Question marks are not rhetorical. They mark indispensable structures that are not yet uniquely reconstructed from the primary corpus.
