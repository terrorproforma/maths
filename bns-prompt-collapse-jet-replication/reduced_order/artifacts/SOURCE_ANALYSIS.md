# Scientific analysis of the uploaded 431-frame movie

## 1. Identification and correction of the premise

The uploaded clip is the movie associated with:

> Kota Hayashi, Kenta Kiuchi, Koutarou Kyutoku, Yuichiro Sekiguchi and Masaru Shibata, “Jet from Binary Neutron Star Merger with Prompt Black Hole Formation,” *Physical Review Letters* **134**, 211407 (2025), DOI 10.1103/PhysRevLett.134.211407, arXiv:2410.10958.

The work was led by researchers at the Max Planck Institute for Gravitational Physics (Albert Einstein Institute) and run on Fugaku. The authors describe a 1.5-second, self-consistent numerical-relativity neutrino-radiation magnetohydrodynamics simulation.

A crucial distinction: the movie is often captioned as “black hole and jet formation,” but the uploaded segment does not show the actual apparent-horizon birth. The first frame reads **14.96 ms after merger**. The supplementary analysis associates the black-hole-formation accretion spike with **less than about 1 ms after merger**. Consequently, every frame in this clip is post-collapse. What evolves visibly is the remnant disk, ejecta, magnetic amplification, polar magnetosphere and Poynting-flux jet.

## 2. What is being visualised

- **Blue–cyan–green–yellow–red translucent surfaces:** rest-mass density, with the right-bottom legend spanning approximately `10^5` to `10^10 g cm^-3`.
- **White/green/magenta filaments:** magnetic-field structures and the magnetically dominated polar funnel. The right-top legend is the magnetisation `b^2/(4πρ)`, spanning approximately `10^-1` to `10^1`.
- **Central compact object:** the apparent horizon is too small to dominate this approximately 1000-km-scale view; the bright central torus surrounds the already-formed black hole.
- **500 km ruler:** projected scale in the rendered camera view.
- **Coordinate triad:** orientation of the Cartesian simulation axes.

The coloured density contours should not be read as an ordinary photograph. They are selected isodensity/volume-rendering layers. A growing low-density blue envelope can occupy a large screen area while containing much less mass than the compact yellow/red torus.

## 3. Source parameters recovered from the paper

| Quantity | Value |
|---|---:|
| Neutron-star masses | 1.25 and 1.65 solar masses |
| Total mass | 2.90 solar masses |
| High-density EOS | finite-temperature SFHo |
| Low-density EOS | Helmholtz |
| Initial state | irrotational LORENE quasi-equilibrium binary |
| Initial orbit | `Ω0 m0 G/c^3 = 0.025`; about five orbits before merger |
| Initial magnetic field | internal poloidal field, maximum `10^15 G` |
| Black-hole mass | approximately 2.77 solar masses |
| Black-hole dimensionless spin | approximately 0.76 |
| Disk mass at about 20 ms | approximately 0.062 solar masses |
| Dynamical ejecta | approximately `1.6×10^-3` solar masses |
| Final post-merger ejecta | approximately `4.7×10^-3` solar masses |
| Final disk mass | approximately `1.6×10^-3` solar masses |
| Peak total neutrino luminosity | approximately `10^53 erg s^-1` |
| Jet isotropic-equivalent luminosity | approximately `10^49 erg s^-1` |
| South/north jet milestones | about 0.13 s / 0.30 s |
| Magnetosphere half-opening angle | below about 6° before 1 s; about 9° at 1.4 s |

## 4. Playback reconstruction

The source file contains 431 frames at 30 fps. Printed timestamps were recovered for every frame and manually checked at OCR discontinuities.

| Video region | Frames | Simulated interval | Typical increment per frame | Playback character |
|---|---:|---:|---:|---:|
| Early segment | 0–129 | 14.96–74.00 ms | approximately 0.46 ms | approximately 72× slow motion |
| Editorial hold | 130–142 | 74.40 ms fixed | 0 | 0.433 s freeze |
| Late segment | 143–430 | 77.28–1398.64 ms | approximately 4.61 ms | approximately 7.23× slow motion |

The overall movie is therefore slow motion, not time compression: 1.38368 s of physical evolution is shown over 14.333 s between the first and last frame timestamps.

## 5. Frame-by-frame phase interpretation

The complete 431-row result is in `frame_by_frame_analysis.csv`. The following partitions explain what each row is tracking.

| Frames | Printed time | Physical interpretation |
|---:|---:|---|
| 0–11 | 14.96–19.57 ms | **Prompt-collapse aftermath.** The horizon already exists. A compact hot torus and innermost dynamical ejecta dominate; no resolved large polar magnetosphere is visible. |
| 12–55 | 20.03–39.87 ms | **Disk circularisation and early MRI.** The paper reports that the fastest MRI mode becomes resolved in lower-density material from about 20 ms. Dynamical ejecta spreads into a highly asymmetric, equatorially weighted cloud. |
| 56–129 | 40.33–74.00 ms | **Magnetic winding and α–Ω dynamo.** The blue low-density envelope expands across the view. Field polarity cycles on a roughly 30–40 ms cadence; this is the organising process that builds a coherent large-scale poloidal component out of turbulence. |
| 130–142 | 74.40 ms | **Editorial freeze.** These are not 13 new physical states. The same simulation frame is held for 0.433 s before the playback-rate change. |
| 143–147 | 77.28–95.73 ms | **Acceleration into secular evolution.** The clip jumps to about ten times larger simulation-time steps per video frame. Magnetic energy approaches its reported saturation scale. |
| 148–154 | 100.34–128.01 ms | **Disk-wide MRI resolution.** The paper reports MRI resolved across essentially the whole disk by about 0.1 s and electromagnetic energy saturating near 1% of internal energy. Neutrino luminosity has a secondary heating peak. |
| 155–169 | 132.63–197.20 ms | **Southern magnetosphere launches first.** The south reaches the reported approximately `10^49 erg s^-1` luminosity at about 0.13 s. The visible polar field is initially one-sided because the dynamo and flux accumulation are stochastic/asymmetric. |
| 170–191 | 201.81–298.66 ms | **Asymmetric bipolar growth.** The long southern helical bundle is established; the northern bundle grows later. This is a magnetically dominated funnel, not a material beam with the same density colours as the torus. |
| 192–212 | 303.27–395.52 ms | **Mature Blandford–Znajek outflow.** Both hemispheres now reach the reported luminosity scale. Black-hole spin supplies Poynting flux through horizon-threading magnetic flux; the surrounding disk/wind pressure collimates it. |
| 213–221 | 400.13–437.02 ms | **Post-merger mass ejection becomes established.** MRI-driven turbulent heating expands the disk and launches a broader, slower wind outside the narrow magnetosphere. |
| 222–256 | 441.64–598.45 ms | **Fixed-spacetime phase and mature wind.** At approximately 0.44 s the authors switch to the Cowling approximation because numerical under-resolution makes the black-hole spin drift. The disk is then below 1% of the black-hole mass, so its self-gravity is dynamically small. |
| 257–343 | 604.21–999.70 ms | **Wind-dominated secular evolution.** The supplementary material reports mass ejection overtaking accretion at about 0.6 s. Neutrino cooling fades; turbulent heat increasingly powers expansion and ejection. |
| 344–430 | 1004.31–1398.64 ms | **Jet weakening and funnel widening.** After about 1 s the collimated Poynting luminosity declines. The magnetic flux has not abruptly vanished; instead, falling confining gas pressure widens the magnetosphere from below about 6° toward about 9° by 1.4 s. |

## 6. Screen-space measurements made for every frame

Each frame was decoded and measured after masking the timestamp, legends, ruler and coordinate triad.

- `density_blob_pixels`, `density_r95_px`, `density_r99_px`: area and radial percentiles of the colour-segmented density rendering.
- `density_r95_screen_km`, `density_r99_screen_km`: approximate projected scales obtained from the displayed 500 km ruler.
- `right_minus_left_density_fraction`: a simple screen asymmetry statistic; positive means more segmented density pixels lie to the right of the image centre.
- `north_magenta_jet_extent_*`, `south_magenta_jet_extent_*`: distance from the image centre to the furthest robust magenta pixel in each hemisphere.
- `density_trend_from_previous_frame`, `jet_trend_from_previous_frame`: thresholded visual changes, not physical derivatives.

The magenta proxy first crosses roughly 1000 projected screen-km to the south around frame 170 (201.81 ms) and to the north around frame 203 (354.01 ms). This is consistent with a visibly earlier southern outflow, but the precise crossing times are renderer/threshold dependent and should not replace the paper's flux diagnostics.

## 7. Physical causal chain

1. The unequal-mass neutron stars merge and promptly collapse because the total mass is high for the SFHo EOS.
2. Tidal disruption leaves a comparatively massive torus despite prompt collapse.
3. Differential rotation winds the seed poloidal field into toroidal field.
4. MRI-driven turbulence becomes increasingly resolved and drives an α–Ω dynamo, creating coherent large-scale poloidal flux.
5. Flux is advected onto the rotating black hole, creating highly magnetised polar regions.
6. The black hole's rotation powers an outgoing Poynting flux through the Blandford–Znajek mechanism.
7. Gas pressure from the torus and disk wind confines the magnetic tower into a narrow bipolar jet.
8. As the disk loses mass and neutrino cooling weakens, turbulent heating drives a broad post-merger wind.
9. The wind depletes/expands the confining disk. The funnel broadens and the luminosity measured inside a fixed narrow cone declines after about one second.

## 8. Why an exact rerun is hard

The published calculation used:

- BSSN moving-puncture spacetime evolution with Z4c constraint propagation;
- fourth-order finite differencing in space and time;
- relativistic MHD with an HLLD Riemann solver;
- constrained transport and magnetic-flux-preserving mesh refinement;
- grey M1 plus leakage neutrino radiation transfer;
- 14 fixed refinement levels, 150 m finest spacing and a domain extending to approximately ±312,115 km;
- 20,736–82,944 Fugaku CPUs per job and approximately 130 million CPU-hours total.

No exact source repository, input deck or checkpoint set is linked from the PRL page, supplement, arXiv record or Max Planck release. The paper is sufficiently detailed to define the target model, but not enough to guarantee bitwise or quantitatively converged reproduction without the authors' code version, EOS/opacity tables, initial-data files and all gauge/floor/refinement implementation choices.

As of 2026, the strongest public starting point for a genuinely independent reproduction is GR-Athena++, which exposes dynamical Z4c spacetime, GRMHD, constrained transport, tabulated microphysical EOS support, LORENE readers and M1 radiation transport. SACRA-K is the authors' newer performance-portable lineage and is highly relevant for GPU acceleration, but its initial public paper validates hydrodynamics rather than the full MHD-plus-neutrino stack required here.

## 9. What the supplied code reproduces

The laptop code reproduces the **observable causal choreography**:

- exact 431-frame source timestamp schedule, including the freeze and speed change;
- compact Kerr-remnant scale and paper-calibrated disk/ejecta masses;
- early dynamical ejecta and slower post-merger wind;
- MRI magnetic-energy growth and saturation timing;
- delayed, asymmetric south/north jet growth;
- approximately one-second luminosity decline and funnel widening;
- density and magnetisation legends with a comparable camera composition.

It does not claim to predict new gravitational waveforms, neutrino spectra, nucleosynthesis, turbulence statistics or horizon flux. Those require the full NR radiation-GRMHD run specified in `exact_reproduction_manifest.yaml`.
