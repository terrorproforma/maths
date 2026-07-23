# Counterexamples to two weighted-rounding conjectures

> **Archived.** This combined package is superseded by the per-result folders
> [`../chairman-counterexample/`](../chairman-counterexample/) and
> [`../planar-cost-lower-bound/`](../planar-cost-lower-bound/); it is retained for the
> record.

> **Attribution.** The flow (DGG/Goemans) counterexample in this package is due to
> **Dmitry Rybin** (constructed with GPT-5.6 Pro; announced at
> <https://x.com/DmitryRybin1/status/2079904005652893709>); the positive-cost variant,
> Morell–Skutella corollaries, and parametric 9/8 family here build on his instance. The
> chairman (Liu–Reis) counterexample is from the repository owner's own session. The
> combined manuscript `paper/main.tex` carries an explicit attribution note for the Rybin
> sections; a chairman-only manuscript is at
> `../2026-rounding-counterexamples/papers/chairman-counterexample.tex`.
> See [`../ATTRIBUTIONS.md`](../ATTRIBUTIONS.md) and
> [`../PROVENANCE_AUDIT.md`](../PROVENANCE_AUDIT.md).

This folder contains a self-contained research package for two finite counterexamples:

1. a planar acyclic counterexample to Goemans' cost-preserving single-source unsplittable-flow conjecture; and
2. a sparse rational counterexample to Liu and Reis' machine-dependent weighted-chairman Conjecture 19 (and hence to their unified Conjecture 21).

Both certificates use exact rational arithmetic. The flow certificate has seven vertices, nine arcs, three terminals, exactly two source-terminal paths per terminal, and exactly eight unsplittable routings. Its fractional cost is 58, whereas every routing obeying the conjectured additive upper bound has cost at least 60.

The chairman certificate has 11 rows and 15 columns. Every fractional column has support two, all weights are strictly positive, and the claimed discrepancy threshold is 1. A three-column forcing gadget repeated five times gives a final certified discrepancy of at least 619/600.

## Status

These are new research claims and have not yet passed journal peer review. The repository is designed for independent checking: the proofs are finite, the source data are machine-readable, and the verification scripts use exact arithmetic wherever possible. The manuscript is anonymous by default; legal authorship and affiliation information must be supplied by the submitting human author.

## Layout

- `paper/` — journal-style LaTeX manuscript and bibliography.
- `figures/` — exact TikZ and SVG illustrations.
- `data/` — machine-readable rational instances.
- `code/` — exact verifiers, an independent MILP check, and parameter searches.
- `research/` — derivations, chronology, importance, failed-gadget lessons, and audit notes.
- `artifacts/` — compiled PDF and build outputs when available.

## Reproduce

```bash
python3 code/verify_dgg.py
python3 code/verify_chairman_certificate.py
python3 code/verify_chairman_milp.py   # requires scipy
make
```

The first two checks require only Python's standard library. The MILP script independently asks whether any integral assignment satisfies all chairman prefix bounds. The LaTeX build requires a TeX distribution with TikZ, `amsmath`, `booktabs`, `microtype`, `natbib`, and `hyperref`.

## Main numerical certificate

For the unsplittable-flow instance, the demands are `(15,10,15)` and `D=15`. The fractional arc loads and costs are

| arc | load | unit cost |
|---|---:|---:|
| `s->t1` | 10 | 2 |
| `s->t2` | 6 | 3 |
| `s->u` | 24 | 0 |
| `u->t3` | 10 | 2 |
| `u->v` | 14 | 0 |
| `v->t1` | 5 | 0 |
| `v->w` | 9 | 0 |
| `w->t2` | 4 | 0 |
| `w->t3` | 5 | 0 |

The fractional cost is `58`. Any additive-`D`-good routing uses at most one of the three zero-cost choices, so it uses at least two choices of integral cost `30`, giving minimum cost `60`.

## Responsible-use note

The discovery and drafting process used GPT-5.6 Pro as a research assistant. The repository records the finite certificates and verification code so that the claims can be evaluated independently of that provenance. An AI system should not be listed as an author; the human submitter is responsible for verification, attribution, disclosure, and submission.
