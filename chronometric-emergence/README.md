# Chronometric Emergence

**Author: Angus Muffatti**

An ongoing theoretical-physics programme investigating whether causal or conformal structure may be primitive while operational duration is reconstructed from common spectral scaling, and how controlled failures of that scaling appear as **chronometric shear**.

## Canonical repository layout

- [`original-info/`](original-info/) — immutable historical archive of the recovered v0.1-v1.9 papers, LaTeX, Markdown, code, data, arrays, figures and matrices.
- [`frontier-evidence-v2/`](frontier-evidence-v2/) — active adversarial evidence repair, errata, independent recomputations and current scientific verdict.
- [`sources/`](sources/) — original project conversation material and the independent 25 August 2026 audit.
- [`STORAGE_POLICY.md`](STORAGE_POLICY.md) — project-specific archival rules, extending the repository-wide policy.

## Current evidence status

The independent audit found that earlier labels such as `PASS`, `CLOSED` and `PILOT AUTHORIZED` often outran the evidence. The project now distinguishes algebraic identity checks, regressions, independent recomputations, convergence tests, external benchmarks, predictions, blockers and retractions.

The active evidence package is:

- [`frontier-evidence-v2/README.md`](frontier-evidence-v2/README.md) — scope and reproduction instructions;
- [`frontier-evidence-v2/ERRATA.md`](frontier-evidence-v2/ERRATA.md) — formal corrections and retractions;
- [`frontier-evidence-v2/EVIDENCE_POLICY.md`](frontier-evidence-v2/EVIDENCE_POLICY.md) — evidence taxonomy;
- [`frontier-evidence-v2/docs/FRONTIER_EVIDENCE_REPORT.md`](frontier-evidence-v2/docs/FRONTIER_EVIDENCE_REPORT.md) — generated consolidated report;
- [`frontier-evidence-v2/results/claim_matrix_v2.csv`](frontier-evidence-v2/results/claim_matrix_v2.csv) and [`frontier-evidence-v2/results/frontier_status.json`](frontier-evidence-v2/results/frontier_status.json) — machine-readable status generated from the executable suite.

### Frontier decision

| Layer | Current status |
|---|---|
| Universal spectral factorisation and chronometric shear | **Conditionally earned formal frontier**; theorem hypotheses and novelty still require specialist review |
| QCD threshold transmission | **Earned at leading one-loop order**; `2/27` retained with higher-order uncertainty |
| Scalar unequal-time numerical infrastructure | **Unit tier earned** through independent Hamiltonian and causal-memory solvers with convergence tests |
| v1.3 RG completion | **Retracted**; cancellation was imposed rather than derived |
| v1.4 direct AMY numbers | **Deprecated** because the collinear mass combination was structurally wrong |
| v1.5 electroweak/Yukawa LPM calculation | **Best current transport anchor**, limited to the collinear sector |
| v1.7-v1.8 arbitrary off-shell kernels | **Model/initialisation family only**, not a physical uncertainty band |
| Full PT/BFM three-loop 3PI/Kadanoff-Baym pilot | **Not authorised**; the archived package specified a solver but did not implement one |
| Cosmological implementation | **Blocked on the archived low-`f_a` ridge**, especially by neutron-star conversion |
| Ultraviolet completion | **Conditional deconstruction skeleton**, not a completed UV theory |

## Reproduce the active evidence layer

```bash
cd chronometric-emergence/frontier-evidence-v2
python -m pip install -e '.[test]'
make full
```

The full LPM recomputation is intentionally expensive. CI runs the calculation from source and commits the generated report/results when they change.

## Historical record

The historical packages are preserved rather than rewritten. Read them together with [`frontier-evidence-v2/ERRATA.md`](frontier-evidence-v2/ERRATA.md). The source transcript is [`sources/Photon_Perspective_in_Relativity.txt`](sources/Photon_Perspective_in_Relativity.txt), and the red-team review is [`sources/Chronometric_Emergence_Audit_2026-08-25.md`](sources/Chronometric_Emergence_Audit_2026-08-25.md).

## Strongest surviving thesis

On a connected domain, a family of positive physical clock frequencies admits one common operational proper-time metric precisely when `omega_A(x) = c_A chi(x)` for constants `c_A` and one positive local scalar `chi`. Equivalently, every pairwise differential frequency ratio vanishes. The Weyl-invariant obstruction is chronometric shear. A vectorlike-colour threshold transmits one scale-lock defect into low-energy QCD with leading one-loop coefficient `2/27`; that coefficient is established QCD threshold physics, while its chronometric interpretation is the project-specific synthesis.

All original project work in this directory is authored by **Angus Muffatti**, with AI assistance disclosed. Third-party physics and mathematics remain attributed in the archived manuscripts and source ledgers.
