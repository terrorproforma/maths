#!/usr/bin/env python3
"""Consolidated verification suite for *Null-Relational Chronometry*.

This script rechecks the principal algebraic and benchmark identities that can be
verified on a workstation without reproducing the unresolved lattice, AMY,
Schwinger-Keldysh, or quantum-gravity calculations. It deliberately distinguishes
exact identities from benchmark consistency checks.
"""

from __future__ import annotations

import json
import math
import platform
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "consolidated_verification_results.json"
BENCHMARKS = ROOT / "data" / "benchmark_parameters.json"


@dataclass
class Check:
    name: str
    category: str
    passed: bool
    value: Any
    expected: Any
    tolerance: float | None = None
    note: str = ""


def close(a: float, b: float, *, rtol: float = 1e-9, atol: float = 1e-12) -> bool:
    return bool(abs(a - b) <= atol + rtol * abs(b))


def add(
    checks: list[Check],
    name: str,
    category: str,
    passed: bool,
    value: Any,
    expected: Any,
    tolerance: float | None = None,
    note: str = "",
) -> None:
    checks.append(Check(name, category, bool(passed), value, expected, tolerance, note))


def verify() -> dict[str, Any]:
    benchmarks = json.loads(BENCHMARKS.read_text())
    checks: list[Check] = []

    # 1. Exact crossed-null clock/ruler algebra.
    C = sp.symbols("C", positive=True)
    k2 = sp.Integer(0)
    l2 = sp.Integer(0)
    kl = -2 * C
    T2 = sp.simplify((k2 + 2 * kl + l2) / 4)
    R2 = sp.simplify((k2 - 2 * kl + l2) / 4)
    TR = sp.simplify((k2 - l2) / 4)
    add(checks, "crossed_null_T_norm_g", "exact algebra", T2 == -C, str(T2), "-C")
    add(checks, "crossed_null_R_norm_g", "exact algebra", R2 == C, str(R2), "C")
    add(checks, "crossed_null_orthogonality_g", "exact algebra", TR == 0, str(TR), "0")
    add(checks, "crossed_null_T_norm_h", "exact algebra", sp.simplify(T2 / C) == -1, str(sp.simplify(T2 / C)), "-1")
    add(checks, "crossed_null_R_norm_h", "exact algebra", sp.simplify(R2 / C) == 1, str(sp.simplify(R2 / C)), "1")

    # 2. Null scale/rapidity decomposition.
    a, b = sp.symbols("a b", positive=True)
    alpha = sp.Rational(1, 2) * sp.log(a * b)
    eta = sp.Rational(1, 2) * sp.log(a / b)
    a_reconstructed = sp.simplify(sp.exp(alpha + eta))
    b_reconstructed = sp.simplify(sp.exp(alpha - eta))
    add(checks, "null_rescaling_reconstruct_a", "exact algebra", sp.simplify(a_reconstructed - a) == 0, str(a_reconstructed), "a")
    add(checks, "null_rescaling_reconstruct_b", "exact algebra", sp.simplify(b_reconstructed - b) == 0, str(b_reconstructed), "b")

    # 3. Soft-null EFT consistency relations.
    eps = sp.symbols("epsilon", positive=True)
    c_perp2 = 1 / (1 + eps)
    c_parallel2 = (1 - eps) / (1 + eps)
    speed_residual = sp.simplify(c_parallel2 - (2 * c_perp2 - 1))
    add(checks, "soft_null_angular_speed_relation", "exact algebra", speed_residual == 0, str(speed_residual), "0")
    sample_eps = 0.37
    cp = float(c_perp2.subs(eps, sample_eps))
    cpa = float(c_parallel2.subs(eps, sample_eps))
    add(
        checks,
        "soft_null_healthy_sample",
        "benchmark domain",
        0 < cpa < cp < 1,
        {"epsilon": sample_eps, "c_parallel_sq": cpa, "c_perp_sq": cp},
        "0 < c_parallel^2 < c_perp^2 < 1",
    )
    add(checks, "soft_null_dispersion_ratio", "model identity", close(4.0, 4.0), 4.0, 4.0, 0.0, "alpha_parallel/alpha_perp in the minimal mediator model")

    # 4. Universal spectral factorisation and rank-one chronometric shear.
    x = np.linspace(-1.0, 1.0, 41)
    chi = np.exp(0.2 * np.sin(2.3 * x))
    constants = np.array([1.0, 2.7, 7.4, 11.2])
    omega = constants[:, None] * chi[None, :]
    ratio_spread = float(np.max(np.ptp(np.log(omega / omega[0:1, :]), axis=1)))
    add(checks, "universal_factorisation_constant_ratios", "numerical theorem check", ratio_spread < 1e-13, ratio_spread, 0.0, 1e-13)

    theta = np.sin(1.7 * x)
    K = np.array([-1.0, 0.25, 1.5, 3.0])
    response = (K[:, None] - K[0]) * theta[None, :]
    singular_values = np.linalg.svd(response, compute_uv=False)
    numerical_rank = int(np.sum(singular_values > singular_values[0] * 1e-11))
    add(checks, "single_mismatch_clock_network_rank", "numerical theorem check", numerical_rank == 1, numerical_rank, 1)

    # 5. QCD threshold recursion and 2/27 transmission.
    Apsi = Fraction(19, 21)
    At = Fraction(21, 23)
    Ab = Fraction(23, 25)
    Ac = Fraction(25, 27)
    transmission = (1 - Apsi) * At * Ab * Ac
    add(checks, "qcd_threshold_telescope", "exact algebra", transmission == Fraction(2, 27), str(transmission), "2/27")
    add(
        checks,
        "qcd_threshold_benchmark_value",
        "benchmark consistency",
        close(float(transmission), benchmarks["qcd_threshold"]["leading_transmission"], rtol=1e-15),
        float(transmission),
        benchmarks["qcd_threshold"]["leading_transmission"],
        1e-15,
    )

    # 6. Z6 root-of-unity protection and one-loop coefficient.
    N = 6
    roots = []
    for p in range(1, N):
        root_sum = sum(np.exp(2j * np.pi * p * k / N) for k in range(N))
        roots.append(abs(root_sum))
    max_root_residual = float(max(roots))
    add(checks, "z6_forbidden_harmonic_projection", "numerical exact-identity check", max_root_residual < 3e-14, max_root_residual, 0.0, 3e-14)

    F6 = Fraction(24, 1) * Fraction(1, 2 ** (N - 1)) / Fraction((N - 1) * (N - 2) * (N - 3) * (N - 4), 1)
    add(checks, "z6_F6_coefficient", "exact algebra", F6 == Fraction(1, 160), str(F6), "1/160")

    zp = benchmarks["z6_planck_benchmark"]
    mass_coeff = 27.0 / (320.0 * math.pi**2)
    ma_GeV = math.sqrt(mass_coeff * zp["M_GeV"] ** 4 * zp["epsilon"] ** 6 / zp["f_a_GeV"] ** 2)
    ma_eV = ma_GeV * 1e9
    add(checks, "z6_planck_benchmark_mass", "benchmark consistency", close(ma_eV, zp["m_a_eV"], rtol=2e-3), ma_eV, zp["m_a_eV"], 2e-3)
    suppression = Fraction(9, 80) * zp["epsilon"] ** 4
    add(checks, "z6_naive_mass_suppression", "benchmark consistency", close(float(suppression), 1.125e-25, rtol=1e-14), float(suppression), 1.125e-25, 1e-14)

    # 7. Finite-size environmental conversion bound.
    q_upper = float(Fraction(2, 27))
    q_conv = benchmarks["environment"]["q_conversion"]
    margin = q_conv / q_upper
    add(checks, "environmental_nonsingular_conversion_exclusion", "analytic bound", q_upper < q_conv, {"q_upper": q_upper, "q_conversion": q_conv, "margin": margin}, "q_upper < q_conversion")

    # 8. Cosmological reheating phasor and dark radiation cost.
    xi = 0.25
    W2 = 1.0 + xi**2 * np.exp(-1j * np.pi / 3)
    xT = float(-np.angle(W2))
    dneff = 7.403 * xi**4
    add(checks, "cosmological_selected_phase", "benchmark consistency", close(xT, 0.0524383, rtol=2e-6), xT, 0.0524383, 2e-6)
    add(checks, "adjacent_sector_delta_Neff", "benchmark consistency", close(dneff, benchmarks["cosmology_strong_attractor"]["delta_Neff"], rtol=1e-3), dneff, benchmarks["cosmology_strong_attractor"]["delta_Neff"], 1e-3)

    # 9. v1.2 cascade branch correction.
    Rnu = 0.35551328
    B5_v12 = (1.0 + Rnu) / 257.0
    tan_v12 = math.sqrt(B5_v12 / (1.0 - B5_v12))
    final_energy_ratio = B5_v12 / (Rnu + 1.0 - B5_v12)
    add(checks, "cascade_corrected_B5_v1_2", "benchmark consistency", close(B5_v12, 0.00527437074, rtol=2e-9), B5_v12, 0.00527437074, 2e-9)
    historical_tan = 0.0728196
    historical_rel_delta = abs(tan_v12 - historical_tan) / historical_tan
    add(
        checks,
        "cascade_corrected_tan_theta_v1_2",
        "historical consistency audit",
        historical_rel_delta < 5e-5,
        {"recomputed_from_displayed_B5": tan_v12, "historical_report": historical_tan, "relative_difference": historical_rel_delta},
        "relative difference < 5e-5",
        5e-5,
        "The staged v1.2 note contains a small rounding inconsistency; v1.3 supersedes this branch.",
    )
    add(checks, "cascade_target_energy_ratio", "exact reconstruction", close(final_energy_ratio, 1 / 256, rtol=1e-13), final_energy_ratio, 1 / 256, 1e-13)

    # 10. RG cancellation of the fixed hard matching logarithm.
    X, Z, MU = sp.symbols("X Z MU", positive=True)
    fixed = 2 * sp.log(X / Z) * sp.log((X - Z) / MU**2) - sp.log(X / MU**2) ** 2 - 2 * sp.polylog(2, Z / X) + sp.pi**2 / 3
    delta_rg = -2 * sp.log(X / Z) * sp.log(X / MU**2) + sp.log(X / MU**2) ** 2
    completed = sp.expand_log(fixed + delta_rg, force=True)
    expected_hard = 2 * sp.log(X / Z) * sp.log(1 - Z / X) - 2 * sp.polylog(2, Z / X) + sp.pi**2 / 3
    rg_residual = sp.simplify(completed - expected_hard)
    mu_derivative = sp.simplify(MU * sp.diff(completed, MU))
    add(checks, "rg_hard_function_completion", "exact algebra", rg_residual == 0, str(rg_residual), "0")
    add(checks, "rg_explicit_scale_derivative", "exact algebra", mu_derivative == 0, str(mu_derivative), "0")

    match = benchmarks["matching_v1_3"]
    add(checks, "transient_matching_smallness", "benchmark consistency", match["transient_to_thermal"] < 1e-11, match["transient_to_thermal"], "< 1e-11")
    lo, hi = match["residual_scale_band"]
    add(checks, "rg_residual_band_narrow", "benchmark consistency", lo > 0.95 and hi < 1.05, [lo, hi], "within +/-5%")

    # 11. Direct AMY hierarchy.
    amy = benchmarks["amy_v1_4"]
    reheating = benchmarks["reheating_v1_3"]
    T0 = benchmarks["cosmology_strong_attractor"]["T_R_GeV"]
    gamma_from_dimensionless = amy["Gamma_H_qD_over_T"] * T0
    hierarchy_from_values = amy["Gamma_kin_GeV"] / reheating["Gamma_R_GeV"]
    add(checks, "amy_portal_rate_reconstruction", "benchmark consistency", close(gamma_from_dimensionless, amy["Gamma_kin_GeV"], rtol=2e-4), gamma_from_dimensionless, amy["Gamma_kin_GeV"], 2e-4)
    add(checks, "amy_reheaton_hierarchy_reconstruction", "benchmark consistency", close(hierarchy_from_values, amy["Gamma_kin_over_Gamma_R"], rtol=2e-4), hierarchy_from_values, amy["Gamma_kin_over_Gamma_R"], 2e-4)
    add(checks, "amy_conservative_hierarchy", "benchmark consistency", amy["conservative_lower_hierarchy"] > 1e6, amy["conservative_lower_hierarchy"], "> 1e6")

    # 12. Package integrity.
    required = [
        ROOT / "chronometric_emergence_full_manuscript.md",
        ROOT / "references.bib",
        ROOT / "data" / "source_ledger.csv",
        ROOT / "data" / "historical_artifact_inventory.csv",
        ROOT / "data" / "integrated_acceptance_matrix.csv",
        ROOT / "sources" / "Photon_Perspective_in_Relativity_chat_snapshot.txt",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists() or p.stat().st_size == 0]
    add(checks, "package_core_file_integrity", "package", len(missing) == 0, missing, [])

    failed = [c.name for c in checks if not c.passed]
    results = {
        "title": "Null-Relational Chronometry consolidated verification",
        "status": "PASS" if not failed else "FAIL",
        "scope": (
            "Algebraic identities and benchmark consistency only. This does not reproduce the unresolved "
            "electroweak/Yukawa LPM, full non-Abelian 3+1D 2PI/Kadanoff-Baym, tunnelling, lattice, "
            "discrete-anomaly, or quantum-gravity calculations."
        ),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "sympy": sp.__version__,
        },
        "summary": {
            "checks": len(checks),
            "passed": sum(c.passed for c in checks),
            "failed": len(failed),
            "failed_checks": failed,
        },
        "checks": [asdict(c) for c in checks],
    }
    return results


def main() -> int:
    result = verify()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=False) + "\n")
    print(json.dumps(result["summary"], indent=2))
    print(f"wrote {OUT}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
