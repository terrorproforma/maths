# Production campaign plan

## Phase A — evidence freeze

1. Archive paper, supplement and movie hashes.
2. Obtain exact solver/input artifacts for X-track.
3. Resolve every production-relevant `unresolved` ledger item or explicitly demote the run from X-track.
4. Freeze observable definitions and tolerances.

## Phase B — implementation qualification

1. Build the target executable in a reproducible container/module environment.
2. Complete Gates 0–4 of `TEST_LADDER.md`.
3. Compare primitive recovery, EOS inversion and neutrino source terms against independent unit references.
4. Audit atmosphere and magnetisation caps with injected-budget diagnostics.

## Phase C — initial data and inspiral

1. Validate LORENE constraints and stellar baryon/gravitational masses.
2. Reproduce the target orbital state and residual eccentricity.
3. Seed the magnetic field using the exact pressure-confined vector potential.
4. Run low/medium/high inspiral resolutions and measure waveform convergence.

## Phase D — prompt collapse pilot

1. Continue through merger and apparent-horizon formation.
2. Validate collapse time, BH mass/spin and disk mass.
3. Run through 100 ms and evaluate MRI quality, magnetic-energy growth, neutrino budgets and polar baryon clearing.
4. Stop if floor injection or unresolved MRI invalidates the intended comparison.

## Phase E — 1.5 s production

Suggested segmentation:

- `P0`: initial data to merger;
- `P1`: merger to 20 ms;
- `P2`: 20–100 ms;
- `P3`: 100–440 ms;
- `P4`: 440–1000 ms;
- `P5`: 1000–1500 ms.

At every boundary, freeze a checkpoint hash, scheduler topology, code hash and conservation ledger. If the target freezes the spacetime near 0.44 s, the transition must occur from a recorded checkpoint and be reproduced in both X and matched E runs.

## Phase F — analysis and rendering

1. Extract horizon, disk, neutrino, ejecta and jet diagnostics at native cadence.
2. Perform multi-resolution and seed-sensitivity analysis.
3. Generate derived volumetric products and a transfer-function-independent feature table.
4. Only then render a source-style movie using documented camera, colormap, clipping and temporal sampling.
