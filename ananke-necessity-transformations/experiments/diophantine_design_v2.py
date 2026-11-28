"""ANANKE v2: Diophantine gate design and noble-phase optimality audit."""

from __future__ import annotations

import json
from math import pi
from pathlib import Path

import numpy as np

from ananke import (
    KARPELEVICH_NOBLE_MARKOV_CONSTANT,
    NON_NOBLE_ANALYTIC_UPPER_BOUND,
    asymptotic_karpelevich_radial_gap,
    certified_distance_to_karpelevich,
    certify_classical_memory_lower_bound,
    karpelevich_boundary_radius,
    noble_phase_turns,
    optimize_phase_in_sector,
    periodic_cf_turns,
    periodic_karpelevich_markov_constant,
    qubit_phase_design_metrics,
    qubit_rotation_process,
    simulate_words_upto,
)

ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "diophantine_design_v2.json"


def main() -> None:
    # 1. Karpelevič Markov spectrum across periodic CF tails (Theorem 4 verification)
    periods = [(1,), (1, 1, 2), (2,), (1, 1, 1, 2), (1, 2, 2), (1, 2), (2, 3), (3,), (1, 3)]
    markov_table = [
        {
            "period": list(p),
            "is_noble": all(a == 1 for a in p),
            "karpelevich_markov_constant": periodic_karpelevich_markov_constant(p),
            "ratio_to_noble": periodic_karpelevich_markov_constant(p)
            / KARPELEVICH_NOBLE_MARKOV_CONSTANT,
        }
        for p in periods
    ]

    # 2. Asymptotic radial gap O(N^{-2}) convergence verification for noble [0; 8, 1_bar]
    noble8_turns = noble_phase_turns(8)
    noble8_rad = 2.0 * pi * noble8_turns
    asymptotic_check = []
    for n in (10, 15, 20, 30, 50, 80, 120):
        exact = 1.0 - karpelevich_boundary_radius(n, noble8_rad)
        asymp = asymptotic_karpelevich_radial_gap(n, noble8_turns)
        asymptotic_check.append(
            {
                "order": n,
                "exact_radial_gap": exact,
                "asymptotic_radial_gap": asymp,
                "relative_error": abs(exact - asymp) / exact,
                "n3_times_exact_gap": (n**3) * exact,
            }
        )

    # 3. Finite-horizon sector k=8 counterexample (Refinement A)
    silver8_rad = 2.0 * pi * periodic_cf_turns((8,), (2,))
    alt12_8_rad = 2.0 * pi * periodic_cf_turns((8,), (1, 2))
    opt15_rad, _ = optimize_phase_in_sector(8, 15, grid_points=300)
    opt25_rad, _ = optimize_phase_in_sector(8, 25, grid_points=300)

    sector8_candidates = [
        ("baseline_0.73", 0.73),
        ("noble_[0;8,1_bar]", noble8_rad),
        ("silver_[0;8,2_bar]", silver8_rad),
        ("alt12_[0;8,(1,2)_bar]", alt12_8_rad),
        ("sector8_opt_N15", opt15_rad),
        ("sector8_opt_N25", opt25_rad),
    ]
    finite_horizon_comparison = []
    for label, theta in sector8_candidates:
        z = complex(np.exp(1j * theta))
        d15 = certified_distance_to_karpelevich(z, 15, tol=5e-5, max_subdivisions=500)
        d25 = certified_distance_to_karpelevich(z, 25, tol=2e-5, max_subdivisions=500)
        finite_horizon_comparison.append(
            {
                "label": label,
                "theta_radians": theta,
                "phase_turns": theta / (2.0 * pi),
                "dist_theta_15_lo": d15.distance_lo,
                "dist_theta_15_hi": d15.distance_hi,
                "dist_theta_25_lo": d25.distance_lo,
                "dist_theta_25_hi": d25.distance_hi,
            }
        )

    # 4. Fixed-shot end-to-end certified gate comparison (Refinement B: sector + Hankel conditioning)
    design_candidates = [
        ("baseline_0.73 (k=8)", 0.73),
        ("noble_[0;8,1_bar]", noble8_rad),
        ("silver_[0;8,2_bar]", silver8_rad),
        ("sector8_opt_N15", opt15_rad),
        ("noble_[0;3,1_bar]", 2.0 * pi * noble_phase_turns(3)),
        ("golden_[0;2,1_bar]", 2.0 * pi * noble_phase_turns(2)),
    ]
    fixed_shot_results = []
    for idx, (label, theta) in enumerate(design_candidates):
        metrics = qubit_phase_design_metrics(
            theta, label=label, target_order=15, shots_per_word=300_000, alpha=0.01
        )
        proc = qubit_rotation_process(theta_x=theta, theta_z=1.11)
        exact_mode = complex(np.exp(1j * theta))
        budget_runs = {}
        for b_idx, shots in enumerate((100_000, 300_000)):
            ds = simulate_words_upto(proc, 7, shots, np.random.default_rng(30_000 + 100 * idx + b_idx))
            rep = certify_classical_memory_lower_bound(
                ds,
                max_prefix_length=3,
                max_suffix_length=3,
                retained_rank=4,
                symbol="x",
                alpha=0.01,
                method="split",
                pilot_fraction=0.15,
                rng=np.random.default_rng(40_000 + 100 * idx + b_idx),
                target=exact_mode,
                maximum_order=45,
                karpelevich_tol=1e-7,
                early_stop=True,
            )
            budget_runs[str(shots)] = {
                "certified_disk_radius": (
                    rep.eigenmode.certified_disk_radius
                    if np.isfinite(rep.eigenmode.certified_disk_radius)
                    else None
                ),
                "true_mode_error": float(abs(rep.eigenmode.point_estimate - exact_mode)),
                "exact_mode_covered": bool(
                    abs(rep.eigenmode.point_estimate - exact_mode)
                    <= rep.eigenmode.certified_disk_radius
                ),
                "certified_classical_state_lower_bound": rep.certified_classical_state_lower_bound,
            }
        fixed_shot_results.append(
            {
                "design_metrics_N15": metrics.to_dict(),
                "end_to_end_certified_runs": budget_runs,
            }
        )

    # Check key assertions
    d15_by_label = {row["label"]: row["dist_theta_15_lo"] for row in finite_horizon_comparison}
    d25_by_label = {row["label"]: row["dist_theta_25_lo"] for row in finite_horizon_comparison}
    golden_row = next(r for r in fixed_shot_results if "golden" in r["design_metrics_N15"]["label"])
    noble8_row = next(r for r in fixed_shot_results if "noble_[0;8" in r["design_metrics_N15"]["label"])

    result = {
        "experiment": "ANANKE v2 Diophantine gate design and noble-phase optimality audit",
        "theorem_4_markov_constants": {
            "exact_noble_constant": KARPELEVICH_NOBLE_MARKOV_CONSTANT,
            "analytic_non_noble_upper_bound": NON_NOBLE_ANALYTIC_UPPER_BOUND,
            "algebraic_gap_proof": "3/4 < 2*phi^3/(5*sqrt(5)) <=> 7*sqrt(5) < 16 <=> 245 < 256",
            "periodic_cf_table": markov_table,
        },
        "asymptotic_radial_gap_verification": asymptotic_check,
        "refinement_a_finite_horizon_sector8": finite_horizon_comparison,
        "refinement_b_fixed_shot_gate_comparison": fixed_shot_results,
        "verdict_on_v1_conjecture": (
            "REFINED AND PARTIALLY PROVED: (1) PROVED asymptotically: noble tails "
            "[0; k, overline{1}] strictly maximize the Karpelevič Markov constant "
            "liminf_{N->inf} N^3 dist(e^{2*pi*i*alpha}, Theta_N) = 2*pi^2*phi^3/(5*sqrt(5)) ~= 7.4789 "
            "over ALL irrationals (non-noble <= 3*pi^2/4 ~= 7.4022). "
            "(2) COUNTEREXAMPLE at fixed finite N: interior Farey-arc asymmetry places the "
            "gap maximum at t < 1/2 while noble sits at t > 0.64, so non-noble phases beat "
            "noble at fixed finite orders (e.g., silver beats noble at N=15; [0;8,(1,2)_bar] beats "
            "noble at N=25). "
            "(3) CROSS-SECTOR CONDITIONING: larger-angle noble phases such as golden [0;2,1_bar] "
            "and [0;3,1_bar] dramatically outperform sector k=8 under fixed shot budgets because "
            "Hankel sigma_4 nearly doubles and scalar sensitivity drops sharply."
        ),
        "pass": bool(
            NON_NOBLE_ANALYTIC_UPPER_BOUND < KARPELEVICH_NOBLE_MARKOV_CONSTANT
            and d15_by_label["silver_[0;8,2_bar]"] > d15_by_label["noble_[0;8,1_bar]"]
            and d25_by_label["alt12_[0;8,(1,2)_bar]"] > d25_by_label["noble_[0;8,1_bar]"]
            and golden_row["design_metrics_N15"]["sigma_4"]
            > 1.7 * noble8_row["design_metrics_N15"]["sigma_4"]
            and all(
                run["exact_mode_covered"]
                for r in fixed_shot_results
                for run in r["end_to_end_certified_runs"].values()
            )
        ),
    }

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
