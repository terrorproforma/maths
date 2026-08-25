# Selector-Threshold Radiative Closure v1.1

This package contains the technical paper, source files, verification suite, numerical outputs, and figures for the first mixed selector-threshold and nonequilibrium audit.

## Main conclusions

- The first primitive connected 1PI selector-reheaton-threshold graph is three-loop.
- Every forbidden lower harmonic must carry transient selector charge, state-density charge, or a decaying memory functional.
- The formal coupled 2PI/Kadanoff-Baym system is derived in the paper.
- The numerical implementation is an exact Gaussian, non-Markovian two-time surrogate, not a full nonlinear non-Abelian 3+1D plasma simulation.
- The original direct scalar inflaton-reheaton portal is generically vulnerable to tachyonic/resonant preheating.
- A selector-gated fermionic parent cascade gives parametrically clean hidden-replica suppression at linear production level.
- An 18-link deconstructed Wilson line supplies a concrete gauge-protected shift-symmetry skeleton; the full global discrete-anomaly audit remains open.

## Reproduction

Run:

```bash
python verify_selector_threshold_kb_v1_1.py
```

The script rewrites the JSON, CSV, NPZ, and PNG numerical outputs in its configured output directory.
