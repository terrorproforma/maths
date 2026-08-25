"""Quantify elementary and deconstructed UV-quality requirements."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import math
from pathlib import Path


MPL = 2.435e18


@dataclass(frozen=True)
class QualityPoint:
    f_a_gev: float = 2.435e10
    heavy_mass_gev: float = 1.002e6
    epsilon: float = 2.70e-13
    n_color: float = 3.0


def protected_amplitude(point: QualityPoint) -> float:
    return 3.0 * point.heavy_mass_gev**4 * point.epsilon**6 / (1280.0 * math.pi**2)


def elementary_c6_bound(point: QualityPoint) -> float:
    return protected_amplitude(point) * MPL**2 / point.f_a_gev**6


def winding_amplitude(point: QualityPoint, links: int, cutoff: float = MPL) -> float:
    f_link = math.sqrt(links) * point.f_a_gev
    return f_link**4 * (f_link / cutoff) ** (links - 4)


def run(point: QualityPoint | None = None) -> dict:
    p = point or QualityPoint()
    protected = protected_amplitude(p)
    c6 = elementary_c6_bound(p)
    rows = []
    for links in (12, 18, 20, 24, 30):
        amplitude = winding_amplitude(p, links)
        rows.append(
            {
                "links": links,
                "winding_amplitude_GeV4": amplitude,
                "protected_amplitude_GeV4": protected,
                "ratio_to_protected": amplitude / protected,
                "quality_pass": amplitude < protected,
            }
        )
    passing = [row["links"] for row in rows if row["quality_pass"]]
    minimum_from_scan = min(passing) if passing else None
    return {
        "evidence_class": "PREDICTION",
        "point": asdict(p),
        "protected_Z6_amplitude_GeV4": protected,
        "elementary_dimension6_coefficient_upper_bound": c6,
        "log10_elementary_c6_bound": math.log10(c6),
        "deconstructed_scan": rows,
        "minimum_passing_link_count_in_declared_scan": minimum_from_scan,
        "recommended_completion": {
            "links": 24,
            "structure": (
                "local U(1)^24 deconstruction with the chronometric phase as a Wilson line; "
                "Z6 acts as a translation by four sites and on the six replica sectors"
            ),
            "why": (
                "local gauge invariance forces a dangerous phase-dependent operator to wind "
                "around the complete moose rather than appear as a dimension-six global-field term"
            ),
        },
        "status": "CONDITIONAL_UV_QUALITY_PASS" if any(
            row["links"] == 24 and row["quality_pass"] for row in rows
        ) else "BLOCKED",
        "conditions": [
            "the moose locality and gauge symmetry survive the UV completion",
            "all mixed gauge and gravitational discrete anomalies cancel",
            "no lower-dimensional nonlocal gravitational operator is generated",
            "messenger loops preserve the complete replica orbit",
        ],
    }


def write_results(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run()
    (output_dir / "uv_quality_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    result = write_results(args.output_dir)
    print(json.dumps(result, indent=2))
