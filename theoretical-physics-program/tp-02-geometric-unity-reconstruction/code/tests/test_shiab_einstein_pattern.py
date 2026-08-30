import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from verify_shiab_einstein_pattern import build_results  # noqa: E402


class ShiabEinsteinPatternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_results()
        cls.checks = cls.result["checks"]

    def test_all_exact_checks_pass(self):
        self.assertTrue(cls_all(self.checks))

    def test_form_degree_target(self):
        degrees = self.result["degree_checks"]
        self.assertEqual(degrees["ricci_like_output_degree"], 13)
        self.assertEqual(degrees["scalar_like_output_degree"], 13)
        self.assertTrue(degrees["pass"])

    def test_einstein_and_weyl_identities(self):
        self.assertTrue(self.checks["ricci_commutator_identity"])
        self.assertTrue(self.checks["scalar_jordan_identity"])
        self.assertTrue(self.checks["einstein_tensor_identity"])
        self.assertTrue(self.checks["weyl_annihilated_by_selected_einstein_map"])

    def test_dimension_14_rank_benchmark(self):
        dims = self.result["dimension_14"]
        self.assertEqual(dims["algebraic_riemann"], 3185)
        self.assertEqual(dims["weyl"], 3080)
        self.assertEqual(dims["symmetric_two_tensors"], 105)

    def test_source_completeness_is_not_overclaimed(self):
        source = self.result["source_completeness"]
        self.assertTrue(source["explicit_substitute_typed_at_form_degree_level"])
        self.assertTrue(source["einstein_pattern_fixed_on_geometric_riemann_subspace"])
        self.assertFalse(source["unique_full_adjoint_extension"])
        self.assertFalse(source["unique_full_hessian_or_principal_symbol"])


def cls_all(checks):
    return all(checks.values())


if __name__ == "__main__":
    unittest.main()
