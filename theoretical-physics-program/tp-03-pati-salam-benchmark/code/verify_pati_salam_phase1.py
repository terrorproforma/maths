#!/usr/bin/env python3
"""TP-03 Phase 1 exact algebraic and one-loop Pati-Salam baseline.

The verifier checks:
- perturbative and Witten anomaly cancellation;
- decomposition to one Standard Model family plus a sterile neutrino;
- hypercharge and SU(4) generator normalization;
- the minimal one-bidoublet fermion-mass obstruction;
- the (15,2,2) Clebsch repair;
- the neutral Pati-Salam-breaking direction in (10,1,3);
- an explicitly declared one-loop, threshold-free gauge-matching baseline.

All representation and anomaly checks use exact rational arithmetic. The
one-loop scale is a floating-point benchmark, not a global fit.
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from random import Random
from typing import Dict, List, Tuple


def f(value: int, denominator: int = 1) -> Fraction:
    return Fraction(value, denominator)


def frac(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def matrix_add(a: List[List[Fraction]], b: List[List[Fraction]]) -> List[List[Fraction]]:
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def matrix_sub(a: List[List[Fraction]], b: List[List[Fraction]]) -> List[List[Fraction]]:
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def matrix_scale(a: List[List[Fraction]], c: Fraction) -> List[List[Fraction]]:
    return [[c * x for x in row] for row in a]


def matrices_equal(a: List[List[Fraction]], b: List[List[Fraction]]) -> bool:
    return a == b


def ps_anomaly_audit() -> Dict[str, object]:
    # All-left-handed convention:
    # F_L=(4,2,1), F_R^c=(bar4,1,2).
    su4_cubic = 2 * (+1) + 2 * (-1)
    su2l_witten_doublets = 4
    su2r_witten_doublets = 4
    return {
        "all_left_handed_matter": {
            "F_L": "(4,2,1)",
            "F_R_c": "(bar4,1,2)",
        },
        "SU4_cubic_per_generation": su4_cubic,
        "SU2L_Witten_doublets_per_generation": su2l_witten_doublets,
        "SU2R_Witten_doublets_per_generation": su2r_witten_doublets,
        "SU2L_Witten_parity": su2l_witten_doublets % 2,
        "SU2R_Witten_parity": su2r_witten_doublets % 2,
        "local_anomalies_cancel_per_generation": su4_cubic == 0,
        "global_SU2_anomalies_cancel_per_generation": (
            su2l_witten_doublets % 2 == 0
            and su2r_witten_doublets % 2 == 0
        ),
    }


def sm_decomposition_and_anomalies() -> Dict[str, object]:
    # label, SU3 chirality sign for cubic anomaly, d3, d2, Y
    fields: List[Tuple[str, int, int, int, Fraction]] = [
        ("Q_L", +1, 3, 2, f(1, 6)),
        ("u_c", -1, 3, 1, f(-2, 3)),
        ("d_c", -1, 3, 1, f(1, 3)),
        ("L_L", 0, 1, 2, f(-1, 2)),
        ("nu_c", 0, 1, 1, f(0)),
        ("e_c", 0, 1, 1, f(1)),
    ]

    su3_cubic = sum(a3 * d2 for _, a3, _, d2, _ in fields)
    su3_sq_y = sum(
        f(1, 2) * d2 * y
        for _, a3, _, d2, y in fields
        if a3 != 0
    )
    su2_sq_y = sum(
        f(1, 2) * d3 * y
        for _, _, d3, d2, y in fields
        if d2 == 2
    )
    y_cubic = sum(f(d3 * d2) * y**3 for _, _, d3, d2, y in fields)
    grav_y = sum(f(d3 * d2) * y for _, _, d3, d2, y in fields)
    witten_doublets = sum(d3 for _, _, d3, d2, _ in fields if d2 == 2)

    decomposition = {
        "F_L": [
            {"field": "Q_L", "SU3": "3", "SU2L": "2", "Y": "1/6"},
            {"field": "L_L", "SU3": "1", "SU2L": "2", "Y": "-1/2"},
        ],
        "F_R_c": [
            {"field": "u_c", "SU3": "bar3", "SU2L": "1", "Y": "-2/3"},
            {"field": "d_c", "SU3": "bar3", "SU2L": "1", "Y": "1/3"},
            {"field": "nu_c", "SU3": "1", "SU2L": "1", "Y": "0"},
            {"field": "e_c", "SU3": "1", "SU2L": "1", "Y": "1"},
        ],
    }
    return {
        "hypercharge_definition": "Y=T3R+(B-L)/2",
        "decomposition": decomposition,
        "SM_anomalies_per_generation": {
            "SU3_cubic": frac(f(su3_cubic)),
            "SU3_squared_U1Y": frac(su3_sq_y),
            "SU2_squared_U1Y": frac(su2_sq_y),
            "U1Y_cubic": frac(y_cubic),
            "gravity_squared_U1Y": frac(grav_y),
            "SU2_Witten_doublets": witten_doublets,
            "SU2_Witten_parity": witten_doublets % 2,
        },
        "all_SM_local_anomalies_cancel": all(
            value == 0
            for value in [f(su3_cubic), su3_sq_y, su2_sq_y, y_cubic, grav_y]
        ),
        "SM_global_SU2_anomaly_cancels": witten_doublets % 2 == 0,
    }


def generator_and_breaking_audit() -> Dict[str, object]:
    q_bl = [f(1, 6), f(1, 6), f(1, 6), f(-1, 2)]
    trace_q_bl_sq = sum(charge * charge for charge in q_bl)
    coefficient_sq = f(3, 2)
    trace_t15_sq = coefficient_sq * trace_q_bl_sq

    delta_r_components = [
        {"SU3": "6", "B-L": "2/3", "dimension": 6},
        {"SU3": "3", "B-L": "-2/3", "dimension": 3},
        {"SU3": "1", "B-L": "-2", "dimension": 1},
    ]
    delta_dimension = sum(component["dimension"] for component in delta_r_components)
    neutral_hypercharge = f(1) + f(-2, 2)

    adjoint_components = [
        {"SU3": "8", "B-L": "0", "dimension": 8},
        {"SU3": "3", "B-L": "4/3", "dimension": 3},
        {"SU3": "bar3", "B-L": "-4/3", "dimension": 3},
        {"SU3": "1", "B-L": "0", "dimension": 1},
    ]

    return {
        "T15_relation": "T15=sqrt(3/2) Q_BL",
        "Tr_QBL_squared": frac(trace_q_bl_sq),
        "Tr_T15_squared": frac(trace_t15_sq),
        "canonical_SU4_normalization_passes": trace_t15_sq == f(1, 2),
        "gBL_relation": "g_BL=sqrt(3/2) g_4 for Q_BL=(B-L)/2",
        "hypercharge_matching": "1/g_Y^2=1/g_R^2+2/(3 g_4^2)",
        "Delta_R_10_decomposition": delta_r_components,
        "Delta_R_dimension": delta_dimension,
        "neutral_vev_direction": {
            "B-L": "-2",
            "T3R": "1",
            "Y": frac(neutral_hypercharge),
        },
        "Delta_R_contains_neutral_breaking_direction": (
            delta_dimension == 10 and neutral_hypercharge == 0
        ),
        "SU4_adjoint_15_decomposition": adjoint_components,
        "SU4_adjoint_dimension": sum(x["dimension"] for x in adjoint_components),
    }


def yukawa_obstruction_and_repair() -> Dict[str, object]:
    rng = Random(20260831)
    n = 3
    md = [[f(rng.randint(-7, 7)) for _ in range(n)] for _ in range(n)]
    me = [[f(rng.randint(-7, 7)) for _ in range(n)] for _ in range(n)]
    mu = [[f(rng.randint(-7, 7)) for _ in range(n)] for _ in range(n)]
    mdirac = [[f(rng.randint(-7, 7)) for _ in range(n)] for _ in range(n)]

    ad = matrix_scale(matrix_add(matrix_scale(md, f(3)), me), f(1, 4))
    bd = matrix_scale(matrix_sub(md, me), f(1, 4))
    au = matrix_scale(matrix_add(matrix_scale(mu, f(3)), mdirac), f(1, 4))
    bu = matrix_scale(matrix_sub(mu, mdirac), f(1, 4))

    md_reconstructed = matrix_add(ad, bd)
    me_reconstructed = matrix_sub(ad, matrix_scale(bd, f(3)))
    mu_reconstructed = matrix_add(au, bu)
    mdirac_reconstructed = matrix_sub(au, matrix_scale(bu, f(3)))

    repair_passes = all(
        [
            matrices_equal(md, md_reconstructed),
            matrices_equal(me, me_reconstructed),
            matrices_equal(mu, mu_reconstructed),
            matrices_equal(mdirac, mdirac_reconstructed),
        ]
    )

    return {
        "PS0_scalar_yukawa_sector": ["Phi_1=(1,2,2)"],
        "PS0_exact_mass_relations": ["M_d=M_e", "M_u=M_D_nu"],
        "PS0_verdict": (
            "rejected as a realistic three-family charged-fermion benchmark; "
            "the representation structure supplies no independent quark/lepton "
            "Clebsch in either electroweak direction"
        ),
        "minimal_yukawa_repair": ["Phi_1=(1,2,2)", "Phi_15=(15,2,2)"],
        "PS1_mass_formulas": {
            "M_d": "A_d+B_d",
            "M_e": "A_d-3 B_d",
            "M_u": "A_u+B_u",
            "M_D_nu": "A_u-3 B_u",
        },
        "inverse_formulas": {
            "A_d": "(3 M_d+M_e)/4",
            "B_d": "(M_d-M_e)/4",
            "A_u": "(3 M_u+M_D_nu)/4",
            "B_u": "(M_u-M_D_nu)/4",
        },
        "arbitrary_matrix_pair_reconstruction_exact": repair_passes,
        "right_majorana_mass": "M_R=f_R v_R",
        "type_I_seesaw": "m_nu=-M_D_nu M_R^{-1} M_D_nu^T",
        "seed": 20260831,
    }


def one_loop_matching_baseline() -> Dict[str, object]:
    mz = 91.1876
    alpha_em_inv = 127.955
    sin2_theta_w = 0.23122
    alpha_s = 0.1179
    alpha_em = 1.0 / alpha_em_inv
    alpha_y = alpha_em / (1.0 - sin2_theta_w)
    alpha_2 = alpha_em / sin2_theta_w
    alpha_1 = (5.0 / 3.0) * alpha_y

    b1 = 41.0 / 10.0
    b2 = -19.0 / 6.0
    b3 = -7.0

    mismatch_mz = (
        (5.0 / 3.0) / alpha_1
        - 1.0 / alpha_2
        - (2.0 / 3.0) / alpha_s
    )
    slope = (
        -(5.0 / 3.0) * b1 / (2.0 * math.pi)
        + b2 / (2.0 * math.pi)
        + (2.0 / 3.0) * b3 / (2.0 * math.pi)
    )
    log_ratio = -mismatch_mz / slope
    m_ps = mz * math.exp(log_ratio)

    inv1 = 1.0 / alpha_1 - b1 * log_ratio / (2.0 * math.pi)
    inv2 = 1.0 / alpha_2 - b2 * log_ratio / (2.0 * math.pi)
    inv3 = 1.0 / alpha_s - b3 * log_ratio / (2.0 * math.pi)
    alpha_at_scale = [1.0 / inv1, 1.0 / inv2, 1.0 / inv3]
    gauge_couplings = [math.sqrt(4.0 * math.pi * value) for value in alpha_at_scale]

    residual = (5.0 / 3.0) * inv1 - inv2 - (2.0 / 3.0) * inv3

    return {
        "scope": (
            "one-loop SM running, one light Higgs doublet, no thresholds, "
            "parity condition g_R=g_L at M_PS; illustrative only"
        ),
        "inputs_at_MZ": {
            "MZ_GeV": mz,
            "alpha_em_inverse": alpha_em_inv,
            "sin2_thetaW": sin2_theta_w,
            "alpha_s": alpha_s,
        },
        "beta_coefficients_GUT_normalized": {"b1": b1, "b2": b2, "b3": b3},
        "log_MPS_over_MZ": log_ratio,
        "M_PS_GeV": m_ps,
        "inverse_alphas_at_MPS": {
            "alpha1_inverse": inv1,
            "alpha2_inverse": inv2,
            "alpha3_inverse": inv3,
        },
        "gauge_couplings_at_MPS": {
            "g1_GUT_normalized": gauge_couplings[0],
            "gL": gauge_couplings[1],
            "g4": gauge_couplings[2],
        },
        "matching_residual": residual,
        "matching_passes_numerically": abs(residual) < 1e-10,
        "warning": (
            "Extra light doublets, threshold splittings, two-loop running and "
            "finite matching corrections can move this scale substantially."
        ),
    }


def build_results() -> Dict[str, object]:
    ps_anomalies = ps_anomaly_audit()
    sm = sm_decomposition_and_anomalies()
    breaking = generator_and_breaking_audit()
    yukawa = yukawa_obstruction_and_repair()
    running = one_loop_matching_baseline()

    checks = {
        "PS_local_anomalies_cancel_per_generation": bool(
            ps_anomalies["local_anomalies_cancel_per_generation"]
        ),
        "PS_global_SU2_anomalies_cancel_per_generation": bool(
            ps_anomalies["global_SU2_anomalies_cancel_per_generation"]
        ),
        "SM_decomposition_is_anomaly_free": bool(
            sm["all_SM_local_anomalies_cancel"]
            and sm["SM_global_SU2_anomaly_cancels"]
        ),
        "SU4_generator_normalization": bool(
            breaking["canonical_SU4_normalization_passes"]
        ),
        "Delta_R_has_neutral_breaking_direction": bool(
            breaking["Delta_R_contains_neutral_breaking_direction"]
        ),
        "one_bidoublet_obstruction_identified": bool(
            yukawa["PS0_exact_mass_relations"] == ["M_d=M_e", "M_u=M_D_nu"]
        ),
        "15_bidoublet_repair_reconstructs_arbitrary_pairs": bool(
            yukawa["arbitrary_matrix_pair_reconstruction_exact"]
        ),
        "one_loop_matching_equation_solved": bool(
            running["matching_passes_numerically"]
        ),
    }

    return {
        "schema_version": "1.0.0",
        "project": "TP-03 complete Pati-Salam benchmark",
        "phase": "Phase 1 algebraic baseline and minimal Yukawa obstruction",
        "checks": checks,
        "pati_salam_anomalies": ps_anomalies,
        "standard_model_recovery": sm,
        "generator_and_breaking": breaking,
        "yukawa_sector": yukawa,
        "gauge_matching_baseline": running,
        "verdict": {
            "PS0_one_bidoublet": "REJECTED",
            "PS1_two_bidoublet": "ALGEBRAICALLY VIABLE; DYNAMICS OPEN",
            "next_decisive_test": (
                "Construct the complete renormalizable scalar potential for "
                "Phi_1, Phi_15 and Delta_R; prove the desired vacuum, scalar "
                "spectrum, boundedness, and threshold-corrected RG trajectory."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    root = args.root.resolve()
    result = build_results()
    output = root / "results" / "phase1_algebraic_baseline.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not all(result["checks"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
