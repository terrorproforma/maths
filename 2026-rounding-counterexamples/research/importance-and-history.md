# Importance and chronology

Literature-check date: **23 July 2026**.

## Goemans' cost conjecture

Dinitz, Garg, and Goemans proved the foundational additive-maximum-demand theorem at FOCS 1998 and in *Combinatorica* 19(1), 17--41 (1999), DOI `10.1007/s004930050043`.

The minimum-cost formulation and the conjectured simultaneous cost/congestion guarantee were part of the research programme surrounding Skutella's FOCS 2000 work and 2002 *Mathematical Programming* paper, DOI `10.1007/s101070100260`.

The 2024 planar paper by Traub, Vargas Koch, and Zenklusen still described Goemans' cost version as open; it proved the planar bound with additive error `2D`, DOI `10.1137/1.9781611977912.24`.

The 2024/2025 series-parallel work of Almoghrabi, Skutella, and Warode described the statement as a **25-year-old conjecture** and proved the exact convex-decomposition result for series-parallel digraphs, arXiv `2412.05182`.

A paper published at SOSA on 6 January 2026 again called it a famous conjecture and reported only limited general progress: Swamy, Traub, Vargas Koch, and Zenklusen, DOI `10.1137/1.9781611978964.42`.

Accordingly, the conservative historical description is that the conjecture remained unresolved for **approximately a quarter century**, dating from the FOCS 2000 / 2002 minimum-cost formulation to 2026. Dating from the 1998--1999 Dinitz--Garg--Goemans theorem gives roughly 27 years of surrounding history, but the paper should avoid presenting that longer interval as the age of the cost conjecture itself.

### Why the counterexample matters

The example does not weaken the classical Dinitz--Garg--Goemans theorem. It pinpoints the failure of combining two individually plausible requirements:

```text
additive upper deviation D, and no increase in cost.
```

It is planar and acyclic, so nonplanarity is not the source of failure. Its undirected topology is a subdivision of `K_4`, making it the first natural forbidden topology immediately beyond the known series-parallel positive result.

The example also yields a quantitative question. Let `alpha_planar` be the best coefficient such that every planar fractional flow can be rounded with no greater cost and upper deviation at most `alpha_planar D`. The construction gives

```text
9/8 <= alpha_planar <= 2,
```

where the upper bound is the 2024 planar theorem.

## Machine-dependent weighted chairman assignment

Liu and Reis posted *The Weighted Chairman Assignment Problem* on arXiv on 23 November 2025 and published it at ITCS 2026, DOI `10.4230/LIPIcs.ITCS.2026.98`. Their Conjecture 19 asks for prefix discrepancy at most the largest machine-dependent weight. Conjecture 21 is a unified support-preserving strengthening.

As measured to 23 July 2026, Conjecture 19 had therefore been in the literature for about **eight months from the preprint** and **six months from formal publication**.

### Why this counterexample matters

The ordinary weighted-chairman problem has a conservation structure because each job has one common weight across all rows. Machine-dependent weights destroy that conservation. The counterexample isolates the failure in a three-column forcing gadget and remains valid even when the integral assignment is allowed to leave the fractional support.

The result does **not** settle the ordinary weighted-carpooling conjecture, in which a column has one common weight. It specifically rules out the proposed machine-dependent extension and any stronger theorem containing it.

## Publication caution

These are new research claims, not established literature facts. The finite certificates are reproducible, but priority, theorem wording, and bibliographic completeness should receive independent expert review before journal submission or a public priority announcement.
