#!/usr/bin/env python3
"""Exact rational verifier for the 7/6 strengthening (Lemma budget / Theorem 7/6).

Checks, in exact arithmetic:

1. the balanced-family identities m1 = m2 = m3 = 1/6 - 2p/3;
2. the certificate conditions of the budget lemma for the concrete
   (N, p, a, q, eta) = (24, 1/20, 11/30, 19/30, 1/10000) instance, giving the
   guaranteed discrepancy 3379/3000 > 9/8;
3. instance sanity for the concrete instance: column sums one, support two,
   weights strictly positive with maximum one;
4. Theorem 7/6 recipe for sampled epsilon: p = 3*eps/8, N = ceil(2/p),
   eta = eps/(13N) yields guaranteed discrepancy > 7/6 - eps;
5. the family optimality bound: min margin <= 1/6 - 2p/3 on a parameter grid.

Uses only fractions.Fraction; no floating point.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import ceil


def margins(p: F, a: F, q: F) -> tuple[F, F, F]:
    return (a / 2 - p, 1 - p - a / 2 - q, q - F(1, 2))


def guaranteed_bound(N: int, p: F, a: F, q: F, eta: F) -> F:
    """min{1 + M - (3N-2)eta, Np - 2Neta} from the budget lemma."""
    M = min(margins(p, a, q))
    assert M > 0, "forcing margins must be positive"
    forcing = 1 + M - (3 * N - 2) * eta
    accumulator = N * p - 2 * N * eta
    return min(forcing, accumulator)


def build_concrete(N: int, p: F, a: F, q: F, eta: F):
    """Materialize the (2N+1) x 3N instance; return (rows, cols, x, d)."""
    rows = ["B"] + [f"{r}{k}" for k in range(1, N + 1) for r in ("A", "H")]
    cols = [f"{c}{k}" for k in range(1, N + 1) for c in ("J", "K", "L")]
    x = {(i, j): F(0) for i in rows for j in cols}
    d = {(i, j): eta for i in rows for j in cols}
    for k in range(1, N + 1):
        A, H = f"A{k}", f"H{k}"
        J, K, L = f"J{k}", f"K{k}", f"L{k}"
        x[A, J], x["B", J] = 1 - p, p
        d[A, J] = d["B", J] = F(1)
        x[A, K], x[H, K] = F(1, 2), F(1, 2)
        d[A, K], d[H, K] = a, F(1)
        x[A, L], x[H, L] = 1 - q, q
        d[A, L] = d[H, L] = F(1)
    return rows, cols, x, d


def check_instance(rows, cols, x, d) -> None:
    for j in cols:
        col = [x[i, j] for i in rows]
        assert sum(col) == 1, f"column {j} does not sum to 1"
        assert sum(1 for v in col if v != 0) == 2, f"column {j} support != 2"
        for i in rows:
            assert 0 <= x[i, j] <= 1
            assert d[i, j] > 0
    assert max(d.values()) == 1, "maximum weight must be 1"


def main() -> None:
    # 1. balanced identities, generic p
    for p in (F(1, 20), F(1, 100), F(3, 25)):
        a = F(1, 3) + 2 * p / 3
        q = F(2, 3) - 2 * p / 3
        m = margins(p, a, q)
        assert m[0] == m[1] == m[2] == F(1, 6) - 2 * p / 3, m
    print("balanced-family identities verified")

    # 2 & 3. concrete 49x72 instance
    N, p, eta = 24, F(1, 20), F(1, 10000)
    a, q = F(11, 30), F(19, 30)
    assert a == F(1, 3) + 2 * p / 3 and q == F(2, 3) - 2 * p / 3
    bound = guaranteed_bound(N, p, a, q, eta)
    assert bound == F(3379, 3000), bound
    assert bound > F(9, 8)
    rows, cols, x, d = build_concrete(N, p, a, q, eta)
    assert (len(rows), len(cols)) == (49, 72)
    assert set(d.values()) == {eta, a, F(1)}
    check_instance(rows, cols, x, d)
    print(f"concrete instance verified: m=49, n=72, "
          f"guaranteed discrepancy = {bound} > 9/8")

    # 4. Theorem 7/6 recipe on sampled epsilon
    for eps in (F(1, 2), F(1, 10), F(1, 100), F(1, 1000)):
        pp = 3 * eps / 8
        NN = ceil(F(2, 1) / pp)
        ee = eps / (13 * NN)
        aa = F(1, 3) + 2 * pp / 3
        qq = F(2, 3) - 2 * pp / 3
        b = guaranteed_bound(NN, pp, aa, qq, ee)
        assert b > F(7, 6) - eps, (eps, b)
        print(f"eps={eps}: N={NN}, bound={b} > 7/6 - eps = {F(7,6)-eps}")

    # 5. family optimality: min margin <= 1/6 - 2p/3 on a grid
    grid = [F(i, 24) for i in range(0, 25)]
    for p in [F(i, 48) for i in range(0, 12)]:
        cap = F(1, 6) - 2 * p / 3
        for a in grid:
            if not (0 < a <= 1):
                continue
            for q in grid:
                m = min(margins(p, a, q))
                assert m <= cap, (p, a, q, m, cap)
    print("family optimality cap 1/6 - 2p/3 verified on grid")

    print("stronger-bound certificate verified exactly")


if __name__ == "__main__":
    main()
