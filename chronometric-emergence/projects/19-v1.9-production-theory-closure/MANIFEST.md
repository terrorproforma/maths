# Manifest - Chronometric 3PI Pre-HPC Theory Closure v1.9

## Primary report

- `production_theory_closure_v1_9.pdf` - visually verified six-page technical closure note.
- `production_theory_closure_v1_9.md` - editable source.
- `production_theory_closure_v1_9.tex` - generated LaTeX source.

## Frozen theory specifications

- `docs/diagram_and_counterterm_ledger_v1_9.md` - exact 11-topology three-loop 3PI ledger and derivative rules.
- `docs/tensor_basis_spec_v1_9.md` - complete component tensor spaces and rank diagnostics.
- `docs/renormalization_closure_v1_9.md` - 32-entry bulk/composite/initial counterterm closure basis.
- `docs/benchmark_hierarchy_v1_9.md` - analytic and reduced numerical limits.
- `docs/production_launch_checklist_v1_9.md` - launch and stop gates.
- `production_theory_acceptance_matrix_v1_9.csv` - integrated status matrix.

## Machine-readable inputs

- `data/diagram_ledger_v1_9.{csv,json}`
- `data/vertex_catalog_v1_9.json`
- `data/tensor_basis_catalog_v1_9.json`
- `data/counterterm_closure_matrix_v1_9.{csv,json}`
- `config/hpc_solver_spec_v1_9.yaml` - absolute-path runtime configuration.
- `config/hpc_solver_spec_portable_v1_9.yaml` - portable package configuration.
- `config/observable_error_contract_v1_9.yaml`

## Executable validation package

- `src/chronometric_hpc/` - configuration, ledger, basis, renormalization, benchmark, kernel, BSE and preflight modules.
- `tests/` - ten regression and closure tests.
- `preflight.sh` - one-command validation.
- `preflight_report_v1_9.json` - 12/12 passing machine-readable result.
- `preflight_and_test_output_v1_9.txt` - archived console output.

## Inherited controlled inputs

- `inputs/prehpc_closure_*_v1_8.*`
- `inputs/gauge_covariant_correlator_*_v1_7.*`
- `inputs/hard_portal_retarded_*_v1_6.*`

## Integrity

- `SHA256SUMS.txt` - hashes for package files, excluding the checksum file itself.
