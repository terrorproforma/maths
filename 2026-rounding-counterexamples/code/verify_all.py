#!/usr/bin/env python3
"""Run every exact certificate verifier in a fresh Python process."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str) -> None:
    path = HERE / script
    print(f"=== {script} ===")
    subprocess.run([sys.executable, str(path)], check=True)
    print()


def main() -> None:
    run("verify_dgg.py")
    run("verify_chairman.py")
    print("All exact certificates passed.")


if __name__ == "__main__":
    main()
