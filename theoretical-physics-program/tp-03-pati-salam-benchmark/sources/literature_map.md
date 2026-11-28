# TP-03 literature and provenance map

This file separates established ingredients from the project’s independent calculations.

| Source | Role in TP-03 | Boundary |
|---|---|---|
| J. C. Pati and A. Salam, *Lepton Number as the Fourth Color*, Phys. Rev. D 10, 275 (1974), DOI `10.1103/PhysRevD.10.275` | Original quark–lepton \(SU(4)\) framework and characteristic vector-leptoquark structure. | Does not supply the `PS1-MM` potential or its invariant count. |
| E. Witten, *An SU(2) Anomaly*, Phys. Lett. B 117, 324 (1982), DOI `10.1016/0370-2693(82)90728-6` | Global \(SU(2)\) parity gate. | The project independently counts the four doublets per \(SU(2)\) factor. |
| C. S. Aulakh and A. Girdhar, *SO(10) a la Pati-Salam*, Int. J. Mod. Phys. A 20, 865 (2005), arXiv `hep-ph/0204097`, DOI `10.1142/S0217751X0502001X` | Tensor decompositions and Pati–Salam Clebsch conventions, including the \((10,1,3)\) daughter of the \(126\). | TP-03 is a standalone Pati–Salam benchmark and does not assume a complete \(SO(10)\) parent. |
| K. S. Babu and R. N. Mohapatra, *Predictive Neutrino Spectrum in Minimal SO(10) Grand Unification*, Phys. Rev. Lett. 70, 2845 (1993), arXiv `hep-ph/9209215` | Established use of \(10_H\) and \(126_H\) doublets to repair quark–lepton mass relations and generate Majorana masses. | The Phase 1 algebraic inverse and the Phase 2B vacuum theorem are independent calculations. |
| K. S. Babu and S. Khan, *A Minimal Non-Supersymmetric SO(10) Model: Gauge Coupling Unification, Proton Decay and Fermion masses*, Phys. Rev. D 92, 075018 (2015), arXiv `1507.06712` | Primary precedent that threshold predictions require a fully specified Higgs potential and complete scalar spectrum. | Its \(54_H+126_H+10_H\) potential is not copied into `PS1-MM`; the present 138-parameter count concerns the standalone complex Pati–Salam field set. |
| TP-00, `../tp-00-gr-sm-frontier-model/` | Governing non-aggregation rule and gates for anomalies, vacuum stability, recovery, flavour, proton stability and cosmology. | TP-00 supplies acceptance criteria, not a Pati–Salam result. |
| S. Weinberg, *Effective Gauge Theories*, Phys. Lett. B 91, 51 (1980); L. J. Hall, *Grand Unification of Effective Gauge Theories*, Nucl. Phys. B 178, 75 (1981) | Standard 1-loop \(\overline{\rm MS}\) gauge-coupling threshold matching formula. | Applied directly to the explicit Phase 2B/3 9-vector + 175-scalar `PS1-EW` spectrum with verified UV–IR sum rules. |
| M. E. Machacek and M. T. Vaughn, *Two-Loop Renormalization Group Equations in a General Quantum Field Theory*, Nucl. Phys. B 222, 83 (1983) | General 2-loop gauge beta-function formula. | Evaluated independently for complex `PS1` to obtain \(b^{\rm PS1}, B^{\rm PS1}\) and verified via \(\dim(G_i)B_{ij}=\dim(G_j)B_{ji}\). |
| D. Buttazzo et al., *Investigating the near-criticality of the Higgs boson*, JHEP 12 (2013) 089, arXiv `1307.3536` | 2-loop SM \((g_i, y_t, \lambda_H)\) beta functions and matching at \(\mu=M_t\) for the SM Higgs instability scale \(\mu_{\rm inst}\simeq 9\times 10^9\text{ GeV}\). | Used as the frozen SM stability baseline for the `PS1-EW` radial-\(\Delta_R\) threshold stabilization condition. |
| G. Valencia and S. Willenbrock, *Quark–lepton unification and rare meson decays*, Phys. Rev. D 50, 6843 (1994); A. D. Smirnov, Mod. Phys. Lett. A 22, 2353 (2007) & 33, 1850019 (2018) | Chiral-enhanced vector-leptoquark \(X_\mu\) amplitude for \(K_L \to \mu^\pm e^\mp\) and \(B_s \to \mu^\pm e^\mp\). | Evaluated on the actual fitted `PS1-EW` quark–lepton mixing matrices \(K_L, K_R\) as well as generic \(\mathcal{O}(1)\) mixing. |
| S. Davidson and A. Ibarra, *A lower bound on the right-handed neutrino mass from leptogenesis*, Phys. Lett. B 535, 25 (2002); L. Covi, E. Roulet, F. Vissani, Phys. Lett. B 384, 169 (1996) | Unflavored Type-I thermal leptogenesis CP asymmetry \(\epsilon_1\) and Davidson–Ibarra mass bound \(M_{R1}\gtrsim 10^9\text{ GeV}\). | Combined with the \(\pi_2(G_{\rm PS}/G_{\rm SM})=\mathbb{Z}\) monopole bound \(T_{\rm rh} < v_R\) across `BM-LR`, `BM-GUT`, `BM-LOW`. |
| G.-y. Huang and S. Zhou, *Precise Values of Running Quark and Lepton Masses in the Standard Model*, Phys. Rev. D 103, 016010 (2021), arXiv `2009.04851`; NuFIT 5.3 (2024); PDG (2024/2026) | Frozen \(\overline{\rm MS}\) fermion mass, CKM, neutrino oscillation, and rare-decay input baselines at \(\mu = M_Z\). | Sourced experimental inputs only; all RG running and Pati–Salam fits are project calculations. |

## Independent Phase 2B and Phase 3 contributions

The following results are project calculations:

1. the exact multigraded Molien–Weyl count \(N_2=7,N_3=0,N_4=131\);
2. the 138-parameter non-predictivity conclusion for gauge-only complex `PS1`;
3. the `PS1-MM` moment-map potential;
4. the global coherent-orbit minimum theorem;
5. the complete \(60\times60\) \(\Delta_R\) Hessian and multiplet spectrum;
6. the explicit Goldstone-orbit and heavy-vector verification;
7. the explicit 16-operator gauge-invariant `PS1-EW` bidoublet portal potential, vanishing theorem for \(\Delta_R^2\) portals, and full \(188\times 188\) one-light-Higgs Hessian verification;
8. the 2-loop complex `PS1` gauge beta matrix \(B^{\rm PS1}\), Weinberg–Hall threshold-matched \(SO(10)\) triple unification, and 60-component \(\Delta_R\) scalar Landau-pole audit;
9. the comparative three-generation fermion/CKM/PMNS/seesaw fits (`PS1-EW-min` real vs complex phase vs `PS1-EW-gen`) and flavour/baryon/relic audit across `BM-LR`, `BM-GUT`, and `BM-LOW`.

These results require independent specialist review before publication.
