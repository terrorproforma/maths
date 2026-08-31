import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from count_scalar_invariants import compute_counts  # noqa: E402
from generate_invariant_coupling_basis import (  # noqa: E402
    build_basis,
    decompose_character,
    irrep_character,
    tensor_decomposition,
)
from verify_phase2b_vacuum import build_results  # noqa: E402


class ScalarInvariantCountTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = compute_counts()

    def test_renormalisable_counts(self):
        self.assertEqual(self.result["totals"]["quadratic"], 7)
        self.assertEqual(self.result["totals"]["cubic"], 0)
        self.assertEqual(self.result["totals"]["quartic"], 131)
        self.assertEqual(
            self.result["totals"]["all_renormalisable_scalar_parameters"],
            138,
        )

    def test_component_count(self):
        self.assertEqual(
            self.result["checks"]["total_real_scalar_components"],
            188,
        )

    def test_weyl_normalization(self):
        self.assertEqual(
            self.result["checks"]["weyl_denominator_constant_term"],
            self.result["checks"]["weyl_group_order"],
        )


class InvariantCouplingBasisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_basis()

    def test_basis_counts_match_molien(self):
        self.assertTrue(self.result["all_pass"])
        self.assertEqual(self.result["checks"]["quadratic_channels"], 7)
        self.assertEqual(self.result["checks"]["cubic_channels"], 0)
        self.assertEqual(self.result["checks"]["quartic_channels"], 131)

    def test_basic_character_dimensions(self):
        self.assertEqual(sum(irrep_character((1, 0, 0, 0, 0)).values()), 4)
        self.assertEqual(sum(irrep_character((1, 0, 1, 1, 1)).values()), 60)
        self.assertEqual(sum(irrep_character((2, 0, 0, 0, 2)).values()), 30)

    def test_fundamental_times_antifundamental(self):
        decomposition = dict(tensor_decomposition((1, 0, 0, 0, 0), (0, 0, 1, 0, 0)))
        self.assertEqual(decomposition, {(0, 0, 0, 0, 0): 1, (1, 0, 1, 0, 0): 1})

    def test_doublet_times_doublet(self):
        decomposition = dict(tensor_decomposition((0, 0, 0, 1, 0), (0, 0, 0, 1, 0)))
        self.assertEqual(decomposition, {(0, 0, 0, 0, 0): 1, (0, 0, 0, 2, 0): 1})


class VacuumSpectrumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_results()
        cls.checks = cls.result["checks"]

    def test_all_checks_pass(self):
        self.assertTrue(self.result["all_pass"])

    def test_goldstone_orbit(self):
        self.assertTrue(self.checks["goldstone_count_is_nine"])
        self.assertTrue(self.checks["broken_generator_rank_is_nine"])
        self.assertTrue(self.checks["goldstone_subspace_matches_broken_orbit"])

    def test_no_tachyon(self):
        self.assertTrue(self.checks["all_physical_scalar_masses_positive"])

    def test_gauge_spectrum(self):
        self.assertTrue(self.checks["gauge_mass_matrix_matches_analytic_spectrum"])
        self.assertEqual(
            self.result["analytic_gauge_spectrum"]["massless_SU3_plus_hypercharge"],
            9,
        )

    def test_scalar_count(self):
        self.assertTrue(self.checks["total_real_scalar_count"])
        self.assertTrue(self.checks["total_physical_scalar_count"])
        self.assertTrue(self.checks["full_scalar_hessian_shape_is_188"])
        self.assertTrue(self.checks["full_scalar_hessian_matches_analytic_spectrum"])
        self.assertTrue(self.checks["full_scalar_hessian_has_nine_goldstones"])
        self.assertTrue(self.checks["full_scalar_hessian_has_179_positive_modes"])


if __name__ == "__main__":
    unittest.main()
