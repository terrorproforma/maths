"""Exact min-max row-prefix discrepancy for machine-dependent chairman instances.

An instance is a list of columns.  Column j is a pair (d, x) of length-m lists of
Fractions: d[i] >= 0 is the weight of column j on row i, x[i] >= 0 is the fractional
assignment, sum(x) == 1.  An integral assignment gives each column to one row.  The
row-prefix discrepancy is

    disc_i(t) = sum_{j <= t} d_ij * (x_ij - y_ij).

`minmax` returns  min over assignments  of  max over (i, t)  of |disc_i(t)|, by
exhaustive depth-first search with branch and bound, in exact rational arithmetic.
Standard library only.
"""
from fractions import Fraction as F


def minmax(cols, m):
    best = [None]

    def rec(j, s, cur):
        if best[0] is not None and cur >= best[0]:
            return
        if j == len(cols):
            best[0] = cur
            return
        d, x = cols[j]
        base = [s[i] + d[i] * x[i] for i in range(m)]
        opts = []
        for i in range(m):
            t = list(base)
            t[i] -= d[i]
            opts.append((max(abs(v) for v in t), t))
        opts.sort(key=lambda o: o[0])
        for c, t in opts:
            rec(j + 1, t, max(cur, c))

    rec(0, [F(0)] * m, F(0))
    return best[0]


def check_instance(cols, m):
    for d, x in cols:
        assert len(d) == m and len(x) == m
        assert all(0 <= v <= 1 for v in d), "weights must lie in [0, 1] (D = 1)"
        assert all(v >= 0 for v in x) and sum(x) == 1, "x must be a fractional assignment"
