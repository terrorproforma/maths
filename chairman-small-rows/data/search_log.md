# Search log, 22 November 2026

Tool: `code/search_small_rows.c` (simulated annealing over instances, exhaustive
branch-and-bound evaluation of each candidate, floating point). Machine: 4 cores.
All values have `D = 1`. "Exact" is the exact min-max of the stored decimal instance in
`search_best.json`, computed by `code/verify_instances.py`.

## Three and four rows

| m | n | run time | value printed by search | exact value of stored instance | two-row value at same n |
|---|---|---|---|---|---|
| 3 | 4 | 270 s | 0.857121 | 0.857058 | 5/6 = 0.8333 |
| 3 | 5 | 270 s | 0.899745 | 0.899700 | 7/8 = 0.8750 |
| 3 | 6 | 270 s | 0.916309 | 0.916286 | 11/12 = 0.9167 |
| 3 | 7 | 1500 s | 0.939729 | 0.939700 | 15/16 = 0.9375 |
| 3 | 8 | 1500 s | 0.957956 | 0.958000 | 23/24 = 0.9583 |
| 3 | 9 | 1500 s | 0.967126 | 0.967100 | 31/32 = 0.9688 |
| 3 | 10 | 270 s | 0.936559 | not stored | 0.9792 (pattern) |
| 3 | 11 | 270 s | 0.945386 | not stored | 63/64 = 0.9844 |
| 4 | 6 | 1500 s | 0.928331 | 0.928300 | 11/12 = 0.9167 |

Reading: for `n = 4, 5, 7` three rows give more than two rows, and four rows give more than
three at `n = 6`. The likely exact values at `m = 3` are `6/7` (`n = 4`) and `9/10`
(`n = 5`); these are guesses from the decimals. For `n ≥ 8` the three-row search does not
reach the two-row value, so it has not converged. No instance at or above 1 was found.

## Two rows

Random-start annealing, `n = 3..16`: best values `3/4, 5/6, 7/8, 11/12, 15/16` for
`n = 3..7`, then `0.9580, 0.9685, 0.9744` for `n = 8, 9, 10` and about `0.983` for
`n = 12, 14, 16` (not converged; the rail family gives more for odd `n`).

Local search started from the rail family, `n = 7, 9, 11, 13`, 150 s each: no improvement
on the rail value. The rail family is a local optimum for the moves tried.
