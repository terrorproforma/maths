from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

@dataclass(frozen=True)
class SolverConfig:
    raw: dict[str, Any]

    @property
    def acceptance(self) -> dict[str, float]:
        return self.raw["acceptance"]

    @property
    def table_path(self) -> Path:
        return Path(self.raw["truncation"]["hard_soft_matching"]["pointwise_regression_table"])


def load_config(path: str | Path) -> SolverConfig:
    path = Path(path)
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("configuration root must be a mapping")
    return SolverConfig(data)
