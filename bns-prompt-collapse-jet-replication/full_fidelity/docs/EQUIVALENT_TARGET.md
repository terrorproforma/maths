# E-track independent-equivalence contract

E-track asks a stronger scientific question than visual reproduction: does an independent implementation of the same physical model produce the same remnant and jet phenomenology?

## Continuum system to match

### Dynamical spacetime

Evolve a 3+1 decomposition of Einstein’s equations with a constraint-damped Z4c/BSSN-family formulation and moving-puncture gauge. The implementation must expose Hamiltonian and momentum constraints, apparent-horizon quantities and gauge diagnostics.

### Ideal general-relativistic magnetohydrodynamics

Evolve baryon number, stress-energy and induction equations:

\[
\nabla_\mu (\rho u^\mu)=0,
\qquad
\nabla_\mu T^{\mu\nu}=Q^\nu_{\nu},
\qquad
\nabla_\mu {{}^*F}^{\mu\nu}=0,
\]

with

\[
T^{\mu\nu}=(\rho h+b^2)u^\mu u^\nu
+\left(p+\frac{b^2}{2}\right)g^{\mu\nu}-b^\mu b^\nu.
\]

The magnetic field must remain divergence-free to the solver’s declared discrete tolerance. Primitive recovery, atmosphere treatment and magnetisation caps are part of the physical-numerical model and must be logged.

### Composition and finite-temperature nuclear EOS

Evolve electron fraction with source terms and close the fluid with the same finite-temperature SFHo table and interpolation conventions as X-track. Match table extrapolation, low-temperature extension, thermodynamic consistency and units.

### Neutrino radiation

Use gray two-moment transport for the species grouping used by the target, with an M1 closure and matched emission, absorption, scattering and leakage/source terms. The interaction four-force must be coupled consistently to fluid energy-momentum and lepton number.

## Discretisation equivalence

It is not necessary to copy SACRA-MPI internals, but it is necessary to demonstrate that differences do not control the answer. The independent solver must document:

- spatial and temporal order in smooth regions;
- reconstruction and Riemann solver;
- constrained-transport or divergence-control scheme;
- metric-fluid coupling and AMR subcycling;
- prolongation/restriction at refinement boundaries;
- neutrino closure and stiff-source integration;
- apparent-horizon finder and excision/puncture handling;
- floor/reset accounting as conserved budgets.

## Statistical/turbulent equivalence

MRI turbulence makes pointwise field identity the wrong target. E-track comparison uses:

- resolution sequences;
- seed-amplitude/topology perturbations that remain in the same physical regime;
- time-windowed means and quantiles;
- integrated budgets and spectra;
- launch-time distributions and hemispheric asymmetry;
- morphology metrics only after physical diagnostics pass.

A single aesthetically convincing movie is not evidence of E-track equivalence.
