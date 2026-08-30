#!/usr/bin/env python3
"""Reconstruct the original TP-01 v1.1 LaTeX source from lossless text chunks."""
from __future__ import annotations

import hashlib
from pathlib import Path

EXPECTED_SHA256 = "e0a531a8aa65a5118527be0bf5caac18471d792fd139fe1b59fe4ef4a5b2b3dd"


def main() -> None:
    paper_dir = Path(__file__).resolve().parent
    chunks = sorted((paper_dir / "source_chunks").glob("part_*.tex"))
    if not chunks:
        raise SystemExit("No source chunks found")
    content = b"".join(path.read_bytes() for path in chunks)
    digest = hashlib.sha256(content).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"Source checksum mismatch: {digest} != {EXPECTED_SHA256}")
    target = paper_dir / "tp01_dirac_brst_global_audit_v1_1.tex"
    target.write_bytes(content)
    print(f"Wrote {target} from {len(chunks)} chunks; SHA-256 {digest}")


if __name__ == "__main__":
    main()
