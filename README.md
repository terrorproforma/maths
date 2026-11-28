# math-and-physics

Research notes, computational certificates, reproducible manuscripts, and ongoing work in mathematics and theoretical physics.

**Author: Angus Muffatti**

Maintained by **Angus Muffatti**. All results are AI-assisted and carry explicit disclosures; all claims are unverified until independently audited.

> **Provenance.** This repository builds on attributed third-party work: the DGG/Goemans flow counterexample is due to **Dmitry Rybin** (with GPT-5.6 Pro), and the Jacobian-conjecture starting map is due to **Levent Alpöge, Akhil Mathew, and Claude Fable 5**. See [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md) for citations and [`PROVENANCE_AUDIT.md`](PROVENANCE_AUDIT.md) for the exact boundary between that work and this repository's own results.

## Mathematics

- [`chairman-counterexample/`](chairman-counterexample/) — **counterexample to the machine-dependent weighted-chairman conjectures** (Liu–Reis Conjectures 19 and 21), plus a quantitative strengthening: prefix discrepancy can be forced arbitrarily close to 7/6·D for the ½-split gadget (concrete 49×72 instance > 9/8), improved to (4−2√2)·D − ε ≈ 1.1716·D by freeing the detector split (exact witness 239/204). Six independent verifiers (exact-rational and MILP). Author: Angus Muffatti.
- [`detector-chains/`](detector-chains/) — **detector chains, $m^* = 3$, and the $1 + \ln 2$ completeness barrier**: begins with the Lambert-W lower bound $\kappa \ge 1 + W(1/e) \approx 1.2785$ (depth-40 certificate 1.272743) and extends in [`frontier_next/`](detector-chains/frontier_next/) and [`frontier_v2/`](detector-chains/frontier_v2/) to settle **$m^* = 3$** ($\kappa_3 \ge 1.101721$, ultra-compact $3 \times 33$ counterexample), prove the even-$m$ ladder ($\kappa_4 \ge 1.26625$, $\kappa_8 \ge 1.41220$), lift the global lower bound to **$\kappa \ge 1 + \ln 2 \approx 1.693147$**, establish an exact $1 + \ln 2$ completeness barrier for disjoint-subtree splitting, and compile the unified manuscript [`frontier_v2/paper/chairman_frontier_2026.pdf`](detector-chains/frontier_v2/paper/chairman_frontier_2026.pdf). Author: Angus Muffatti.
- [`chairman-small-rows/`](chairman-small-rows/) — **machine-dependent chairman assignment with two rows: κ₂ = 1** (working notes). The Liu–Reis bound `D` is proved for two machines, with a linear-time algorithm, and an explicit two-row family with min-max prefix discrepancy exactly 1 − 2^−(k+1) shows that it is optimal; the online problem is unbounded already for two rows. Exact standard-library verifiers. Author: Angus Muffatti.
- [`ananke-necessity-transformations/`](ananke-necessity-transformations/) — **ANANKE (v0–v3): certified classical counterfeit complexity**: operational Hankel extraction, outward-rounded interval-certified Karpelevič separation ($N_{\mathrm{cl}} \ge 16$), the **Karpelevič Markov Theorem** ($\kappa_\Theta(\alpha_*) = \frac{2\pi^2\varphi^3}{5\sqrt{5}} > \frac{3\pi^2}{4}$), non-asymptotic Matrix Hoeffding / Schur-complement certificates, and **rank-unrestricted B-spline Cayley–Hamilton + subharmonic dual certificates** paired with constructive classical counterfeits; compiled manuscript [`paper/ananke_certified_counterfeit_complexity.pdf`](ananke-necessity-transformations/paper/ananke_certified_counterfeit_complexity.pdf) (56 unit tests). Author: Angus Muffatti.
- [`subtree-shuffling-counterexample/`](subtree-shuffling-counterexample/) — **explicit fixed-parameter obstruction to the subtree-shuffling conjecture** at (d,p) = (7,15) for all k = 3m, via a weighted Horner suspension of the Alpöge map (attributed) and an exact Lagrange-inversion certificate. Author: Angus Muffatti.
- [`planar-cost-lower-bound/`](planar-cost-lower-bound/) — **corollaries of Rybin's counterexample** (Morell–Skutella convex-decomposition failure) **and the planar 9/8 lower bound** for cost-preserving unsplittable flow, giving α_planar ∈ [9/8, 2]. Base instance due to Rybin (attributed). Author of the note: Angus Muffatti.

## Physics

- [`theoretical-physics-program/`](theoretical-physics-program/) — the complete numbered TP-00 through TP-16 programme under one root directory. TP-00 is the frozen acceptance framework, TP-01 is frozen at its common-parent/no-go result, TP-02 is frozen at its observation-pullback obstruction, and TP-03 (Pati–Salam benchmark) is active with Phase 2B complete (`PS1-MM` certified vacuum).
- [`chronometric-emergence/`](chronometric-emergence/) — independent programme on null/conformal structure, universal spectral clock factorisation, QCD scale locking, cyclic protection, cosmological state selection, and nonequilibrium transport. Its [`projects/`](chronometric-emergence/projects/) directory contains one self-contained folder per research stage (including [`scale-conformal-chronometry-bridge/`](chronometric-emergence/projects/scale-conformal-chronometry-bridge/)); [`frontier-evidence-v2/`](chronometric-emergence/frontier-evidence-v2/) records the canonical current audit; and [`original-info/`](chronometric-emergence/original-info/) preserves the recovered original packages and binary artefacts.
- [`bns-prompt-collapse-jet-replication/`](bns-prompt-collapse-jet-replication/) — reduced-order visual surrogate and full-fidelity GRMHD replication specification/harness (X-track & E-track) for Hayashi et al. (PRL 134, 211407, 2025).

## Archived combined packages

- [`2026-rounding-counterexamples/`](2026-rounding-counterexamples/) and [`2026-dgg-and-chairman-counterexamples/`](2026-dgg-and-chairman-counterexamples/) — earlier combined packages bundling Rybin's DGG counterexample with the chairman result. Superseded by the per-result folders above; retained for the record with attribution notes intact.

Every active result folder carries its own README, verification instructions, data, and manuscript source where applicable.
