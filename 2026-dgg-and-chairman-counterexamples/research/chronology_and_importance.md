# Chronology and importance

This note records the literature status checked on **23 July 2026**. It is not a substitute for a fresh priority search on the submission date.

## Single-source unsplittable flow

- **1998/1999:** Dinitz, Garg, and Goemans presented and published the sharp additive upper-bound theorem: every feasible fractional single-source flow has an unsplittable routing with arc load at most `x_a+d_max`. The journal paper is *Combinatorica* 19(1), 17–41 (1999), DOI `10.1007/s004930050043`.
- **2000/2002:** Skutella's FOCS work and *Mathematical Programming* article on min-cost unsplittable flow recorded the cost-preserving conjecture attributed to Goemans.
- **2021/2022:** Morell and Skutella formulated simultaneous lower/upper and cost-strengthened conjectures in *Mathematical Programming* 192, 477–496, DOI `10.1007/s10107-021-01704-4`.
- **2024:** Traub, Vargas Koch, and Zenklusen proved the planar cost theorem with additive factor `2 d_max`, SODA 2024, DOI `10.1137/1.9781611977912.24`.
- **January 2026:** Swamy, Traub, Vargas Koch, and Zenklusen still described Goemans' statement as a famous open conjecture with limited progress, SOSA 2026, DOI `10.1137/1.9781611978964.42`.
- **29 June 2026:** Almoghrabi, Skutella, and Warode published the exact convex-decomposition theorem for series-parallel digraphs, DOI `10.1007/s10107-026-02392-8`, describing the underlying question as 25 years old.
- **22 July 2026:** the seven-vertex `58<60` certificate was publicly circulated for independent checking.

### How long was it open?

There are two reasonable starting dates. From the 1999 Dinitz–Garg–Goemans journal theorem to July 2026 is about **27 years**. From the explicit min-cost formulation in Skutella's 2002 journal paper it is about **24 years**. Recent specialists called it a **25-year-old conjecture**, so “roughly a quarter-century” is the conservative wording for a paper. “Thirty years” is rhetorically understandable but bibliographically imprecise.

### Why the counterexample matters

1. **It isolates the exact point of failure.** The Dinitz–Garg–Goemans theorem remains true and sharp without costs. The counterexample shows that exact cost preservation cannot be added to the same `+d_max` guarantee.
2. **It is planar.** Nonplanarity is not responsible for the failure. The known planar factor `2` remains valid, but factor `1` does not.
3. **It lies at the first topological boundary beyond series-parallel graphs.** Suppressing its three degree-two terminals gives `K4`, while the exact theorem holds on series-parallel digraphs.
4. **It is finite and exhaustive.** There are six source-terminal paths and only eight routings. The strict gap is integer-valued and does not rely on numerical optimization.
5. **It gives a quantitative research direction.** The parametric family proves a planar lower bound of `9/8` for any universal cost-preserving additive factor, compared with the known upper bound `2`.
6. **It also destroys the cost-enhanced two-sided conjecture and associated convex-decomposition strengthening.** It does not destroy the costless two-sided existence conjecture.

## Machine-dependent weighted chairman assignment

- **23 November 2025:** Liu and Reis posted the preprint *Weighted Chairman Assignment and Flow-Time Scheduling*, arXiv `2511.18546`.
- **23 January 2026:** the paper appeared at ITCS 2026, DOI `10.4230/LIPIcs.ITCS.2026.98`. Conjecture 19 asks for the maximum-weight prefix bound with weights `d_ij` depending on both row and column; Conjecture 21 adds support and committee constraints.
- **July 2026:** the repeated three-column detector in this repository gives a strict rational counterexample.

### How long was it open?

Measured from the preprint, the machine-dependent conjecture was open for about **eight months**; measured from formal conference publication, about **six months**.

### Why the chairman counterexample matters

The common-column-weight theorem remains intact. The construction identifies machine dependence as a real boundary, not merely a technical obstacle. It remains false even with fractional support two per column, only 11 rows and 15 columns, strictly positive weights, and only three distinct weight values. Because the proof allows arbitrary off-support assignments, it refutes the unrestricted Conjecture 19 before using the extra support restriction in Conjecture 21.

## Recommended description in public communication

Use the phrase:

> A finite counterexample to a roughly quarter-century-old cost-preserving unsplittable-flow conjecture, together with a counterexample to a 2026 machine-dependent prefix-discrepancy conjecture.

Until peer review, also state prominently that the claims are new and independently checkable but not yet formally refereed.
