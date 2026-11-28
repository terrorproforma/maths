"""Reproducible ANANKE v3 experiment: two-sided upper vs. lower bounds on C_classical(f; eps, W)."""

from __future__ import annotations

import json
from pathlib import Path
import time

import numpy as np

from ananke import (
    build_hankel,
    certify_noiseless_counterfeit_error_lower_bound,
    construct_bloch_polytope_counterfeit,
    construct_karpelevich_unary_counterfeit,
    construct_shift_register_counterfeit,
    fit_static_simplex_box_nmf,
    optimize_unary_classical_counterfeit,
    qubit_rotation_process,
    words_upto,
)

RESULTS_PATH = Path(__file__).resolve().parents[1] / "results" / "counterfeit_upper_vs_lower_v3.json"


def run_unary_two_sided_bracket() -> dict[str, object]:
    """Compare certified lower bounds against Ito, shift-register, and numerical HMM upper bounds."""
    configs = {
        "baseline_mixed_0p73": (
            0.73,
            qubit_rotation_process(theta_x=0.73, theta_z=1.11),
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
    horizons = [7, 15, 30, 60, 120]
    orders = [3, 4, 5, 6, 7, 8]
    out: dict[str, object] = {}

    for name, (theta, proc) in configs.items():
        print(f"\n=== Unary Two-Sided Bracket: {name} (theta={theta}) ===")
        max_h = max(horizons)
        ray = [proc.behavior("x" * k) for k in range(max_h + 1)]
        table = []
        for horizon in horizons:
            sub = ray[: horizon + 1]
            row_entries = []
            for n in orders:
                # Certified lower bound (when M = horizon // n >= 2; else trivially 0)
                if horizon // n >= 2:
                    lb_res = certify_noiseless_counterfeit_error_lower_bound(
                        sub, n, theta, boxcar_length=horizon // n, tol=2e-3
                    )
                    lb_val = lb_res.best_error_lower_bound
                    psi_cert = lb_res.multiplier.psi_upper_bound
                else:
                    lb_val = 0.0
                    psi_cert = None

                # Exact structured upper bound (shift register / Ito Karpelevič / deterministic cycle)
                ito_res = construct_karpelevich_unary_counterfeit(sub, n, theta, symbol="x")

                # Numerical unconstrained arbitrary-rank upper bound (warm-started from Ito)
                opt_res = optimize_unary_classical_counterfeit(
                    sub,
                    n,
                    theta_radians=theta,
                    symbol="x",
                    restarts=6 if horizon <= 60 else 3,
                    maxiter=200,
                    seed=100 * horizon + n,
                )

                assert lb_val <= ito_res.max_error + 1e-8
                assert lb_val <= opt_res.max_error + 1e-8

                row_entries.append(
                    {
                        "order": n,
                        "certified_error_lb": lb_val,
                        "psi_cert": psi_cert if (psi_cert is not None and np.isfinite(psi_cert)) else None,
                        "ito_structured_ub": ito_res.max_error,
                        "ito_construction": ito_res.method,
                        "numerical_hmm_ub": opt_res.max_error,
                    }
                )
            table.append({"horizon_L": horizon, "orders": row_entries})
            summary = "  ".join(
                f"N={e['order']}:[{e['certified_error_lb']:.4f},{e['numerical_hmm_ub']:.4f}]"
                for e in row_entries
            )
            print(f"  L={horizon:3d}: {summary}")

        # Explicitly verify the L=7 shift-register loophole witness
        sr7 = construct_shift_register_counterfeit(ray[:8], symbol="x")
        sr7_err = float(np.max(np.abs(sr7.evaluate_unary_ray("x", 7) - np.array(ray[:8]))))
        out[name] = {
            "theta": theta,
            "shift_register_L7_states": sr7.state_count,
            "shift_register_L7_max_error": sr7_err,
            "bracket_by_horizon": table,
        }
    return out


def run_two_symbol_and_static_nmf() -> dict[str, object]:
    """Compare 2-symbol Bloch-polytope counterfeits on {x,z}^{<=7} vs static simplex-box NMF on H_f."""
    words_l7 = words_upto(("x", "z"), 7)
    configs = {
        "baseline_mixed_0p73": qubit_rotation_process(theta_x=0.73, theta_z=1.11),
        "golden_mixed_2p40": qubit_rotation_process(theta_x=2.40, theta_z=1.11),
        "golden_pure_2p40": qubit_rotation_process(
            theta_x=2.40,
            theta_z=1.11,
            initial_bloch=np.array([0.0, 0.0, 1.0]),
            measurement_axis=np.array([0.0, 0.0, 1.0]),
        ),
    }
    poly_orders = [4, 6, 8, 12, 16, 20, 32, 64, 128]
    nmf_orders = [4, 5, 6, 7, 8]
    out: dict[str, object] = {}

    for name, proc in configs.items():
        print(f"\n=== Two-Symbol Bloch Polytopes & Static NMF: {name} ===")
        poly_rows = []
        for n in poly_orders:
            res = construct_bloch_polytope_counterfeit(proc, n, words_l7)
            poly_rows.append(res.to_dict())
            print(
                f"  Polytope N={n:3d}: rho_in={res.inradius_rho:.4f}, "
                f"max_err(L=7)={res.max_error:.4f}, rms={res.rms_error:.4f}"
            )

        h_mat = build_hankel(proc.behavior, ("x", "z"), 3, 3).matrix
        nmf_rows = []
        for n in nmf_orders:
            mx, fro = fit_static_simplex_box_nmf(h_mat, n, restarts=8, iterations=180, seed=50 + n)
            nmf_rows.append({"order": n, "static_max_error": mx, "static_fro_error": fro})
        print(
            "  Static 15x15 NMF: "
            + "  ".join(f"N={r['order']}:{r['static_max_error']:.5f}" for r in nmf_rows)
        )
        out[name] = {
            "word_count_L7": len(words_l7),
            "bloch_polytope_counterfeits": poly_rows,
            "static_15x15_simplex_box_nmf": nmf_rows,
        }
    return out


def main() -> None:
    t0 = time.perf_counter()
    print("=== ANANKE v3: Constructive Counterfeits vs. Certified Lower Bounds ===")
    unary = run_unary_two_sided_bracket()
    two_sym = run_two_symbol_and_static_nmf()
    elapsed = time.perf_counter() - t0

    payload = {
        "experiment": "counterfeit_upper_vs_lower_v3",
        "elapsed_seconds": round(elapsed, 2),
        "unary_two_sided_bracket": unary,
        "two_symbol_and_static_nmf": two_sym,
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nSaved results to {RESULTS_PATH} in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
