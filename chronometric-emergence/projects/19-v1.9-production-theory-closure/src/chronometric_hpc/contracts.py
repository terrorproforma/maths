from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml


def load_contract(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("observable contract must be a mapping")
    return data


def validate_contract(path: str | Path) -> dict[str, Any]:
    c = load_contract(path)
    primary = c.get("primary_observables", {})
    required = {"complex_poles", "portal_reaction_rate", "HdagH_spectral_density", "sector_energy_and_charges", "temperature_ratio_T5_T0"}
    missing = sorted(required.difference(primary))
    error_terms = c.get("error_budget", {})
    required_error = {"radial_grid", "angular_lmax", "time_step_Tdt", "memory_steps", "quantum_gauge_xi", "factorization_qstar_over_T", "truncation_proxy"}
    missing_error = sorted(required_error.difference(error_terms))
    return {
        "missing_primary_observables": missing,
        "missing_error_components": missing_error,
        "all_pass": not missing and not missing_error,
    }
