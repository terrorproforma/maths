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

**Quantitative strengthening (7/6).** A balanced version of the same gadget forces
discrepancy arbitrarily close to `7/6·D`: for every ε > 0 there is a finite instance (unit
maximum weight, support two per column) on which every integral assignment incurs some
prefix discrepancy ≥ 7/6 − ε, and 7/6 is optimal for this three-column family. A concrete
49×72 instance forces discrepancy ≥ 3379/3000 > 9/8. No constant upper bound for
machine-dependent prefix discrepancy appears to be known — posed as an open problem in the
paper.

## Verify

Three independent checks:

```bash
python3 code/verify_chairman.py                # exact rationals, reads data/chairman_instance.json
python3 code/verify_chairman_certificate.py    # exact rationals, self-contained construction
python3 code/verify_chairman_milp.py           # independent MILP infeasibility (needs numpy+scipy/HiGHS)
python3 code/verify_stronger_bound.py          # exact certificate for the 7/6 theorem and 9/8 instance
python3 code/verify_stronger_milp.py           # independent MILP: 49x72 instance infeasible at budget 9/8
```

Expected: `final accumulator lower bound = 619/600`, `chairman certificate verified
exactly`, `MILP independently certifies infeasibility`, `stronger-bound certificate
verified exactly`, and `MILP independently certifies infeasibility at budget 9/8`.

## Build the paper

```bash
make paper    # compiles paper/chairman_counterexample.pdf (the single source of truth)
make arxiv    # assembles and test-compiles the self-contained arXiv package in arxiv-upload/
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
