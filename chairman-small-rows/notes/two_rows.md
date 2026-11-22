# Machine-dependent chairman assignment with few rows

**Author:** Angus Muffatti (AI-assisted).
**Status:** working notes, 22 November 2026. Not peer reviewed. Theorems 1 and 2 have short
proofs below and Theorem 1 is also machine-checked for depth 0 to 9. Everything marked
*numerical* is search evidence, not proof.

## 1. Setting

Rows `i = 1..m`, columns `j = 1..n`, weights `d_ij ≥ 0` with `D = max d_ij = 1`, a fractional
assignment `x` (each column sums to 1) and an integral assignment `y` (each column goes to
one row). The row-prefix discrepancy is

```
disc_i(t) = Σ_{j ≤ t} d_ij (x_ij − y_ij).
```

Define

```
κ_m = sup over instances with m rows of  min_y  max_{i,t} |disc_i(t)|,        κ = sup_m κ_m.
```

Liu and Reis (arXiv:2511.18546, Conjecture 3) conjectured `κ ≤ 1`. The companion folders
`chairman-counterexample/` and `detector-chains/` refute this with 11 rows and prove
`κ ≥ 1 + W(1/e) ≈ 1.2785`. Those constructions use a number of rows that grows with the
target value. These notes ask what happens when `m` is small.

### Two rows as a planar walk

For `m = 2` write `w_j = x_1j`, `a_j = d_1j`, `b_j = d_2j`, `h_j = (a_j, b_j) ∈ [0,1]²`, and
put `p_t = (−disc_1(t), disc_2(t))`. Then, with `y_j = 1` when column `j` goes to row 1,

```
p_t = Σ_{j ≤ t} (y_j − w_j) h_j .
```

So each column offers two moves from the current point `p`: `p + (1 − w) h` or `p − w h`.
The two end points differ by exactly `h`, a vector in the closed positive quadrant with
sup norm at most 1. The quantity to control is `max_t ‖p_t‖_∞`. In this form `κ_2` is the
prefix linear discrepancy of non-negative `2 × n` matrices with entries in `[0, 1]`.

## 2. Results

| Statement | Status |
|---|---|
| `κ_2 ≥ 1`: an explicit family with `2k+1` columns has min-max exactly `1 − 2^−(k+1)` | **Theorem 1**, proved; exact check for `k ≤ 9` |
| The online problem is unbounded already for `m = 2` | **Theorem 2**, proved |
| `κ_m ≤ 2m` | Follows from the Bárány–Grinberg selection theorem (citation to verify, §5) |
| `κ_2 = 1`, and the value 1 is not attained | **Conjecture**, numerical evidence (§4) |
| Smallest `m` with `κ_m > 1` | Open. `3 ≤ m* ≤ 11`; no instance above 1 found for `m = 3, 4` at small `n` |

For comparison, with common weights (`d_ij = d_j`) and two rows the problem is one-dimensional
and the exact value is `1/2` (Tijdeman's `1 − 1/(2m−2)`). Machine-dependent weights double
it. So the Liu–Reis bound `D` is conjecturally **true and tight** for two machines, although
it fails for eleven.

## 3. Theorem 1: the rail family

**Instance `R_k(η)`.** Two rows, `n = 2k + 1` columns, every split `w_j = 1/2`. In the planar
form the vectors `h_j` are

```
(1, η),   then for i = k, k−1, …, 1:   (1 − 2^−i, 1),  (1, 1).
```

**Theorem 1.** For every `k ≥ 0` and every `0 ≤ η ≤ 2^−k`, the min-max row-prefix
discrepancy of `R_k(η)` is exactly `T_k = 1 − 2^−(k+1)`. Hence `κ_2 ≥ 1`. With `η > 0` all
weights are strictly positive.

*Proof.* All splits are `1/2`, so each column moves the point by `± h/2`, and the instance is
invariant under `p ↦ −p`. After column 0 the point is `±(1/2, η/2)`; by symmetry take
`(1/2, η/2)`.

Number the pairs `j = 0, …, k−1` in order, so pair `j` has `ε_j = 2^{j−k}` and vectors
`(1 − ε_j, 1)`, `(1, 1)`. Put

```
u_j = 1/2 + (2^j − 1) 2^−(k+1),        S_j = (u_j, η/2).
```

Then `S_0 = (1/2, η/2)`. Suppose the point is `S_j` before pair `j`. There are four ways to
play the pair.

- First move `+`. The first coordinate becomes `u_j + (1 − ε_j)/2 = 1 − 2^−(k+1) = T_k`.
- Moves `−, −`. The second coordinate becomes `η/2 − 1`, of absolute value
  `1 − η/2 ≥ T_k` because `η ≤ 2^−k`.
- Moves `−, +`. The point becomes `(u_j + ε_j/2, η/2) = S_{j+1}`.

So a path either reaches sup norm at least `T_k` inside some pair, or it arrives at
`S_k = (T_k, η/2)`, of sup norm `T_k`. Every path therefore has a prefix of norm at least
`T_k`. The path "`+`, then `−, +` in every pair" has all prefixes of norm at most `T_k`: its
points are `S_j` and `(u_j − (1 − ε_j)/2, η/2 − 1/2)`, and `0 < u_j − (1−ε_j)/2 < 1/2`. ∎

The condition on `η` is necessary: `R_7(1/100)` has value `199/200 = 1 − η/2`.

**What the family shows.** The scheduler is confined to a "rail" `v = η/2`: each pair gives it
a move of size `1/2` in the second coordinate that it must undo at once, and each pair
lifts the first coordinate by `ε_j/2`. This is the same creeping mechanism as the detector
chain, but it needs no fresh rows and no accumulator, and it stops exactly at 1.

`code/verify_rail_family.py` checks the theorem by exhaustive exact search for `k = 0..9`
and `η ∈ {0, 2^−k, 10^−6}` (30 cases).

## 4. Theorem 2: no online rule works, even for two rows

In the online problem the columns arrive one at a time, the scheduler must fix `y_j` when
column `j` arrives, and the adversary may choose column `j+1` after it sees `y_j`.

**Theorem 2.** For `m = 2` and every budget `c`, the adaptive adversary can force
`max_t ‖p_t‖_∞ > c`.

*Proof.* Let `W` be the set of points from which the scheduler can stay in `[−c, c]²` for
ever. If `p ∈ W`, then for every column `(h, w)` at least one of `p + (1−w)h`, `p − wh` is in
`W`. Suppose `W ≠ ∅` and let `M = sup{p_1 : p ∈ W} ≤ c`. Fix an integer `K > 4c` and
`ε = 3^−K / 4`, and take `P ∈ W` with `P_1 > M − ε`.

Play the column `h = (4ε_i, 1)`, `w = 1/2`, where `ε_i = 3^i ε`, for `i = 0, …, K−1`.
Before step `i` the point is in `W` with first coordinate above `M − ε_i`. The move `+`
raises the first coordinate by `2ε_i`, above `M`, so it leaves `W`. Hence the move `−` must
stay in `W`: the first coordinate falls by `2ε_i`, so it is above `M − ε_{i+1}`, and the
second coordinate falls by `1/2`. After `K` steps the second coordinate has fallen by
`K/2 > 2c`, so the point is outside `[−c, c]²`, a contradiction. Hence `W = ∅`. In
particular the origin is not in `W`. ∎

In the original variables the columns in the proof have `d_1j = 4ε_i`, `d_2j = 1`,
`x_1j = x_2j = 1/2`: all weights are positive.

**Consequence for the programme.** `detector-chains/` reports that a simple online rule
performs well on all constructed instances and suggests a potential-function analysis. By
Theorem 2 no purely online rule has a bounded guarantee, even for two rows. Any proof that
`κ` is finite, or that `κ_2 ≤ 1`, must use knowledge of future columns. Equivalently, there
is no bounded safe region for single states; an invariant must be a property of the whole
set of reachable states.

## 5. Upper bounds from the literature

- **`κ_m ≤ 2m`.** Bárány's survey on the Steinitz lemma states the selection version of the
  Bárány–Grinberg theorem: given sets `V_j` in the unit ball of a `d`-dimensional norm with
  `0 ∈ conv V_j`, one can choose `u_j ∈ V_j` with all partial sums of norm at most `2d`.
  For column `j` take `V_j = { (d_ij x_ij)_i − d_rj e_r : r = 1..m }`. Each vector has sup
  norm at most 1, and the combination with coefficients `x_rj` is zero. So `κ_m ≤ 2m`, and
  `κ_2 ≤ 4`. *To verify against the source before use in a manuscript.*
- The `O(√log n)` bound of Banaszczyk type is stated in the literature for the common-weight
  conjecture. For machine-dependent weights the flow-time paper of Bansal, Rohwedder and
  Svensson states it as a one-sided integrality gap. The two-sided statement is not written
  as a theorem there. *Not verified.*
- The offline Komlós and Beck–Fiala conjectures were proved in September 2026
  (arXiv:2609.11189, arXiv:2609.20979) for the final sum only. The prefix version with
  `ℓ1`-bounded columns, including sparsity 2, is still open.

**Proposed correction to `detector-chains/paper/kappa_chains.tex`.** Open problem 1 says "Any
finite upper bound would be the first". Change this to "any upper bound independent of `m`
and `n`", and cite `κ_m ≤ 2m`. Section 6 should also say that an online potential argument
cannot work (Theorem 2).

## 6. Numerical evidence (not certified unless stated)

Simulated annealing over instances, with exact depth-first evaluation of each candidate in
floating point (`code/search_small_rows.c`). Values are the best found; they are lower bounds
on the true optimum for that size only if the instance is re-checked exactly.

Two rows, best value found for `n` columns:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| best found | 1/2 | 2/3 | 3/4 | 5/6 | 7/8 | 11/12 | 15/16 | 0.9580 | 0.9685 |
| pattern | 1/2 | 2/3 | 3/4 | 5/6 | 7/8 | 11/12 | 15/16 | 23/24 | 31/32 |

The odd entries are the rail family. The even entries `n = 2, 4, 6` have exact rational
instances in `data/two_row_even.json`, checked by `code/verify_instances.py`. For
`n = 10..16` the search stalls near `0.983`, below the rail value for the same `n`; no
two-row instance at or above 1 was found. The pattern suggests

```
best(2k+1) = 1 − 2^−(k+1),        best(2k+2) = 1 − 2^−k / 3.
```

Three and four rows: see `data/search_log.md`. At small `n` more rows give larger values:
for `m = 3` the search finds about `6/7`, `9/10` and `0.9397` at `n = 4, 5, 7`, against
`5/6`, `7/8` and `15/16` for two rows, and `m = 4` gives `0.9283` at `n = 6` against
`11/12`. No instance at or above 1 was found for `m = 3`, `n ≤ 11` or `m = 4`, `n = 6`. The
search does not converge for `n ≥ 8`, so this is not evidence that `κ_3 ≤ 1`.

A local search started from the rail family (`n = 7, 9, 11, 13`) found no improvement.

## 7. Open problems, in order of attack

1. **Prove `κ_2 ≤ 1`.** By Theorem 2 the proof must be offline. In the planar form the
   dangerous regions are the top-left and bottom-right corners of the square; a single
   state in the band `|p_1 − p_2| ≤ 1` cannot be killed by one column, but can be driven
   out of the band. The invariant must concern the set of reachable states.
2. **Find `m*`, the least `m` with `κ_m > 1`.** The chain needs a row at height near 1
   *before* the two-row dynamics start; this is what the accumulator and the detector column
   supply. With three rows the blocks must reuse their rows, so the entry state must be
   pinned. The rail forces exact states and is a candidate pinning device.
3. **Growth of `κ_m`.** Between `κ_2 ≥ 1` and `κ_m ≤ 2m` nothing is known.
