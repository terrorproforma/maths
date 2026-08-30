# X-track exact-replication contract

## Definition

“Exact” is reserved for a run whose executable and all physics-bearing inputs can be traced to immutable artifacts from the target calculation. Similar equations or the same named code are insufficient.

## Required immutable inputs

| Class | Required artifact | Why it matters |
|---|---|---|
| Solver | SACRA-MPI repository revision plus uncommitted patches | Numerical fluxes, prolongation, gauge, atmosphere and diagnostics are implementation-sensitive. |
| Toolchain | compiler/MPI versions, flags, linked libraries, target architecture | Floating-point contraction, reductions and vectorisation alter a chaotic turbulent trajectory. |
| Initial data | exact LORENE binary and generation parameter file | Constraint residuals, orbital eccentricity and stellar profiles seed the entire evolution. |
| EOS | exact finite-temperature SFHo table bytes and interpolation settings | Pressure, collapse time, disk thermodynamics and neutrino rates depend on table details. |
| Weak interactions | exact opacity/rate tables, species grouping and interpolation | Cooling, electron fraction and baryon loading of the funnel are sensitive to these choices. |
| Magnetic seed | vector-potential prescription, pressure cutoff, exponent and normalisation | MRI onset and large-scale flux accumulation depend on seed topology and amplitude. |
| Mesh | every level extent, spacing, moving-box rule, symmetry and boundary condition | Effective MRI quality factors and ejecta propagation depend on the hierarchy. |
| Floors | atmosphere reset, density/temperature/Ye limits and magnetisation caps | Jet luminosity and polar baryon pollution can be floor-dominated. |
| Run history | checkpoints, restarts, Cowling transition and manual interventions | A long production run is a lineage, not just an input deck. |
| Analysis | exact extraction surfaces, unbound criteria, masks and smoothing | Published diagnostics cannot be compared if their definitions drift. |

## Exactness tiers

- **X0 — documentary:** paper/supplement parameters only.
- **X1 — source exact:** exact solver source and build environment, reconstructed inputs.
- **X2 — input exact:** exact source plus initial data, tables and full input deck.
- **X3 — lineage exact:** X2 plus checkpoint lineage, scheduler decomposition and intervention log.
- **X4 — bitwise attempt:** X3 on the original or faithfully emulated architecture and software stack.

The realistic scientific target is X3. X4 may fail despite perfect provenance because large MPI reductions and chaotic turbulence are not generally bitwise portable. Failure of bitwise identity is not failure of physical replication; it must, however, be measured rather than waved away.

## Acceptance conditions

1. `bnsjet freeze-provenance` records hashes for every declared artifact.
2. No unresolved artifact marked as blocking X-track remains.
3. Canonical tests pass on the frozen executable.
4. At least three production resolutions are run, including the target 150 m finest spacing.
5. Constraint norms and magnetic-divergence errors remain within declared bounds.
6. Horizon, disk, ejecta, neutrino and jet diagnostics match the target within the convergence/turbulence envelope in `VALIDATION_MATRIX.md`.
7. Rendering is regenerated from volumetric fields with a documented transfer function.
