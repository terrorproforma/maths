# Chronometric 3PI Pre-HPC Theory Closure v1.9

This package closes the five finite theory tasks remaining after v1.8 and authorizes a PT/BFM-constrained unit test and pilot run.

## Status

- Preflight: **12/12 PASS**
- Unit tests: **10/10 PASS**
- Pilot: **AUTHORIZED**
- Production: **CONDITIONAL ON PILOT**

## Start here

1. `production_theory_closure_v1_9.pdf`
2. `docs/production_launch_checklist_v1_9.md`
3. `config/hpc_solver_spec_portable_v1_9.yaml`
4. `production_theory_acceptance_matrix_v1_9.csv`

## Run

```bash
./preflight.sh
```

## Scope

The package freezes the declared three-loop 3PI functional, component tensor spaces, local power-counting counterterm basis, initial correlations, benchmarks, observables and error gates. It does not claim an all-order proof of gauge invariance or renormalizability for finite non-Abelian 3PI truncations. Those are pilot acceptance questions.
