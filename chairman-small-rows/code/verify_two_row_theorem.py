"""Exact test of the two-row theorem (kappa_2 <= 1) through its constructive proof.

1. Runs code/two_row_algorithm.py on many instances and checks, in exact rational
   arithmetic, that the returned assignment has every row-prefix discrepancy at most 1.
   The algorithm asserts each claim of the proof (Claim B, Lemma M, Lemma T, Claim F and
   the invariant) at every step, so a pass also checks the proof on those instances.
2. For small instances, compares with the exhaustive exact min-max from minmax.py.

Instances: the rail family, random rational instances from several distributions that
favour extreme weights and splits, and instances with collinear or zero weight vectors.
Deterministic (fixed seed).  Standard library only.
"""
import random
import sys
from fractions import Fraction as F
from two_row_algorithm import solve, max_discrepancy
from minmax import minmax

H = F(1, 2)


def rail(k, eta=F(0)):
    cols = [(F(1), eta, H)]
    for i in range(k, 0, -1):
        cols += [(1 - F(1, 2 ** i), F(1), H), (F(1), F(1), H)]
    return cols


def rnd_frac(rng, den):
    return F(rng.randint(0, den), den)


def random_instance(rng, n, kind):
    cols = []
    for _ in range(n):
        if kind == 0:      # generic
            d1, d2, x = rnd_frac(rng, 12), rnd_frac(rng, 12), rnd_frac(rng, 12)
        elif kind == 1:    # extreme weights
            d1 = rng.choice([F(0), F(1), F(1), rnd_frac(rng, 8)])
            d2 = rng.choice([F(0), F(1), F(1), rnd_frac(rng, 8)])
            x = rng.choice([H, rnd_frac(rng, 8), rnd_frac(rng, 8)])
        elif kind == 2:    # few directions: many collinear generators
            base = rng.choice([(F(1), F(0)), (F(0), F(1)), (F(1), F(1)), (F(1), H), (H, F(1))])
            s = rng.choice([F(1), H, F(1, 3), F(0)])
            d1, d2, x = base[0] * s, base[1] * s, rnd_frac(rng, 6)
        else:              # fine denominators, splits near 0 and 1
            d1, d2 = rnd_frac(rng, 97), rnd_frac(rng, 89)
            x = rng.choice([F(1, 101), F(100, 101), rnd_frac(rng, 101)])
        cols.append((d1, d2, x))
    return cols


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    rng = random.Random(20261124)
    worst = F(0)
    count = 0

    for k in range(0, 12):
        for eta in (F(0), F(1, 2 ** k)):
            cols = rail(k, eta)
            for sup in (True, False):
                y = solve(cols, respect_support=sup)
                v = max_discrepancy(cols, y)
                assert v <= 1, (k, eta, v)
                worst = max(worst, v)
                count += 1
    print(f"rail family, depth 0..11: algorithm output within 1 (worst {worst})")

    small = 0
    for t in range(trials):
        kind = t % 4
        n = rng.choice([1, 2, 3, 5, 8, 12, 20, 40, 80])
        cols = random_instance(rng, n, kind)
        for sup in (True, False):
            y = solve(cols, respect_support=sup)
            assert len(y) == n
            v = max_discrepancy(cols, y)
            assert v <= 1, (cols, y, v)
            if sup:
                for (d1, d2, x), yj in zip(cols, y):
                    assert not (x == 0 and yj == 1) and not (x == 1 and yj == 0)
            worst = max(worst, v)
            count += 1
        if n <= 12 and t % 5 == 0:
            mcols = [([c[0], c[1]], [c[2], 1 - c[2]]) for c in cols]
            opt = minmax(mcols, 2)
            assert opt <= 1 and opt <= max_discrepancy(cols, solve(cols, respect_support=False))
            small += 1
    print(f"{count} runs of the algorithm, all outputs within 1 (largest value seen: {worst} ~ {float(worst):.6f})")
    print(f"{small} small instances cross-checked against exhaustive exact min-max")
    print("two-row theorem verified on all test instances")


if __name__ == "__main__":
    main()
