#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMPAIGN="${1:-$ROOT/configs/campaign.yaml}"
RUN_ROOT="${2:-$ROOT/runs}"

bnsjet validate-manifest "$CAMPAIGN"
bnsjet estimate-resources "$CAMPAIGN"
bnsjet check-artifacts "$CAMPAIGN"
bnsjet prepare-run "$CAMPAIGN" --run-root "$RUN_ROOT"
