# Theoretical Physics Programme — TP-00 through TP-16

**Author:** Angus Muffatti  
**Programme status:** ACTIVE  
**Canonical repository root:** `theoretical-physics-program/`

## Purpose

This directory contains the complete numbered theoretical-physics research programme. TP-00 supplies the frozen GR + Standard Model baseline and independent fatal gates. Every later project is self-contained but imports those gates.

\[
\boxed{
\text{one programme root}
+
\text{one auditable subproject per investigation}
+
\text{one shared commit history}.
}
\]

## Programme index

| ID | Project | Status | Current decisive result |
|---|---|---|---|
| TP-00 | [`tp-00-gr-sm-frontier-model/`](tp-00-gr-sm-frontier-model/) | Frozen | 18 seams and 29 independent successor gates. |
| TP-01 | [`tp-01-common-geometric-parent/`](tp-01-common-geometric-parent/) | Frozen v1.1 | Exact relative Chern–Weil genealogy; regular spectrum-preserving pure-connection reduction fails. |
| TP-02 | [`tp-02-geometric-unity-reconstruction/`](tp-02-geometric-unity-reconstruction/) | Frozen v0.6 | Source and repaired full-\(Y\) branches fail; surviving pullback has no intrinsic dynamics. |
| TP-03 | [`tp-03-pati-salam-benchmark/`](tp-03-pati-salam-benchmark/) | **Active v0.1** | Matter embedding and anomalies pass; one-bidoublet branch fails; \((15,2,2)\) repair advances to scalar-vacuum audit. |
| TP-04 | [`tp-04-quark-lepton-rotations/`](tp-04-quark-lepton-rotations/) | Queued | Broken generators, effective operators and matter-stability bounds. |
| TP-05 | [`tp-05-neutral-charged-conversion/`](tp-05-neutral-charged-conversion/) | Queued | Standard Model ceiling and minimal enhanced-conversion model. |
| TP-06 | [`tp-06-dark-chemistry/`](tp-06-dark-chemistry/) | Queued | Hidden bound states, cooling, structure and observables. |
| TP-07 | [`tp-07-dark-light/`](tp-07-dark-light/) | Queued | Falsifiable definition and distinction from dark photons/radiation. |
| TP-08 | [`tp-08-extra-chiral-families/`](tp-08-extra-chiral-families/) | Queued | Classification and viability of two extra chiral families. |
| TP-09 | [`tp-09-spin-3-2-matter/`](tp-09-spin-3-2-matter/) | Queued | Consistent interacting spin-\(3/2\) matter or obstruction. |
| TP-10 | [`tp-10-dynamical-dark-energy/`](tp-10-dynamical-dark-energy/) | Queued | Bianchi/Lovelock-consistent evolving dark energy. |
| TP-11 | [`tp-11-singularity-resolution/`](tp-11-singularity-resolution/) | Queued | Nonsingular construction with stability and GR recovery. |
| TP-12 | [`tp-12-pre-manifold-spacetime/`](tp-12-pre-manifold-spacetime/) | Queued | Lorentzian continuum reconstruction from non-manifold primitives. |
| TP-13 | [`tp-13-multiple-time-dimensions/`](tp-13-multiple-time-dimensions/) | Queued | Multi-time consistency and one physical time. |
| TP-14 | [`tp-14-pinch-to-zoom/`](tp-14-pinch-to-zoom/) | Queued | Invariant distance-changing dynamics or no-go theorem. |
| TP-15 | [`tp-15-shear-to-tilt/`](tp-15-shear-to-tilt/) | Queued | Covariant shear/tilt conversion. |
| TP-16 | [`tp-16-gravity-shielding/`](tp-16-gravity-shielding/) | Queued | GR obstruction and minimal consistent evasion. |

## Current execution order

1. Complete TP-03's renormalisable scalar potential, vacuum and threshold spectrum.
2. Run the RG-improved fermion/neutrino fit and laboratory constraints.
3. Feed TP-03's concrete heavy gauge/scalar spectrum into TP-04.
4. Freeze each branch immediately on an applicable fatal zero.

## Project structure

Each active child project should contain source, code, machine-readable results, acceptance matrices and reproduction instructions. Generated artifacts must be rebuildable; missing sources are never silently fabricated.

## Separate programme

[`../chronometric-emergence/`](../chronometric-emergence/) remains independent because it has its own multi-stage architecture.
