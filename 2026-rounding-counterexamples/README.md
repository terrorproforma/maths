# Counterexamples to two weighted-rounding conjectures

> **Archived.** This combined package is superseded by the per-result folders
> [`../chairman-counterexample/`](../chairman-counterexample/) and
> [`../planar-cost-lower-bound/`](../planar-cost-lower-bound/); it is retained for the
> record.

**Status:** research preprint and exact certificate package, prepared for independent review. The mathematical claims are explicit and finitely checkable; priority and novelty should still be checked by the eventual human authors and referees before public announcement.

> **Attribution.** Result 1 below (the DGG/Goemans flow counterexample,
> `papers/dgg-counterexample.tex`, and the DGG half of `papers/overview.tex`) is due to
> **Dmitry Rybin** (with GPT-5.6 Pro; announced at
> <https://x.com/DmitryRybin1/status/2079904005652893709>) and is built upon here with
> credit, not claimed. Result 2 (the chairman counterexample,
> `papers/chairman-counterexample.tex`) is from the repository owner's session.
> See [`../ATTRIBUTIONS.md`](../ATTRIBUTIONS.md) and
> [`../PROVENANCE_AUDIT.md`](../PROVENANCE_AUDIT.md).

This directory contains two self-contained results.

1. **A planar counterexample to Goemans' cost conjecture for single-source unsplittable flow.** The instance has seven vertices, nine arcs, three demands, exactly two paths per terminal, and exactly eight unsplittable routings. The fractional cost is `58`; every unsplittable routing satisfying the conjectured additive upper bound has cost at least `60`.
2. **A counterexample to the machine-dependent weighted-chairman conjecture of Liu and Reis.** The instance has 11 rows and 15 columns. A three-column forcing gadget is repeated five times, producing an exact prefix discrepancy of at least `619/600 > 1`.

## Fast verification

The verifiers use only the Python standard library and exact integer or rational arithmetic.

```bash
cd 2026-rounding-counterexamples
python3 code/verify_all.py
```

Expected final lines:

```text
DGG certificate verified: min good cost = 60 > fractional cost = 58
Chairman certificate verified: forced accumulator lower bound = 619/600 > 1
All exact certificates passed.
```

## Build the manuscripts

A TeX Live installation with `latexmk`, `pdflatex`, TikZ, `booktabs`, and `hyperref` is sufficient.

```bash
make papers
```

The expected PDFs are:

```text
build/dgg-counterexample.pdf
build/chairman-counterexample.pdf
build/overview.pdf
```

GitHub Actions runs the exact verifiers and compiles all three PDFs. The compiled PDFs are uploaded as workflow artifacts; generated binaries are deliberately not treated as source files.

## Directory map

```text
2026-rounding-counterexamples/
├── README.md
├── Makefile
├── AI_DISCLOSURE.md
├── code/
│   ├── verify_dgg.py
│   ├── verify_chairman.py
│   ├── verify_all.py
│   ├── derive_dgg_family.py
│   └── derive_chairman_family.py
├── data/
│   ├── dgg_instance.json
│   └── chairman_instance.json
├── figures/
│   ├── dgg_network.tex
│   ├── dgg_obstruction.tex
│   ├── chairman_gadget.tex
│   └── graphical_abstract.tex
├── papers/
│   ├── dgg-counterexample.tex
│   ├── chairman-counterexample.tex
│   ├── overview.tex
│   └── references.bib
└── research/
    ├── derivation-dgg.md
    ├── derivation-chairman.md
    ├── importance-and-history.md
    ├── provenance.md
    └── validation-report.md
```

## Central certificates

For the flow instance, the three zero-cost path choices form a triangle conflict graph. If `z_i=1` denotes choosing the cheap path for terminal `i`, every capacity-good integral routing satisfies

```text
z_1 + z_2 + z_3 <= 1,
```

whereas the fractional cheap-path marginals are `(1/3, 2/5, 1/3)` and sum to `16/15`. The costs are the nonnegative separator of this violated stable-set inequality.

For the chairman instance, every hypothetical discrepancy-1 assignment is forced to make five specific decisions. Each decision contributes `5/24` to an accumulator row. Ten detector columns can offset the accumulator by at most `10/1000`, giving

```text
5*(5/24) - 10/1000 = 619/600 > 1.
```

## Scope of the record

The repository contains the complete final derivations, exact data, exact certificate verifiers, parametric-family reconstruction scripts, manuscript sources, figures, and build automation. Earlier exploratory searches were conducted interactively and were not all preserved as standalone programs; `research/provenance.md` distinguishes final reproducible code from ephemeral exploration.

## Authorship and submission

The manuscripts use `Anonymous for review`. Replace that placeholder with the legal author list, affiliations, acknowledgements, contribution statement, and corresponding-author details before submission. Do not list an AI system as an author. See `AI_DISCLOSURE.md`.
