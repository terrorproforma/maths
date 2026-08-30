"""Correct and independently re-run the v1.4/v1.5 LPM evidence layer."""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _legacy_paths(repo_root: Path) -> tuple[Path, Path]:
    base = repo_root / "chronometric-emergence" / "original-info"
    v14 = base / "direct_amy_transport_research_package_v1_4"
    v15 = base / "electroweak_yukawa_lpm_package_v1_5"
    if not v14.exists() or not v15.exists():
        raise FileNotFoundError(f"Legacy transport packages not found below {base}")
    return v14, v15


def corrected_setup_factory(v14: Any):
    def corrected_setup(channel: str, x: float, parameters: dict) -> tuple[tuple[float, float, float], float]:
        mg = parameters["mg2_T2"]
        mq = parameters["mq2_T2"]
        md = parameters["mDf2_T2"]
        mh = parameters["mH2_T2"]
        if channel == "g_to_gg":
            casimirs, masses = (v14.CA, v14.CA, v14.CA), (mg, mg, mg)
        elif channel == "q_to_gq":
            casimirs, masses = (v14.CF, v14.CA, v14.CF), (mq, mg, mq)
        elif channel == "D_to_gD":
            casimirs, masses = (v14.CF, v14.CA, v14.CF), (md, mg, md)
        elif channel == "g_to_qq":
            casimirs, masses = (v14.CA, v14.CF, v14.CF), (mg, mq, mq)
        elif channel == "g_to_DD":
            casimirs, masses = (v14.CA, v14.CF, v14.CF), (mg, md, md)
        elif channel == "H_to_qD":
            casimirs, masses = (0.0, v14.CF, v14.CF), (mh, mq, md)
        else:
            raise KeyError(channel)
        parent, daughter_x, daughter_1mx = masses
        mass_combination = (
            (1.0 - x) * daughter_x
            + x * daughter_1mx
            - x * (1.0 - x) * parent
        ) / mg
        return v14.ccoeff(*casimirs), mass_combination

    return corrected_setup


def run(repo_root: Path, full: bool = True) -> dict:
    repo_root = repo_root.resolve()
    v14_dir, v15_dir = _legacy_paths(repo_root)
    sys.path.insert(0, str(v14_dir))
    v14 = _load_module("frontier_legacy_v14", v14_dir / "verify_full_amy_collision_v1_4.py")
    original_setup = v14.setup
    channels = ["g_to_gg", "q_to_gq", "D_to_gD", "g_to_qq", "g_to_DD", "H_to_qD"]
    point = {"pT": 3.0, "alpha": 0.0393544, "yD": 0.30, "MDT": 0.01}

    old_rates = {
        channel: float(v14.integrated_rate(channel, point["pT"], point["alpha"], point["yD"], point["MDT"]))
        for channel in channels
    }
    v14.setup = corrected_setup_factory(v14)
    corrected_rates = {
        channel: float(v14.integrated_rate(channel, point["pT"], point["alpha"], point["yD"], point["MDT"]))
        for channel in channels
    }
    v14.setup = original_setup

    rate_changes = {
        channel: {
            "old": old_rates[channel],
            "corrected": corrected_rates[channel],
            "relative_change": corrected_rates[channel] / max(old_rates[channel], 1.0e-300) - 1.0,
        }
        for channel in channels
    }

    v14.setup = corrected_setup_factory(v14)
    weak_alphas = np.asarray([1.0e-4, 2.0e-4, 4.0e-4])
    weak_rates = np.asarray(
        [v14.integrated_rate("g_to_gg", 3.0, float(a), 0.30, 0.01) for a in weak_alphas]
    )
    v14.setup = original_setup
    weak_slope = float(np.polyfit(np.log(weak_alphas), np.log(np.maximum(weak_rates, 1.0e-300)), 1)[0])

    deep_lpm = []
    for eta in (10.0, 100.0, 1000.0):
        exact = float(v14.solve_lpm(eta, 0.5, 0.0, v14.ccoeff(v14.CA, v14.CA, v14.CA)).mu2)
        asymptotic = float(v14.deep_lpm_gg(eta))
        deep_lpm.append(
            {
                "eta": eta,
                "direct": exact,
                "deep_LPM": asymptotic,
                "relative_difference": (exact - asymptotic) / asymptotic,
            }
        )

    sys.path.insert(0, str(v15_dir))
    v15 = _load_module("frontier_legacy_v15", v15_dir / "verify_electroweak_yukawa_lpm_v1_5.py")
    qd = v15.qd_thermal_data(v15.ModelPoint())
    electron = v15.electron_thermal_data()
    quality_low = v15.MEDIUM if not full else v15.HIGH8
    quality_high = v15.HIGH8 if not full else v15.HIGH10

    electron_low, _ = v15.integrate_lpm(electron, quality_low)
    electron_high, _ = v15.integrate_lpm(electron, quality_high)
    qd_low, _ = v15.integrate_lpm(qd, quality_low)
    qd_high, _ = v15.integrate_lpm(qd, quality_high)
    susceptibility = 2.0 / 3.0
    gamma_occ = v15.NC * v15.ModelPoint().y_d**2 * qd_high / susceptibility

    gates = {
        "v14_mass_formula_changed_nontrivially": any(
            abs(value["relative_change"]) > 1.0e-3 for value in rate_changes.values()
        ),
        "weak_scattering_log_slope_near_one": abs(weak_slope - 1.0) < 0.12,
        "v15_electron_external_fit_within_15_percent": abs(electron_high - electron["fit"]) / electron["fit"] < 0.15,
        "v15_qd_resolution_change_lt_8_percent": abs(qd_high - qd_low) / max(abs(qd_high), 1.0e-30) < 0.08,
        "v15_electron_resolution_change_lt_8_percent": abs(electron_high - electron_low) / max(abs(electron_high), 1.0e-30) < 0.08,
        "corrected_rates_finite_nonnegative": all(
            math.isfinite(value) and value >= 0.0 for value in corrected_rates.values()
        ),
    }

    return {
        "evidence_class": ["INDEPENDENT_RECOMPUTATION", "CONVERGENCE", "EXTERNAL_BENCHMARK"],
        "full_recomputation": full,
        "benchmark_point": point,
        "v14_mass_formula": {
            "deprecated": "m_parent^2-(1-x)m_1^2-xm_2^2",
            "corrected": "(1-x)m_1^2+xm_2^2-x(1-x)m_parent^2",
            "rates": rate_changes,
            "scientific_status": "DEPRECATED_NUMBERS_RECOMPUTED_AS_DIAGNOSTIC",
        },
        "bethe_heitler_scaling": {
            "alpha_s": weak_alphas.tolist(),
            "rates": weak_rates.tolist(),
            "log_log_slope": weak_slope,
        },
        "deep_lpm_comparison": deep_lpm,
        "v15_recomputation": {
            "electron_low_resolution": electron_low,
            "electron_high_resolution": electron_high,
            "published_fit": electron["fit"],
            "electron_high_relative_to_fit": (electron_high - electron["fit"]) / electron["fit"],
            "qd_low_resolution": qd_low,
            "qd_high_resolution": qd_high,
            "qd_resolution_relative_change": (qd_high - qd_low) / qd_high,
            "Gamma_H_occupation_over_T": gamma_occ,
            "scope": (
                "collinear LPM q-D-H contribution; hard Yukawa-assisted 2<->2 cuts and full off-shell "
                "matching are not included"
            ),
        },
        "gates": gates,
        "all_gates_pass": bool(all(gates.values())),
    }


def write_results(repo_root: Path, output_dir: Path, full: bool = True) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run(repo_root, full=full)
    (output_dir / "lpm_repair_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args()
    result = write_results(args.repo_root, args.output_dir, full=not args.fast)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["all_gates_pass"] else 2)
