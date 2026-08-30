# Equations and numerical obligations

This is a solver-facing checklist. It prevents a nominally “GRMHD” run from quietly omitting the physics that determines the target result.

## Spacetime sector

Required evolved or reconstructible fields include the spatial metric, extrinsic curvature, conformal variables, lapse, shift and Z4c constraint variable(s). Record:

- formulation and damping coefficients;
- 1+log slicing implementation;
- Gamma-driver shift implementation;
- finite-difference order and dissipation;
- outer-boundary condition and causal distance during the run;
- transition into any frozen-spacetime/Cowling phase.

Minimum diagnostics:

- volume-weighted and maximum Hamiltonian constraint;
- momentum-constraint norms;
- Z4 constraint norm;
- apparent-horizon area, irreducible mass, angular momentum and spin;
- gravitational-wave multipoles through collapse.

## GRMHD sector

Conservative variables must map unambiguously to primitive fields and metric conventions. Record:

- densitisation convention;
- reconstruction variables and limiter;
- HLLD fallback ladder;
- primitive-recovery tolerances and failure actions;
- equation-of-state inversion tolerances;
- constrained-transport staggering and EMF construction;
- floor injections in mass, energy and momentum units.

Minimum diagnostics:

- total baryon mass and budget decomposition;
- disk mass outside the horizon;
- horizon accretion rate;
- magnetic energy by region;
- divergence-error norm;
- MRI quality factors \(Q_\theta\) and \(Q_\phi\);
- Maxwell and Reynolds stresses and effective \(\alpha\).

## Neutrino sector

Record species definitions, energy integration assumptions, closure, source-term integrator, opacity interpolation, treatment in optically thick/thin limits and coupling to electron fraction.

Minimum diagnostics:

- luminosity by species and extraction radius;
- mean energy if represented;
- optical-depth distribution;
- fluid-radiation energy and lepton-number exchange budgets;
- cooling time relative to orbital time in the disk.

## Jet and ejecta sector

A jet is not merely a coloured polar feature. The analysis must report at multiple radii:

- outward electromagnetic energy flux;
- matter energy flux;
- magnetisation \(\sigma=b^2/\rho\) in a declared unit convention;
- energy-per-baryon proxy and baryon loading;
- opening angle containing fixed fractions of Poynting luminosity;
- north/south luminosities separately;
- unbound mass using both geodesic and Bernoulli criteria;
- ejecta velocity and electron-fraction distributions.

All surface integrals must state coordinate radius, proper measure, masks and sign conventions.
