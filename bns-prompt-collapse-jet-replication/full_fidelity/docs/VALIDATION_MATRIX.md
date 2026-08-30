# Validation matrix

Exact tolerances must be frozen before inspecting the final production output. The defaults below are campaign starting points, not post-hoc permission slips.

| Observable | Comparison object | Initial gate | Final interpretation |
|---|---|---:|---|
| Merger time/phasing | waveform phase aligned in early inspiral | convergence demonstrated | Sensitive to initial data and resolution. |
| Horizon formation | time relative to peak GW amplitude | within combined temporal-resolution error | Prompt-collapse classification must agree. |
| BH mass and spin | time series and late-time mean | 2–5% | Use the same quasi-local definitions. |
| Disk baryon mass | outside-horizon integral | 10% early, 20% late | Turbulence and floors must be budgeted. |
| Accretion rate | horizon flux, smoothed over declared windows | factor 1.5 pointwise; 20% windowed | Compare common windows, not cherry-picked peaks. |
| Magnetic energy | region-integrated growth and saturation | growth-rate overlap; saturation within factor 2 | Seed and MRI resolution are dominant sensitivities. |
| MRI quality factors | volume distributions | target-resolved volume fraction agrees | A visual jet with unresolved MRI fails. |
| Neutrino luminosity | species-separated time series | 20–30% | Microphysics/table differences must be isolated. |
| Ejecta mass | geodesic and Bernoulli criteria | 30% or convergence-overlap | Small masses are grid/floor sensitive. |
| Ejecta velocity/Ye | mass-weighted distributions | Wasserstein/quantile thresholds | Compare distributions, not only means. |
| Jet launch time | first sustained outward EM luminosity at multiple radii | within 50 ms or uncertainty envelope | Define persistence and radius before the run. |
| Poynting luminosity | north/south separately and total | within factor 2, then tighten | Turbulent and floor-sensitive. |
| Funnel magnetisation | radial/angle distributions | same regime and trend | Report cap/floor occupancy. |
| Opening angle | luminosity-containing angle versus time/radius | within several degrees plus convergence | Coordinate geometry must be converted consistently. |
| Movie morphology | derived images and feature metrics | only after all above pass | Presentation is the last gate, not the first. |

## Cross-resolution method

For a scalar observable \(f(h)\), estimate observed order

\[
p=\frac{\log\left|\frac{f_{h_1}-f_{h_2}}{f_{h_2}-f_{h_3}}\right|}
{\log r}
\]

when the refinement ratio \(r=h_1/h_2=h_2/h_3\) is common and the solution is in an asymptotic regime. Turbulent time series additionally require common filtering/window definitions and ensemble-aware uncertainty.

## Failure rule

A failed physical gate cannot be rescued by tuning the transfer function of the rendered movie.
