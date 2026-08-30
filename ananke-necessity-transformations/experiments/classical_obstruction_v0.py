"""ANANKE v0.1: extract and certify a finite-classical obstruction."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from ananke import (
    build_hankel,
    extract_minimal_process,
    finite_classical_channel_obstruction_from_rational_angles,
    qubit_rotation_process,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "classical_obstruction_v0.json"


def main() -> None:
    exact_angles = {
        "x": Fraction(73, 100),
        "z": Fraction(111, 100),
    }
    physical = qubit_rotation_process(
        theta_x=float(exact_angles["x"]),
        theta_z=float(exact_angles["z"]),
    )
    hankel = build_hankel(
        physical.behavior,
        physical.alphabet,
        max_prefix_length=2,
        max_suffix_length=2,
    )
    extraction = extract_minimal_process(hankel)
    obstruction = finite_classical_channel_obstruction_from_rational_angles(
        extraction.process,
        exact_angles,
    )

    result = {
        "experiment": "ANANKE finite-classical obstruction v0.1",
        "extracted_rank": extraction.retained_rank,
        "obstruction": obstruction,
        "pass": bool(
            extraction.retained_rank == 4
            and obstruction["finite_classical_realization_obstructed"]
        ),
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
