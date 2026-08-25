#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python -m chronometric_hpc.driver \
  --config "$ROOT/config/hpc_solver_spec_portable_v1_9.yaml" \
  --results "$ROOT/inputs/prehpc_closure_results_v1_8.json" \
  --output "$ROOT/preflight_report_v1_9.json"
pytest -q "$ROOT/tests"
