"""Leading and next-to-leading heavy-threshold transmission audit."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import math
from pathlib import Path


@dataclass(frozen=True)
class ThresholdPoint:
    alpha_s_at_heavy_threshold: float = 0.0393544
    alpha_s_scale_low: float = 0.032
    alpha_s_scale_high: float = 0.050


def one_loop() -> float:
    return (1.0 - 19.0 / 21.0) * (21.0 / 23.0) * (23.0 / 25.0) * (25.0 / 27.0)


def nlo_low_energy_theorem(alpha_s: float) -> float:
    """Conventional NLO heavy-quark scalar/gluon sensitivity estimate."""
    return one_loop() * (1.0 + 11.0 * alpha_s / (4.0 * math.pi))


def run(point: ThresholdPoint | None = None) -> dict:
    p = point or ThresholdPoint()
    leading = one_loop()
    central = nlo_low_energy_theorem(p.alpha_s_at_heavy_threshold)
    low = nlo_low_energy_theorem(p.alpha_s_scale_low)
    high = nlo_low_energy_theorem(p.alpha_s_scale_high)
    return {
        "evidence_class": ["IDENTITY_PIN", "EXTERNAL_BENCHMARK"],
        "point": asdict(p),
        "one_loop_exact": leading,
        "one_loop_exact_fraction": "2/27",
        "conventional_NLO_estimate": central,
        "relative_NLO_shift": central / leading - 1.0,
        "alpha_s_band": [low, high],
        "scientific_status": (
            "The 2/27 coefficient is valid only at leading order. The NLO estimate "
            "moves it by a few percent; hadronic and multi-threshold uncertainties "
            "must be propagated in any phenomenological line."
        ),
        "novelty_boundary": (
            "Neither 2/27 nor its heavy-quark QCD corrections are new. The project-specific "
            "claim is their interpretation as transmission of a scale-lock defect."
        ),
    }


def write_results(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run()
    (output_dir / "qcd_threshold_results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    result = write_results(args.output_dir)
    print(json.dumps(result, indent=2))
