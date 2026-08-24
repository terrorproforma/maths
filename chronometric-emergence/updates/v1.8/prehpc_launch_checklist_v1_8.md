# PT/BFM-Constrained 3PI Pilot Launch Checklist — v1.8

**Author: Angus Muffatti**  
**Status:** Pre-HPC closure complete; pilot launch specification.

This checklist defines the minimum evidence required before, during, and after the first two-time pilot. A run is not accepted merely because it converges numerically.

## 1. Source and configuration control

- [ ] Record the exact Git commit SHA.
- [ ] Freeze `config/hpc_solver_spec_v1_8.yaml` for the run.
- [ ] Record compiler, CUDA/HIP, MPI, BLAS, FFT, Python, and driver versions.
- [ ] Record all random seeds and initial-state files.
- [ ] Record the PT/BFM background gauge and every quantum-gauge parameter used in the scan.
- [ ] Record the renormalisation prescription, subtraction points, and initial-surface counterterms.
- [ ] Record the hard-soft separation scales and momentum-grid definitions.

## 2. Preflight regression tests

- [ ] Run `make verify` and require all 32 consolidated checks to pass.
- [ ] Reproduce the v1.6 integrated and on-shell hard-plus-LPM anchor.
- [ ] Reproduce the v1.7 background Ward-identity regression.
- [ ] Verify pointwise hard/HTL/overlap cancellation over every declared `q_*` value.
- [ ] Verify retarded-cut oddness within the configured tolerance.
- [ ] Verify KMS-noise positivity on the complete preflight grid.
- [ ] Verify the declared matter-ghost STI residual.
- [ ] Verify exact transversality of the finite transverse initialization.
- [ ] Verify the conserving `H^\dagger H` BSE residual and positive-frequency spectral positivity.

## 3. Unit-test tier

- [ ] Run `N_r=32`, `l_max=1`, `N_t=512`, `N_mem=64` on one GPU.
- [ ] Check equal-time commutators and spectral normalization at every saved time.
- [ ] Check energy and all implemented charges after each time step.
- [ ] Check causality: retarded kernels must vanish outside the allowed time ordering.
- [ ] Check KMS recovery from an equilibrium initial state.
- [ ] Check exact symmetry preservation from a symmetric initial state.
- [ ] Check checkpoint/restart reproducibility to round-off tolerance.
- [ ] Check that all stop conditions terminate the run cleanly and preserve diagnostics.

## 4. Pilot tier

- [ ] Run `N_r=96`, `l_max=4`, `N_t=4096`, `N_mem=256` on eight GPUs.
- [ ] Evolve propagators and three-point vertices self-consistently; do not freeze the gauge vertices.
- [ ] Evolve or reconstruct ghost and matter-ghost kernels at every diagnostic interval.
- [ ] Generate the `H^\dagger H` ladder kernel from the same time-dependent truncation.
- [ ] Store separate real, virtual, HTL, LPM, and overlap contributions.
- [ ] Store pole locations, residues, widths, integrated rates, and singlet spectral moments.
- [ ] Store Ward, STI, Nielsen, KMS, conservation, and `q_*` residuals as time series.
- [ ] Perform at least three quantum-gauge parameter runs.
- [ ] Perform at least three hard-soft separation-scale runs.
- [ ] Perform at least three memory-window runs.

## 5. Mandatory acceptance gates

- [ ] Background Ward residual remains below the configured threshold.
- [ ] Quantum Slavnov-Taylor residual remains below the configured threshold.
- [ ] Complex poles are stable under the gauge-parameter scan.
- [ ] Integrated rates and gauge-singlet observables are stable under the gauge-parameter scan.
- [ ] `q_*` dependence cancels at the resolved perturbative order.
- [ ] KMS relations are recovered in equilibrium and approached during thermalisation.
- [ ] Energy and implemented charges remain conserved within the configured tolerance.
- [ ] Positive-frequency `H^\dagger H` spectral density remains nonnegative.
- [ ] Equal-time commutators and spectral sum rules remain stable.
- [ ] Momentum, angular, time-step, and memory-window refinements change accepted observables by less than the convergence target.
- [ ] No accepted conclusion depends on the arbitrary off-shell shape of an elementary gauge-dependent propagator.

## 6. Automatic stop conditions

Stop the run and preserve the last valid checkpoint when any of the following occurs:

- [ ] A Ward or STI residual exceeds its hard limit for more than the permitted number of steps.
- [ ] A Nielsen pole drift exceeds its hard limit.
- [ ] Energy or charge conservation exceeds its hard limit.
- [ ] A positive-frequency gauge-singlet spectral density becomes negative beyond numerical tolerance.
- [ ] KMS-noise positivity fails in an equilibrium control run.
- [ ] NaN, infinity, negative occupation, or noncausal support appears.
- [ ] GPU memory pressure prevents a complete checkpoint.

## 7. Production promotion gate

Do not promote the pilot to the production tier until:

- [ ] Every mandatory acceptance gate passes on the pilot grid.
- [ ] The gauge, `q_*`, memory, momentum, angular, and time-step scans close.
- [ ] The pilot reproduces the v1.6 integrated anchor within uncertainty.
- [ ] The gauge-singlet control correlator and pole observables agree across gauges.
- [ ] The full diagnostic bundle is independently reviewed.

The production target is `N_r=192`, `l_max=6`, `N_t=16384`, `N_mem=512` on 128 GPUs, with an estimated aggregate working-memory envelope of approximately 43.93 GB under the declared storage model.
