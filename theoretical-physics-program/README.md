# Theoretical Physics Programme — TP-00 through TP-16

**Author:** Angus Muffatti  
**Programme status:** ACTIVE  
**Canonical repository root:** `theoretical-physics-program/`

## Purpose

This directory contains the complete numbered TP research programme derived from the theoretical-
physics concepts extracted from the source transcript. The projects share one governing programme
but remain individually executable and auditable.

\[
\boxed{
\text{one programme root}
+
\text{one self-contained subdirectory per investigation}
+
\text{one commit history for all progress}.
}
\]

TP-00 supplies the frozen baseline, seam ledger and acceptance gates. Every later project imports
those gates. Fatal failures remain independent and cannot be averaged against attractive results.

## Programme index

| ID | Project | Status | Current role or decisive result |
|---|---|---|---|
| TP-00 | [`tp-00-gr-sm-frontier-model/`](tp-00-gr-sm-frontier-model/) | Frozen baseline | GR + SM constraint, seam and recovery ledger; 18 seams and 29 independent gates. |
| TP-01 | [`tp-01-common-geometric-parent/`](tp-01-common-geometric-parent/) | Frozen at v1.1 | Exact relative Chern–Weil genealogy survives; regular spectrum-preserving dynamical reduction fails in the declared pure-connection class. |
| TP-02 | [`tp-02-geometric-unity-reconstruction/`](tp-02-geometric-unity-reconstruction/) | Frozen at v0.6 | Literal covariance and full-\((7,7)\) propagation fail; the repaired Einstein contraction survives algebraically, but pullback alone does not close four-dimensional dynamics. |
| TP-03 | [`tp-03-pati-salam-benchmark/`](tp-03-pati-salam-benchmark/) | Active, Phase 2B complete | `PS0` fails its Yukawa relations; complex gauge-only `PS1` has 138 invariant channels; `PS1-MM` has a certified global high-scale vacuum with an explicit 188x188 Hessian, 9 Goldstones and no physical scalar tachyon. |
| TP-04 | [`tp-04-quark-lepton-rotations/`](tp-04-quark-lepton-rotations/) | Queued | Broken generators, effective operators and matter-stability bounds. |
| TP-05 | [`tp-05-neutral-charged-conversion/`](tp-05-neutral-charged-conversion/) | Queued | Standard Model ceiling and minimal consistent enhanced conversion model. |
| TP-06 | [`tp-06-dark-chemistry/`](tp-06-dark-chemistry/) | Queued | Hidden-sector bound states, cooling, structure and observables. |
| TP-07 | [`tp-07-dark-light/`](tp-07-dark-light/) | Queued | Falsifiable definition and differentiation from ordinary dark photons/radiation. |
| TP-08 | [`tp-08-extra-chiral-families/`](tp-08-extra-chiral-families/) | Queued | Classification and viability of two additional chiral families. |
| TP-09 | [`tp-09-spin-3-2-matter/`](tp-09-spin-3-2-matter/) | Queued | Consistent interacting spin-\(3/2\) matter or sharp obstruction. |
| TP-10 | [`tp-10-dynamical-dark-energy/`](tp-10-dynamical-dark-energy/) | Queued | Bianchi/Lovelock-consistent evolving dark-energy dynamics. |
| TP-11 | [`tp-11-singularity-resolution/`](tp-11-singularity-resolution/) | Queued | Explicit nonsingular construction with stability and GR recovery. |
| TP-12 | [`tp-12-pre-manifold-spacetime/`](tp-12-pre-manifold-spacetime/) | Queued | Reconstruction of Lorentzian continuum geometry from non-manifold primitives. |
| TP-13 | [`tp-13-multiple-time-dimensions/`](tp-13-multiple-time-dimensions/) | Queued | Multi-time consistency and emergence of one physical time. |
| TP-14 | [`tp-14-pinch-to-zoom/`](tp-14-pinch-to-zoom/) | Queued | Invariant distance-changing dynamics or a restricted no-go theorem. |
| TP-15 | [`tp-15-shear-to-tilt/`](tp-15-shear-to-tilt/) | Queued | Covariant shear/tilt conversion and gauge-independence test. |
| TP-16 | [`tp-16-gravity-shielding/`](tp-16-gravity-shielding/) | Queued | Ordinary-GR obstruction and minimal consistent evasion audit. |

## Programme structure

```text
theoretical-physics-program/
├── README.md
├── tp-00-gr-sm-frontier-model/
├── tp-01-common-geometric-parent/
├── tp-02-geometric-unity-reconstruction/
├── ...
└── tp-16-gravity-shielding/
```

Each active project should contain, as applicable:

```text
README.md
PROJECT_BRIEF.md
CITATION.cff
paper/
code/
results/
sources/
acceptance_matrix.csv
manifest_sha256.csv
```

Generated PDFs and binary arrays should be reproducible from committed source. Missing source must
never be silently fabricated to satisfy a manifest.

## Current execution order

1. Continue TP-03 through `PS1-EW`: bidoublet mass mixing, one-light-Higgs matching, RG running,
   fermion/neutrino fits, flavour and baryon-stability gates.
2. Use TP-03's concrete broken-generator and scalar spectrum as input to TP-04.
3. Launch later projects only with their own named branch and imported TP-00 gates.

## Related but separate programme

The repository's [`../chronometric-emergence/`](../chronometric-emergence/) programme remains
independent because it has its own multi-stage architecture and predates this numbered TP sequence.
