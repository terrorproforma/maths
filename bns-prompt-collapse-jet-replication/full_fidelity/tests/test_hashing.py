from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from bnsjet.errors import ArtifactError
from bnsjet.hashing import digest_tree, sha256_file, verify_file


def test_hash_and_verify(tmp_path: Path) -> None:
    path = tmp_path / "artifact.bin"
    path.write_bytes(b"black-hole-jet")
    expected = hashlib.sha256(b"black-hole-jet").hexdigest()
    assert sha256_file(path) == expected
    assert verify_file(path, expected).sha256 == expected
    with pytest.raises(ArtifactError):
        verify_file(path, "0" * 64)


def test_tree_digest_is_sorted(tmp_path: Path) -> None:
    (tmp_path / "b").write_bytes(b"b")
    (tmp_path / "a").write_bytes(b"a")
    records = digest_tree(tmp_path)
    assert [record.path for record in records] == ["a", "b"]
