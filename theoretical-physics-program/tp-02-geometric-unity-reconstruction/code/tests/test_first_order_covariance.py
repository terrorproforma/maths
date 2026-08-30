import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from verify_first_order_action_covariance import build_results  # noqa: E402


class FirstOrderActionCovarianceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_results()
        cls.checks = cls.result["checks"]

    def test_pairing_is_ad_invariant(self):
        self.assertTrue(self.checks["trace_pairing_is_Ad_invariant_for_test_data"])

    def test_printed_branch_fails(self):
        self.assertFalse(self.checks["printed_action_is_invariant"])
        self.assertTrue(self.checks["printed_action_defect_equals_14"])
        self.assertTrue(self.checks["printed_action_defect_matches_analytic_matrix_defect"])

    def test_repaired_branch_passes(self):
        self.assertTrue(self.checks["repaired_action_is_invariant"])


if __name__ == "__main__":
    unittest.main()
