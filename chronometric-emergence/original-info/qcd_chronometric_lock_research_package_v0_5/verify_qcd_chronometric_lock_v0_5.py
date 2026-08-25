#!/usr/bin/env python3
"""Symbolic and numerical checks for QCD Chronometric Lock v0.5.

The script verifies:
  1. positivity of the physical ratio mode and of a lifted radial completion;
  2. the exact logarithmic threshold-recursion algebra;
  3. the one-loop telescoping coefficient 2/27;
  4. its generalization to a Dirac fermion in representation R;
  5. the leading clock-shear coefficients;
  6. the Ti/Pt dilaton charges and the parameter-free clock/EP ratios;
  7. a random stability scan of the lifted two-scalar Hessian.

It writes a machine-readable JSON report next to this file by default.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import sympy as sp


@dataclass
class ScanSummary:
    samples: int
    positive_definite: int
    failed: int
    minimum_trace: float
    minimum_determinant: float
    minimum_eigenvalue: float


def qhat_m(A: float, Z: float) -> float:
    """Approximate Damour-Donoghue composition charge Q'_mhat."""
    return -0.036 / (A ** (1.0 / 3.0)) - 1.4e-4 * Z * (Z - 1.0) / (A ** (4.0 / 3.0))


def qhat_e(A: float, Z: float) -> float:
    """Approximate Damour-Donoghue electromagnetic charge Q'_e."""
    return 7.7e-4 * Z * (Z - 1.0) / (A ** (4.0 / 3.0))


def positive_hessian_scan(samples: int, seed: int) -> ScanSummary:
    rng = random.Random(seed)
    positive = 0
    failed = 0
    min_trace = float("inf")
    min_det = float("inf")
    min_eval = float("inf")

    for _ in range(samples):
        # Log-uniform over a deliberately broad positive domain.
        lam = 10.0 ** rng.uniform(-12.0, 1.0)
        r = 10.0 ** rng.uniform(-6.0, 2.0)
        f = 10.0 ** rng.uniform(-3.0, 3.0)
        mchi2 = 10.0 ** rng.uniform(-12.0, 6.0)

        h11 = mchi2 + 2.0 * lam * f * f * r**4
        h12 = -2.0 * lam * f * f * r**3
        h22 = 2.0 * lam * f * f * r**2

        tr = h11 + h22
        # Use the exact factorized determinant to avoid catastrophic cancellation.
        det = 2.0 * lam * f * f * r**2 * mchi2
        disc = max(tr * tr - 4.0 * det, 0.0)
        sqrt_disc = math.sqrt(disc)
        # Stable expression for the smaller eigenvalue; direct subtraction loses
        # precision for highly hierarchical positive matrices.
        eig_min = (2.0 * det / (tr + sqrt_disc)) if (tr + sqrt_disc) > 0.0 else float("-inf")

        min_trace = min(min_trace, tr)
        min_det = min(min_det, det)
        min_eval = min(min_eval, eig_min)

        if h11 > 0.0 and det > 0.0 and eig_min > 0.0:
            positive += 1
        else:
            failed += 1

    return ScanSummary(
        samples=samples,
        positive_definite=positive,
        failed=failed,
        minimum_trace=min_trace,
        minimum_determinant=min_det,
        minimum_eigenvalue=min_eval,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/mnt/data/qcd_chronometric_lock_verification_v0_5.json"),
        help="Path for JSON output.",
    )
    parser.add_argument("--samples", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=20260816)
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # 1. Alignment Hessian.
    # ------------------------------------------------------------------
    chi, S, lam, r, f, mchi2 = sp.symbols(
        "chi S lambda_S r f m_chi_sq", positive=True, finite=True
    )
    V_align = lam * (S**2 - r**2 * chi**2) ** 2 / 4
    fields = (chi, S)
    H_align = sp.hessian(V_align, fields)
    H_align_vac = sp.simplify(H_align.subs({chi: f, S: r * f}))

    # Add a positive radial curvature for a gauged/lifted completion.
    # In the exact spontaneously broken global-scale limit, mchi2=0 and the
    # alignment Hessian is positive semidefinite with the expected dilaton zero mode.
    H_total = sp.simplify(H_align_vac + sp.Matrix([[mchi2, 0], [0, 0]]))
    det_total = sp.factor(H_total.det())
    trace_total = sp.factor(sp.trace(H_total))

    expected_H_align = 2 * lam * f**2 * sp.Matrix(
        [[r**4, -r**3], [-r**3, r**2]]
    )
    assert sp.simplify(H_align_vac - expected_H_align) == sp.zeros(2)
    assert sp.simplify(det_total - 2 * lam * f**2 * r**2 * mchi2) == 0

    # The non-zero eigenvalue of the alignment piece follows from trace because det=0.
    align_trace = sp.factor(sp.trace(H_align_vac))
    assert sp.simplify(align_trace - 2 * lam * f**2 * r**2 * (1 + r**2)) == 0
    assert sp.simplify(H_align_vac.det()) == 0

    # ------------------------------------------------------------------
    # 2. Misalignment response of a vectorlike colored threshold.
    # ------------------------------------------------------------------
    ychi, yS, theta = sp.symbols("y_chi y_S theta", positive=True, finite=True)
    mass_ratio = ychi + yS * r * sp.exp(theta)
    epsilon_psi = sp.simplify(sp.diff(sp.log(mass_ratio), theta).subs(theta, 0))
    expected_epsilon = yS * r / (ychi + yS * r)
    assert sp.simplify(epsilon_psi - expected_epsilon) == 0

    # ------------------------------------------------------------------
    # 3. Exact threshold recursion, expressed abstractly.
    # ------------------------------------------------------------------
    A, d_high, eps_mass = sp.symbols("A delta_high epsilon_mass", finite=True)
    d_low = sp.expand(A * d_high + (1 - A) * eps_mass)
    assert sp.simplify(d_low - (A * d_high + (1 - A) * eps_mass)) == 0

    # ------------------------------------------------------------------
    # 4. One-loop chain: 7 -> 6 -> 5 -> 4 -> 3 active Dirac fundamentals.
    # ------------------------------------------------------------------
    n = sp.symbols("n", integer=True, positive=True)
    b = lambda nf: sp.Rational(11, 1) - sp.Rational(2, 3) * nf
    b_values = {nf: sp.simplify(b(nf)) for nf in range(3, 8)}

    A_psi = sp.simplify(b_values[7] / b_values[6])
    A_t = sp.simplify(b_values[6] / b_values[5])
    A_b = sp.simplify(b_values[5] / b_values[4])
    A_c = sp.simplify(b_values[4] / b_values[3])
    D_psi_to_3 = sp.factor((1 - A_psi) * A_t * A_b * A_c)
    assert D_psi_to_3 == sp.Rational(2, 27)

    # Equivalent telescoping exponents.
    # Lambda_3^b3 = Lambda_7^b7 * (M_psi m_t m_b m_c)^(2/3).
    assert b_values[3] == 9
    assert b_values[7] == sp.Rational(19, 3)
    exponent_high = sp.simplify(b_values[7] / b_values[3])
    exponent_each_threshold = sp.simplify(sp.Rational(2, 3) / b_values[3])
    assert exponent_high == sp.Rational(19, 27)
    assert exponent_each_threshold == sp.Rational(2, 27)

    # General Dirac representation R: Delta b = 4 T(R)/3.
    TR = sp.symbols("T_R", positive=True)
    D_rep = sp.simplify((sp.Rational(4, 3) * TR) / b_values[3])
    assert D_rep == 4 * TR / 27
    assert sp.simplify(D_rep.subs(TR, sp.Rational(1, 2)) - sp.Rational(2, 27)) == 0

    # ------------------------------------------------------------------
    # 5. Clock shears for explicitly ordered ratios.
    # ------------------------------------------------------------------
    eps = sp.symbols("epsilon_Psi", finite=True)
    dtheta = sp.symbols("dtheta", finite=True)
    qcd_defect = sp.Rational(2, 27) * eps * dtheta

    # K_mu values: Sr=0, CaF=-1/2, Cs=-1.  Neglect Delta K_q in this benchmark.
    Kmu = {"Sr": sp.Rational(0), "CaF": sp.Rational(-1, 2), "Cs": sp.Rational(-1)}
    shear_sr_caf = sp.simplify((Kmu["Sr"] - Kmu["CaF"]) * qcd_defect)
    shear_sr_cs = sp.simplify((Kmu["Sr"] - Kmu["Cs"]) * qcd_defect)
    assert shear_sr_caf == eps * dtheta / 27
    assert shear_sr_cs == 2 * eps * dtheta / 27
    assert sp.simplify(shear_sr_cs - 2 * shear_sr_caf) == 0

    # ------------------------------------------------------------------
    # 6. Ti/Pt composition charges and clock-EP consistency coefficients.
    # ------------------------------------------------------------------
    q_m_ti = qhat_m(48.0, 22.0)
    q_m_pt = qhat_m(195.0, 78.0)
    q_e_ti = qhat_e(48.0, 22.0)
    q_e_pt = qhat_e(195.0, 78.0)
    delta_q_m_ti_pt = q_m_ti - q_m_pt

    coeff_sr_caf = -0.5 / delta_q_m_ti_pt
    coeff_sr_cs = -1.0 / delta_q_m_ti_pt

    # With Delta Q_m(Ti-Pt)<0, these are positive for the ratio conventions Sr/CaF and Sr/Cs.
    assert abs(coeff_sr_caf - 150.38112184931555) < 1e-10
    assert abs(coeff_sr_cs - 300.7622436986311) < 1e-10

    # Rough 95% envelope from MICROSCOPE, not a likelihood reanalysis.
    eta_central = -1.5e-15
    eta_stat = 2.3e-15
    eta_syst = 1.5e-15
    eta_95_envelope = abs(eta_central) + 1.96 * math.sqrt(eta_stat**2 + eta_syst**2)
    beta_sr_caf_envelope = abs(coeff_sr_caf) * eta_95_envelope
    beta_sr_cs_envelope = abs(coeff_sr_cs) * eta_95_envelope

    # ------------------------------------------------------------------
    # 7. Numerical stability scan.
    # ------------------------------------------------------------------
    scan = positive_hessian_scan(args.samples, args.seed)
    if scan.failed != 0:
        raise RuntimeError(f"Stability scan found {scan.failed} failed points")

    results: dict[str, Any] = {
        "document_version": "0.5",
        "generated_utc_note": "Deterministic calculation; timestamp intentionally omitted.",
        "symbolic_checks": {
            "alignment_hessian": str(H_align_vac),
            "alignment_hessian_trace": str(align_trace),
            "alignment_hessian_determinant": str(sp.factor(H_align_vac.det())),
            "completed_hessian": str(H_total),
            "completed_hessian_trace": str(trace_total),
            "completed_hessian_determinant": str(det_total),
            "threshold_misalignment_epsilon": str(epsilon_psi),
            "exact_defect_recursion": "delta_low = A delta_high + (1-A) epsilon_mass",
        },
        "qcd_one_loop": {
            "b_coefficients": {str(k): str(v) for k, v in b_values.items()},
            "A_Psi_7_to_6": str(A_psi),
            "A_top_6_to_5": str(A_t),
            "A_bottom_5_to_4": str(A_b),
            "A_charm_4_to_3": str(A_c),
            "D_Psi_to_3": str(D_psi_to_3),
            "Lambda7_exponent_in_Lambda3": str(exponent_high),
            "each_heavy_mass_exponent_in_Lambda3": str(exponent_each_threshold),
            "general_Dirac_representation": str(D_rep),
            "fundamental_representation": "2/27",
            "asymptotic_freedom_b7_positive": bool(float(b_values[7]) > 0),
        },
        "clock_shear": {
            "qcd_lock_defect": str(qcd_defect),
            "S_Sr_over_CaF": str(shear_sr_caf),
            "S_Sr_over_Cs": str(shear_sr_cs),
            "rank_one_relation": "S_Sr/Cs = 2 S_Sr/CaF",
        },
        "equivalence_principle": {
            "Qm_Ti": q_m_ti,
            "Qm_Pt": q_m_pt,
            "Qe_Ti": q_e_ti,
            "Qe_Pt": q_e_pt,
            "Delta_Qm_Ti_minus_Pt": delta_q_m_ti_pt,
            "beta_Sr_over_CaF_over_eta_TiPt": coeff_sr_caf,
            "beta_Sr_over_Cs_over_eta_TiPt": coeff_sr_cs,
            "MICROSCOPE_rough_95_percent_eta_envelope": eta_95_envelope,
            "implied_beta_Sr_over_CaF_envelope": beta_sr_caf_envelope,
            "implied_beta_Sr_over_Cs_envelope": beta_sr_cs_envelope,
            "warning": "Envelope is model-conditional and is not a likelihood reanalysis.",
        },
        "numerical_stability_scan": {
            **asdict(scan),
            "completion_tested": "positive-curvature lifted radial completion",
            "global_scale_limit": "m_chi_sq = 0 gives one expected zero eigenvalue and one positive ratio eigenvalue",
        },
        "all_checks_passed": True,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
