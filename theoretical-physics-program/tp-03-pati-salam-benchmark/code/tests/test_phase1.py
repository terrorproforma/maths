import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from verify_pati_salam_phase1 import build_results  # noqa: E402


class PatiSalamPhase1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = build_results()
        cls.checks = cls.results["checks"]

    def test_pati_salam_anomalies(self):
        self.assertTrue(
            self.checks["PS_local_anomalies_cancel_per_generation"]
        )
        self.assertTrue(
            self.checks["PS_global_SU2_anomalies_cancel_per_generation"]
        )

    def test_standard_model_recovery(self):
        self.assertTrue(self.checks["SM_decomposition_is_anomaly_free"])
        anomalies = self.results["standard_model_recovery"][
            "SM_anomalies_per_generation"
        ]
        for key in [
            "SU3_cubic",
            "SU3_squared_U1Y",
            "SU2_squared_U1Y",
            "U1Y_cubic",
            "gravity_squared_U1Y",
        ]:
            self.assertEqual(anomalies[key], "0")

    def test_breaking_direction_and_normalization(self):
        self.assertTrue(self.checks["SU4_generator_normalization"])
        self.assertTrue(
            self.checks["Delta_R_has_neutral_breaking_direction"]
        )

    def test_minimal_yukawa_obstruction(self):
        sector = self.results["yukawa_sector"]
        self.assertTrue(sector["PS0_verdict"].startswith("rejected"))
        self.assertEqual(
            sector["PS0_exact_mass_relations"],
            ["M_d=M_e", "M_u=M_D_nu"],
        )

    def test_15_bidoublet_repair(self):
        self.assertTrue(
            self.checks[
                "15_bidoublet_repair_reconstructs_arbitrary_pairs"
            ]
        )

    def test_one_loop_matching_baseline(self):
        baseline = self.results["gauge_matching_baseline"]
        self.assertTrue(baseline["matching_passes_numerically"])
        self.assertGreater(baseline["M_PS_GeV"], 1.0e12)
        self.assertLess(baseline["M_PS_GeV"], 1.0e15)


if __name__ == "__main__":
    unittest.main()
