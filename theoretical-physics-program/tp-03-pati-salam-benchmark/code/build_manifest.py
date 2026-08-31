#!/usr/bin/env python3
"""Build a SHA-256 manifest for committed TP-03 text and data files."""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

EXCLUDED = {
    "manifest_sha256.csv",
    "PROGRAM_README.md",
    "tp-03-pati-salam.yml",
}
EXCLUDED_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".git",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    root = args.root.resolve()
    rows = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if path.name in EXCLUDED or any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append((relative.as_posix(), path.stat().st_size, digest))

    output = root / "manifest_sha256.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "bytes", "sha256"])
        writer.writerows(rows)
    print(f"wrote {output} with {len(rows)} entries")


if __name__ == "__main__":
    main()
