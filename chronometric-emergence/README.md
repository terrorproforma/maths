# Chronometric Emergence

**Author: Angus Muffatti**

An ongoing theoretical-physics programme investigating whether causal or conformal structure may be primitive while operational duration is reconstructed from common spectral scaling, and how controlled failures of that scaling appear as **chronometric shear**.

## Current evidence status

The project has completed an adversarial post-audit rebuild. Earlier labels such as `PASS`, `CLOSED`, and `PILOT AUTHORIZED` were often too strong: several checks established algebraic consistency or regression stability rather than physical validity.

The canonical evidence-repair package is:

- [`frontier-evidence-v2/`](frontier-evidence-v2/) — source, tests, independent recomputations and generated results.
- [`frontier-evidence-v2/docs/FRONTIER_EVIDENCE_REPORT.md`](frontier-evidence-v2/docs/FRONTIER_EVIDENCE_REPORT.md) — consolidated scientific verdict.
- [`frontier-evidence-v2/ERRATA.md`](frontier-evidence-v2/ERRATA.md) — retractions and corrected claims.
- [`frontier-evidence-v2/EVIDENCE_POLICY.md`](frontier-evidence-v2/EVIDENCE_POLICY.md) — distinction between identities, regressions, independent recomputations, convergence tests, external benchmarks and predictions.
- [`frontier-evidence-v2/results/claim_matrix_v2.csv`](frontier-evidence-v2/results/claim_matrix_v2.csv) — claim-by-claim status.
- [`frontier-evidence-v2/results/frontier_status.json`](frontier-evidence-v2/results/frontier_status.json) — machine-readable frontier decision.

### Frontier decision

| Layer | Current status |
|---|---|
| Universal spectral factorisation and chronometric shear | **Conditionally earned formal frontier**; theorem hypotheses corrected and specialist novelty review still required |
| QCD threshold transmission | **Earned at leading one-loop order**; `2/27` retained with a conventional higher-order uncertainty band |
| Real-time numerical infrastructure | **Scalar unit tier earned** through an unequal-time open-system calculation with independent solvers and convergence tests |
| v1.3 RG completion | **Retracted**; its cancellation was imposed rather than derived from operator mixing |
| v1.4 direct AMY numbers | **Deprecated and recomputed diagnostically** because the collinear mass combination was wrong |
| v1.5 electroweak/Yukawa LPM calculation | **Best current transport anchor**, limited to the collinear LPM sector; hard cuts and full matching remain incomplete |
| v1.7–v1.8 arbitrary off-shell kernels | **Model/initialisation family only**, not a calculated physical off-shell uncertainty band |
| Full PT/BFM three-loop 3PI/Kadanoff–Baym pilot | **Not authorised**; the archived v1.9 package specified a solver but did not implement one |
| Cosmological implementation | **Blocked on the archived low-`f_a` ridge** by compact-object, especially neutron-star, conversion |
| Ultraviolet quality | **Conditional 24-link local-gauge/deconstruction skeleton**, not a completed UV theory |

The narrow formal and threshold programme remains worth pursuing. The full cosmological and non-Abelian-HPC superstructure has not yet earned publication-grade frontier status.

## Evidence-repair calculations

The v2 suite includes:

- independent coloured half-edge automorphism checks for all eleven three-loop 3PI coefficient magnitudes;
- a real Caldeira–Leggett unequal-time scalar benchmark solved by both Hamiltonian normal modes and a causal memory equation;
- timestep, memory-window, commutator, fluctuation–dissipation and energy diagnostics;
- corrected v1.4 LPM mass kinematics and a complete v1.5 high-resolution recomputation;
- an explicit prompt-daughter dark-radiation calculation and a conditional exact-replica gauge-charged repair;
- Earth, Sun, white-dwarf and neutron-star conversion estimates on the actual low-`f_a` ridge;
- a quantitative elementary UV-quality failure and 24-link deconstruction estimate;
- direct v1.7/v1.8 off-shell model-discrepancy and table-coverage audits;
- a clean-checkout portability scanner and declared Python dependencies.

## Reproduce

```bash
cd chronometric-emergence/frontier-evidence-v2
python -m pip install -e '.[test]'
python -m frontier_evidence.run_all --repo-root ../..
pytest -q
```

The complete LPM recomputation is deliberately expensive. CI runs it rather than silently loading the archived high-resolution result.

## Historical research record

- [`original-info/`](original-info/) — recovered original PDFs, LaTeX, Markdown, scripts, arrays, figures, matrices and packages from the iterative programme.
- [`sources/`](sources/) — source conversation material.

Historical packages are retained as research provenance even where later evidence retracts or supersedes their conclusions. They must be read together with the v2 errata.

## Strongest surviving thesis

On a connected domain, a family of positive physical clock frequencies admits one common operational proper-time metric precisely when

```text
omega_A(x) = c_A chi(x)
```

for constants `c_A` and one positive local scalar `chi`. Equivalently, every pairwise differential frequency ratio vanishes. The Weyl-invariant obstruction is chronometric shear. A displayed vectorlike-colour threshold transmits one scale-lock defect into low-energy QCD with leading one-loop coefficient `2/27`; this coefficient is established QCD threshold physics, while its chronometric interpretation is the project-specific synthesis.

All original project work in this directory is authored by **Angus Muffatti**, with AI assistance disclosed. Third-party physics and mathematics remain attributed in the archived manuscripts and source ledgers.
