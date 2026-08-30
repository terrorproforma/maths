"""Transparent resource estimates anchored to the published campaign."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .errors import ConfigurationError


@dataclass(frozen=True)
class ResolutionEstimate:
    spacing_m: float
    cpu_hours: float
    allocated_cores: int
    ideal_wall_hours: float
    resolution_ratio_to_reference: float

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def estimate_resolution_costs(campaign: dict[str, Any]) -> list[ResolutionEstimate]:
    """Estimate CPU and ideal wall hours for each production resolution.

    The scaling law is

        C(h) = C_ref * (h_ref / h)**p,

    where *p* is explicit in the campaign file. This is a planning anchor, not a
    performance claim; real production sizing requires representative scaling runs.
    """

    mesh = campaign["mesh"]
    anchor = campaign["resource_anchor"]
    scheduler = campaign["scheduler"]

    reference_cost = float(anchor["reference_cpu_hours"])
    reference_spacing = float(anchor["reference_finest_spacing_m"])
    exponent = float(anchor["resolution_scaling_exponent"])
    nodes = int(scheduler["nodes"])
    ranks_per_node = int(scheduler["ranks_per_node"])
    threads_per_rank = int(scheduler["threads_per_rank"])
    allocated_cores = nodes * ranks_per_node * threads_per_rank
    if allocated_cores <= 0:
        raise ConfigurationError("Allocated core count must be positive")

    estimates: list[ResolutionEstimate] = []
    for raw_spacing in mesh["production_resolutions_m"]:
        spacing = float(raw_spacing)
        if spacing <= 0:
            raise ConfigurationError("Every production spacing must be positive")
        ratio = reference_spacing / spacing
        cpu_hours = reference_cost * ratio**exponent
        estimates.append(
            ResolutionEstimate(
                spacing_m=spacing,
                cpu_hours=cpu_hours,
                allocated_cores=allocated_cores,
                ideal_wall_hours=cpu_hours / allocated_cores,
                resolution_ratio_to_reference=ratio,
            )
        )
    return estimates


def stage_duration_fractions(campaign: dict[str, Any]) -> dict[str, float]:
    """Allocate post-merger duration fractions to stages with finite starts."""

    intervals: list[tuple[str, float]] = []
    for stage in campaign["stages"]:
        start = stage["start_s"]
        stop = stage["stop_s"]
        if start is None:
            continue
        duration = float(stop) - float(start)
        if duration < 0:
            raise ConfigurationError(f"Stage {stage['id']} has stop before start")
        intervals.append((str(stage["id"]), duration))

    total = sum(duration for _, duration in intervals)
    if total <= 0:
        raise ConfigurationError("Campaign has no positive finite stage duration")
    return {name: duration / total for name, duration in intervals}
