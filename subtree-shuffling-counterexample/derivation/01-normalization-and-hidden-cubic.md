# Normalization and hidden cubic

Let

```text
u = 1 + xy
```

and define the supplied map `F=(P,Q,R)` by

```text
P = u^3 z + y^2 u(4+3xy),
Q = y + 3xu^2z + 3xy^2(4+3xy),
R = 2x - 3x^2y - x^3z.
```

Its Jacobian determinant is `-2`. The exact SymPy check is in `src/shuffle_counterexample/maps.py`.

## Determinant-one normalization

Set

```text
G(x,y,z) = (R(x,2y,2z)/2,
            Q(x,2y,2z)/2,
            P(x,2y,2z)/2).
```

Then `G=(A,B,C)` is

```text
A = x - 3x^2y - x^3z,

B = y + 3xz + 24xy^2 + 12x^2yz
      + 36x^2y^3 + 12x^3y^2z,

C = z + 8y^2 + 6xyz + 28xy^3 + 12x^2y^2z
      + 24x^2y^4 + 8x^3y^3z.
```

The source scaling has determinant `4`. The target permutation and scaling has determinant `-1/8`. Thus

```text
det JG = (-1/8) * (-2) * 4 = 1.
```

The normalized collision points are

```text
(0,0,-1/8), (1,-3/4,13/4), (-1,3/4,13/4),
```

and their common image is `(0,0,-1/8)`.

## Hidden cubic coordinates

Put

```text
u = 1 + 2xy,
r = x/u.
```

Direct simplification gives

```text
B = y + 3rC,
A = r - r^2B + 2r^3C.
```

For fixed target `(A,B,C)`, the possible values of `r` therefore satisfy

```text
2Cr^3 - Br^2 + r - A = 0.
```

On `B=0`,

```text
A = r + 2Cr^3,
y = -3Cr.
```

Since `x=ru` and `u=1+2xy`, substitution gives

```text
u(1+6Cr^2)=1,
x = r/(1+6Cr^2).
```

Differentiating `A=r+2Cr^3` at fixed `C` gives

```text
dr/dA = 1/(1+6Cr^2),
```

hence

```text
x = r dr/dA = (1/2) d(r^2)/dA.
```
