"""Exact check of the stored instances in ../data.  Standard library only.

two_row_even.json : each column is [d_1, d_2, x_1]; the claimed value must match exactly.
search_best.json  : general m; each column is {"d": [...], "x": [...]} with decimal strings.
                    The decimals are read as exact rationals, x is renormalised exactly,
                    and the exact min-max of that rational instance is printed.  This is a
                    certified value for the stored instance (it can differ slightly from
                    the floating-point value the search printed).
mixed_sign_example.json : a planar walk with mixed-sign vectors (not a chairman instance);
                    the claimed exact min-max 15/14 must match.
"""
import json, os, sys
from fractions import Fraction as F
from minmax import minmax, check_instance

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def main():
    ok = True
    with open(os.path.join(DATA, "two_row_even.json")) as f:
        for inst in json.load(f)["instances"]:
            cols = [([F(c[0]), F(c[1])], [F(c[2]), 1 - F(c[2])]) for c in inst["columns"]]
            check_instance(cols, 2)
            v = minmax(cols, 2)
            good = v == F(inst["value"])
            ok &= good
            print(f"two rows  n={inst['n']}  minmax={v}  claimed={inst['value']}  {'ok' if good else 'MISMATCH'}")
    path = os.path.join(DATA, "search_best.json")
    if os.path.exists(path):
        with open(path) as f:
            for inst in json.load(f)["instances"]:
                m = inst["m"]
                cols = []
                for c in inst["columns"]:
                    d = [F(s) for s in c["d"]]
                    x = [F(s) for s in c["x"]]
                    t = sum(x)
                    cols.append((d, [v / t for v in x]))
                check_instance(cols, m)
                v = minmax(cols, m)
                below = v < 1
                print(f"m={m}  n={len(cols)}  exact minmax={v} ~ {float(v):.6f}  (search printed {inst['search_value']})"
                      f"  {'below 1' if below else 'AT OR ABOVE 1'}")
    with open(os.path.join(DATA, "mixed_sign_example.json")) as f:
        inst = json.load(f)
    walk = [(F(c[0]), F(c[1]), F(c[2])) for c in inst["columns"]]
    assert all(abs(a) <= 1 and abs(b) <= 1 and 0 <= w <= 1 for a, b, w in walk)
    best = [None]

    def rec(j, p, q, cur):
        if best[0] is not None and cur >= best[0]:
            return
        if j == len(walk):
            best[0] = cur
            return
        a, b, w = walk[j]
        for (x, y) in ((p + (1 - w) * a, q + (1 - w) * b), (p - w * a, q - w * b)):
            rec(j + 1, x, y, max(cur, abs(x), abs(y)))

    rec(0, F(0), F(0), F(0))
    good = best[0] == F(inst["value"])
    ok &= good
    print(f"mixed-sign planar walk  minmax={best[0]}  claimed={inst['value']}  {'ok' if good else 'MISMATCH'}")
    print("stored instances verified exactly" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
