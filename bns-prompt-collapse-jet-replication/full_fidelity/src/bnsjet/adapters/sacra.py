"""SACRA-MPI exact-lineage adapter contract.

This module intentionally does not invent a private input-file syntax. It validates
that exact artifacts are present and emits a machine-readable handoff contract for
an authorised SACRA-MPI checkout. Once the exact revision is available, the thin
renderer can be completed against that revision without contaminating generic
campaign logic.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base import SolverAdapter


class SacraMPIAdapter(SolverAdapter):
    @property
    def name(self) -> str:
        return "SACRA-MPI"

    def validate_campaign(self, campaign: dict[str, Any]) -> list[str]:
        problems: list[str] = []
        if campaign.get("track") != "X":
            problems.append("SACRA-MPI exact adapter requires track X")
        required = ("solver_source", "initial_data", "eos_table", "neutrino_tables")
        for name in required:
            declaration = campaign.get("artifacts", {}).get(name, {})
            if not declaration.get("path"):
                problems.append(f"missing exact artifact path: {name}")
            if not declaration.get("sha256"):
                problems.append(f"missing exact artifact digest: {name}")
        return problems

    def render_input(self, campaign: dict[str, Any], destination: str | Path) -> list[Path]:
        problems = self.validate_campaign(campaign)
        if problems:
            joined = "\n- ".join(problems)
            raise ValueError(f"SACRA-MPI campaign is not renderable:\n- {joined}")

        target = Path(destination).expanduser().resolve()
        target.mkdir(parents=True, exist_ok=True)
        contract_path = target / "sacra-mpi-handoff.json"
        payload = {
            "adapter": self.name,
            "contract_version": 1,
            "campaign_id": campaign["campaign_id"],
            "physical_model": campaign["physical_model"],
            "numerics": campaign["numerics"],
            "mesh": campaign["mesh"],
            "run_control": campaign["run_control"],
            "stages": campaign["stages"],
            "artifacts": campaign["artifacts"],
            "instruction": (
                "Translate this frozen contract with the input renderer belonging to the declared "
                "SACRA-MPI revision. Do not infer missing private-key names or defaults."
            ),
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
            "--campaign-contract",
            str(run_root / "solver-input" / "sacra-mpi-handoff.json"),
            "--stage",
            stage_id,
        ]
