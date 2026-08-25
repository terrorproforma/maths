# Gauge-Covariant Correlator Closure v1.7

## Purpose

This package corrects and advances the requested off-shell correlator target for the q-D-H portal.

The conventional arbitrary-off-shell elementary Higgs self-energy is gauge dependent. The package therefore supplies:

- a PT/BFM near-shell retarded benchmark anchored to the v1.6 hard+LPM rate;
- numerical longitudinal Ward-identity closure for dressed scalar and fermion propagators;
- a Nielsen gauge-dependence diagnostic;
- a gauge-singlet H-dagger-H control spectral function;
- a concrete three-loop 3PI/Kadanoff-Baym implementation specification.

## Reproduce

Run:

```bash
python verify_gauge_covariant_correlator_v1_7.py
```

The script expects the included v1.6 input files:

- `hard_portal_retarded_results_v1_6.json`
- `hard_portal_retarded_grid_v1_6.npz`

## Scope

The PT/BFM grid is a controlled near-shell benchmark, not an exact arbitrary-off-shell full-Standard-Model thermal self-energy. The full differential hard-soft subtraction, ghost/matter kernels and transverse vertex system remain open.
