#!/usr/bin/env bash
set -euo pipefail
python run_simulation.py --frames 144 --fps 10 --disk-particles 6000 --ejecta-particles 10000 --wind-particles 8000 --output preview.mp4 --state-csv preview_state.csv
