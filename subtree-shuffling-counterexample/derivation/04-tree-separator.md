# Tree separator

Write the homogeneous suspension as

```text
Phi = I - H,
```

so `H` is homogeneous of degree seven and `(JH)^15=0`.

For `m>=1`, set

```text
k = 3m,
alpha_m = (2m+1, 0, m, 0,...,0, 15m) in Z_{>=0}^15,
```

where the eleven auxiliary coordinates are zero. Then

```text
|alpha_m| = 18m+1 = 6k+1.
```

For a planar 7-ary Catalan tree `T` with `k` internal vertices, define

```text
w_m(T) = E_{1,alpha_m,H}(T),
```

where `E` is the average `H`-weight in the factorial normalization of Bisi et al.

## Shuffle orthogonality

The shuffle lemma says that `(JH)^15=0` implies

```text
sum_{T in S} w_m(T) = 0
```

for every length-15 shuffle class `S`. If `M` is the tree-by-class incidence matrix, this is

```text
M^T w_m = 0.
```

## Nonzero total

The tree-inverse formula says

```text
[A^(2m+1) C^m h^(15m)] (Phi^{-1})_1
 = 1/(7!)^(3m) sum_T w_m(T).
```

The coefficient calculation therefore yields

```text
1^T w_m
 = (7!)^(3m) (-1)^m 2^m binom(3m+1,m),
```

which is nonzero.

If the constant vector were in the column span of `M`, say `1=M lambda`, then

```text
1^T w_m = lambda^T M^T w_m = 0,
```

contradiction.

## Why approximation survives

A 15-perfect tree lies in a singleton length-15 shuffle class. The shuffle identity then forces `w_m(T)=0` on every 15-perfect tree. The published random-tree theorem says non-perfect trees form an exponentially small proportion. Thus the exact obstruction is supported on a rare exceptional family even though its total weighted sum is nonzero.
