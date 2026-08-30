import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from verify_cl77_rplus_ein import build_results  # noqa: E402


class Cl77RPlusEinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = build_results()
        cls.checks = cls.results["checks"]

    def test_exact_clifford_representation(self):
        self.assertTrue(self.checks["Cl_7_7_exact"])
        self.assertEqual(
            self.results["clifford_representation"]["spinor_dimension"],
            128,
        )

    def test_split_spinor_form_and_chirality(self):
        split = self.results["clifford_representation"]["split_spinor_form"]
        chirality = self.results["clifford_representation"]["chirality"]
        self.assertEqual(
            (split["positive_eigenvalue_count"], split["negative_eigenvalue_count"]),
            (64, 64),
        )
        self.assertEqual(
            (chirality["plus_dimension"], chirality["minus_dimension"]),
            (64, 64),
        )
        self.assertTrue(chirality["H_pairs_opposite_chiralities"])

    def test_spin_embedding(self):
        self.assertTrue(self.checks["Spin_7_7_embeds_in_u_64_64"])

    def test_full_adjoint_completion_closes(self):
        audit = self.results["full_adjoint_einstein_extension"]
        self.assertEqual(
            audit["symmetrized_extension_max_H_skew_residual"],
            0,
        )
        self.assertGreater(
            audit["naive_unsymmetrized_max_H_skew_residual"],
            0,
        )

    def test_split_signature_symbol_obstruction(self):
        symbol = self.results["split_signature_principal_symbol"]
        self.assertFalse(symbol["hyperbolic_with_respect_to_any_covector"])
        self.assertEqual(symbol["formal_14d_einstein_metric_polarizations"], 77)
        self.assertEqual(symbol["formal_excess_before_observation_reduction"], 75)


if __name__ == "__main__":
    unittest.main()
