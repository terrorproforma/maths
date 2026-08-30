# TP-01 v1.1 - Dirac, BRST, Kaluza-Klein and Global Audit

**Author:** Angus Muffatti  
**Version:** 1.1  
**Date:** 28 August 2026  
**Status:** **COMPLETE / STRONG DYNAMICAL PARENT REJECTED IN THE DECLARED CLASS**

## Research question

The v1.0 project established an exact action-level genealogy:

\[
\text{6D relative Chern-Weil}
\longrightarrow
\text{5D transgression / Chern-Simons}
\longrightarrow
\text{4D }\phi F\wedge F
\longrightarrow
\text{fixed-holonomy MacDowell-Mansouri}
\longrightarrow
\text{Einstein-Cartan}+\Lambda+\text{Euler}.
\]

The remaining question was whether the fixed-holonomy Einstein sector is a genuine dynamical reduction of the parent, rather than a non-invertible deletion of fields and equations.

## Terminal verdict

\[
\boxed{
\begin{array}{c}
\text{Exact common geometric genealogy: YES.}\\[1mm]
\text{Correct Einstein-sector symplectic pullback: YES.}\\[1mm]
\text{Dynamically invariant BRST/symplectic reduction: NO.}\\[1mm]
\text{Healthy two-helicity parent in the stated class: NO.}
\end{array}}
\]

The named follow-up calculation is complete. No HPC calculation is required.

## Strongest results

1. **Regular canonical parent sector:** the five-dimensional `Spin(4,2)` Chern-Simons theory has a regular canonical stratum with presymplectic rank 56 and **13 local configuration degrees of freedom**.
2. **BRST verdict:** the full circle holonomy has gauge-invariant conjugacy data. Fixing its norm is not a BRST gauge condition.
3. **Deleted equation:** varying the circle zero mode retains the gauge-invariant condition
   \[
   \langle\phi F\wedge F\rangle=0,
   \]
   which generic Einstein solutions violate.
4. **Unexpected pass:** the local covariant presymplectic pullback to the fixed-holonomy surface is exactly the Einstein-Cartan plus Euler potential with the correct coefficients.
5. **Why that is insufficient:** the fixed surface is not invariant under the parent equations and is not a regular gauge/symplectic quotient.
6. **First KK level:** the nonlinear mode set `{-1,0,+1}` is not BRST closed; it generates `+/-2` and hence the full tower. At quadratic order the first conjugate pair adds **26 real regular-sector degrees of freedom**.
7. **Global audit:** the Einstein sector requires a selected Wilson-line conjugacy class, a Lorentz structure-group reduction, and declared bundle/cobordism data.
8. **Strengthened theorem:** under the declared local, polynomial, pure-connection, regular, all-zero-mode, BRST-preserving and globally specified assumptions, no parent in the tested class reduces to pure four-dimensional Einstein gravity with only two graviton helicities.

## Numerical verification

The deterministic regular-sector witness uses seed `0` and gives:

- `||K|| = 3.9459171e-13`
- constraint Jacobian rank `15`
- presymplectic rank `56`
- four diffeomorphism null vectors
- maximum null residual `1.5796062e-12`
- full adjoint orbit dimension of `J_54`: `8`
- centralizer dimension: `7`
- `SO(3,2)` vector orbit dimension: `4`
- first missing KK modes: `[-2,+2]`
- first KK conjugate pair: `26` real configuration degrees of freedom

All **12 programmed checks** and **5 unit tests** pass. This means the calculations are internally verified; it does **not** mean the strong parent passes the TP-00 acceptance gates.

## TP-00 acceptance result

The exact genealogy passes its definition and reproducibility tests. The strong dynamical parent receives fatal zeros on symmetry/reduction closure, physical degree count, constraint reduction, perturbative health of the claimed GR-like vacuum, radiative/EFT decoupling, and full-parent Einstein recovery. Scores are independent and are not averaged.

See:

- `acceptance_matrix.csv`
- `claim_novelty_acceptance_matrix.csv`
- `strengthened_no_go_theorem.md`

## Publication position

The package is suitable as a mathematical-physics clarification/preprint. It is **not** a new fundamental interaction or UV completion. Before journal submission, the remaining external checks are:

- specialist review of the minimal integral lattice for the chosen global Lorentzian `Spin(4,2)` form;
- independent review of the scope assigned to exotic degenerate/irregular strata.

These are review items, not unperformed calculations needed for the terminal theorem.

## Reproduce

```bash
python -m pip install -r requirements.txt
make all
```

Equivalent explicit sequence:

```bash
python code/verify_dirac_brst_global_v1_1.py --root .
python code/generate_summary_figures.py --root .
python -m unittest discover -s code/tests -v
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  tp01_dirac_brst_global_audit_v1_1.tex
cd ..
python code/final_validate.py --root .
python code/build_manifest.py --root .
```

## Key files

### Main paper

- `TP-01_Dirac_BRST_Global_Audit_v1.1.pdf` - compiled 20-page technical paper
- `paper/tp01_dirac_brst_global_audit_v1_1.tex` - complete LaTeX source

### Analytic work

- `dirac_brst_analysis.md` - canonical constraint and BRST/BFV derivation
- `kk_brst_closure.md` - exact mode algebra, finite-mode theorem and first-level count
- `global_bundle_large_gauge_audit.md` - bundle, Wilson line, large-gauge and boundary audit
- `strengthened_no_go_theorem.md` - theorem, proof and escape assumptions
- `source_and_notation_ledger.md` - conventions and source roles
- `notes/research_notes.md` - concise research log and interpretation

### Verification

- `code/verify_dirac_brst_global_v1_1.py`
- `code/generate_summary_figures.py`
- `code/tests/test_verification.py`
- `results/verification_results.json`
- `results/verification_summary.json`
- `acceptance_matrix.csv`
- `claim_novelty_acceptance_matrix.csv`

### Provenance

- `tp00_import/` - frozen TP-00 gates, seams and recovery limits
- `tp01_original_brief.md` - original standalone assignment
- `v1_0_input_digest.md` - v1.0 construction and named unresolved calculation
- `bibliography/references.bib` - persistent source metadata
- `manifest_sha256.csv` - file checksums

## Scope warning

The regular-sector numerical object is a local algebraic phase-space witness, not a global five-dimensional spacetime solution. The theorem does not claim to classify every singular Chern-Simons stratum. It instead proves that the proposed route cannot simultaneously retain regularity, all zero modes, pure-connection dynamics, BRST closure and a pure two-helicity Einstein daughter.
