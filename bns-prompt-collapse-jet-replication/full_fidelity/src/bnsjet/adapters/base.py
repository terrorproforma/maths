"""Abstract boundary between campaign control and a production solver."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class SolverAdapter(ABC):
    """Interface required to turn a frozen campaign into solver-specific inputs."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable solver name."""

    @abstractmethod
    def validate_campaign(self, campaign: dict[str, Any]) -> list[str]:
        """Return blocking incompatibilities between campaign and solver."""

    @abstractmethod
    def render_input(
        self,
        campaign: dict[str, Any],
        destination: str | Path,
    ) -> list[Path]:
        """Render solver-specific input files and return their paths."""

    @abstractmethod
    def launch_arguments(
        self,
        campaign: dict[str, Any],
        stage_id: str,
        run_directory: str | Path,
    ) -> list[str]:
        """Return executable arguments for one campaign stage."""
