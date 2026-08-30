#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${BNSJET_VENV:-$ROOT/.venv}"
PYTHON="${PYTHON:-python3}"

"$PYTHON" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -e "$ROOT[test]"
"$VENV/bin/bnsjet" validate-manifest "$ROOT/configs/campaign.yaml"
"$VENV/bin/bnsjet" validate-targets "$ROOT/reference_targets/target_metrics.yaml"
"$VENV/bin/pytest" "$ROOT/tests"
