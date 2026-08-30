# Official Oxford-lecture source audit

**Project:** TP-02 — Independent Reconstruction of Geometric Unity  
**Source:** `https://geometricunity.org/2013-oxford-lecture/`  
**Audit date:** 31 August 2026  
**Status:** official composite primary source

## 1. What the page contains

The page is not merely a link to a 2013 talk. It combines three chronologically distinct primary-source components:

1. the first University of Oxford lecture, delivered in 2013;
2. the Portal preface and publication context associated with the 2 April 2020 upload;
3. a supplementary PowerPoint described by the official page as using more up-to-date notation.

The technical transcript and supplementary slide images are source evidence for what the proposal asserted at those dates. They do not establish mathematical consistency or physical correctness.

The 2021 working draft remains the controlling source when definitions conflict with the earlier lecture. Conflicts are preserved rather than harmonised silently.

## 2. Technical content added to the reconstruction

### 2.1 Inhomogeneous and tilted gauge groups

At approximately `01:27:54`, the lecture writes the tilted map with a plus sign,

\[
h\longmapsto
\left(
h,\,
+h^{-1}d_{A_0}h
\right).
\]

The 2021 draft instead prints

\[
\tau_{A_0}(h)
=
\left(
h,\,
-h^{-1}d_{A_0}h
\right)
\]

in its stabiliser construction.

This is a real cross-version convention change, not a paraphrase. Under the 2021 right action, the minus-sign map is the actual stabiliser of \(A_0\). The earlier plus-sign map pairs naturally with the minus-sign augmented torsion for covariance, but it is not the same stabiliser under that later action convention.

### 2.2 Augmented torsion

At approximately `01:41:26`, and again in the supplementary slide headed **Augmented Torsion**, the page gives the minus-sign expression

\[
T_{\varepsilon,\pi}
=
\pi-\varepsilon^{-1}d_{A_0}\varepsilon.
\]

Thus the official source history contains at least these pairs:

| Source component | Tilted-map sign | Torsion sign |
|---|---:|---:|
| 2013 lecture / supplementary presentation | \(+\) | \(-\) |
| 2021 draft as printed | \(-\) | \(-\) |
| TP-02 stabiliser-compatible repair | \(-\) | \(+\) |

The source history therefore confirms the draft's own warning that multiple sign conventions were combined.

### 2.3 Shiab operator family

At approximately `01:35:41`–`01:38:00`, the page describes a Shiab as a gauge-conjugated contraction built from invariant Clifford/exterior-algebra elements. It states the form-degree target

\[
\operatorname{Sh}_{\varepsilon}:
\Omega^i(Y,\operatorname{ad}P)
\longrightarrow
\Omega^{d-3+i}(Y,\operatorname{ad}P).
\]

For curvature, \(i=2\), so in \(d=14\),

\[
\Omega^2
\longrightarrow
\Omega^{13}.
\]

The page also says the bracket can combine:

- wedge or contraction in the differential-form factor;
- Lie commutator or \(i\) times a Jordan anticommutator in the matrix factor.

That freedom is mathematically material. It changes the operator outside the geometric Riemann-curvature sector.

### 2.4 First-order equation

At approximately `01:43:32`, the lecture gives the schematic first-order bosonic equation

\[
\operatorname{Sh}_{\varepsilon}(F)
+
\left[
\operatorname{Sh}_{\varepsilon}(T),
T
\right]
+
*T
=
0.
\]

The accompanying supplementary slide calls the left side **swervature** and the right torsion term **displasion**. This is proposal-level evidence, not a derivation of the Euler–Lagrange system.

## 3. Relation to the explicit 2021 substitute

The 2021 draft supplies a concrete substitute at eq. (9.3). The Oxford page helps interpret its intent:

- the first contraction is Ricci-like;
- the nested contraction is scalar-curvature-like;
- the Weyl-like component is intended to be annihilated.

The exact Clifford audit in `phase3b_shiab_reconstruction.md` shows that this intended Einstein pattern selects:

1. a commutator for the vector–bivector contraction;
2. a Jordan/anticommutator contraction for the bivector trace;
3. scalar multiplication in the final one-form.

This resolves the product pattern on the geometric Riemann subspace. It does not uniquely define the full \(U(64,64)\)-adjoint extension.

## 4. Epistemic consequence

The additional official source improves the reconstruction but does not remove the terminal source gap.

\[
\boxed{
\begin{array}{c}
\text{The explicit substitute Shiab can be typed and checked}\\
\text{on the geometric Riemann-curvature subspace.}\\[1mm]
\text{The full adjoint-valued nonlinear operator, its metric derivative,}\\
\text{and its boundary/adjoint domains remain non-unique.}
\end{array}
}
\]

No principal-symbol or physical-spectrum claim may silently replace those missing data with an investigator's preferred completion.