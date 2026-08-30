# Reduced-order replication

This directory preserves the complete workstation-scale analysis and surrogate renderer.

## Quick start

The original package is under `package/`. Start with its README and environment metadata. Curated outputs are mirrored under `artifacts/`:

- `surrogate_replication_demo.mp4` — surrogate-only playback.
- `source_vs_surrogate.mp4` — synchronised comparison.
- `SOURCE_ANALYSIS.md` — scientific interpretation and timing reconstruction.
- `keyframe_timeline.jpg` — annotated event timeline.

## Scope

The surrogate reproduces the causal choreography and presentation timing of the reference movie. It does not evolve the Einstein equations, relativistic MHD conservation laws, neutrino moments, nuclear EOS, or apparent horizon. Those belong to `../full_fidelity/`.
