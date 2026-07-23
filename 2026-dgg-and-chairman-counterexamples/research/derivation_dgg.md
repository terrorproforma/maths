# Derivation of the unsplittable-flow counterexample

## 1. Convex-hull target

For a fixed fractional flow `x`, let `U+(x)` be the finite set of unsplittable load vectors satisfying

```text
y_a <= x_a + D  for every arc a,
```

where `D` is the largest demand. A cost counterexample is exactly a nonnegative vector `c` for which

```text
c·y > c·x  for every y in U+(x).
```

The useful design principle is therefore to make the fractional path-choice marginals violate a facet of the integral choices that survive the arc bounds.

## 2. Triangle stable-set obstruction

Give each of three terminals an expensive path `E_i` and a cheap path `Z_i`. Arrange three shared arcs so that every pair of cheap choices is incompatible:

```text
Z1 + Z2  -> overload arc s->u,
Z1 + Z3  -> overload arc u->v,
Z2 + Z3  -> overload arc v->w.
```

Writing `z_i=1` for selection of `Z_i`, every upper-good integral routing then satisfies

```text
z1 + z2 + z3 <= 1.
```

Choose fractional cheap-path probabilities

```text
p = (1/3, 2/5, 1/3).
```

Their sum is `16/15`, so the fractional point lies outside the triangle stable-set polytope. Give each expensive choice total integral cost 30 and each cheap choice cost zero. The fractional cost is

```text
30 * [(1-1/3) + (1-2/5) + (1-1/3)] = 58,
```

whereas an upper-good integral choice uses at least two expensive paths and costs at least 60.

## 3. Realizing the three conflicts without hybrid paths

The graph has a backbone

```text
s -> u -> v -> w
```

and three sink pairs attached to nested suffixes:

```text
t1:  E1 = s->t1,              Z1 = s->u->v->t1
t2:  E2 = s->t2,              Z2 = s->u->v->w->t2
t3:  E3 = s->u->t3,           Z3 = s->u->v->w->t3
```

All terminals are sinks. Consequently these are literally all source-terminal paths; there is no merge-then-split location that creates an omitted hybrid.

With demands `(15,10,15)`, the fractional decomposition amounts are

```text
t1: 10 E1 + 5 Z1
t2:  6 E2 + 4 Z2
t3: 10 E3 + 5 Z3.
```

The shared loads are

```text
x(su)=5+4+15=24,
x(uv)=5+4+5=14,
x(vw)=4+5=9.
```

Since `D=15`, their permitted upper loads are `39,29,24`.

The three cheap pairs produce

```text
Z1,Z2: y(su)=15+10+15=40 > 39,
Z1,Z3: y(uv)=15+15=30 > 29,
Z2,Z3: y(vw)=10+15=25 > 24.
```

Each violation is exactly one unit. Any routing using at most one cheap path stays within every upper bound.

## 4. Arc costs

Set

```text
c(s->t1)=2,
c(s->t2)=3,
c(u->t3)=2,
```

and all other costs to zero. Then each expensive integral path costs 30 after multiplication by its terminal demand:

```text
15*2 = 10*3 = 15*2 = 30.
```

The fractional cost is `2*10 + 3*6 + 2*10 = 58`.

## 5. All-positive-cost perturbation

To show that zero costs are inessential, put cost one on every formerly zero-cost arc and use costs `12,18,12` on `s->t1,s->t2,u->t3`. The fractional cost becomes

```text
12*10 + 18*6 + 12*10 + (24+14+5+9+4+5) = 409.
```

The four upper-good routing costs are `555,420,415,420`, so the new strict gap is `409<415`.

## 6. Planarity and the series-parallel boundary

In the underlying undirected graph, suppress the degree-two terminals `t1,t2,t3`. The remaining branch vertices are `s,u,v,w`, and the six resulting branch connections form `K4`. Thus the graph is a planar subdivision of `K4`, but it is not series-parallel. This places the obstruction immediately beyond the class where the exact convex-decomposition theorem is known.

## 7. Parametric family

Normalize demands to `(1,b,1)` and cheap probabilities to `(r,q,r)`. Give each expensive path total cost one. Cost separation requires

```text
2r+q > 1.
```

The three pair deviations are

```text
Z1,Z2 or Z2,Z3: 1 + b(1-q) - r,
Z1,Z3:           2 - 2r - bq.
```

Both exceed `D=1` exactly when

```text
b(1-q) > r,
2r+bq < 1.
```

On the cost boundary `q=1-2r`, balancing the two deviations gives `r=1-b` and value `b(3-2b)`. This is maximized at `b=3/4`, giving the supremum `9/8`. Taking `r=1/4` and `q=1/2+epsilon` yields a strict cost gap and forced additive deviation `9/8-3epsilon/4`.
