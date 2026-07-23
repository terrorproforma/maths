# Machine-dependent weighted chairman assignment: a counterexample

**Author:** Angus Muffatti (AI-assisted; see the disclosure in the manuscript).
**Status:** research preprint with exact certificates; not yet peer reviewed.

This package disproves Conjecture 19 of Liu and Reis (machine-dependent weighted chairman
assignment), and consequently their unified support-preserving Conjecture 21.

## The result

For positive machine-dependent weights `d_ij`, Liu and Reis conjectured that every
fractional assignment admits an integral assignment whose row/prefix discrepancy is at most
`D = max d_ij`. The instance here has 11 rows and 15 columns, every fractional column has
support two, all weights lie in `{1/1000, 1/2, 1}` (so `D = 1`), and **every** integral
assignment — including assignments outside the fractional support — has some row/prefix
discrepancy at least `619/600 > 1`.

The mechanism: machine-dependent weights break the conservation identity that protects the
classical (common-weight) chairman problem. A three-column detector gadget forces one
decision per block; five forced decisions make an accumulator row overflow.

## Verify

Three independent checks:

```bash
python3 code/verify_chairman.py                # exact rationals, reads data/chairman_instance.json
python3 code/verify_chairman_certificate.py    # exact rationals, self-contained construction
python3 code/verify_chairman_milp.py           # independent MILP infeasibility (needs numpy+scipy/HiGHS)
```

Expected: `final accumulator lower bound = 619/600`, `chairman certificate verified
exactly`, and `MILP independently certifies infeasibility`.

## Build the paper

```bash
cd paper && latexmk -pdf chairman_counterexample.tex
```

## Contents

- `paper/` — the manuscript (`chairman_counterexample.tex`) and bibliography.
- `figures/` — TikZ source for the detector/accumulator figure.
- `data/` — the machine-readable rational instance.
- `code/` — the three verifiers and the gadget-parameter derivation script.
- `research/` — the derivation notes.

## Attribution and provenance

This result is from the author's own AI-assisted research session (23 July 2026). It is
methodologically adjacent to — but shares no content with — Dmitry Rybin's counterexample
to Goemans' cost-preserving unsplittable-flow conjecture, which inspired the search for
nearby rounding conjectures to test; see `../ATTRIBUTIONS.md`. The classical context is
Tijdeman's chairman assignment problem; the refuted conjectures are from Liu and Reis
(preprint November 2025, published January 2026).
