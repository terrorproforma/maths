"""ANANKE v2: interval-certified Karpelevič & non-asymptotic finite-sample certification."""

from __future__ import annotations

import json
from math import pi
from pathlib import Path

import numpy as np

from ananke import (
    certified_distance_to_karpelevich,
    certified_karpelevich_radius,
    certify_classical_memory_lower_bound,
    certify_eigenmode_single_sample,
    certify_eigenmode_split_sample,
    certify_finite_stochastic_exclusions,
    certify_hankel_rank,
    classical_cycle_process,
    entrywise_frobenius_hankel_bound,
    hankel_matrix_hoeffding_bound,
    qubit_rotation_process,
    simulate_words_upto,
)

ROOT = Path(__file__).resolve().parents[1]
V1_BASELINE_PATH = ROOT / "results" / "noisy_qubit_v1.json"
RESULT_PATH = ROOT / "results" / "certify_baseline_v2.json"


def main() -> None:
    # 1. Interval-certified audit of KLS (2020) benchmark and exact v1 baseline disk
    kls_angle = 7.0 * pi / 12.0
    kls_r5 = certified_karpelevich_radius(5, kls_angle)
    kls_r6 = certified_karpelevich_radius(6, kls_angle)
    kls_z = 0.9 * np.exp(1j * kls_angle)
    kls_d5 = certified_distance_to_karpelevich(kls_z, 5, tol=1e-4, max_subdivisions=600)
    kls_d6 = certified_distance_to_karpelevich(kls_z, 6, tol=1e-4, max_subdivisions=600)

    v1_data = json.loads(V1_BASELINE_PATH.read_text(encoding="utf-8"))
    v1_pt_pair = v1_data["x_eigenmode_bootstrap"]["point_estimate"]
    v1_z = complex(v1_pt_pair[0], v1_pt_pair[1])
    v1_rad = float(v1_data["x_eigenmode_bootstrap"]["confidence_disk_radius"])
    v1_certified = certify_finite_stochastic_exclusions(
        v1_z,
        v1_rad,
        confidence_level=0.99,
        hankel_rank_lower_bound=4,
        maximum_order=18,
        tol=1e-4,
        early_stop=False,
    )

    # 2. Non-asymptotic finite-sample shot scaling on the baseline qubit (alpha = 0.01)
    process = qubit_rotation_process()
    exact_x_mode = complex(np.exp(0.73j))
    shot_budgets = [10_000, 30_000, 100_000, 300_000, 1_000_000, 3_000_000, 10_000_000]
    scaling_rows: list[dict[str, object]] = []

    for idx, shots in enumerate(shot_budgets):
        ds = simulate_words_upto(process, 7, shots, np.random.default_rng(12_345 + idx))
        rank_cert = certify_hankel_rank(ds, 3, 3, alpha=0.01)
        mh_h = hankel_matrix_hoeffding_bound(ds, 3, 3, delta=0.005)
        frob_kl = entrywise_frobenius_hankel_bound(ds, 3, 3, delta=0.005, method="kl")

        single_rep = certify_classical_memory_lower_bound(
            ds,
            max_prefix_length=3,
            max_suffix_length=3,
            retained_rank=4,
            symbol="x",
            alpha=0.01,
            method="single",
            target=exact_x_mode,
            maximum_order=45,
            karpelevich_tol=1e-7,
            early_stop=True,
        )
        split_rep = certify_classical_memory_lower_bound(
            ds,
            max_prefix_length=3,
            max_suffix_length=3,
            retained_rank=4,
            symbol="x",
            alpha=0.01,
            method="split",
            pilot_fraction=0.15,
            rng=np.random.default_rng(9_000 + idx),
            target=exact_x_mode,
            maximum_order=50,
            karpelevich_tol=1e-7,
            early_stop=True,
        )

        s_eig = single_rep.eigenmode
        p_eig = split_rep.eigenmode
        scaling_rows.append(
            {
                "shots_per_word": shots,
                "total_hankel_trials": int(ds.total_trials),
                "unconditional_rank_lower_bound": rank_cert.certified_rank_lower_bound,
                "matrix_hoeffding_h_delta_005": mh_h,
                "entrywise_kl_frobenius_h_delta_005": frob_kl,
                "single_sample": {
                    "certified_isolated": s_eig.certified_isolated,
                    "certified_disk_radius": (
                        s_eig.certified_disk_radius
                        if np.isfinite(s_eig.certified_disk_radius)
                        else None
                    ),
                    "bauer_fike_comparison_radius": s_eig.bauer_fike_comparison_radius,
                    "true_mode_error": float(abs(s_eig.point_estimate - exact_x_mode)),
                    "exact_mode_covered": bool(
                        abs(s_eig.point_estimate - exact_x_mode) <= s_eig.certified_disk_radius
                    ),
                    "certified_classical_state_lower_bound": single_rep.certified_classical_state_lower_bound,
                },
                "split_sample": {
                    "certified_isolated": p_eig.certified_isolated,
                    "certified_disk_radius": (
                        p_eig.certified_disk_radius
                        if np.isfinite(p_eig.certified_disk_radius)
                        else None
                    ),
                    "scalar_linear_bound": p_eig.scalar_linear_bound,
                    "true_mode_error": float(abs(p_eig.point_estimate - exact_x_mode)),
                    "exact_mode_covered": bool(
                        abs(p_eig.point_estimate - exact_x_mode) <= p_eig.certified_disk_radius
                    ),
                    "certified_classical_state_lower_bound": split_rep.certified_classical_state_lower_bound,
                },
            }
        )

    # 3. Empirical coverage & classical 3-cycle boundary calibration (40 independent trials each)
    calibration_trials = 40
    qubit_covered = 0
    for trial in range(calibration_trials):
        ds = simulate_words_upto(process, 7, 100_000, np.random.default_rng(50_000 + trial))
        eig = certify_eigenmode_split_sample(
            ds,
            max_prefix_length=3,
            max_suffix_length=3,
            retained_rank=4,
            symbol="x",
            alpha=0.01,
            pilot_fraction=0.15,
            rng=np.random.default_rng(60_000 + trial),
            target=exact_x_mode,
        )
        if eig.certified_isolated and abs(eig.point_estimate - exact_x_mode) <= eig.certified_disk_radius:
            qubit_covered += 1

    cycle = classical_cycle_process(3, response_probabilities=np.array([0.17, 0.63, 0.89]))
    cycle_mode = complex(np.exp(2j * pi / 3.0))
    cycle_false_exclusions = 0
    for trial in range(calibration_trials):
        ds_c = simulate_words_upto(cycle, 5, 50_000, np.random.default_rng(70_000 + trial))
        rep_c = certify_classical_memory_lower_bound(
            ds_c,
            max_prefix_length=2,
            max_suffix_length=2,
            retained_rank=3,
            symbol="a",
            alpha=0.01,
            method="split",
            pilot_fraction=0.2,
            rng=np.random.default_rng(80_000 + trial),
            target=cycle_mode,
            maximum_order=3,
            karpelevich_tol=1e-6,
            early_stop=True,
        )
        if rep_c.certified_classical_state_lower_bound > 3:
            cycle_false_exclusions += 1

    all_covered = all(
        row["single_sample"]["exact_mode_covered"] and row["split_sample"]["exact_mode_covered"]
        for row in scaling_rows
    )
    row_300k = next(row for row in scaling_rows if row["shots_per_word"] == 300_000)
    row_10m = next(row for row in scaling_rows if row["shots_per_word"] == 10_000_000)

    result = {
        "experiment": "ANANKE v2 certified baseline and finite-sample scaling",
        "kls_2020_benchmark": {
            "angle_radians": kls_angle,
            "theta_5_radius": kls_r5.to_dict(),
            "theta_6_radius": kls_r6.to_dict(),
            "z_0p9_distance_theta_5": kls_d5.to_dict(),
            "z_0p9_distance_theta_6": kls_d6.to_dict(),
        },
        "v1_baseline_disk_interval_audit": {
            "v1_bootstrap_disk_radius": v1_rad,
            "v1_numerical_lower_bound": v1_data["finite_classical_state_exclusion"][
                "numerical_classical_state_lower_bound"
            ],
            "v2_interval_certified_report": v1_certified.to_dict(),
            "v1_n_ge_16_genuinely_certified": bool(
                v1_certified.certified_classical_state_lower_bound == 16
            ),
        },
        "non_asymptotic_shot_scaling": scaling_rows,
        "empirical_calibration": {
            "trials": calibration_trials,
            "nominal_confidence": 0.99,
            "qubit_100k_exact_mode_coverage": f"{qubit_covered}/{calibration_trials}",
            "classical_3cycle_50k_false_exclusions": f"{cycle_false_exclusions}/{calibration_trials}",
        },
        "pass": bool(
            v1_certified.certified_classical_state_lower_bound == 16
            and all_covered
            and row_300k["split_sample"]["certified_classical_state_lower_bound"] >= 16
            and row_10m["split_sample"]["certified_classical_state_lower_bound"] >= 25
            and qubit_covered == calibration_trials
            and cycle_false_exclusions == 0
        ),
    }

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
