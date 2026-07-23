"""Command-line verification entry point."""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from .certificates import verify_coefficient_formula
from .horner import specialized_nilpotency_checks, verify_counterexample_suspension
from .maps import verify_three_variable_maps


def run(strict: bool = False) -> dict[str, object]:
    report: dict[str, object] = {
        "three_variable_maps": verify_three_variable_maps(),
        "weighted_horner_suspension": verify_counterexample_suspension(),
        "inverse_coefficients": verify_coefficient_formula(6 if strict else 3),
        "claim_scope": {
            "d": 7,
            "p": 15,
            "k_family": "3m",
            "statement": "fixed pair only",
        },
    }
    if strict:
        report["nilpotency_regressions"] = specialized_nilpotency_checks()
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="run extra exact matrix-power regression checks",
    )
    args = parser.parse_args(argv)
    report = run(strict=args.strict)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
