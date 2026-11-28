"""Unit tests for ANANKE v3 rank-unrestricted B-spline Cayley--Hamilton certifiers."""

from __future__ import annotations

from decimal import Context, Decimal
from math import pi
import unittest

import numpy as np

from ananke import (
    Interval,
    bspline_conjugate_leakage,
    bspline_window,
    certify_bspline_multiplier,
    certify_noiseless_counterfeit_error_lower_bound,
    certify_rank_unrestricted_fourier_cap,
    certify_rank_unrestricted_split_sample,
    classical_cycle_process,
    construct_karpelevich_boundary_matrix,
    exp_interval,
    ln2_interval,
    log_interval,
    qubit_rotation_process,
    ray_words,
    simulate_shot_dataset,
)


class RankUnrestrictedV3Tests(unittest.TestCase):
    def test_log_and_exp_intervals_contain_high_precision_reference(self) -> None:
        ctx = Context(prec=50)
        ln2 = ln2_interval(28)
        self.assertLessEqual(ln2.lo, ctx.ln(Decimal(2)))
        self.assertLessEqual(ctx.ln(Decimal(2)), ln2.hi)
        self.assertLess(float(ln2.width()), 1e-24)

        for s in ("0.001", "0.25", "1", "1.37", "2.718281828", "1000"):
            d = Decimal(s)
            iv = log_interval(Interval(d, d), 24)
            ref = ctx.ln(d)
            self.assertLessEqual(iv.lo, ref)
            self.assertLessEqual(ref, iv.hi)

        for s in ("-15", "-1.2", "0", "0.4", "3.5", "25"):
            d = Decimal(s)
            iv = exp_interval(Interval(d, d), 24)
            ref = ctx.exp(d)
            self.assertLessEqual(iv.lo, ref)
            self.assertLessEqual(ref, iv.hi)

        # Wide interval monotonicity check
        wide = Interval(Decimal("0.5"), Decimal("4.0"))
        lw = log_interval(wide, 20)
        self.assertLessEqual(lw.lo, ctx.ln(Decimal("0.5")))
        self.assertGreaterEqual(lw.hi, ctx.ln(Decimal("4.0")))

    def test_bspline_exact_finite_difference_norm_and_cayley_hamilton_identity(self) -> None:
        # Verify Theorem 1 algebra directly on random high-rank stochastic matrices
        rng = np.random.default_rng(123)
        theta = 2.40
        z = np.exp(1j * theta)
        for n, m in ((3, 4), (5, 5), (6, 4)):
            w = bspline_window(n, m)
            self.assertAlmostEqual(float(np.sum(w)), 1.0, places=12)
            # Check exact ||nabla^k w||_1 <= (2/M)^k for all k = 1..N
            diff_w = w.copy()
            for k in range(1, n + 1):
                diff_w = np.diff(np.concatenate([[0.0], diff_w, [0.0]]))
                self.assertLessEqual(float(np.sum(np.abs(diff_w))), (2.0 / m) ** k + 1e-12)

            # Check Theorem 1(a) on random stochastic matrix A of size N (full rank!)
            mat = rng.dirichlet(np.ones(n), size=n)
            p = rng.dirichlet(np.ones(n))
            e = rng.uniform(0.0, 1.0, size=n)
            eigs = np.linalg.eigvals(mat)
            psi_exact = float(np.prod(1.0 + 2.0 / (m * np.abs(z - eigs))))
            # Evaluate g(k) = p A^k e
            k_len = w.size
            g = np.empty(k_len, dtype=float)
            v = p.copy()
            for k in range(k_len):
                g[k] = float(v @ e)
                v = v @ mat
            ks = np.arange(k_len, dtype=float)
            fourier_g = abs(complex(np.sum(w * np.exp(-1j * ks * theta) * (g - 0.5))))
            self.assertLessEqual(fourier_g, 0.5 * (psi_exact - 1.0) + 1e-11)

            # Check certified Psi_N dominates psi_exact
            cert = certify_bspline_multiplier(n, m, theta)
            self.assertTrue(cert.certified)
            self.assertGreaterEqual(cert.psi_upper_bound + 1e-12, psi_exact)

    def test_certified_multiplier_dominates_ito_boundary_and_random_matrices(self) -> None:
        theta = 2.40
        z = np.exp(1j * theta)
        for n, m in ((2, 4), (3, 3), (4, 3), (5, 5), (6, 6)):
            cert = certify_bspline_multiplier(n, m, theta)
            self.assertTrue(cert.certified)
            mat_ito = construct_karpelevich_boundary_matrix(n, theta)
            eigs_ito = np.linalg.eigvals(mat_ito)
            psi_ito = float(np.prod(1.0 + 2.0 / (m * np.abs(z - eigs_ito))))
            self.assertGreaterEqual(cert.psi_upper_bound + 1e-10, psi_ito)

    def test_noiseless_rank_unrestricted_excludes_beyond_rank_4_on_qubit(self) -> None:
        # Pure golden-angle qubit: rank 4, yet N=4, 5, 6 are ALL excluded without rank cap!
        proc = qubit_rotation_process(
            theta_x=2.40,
            theta_z=1.11,
            initial_bloch=np.array([0.0, 0.0, 1.0]),
            measurement_axis=np.array([0.0, 0.0, 1.0]),
        )
        vals = [proc.behavior("x" * k) for k in range(61)]
        for n, m in ((3, 4), (4, 4), (5, 6), (6, 8)):
            res = certify_noiseless_counterfeit_error_lower_bound(vals, n, 2.40, boxcar_length=m)
            self.assertTrue(res.multiplier.certified)
            self.assertGreater(res.best_error_lower_bound, 0.005)

    def test_finite_shot_mode_a_and_mode_b_certify_qubit_beyond_rank_4(self) -> None:
        rng = np.random.default_rng(2026)
        theta = 2.40
        proc = qubit_rotation_process(
            theta_x=theta,
            theta_z=1.11,
            initial_bloch=np.array([0.0, 0.0, 1.0]),
            measurement_axis=np.array([0.0, 0.0, 1.0]),
        )
        # Mode A (ultra-shot-efficient): 400 unary words, only 200 shots/word = 80k total shots!
        words_a = ray_words("x", 400)
        ds_a = simulate_shot_dataset(proc, words_a, 200, rng)
        rep_a = certify_rank_unrestricted_fourier_cap(
            ds_a,
            symbol="x",
            max_ray_power=400,
            theta_radians=theta,
            maximum_order=6,
            alpha=0.01,
        )
        # Must unconditionally certify N >= 5 (strictly beyond rank 4, with ZERO rank cap!)
        self.assertGreaterEqual(rep_a.certified_classical_state_lower_bound, 5)

        # Mode B (short circuit depth L = 60, 50k shots/word): certifies N >= 7 with ZERO rank cap!
        words_b = ray_words("x", 60)
        ds_b = simulate_shot_dataset(proc, words_b, 50_000, rng)
        rep_b = certify_rank_unrestricted_split_sample(
            ds_b,
            symbol="x",
            max_ray_power=60,
            theta_radians=theta,
            maximum_order=8,
            alpha=0.01,
            rng=np.random.default_rng(7),
        )
        self.assertGreaterEqual(rep_b.certified_classical_state_lower_bound, 6)

    def test_classical_three_cycle_is_never_falsely_excluded_at_order_3(self) -> None:
        # Exact 3-state classical cycle at its own frequency 2*pi/3 MUST NOT be excluded at N=3!
        cycle = classical_cycle_process(period=3, damping=0.0, symbol="a")
        theta_3 = 2.0 * pi / 3.0
        words = ray_words("a", 60)
        rng = np.random.default_rng(99)
        ds = simulate_shot_dataset(cycle, words, 10_000, rng)
        rep_a = certify_rank_unrestricted_fourier_cap(
            ds,
            symbol="a",
            max_ray_power=60,
            theta_radians=theta_3,
            orders=(2, 3),
            alpha=0.01,
            early_stop=False,
        )
        # N=2 (Theta_2 = [-1, 1]) IS excluded, N=3 MUST NOT be excluded!
        by_order = {c.order: c for c in rep_a.tested_orders}
        self.assertTrue(by_order[2].excluded_exact)
        self.assertFalse(by_order[3].excluded_exact)
        self.assertEqual(rep_a.certified_classical_state_lower_bound, 3)

        # Also test off-frequency (theta = 2.40) on a 3-cycle: signal at 2.40 is 0, so NOTHING is excluded!
        rep_off = certify_rank_unrestricted_split_sample(
            ds,
            symbol="a",
            max_ray_power=60,
            theta_radians=2.40,
            orders=(2, 3),
            alpha=0.01,
            rng=np.random.default_rng(11),
            early_stop=False,
        )
        for check in rep_off.tested_orders:
            self.assertFalse(check.excluded_exact)


if __name__ == "__main__":
    unittest.main()
