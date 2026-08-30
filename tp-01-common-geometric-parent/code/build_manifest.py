#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for distributable TP-01 v1.1 files."""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

EXCLUDED_SUFFIXES = {".aux", ".fdb_latexmk", ".fls", ".log", ".out", ".toc", ".synctex.gz"}
EXCLUDED_NAMES = {"manifest_sha256.csv"}
EXCLUDED_DIRS = {"__pycache__", ".git", "_renders"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def included(root: Path, path: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if path.name in EXCLUDED_NAMES:
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    paths = sorted(path for path in root.rglob("*") if included(root, path))
    manifest = root / "manifest_sha256.csv"
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "bytes", "sha256"])
        for path in paths:
            writer.writerow([path.relative_to(root).as_posix(), path.stat().st_size, sha256(path)])
    print(f"Wrote {manifest} with {len(paths)} entries")


if __name__ == "__main__":
    main()
