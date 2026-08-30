# Numerical test ladder

Production access is gated. A solver does not proceed because it compiles; it proceeds because each lower-cost failure mode has been killed first.

## Gate 0 — build and determinism envelope

- frozen dependency hashes and compiler flags;
- reproducible small-run checksum on a fixed rank topology;
- documented variation under rank/thread decomposition;
- checkpoint/restart continuity test.

## Gate 1 — special-relativistic MHD

- relativistic Brio–Wu and Komissarov shock tubes;
- circularly polarised Alfvén wave convergence;
- relativistic rotor and blast wave;
- Orszag–Tang vortex;
- constrained-transport divergence preservation.

## Gate 2 — spacetime

- robust stability test;
- gauge wave and linear wave convergence;
- single puncture black hole;
- stable TOV star and radial-mode spectrum;
- migration/collapse of an unstable TOV star.

## Gate 3 — GRMHD in curved spacetime

- magnetised TOV equilibrium;
- Bondi accretion;
- Fishbone–Moncrief torus equilibrium;
- magnetised torus MRI growth and stress convergence;
- black-hole energy-extraction benchmark with signed horizon flux.

## Gate 4 — radiation and microphysics

- free-streaming beam;
- shadow test;
- diffusion pulse;
- radiation shock;
- optically thick thermalisation;
- EOS inversion over the entire production domain;
- beta-equilibrium and source-term relaxation;
- energy/lepton conservation under stiff coupling.

## Gate 5 — isolated and binary neutron stars

- cold and finite-temperature SFHo TOV sequences;
- magnetised rotating star stability;
- equal-mass BNS inspiral at multiple resolutions;
- unequal-mass BNS inspiral matching the target masses;
- eccentricity-reduction verification;
- prompt-collapse timing sensitivity study.

## Gate 6 — short post-merger pilot

Run through at least 100 ms post-merger at coarse, medium and target resolution. Require:

- consistent horizon formation;
- bounded constraint growth;
- disk mass and accretion convergence;
- resolved MRI quality factors in the regions used for claims;
- neutrino and floor budgets below declared thresholds.

## Gate 7 — long production

Run through 1.5 s with checkpoint intervals sufficient to recover from failures without unrecorded state changes. Complete at least three resolutions and one independent seed/control perturbation.
