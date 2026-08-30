# TP-02 — Independent Reconstruction of Geometric Unity

**Author:** Angus Muffatti  
**Project status:** **ACTIVE — source-faithful branch classified; repaired completion entering quadratic audit**  
**Source freeze:** 31 August 2026  
**Current version:** 0.4.0

## Research question

Can the official Geometric Unity primary material be converted into a complete, independently reproducible mathematical theory tuple and then tested against the frozen TP-00 acceptance gates?

## Current verdict

\[
\boxed{
\begin{array}{c}
\textbf{Substantial geometric architecture: YES.}\\[1mm]
\textbf{Literal printed first-order covariance: NO.}\\[1mm]
\textbf{Explicit substitute Shiab typeable: YES.}\\[1mm]
\textbf{Einstein contraction on the Riemann sector: VERIFIED.}\\[1mm]
\textbf{Unique full source-defined Hessian and spectrum: NO.}
\end{array}
}
\]

The project has now separated four things that were previously easy to conflate:

1. the literal 2021 draft;
2. the earlier Oxford/PowerPoint convention;
3. a minimal algebraic repair;
4. an independent completion suitable for physical testing.

## Completed work

### Phase 1 — source reconstruction

- Froze the official source corpus.
- Typed the initial theory tuple.
- Indexed definitions and claims.
- Verified the basic representation dimensions exactly.

### Phase 2 — sign-convention audit

The 2021 printed right action and tilted stabiliser give

\[
T_-\bigl(g\tau_-(h)\bigr)
=
h^{-1}T_-(g)h
-
2h^{-1}d_{A_0}h.
\]

Therefore the printed augmented torsion is not equivariant under the printed stabiliser.

The stabiliser-compatible repair is

\[
T_+
=
a+\varepsilon^{-1}d_{A_0}\varepsilon.
\]

### Phase 3A — first-order action covariance

For the literal branch,

\[
I_-^h-I_-=14
\]

in the exact rational witness.

For the repaired branch,

\[
I_+^h-I_+=0.
\]

Thus the literal first-order action fails in its claimed tilted-gauge-invariant form, while the repaired branch survives the kinematic covariance test.

### Phase 3B — Oxford-source integration and Shiab reconstruction

The official Oxford page is a composite primary source containing:

- the 2013 lecture;
- the 2020 Portal presentation context;
- a supplementary PowerPoint with updated notation.

It records a plus-sign tilted map but a minus-sign augmented torsion, confirming genuine convention drift across official versions.

The explicit 2021 substitute Shiab at eq. (9.3) has now been typed as

\[
\operatorname{Sh}_{\varepsilon}:
\Omega^2(Y,\operatorname{ad}P_H)
\longrightarrow
\Omega^{13}(Y,\operatorname{ad}P_H).
\]

An exact Clifford calculation shows that its Einstein-like property selects:

\[
\text{vector--bivector commutator}
+
\text{bivector Jordan trace}
+
\text{scalar multiplication}.
\]

On algebraic Riemann curvature,

\[
[\gamma^c,F_{cd}]
=
R_{db}\gamma^b,
\]

\[
\{\gamma^{cd},F_{cd}\}
=
-R\,\mathbf1,
\]

and therefore

\[
[\gamma^c,F_{cd}]
+
\frac12\{\gamma^{cd},F_{cd}\}\gamma_d
=
G_{db}\gamma^b.
\]

For \(n=14\), the map has the expected algebraic benchmark

\[
\operatorname{rank}=105,
\qquad
\dim\ker=3080,
\]

with the Weyl sector forming the kernel.

## Why this still does not produce a unique spectrum

The official corpus does not uniquely specify:

- concrete normalised \(\Phi_1,\Phi_2\) representatives over the full \(U(64,64)\) adjoint bundle;
- their dependence on the observation field;
- the extension of the mixed Clifford products beyond geometric curvature;
- the global Hodge, reality and formal-adjoint domains;
- boundary conditions;
- a background solving the repaired equations;
- the complete fermionic and deformation-complex completion.

The source itself says the originally preferred Bianchi-selected Shiab cannot presently be located and offers eq. (9.3) as a substitute.

So the source-faithful terminal result is:

\[
\boxed{
\text{no unique full principal symbol or physical mode count follows from the official corpus alone.}
}
\]

This is source incompleteness, not a theorem against every completion.

## Active branch

The next independent branch is

\[
\mathsf{R}_+\text{-EIN},
\]

defined by:

- the stabiliser-compatible \(T_+\) repair;
- the verified mixed Clifford Einstein contraction;
- explicit project-selected \(\Phi_1,\Phi_2\) representatives;
- declared metric, boundary and adjoint domains.

Every result from this branch is labelled as a project construction rather than attributed back to the source.

## Next decisive calculation

1. Construct explicit split-signature \(Cl(7,7)\) representatives on the 128-dimensional spin module.
2. Build canonical candidate tensors
   \[
   \Phi_1=e^A\otimes\Gamma_A,
   \qquad
   \Phi_2=e^A\wedge e^B\otimes\Gamma_{AB}.
   \]
3. Extend the verified Einstein contraction to the full declared adjoint sector.
4. Compute the quadratic symbol around the simplest local repaired background.
5. Test the linearised gauge/deformation complex.
6. Count gauge, constrained and propagating modes.
7. Stop on the first applicable fatal TP-00 zero.

## Reproduce

```bash
make verify
```

This runs:

- representation-dimension checks;
- inhomogeneous-group sign checks;
- first-order action covariance checks;
- exact Clifford–Einstein Shiab checks;
- all unit tests.

## Key files

- `STATUS.md` — current phase and gate status.
- `sources/primary_source_manifest.json` — authoritative source hierarchy.
- `sources/oxford_lecture_source_audit.md` — detailed audit of the added official page.
- `sources/oxford_lecture_equation_index.csv` — equation/timestamp map.
- `sign_convention_audit.md` — exact section 5–7 sign result.
- `phase3_first_order_variational_audit.md` — literal versus repaired action covariance.
- `phase3b_shiab_reconstruction.md` — typed operator, derivatives and Clifford theorem.
- `completion_branches_v0_4.md` — branch separation.
- `code/verify_shiab_einstein_pattern.py` — exact rational Clifford verifier.
- `results/shiab_einstein_pattern.json` — machine-readable result.
- `acceptance_matrix.csv` — independent TP-00 gate scores.

## Epistemic rule

The official draft, lecture and supplementary slides establish what the proposal says. They do not establish that it is mathematically consistent or physically correct. Source statements, source conflicts, repairs and independent completions are recorded separately.

## Scope and rights

The copyrighted draft is not mirrored. This repository stores bibliographic metadata, narrow mathematical paraphrases, equation references and independent verification code.
