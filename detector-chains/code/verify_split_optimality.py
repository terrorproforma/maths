#!/usr/bin/env python3
"""Split-optimality: the two alternatives of the binding lemma, tested.

The lemma of Section 3 says that at every maximizer of min{f, g} over the
closed box of splits, either the terminal helper height binds (f = g) or
else x_2 = 1 and the value is exactly 1 + d_2.  Two facts about that
dichotomy are checked here.

1. The second alternative is REAL (exact, standard library).  At depth 4
   with weights d = (1/10, 1/5) the splits x = (1, 1/2, 1/5) make all
   three A-side heights 11/10 while term_H = 13/10; since
   f <= dev_2 = 1 + d_2 x_2 <= 1 + d_2 = 11/10 everywhere on the box, this
   point maximizes min{f, g} with f < g.  So the lemma cannot be
   strengthened to "f = g always" on the closed box.

2. Admissibility separates the alternatives (needs scipy; skipped if
   absent).  Over random nondecreasing weight vectors at depths 3..7 the
   max-min over splits, computed by linear programming, equals the
   balanced value tau at every admissible weight vector and the cap
   1 + d_2 at every inadmissible one.  Consequence for the direction of
   error: at inadmissible weights the closed form OVERSTATES what the box
   permits, which is why every certified rung is checked for
   admissibility.

Run:  python3 verify_split_optimality.py
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction as F


def heights(k, d, x):
    """Exact p=0 heights; d and x are dicts keyed by column index."""
    dev, drain = {}, F(0)
    for j in range(2, k):
        dev[j] = 1 - drain + d[j] * x[j]
        drain += d[j] * (1 - x[j])
    term_A = 1 - drain + x[k]
    term_H = sum(1 - x[j] for j in range(2, k)) + (1 - x[k])
    return dev, term_A, term_H


def balanced_tau(k, dws):
    """Value of the balanced design at weights dws = (d_2..d_{k-1})."""
    R = sum(dws[i] / (dws[i + 1] if i + 1 < len(dws) else F(1))
            for i in range(len(dws)))
    return (dws[0] * (k - 1 - R) + 1) / (1 + dws[0])


def check_second_alternative() -> bool:
    k = 4
    d = {2: F(1, 10), 3: F(1, 5), 4: F(1)}
    x = {2: F(1), 3: F(1, 2), 4: F(1, 5)}
    dev, tA, tH = heights(k, d, x)
    f = min(list(dev.values()) + [tA])
    g = tH
    cap = 1 + d[2]
    tau = balanced_tau(k, [d[2], d[3]])
    print("1. the second alternative is attained (exact):")
    print(f"     A-side heights {[str(v) for v in dev.values()]}, "
          f"term_A = {tA}")
    print(f"     f = {f}, g = {g}, so f < g with x_2 = 1 and "
          f"f = 1 + d_2 = {cap}")
    print(f"     balanced tau = {tau} = {float(tau):.6f} exceeds the cap "
          f"{cap} = {float(cap):.6f}")
    print(f"     => these weights are inadmissible and the closed form "
          f"overstates by {float(tau - cap):.6f}")
    return f < g and x[2] == 1 and f == cap and tau > cap


def lp_maxmin(k, dws):
    """max over splits of min{dev_j, term_A, term_H}; None if unavailable."""
    import numpy as np
    from scipy.optimize import linprog

    d = [None, None] + [float(w) for w in dws] + [1.0]     # d[2..k]
    nx = k - 1                                             # x_2..x_k
    nv = nx + 1                                            # + v
    A, b = [], []

    def pos(j):
        return j - 2

    for j in range(2, k):                                  # dev_j >= v
        row = [0.0] * nv
        for i in range(2, j):
            row[pos(i)] = -d[i]
        row[pos(j)] += -d[j]
        row[nx] = 1.0
        A.append(row)
        b.append(1.0 - sum(d[i] for i in range(2, j)))
    row = [0.0] * nv                                       # term_A >= v
    for i in range(2, k):
        row[pos(i)] = -d[i]
    row[pos(k)] += -1.0
    row[nx] = 1.0
    A.append(row)
    b.append(1.0 - sum(d[i] for i in range(2, k)))
    row = [0.0] * nv                                       # term_H >= v
    for i in range(2, k + 1):
        row[pos(i)] = 1.0
    row[nx] = 1.0
    A.append(row)
    b.append(float(k - 1))

    c = [0.0] * nv
    c[nx] = -1.0
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b),
                  bounds=[(0, 1)] * nx + [(None, None)], method="highs")
    return -res.fun if res.success else None


def sweep(trials=2000, seed=5) -> bool:
    try:
        import scipy  # noqa: F401
    except ImportError:
        print("2. separation sweep SKIPPED (needs numpy + scipy)")
        return True
    rng = random.Random(seed)
    adm_ok = adm_bad = inadm_ok = inadm_bad = 0
    for _ in range(trials):
        k = rng.choice([3, 4, 5, 6, 7])
        dws = sorted(F(rng.randint(1, 20), 20) for _ in range(k - 2))
        tau = balanced_tau(k, dws)
        cap = 1 + dws[0]
        V = lp_maxmin(k, dws)
        if V is None:
            continue
        if tau <= cap:
            if abs(V - float(tau)) < 1e-9:
                adm_ok += 1
            else:
                adm_bad += 1
        else:
            if abs(V - float(cap)) < 1e-9:
                inadm_ok += 1
            else:
                inadm_bad += 1
    print(f"2. separation sweep ({trials} random weight vectors, k in 3..7):")
    print(f"     admissible   : LP max-min == balanced tau in {adm_ok} "
          f"cases, exceptions {adm_bad}")
    print(f"     inadmissible : LP max-min == cap 1+d_2  in {inadm_ok} "
          f"cases, exceptions {inadm_bad}")
    return adm_bad == 0 and inadm_bad == 0


if __name__ == "__main__":
    ok = check_second_alternative()
    print()
    ok &= sweep()
    print("\nsplit-optimality checks passed" if ok else
          "\n*** A CHECK FAILED ***")
    sys.exit(0 if ok else 1)
