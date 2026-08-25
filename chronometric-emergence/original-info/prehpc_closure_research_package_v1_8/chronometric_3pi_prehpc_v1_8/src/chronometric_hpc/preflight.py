from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from .config import load_config
from .kernels import MatchedKernel


def run(config_path: str | Path, results_path: str | Path) -> dict:
    cfg = load_config(config_path)
    kernel = MatchedKernel.load(cfg.table_path)
    with Path(results_path).open(encoding="utf-8") as handle:
        results = json.load(handle)
    acc = cfg.acceptance
    checks = {
        "factorization_scale": kernel.factorization_spread() <= acc["factorization_scale_relative_spread_max"],
        "on_shell_anchor": results["pointwise_matching"]["on_shell_max_interpolation_residual"] <= acc["on_shell_width_relative_error_max"],
        "STI": results["vertex_and_STI_closure"]["STI_max_relative_residual"] <= acc["quantum_STI_relative_residual_max"],
        "singlet_BSE": results["singlet_BSE"]["BSE_equation_max_absolute_residual"] <= acc["singlet_BSE_equation_residual_max"],
        "singlet_positivity": results["singlet_BSE"]["positive_frequency_minimum"] >= -acc["singlet_spectral_negative_tolerance"],
        "KMS_noise_positivity": results["pointwise_matching"]["KMS_noise_minimum"] >= -acc["singlet_spectral_negative_tolerance"],
    }
    return {"checks": checks, "all_pass": all(checks.values())}
