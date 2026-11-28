from __future__ import annotations

import unittest
from math import pi

import numpy as np

from ananke import (
    build_hankel,
    build_unbiased_empirical_hankel,
    certify_classical_memory_lower_bound,
    certify_eigenmode_single_sample,
    certify_eigenmode_split_sample,
    certify_hankel_rank,
    classical_cycle_process,
    entrywise_frobenius_hankel_bound,
    hankel_matrix_hoeffding_bound,
    kl_binomial_confidence_interval,
    qubit_rotation_process,
    simulate_words_upto,
    split_shot_dataset,
)


class CertifiedInferenceV2Tests(unittest.TestCase):
    def test_matrix_hoeffding_beats_entrywise_frobenius_and_holds_empirically(self) -> None:
        process = qubit_rotation_process()
        exact_h = build_hankel(process.behavior, process.alphabet, 3, 3)
        ds = simulate_words_upto(process, 7, 10_000, np.random.default_rng(12345))
        emp_h = build_unbiased_empirical_hankel(ds, 3, 3)

        mh_bound = hankel_matrix_hoeffding_bound(ds, 3, 3, delta=0.005)
        frob_bound = entrywise_frobenius_hankel_bound(ds, 3, 3, delta=0.005, method="kl")
        true_err = float(np.linalg.norm(emp_h.matrix - exact_h.matrix, 2))

        self.assertLess(true_err, mh_bound)
        self.assertLess(mh_bound, frob_bound / 3.0)

    def test_kl_confidence_interval_valid_and_tighter_than_hoeffding(self) -> None:
        lo, hi = kl_binomial_confidence_interval(50, 1000, delta=0.01)
        self.assertLess(lo, 0.05)
        self.assertGreater(hi, 0.05)
        # Compare width against Hoeffding
        hoef_rad = float(np.sqrt(np.log(2.0 / 0.01) / (2.0 * 1000)))
        self.assertLess(hi - lo, 2.0 * hoef_rad)

    def test_hypergeometric_split_preserves_counts_and_marginals(self) -> None:
        process = qubit_rotation_process()
        ds = simulate_words_upto(process, 4, 1_000, np.random.default_rng(7))
        ds1, ds2 = split_shot_dataset(ds, 0.2, np.random.default_rng(8))
        for w in ds.words:
            self.assertEqual(ds1.trials[w] + ds2.trials[w], ds.trials[w])
            self.assertEqual(ds1.successes[w] + ds2.successes[w], ds.successes[w])
            self.assertEqual(ds1.trials[w], 200)
            self.assertEqual(ds2.trials[w], 800)

    def test_unconditional_rank_certification_at_v1_shot_budget(self) -> None:
        process = qubit_rotation_process()
        ds = simulate_words_upto(process, 7, 10_000, np.random.default_rng(12345))
        rank_cert = certify_hankel_rank(ds, 3, 3, alpha=0.01)
        self.assertEqual(rank_cert.certified_rank_lower_bound, 4)
        self.assertLess(rank_cert.certified_tail_upper_bound, 0.15)

    def test_single_and_split_sample_eigenmode_certificates_contain_exact_mode(self) -> None:
        process = qubit_rotation_process()
        exact_mode = complex(np.exp(0.73j))
        ds = simulate_words_upto(process, 7, 300_000, np.random.default_rng(2026))

        single = certify_eigenmode_single_sample(
            ds,
            max_prefix_length=3,
            max_suffix_length=3,
            retained_rank=4,
            symbol="x",
            alpha=0.01,
            target=exact_mode,
        )
        split = certify_eigenmode_split_sample(
            ds,
            max_prefix_length=3,
            max_suffix_length=3,
            retained_rank=4,
            symbol="x",
            alpha=0.01,
            pilot_fraction=0.15,
            rng=np.random.default_rng(42),
            target=exact_mode,
        )
        self.assertTrue(single.certified_isolated)
        self.assertTrue(split.certified_isolated)
        self.assertEqual(single.certified_rank_lower_bound, 4)
        self.assertEqual(split.certified_rank_lower_bound, 4)

        # True mode MUST lie inside both certified disks
        self.assertLessEqual(abs(single.point_estimate - exact_mode), single.certified_disk_radius)
        self.assertLessEqual(abs(split.point_estimate - exact_mode), split.certified_disk_radius)
        # Split-sample scalar+projected certificate beats single-sample by a wide margin
        self.assertLess(split.certified_disk_radius, 0.35 * single.certified_disk_radius)
        # Both beat naive Bauer-Fike
        assert single.bauer_fike_comparison_radius is not None
        self.assertLess(single.certified_disk_radius, single.bauer_fike_comparison_radius)

    def test_end_to_end_certified_memory_bound_on_qubit_and_classical_cycle(self) -> None:
        # 1. Qubit at 300k shots/word should rigorously certify N >= 16!
        qubit = qubit_rotation_process()
        ds_q = simulate_words_upto(qubit, 7, 300_000, np.random.default_rng(12345))
        rep_q = certify_classical_memory_lower_bound(
            ds_q,
            max_prefix_length=3,
            max_suffix_length=3,
            retained_rank=4,
            symbol="x",
            alpha=0.01,
            method="split",
            pilot_fraction=0.15,
            rng=np.random.default_rng(999),
            target=complex(np.exp(0.73j)),
            maximum_order=20,
            early_stop=True,
        )
        self.assertGreaterEqual(rep_q.certified_classical_state_lower_bound, 16)

        # 2. Exact 3-state classical cycle MUST NOT be excluded from Theta_3!
        cycle = classical_cycle_process(
            3, response_probabilities=np.array([0.17, 0.63, 0.89])
        )
        ds_c = simulate_words_upto(cycle, 5, 50_000, np.random.default_rng(101))
        rep_c = certify_classical_memory_lower_bound(
            ds_c,
            max_prefix_length=2,
            max_suffix_length=2,
            retained_rank=3,
            symbol="a",
            alpha=0.01,
            method="split",
            pilot_fraction=0.2,
            rng=np.random.default_rng(102),
            target=complex(np.exp(2j * pi / 3.0)),
            maximum_order=4,
            early_stop=True,
        )
        self.assertEqual(rep_c.certified_classical_state_lower_bound, 3)


if __name__ == "__main__":
    unittest.main()
