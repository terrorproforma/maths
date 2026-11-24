# Machine-dependent chairman assignment with few rows

**Author:** Angus Muffatti (AI-assisted).
**Status:** working notes, 24 November 2026. Not peer reviewed. Theorems 1, 2 and 3 have
complete proofs below. Theorem 1 is machine-checked for depth 0 to 9, and the proof of
Theorem 3 is implemented as an exact algorithm that asserts each claim of the proof at
every step. Everything marked *numerical* is search evidence, not proof.

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
| `κ_2 ≤ 1`: with two rows there is always an assignment with all `|disc_i(t)| ≤ D` | **Theorem 3**, proved; proof run as an exact algorithm |
| `κ_m ≤ 2m` | Follows from the Bárány–Grinberg selection theorem (citation to verify, §6) |
| Smallest `m` with `κ_m > 1` | Open. `3 ≤ m* ≤ 11`; no instance above 1 found for `m = 3, 4` at small `n` |

**Corollary.** `κ_2 = 1`. The Liu–Reis conjecture (Conjecture 3 of arXiv:2511.18546) is
true for two machines, and the constant `D` cannot be lowered. It is false for eleven
machines (`chairman-counterexample/`). The supremum 1 is approached and, in all instances
found, not attained.

For comparison, with common weights (`d_ij = d_j`) and two rows the problem is
one-dimensional and the exact value is `1/2` (Tijdeman's `1 − 1/(2m−2)`). Machine-dependent
weights double it.

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

**Relation to known results.** All splits of `R_k` are `1/2`. For that case the upper bound
1 was known: it is the theorem of Lund and Magazinov for normed planes (§5). They note
that their bound is attained in the max-norm plane, by two vectors of mixed sign. The
rail family shows that the bound is also approached with non-negative vectors, which is
the case that two-row chairman instances produce.

## 4. Theorem 2: no online rule works, even for two rows

In the online problem the columns arrive one at a time, the scheduler must fix `y_j` when
column `j` arrives, and the adversary may choose column `j+1` after it sees `y_j`.

**Theorem 2.** For `m = 2` and every budget `c`, the adaptive adversary can force
`max_t ‖p_t‖_∞ > c`.

*Proof.* Let `L` be the set of points of `[−c, c]²` from which the adversary has a strategy
that forces the point out of `[−c, c]²` after finitely many columns, and let `W` be the rest
of `[−c, c]²`. If `p ∈ W`, then for every column `(h, w)` at least one of `p + (1−w)h`,
`p − wh` is in `W`; otherwise the adversary plays this column and continues with the
strategy of the point that is reached, so `p ∈ L`. Suppose `W ≠ ∅` and let `M = sup{p_1 : p ∈ W} ≤ c`. Fix an integer `K > 4c` and
`ε = 3^−K / 4`, and take `P ∈ W` with `P_1 > M − ε`.

Play the column `h = (4ε_i, 1)`, `w = 1/2`, where `ε_i = 3^i ε`, for `i = 0, …, K−1`.
Before step `i` the point is in `W` with first coordinate above `M − ε_i`. The move `+`
raises the first coordinate by `2ε_i`, above `M`, so it leaves `W`. Hence the move `−` must
stay in `W`: the first coordinate falls by `2ε_i`, so it is above `M − ε_{i+1}`, and the
second coordinate falls by `1/2`. After `K` steps the second coordinate has fallen by
`K/2 > 2c`, so the point is outside `[−c, c]²`, a contradiction. Hence `W = ∅`. In
particular the origin is in `L`. ∎

In the original variables the columns in the proof have `d_1j = 4ε_i`, `d_2j = 1`,
`x_1j = x_2j = 1/2`: all weights are positive.

**Consequence for the programme.** `detector-chains/` reports that a simple online rule
performs well on all constructed instances and suggests a potential-function analysis. By
Theorem 2 no purely online rule has a bounded guarantee, even for two rows. Any proof that
`κ` is finite must use knowledge of future columns. Equivalently, there is no bounded safe
region for single states; an invariant must be a property of a set of reachable states.
The proof of Theorem 3 uses such an invariant (a set of at most four states). Its
algorithm reads the columns once, but it keeps up to four partial assignments and chooses
between them only at the end.

## 5. Theorem 3: the bound `D` holds for two rows

**Theorem 3.** Let `m = 2`, weights `d_ij ∈ [0, D]` and any fractional assignment `x`. There
is an integral assignment `y` with `|disc_i(t)| ≤ D` for `i = 1, 2` and every prefix `t`.
The assignment can be chosen with `y_ij = 0` whenever `x_ij = 0`, and it is found in `O(n)`
arithmetic operations (with back-pointers for the four partial assignments; the reference
code copies lists and so does `O(n²)` list work).

Take `D = 1` and use the planar form: `h_j ∈ [0,1]²`, `w_j ∈ [0,1]`, and each column moves
the point by `+(1 − w_j) h_j` or `−w_j h_j`. Let `Q = [−1, 1]²`. Let `R_t` be the set of
points `p_t` that are reachable by a path with `p_1, …, p_t ∈ Q`. We must show `R_n ≠ ∅`.

**Invariant `I(t)`.** There are `g_1, g_2 ∈ [0,1]²` and `λ_1, λ_2 ∈ [0,1]` such that, with

```
π(ε) = (ε_1 − λ_1) g_1 + (ε_2 − λ_2) g_2,        ε ∈ {0,1}²,
```

every one of the four points `π(ε)` that lies in `Q` belongs to `R_t`.

The four points are the vertices of a parallelogram that has the origin in its convex
hull. A vertex outside `Q` carries no information. `I(0)` holds with `g_1 = g_2 = 0`.

**`I(t)` implies `R_t ≠ ∅`.** The point `π(1,0) = (1 − λ_1) g_1 − λ_2 g_2` has both
coordinates in `[−1, 1]`, because `g_1, g_2 ∈ [0,1]²`. So it lies in `Q`, hence in `R_t`.
The same holds for `π(0,1)`.

**Step.** Assume `I(t)`. Let `g_3 = h_{t+1}`, `λ_3 = w_{t+1}`, and for `ε ∈ {0,1}³` put

```
P(ε) = Σ_{i=1..3} (ε_i − λ_i) g_i = π(ε_1, ε_2) + (ε_3 − λ_3) g_3 .
```

If `π(ε_1, ε_2) ∈ R_t` and `P(ε) ∈ Q`, then `P(ε) ∈ R_{t+1}`: extend the path with
`y_{t+1} = ε_3`. Call `ε` **bad** if `P(ε) ∈ Q` but `π(ε_1, ε_2) ∉ Q`. If `ε` is not bad and
`P(ε) ∈ Q`, then `π(ε_1,ε_2) ∈ Q`, so `π(ε_1,ε_2) ∈ R_t` by `I(t)`, so `P(ε) ∈ R_{t+1}`.

*Claim B. A bad vertex is `(0,0,1)` or `(1,1,0)`, and at most one of the two is bad.*
The points `π(1,0)`, `π(0,1)` are always in `Q`, so no vertex `(1,0,·)` or `(0,1,·)` is bad. The point `π(0,0) = −λ_1 g_1 − λ_2 g_2` has
non-positive coordinates; if it is outside `Q`, a coordinate is below `−1`, and the same
coordinate of `P(0,0,0) = π(0,0) − λ_3 g_3` is below `−1`, so `(0,0,0)` is not bad. In the
same way `(1,1,1)` is not bad. If both `(0,0,1)` and `(1,1,0)` were bad, then `π(0,0) ∉ Q`
gives `λ_1 + λ_2 > 1` (a coordinate of `λ_1 g_1 + λ_2 g_2` exceeds 1) and `π(1,1) ∉ Q` gives
`(1 − λ_1) + (1 − λ_2) > 1`, a contradiction.

*Lemma M. Among three vectors in the closed positive quadrant, one is a non-negative
combination of the other two.* A zero vector is such a combination. If all three are
non-zero, order them by angle; the middle one lies in the cone of the other two (or all
three are parallel).

Fix names `{α, β, γ} = {1, 2, 3}` and numbers `ρ, σ ≥ 0` with `g_β = ρ g_α + σ g_γ`. So `β` is
the index of the "middle" generator. The relation is symmetric in `(α, ρ)` and `(γ, σ)`.

*Lemma T. (i) There is `τ ≥ 0` such that the triple `μ` with

```
μ_α = λ_α − τρ,    μ_β = λ_β + τ,    μ_γ = λ_γ − τσ
```

lies in `[0,1]³` and: `μ_β = 1`, or `ρ > 0` and `μ_α = 0`, or `σ > 0` and `μ_γ = 0`.
(ii) There is `τ ≥ 0` such that the triple `μ` with

```
μ_α = λ_α + τρ,    μ_β = λ_β − τ,    μ_γ = λ_γ + τσ
```

lies in `[0,1]³` and: `μ_β = 0`, or `ρ > 0` and `μ_α = 1`, or `σ > 0` and `μ_γ = 1`.
In both cases `Σ μ_i g_i = Σ λ_i g_i`.* Take the largest `τ` that keeps the three coordinates
in `[0,1]`; it is finite because of the coordinate `β`, and the constraint that stops it is
one of the three listed. The sum does not change because `g_β − ρ g_α − σ g_γ = 0`.

If `μ ∈ [0,1]³`, `Σ μ_i g_i = Σ λ_i g_i` and `μ_k = v ∈ {0,1}`, then `0 = Σ (μ_i − λ_i) g_i` is a
convex combination of the four points `P(ε)` with `ε_k = v`: the point `P(ε)` has weight
`Π_{i ≠ k} (μ_i if ε_i = 1, else 1 − μ_i)`. So each outcome of Lemma T gives a face
`{ε_k = v}` of the cube whose four points have the origin in their convex hull: `μ_β = 1`
gives `{ε_β = 1}`, `μ_α = 0` gives `{ε_α = 0}`, and so on.

*Claim F. There are `k ∈ {1,2,3}`, `v ∈ {0,1}` and `μ ∈ [0,1]³` with `μ_k = v` and
`Σ μ_i g_i = Σ λ_i g_i`, such that the face `{ε_k = v}` contains no bad vertex.* (By the last
paragraph the four points of this face have the origin in their convex hull.)

- No bad vertex: use Lemma T (i).
- `(0,0,1)` is bad. The faces without this vertex are `{ε_3 = 0}`, `{ε_1 = 1}`, `{ε_2 = 1}`.
  - If `β = 3` (the new generator is the middle one), Lemma T (ii) gives `μ_3 = 0`, `μ_α = 1`
    or `μ_γ = 1`, with `α, γ ∈ {1, 2}`. All three faces are permitted.
  - If `β ≠ 3`, name the indices so that `γ = 3`; then `α, β ∈ {1, 2}`. Lemma T (i) gives
    `μ_β = 1` or `μ_3 = 0`, both permitted, or `ρ > 0` and `μ_α = 0`. In the last case
    `τ = λ_α / ρ`, so `λ_α g_α = τ (g_β − σ g_3)` and

    ```
    π(0,0) = −λ_α g_α − λ_β g_β = −(λ_β + τ) g_β + τσ g_3 = −μ_β g_β + (λ_3 − μ_3) g_3 .
    ```

    Both coefficients `μ_β` and `λ_3 − μ_3 = τσ` lie in `[0, 1]` (the second because
    `0 ≤ μ_3 ≤ λ_3`). So each coordinate of `π(0,0)` lies in `[−1, 1]`, that is `π(0,0) ∈ Q`.
    This contradicts that `(0,0,1)` is bad.
- `(1,1,0)` is bad. The faces without this vertex are `{ε_3 = 1}`, `{ε_1 = 0}`, `{ε_2 = 0}`.
  - If `β = 3`, Lemma T (i) gives `μ_3 = 1`, `μ_α = 0` or `μ_γ = 0`. All are permitted.
  - If `β ≠ 3` and `γ = 3`, Lemma T (ii) gives `μ_β = 0` or `μ_3 = 1`, both permitted, or
    `ρ > 0` and `μ_α = 1`. In the last case `τ = (1 − λ_α) / ρ`, so
    `(1 − λ_α) g_α = τ (g_β − σ g_3)` and

    ```
    π(1,1) = (1 − λ_α) g_α + (1 − λ_β) g_β = (1 − μ_β) g_β − (μ_3 − λ_3) g_3 .
    ```

    Both coefficients `1 − μ_β` and `μ_3 − λ_3 = τσ` lie in `[0, 1]`. So `π(1,1) ∈ Q`. This
    contradicts that `(1,1,0)` is bad.

**End of the step.** Take `k`, `v` and `μ` from Claim F. Let `{i, j} = {1,2,3} ∖ {k}`. For `ε` in the face,
`P(ε) = (ε_i − μ_i) g_i + (ε_j − μ_j) g_j`, because `Σ (μ_l − λ_l) g_l = 0` gives
`(v − λ_k) g_k = −(μ_i − λ_i) g_i − (μ_j − λ_j) g_j`.
No vertex of the face is bad, so each `P(ε)` in `Q` is in `R_{t+1}`. Hence `I(t+1)` holds with
generators `g_i, g_j` and coefficients `μ_i, μ_j`. ∎

**Support.** If `w_{t+1} = 0`, the move "column to row 2" does not move the point, and the
old parallelogram satisfies `I(t+1)`. The same holds for `w_{t+1} = 1`. So `y` can respect
the support of `x`.

**Algorithm and check.** `code/two_row_algorithm.py` stores the parallelogram and one
partial assignment for each vertex in `Q`, and follows the proof. It asserts Claim B,
Lemma M, Lemma T, Claim F and the invariant at every step, in exact rational arithmetic.
`code/verify_two_row_theorem.py` runs it on the rail family and on 20,000 random instances
of four kinds with up to 80 columns (40,048 runs), checks that each output has all
discrepancies at most 1, and compares 2,665 small instances with exhaustive search. The
"largest value seen" that it prints is the worst output of the algorithm, which is not
optimal; it is not the min-max of an instance.

**Independent check (24 November 2026).** A separate reviewer session re-derived each step
and found no error. It also ran its own exact brute force on 18,000 random instances with
up to 14 columns and on all 331,776 four-column instances with weights in `{0, 1/2, 1}` and
splits in `{1/3, 1/2, 2/3}`, and tested Claims B and F and Lemmas M and T on 300,000
arbitrary states. This was an AI review, not a human audit.

**Where the idea comes from.** The proof is a version of the *trapping families* of Lund
and Magazinov (arXiv:1510.04536). They prove that in any normed plane a sequence of
vectors of norm at most 1 has signs with all partial sums of norm at most 2. In our scale
this is the case "all splits equal to `1/2`" of Theorem 3, for vectors of any direction.
Their sets are centrally symmetric parallelograms. For general splits the parallelogram
is not symmetric, and two things change: a vertex may leave `Q`, and the direction of the
vectors matters.

**The non-negative weights are necessary.** If the vectors `h_j` may have mixed signs
(sup norm at most 1), the bound 1 fails for general splits. `data/mixed_sign_example.json`
has six vectors with exact min-max `15/14`. Such a column is not a chairman column, so
this does not concern `κ_m`; it shows that Theorem 3 does not follow from the symmetric
theorem by a general argument. A general argument does give a weaker bound: the
symmetric theorem and the Lovász–Spencer–Vesztergombi inequality (linear discrepancy is
at most hereditary discrepancy) give 2 in place of 1.

**What does not extend.** Lemma M is a fact about the plane. With `m ≥ 3` rows the state has
`m` coordinates and three generators need not be dependent.

## 6. Upper bounds from the literature

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
cannot work (Theorem 2), and that the conjectured bound `D` is true for two rows
(Theorem 3).

## 7. Numerical evidence (not certified unless stated)

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
`n = 10..16` the search stalls near `0.983`, below the rail value for the same `n`. By
Theorem 3 no two-row instance exceeds 1. The pattern suggests

```
best(2k+1) = 1 − 2^−(k+1),        best(2k+2) = 1 − 2^−k / 3.
```

Three and four rows: see `data/search_log.md`. At small `n` more rows give larger values:
for `m = 3` the search finds about `6/7`, `9/10` and `0.9435` at `n = 4, 5, 7`, against
`5/6`, `7/8` and `15/16` for two rows, and `m = 4` gives `0.9283` at `n = 6` against
`11/12`. No instance at or above 1 was found for `m = 3`, `n ≤ 11` or `m = 4`, `n ≤ 7`. The
search does not converge for `n ≥ 8`, so this is not evidence that `κ_3 ≤ 1`.

## 8. Open problems

1. **Find `m*`, the least `m` with `κ_m > 1`.** It is between 3 and 11. The chain needs a row
   at height near 1 *before* the two-row dynamics start; this is what the accumulator and
   the detector column supply. With three rows the blocks must reuse their rows, so the
   entry state must be pinned. Is `κ_3 = 1`?
2. **Is the value 1 attained with two rows?** All instances found have min-max below 1, and
   the best values follow `1 − 2^−(k+1)` (odd `n`) and `1 − 2^−k / 3` (even `n`).
3. **A stronger two-row statement.** Search suggests that one can also keep
   `|disc_1(t) + disc_2(t)| ≤ D`, that is, stay in the hexagon
   `max(|p_1|, |p_2|, |p_1 − p_2|) ≤ 1`. The invariant of Theorem 3 does not prove this: its
   closure fails for the hexagon in random tests.
4. **Growth of `κ_m`.** Between `κ_m ≥ 1` and `κ_m ≤ 2m` nothing is known for `3 ≤ m ≤ 10`.
