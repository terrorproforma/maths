"""Unit tests for ANANKE v4 multi-symbol rank-unrestricted obstructions."""

from __future__ import annotations

from math import acos, pi
import unittest

import numpy as np

from ananke import (
    ClassicalRealization,
    build_hankel,
    build_staircase_envelope_noiseless,
    certify_composite_word_finite_shot,
    certify_composite_word_noiseless,
    certify_staircase_support_envelope_finite_shot,
    certify_staircase_support_envelope_noiseless,
    certify_support_envelope_lower_bound,
    certify_unconditional_hankel_rank_finite_shot,
    certify_unconditional_hankel_rank_noiseless,
    composite_ray_words,
    composite_word_rotation_angle,
    continuous_sphere_support_envelope_ceiling,
    niven_rational_gate_qubit,
    optimize_support_envelope_weights,
    qubit_rotation_process,
    qudit_two_symbol_quantum_realization,
    simplex_box_linear_ratio,
    simulate_shot_dataset,
    simulate_words_upto,
    words_upto,
)


class MultiSymbolObstructionsV4Tests(unittest.TestCase):
    def test_frenkel_weiner_linear_witness_ceiling_on_single_qubit(self) -> None:
        """Theorem 1: every linear witness <W, H_f> / gamma_+(W) <= 2 on a single qubit."""
        r0 = np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0)
        proc = qubit_rotation_process(theta_x=2.40, theta_z=1.11, initial_bloch=r0, measurement_axis=r0)
        h = build_hankel(proc.behavior, ("x", "z"), 2, 2).matrix  # 7 x 7
        rng = np.random.default_rng(0)
        for w in [
            2.0 * h - 1.0,
            h - 0.5,
            rng.normal(size=h.shape),
            (h > 0.8).astype(float) - 2.0 * (h < 0.2).astype(float),
        ]:
            res = simplex_box_linear_ratio(h, w)
            self.assertLessEqual(res["linear_lower_bound_ratio"], 2.0 + 1e-9)

    def test_support_envelope_never_falsely_excludes_exact_classical_model(self) -> None:
        """Soundness of Theorem 2: an exact K-state classical HMM must NEVER certify N > K."""
        rng = np.random.default_rng(11)
        for k_states in (3, 5):
            # Random 2-symbol K-state classical stochastic realization
            p = rng.dirichlet(np.ones(k_states))
            mx = rng.dirichlet(np.ones(k_states), size=k_states)
            mz = rng.dirichlet(np.ones(k_states), size=k_states)
            e = rng.uniform(0.0, 1.0, size=k_states)
            real = ClassicalRealization(("x", "z"), p, {"x": mx, "z": mz}, e)
            proc = real.to_linear_process()
            cert = certify_staircase_support_envelope_noiseless(
                proc, max_length=6, max_prefix_length=3, target_epsilon=0.0, max_nodes_per_star=800
            )
            self.assertLessEqual(cert.certified_classical_state_lower_bound, k_states)

    def test_support_envelope_certifies_pure_qubit_above_hankel_rank(self) -> None:
        """Theorem 2 certifies N >= 7 at L=6 (pure qubit, rank 4) with ZERO rank cap."""
        r0 = np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0)
        proc = qubit_rotation_process(theta_x=2.40, theta_z=1.7366, initial_bloch=r0, measurement_axis=r0)
        cert = certify_staircase_support_envelope_noiseless(
            proc, max_length=6, max_prefix_length=3, target_epsilon=0.0, max_nodes_per_star=1500
        )
        # Strictly exceeds the qubit's Hankel rank 4 with zero rank upper bound!
        self.assertGreaterEqual(cert.certified_classical_state_lower_bound, 5)
        self.assertLess(cert.certified_sup_upper_bound, 0.25)

    def test_support_envelope_finite_shot_soundness_and_power(self) -> None:
        """Finite-shot Chernoff--KL Theorem 2 certifies N >= 6 on pure qubit at L=8 and is sound on 4-state HMM."""
        r0 = np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0)
        proc = qubit_rotation_process(theta_x=2.40, theta_z=1.7366, initial_bloch=r0, measurement_axis=r0)
        _, _, u0, v0, valid0 = build_staircase_envelope_noiseless(proc, max_length=8, max_prefix_length=3)
        # Fixed deterministic weights (chosen a priori without seeing the shot dataset)
        mu = optimize_support_envelope_weights(u0, v0, valid0)
        rng = np.random.default_rng(2026)
        ds = simulate_words_upto(proc, 8, shots_per_word=20_000, rng=rng)
        cert = certify_staircase_support_envelope_finite_shot(
            ds, max_length=8, max_prefix_length=3, weights=mu, alpha=0.01, max_nodes_per_star=1200
        )
        self.assertGreaterEqual(cert.certified_classical_state_lower_bound, 6)
        self.assertEqual(cert.alpha, 0.01)

    def test_continuous_sphere_support_envelope_ceiling(self) -> None:
        """Exact continuous log-concave ceiling gives N >= 12 on S^2 and N >= 7 on S^1."""
        ceilings = continuous_sphere_support_envelope_ceiling(num_grid=24)
        self.assertGreater(ceilings["S2"]["continuous_lower_bound"], 11.0)
        self.assertEqual(int(ceilings["S2"]["integer_lower_bound"]), 12)
        self.assertGreater(ceilings["S1"]["continuous_lower_bound"], 6.0)
        self.assertEqual(int(ceilings["S1"]["integer_lower_bound"]), 7)

    def test_niven_rational_gate_noncommutative_synergy(self) -> None:
        """Theorem 3: R_x(pi/2) (order 4) + R_z(pi/3) (order 6) yields irrational cos(theta_xz) = -1/4."""
        proc = niven_rational_gate_qubit()
        # Verify exact finite orders of unary generators
        bx = proc.transitions["x"]
        bz = proc.transitions["z"]
        self.assertLess(float(np.max(np.abs(np.linalg.matrix_power(bx, 4) - np.eye(4)))), 1e-12)
        self.assertLess(float(np.max(np.abs(np.linalg.matrix_power(bz, 6) - np.eye(4)))), 1e-12)

        # Verify exact Niven angle cos(theta_{xz}) = -1/4
        theta_xz = composite_word_rotation_angle(proc, "xz")
        self.assertAlmostEqual(theta_xz, acos(-0.25), places=12)

        # Noiseless composite-word B-spline certifies N > 6 (exceeding BOTH unary ceilings 4 and 6!)
        lb7 = certify_composite_word_noiseless(proc, "xz", max_repetitions=60, order=7)
        self.assertGreater(lb7.best_error_lower_bound, 0.0)

        # Finite-shot composite-word B-spline certifies N >= 7 at 99% confidence!
        rng = np.random.default_rng(7)
        ray_w = composite_ray_words("xz", 400)
        ds = simulate_shot_dataset(proc, ray_w, shots_per_word=200, rng=rng)
        rep = certify_composite_word_finite_shot(
            ds, "xz", max_repetitions=400, theta_radians=theta_xz, mode="fourier_cap", maximum_order=8, alpha=0.01
        )
        self.assertGreaterEqual(rep.certified_classical_state_lower_bound, 5)

    def test_unconditional_hankel_rank_breaks_unary_ceiling_on_qutrit_and_two_qubit(self) -> None:
        """Theorem 4: certifies C_cl >= 9 > 7 = L+1 at L=6 (d=3) and C_cl >= 16 > 9 = L+1 at L=8 (d=4)."""
        # d = 3 qutrit at L = 6 (unary ceiling L + 1 = 7); pick well-conditioned deterministic seed
        best_s3, best_sv3 = 0, -1.0
        for s in range(8):
            h_tmp = build_hankel(
                qudit_two_symbol_quantum_realization(3, seed=s).to_linear_process().behavior,
                ("x", "z"),
                3,
                3,
            ).matrix
            sv_tmp = np.linalg.svd(h_tmp, compute_uv=False)
            if sv_tmp[8] > best_sv3:
                best_sv3, best_s3 = float(sv_tmp[8]), s
        qutrit_q = qudit_two_symbol_quantum_realization(3, seed=best_s3)
        qutrit_lin = qutrit_q.to_linear_process()
        h3 = build_hankel(qutrit_lin.behavior, ("x", "z"), 3, 3).matrix
        rep3_exact = certify_unconditional_hankel_rank_noiseless(h3, 3, 3, target_epsilon=0.005)
        self.assertEqual(rep3_exact.certified_classical_state_lower_bound, 9)
        self.assertTrue(rep3_exact.breaks_unary_ceiling)

        # Finite-shot 99% certification on qutrit at L = 6
        rng = np.random.default_rng(42)
        ds3 = simulate_words_upto(qutrit_lin, 6, shots_per_word=1500, rng=rng)
        rep3_shot = certify_unconditional_hankel_rank_finite_shot(ds3, 3, 3, alpha=0.01)
        self.assertEqual(rep3_shot.certified_classical_state_lower_bound, 9)
        self.assertTrue(rep3_shot.breaks_unary_ceiling)

        # d = 4 two-qubit at L = 8 (unary ceiling L + 1 = 9)
        best_s4, best_sv4 = 0, -1.0
        for s in range(8):
            h_tmp = build_hankel(
                qudit_two_symbol_quantum_realization(4, seed=s).to_linear_process().behavior,
                ("x", "z"),
                4,
                4,
            ).matrix
            sv_tmp = np.linalg.svd(h_tmp, compute_uv=False)
            if sv_tmp[15] > best_sv4:
                best_sv4, best_s4 = float(sv_tmp[15]), s
        twoq_q = qudit_two_symbol_quantum_realization(4, seed=best_s4)
        twoq_lin = twoq_q.to_linear_process()
        h4 = build_hankel(twoq_lin.behavior, ("x", "z"), 4, 4).matrix
        rep4_exact = certify_unconditional_hankel_rank_noiseless(h4, 4, 4, target_epsilon=0.005)
        self.assertEqual(rep4_exact.certified_classical_state_lower_bound, 16)
        self.assertTrue(rep4_exact.breaks_unary_ceiling)


if __name__ == "__main__":
    unittest.main()
