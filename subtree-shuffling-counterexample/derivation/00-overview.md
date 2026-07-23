# Derivation overview

The proof has four exact layers.

## 1. Normalize the three-variable collision

The supplied map `F=(P,Q,R)` has constant Jacobian `-2` and three rational preimages of one point. Apply the source scaling

```text
(x,y,z) -> (x,2y,2z)
```

and the target transformation

```text
(P,Q,R) -> (R/2,Q/2,P/2).
```

The resulting map `G=(A,B,C)` has identity linear part, determinant one, and the three normalized collisions.

## 2. Homogenize without losing the collision

Write each component as

```text
G_i = X_i + K_{i,2} + ... + K_{i,d_i},
```

where the `K_{i,j}` are homogeneous of degree `j`. A weighted Horner chain replaces each higher-degree tail by auxiliary variables. The prehomogeneous map `U_s=I+sN` satisfies a telescoping target-shear identity

```text
X_i' - sum_{j=3}^{d_i} s^(j-2) Y_{i,j}' = s^(-1) G_i(sX).
```

Since the auxiliary block is unit triangular and `det JG=1`,

```text
det(I+s JN)=1.
```

Cayley-Hamilton gives `(JN)^14=0`. A final homogenizing variable `h` turns `N` into a degree-seven homogeneous map in 15 variables and gives `(JH)^15=0`.

## 3. Extract a nonzero inverse coefficient

For `G^{-1}` on the target plane `B=0`, the hidden coordinate

```text
r = x/(1+2xy)
```

satisfies

```text
A = r + 2 C r^3,
x = r/(1+6 C r^2) = (1/2) d(r^2)/dA.
```

Lagrange inversion yields

```text
[A^(2m+1) C^m] (G^{-1})_1
  = (-1)^m 2^m binom(3m+1,m).
```

The suspension inverse-slice identity moves this coefficient to

```text
[A^(2m+1) C^m h^(15m)] (Phi^{-1})_1.
```

The total degree is `18m+1 = 6(3m)+1`, the leaf count for a 7-ary Catalan tree with `3m` internal vertices.

## 4. Convert it into a shuffle separator

Write `Phi=I-H`. The published shuffle lemma says that `(JH)^15=0` makes every average tree-weight function orthogonal to every length-15 shuffle-class indicator. The published tree-inverse formula says that the total sum of the same function is `(7!)^(3m)` times the inverse coefficient.

Therefore the vector

```text
w_m(T) = E_{1,alpha_m,H}(T)
```

satisfies

```text
M^T w_m = 0,
1^T w_m = (7!)^(3m) (-1)^m 2^m binom(3m+1,m) != 0.
```

This separates the constant vector from the shuffle span for every `k=3m`.
