# ANANKE v2 — Certified Core Summary

ANANKE v2 upgrades the v1 finite-shot pipeline into a theorem-and-algorithm package
with zero new runtime dependencies (pure Python standard library + NumPy).

## Modules Added (`src/ananke/`)

- [`interval.py`](../src/ananke/interval.py): self-contained outward-rounded `Decimal`
  interval arithmetic (`ROUND_FLOOR`/`ROUND_CEILING`, verified outward `sqrt`, Machin
  $\pi$, certified Taylor `sin`/`cos`/`atan`/`atan2`).
- [`karpelevich_certified.py`](../src/ananke/karpelevich_certified.py): interval-certified
  Karpelevič radius and global branch-and-bound Euclidean distance over all Farey arcs
  via the reduced positive-trinomial zero-cancellation gap equation (Theorem 1).
- [`certified_inference.py`](../src/ananke/certified_inference.py): non-asymptotic
  Hankel Matrix Hoeffding (Theorem 2), unconditional Weyl rank lower bound, exact
  similarity elimination & Schur-complement block isolation (Theorem 3), and two-stage
  Hypergeometric split-sample scalar+projected certification.
- [`diophantine_design.py`](../src/ananke/diophantine_design.py): Karpelevič Markov
  spectrum evaluator (Theorem 4), asymptotic radial gap scaling, finite-horizon sector
  optimization, and joint Hankel/Karpelevič gate design metrics.

## Experiments, Results, Tests, and Proofs

- Full proofs and epistemic audit: [`docs/ananke_v2_certified_core.md`](../docs/ananke_v2_certified_core.md)
- Reproducible experiments:
  - [`experiments/certify_baseline_v2.py`](../experiments/certify_baseline_v2.py) $\to$ [`results/certify_baseline_v2.json`](../results/certify_baseline_v2.json)
  - [`experiments/diophantine_design_v2.py`](../experiments/diophantine_design_v2.py) $\to$ [`results/diophantine_design_v2.json`](../results/diophantine_design_v2.json)
- Automated test suites (20 new v2 tests + 18 existing v0/v1 tests = 38 tests):
  - `tests/test_interval_v2.py`
  - `tests/test_karpelevich_certified_v2.py`
  - `tests/test_certified_inference_v2.py`
  - `tests/test_diophantine_design_v2.py`
