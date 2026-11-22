"""Exact verification of the two-row rail family (Theorem 1 of notes/two_rows.md).

Rows 1, 2.  Depth k >= 0, n = 2k + 1 columns, every fractional split equal to 1/2:

    column 0 :  weights (1, eta)
    then for i = k, k-1, ..., 1 :
        weights (1 - 2^-i, 1)   followed by   weights (1, 1)

Claim: the min-max row-prefix discrepancy is exactly 1 - 2^-(k+1)  (D = 1).
The claim holds for 0 <= eta <= 2^-k.  (For larger eta the value drops: for example
eta = 1/100, k = 7 gives 199/200 = 1 - eta/2.)  The script checks the claim by exhaustive
exact search for k = 0..K with eta = 0, eta = 2^-k and eta = 10^-6.  Standard library only.
"""
import sys
from fractions import Fraction as F
from minmax import minmax, check_instance

H = F(1, 2)


def rail(k, eta):
    cols = [([F(1), eta], [H, H])]
    for i in range(k, 0, -1):
        cols.append(([1 - F(1, 2 ** i), F(1)], [H, H]))
        cols.append(([F(1), F(1)], [H, H]))
    return cols


def main():
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    ok = True
    for label in ("0", "2^-k", "1e-6"):
        for k in range(K + 1):
            eta = {"0": F(0), "2^-k": F(1, 2 ** k), "1e-6": F(1, 10 ** 6)}[label]
            cols = rail(k, eta)
            check_instance(cols, 2)
            v = minmax(cols, 2)
            target = 1 - F(1, 2 ** (k + 1))
            flag = "ok" if v == target else "MISMATCH"
            ok &= v == target
            print(f"eta={str(eta):>9}  k={k}  n={len(cols):2d}  minmax={v}  target={target}  {flag}")
    print("rail family verified exactly" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
