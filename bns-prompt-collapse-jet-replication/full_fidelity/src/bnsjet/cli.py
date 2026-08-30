"""Command-line interface for campaign preparation and validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .campaign import load_campaign, prepare_run, resolve_artifacts
from .contract import check_output_contract
from .errors import BNSJetError, ValidationFailure
from .io import dump_json_atomic, load_document
from .provenance import collect_provenance
from .resources import estimate_resolution_costs, stage_duration_fractions
from .validation import load_targets, validate_observations


def _print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))


def _artifact_pairs(values: Sequence[str]) -> dict[str, Path]:
    artifacts: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Artifact must use NAME=PATH syntax: {value}")
        name, raw_path = value.split("=", 1)
        name = name.strip()
        if not name:
            raise ValueError(f"Artifact name is empty: {value}")
        artifacts[name] = Path(raw_path).expanduser().resolve()
    return artifacts


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bnsjet",
        description="Prepare and validate prompt-collapse BNS jet replication campaigns.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_manifest = subparsers.add_parser("validate-manifest", help="Validate campaign YAML")
    validate_manifest.add_argument("campaign")

    validate_targets = subparsers.add_parser("validate-targets", help="Validate target YAML")
    validate_targets.add_argument("targets")

    estimate = subparsers.add_parser("estimate-resources", help="Estimate resolution costs")
    estimate.add_argument("campaign")

    artifacts = subparsers.add_parser("check-artifacts", help="Resolve and hash campaign artifacts")
    artifacts.add_argument("campaign")
    artifacts.add_argument("--strict", action="store_true")

    prepare = subparsers.add_parser("prepare-run", help="Create an immutable run snapshot")
    prepare.add_argument("campaign")
    prepare.add_argument("--run-root", default="runs")
    prepare.add_argument("--strict-artifacts", action="store_true")

    freeze = subparsers.add_parser("freeze-provenance", help="Write host/software/artifact provenance")
    freeze.add_argument("--repository", default=".")
    freeze.add_argument("--artifact", action="append", default=[], metavar="NAME=PATH")
    freeze.add_argument("--output", required=True)

    validate_output = subparsers.add_parser("validate-output", help="Compare observed JSON metrics")
    validate_output.add_argument("targets")
    validate_output.add_argument("observations")
    validate_output.add_argument("--allow-missing", action="store_true")
    validate_output.add_argument("--output")

    contract = subparsers.add_parser("check-output-contract", help="Check required run outputs")
    contract.add_argument("run_directory")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    arguments = parser.parse_args(argv)

    try:
        if arguments.command == "validate-manifest":
            campaign = load_campaign(arguments.campaign)
            _print_json(
                {
                    "valid": True,
                    "campaign_id": campaign["campaign_id"],
                    "track": campaign["track"],
                    "stages": len(campaign["stages"]),
                }
            )
        elif arguments.command == "validate-targets":
            targets = load_targets(arguments.targets)
            _print_json({"valid": True, "metrics": len(targets["metrics"])})
        elif arguments.command == "estimate-resources":
            campaign = load_campaign(arguments.campaign)
            _print_json(
                {
                    "resolutions": [item.as_dict() for item in estimate_resolution_costs(campaign)],
                    "stage_duration_fractions": stage_duration_fractions(campaign),
                    "warning": "Planning anchor only; benchmark the production executable.",
                }
            )
        elif arguments.command == "check-artifacts":
            campaign = load_campaign(arguments.campaign)
            available, missing = resolve_artifacts(arguments.campaign, campaign)
            if arguments.strict and missing:
                raise ValueError(f"Missing required artifacts: {', '.join(missing)}")
            _print_json(
                {
                    "track": campaign["track"],
                    "available": {name: str(path) for name, path in available.items()},
                    "missing_required": missing,
                    "runnable": not missing,
                }
            )
        elif arguments.command == "prepare-run":
            run_directory = prepare_run(
                arguments.campaign,
                arguments.run_root,
                strict_artifacts=arguments.strict_artifacts,
            )
            _print_json({"prepared": str(run_directory)})
        elif arguments.command == "freeze-provenance":
            provenance = collect_provenance(
                repository=arguments.repository,
                artifacts=_artifact_pairs(arguments.artifact),
            )
            output = dump_json_atomic(arguments.output, provenance)
            _print_json({"written": str(output)})
        elif arguments.command == "validate-output":
            targets = load_targets(arguments.targets)
            observations = load_document(arguments.observations)
            results = validate_observations(
                targets,
                observations,
                fail_on_missing=not arguments.allow_missing,
            )
            payload = {"passed": True, "results": [result.as_dict() for result in results]}
            if arguments.output:
                dump_json_atomic(arguments.output, payload)
            _print_json(payload)
        elif arguments.command == "check-output-contract":
            missing = check_output_contract(arguments.run_directory)
            _print_json({"complete": not missing, "missing": missing})
            return 0 if not missing else 2
        else:
            parser.error(f"Unhandled command: {arguments.command}")
    except ValidationFailure as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        return 3
    except (BNSJetError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
