# Phase 3A — First-order bosonic action: covariance and variational audit

**Project:** TP-02 — Independent Reconstruction of Geometric Unity  
**Status:** **DECISIVE KINEMATIC RESULT / FULL SHIAB VARIATION STILL OPEN**  
**Convention branches:** literal printed branch `PRINTED` and repaired branch `R_PLUS`

## 1. Purpose

The next research target is the first variation and principal symbol of the source's first-order bosonic action. Before attempting that calculation, one must establish that the proposed integrand can transform as a gauge scalar under the source's tilted subgroup.

The audit uses only the minimum structure asserted by the construction:

1. an invariant bilinear pairing \(\langle\cdot,\cdot\rangle\);
2. an augmented torsion \(T\);
3. a Shiab/curvature output \(Q\) claimed to transform covariantly;
4. the first-order action skeleton
   \[
   I[T,Q]=\int_Y\mu\,\langle T,Q\rangle.
   \]

No detailed choice of Shiab is needed for this covariance test.

## 2. Exact finite transformation

Let

\[
\tau_-(h)=\left(h,-h^{-1}d_{A_0}h\right)
\]

be the printed tilted stabilizer. Phase 2 established

\[
T_-\bigl(g\tau_-(h)\bigr)
=
h^{-1}T_-(g)h-2h^{-1}d_{A_0}h,
\]

whereas the repaired branch obeys

\[
T_+\bigl(g\tau_-(h)\bigr)=h^{-1}T_+(g)h.
\]

Assume the second factor transforms as the source's covariance language requires:

\[
Q\longmapsto Q^h=h^{-1}Qh.
\]

Ad-invariance of the pairing gives

\[
\langle h^{-1}T_+h,h^{-1}Qh\rangle=\langle T_+,Q\rangle.
\]

Therefore the repaired action is kinematically compatible with tilted gauge invariance:

\[
\boxed{I_+[g\tau_-(h),Q^h]=I_+[g,Q].}
\]

For the literal printed branch,

\[
\boxed{
I_-[g\tau_-(h),Q^h]-I_-[g,Q]
=
-2\int_Y\mu\,
\left\langle h^{-1}d_{A_0}h,\,h^{-1}Qh\right\rangle.
}
\]

This is nonzero for generic \(h\) and \(Q\). Thus the printed action skeleton is not invariant under the printed tilted subgroup if the Shiab/curvature factor transforms covariantly.

## 3. Infinitesimal Noether defect

Set

\[
h=e^{t\xi}.
\]

To first order,

\[
\delta_\xi T_-=[T_-,\xi]-2d_{A_0}\xi,
\qquad
\delta_\xi Q=[Q,\xi].
\]

The commutator terms cancel under an invariant pairing, leaving

\[
\boxed{
\delta_\xi I_-
=
-2\int_Y\mu\,\langle d_{A_0}\xi,Q\rangle.
}
\]

After integration by parts,

\[
\delta_\xi I_-
=
2\int_Y\mu\,\langle\xi,d_{A_0}^{\dagger}Q\rangle
-2\int_{\partial Y}\mathcal B(\xi,Q).
\]

This is not an off-shell Noether identity unless the theory adds one of the following:

1. a non-covariant affine transformation of \(Q\) tuned to cancel the defect;
2. a restriction to \(d_{A_0}h=0\), reducing the claimed gauge group;
3. an off-shell identity \(d_{A_0}^{\dagger}Q\equiv0\) plus compatible boundary conditions;
4. the plus-sign repair \(T_+\).

An equation of motion cannot be used to manufacture an off-shell gauge symmetry without changing the constraint structure.

## 4. Exact matrix witness at the action level

Use the Phase 2 exact matrices and the trace pairing

\[
\langle X,Y\rangle=\operatorname{tr}(XY).
\]

For

\[
Q=\begin{pmatrix}1&2\\3&4\end{pmatrix},
\]

the printed branch gives the exact finite change

\[
\boxed{I_-^{\,h}-I_-=14.}
\]

The repaired branch gives

\[
\boxed{I_+^{\,h}-I_+=0.}
\]

The executable verifier performs this test over the rational numbers.

## 5. Universal first-variation formula

Define

\[
K=\varepsilon^{-1}d_{A_0}\varepsilon,
\qquad
T_s=a+sK,
\qquad
s\in\{-1,+1\}.
\]

Let

\[
\eta=\varepsilon^{-1}\delta\varepsilon.
\]

Because

\[
A_0^\varepsilon=A_0+K,
\]

the exact variation is

\[
\boxed{
\delta K
=
d_{A_0+K}\eta
+
\left(\operatorname{Ad}_{\varepsilon^{-1}}-1\right)\delta A_0.
}
\]

Hence

\[
\boxed{
\delta T_s
=
\delta a
+s\,d_{A_0+K}\eta
+s\left(\operatorname{Ad}_{\varepsilon^{-1}}-1\right)\delta A_0.
}
\]

The final term is indispensable because the distinguished connection is not an independent immutable background:

\[
A_0=A_0[\gimel].
\]

For an action

\[
I_s[\omega,\gimel]
=
\int_Y\mu_{\gimel}
\left\langle T_s(\omega,\gimel),Q(\omega,\gimel)\right\rangle,
\]

the complete abstract first variation is

\[
\begin{aligned}
\delta I_s
={}&
\int_Y\mu_{\gimel}
\Bigl[
\langle\delta T_s,Q\rangle
+
\langle T_s,DQ[\delta\omega,\delta\gimel]\rangle
\Bigr]\\
&+
\int_Y\delta\mu_{\gimel}\,\langle T_s,Q\rangle
+
\int_Y\mu_{\gimel}\,\delta\langle T_s,Q\rangle_{\gimel}
+
\text{boundary terms}.
\end{aligned}
\]

If

\[
Q=\operatorname{Sh}_{\omega,\gimel}(F_\omega),
\]

then

\[
DQ[\delta\omega,\delta\gimel]
=
(D\operatorname{Sh})[\delta\omega,\delta\gimel](F_\omega)
+
\operatorname{Sh}_{\omega,\gimel}(d_\omega\delta\omega).
\]

This formula identifies every derivative required for a source-complete Euler–Lagrange calculation.

## 6. What is fixed and what remains underdetermined

The following are now fixed independently of the detailed Shiab choice:

- the printed branch has an off-shell tilted-gauge covariance defect;
- the repaired branch removes that defect;
- the exact variation of the augmented torsion contains the observation-induced connection variation;
- treating \(A_0\) as fixed during an observation-field variation is incorrect except on a declared restricted slice.

The following remain necessary before a unique principal symbol can be calculated:

1. the exact domain and codomain of the selected Shiab operator;
2. its complete dependence on \(\omega\) and \(\gimel\);
3. the Fréchet derivative \(D\operatorname{Sh}\);
4. the map \(D A_0[\delta\gimel]\);
5. the invariant pairing and its metric dependence;
6. the measure on \(Y\);
7. the independent variables and reality conditions;
8. boundary conditions and the adjoint domain.

Without these data, different source-compatible completions can possess different Hessians and characteristic polynomials. A unique full principal symbol cannot be inferred from the action's typography alone.

## 7. Acceptance result

### Literal printed branch

`ALG-02 = 0` **for the claimed tilted-gauge-invariant first-order action**, unless an additional compensating transformation or off-shell identity is supplied.

### Repaired branch

`ALG-02 = 1` **partial**. Kinematic covariance passes, but closure of the full deformation/BRST complex and propagation of constraints remain unproved.

### Overall TP-02 status

The project does not collapse the branches into one score. The literal printed branch is rejected in the stated invariant-action form. The repaired branch remains alive and is the correct object for the next dynamic calculation.

## 8. Next decisive calculation

Type the explicit substitute Shiab of draft eq. (9.3) as a map between declared bundles. Then compute

\[
D\operatorname{Sh},
\qquad
D A_0,
\qquad
\delta I_+,
\qquad
\delta^2 I_+,
\]

on the simplest source-compatible background. The resulting deformation operator must be checked for complex closure before any Standard Model spectrum matching is attempted.
