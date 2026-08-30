#!/usr/bin/env python3
"""Create a deterministic SHA-256 manifest for the distributable research package."""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

EXCLUDED_NAMES = {
    "manifest_sha256.csv",
}
EXCLUDED_SUFFIXES = {
    ".aux", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".run.xml", ".toc",
    ".pyc",
}
EXCLUDED_DIRS = {"__pycache__", ".git"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def should_include(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.name in EXCLUDED_NAMES:
        return False
    if any(path.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES):
        return False
    return path.is_file()


def main(root: Path) -> None:
    root = root.resolve()
    rows = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if should_include(path, root):
            rows.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )

    output = root / "manifest_sha256.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {output} with {len(rows)} files")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    main(Path(args.root))
