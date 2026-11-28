"""Unit tests for ANANKE v3 explicit classical counterfeit constructions."""

from __future__ import annotations

import unittest

import numpy as np

from ananke import (
    build_hankel,
    certify_noiseless_counterfeit_error_lower_bound,
    construct_bloch_polytope_counterfeit,
    construct_karpelevich_boundary_matrix,
    construct_karpelevich_unary_counterfeit,
    construct_shift_register_counterfeit,
    fit_static_simplex_box_nmf,
    karpelevich_boundary_radius,
    optimize_unary_classical_counterfeit,
    qubit_rotation_process,
    words_upto,
)


class ApproximateRealizationV3Tests(unittest.TestCase):
    def test_shift_register_matches_unary_qubit_with_zero_error_on_length_7(self) -> None:
        # Explicitly demonstrates why ANANKE v2's L=7 unary block cannot rule out N=8 without rank cap!
        proc = qubit_rotation_process(theta_x=0.73, theta_z=1.11)
        vals = [proc.behavior("x" * k) for k in range(8)]
        sr = construct_shift_register_counterfeit(vals, symbol="x")
        self.assertEqual(sr.state_count, 8)
        preds = sr.evaluate_unary_ray("x", 7)
        self.assertLess(float(np.max(np.abs(preds - np.array(vals)))), 1e-14)
        # Its eigenvalues are {1, 0, ..., 0} (far from e^{0.73i}), yet H_g == H_f on 4x4 unary block!
        eigs = np.linalg.eigvals(sr.transitions["x"])
        self.assertGreater(float(np.min(np.abs(eigs - np.exp(0.73j)))), 0.7)

    def test_ito_karpelevich_boundary_matrix_attains_exact_boundary_eigenvalue(self) -> None:
        for theta in (0.73, 1.7366, 2.40):
            for n in (3, 4, 5, 6, 7, 8, 9, 10, 12):
                mat = construct_karpelevich_boundary_matrix(n, theta)
                self.assertEqual(mat.shape, (n, n))
                self.assertGreaterEqual(float(mat.min()), -1e-12)
                self.assertLess(float(np.max(np.abs(mat.sum(axis=1) - 1.0))), 1e-12)
                rho = karpelevich_boundary_radius(n, theta)
                target = rho * np.exp(1j * theta)
                eigs = np.linalg.eigvals(mat)
                self.assertLess(float(np.min(np.abs(eigs - target))), 1e-7)

    def test_certified_lower_bound_never_exceeds_constructive_upper_bound(self) -> None:
        proc = qubit_rotation_process(
            theta_x=2.40,
            theta_z=1.11,
            initial_bloch=np.array([0.0, 0.0, 1.0]),
            measurement_axis=np.array([0.0, 0.0, 1.0]),
        )
        for n, m in ((3, 4), (4, 4), (5, 5)):
            l_max = n * m
            vals = [proc.behavior("x" * k) for k in range(l_max + 1)]
            lb = certify_noiseless_counterfeit_error_lower_bound(vals, n, 2.40, boxcar_length=m)
            ub_ito = construct_karpelevich_unary_counterfeit(vals, n, 2.40)
            ub_opt = optimize_unary_classical_counterfeit(
                vals, n, theta_radians=2.40, restarts=3, maxiter=120, seed=n
            )
            self.assertLessEqual(lb.best_error_lower_bound, ub_ito.max_error + 1e-9)
            self.assertLessEqual(lb.best_error_lower_bound, ub_opt.max_error + 1e-9)
            self.assertLessEqual(ub_opt.max_error, ub_ito.max_error + 1e-9)

    def test_bloch_polytope_two_symbol_counterfeit_converges_with_state_count(self) -> None:
        proc = qubit_rotation_process(theta_x=0.73, theta_z=1.11)
        words = words_upto(("x", "z"), 5)
        r6 = construct_bloch_polytope_counterfeit(proc, 6, words)
        r20 = construct_bloch_polytope_counterfeit(proc, 20, words)
        r64 = construct_bloch_polytope_counterfeit(proc, 64, words)
        self.assertGreater(r64.inradius_rho, r20.inradius_rho)
        self.assertGreater(r20.inradius_rho, r6.inradius_rho)
        self.assertLess(r64.max_error, r20.max_error)
        self.assertLess(r20.max_error, r6.max_error)

    def test_static_simplex_box_nmf_decreases_rapidly_on_mixed_qubit_hankel(self) -> None:
        proc = qubit_rotation_process(theta_x=0.73, theta_z=1.11)
        h = build_hankel(proc.behavior, ("x", "z"), 3, 3).matrix
        e4, _ = fit_static_simplex_box_nmf(h, 4, restarts=4, iterations=120, seed=1)
        e8, _ = fit_static_simplex_box_nmf(h, 8, restarts=4, iterations=120, seed=2)
        self.assertLess(e8, e4)
        self.assertLess(e8, 0.02)


if __name__ == "__main__":
    unittest.main()
