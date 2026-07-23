# Mathematical audit report

Audit date: **23 July 2026**.

## Flow certificate

### Definitions checked

- Costs are nonnegative per-unit arc costs, so a terminal routed on path `P` contributes `d_i * sum_{a in P} c_a`.
- The claimed additive rule is `y_a <= x_a + D`, with `D=max_i d_i=15`.
- The graph is acyclic and all terminals are sinks.
- Setting capacities equal to `x` makes the displayed fractional flow feasible; the conjecture concerns rounding that fixed flow.

### Arithmetic checked

- Source outflow: `10+6+24=40`.
- Internal conservation: `24=10+14`, `14=5+9`, `9=4+5`.
- Terminal inflows: `10+5=15`, `6+4=10`, `10+5=15`.
- Fractional cost: `2*10+3*6+2*10=58`.
- Additive thresholds on the three conflict arcs: `39,29,24`.
- Pair loads: `40,30,25`; every conflict exceeds its threshold by exactly one.
- Every routing using at most one cheap path satisfies all arc bounds.
- Each expensive integral choice costs 30, so the minimum good routing cost is 60.

### Completeness checked

A direct DFS on the nine-arc graph returns exactly two paths for each terminal. Therefore the Cartesian product has exactly eight routings. The verifier recomputes this rather than trusting a prescribed path list.

### Topology checked

The graph has a planar embedding. In its underlying undirected graph, suppressing the degree-two terminals produces `K4`, so it is a `K4` subdivision and not series-parallel.

### Robustness checked

The all-positive-cost perturbation gives fractional cost 409 and good integral optimum 415. The counterexample therefore does not depend on zero arc costs.

### Statements deliberately not made

- The Dinitz–Garg–Goemans theorem is not false; only the cost-preserving strengthening is refuted.
- The example does not refute the costless Morell–Skutella simultaneous lower/upper existence conjecture.
- No claim is made that `9/8` is the optimal planar factor; only `9/8 <= alpha_planar <= 2` is established.

## Chairman certificate

### Instance checked

- `m=11`, `n=15`.
- Every fractional column sums to one and has support exactly two.
- Every weight is positive and belongs to `{1/1000,1/2,1}`.
- The maximum weight is `D=1`.

### Local forcing checked

For the fifth and therefore worst block, the three strict lower bounds are

```text
-12/1000 + 25/24              > 1,
-12/1000 + 49/48              > 1,
-13/1000 + 49/48              > 1.
```

Thus the proof has positive slack after accounting for every possible earlier off-support assignment to a fresh detector row.

### Accumulator checked

Five forced decision columns give `25/24`; ten possible off-support detector assignments can subtract at most `10/1000`. The exact lower bound is

```text
25/24 - 1/100 = 619/600 > 1.
```

The proof permits assignments outside the fractional support. It therefore refutes Conjecture 19 itself and, a fortiori, the support-preserving Conjecture 21.

### Independent model

The SciPy script scales the rational model by 6000. All MILP coefficients and bounds are integers. It imposes one assignment equality per column and one two-sided interval constraint per row and prefix. A valid independent run must terminate with HiGHS status `infeasible` rather than a time limit.

## Remaining review obligations

The finite certificates are internally consistent, but the results are new and not yet journal-refereed. A submitting author should obtain expert review of the exact conjecture formulations, priority, and bibliographic framing; rerun the code in a clean environment; and inspect the compiled manuscript page by page.
