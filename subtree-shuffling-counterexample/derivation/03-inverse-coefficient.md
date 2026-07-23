# Inverse coefficient

On the target plane `B=0`, the hidden coordinate satisfies

```text
r = A/(1+2Cr^2).
```

The Lagrange-Buermann formula gives, for `n=2m+2`,

```text
[A^(2m+2)] r^2
 = 2/(2m+2) [t^(2m)] (1+2Ct^2)^(-(2m+2))
 = (-1)^m 2^m/(m+1) binom(3m+1,m) C^m.
```

Because

```text
x = (1/2) d(r^2)/dA,
```

we obtain

```text
[A^(2m+1) C^m] (G^{-1})_1
 = (-1)^m 2^m binom(3m+1,m).
```

## Inverse slice of the suspension

Let `Phi(Z,h)=(h U_s(Z/h),h)` with `s=h^(d-1)`. If the auxiliary target coordinates vanish, the weighted target shear leaves the original target coordinates unchanged and gives

```text
s^(-1)G(sx)=A/h.
```

Thus

```text
G(sx)=h^(d-2)A,
sx=G^{-1}(h^(d-2)A),
Z_original=hx=h^(-(d-2))G^{-1}(h^(d-2)A).
```

For `d=7`,

```text
(Phi^{-1})_original(A,0,h)
 = h^(-5) G^{-1}(h^5 A).
```

A monomial `A^(2m+1)C^m` of total degree `3m+1` therefore acquires the factor

```text
h^(5(3m+1)-5) = h^(15m).
```

The resulting monomial has total degree

```text
(2m+1) + m + 15m = 18m+1 = 6(3m)+1.
```
