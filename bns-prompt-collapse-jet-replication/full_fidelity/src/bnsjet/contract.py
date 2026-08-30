"""Solver-neutral output contract for cross-code diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .errors import ArtifactError


@dataclass(frozen=True)
class RequiredOutput:
    relative_path: str
    description: str
    blocking: bool = True


REQUIRED_OUTPUTS = (
    RequiredOutput("diagnostics/horizon.csv", "Apparent-horizon mass, spin, area and fluxes"),
    RequiredOutput("diagnostics/conservation.csv", "Mass, energy, lepton and floor budgets"),
    RequiredOutput("diagnostics/disk.csv", "Disk mass, accretion and thermodynamic diagnostics"),
    RequiredOutput("diagnostics/neutrinos.csv", "Species-separated luminosity/source diagnostics"),
    RequiredOutput("diagnostics/ejecta.csv", "Unbound mass, velocity and composition diagnostics"),
    RequiredOutput("diagnostics/jet.csv", "Polar flux, magnetisation and opening-angle diagnostics"),
    RequiredOutput("diagnostics/constraints.csv", "Einstein and magnetic-divergence constraints"),
    RequiredOutput("RUN_STATE.json", "Campaign lineage and stage state"),
    RequiredOutput("snapshot/PROVENANCE.json", "Frozen software and artifact provenance"),
)


def check_output_contract(run_directory: str | Path) -> list[str]:
    """Return missing blocking output paths."""

    root = Path(run_directory).expanduser().resolve()
    if not root.is_dir():
        raise ArtifactError(f"Run directory does not exist: {root}")
    return [
        output.relative_path
        for output in REQUIRED_OUTPUTS
        if output.blocking and not (root / output.relative_path).is_file()
    ]
