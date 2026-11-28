"""Reproducible ANANKE v3 experiment: rank-unrestricted finite-shot and noiseless certification."""

from __future__ import annotations

import json
from math import pi
from pathlib import Path
import time

import numpy as np

from ananke import (
    certify_noiseless_counterfeit_error_lower_bound,
    certify_rank_unrestricted_fourier_cap,
    certify_rank_unrestricted_split_sample,
    classical_cycle_process,
    qubit_rotation_process,
    ray_words,
    simulate_shot_dataset,
)

RESULTS_PATH = Path(__file__).resolve().parents[1] / "results" / "certify_rank_unrestricted_v3.json"


def run_noiseless_horizon_sweep() -> dict[str, object]:
    """Certify noiseless rank-unrestricted N_min(eps, L) across horizons L."""
    configs = {
        "baseline_mixed_0p73": (
            0.73,
            qubit_rotation_process(theta_x=0.73, theta_z=1.11),
        ),
        "golden_mixed_2p40": (
            2.40,
            qubit_rotation_process(theta_x=2.40, theta_z=1.11),
        ),
        "golden_pure_2p40": (
            2.40,
            qubit_rotation_process(
                theta_x=2.40,
                theta_z=1.11,
                initial_bloch=np.array([0.0, 0.0, 1.0]),
                measurement_axis=np.array([0.0, 0.0, 1.0]),
            ),
        ),
    }
    horizons = [12, 24, 48, 96, 200, 400, 800, 1600]
    epsilons = [0.0, 0.001, 0.005, 0.01]
    out: dict[str, object] = {}

    for name, (theta, proc) in configs.items():
        max_h = max(horizons)
        ray = [proc.behavior("x" * k) for k in range(max_h + 1)]
        rows = []
        for horizon in horizons:
            per_order = []
            lbs_at_eps = {str(e): 2 for e in epsilons}
            # Test orders starting from 2 while feasible (M >= 2 => N <= horizon // 2)
            max_n = min(14, horizon // 2)
            all_excl = {str(e): True for e in epsilons}
            for n in range(2, max_n + 1):
                m = horizon // n
                res = certify_noiseless_counterfeit_error_lower_bound(
                    ray[: horizon + 1], n, theta, boxcar_length=m, tol=2e-3
                )
                per_order.append(
                    {
                        "order": n,
                        "boxcar_M": m,
                        "psi_cert": res.multiplier.psi_upper_bound
                        if np.isfinite(res.multiplier.psi_upper_bound)
                        else None,
                        "mode_a_lb": res.mode_a_error_lower_bound,
                        "mode_b_lb": res.mode_b_error_lower_bound,
                        "best_lb": res.best_error_lower_bound,
                    }
                )
                for e in epsilons:
                    ek = str(e)
                    if all_excl[ek] and res.best_error_lower_bound > e:
                        lbs_at_eps[ek] = n + 1
                    else:
                        all_excl[ek] = False
                if not any(all_excl.values()):
                    break
            rows.append(
                {
                    "horizon_L": horizon,
                    "certified_N_min_at_epsilon": lbs_at_eps,
                    "order_details": per_order,
                }
            )
            print(
                f"  [Noiseless {name}] L={horizon:4d}: "
                + ", ".join(f"eps={e}: N>={lbs_at_eps[str(e)]}" for e in epsilons)
            )
        out[name] = {"theta": theta, "horizons": rows}
    return out


def run_finite_shot_certifications() -> dict[str, object]:
    """Run non-asymptotic Mode A (shot-efficient) and Mode B (short-depth) finite-shot certificates."""
    rng = np.random.default_rng(202603)
    golden_pure = qubit_rotation_process(
        theta_x=2.40,
        theta_z=1.11,
        initial_bloch=np.array([0.0, 0.0, 1.0]),
        measurement_axis=np.array([0.0, 0.0, 1.0]),
    )
    golden_mixed = qubit_rotation_process(theta_x=2.40, theta_z=1.11)
    baseline_mixed = qubit_rotation_process(theta_x=0.73, theta_z=1.11)

    mode_a_runs = []
    mode_a_specs = [
        ("golden_pure_2p40", golden_pure, 2.40, 120, 200, 6),
        ("golden_pure_2p40", golden_pure, 2.40, 400, 200, 7),
        ("golden_pure_2p40", golden_pure, 2.40, 1200, 100, 9),
        ("golden_pure_2p40", golden_pure, 2.40, 4000, 50, 10),
        ("golden_mixed_2p40", golden_mixed, 2.40, 1200, 200, 9),
        ("baseline_mixed_0p73", baseline_mixed, 0.73, 1200, 200, 9),
    ]
    print("\n--- Mode A: Unconditional Fourier-Cap (Single Sample, Ultra-Shot-Efficient, alpha=0.01) ---")
    for label, proc, th, l_max, shots_per_word, max_ord in mode_a_specs:
        words = ray_words("x", l_max)
        ds = simulate_shot_dataset(proc, words, shots_per_word, rng)
        rep = certify_rank_unrestricted_fourier_cap(
            ds,
            symbol="x",
            max_ray_power=l_max,
            theta_radians=th,
            maximum_order=max_ord,
            target_epsilon=0.0,
            alpha=0.01,
        )
        mode_a_runs.append({"process": label, "shots_per_word": shots_per_word, "report": rep.to_dict()})
        print(
            f"  {label:20s} L={l_max:4d}, M_shots={shots_per_word:4d} "
            f"(total={rep.total_shots:7d}): CERTIFIED N >= {rep.certified_classical_state_lower_bound}"
        )

    mode_b_runs = []
    mode_b_specs = [
        ("golden_pure_2p40", golden_pure, 2.40, 20, 50_000, 6),
        ("golden_pure_2p40", golden_pure, 2.40, 60, 50_000, 8),
        ("golden_pure_2p40", golden_pure, 2.40, 160, 100_000, 10),
        ("golden_pure_2p40", golden_pure, 2.40, 320, 200_000, 11),
        ("golden_mixed_2p40", golden_mixed, 2.40, 160, 100_000, 10),
        ("baseline_mixed_0p73", baseline_mixed, 0.73, 160, 100_000, 10),
    ]
    print("\n--- Mode B: Split-Sample Reference-Sinusoid (Short Depth, alpha=0.01) ---")
    for label, proc, th, l_max, shots_per_word, max_ord in mode_b_specs:
        words = ray_words("x", l_max)
        ds = simulate_shot_dataset(proc, words, shots_per_word, rng)
        rep = certify_rank_unrestricted_split_sample(
            ds,
            symbol="x",
            max_ray_power=l_max,
            theta_radians=th,
            maximum_order=max_ord,
            target_epsilon=0.0,
            alpha=0.01,
            rng=np.random.default_rng(int(rng.integers(1, 10**6))),
        )
        # Also compute the certified N_min at epsilon = 0.002 from the SAME tested orders
        lb_eps_2e3 = 1
        for chk in rep.tested_orders:
            if chk.certified_error_lower_bound > 0.002:
                lb_eps_2e3 = chk.order + 1
            else:
                break
        mode_b_runs.append(
            {
                "process": label,
                "shots_per_word": shots_per_word,
                "certified_N_min_at_eps_0p002": lb_eps_2e3,
                "report": rep.to_dict(),
            }
        )
        print(
            f"  {label:20s} L={l_max:4d}, M_shots={shots_per_word:6d} "
            f"(total={rep.total_shots:9d}): CERTIFIED N >= {rep.certified_classical_state_lower_bound} "
            f"(at eps=0.002: N >= {lb_eps_2e3})"
        )

    return {"mode_a_fourier_cap": mode_a_runs, "mode_b_split_sample": mode_b_runs}


def run_empirical_calibration(trials: int = 30) -> dict[str, object]:
    """Verify empirical coverage on exact 3-state classical cycle (0 false exclusions) and golden qubit."""
    rng = np.random.default_rng(777)
    cycle = classical_cycle_process(period=3, damping=0.0, symbol="a")
    th3 = 2.0 * pi / 3.0
    words_c = ray_words("a", 60)

    cycle_false_exclusions_n3 = 0
    cycle_true_exclusions_n2 = 0
    for _ in range(trials):
        ds = simulate_shot_dataset(cycle, words_c, 5_000, rng)
        rep = certify_rank_unrestricted_fourier_cap(
            ds,
            symbol="a",
            max_ray_power=60,
            theta_radians=th3,
            orders=(2, 3),
            alpha=0.01,
            early_stop=False,
        )
        by_n = {c.order: c for c in rep.tested_orders}
        if by_n[2].excluded_exact:
            cycle_true_exclusions_n2 += 1
        if by_n[3].excluded_exact:
            cycle_false_exclusions_n3 += 1

    golden_pure = qubit_rotation_process(
        theta_x=2.40,
        theta_z=1.11,
        initial_bloch=np.array([0.0, 0.0, 1.0]),
        measurement_axis=np.array([0.0, 0.0, 1.0]),
    )
    words_q = ray_words("x", 400)
    qubit_cert_ge_5 = 0
    for _ in range(trials):
        ds = simulate_shot_dataset(golden_pure, words_q, 200, rng)
        rep = certify_rank_unrestricted_fourier_cap(
            ds,
            symbol="x",
            max_ray_power=400,
            theta_radians=2.40,
            orders=(2, 3, 4, 5),
            alpha=0.01,
        )
        if rep.certified_classical_state_lower_bound >= 5:
            qubit_cert_ge_5 += 1

    print(
        f"\n--- Calibration ({trials} trials, alpha=0.01) ---\n"
        f"  3-state cycle: N=2 excluded {cycle_true_exclusions_n2}/{trials}, "
        f"N=3 FALSE exclusions {cycle_false_exclusions_n3}/{trials}\n"
        f"  Golden pure qubit (L=400, 200 shots/word): N>=5 certified {qubit_cert_ge_5}/{trials}"
    )
    return {
        "trials": trials,
        "alpha": 0.01,
        "classical_3_cycle": {
            "true_exclusions_n2": cycle_true_exclusions_n2,
            "false_exclusions_n3": cycle_false_exclusions_n3,
        },
        "golden_pure_qubit_mode_a": {
            "certified_n_ge_5_count": qubit_cert_ge_5,
        },
    }


def main() -> None:
    t0 = time.perf_counter()
    print("=== ANANKE v3: Rank-Unrestricted Certification Experiments ===")
    noiseless = run_noiseless_horizon_sweep()
    finite_shot = run_finite_shot_certifications()
    calibration = run_empirical_calibration(trials=30)
    elapsed = time.perf_counter() - t0

    payload = {
        "experiment": "certify_rank_unrestricted_v3",
        "elapsed_seconds": round(elapsed, 2),
        "noiseless_horizon_sweep": noiseless,
        "finite_shot_certifications": finite_shot,
        "empirical_calibration": calibration,
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nSaved results to {RESULTS_PATH} in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
