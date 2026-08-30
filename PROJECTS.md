# Project registry

**Repository:** `terrorproforma/maths`  
**Maintainer and principal author:** Angus Muffatti

This file records the canonical project structure. The repository README remains the live top-level index; this registry defines where new work belongs.

## Canonical research roots

### Mathematics

- [`chairman-counterexample/`](chairman-counterexample/) — machine-dependent weighted-chairman counterexample and strengthened lower bounds.
- [`detector-chains/`](detector-chains/) — detector-chain lower bounds for machine-dependent chairman assignment.
- [`subtree-shuffling-counterexample/`](subtree-shuffling-counterexample/) — fixed-parameter obstruction to the subtree-shuffling conjecture.
- [`planar-cost-lower-bound/`](planar-cost-lower-bound/) — planar cost-preserving unsplittable-flow lower bound and corollaries.
- [`ananke-necessity-transformations/`](ananke-necessity-transformations/) — transformations/necessity research programme.

### Physics

- [`chronometric-emergence/`](chronometric-emergence/) — chronometric shear, scale locking, QCD thresholds, cosmology and nonequilibrium transport. Self-contained stages live under `chronometric-emergence/projects/`; the current adversarial evidence layer is `chronometric-emergence/frontier-evidence-v2/`.
- [`theoretical-physics-program/`](theoretical-physics-program/) — the TP-00 through TP-16 programme. Each TP project has its own self-contained directory inside the programme root so the dependency graph remains coherent without scattering one programme across the repository root.

## Archived combined packages

- [`2026-rounding-counterexamples/`](2026-rounding-counterexamples/) and [`2026-dgg-and-chairman-counterexamples/`](2026-dgg-and-chairman-counterexamples/) are retained for provenance and are superseded by the per-result folders.
- [`_bootstrap/`](_bootstrap/) is migration staging only and is not a canonical location for new work.

## Rule for new work

A genuinely independent project receives its own stable project directory. A stage that is intrinsically part of an existing programme receives its own self-contained subdirectory inside that programme root. In either case, source, code, data, results, provenance and status must be committed to GitHub before the work is considered durably stored.
