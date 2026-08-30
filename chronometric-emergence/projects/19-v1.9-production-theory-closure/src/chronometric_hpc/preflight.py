from __future__ import annotations
import json
from pathlib import Path
from .config import load_config
from .kernels import MatchedKernel
from .diagram_ledger import validate_ledger
from .tensor_basis import evaluate_basis_metrics
from .renormalization import validate_closure
from .benchmarks import run_benchmarks
from .contracts import validate_contract


def run(config_path: str | Path, results_path: str | Path) -> dict:
    cfg = load_config(config_path)
    kernel = MatchedKernel.load(cfg.table_path)
    with Path(results_path).open(encoding="utf-8") as handle:
        results = json.load(handle)
    acc = cfg.acceptance
    ledger = validate_ledger(cfg.diagram_ledger_path)
    basis = evaluate_basis_metrics()
    closure = validate_closure(cfg.counterterm_matrix_path)
    benchmarks = run_benchmarks()
    contract = validate_contract(cfg.observable_contract_path)
    checks = {
        "factorization_scale": kernel.factorization_spread() <= acc["factorization_scale_relative_spread_max"],
        "on_shell_anchor": results["pointwise_matching"]["on_shell_max_interpolation_residual"] <= acc["on_shell_width_relative_error_max"],
        "STI_seed": results["vertex_and_STI_closure"]["STI_max_relative_residual"] <= acc["quantum_STI_relative_residual_max"],
        "singlet_BSE": results["singlet_BSE"]["BSE_equation_max_absolute_residual"] <= acc["singlet_BSE_equation_residual_max"],
        "singlet_positivity": results["singlet_BSE"]["positive_frequency_minimum"] >= -acc["singlet_spectral_negative_tolerance"],
        "KMS_noise_positivity": results["pointwise_matching"]["KMS_noise_minimum"] >= -acc["singlet_spectral_negative_tolerance"],
        "diagram_ledger": ledger["all_pass"] and len(ledger["loop_failures"]) <= acc["diagram_ledger_loop_failures_max"],
        "fermion_vertex_basis": basis.fermion_vertex_rank >= acc["fermion_vertex_transverse_rank_min"] and basis.fermion_vertex_transverse_residual < 1e-12,
        "three_gauge_basis": basis.three_gauge_rank >= acc["three_gauge_transverse_rank_min"] and basis.three_gauge_transverse_residual < 1e-12,
        "counterterm_closure_basis": closure["all_pass"] and len(closure["missing_required_signatures"]) <= acc["counterterm_unmapped_signatures_max"],
        "analytic_benchmarks": benchmarks["all_pass"],
        "observable_contract": contract["all_pass"],
    }
    return {
        "checks": checks,
        "all_pass": all(checks.values()),
        "details": {
            "diagram_ledger": ledger,
            "tensor_basis": basis.__dict__,
            "counterterm_closure": closure,
            "analytic_benchmarks": benchmarks,
            "observable_contract": contract,
        },
    }
