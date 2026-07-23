# Provenance audit

**Date:** 24 July 2026 (revised same day: third-party work is *attributed and built upon*,
not removed).
**Purpose:** record exactly which results in this repository originate from the repository
owner's own research sessions and which originate elsewhere, so that third-party work is
always credited and never accidentally claimed as the owner's. Full citations live in
[`ATTRIBUTIONS.md`](ATTRIBUTIONS.md).

Both underlying AI research conversations began as a **shared conversation created by
Dmitry Rybin** (see attribution 1). The repository owner's participation starts at the
message *"Very cool see you can do it. Ok let's find adjacent unsolved conjectures to
break"* (23 July 2026, 10:47). One later message pasted Levent Alpöge's publicly announced
Jacobian counterexample map (attribution 2) as a prompt.

## 1. Third-party foundations — attribute, don't claim

### 1a. The seven-vertex DGG / Goemans cost-conjecture counterexample — **Dmitry Rybin (with GPT-5.6 Pro)**

- The 7-vertex, 9-arc planar instance (fractional cost 58 vs unsplittable cost 60) and its
  exhaustive certificate were produced in Rybin's portion of the conversation
  (21–22 July 2026), announced at
  <https://x.com/DmitryRybin1/status/2079904005652893709>.
- Direct developments of that instance in this repository — the Morell–Skutella
  cost-and-two-sided and convex-decomposition refutations, the positive-cost variant, the
  parametric family, and the planar 9/8 lower bound — build on Rybin's instance and must
  cite it.
- Where it appears:
  - `2026-dgg-and-chairman-counterexamples/paper/main.tex` Sections 3–4 (see the in-paper
    attribution note) plus `code/verify_dgg.py`, `code/search_dgg_family.py`,
    `data/dgg_*.json`, `figures/dgg_network.*`, `research/derivation_dgg.md`;
  - `2026-rounding-counterexamples/papers/dgg-counterexample.tex`, the DGG half of
    `papers/overview.tex`, and the corresponding `code/`, `data/`, `figures/`,
    `research/` entries.

### 1b. The three-dimensional Jacobian-counterexample map — **Levent Alpöge / Akhil Mathew / Claude Fable 5**

- The starting map (det −2, three-point collision) was announced at
  <https://x.com/__alpoge__/status/2079028340955197566> and pasted into the conversation
  as a prompt. The owner claims no part of the map.
- The in-conversation analyses of the map (fiber stratification / nonproper locus, the
  gradient-Jacobian, polynomial-symplectic, and Weyl-algebra lifts) are derivative of the
  map and were disclaimed by the owner; treat them as exploratory notes requiring both
  attribution and independent verification before any use.
- Where it appears: the starting map and normalization `G` in
  `subtree-shuffling-counterexample/` (`PROVENANCE.md`, `derivation/01-…`,
  `src/…/maps.py`, and the manuscript's normalized-Keller-map section).

## 2. The owner's session results (AI-assisted, still requiring independent verification)

- **Machine-dependent weighted-chairman counterexample** (Liu–Reis Conjectures 19 and 21):
  the 11×15 detector/accumulator instance with weights {1/1000, 1/2, 1} and discrepancy
  ≥ 619/600. Constructed 23 July 2026 in the owner's portion. Standalone manuscript:
  `2026-rounding-counterexamples/papers/chairman-counterexample.tex`. Methodologically
  inspired by 1a but shares none of its content — cite Rybin for inspiration/context.
- **Subtree-shuffling fixed-parameter certificate** ((d,p) = (7,15), integer left-kernel
  vector with nonzero sum): constructed in the owner's portion, building directly on 1b.
  The weighted Horner suspension, inverse-coefficient calculation, and tree separator are
  the owner's-session contributions; the starting map must be attributed to
  Alpöge–Mathew–Fable in every write-up.
- The search logs, audits, figures, CI, and verification code for the two items above.

## 3. Publication guidance

- The combined manuscript `2026-dgg-and-chairman-counterexamples/paper/main.tex` may be
  used **only with Sections 3–4 explicitly attributed to Rybin** (the in-paper note does
  this); alternatively submit the standalone chairman manuscript, which is entirely from
  the owner's session.
- The subtree-shuffling manuscript already dates the "three-dimensional Keller
  announcement" (20 July 2026) in its timeline; ensure the final version cites Alpöge's
  announcement explicitly, not just by date.
- Conversation transcripts are kept out of the public repository (gitignored); the
  attribution links above are the citable public record.

## 4. What remains the owner's responsibility

- Independent mathematical verification of the chairman and subtree-shuffling results
  before any announcement (all claims here are AI-generated; the conversation record shows
  the DGG result emerged only after repeated insistence following three explicit
  "no counterexample found" reports — Rybin's result now has public scrutiny, but the
  owner's two results have none yet).
- Priority and novelty checks immediately before submission.
