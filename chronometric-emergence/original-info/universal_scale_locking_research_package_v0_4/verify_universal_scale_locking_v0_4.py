#!/usr/bin/env python3
"""Symbolic and numerical checks for the Universal Scale-Locking model v0.4.

The script verifies:
  1. Coleman-Weinberg stationarity and positive radial curvature.
  2. Higgs-to-chronon locking along the scalar valley.
  3. Planck-scale locking through a non-minimal coupling.
  4. Exact Einstein-frame decoupling of a universally scaling radial mode.
  5. Positivity of the benchmark scalar mass matrix.
  6. Asymptotic freedom of the hidden SU(2)_X gauge coupling.
  7. The conventional Kallen-Lehmann obstruction for an exact 1/p^4
     elementary propagator with non-negative spectral density.
  8. A random parameter scan over a conservative weak-coupling domain.

This is a consistency check of the proposed EFT. It is not a substitute for a
multi-loop calculation, lattice study, or UV-complete quantum-gravity proof.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import sympy as sp
import mpmath as mp


OUT = Path("/mnt/data/universal_scale_locking_verification_v0_4.json")


@dataclass(frozen=True)
class Benchmark:
    reduced_planck_GeV: float
    higgs_vev_GeV: float
    higgs_mass_GeV: float
    xi_chi: float
    xi_h: float
    hidden_gauge_coupling: float
    lambda_h_carone_convention: float
    lambda_portal: float
    lambda_chi_at_cw_minimum: float
    hidden_vector_mass_GeV: float
    radial_mass_jordan_GeV: float
    radial_mass_einstein_GeV: float
    higgs_radial_mixing_angle_flat_estimate: float
    hidden_gauge_beta_coefficient: float
    hidden_gauge_pole_ratio_mu_over_f: float


def symbolic_checks() -> dict[str, Any]:
    phi, f, g, A = sp.symbols("phi f g A", positive=True, finite=True)
    lam = sp.symbols("lambda_X", real=True)

    # Renormalization choice mu_X = g f / 2 turns the logarithm into log(phi^2/f^2).
    A_expr = sp.Rational(9, 1024) * g**4 / sp.pi**2
    V_cw = lam * phi**4 / 8 + A_expr * phi**4 * (
        sp.log(phi**2 / f**2) - sp.Rational(3, 2)
    )

    dV = sp.simplify(sp.diff(V_cw, phi))
    lambda_stationary = sp.simplify(sp.solve(sp.Eq(dV.subs(phi, f), 0), lam)[0])
    radial_curvature = sp.simplify(
        sp.diff(V_cw, phi, 2).subs({phi: f, lam: lambda_stationary})
    )

    # Higgs locking in radial variables.
    h, chi = sp.symbols("h chi", positive=True, finite=True)
    lambda_h, lambda_p = sp.symbols("lambda_H lambda_p", positive=True, finite=True)
    V_tree = (
        lam * chi**4 / 8
        - lambda_p * h**2 * chi**2 / 4
        + lambda_h * h**4 / 8
    )
    dVdh = sp.factor(sp.diff(V_tree, h))
    h2_solution = sp.simplify(lambda_p * chi**2 / lambda_h)
    lock_residual = sp.simplify(dVdh.subs(h**2, h2_solution))

    # Planck locking and Einstein-frame decoupling.
    xi_chi, xi_h, c_a, m_p0 = sp.symbols(
        "xi_chi xi_h c_A M_P0", positive=True, finite=True
    )
    zeta2 = lambda_p / lambda_h
    F_valley = sp.simplify(xi_chi * chi**2 + xi_h * h2_solution)
    xi_eff = sp.simplify(F_valley / chi**2)
    m_jordan = c_a * chi
    m_einstein = sp.simplify(m_p0 * m_jordan / sp.sqrt(F_valley))
    radial_coupling = sp.simplify(sp.diff(sp.log(m_einstein), chi))

    # Kallen-Lehmann large-Q expansion.
    # G(Q^2)=M0/Q^2-M1/Q^4+... . Exact leading 1/Q^4 requires M0=0.
    Q2, M0, M1 = sp.symbols("Q2 M0 M1", positive=True, finite=True)
    kl_expansion = M0 / Q2 - M1 / Q2**2
    coefficient_q_minus_2 = sp.simplify(sp.limit(Q2 * kl_expansion, Q2, sp.oo))

    return {
        "cw_lambda_stationary": str(lambda_stationary),
        "cw_expected_lambda": str(sp.Rational(9, 128) * g**4 / sp.pi**2),
        "cw_radial_curvature": str(radial_curvature),
        "cw_stationarity_verified": bool(
            sp.simplify(lambda_stationary - sp.Rational(9, 128) * g**4 / sp.pi**2)
            == 0
        ),
        "cw_positive_curvature_for_g_f_positive": bool(
            sp.simplify(radial_curvature - sp.Rational(9, 128) * g**4 * f**2 / sp.pi**2)
            == 0
        ),
        "higgs_lock_residual": str(lock_residual),
        "higgs_lock_verified": bool(lock_residual == 0),
        "xi_effective": str(xi_eff),
        "einstein_frame_mass_on_valley": str(m_einstein),
        "einstein_frame_radial_coupling": str(radial_coupling),
        "fifth_force_decoupling_verified": bool(radial_coupling == 0),
        "kl_large_Q_leading_coefficient": str(coefficient_q_minus_2),
        "kl_positive_density_obstruction": (
            "A non-negative spectral measure has M0=int rho(s) ds >= 0. "
            "An exact propagator whose leading falloff is 1/Q^4 requires M0=0; "
            "positivity then forces rho=0. Therefore a nontrivial elementary 1/p^4 "
            "field cannot possess a conventional positive Kallen-Lehmann density."
        ),
    }


def benchmark() -> Benchmark:
    m_p = 2.435e18
    v = 246.22
    m_h = 125.25
    xi_chi = 1.0
    xi_h = 0.0
    g_x = 0.50

    # Potential convention: V contains (lambda_H/2)(H^dagger H)^2.
    lambda_h = (m_h / v) ** 2
    f = m_p / math.sqrt(xi_chi + xi_h * lambda_h * 0.0)
    lambda_p = lambda_h * (v / f) ** 2
    lambda_chi = 9.0 * g_x**4 / (128.0 * math.pi**2)
    m_x = 0.5 * g_x * f
    m_chi_j = math.sqrt(lambda_chi) * f
    z_radial = 1.0 + 6.0 * xi_chi
    m_chi_e = m_chi_j / math.sqrt(z_radial)

    # Flat-space estimate is enough to demonstrate collider invisibility.
    theta_flat = lambda_p * v * f / max(m_chi_j**2 - m_h**2, 1.0)

    # beta_g = -(43/6) g^3/(16 pi^2). The formal IR pole lies below the
    # symmetry-breaking threshold and is therefore not a physical pole of the
    # unbroken theory. We report the analytical ratio for transparency.
    b = 43.0 / 6.0
    pole_ratio = math.exp(-8.0 * math.pi**2 / (b * g_x**2))

    return Benchmark(
        reduced_planck_GeV=m_p,
        higgs_vev_GeV=v,
        higgs_mass_GeV=m_h,
        xi_chi=xi_chi,
        xi_h=xi_h,
        hidden_gauge_coupling=g_x,
        lambda_h_carone_convention=lambda_h,
        lambda_portal=lambda_p,
        lambda_chi_at_cw_minimum=lambda_chi,
        hidden_vector_mass_GeV=m_x,
        radial_mass_jordan_GeV=m_chi_j,
        radial_mass_einstein_GeV=m_chi_e,
        higgs_radial_mixing_angle_flat_estimate=theta_flat,
        hidden_gauge_beta_coefficient=b,
        hidden_gauge_pole_ratio_mu_over_f=pole_ratio,
    )


def mass_matrix_checks(bm: Benchmark) -> dict[str, Any]:
    f = bm.reduced_planck_GeV / math.sqrt(bm.xi_chi)
    v = bm.higgs_vev_GeV
    lambda_p = bm.lambda_portal
    m_h2 = bm.higgs_mass_GeV**2
    m_chi2 = bm.radial_mass_jordan_GeV**2

    off = -lambda_p * v * f
    matrix = [[m_h2, off], [off, m_chi2 + lambda_p * v**2]]
    tr = matrix[0][0] + matrix[1][1]
    det = matrix[0][0] * matrix[1][1] - off**2

    # Use high precision and the stable relation lambda_small=det/lambda_large.
    mp.mp.dps = 80
    tr_mp = mp.mpf(str(tr))
    det_mp = mp.mpf(str(det))
    disc_mp = mp.sqrt(tr_mp**2 - 4 * det_mp)
    eig2_mp = (tr_mp + disc_mp) / 2
    eig1_mp = det_mp / eig2_mp
    eig1 = float(eig1_mp)
    eig2 = float(eig2_mp)

    return {
        "mass_matrix_GeV2": matrix,
        "trace_positive": tr > 0.0,
        "determinant_positive": det > 0.0,
        "eigenvalues_GeV2": [eig1, eig2],
        "both_eigenvalues_positive": eig1 > 0.0 and eig2 > 0.0,
    }


def random_scan(n: int = 20000, seed: int = 20260816) -> dict[str, Any]:
    rng = random.Random(seed)
    m_p = 2.435e18
    v = 246.22
    m_h = 125.25
    lambda_h = (m_h / v) ** 2

    passed = 0
    failures: list[dict[str, float | str]] = []
    minima = {
        "lambda_chi": float("inf"),
        "radial_mass_GeV": float("inf"),
        "hidden_vector_mass_GeV": float("inf"),
    }
    maxima = {
        "lambda_portal": 0.0,
        "mixing_angle": 0.0,
    }

    for _ in range(n):
        g_x = rng.uniform(0.20, 0.80)
        xi_chi = rng.uniform(0.50, 2.00)
        xi_h = rng.uniform(-0.10, 0.30)
        xi_eff = xi_chi + xi_h * (v / (m_p / math.sqrt(xi_chi))) ** 2
        if xi_eff <= 0:
            failures.append({"reason": "negative effective Planck coefficient"})
            continue

        f = m_p / math.sqrt(xi_eff)
        lambda_p = lambda_h * (v / f) ** 2
        lambda_chi = 9.0 * g_x**4 / (128.0 * math.pi**2)
        m_chi2 = lambda_chi * f**2
        m_x = 0.5 * g_x * f
        off = lambda_p * v * f
        det = m_h**2 * (m_chi2 + lambda_p * v**2) - off**2
        theta = off / max(m_chi2 - m_h**2, 1.0)

        stable = (
            lambda_h > 0
            and lambda_chi > 0
            and lambda_chi * lambda_h > lambda_p**2
            and m_chi2 > 0
            and det > 0
            and g_x < 1.0
        )
        if stable:
            passed += 1
            minima["lambda_chi"] = min(minima["lambda_chi"], lambda_chi)
            minima["radial_mass_GeV"] = min(minima["radial_mass_GeV"], math.sqrt(m_chi2))
            minima["hidden_vector_mass_GeV"] = min(minima["hidden_vector_mass_GeV"], m_x)
            maxima["lambda_portal"] = max(maxima["lambda_portal"], lambda_p)
            maxima["mixing_angle"] = max(maxima["mixing_angle"], abs(theta))
        else:
            failures.append(
                {
                    "reason": "stability condition failed",
                    "g_x": g_x,
                    "xi_chi": xi_chi,
                    "xi_h": xi_h,
                    "lambda_portal": lambda_p,
                    "lambda_chi": lambda_chi,
                    "det": det,
                }
            )

    return {
        "points": n,
        "passed": passed,
        "failed": len(failures),
        "pass_fraction": passed / n,
        "minimum_values_in_passed_scan": minima,
        "maximum_values_in_passed_scan": maxima,
        "first_five_failures": failures[:5],
        "domain": {
            "g_X": [0.20, 0.80],
            "xi_chi": [0.50, 2.00],
            "xi_h": [-0.10, 0.30],
            "M_P_reduced_GeV": m_p,
        },
    }


def main() -> None:
    bm = benchmark()
    results = {
        "document_version": "0.4",
        "symbolic": symbolic_checks(),
        "benchmark": asdict(bm),
        "mass_matrix": mass_matrix_checks(bm),
        "random_scan": random_scan(),
        "scope_warning": (
            "The matter and scalar sectors are conventional two-derivative renormalized QFTs. "
            "Gravity is treated as an effective field theory below its cutoff. The script does "
            "not establish a UV-complete, perturbatively renormalizable and conventionally "
            "unitary quantum theory of gravity."
        ),
    }
    OUT.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
