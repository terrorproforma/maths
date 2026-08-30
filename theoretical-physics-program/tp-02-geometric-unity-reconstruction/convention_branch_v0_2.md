# Provisional repaired convention branch v0.2

This file freezes one internally consistent convention so TP-02 can proceed beyond source transcription. It does **not** overwrite the primary source.

## Branch name

\[
\mathsf{R}_+
\]

— right action, stabilizing tilted subgroup, plus-sign augmented torsion.

## Definitions

The ordinary right gauge action is

\[
A\cdot\varepsilon
=
\varepsilon^{-1}A\varepsilon+\varepsilon^{-1}d\varepsilon.
\]

The covariant derivative relative to the observation-dependent distinguished connection is

\[
d_{A_0}\varepsilon
=
d\varepsilon+A_0\varepsilon-\varepsilon A_0.
\]

The right semidirect product is

\[
(\varepsilon_1,a_1)(\varepsilon_2,a_2)
=
\left(\varepsilon_1\varepsilon_2,\,\varepsilon_2^{-1}a_1\varepsilon_2+a_2\right).
\]

The tilted subgroup is the actual stabilizer of \(A_0\):

\[
\tau_-(h)=\left(h,-h^{-1}d_{A_0}h\right).
\]

The repaired augmented torsion is

\[
\boxed{\widetilde T_\omega=a+\varepsilon^{-1}d_{A_0}\varepsilon.}
\]

It transforms covariantly:

\[
\widetilde T_{g\tau_-(h)}=h^{-1}\widetilde T_g h.
\]

## Geometric interpretation

The source defines an affine difference and orders the two connections in a way that produces the printed minus-sign expression. The repaired branch is equivalent to reversing that ordered difference while preserving both the source's right action and the claim that the tilted subgroup stabilizes \(A_0\).

## Rules for subsequent work

1. The literal source branch \(T_-\) is never silently replaced.
2. Every equation depending on augmented torsion is labelled `PRINTED` or `R_PLUS`.
3. The distinguished connection remains \(A_0[\gimel]\); it is not varied as a fixed background when the observation field varies.
4. Boundary pairings and formal adjoints are not used until their domains are declared.
5. A pass in the repaired branch does not retroactively prove the printed lemma.
6. A failure common to both branches is convention-independent and receives greater evidential weight.
