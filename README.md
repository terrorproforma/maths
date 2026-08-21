# math-and-physics

Research notes, computational certificates, reproducible manuscripts, and ongoing work in mathematics and theoretical physics.

**Author: Angus Muffatti**

Maintained by **Angus Muffatti**. All results are AI-assisted and carry explicit disclosures; all claims are unverified until independently audited.

> **Provenance.** This repository builds on attributed third-party work: the DGG/Goemans flow counterexample is due to **Dmitry Rybin** (with GPT-5.6 Pro), and the Jacobian-conjecture starting map is due to **Levent Alpöge, Akhil Mathew, and Claude Fable 5**. See [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md) for citations and [`PROVENANCE_AUDIT.md`](PROVENANCE_AUDIT.md) for the exact boundary between that work and this repository's own results.

## Mathematics

- [`chairman-counterexample/`](chairman-counterexample/) — **counterexample to the machine-dependent weighted-chairman conjectures** (Liu–Reis Conjectures 19 and 21), plus a quantitative strengthening: prefix discrepancy can be forced arbitrarily close to 7/6·D for the ½-split gadget (concrete 49×72 instance > 9/8), improved to (4−2√2)·D − ε ≈ 1.1716·D by freeing the detector split (exact witness 239/204). Six independent verifiers (exact-rational and MILP). Author: Angus Muffatti.
- [`detector-chains/`](detector-chains/) — **a Lambert-W lower bound for machine-dependent chairman assignment** (working draft): deepening the companion paper's detector to a chain of length k gives the closed form τ(k) and the limit κ ≥ 1 + W(1/e) ≈ 1.2785, with exact certificates to depth 40 (deepest instance 1.272743) and exhaustive, solver-free verification of the block-game section. Author: Angus Muffatti.
- [`subtree-shuffling-counterexample/`](subtree-shuffling-counterexample/) — **explicit fixed-parameter obstruction to the subtree-shuffling conjecture** at (d,p) = (7,15) for all k = 3m, via a weighted Horner suspension of the Alpöge map (attributed) and an exact Lagrange-inversion certificate. Author: Angus Muffatti.
- [`planar-cost-lower-bound/`](planar-cost-lower-bound/) — **corollaries of Rybin's counterexample** (Morell–Skutella convex-decomposition failure) **and the planar 9/8 lower bound** for cost-preserving unsplittable flow, giving α_planar ∈ [9/8, 2]. Base instance due to Rybin (attributed). Author of the note: Angus Muffatti.

## Physics

- [`chronometric-emergence/`](chronometric-emergence/) — ongoing theoretical-physics programme on null/conformal structure, universal spectral clock factorisation, QCD scale locking, cyclic protection, cosmological state selection, and nonequilibrium transport. Author: Angus Muffatti.

## Archived combined packages

- [`2026-rounding-counterexamples/`](2026-rounding-counterexamples/) and [`2026-dgg-and-chairman-counterexamples/`](2026-dgg-and-chairman-counterexamples/) — earlier combined packages bundling Rybin's DGG counterexample with the chairman result. Superseded by the per-result folders above; retained for the record with attribution notes intact.

Every active result folder carries its own README, verification instructions, data, and manuscript source where applicable.
