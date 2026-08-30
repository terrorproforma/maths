#!/usr/bin/env bash
set -euo pipefail
python run_simulation.py --fps 30 --output surrogate_replication.mp4 --state-csv surrogate_state_history.csv
