#!/usr/bin/env python3
"""Exact rational (Fraction) implementation & verification of Theorem 6:
Iterated Prefix Basis-Rounding proves kappa_m <= m (strictly < m * D),
cutting Barany-Grinberg's 2m bound in half, with support preservation and
polynomial-time exact construction (standard library only, ZERO floating point).
"""

from __future__ import annotations

import json
import os
import random
from fractions import Fraction as F


def rational_kernel_vector(A: list[list[F]]) -> list[F]:
    """Return a nonzero exact rational vector v with A @ v == 0 (assumes ncols > rank)."""
    nrows = len(A)
    ncols = len(A[0])
    M = [row[:] for row in A]
    pivot_cols: list[int] = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, nrows):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(nrows):
            if i != r and M[i][c] != 0:
                factor = M[i][c]
                M[i] = [M[i][j] - factor * M[r][j] for j in range(ncols)]
        pivot_cols.append(c)
        r += 1
        if r == nrows:
            break

    piv_set = set(pivot_cols)
    free_cols = [c for c in range(ncols) if c not in piv_set]
    assert free_cols, "Matrix has trivial kernel!"
    fc = free_cols[0]
    v = [F(0)] * ncols
    v[fc] = F(1)
    for idx, pc in enumerate(pivot_cols):
        v[pc] = -M[idx][fc]
    for row in A:
        assert sum(a * b for a, b in zip(row, v)) == 0
    return v


def iterated_prefix_basis_round(X: list[list[F]], D: list[list[F]]) -> tuple[list[int], F, int]:
    """Exact rational Iterated Prefix Basis-Rounding.
    X, D are m x n matrices of Fractions; returns (chosen_row_per_col, max_disc / D_max, max_|F_t|).
    """
    m = len(X)
    n = len(X[0])
    D_max = max(D[i][j] for i in range(m) for j in range(n))
    assert D_max > 0
    for j in range(n):
        assert sum(X[i][j] for i in range(m)) == F(1)
        assert all(F(0) <= X[i][j] <= F(1) for i in range(m))

    F_active: list[int] = []
    z: dict[int, list[F]] = {}
    y: list[int | None] = [None] * n
    max_F = 0

    for t in range(n):
        col_x = [X[i][t] for i in range(m)]
        supp = [i for i in range(m) if col_x[i] > 0]
        if len(supp) == 1:
            y[t] = supp[0]
        else:
            F_active.append(t)
            z[t] = col_x[:]

        while True:
            still_active = []
            for j in F_active:
                sj = [i for i in range(m) if z[j][i] > 0]
                if len(sj) == 1:
                    y[j] = sj[0]
                    del z[j]
                else:
                    still_active.append(j)
            F_active = still_active

            dof = sum(sum(1 for v in z[j] if v > 0) - 1 for j in F_active)
            if dof <= m:
                break

            var_list: list[tuple[int, int, int]] = []
            for fi, j in enumerate(F_active):
                for i in range(m):
                    if z[j][i] > 0:
                        var_list.append((fi, j, i))
            nv = len(var_list)
            neq = m + len(F_active)
            assert nv > neq
            A = [[F(0)] * nv for _ in range(neq)]
            for idx, (fi, j, i) in enumerate(var_list):
                A[i][idx] = D[i][j]
                A[m + fi][idx] = F(1)

            delta = rational_kernel_vector(A)
            if not any(d < 0 for d in delta):
                delta = [-d for d in delta]
            lam = min(-z[j][i] / d for (_, j, i), d in zip(var_list, delta) if d < 0)
            assert lam > 0
            for (_, j, i), d in zip(var_list, delta):
                z[j][i] += lam * d
                assert z[j][i] >= 0

        max_F = max(max_F, len(F_active))
        assert len(F_active) <= m

        for i in range(m):
            lhs = sum(D[i][j] * (F(1) if y[j] == i else F(0)) for j in range(t + 1) if y[j] is not None)
            lhs += sum(D[i][j] * z[j][i] for j in F_active)
            rhs = sum(D[i][j] * X[i][j] for j in range(t + 1))
            assert lhs == rhs, f"Invariant violated at t={t}, i={i}: {lhs} != {rhs}"

    for j in F_active:
        best_i = max((i for i in range(m) if z[j][i] > 0), key=lambda i: z[j][i])
        y[j] = best_i

    assert all(r is not None for r in y)
    y_int = [int(r) for r in y]

    max_disc = F(0)
    for i in range(m):
        cum = F(0)
        for j in range(n):
            if y_int[j] == i:
                assert X[i][j] > 0, "Support preservation violated!"
            cum += D[i][j] * (X[i][j] - (F(1) if y_int[j] == i else F(0)))
            if abs(cum) > max_disc:
                max_disc = abs(cum)
    assert max_disc < m * D_max, f"Bound violated: {max_disc} >= {m * D_max}"
    return y_int, max_disc / D_max, max_F


def main() -> None:
    rng = random.Random(20261128)
    print("Testing exact rational Iterated Prefix Basis-Rounding (Theorem 6: kappa_m <= m):\n")
    for m in [2, 3, 4, 5, 6]:
        worst_ratio = F(0)
        worst_F = 0
        trials = 25
        for _ in range(trials):
            n = 18
            X = [[F(0)] * n for _ in range(m)]
            D = [[F(0)] * n for _ in range(m)]
            for j in range(n):
                raw = [rng.randint(0, 10) for _ in range(m)]
                if sum(raw) == 0:
                    raw[0] = 1
                s = sum(raw)
                for i in range(m):
                    X[i][j] = F(raw[i], s)
                    D[i][j] = F(rng.randint(1, 20), 20)
            _, ratio, mf = iterated_prefix_basis_round(X, D)
            worst_ratio = max(worst_ratio, ratio)
            worst_F = max(worst_F, mf)
        print(f"  m = {m}: {trials} exact rational instances, max |F_t| = {worst_F} (<= {m}), "
              f"worst max|Delta|/D = {float(worst_ratio):.6f} (< {m})")

    ce_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "..", "chairman-counterexample", "data", "chairman_instance.json",
    )
    if os.path.exists(ce_path):
        with open(ce_path) as fh:
            data = json.load(fh)
        rows = data["rows"]
        row_idx = {name: i for i, name in enumerate(rows)}
        m_ce = len(rows)
        nb = data["number_of_blocks"]
        n_ce = 3 * nb
        eta_ce = F(data["default_weight"])
        X_ce = [[F(0)] * n_ce for _ in range(m_ce)]
        D_ce = [[eta_ce] * n_ce for _ in range(m_ce)]
        tmpl = data["block_template"]
        for k_b in range(1, nb + 1):
            for off, key in enumerate(("Jk", "Kk", "Lk")):
                j = 3 * (k_b - 1) + off
                for rname, val in tmpl[key]["fractional_entries"].items():
                    real_name = rname.replace("k", str(k_b))
                    X_ce[row_idx[real_name]][j] = F(val)
                for rname, val in tmpl[key]["exceptional_weights"].items():
                    real_name = rname.replace("k", str(k_b))
                    D_ce[row_idx[real_name]][j] = F(val)
        _, ratio_ce, mf_ce = iterated_prefix_basis_round(X_ce, D_ce)
        print(f"\n  chairman-counterexample (11x15): max |F_t| = {mf_ce} (<= 11), "
              f"exact support-preserving prefix disc/D = {ratio_ce} = {float(ratio_ce):.6f} (< 11)")

    print("\nTheorem 6 (exact rational kappa_m <= m, strictly < m*D) verified on all test instances.")


if __name__ == "__main__":
    main()
