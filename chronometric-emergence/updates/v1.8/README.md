# Pre-HPC Closure of the Gauge-Covariant q-D-H Portal — v1.8

**Author: Angus Muffatti**  
**Date: 23 August 2026**  
**Status: Launch-ready reduced pilot specification; not peer reviewed**

## Executive result

The pre-HPC programme is complete as a declared, executable truncation. The HPC target is

\[
\boxed{
\text{PT/BFM-constrained three-loop 3PI}
+
\text{explicit Ward/ST/Nielsen diagnostics}
+
\text{a conserving }H^\dagger H\text{ control ladder}
}
\]

It is not a naive finite 3PI calculation whose gauge consistency is assumed.

The update closes the reduced analytic and numerical work required before a serious non-Abelian real-time run:

1. a pointwise Born/LPM/hard/HTL/overlap retarded benchmark;
2. factorisation-scale regression tests;
3. exact longitudinal background-Ward and declared Slavnov-Taylor closure;
4. finite transverse form factors from a separable Bethe-Salpeter seed;
5. a conserving gauge-singlet \(H^\dagger H\) ladder;
6. machine-readable grids, resource tiers, checkpoint rules and hard failure gates.

## Key results

| Diagnostic | Result |
|---|---:|
| Pointwise grid | \(36\times1601\) |
| Relevant \(q_*\)-spread | \(5.60\times10^{-16}\) |
| On-shell interpolation residual | \(3.20\times10^{-16}\) |
| Oddness residual | \(8.88\times10^{-16}\) |
| KMS-noise minimum | \(2.90\times10^{-4}\) |
| Transverse contraction residual | \(1.57\times10^{-16}\) |
| STI residual | \(1.71\times10^{-15}\) |
| Singlet BSE residual | \(2.53\times10^{-16}\) |
| Preflight checks | 6/6 pass |
| Unit tests | 4/4 pass |

## Resource tiers

| Tier | Radial points | \(\ell_{\max}\) | Momentum cells | Time steps | Memory window | GPUs | Estimated aggregate memory |
|---|---:|---:|---:|---:|---:|---:|---:|
| Unit test | 32 | 1 | 128 | 512 | 64 | 1 | 0.11 GB |
| Pilot | 96 | 4 | 2,400 | 4,096 | 256 | 8 | 6.49 GB |
| Production | 192 | 6 | 9,408 | 16,384 | 512 | 128 | 43.9 GB |

## Mandatory pilot gates

The pilot is rejected if any of the following fail: on-shell width \(10^{-3}\), factorisation spread \(10^{-5}\), background Ward residual \(10^{-8}\), quantum STI residual \(10^{-6}\), Nielsen pole spread \(10^{-6}\), KMS residual \(10^{-7}\), equal-time commutator error \(10^{-7}\), energy drift \(10^{-6}\), gauge-charge drift \(10^{-7}\), negative singlet spectral tolerance \(10^{-10}\), singlet BSE residual \(10^{-8}\), memory-window convergence \(5\times10^{-3}\), and gauge-parameter variation of physical observables \(10^{-3}\).

## Remaining work inside HPC

The simulation must evolve unequal-time propagators and three-point vertices, replace scalar matter-ghost initialization with matrix-valued kernels, evaluate the complete differential real/virtual/HTL/LPM contributions, evolve the chosen transverse basis, generate the singlet ladder from the same truncation, and run convergence and gauge scans. No further hand-built off-shell ansatz is an honest substitute for this pilot.
