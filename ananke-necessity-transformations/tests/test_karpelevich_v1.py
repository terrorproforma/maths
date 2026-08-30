from __future__ import annotations

import unittest
from math import pi

import numpy as np

from ananke import (
    bootstrap_transition_eigenmode,
    classical_cycle_process,
    exclude_finite_stochastic_orders,
    karpelevich_boundary_radius,
    karpelevich_contains,
    simulate_shot_dataset,
    words_upto,
)


class KarpelevichV1Tests(unittest.TestCase):
    def test_published_theta5_theta6_example(self) -> None:
        angle = 7.0 * pi / 12.0
        value = 0.9 * np.exp(1j * angle)
        self.assertAlmostEqual(
            karpelevich_boundary_radius(5, angle),
            0.8675221204970267,
            places=10,
        )
        self.assertAlmostEqual(
            karpelevich_boundary_radius(6, angle),
            0.9114159452656427,
            places=10,
        )
        self.assertFalse(karpelevich_contains(value, 5))
        self.assertTrue(karpelevich_contains(value, 6))

    def test_farey_roots_lie_on_the_unit_boundary(self) -> None:
        for order in range(2, 10):
            for denominator in range(1, order + 1):
                for numerator in range(denominator):
                    if np.gcd(numerator, denominator) != 1:
                        continue
                    angle = 2.0 * pi * numerator / denominator
                    self.assertAlmostEqual(
                        karpelevich_boundary_radius(order, angle),
                        1.0,
                        places=10,
                    )

    def test_exact_and_damped_three_cycles_are_in_theta3(self) -> None:
        exact = np.exp(2j * pi / 3.0)
        damped = 0.88 * exact
        self.assertTrue(karpelevich_contains(exact, 3))
        self.assertTrue(karpelevich_contains(damped, 3))

    def test_noisy_classical_cycle_is_not_falsely_excluded(self) -> None:
        process = classical_cycle_process(
            3,
            response_probabilities=np.array([0.17, 0.63, 0.89]),
        )
        words = words_upto(process.alphabet, 9)
        dataset = simulate_shot_dataset(
            process,
            words,
            20_000,
            np.random.default_rng(4),
        )
        target = complex(np.exp(2j * pi / 3.0))
        eigenmode = bootstrap_transition_eigenmode(
            dataset,
            max_prefix_length=2,
            max_suffix_length=2,
            retained_rank=3,
            symbol="a",
            repetitions=50,
            confidence_level=0.95,
            rng=np.random.default_rng(14),
            target=target,
        )
        report = exclude_finite_stochastic_orders(
            eigenmode.point_estimate,
            eigenmode.confidence_disk_radius,
            confidence_level=0.95,
            hankel_rank_lower_bound=3,
            maximum_order=3,
            coarse_points=64,
        )
        order_three = next(test for test in report.tests if test.order == 3)
        self.assertFalse(order_three.excluded_by_full_region_numerically)
        self.assertEqual(report.numerical_classical_state_lower_bound, 3)


if __name__ == "__main__":
    unittest.main()
