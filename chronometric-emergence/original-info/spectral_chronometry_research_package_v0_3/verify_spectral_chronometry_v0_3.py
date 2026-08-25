#!/usr/bin/env python3
"""Symbolic and numerical checks for Spectral Chronometry v0.3.

The script verifies the algebraic claims in the companion research note:

1. Weyl invariance of clock phase and the composite chronometric metric.
2. Common-factor clock spectra imply constant dimensionless frequency ratios.
3. Positivity and spectrum of the Higgs-dilaton vacuum Hessian.
4. Positivity of the Einstein-frame two-scalar field-space metric for F > 0.
5. Null-component decomposition of a massive momentum.
6. Rank bounds for differential clock-drift networks sourced by r scalar fields.
7. Positive-semidefiniteness of the chronometric obstruction tensor.
8. The Higgs-only induced-gravity coupling estimate.

It writes a machine-readable JSON report beside this file.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

OUT = Path("/mnt/data/spectral_chronometry_verification_v0_3.json")


def sympy_zero(expr: sp.Expr) -> bool:
    """Return True when SymPy simplifies an expression exactly to zero."""
    return sp.simplify(expr) == 0


def main() -> None:
    results: dict[str, Any] = {
        "title": "Spectral Chronometry and Higgs-Dilaton Completion v0.3 verification",
        "status": "PASS",
        "checks": {},
    }

    # ------------------------------------------------------------------
    # 1. Weyl invariants
    # ------------------------------------------------------------------
    Omega, omega, ds, chi, chi_star, g = sp.symbols(
        "Omega omega ds chi chi_star g", positive=True, finite=True
    )
    phase_before = omega * ds
    phase_after = (omega / Omega) * (Omega * ds)
    metric_before = (chi / chi_star) ** 2 * g
    metric_after = ((chi / Omega) / chi_star) ** 2 * (Omega**2 * g)

    phase_invariant = sympy_zero(phase_after - phase_before)
    metric_invariant = sympy_zero(metric_after - metric_before)
    results["checks"]["weyl_invariance"] = {
        "pass": phase_invariant and metric_invariant,
        "phase_difference": str(sp.simplify(phase_after - phase_before)),
        "metric_difference": str(sp.simplify(metric_after - metric_before)),
    }

    # ------------------------------------------------------------------
    # 2. Universal clock factorization: omega_A = c_A chi
    # ------------------------------------------------------------------
    cA, cB = sp.symbols("c_A c_B", positive=True, finite=True)
    x = sp.symbols("x", real=True)
    chi_fun = sp.Function("chi")(x)
    omega_A = cA * chi_fun
    omega_B = cB * chi_fun
    ratio_derivative = sp.simplify(sp.diff(sp.log(omega_A / omega_B), x))
    factorization_check = ratio_derivative == 0
    results["checks"]["universal_factorization"] = {
        "pass": factorization_check,
        "d_log_ratio": str(ratio_derivative),
        "interpretation": (
            "A common positive scalar factor cancels from every dimensionless clock ratio."
        ),
    }

    # ------------------------------------------------------------------
    # 3. Higgs-dilaton potential Hessian on h = alpha * chi
    # ------------------------------------------------------------------
    h, X, lam, alpha = sp.symbols("h X lambda alpha", positive=True, finite=True)
    V = lam * (h**2 - alpha**2 * X**2) ** 2 / 4
    vars_ = sp.Matrix([h, X])
    hessian = sp.hessian(V, vars_)
    hessian_valley = sp.simplify(hessian.subs(h, alpha * X))
    expected_hessian = (
        2
        * lam
        * alpha**2
        * X**2
        * sp.Matrix([[1, -alpha], [-alpha, alpha**2]])
    )
    hessian_match = all(
        sympy_zero(hessian_valley[i, j] - expected_hessian[i, j])
        for i in range(2)
        for j in range(2)
    )
    trace_h = sp.factor(sp.trace(hessian_valley))
    det_h = sp.factor(hessian_valley.det())
    expected_nonzero = 2 * lam * alpha**2 * X**2 * (1 + alpha**2)
    spectrum_match = sympy_zero(det_h) and sympy_zero(trace_h - expected_nonzero)
    results["checks"]["higgs_dilaton_hessian"] = {
        "pass": hessian_match and spectrum_match,
        "hessian_on_valley": str(hessian_valley),
        "determinant": str(det_h),
        "trace": str(trace_h),
        "eigenvalues": ["0", str(sp.factor(expected_nonzero))],
        "stability_condition": "lambda > 0, alpha != 0, chi != 0",
    }

    # ------------------------------------------------------------------
    # 4. Einstein-frame field-space metric positivity
    # G = A I + b v v^T, A = M_P^2/F > 0, b = 3 M_P^2/(2F^2) > 0.
    # In two dimensions its eigenvalues are A and A + b |v|^2.
    # ------------------------------------------------------------------
    MP, F, v1, v2 = sp.symbols("M_P F v_1 v_2", positive=True, finite=True)
    A = MP**2 / F
    b = 3 * MP**2 / (2 * F**2)
    vec = sp.Matrix([v1, v2])
    G = sp.simplify(A * sp.eye(2) + b * (vec * vec.T))
    det_G = sp.factor(G.det())
    expected_det_G = sp.factor(A * (A + b * (v1**2 + v2**2)))
    determinant_match = sympy_zero(det_G - expected_det_G)

    rng = np.random.default_rng(20260815)
    min_eigenvalue = math.inf
    for _ in range(10_000):
        MP_n = float(10 ** rng.uniform(-2, 2))
        F_n = float(10 ** rng.uniform(-3, 3))
        v_n = rng.normal(size=2)
        A_n = MP_n**2 / F_n
        b_n = 3 * MP_n**2 / (2 * F_n**2)
        G_n = A_n * np.eye(2) + b_n * np.outer(v_n, v_n)
        eig_min = float(np.linalg.eigvalsh(G_n).min())
        min_eigenvalue = min(min_eigenvalue, eig_min)
    kinetic_positive = determinant_match and min_eigenvalue > 0.0
    results["checks"]["einstein_frame_kinetic_metric"] = {
        "pass": kinetic_positive,
        "symbolic_determinant": str(det_G),
        "expected_determinant": str(expected_det_G),
        "analytic_eigenvalues": [
            "M_P^2/F",
            "M_P^2/F + 3 M_P^2 |grad F|^2/(2 F^2)",
        ],
        "minimum_numeric_eigenvalue_over_10000_samples": min_eigenvalue,
        "domain": "M_P > 0 and F > 0",
    }

    # ------------------------------------------------------------------
    # 5. Null decomposition of massive momentum
    # ------------------------------------------------------------------
    mass, eta = sp.symbols("m eta", positive=True, real=True)
    p_plus = mass * sp.exp(eta) / sp.sqrt(2)
    p_minus = mass * sp.exp(-eta) / sp.sqrt(2)
    product_identity = sp.simplify(2 * p_plus * p_minus - mass**2)
    ratio_identity = sp.simplify(p_plus / p_minus - sp.exp(2 * eta))
    null_decomposition_pass = product_identity == 0 and ratio_identity == 0
    results["checks"]["null_component_decomposition"] = {
        "pass": null_decomposition_pass,
        "2_p_plus_p_minus_minus_m2": str(product_identity),
        "ratio_minus_exp_2eta": str(ratio_identity),
    }

    # ------------------------------------------------------------------
    # 6. Rank of multi-clock drift networks
    # log omega_A = log c_A + log chi + sum_I K_AI theta_I.
    # Pairwise/reference clock ratios remove log chi. The clock x sample matrix
    # has rank at most the number r of independent mismatch fields.
    # ------------------------------------------------------------------
    clock_count = 9
    sample_count = 120
    rank_trials: list[dict[str, Any]] = []
    rank_checks_pass = True
    for r in (1, 2, 3, 4):
        K = rng.normal(size=(clock_count, r))
        theta = rng.normal(size=(r, sample_count))
        # Compare every clock to clock 0, which removes the common scale exactly.
        differential = (K[1:, :] - K[0:1, :]) @ theta
        rank = int(np.linalg.matrix_rank(differential, tol=1e-10))
        expected_max = min(r, clock_count - 1, sample_count)
        rank_ok = rank <= expected_max
        rank_checks_pass &= rank_ok
        rank_trials.append(
            {
                "number_of_mismatch_fields": r,
                "measured_matrix_rank": rank,
                "maximum_allowed_rank": expected_max,
                "pass": rank_ok,
            }
        )
    results["checks"]["clock_network_rank_bound"] = {
        "pass": rank_checks_pass,
        "trials": rank_trials,
        "claim": "rank(differential log-frequency network) <= number of independent nonuniversal scalar fields",
    }

    # ------------------------------------------------------------------
    # 7. Positive-semidefinite chronometric obstruction tensor
    # C = sum_A w_A Sigma_A Sigma_A^T.
    # ------------------------------------------------------------------
    obstruction_pass = True
    worst_obstruction_eigenvalue = math.inf
    for _ in range(5_000):
        dimensions = 4
        species = 7
        weights = rng.random(species)
        weights /= weights.sum()
        B = rng.normal(size=(species, dimensions))
        mean = np.sum(weights[:, None] * B, axis=0)
        Sigma = B - mean[None, :]
        C = np.einsum("a,ai,aj->ij", weights, Sigma, Sigma)
        eig_min = float(np.linalg.eigvalsh(C).min())
        worst_obstruction_eigenvalue = min(worst_obstruction_eigenvalue, eig_min)
        if eig_min < -1e-10:
            obstruction_pass = False
            break
    results["checks"]["chronometric_obstruction_tensor"] = {
        "pass": obstruction_pass,
        "minimum_eigenvalue_over_5000_samples": worst_obstruction_eigenvalue,
        "analytic_form": "C_{mu nu} = sum_A w_A Sigma^A_mu Sigma^A_nu is a Gram/covariance tensor",
    }

    # ------------------------------------------------------------------
    # 8. Higgs-only induced gravity estimate
    # Mbar_P^2 = xi_H v^2.
    # ------------------------------------------------------------------
    reduced_planck_gev = 2.435e18
    higgs_vev_gev = 246.22
    xi_induced = (reduced_planck_gev / higgs_vev_gev) ** 2
    target = 9.78e31
    xi_check = abs(xi_induced / target - 1.0) < 0.02
    results["checks"]["higgs_only_induced_gravity"] = {
        "pass": xi_check,
        "reduced_planck_mass_GeV": reduced_planck_gev,
        "higgs_vev_GeV": higgs_vev_gev,
        "xi_required": xi_induced,
        "order_of_magnitude": "10^32",
        "interpretation": (
            "Using the observed Higgs VEV as the sole source of the reduced Planck mass "
            "requires an enormous nonminimal coupling."
        ),
    }

    # ------------------------------------------------------------------
    # 9. Higgs-only viability logic table (not a numerical theorem)
    # ------------------------------------------------------------------
    results["checks"]["higgs_only_viability_logic"] = {
        "pass": True,
        "ordinary_standard_model": {
            "verdict": "INSUFFICIENT",
            "reason": "The Higgs sets electroweak masses but does not by itself set the Planck scale or guarantee that QCD and all spectral standards share one local factor.",
        },
        "higgs_as_sole_local_weyl_compensator": {
            "verdict": "PHENOMENOLOGICALLY_DISFAVORED_IN_MINIMAL_FORM",
            "reason": "After three electroweak Goldstones are eaten, the remaining radial Higgs degree is also used to fix local scale; the minimal construction therefore lacks the observed physical radial Higgs excitation.",
        },
        "higgs_locked_to_deeper_scale_field": {
            "verdict": "VIABLE_EFT_DIRECTION",
            "reason": "A separate radial scale field can normalize gravity and all mass sectors while an angular Higgs-like excitation remains physical.",
        },
    }

    # Aggregate status.
    failed = [
        name for name, payload in results["checks"].items() if not bool(payload.get("pass"))
    ]
    results["failed_checks"] = failed
    results["status"] = "PASS" if not failed else "FAIL"

    OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
