# Binary-neutron-star black-hole jet replication

This project reverse-engineers and reproduces the 1.4 s post-merger visualisation associated with:

> K. Hayashi, K. Kiuchi, K. Kyutoku, Y. Sekiguchi and M. Shibata, “Jet from Binary Neutron Star Merger with Prompt Black Hole Formation,” *Physical Review Letters* **134**, 211407 (2025). DOI: `10.1103/PhysRevLett.134.211407`; arXiv: `2410.10958`.

The project deliberately separates two claims that are easy to blur:

1. **Reduced-order visual replication** — runnable on a workstation now. It reconstructs the movie timing and emulates the observed disk, ejecta, magnetic-funnel and jet morphology. It is a calibrated surrogate, not a numerical-relativity solve.
2. **Full-fidelity scientific replication** — a staged GRMHD + dynamical-spacetime + neutrino-radiation campaign whose target is both code-lineage exactness and independently equivalent physics. The orchestration, manifests, validation suite and HPC campaign scaffolding live under `full_fidelity/`.

## Repository map

- `reduced_order/` — source analysis, frame-by-frame data, reproducible surrogate code and rendered videos.
- `full_fidelity/` — exact/equivalent replication specification, run-control code, diagnostics, tests and HPC templates.
- `references/` — primary-source bibliography, parameter ledger and provenance.

## Epistemic status

The uploaded clip begins at approximately **14.96 ms after merger**. The prompt collapse has already occurred; the movie visualises the post-collapse black-hole–torus system, magnetic-field amplification, disk wind and bipolar jet through approximately **1.399 s**.

An *exact* rerun of the authors’ calculation requires the precise SACRA-MPI revision, build options, LORENE initial-data file, finite-temperature EOS table, weak-interaction/opacity tables, grid decomposition, atmosphere/floor policy, and checkpoint/restart history. Those assets were not all published with the paper. This repository therefore keeps two parallel targets:

- **X-track:** byte/provenance-level reproduction using the authors’ exact artifacts once obtained.
- **E-track:** an independently implemented calculation matching the governing equations, physical inputs, effective resolution, diagnostics and convergence envelope.

No surrogate output is represented as full GRMHD data.
