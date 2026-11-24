# Machine-dependent chairman assignment with few rows

**Author:** Angus Muffatti (AI-assisted).
**Status:** working notes with proofs and exact checks, 24 November 2026. Not peer reviewed.
Companion to [`../chairman-counterexample/`](../chairman-counterexample/) and
[`../detector-chains/`](../detector-chains/).

## Question

The counterexamples to Liu–Reis Conjecture 3 use 11 rows or more, and the lower bound
`κ ≥ 1 + W(1/e)` uses a number of rows that grows with the target. Let `κ_m` be the same
constant for instances with `m` rows. What is `κ_m` for small `m`?

## Results

1. **`κ_2 = 1` (proved).** With two rows there is always an integral assignment with every
   row-prefix discrepancy at most `D` (Theorem 3), and no smaller constant works
   (Theorem 1). So the Liu–Reis conjecture is true for two machines, although it is false
   for eleven. The assignment respects the support of `x` and is found in linear time.
   - *Upper bound.* The proof keeps a parallelogram of reachable states that has the
     origin in its convex hull, and shows that each new column leaves such a
     parallelogram. It adapts the trapping families of Lund and Magazinov
     (arXiv:1510.04536) to unequal splits. The proof is implemented as an exact algorithm
     that asserts each claim at every step.
   - *Lower bound.* The *rail family* `R_k` has two rows, `2k + 1` columns and all splits
     equal to `1/2`. Its min-max row-prefix discrepancy is exactly `1 − 2^−(k+1)`. With
     common weights the two-row value is `1/2`.
2. **The online problem is unbounded for two rows (proved).** An adaptive adversary forces
   any discrepancy. No online rule has a bounded guarantee, so a proof that `κ` is finite
   must use future columns.
3. **`κ_m ≤ 2m`** follows from the Bárány–Grinberg selection theorem (citation to verify).
4. **Open: the least `m` with `κ_m > 1`.** It is between 3 and 11. Search with three and four
   rows found values above the two-row values at the same `n`, but none above 1.

Proofs and details: [`notes/two_rows.md`](notes/two_rows.md).

## Verify

```bash
python3 code/verify_rail_family.py 9        # exact: rail family, depth 0..9, 30 cases
python3 code/verify_two_row_theorem.py      # exact: proof of Theorem 3 run on 40,048 instances
python3 code/verify_instances.py            # exact: stored instances in data/
```

All use the Python standard library only. The first and third run in a few seconds, the
second in about two minutes (`verify_two_row_theorem.py 2000` is a 15-second version).
Expected last lines: `rail family verified exactly`,
`two-row theorem verified on all test instances`, `stored instances verified exactly`.

## Search (not a proof)

```bash
gcc -O2 -o search code/search_small_rows.c -lm
./search 3 7 1 150000        # m rows, n columns, seed, annealing steps per restart
```

The search prints each new best instance and runs until it is stopped. Its values are
floating point. `data/search_best.json` holds the best instances found, and
`verify_instances.py` computes the exact value of each stored instance.

## Layout

- `notes/two_rows.md` — statements, proofs, literature status, open problems.
- `code/minmax.py` — exact exhaustive evaluator for any number of rows.
- `code/two_row_algorithm.py` — the proof of Theorem 3 as an exact algorithm.
- `code/verify_rail_family.py`, `code/verify_two_row_theorem.py`,
  `code/verify_instances.py` — exact checks.
- `code/search_small_rows.c` — annealing search.
- `data/` — exact even-`n` two-row instances, best search instances, a mixed-sign example
  that shows the non-negative weights are necessary, and the search log.

## Disclosure

The results, proofs, code and text in this folder were produced with AI assistance and
have not been independently audited.
