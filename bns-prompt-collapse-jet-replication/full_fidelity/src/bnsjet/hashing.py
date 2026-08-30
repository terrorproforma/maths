"""Cryptographic hashing and artifact verification."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .errors import ArtifactError


@dataclass(frozen=True)
class ArtifactDigest:
    """Digest record for one file."""

    path: str
    size_bytes: int
    sha256: str


def sha256_file(path: str | Path, *, chunk_size: int = 8 * 1024 * 1024) -> str:
    """Return the SHA-256 digest of a file without loading it into memory."""

    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise ArtifactError(f"Artifact is not a regular file: {source}")

    digest = hashlib.sha256()
    with source.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def digest_file(path: str | Path) -> ArtifactDigest:
    """Return path, size and SHA-256 for one file."""

    source = Path(path).expanduser().resolve()
    return ArtifactDigest(
        path=str(source),
        size_bytes=source.stat().st_size,
        sha256=sha256_file(source),
    )


def verify_file(path: str | Path, expected_sha256: str) -> ArtifactDigest:
    """Hash a file and require the declared SHA-256 digest."""

    record = digest_file(path)
    expected = expected_sha256.strip().lower()
    if record.sha256 != expected:
        raise ArtifactError(
            f"Digest mismatch for {record.path}: expected {expected}, got {record.sha256}"
        )
    return record


def digest_tree(root: str | Path, *, excluded_names: Iterable[str] = ()) -> list[ArtifactDigest]:
    """Hash every regular file below *root* in stable relative-path order."""

    directory = Path(root).expanduser().resolve()
    excluded = set(excluded_names)
    records: list[ArtifactDigest] = []
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        if path.name in excluded:
            continue
        record = digest_file(path)
        records.append(
            ArtifactDigest(
                path=str(path.relative_to(directory)),
                size_bytes=record.size_bytes,
                sha256=record.sha256,
            )
        )
    return records
