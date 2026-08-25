---
title: "Production-Theory Closure of the PT/BFM-Constrained Three-Loop 3PI Pilot"
subtitle: "Exact topology ledger, complete thermal tensor spaces, counterterm closure basis, analytic benchmark hierarchy, and preregistered observable contract"
author: "Angus Muffatti"
date: "24 August 2026"
geometry: margin=0.72in
fontsize: 10pt
toc: true
numbersections: true
colorlinks: true
linkcolor: blue
urlcolor: blue
header-includes:
  - \usepackage{amsmath,amssymb,mathtools}
  - \usepackage{booktabs,longtable,array}
  - \usepackage{microtype}
  - \setlength{\parindent}{0pt}
  - \setlength{\parskip}{5pt plus 1pt minus 1pt}
  - \renewcommand{\arraystretch}{1.13}
---

# Executive verdict

The five residual theory tasks identified after v1.8 are complete:

1. the exact generic three-loop 3PI diagram ledger is frozen;
2. the finite-temperature tensor spaces are complete for the declared symmetry class;
3. every local counterterm, composite insertion and initial-surface signature required by power counting is mapped;
4. the analytic and reduced-numerical benchmark hierarchy is frozen;
5. the physical-observable and error contract is preregistered.

\[
\boxed{12/12\ \text{preflight checks passed}},
\qquad
\boxed{10/10\ \text{unit tests passed}}.
\]

\[
\boxed{\text{PASS FOR UNIT TEST AND PILOT}}
\]

This is not an unconditional production pass. A finite non-Abelian 3PI truncation is not guaranteed to preserve gauge identities or possess a conventional all-order renormalization proof. The pilot tests those properties through Ward, Slavnov-Taylor, Nielsen, cutoff, KMS, conservation and gauge-singlet spectral gates.

The v1.8 package already supplied the matched retarded benchmark, seed STI closure, singlet ladder and executable solver specification. The present work removes the remaining ambiguity in what equations, tensor components, counterterms, limits and observables the pilot means.

# Frozen scope

The high-temperature electroweak-symmetric portal is

\[
\mathcal L_Y=-y_D\,\overline Q_L H D_R+\mathrm{h.c.},
\]

coupled to \(SU(3)_c\times SU(2)_L\times U(1)_Y\), with vectorlike colored singlet \(D\). The temperature anchor is \(T=1.002\times10^8\,\mathrm{GeV}\).

Dynamical two-point functions:

\[
G_H,S_Q,S_D,D_g,D_W,D_B,G_{c_3},G_{c_2}.
\]

Dynamical three-point vertices include portal, matter-gauge, scalar-gauge, three-gauge and gauge-ghost families. Four-point vertices remain at renormalized classical values at this truncation order, with their counterterms retained.

# Exact three-loop 3PI functional

\[
\Gamma_2=\Gamma_2^0+\Gamma_2^{\rm int}.
\]

\[
\begin{aligned}
\Gamma_2^0={}&-\frac18D^2V_4^0+\frac{i}{6}D^3V_3V_3^0-iD\Delta^2UU_0
+\frac{i}{24}D^4V_4V_4^0+\frac18D^5V_3^2V_4^0,\\
\Gamma_2^{\rm int}={}&-\frac{i}{12}D^3V_3^2+\frac{i}{2}D\Delta^2U^2-\frac{i}{48}D^4V_4^2
-\frac{i}{24}D^6V_3^4+\frac{i}{3}D^3\Delta^3U^3V_3+\frac{i}{4}D^2\Delta^4U^4.
\end{aligned}
\]

All contour signs and multiplicities are carried by superfield tensors. The ledger contains **11** unique generic topologies; every row passes \(L=I-V+1\).

## Why the ledger matters

Self-energies, dynamical vertices and the singlet Bethe-Salpeter kernel must be differentiated from one functional. Independent coding risks double counting and breaks the conserving relation

\[
K=\frac{\delta\Sigma_H}{\delta G_H}.
\]

## Frozen topology summary

| ID | L | Coefficient | Topology |
| --- | --- | --- | --- |
| G20_B4_BARE | 2 | -1/8 | bosonic double-bubble/seagull |
| G20_B33_MIX | 2 | +i/6 | bosonic sunset with one dressed and one bare cubic vertex |
| G20_F3_MIX | 2 | -i | Grassmann sunset with one dressed and one bare boson-Grassmann vertex |
| G30_B44_MIX | 3 | +i/24 | bosonic basketball with one dressed and one bare quartic vertex |
| G30_B334 | 3 | +1/8 | bosonic squint with two dressed cubics and one bare quartic |
| G2I_B33 | 2 | -i/12 | bosonic sunset with two dressed cubic vertices |
| G2I_F3 | 2 | +i/2 | Grassmann sunset with two dressed vertices |
| G3I_B44 | 3 | -i/48 | bosonic basketball with two dressed quartics |
| G3I_B3333 | 3 | -i/24 | bosonic tetrahedron/Mercedes with four dressed cubic vertices |
| G3I_FFFB | 3 | +i/3 | Grassmann triangle joined to a dressed bosonic cubic vertex |
| G3I_FFFF | 3 | +i/4 | Grassmann box with four dressed boson-Grassmann vertices |

# Complete tensor spaces

The state is homogeneous, CP-even and parity-even, with thermal four-velocity \(u^\mu\). Angular dependence is carried by spherical harmonics.

The complete Clifford basis has rank 16. A generic fermion-gauge vertex has

\[
64=16_L+48_T
\]

components. The STI fixes the longitudinal matrix sector; all 48 transverse components are dynamical. The measured transversality residual is \(1.556e-17\).

Other allocations:

- scalar/ghost-gauge vertex: one longitudinal plus three transverse components;
- chiral portal vertex: four projected matrices per orientation;
- matter-ghost kernel: all 16 Clifford components;
- three-gauge vertex: 27 fully transverse component tensors before Bose/color/permutation reduction.

The three-gauge transversality residual is \(4.445e-16\). These are storage component spaces, not counts of final independent physical scalar form factors.

# Renormalization closure

For the declared renormalizable theory and initial-state class, every local structure allowed by power counting and symmetries has a mapped counterterm or initial kernel. The superficial degree is

\[
\omega=4-d_I-n_B-n_c-\frac32n_F.
\]

The matrix contains **32** signatures and no missing entries.

The basis includes two-point, split three-point, Yukawa, quartic, truncation-longitudinal, composite-operator and initial-surface structures. For \(\mathcal O_H=H^\dagger H\), it includes operator renormalization, mixing and a local two-source contact term. The initial state includes \(\alpha_2,\alpha_3,\alpha_4\) prepared through an interacting imaginary-time leg plus a UV-soft finite deformation.

No free state-independent counterterm exists for an unaccompanied \(p<6\) harmonic. Persistence after selector/state charges vanish is a hard failure.

This is a power-counting and symmetry closure basis, not an all-order theorem for finite non-Abelian 3PI. Cutoff independence during evolution is the real test.

# Benchmark hierarchy

The frozen hierarchy covers free unequal-time normalization, equilibrium KMS, Abelian Ward, pure Yukawa, linear response, kinetic/AMY, narrow width, factorization-scale cancellation and conserving singlet BSE limits.

| Check | Result |
| --- | --- |
| Free equal-time spectral value | 0.000e+00 |
| Free commutator derivative error | 8.817e-13 |
| KMS residual | 1.474e-16 |
| Abelian Ward residual | 4.487e-16 |
| Finite-memory/Markov error | 7.919e-04 |
| Narrow-width area error | 7.639e-03 |

All current analytic checks pass.

# Observable and error contract

Claim-bearing quantities are limited to:

- Nielsen-stable complex poles;
- integrated matched portal rate;
- gauge-singlet \(H^\dagger H\) spectral density;
- conserved sector energy and gauge charges;
- downstream \(T_5/T_0\).

Conventional gauge-fixed off-shell elementary line shapes and individual ghost/longitudinal dressings are diagnostics.

Preregistered systematic scans cover momentum and angular resolution, timestep, memory, gauge parameter, separation scale, renormalization scale, tensor-basis size and truncation controls. Signed shifts and covariance are reported; broken identities are not error bars.

# Pilot configuration

\[
N_r=96,\qquad\ell_{\max}=4,\qquad N_t=4096,\qquad N_{\rm mem}=256.
\]

\[
\xi\in\{0,0.5,1,2\},\qquad q_*/T\in\{0.15,0.25,0.40\}.
\]

The package uses deterministic reductions in validation, HDF5 checkpoints and full double/complex-double precision.

# Validation

| Gate | Status |
| --- | --- |
| factorization_scale | PASS |
| on_shell_anchor | PASS |
| STI_seed | PASS |
| singlet_BSE | PASS |
| singlet_positivity | PASS |
| KMS_noise_positivity | PASS |
| diagram_ledger | PASS |
| fermion_vertex_basis | PASS |
| three_gauge_basis | PASS |
| counterterm_closure_basis | PASS |
| analytic_benchmarks | PASS |
| observable_contract | PASS |

All 12 preflight gates pass. The Python suite contains 10 tests; all pass without warnings.

# Production authorization

Unit and eight-GPU pilot runs are authorized. Production remains blocked until the pilot preserves simultaneously

\[
\boxed{\text{Ward/ST}+\text{Nielsen}+\text{KMS}+\text{conservation}+\text{cutoff/}q_*\text{ independence}+\text{singlet positivity}}.
\]

The pilot's central scientific question is whether the finite three-loop 3PI truncation maintains physical gauge consistency over long real-time evolution. No remaining small analytic exercise can settle that honestly.

# Final status

| Item | Status |
|---|---|
| Exact three-loop 3PI ledger | PASS |
| Complete component tensor spaces | PASS |
| Counterterm/initial-state closure basis | PASS FOR DECLARED TRUNCATION |
| Analytic benchmark hierarchy | PASS |
| Observable/error contract | PASS |
| Automated preflight | 12/12 PASS |
| Unit tests | 10/10 PASS |
| Pilot authorization | APPROVED |
| Production authorization | CONDITIONAL ON PILOT |
| All-order non-Abelian 3PI renormalization theorem | NOT CLAIMED |

The remaining uncertainty now sits inside the evolving non-Abelian correlator/vertex system, where it is measured by identities and physical controls rather than hidden in an ansatz.

# References

1. J. Berges, *n-Particle irreducible effective action techniques for gauge theories*, arXiv:hep-ph/0401172.
2. J. Berges, *Introduction to Nonequilibrium Quantum Field Theory*, arXiv:hep-ph/0409233.
3. U. Reinosa and J. Serreau, *2PI effective action for gauge theories: Renormalization*, arXiv:hep-th/0605023.
4. M. Garny and M. M. Muller, *Kadanoff-Baym Equations with Non-Gaussian Initial Conditions: The Equilibrium Limit*, arXiv:0904.3600.
5. S. Borsanyi and U. Reinosa, *Renormalized nonequilibrium quantum field theory: Scalar fields*, arXiv:0809.0496.
6. Project v1.8, *Pre-HPC Closure of the Gauge-Covariant q-D-H Portal*.

# Machine-readable deliverables

The package includes the topology ledger, vertex/tensor catalogues, counterterm matrix, solver specifications, observable contract, preflight driver, tests, launch checklist, acceptance matrix and checksums.
