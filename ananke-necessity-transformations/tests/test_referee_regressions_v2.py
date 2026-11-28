"""Adversarial referee regression tests for ANANKE v2 soundness fixes.

Covers every fatal/major counterexample surfaced by cross-model referee audit:
1. Deterministic 2-state process at M=10^50 must NOT certify rank > 2.
2. Low-precision angle wrapping at (N=3, theta=6.2, prec=2) must contain true ~0.87684.
3. Order 1 (Theta_1 = {1}) must NOT be excluded by initialization when z=1, r=0.
4. Binary64 overflow on finite Decimal distance must return sys.float_info.max, not inf.
5. Tiny sub-exponent Interval.sqrt(1e-1000059) must return immediately and soundly.
6. Default split_shot_dataset RNG must not be fixed to seed 0 across calls.
7. Periodic Karpelevic Markov helper must include both d and d+1 plateau candidates.
"""

from __future__ import annotations

import math
import sys
import unittest
from decimal import Decimal

import numpy as np

from ananke.certified_inference import (
    certify_classical_memory_lower_bound,
    certify_eigenmode_split_sample,
    certify_hankel_rank,
)
from ananke.diophantine_design import periodic_karpelevich_markov_constant
from ananke.interval import Interval
from ananke.karpelevich_certified import (
    certified_distance_to_karpelevich,
    certified_karpelevich_radius,
    certify_finite_stochastic_exclusions,
)
from ananke.observations import ShotDataset
from ananke.words import words_upto


class RefereeRegressionV2Tests(unittest.TestCase):
    def test_deterministic_two_state_process_huge_shots_never_certifies_rank_above_two(
        self,
    ) -> None:
        alphabet = ("x", "z")
        m_trials = 10**50
        successes: dict[str, int] = {}
        trials: dict[str, int] = {}
        for word in words_upto(alphabet, 5):
            trailing_z = 0
            for ch in reversed(word):
                if ch == "z":
                    trailing_z += 1
                else:
                    break
            trials[word] = m_trials
            successes[word] = m_trials if (trailing_z % 2 == 0) else 0
        ds = ShotDataset(alphabet, successes, trials)

        rank_res = certify_hankel_rank(ds, 2, 2, alpha=0.01)
        self.assertEqual(rank_res.certified_rank_lower_bound, 2)

        mem_res = certify_classical_memory_lower_bound(
            ds,
            max_prefix_length=2,
            max_suffix_length=2,
            retained_rank=2,
            symbol="z",
            method="single",
            alpha=0.01,
            target=-1.0 + 0.0j,
            maximum_order=5,
        )
        self.assertLessEqual(mem_res.certified_classical_state_lower_bound, 2)

    def test_low_precision_angle_wrap_retains_true_radius(self) -> None:
        true_r = 0.5 / math.cos(6.2 - 5.0 * math.pi / 3.0)
        enc = certified_karpelevich_radius(3, 6.2, prec=2)
        self.assertLessEqual(enc.radius_lo, true_r)
        self.assertGreaterEqual(enc.radius_hi, true_r)

    def test_order_one_not_excluded_when_point_is_one(self) -> None:
        rep = certify_finite_stochastic_exclusions(
            1.0 + 0.0j,
            0.0,
            confidence_level=0.99,
            hankel_rank_lower_bound=1,
            maximum_order=2,
        )
        self.assertEqual(rep.certified_excluded_through, 0)
        self.assertEqual(rep.certified_classical_state_lower_bound, 1)

    def test_binary64_overflow_returns_finite_float_max_lower_bound(self) -> None:
        res = certified_distance_to_karpelevich(complex(1.7e308, 1.7e308), 1)
        self.assertEqual(res.distance_lo, sys.float_info.max)
        self.assertTrue(math.isinf(res.distance_hi) and res.distance_hi > 0.0)

    def test_tiny_subexponent_interval_sqrt_terminates_and_encloses(self) -> None:
        val = Decimal("1e-1000059")
        root_iv = Interval.exact(val).sqrt(28)
        self.assertGreater(root_iv.lo, Decimal(0))
        self.assertLessEqual(root_iv.lo, root_iv.hi)
        # Verify scaled enclosure: (lo * 10^500030)^2 <= 10 <= (hi * 10^500030)^2
        lo_s = root_iv.lo.scaleb(500030)
        hi_s = root_iv.hi.scaleb(500030)
        self.assertLessEqual(lo_s * lo_s, Decimal(10))
        self.assertGreaterEqual(hi_s * hi_s, Decimal(10))

    def test_default_split_sample_uses_fresh_randomness(self) -> None:
        from ananke import qubit_rotation_process, simulate_words_upto

        proc = qubit_rotation_process()
        ds = simulate_words_upto(proc, 7, 500, np.random.default_rng(7))
        estimates = {
            certify_eigenmode_split_sample(
                ds,
                max_prefix_length=3,
                max_suffix_length=3,
                retained_rank=4,
                symbol="x",
                alpha=0.05,
                rng=None,
            ).point_estimate
            for _ in range(6)
        }
        self.assertGreater(len(estimates), 1)

    def test_periodic_markov_helper_handles_second_plateau_candidate(self) -> None:
        val = periodic_karpelevich_markov_constant((10, 1, 1, 1))
        self.assertGreater(val, 0.0)
        self.assertLess(val, 7.4789)

    def test_v3_bspline_multiplier_exact_angle_and_low_ambient_prec(self) -> None:
        from decimal import localcontext
        from ananke.interval import exp_interval, log_interval
        from ananke.rank_unrestricted import certify_bspline_multiplier

        # Exact angle 3.2 at N=2, M=2: exact supremum ~ 27.20017565866149
        r1 = certify_bspline_multiplier(2, 2, 3.2, num_moments=0)
        self.assertTrue(r1.certified)
        self.assertGreaterEqual(r1.psi_upper_bound, 27.20017565866149)

        # Low ambient Decimal precision (prec=3) must never corrupt sqrt(40) or multiplier
        with localcontext() as ctx:
            ctx.prec = 3
            s = Interval.exact(2).sqrt(40)
            ref = Decimal("1.41421356237309504880168872420969807856967")
            self.assertLess(s.lo, ref)
            self.assertGreater(s.hi, ref)
            r2 = certify_bspline_multiplier(2, 1, 0.73, num_moments=0, tol=1e-12)
            self.assertTrue(r2.certified)
            self.assertGreaterEqual(r2.psi_upper_bound, 15.202602328265127)

        # Extreme positive log and subnormal exp must terminate soundly without Overflow
        lg = log_interval(Interval.exact(Decimal("1e1000001")), 28)
        self.assertGreater(lg.lo, Decimal("2302585"))
        self.assertLess(lg.hi, Decimal("2302590"))
        ex = exp_interval(Interval.exact(Decimal("-2302586")), 28)
        self.assertGreaterEqual(ex.lo, Decimal(0))
        self.assertGreater(ex.hi, Decimal(0))


if __name__ == "__main__":
    unittest.main()
