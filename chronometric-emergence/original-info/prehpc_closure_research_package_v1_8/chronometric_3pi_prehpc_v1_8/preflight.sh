#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PYTHONPATH=src python -m chronometric_hpc.driver \
  --config config/hpc_solver_spec_portable_v1_8.yaml \
  --results inputs/prehpc_closure_results_v1_8.json
PYTHONPATH=src pytest -q
