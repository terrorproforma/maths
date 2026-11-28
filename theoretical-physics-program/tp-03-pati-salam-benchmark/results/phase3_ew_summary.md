# TP-03 Phase 3 (`PS1-EW`) summary

\[
\boxed{
\begin{array}{c}
\textbf{Full 188x188 PS1-EW Higgs-mixing Hessian (9 Goldstones, 4 light Higgs, 175 heavy): PASS.}\\
\textbf{2-loop gauge perturbativity to }M_{\rm Pl}\textbf{ across }v_R\in[10^5,10^{16}]\text{ GeV}\textbf{: PASS.}\\
\textbf{Phase 2B } \lambda_\Delta=2.0 \textbf{ hits scalar Landau pole at } 3.2\,v_R \textbf{; rescaled } \lambda_\Delta=0.08 \textbf{: PASS.}\\
\textbf{PS1-EW-min (2 Dirac Yukawas): PASS at }v_R\gtrsim 8\times 10^{11}\text{ GeV (complex phase required); FAIL below.}\\
\textbf{PS1-EW-gen (4 gauge-allowed Yukawas): PASS across entire }v_R\in[4.5\times 10^6,10^{16}]\text{ GeV window.}\\
\textbf{Flavour, baryon stability, and monopole-safe leptogenesis (BM-LR / BM-GUT): PASS (conditional on }T_{\rm rh}<v_R\textbf{).}
\end{array}
}
\]

## Key quantitative findings

1. **Exact $188\times 188$ bidoublet + $\Delta_R$ scalar Hessian:**
   - All 16 gauge-invariant quadratic and $\Delta_R^\dagger \Delta_R$ portal operators verify $SU(4)_C\times SU(2)_L\times SU(2)_R$ invariance to `7.37e-15`.
   - All $\Delta_R^2$ and $(\Delta_R^\dagger)^2$ cross-couplings vanish identically on the coherent vacuum $\langle\Delta_R\rangle$ (residual `0.00e+00`).
   - The $4\times 4$ colour-singlet doublet mass matrix $\mathcal{M}_H^2$ maps surjectively onto all 16 real Hermitian entries independently of the colour-octet ($\Omega_{1,2}$) and colour-triplet leptoquark ($\Sigma_{7/6}, \Sigma_{1/6}$) blocks via the $84$-channel $\Phi_{15}^2\Delta_R^\dagger\Delta_R$ and $15$-channel $\Phi_1\Phi_{15}\Delta_R^\dagger\Delta_R$ portals.
   - At the one-light-Higgs fine-tuning surface, the full $188\times 188$ Hessian has 9 exact Goldstones (orbit residual `4.91e-18`), 4 light SM Higgs doublet modes (eigenvector subspace error `6.66e-16`), and 175 strictly positive heavy physical modes (max spectrum error `3.11e-15`).
   - Electroweak hierarchy fine-tuning is explicit and unhidden: $\Delta_{\rm FT} = v_R^2 / \mu_{\rm SM}^2 \simeq 3.29e+23$ at `BM-LR` ($v_R = 5.08e+13$ GeV).

2. **Gauge RGEs, thresholds, triple unification, and scalar Landau poles:**
   - Exact complex `PS1` 1-loop gauge beta coefficients: $b_{4} = -7/3$, $b_{2L} = +2$, $b_{2R} = +26/3$.
   - Exact 1-loop (no thresholds) landmarks: $v_R(g_{2R}=g_{2L}) = 5.078e+13$ GeV; exact $SO(10)$ triple unification $v_R^{\rm unif} = 3.153e+11$ GeV, $M_{\rm GUT} = 2.259e+16$ GeV ($\alpha_{\rm GUT}^{-1} = 37.10$).
   - Exact 2-loop (with 1-loop Weinberg–Hall thresholds from the 9 heavy vectors + 175 heavy scalars) landmarks: $v_R(g_{2R}=g_{2L}) = 5.715e+13$ GeV; triple unification $v_R^{\rm unif} = 2.145e+10$ GeV, $M_{\rm GUT} = 5.129e+16$ GeV ($\alpha_{\rm GUT}^{-1} = 32.40$).
   - All three gauge couplings remain perturbative up to $M_{\rm Pl} = 1.22\times 10^{19}$ GeV at 2-loop for every scanned $v_R \in [10^{5.5}, 10^{16}]$ GeV.
   - **Scalar Landau pole obstruction in Phase 2B numerical certificate:** The 60-real-component $\Delta_R$ quartic has $16\pi^2 \beta_{\lambda_\Delta} \supset 68\lambda_\Delta^2$, so Phase 2B's $\lambda_\Delta = 2.0$ hits a scalar Landau pole at $3.2\,v_R$. Rescaling to $\lambda_\Delta = 0.08, \kappa_4 = 0.016, \kappa_R = 0.012$ ($\lambda_{\rm eff} = 0.044$) keeps the vacuum certified and perturbative up to $M_{\rm Pl}$ across all three benchmarks.
   - **SM Higgs quartic stability:** The 2-loop SM quartic $\lambda_H^{\rm SM}(\mu)$ crosses zero at $\mu_{\rm inst}^{(2\ell)} \simeq 9.04e+09$ GeV (so `BM-LOW` at $10^7$ GeV has $\lambda_H^{\rm SM} = +0.0212 > 0$). Above $\mu_{\rm inst}$, the radial $\Delta_R$ threshold shift $\Delta\lambda_H = -\lambda_{h\Delta}^2 / (4\lambda_{\rm eff})$ stabilizes $\lambda_H^{\rm UV}(v_R) > 0$ for $|\lambda_{h\Delta}| > 0.044$ at `BM-LR` ($\lambda_H^{\rm SM} = -0.0112$).

3. **Fermion, CKM, neutrino, and PMNS fits (`PS1-EW-min` vs `PS1-EW-gen`):**
   - **`BM-LR` ($v_R = 5.08e+13$ GeV):** `PS1-EW-min` with complex light-Higgs phase reproduces all 9 charged-fermion masses, 4 CKM observables, 2 neutrino $\Delta m^2$, and 3 PMNS angles to `4.95e-13` with perturbative couplings $\|Y_1\|_2 = 0.519$, $\|Y_{15}\|_2 = 0.576$, $\|f_R\|_2 = 0.0539$ and $M_R = (7.28e+09, 1.06e+12, 1.93e+12)$ GeV. By contrast, restricting `PS1-EW-min` to real Higgs-mixing ratios forces $\|f_R\|_2 = 6.54 > \sqrt{4\pi}$, violating perturbativity!
   - **`BM-GUT` ($v_R = 2.15e+10$ GeV):** `PS1-EW-min` fails $f_R$ perturbativity ($\|f_R\|_2 = 182.92 > \sqrt{4\pi}$), whereas the full gauge-invariant `PS1-EW-gen` reproduces all observables to `6.80e-15` with $\max \|Y\|_2 = 0.831$.
   - **`BM-LOW` ($v_R = 1.00e+07$ GeV):** `PS1-EW-gen` fits all observables perturbatively ($\max \|Y\|_2 = 0.831$) with $\lambda_H^{\rm SM}(v_R) > 0$, while `PS1-EW-min` is violently non-perturbative and hierarchical thermal leptogenesis is closed below $v_R$.

4. **Flavour, baryon stability, and cosmological relics:**
   - Generic $O(1)$ quark–lepton mixing in $K_L \to \mu^\pm e^\mp$ sets $M_X \gtrsim 2.43e+06$ GeV ($v_R \gtrsim 4.49e+06$ GeV). All three benchmarks pass $K_L \to \mu e$, $B_s \to \mu e$, $\mu \to e\gamma$, $W_R/Z_R$, and heavy-Higgs FCNC bounds.
   - Pure Pati–Salam forbids $d=6$ gauge and scalar $\Delta B = 1$ proton decay; $n\text{--}\bar{n}$ oscillations vanish at tree level in `PS1-MM` by $U(1)_\Delta$ and pass $\tau_{n\bar{n}} > 4.7\times 10^8$ s at all three benchmarks even if $\lambda_{\Delta 4} = \mathcal{O}(1)$.
   - $\pi_2(G_{\rm PS}/G_{\rm SM}) = \mathbb{Z}$ guarantees doubly-charged Pati–Salam monopoles ($M_{\rm mon} \sim 15\,v_R$), requiring $T_{\rm rh} < v_R$ (monopole inflation). No $D$-parity domain walls exist because $\Delta_L$ is absent. Both `BM-LR` and `BM-GUT` leave an open monopole-safe thermal leptogenesis window $M_{R1} < T_{\rm rh} < v_R$.

All executable Phase 3 checks pass (`all_pass = True`).
