import json
import unittest
from pathlib import Path


class VerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[2]
        cls.data = json.loads((root / "results" / "verification_results.json").read_text())

    def test_all_checks_pass(self):
        self.assertTrue(self.data["all_pass"])

    def test_regular_canonical_sector(self):
        witness = self.data["regular_sector_witness"]
        self.assertLess(witness["constraint_norm"], 1e-9)
        self.assertEqual(witness["constraint_jacobian_rank"], 15)
        self.assertEqual(witness["omega_rank"], 56)
        self.assertEqual(witness["diffeomorphism_null_map_rank"], 4)

    def test_KK_truncation_is_not_closed(self):
        modes = self.data["KK_mode_closure"]
        self.assertFalse(modes["finite_truncation_closed"])
        self.assertEqual(modes["missing_modes"], [-2, 2])
        self.assertEqual(modes["first_KK_pair_regular_sector_real_dof"], 26)

    def test_fixed_holonomy_is_not_pure_gauge(self):
        orbit = self.data["orbit_and_holonomy"]
        self.assertEqual(orbit["full_adjoint_orbit_dimension_of_J54"], 8)
        self.assertEqual(orbit["full_adjoint_centralizer_dimension"], 7)
        self.assertEqual(orbit["SO32_vector_orbit_dimension_of_delta5"], 4)
        self.assertEqual(orbit["SO32_vector_stabilizer_dimension"], 6)
        self.assertLess(orbit["vector_holonomy_trace_residual"], 1e-10)

    def test_symplectic_pullback_coefficients(self):
        pullback = self.data["symplectic_pullback"]
        self.assertLess(pullback["EC_coefficient_residual"], 1e-14)
        self.assertLess(pullback["perfect_square_residual"], 1e-14)


if __name__ == "__main__":
    unittest.main()
