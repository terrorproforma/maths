# TP-03 Phase 3 (`PS1-EW`) summary (post-referee revision)

\[
\boxed{
\begin{array}{c}
\textbf{188x188 heavy-spectrum Hessian at unbroken EW origin (9 Goldstones, 4 light Higgs, 175 heavy): PASS (EW-broken vacuum open).}\\
\textbf{Tree-level global Higgs+}\Delta_R\textbf{ stability at matched negative-portal BM-LR (}\lambda_{h\Delta}=-1.648\textbf{): FAIL (NP-02).}\\
\textbf{Gauge-only 2-loop perturbativity to }M_{\rm Pl}\textbf{: PASS (UV 2-loop Yukawa traces \& }M_{\rm GUT}\textbf{ parent thresholds omitted).}\\
\textbf{Phase 2B }\lambda_\Delta=2.0\textbf{ hits pure-self-coupling }136\lambda_\Delta^2\textbf{ pole at }1.787\,v_R\textbf{; rescaled }\lambda_\Delta=0.03\textbf{: PARTIAL (coupled scalar RGEs open).}\\
\textbf{PS1-EW-min (30 real Yukawa params vs 18 observables): existence witnesses PASS for real \& complex ratios at BM-LR and at }6\times 10^{11}\text{ GeV.}\\
\textbf{PS1-EW-gen (corrected tilde signs, }D=|\alpha_u|^2-|\alpha_d|^2\textbf{): PASS across BM-LR, BM-GUT, BM-LOW (direct contraction verified).}\\
\textbf{Valencia--Willenbrock }K_L\to\mu e\textbf{ aligned floor }v_R\gtrsim 3.78e+06\text{ GeV; }n\text{--}\bar{n}\text{/FCNC/}W_R\textbf{ preliminary (LAB-02 PARTIAL).}\\
\textbf{Cosmology: }\pi_2=\mathbb{Z}\textbf{ monopoles + }\pi_1=\mathbb{Z}_2\textbf{ strings require }T_{\rm rh}<v_R\textbf{; vanilla }N_1\textbf{ leptogenesis at BM-GUT falls short (COS-01 OPEN/PARTIAL).}
\end{array}
}
\]

## Key quantitative findings

1. **Exact $188\times 188$ bidoublet + $\Delta_R$ scalar Hessian (unbroken EW origin) & negative-portal obstruction:**
   - All **17** gauge-invariant quadratic and $\Delta_R^\dagger \Delta_R$ portal operators (**25 real parameters**) verify $SU(4)_C\times SU(2)_L\times SU(2)_R$ invariance to `7.37e-15`.
   - All $\Delta_R^2$ and $(\Delta_R^\dagger)^2$ cross-couplings vanish identically on $\langle\Delta_R\rangle$ (residual `0.00e+00`).
   - The linear map from the 25 real parameters to the 16 real Hermitian entries of $\mathcal{M}_H^2$ is **rank-16 surjective with a 9-dimensional kernel** (NOT a bijection); fixing the coloured blocks leaves 4 redundant directions fixed by convention.
   - At the one-light-Higgs surface (unbroken EW origin $\langle\Phi\rangle=0$), the $188\times 188$ Hessian has 9 exact Goldstones (orbit residual `2.45e-18`), 4 light SM Higgs doublet modes (eigenvector subspace error `4.44e-16`), and 175 strictly positive heavy physical modes (max spectrum error `3.33e-15`). Setting $\lambda_1 = -\mu_{\rm SM}^2$ gives the expected tachyonic EWSB curvature at the origin; full EW-broken vacuum verification remains open (`PERT-01` scoped to heavy spectrum).
   - **Tree-level global Higgs+$\Delta_R$ stability (`NP-02` = FAIL):** At the matched `BM-LR` criticality point, the effective Higgs–$\Delta_R$ portal is negative ($\lambda_{h\Delta} = -1.648 < 0$) and $\lambda_H^{\rm SM}(v_R) = -0.01122 < 0$. Along the physical coherent ray $r = -\lambda_{h\Delta} x / (2\lambda_{\rm eff}) = 49.95\,x > 0$, the quartic potential evaluates to $V_4(x, r) = (\lambda_H^{\rm UV} - \lambda_{h\Delta}^2/(4\lambda_{\rm eff})) x^2 = \lambda_H^{\rm SM}(v_R) x^2 = -0.01122\,x^2 < 0$ — **unbounded below at tree level**. Stabilizing requires $\lambda_H^{\rm SM}(v_R) > 0$, positive-portal $\lambda_{h\Delta} > 0$ copositivity, or radiative effective-potential stabilization.
   - Electroweak hierarchy fine-tuning is explicit: $\Delta_{\rm FT} = v_R^2 / \mu_{\rm SM}^2 \simeq 3.29e+23$ at `BM-LR`.

2. **Gauge-only 2-loop RGEs, thresholds, approximate $SO(10)$ crossing, and corrected $136\lambda_\Delta^2$ Landau pole:**
   - Exact complex `PS1` 1-loop gauge beta coefficients: $b_{4} = -7/3$, $b_{2L} = +2$, $b_{2R} = +26/3$. Above $v_R$, 2-loop UV Yukawa traces are omitted (gauge-only 2-loop PS RGEs + 1-loop Weinberg–Hall thresholds at $v_R$).
   - 1-loop (no thresholds): $v_R(g_{2R}=g_{2L}) = 5.078e+13$ GeV; approximate $SO(10)$ triple crossing $v_R^{\rm unif} = 3.153e+11$ GeV, $M_{\rm GUT} = 2.259e+16$ GeV ($\alpha_{\rm GUT}^{-1} = 37.10$).
   - Gauge-only 2-loop + 1-loop Weinberg–Hall thresholds (with rescaled $\Delta_R$ spectrum, no $M_{\rm GUT}$ parent thresholds): $v_R(g_{2R}=g_{2L}) = 4.682e+13$ GeV; approximate triple crossing $v_R^{\rm unif} = 7.322e+09$ GeV, $M_{\rm GUT} = 8.147e+16$ GeV ($\alpha_{\rm GUT}^{-1} = 31.05$).
   - **Corrected $\Delta_R$ 1-loop quartic beta function (`PERT-05` = PARTIAL):** With canonical real $r = \varphi^T\varphi/2$ and $V_4 = \lambda_\Delta (\varphi^T\varphi)^2/4$, $16\pi^2 \beta_{\lambda_\Delta} \supset 2(60+8)\lambda_\Delta^2 - 36\lambda_\Delta\kappa_4 - 16\lambda_\Delta\kappa_R = 136\lambda_\Delta^2 - 36\lambda_\Delta\kappa_4 - 16\lambda_\Delta\kappa_R$ (with $\kappa^2$, portal, gauge, and Yukawa terms omitted). Phase 2B's $\lambda_\Delta = 2.0$ hits its formal pure-self-coupling pole at `1.787 v_R`; Planck-scale starting caps are `0.0937` (`BM-LR`), `0.0547` (`BM-GUT`), and `0.0417` (`BM-LOW`). Rescaling to $\lambda_\Delta = 0.03, \kappa_4 = 0.006, \kappa_R = 0.0045$ ($\lambda_{\rm eff} = 0.0165$) stays below the pure-self-coupling cap at all three benchmarks; the full coupled 138-parameter scalar RGE system remains open.

3. **Fermion, CKM, neutrino, and PMNS existence fits (`REC-03` = PARTIAL):**
   - `PS1-EW-min` retains **30 real Yukawa parameters** after $U(3)_L\times U(3)_R$ basis removal vs **18 real flavour observables** — fits are existence/interpolation witnesses, NOT constrained predictions.
   - **Retracted exclusions:** Both the earlier real-ratio exclusion and the fixed-fit $7.7\times 10^{11}$ GeV floor were false. Explicit perturbative `PS1-EW-min` witnesses exist at `BM-LR` with **real** ratios ($c_d = 113.38, c_e = 28.37$, $\|Y_1\|_2 = 0.522$, $\|Y_{15}\|_2 = 0.571$, $\|f_R\|_2 = 0.1972$, err `5.87e-13`), at `BM-LR` with **complex** ratios ($\|Y_1\|_2 = 0.522$, $\|Y_{15}\|_2 = 0.566$, $\|f_R\|_2 = 0.0380$), and at the refit lower scale **$v_R = 6.0\times 10^{11}$ GeV** ($\|Y_1\|_2 = 0.565$, $\|Y_{15}\|_2 = 0.594$, $\|f_R\|_2 = 2.7986 < \sqrt{4\pi}$, err `4.84e-13`).
   - **Corrected `PS1-EW-gen` down-type tilde signs & seesaw basis:** With $\Phi = (\epsilon H_d^*, H_u)$ and $\widetilde{\Phi} = (\epsilon H_u^*, H_d)$, down-type tilde terms add with the same relative sign and the exact inverse has determinant $D = |\alpha_u|^2 - |\alpha_d|^2$ (verified directly against $2\times 2$ bidoublet tensor contraction to `< 2e-12`). All seesaw inversions use $m_\nu = U_{eL} m_\nu^\ell U_{eL}^T$ and directly recover all PMNS angles, $\delta_{\rm PMNS}$, and $\Delta m^2$ in the charged-lepton mass basis to `< 1e-12`. Recomputed `PS1-EW-gen` max Yukawa norms are `1.193` (`BM-LR`), `1.766` (`BM-GUT`), and `2.034` (`BM-LOW`).

4. **Flavour, baryon stability (`LAB-02` = PARTIAL), and cosmological relics (`COS-01` = OPEN / PARTIAL):**
   - Corrected Valencia–Willenbrock $K_L \to \mu^\pm e^\mp$ normalization ($1/(32\pi)$) sets the aligned lower bound $M_X \gtrsim 2.06e+06$ GeV ($v_R \gtrsim 3.78e+06$ GeV). All three benchmarks pass aligned/fitted $K_L \to \mu e$, $B_s \to \mu e$, and the updated MEG II $\mu \to e\gamma < 1.5\times 10^{-13}$ bound.
   - $W_R/Z_R$, heavy-Higgs FCNC, and $\Delta B = 2$ $n\text{--}\bar{n}$ (evaluated with actual lightest sextet mass $M_{\Delta_6} \in [0.11, 0.14]\,v_R$) are preliminary order-of-magnitude checks; pure PS preserves perturbative baryon number ($3B+L$) while gauged $B-L$ is broken by $\Delta(B-L)=2$.
   - Both $\pi_2(G_{\rm PS}/G_{\rm SM}) = \mathbb{Z}$ doubly-charged monopoles and $\pi_1(G_{\rm PS}/G_{\rm SM}) = \mathbb{Z}_2$ cosmic strings (from the disconnected stabilizer) arise at $v_R$, requiring $T_{\rm rh} < v_R$. At `BM-GUT`, vanilla $N_1$-dominated thermal leptogenesis yields $|\epsilon_1| = 7.45e-09$ ($\eta_B^{\max} \simeq 7.16e-12$), falling a factor of `85.3x` short of observed $\eta_B \simeq 6.1\times 10^{-10}$ (with $M_{R1} = 7.82e+08$ GeV).

All executable mathematical verification and obstruction-detection checks pass (`all_pass = True`), while TP-00 gates reflect honest fails/partials (`NP-02` = FAIL; `PERT-01`, `PERT-05`, `REC-03`, `LAB-02` = PARTIAL; `COS-01` = OPEN/PARTIAL).
