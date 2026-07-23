# Derivation of the machine-dependent chairman counterexample

## 1. Target statement

For rows `i`, ordered columns `j`, positive machine-dependent weights `d_ij`, a fractional assignment `x`, and an integral assignment `y`, define

```text
Delta_i(t) = sum_{j<=t} d_ij (x_ij-y_ij).
```

The conjectured bound is `|Delta_i(t)| <= D` for all rows and prefixes, where `D=max_ij d_ij`. We normalize `D=1`.

The main difficulty is that the integral assignment is not required to respect the support of `x`. The construction therefore gives every off-support pair a small positive weight `eta`, and its proof explicitly includes every off-support assignment.

## 2. One forcing block

A block has a decision column `J` and detector columns `K,L`, with fresh rows `A,H` and a global accumulator row `B`.

Choose parameters `p,a,q` and set

```text
J: x_A=1-p, x_B=p,       d_A=d_B=1;
K: x_A=x_H=1/2,          d_A=a, d_H=1;
L: x_A=1-q, x_H=q,       d_A=d_H=1.
```

All unlisted fractional entries are zero and all unlisted weights equal `eta>0`.

Suppose `J` is not assigned to `A`. Ignoring the small previous off-support loss, row `A` gains `1-p`.

If `K` is not assigned to `A`, row `A` gains another `a/2`. This already violates the unit bound when

```text
a/2 > p.
```

Thus a surviving assignment must send `K` to `A`. Then row `A` is at `1-p-a/2`, while row `H` gains `1/2`.

If `L` is assigned to `H`, row `A` gains `1-q`; if `L` is not assigned to `H`, row `H` gains `q`. Both choices violate when

```text
q > 1/2,
q < 1-p-a/2.
```

The feasible parameter region is therefore

```text
p < a/2,
1/2 < q < 1-p-a/2.
```

## 3. Closing the contradiction with an accumulator

Repeat the block `N` times using fresh detector rows `A_k,H_k`. Every discrepancy-good integral assignment is forced to send `J_k` to `A_k`. The accumulator `B` is then unassigned on every `J_k` and gains `p` per block.

There are only `2N` detector columns, so even if every one is assigned to `B` outside its fractional support, the total negative correction is at most `2N eta`. The final accumulator discrepancy is at least

```text
Np - 2N eta.
```

Choose parameters with `Np>1` and then choose `eta` small enough.

## 4. Exact rational values

Use

```text
N=5,
p=5/24,
a=1/2,
q=25/48,
eta=1/1000.
```

The three ideal forcing margins are

```text
a/2-p            = 1/24,
1-p-a/2-q        = 1/48,
q-1/2            = 1/48.
```

Before block `k`, a fresh detector row can have received at most `3(k-1)<=12` earlier columns outside its support, so its discrepancy is at least `-12 eta`. If `J_k` itself is assigned to `H_k`, that row can incur one additional loss, giving `-13 eta`.

The exact detector lower bounds are therefore

```text
K not sent to A: 25/24 - 12/1000 > 1;
L sent to H:     49/48 - 12/1000 > 1;
L not sent to H: 49/48 - 13/1000 = 6047/6000 > 1.
```

Hence every good assignment must send all five `J_k` columns to `A_k`. The accumulator then satisfies

```text
Delta_B(15) >= 5*(5/24)-10/1000 = 619/600 > 1.
```

This contradiction applies even when columns are assigned outside the support of `x`.

## 5. Final instance size

The rows are

```text
B,A1,H1,A2,H2,A3,H3,A4,H4,A5,H5,
```

and the columns are

```text
J1,K1,L1,...,J5,K5,L5.
```

Thus `m=11`, `n=15`, every fractional column has support size two, every weight is strictly positive, and the weight set is contained in `{1/1000,1/2,1}`.

Because no integral assignment at all satisfies the bound, the same instance also refutes any stronger support-preserving formulation with one selected row per column.
