"""Campaign validation, artifact resolution and immutable run preparation."""

from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .errors import ArtifactError, ConfigurationError
from .hashing import digest_file, verify_file
from .io import dump_json_atomic, load_document, resolve_relative
from .provenance import collect_provenance
from .resources import estimate_resolution_costs, stage_duration_fractions
from .schema import project_schema, validate_against_schema


def load_campaign(path: str | Path) -> dict[str, Any]:
    """Load and schema-validate a campaign document."""

    campaign = load_document(path)
    validate_against_schema(
        campaign,
        project_schema("campaign.schema.json"),
        document_name=f"campaign {Path(path)}",
    )
    _validate_stage_order(campaign)
    return campaign


def _validate_stage_order(campaign: dict[str, Any]) -> None:
    previous_stop: float | None = None
    identifiers: set[str] = set()
    for stage in campaign["stages"]:
        identifier = str(stage["id"])
        if identifier in identifiers:
            raise ConfigurationError(f"Duplicate stage id: {identifier}")
        identifiers.add(identifier)

        start = stage["start_s"]
        stop = float(stage["stop_s"])
        if start is not None:
            start_value = float(start)
            if stop < start_value:
                raise ConfigurationError(f"Stage {identifier} stops before it starts")
            if previous_stop is not None and abs(start_value - previous_stop) > 1.0e-12:
                raise ConfigurationError(
                    f"Stage {identifier} starts at {start_value}, but previous finite stage "
                    f"stops at {previous_stop}"
                )
        previous_stop = stop


def resolve_artifacts(
    campaign_path: str | Path,
    campaign: dict[str, Any],
) -> tuple[dict[str, Path], list[str]]:
    """Resolve and verify declared artifacts.

    Returns a mapping of available artifacts and a list of missing artifacts that
    are required for the selected track.
    """

    track = str(campaign["track"])
    available: dict[str, Path] = {}
    missing: list[str] = []

    for name, declaration in sorted(campaign["artifacts"].items()):
        required = track in declaration.get("required_for", [])
        raw_path = declaration.get("path")
        expected_digest = declaration.get("sha256")

        if raw_path is None:
            if required:
                missing.append(name)
            continue

        path = resolve_relative(campaign_path, raw_path)
        if not path.is_file():
            if required:
                missing.append(name)
            continue

        if expected_digest:
            verify_file(path, str(expected_digest))
        available[name] = path

    return available, missing


def _template_directory() -> Path:
    directory = Path(__file__).resolve().parents[2] / "hpc"
    if not directory.is_dir():
        raise ConfigurationError(f"HPC template directory not found: {directory}")
    return directory


def _render_scheduler(campaign: dict[str, Any], destination: Path) -> Path:
    scheduler = campaign["scheduler"]
    kind = scheduler["kind"]
    if kind == "local":
        script_name = "run-local.sh"
        template_relative = "slurm/run-local.sh.j2"
    elif kind == "slurm":
        script_name = "submit.slurm"
        template_relative = "slurm/production.sbatch.j2"
    elif kind == "pjm":
        script_name = "submit.pjm"
        template_relative = "pjm/production.pjm.j2"
    else:
        raise ConfigurationError(f"Unsupported scheduler kind: {kind}")

    environment = Environment(
        loader=FileSystemLoader(str(_template_directory())),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    template = environment.get_template(template_relative)
    rendered = template.render(campaign=campaign, scheduler=scheduler)
    output = destination / script_name
    output.write_text(rendered, encoding="utf-8")
    output.chmod(0o750)
    return output


def prepare_run(
    campaign_path: str | Path,
    run_root: str | Path,
    *,
    strict_artifacts: bool = False,
) -> Path:
    """Create an immutable, self-describing run directory.

    Missing required artifacts are recorded for scaffold campaigns. They become a
    hard error when ``strict_artifacts`` is true or campaign status is ``production``.
    """

    source_path = Path(campaign_path).expanduser().resolve()
    campaign = load_campaign(source_path)
    available_artifacts, missing_artifacts = resolve_artifacts(source_path, campaign)
    production = str(campaign.get("status", "")).lower() == "production"
    if missing_artifacts and (strict_artifacts or production):
        joined = ", ".join(missing_artifacts)
        raise ArtifactError(f"Required artifacts are missing for track {campaign['track']}: {joined}")

    root = Path(run_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_name = f"{campaign['campaign_id']}-{str(campaign['track']).lower()}-{timestamp}"
    destination = root / run_name
    if destination.exists():
        raise ConfigurationError(f"Run directory already exists: {destination}")

    temporary = Path(tempfile.mkdtemp(prefix=f".{run_name}.", dir=root))
    try:
        snapshot = temporary / "snapshot"
        snapshot.mkdir()
        shutil.copy2(source_path, snapshot / "campaign.yaml")

        ledger = resolve_relative(source_path, campaign["source_target"]["parameter_ledger"])
        if ledger.is_file():
            shutil.copy2(ledger, snapshot / "parameter_ledger.yaml")

        target_path = resolve_relative(source_path, campaign["validation"]["target_metrics"])
        if target_path.is_file():
            shutil.copy2(target_path, snapshot / "target_metrics.yaml")

        artifact_manifest: dict[str, dict[str, Any]] = {}
        for name, path in sorted(available_artifacts.items()):
            record = digest_file(path)
            artifact_manifest[name] = asdict(record)

        provenance = collect_provenance(
            repository=source_path.parents[2],
            artifacts=available_artifacts,
        )
        provenance["campaign"] = {
            "source": str(source_path),
            "track": campaign["track"],
            "status": campaign.get("status"),
            "missing_required_artifacts": missing_artifacts,
        }
        dump_json_atomic(snapshot / "PROVENANCE.json", provenance)
        dump_json_atomic(snapshot / "ARTIFACTS.json", artifact_manifest)

        estimates = [record.as_dict() for record in estimate_resolution_costs(campaign)]
        dump_json_atomic(snapshot / "RESOURCE_ESTIMATE.json", estimates)
        dump_json_atomic(snapshot / "STAGE_FRACTIONS.json", stage_duration_fractions(campaign))

        scheduler_script = _render_scheduler(campaign, temporary)
        state = {
            "run_id": run_name,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "track": campaign["track"],
            "runnable": not missing_artifacts,
            "missing_required_artifacts": missing_artifacts,
            "scheduler_script": scheduler_script.name,
            "stages": [
                {
                    "id": stage["id"],
                    "status": "pending",
                    "checkpoint_in": None,
                    "checkpoint_out": None,
                }
                for stage in campaign["stages"]
            ],
        }
        dump_json_atomic(temporary / "RUN_STATE.json", state)
        (temporary / "checkpoints").mkdir()
        (temporary / "diagnostics").mkdir()
        (temporary / "logs").mkdir()

        os.replace(temporary, destination)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return destination
