"""Run provenance collection."""

from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .hashing import digest_file


def _run_git(repository: Path, *arguments: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return completed.stdout.strip()


def _installed_packages() -> list[dict[str, str]]:
    packages = [
        {"name": distribution.metadata["Name"], "version": distribution.version}
        for distribution in importlib.metadata.distributions()
        if distribution.metadata.get("Name")
    ]
    return sorted(packages, key=lambda item: item["name"].lower())


def collect_provenance(
    *,
    repository: str | Path | None = None,
    artifacts: dict[str, Path] | None = None,
) -> dict[str, Any]:
    """Collect software, host, scheduler and artifact provenance."""

    repo = Path(repository).expanduser().resolve() if repository is not None else Path.cwd()
    artifact_records: dict[str, dict[str, Any]] = {}
    for name, path in sorted((artifacts or {}).items()):
        record = digest_file(path)
        artifact_records[name] = {
            "path": record.path,
            "size_bytes": record.size_bytes,
            "sha256": record.sha256,
        }

    scheduler_keys = [
        "SLURM_JOB_ID",
        "SLURM_JOB_NAME",
        "SLURM_JOB_NODELIST",
        "SLURM_NNODES",
        "SLURM_NTASKS",
        "SLURM_CPUS_PER_TASK",
        "PJM_JOBID",
        "PJM_NODE",
        "OMP_NUM_THREADS",
        "CUDA_VISIBLE_DEVICES",
        "ROCR_VISIBLE_DEVICES",
    ]
    scheduler = {key: os.environ[key] for key in scheduler_keys if key in os.environ}

    return {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "host": {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": sys.version,
            "executable": sys.executable,
        },
        "git": {
            "repository": str(repo),
            "commit": _run_git(repo, "rev-parse", "HEAD"),
            "branch": _run_git(repo, "branch", "--show-current"),
            "status_porcelain": _run_git(repo, "status", "--porcelain=v1"),
            "remote": _run_git(repo, "remote", "get-url", "origin"),
        },
        "scheduler": scheduler,
        "artifacts": artifact_records,
        "environment": {
            "selected": {
                key: value
                for key, value in sorted(os.environ.items())
                if key.startswith(("BNSJET_", "SACRA_", "ATHENA_", "OMP_", "MPI_"))
            },
            "packages": _installed_packages(),
        },
    }


def canonical_provenance_json(provenance: dict[str, Any]) -> str:
    """Return a canonical JSON representation suitable for hashing."""

    return json.dumps(provenance, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
