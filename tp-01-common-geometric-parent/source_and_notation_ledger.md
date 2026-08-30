# Source and notation ledger

## Freeze date and provenance

- Literature freeze: **2026-08-28**.
- Parent definitions and the weak/strong claim split are inherited from TP-01 v1.0.
- TP-00 gates are imported without aggregation.
- The motivating interview supplies only the phrase that Einstein-Hilbert and Chern-Simons/transgression might be daughter actions. It supplies no mathematical evidence.

## Epistemic labels

- **Established result:** derived in the cited primary literature.
- **v1.0 input:** established in the preceding TP-01 package and rechecked where used.
- **v1.1 derivation:** new calculation or synthesis in this audit.
- **Inference:** conclusion obtained by combining established results and v1.1 calculations.

## Primary sources

| Key | Source | Persistent identifier | Use in v1.1 |
|---|---|---|---|
| BGH-1995 | M. Banados, L. J. Garay, M. Henneaux, *The local degrees of freedom of higher dimensional pure Chern-Simons theories* | arXiv:hep-th/9506187; DOI:10.1103/PhysRevD.53.593 | Primary/secondary constraints, symplectic rank, generic degree count. |
| BGH-1996 | M. Banados, L. J. Garay, M. Henneaux, *The dynamical structure of higher dimensional Chern-Simons theory* | arXiv:hep-th/9605159; DOI:10.1016/0550-3213(96)00384-7 | Dirac bracket, first/second-class split, boundary charges and torsion. |
| MTZ-2005 | O. Miskovic, R. Troncoso, J. Zanelli, *Canonical sectors of five-dimensional Chern-Simons theories* | arXiv:hep-th/0504055; DOI:10.1016/j.physletb.2005.04.043 | Generic/regular/canonical strata and irregularity warnings. |
| MOTZ-2006 | P. Mora, R. Olea, R. Troncoso, J. Zanelli, *Transgression forms and extensions of Chern-Simons gauge theories* | arXiv:hep-th/0601081; DOI:10.1088/1126-6708/2006/02/067 | Strict gauge invariance, boundary action and endpoint interpretations. |
| PSRV-2023 | P. Pais, P. Salgado-Rebolledo, A. Vera, *A note on the Hamiltonian structure of transgression forms* | arXiv:2309.16760; DOI:10.1007/JHEP12(2023)190 | Dirac algorithm with transgression boundary variations and charges. |
| CS-1974 | S.-S. Chern, J. Simons, *Characteristic forms and geometric invariants* | DOI:10.2307/1971013 | Integral characteristic-class and transgression foundations. |
| CH-1990 | A. H. Chamseddine, *Topological gauge theory of gravity in five and all odd dimensions* / even-dimensional reduction work | Nucl. Phys. B346 (1990) 213; Phys. Lett. B233 (1989) 291 | Odd-dimensional CS gravity and Phi F^n reduction ancestry. |
| MM-1977 | S. MacDowell, F. Mansouri, *Unified geometric theory of gravity and supergravity* | Phys. Rev. Lett. 38 (1977) 739 | Fixed-compensator Einstein daughter. |
| SW-1980 | K. Stelle, P. West, *Spontaneously broken de Sitter symmetry and the gravitational holonomy group* | Phys. Rev. D21 (1980) 1466 | Covariant constrained compensator escape route. |
| HOS-2005 | Y. Hosotani, *Dynamical Gauge Symmetry Breaking by Wilson Lines in the Electroweak Theory* | arXiv:hep-ph/0504272 | Wilson-line phase as the global compactification variable. |

## Conventions

| Symbol | Meaning |
|---|---|
| `G` | local gauge group `Spin(4,2)`; vector calculations use `so(4,2)` |
| `eta_hatAhatB` | `diag(-,+,+,+,+,-)` |
| `epsilon_012345` | `+1` |
| `M5` | five-dimensional operational parent spacetime |
| `M4 x S1_y` | compactification geometry, circle length `L_y=2 pi R` |
| `A`, `Abar` | endpoint connections of the relative transgression |
| `Theta` | `A-Abar` |
| `F` | `dA+A^2` |
| `g_abc` | rank-three invariant; in the vector basis `epsilon_ABCDEF` |
| `I,J,K,L` | four spatial indices on a Hamiltonian slice of the five-dimensional theory |
| `a,b,c` | gauge-algebra indices, `1,...,15` |
| `B_mu` | four-dimensional part of the compactified connection |
| `phi=A_y` | full adjoint circle zero mode |
| `Phi^A` | v1.0 coset/vector zero mode in the special endpoint ansatz |
| `H=J_54` | fixed holonomy generator |
| `W` | `P exp integral_S1 A_y dy`, defined up to conjugacy |
| `Omega_ab^{IJ}` | curvature-dependent CS symplectic matrix |
| `K_a` | secondary CS curvature constraint |
| `G_a` | Gauss first-class constraint |
| `H_I` | spatial-diffeomorphism first-class constraint |
| `c`, `xi` | internal-gauge and spatial-diffeomorphism ghosts |

## Numerical statement

The numerical witness solves only the algebraic phase-space conditions at one point. It is used to verify existence of a regular canonical stratum for the epsilon invariant. It is not labeled as a global spacetime solution, a perturbative vacuum, or an HPC simulation.
