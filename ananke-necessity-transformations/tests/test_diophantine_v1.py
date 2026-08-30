from __future__ import annotations

import unittest
from math import pi, sqrt

from ananke import (
    approximation_record_sequence,
    continued_fraction,
    convergents,
    nearest_root_of_unity,
)


class DiophantineV1Tests(unittest.TestCase):
    def test_current_phase_has_near_fibonacci_prefix(self) -> None:
        coefficients = continued_fraction(0.73 / (2.0 * pi), 8)
        self.assertEqual(coefficients[:6], (0, 8, 1, 1, 1, 1))
        fractions = convergents(coefficients[:7])
        self.assertEqual(
            [fraction.denominator for fraction in fractions],
            [1, 8, 9, 17, 26, 43, 241],
        )

    def test_noble_target_is_extremely_close_to_current_angle(self) -> None:
        phi = (1.0 + sqrt(5.0)) / 2.0
        noble_turns = 1.0 / (8.0 + 1.0 / phi)
        self.assertLess(abs(0.73 - 2.0 * pi * noble_turns), 0.001)

    def test_noble_target_resists_order_241_root_better(self) -> None:
        phi = (1.0 + sqrt(5.0)) / 2.0
        current = 0.73 / (2.0 * pi)
        noble = 1.0 / (8.0 + 1.0 / phi)
        current_distance = nearest_root_of_unity(current, 241).root_of_unity_distance
        noble_distance = nearest_root_of_unity(noble, 241).root_of_unity_distance
        self.assertGreater(noble_distance, 20.0 * current_distance)

    def test_approximation_record_sequence_changes_only_when_fraction_changes(self) -> None:
        records = approximation_record_sequence(0.73 / (2.0 * pi), 50)
        identities = [
            (approximant.numerator, approximant.denominator)
            for _, approximant in records
        ]
        self.assertEqual(len(identities), len(set(identities)))
        self.assertIn((1, 8), identities)
        self.assertIn((1, 9), identities)
        self.assertIn((2, 17), identities)


if __name__ == "__main__":
    unittest.main()
