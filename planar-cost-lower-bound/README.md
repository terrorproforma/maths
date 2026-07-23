# Consequences of Rybin's counterexample: convex-decomposition failure and a planar 9/8 lower bound

**Author:** Angus Muffatti (AI-assisted; see the disclosure in the manuscript).
**Status:** research note with exact certificates; not yet peer reviewed.
**Builds on:** Dmitry Rybin's counterexample to Goemans' cost-preserving unsplittable-flow
conjecture (constructed with GPT-5.6 Pro; announced at
<https://x.com/DmitryRybin1/status/2079904005652893709>). The base instance is Rybin's;
this note claims only the corollaries and the parametric analysis. See
[`../ATTRIBUTIONS.md`](../ATTRIBUTIONS.md).

## Contents of the note

1. **Corollary:** Rybin's seven-vertex instance also refutes the
   cost-and-two-sided-bounds conjecture and the convex-decomposition strengthening of
   Morell and Skutella (2022). Their costless two-sided existence conjecture survives.
2. **Sharp boundary remark:** the instance's underlying graph is a K₄ subdivision — the
   first topology beyond the series-parallel class where the decomposition is a theorem.
3. **Quantitative planar bound:** a parametric form of the instance forces additive
   congestion at least (9/8 − o(1))·D for any cost-preserving planar rounding theorem, so
   the optimal planar constant lies in **[9/8, 2]** (upper bound: Traub–Vargas Koch–
   Zenklusen).
4. **The triangle-facet mechanism**, stated as a reusable design principle.

## Verify

```bash
python3 code/verify_dgg.py            # exhaustive exact check of the base certificate (Rybin's instance)
python3 code/search_dgg_family.py     # enumerate the parametric family; supremum 9/8
```

## Build the paper

```bash
cd paper && latexmk -pdf planar_cost_lower_bound.tex
```
