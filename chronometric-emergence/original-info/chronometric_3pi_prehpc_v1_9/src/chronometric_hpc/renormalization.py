from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def superficial_degree(n_boson: int = 0, n_ghost: int = 0, n_fermion: int = 0, insertion_dimension: int = 0) -> float:
    """Four-dimensional renormalizable gauge-Yukawa power counting."""
    return 4.0 - insertion_dimension - n_boson - n_ghost - 1.5 * n_fermion


def load_closure_matrix(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("counterterm closure matrix must be a list")
    return data


def required_signature_tokens() -> list[str]:
    return [
        "A_SU3 A_SU3", "A_SU2 A_SU2", "A_U1 A_U1",
        "cbar_SU3 c_SU3", "cbar_SU2 c_SU2", "Hdag H", "Qbar Q", "Dbar D",
        "A_SU3 A_SU3 A_SU3", "A_SU2 A_SU2 A_SU2",
        "A_SU3 cbar_SU3 c_SU3", "A_SU2 cbar_SU2 c_SU2",
        "A_SU3 Qbar Q", "A_SU2 Qbar Q", "A_U1 Qbar Q",
        "A_SU3 Dbar D", "A_U1 Dbar D", "A_SU2 Hdag H", "A_U1 Hdag H",
        "H Qbar D plus h.c.", "A3^4", "W^4", "W^2 Hdag H", "B^2 Hdag H",
        "W B Hdag H", "(Hdag H)^2", "O_H = Hdag H insertion", "O_H O_H",
        "initial alpha_2", "initial alpha_3", "initial alpha_4", "Z6 harmonic p<6",
    ]


def validate_closure(path: str | Path) -> dict[str, Any]:
    rows = load_closure_matrix(path)
    signatures = [str(row["external_signature"]) for row in rows]
    missing = [sig for sig in required_signature_tokens() if sig not in signatures]
    blank_counterterms = [row["external_signature"] for row in rows if not str(row.get("counterterm_parameters", "")).strip()]
    return {
        "row_count": len(rows),
        "missing_required_signatures": missing,
        "blank_counterterm_entries": blank_counterterms,
        "all_pass": not missing and not blank_counterterms,
    }
