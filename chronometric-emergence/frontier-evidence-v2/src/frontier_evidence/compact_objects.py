"""Compact-object audit of the low-f_a chronometric ridge."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path


MPL = 2.435e18
P_QCD = 2.0 / 27.0
Q_CONVERSION = 0.633135


@dataclass(frozen=True)
class RidgePoint:
    f_a_gev: float = 2.435e10
    epsilon: float = 2.70e-13
    d_g: float = 1.0e-6
    eta_heavy_max: float = 612.0


OBJECTS = {
    "Earth": 6.95e-10,
    "Sun_surface": 2.12e-6,
    "white_dwarf_typical": 1.0e-4,
    "neutron_star_low_compactness": 0.12,
    "neutron_star_typical": 0.20,
    "neutron_star_high_compactness": 0.30,
}


def scalar_compactness(phi_newton: float, point: RidgePoint) -> float:
    return 2.0 * P_QCD * point.epsilon * (MPL / point.f_a_gev) ** 2 * phi_newton


def run(point: RidgePoint | None = None) -> dict:
    p = point or RidgePoint()
    objects = []
    for name, potential in OBJECTS.items():
        q = scalar_compactness(potential, p)
        objects.append(
            {
                "object": name,
                "newtonian_potential": potential,
                "q": q,
                "q_over_conversion_threshold": q / Q_CONVERSION,
                "conversion_necessary_condition_met": q > Q_CONVERSION,
            }
        )

    y = p.f_a_gev / MPL
    epsilon_from_ridge = 27.0 * p.d_g * y
    relation_error = abs(epsilon_from_ridge - p.epsilon) / p.epsilon
    safe_y_ns = 4.0 * p.d_g * OBJECTS["neutron_star_typical"] / Q_CONVERSION
    safe_fa_ns = safe_y_ns * MPL
    eta_at_no_conversion_boundary = 6.12 * p.d_g / safe_y_ns
    q_eta_ratio_ns = scalar_compactness(OBJECTS["neutron_star_typical"], p) / p.eta_heavy_max

    blocker = any(
        row["conversion_necessary_condition_met"]
        for row in objects
        if row["object"].startswith("neutron_star")
    )
    return {
        "evidence_class": "PREDICTION",
        "point": asdict(p),
        "ridge_relation_epsilon_27dg_y_relative_error": relation_error,
        "objects": objects,
        "no_conversion_fa_min_GeV_for_typical_NS_at_same_dg": safe_fa_ns,
        "maximum_heavy_focusing_at_NS_no_conversion_boundary": eta_at_no_conversion_boundary,
        "q_over_eta_for_typical_NS": q_eta_ratio_ns,
        "single_source_ridge_no_go": {
            "statement": (
                "Within the archived N=6 ridge relations, the same d_g/f_a combination "
                "controls heavy-threshold focusing and compact-object conversion. Requiring "
                "q_NS<q_conv caps the heavy focusing measure near 4.8, below the demonstrated "
                "strong-attractor regime."
            ),
            "assumptions": [
                "one QCD-coupled ratio mode",
                "epsilon=27 d_g f_a/M_P",
                "archived heavy-threshold focusing fit",
                "spherical conversion capacity criterion",
                "no additional density-dependent screening or transient selector bath",
            ],
        },
        "neutron_star_blocker": blocker,
        "scientific_status": "BLOCKED" if blocker else "CONDITIONAL",
        "allowed_repairs": [
            "derive and confront a converted/scalarised neutron-star branch with binary-pulsar data",
            "introduce a demonstrated compact-object screening mechanism",
            "separate the transient cosmological focusing interaction from the late QCD coupling",
        ],
    }


def write_results(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run()
    (output_dir / "compact_object_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    answer = write_results(args.output_dir)
    print(json.dumps(answer, indent=2))
