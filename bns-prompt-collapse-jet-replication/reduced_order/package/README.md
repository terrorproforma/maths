# Prompt-collapse neutron-star merger: frame analysis and replication

This package identifies, measures and reproduces the uploaded Max Planck / AEI movie of a prompt-collapse binary-neutron-star merger.

## The source

**Paper:** Kota Hayashi, Kenta Kiuchi, Koutarou Kyutoku, Yuichiro Sekiguchi and Masaru Shibata, “Jet from Binary Neutron Star Merger with Prompt Black Hole Formation,” *Physical Review Letters* **134**, 211407 (2025).

- DOI: https://doi.org/10.1103/PhysRevLett.134.211407
- arXiv: https://arxiv.org/abs/2410.10958
- Max Planck release and source movie: https://www.mpg.de/24689430/breakthrough-in-simulating-how-neutron-stars-collide

The source calculation follows a 1.25 + 1.65 solar-mass binary through five inspiral orbits, prompt black-hole formation, disk evolution, magnetic-field amplification, mass ejection and jet formation. The published run used numerical-relativity neutrino-radiation magnetohydrodynamics and about 130 million CPU-hours on Fugaku.

## Critical interpretation

The uploaded 14.37-second clip does **not** begin at the instant the black hole forms. Its first printed timestamp is 14.96 ms after merger. The supplementary paper places black-hole formation at roughly 1 ms after merger. The visible sequence is therefore mainly the already-formed black hole's torus, ejecta, MRI/dynamo, magnetosphere and asymmetric-to-bipolar jet evolution.

The playback is deliberately nonlinear:

- frames 0–129: approximately 72× slow motion;
- frames 130–142: a 13-frame freeze at 74.40 ms;
- frames 143–430: approximately 7.23× slow motion;
- full clip: 1.38368 seconds of simulated evolution over 14.333 seconds of frame time, or approximately 10.36× slow motion overall.

## Start here

Unzip the package and open `index.html` in a modern browser. The source video remains local; no server or internet connection is required.

## Files

- `index.html` / `frame_explorer.html` — self-contained browser UI; click any of the 431 rows to seek the source video to that exact frame.
- `source_timeline.csv` — recovered printed timestamp for every source frame.
- `keyframe_timeline.jpg` — annotated 16-keyframe scientific timeline.
- `sim_time_vs_video_time.png` and `slow_motion_factor.png` — playback analysis.
- `SOURCE_ANALYSIS.md` — scientific interpretation, phase-by-phase timeline and caveats.
- `physics.py`, `renderer.py`, `run_simulation.py` — runnable reduced-order physical/visual surrogate.
- `surrogate_replication_demo.mp4` — pre-rendered 14.4-second demonstration.
- `source_vs_surrogate.mp4` — synchronized side-by-side comparison of the paper movie and the reduced-order output.
- `surrogate_integral_state.png` — normalized disk, ejecta, magnetic and jet state curves used by the surrogate.
- `analyze_source_video.py` — reproduces the 431-frame screen-space measurements.
- `exact_reproduction_manifest.yaml` — full numerical-relativity reproduction target, known parameters, missing inputs and validation gates.
- `CITATION.bib` — paper and numerical-method citations.

## Run the surrogate

Python 3.10 or newer and `ffmpeg` are recommended.

```bash
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Fast preview: 144 frames, 10 fps, lower particle count
python run_simulation.py \
  --frames 144 \
  --fps 10 \
  --disk-particles 6000 \
  --ejecta-particles 10000 \
  --wind-particles 8000 \
  --output preview.mp4 \
  --state-csv preview_state.csv

# Full 431-frame visual surrogate matching the source timestamp schedule
python run_simulation.py \
  --fps 30 \
  --output surrogate_replication.mp4 \
  --state-csv surrogate_state_history.csv
```

The generated movie is deterministic because all Monte Carlo initial conditions use a fixed seed.

## Re-run the source-frame measurements

```bash
python analyze_source_video.py \
  source_clip.mp4 \
  --timeline source_timeline.csv \
  --output frame_by_frame_analysis_recomputed.csv
```

## What the surrogate is—and is not

The executable code is a **physics-informed reduced-order surrogate**. It evolves paper-calibrated integral quantities and renders a rotating torus, two ejecta components, magnetic bundles and asymmetric jet growth. It is useful for reconstructing the movie's causal sequence, testing timing, making variants and creating a visual analogue on a laptop.

It is **not** a solution of the Einstein, GRMHD or neutrino-transport PDEs. A defensible full rerun requires an NR radiation-GRMHD code, the SFHo/Helmholtz tables, LORENE initial data, the exact atmosphere and AMR setup, and a large HPC allocation. See `exact_reproduction_manifest.yaml`.

## Measurement caveats

The frame metrics are extracted from the rendered pixels, not the underlying simulation arrays. Density segmentation deliberately removes legends and thin field lines. Jet extent is a magenta-pixel proxy and therefore a lower bound on the visible magnetic structure. The 500 km ruler gives an approximate projected screen scale only; it is not a deprojected physical radius.
