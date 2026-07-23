#!/usr/bin/env python3
"""Run every certificate verifier from the repository root or code folder."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(name: str) -> None:
    print(f"\n== {name} ==")
    subprocess.run([sys.executable, str(HERE / name)], check=True)


def main() -> None:
    run("verify_dgg.py")
    run("verify_chairman_certificate.py")
    try:
        run("verify_chairman_milp.py")
    except ModuleNotFoundError:
        print("SciPy is unavailable; exact certificate checks passed, MILP check skipped.")


if __name__ == "__main__":
    main()
