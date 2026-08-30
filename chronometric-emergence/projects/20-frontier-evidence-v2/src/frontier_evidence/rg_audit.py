"""Audit the v1.3 matching-scale cancellation without laundering it as RG proof."""
from __future__ import annotations

import json
from pathlib import Path
import sympy as sp


def run() -> dict:
    x, z = sp.symbols("x z", positive=True)
    t = sp.symbols("t", real=True)
    log_x = sp.log(x) - t
    log_gap = sp.log(x - z) - t
    L = sp.log(x / z)
    fixed = 2 * L * log_gap - log_x**2 - 2 * sp.polylog(2, z / x) + sp.pi**2 / 3
    imposed = -2 * L * log_x + log_x**2
    completed = sp.simplify(fixed + imposed)
    d_fixed = sp.simplify(sp.diff(fixed, t))
    d_imposed = sp.simplify(sp.diff(imposed, t))
    d_completed = sp.simplify(sp.diff(completed, t))
    expected_completed = sp.simplify(
        2 * L * sp.log(1 - z / x) - 2 * sp.polylog(2, z / x) + sp.pi**2 / 3
    )
    algebraic_match = sp.simplify(completed - expected_completed) == 0
    cancellation = d_completed == 0

    return {
        "evidence_class": "IDENTITY_PIN",
        "fixed_order_scale_derivative": str(d_fixed),
        "added_term_scale_derivative": str(d_imposed),
        "sum_scale_derivative": str(d_completed),
        "completed_expression": str(completed),
        "algebraic_match": bool(algebraic_match),
        "cancellation_is_exact": bool(cancellation),
        "scientific_verdict": "RETRACTED",
        "reason": (
            "The finite addition was selected so its derivative cancels the fixed-order derivative. "
            "No operator anomalous-dimension matrix, threshold evolution, or counterterm derivation "
            "produces this term in the archived calculation. The natural-scale hard matching value "
            "may be retained, but the claimed RG completion is not established."
        ),
        "required_for_reinstatement": [
            "declare a complete renormalised transient-operator basis",
            "derive its anomalous-dimension matrix from UV divergences",
            "match at m_R and M with independent finite parts",
            "run to the low scale and demonstrate scale cancellation without defining it",
        ],
    }


def write_results(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run()
    (output_dir / "rg_audit_results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    result = write_results(args.output_dir)
    print(json.dumps(result, indent=2))
