# PT/BFM-Constrained 3PI Pilot Launch Checklist - v1.9

**Status:** Ready for unit test and pilot; production remains gated by pilot results.

## Frozen theory inputs

- [ ] Confirm Git commit and package checksum.
- [ ] Load the 11-row topology ledger without local edits.
- [ ] Load the vertex catalogue and group representations.
- [ ] Load the tensor-basis catalogue.
- [ ] Load the 32-row counterterm matrix.
- [ ] Load the observable/error contract.
- [ ] Confirm v1.8 input checksums.

## Build and reproducibility

- [ ] Record compiler, GPU stack, MPI, BLAS/LAPACK and HDF5 versions.
- [ ] Enable deterministic reductions for validation.
- [ ] Run `./preflight.sh`; archive stdout, JSON and pytest output.
- [ ] Verify 12/12 preflight checks and all tests pass.
- [ ] Record random seeds and initial-state data.

## Unit run

- [ ] Use 32 radial points, `lmax=1`, 512 time steps, memory 64.
- [ ] Reproduce free, KMS, Ward, narrow-width and Markov benchmarks.
- [ ] Verify equal-time commutators at every checkpoint.
- [ ] Verify no NaN/Inf and no unexplained rank loss.
- [ ] Verify checkpoint/restart reproducibility.

## Pilot run

- [ ] Use 96 radial points, `lmax=4`, 4,096 time steps, memory 256.
- [ ] Evolve every declared two-point function and three-point vertex.
- [ ] Reconstruct/evolve matrix-valued matter-ghost kernels.
- [ ] Generate the `H†H` BSE kernel from the evolving functional.
- [ ] Run `xi={0,0.5,1,2}` and `q*/T={0.15,0.25,0.40}`.
- [ ] Run memory, timestep and basis convergence scans.
- [ ] Archive observables and identity residuals.

## Hard gates

- [ ] Portal-rate error < `1e-3`.
- [ ] Factorization-scale spread < `1e-5`.
- [ ] Background Ward residual < `1e-8`.
- [ ] Quantum STI residual < `1e-6`.
- [ ] Nielsen pole spread < `1e-6`.
- [ ] KMS residual < `1e-7`.
- [ ] Equal-time commutator error < `1e-7`.
- [ ] Energy drift < `1e-6`.
- [ ] Gauge-charge drift < `1e-7`.
- [ ] Singlet spectral negativity < `1e-10`.
- [ ] BSE residual < `1e-8`.
- [ ] Memory-window observable shift < `5e-3`.
- [ ] Gauge-parameter physical-observable shift < `1e-3`.
- [ ] No persistent unaccompanied `p<6` harmonic.

## Production authorization

- [ ] Every hard gate passes.
- [ ] Physical observables converge under all declared scans.
- [ ] Counterterms produce cutoff-independent results.
- [ ] Full-component vertices agree with or improve controls.
- [ ] Singlet control and Nielsen-stable poles give compatible relaxation scales.
- [ ] Independent reviewer signs the ledger.
- [ ] Production resources and retention are approved.

A failed hard gate blocks production. More GPUs are not a remedy for a broken identity.
