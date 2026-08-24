#!/usr/bin/env bash
# Run the workstation-verifiable checks for the consolidated research package.
# Author: Angus Muffatti
set -euo pipefail

cd "$(dirname "$0")"

python3 - <<'PY'
from importlib.util import find_spec
missing = [name for name in ("numpy", "sympy") if find_spec(name) is None]
if missing:
    raise SystemExit(
        "Missing Python dependencies: " + ", ".join(missing) +
        ". Install them with: python3 -m pip install -r requirements.txt"
    )
PY

python3 scripts/run_repository_verification.py

echo "Verification complete. See data/consolidated_verification_results.json."
