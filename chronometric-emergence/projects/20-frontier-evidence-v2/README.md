# Chronometric emergence — frontier evidence repair v2

**Author: Angus Muffatti**

This is the adversarial repair layer created after an independent audit found that many earlier `PASS` labels proved internal consistency rather than physics. It does not conceal that result. It turns the criticism into executable gates.

## What this package actually does

- independently checks the magnitudes of all eleven three-loop 3PI ledger coefficients by coloured half-edge graph automorphisms;
- demonstrates that the former v1.3 RG cancellation was imposed rather than derived and formally retracts it;
- runs a genuine non-Markovian two-time scalar benchmark with independent normal-mode and causal-memory solvers, timestep/memory convergence, commutator, FDT, and energy diagnostics;
- recalculates the cascade daughter fate and supplies an exact-`Z6` gauge-charged thermalisation repair;
- evaluates the low-`f_a` ridge for Earth, Sun, white dwarfs, and neutron stars;
- quantifies a 24-link gauge/deconstruction route to the required UV quality;
- recomputes the v1.4 LPM diagnostic with the corrected collinear mass combination, executes the v1.5 high-resolution recomputation, and checks weak-scattering scaling;
- measures the v1.7/v1.8 off-shell model discrepancy and forbids table extrapolation;
- scans portability and replaces the old binary `PASS` vocabulary with an evidence taxonomy.

## Run

```bash
python -m pip install -e '.[test]'
python -m frontier_evidence.run_all --repo-root ../..
pytest -q
```

The run writes machine-readable evidence to `results/` and a consolidated report to `docs/FRONTIER_EVIDENCE_REPORT.md`.

## Honest status

The package earns a **credible evidence frontier** for the narrow formal theorem, one-loop threshold interpretation, code-quality repairs, and scalar two-time infrastructure. It does **not** yet earn the claimed non-Abelian/cosmological frontier: neutron-star conversion, full UV completion, complete hard+LPM matching, and a real 3PI evolution engine remain load-bearing.
