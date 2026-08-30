import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from verify_observation_pullback import build_results  # noqa: E402


class ObservationPullbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = build_results()

    def test_dimension_and_signature_split(self):
        geometry = self.results["geometry"]
        self.assertEqual(geometry["dim_X"], 4)
        self.assertEqual(geometry["dim_Y"], 14)
        self.assertEqual(geometry["normal_rank"], 10)
        self.assertEqual(geometry["signature_X"], [1, 3])
        self.assertEqual(geometry["signature_normal"], [6, 4])
        self.assertEqual(geometry["signature_Y"], [7, 7])

    def test_all_normal_witnesses_break_descent(self):
        witnesses = self.results["normal_jet_witnesses"]
        self.assertEqual(len(witnesses), 10)
        self.assertTrue(all(not witness["ideal_preserved"] for witness in witnesses))
        self.assertTrue(
            all(witness["ambient_operator_then_pullback"] in (-2, 2)
                for witness in witnesses)
        )

    def test_naive_pullback_branch_is_rejected(self):
        verdict = self.results["verdict"]
        self.assertEqual(verdict["R_PLUS_EIN_OBS4_PULLBACK"], "REJECTED")
        self.assertEqual(verdict["fatal_gate"], "PERT-02")


if __name__ == "__main__":
    unittest.main()
