# Pre-HPC launch checklist v1.8

## Required inputs

- [x] Pointwise retarded benchmark table
- [x] Independent on-shell hard+LPM anchor
- [x] Hard/HTL/overlap factorization-scale regression
- [x] Longitudinal background-Ward vertex
- [x] Declared quantum-STI initialization
- [x] Finite transverse form-factor initialization
- [x] Ghost dressing and matter-ghost-kernel initialization
- [x] Gauge-singlet H-dagger-H conserving ladder
- [x] KMS/noise table
- [x] Initial-surface counterterm classes
- [x] Resource and decomposition model
- [x] Automated preflight and unit tests

## Pilot launch gates

- [ ] Reproduce v1.6 integrated portal rate within 0.1%
- [ ] Reproduce pointwise on-shell widths within 0.1%
- [ ] Factorization-scale spread below 1e-5
- [ ] Background Ward residual below 1e-8
- [ ] Quantum STI residual below 1e-6
- [ ] Nielsen pole spread below 1e-6
- [ ] KMS residual below 1e-7
- [ ] Equal-time commutator error below 1e-7
- [ ] Energy drift below 1e-6
- [ ] Gauge-charge drift below 1e-7
- [ ] H-dagger-H spectral density above -1e-10
- [ ] H-dagger-H BSE residual below 1e-8
- [ ] Memory-window convergence below 0.5%
- [ ] Physical-observable gauge scan below 0.1%

## Stop conditions

Stop the run rather than “tuning through” any of the following:

- physical poles move materially with gauge parameter;
- the singlet spectrum becomes negative beyond tolerance;
- Ward/ST residuals improve only by violating KMS or conservation;
- q-star dependence does not converge with resolution;
- memory-window enlargement changes observables above threshold;
- a bare-vertex substitution is required to stabilize a dressed propagator.
