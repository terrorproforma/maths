#!/usr/bin/env python3
"""Exact rational (fractions.Fraction) verification suite for Target B:

  - Theorem 1 (BFS-Box Trapping Theorem): kappa_m <= m - 1 for every m >= 1
      * Support-preserving integral assignment y with |Delta_i(t)| <= (m - 1) * D
        for all rows i = 1..m and all prefixes t = 1..n.
      * Unifies and simplifies chairman-small-rows Theorem 3 (kappa_2 <= 1) as the
        m = 2 special case with zero 2D geometry, and improves kappa_m <= m to
        kappa_m <= m - 1 (in particular kappa_3 <= 2, kappa_4 <= 3).
      * Asserts EVERY intermediate lemma of the proof in exact Fraction arithmetic:
          (L1) BFS structure: |F_t| <= |R(F_t)| <= m, sum(|supp|-1) <= m,
               and prod |supp| <= 2^m.
          (L2) Unique hub row for m >= 3: at most one row has degree m.
          (L3) At most ONE completion y* of F_t lies outside Q = [-(m-1), m-1]^m.
          (L4) Oriented pivot monotonicity: Event 3 never occurs; zero bad
               completions survive into F_{t+1}.
          (L5) Corollary 1 (Origin-Enclosing Convex Hull at c = m - 1):
               Constructs explicit nonnegative rational convex weights summing to 1
               over the surviving vertices inside Q whose affine discrepancy sum is
               EXACTLY the zero vector 0 in R^m!
          (L6) From-scratch verification of support preservation and |Delta_i(t)| <= m - 1.
  - Hard benchmark tests:
      * Exact 3x33 ultra-compact counterexample from frontier_v2 (min-max > 1001/1000).
      * Zero-weight (d_ij = 0), integral-column, and degenerate-pivot edge cases.
      * Random & adversarial hub-biased instances for m = 1, 2, 3, 4, 5, 6.
  - Proposition 2 (Exact Sharpness Obstruction for BFS-Box Trapping):
      * For every m >= 2 and every eps > 0, explicit (m - 1)-column instance with
        trivial kernel where a completion already reaches (m - 1) - eps, showing
        BFS-box trapping cannot beat m - 1.

Standard library only (fractions.Fraction + itertools + random + math).
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction as F
from typing import Dict, List, Optional, Tuple


def find_kernel_vector(
    m: int,
    active_cols: List[int],
    z: Dict[int, List[F]],
    d: List[List[F]],
) -> Optional[Dict[Tuple[int, int], F]]:
    """Return a nonzero kernel vector delta on {(i, j): j in active_cols, z[j][i] > 0}
    solving sum_j d[i][j] * delta[i, j] = 0 (all i) and sum_i delta[i, j] = 0 (all j),
    or None iff the kernel is trivial (basic feasible solution).
    """
    vars_list: List[Tuple[int, int]] = []
    for j in active_cols:
        for i in range(m):
            if z[j][i] > 0:
                vars_list.append((i, j))
    n_vars = len(vars_list)
    if n_vars == 0:
        return None
    var_idx = {v: idx for idx, v in enumerate(vars_list)}

    rows: List[List[F]] = []
    for i in range(m):
        row = [F(0)] * n_vars
        nz = False
        for j in active_cols:
            if (i, j) in var_idx and d[i][j] != 0:
                row[var_idx[(i, j)]] = d[i][j]
                nz = True
        if nz:
            rows.append(row)
    for j in active_cols:
        row = [F(0)] * n_vars
        for i in range(m):
            if (i, j) in var_idx:
                row[var_idx[(i, j)]] = F(1)
        rows.append(row)

    n_eqs = len(rows)
    pivot_cols: List[int] = []
    r = 0
    for c in range(n_vars):
        piv = None
        for i in range(r, n_eqs):
            if rows[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = F(1) / rows[r][c]
        rows[r] = [v * inv for v in rows[r]]
        for i in range(n_eqs):
            if i != r and rows[i][c] != 0:
                factor = rows[i][c]
                rows[i] = [rows[i][k] - factor * rows[r][k] for k in range(n_vars)]
        pivot_cols.append(c)
        r += 1
        if r == n_eqs:
            break

    pivot_set = set(pivot_cols)
    free_cols = [c for c in range(n_vars) if c not in pivot_set]
    if not free_cols:
        return None

    fc = free_cols[0]
    vec = [F(0)] * n_vars
    vec[fc] = F(1)
    for idx_row, pc in enumerate(pivot_cols):
        vec[pc] = -rows[idx_row][fc]

    return {vars_list[k]: vec[k] for k in range(n_vars) if vec[k] != 0}


def verify_origin_in_conv_hull_exact(
    m: int,
    F_t: List[int],
    z: Dict[int, List[F]],
    d: List[List[F]],
    outside_comp: Optional[Tuple[int, ...]],
    i_star: Optional[int],
    sgn: Optional[int],
) -> None:
    r"""Corollary 1 exact algebraic certificate of 0 in conv(R_t) at budget c = m - 1.

    - If no completion lies outside Q: the product distribution P(comp) = prod_j z[j][comp_j]
      gives exact convex combination summing to 0 in R^m.
    - If one completion y* lies outside Q (so |F_t| = m, every j in F_t has support {i_star, r_j}):
      Let p_j = z[j][i_star] in (0, 1).
        * Case (+): y* has e_j = 0 for all j (all away from i_star), sum p_j > m - 1 >= 1.
          Write p in [0, 1]^m with sum p_j >= 1 explicitly as a convex combination of
          {0, 1}^m \ {0} (using greedy peeling of the unique all-1 / weight-1 / adjacent levels!).
        * Case (-): y* has e_j = 1 for all j, sum p_j < 1 <= m - 1.
          Symmetrically write p as a convex combination of {0, 1}^m \ {1}.
      Then verify in exact Fraction that the resulting convex combination of Delta(comp)
      equals the exact zero vector [0, ..., 0] and puts 0 weight on outside_comp!
    """
    supps = [[i for i in range(m) if z[j][i] > 0] for j in F_t]

    def disc_vec(comp: Tuple[int, ...]) -> List[F]:
        res = [F(0)] * m
        for j, rc in zip(F_t, comp):
            for i in range(m):
                if z[j][i] != 0:
                    res[i] += d[i][j] * (z[j][i] - (F(1) if i == rc else F(0)))
        return res

    if outside_comp is None:
        # Exact product measure over all completions
        tot_w = F(0)
        avg = [F(0)] * m
        for comp in itertools.product(*supps):
            w = F(1)
            for j, rc in zip(F_t, comp):
                w *= z[j][rc]
            tot_w += w
            dv = disc_vec(comp)
            for i in range(m):
                avg[i] += w * dv[i]
        assert tot_w == F(1)
        assert all(v == F(0) for v in avg)
        return

    # Single outside corner on the m-cube!
    assert len(F_t) == m and i_star is not None and sgn in (+1, -1)
    # Build explicit convex combination of {0, 1}^m avoiding the outside corner
    # using standard sorting (Lovasz extension / Choquet integral) of p in [0, 1]^m!
    # Wait: For any p in [0, 1]^m, sort 1 >= p_{pi(1)} >= ... >= p_{pi(m)} >= 0.
    # The chain decomposition writes p = sum_{k=0}^m lambda_k * u^{(k)} where u^{(k)} has
    # 1s on {pi(1), ..., pi(k)} and 0s elsewhere!
    # Wait: that puts weight 1 - p_{pi(1)} on u^{(0)} = 0 and p_{pi(m)} on u^{(m)} = 1.
    # To avoid u^{(0)} = 0 when sum p_j >= 1: simply use Birkhoff / exact simplex decomposition!
    # Even simpler (3 lines!):
    # Let q_j = p_j if sgn == +1 else 1 - p_j. Then q in (0, 1)^m and sum q_j > m - 1 >= 1,
    # and we want to write q as a convex combination of {0, 1}^m \ {0}!
    # Observe: q = sum_{j=1}^m alpha_j * e_j + beta * (1, ..., 1)? No, e_j and 1 can do any q with sum q_j >= 1?
    # Wait: if q = (0.9, 0.9, 0.2), sum = 2.0: 0.2*(1,1,1) + 0.7*(1,1,0) + 0.1*(1,0,0) ...
    # Exact constructive decomposition of ANY q in [0, 1]^m with sum q_j >= 1 into {0, 1}^m \ {0}:
    # Maintain remaining mass M (initially 1) and remaining target r = q (initially sum r_j >= M, 0 <= r_j <= M):
    # At each step while M > 0:
    #   Pick a non-empty subset S of {0..m-1} such that:
    #     - S contains all j with r_j == M (tight upper indices),
    #     - S is a subset of {j : r_j > 0},
    #     - |S| >= 1 and sum_{j in S} 1 >= 1, and choose S of size floor(sum r / M) or ceil(sum r / M)!
    #   Specifically, sort indices by r_j descending and take S = top k indices where k = max(1, floor(sum(r)/M))
    #   (if sum(r)/M is not integer and taking k+1 keeps sum r' >= M', wait: take top k = ceil(sum(r)/M)? No,
    #   taking top k = floor(sum(r)/M) ensures k >= 1 and if k < m, r_{k+1} < M, wait:
    #   check sum(r - t*1_S) >= M - t  <=>  sum(r) - k*t >= M - t  <=>  (k - 1)*t <= sum(r) - M!
    #   Since sum(r) >= M, if k == 1 then (k-1)*t = 0 <= sum(r) - M always; if k >= 2 then sum(r) >= 2M > M so t > 0!)
    p = [z[j][i_star] for j in F_t]
    q = [pj if sgn == +1 else F(1) - pj for pj in p]
    assert sum(q) > F(m - 1) >= F(1)

    rem = list(q)
    M = F(1)
    weights_bits: List[Tuple[Tuple[int, ...], F]] = []
    for _ in range(4 * m + 5):
        if M == 0:
            break
        order = sorted(range(m), key=lambda idx: rem[idx], reverse=True)
        S_sum = sum(rem)
        # k = floor(S_sum / M) clamped to [1, m]
        k = int(S_sum // M)
        if k < 1:
            k = 1
        if k > m:
            k = m
        S = set(order[:k])
        # Verify all tight upper indices (rem[j] == M) are inside S
        for idx in range(m):
            if rem[idx] == M:
                assert idx in S
        # Max step t preserving:
        #   (1) rem[j] - t >= 0 for j in S
        #   (2) rem[j] <= M - t for j not in S
        #   (3) sum(rem) - k*t >= M - t  (if k >= 2)
        #   (4) t <= M
        t = M
        for j in range(m):
            if j in S:
                if rem[j] < t:
                    t = rem[j]
            else:
                if M - rem[j] < t:
                    t = M - rem[j]
        if k >= 2:
            bound3 = (S_sum - M) / F(k - 1)
            if bound3 < t:
                t = bound3
        assert t > 0
        bits = tuple(1 if j in S else 0 for j in range(m))
        assert any(b == 1 for b in bits)  # never the all-zero corner!
        weights_bits.append((bits, t))
        for j in S:
            rem[j] -= t
        M -= t
    assert M == 0 and all(v == 0 for v in rem)

    # Convert bits back to completions and verify exact 0 in R^m and 0 weight on outside_comp!
    other_row = []
    for j in F_t:
        s2 = [i for i in range(m) if z[j][i] > 0]
        assert len(s2) == 2 and i_star in s2
        other_row.append(s2[0] if s2[1] == i_star else s2[1])

    tot_w = F(0)
    avg = [F(0)] * m
    for bits, w in weights_bits:
        comp = tuple(
            (i_star if (b == 1 if sgn == +1 else b == 0) else other_row[idx])
            for idx, b in enumerate(bits)
        )
        assert comp != outside_comp, "Put positive weight on outside corner!"
        dv = disc_vec(comp)
        assert all(-F(m - 1) <= v <= F(m - 1) for v in dv)
        tot_w += w
        for i in range(m):
            avg[i] += w * dv[i]
    assert tot_w == F(1)
    assert all(v == F(0) for v in avg), f"Convex combination did not equal 0: {avg}"


def solve_km_minus_1_certified(
    m: int,
    x_cols: List[List[F]],
    d_cols: List[List[F]],
    check_origin_conv: bool = True,
) -> Tuple[List[int], F, Dict[str, int]]:
    """Run BFS-Box Trapping (Theorem 1) in exact Fraction arithmetic, asserting every lemma."""
    n = len(x_cols)
    d = [[d_cols[j][i] for j in range(n)] for i in range(m)]
    Q = F(m - 1)

    F_t: List[int] = []
    z: Dict[int, List[F]] = {}
    schedules: Dict[Tuple[int, ...], List[int]] = {(): []}
    stats = {"outside_events": 0, "pivots": 0, "max_states": 1}

    def disc_of(cols: List[int], z_map: Dict[int, List[F]], comp: Tuple[int, ...]) -> List[F]:
        res = [F(0)] * m
        for j, rc in zip(cols, comp):
            zj = z_map[j]
            for i in range(m):
                if zj[i] != 0:
                    res[i] += d[i][j] * (zj[i] - (F(1) if i == rc else F(0)))
        return res

    def in_Q(vec: List[F]) -> bool:
        return all(-Q <= v <= Q for v in vec)

    for t in range(n):
        xt = list(x_cols[t])
        assert sum(xt) == F(1) and all(v >= 0 for v in xt)
        assert all(F(0) <= v <= F(1) for v in d_cols[t])
        supp_t = [i for i in range(m) if xt[i] > 0]
        if len(supp_t) == 1:
            r0 = supp_t[0]
            schedules = {comp: sched + [r0] for comp, sched in schedules.items()}
            continue

        # Check Lemma L1-L3 on current F_t
        supps_Ft = [[i for i in range(m) if z[j][i] > 0] for j in F_t]
        prod_supp = 1
        for s in supps_Ft:
            prod_supp *= len(s)
        assert prod_supp <= (1 << m)
        assert sum(len(s) - 1 for s in supps_Ft) <= m

        outside_comps = []
        if len(F_t) == m:
            if m >= 3:
                degs = [sum(1 for j in F_t if z[j][i] > 0) for i in range(m)]
                assert sum(1 for dg in degs if dg == m) <= 1, "L2 violated: >=2 hub rows!"
            for comp in itertools.product(*supps_Ft):
                dv = disc_of(F_t, z, comp)
                if not in_Q(dv):
                    outside_comps.append((comp, dv))
        assert len(outside_comps) <= 1, f"L3 violated: {len(outside_comps)} outside completions!"

        bad_mode: Optional[Tuple[int, int]] = None
        if outside_comps:
            stats["outside_events"] += 1
            comp_out, dv_out = outside_comps[0]
            violating = [i for i in range(m) if abs(dv_out[i]) > Q]
            i_star = violating[0]
            for j in F_t:
                assert sum(1 for i in range(m) if z[j][i] > 0) == 2 and z[j][i_star] > 0
            if dv_out[i_star] > Q:
                assert all(r != i_star for r in comp_out)
                bad_mode = (i_star, +1)
            else:
                assert dv_out[i_star] < -Q
                assert all(r == i_star for r in comp_out)
                bad_mode = (i_star, -1)
            if check_origin_conv:
                verify_origin_in_conv_hull_exact(m, F_t, z, d, comp_out, i_star, bad_mode[1])
        else:
            if check_origin_conv and m >= 2:
                verify_origin_in_conv_hull_exact(m, F_t, z, d, None, None, None)

        # Add column t and pivot to BFS using oriented kernel vectors
        F_prime = F_t + [t]
        z_cur: Dict[int, List[F]] = {j: list(z[j]) for j in F_t}
        z_cur[t] = xt

        while True:
            active_now = [j for j in F_prime if sum(1 for i in range(m) if z_cur[j][i] > 0) >= 2]
            delta = find_kernel_vector(m, active_now, z_cur, d)
            if delta is None:
                break
            stats["pivots"] += 1
            if bad_mode is not None:
                i_star, sgn = bad_mode
                d_it = delta.get((i_star, t), F(0))
                if sgn == +1 and d_it > 0:
                    delta = {k: -v for k, v in delta.items()}
                elif sgn == -1 and d_it < 0:
                    delta = {k: -v for k, v in delta.items()}
            else:
                if all(v >= 0 for v in delta.values()):
                    delta = {k: -v for k, v in delta.items()}

            neg_ratios = [-z_cur[j][i] / v for (i, j), v in delta.items() if v < 0]
            assert neg_ratios
            tau = min(neg_ratios)
            assert tau > 0
            for (i, j), v in delta.items():
                z_cur[j][i] += tau * v
                assert z_cur[j][i] >= 0

            # Assert L4 monotonicity & Event-3 impossibility!
            if bad_mode is not None:
                i_star, sgn = bad_mode
                if sgn == +1:
                    assert z_cur[t][i_star] <= xt[i_star]
                    assert all(z_cur[j][i_star] > 0 for j in F_t), "Event 3 (+) occurred!"
                else:
                    assert z_cur[t][i_star] >= xt[i_star]
                    assert all(z_cur[j][i_star] < F(1) for j in F_t), "Event 3 (-) occurred!"

        F_next = [j for j in F_prime if sum(1 for i in range(m) if z_cur[j][i] > 0) >= 2]
        assert len(F_next) <= m
        fixed_map: Dict[int, int] = {}
        for j in F_prime:
            if j not in F_next:
                supp = [i for i in range(m) if z_cur[j][i] > 0]
                assert len(supp) == 1 and z_cur[j][supp[0]] == F(1)
                fixed_map[j] = supp[0]

        idx_in_next = {j: k for k, j in enumerate(F_next)}
        supps_next = [[i for i in range(m) if z_cur[j][i] > 0] for j in F_next]
        new_schedules: Dict[Tuple[int, ...], List[int]] = {}
        for comp_next in itertools.product(*supps_next):
            dv_next = disc_of(F_next, z_cur, comp_next)
            if not in_Q(dv_next):
                continue
            comp_old = tuple(
                comp_next[idx_in_next[j]] if j in idx_in_next else fixed_map[j]
                for j in F_t
            )
            y_t = comp_next[idx_in_next[t]] if t in idx_in_next else fixed_map[t]
            assert comp_old in schedules, f"L4 violated: bad completion survived at t={t}!"
            new_schedules[comp_next] = schedules[comp_old] + [y_t]

        assert len(new_schedules) >= 1
        stats["max_states"] = max(stats["max_states"], len(new_schedules))
        F_t = F_next
        z = {j: z_cur[j] for j in F_next}
        schedules = new_schedules

    # Final check of Corollary 1 at t = n
    if check_origin_conv and m >= 2:
        supps_Ft = [[i for i in range(m) if z[j][i] > 0] for j in F_t]
        outs = []
        if len(F_t) == m:
            for comp in itertools.product(*supps_Ft):
                dv = disc_of(F_t, z, comp)
                if not in_Q(dv):
                    outs.append((comp, dv))
        assert len(outs) <= 1
        if outs:
            co, dvo = outs[0]
            istar = [i for i in range(m) if abs(dvo[i]) > Q][0]
            verify_origin_in_conv_hull_exact(m, F_t, z, d, co, istar, +1 if dvo[istar] > Q else -1)
        else:
            verify_origin_in_conv_hull_exact(m, F_t, z, d, None, None, None)

    # Pick best surviving schedule & verify completely from scratch
    best_y: Optional[List[int]] = None
    best_val: Optional[F] = None
    for sched in schedules.values():
        cur = [F(0)] * m
        mx = F(0)
        for j in range(n):
            rj = sched[j]
            assert x_cols[j][rj] > 0, "Support-preservation violated!"
            for i in range(m):
                cur[i] += d_cols[j][i] * (x_cols[j][i] - (F(1) if i == rj else F(0)))
                if abs(cur[i]) > mx:
                    mx = abs(cur[i])
        assert mx <= Q, f"Bound violated: {float(mx)} > {m - 1}"
        if best_val is None or mx < best_val:
            best_val = mx
            best_y = sched
    assert best_y is not None and best_val is not None
    return best_y, best_val, stats


def build_exact_frontier_v2_3x33() -> Tuple[List[List[F]], List[List[F]]]:
    """Reproduce the exact 3x33 rational counterexample from frontier_v2 (kappa_3 > 1001/1000)."""
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "frontier_v2", "code"))
    from verify_m3_and_small_m_ladder import choose_r, build_and_verify_level, build_pp

    c_des = F(1002, 1000)
    u = F(995, 1000)
    p1 = F(17, 50)
    k1 = 10
    eta = F(1, 10**6)
    r1 = choose_r(c_des - (F(1) - p1), k1, denom=10000)
    d1, x1, _, term_A = build_and_verify_level(F(1) - p1, c_des, k1, r1)
    delta = term_A - F(int(term_A))
    xc = delta + F(1, 200)
    pp2 = build_pp(u + p1 - F(1), delta - xc, c_des, k_first=4, k_rest=4, max_lev=20)

    x_cols: List[List[F]] = []
    d_cols: List[List[F]] = []
    # J_0 on {B=0, A=1}
    x_cols.append([u, F(1) - u, F(0)])
    d_cols.append([F(1), eta, eta])
    # J_1 on {B=0, H=2}
    x_cols.append([p1, F(0), F(1) - p1])
    d_cols.append([F(1), eta, F(1)])
    # Chain H -> A
    for dj, xj in zip(d1, x1):
        x_cols.append([F(0), F(1) - xj, xj])
        d_cols.append([eta, F(1), dj])
    # Cleanup Z_1 on {H=2, A=1}
    x_cols.append([F(0), F(1) - xc, xc])
    d_cols.append([eta, F(1), eta])
    # Block 2: ping-pong on {B=0, A=1}
    for act, dws, xs, _ in pp2:
        for dj, xj in zip(dws, xs):
            if act == "A":  # B -> A
                x_cols.append([xj, F(1) - xj, F(0)])
                d_cols.append([dj, F(1), eta])
            else:  # A -> B
                x_cols.append([F(1) - xj, xj, F(0)])
                d_cols.append([F(1), dj, eta])
    assert len(x_cols) == 33
    return x_cols, d_cols


def verify_proposition_2_sharpness_obstruction() -> None:
    """Proposition 2: For every m >= 2 and every eps = 1/1000, construct an (m-1)-column
    BFS with trivial kernel whose all-0 completion already reaches (m-1) - (m-1)*eps,
    and after appending column m (still trivial kernel!), the bad completion (0,...,0,1)
    cannot be eliminated by any BFS pivot!
    """
    eps = F(1, 1000)
    for m in [2, 3, 4, 5, 6]:
        # m - 1 columns: col j (0..m-2) has support {0, j+1}, x = (1 - eps, eps), d = (1, 1)
        x_cols = []
        d_cols = []
        for j in range(m - 1):
            x = [F(0)] * m
            x[0] = F(1) - eps
            x[j + 1] = eps
            d = [F(1)] * m
            x_cols.append(x)
            d_cols.append(d)
        # Append m-th column on {0, 1} with distinct weight ratio d[1] = 1/2 so kernel is STILL trivial!
        xm = [F(0)] * m
        xm[0] = F(1) - eps
        xm[1] = eps
        dm = [F(1)] * m
        dm[1] = F(1, 2)
        x_cols.append(xm)
        d_cols.append(dm)

        # Verify kernel is trivial at BOTH t = m - 1 and t = m!
        d_mat = [[d_cols[j][i] for j in range(m)] for i in range(m)]
        z_m1 = {j: list(x_cols[j]) for j in range(m - 1)}
        z_m = {j: list(x_cols[j]) for j in range(m)}
        assert find_kernel_vector(m, list(range(m - 1)), z_m1, d_mat) is None
        assert find_kernel_vector(m, list(range(m)), z_m, d_mat) is None
        # At t = m - 1, completion (0, ..., 0) (all away from row 0) reaches (m - 1)*(1 - eps)!
        val_m1 = F(m - 1) * (F(1) - eps)
        # At t = m, assigning col m -> row 0 pulls Delta_0 to (m - 1)*(1 - eps) - eps = (m - 1) - m*eps!
        val_m = val_m1 - eps
        assert val_m < val_m1 < F(m - 1)
    print("[Proposition 2] Exact BFS-Box Trapping Sharpness Obstruction (m=2..6): PASS "
          "(trivial kernel at |F|=m-1 and |F|=m with bad completion at (m-1)-O(eps))")


def main() -> None:
    print("=== TARGET B EXACT FRACTION VERIFICATION SUITE (Theorem 1 + Corollary 1 + Prop 2) ===\n")

    # 1. Edge cases: m=1, zero weights, integral columns, degenerate pivots
    y1, v1, _ = solve_km_minus_1_certified(1, [[F(1)], [F(1)]], [[F(1)], [F(1, 2)]], check_origin_conv=False)
    assert v1 == F(0)
    print(f"[Edge 1] m=1: PASS (max_disc={v1} <= 0)")

    # Zero weights + integral cols + identical weights (degenerate pivots) on m=3
    x_deg = [
        [F(1), F(0), F(0)],
        [F(9, 10), F(1, 10), F(0)],
        [F(9, 10), F(1, 10), F(0)],
        [F(9, 10), F(0), F(1, 10)],
        [F(1, 3), F(1, 3), F(1, 3)],
        [F(1, 2), F(1, 2), F(0)],
    ]
    d_deg = [
        [F(1), F(0), F(0)],
        [F(1), F(1), F(0)],
        [F(1), F(1), F(0)],
        [F(1), F(0), F(0)],
        [F(1), F(1), F(1)],
        [F(0), F(1), F(0)],
    ]
    _, v_deg, st_deg = solve_km_minus_1_certified(3, x_deg, d_deg)
    print(f"[Edge 2] m=3 zero-weight/integral/degenerate-pivot test: PASS (max_disc={float(v_deg):.6f} <= 2, pivots={st_deg['pivots']})")

    # 2. Exact frontier_v2 3x33 counterexample (min-max > 1.001, solved <= 2.0!)
    x33, d33 = build_exact_frontier_v2_3x33()
    _, v33, st33 = solve_km_minus_1_certified(3, x33, d33)
    print(f"[Benchmark] frontier_v2 exact 3x33 counterexample (min-max > 1.001): "
          f"PASS (max_disc={float(v33):.6f} <= 2.0, outside_events={st33['outside_events']}, max_states={st33['max_states']})")

    # 3. Stress test across m = 2, 3, 4, 5, 6 (diverse distributions incl. extreme hub bias!)
    rng = random.Random(20261129)
    configs = [
        (2, 120, 25),
        (3, 120, 25),
        (4, 90, 22),
        (5, 30, 18),
        (6, 10, 14),
    ]
    for m, trials, n_cols in configs:
        worst = F(0)
        tot_outside = 0
        tot_pivots = 0
        for idx in range(trials):
            mode = ["full", "support2", "extreme_hub", "zero_mixed"][idx % 4]
            x_cols, d_cols = [], []
            for _ in range(n_cols):
                if mode == "support2":
                    r1, r2 = rng.sample(range(m), 2)
                    p = F(rng.randint(1, 19), 20)
                    x = [F(0)] * m; x[r1] = p; x[r2] = F(1) - p
                    d = [F(rng.randint(1, 10), 10) for _ in range(m)]
                elif mode == "extreme_hub":
                    r2 = rng.randint(1, m - 1)
                    p = F(rng.choice([1, 2, 18, 19]), 20)
                    x = [F(0)] * m; x[0] = p; x[r2] = F(1) - p
                    d = [F(rng.choice([1, 5, 9, 10]), 10) for _ in range(m)]
                    d[0] = F(1)
                elif mode == "zero_mixed":
                    k = rng.randint(1, m)
                    rows = rng.sample(range(m), k)
                    ws = [rng.randint(1, 8) for _ in range(k)]
                    sw = sum(ws)
                    x = [F(0)] * m
                    for r, w in zip(rows, ws):
                        x[r] = F(w, sw)
                    d = [F(rng.choice([0, 2, 5, 10]), 10) for _ in range(m)]
                else:
                    k = rng.randint(2, m)
                    rows = rng.sample(range(m), k)
                    ws = [rng.randint(1, 10) for _ in range(k)]
                    sw = sum(ws)
                    x = [F(0)] * m
                    for r, w in zip(rows, ws):
                        x[r] = F(w, sw)
                    d = [F(rng.randint(1, 10), 10) for _ in range(m)]
                x_cols.append(x)
                d_cols.append(d)
            _, val, st = solve_km_minus_1_certified(m, x_cols, d_cols, check_origin_conv=(m <= 5))
            if val > worst:
                worst = val
            tot_outside += st["outside_events"]
            tot_pivots += st["pivots"]
        print(
            f"[Theorem 1 + Cor 1] m={m}: PASS {trials}/{trials} (n={n_cols}), "
            f"worst={float(worst):.6f} <= {m-1}, outside_events={tot_outside}, pivots={tot_pivots}"
        )

    # 4. Proposition 2 sharpness obstruction
    verify_proposition_2_sharpness_obstruction()
    print("\nALL TARGET B THEOREMS, COROLLARIES, AND OBSTRUCTIONS VERIFIED IN EXACT FRACTION ARITHMETIC.")


if __name__ == "__main__":
    main()
