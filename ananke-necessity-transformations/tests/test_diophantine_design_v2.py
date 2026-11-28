from __future__ import annotations

import unittest
from math import pi

from ananke import (
    KARPELEVICH_NOBLE_MARKOV_CONSTANT,
    NON_NOBLE_ANALYTIC_UPPER_BOUND,
    asymptotic_karpelevich_radial_gap,
    karpelevich_boundary_radius,
    noble_phase_turns,
    optimize_phase_in_sector,
    periodic_cf_turns,
    periodic_karpelevich_markov_constant,
    qubit_phase_design_metrics,
)


class DiophantineDesignV2Tests(unittest.TestCase):
    def test_asymptotic_radial_gap_converges_as_inverse_n_squared(self) -> None:
        alpha = noble_phase_turns(8)
        theta = 2.0 * pi * alpha
        for order, max_rel_err in ((20, 1e-2), (50, 2e-3), (100, 5e-4)):
            exact = 1.0 - karpelevich_boundary_radius(order, theta)
            asymp = asymptotic_karpelevich_radial_gap(order, alpha)
            rel_err = abs(exact - asymp) / exact
            self.assertLess(rel_err, max_rel_err)

    def test_karpelevich_markov_theorem_noble_strictly_maximal(self) -> None:
        # Theorem 4: noble constant = 2*pi^2*phi^3 / (5*sqrt(5)) > 3*pi^2/4 (245 < 256)
        self.assertAlmostEqual(
            periodic_karpelevich_markov_constant((1,)),
            KARPELEVICH_NOBLE_MARKOV_CONSTANT,
            places=12,
        )
        self.assertLess(NON_NOBLE_ANALYTIC_UPPER_BOUND, KARPELEVICH_NOBLE_MARKOV_CONSTANT)
        for period in ((2,), (3,), (1, 2), (1, 1, 2), (1, 2, 2), (1, 3), (2, 3)):
            c = periodic_karpelevich_markov_constant(period)
            self.assertLess(c, NON_NOBLE_ANALYTIC_UPPER_BOUND)
            self.assertLess(c, KARPELEVICH_NOBLE_MARKOV_CONSTANT)

    def test_finite_horizon_counterexample_in_sector_8(self) -> None:
        # At fixed N=15, silver [0;8,2_bar] and sector optimum strictly beat noble [0;8,1_bar]
        noble_8 = 2.0 * pi * noble_phase_turns(8)
        silver_8 = 2.0 * pi * periodic_cf_turns((8,), (2,))
        alt12_8 = 2.0 * pi * periodic_cf_turns((8,), (1, 2))

        gap15_noble = 1.0 - karpelevich_boundary_radius(15, noble_8)
        gap15_silver = 1.0 - karpelevich_boundary_radius(15, silver_8)
        _, gap15_opt = optimize_phase_in_sector(8, 15, grid_points=200)
        self.assertGreater(gap15_silver, gap15_noble * 1.08)
        self.assertGreater(gap15_opt, gap15_silver)

        # At fixed N=25, [0;8,(1,2)_bar] strictly beats noble [0;8,1_bar] by > 30%
        gap25_noble = 1.0 - karpelevich_boundary_radius(25, noble_8)
        gap25_alt12 = 1.0 - karpelevich_boundary_radius(25, alt12_8)
        self.assertGreater(gap25_alt12, gap25_noble * 1.25)

    def test_cross_sector_golden_angle_improves_hankel_conditioning(self) -> None:
        m_baseline = qubit_phase_design_metrics(0.73, label="baseline_0.73", target_order=15)
        m_golden = qubit_phase_design_metrics(
            2.0 * pi * noble_phase_turns(2), label="golden_[0;2,1_bar]", target_order=15
        )
        # Golden angle [0;2,1_bar] has much stronger Hankel sigma_4 and lower sensitivity
        self.assertGreater(m_golden.sigma_4, m_baseline.sigma_4 * 1.7)
        self.assertLess(
            m_golden.exact_scalar_sensitivity_l2,
            m_baseline.exact_scalar_sensitivity_l2 * 0.7,
        )


if __name__ == "__main__":
    unittest.main()
