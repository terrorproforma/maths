# Weighted Horner suspension

This note records the general algebra used to obtain the 15-variable homogeneous map.

Let

```text
G_i(X) = X_i + sum_{j=2}^{d_i} K_{i,j}(X),
```

where each `K_{i,j}` is homogeneous of degree `j` and `det JG=1`.

For each component introduce auxiliary variables

```text
Y_{i,3},...,Y_{i,d_i}.
```

Define a polynomial map `N` by

```text
N_{X_i}       = K_{i,2} + Y_{i,3},
N_{Y_{i,j}}   = -K_{i,j} - Y_{i,j+1}  (3 <= j < d_i),
N_{Y_{i,d_i}} = -K_{i,d_i}.
```

Let `U_s=I+sN`. Its outputs obey the telescoping identity

```text
X_i' - sum_{j=3}^{d_i} s^(j-2) Y_{i,j}'
  = X_i + sum_{j=2}^{d_i} s^(j-1)K_{i,j}(X)
  = s^(-1)G_i(sX).
```

The transformation on the left is a target shear of determinant one. After this shear, the original-coordinate outputs depend only on `X`, while the auxiliary-output Jacobian with respect to the auxiliary inputs is unit triangular. Therefore

```text
det(I+s JN) = det J(s^(-1)G(sX)) = det JG(sX) = 1.
```

If `M` is the dimension of `N`, the identity `det(I+sJN)=1` says that the characteristic polynomial of `JN` is `lambda^M`. Cayley-Hamilton gives

```text
(JN)^M = 0.
```

Now let `d=max_i d_i`, add one variable `h`, and set

```text
mathcalH(Z,h) = (h^d N(Z/h), 0).
```

Every term of `mathcalH` has total degree `d`. On the dense set `h != 0`,

```text
J mathcalH = [[h^(d-1) JN(Z/h), *],
              [0,                 0]].
```

Since `(JN)^M=0`, the block matrix has `(M+1)`st power zero. Polynomial continuation extends the identity to `h=0`.

For the normalized map in this project,

```text
(d_1,d_2,d_3) = (4,6,7),
M = 3 + (4-2) + (6-2) + (7-2) = 14,
d = 7.
```

Thus the homogeneous suspension has dimension `15`, degree `7`, and

```text
(JH)^15 = 0.
```

## Collision lift

At `h=1`, choose

```text
Y_{i,j} = sum_{ell=j}^{d_i} K_{i,ell}(q).
```

Then all auxiliary outputs telescope to zero and the original outputs equal `G(q)`. Every collision of `G` therefore lifts to a collision of the homogeneous suspension.
