# Machine-Dependent Chairman Assignment: Next-Frontier Theorems & Exact Certificates

This directory advances the machine-dependent weighted chairman assignment programme beyond [`chairman-counterexample/`](../../chairman-counterexample/), [`detector-chains/`](../), and the small-row results on `origin/claude/clever-davinci-ztxm29` (`chairman-small-rows/`).

Every theorem is proved analytically and backed by standalone exact rational (`fractions.Fraction`, Python stdlib only) verifiers, plus independent HiGHS MILP infeasibility checks allowing all off-support assignments.

## Headline Results

| Problem | Previous State | New Proved Result | Exact Certificate |
|---|---|---|---|
| **Problem B (Lower bound on $\kappa$)** | $\kappa \ge 1 + W(1/e) \approx 1.278465$ | **$\kappa \ge 1 + \ln 2 \approx 1.693147$** (via three escalating families: Fresh Cascade $1 + 1/e \approx 1.367879$, 2-Row Ping-Pong $1 + W(1) \approx 1.567143$, Recursive Binary-Tree Splitting $1 + \ln 2 \approx 1.693147$; all support-2, strictly positive weights, zero composition barrier) | `verify_cascade_and_pingpong.py` (certified rungs up to `1.681499`) + `verify_independent_milp.py` |
| **Problem A (Minimal machines $m^*$ with $\kappa_{m^*} > 1$)** | $3 \le m^* \le 11$ | **$m^* \in \{3, 4\}$**, proving **$\kappa_4 \ge c_4^* \approx 1.079253$** (unique root of $3c - 2 = e^{-(c-1)} + e^{1-2c}$) and a compact $5 \times 47$ counterexample ($\kappa_5 > 1001/1000$) | `verify_small_rows_m4_m5.py` (rungs up to `1.072` on $m=4$; `1.001` on $m=5, n=47$) + `verify_independent_milp.py` |
| **Problem B (Upper bound on $\kappa_m$)** | $\kappa_m \le 2m$ (Bárány–Grinberg) | **$\kappa_m \le m$** (strictly $< m \cdot D$ for every finite instance, support-preserving, exact polynomial-time Iterated Prefix Basis-Rounding), giving **$\kappa_3 \le 3$**, **$\kappa_4 \le 4$** | `verify_upper_bound_km.py` (exact `Fraction` Gaussian elimination, 126 instances) |
| **Open Problem 3 of `detector-chains` (Split optimality)** | Empirical 2000-trial LP sweep | **Completely resolved (Theorem 7):** $\max_{x \in [0,1]^{k-1}} \min\{f(x), g(x)\} = \min\{\tau_{\mathrm{bal}}(d),\, 1 + d_2\}$ for all nondecreasing $0 < d_2 \le \dots \le d_{k-1} \le 1$ via a 10-line dual identity | `verify_split_optimality_proof.py` (3007 exact rational vectors) |
| **$m = 3$ convex-hull obstruction** | Open whether 2D parallelogram invariant lifts to 3D | **Refuted in 3 columns:** $0 \notin \mathrm{conv}(R_3)$ on 3 rows ($|R_3| = 4$, every surviving state has $\Delta_B \ge 311/1500 > 0$) | `verify_small_rows_m4_m5.py` |

## Verify Everything

Standard library only (`fractions.Fraction`, no external solver):

```bash
python code/verify_split_optimality_proof.py   # Theorem 7 (Open Problem 3), 3007 vectors
python code/verify_cascade_and_pingpong.py     # Theorems 1, 2, 3 (1+1/e, 1+W(1), 1+ln 2; LB >= 1.681499)
python code/verify_small_rows_m4_m5.py         # Theorems 4 & 5 (m=5 n=47, m=4 to 1.072, m=3 obstruction)
python code/verify_upper_bound_km.py           # Theorem 6 (exact rational kappa_m <= m algorithm)
```

Independent MILP verification (requires `numpy` + `scipy` / HiGHS, allows all off-support assignments):

```bash
python code/verify_independent_milp.py         # 5 independent HiGHS infeasibility / min-max checks
```

## Full Technical Report

See [`REPORT.md`](REPORT.md) for complete proofs of Theorems 1–7, exact obstruction analyses for $m = 3$ and $\kappa < \infty$, and the classical/adjacent conjecture roadmap (Problem C).
