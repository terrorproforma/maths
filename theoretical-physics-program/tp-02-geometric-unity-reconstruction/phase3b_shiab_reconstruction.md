# Phase 3B — Explicit Shiab typing and Clifford–Einstein selection

**Project:** TP-02 — Independent Reconstruction of Geometric Unity  
**Status:** **PHASE 3B COMPLETE AT THE SOURCE-RECONSTRUCTION LEVEL**  
**Primary equations:** draft eqs. (8.1), (8.7), (9.2), (9.3); official Oxford transcript and supplementary slides

## 1. Result

The newly elevated Oxford source and the 2021 draft together permit a stronger result than the earlier source-completeness statement:

\[
\boxed{
\text{The explicit substitute Shiab in draft eq. (9.3) is typeable}
}
\]

and its intended product pattern can be reconstructed exactly on the geometric Riemann-curvature sector.

However,

\[
\boxed{
\text{the official corpus still does not determine one full}
\ U(64,64)\text{-adjoint Hessian or principal symbol}.
}
\]

Both statements matter. The first prevents us from dismissing the displayed operator as pure rhetoric. The second prevents us from mistaking one sympathetic completion for the source theory.

## 2. Typed operator

Let:

- \(Y\) be oriented, fourteen-dimensional and equipped locally with the source's signature-\((7,7)\) metric;
- \(P_H\to Y\) be the principal \(U(64,64)\) bundle;
- \(\varepsilon\in\mathcal H=\Gamma^\infty(\operatorname{Ad}P_H)\);
- \(\xi\in\Omega^2(Y,\operatorname{ad}P_H)\);
- \(\Phi_1\in\Omega^1(Y,\operatorname{ad}P_H)\) and
  \(\Phi_2\in\Omega^2(Y,\operatorname{ad}P_H)\) be invariant pure-trace tensors;
- \(C_i=\operatorname{Ad}_{\varepsilon^{-1}}\Phi_i\).

The displayed structure is

\[
\operatorname{Sh}_{\varepsilon}\xi
=
\mathcal B_1(C_1,*\xi)
-
\frac12*
\mathcal B_2
\left(
C_1,
*
\mathcal B_3(C_2,*\xi)
\right),
\]

where each \(\mathcal B_j\) is an equivariant matrix/form product of the kind described in section 8.

The form degrees close exactly:

\[
*\xi\in\Omega^{12},
\qquad
C_1\wedge *\xi\in\Omega^{13},
\]

and

\[
C_2\wedge *\xi\in\Omega^{14}
\overset{*}{\longrightarrow}
\Omega^0
\overset{C_1\wedge}{\longrightarrow}
\Omega^1
\overset{*}{\longrightarrow}
\Omega^{13}.
\]

Therefore,

\[
\boxed{
\operatorname{Sh}_{\varepsilon}:
\Omega^2(Y,\operatorname{ad}P_H)
\longrightarrow
\Omega^{13}(Y,\operatorname{ad}P_H)
}
\]

is a zeroth-order linear map in \(\xi\), once its invariant tensors, product operations and metric are frozen.

For signature \((7,7)\),

\[
*^2\big|_{\Omega^p}
=
(-1)^{p(14-p)+7},
\]

so the relevant signs are

\[
*^2_{\Omega^2}=-1,
\qquad
*^2_{\Omega^{14}}=-1,
\qquad
*^2_{\Omega^1}=+1.
\]

These signs must be retained in every adjoint and Hessian calculation.

## 3. Clifford–Einstein selection lemma

The source says the first part is Ricci-like, the second scalar-like, and the Weyl component is annihilated. Those requirements select a definite algebraic pattern on the geometric curvature subspace.

Let \((V,g)\) have dimension \(n\ge3\), with Clifford generators

\[
\{\gamma_a,\gamma_b\}=2g_{ab},
\qquad
\gamma_{ab}=\frac12[\gamma_a,\gamma_b].
\]

For an algebraic Riemann tensor, define spin curvature

\[
F_{cd}
=
\frac14R_{cdab}\gamma^{ab}.
\]

Then:

\[
\boxed{
[\gamma^c,F_{cd}]
=
R_{db}\gamma^b
}
\]

and

\[
\boxed{
\{\gamma^{cd},F_{cd}\}
=
-R\,\mathbf1
}
\]

in the convention used by the verifier.

Consequently,

\[
\boxed{
\mathcal E_d
=
[\gamma^c,F_{cd}]
+
\frac12
\{\gamma^{cd},F_{cd}\}\gamma_d
=
\left(
R_{db}-\frac12Rg_{db}
\right)\gamma^b.
}
\]

### Proof sketch

The first identity follows from

\[
[\gamma^c,\gamma^{ab}]
=
2(g^{ca}\gamma^b-g^{cb}\gamma^a)
\]

and the pair antisymmetries of \(R_{cdab}\).

The scalar part of

\[
\{\gamma^{cd},\gamma^{ab}\}
\]

contains the metric double contraction and a four-gamma term. The four-gamma term contracts with \(R_{[cdab]}\) and vanishes by the algebraic Bianchi identity. The metric contraction gives \(-R\mathbf1\) in the declared convention.

A pure Weyl tensor has vanishing Ricci tensor and scalar, so both contractions vanish.

Thus the intended geometric branch requires:

- a **commutator** in the vector–bivector Ricci contraction;
- an **anticommutator/Jordan** operation in the bivector scalar contraction;
- ordinary scalar multiplication in the final one-form.

A uniform use of only commutators or only anticommutators does not reproduce the stated Einstein decomposition.

## 4. Rank on the fourteen-dimensional Riemann sector

For \(n=14\),

\[
\dim\mathcal R
=
\frac{n^2(n^2-1)}{12}
=
3185,
\]

\[
\dim\mathcal W
=
\frac{(n+2)(n+1)n(n-3)}{12}
=
3080,
\]

and

\[
\dim\operatorname{Sym}^2(V^*)
=
\frac{n(n+1)}2
=
105.
\]

The Einstein map is invertible on the Ricci-plus-scalar quotient for \(n\neq2\). Hence, on the algebraic Riemann subspace,

\[
\boxed{
\operatorname{rank}\operatorname{Sh}_{\rm Einstein}=105,
\qquad
\dim\ker\operatorname{Sh}_{\rm Einstein}=3080.
}
\]

The kernel is precisely the Weyl sector.

This is an algebraic benchmark. It is not yet the physical kinetic rank of the complete GU field theory.

## 5. Fréchet derivatives fixed by the displayed formula

Write a right-trivialised variation as

\[
\delta\varepsilon=\varepsilon X.
\]

Then

\[
\delta C_i=[C_i,X]
+
\operatorname{Ad}_{\varepsilon^{-1}}(\delta\Phi_i).
\]

With the metric and \(\Phi_i\) temporarily frozen,

\[
D_{\varepsilon}\operatorname{Sh}[\varepsilon X](\xi)
=
\mathcal B_1([C_1,X],*\xi)
\]

\[
-\frac12*
\left[
\mathcal B_2
\left(
[C_1,X],
*
\mathcal B_3(C_2,*\xi)
\right)
+
\mathcal B_2
\left(
C_1,
*
\mathcal B_3([C_2,X],*\xi)
\right)
\right].
\]

The derivative in the curvature slot is simply

\[
D_{\xi}\operatorname{Sh}[\delta\xi]
=
\operatorname{Sh}(\delta\xi).
\]

For a metric variation \(h=\delta g\),

\[
D_g(*)(h)\alpha
=
*
\left[
\frac12\operatorname{tr}_g(h)\,\alpha
-
h^\sharp\bullet\alpha
\right],
\]

where \(h^\sharp\bullet\alpha\) acts on every form index. This formula must be inserted at all three Hodge stars, together with the still-unspecified terms

\[
D_g\Phi_1[h],
\qquad
D_g\Phi_2[h].
\]

The observation-induced connection has the universal Levi-Civita variation

\[
\delta\Gamma^\rho{}_{\mu\nu}
=
\frac12g^{\rho\sigma}
\left(
\nabla_\mu h_{\nu\sigma}
+
\nabla_\nu h_{\mu\sigma}
-
\nabla_\sigma h_{\mu\nu}
\right),
\]

followed by the spin lift. But the source still must specify the complete map

\[
\delta\gimel
\longmapsto
\delta g_Y
\longmapsto
\delta A_0.
\]

## 6. What the official sources still do not fix

The source itself says the preferred Bianchi-selected Shiab cannot presently be located and presents eq. (9.3) as a starting substitute. Even for that substitute, the corpus does not uniquely supply:

1. concrete normalised representatives for \(\Phi_1,\Phi_2\) over the full bundle;
2. their variation with the observation field;
3. the extension of the mixed commutator/Jordan pattern from the geometric Riemann sector to arbitrary \(u(64,64)\)-valued curvature;
4. the global metric, orientation and reality domains needed for the Hodge adjoint;
5. boundary conditions and formal-adjoint domains;
6. a background solving the repaired equations;
7. the complete fermionic and deformation-complex completion.

Different choices agree on the Einstein subspace and differ on the extra adjoint directions. Those directions are precisely where additional modes, ghosts, constraints or claimed matter sectors may live.

## 7. Terminal Phase 3B verdict

\[
\boxed{
\begin{array}{c}
\textbf{Explicit substitute typed: YES.}\\[1mm]
\textbf{Einstein contraction on geometric curvature: VERIFIED.}\\[1mm]
\textbf{Unique source-faithful full Hessian: NO.}\\[1mm]
\textbf{Unique physical spectrum from the official corpus: NO.}
\end{array}
}
\]

This is a source-incompleteness result, not a theorem that every completion of the geometric idea is impossible.

## 8. Next branch

The next independent construction is labelled

\[
\mathsf{R}_{+}\text{-EIN}
\]

and must declare, rather than smuggle in:

- repaired stabiliser-compatible torsion \(T_+\);
- the Clifford–Einstein mixed commutator/Jordan pattern;
- explicit \(\Phi_1,\Phi_2\) representatives and normalisations;
- compact-support or boundary conditions;
- one local background;
- a full quadratic symbol and gauge-complex calculation.

Results from that branch are project constructions. They will not be retroactively attributed to the official Geometric Unity source.