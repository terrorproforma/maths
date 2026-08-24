#!/usr/bin/env python3
"""Run the consolidated verification suite against the repository layout.

The historical verifier was generated for the original flat archive layout.  The
GitHub repository uses clearer subdirectories, so this launcher creates a temporary
compatibility staging tree, executes the unchanged scientific checks, and writes the
result back to ``data/consolidated_verification_results.json``.

Author: Angus Muffatti
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "verify_consolidated_chronometry.py"
RESULTS = ROOT / "data" / "consolidated_verification_results.json"


def load_verifier():
    spec = importlib.util.spec_from_file_location("chronometric_verifier", VERIFIER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load verifier: {VERIFIER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def stage_file(source: Path, destination: Path) -> None:
    if not source.is_file() or source.stat().st_size == 0:
        raise FileNotFoundError(f"Required source file is missing or empty: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main() -> int:
    module = load_verifier()

    with tempfile.TemporaryDirectory(prefix="chronometric-verification-") as tmp:
        stage = Path(tmp)

        stage_file(
            ROOT / "manuscript" / "null_relational_chronometry_v1_4.md",
            stage / "chronometric_emergence_full_manuscript.md",
        )
        stage_file(
            ROOT / "manuscript" / "references.bib",
            stage / "references.bib",
        )
        stage_file(
            ROOT / "sources" / "Photon_Perspective_in_Relativity.txt",
            stage / "sources" / "Photon_Perspective_in_Relativity_chat_snapshot.txt",
        )

        for name in (
            "benchmark_parameters.json",
            "source_ledger.csv",
            "historical_artifact_inventory.csv",
            "integrated_acceptance_matrix.csv",
        ):
            stage_file(ROOT / "data" / name, stage / "data" / name)

        module.ROOT = stage
        module.BENCHMARKS = stage / "data" / "benchmark_parameters.json"
        module.OUT = RESULTS

        result = module.verify()
        RESULTS.write_text(json.dumps(result, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    print(json.dumps(result["summary"], indent=2))
    print(f"wrote {RESULTS}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
