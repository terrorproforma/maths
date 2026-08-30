"""Validation for solver-neutral HDF5 field snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import h5py
import numpy as np

from .errors import ArtifactError


@dataclass(frozen=True)
class DatasetRequirement:
    path: str
    rank: int | None
    description: str


REQUIRED_DATASETS = (
    DatasetRequirement("/coordinates/x", 1, "Cell-centre x coordinates"),
    DatasetRequirement("/coordinates/y", 1, "Cell-centre y coordinates"),
    DatasetRequirement("/coordinates/z", 1, "Cell-centre z coordinates"),
    DatasetRequirement("/fields/rho", 3, "Rest-mass density"),
    DatasetRequirement("/fields/pressure", 3, "Fluid pressure"),
    DatasetRequirement("/fields/temperature", 3, "Temperature"),
    DatasetRequirement("/fields/ye", 3, "Electron fraction"),
    DatasetRequirement("/fields/b_squared", 3, "Comoving magnetic four-vector norm"),
    DatasetRequirement("/fields/u_t", 3, "Covariant temporal four-velocity component"),
    DatasetRequirement("/fields/sqrt_gamma", 3, "Spatial-metric volume factor"),
    DatasetRequirement("/metric/lapse", 3, "Lapse"),
    DatasetRequirement("/meta/time_s", 0, "Physical time after merger"),
)

REQUIRED_ROOT_ATTRIBUTES = (
    "contract_version",
    "coordinate_system",
    "length_unit",
    "mass_unit",
    "time_unit",
    "solver",
    "campaign_id",
)


def validate_field_snapshot(path: str | Path) -> dict[str, Any]:
    """Validate one HDF5 snapshot and return a compact summary."""

    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise ArtifactError(f"Field snapshot does not exist: {source}")

    missing: list[str] = []
    wrong_rank: list[str] = []
    nonfinite: list[str] = []
    summary: dict[str, Any] = {"path": str(source), "datasets": {}}

    with h5py.File(source, "r") as handle:
        missing_attributes = [name for name in REQUIRED_ROOT_ATTRIBUTES if name not in handle.attrs]
        if missing_attributes:
            missing.extend(f"@{name}" for name in missing_attributes)

        shapes: dict[str, tuple[int, ...]] = {}
        for requirement in REQUIRED_DATASETS:
            if requirement.path not in handle:
                missing.append(requirement.path)
                continue
            dataset = handle[requirement.path]
            if not isinstance(dataset, h5py.Dataset):
                missing.append(requirement.path)
                continue
            shapes[requirement.path] = dataset.shape
            if requirement.rank is not None and dataset.ndim != requirement.rank:
                wrong_rank.append(
                    f"{requirement.path}: expected rank {requirement.rank}, got {dataset.ndim}"
                )
            values = dataset[()]
            if np.issubdtype(np.asarray(values).dtype, np.number) and np.any(~np.isfinite(values)):
                nonfinite.append(requirement.path)
            summary["datasets"][requirement.path] = {
                "shape": list(dataset.shape),
                "dtype": str(dataset.dtype),
            }

        field_shapes = {
            shapes[path]
            for path in (
                "/fields/rho",
                "/fields/pressure",
                "/fields/temperature",
                "/fields/ye",
                "/fields/b_squared",
                "/fields/u_t",
                "/fields/sqrt_gamma",
                "/metric/lapse",
            )
            if path in shapes
        }
        if len(field_shapes) > 1:
            wrong_rank.append(f"three-dimensional field shapes disagree: {sorted(field_shapes)}")

        summary["attributes"] = {
            name: _normalise_attribute(handle.attrs[name])
            for name in REQUIRED_ROOT_ATTRIBUTES
            if name in handle.attrs
        }

    if missing or wrong_rank or nonfinite:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if wrong_rank:
            details.append(f"shape/rank: {'; '.join(wrong_rank)}")
        if nonfinite:
            details.append(f"non-finite datasets: {', '.join(nonfinite)}")
        raise ArtifactError("Invalid field snapshot — " + " | ".join(details))
    return summary


def _normalise_attribute(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value
