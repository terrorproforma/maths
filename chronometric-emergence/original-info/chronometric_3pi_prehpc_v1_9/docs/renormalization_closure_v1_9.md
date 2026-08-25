# Renormalization and Initial-Surface Closure Specification - v1.9

**Author:** Angus Muffatti  
**Status:** Complete local basis for the declared pilot truncation  
**Date:** 24 August 2026

## Claim and limitation

Every local ultraviolet structure allowed by four-dimensional renormalizable power counting, the declared gauge and global symmetries, the composite control operator, and the selected initial-state class has a parameter or initial kernel in the pilot action.

This is **not** an all-orders proof of renormalizability for finite non-Abelian 3PI truncations. Finite nPI approximations can require truncation-specific counterterms and extra renormalization conditions. The pilot therefore retains split vertex counterterms, longitudinal diagnostic counterterms, cutoff scans and hard failure gates.

## Power counting

\[
\omega = 4-d_I-n_B-n_c-\frac32n_F.
\]

Every required signature with \(\omega\ge0\), plus composite-contact and initial-surface structures, is mapped.

## Closure classes

| Closure class | Entries | External signatures |
| --- | --- | --- |
| bulk two-point | 8 | A_SU3 A_SU3; A_SU2 A_SU2; A_U1 A_U1; cbar_SU3 c_SU3; cbar_SU2 c_SU2; Hdag H; Qbar Q; Dbar D |
| bulk three-point split vertex | 11 | A_SU3 A_SU3 A_SU3; A_SU3 cbar_SU3 c_SU3; A_SU2 A_SU2 A_SU2; A_SU2 cbar_SU2 c_SU2; A_SU3 Qbar Q; A_SU2 Qbar Q; A_U1 Qbar Q; A_SU3 Dbar D; A_U1 Dbar D; A_SU2 Hdag H; A_U1 Hdag H |
| bulk Yukawa vertex | 1 | H Qbar D plus h.c. |
| bulk four-point bare-at-3PI | 6 | A3^4; W^4; W^2 Hdag H; B^2 Hdag H; W B Hdag H; (Hdag H)^2 |
| composite operator | 1 | O_H = Hdag H insertion |
| composite contact | 1 | O_H O_H |
| initial surface | 2 | initial alpha_2; initial alpha_3 |
| initial correlation data | 1 | initial alpha_4 |
| exact selection rule | 1 | Z6 harmonic p<6 |

## Complete matrix

| External signature | Degree | Operator family | Counterterms | Class | Condition |
| --- | --- | --- | --- | --- | --- |
| A_SU3 A_SU3 | 2 | F_SU3_munu F_SU3^munu plus gauge-fixing longitudinal structures | delta_Z_A_SU3; delta_xi_SU3; delta_tr_L2_SU3 | bulk two-point | Transverse pole/residue and longitudinal STI condition at the subtraction point. |
| A_SU2 A_SU2 | 2 | F_SU2_munu F_SU2^munu plus gauge-fixing longitudinal structures | delta_Z_A_SU2; delta_xi_SU2; delta_tr_L2_SU2 | bulk two-point | Transverse pole/residue and longitudinal STI condition at the subtraction point. |
| A_U1 A_U1 | 2 | F_U1_munu F_U1^munu plus gauge-fixing longitudinal structures | delta_Z_A_U1; delta_xi_U1; delta_tr_L2_U1 | bulk two-point | Transverse pole/residue and longitudinal STI condition at the subtraction point. |
| cbar_SU3 c_SU3 | 2 | cbar D^2 c | delta_Z_c_SU3 | bulk two-point | Ghost residue at subtraction point. |
| cbar_SU2 c_SU2 | 2 | cbar D^2 c | delta_Z_c_SU2 | bulk two-point | Ghost residue at subtraction point. |
| Hdag H | 2 | \|D H\|^2 and Hdag H | delta_Z_H; delta_m_H2 | bulk two-point | Thermal-vacuum matched pole and residue. |
| Qbar Q | 1 | Qbar i slash D Q | delta_Z_Q | bulk two-point | Chiral fermion residue; no gauge-invariant Q mass. |
| Dbar D | 1 | Dbar i slash D D and M_D Dbar D | delta_Z_D; delta_M_D | bulk two-point | Vectorlike pole mass and residue. |
| A_SU3 A_SU3 A_SU3 | 1 | three-gauge vertex | delta_g_AAA_SU3 | bulk three-point split vertex | PT/BFM background coupling plus quantum STI matching. |
| A_SU3 cbar_SU3 c_SU3 | 1 | ghost-gauge vertex | delta_g_Acc_SU3 | bulk three-point split vertex | Taylor/STI subtraction condition. |
| A_SU2 A_SU2 A_SU2 | 1 | three-gauge vertex | delta_g_AAA_SU2 | bulk three-point split vertex | PT/BFM background coupling plus quantum STI matching. |
| A_SU2 cbar_SU2 c_SU2 | 1 | ghost-gauge vertex | delta_g_Acc_SU2 | bulk three-point split vertex | Taylor/STI subtraction condition. |
| A_SU3 Qbar Q | 0 | matter-gauge vertex | delta_g_AQQ_SU3 | bulk three-point split vertex | Background Ward and quantum STI conditions. |
| A_SU2 Qbar Q | 0 | matter-gauge vertex | delta_g_AQQ_SU2 | bulk three-point split vertex | Background Ward and quantum STI conditions. |
| A_U1 Qbar Q | 0 | matter-gauge vertex | delta_g_AQQ_U1 | bulk three-point split vertex | Background Ward and quantum STI conditions. |
| A_SU3 Dbar D | 0 | matter-gauge vertex | delta_g_ADD_SU3 | bulk three-point split vertex | Background Ward and quantum STI conditions. |
| A_U1 Dbar D | 0 | matter-gauge vertex | delta_g_ADD_U1 | bulk three-point split vertex | Background Ward and quantum STI conditions. |
| A_SU2 Hdag H | 1 | scalar-gauge vertex | delta_g_AHH_SU2 | bulk three-point split vertex | Scalar background Ward and quantum STI conditions. |
| A_U1 Hdag H | 1 | scalar-gauge vertex | delta_g_AHH_U1 | bulk three-point split vertex | Scalar background Ward and quantum STI conditions. |
| H Qbar D plus h.c. | 0 | y_D Qbar_L H D_R plus h.c. | delta_y_D | bulk Yukawa vertex | Symmetric Euclidean subtraction point or on-shell thermal matching. |
| A3^4 | 0 | A3^4 | delta_lambda_AAAA_SU3 | bulk four-point bare-at-3PI | Four-point amplitude at a symmetric subtraction point. |
| W^4 | 0 | W^4 | delta_lambda_AAAA_SU2 | bulk four-point bare-at-3PI | Four-point amplitude at a symmetric subtraction point. |
| W^2 Hdag H | 0 | W^2 Hdag H | delta_lambda_WWHH | bulk four-point bare-at-3PI | Four-point amplitude at a symmetric subtraction point. |
| B^2 Hdag H | 0 | B^2 Hdag H | delta_lambda_BBHH | bulk four-point bare-at-3PI | Four-point amplitude at a symmetric subtraction point. |
| W B Hdag H | 0 | W B Hdag H | delta_lambda_WBHH | bulk four-point bare-at-3PI | Four-point amplitude at a symmetric subtraction point. |
| (Hdag H)^2 | 0 | (Hdag H)^2 | delta_lambda_H | bulk four-point bare-at-3PI | Four-point amplitude at a symmetric subtraction point. |
| O_H = Hdag H insertion | 2 | Z_O O_H and mixing with identity/Hdag H | delta_Z_O; delta_c_O1; delta_c_OH | composite operator | Normalize the one-insertion vertex at the subtraction point. |
| O_H O_H | 0 | local J_O^2 contact term | delta_zeta_OO | composite contact | Subtracted singlet susceptibility/BSE correlator. |
| initial alpha_2 | boundary | vacuum/thermal-matched two-point initial kernel | delta_alpha2_species | initial surface | Match the interacting Euclidean-leg state at high momentum. |
| initial alpha_3 | boundary | initial cubic correlation kernels matching all retained V3/U channels | delta_alpha3_vertex_families | initial surface | Asymptote to interacting vacuum/thermal three-point functions. |
| initial alpha_4 | boundary | initial four-point correlations for V4 and BSE consistency | delta_alpha4_quartic_families | initial correlation data | UV difference from equilibrium must fall faster than the power-counting bound. |
| Z6 harmonic p<6 | forbidden without charge | exp(i p a/f_a) times compensating selector/state/spurion charge | no state-independent bulk counterterm | exact selection rule | Enforce Z6 covariance and epsilon spurion power counting. |

## Split counterterms

The implementation retains separate bookkeeping counterterms for propagators, background and quantum three-point vertices, the portal Yukawa vertex, classical quartics and finite-truncation longitudinal structures. Their differences must vanish with improved truncation and are reported as a systematic, not interpreted as new physical couplings.

## Composite operator

For \(\mathcal O_H=H^\dagger H\), the basis includes operator renormalization, identity/Higgs mixing and a local \(J_{\mathcal O}^2\) contact term. The same differentiated functional generates the self-energy and Bethe-Salpeter kernel.

## Initial surface

The pilot uses an interacting thermal imaginary-time leg plus a UV-soft finite deformation. It includes \(\alpha_2,\alpha_3,\alpha_4\). Abrupt production quenches are forbidden. Missing initial correlations are treated as a renormalization failure, not particle production.

## Exact cyclic/shift selection rule

An unaccompanied state-independent \(p<6\) harmonic has no free bulk counterterm. Any lower harmonic must carry selector, state or shift-spurion charge. Persistence after those charges vanish is a hard failure.

## Validation

- Closure rows: **32**
- Missing signatures: **0**
- Blank mappings: **0**
- Verdict: **PASS FOR PILOT**

## Production criterion

The evolved physical observables must become insensitive to cutoff, subtraction point, initialization and split-counterterm choices within the preregistered tolerances. Basis closure is necessary; cutoff independence is the actual renormalization test.
