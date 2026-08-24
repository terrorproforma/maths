# Gauge-Covariant Correlator Closure for the q-D-H Portal — v1.7

**Author: Angus Muffatti**  
**Date: 21 August 2026**  
**Status: Technical research note; not peer reviewed**

## Executive result

The conventional arbitrary-off-shell elementary Higgs self-energy is generally gauge-parameter dependent and is not by itself a unique physical observable. The corrected target is

\[
\boxed{
\text{PT/BFM hard-soft retarded kernel}
+
\text{Ward/ST-consistent vertex set}
+
H^\dagger H\text{ control correlator}
}
\]

The exact v1.6 on-shell portal anchor remains

\[
\frac{\overline\Gamma_{H,\mathrm{total}}^{\mathrm{occ}}}{T}
=1.1585159\times10^{-3},
\qquad
\frac{\overline\Gamma_{H,\mathrm{total}}^{\mathrm{occ}}}{\Gamma_R}
=7.8514\times10^6.
\]

The v1.7 work supplies a PT/BFM near-shell retarded grid, line-integral scalar and fermion vertices, a Nielsen pole diagnostic, and a gauge-singlet \(H^\dagger H\) control correlator. It also rejects bare-vertex 2PI as the final non-Abelian method and identifies three-loop 3PI, or an equivalent Bethe-Salpeter vertex closure, as the correct next computational architecture.

## Numerical checks

| Test | Result |
|---|---:|
| Fermion Ward residual, maximum | \(1.53\times10^{-15}\) |
| Scalar Ward residual, maximum | \(7.07\times10^{-14}\) |
| Transverse contraction residual | \(5.24\times10^{-16}\) |
| Nielsen complex-pole displacement | \(1.42\times10^{-12}\) |
| Nielsen median off-shell spread | 0.688 |
| PT/BFM shell interpolation residual | \(9.44\times10^{-4}\) |
| PT/BFM oddness residual | \(1.56\times10^{-17}\) |
| Singlet positive-frequency minimum | \(4.91\times10^{-6}\) |

## Acceptance status

- Conventional gauge-independent arbitrary-off-shell \(\Pi_H^R\): **fail as stated**.
- Exact on-shell hard-plus-LPM anchor: **pass**.
- PT/BFM near-shell retarded kernel: **pass as benchmark**.
- Longitudinal background Ward closure: **pass**.
- Full quantum Slavnov-Taylor closure: **partial**.
- Gauge-singlet \(H^\dagger H\) control: **pass as baseline**.
- Exact full-plane hard-soft matching: **open**.
- Bare-vertex 2PI as final gauge dynamics: **rejected**.
- Three-loop 3PI / Bethe-Salpeter closure: **next target**.

## Scientific boundary

The exact physical target is not an isolated off-shell Higgs self-energy. It is a PT/BFM hard-soft kernel, its Ward/ST vertex completion, and a gauge-singlet spectral control evolved self-consistently. This update prevents the project from treating an attractive gauge-dependent line shape as a physical prediction.
