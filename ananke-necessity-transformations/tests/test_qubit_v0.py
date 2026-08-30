from __future__ import annotations

import unittest
from fractions import Fraction

import numpy as np

from ananke import (
    build_hankel,
    extract_minimal_process,
    finite_classical_channel_obstruction_from_rational_angles,
    qubit_rotation_process,
    words_upto,
)


class AnankeQubitV0Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.process = qubit_rotation_process()

    def test_gauge_transformation_preserves_all_checked_behaviour(self) -> None:
        coordinate_map = np.array(
            [
                [1.2, 0.1, -0.2, 0.3],
                [0.4, 1.1, 0.2, -0.1],
                [-0.3, 0.2, 1.4, 0.2],
                [0.1, -0.2, 0.3, 0.9],
            ],
            dtype=float,
        )
        transformed = self.process.gauge_transform(coordinate_map)
        maximum_error = max(
            abs(self.process.behavior(word) - transformed.behavior(word))
            for word in words_upto(self.process.alphabet, 7)
        )
        self.assertLess(maximum_error, 1e-12)

    def test_unreachable_hidden_dynamics_are_operationally_erased(self) -> None:
        hidden = {
            "x": np.array(
                [[0.2, 0.1, 0.0], [0.0, -0.3, 0.4], [0.1, 0.0, 0.5]],
                dtype=float,
            ),
            "z": np.array(
                [[-0.1, 0.0, 0.2], [0.3, 0.4, 0.0], [0.0, -0.2, 0.1]],
                dtype=float,
            ),
        }
        padded = self.process.pad_with_unreachable_hidden_dynamics(hidden)
        self.assertEqual(padded.dimension, 7)

        maximum_error = max(
            abs(self.process.behavior(word) - padded.behavior(word))
            for word in words_upto(self.process.alphabet, 7)
        )
        self.assertLess(maximum_error, 1e-12)

        hankel = build_hankel(
            padded.behavior,
            padded.alphabet,
            max_prefix_length=2,
            max_suffix_length=2,
        )
        extraction = extract_minimal_process(hankel)
        self.assertEqual(extraction.retained_rank, 4)

    def test_hankel_extraction_predicts_unseen_longer_words(self) -> None:
        hankel = build_hankel(
            self.process.behavior,
            self.process.alphabet,
            max_prefix_length=2,
            max_suffix_length=2,
        )
        extraction = extract_minimal_process(hankel)
        self.assertEqual(extraction.retained_rank, 4)

        maximum_error = max(
            abs(
                self.process.behavior(word)
                - extraction.process.behavior(word)
            )
            for word in words_upto(self.process.alphabet, 9)
        )
        self.assertLess(maximum_error, 1e-10)

    def test_rational_radian_phases_obstruct_finite_classical_channels(self) -> None:
        hankel = build_hankel(
            self.process.behavior,
            self.process.alphabet,
            max_prefix_length=2,
            max_suffix_length=2,
        )
        extraction = extract_minimal_process(hankel)
        report = finite_classical_channel_obstruction_from_rational_angles(
            extraction.process,
            {
                "x": Fraction(73, 100),
                "z": Fraction(111, 100),
            },
        )
        self.assertTrue(report["finite_classical_realization_obstructed"])
        self.assertTrue(
            report["symbol_certificates"]["x"][
                "classical_finite_channel_obstructed"
            ]
        )
        self.assertTrue(
            report["symbol_certificates"]["z"][
                "classical_finite_channel_obstructed"
            ]
        )

    def test_extracted_transition_spectra_are_similarity_invariant(self) -> None:
        hankel = build_hankel(
            self.process.behavior,
            self.process.alphabet,
            max_prefix_length=2,
            max_suffix_length=2,
        )
        extraction = extract_minimal_process(hankel)

        for symbol in self.process.alphabet:
            expected = np.sort_complex(
                np.linalg.eigvals(self.process.transitions[symbol])
            )
            actual = np.sort_complex(
                np.linalg.eigvals(extraction.process.transitions[symbol])
            )
            np.testing.assert_allclose(actual, expected, atol=1e-10, rtol=1e-10)


if __name__ == "__main__":
    unittest.main()
