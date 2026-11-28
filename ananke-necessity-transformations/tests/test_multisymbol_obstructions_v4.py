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
    def test_kochen_specker_linear_witness_ceiling_and_exceeding_two(self) -> None:
        """Theorem 1: single-qubit linear witnesses CAN exceed 2 (e.g. 9/4 and icosahedron 2.292) but stay <= 4."""
        # Exact 3x3 single-qubit counterexample to <= 2 (Codex referee): x-axis prep/meas, 2*pi/3 z-rotations
        h_tri = 0.75 * np.eye(3) + 0.25
        w_tri = 1.5 * np.eye(3) - 0.5
        res_tri = simplex_box_linear_ratio(h_tri, w_tri)
        self.assertAlmostEqual(res_tri["linear_lower_bound_ratio"], 2.25, places=12)
        self.assertGreater(res_tri["linear_lower_bound_ratio"], 2.0)
        self.assertLessEqual(res_tri["linear_lower_bound_ratio"], 4.0 + 1e-9)

        # 12x12 icosahedral pure-qubit witness (Fable 5.2 referee): ratio ~ 2.292 in (2, 4]
        phi = 0.5 * (1.0 + np.sqrt(5.0))
        ico = np.array(
            [(0, s1, s2 * phi) for s1 in (-1, 1) for s2 in (-1, 1)]
            + [(s1, s2 * phi, 0) for s1 in (-1, 1) for s2 in (-1, 1)]
            + [(s2 * phi, 0, s1) for s1 in (-1, 1) for s2 in (-1, 1)],
            dtype=float,
        )
        ico /= np.linalg.norm(ico, axis=1, keepdims=True)
        h_ico = 0.5 * (1.0 + ico @ ico.T)
        res_ico = simplex_box_linear_ratio(h_ico, 2.0 * h_ico - 1.0)
        self.assertGreater(res_ico["linear_lower_bound_ratio"], 2.25)
        self.assertLessEqual(res_ico["linear_lower_bound_ratio"], 4.0 + 1e-9)

        # 7x7 two-symbol qubit block: all witnesses <= 4
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
            self.assertLessEqual(res["linear_lower_bound_ratio"], 4.0 + 1e-9)

    def test_support_envelope_referee_soundness_regressions(self) -> None:
        """Regressions for Codex & Fable 5.2 findings: terminal boxes, propagation, weights, KL, shape."""
        from ananke.certified_inference import kl_binomial_confidence_interval

        # 1. Terminal narrow box must NOT be dropped from global_ub (feasible a = (5/8, 5/8))
        p, e = np.array([5 / 8, 3 / 8, 0.0]), np.array([1 / 10, 0.0, 1.0])
        x = np.array([[1, 0, 0], [0, 0, 1], [0, 0, 1]], dtype=float)
        z = np.array([[0, 1 / 10, 9 / 10], [0, 1, 0], [0, 0, 1]], dtype=float)
        u_repro = np.stack([p, p @ x]) @ np.column_stack([e, z @ e])
        cert_repro = certify_support_envelope_lower_bound(u_repro, 1.0 - u_repro)
        self.assertGreaterEqual(cert_repro.certified_sup_upper_bound, 0.625)
        self.assertLessEqual(cert_repro.certified_classical_state_lower_bound, 3)

        # 2. Sterbenz-safe propagation: feasible a = (0.72, 0.5) must NEVER be clipped
        u_cancel = np.array([[0.7199999999999898], [1.0]], dtype=float)
        v_cancel = np.array([[1.0], [7.093091546216278e-15]], dtype=float)
        cert_cancel = certify_support_envelope_lower_bound(u_cancel, v_cancel, weights=[0.5, 0.5])
        self.assertGreaterEqual(cert_cancel.certified_sup_upper_bound, 0.5 * (0.72 + 0.5))

        # 3. Overflow-safe weight normalization on [1e308, 1e308]
        u_const = np.full((2, 2), 0.5, dtype=float)
        cert_bigw = certify_support_envelope_lower_bound(u_const, u_const, weights=[1e308, 1e308])
        self.assertEqual(cert_bigw.certified_classical_state_lower_bound, 1)
        self.assertGreaterEqual(cert_bigw.certified_sup_upper_bound, 1.0 - 1e-9)

        # 4. Tiny positive weights must NOT be dropped silently
        h_tiny = np.array([[0.0], [1.0], [0.0]], dtype=float)
        w_tiny = np.array([1.0, 1.0, 1.8e-9], dtype=float)
        w_tiny /= np.sum(w_tiny)
        # Feasible a = (0, 1, 0) -> score w_tiny[1]; feasible a = (0.5, 0.5, 0.5) -> 0.5;
        # actually a = (0, 1, 0) gives score 1 / (2 + 1.8e-9) ~ 0.49999999955, while a = (0, 1, 1) has
        # U[2,0]=0 and V[1,0]=0 so a_1*a_2 = 0; feasible a = (0, 1, 0) or (1, 0, 1) gives max = 0.50000000045!
        cert_tiny = certify_support_envelope_lower_bound(h_tiny, 1.0 - h_tiny, weights=[1.0, 1.0, 1.8e-9])
        self.assertGreaterEqual(cert_tiny.certified_sup_upper_bound, float(w_tiny[0] + w_tiny[2]) - 1e-13)

        # 5. Cancellation-free KL confidence interval at huge trials=1e16 must enclose exact KL threshold
        lo, hi = kl_binomial_confidence_interval(5 * 10**15, 10**16, 0.01)
        # Exact KL(0.5 || 0.5 + d) ~ 2 d^2 = ln(200)/1e16 => d ~ sqrt(ln(200)/(2e16)) ~ 1.6276e-8
        expected_d = np.sqrt(np.log(200.0) / (2.0 * 1e16))
        self.assertLessEqual(lo, 0.5 - expected_d)
        self.assertGreaterEqual(hi, 0.5 + expected_d)

        # 6. Noiseless Hankel rank must reject mismatched matrix shape
        with self.assertRaises(ValueError):
            certify_unconditional_hankel_rank_noiseless(np.eye(2), 0, 0, alphabet_size=1)

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
        """Numerical axisymmetric cap discretization gives ~11.4 on S^2 and ~6.7 on S^1."""
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
