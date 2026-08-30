# Sign-convention audit of the inhomogeneous gauge group

**Project:** TP-02 — Independent Reconstruction of Geometric Unity  
**Phase:** 2  
**Primary source:** *Geometric Unity: Author's Working Draft*, v1.0, pp. 31–39, especially eqs. (5.9), (5.10), (6.2), (6.4), (6.13), (7.3), and (7.4).  
**Audit status:** **DECISIVE LOCAL RESULT — PRINTED FORMULAS ARE NOT MUTUALLY CONSISTENT**

## Scope

This audit asks whether the printed right semidirect-product convention, affine action on connections, tilted stabilizer, and augmented-torsion transformation law are mutually compatible. The source itself warns that this section may contain conflicting sign conventions. The result below localizes that conflict exactly. It does not show that every repaired formulation of Geometric Unity fails.

## Printed formulas

Let

\[
N=\Omega^1(Y,\operatorname{ad}P_H).
\]

The printed right semidirect product is reconstructed as

\[
(\varepsilon_1,a_1)(\varepsilon_2,a_2)
=
\left(\varepsilon_1\varepsilon_2,\,\varepsilon_2^{-1}a_1\varepsilon_2+a_2\right).
\]

The ordinary right gauge action is

\[
A\cdot\varepsilon=\varepsilon^{-1}A\varepsilon+\varepsilon^{-1}d\varepsilon.
\]

For a distinguished connection \(A_0\), define

\[
d_{A_0}\varepsilon=d\varepsilon+A_0\varepsilon-\varepsilon A_0.
\]

Then

\[
A_0\cdot\varepsilon=A_0+\varepsilon^{-1}d_{A_0}\varepsilon.
\]

For \(\alpha=A-A_0\), draft eq. (6.2) reads

\[
\alpha\cdot(\varepsilon,a)
=
\varepsilon^{-1}\alpha\varepsilon
+
\varepsilon^{-1}d_{A_0}\varepsilon
+a.
\]

The stabilizing tilted map in eq. (6.4) is

\[
\tau_-(h)=\left(h,-h^{-1}d_{A_0}h\right),
\]

and it indeed satisfies

\[
A_0\cdot\tau_-(h)=A_0.
\]

The corresponding right action, eq. (6.13), is

\[
(\varepsilon,a)\tau_-(h)
=
\left(\varepsilon h,\,h^{-1}ah-h^{-1}d_{A_0}h\right).
\]

The printed augmented torsion in eq. (7.3) is

\[
T_-(\varepsilon,a)=a-\varepsilon^{-1}d_{A_0}\varepsilon,
\]

while Lemma 7.2 claims

\[
T_-\bigl((\varepsilon,a)\tau_-(h)\bigr)=h^{-1}T_-(\varepsilon,a)h.
\]

## Exact transformation

The covariant product rule gives

\[
d_{A_0}(\varepsilon h)=(d_{A_0}\varepsilon)h+\varepsilon\,d_{A_0}h.
\]

Substitution yields

\[
\boxed{
T_-\bigl(g\tau_-(h)\bigr)
=
\operatorname{Ad}(h^{-1})T_-(g)-2h^{-1}d_{A_0}h.
}
\]

The claimed equivariance holds only when \(d_{A_0}h=0\), not for a general tilted gauge transformation. The source proof changes the sign of the second component between displayed lines, thereby manufacturing the cancellation.

## Exact rational counterexample

The executable verifier uses exact \(2\times2\) rational matrices and the derivation \(dM=[D,M]\). For

\[
D=\begin{pmatrix}0&1\\0&0\end{pmatrix},\quad
A_0=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
\varepsilon=\begin{pmatrix}1&1\\0&1\end{pmatrix},
\]

\[
h=\begin{pmatrix}2&0\\1&1\end{pmatrix},\qquad
a=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\]

the residual is exactly

\[
T_-\bigl(g\tau_-(h)\bigr)-h^{-1}T_-(g)h
=
\begin{pmatrix}-1&1\\5&1\end{pmatrix}
=-2h^{-1}d_{A_0}h.
\]

No floating-point approximation is involved.

The same exact test confirms:

- the printed semidirect-product law is associative;
- the printed affine formula is a right action;
- \(\tau_-\) is a homomorphism;
- \(\tau_-\) stabilizes \(A_0\).

The failure is therefore localized to the incompatibility between the printed stabilizer sign and the printed augmented-torsion sign.

## Two repairs

### Repair A — preserve the actual stabilizer

Keep the printed right action and

\[
\tau_-(h)=\left(h,-h^{-1}d_{A_0}h\right),
\]

but reverse the ordered connection difference, equivalently define

\[
\boxed{T_+(\varepsilon,a)=a+\varepsilon^{-1}d_{A_0}\varepsilon.}
\]

Then

\[
T_+\bigl(g\tau_-(h)\bigr)=h^{-1}T_+(g)h
\]

exactly. This is the minimal repair if the intended geometry requires the tilted subgroup to stabilize \(A_0\).

### Repair B — preserve the printed torsion

Keep \(T_-\), but use

\[
\tau_+(h)=\left(h,+h^{-1}d_{A_0}h\right).
\]

This restores torsion equivariance but gives

\[
A_0\cdot\tau_+(h)=A_0+2h^{-1}d_{A_0}h,
\]

so it is not the stabilizer asserted in section 6.

## Project convention

TP-02 provisionally adopts Repair A as the strongest algebraically coherent branch:

\[
\boxed{
\text{printed right action}
+
\tau_-\text{ stabilizer}
+
T_+\text{ repaired augmented torsion}.
}
\]

This is a project repair, not a quotation or attribution to the source. Every later calculation retains both:

1. the literal printed branch \(T_-\);
2. the repaired stabilizer-compatible branch \(T_+\).

## Acceptance consequence

- `ALG-02` remains **1 — PARTIAL / REPAIR REQUIRED**.
- The group law and affine action pass their local algebraic tests.
- The printed augmented-torsion equivariance claim fails exactly.
- A coherent repair exists, so this is not yet a fatal zero against every GU completion.
- No bosonic field equation or principal symbol is uniquely source-faithful until the convention branch is stated.

## Next decisive calculation

Using the explicit Shiab branch displayed in draft eq. (9.3), derive the first variation of the first-order bosonic action in both branches:

\[
\delta I_{B,1}^{\rm printed}[T_-],
\qquad
\delta I_{B,1}^{\rm repaired}[T_+].
\]

The calculation must retain the dependence

\[
A_0=A_0[\text{observation field}]
\]

and compare the resulting gauge identities, deformation operators, and principal symbols.