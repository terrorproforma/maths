from __future__ import annotations

import unittest

import numpy as np

from ananke import (
    bootstrap_hankel_singular_values,
    bootstrap_transition_eigenmode,
    build_empirical_hankel,
    qubit_rotation_process,
    select_hankel_rank,
    simulate_shot_dataset,
    words_upto,
)


class NoisyInferenceV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.process = qubit_rotation_process()
        cls.words = words_upto(cls.process.alphabet, 9)
        cls.validation_words = tuple(word for word in cls.words if len(word) >= 8)
        cls.dataset = simulate_shot_dataset(
            cls.process,
            cls.words,
            2_000,
            np.random.default_rng(123),
        )

    def test_empirical_hankel_reuses_word_estimates(self) -> None:
        hankel = build_empirical_hankel(
            self.dataset,
            max_prefix_length=3,
            max_suffix_length=3,
        )
        # H['x','z'] and H['','xz'] are the same operational word and must be
        # exactly identical, not two independent noisy cells.
        row_x = hankel.prefixes.index("x")
        column_z = hankel.suffixes.index("z")
        row_empty = hankel.prefixes.index("")
        column_xz = hankel.suffixes.index("xz")
        self.assertEqual(
            hankel.matrix[row_x, column_z],
            hankel.matrix[row_empty, column_xz],
        )

    def test_held_out_selector_recovers_rank_four(self) -> None:
        result = select_hankel_rank(
            self.dataset,
            max_prefix_length=3,
            max_suffix_length=3,
            validation_words=self.validation_words,
            candidate_ranks=range(1, 9),
        )
        self.assertEqual(result.selected_rank, 4)
        self.assertGreater(result.singular_values[3], result.singular_values[4] * 5.0)

    def test_bootstrap_invariant_contains_exact_mode(self) -> None:
        eigenmode = bootstrap_transition_eigenmode(
            self.dataset,
            max_prefix_length=3,
            max_suffix_length=3,
            retained_rank=4,
            symbol="x",
            repetitions=80,
            confidence_level=0.95,
            rng=np.random.default_rng(321),
            target=complex(np.exp(0.73j)),
        )
        exact = complex(np.exp(0.73j))
        self.assertLessEqual(
            abs(eigenmode.point_estimate - exact),
            1.5 * eigenmode.confidence_disk_radius,
        )
        self.assertGreater(eigenmode.successful_repetitions, 70)

    def test_singular_value_bootstrap_separates_signal_from_noise(self) -> None:
        result = bootstrap_hankel_singular_values(
            self.dataset,
            max_prefix_length=3,
            max_suffix_length=3,
            number_of_values=6,
            repetitions=50,
            confidence_level=0.95,
            rng=np.random.default_rng(456),
        )
        fourth_lower = result.intervals[3][0]
        fifth_upper = result.intervals[4][1]
        self.assertGreater(fourth_lower, fifth_upper * 4.0)


if __name__ == "__main__":
    unittest.main()
