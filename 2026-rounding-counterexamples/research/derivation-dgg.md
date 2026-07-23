# Derivation of the SSUF counterexample

## 1. The convex-hull target

Fix a feasible fractional single-source flow `x` and let `D` be the largest terminal demand. Let `U(x)` be the finite set of load vectors of unsplittable routings satisfying

```text
y_a <= x_a + D  for every arc a.
```

The cost conjecture is equivalent, on an acyclic support, to the assertion that `x` belongs to `conv U(x)`. If it does not, a separating linear functional can be shifted by vertex potentials to become a nonnegative arc-cost vector without changing its value on flow differences with the same divergence.

The design task is therefore to put the fractional load outside the convex hull of capacity-good routings.

## 2. Triangle stable-set obstruction

Give each terminal one cheap path `Z_i` and one expensive path `E_i`. We seek three shared bottlenecks with the following property:

```text
Z_1 and Z_2 cannot be used together;
Z_1 and Z_3 cannot be used together;
Z_2 and Z_3 cannot be used together.
```

Writing `z_i=1` when `Z_i` is selected, every good integral routing then satisfies the triangle stable-set facet

```text
z_1 + z_2 + z_3 <= 1.
```

If the fractional cheap-path probabilities sum to more than one, the fractional point violates that facet. Assigning a common total cost to each expensive path gives the separating objective.

## 3. A graph that realizes the triangle without hybrid paths

Use the directed graph with arcs

```text
s->t1, s->t2, s->u, u->t3, u->v,
v->t1, v->w, w->t2, w->t3.
```

Each terminal has exactly two paths:

```text
E1 = s->t1                    Z1 = s->u->v->t1
E2 = s->t2                    Z2 = s->u->v->w->t2
E3 = s->u->t3                 Z3 = s->u->v->w->t3.
```

There are no other source-terminal paths. The three conflict witnesses are nested:

```text
Z1 + Z2 conflict on s->u, because every t3 path also uses s->u;
Z1 + Z3 conflict on u->v;
Z2 + Z3 conflict on v->w.
```

This nesting avoids the path-splicing problem that defeats abstract resource gadgets.

## 4. Rational family

Normalize `D=1` and take demands

```text
d1=d3=1,  d2=b.
```

Let the cheap-path probabilities be `r,q,r`. The three relevant fractional shared loads are

```text
x(su) = 1 + r + bq,
x(uv) = 2r + bq,
x(vw) = r + bq.
```

The additive deviation forced by the cheap pairs is

```text
A12=A23 = 1 + b(1-q) - r,
A13     = 2 - 2r - bq.
```

If each expensive integral path has the same total cost, cost preservation forces at least two cheap paths whenever

```text
2r+q > 1.
```

Choose

```text
b=2/3, r=1/3, q=2/5.
```

Then

```text
2r+q = 16/15,
A12=A13=A23 = 16/15.
```

Scaling by 15 gives demands `(15,10,15)` and integer fractional loads

```text
x(st1)=10, x(st2)=6, x(su)=24,
x(ut3)=10, x(uv)=14, x(vt1)=5,
x(vw)=9, x(wt2)=4, x(wt3)=5.
```

With `D=15`, every cheap pair exceeds its relevant upper allowance by exactly one.

## 5. Cost separator

Give the three expensive paths a common total integral cost of 30:

```text
c(st1)=2, c(st2)=3, c(ut3)=2,
```

and put zero cost on the other arcs. The fractional cost is

```text
30*((1-r)+(1-q)+(1-r)) = 58.
```

Every capacity-good routing uses at most one cheap path and therefore at least two expensive paths, so its cost is at least 60. Hence

```text
min{c^T y : y unsplittable, y <= x + D} = 60 > 58 = c^T x.
```

## 6. Planar quantitative family

Set instead

```text
b=3/4, r=1/4, q=1/2+epsilon.
```

Cost preservation again forces at least two cheap paths because `2r+q=1+epsilon`. Every cheap pair has additive deviation

```text
9/8 - 3epsilon/4.
```

Thus the best universal cost-preserving upper-deviation coefficient for planar acyclic graphs is at least `9/8` in the limit. The known planar theorem gives an upper bound of `2`.

## 7. Topology

Ignoring directions, the graph is a subdivision of `K_4`: the branch vertices are `s,u,v,w`, while `t1,t2,t3` subdivide the edges `sv,sw,uw`. It is planar but lies immediately outside the series-parallel class for which an exact convex-decomposition theorem is known.
