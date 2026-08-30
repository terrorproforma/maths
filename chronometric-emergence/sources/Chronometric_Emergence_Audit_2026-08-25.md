**Independent review · 25 Aug 2026**

# Chronometric Emergence Audit

Errors and missed opportunities across the original research packages v0.1–v1.9 in `chronometric-emergence/original-info/`. Every load-bearing formula and benchmark quoted below was re-derived or recomputed independently; all 18 shipped verifier suites were re-run.

## Verdict

The arithmetic is remarkably healthy; the *evidence* is not. Across roughly 150 independently recomputed quantities, nearly every displayed number reproduces — including the load-bearing **2/27** QCD transmission coefficient (exact at one loop; a fresh two-loop run shifts it only +2.9%). All 18 verifier suites pass when re-run, and every recorded results file reproduces within floating-point noise. But the programme's verification layer is dominated by checks that **cannot fail** — identities tested on objects constructed to satisfy them, hardcoded PASS verdicts, and stored numbers re-asserted as gates — and the two deepest problems are a structural physics error in v1.4's LPM kernel and a v1.9 "PILOT AUTHORIZED" status with no solver behind it.

**18 / 18verifier suites re-run, pass**

**17 / 17result files reproduce**

**~150numbers recomputed by hand**

**5critical findings**

**~20moderate findings**

## Reproducibility & portability

None of the shipped verifiers runs as delivered on a normal machine: most hardcode the ChatGPT sandbox path `/mnt/data/` for outputs, and the late-chain verifiers hardcode it for *inputs* too (v1.6 imports the v1.5 script from `/mnt/data`; v1.7 and v1.8 load v1.6/v1.7 result JSONs the same way). v1.1 needs an undeclared `networkx` dependency. After staging all packages into one flat directory and patching paths, every suite ran to completion with zero failing checks.

| **Result fileReproduction**                      |                                                                                                                |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| v0.2, v0.5, v0.7, v0.9, v0.4, v1.8 driver report | **Bit-identical or exact**                                                                                     |
| v0.3, v0.8, v1.0–v1.8 results                    | **Reproduced — diffs confined to wall-clock fields and residual diagnostics at machine epsilon (1e-13…1e-31)** |

- The v0.9 run log and results JSON come from *different executions* (different residuals under a fixed RNG seed) — the packaged log is not the log of the packaged run.
- The nested v1.8 `SHA256SUMS.txt` lists absolute `/mnt/data` paths and fails `shasum -c` as shipped; after rewriting, all hashes verify. The v1.9 manifest verifies cleanly (44/44).
- Shipped text corruption: the v0.4 PDF renders `|heta| ≃ 6.0×10⁻⁴⁶` (a mangled `\theta`) and "+cdots"; the v0.5 Markdown has broken `\frac`/`\neq` escapes (its .tex is correct).

## v0.1 – v0.4Crossed-null phases, spectral chronometry, scale locking

**Moderatev0.1's central construction is the mimetic map, uncited**

The exact null constraints reduce hab = C gab to precisely the Chamseddine–Mukhanov mimetic conformal map (arXiv:1308.5410). v0.1's related-work section and bibliography omit mimetic gravity entirely; v0.2 concedes the overlap ("must not be claimed as new").

**Moderatev0.3's Higgs-only obstruction proposition outruns its proof**

The stated conclusion needs a no-cancellation genericity assumption that appears only inside the proof ("whenever the indicated variation is not cancelled"), not in the hypotheses. False as printed; fixable with a genericity clause.

**Moderatev0.4's 20,000-point "stability scan" provably cannot fail**

Given the scan's own formulas, the tightest margin is ~57 orders of magnitude; the manuscript presents a test with no failure mode as a stress test. Also: the benchmark lock uses the EW-scale λH = 0.259 at f = MP, where the running quartic is ≈ 0 or negative — the tree valley may not exist at the matching scale, and λp is scale-ambiguous by orders of magnitude.

**ModerateThe layer's only falsifiable predictions are silently abandoned**

v0.2 derived two tree-level dimensionless sum rules (c∥² = 2c⊥² − 1 and the ΩH² relation) and flagged them as the candidate contribution. v0.3/v0.4 never mention them; v0.4's scorecard says a nontrivial prediction is still OPEN. They should be defended or formally retired.

**Verifiedv0.2 audit is sound; v0.1–v0.4 algebra checks out**

Every re-derived identity holds: the mimetic reduction, transverse rank deficiency, superluminal lock branch (c⊥² = 1/(1−ε) > 1), the v0.4 benchmark table, Einstein-frame fifth-force cancellation, the 1/p⁴ no-go. The v0.2 results JSON regenerates bit-identically. Caveat: several load-bearing post-2025 arXiv citations could not be checked offline and must be audited before external use.

## v0.5 – v0.8QCD lock, Z₆ protection, screening, cosmology

**Verified2/27 confirmed — and robust at two loops**

Independent re-derivation: (1 − 19/21)(21/23)(23/25)(25/27) telescopes exactly to 2/27, cross-checked three ways. A fresh two-loop RG run (which the packages defer as the "next decisive calculation") gives 0.0762 vs 0.0741 — +2.9%, so the headline is safe. Warning: the per-threshold response at charm shifts +30% at two loops, so the telescoping is fragile at low thresholds.

**Moderatev0.8 imports v0.7's no-screening theorem outside its hypotheses**

The theorem assumes fa ≥ MP; the v0.8 ridge sits at fa = 10⁻⁸MP. Recomputed on the ridge, the Sun's conversion margin collapses from 12 orders of magnitude to ~3 — and a neutron star gives q ≈ 80 ≫ qconv = 0.63: phase conversion inside neutron stars is energetically allowed on the headline benchmark, with binary-pulsar constraints never examined.

**ModerateThe UV quality problem silently disappears after v0.6**

v0.6 grades the elementary-Φ completion FAIL for UV completeness; v0.8 never mentions quality. At ridge parameters the Z₆-allowed Φ⁶/MP² operator must have coefficient c₆ ≲ 10⁻⁸¹ — this, not cosmology, is the binding viability constraint, and it rests on an unconstructed Wilson-line completion.

**ModeratePrecision theater on the v0.5 clock-comparison numbers**

The boxed β/η = 150.38 quotes 5 significant figures while neglecting the Damour–Donoghue isospin term (−6%, moving it to ≈ 159.9), the one-loop-only 2/27 (±3%), and the pure-gluonic proton (±9%). Realistic uncertainty ~10–15%. Also: v0.5's "exact threshold recursion" check literally asserts X − X = 0.

**MinorCross-package factor 2 in dg**

Cosmology selects x = π/6, halving dg from 7.41e-8 to 3.70e-8 — every v0.7 signal number implicitly refers to the π/2 vacuum the programme's own cosmology later rejects. No erratum notes it. The dramatic solar-core spinodal result is likewise specific to the discarded branch.

**Verifiedv0.8's honesty and numerics hold up**

The overclosure admission (Ω h² = 163.9, reproduced exactly) originates in v0.8 itself. The 12/12 strong-attractor claim survived a 1000× tolerance stress test. The thermal-focus coefficient 0.22673, ΔNeff = 7.403ξ⁴, and the v0.6 F₆ = 1/160 closed form all re-derive exactly; v0.6's Coleman–Weinberg Fourier check is the best genuine verification in the early programme.

## v0.9 – v1.2Reheating, in-in asymmetry, Kadanoff–Baym, cascade

**Criticalν₀ thermalization is assumed in a code comment — and likely false**

The v1.2 branch correction (B₅ = 0.005274, restoring T₅/T₀ = 1/4) assumes ν₀ thermalizes into sector 0. At the benchmark, yR ≈ 4.6e-5 and its only channels are yR⁴-suppressed scattering or inverse decay exactly at threshold — so ν₀ almost certainly free-streams, contributing **ΔNeff ≈ 0.85**, eight times the programme's own bound (0.107). If it free-streams, the plasma ratio reverts to 1/4 anyway and the entire §6 correction is moot. No manuscript or matrix row addresses this.

**Criticalv1.1's headline KB result is an invariant-manifold identity**

The "nontrivial two-time consistency check" E₅/E₀ = 1/256 is exact by construction: channel 5 is an identical copy of channel 0 coupled at exactly c/16, so the ratio is invariant for all time. Demonstrated from the shipped arrays: the ratio equals 1/256 with *zero* floating-point deviation at all 301 stored time slices. The surrogate could not have produced any other answer.

**Moderatetan θ transcription error in the boxed v1.2 result**

Boxed twice as 0.0728196; the package's own JSON/CSV say 0.07281715, and √(B₅/(1−B₅)) with the displayed B₅ confirms the JSON. Wrong in the 5th significant figure — a transcription, not a rounding. A second stale number (energy residual 5.59e-16 vs shipped 4.45e-16) confirms the manuscript was written from an earlier run.

**ModerateTautological controls around the cascade's real risk**

The two headline energy-conservation residuals are a Lorentz-boost identity and a quantity actively zeroed into the spectator bath before measurement — while that untracked bath holds 61.6% of final sector energy. (An independent check from the npz shows ρa⁴ behaves correctly, so the dynamics look sound; the shipped controls just prove nothing.) Same pattern: v0.9's 50k eigenvalue scan constructs its matrices positive; v1.0's "symbolic projection" hardcodes the projector's answer.

**VerifiedThe layer's arithmetic and self-corrections are real**

~60 recomputed quantities match (phasors, slow-roll chain, NDA, DFFS, Landau–Zener exponents, preheating tail self-consistency — including a nontrivial confirmation that the fitted Gaussian tail slope equals −π/k*² at the last tachyonic crossing). v1.1's grading of the original portal as "FAIL GENERICALLY" is a legitimate, documented correction. Unstated favorable corollary: even the uncorrected branch passes the ΔNeff bound (0.0213 < 0.107) — only the ξ₅ = 1/4 aesthetic needed the correction.

## v1.3 – v1.6Collision kernels, AMY/LPM transport, checkpoint

**Criticalv1.4's LPM effective-mass term is structurally wrong**

v1.4 uses m₁² − (1−x)m₂² − x m₃²; the standard AMY/BDMPS combination — used by v1.3 *and* v1.5 — is (1−x)m₂² + x m₃² − x(1−x)m₁². Substituting only the correct term moves the portal rate −30% and g→qq̄ +116%. The only validation (deep-LPM η ≥ 10) is blind to the error; all physical rates sit at η ≲ 4.5. v1.5 silently fixes it and mislabels the shift "normalization." The 10⁶ hierarchy conclusion survives; v1.4's specific numbers do not.

**Criticalv1.3's headline RG completion is asserted, not derived**

The counterterm ΔRG = −2Lℓ + ℓ² is defined as exactly the polynomial that cancels the fixed-order logs, then "proven" to cancel them by sympy — an identity true by construction. Nothing derives it from the declared RGE system, yet the entire v1.3 result (I₃ jumping from [−96.9, +102.4] to 6.58) rests on it.

**Moderate"Slowest channel in every row" is contradicted by its own CSV**

Γg→DD̄ < Γportal in 72 of 108 rows of v1.4's own table; the executive summary omits the two slowest QCD channels. The bottleneck conclusion survives only via an argument (D chemistry is portal-fed) the text never makes.

**Moderatev1.5's default verification never recomputes its headline**

The n = 10 quadrature value behind the Richardson-extrapolated ILPM and the entire published table is a hardcoded constant unless optional expensive flags are passed — undisclosed in the matrix ("Portal normalization band — CLOSED"). Balancing strength: v1.5's transcription of the Bödeker–Schröder validation target was checked against arXiv:1902.07220 and is correct (0.9% agreement), the strongest external validation in the programme.

**MinorSilent corrections and normalization slips**

v1.3 uses Nf = 6 in the Debye mass while counting D as thermal; v1.4 silently corrects to Nf = 7. v1.3's Γ⁽⁰⁰⁾ tensor carries a factor-6 slip on scalar diagonals and is internally inconsistent with its own portal_gamma. v1.6's "eR normalization identity" check compares an expression to itself (residual ≡ 0), and its manuscript never mentions the computed top four-fermion term (7.5% of the hard rate, JSON only).

## v1.7 – v1.9Gauge-covariant closure and the HPC pilot

**Critical"PILOT AUTHORIZED" — but there is nothing to run**

v1.9's `src/` contains only loaders and checklist validators; no Kadanoff–Baym/3PI evolution code exists anywhere in v1.7–v1.9. Of the 12 preflight gates, five re-read stored v1.8 numbers against thresholds beaten by 9–13 orders; three check that hand-written files contain hardcoded copies of their own strings; the rest are toy identities. One test is literally named `test_precomputed_acceptance_metrics`. The full suite passes in 0.85 s.

**CriticalThe gauge-consistency evidence base is empty**

The v1.7 Ward closure integrates a vertex defined so that q·Γ is the fundamental theorem of calculus on toy propagators; the Nielsen family has its pole ξ-independent by definition (the quoted 1.4e-12 tests scipy's root-finder); the v1.8 "quantum STI" multiplies both sides of the same Abelian Ward identity by the same scalar factor. Each carries fine-print disclosure — but the acceptance matrices compress all of it into PASS rows that v1.9 then inherits as "supplied by v1.8."

**CriticalThe frozen kernel moved up to ~2 orders of magnitude, and its error band vanished**

Interpolating the v1.7 and v1.8 tables onto a common grid: on shell they agree to <1%, but at ω = 2.5Ek the v1.8 value is up to ~435× the v1.7 value — physically expected (Born pair cut added), but it means v1.7's "conservative ±25%" envelope was wrong by two orders of magnitude, and v1.8/v1.9 freeze the new table as the pilot's regression target with *zero* off-shell uncertainty. The pilot grid (p/T up to 30) also silently extrapolates beyond the table domain (k/T ≤ 12) via `fill_value=None`.

**ModerateThe 3PI diagram ledger — the most consequential frozen input — is checked by nothing**

The 11 coefficients (−1/8, +i/6, …) sourced to the Berges review are validated only by Euler's formula and by matching a hardcoded copy of their own IDs. No existing gate could catch a wrong coefficient, and everything downstream depends on them.

**ModerateSilent spec contractions and stale numbers**

Memory window shrank from the declared T·tmem = 30 (v1.7) to 5.12, with the convergence scan topping out at 10.24 — the earlier target is unreachable even in the scan. v1.8's manuscript/claim matrix carry stale numbers vs the shipped JSON (2.53e-16 vs 2.65e-16; 0.319% vs 0.358%; 1.00339 vs 1.00588). v1.9 claims benchmark coverage ("pure Yukawa, linear response, kinetic/AMY") that its own docs grade as future regressions with no preregistered targets. The v1.9 acceptance matrix cites `pytest_output_v1_9.txt`, which does not exist.

**VerifiedThe anchor chain and specification layer are genuinely good**

ΓH/T = 1.1585158821e-3 is consistent across v1.6→v1.9; resource-tier arithmetic reproduces exactly; the v1.9 SHA manifest verifies 44/44; the observable contract / stop policy / counterterm basis are good preregistration practice. The problem is not the spec — it is that nothing yet exists that can fail.

## Cross-cutting patterns

- **Verification theater is the programme's systemic defect.** Every layer mixes a few genuine checks (v0.6's Fourier extraction, v0.7's BVP, v0.8's solver, v1.5's external validation) with tautologies graded PASS: unfailable scans, X−X=0 identities, hardcoded verdicts, ansatz-based "benchmarks", residuals zeroed before measurement.
- **Prose and matrices systematically outrun the evidence** — fine-print disclosures ("by construction", "assumed") vanish when compressed into PASS rows, and headline language escalates version over version ("benchmark" → "CLOSED" → "AUTHORIZED").
- **Corrections between versions are silent.** Nf = 6→7, the LPM mass-term fix, the dg halving, the vanished ±25% envelope, the shrunk memory window — none flagged as errata, though the programme elsewhere prides itself on documented failure.
- **Precision theater:** 5–9 significant figures routinely quoted on quantities with 5–15% of neglected physics or single-resolution numerics.

## Ranked repair & opportunity list

1. **Implement the already-specified 0.11 GB unit-test tier** as a real two-time evolution of even one scalar mode against the frozen kernel. Minutes in numpy; converts every currently-tautological gate (KMS, commutator, energy drift, memory-window convergence, anchor recovery) into a fallible measurement. Until something can fail, nothing at the frontier is verified.
2. **Symbolically verify the 11 3PI ledger coefficients** (toy-model Legendre transform in sympy) before any solver code is generated from them — the one pre-pilot task that could invalidate everything downstream.
3. **Resolve the ν₀ fate**: specify a thermalization mechanism (new couplings, re-audited against the portal analysis) or accept free-streaming — which breaks the ΔNeff bound at ≈ 0.85 but also moots the v1.2 branch correction. Re-derive v0.9's S₅₀ = 0 under two-stage injection.
4. **Deprecate or recompute v1.4** with the standard LPM mass term; cross-run v1.5's validated solver on v1.4's QCD channels; add a Bethe–Heitler-limit check and validate hard+LPM totals against Bödeker–Schröder Table 1. Derive (or delete) v1.3's ΔRG.
5. **Adopt the v1.7-vs-v1.8 kernel difference as the declared off-shell uncertainty band** (seconds of compute, already done here) and make it a fallible preflight gate; fix the pilot-grid extrapolation beyond the table domain.
6. **Convergence studies for single-resolution load-bearing numbers**: Rν (a 35% correction on one 280-bin grid), the v1.1 leakage, Txrec, the x-cutoff window. Each is a cheap halving/doubling run.
7. **Run the advertised-but-never-executed checks**: the singlet-vs-elementary pole/width comparison (ten lines), a real Nielsen test on a one-loop Rξ self-energy, v1.5 with `--recompute-high`.
8. **Close the v0.x loose ends**: defend or retire the v0.2 sum rules; recompute the v0.8 screening/neutron-star margins on the ridge; state the UV quality requirement (c₆ ≲ 10⁻⁸¹) wherever "viable" is claimed; fix the v0.3 proposition, the v0.4 λH-running gap, and the tan θ / |heta| / stale-number transcriptions.
9. **Fix portability**: replace `/mnt/data` with script-relative paths, declare dependencies, regenerate the broken SHA manifest, and cull every check that cannot fail from the acceptance matrices (or relabel as "consistency pin").

**Reading the whole:** the programme's self-critical instinct is real — v0.2 killed v0.1's novelty claim with correct proofs, v0.8 admits its own overclosure, v1.6 says "do not submit" — and the surviving narrow thesis (chronometric shear as Weyl-invariant obstruction; the 2/27 transmission) is arithmetically solid. What separates this from publishable work is not the math but the evidential hygiene: tautological gates, silent corrections, and a frontier whose authorization rests on tests that cannot fail.

Sources: five independent review passes over the manuscripts, data, and code in `original-info/`; full re-run of all shipped verifier suites in a staged sandbox replica; targeted recomputations in sympy/numpy/scipy including a two-loop RG run, kernel-table cross-interpolation, and shipped-array forensics.
