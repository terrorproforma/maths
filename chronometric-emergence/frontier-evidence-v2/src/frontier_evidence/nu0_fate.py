"""Prompt-daughter fate in the state-selected fermionic cascade.

The archived cascade assumes that the massless daughter from N0 -> R0 + nu0
thermalises in the visible sector. This module treats the sterile branch as a
separate radiation component, quantifies the resulting dark radiation, and
implements an exact-replica gauge-charged repair.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


MPL_REDUCED_GEV = 2.435e18


@dataclass(frozen=True)
class CascadePoint:
    m_n: float = 3.0e9
    m_r: float = 1.0e9
    gamma_n: float = 0.1
    gamma_r: float = 1.4135e-2
    b5: float = 0.005274370843322566
    g2: float = 0.57
    gstar_high: float = 117.25
    gstar_neutrino_decoupling: float = 10.75


def two_body_fractions(point: CascadePoint) -> tuple[float, float]:
    ratio2 = (point.m_r / point.m_n) ** 2
    daughter = 0.5 * (1.0 - ratio2)
    reheaton = 0.5 * (1.0 + ratio2)
    return daughter, reheaton


def delta_neff_from_decoupled_fraction(
    ratio_to_visible_at_high_t: float,
    gstar_high: float,
    gstar_at_neutrino_decoupling: float = 10.75,
) -> float:
    dilution = (gstar_at_neutrino_decoupling / gstar_high) ** (1.0 / 3.0)
    ratio_at_decoupling = ratio_to_visible_at_high_t * dilution
    one_neutrino_fraction = (7.0 / 4.0) / gstar_at_neutrino_decoupling
    return ratio_at_decoupling / one_neutrino_fraction


def required_yukawa(point: CascadePoint) -> float:
    phase = (1.0 - (point.m_r / point.m_n) ** 2) ** 2
    return math.sqrt(point.gamma_n * 32.0 * math.pi / (point.m_n * phase))


def thermalisation_metrics(point: CascadePoint) -> dict[str, float]:
    alpha2 = point.g2**2 / (4.0 * math.pi)
    h_prefactor = math.sqrt(math.pi**2 * point.gstar_high / 90.0)
    t_decay = math.sqrt(point.gamma_n * MPL_REDUCED_GEV / h_prefactor)
    h_decay = h_prefactor * t_decay**2 / MPL_REDUCED_GEV
    gamma_scatter = alpha2**2 * t_decay
    return {
        "alpha2": alpha2,
        "temperature_at_N_decay_GeV": t_decay,
        "H_at_N_decay_GeV": h_decay,
        "conservative_weak_scattering_rate_GeV": gamma_scatter,
        "scattering_over_H": gamma_scatter / h_decay,
        "scattering_over_Gamma_N": gamma_scatter / point.gamma_n,
    }


def cascade_ode(point: CascadePoint, charged_daughter: bool) -> dict[str, float]:
    f_l, f_r = two_body_fractions(point)
    b0 = 1.0 - point.b5
    gn = point.gamma_n / point.gamma_r
    thermal = thermalisation_metrics(point)
    gth = thermal["conservative_weak_scattering_rate_GeV"] / point.gamma_r
    if not charged_daughter:
        gth = 0.0

    h0 = 15.0
    rho_scale = 3.0 * (MPL_REDUCED_GEV * point.gamma_r) ** 2
    y0 = np.array([h0 * h0, 0.0, 0.0, 1.0e-30, 1.0e-30], dtype=float)

    def rhs(_: float, y: np.ndarray) -> np.ndarray:
        rn, rr, rd, r0, r5 = np.maximum(y, 0.0)
        h = math.sqrt(max(rn + rr + rd + r0 + r5, 0.0))
        return np.array(
            [
                -(3.0 * h + gn) * rn,
                -3.0 * h * rr + f_r * gn * rn - rr,
                -4.0 * h * rd + f_l * gn * rn - gth * rd,
                -4.0 * h * r0 + gth * rd + b0 * rr,
                -4.0 * h * r5 + point.b5 * rr,
            ],
            dtype=float,
        )

    sol = solve_ivp(
        rhs,
        (0.0, 500.0),
        y0,
        method="BDF",
        rtol=2.0e-10,
        atol=1.0e-16,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    rn, rr, rd, r0, r5 = np.maximum(sol.y[:, -1], 0.0)
    free_ratio = rd / max(r0, 1.0e-300)
    hidden_ratio = r5 / max(r0, 1.0e-300)
    delta_prompt = delta_neff_from_decoupled_fraction(
        free_ratio, point.gstar_high, point.gstar_neutrino_decoupling
    )
    t_ratio = hidden_ratio ** 0.25
    delta_hidden_copy = 7.403 * t_ratio**4
    return {
        "N_residual": rn,
        "R_residual": rr,
        "prompt_daughter_to_visible": free_ratio,
        "sector5_to_visible": hidden_ratio,
        "T5_over_T0": t_ratio,
        "DeltaNeff_prompt": delta_prompt,
        "DeltaNeff_hidden_copy": delta_hidden_copy,
        "DeltaNeff_total": delta_prompt + delta_hidden_copy,
        "dimensionless_final_energy": float(rn + rr + rd + r0 + r5),
        "rho_scale_GeV4": rho_scale,
        "charged_daughter": charged_daughter,
    }


def run(point: CascadePoint | None = None) -> dict:
    p = point or CascadePoint()
    f_l, f_r = two_body_fractions(p)
    b0 = 1.0 - p.b5
    visible_if_sterile = f_r * b0
    sterile_ratio = f_l / visible_if_sterile
    analytic_delta = delta_neff_from_decoupled_fraction(sterile_ratio, p.gstar_high)

    yukawa = required_yukawa(p)
    thermal = thermalisation_metrics(p)
    loop_mass_sq = yukawa**2 * p.m_n**2 / (16.0 * math.pi**2)
    sterile = cascade_ode(p, charged_daughter=False)
    repaired = cascade_ode(p, charged_daughter=True)

    gates = {
        "sterile_branch_excluded_DeltaNeff_gt_0_1": bool(sterile["DeltaNeff_total"] > 0.1),
        "charged_daughter_thermalises_before_Hubble": bool(thermal["scattering_over_H"] > 1.0e4),
        "charged_daughter_residual_lt_1e_8": bool(repaired["prompt_daughter_to_visible"] < 1.0e-8),
        "repaired_total_DeltaNeff_lt_0_107": bool(repaired["DeltaNeff_total"] < 0.107),
        "portal_loop_correction_small": bool(math.sqrt(loop_mass_sq) / p.m_r < 1.0e-3),
    }

    return {
        "evidence_class": ["INDEPENDENT_RECOMPUTATION", "PREDICTION"],
        "point": asdict(p),
        "two_body_energy_fractions": {"prompt_daughter": f_l, "R": f_r},
        "instantaneous_sterile_ratio_to_visible": sterile_ratio,
        "instantaneous_sterile_DeltaNeff": analytic_delta,
        "sterile_cascade": sterile,
        "repaired_cascade": repaired,
        "repair": {
            "lagrangian": "-y_R sum_k R_k bar(N_k) L_k + h.c.",
            "representation": (
                "N_k is a complete vectorlike SU(2)_k doublet orbit with Y=-1/2; "
                "L_k is the ordinary lepton doublet in replica k."
            ),
            "exact_replica_symmetry": True,
            "required_y_R": yukawa,
            "thermalisation": thermal,
            "one_loop_R_mass_correction_GeV": math.sqrt(loop_mass_sq),
            "linear_isocurvature": (
                "zero for fixed branching and a heavy mixing sector; no light modulus controls y_R"
            ),
        },
        "gates": gates,
        "all_repair_gates_pass": bool(all(gates.values())),
        "scope": (
            "Energy-flow and rate closure for the daughter. A complete finite-temperature "
            "spectral calculation of the new electroweak parent is not included."
        ),
    }


def write_results(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run()
    (output_dir / "nu0_fate_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    result = write_results(args.output_dir)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["all_repair_gates_pass"] else 2)
