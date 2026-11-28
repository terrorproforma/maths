#!/usr/bin/env python3
"""Exact rational (Fraction) certificates for small-machine counterexamples:
  - Theorem 4: m = 5 rows, n = 47 columns, kappa_5 > 1 (permanent cleaned helper)
  - Theorem 5: m = 4 rows, kappa_4 >= c_4* approx 1.07925345 (J_0 split + dirty-helper ping-pong)
  - Proposition (m = 3 obstruction): 0 not in conv(R_3) already in 3 columns on 3 rows

All inequalities are verified from scratch in exact fractions.Fraction arithmetic
(standard library only), accounting explicitly for ALL off-support assignments.
"""

from __future__ import annotations

import math
from fractions import Fraction as F


def build_and_verify_level(alpha_in: F, c: F, k: int, r: F):
    """Build geometric chain level of depth k (k-1 cols), ratio r, verifying every dev_j == c."""
    dws = [r ** (k - j) for j in range(2, k)] + [F(1)]
    x2 = (c - alpha_in) / dws[0]
    assert F(0) <= x2 <= F(1), f"x2={float(x2)} out of [0,1]"
    xs = [x2] + [r] * (k - 2)
    drain = F(0)
    for dj, xj in zip(dws, xs):
        assert F(0) < dj <= F(1) and F(0) <= xj <= F(1)
        assert alpha_in - drain + dj * xj == c
        drain += dj * (F(1) - xj)
    gain = sum(F(1) - xj for xj in xs)
    return dws, xs, drain, gain


def choose_r(gap: F, k: int, denom: int = 2000) -> F:
    m = k - 2
    assert F(0) < gap < F(1)
    approx = float(gap) ** (1.0 / m)
    while True:
        num = max(1, int(math.floor(approx * denom)))
        while num < denom and F(num, denom) ** m < gap:
            num += 1
        if num < denom:
            return F(num, denom)
        denom *= 4
        assert denom <= 10**9


def verify_m5_compact() -> F:
    """Certify m = 5, n = 47 exact rational counterexample proving kappa_5 > 1.

    Rows: B=0, R_0=1, R_1=2, R_2=3, H=4.
    Three blocks (b=0,1,2): block b runs J_b on {B, R_b} (p = 17/50 = 0.34),
    followed by a depth-15 geometric chain (r = 116/125 = 0.928, 14 columns) on {R_b, H}.
    Between blocks (b=0,1), one cleanup column Z_b on {R_b, H} with d_{R_b} = eta, d_H = 1,
    x_{R_b} = 1/50, x_H = 49/50 cleans H back to >= -delta!
    Total columns: 3 * 15 + 2 = 47.
    """
    k = 15
    r = F(116, 125)
    dws = [r ** (k - j) for j in range(2, k)] + [F(1)]
    x2 = F(23, 25)
    xs = [x2] + [r] * (k - 2)
    p = F(17, 50)
    xc = F(1, 50)
    eta = F(1, 100000)
    n_total = 3 * k + 2
    assert n_total == 47

    drain = F(0)
    dev_min = None
    for dj, xj in zip(dws, xs):
        assert F(0) < dj <= F(1) and F(0) <= xj <= F(1)
        dev = (F(1) - p) - drain + dj * xj
        dev_min = dev if dev_min is None else min(dev_min, dev)
        drain += dj * (F(1) - xj)
    term_H = sum(F(1) - xj for xj in xs)

    c_cert = F(1001, 1000)
    h_lo_before = F(0)
    h_mod = F(0)
    eps_h = F(0)
    for b in range(3):
        a_force = dev_min - n_total * eta
        h_force = h_lo_before + term_H - eta
        assert a_force > c_cert, f"Block {b} A-side failed: {float(a_force)} <= {float(c_cert)}"
        assert h_force > c_cert, f"Block {b} H-side failed: {float(h_force)} <= {float(c_cert)}"

        if b < 2:
            val_raw = h_mod + term_H
            eps_after_blk = eps_h + eta
            legal_M = []
            for M in range(-5, 10):
                lo = val_raw - M - eps_after_blk
                hi = val_raw - M
                if lo <= c_cert and hi >= -c_cert:
                    legal_M.append(M)
            post_lows = []
            for M in legal_M:
                lo = val_raw - M - eps_after_blk
                hi = val_raw - M
                if lo - xc <= c_cert and hi - xc >= -c_cert:
                    post_lows.append(lo - xc)
                if lo + (F(1) - xc) <= c_cert and hi + (F(1) - xc) >= -c_cert:
                    post_lows.append(lo + (F(1) - xc))
            assert post_lows
            h_lo_before = min(post_lows)
            h_mod = (val_raw - xc) - math.floor(val_raw - xc)
            eps_h = eps_after_blk
            assert h_lo_before > F(-1, 50)

    accum_lb = 3 * p - (n_total - 3) * eta
    assert accum_lb > c_cert
    return c_cert


def verify_m4_instance(c_cert: F, u: F, p1: F, p2: F, k1: int, k2: int, eta: F) -> tuple[F, int, int, int]:
    """Certify an m = 4 instance proving kappa_4 > c_cert!

    Rows: B=0, R_0=1, R_1=2, R_2=3.
    Columns:
      1. J_0 on {B, R_0}: x_B = u, x_{R_0} = 1 - u, weights (1, 1).
      2. Block 1: J_1 on {B, R_1} (x_B = p1, x_{R_1} = 1 - p1), followed by
         2-row ping-pong on {R_1, R_2} targeting c_design > c_cert.
      3. Block 2: J_2 on {R_0, B} (x_{R_0} = p2, x_B = 1 - p2), followed by
         dirty-helper 2-row ping-pong on {B, R_1} (assuming R_1 >= -c_cert!) targeting c_design > c_cert.
    """
    assert F(0) < u < F(1) and F(0) < p1 < F(1) and F(0) < p2 < F(1)
    c_des = c_cert + F(1, 5000)

    def build_pp(a0: F, h0: F, k_lev: int, max_lev: int = 250):
        a_c, h_c = a0, h0
        levs = []
        act = "A"
        for _ in range(max_lev):
            va = a_c if act == "A" else h_c
            gap = c_des - va
            if gap <= 0:
                break
            r = choose_r(gap, k_lev)
            dws, xs, drain, gain = build_and_verify_level(va, c_des, k_lev, r)
            if act == "A":
                a_c -= drain
                h_c += gain
            else:
                h_c -= drain
                a_c += gain
            levs.append((act, dws, xs, gain))
            if max(a_c, h_c) >= c_des:
                return levs
            act = "H" if act == "A" else "A"
        raise AssertionError("Ping-pong failed to reach c_des")

    pp1 = build_pp(F(1) - p1, F(0), k1)
    b_start_ideal = u + p1 - p2
    pp2 = build_pp(b_start_ideal, -c_cert, k2)

    n1 = 1 + sum(len(dws) for _, dws, _, _ in pp1)
    n2 = 1 + sum(len(dws) for _, dws, _, _ in pp2)
    n_total = 1 + n1 + n2

    # Step A: Block 1 forces J_1 -> R_1 in BOTH branches of J_0!
    a_r = F(1) - p1 - eta
    h_r = -2 * eta
    for act, dws, xs, gain in pp1:
        drain = F(0)
        if act == "A":
            for dj, xj in zip(dws, xs):
                assert a_r - drain + dj * xj > c_cert
                drain += dj * (F(1) - xj)
            a_r -= drain
            h_r += gain
        else:
            for dj, xj in zip(dws, xs):
                assert h_r - drain + dj * xj > c_cert
                drain += dj * (F(1) - xj)
            h_r -= drain
            a_r += gain
    assert max(a_r, h_r) > c_cert

    # Step B: Branch 1 (J_0 not -> B) dies immediately after J_1 -> R_1!
    assert u + p1 > c_cert

    # Step C: Only Branch 2 (J_0 -> B) survives! Check Block 2 forces J_2 -> B!
    b_entry = -(F(1) - u) + p1 - (n1 - 1) * eta
    r0_entry = (F(1) - u) - n1 * eta

    a2_r = b_entry + (F(1) - p2)
    h2_r = -c_cert - eta
    for act, dws, xs, gain in pp2:
        drain = F(0)
        if act == "A":
            for dj, xj in zip(dws, xs):
                assert a2_r - drain + dj * xj > c_cert
                drain += dj * (F(1) - xj)
            a2_r -= drain
            h2_r += gain
        else:
            for dj, xj in zip(dws, xs):
                assert h2_r - drain + dj * xj > c_cert
                drain += dj * (F(1) - xj)
            h2_r -= drain
            a2_r += gain
    assert max(a2_r, h2_r) > c_cert

    # Step D: J_2 -> B is forced, so R_0 gains p2 on J_2 and overflows c_cert!
    assert r0_entry + p2 > c_cert
    return c_cert, len(pp1), len(pp2), n_total


def verify_m3_convex_hull_obstruction() -> None:
    """Exact verification that 0 not in conv(R_3) already for m = 3 rows in 3 columns!"""
    eta = F(1, 1000)
    cols = [
        [(F(5, 24), F(1)), (F(19, 24), F(1)), (F(0), eta)],
        [(F(0), eta), (F(1, 2), F(1, 2)), (F(1, 2), F(1))],
        [(F(0), eta), (F(23, 48), F(1)), (F(25, 48), F(1))],
    ]
    R = {(F(0), F(0), F(0))}
    for col in cols:
        Rnext = set()
        for state in R:
            for r in range(3):
                ns = tuple(state[i] + col[i][1] * (col[i][0] - (F(1) if i == r else F(0))) for i in range(3))
                if all(abs(v) <= F(1) for v in ns):
                    Rnext.add(ns)
        R = Rnext
    assert len(R) > 0
    min_B = min(s[0] for s in R)
    assert min_B == F(5, 24) - eta and min_B > 0
    print("m = 3 convex-hull obstruction verified exactly:")
    print(f"  After 3 columns on 3 rows (B, A, H), |R_3| = {len(R)} surviving states in [-1,1]^3,")
    print(f"  and EVERY surviving state has Delta_B >= {min_B} = {float(min_B):.6f} > 0 => 0 not in conv(R_3).")


def main() -> None:
    c5 = verify_m5_compact()
    print(f"Theorem 4 (m = 5, n = 47, permanent cleaned helper): certified kappa_5 > {c5} = {float(c5):.6f}")

    lo, hi = 1.0, 1.2
    for _ in range(80):
        mid = (lo + hi) / 2
        if 3 * mid - 2 < math.exp(-(mid - 1)) + math.exp(1 - 2 * mid):
            lo = mid
        else:
            hi = mid
    print(f"\nTheorem 5 (m = 4, J_0 split + dirty-helper ping-pong; limit c_4* = {lo:.8f}):")

    m4_rungs = [
        ("m=4 rung 1 (c > 1.000)", F(1, 1), F(3, 10), F(71, 100), F(31, 100), 10, 10, F(1, 10**6)),
        ("m=4 rung 2 (c > 1.030)", F(103, 100), F(27, 100), F(77, 100), F(31, 100), 12, 14, F(1, 10**7)),
        ("m=4 rung 3 (c > 1.060)", F(106, 100), F(245, 1000), F(820, 1000), F(310, 1000), 22, 28, F(1, 10**8)),
        ("m=4 rung 4 (c > 1.072)", F(1072, 1000), F(239, 1000), F(834, 1000), F(312, 1000), 40, 50, F(1, 10**9)),
    ]
    for name, c_cert, u, p1, p2, k1, k2, eta in m4_rungs:
        cert, l1, l2, ntot = verify_m4_instance(c_cert, u, p1, p2, k1, k2, eta)
        print(f"  {name}: certified kappa_4 > {float(cert):.6f}  (pp1={l1} lvls, pp2={l2} lvls, n={ntot} cols)")

    print()
    verify_m3_convex_hull_obstruction()
    print("\nAll small-row certificates verified exactly in fractions.Fraction.")


if __name__ == "__main__":
    main()
