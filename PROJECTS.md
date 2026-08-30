# Project registry

**Repository:** `terrorproforma/maths`  
**Maintainer and principal author:** Angus Muffatti  
**Last structural audit:** 30 August 2026

This is the canonical index of self-contained projects in the repository. Each active project has one root-level directory. Iterations, working papers, data, code, figures and generated results stay inside that project directory rather than becoming loose repository-root files.

## Canonical active projects

| Folder | Project | Current status |
|---|---|---|
| [`chairman-counterexample/`](chairman-counterexample/) | Machine-dependent weighted-chairman counterexample and strengthened lower-bound family | Active research package; exact certificate and independent verifiers |
| [`detector-chains/`](detector-chains/) | Detector-chain lower bounds for machine-dependent chairman assignment | Working draft with exact certificates |
| [`subtree-shuffling-counterexample/`](subtree-shuffling-counterexample/) | Fixed-parameter obstruction to the subtree-shuffling conjecture | Active research package |
| [`planar-cost-lower-bound/`](planar-cost-lower-bound/) | Planar cost-preserving unsplittable-flow lower bound and corollaries | Active note built on attributed third-party base instance |
| [`chronometric-emergence/`](chronometric-emergence/) | Chronometric shear, scale locking, QCD thresholds, cosmology and nonequilibrium transport | Ongoing; historical archive plus active adversarial evidence layer |
| [`tp-00-gr-sm-frontier-model/`](tp-00-gr-sm-frontier-model/) | GR + Standard Model constraint and seam ledger | Complete baseline/audit framework; not a successor theory |
| [`tp-01-common-geometric-parent/`](tp-01-common-geometric-parent/) | Common geometric parent for Einstein-Hilbert and Chern-Simons/transgression actions | Completed candidate with a negative successor-theory verdict under TP-00 gates |
| [`tp-02-geometric-unity-reconstruction/`](tp-02-geometric-unity-reconstruction/) | Primary-source reconstruction and acceptance-gate audit of Geometric Unity | Current public draft; not yet an experimentally adequate successor theory |

## Archived combined packages

| Folder | Status |
|---|---|
| [`2026-rounding-counterexamples/`](2026-rounding-counterexamples/) | Archived combined package, superseded by the per-result folders |
| [`2026-dgg-and-chairman-counterexamples/`](2026-dgg-and-chairman-counterexamples/) | Archived combined package, superseded by the per-result folders |

## Migration-only material

[`_bootstrap/`](_bootstrap/) is migration staging retained for recovery provenance. It is **not** a canonical project location and must not be used for new work.

## Repository rules

The binding storage and provenance rules are in [`REPOSITORY_STORAGE_POLICY.md`](REPOSITORY_STORAGE_POLICY.md). In particular:

1. every new self-contained project receives one new root-level, kebab-case directory;
2. chat or sandbox files are ingress material only and must be committed before they are treated as durable work;
3. historical iterations remain versioned inside the relevant project;
4. errors are corrected through explicit errata or superseding versions rather than silently rewriting the research record;
5. third-party contributions retain explicit attribution.
