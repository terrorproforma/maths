import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from verify_inhomogeneous_group_signs import build_results  # noqa: E402


class SignConventionAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_results()
        cls.checks = cls.result["checks"]

    def test_group_and_action_are_consistent(self):
        self.assertTrue(self.checks["printed_semidirect_product_is_associative_in_exact_test"])
        self.assertTrue(self.checks["printed_affine_formula_is_a_right_action_in_exact_test"])

    def test_printed_tilted_map_is_the_stabilizer(self):
        self.assertTrue(self.checks["printed_tau_minus_is_a_homomorphism_in_exact_test"])
        self.assertTrue(self.checks["printed_tau_minus_stabilizes_A0"])

    def test_printed_augmented_torsion_fails_equivariance(self):
        self.assertFalse(self.checks["printed_T_minus_is_equivariant_under_tau_minus"])
        self.assertTrue(self.checks["T_minus_failure_matches_minus_2_h_inverse_dA0_h"])

    def test_plus_sign_repair_works(self):
        self.assertTrue(self.checks["repaired_T_plus_is_equivariant_under_tau_minus"])

    def test_alternative_tau_loses_stabilizer_property(self):
        self.assertTrue(self.checks["printed_T_minus_is_equivariant_under_tau_plus"])
        self.assertFalse(self.checks["alternative_tau_plus_stabilizes_A0"])


if __name__ == "__main__":
    unittest.main()
