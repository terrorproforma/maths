#!/usr/bin/env python3
"""Atomically promote a checkpoint into durable storage with a SHA-256 sidecar."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def copy_atomic(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".partial", dir=destination.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copyfile(source, temporary)
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--stage", required=True)
    arguments = parser.parse_args()

    source = arguments.source.expanduser().resolve()
    destination = arguments.destination.expanduser().resolve()
    if not source.is_file():
        parser.error(f"Source checkpoint is not a file: {source}")
    if destination.exists():
        parser.error(f"Destination already exists: {destination}")

    source_digest = sha256(source)
    copy_atomic(source, destination)
    destination_digest = sha256(destination)
    if source_digest != destination_digest:
        destination.unlink(missing_ok=True)
        raise RuntimeError("Checkpoint digest changed during promotion")

    metadata = {
        "stage": arguments.stage,
        "source": str(source),
        "destination": str(destination),
        "size_bytes": destination.stat().st_size,
        "sha256": destination_digest,
        "promoted_utc": datetime.now(timezone.utc).isoformat(),
    }
    sidecar = destination.with_suffix(destination.suffix + ".json")
    sidecar.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
