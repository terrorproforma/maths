#!/usr/bin/env python3
"""Exact rational (fractions.Fraction) certificates for:

  - Theorem 1 (Resolution of m* = 3):
      * Ultra-compact m = 3, n = 33 full instance proving kappa_3 > 1001/1000
        (zero-pollution J_0 + 1-level Block 1 + cleanup Z_1 + clean ping-pong Block 2).
      * Asymptotic m = 3 family proving kappa_3 >= c_3* approx 1.1017206620,
        unique root of 2c - 1 = exp(-(c - 1)) + exp(1 - 2c), with exact certified
        rungs at c > 1.000, 1.050, 1.080 (beating the prior m = 4 limit 1.079253!),
        and 1.095.
  - Theorem 2 (Even-m Zero-Pollution Ladder):
      * For every even m = 2q + 2 >= 4, kappa_m >= c_m*, unique root of
        exp(-(c - 1)) - (c - 1) = 2 / m:
          m = 4: c_4** approx 1.2662486082  (rungs certified up to c > 1.258)
          m = 6: c_6*  approx 1.3625595433  (rungs certified up to c > 1.355)
          m = 8: c_8*  approx 1.4121950815  (rungs certified up to c > 1.402 > 1 + 1/e)

All inequalities are verified from scratch in exact fractions.Fraction arithmetic
(Python standard library only), accounting explicitly for ALL off-support assignments.
"""

from __future__ import annotations

import math
from fractions import Fraction as F


def build_and_verify_level(alpha_in: F, c: F, k: int, r: F) -> tuple[list[F], list[F], F, F]:
    """Build geometric chain level of depth k (k-1 cols), ratio r, verifying every dev_j == c."""
    assert k >= 3 and F(0) < r < F(1)
    dws = [r ** (k - j) for j in range(2, k)] + [F(1)]
    x2 = (c - alpha_in) / dws[0]
    assert F(0) <= x2 <= F(1), f"x2={float(x2):.6f} out of [0,1]"
    xs = [x2] + [r] * (k - 2)
    drain = F(0)
    for dj, xj in zip(dws, xs):
        assert F(0) < dj <= F(1) and F(0) <= xj <= F(1)
        assert alpha_in - drain + dj * xj == c
        drain += dj * (F(1) - xj)
    gain = sum(F(1) - xj for xj in xs)
    assert alpha_in - drain == c - F(1)
    return dws, xs, drain, gain


def choose_r(gap: F, k: int, denom: int = 2000) -> F:
    """Choose rational r = num/denom in (0, 1) with r^(k-2) >= gap."""
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


def build_pp(a0: F, h0: F, c_des: F, k_first: int, k_rest: int, max_lev: int = 300):
    """Build a 2-row ping-pong block from (a0, h0) targeting c_des."""
    a_c, h_c = a0, h0
    levs = []
    act = "A"
    for lev in range(max_lev):
        va = a_c if act == "A" else h_c
        gap = c_des - va
        if gap <= 0:
            break
        ku = k_first if lev == 0 else k_rest
        r = choose_r(gap, ku)
        dws, xs, drain, gain = build_and_verify_level(va, c_des, ku, r)
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
    raise AssertionError(f"Ping-pong failed to reach {float(c_des)}: a={float(a_c):.5f}, h={float(h_c):.5f}")


def verify_pp_adversarial(levs, a_start: F, h_start: F, c_cert: F) -> None:
    """Verify every prefix deviation and final peak strictly exceeds c_cert in exact Fraction."""
    a_r, h_r = a_start, h_start
    for act, dws, xs, gain in levs:
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


def verify_m3_ultracompact() -> tuple[F, int]:
    """Certify ultra-compact m = 3, n = 33 exact rational counterexample proving kappa_3 > 1001/1000.

    Rows: B=0, A=1, H=2.
    Columns:
      1. J_0 on {B, A}: x_B = 995/1000, x_A = 5/1000, weights d_B = 1, d_A = eta, d_H = eta.
      2. Block 1: J_1 on {B, H} (x_B = 17/50, x_H = 33/50, d_B=1, d_H=1, d_A=eta),
         followed by 1-level chain H -> A (k1 = 10, 9 columns).
      3. Cleanup column Z_1 on {H, A}: d_H = eta, d_A = 1, d_B = eta, x_H = xc, x_A = 1 - xc.
         Since A has weight 1 on every chain column of Block 1, A mod 1 is fixed up to O(eta),
         so Z_1 lifts A to >= a_clean > -1/50 on EVERY surviving schedule!
      4. Block 2: Clean ping-pong directly on {B, A} (7 levels, k = 4 per level = 21 cols).
    Total columns: 1 + 1 + 9 + 1 + 21 = 33.
    """
    c_cert = F(1001, 1000)
    c_des = F(1002, 1000)
    u = F(995, 1000)
    p1 = F(17, 50)
    k1 = 10
    eta = F(1, 10**6)

    gap1 = c_des - (F(1) - p1)
    r1 = choose_r(gap1, k1, denom=10000)
    d1, x1, _, term_A = build_and_verify_level(F(1) - p1, c_des, k1, r1)
    assert term_A > c_des
    delta = term_A - F(int(term_A))
    xc = delta + F(1, 200)
    assert F(0) < xc < F(1, 2)
    a_clean_ideal = delta - xc  # = -1/200

    pp2 = build_pp(u + p1 - F(1), a_clean_ideal, c_des, k_first=4, k_rest=4, max_lev=20)
    n_total = 1 + 1 + len(d1) + 1 + sum(len(dws) for _, dws, _, _ in pp2)
    assert n_total == 33, f"Expected 33 cols, got {n_total}"

    # Step 1: After J_0, ALL three assignments satisfy:
    #   Branch 1 (J_0 -> A): B = +u, A = -(1-u)*eta, H = 0
    #   Branch 2 (J_0 -> B): B = -(1-u), A = +(1-u)*eta, H = 0
    #   Branch 3 (J_0 -> H): B = +u, A = +(1-u)*eta, H = -eta
    # Worst-case lower bounds for Block 1 forcing J_1 -> H across ALL 3 branches:
    h_start_b1 = F(1) - p1 - eta
    a_start_b1 = -eta - eta  # -(1-u)*eta on J_0 and possibly -eta on J_1
    drain = F(0)
    for dj, xj in zip(d1, x1):
        assert h_start_b1 - drain + dj * xj > c_cert
        drain += dj * (F(1) - xj)
    assert a_start_b1 + term_A > c_cert

    # Step 2: Therefore J_1 -> H is FORCED in all 3 branches!
    # Branches 1 & 3 immediately hit B = u + p1 > c_cert and die!
    assert u + p1 > c_cert

    # Step 3: Only Branch 2 (J_0 -> B, J_1 -> H) survives!
    # At the end of Block 1's 1-level chain H -> A, A was touched by:
    #   J_0 (+(1-u)*eta), J_1 (-eta if off-support, else 0), and the 9 weight-1 columns of H -> A.
    # Thus A = term_A - M + err_A, where M in Z and err_A in [-eta, (1-u)*eta].
    err_lo = -eta
    err_hi = (F(1) - u) * eta
    post_lows = []
    for M in range(-5, 10):
        lo = term_A - M + err_lo
        hi = term_A - M + err_hi
        if lo <= c_cert and hi >= -c_cert:
            # Z_1 -> A shifts A by -xc; Z_1 not -> A shifts A by +(1 - xc)
            if lo - xc <= c_cert and hi - xc >= -c_cert:
                post_lows.append(lo - xc)
            if lo + (F(1) - xc) <= c_cert and hi + (F(1) - xc) >= -c_cert:
                post_lows.append(lo + (F(1) - xc))
    assert post_lows
    a_after_clean = min(post_lows)
    assert a_after_clean > F(-1, 100)

    # Step 4: B was untouched except off-support (-eta) on len(d1) + 1 cols:
    b_after_clean = -(F(1) - u) + p1 - (len(d1) + 1) * eta

    # Step 5: Block 2 clean ping-pong on {B, A} kills Branch 2!
    verify_pp_adversarial(pp2, b_after_clean, a_after_clean, c_cert)
    return c_cert, n_total


def verify_m3_asymptotic(c_cert: F, u: F, p1: F, k1: int, k2: int, eta: F) -> tuple[F, int, int, int]:
    """Certify an m = 3 instance from the asymptotic family (limit c_3* approx 1.10172066).

    Rows: B=0, A=1, H=2.
      1. J_0 on {B, A}: x_B = u, x_A = 1 - u, d_B = 1, d_A = eta, d_H = eta.
      2. Block 1: J_1 on {B, H} (x_B = p1, x_H = 1 - p1, d_B=1, d_H=1, d_A=eta),
         followed by 2-row ping-pong on {H, A} targeting c_des > c_cert.
      3. Block 2: Dirty-helper 2-row ping-pong directly on {B, A} (assuming A >= -c_cert!).
    """
    assert F(0) < u < F(1) and F(0) < p1 < F(1)
    c_des = c_cert + F(1, 5000)

    pp1 = build_pp(F(1) - p1, F(0), c_des, k_first=k1, k_rest=k1)
    pp2 = build_pp(u + p1 - F(1), -c_cert, c_des, k_first=k2, k_rest=k2)

    n1 = 1 + sum(len(dws) for _, dws, _, _ in pp1)
    n2 = sum(len(dws) for _, dws, _, _ in pp2)
    n_total = 1 + n1 + n2

    # Step A: Block 1 forces J_1 -> H in ALL 3 branches of J_0!
    # Worst-case entry to {H, A} ping-pong: H >= 1 - p1 - eta, A >= -2*eta.
    verify_pp_adversarial(pp1, F(1) - p1 - eta, -2 * eta, c_cert)

    # Step B: Branches 1 (J_0 -> A) and 3 (J_0 -> H) die immediately after J_1 -> H!
    assert u + p1 > c_cert

    # Step C: Only Branch 2 (J_0 -> B, J_1 -> H) survives!
    # After Block 1: B >= -(1 - u) + p1 - (n1 - 1)*eta, and A >= -c_cert (legal schedule!).
    b_entry = -(F(1) - u) + p1 - (n1 - 1) * eta
    verify_pp_adversarial(pp2, b_entry, -c_cert, c_cert)

    return c_cert, len(pp1), len(pp2), n_total


def verify_even_m_ladder(m: int, c_cert: F, u: F, p1: F, k_blk: int, k_fin: int, eta: F) -> tuple[F, int, int, int]:
    """Certify an even-m (m = 2q + 2 >= 4) instance from the Zero-Pollution Ladder.

    Rows: B=0, R_0=1, and q fresh pairs (A_r, H_r) = (2r, 2r+1) for r = 1..q.
      1. J_0 on {B, R_0}: x_B = u, x_{R_0} = 1 - u, d_B = 1, all other d = eta.
      2. Blocks r = 1..q: J_r on {B, A_r} (x_B = p1, x_{A_r} = 1 - p1),
         followed by clean 2-row ping-pong on {A_r, H_r}.
      3. Final block: Clean 2-row ping-pong directly on {B, R_0}!
    """
    assert m >= 4 and m % 2 == 0
    q = (m - 2) // 2
    c_des = c_cert + F(1, 5000)

    pp_blk = build_pp(F(1) - p1, F(0), c_des, k_first=k_blk, k_rest=k_blk)
    n_blk = 1 + sum(len(dws) for _, dws, _, _ in pp_blk)

    b_fin_ideal = u + q * p1 - F(1)
    pp_fin = build_pp(b_fin_ideal, F(0), c_des, k_first=k_fin, k_rest=k_fin)
    n_fin = sum(len(dws) for _, dws, _, _ in pp_fin)
    n_total = 1 + q * n_blk + n_fin

    # Step A: Every Block r = 1..q forces J_r -> A_r in ALL branches of J_0!
    # Prior to Block r, A_r and H_r were untouched except possibly off-support (-eta) on <= n_total cols:
    verify_pp_adversarial(pp_blk, F(1) - p1 - n_total * eta, -n_total * eta, c_cert)

    # Step B: Every non-(J_0 -> B) branch has B >= u + q*p1 - q*(n_blk - 1)*eta > c_cert and dies!
    assert u + q * p1 - q * (n_blk - 1) * eta > c_cert

    # Step C: Only J_0 -> B survives! Entering Final block:
    #   B >= -(1 - u) + q*p1 - q*(n_blk - 1)*eta,
    #   R_0 >= -q*n_blk*eta (since J_0 -> B gave +(1-u)*eta >= 0, and subsequent cols at most -eta!).
    b_entry = -(F(1) - u) + q * p1 - q * (n_blk - 1) * eta
    r0_entry = -q * n_blk * eta
    verify_pp_adversarial(pp_fin, b_entry, r0_entry, c_cert)

    return c_cert, len(pp_blk), len(pp_fin), n_total


def solve_root(fn, lo: float = 1.0, hi: float = 1.6) -> float:
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if fn(mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo


def main() -> None:
    c3_star = solve_root(lambda c: math.exp(-(c - 1)) + math.exp(1 - 2 * c) - (2 * c - 1))
    print(f"=== Theorem 1: Resolution of m* = 3 (asymptotic limit c_3* = {c3_star:.10f}) ===")

    c_uc, n_uc = verify_m3_ultracompact()
    print(f"  Ultra-compact m = 3, n = {n_uc} (cleaned helper): certified kappa_3 > {c_uc} = {float(c_uc):.6f}")

    m3_rungs = [
        ("m=3 rung 1 (c > 1.000)", F(1, 1), F(99, 100), F(78, 100), 8, 8, F(1, 10**6)),
        ("m=3 rung 2 (c > 1.050)", F(105, 100), F(995, 1000), F(80, 100), 14, 14, F(1, 10**7)),
        ("m=3 rung 3 (c > 1.080)", F(108, 100), F(998, 1000), F(805, 1000), 22, 22, F(1, 10**8)),
        ("m=3 rung 4 (c > 1.095)", F(1095, 1000), F(9995, 10000), F(804, 1000), 45, 45, F(1, 10**9)),
    ]
    for name, c_cert, u, p1, k1, k2, eta in m3_rungs:
        cert, l1, l2, ntot = verify_m3_asymptotic(c_cert, u, p1, k1, k2, eta)
        print(f"  {name}: certified kappa_3 > {float(cert):.6f}  (pp1={l1} lvls, pp2={l2} lvls, n={ntot} cols)")

    print("\n=== Theorem 2: Even-m Zero-Pollution Ladder (exp(-(c-1)) - (c-1) = 2/m) ===")
    for m_val in [4, 6, 8]:
        cm_star = solve_root(lambda c, m=m_val: math.exp(-(c - 1)) - (c - 1) - 2.0 / m)
        print(f"  m = {m_val}: asymptotic limit c_{m_val}* = {cm_star:.10f}")

    even_rungs = [
        ("m=4 rung 1 (c > 1.200)", 4, F(120, 100), F(995, 1000), F(52, 100), 14, 14, F(1, 10**7)),
        ("m=4 rung 2 (c > 1.240)", 4, F(124, 100), F(998, 1000), F(51, 100), 25, 25, F(1, 10**8)),
        ("m=4 rung 3 (c > 1.258)", 4, F(1258, 1000), F(9995, 10000), F(505, 1000), 50, 50, F(1, 10**9)),
        ("m=6 rung 1 (c > 1.320)", 6, F(132, 100), F(998, 1000), F(35, 100), 20, 20, F(1, 10**8)),
        ("m=6 rung 2 (c > 1.355)", 6, F(1355, 1000), F(9995, 10000), F(337, 1000), 45, 45, F(1, 10**9)),
        ("m=8 rung 1 (c > 1.370)", 8, F(137, 100), F(998, 1000), F(27, 100), 22, 22, F(1, 10**8)),
        ("m=8 rung 2 (c > 1.402)", 8, F(1402, 1000), F(9995, 10000), F(256, 1000), 45, 45, F(1, 10**9)),
    ]
    for name, m_val, c_cert, u, p1, kb, kf, eta in even_rungs:
        cert, lb, lf, ntot = verify_even_m_ladder(m_val, c_cert, u, p1, kb, kf, eta)
        print(f"  {name}: certified kappa_{m_val} > {float(cert):.6f}  (blk={lb} lvls, fin={lf} lvls, n={ntot} cols)")

    print("\nALL EXACT RATIONAL CERTIFICATES VERIFIED IN fractions.Fraction!")


if __name__ == "__main__":
    main()
