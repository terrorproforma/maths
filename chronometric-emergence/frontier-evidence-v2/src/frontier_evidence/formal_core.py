"""Corrected formal statements for the surviving chronometric core."""
from __future__ import annotations

import json
from pathlib import Path


def run() -> dict:
    return {
        "evidence_class": "IDENTITY_PIN",
        "universal_clock_factorisation": {
            "statement": (
                "On a connected domain with positive differentiable frequencies omega_A, "
                "there exist a positive scalar chi and positive constants c_A such that "
                "omega_A=c_A chi for every A iff d ln(omega_A/omega_B)=0 for every pair."
            ),
            "proof_outline": [
                "factorisation implies every ratio is constant",
                "if all ratio differentials vanish, choose a reference clock B and set chi=omega_B",
                "connectedness makes each ratio omega_A/omega_B a constant c_A",
            ],
            "status": "EXACT_ELEMENTARY_THEOREM",
        },
        "rank_diagnostic": {
            "one_way_bound": "rank(clock-ratio response) <= number of independent non-universal fields",
            "inference_conditions": [
                "the clock sensitivity-difference matrix has full column rank on the active fields",
                "the fields are independently excited over the data set",
                "noise and unmodelled systematics do not lower the observed rank",
            ],
            "correction": (
                "Observed rank r does not by itself prove that exactly r fields exist; it is a lower "
                "bound only under the declared genericity and excitation assumptions."
            ),
        },
        "v0_2_relations": {
            "status": "RETIRED_AS_UNIVERSAL_CLAIMS",
            "retained_scope": "tree-level consistency relations of the minimal one-mediator soft-null EFT",
        },
        "v0_4_benchmark": {
            "status": "WITHDRAWN_AS_UV_STABLE_BENCHMARK",
            "reason": "later one-loop running drove the displayed Higgs quartic negative before the heavy scale",
        },
        "novelty_status": (
            "The theorem is elementary once stated. Candidate novelty lies in the clock-space quotient, "
            "chronometric-shear interpretation, and its use as a model-selection/experimental framework; "
            "specialist priority review remains required."
        ),
    }


def write_results(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run()
    (output_dir / "formal_core_results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    answer = write_results(args.output_dir)
    print(json.dumps(answer, indent=2))
