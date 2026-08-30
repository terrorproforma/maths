# Analytic and Reduced-Numerical Benchmark Hierarchy - v1.9

**Author:** Angus Muffatti  
**Status:** Frozen regression hierarchy  
**Date:** 24 August 2026

## Purpose

The pilot is not trusted merely because it runs. Each limit isolates a different part of the equations, discretization or matching. A failed identity or conservation law stops the run; it is not absorbed into an uncertainty bar.

## Hierarchy

| Limit | Required result | Current pre-HPC status |
|---|---|---|
| Free unequal-time scalar | \(\rho(t,t)=0\), \(\partial_t\rho|_{t=t'}=1\) | PASS |
| Equilibrium KMS | Fluctuation-dissipation | PASS |
| Abelian Ward limit | \(Q_\mu\Gamma^\mu=S^{-1}(P+Q)-S^{-1}(P)\) | PASS |
| Pure Yukawa limit | Recover scalar-fermion portal kinetics | Registered pilot regression |
| Linear response | Reproduce hard+LPM portal anchor | PASS from v1.8 input |
| Kinetic/AMY limit | Approach explicit collision result | Registered pilot regression |
| Narrow width | Normalized delta sequence | PASS |
| Factorization scale | Matched kernel independent of \(q_*\) | PASS from v1.8 input |
| Singlet BSE | Conserving positive \(H^\dagger H\) ladder | PASS from v1.8 input |

## Current analytic metrics

| Metric | Value | Gate |
| --- | --- | --- |
| Equal-time spectral value | 0.000e+00 | < 1e-14 |
| Equal-time derivative error | 8.817e-13 | < 1e-9 |
| KMS residual | 1.474e-16 | < 1e-12 |
| Abelian Ward residual | 4.487e-16 | < 1e-12 |
| Finite-memory/Markov error | 7.919e-04 | < 1e-2 |
| Narrow-width area error | 7.639e-03 | < 1e-2 |
| Narrow-width peak error | 0.000e+00 | < 1e-12 |

## Required scans

- radial momentum: 64, 96, 144;
- \(\ell_{\max}=2,4,6\);
- \(T\Delta t=0.04,0.02,0.01\);
- memory: 128, 256, 384, 512;
- \(\xi=0,0.5,1,2\);
- \(q_*/T=0.15,0.25,0.40\);
- \(\mu/T=\pi,2\pi,4\pi\);
- minimal-seed versus full-component vertices;
- full 3PI, no-transverse-seed and bare-vertex 2PI controls.

## Stop policy

Ward/STI, Nielsen, conservation, KMS, commutator, singlet positivity, \(q_*\)-cancellation, cyclic-symmetry or convergence failures stop the claim-bearing run. Diagnostic continuation is allowed, but no physical result may be extracted.
