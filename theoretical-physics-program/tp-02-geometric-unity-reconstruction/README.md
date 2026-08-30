# TP-02 — Independent Reconstruction of Geometric Unity

**Author:** Angus Muffatti  
**Project status:** **ACTIVE — Phase 1 primary-source reconstruction**  
**Source freeze:** 30 August 2026  
**Current version:** 0.1.0

## Research question

Can the primary Geometric Unity material be converted into a complete, independently reproducible mathematical theory tuple and then tested against the frozen TP-00 acceptance gates?

## Current result

The official primary corpus is sufficient to begin a serious reconstruction. It is **not yet sufficient to treat Geometric Unity as a fully typed, dynamically complete successor theory without additional derivation**.

The source gives a substantial geometric architecture:

- an `Observerse` consisting of two spaces linked by local observation maps;
- the Einsteinian choice `Y = Met(X)` with `dim X = 4` and `dim Y = 14`;
- a rank-14 metric `Chimeric Bundle` with stated signature `(7,7)`;
- `Spin(7,7)` spinors and a main structure group `U(64,64)`;
- an inhomogeneous gauge group built from gauge transformations and adjoint-valued one-forms;
- a distinguished connection, augmented torsion and a family of `Shiab` contraction operators;
- first- and second-order bosonic actions, a fermionic operator proposal and a deformation-complex proposal;
- claimed observed-field decompositions including ordinary, exotic spin-3/2 and dark sectors.

The initial executable audit confirms the basic dimension bookkeeping:

\[
4 + \dim\operatorname{Sym}^2(\mathbb R^4)=4+10=14,
\]

\[
\dim S_{7,7}^{\rm Dirac}=128,
\qquad
\dim S_{7,7}^{\rm Weyl}=64,
\]

and the source's gamma-traceless vector-spinor accounting:

\[
832 = 64 + 192 + 576.
\]

These checks verify **dimensions only**. They do not prove the claimed branching rules, chirality mechanism, dynamics or phenomenology.

## Why the project is not yet at the spectrum calculation

The primary draft itself labels several components as provisional. In particular:

- a Clifford-algebra decomposition is flagged as needing verification;
- the displayed deformation-complex diagram is explicitly caveated as potentially inconsistent;
- the 14-dimensional propagation mechanism that must appear four-dimensional to observers is not worked out;
- the source describes the presentation as a working draft rather than a finished theory;
- no complete Hamiltonian/BRST degree count, anomaly polynomial, quantum measure or global phenomenological fit is supplied.

Those are not rhetorical objections. They determine the order of work. We first reconstruct and type every object, then derive the gauge complex and principal symbol, and only then run the fatal spectrum and recovery gates.

## Exact next calculation

The next committed phase will:

1. select the source's explicit first-order bosonic model;
2. replace the source glyphs with a reversible notation dictionary, without changing their meaning;
3. derive the first variation independently;
4. choose the simplest source-compatible background;
5. compute the linearized gauge complex and principal symbol;
6. test whether the proposed deformation sequence is actually a complex;
7. count propagating and gauge degrees of freedom before attempting Standard Model matching.

The first fatal kill tests are therefore:

\[
\boxed{
\text{typed field equations}
+
\text{gauge/BRST closure}
+
\text{quadratic principal symbol}
+
\text{physical degree count}.
}
\]

## Repository structure

- `sources/primary_source_manifest.json` — frozen official corpus and usage rules.
- `sources/primary_source_notes.md` — source-derived outline with page/equation references.
- `theory_tuple_v0_1.md` — first independent typing of spaces, bundles, fields, symmetries and dynamics.
- `source_definition_index.csv` — object-by-object source locations and reconstruction status.
- `source_claim_ledger.csv` — claims separated from checks and unresolved assumptions.
- `symbol_typing_issues.md` — overloaded or unstable notation requiring reversible aliases.
- `acceptance_matrix.csv` — non-aggregated TP-00 gate status.
- `code/verify_representation_dimensions.py` — executable dimension bookkeeping.
- `results/representation_dimension_checks.json` — machine-readable output.
- `results/initial_audit_summary.md` — current terminal status of Phase 1.
- `tp00_import/` — symlinks to the authoritative frozen TP-00 gates and limits.

## Reproduce

```bash
python code/verify_representation_dimensions.py --root .
```

or:

```bash
make verify
```

## Epistemic rule

The 2021 draft and official lecture transcript are primary evidence for **what Geometric Unity proposes**. They are not evidence that the proposal is mathematically consistent or physically correct. Source statements, project derivations and external literature are tracked separately.

## Scope and rights

The official PDF identifies itself as a copyrighted working draft and restricts derivative use. The PDF is therefore not mirrored in this repository. This project stores a source manifest, narrow mathematical paraphrases, equation references and independent verification code. It does not republish the manuscript.
