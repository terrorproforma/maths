# Derivation of the machine-dependent chairman counterexample

## 1. Desired forcing pattern

The goal is to force one designated decision in each block while making the forced decisions accumulate on a common row.

A block uses fresh rows `A_k,H_k`, one global row `B`, and columns `J_k,K_k,L_k`.

- `J_k` is the decision column. If it is assigned to `A_k`, row `B` gains a positive discrepancy increment.
- If `J_k` is not assigned to `A_k`, the detector columns `K_k,L_k` make every continuation violate a prefix bound.
- Repeating the block forces enough increments on `B` to exceed the maximum weight.

## 2. Two-parameter idealized gadget

Ignore small off-support weights temporarily. Let

```text
J: x_A=1-p, x_B=p, both weights 1;
K: x_A=x_H=1/2, weights d_A=1/2, d_H=1;
L: x_A=1-q, x_H=q, both weights 1.
```

Suppose `J` is not assigned to `A`.

- Row `A` gains `1-p`.
- If `K` is not assigned to `A`, it gains another `1/4`; forcing at `K` requires `1-p+1/4>1`, i.e. `p<1/4`.
- If `K` is assigned to `A`, row `A` becomes `3/4-p` and row `H` becomes `1/2`.
- If `L` is assigned to `H`, row `A` gains `1-q`; forcing requires `(3/4-p)+(1-q)>1`, i.e. `p+q<3/4`.
- If `L` is not assigned to `H`, row `H` gains `q`; forcing requires `1/2+q>1`, i.e. `q>1/2`.

Thus the open parameter region is

```text
p < 1/4,
q > 1/2,
p+q < 3/4.
```

Five repetitions can defeat a unit bound when `5p>1`, so choose `p>1/5` inside this region.

## 3. Rational choice and strictly positive off-support weights

Take

```text
p = 5/24,
q = 25/48,
eta = 1/1000.
```

Then

```text
1-p = 19/24,
1-q = 23/48.
```

All unspecified weights are set to `eta`, rather than zero. This makes every `d_ij` strictly positive, as required by the conjecture. Off-support assignments can lower a fresh detector row by at most one `eta` per earlier column.

Before block `k`, there are at most `3(k-1)<=12` earlier columns. Therefore each fresh detector row starts in `[-12 eta,0]`.

## 4. Exact forcing inequalities

Assume `J_k` is not assigned to `A_k`.

After `J_k`:

```text
Delta_A >= -12 eta + 19/24,
Delta_H >= -13 eta.
```

If `K_k` is not assigned to `A_k`, then

```text
Delta_A >= -12 eta + 19/24 + 1/4
        = -12 eta + 25/24
        > 1.
```

Thus `K_k` must be assigned to `A_k`. Afterwards,

```text
Delta_A >= -12 eta + 13/24,
Delta_H >= -13 eta + 1/2.
```

If `L_k` is assigned to `H_k`, then `A_k` is unassigned and

```text
Delta_A >= -12 eta + 13/24 + 23/48
        = 49/48 - 12 eta
        > 1.
```

If `L_k` is not assigned to `H_k`, then `H_k` is unassigned and

```text
Delta_H >= -13 eta + 1/2 + 25/48
        = 49/48 - 13 eta
        > 1.
```

Hence every placement of `L_k` violates. The assumption was false, so every good assignment must send `J_k` to `A_k`.

## 5. Accumulator

Because `J_k` is assigned to `A_k`, row `B` is unassigned and gains `5/24` in every block. The ten `K/L` columns can each reduce `B` by at most `eta` if assigned there. At the final prefix,

```text
Delta_B >= 5*(5/24) - 10/1000
        = 619/600
        > 1.
```

No assignment obeys all unit prefix bounds. Since this proof permits arbitrary off-support assignments, it refutes the unrestricted machine-dependent conjecture and therefore also the support-preserving unified conjecture.

## 6. Why common column weights survive

With a common weight `d_j` in each column, discrepancies across rows sum to zero at every prefix. Machine-dependent weights destroy that conservation law. The gadget exploits this by giving an off-support placement only weight `eta` while assigning unit weight to the detector row whose fractional increment must be protected.
