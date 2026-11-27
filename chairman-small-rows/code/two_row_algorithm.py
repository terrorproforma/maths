"""Constructive proof of the two-row theorem, as an exact linear-time algorithm.

Theorem.  Let d be a 2 x n matrix of weights in [0, D] and x a fractional assignment.
Then there is an integral assignment y with |disc_i(t)| <= D for both rows i and every
prefix t, where disc_i(t) = sum_{j <= t} d_ij (x_ij - y_ij).

Planar form (D = 1).  Put h_j = (d_1j, d_2j), w_j = x_1j and y_j = 1 when column j goes to
row 1.  Then p_t = (-disc_1(t), disc_2(t)) = sum_{j <= t} (y_j - w_j) h_j, and each column
moves the point by +(1 - w) h or by -w h.  Q is the square [-1, 1]^2.

Invariant.  There are g1, g2 in [0,1]^2 and l1, l2 in [0,1] such that each of the four
points  pi(e) = (e1 - l1) g1 + (e2 - l2) g2,  e in {0,1}^2,  that lies in Q is reachable by
a path that stays in Q.  The points pi(1,0) and pi(0,1) always lie in Q, so the invariant
gives a reachable point.

Step.  With the new column as third generator (g3, l3) = (h, w), the eight points
P(e) = sum_i (e_i - l_i) g_i are candidates.  The proof (notes/two_rows.md, Theorem 3)
shows that some face {e_k = c} of the cube has the origin in the convex hull of its four
points and contains no "bad" vertex (a point in Q whose parent pi is outside Q).  That
face is the new parallelogram.  This file follows the proof literally and asserts every
claim it uses, in exact rational arithmetic.

Standard library only.
"""
from fractions import Fraction as F
from itertools import product

ZERO, ONE = F(0), F(1)


def in_q(p):
    return -1 <= p[0] <= 1 and -1 <= p[1] <= 1


def comb(coeffs, gens):
    return (sum(c * g[0] for c, g in zip(coeffs, gens)),
            sum(c * g[1] for c, g in zip(coeffs, gens)))


def middle(gens):
    """Lemma M: indices (m, a, c) and p, q >= 0 with g_m = p g_a + q g_c."""
    for m in (2, 1, 0):
        a, c = [i for i in range(3) if i != m]
        gm, ga, gc = gens[m], gens[a], gens[c]
        if gm == (ZERO, ZERO):
            return m, a, c, ZERO, ZERO
        det = ga[0] * gc[1] - ga[1] * gc[0]
        if det != 0:
            p = (gm[0] * gc[1] - gm[1] * gc[0]) / det
            q = (ga[0] * gm[1] - ga[1] * gm[0]) / det
            if p >= 0 and q >= 0:
                return m, a, c, p, q
        else:
            for (s, other) in ((a, c), (c, a)):
                gs = gens[s]
                if gs != (ZERO, ZERO) and gm[0] * gs[1] - gm[1] * gs[0] == 0:
                    r = gm[0] / gs[0] if gs[0] != 0 else gm[1] / gs[1]
                    if r >= 0:
                        return (m, a, c, r, ZERO) if s == a else (m, a, c, ZERO, r)
    raise AssertionError("Lemma M failed")


def solve(columns, respect_support=True, check=True):
    """columns: list of (d1, d2, x1) with d1, d2, x1 in [0, 1] (Fractions).

    Returns y (list of 0/1; 1 means the column goes to row 1) with all prefix
    discrepancies of absolute value at most 1.  With respect_support, a column with
    x1 = 0 goes to row 2 and a column with x1 = 1 goes to row 1.
    """
    gens = [(ZERO, ZERO), (ZERO, ZERO)]
    lam = [ZERO, ZERO]
    paths = {e: [] for e in product((0, 1), repeat=2)}   # all four points are the origin

    for (d1, d2, x1) in columns:
        h, w = (F(d1), F(d2)), F(x1)
        assert 0 <= h[0] <= 1 and 0 <= h[1] <= 1 and 0 <= w <= 1
        if respect_support and w in (ZERO, ONE):
            # the forced move does not move the point: keep the parallelogram
            paths = {e: (None if pth is None else pth + [int(w)]) for e, pth in paths.items()}
            continue

        g = gens + [h]
        l = lam + [w]
        P = {e: comb([e[i] - l[i] for i in range(3)], g) for e in product((0, 1), repeat=3)}
        pi = {e: comb([e[i] - lam[i] for i in range(2)], gens) for e in product((0, 1), repeat=2)}
        if check:
            assert in_q(pi[(1, 0)]) and in_q(pi[(0, 1)])
            for e, pt in pi.items():
                assert (not in_q(pt)) or paths[e] is not None, "invariant broken"
        bad = [e for e in P if in_q(P[e]) and not in_q(pi[e[:2]])]
        assert set(bad) <= {(0, 0, 1), (1, 1, 0)} and len(bad) <= 1, "Claim B failed"

        m, a, c, p, q = middle(g)
        if m != 2 and c != 2:            # make the new generator play the role of c
            a, c, p, q = c, a, q, p
        if not bad:
            plus = True
        elif bad[0] == (0, 0, 1):
            plus = (m != 2)
        else:
            plus = (m == 2)

        # Lemma T: slide along g_m = p g_a + q g_c until a coefficient reaches 0 or 1
        if plus:      # mu = (l_a - tau p, l_m + tau, l_c - tau q)
            cands = [(1 - l[m], m, 1)]
            if p > 0:
                cands.append((l[a] / p, a, 0))
            if q > 0:
                cands.append((l[c] / q, c, 0))
            tau = min(t for t, _, _ in cands)
            mu = list(l)
            mu[a], mu[m], mu[c] = l[a] - tau * p, l[m] + tau, l[c] - tau * q
        else:         # mu = (l_a + tau p, l_m - tau, l_c + tau q)
            cands = [(l[m], m, 0)]
            if p > 0:
                cands.append(((1 - l[a]) / p, a, 1))
            if q > 0:
                cands.append(((1 - l[c]) / q, c, 1))
            tau = min(t for t, _, _ in cands)
            mu = list(l)
            mu[a], mu[m], mu[c] = l[a] + tau * p, l[m] - tau, l[c] + tau * q
        assert all(0 <= v <= 1 for v in mu)
        assert comb(mu, g) == comb(l, g)

        faces = [(k, cc) for t, k, cc in cands if t == tau]
        allowed = [(k, cc) for (k, cc) in faces if all(b[k] != cc for b in bad)]
        assert allowed, "Claim F failed: every face through the origin contains a bad vertex"
        k, cc = allowed[0]
        assert mu[k] == cc
        i, j = [r for r in range(3) if r != k]

        new_gens = [g[i], g[j]]
        new_lam = [mu[i], mu[j]]
        new_paths = {}
        for e2 in product((0, 1), repeat=2):
            e = [0, 0, 0]
            e[i], e[j], e[k] = e2[0], e2[1], cc
            e = tuple(e)
            pt = P[e]
            assert pt == comb([e2[0] - new_lam[0], e2[1] - new_lam[1]], new_gens)
            if in_q(pt):
                parent = paths[e[:2]]
                assert in_q(pi[e[:2]]) and parent is not None, "a bad vertex was used"
                new_paths[e2] = parent + [e[2]]
            else:
                new_paths[e2] = None
        gens, lam, paths = new_gens, new_lam, new_paths

    y = paths[(1, 0)]
    assert y is not None
    return y


def max_discrepancy(columns, y):
    """Exact max over rows and prefixes of |disc_i(t)| for the assignment y."""
    s1 = s2 = ZERO
    worst = ZERO
    for (d1, d2, x1), yj in zip(columns, y):
        d1, d2, x1 = F(d1), F(d2), F(x1)
        s1 += d1 * (x1 - yj)
        s2 += d2 * ((1 - x1) - (1 - yj))
        worst = max(worst, abs(s1), abs(s2))
    return worst
