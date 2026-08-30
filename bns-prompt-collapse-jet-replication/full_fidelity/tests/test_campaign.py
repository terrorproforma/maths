from __future__ import annotations

import json
from pathlib import Path

from bnsjet.campaign import load_campaign, prepare_run, resolve_artifacts
from bnsjet.resources import estimate_resolution_costs, stage_duration_fractions
from bnsjet.validation import load_targets


PROJECT = Path(__file__).resolve().parents[1]
CAMPAIGN = PROJECT / "configs" / "campaign.yaml"
TARGETS = PROJECT / "reference_targets" / "target_metrics.yaml"


def test_campaign_and_targets_validate() -> None:
    campaign = load_campaign(CAMPAIGN)
    targets = load_targets(TARGETS)
    assert campaign["track"] == "E"
    assert len(campaign["stages"]) == 6
    assert len(targets["metrics"]) >= 5


def test_resource_estimates_are_monotonic() -> None:
    campaign = load_campaign(CAMPAIGN)
    estimates = estimate_resolution_costs(campaign)
    assert [estimate.spacing_m for estimate in estimates] == [240.0, 190.0, 150.0]
    assert estimates[0].cpu_hours < estimates[1].cpu_hours < estimates[2].cpu_hours
    fractions = stage_duration_fractions(campaign)
    assert abs(sum(fractions.values()) - 1.0) < 1.0e-12


def test_scaffold_run_prepares_and_records_missing_artifacts(tmp_path: Path) -> None:
    campaign = load_campaign(CAMPAIGN)
    _, missing = resolve_artifacts(CAMPAIGN, campaign)
    assert set(missing) == {"initial_data", "eos_table", "neutrino_tables"}

    run = prepare_run(CAMPAIGN, tmp_path)
    state = json.loads((run / "RUN_STATE.json").read_text(encoding="utf-8"))
    assert state["runnable"] is False
    assert set(state["missing_required_artifacts"]) == set(missing)
    assert (run / "submit.slurm").is_file()
    assert (run / "snapshot" / "PROVENANCE.json").is_file()
