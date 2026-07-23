# Provenance audit

**Date:** 24 July 2026.
**Purpose:** record exactly which results in this repository originate from the repository
owner's own research sessions and which originate elsewhere, so that no third-party work is
ever claimed, submitted, or announced as the owner's.

Both underlying AI research conversations began as a **shared conversation created by another
person**. The repository owner's participation starts at the message
*"Very cool see you can do it. Ok let's find adjacent unsolved conjectures to break"*
(23 July 2026, 10:47). Everything before that point is third-party work. In addition, one
later message pasted an externally announced construction (see item 2).

## 1. NOT the owner's work — excluded from any claimed contribution

### 1a. The seven-vertex DGG / Goemans cost-conjecture counterexample

- The 7-vertex, 9-arc planar instance (fractional cost 58 vs unsplittable cost 60), the
  triangle stable-set obstruction, and the positive-cost variant (409 vs 415) were all
  produced **before** the owner joined the conversation (21–22 July 2026).
- Direct downstream corollaries that reuse that instance are likewise excluded:
  - the Morell–Skutella cost-and-two-sided-bounds refutation (Corollary in the papers);
  - the Morell–Skutella convex-decomposition refutation;
  - the parametric family and the planar 9/8 lower bound (the family is the same gadget).
- Affected files:
  - `2026-dgg-and-chairman-counterexamples/paper/main.tex` — Sections 3–5 and the parts of
    the abstract/intro/conclusion describing the flow result (see the in-paper provenance
    note added by this audit);
  - `2026-dgg-and-chairman-counterexamples/{code/verify_dgg.py, code/search_dgg_family.py,
    data/dgg_instance.json, data/dgg_positive_costs.json, figures/dgg_network.*,
    research/derivation_dgg.md}`;
  - `2026-rounding-counterexamples/papers/dgg-counterexample.tex`, `papers/overview.tex`
    (its DGG half), and the corresponding `code/`, `data/`, `figures/`, `research/` entries.

### 1b. The three-dimensional Jacobian-conjecture counterexample map

- The map `((1+xy)^3 z + y^2(1+xy)(4+3xy), y + 3x(1+xy)^2 z + 3xy^2(4+3xy),
  2x - 3x^2y - x^3z)` with Jacobian determinant −2 and the three-point collision was
  **pasted into the conversation from an external announcement** (public record dated
  20 July 2026; the conversation's own research attributes the announcement to Levent
  Alpöge, with an AI system credited for producing the example). The owner supplied it
  only as a prompt and claims **no part** of the map, its verification, or its analysis.
- Also excluded: the fiber-stratification/nonproper-locus analysis of that map and the
  "formula-level lifts" (gradient/symmetric Jacobian in dimension 6, polynomial symplectic
  non-automorphism, Dixmier for the third Weyl algebra) — these were derived in-session
  directly from the pasted map and inherit its provenance; the owner has disclaimed the
  Jacobian-breaking message as not their work.
- Affected files: the *starting map* and normalization `G` recorded in
  `subtree-shuffling-counterexample/` (`PROVENANCE.md`, `derivation/01-…`, `src/…/maps.py`,
  and the manuscript's Section on the normalized Keller map).

## 2. From the owner's sessions (AI-assisted, still requiring independent verification)

- **Machine-dependent weighted-chairman counterexample** (Liu–Reis Conjectures 19 and 21):
  the 11×15 detector/accumulator instance with weights {1/1000, 1/2, 1} and discrepancy
  ≥ 619/600. Constructed 23 July 2026 in the owner's portion of the conversation.
  Standalone manuscript: `2026-rounding-counterexamples/papers/chairman-counterexample.tex`.
- **Subtree-shuffling fixed-parameter certificate** ((d,p) = (7,15), integer left-kernel
  vector with nonzero sum): constructed in the owner's portion. **Caveat:** the
  construction *starts from* the third-party map in 1b; any write-up must attribute the
  starting map and must not present the map, its normalization, or the fiber analysis as
  original. The weighted Horner suspension, the inverse-coefficient calculation, and the
  tree separator are the parts that arose in the owner's session.
- The generic "obstruction engine" methodology write-ups, search logs, audits, figures, CI,
  and verification code for the two items above.

## 3. Actions taken by this audit

1. Merged `agent/rounding-counterexample-papers` (PR #1 content) into `main` so the
   standalone per-result manuscripts are available: the chairman-only paper is the correct
   submission vehicle for the owner's flow-adjacent work; the DGG-only paper is retained
   solely as a record of third-party-derived material.
2. Added a provenance note to `2026-dgg-and-chairman-counterexamples/paper/main.tex`
   stating that the flow counterexample is not the submitting author's contribution; the
   combined paper must not be submitted as-is under the owner's name.
3. Updated the README and AI_DISCLOSURE in `2026-dgg-and-chairman-counterexamples/`, the
   README in `2026-rounding-counterexamples/`, and `subtree-shuffling-counterexample/
   PROVENANCE.md` with the same boundaries.
4. Added `CONJECTURE_TARGETS.md` listing every target discussed in both conversations,
   labelled by provenance.

## 4. What remains the owner's responsibility

- Independent mathematical verification of the chairman and subtree-shuffling results
  before any announcement (both are AI-generated claims; the conversations show the DGG
  "result" appeared only after repeated insistence following three explicit
  "no counterexample found" reports, so skepticism is warranted everywhere).
- Priority checks immediately before submission.
- Deciding whether third-party-derived folders should remain in a public repository at all.
