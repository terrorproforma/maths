from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

@dataclass(frozen=True)
class SolverConfig:
    raw: dict[str, Any]
    source_path: Path

    @property
    def acceptance(self) -> dict[str, float]:
        return self.raw["acceptance"]

    def resolve(self, value: str | Path) -> Path:
        path = Path(value)
        if path.is_absolute():
            return path
        return (self.source_path.parent.parent / path).resolve()

    @property
    def table_path(self) -> Path:
        return self.resolve(self.raw["truncation"]["hard_soft_matching"]["pointwise_regression_table"])

    @property
    def diagram_ledger_path(self) -> Path:
        return self.resolve(self.raw["truncation"]["diagram_ledger"])

    @property
    def counterterm_matrix_path(self) -> Path:
        return self.resolve(self.raw["truncation"]["counterterm_closure_matrix"])

    @property
    def tensor_catalog_path(self) -> Path:
        return self.resolve(self.raw["truncation"]["tensor_basis_catalog"])

    @property
    def observable_contract_path(self) -> Path:
        return self.resolve(self.raw["observable_contract"])


def load_config(path: str | Path) -> SolverConfig:
    path = Path(path).resolve()
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("configuration root must be a mapping")
    return SolverConfig(data, path)
