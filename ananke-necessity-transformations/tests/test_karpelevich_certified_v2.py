from __future__ import annotations

import unittest
from math import pi

import numpy as np

from ananke import (
    certified_distance_to_karpelevich,
    certified_karpelevich_radius,
    certify_finite_stochastic_exclusions,
    distance_to_karpelevich_region,
    karpelevich_boundary_radius,
)


class KarpelevichCertifiedV2Tests(unittest.TestCase):
    def test_kls_2020_theta5_theta6_certified(self) -> None:
        angle = 7.0 * pi / 12.0
        r5 = certified_karpelevich_radius(5, angle)
        r6 = certified_karpelevich_radius(6, angle)
        self.assertLess(r5.radius_hi, 0.9)
        self.assertGreater(r6.radius_lo, 0.9)
        self.assertAlmostEqual(r5.radius_lo, 0.8675221204970267, places=12)
        self.assertAlmostEqual(r6.radius_lo, 0.9114159452656427, places=12)

        z = 0.9 * np.exp(1j * angle)
        d5 = certified_distance_to_karpelevich(z, 5, tol=5e-4)
        d6 = certified_distance_to_karpelevich(z, 6, tol=5e-4)
        self.assertFalse(d5.certified_inside)
        self.assertGreater(d5.distance_lo, 0.02)
        self.assertTrue(d6.certified_inside)
        self.assertEqual(d6.distance_hi, 0.0)

    def test_orders_one_two_and_conjugation_symmetry(self) -> None:
        z = complex(0.4, 0.7)
        d1 = certified_distance_to_karpelevich(z, 1)
        self.assertAlmostEqual(d1.distance_lo, abs(z - 1.0), places=12)
        self.assertAlmostEqual(d1.distance_hi, abs(z - 1.0), places=12)

        d2 = certified_distance_to_karpelevich(z, 2)
        self.assertAlmostEqual(d2.distance_lo, 0.7, places=12)
        self.assertAlmostEqual(d2.distance_hi, 0.7, places=12)

        # Lower half-plane must match upper half-plane identically
        d5_pos = certified_distance_to_karpelevich(complex(0.6, 0.75), 5, tol=5e-4)
        d5_neg = certified_distance_to_karpelevich(complex(0.6, -0.75), 5, tol=5e-4)
        self.assertLessEqual(d5_pos.distance_lo, d5_neg.distance_hi)
        self.assertLessEqual(d5_neg.distance_lo, d5_pos.distance_hi)

    def test_certified_enclosure_brackets_v1_numerical_distance(self) -> None:
        z = complex(np.exp(0.73j))
        for order in (3, 5, 8, 9, 15):
            cert = certified_distance_to_karpelevich(z, order, tol=5e-4, max_subdivisions=600)
            num = distance_to_karpelevich_region(z, order, coarse_points=256).distance
            self.assertLessEqual(cert.distance_lo, num + 1e-7)
            self.assertGreaterEqual(cert.distance_hi, num - 1e-7)
            self.assertLessEqual(cert.distance_hi - cert.distance_lo, 1e-3)

    def test_classical_three_cycle_boundary_and_interior_not_excluded(self) -> None:
        exact_3 = complex(np.exp(2j * pi / 3.0))
        damped_3 = 0.88 * exact_3
        d_exact = certified_distance_to_karpelevich(exact_3, 3, target_radius=1e-4)
        d_damped = certified_distance_to_karpelevich(damped_3, 3, target_radius=1e-4)
        self.assertLessEqual(d_exact.distance_hi, 1e-4)
        self.assertTrue(d_damped.certified_inside)
        self.assertEqual(d_damped.distance_hi, 0.0)

    def test_v1_baseline_qubit_exclusion_is_genuinely_certified_n_ge_16(self) -> None:
        # Exact point estimate and 99% bootstrap disk radius from results/noisy_qubit_v1.json
        z_v1 = complex(0.7462648445835013, 0.667842916840135)
        r_v1 = 0.007926034862237889
        d15 = certified_distance_to_karpelevich(z_v1, 15, target_radius=r_v1, tol=1e-7)
        d16 = certified_distance_to_karpelevich(z_v1, 16, target_radius=r_v1, tol=1e-7)
        self.assertGreater(d15.distance_lo, r_v1)
        self.assertLessEqual(d16.distance_hi, r_v1)

        report = certify_finite_stochastic_exclusions(
            z_v1,
            r_v1,
            confidence_level=0.99,
            hankel_rank_lower_bound=4,
            maximum_order=18,
            early_stop=True,
        )
        self.assertEqual(report.certified_excluded_through, 15)
        self.assertEqual(report.certified_classical_state_lower_bound, 16)

    def test_certified_radius_matches_v1_across_orders(self) -> None:
        for order in (3, 4, 7, 11):
            for angle in (0.37, 1.11, 2.4, 4.9):
                enc = certified_karpelevich_radius(order, angle)
                ref = karpelevich_boundary_radius(order, angle)
                self.assertLessEqual(enc.radius_lo, ref + 1e-11)
                self.assertGreaterEqual(enc.radius_hi, ref - 1e-11)


if __name__ == "__main__":
    unittest.main()
