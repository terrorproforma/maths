#!/usr/bin/env python3
"""Phase-1 exact dimension checks for the Geometric Unity reconstruction.

These checks validate arithmetic and standard Clifford-module dimensions only.
They do not prove representation branching, dynamics, chirality, anomaly
cancellation or phenomenological viability.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def dirac_spinor_dimension(even_dimension: int) -> int:
    if even_dimension <= 0 or even_dimension % 2:
        raise ValueError("dimension must be a positive even integer")
    return 2 ** (even_dimension // 2)


def weyl_spinor_dimension(even_dimension: int) -> int:
    return dirac_spinor_dimension(even_dimension) // 2


def gamma_traceless_vector_spinor_dimension(vector_dim: int, spinor_dim: int) -> int:
    """Dimension of the algebraic kernel of gamma contraction, assuming surjectivity."""
    return vector_dim * spinor_dim - spinor_dim


def build_results() -> dict:
    x_dim = 4
    metric_fibre_dim = x_dim * (x_dim + 1) // 2
    y_dim = x_dim + metric_fibre_dim

    spin77_dirac = dirac_spinor_dimension(14)
    spin77_weyl = weyl_spinor_dimension(14)
    spin64_dirac = dirac_spinor_dimension(10)
    spin64_weyl = weyl_spinor_dimension(10)
    spin13_weyl = weyl_spinor_dimension(4)

    internal_rs_144 = gamma_traceless_vector_spinor_dimension(10, spin64_weyl)
    rs_832 = gamma_traceless_vector_spinor_dimension(14, spin77_weyl)

    f_half = 2 * spin64_weyl + 2 * spin64_weyl
    q_three_halves = 6 * spin64_weyl + 6 * spin64_weyl
    z_half = 2 * internal_rs_144 + 2 * internal_rs_144
    decomposition_total = f_half + q_three_halves + z_half

    pati_salam_family = 4 * 2 + 4 * 2

    values = {
        "X_dimension": x_dim,
        "metric_fibre_dimension": metric_fibre_dim,
        "Y_dimension": y_dim,
        "chimeric_rank": y_dim,
        "dim_so_7_7": 14 * 13 // 2,
        "dim_u_64_64_real_lie_algebra": (64 + 64) ** 2,
        "spin_7_7_Dirac_complex_dimension": spin77_dirac,
        "spin_7_7_Weyl_complex_dimension": spin77_weyl,
        "spin_6_4_Dirac_complex_dimension": spin64_dirac,
        "spin_6_4_Weyl_complex_dimension": spin64_weyl,
        "spin_1_3_Weyl_complex_dimension": spin13_weyl,
        "spin_6_4_gamma_traceless_vector_spinor_dimension": internal_rs_144,
        "spin_7_7_chiral_gamma_traceless_vector_spinor_dimension": rs_832,
        "F_half_dimension": f_half,
        "Q_three_halves_dimension": q_three_halves,
        "Z_half_dimension": z_half,
        "F_plus_Q_plus_Z": decomposition_total,
        "Pati_Salam_one_family_dimension": pati_salam_family,
    }

    checks = {
        "metric_bundle_dimension_4_plus_10_equals_14": y_dim == 14,
        "chimeric_rank_matches_Y_dimension": y_dim == 14,
        "Spin77_Dirac_dimension_is_128": spin77_dirac == 128,
        "Spin77_Weyl_dimension_is_64": spin77_weyl == 64,
        "Spin64_Weyl_dimension_is_16": spin64_weyl == 16,
        "internal_gamma_traceless_vector_spinor_is_144": internal_rs_144 == 144,
        "Spin77_chiral_gamma_traceless_vector_spinor_is_832": rs_832 == 832,
        "source_F_dimension_is_64": f_half == 64,
        "source_Q_dimension_is_192": q_three_halves == 192,
        "source_Z_dimension_is_576": z_half == 576,
        "source_decomposition_sums_to_832": decomposition_total == rs_832,
        "Pati_Salam_family_dimension_is_16": pati_salam_family == 16,
    }

    return {
        "schema_version": "1.0.0",
        "project": "TP-02 independent Geometric Unity reconstruction",
        "phase": "primary-source dimension audit",
        "values": values,
        "checks": checks,
        "all_pass": all(checks.values()),
        "scope_warning": (
            "Passing these identities verifies only standard dimension bookkeeping. "
            "It is not evidence that the stated representation branching, field equations, "
            "chirality mechanism or phenomenology is correct."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    result = build_results()
    out = root / "results" / "representation_dimension_checks.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
