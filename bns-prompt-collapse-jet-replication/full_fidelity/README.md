# Full-fidelity replication

This directory turns the paper into an executable scientific campaign rather than a cinematic imitation.

## What “full fidelity” means here

A successful production result must simultaneously reproduce, within declared convergence and stochastic/turbulent envelopes:

- inspiral and merger phasing;
- prompt apparent-horizon formation and black-hole mass/spin evolution;
- remnant-disk mass, accretion rate and thermodynamics;
- magnetic winding, MRI resolution and magnetic-energy saturation;
- neutrino luminosities and cooling transition;
- dynamical ejecta and secular disk-wind mass, velocity and composition;
- polar baryon clearing, magnetisation and jet-launch timing;
- Poynting luminosity, hemispheric asymmetry and opening-angle evolution;
- the reported late-time transition to a widening, less-confined funnel;
- the published movie as a *derived rendering*, never as the primary validation observable.

## Two tracks

### X-track — exact lineage

Use the exact SACRA-MPI revision, initial data, tables, build environment, input deck and checkpoint lineage. The campaign refuses to label an X-track run “exact” while any blocking artifact in `../references/parameter_ledger.yaml` remains unresolved.

### E-track — independent equivalence

Use an independently auditable solver with the same continuum system and matched discretisation order/effective resolution. E-track must pass the unit, canonical-problem, isolated-star, binary, collapse, disk/MRI, radiation and full-production gates before its result is compared with the target.

## Quick start

```bash
cd full_fidelity
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[test]'

bnsjet validate-manifest configs/campaign.yaml
bnsjet estimate-resources configs/campaign.yaml
bnsjet prepare-run configs/campaign.yaml --run-root runs
pytest
```

`prepare-run` creates an immutable run snapshot, hashes all declared artifacts, records the software environment, and renders scheduler scripts. It does not fabricate missing SACRA inputs.

## Current completion state

Implemented here:

- machine-readable campaign and artifact contracts;
- provenance freezing and checksum verification;
- resource modelling and staged scheduler templates;
- solver-adapter boundary for SACRA-MPI and an independent equivalent implementation;
- horizon, flux, ejecta, jet and convergence diagnostics;
- validation-target schema and comparison engine;
- canonical numerical test ladder;
- exact-artifact acquisition checklist and author request;
- CI tests for the orchestration and diagnostic mathematics.

Still requires external execution/assets:

- the unpublished or non-archived X-track artifacts listed in the parameter ledger;
- porting the rendered input contract to the selected production solver revision;
- allocation of leadership-class compute and storage;
- the actual multi-resolution production campaign.
