# Machine-dependent chairman assignment with few rows

**Author:** Angus Muffatti (AI-assisted).
**Status:** working notes with exact certificates, 22 November 2026. Not peer reviewed.
Companion to [`../chairman-counterexample/`](../chairman-counterexample/) and
[`../detector-chains/`](../detector-chains/).

## Question

The counterexamples to Liu–Reis Conjecture 3 use 11 rows or more, and the lower bound
`κ ≥ 1 + W(1/e)` uses a number of rows that grows with the target. Let `κ_m` be the same
constant for instances with `m` rows. What is `κ_m` for small `m`?

## Results

1. **`κ_2 ≥ 1` (proved).** The *rail family* `R_k` has two rows, `2k + 1` columns and all
   splits equal to `1/2`. Its min-max row-prefix discrepancy is exactly `1 − 2^−(k+1)`.
   With common weights the two-row value is `1/2`, so machine-dependent weights double it.
2. **The online problem is unbounded for two rows (proved).** An adaptive adversary forces
   any discrepancy. No online rule has a bounded guarantee, so a proof that `κ` is finite
   must use future columns.
3. **`κ_m ≤ 2m`** follows from the Bárány–Grinberg selection theorem (citation to verify).
4. **Conjecture: `κ_2 = 1`.** The Liu–Reis bound is then true and tight for two machines.
   Evidence: search for `n ≤ 16` columns finds nothing at or above 1, and the best values
   for `n ≤ 9` follow the exact pattern `1 − 2^−(k+1)` (odd `n`) and `1 − 2^−k / 3` (even `n`).
5. **Open: the least `m` with `κ_m > 1`.** It is between 3 and 11. Search with three and four
   rows found values above the two-row values at the same `n`, but none above 1.

Proofs and details: [`notes/two_rows.md`](notes/two_rows.md).

## Verify

```bash
python3 code/verify_rail_family.py 9   # exact: rail family, depth 0..9, 30 cases
python3 code/verify_instances.py       # exact: stored instances in data/
```

Both use the Python standard library only and run in a few seconds. Expected last lines:
`rail family verified exactly` and `stored instances verified exactly`.

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
- `code/verify_rail_family.py`, `code/verify_instances.py` — exact checks.
- `code/search_small_rows.c` — annealing search.
- `data/` — exact even-`n` two-row instances, best search instances, search log.

## Disclosure

The results, proofs, code and text in this folder were produced with AI assistance and
have not been independently audited.
