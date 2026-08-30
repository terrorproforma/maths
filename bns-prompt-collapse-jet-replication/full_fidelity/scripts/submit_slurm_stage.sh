#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "usage: $0 RUN_DIRECTORY STAGE_ID" >&2
    exit 2
fi

RUN_DIR="$(cd "$1" && pwd)"
STAGE_ID="$2"
if [[ ! -f "$RUN_DIR/submit.slurm" ]]; then
    echo "missing Slurm script: $RUN_DIR/submit.slurm" >&2
    exit 2
fi

cd "$RUN_DIR"
sbatch --export=ALL,BNSJET_STAGE="$STAGE_ID" submit.slurm
