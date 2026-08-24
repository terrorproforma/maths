# Null-Relational Chronometry

**Author: Angus Muffatti**

This directory is the source-controlled home of the chronometric-emergence research programme. It consolidates the work developed from the original photon-frame discussion through crossed-null kinematics, spectral factorisation, scale locking, QCD-transmitted chronometric shear, cyclic protection, environmental and cosmological tests, nonequilibrium transport, gauge-covariant correlator closure, and the v1.8 pre-HPC launch specification.

## Published project contents

### Consolidated manuscript

- [`manuscript/null_relational_chronometry_v1_4.md`](manuscript/null_relational_chronometry_v1_4.md) — canonical editable manuscript.
- [`manuscript/null_relational_chronometry_v1_4.tex`](manuscript/null_relational_chronometry_v1_4.tex) — complete LaTeX source.
- [`manuscript/references.bib`](manuscript/references.bib) — consolidated bibliography.

### Reproducibility and working data

- [`scripts/verify_consolidated_chronometry.py`](scripts/verify_consolidated_chronometry.py) — original consolidated symbolic and numerical verifier.
- [`scripts/run_repository_verification.py`](scripts/run_repository_verification.py) — repository-layout launcher for the verifier.
- [`data/benchmark_parameters.json`](data/benchmark_parameters.json) — benchmark inputs required by the verification suite.
- [`data/consolidated_verification_results.json`](data/consolidated_verification_results.json) — recorded 32-check verification result.
- [`data/source_ledger.csv`](data/source_ledger.csv) — literature source and role ledger.
- [`data/version_crosswalk.csv`](data/version_crosswalk.csv) — version-by-version result and correction map.
- [`data/integrated_acceptance_matrix.csv`](data/integrated_acceptance_matrix.csv) — integrated PASS, FAIL, CONDITIONAL, and OPEN outcomes.
- [`data/historical_artifact_inventory.csv`](data/historical_artifact_inventory.csv) — inventory of every earlier working filename named during the research sequence.
- [`sources/Photon_Perspective_in_Relativity.txt`](sources/Photon_Perspective_in_Relativity.txt) — original project conversation snapshot.

### Latest correlator and pre-HPC updates

- [`updates/v1.7/README.md`](updates/v1.7/README.md) — gauge-covariant correlator closure, Nielsen control, PT/BFM target correction, and 3PI requirement.
- [`updates/v1.8/README.md`](updates/v1.8/README.md) — completed pre-HPC closure and pilot specification.
- [`config/hpc_solver_spec_v1_8.yaml`](config/hpc_solver_spec_v1_8.yaml) — executable solver and acceptance specification.
- [`updates/v1.8/prehpc_acceptance_matrix_v1_8.csv`](updates/v1.8/prehpc_acceptance_matrix_v1_8.csv) — pre-HPC acceptance matrix.
- [`updates/v1.8/prehpc_claim_matrix_v1_8.csv`](updates/v1.8/prehpc_claim_matrix_v1_8.csv) — claim and scope boundaries.
- [`updates/v1.8/prehpc_resource_estimates_v1_8.csv`](updates/v1.8/prehpc_resource_estimates_v1_8.csv) — unit, pilot, and production resource tiers.
- [`updates/v1.8/prehpc_launch_checklist_v1_8.md`](updates/v1.8/prehpc_launch_checklist_v1_8.md) — launch, acceptance, stop, and promotion gates.

The complete current inventory is in [`FILE_MANIFEST.md`](FILE_MANIFEST.md).

## Run the workstation-verifiable checks

From this directory:

```bash
python3 -m pip install -r requirements.txt
make verify
```

or:

```bash
./reproduce.sh
```

The repository launcher stages the historical archive layout in a temporary directory, runs the unchanged consolidated verifier, and writes the result to `data/consolidated_verification_results.json`. The checked package passes 32 of 32 symbolic and benchmark consistency checks.

The verification suite does **not** reproduce the unresolved full electroweak/Yukawa LPM calculation, arbitrary-off-shell Standard-Model kernel, complete matrix-valued non-Abelian STI system, or full 3+1-dimensional three-loop 3PI/Kadanoff–Baym evolution.

## Current scientific frontier

The corrected computational target is not a gauge-fixed off-shell Higgs self-energy in isolation. It is:

```text
PT/BFM-constrained three-loop 3PI evolution
+ dynamic propagators and three-point vertices
+ ghost and matter-ghost Slavnov–Taylor diagnostics
+ Nielsen pole monitoring
+ pointwise hard/HTL/LPM/overlap matching
+ a conserving gauge-singlet H†H Bethe–Salpeter control
```

The first honest next step is the pilot two-time run defined in the v1.8 solver specification and launch checklist.

## Scientific status and negative results retained

This is an ongoing technical research programme, not a peer-reviewed paper. The repository deliberately preserves corrections and failures that constrain the final theory:

- a photon has no physical rest frame;
- the original exact-null action has a rank-deficient transverse principal symbol;
- the direct crossed-phase composite metric overlaps the singular mimetic construction;
- the Planck-scale cosmological benchmark does not generically select the vacuum and can overclose;
- the original direct bosonic inflaton portal is unsafe during preheating;
- an elementary arbitrary-off-shell gauge-fixed Higgs self-energy is not a unique physical observable;
- finite 3PI truncations cannot be assumed gauge invariant without explicit diagnostics.

The strongest current thesis is narrower: causal or conformal structure may be primitive, while universal operational duration exists precisely when viable clock spectra share one local scalar factor. Chronometric shear is the Weyl-invariant obstruction. A controlled QCD threshold defect transmits into that shear with leading coefficient `2/27` in the displayed model.

## Authorship and provenance

All original research, synthesis, manuscript text, calculations, and project files in this directory are authored by **Angus Muffatti**, with AI assistance disclosed by the repository context. Third-party results remain attributed in the bibliography, source ledger, and provenance record.

Earlier temporary links named many version-specific PDFs, arrays, scripts, and archives. Not every historical binary remained recoverable byte-for-byte. The repository therefore publishes the complete recoverable source package, consolidated manuscript, conversation source, reproducibility files, historical inventory, and latest pre-HPC specification without pretending that expired binaries were recovered. See [`SOURCE_PROVENANCE.md`](SOURCE_PROVENANCE.md).
