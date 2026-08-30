"""Adapter contract for an independently implemented equivalent solver."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base import SolverAdapter


class EquivalentSolverAdapter(SolverAdapter):
    """Emit a strict solver-neutral contract for an E-track implementation."""

    @property
    def name(self) -> str:
        return "independent-equivalent-GRRMHD"

    def validate_campaign(self, campaign: dict[str, Any]) -> list[str]:
        problems: list[str] = []
        if campaign.get("track") != "E":
            problems.append("Independent-equivalent adapter requires track E")
        physical = campaign.get("physical_model", {})
        required_physics = {
            "spacetime": "dynamical_z4c_moving_puncture",
            "fluid": "ideal_grmhd",
            "neutrinos": "gray_m1_plus_source_terms",
        }
        for key, expected in required_physics.items():
            if physical.get(key) != expected:
                problems.append(f"{key} must be {expected!r}")
        if campaign.get("numerics", {}).get("magnetic_divergence_control") != "constrained_transport":
            problems.append("E-track baseline requires constrained transport")
        return problems

    def render_input(self, campaign: dict[str, Any], destination: str | Path) -> list[Path]:
        problems = self.validate_campaign(campaign)
        if problems:
            joined = "\n- ".join(problems)
            raise ValueError(f"Equivalent-solver campaign is not renderable:\n- {joined}")

        target = Path(destination).expanduser().resolve()
        target.mkdir(parents=True, exist_ok=True)
        contract_path = target / "equivalent-solver-contract.json"
        payload = {
            "adapter": self.name,
            "contract_version": 1,
            "campaign_id": campaign["campaign_id"],
            "continuum_system": campaign["physical_model"],
            "required_numerics": campaign["numerics"],
            "mesh": campaign["mesh"],
            "run_control": campaign["run_control"],
            "stages": campaign["stages"],
            "required_output_contract": {
                "format": "project diagnostic CSV/HDF5 contract",
                "documentation": "docs/EQUATIONS_AND_NUMERICS.md",
            },
        }
        contract_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return [contract_path]

    def launch_arguments(
        self,
        campaign: dict[str, Any],
        stage_id: str,
        run_directory: str | Path,
    ) -> list[str]:
        valid_stages = {stage["id"] for stage in campaign["stages"]}
        if stage_id not in valid_stages:
            raise ValueError(f"Unknown campaign stage: {stage_id}")
        run_root = Path(run_directory).expanduser().resolve()
        return [
            "--contract",
            str(run_root / "solver-input" / "equivalent-solver-contract.json"),
            "--stage",
            stage_id,
        ]
