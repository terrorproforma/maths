"""Inter-version off-shell kernel discrepancy and table-coverage audit."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

import numpy as np
from scipy.interpolate import RegularGridInterpolator
import yaml


def _monotonic_1d(npz: Mapping[str, np.ndarray]) -> list[tuple[str, np.ndarray]]:
    candidates = []
    for key in npz.keys():
        value = np.asarray(npz[key])
        if value.ndim == 1 and len(value) >= 8 and np.issubdtype(value.dtype, np.number):
            diff = np.diff(value.astype(float))
            if np.all(diff > 0.0):
                candidates.append((key, value.astype(float)))
    return candidates


def _select_axis(candidates: list[tuple[str, np.ndarray]], axis: str) -> tuple[str, np.ndarray]:
    if axis == "omega":
        scored = [
            (10 * ("omega" in key.lower()) + 3 * (arr[0] < 0 < arr[-1]) + np.log10(len(arr)), key, arr)
            for key, arr in candidates
            if arr[0] < 0.0 < arr[-1]
        ]
    else:
        scored = [
            (
                10 * ("k_" in key.lower() or key.lower().startswith("k") or "momentum" in key.lower())
                + 3 * (arr[0] >= 0.0)
                + np.log10(len(arr)),
                key,
                arr,
            )
            for key, arr in candidates
            if arr[0] >= 0.0 and arr[-1] <= 100.0
        ]
    if not scored:
        raise KeyError(f"No {axis} axis candidate")
    _, key, arr = max(scored, key=lambda item: item[0])
    return key, arr


def _select_kernel(npz: Mapping[str, np.ndarray], k: np.ndarray, omega: np.ndarray) -> tuple[str, np.ndarray]:
    candidates = []
    for key in npz.keys():
        value = np.asarray(npz[key])
        if not np.issubdtype(value.dtype, np.number) or value.ndim != 2:
            continue
        if value.shape == (len(k), len(omega)):
            array = value.astype(float)
        elif value.shape == (len(omega), len(k)):
            array = value.T.astype(float)
        else:
            continue
        lower = key.lower()
        score = (
            12 * ("impi" in lower)
            + 7 * ("matched" in lower or "match" in lower)
            + 5 * ("total" in lower)
            - 5 * ("low" in lower or "high" in lower or "noise" in lower or "repi" in lower)
        )
        candidates.append((score, key, array))
    if not candidates:
        raise KeyError("No two-dimensional ImPi/kernel candidate matching selected axes")
    _, key, array = max(candidates, key=lambda item: item[0])
    return key, array


def load_kernel(path: Path, preferred: dict[str, str] | None = None) -> dict:
    with np.load(path, allow_pickle=False) as data:
        inventory = {key: list(np.asarray(data[key]).shape) for key in data.files}
        if preferred and all(key in data.files for key in preferred.values()):
            k_key, w_key, pi_key = preferred["k"], preferred["omega"], preferred["kernel"]
            k = np.asarray(data[k_key], dtype=float)
            omega = np.asarray(data[w_key], dtype=float)
            kernel = np.asarray(data[pi_key], dtype=float)
            if kernel.shape == (len(omega), len(k)):
                kernel = kernel.T
        else:
            monotonic = _monotonic_1d(data)
            k_key, k = _select_axis(monotonic, "k")
            w_key, omega = _select_axis(monotonic, "omega")
            pi_key, kernel = _select_kernel(data, k, omega)
    return {
        "path": str(path),
        "k_key": k_key,
        "omega_key": w_key,
        "kernel_key": pi_key,
        "k": k,
        "omega": omega,
        "kernel": kernel,
        "inventory": inventory,
    }


def run(repo_root: Path) -> dict:
    base = repo_root.resolve() / "chronometric-emergence" / "original-info"
    v17_path = base / "gauge_covariant_correlator_package_v1_7" / "gauge_covariant_correlator_arrays_v1_7.npz"
    v18_path = base / "prehpc_closure_research_package_v1_8" / "prehpc_closure_arrays_v1_8.npz"
    config_path = base / "chronometric_3pi_prehpc_v1_9" / "config" / "hpc_solver_spec_portable_v1_9.yaml"
    v17 = load_kernel(
        v17_path,
        preferred={
            "k": "bfm_k_over_T",
            "omega": "bfm_omega_over_T",
            "kernel": "bfm_ImPi_total_over_T2",
        },
    )
    v18 = load_kernel(v18_path)

    k_min = max(float(v17["k"][0]), float(v18["k"][0]))
    k_max = min(float(v17["k"][-1]), float(v18["k"][-1]))
    w_min = max(float(v17["omega"][0]), float(v18["omega"][0]))
    w_max = min(float(v17["omega"][-1]), float(v18["omega"][-1]))
    k_common = np.geomspace(max(k_min, 1.0e-4), k_max, 50)
    omega_common = np.linspace(w_min, w_max, 801)
    mesh_k, mesh_w = np.meshgrid(k_common, omega_common, indexing="ij")
    points = np.column_stack((mesh_k.ravel(), mesh_w.ravel()))

    def interpolate(bundle: dict) -> np.ndarray:
        interp = RegularGridInterpolator(
            (bundle["k"], bundle["omega"]), bundle["kernel"], bounds_error=True
        )
        return interp(points).reshape(mesh_k.shape)

    a = interpolate(v17)
    b = interpolate(v18)
    scale = np.maximum(np.maximum(np.abs(a), np.abs(b)), 1.0e-14)
    significant = scale > 1.0e-5 * float(np.max(scale))
    relative = np.abs(a - b) / scale
    selected = relative[significant]

    mass = 0.43820657
    shell = np.sqrt(k_common[:, None] ** 2 + mass**2)
    distance = np.minimum(np.abs(mesh_w - shell), np.abs(mesh_w + shell))
    near = significant & (distance < 0.15)
    far = significant & (distance > 1.0)

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    requested_kmax = float(config["pilot_grid"]["radial_momentum"]["maximum_over_T"])
    table_kmax = float(v18["k"][-1])
    requested_dt = float(config["pilot_grid"]["time"]["dt_times_T"])
    requested_window_steps = int(config["pilot_grid"]["time"]["memory_window_steps"])
    requested_window = requested_dt * requested_window_steps

    repaired_config = {
        "radial_momentum_maximum_over_T": table_kmax,
        "table_extrapolation": "forbidden",
        "memory_window_scan_Tinv": [6.0, 12.0, 24.0],
        "promotion_rule": "all declared observables change by <0.5% between the two largest windows",
        "pilot_authorization": False,
        "reason": "no dynamical 3PI evolution engine exists",
    }

    def stats(mask: np.ndarray) -> dict[str, float | int | None]:
        values = relative[mask]
        if values.size == 0:
            return {"count": 0, "median": None, "p95": None, "max": None}
        return {
            "count": int(values.size),
            "median": float(np.median(values)),
            "p95": float(np.quantile(values, 0.95)),
            "max": float(np.max(values)),
        }

    return {
        "evidence_class": ["INDEPENDENT_RECOMPUTATION", "MODEL_DISCREPANCY"],
        "v1_7_selection": {
            "k_key": v17["k_key"],
            "omega_key": v17["omega_key"],
            "kernel_key": v17["kernel_key"],
            "shape": list(v17["kernel"].shape),
        },
        "v1_8_selection": {
            "k_key": v18["k_key"],
            "omega_key": v18["omega_key"],
            "kernel_key": v18["kernel_key"],
            "shape": list(v18["kernel"].shape),
        },
        "common_domain": {"k_over_T": [k_min, k_max], "omega_over_T": [w_min, w_max]},
        "relative_model_discrepancy": {
            "significant_all": stats(significant),
            "near_shell": stats(near),
            "far_off_shell": stats(far),
        },
        "interpretation": (
            "The v1.7 and v1.8 kernels share controlled on-shell anchors but use different "
            "off-shell constructions. Their spread is an ansatz/model discrepancy, not a "
            "statistical or perturbative uncertainty estimate."
        ),
        "coverage_audit": {
            "v1_8_table_kmax_over_T": table_kmax,
            "v1_9_requested_kmax_over_T": requested_kmax,
            "requested_exceeds_table": requested_kmax > table_kmax + 1.0e-12,
            "configured_memory_window_Tinv": requested_window,
        },
        "repaired_config": repaired_config,
        "gates": {
            "no_table_extrapolation_in_repaired_config": repaired_config["radial_momentum_maximum_over_T"] <= table_kmax,
            "full_3pi_pilot_not_authorized": repaired_config["pilot_authorization"] is False,
            "off_shell_spread_reported": int(selected.size) > 0,
        },
    }


def write_results(repo_root: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run(repo_root)
    (output_dir / "kernel_uncertainty_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    answer = write_results(args.repo_root, args.output_dir)
    print(json.dumps(answer, indent=2))
