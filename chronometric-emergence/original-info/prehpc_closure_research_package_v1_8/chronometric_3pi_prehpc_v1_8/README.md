# Chronometric PT/BFM-3PI pre-HPC package v1.8

This package is the executable preflight layer for the next numerical stage of the chronometric q-D-H project.

It **does not** assume that a finite 3PI truncation is gauge invariant. The numerical calculation must pass explicit background Ward, quantum Slavnov-Taylor, Nielsen-pole, KMS, conservation, factorization-scale and gauge-singlet-spectrum tests.

## Included

- A machine-readable three-loop 3PI/Kadanoff-Baym solver specification.
- Loader and interpolator for the pointwise PT/BFM matching table.
- Factorization-scale cancellation regression.
- Transverse separable-BSE and STI helper routines.
- Conserving singlet-ladder helper.
- Automated preflight and unit tests.

## Run the preflight

```bash
PYTHONPATH=src python -m chronometric_hpc.driver \
  --config config/hpc_solver_spec_v1_8.yaml \
  --results /mnt/data/prehpc_closure_results_v1_8.json
```

## Run tests

```bash
PYTHONPATH=src pytest -q
```

## Correct numerical target

The production calculation is a **PT/BFM-constrained three-loop 3PI system with a conserving H-dagger-H Bethe-Salpeter control**, not a naive 3PI truncation with bare vertices. Gauge consistency is measured, not presumed.
