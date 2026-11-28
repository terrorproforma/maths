# TP-03 Phase 3 (`PS1-EW`) — Electroweak Matching, RG Evolution, Fermion/Neutrino Fit, and Stability Audit

**Author:** Angus Muffatti  
**Project:** TP-03 — Complete Pati–Salam benchmark  
**Status:** **PHASE 3 AUDITED — PARTIAL / REVISED WITH SHARP OBSTRUCTIONS RECORDED**  
**Active branches:** `PS1-EW-min` (minimal 2-Dirac-Yukawa sub-branch) and `PS1-EW-gen` (full gauge-invariant 4-Dirac-Yukawa branch)

---

## 1. Terminal result (post-referee revision)

Extending the certified Phase 2B high-scale vacuum (`PS1-MM`) through electroweak matching, renormalisation-group evolution, three-generation fermion/neutrino existence fits, and flavour/baryon/relic audits — and incorporating a hostile theoretical-physics referee audit under the TP-00 non-aggregation rule (**"Fatal failures remain independent and cannot be averaged against attractive results"**) — yields a revised verdict with explicit fails, partials, and retracted overclaims:

\[
\boxed{
\begin{array}{c}
\textbf{188}\times\textbf{188 heavy-spectrum Hessian at unbroken EW origin (9 Goldstones, 4 light Higgs, 175 heavy): PASS (EW-broken vacuum open).}\\
\textbf{Tree-level global Higgs+}\Delta_R\textbf{ stability at matched negative-portal BM-LR (}\lambda_{h\Delta}=-1.648\textbf{): FAIL (NP-02).}\\
\textbf{Gauge-only 2-loop perturbativity to }M_{\rm Pl}\textbf{: PASS (2-loop UV Yukawa traces \& }M_{\rm GUT}\textbf{ parent thresholds omitted).}\\
\textbf{Phase 2B }\lambda_\Delta=2.0\textbf{ hits pure-self-coupling }136\lambda_\Delta^2\textbf{ pole at }1.787\,v_R\textbf{; rescaled }\lambda_\Delta=0.03\textbf{: PARTIAL (coupled scalar RGEs open).}\\
\textbf{PS1-EW-min (30 real Yukawa params vs 18 observables): existence witnesses PASS for real \& complex ratios at BM-LR and at }6\times 10^{11}\text{ GeV.}\\
\textbf{PS1-EW-gen (corrected tilde signs, }D=|\alpha_u|^2-|\alpha_d|^2\textbf{): PASS across BM-LR, BM-GUT, BM-LOW (direct contraction verified).}\\
\textbf{Valencia--Willenbrock }K_L\to\mu e\textbf{ aligned floor }v_R\gtrsim 3.78\times 10^6\text{ GeV; }n\text{--}\bar{n}\text{/FCNC/}W_R\textbf{ preliminary (LAB-02 PARTIAL).}\\
\textbf{Cosmology: }\pi_2=\mathbb{Z}\textbf{ monopoles + }\pi_1=\mathbb{Z}_2\textbf{ strings require }T_{\rm rh}<v_R\textbf{; vanilla }N_1\textbf{ leptogenesis at BM-GUT falls short (COS-01 OPEN/PARTIAL).}
\end{array}
}
\]

### Summary of Referee Corrections and Honest Obstructions
1. **Corrected $O(60)$ $\Delta_R$ quartic beta coefficient ($68 \to 136$):** With canonical real $r = \varphi^T\varphi/2$ and $V_4 = \lambda_\Delta(\varphi^T\varphi)^2/4$, $16\pi^2\beta_{\lambda_\Delta} \supset 2(60+8)\lambda_\Delta^2 - 36\lambda_\Delta\kappa_4 - 16\lambda_\Delta\kappa_R = 136\lambda_\Delta^2 - 36\lambda_\Delta\kappa_4 - 16\lambda_\Delta\kappa_R$ ($\kappa^2$, portal, gauge, and Yukawa terms omitted). Phase 2B's $\lambda_\Delta = 2.0$ hits its formal pure-self-coupling pole at $1.787\,v_R$; the rescaled benchmark is lowered to $\lambda_\Delta = 0.03, \kappa_4 = 0.006, \kappa_R = 0.0045$ ($\lambda_{\rm eff} = 0.0165$), below the pure-self-coupling Planck starting cap at all three benchmarks (`0.0937`, `0.0547`, `0.0417`), while the full coupled 138-parameter scalar RGE system remains open (`PERT-05` = PARTIAL).
2. **Tree-level Higgs+$\Delta_R$ unbounded-below failure at matched `BM-LR` (`NP-02` = FAIL):** At the matched `BM-LR` criticality point, $\lambda_{h\Delta} = -1.648 < 0$ and $\lambda_H^{\rm SM}(v_R) = -0.01122 < 0$. Along the physical coherent ray $r = -\lambda_{h\Delta} x / (2\lambda_{\rm eff}) = 49.95\,x > 0$, $V_4(x,r) = \lambda_H^{\rm SM}(v_R) x^2 = -0.01122\,x^2 < 0$ — **unbounded below at tree level**. The earlier tree-level stabilization claim for negative portal is retracted.
3. **Corrected `PS1-EW-gen` down-type tilde signs & consistent charged-lepton seesaw basis:** With $\Phi = (\epsilon H_d^*, H_u)$ and $\tilde{\Phi} = \epsilon\Phi^*\epsilon^T = (\epsilon H_u^*, H_d)$, down-type tilde Yukawas add with the **same** relative sign (`+`), and the exact inverse has determinant $D = |\alpha_u|^2 - |\alpha_d|^2$ (singular at $|\alpha_u|=|\alpha_d|$), independently verified against direct $2\times 2$ tensor contraction. In the seesaw inversion, $Y_\nu^\ell = U_{eL}^\dagger Y_\nu^D$ requires $m_\nu = U_{eL} m_\nu^\ell U_{eL}^T$ (not $U_{eL}^* m_\nu^\ell U_{eL}^\dagger$), now verified via direct charged-lepton-basis PMNS round-trip recovery of all angles, $\delta_{\rm PMNS}$, and $\Delta m^2$.
4. **Retracted false exclusions in `PS1-EW-min` (`REC-03` = PARTIAL):** Both the earlier claim that real Higgs-mixing ratios fail perturbativity and the fixed-fit $7.7\times 10^{11}\text{ GeV}$ hard floor were false. Explicit perturbative witnesses exist at `BM-LR` with **real** ratios ($c_d = 113.38, c_e = 28.37, \|f_R\|_2 = 0.197$) and at $v_R = 6.0\times 10^{11}\text{ GeV}$ with refitted complex ratios ($\|f_R\|_2 = 2.80 < \sqrt{4\pi}$). Moreover, `PS1-EW-min` has **30 real Yukawa parameters** after $U(3)_L\times U(3)_R$ basis removal vs **18 real flavour observables**, making it an existence/interpolation test rather than a constrained prediction.
5. **Corrected flavour/cosmology scope (`LAB-02` = PARTIAL, `COS-01` = OPEN/PARTIAL):** The Valencia–Willenbrock $K_L \to \mu^\pm e^\mp$ width normalization is corrected to $\frac{1}{32\pi}$ ($M_X \gtrsim 2.06\times 10^6\text{ GeV}$, $v_R \gtrsim 3.78\times 10^6\text{ GeV}$); $\mu \to e\gamma$ is updated to MEG II ($1.5\times 10^{-13}$); $n\text{--}\bar{n}$ (with actual sextet masses $0.11\text{–}0.14\,v_R$), heavy-Higgs FCNC, and $W_R/Z_R$ are labelled as preliminary order-of-magnitude checks; $\pi_1(G_{\rm PS}/G_{\rm SM}) = \mathbb{Z}_2$ cosmic strings are recorded alongside $\pi_2 = \mathbb{Z}$ monopoles; and vanilla $N_1$-dominated thermal leptogenesis at `BM-GUT` is recorded as falling well short of observed $\eta_B$.

---

## 2. Complete $\Phi_1$–$\Phi_{15}$ High-Scale Bidoublet Mass Matrix and One-Light-Higgs Matching

### 2.1. Exact SM Decomposition of the 188 Real Scalar Modes

In `PS1`, the three independent complex multiplets are $\Phi_1(1,2,2)$ (8 real), $\Phi_{15}(15,2,2)$ (120 real), and $\Delta_R(10,1,3)$ (60 real). There is **no** $\Delta_L(10,3,1)$ in `PS1-MM` / `PS1-EW` (that belongs to the deferred parity branch `PS1P`), so Type-II seesaw is identically absent at tree level, and unbroken $SU(2)_L$ at $\mu = v_R$ forbids quadratic mixing between $\Delta_R$ and the bidoublets.

Writing $\Phi_1 = (\phi_{1d}, \, \phi_{1u})$ with $H_{1u} \equiv \phi_{1u} \sim (1,2)_{+1/2}$ and $H_{1d} \equiv -\epsilon \phi_{1d}^* \sim (1,2)_{+1/2}$ (where $\epsilon = i\sigma_2 = \begin{pmatrix}0&1\\-1&0\end{pmatrix}$, so $\Phi_1 = (\epsilon H_{1d}^*, H_{1u})$), and expanding $\Phi_{15} = \sqrt{2}\sum_{A=1}^{15} T^A \Phi_{15}^A$ with $T^{15} = \frac{1}{\sqrt{24}}\operatorname{diag}(1,1,1,-3)$, the 128 real bidoublet degrees of freedom decompose under $G_{\rm SM} = SU(3)_C \times SU(2)_L \times U(1)_Y$ into four independent Hermitian mass blocks:

| SM multiplet | Components | Mass-matrix dimension | Real d.o.f. |
|---|---|---:|---:|
| Colour-singlet Higgs doublets $(1,2)_{+1/2}$ | $\mathbf{H} = (H_{1u}, H_{1d}, H_{15u}, H_{15d})^T$ | $4\times 4$ Hermitian $\mathcal{M}_H^2$ | 16 |
| Colour-octet doublets $(8,2)_{+1/2}$ | $\mathbf{\Omega} = (\Omega_u, \tilde{\Omega}_d)^T$ | $2\times 2$ Hermitian $\mathcal{M}_\Omega^2$ | 64 |
| Triplet leptoquarks $(3,2)_{+7/6}$ | $\mathbf{\Sigma}_{7/6} = (\Sigma_{+7/6}, \tilde{\bar{\Sigma}}_{-7/6})^T$ | $2\times 2$ Hermitian $\mathcal{M}_{7/6}^2$ | 24 |
| Triplet leptoquarks $(3,2)_{+1/6}$ | $\mathbf{\Sigma}_{1/6} = (\Sigma_{+1/6}, \tilde{\bar{\Sigma}}_{-1/6})^T$ | $2\times 2$ Hermitian $\mathcal{M}_{1/6}^2$ | 24 |
| **Total bidoublet sector** | $\Phi_1 + \Phi_{15}$ | Block-diagonal | **128** |

Combined with the 60 real components of $\Delta_R$ (9 eaten Goldstones + 51 physical modes), all $128 + 60 = 188$ real scalar modes are accounted for.

### 2.2. Exact Vanishing of $\Delta_R^2$ Cross-Couplings and 17-Operator (25-Parameter) Portal Map

On the certified Phase 2B coherent vacuum
\[
\langle \Delta_R \rangle = \frac{v_R}{\sqrt{2}} |44\rangle_{\rm sym} \otimes |T_R^3 = +1\rangle,
\]
the tensor square $\langle \Delta_R \rangle \otimes \langle \Delta_R \rangle$ lies purely in $([4,0,0], 1, 5)$. Every $\Phi_{15}^2 \Delta_R^2$ and $\Phi_{15}\Phi_{15}^\dagger \Delta_R^2$ invariant in `invariant_coupling_basis.csv` couples through $[0,2,0]$ or $[2,1,0]$ and $j_R \le 1$, so **all $\Delta_R^2$ and $(\Delta_R^\dagger)^2$ bidoublet portals vanish identically on $\langle \Delta_R \rangle$** (machine residual `0.00e+00`).

Defining $(D_0)_a{}^b = \sum_{c,i} (\Delta_R)_{ac,i} (\Delta_R^\dagger)^{bc,i}$ and $(D_k)_a{}^b = \sum_{c,i,j} (\Delta_R^\dagger)^{bc,i} (t_3^k)_{ij} (\Delta_R)_{ac,j}$ (evaluating on $\langle\Delta_R\rangle$ to $D_0 = \frac{v_R^2}{2} P_4$ and $D_k = \frac{v_R^2}{2}\delta_{k3} P_4$), the declared gauge-invariant `PS1-EW` quadratic + portal Lagrangian contains **17 operators (9 real + 8 complex = 25 real parameters)**:
\[
\begin{aligned}
V_{\rm bi}^{(2)} + V_{\rm portal}
&= \mu_1^2 \operatorname{Tr}(\Phi_1^\dagger\Phi_1) + \big[\tilde{\mu}_1^2 \operatorname{Tr}(\tilde{\Phi}_1^\dagger\Phi_1) + \text{h.c.}\big]
 + \mu_{15}^2 \operatorname{Tr}(\Phi_{15}^\dagger\Phi_{15}) + \big[\tilde{\mu}_{15}^2 \operatorname{Tr}(\tilde{\Phi}_{15}^\dagger\Phi_{15}) + \text{h.c.}\big]\\
&\quad + \alpha_{1,0}\, r \operatorname{Tr}(\Phi_1^\dagger\Phi_1) + \alpha_{1,R}\sum_{k=1}^3 \mu_R^k \operatorname{Tr}(\Phi_1^\dagger\Phi_1\sigma_k)
 + \big[\tilde{\alpha}_{1,0}\, r \operatorname{Tr}(\tilde{\Phi}_1^\dagger\Phi_1) + \text{h.c.}\big]\\
&\quad + \alpha_{15,0}\, r \operatorname{Tr}(\Phi_{15}^\dagger\Phi_{15})
 + \alpha_{15,a}\operatorname{Tr}(\Phi_{15}^\dagger\Phi_{15} D_0) + \alpha_{15,b}\operatorname{Tr}(\Phi_{15}\Phi_{15}^\dagger D_0)\\
&\quad + \alpha_{15,c}\,\mathcal{O}_{15}^{(84)} + \alpha_{15,cR}\,\mathcal{O}_{15}^{(84,R)}
 + \big[\tilde{\alpha}_{15,c}\,\mathcal{O}_{15}^{(84,\rm hol)} + \text{h.c.}\big]\\
&\quad + \Big[\beta_0 \operatorname{Tr}(\Phi_1^\dagger\Phi_{15} D_0) + \beta_R \sum_k \operatorname{Tr}(\Phi_1^\dagger\Phi_{15}\sigma_k D_k)
 + \tilde{\beta}_0 \operatorname{Tr}(\tilde{\Phi}_1^\dagger\Phi_{15} D_0) + \tilde{\beta}_R \sum_k \operatorname{Tr}(\tilde{\Phi}_1^\dagger\Phi_{15}\sigma_k D_k) + \text{h.c.}\Big],
\end{aligned}
\]
where $\mathcal{O}_{15}^{(84)}, \mathcal{O}_{15}^{(84,R)}, \mathcal{O}_{15}^{(84,\rm hol)}$ project exclusively onto $|(\Phi_{15})_4{}^4|^2 = \frac{3}{4}|\Phi_{15}^{(15)}|^2$ and vanish identically on $\Omega, \Sigma_{7/6}, \Sigma_{1/6}$. All 17 operators verify $SU(4)_C\times SU(2)_L\times SU(2)_R$ invariance on random group transformations to relative error `7.37e-15`.

Evaluating on $\langle \Delta_R \rangle$ gives the exact $4\times 4$ Hermitian doublet mass matrix $\mathcal{M}_H^2$ in basis $(H_{1u}, H_{1d}, H_{15u}, H_{15d})^T$:
- $(\mathcal{M}_H^2)_{11,22} = \mu_1^2 + \frac{v_R^2}{2}(\alpha_{1,0} \mp \alpha_{1,R})$,
- $(\mathcal{M}_H^2)_{33,44} = M_{15,\rm bare}^2 + \frac{3v_R^2}{8}(\alpha_{15,a}+\alpha_{15,b}+\alpha_{15,c} \mp \alpha_{15,cR})$,
- $(\mathcal{M}_H^2)_{21} = 2\tilde{\mu}_1^2 + v_R^2 \tilde{\alpha}_{1,0}$, $\quad (\mathcal{M}_H^2)_{43} = 2\tilde{\mu}_{15}^2 + \frac{3}{4}v_R^2 \tilde{\alpha}_{15,c}$,
- $(\mathcal{M}_H^2)_{13} = c_{\rm mix}(\beta_0 - \beta_R)$, $\; (\mathcal{M}_H^2)_{42} = c_{\rm mix}(\beta_0+\beta_R)$, $\; (\mathcal{M}_H^2)_{23} = c_{\rm mix}(\tilde{\beta}_0 - \tilde{\beta}_R)$, $\; (\mathcal{M}_H^2)_{41} = c_{\rm mix}(\tilde{\beta}_0 + \tilde{\beta}_R)$ with $c_{\rm mix} = -\frac{\sqrt{3}}{4}v_R^2$.

**Exact map structure (retracting "bijection"):** The linear map from the **25 real parameters** of the 17 operators onto the **16 real entries** of $4\times 4$ Hermitian $\mathcal{M}_H^2$ is a **rank-16 surjective linear map with a 9-dimensional kernel** (verified directly via `portal_map_rank_and_nullity()`). Fixing the coloured blocks
\[
\mathcal{M}_\Omega^2 = \begin{pmatrix} M_{15,\rm bare}^2 & 2\tilde{\mu}_{15}^{2*} \\ 2\tilde{\mu}_{15}^2 & M_{15,\rm bare}^2 \end{pmatrix}, \qquad
\mathcal{M}_{7/6}^2 = \mathcal{M}_{1/6}^2 = \begin{pmatrix} M_{15,\rm bare}^2 + \frac{v_R^2}{2}\alpha_{15,a} & 2\tilde{\mu}_{15}^{2*} \\ 2\tilde{\mu}_{15}^2 & M_{15,\rm bare}^2 + \frac{v_R^2}{2}\alpha_{15,b} \end{pmatrix},
\]
fixes 5 real combinations ($M_{15,\rm bare}^2, \tilde{\mu}_{15}^2, \alpha_{15,a}, \alpha_{15,b}$), leaving 4 redundant directions fixed by convention ($\alpha_{1,0}=0.30, \alpha_{15,0}=0.40, \tilde{\alpha}_{1,0}=0$) in `solve_portal_parameters_for_light_higgs`.

### 2.3. One-Light-Higgs Fine-Tuning, Full $188\times 188$ Hessian at the Unbroken EW Origin, and EW-Broken Scope

Tuning the single determinant condition
\[
\det \mathcal{M}_H^2 = \lambda_1(\mathcal{M}_H^2)\, M_{H_2}^2 M_{H_3}^2 M_{H_4}^2, \qquad \lambda_1(\mathcal{M}_H^2) = -\mu_{\rm SM}^2 \simeq -(88.57\text{ GeV})^2,
\]
with $M_{H_{2,3,4}}^2 = (0.80, 1.20, 1.60)v_R^2$, $M_{\Omega_{1,2}}^2 = (1.10, 1.30)v_R^2$, and $M_{\Sigma_{7/6,1/6}}^2 = (1.40, 1.80)v_R^2$ isolates one light SM Higgs doublet $h \sim (1,2)_{+1/2}$ along any unit vector $u = (\alpha_{1u}, \alpha_{1d}, \alpha_{15u}, \alpha_{15d})^T \in \mathbb{C}^4$:
\[
H_{1u} = \alpha_{1u} h, \qquad H_{1d} = \alpha_{1d} h, \qquad H_{15u} = \alpha_{15u} h, \qquad H_{15d} = \alpha_{15d} h.
\]

Direct assembly of the full $188\times 188$ real scalar Hessian at the unbroken EW origin ($\langle\Phi\rangle=0$) for the rescaled `PS1-EW` quartic point ($\lambda_\Delta = 0.03, \kappa_4 = 0.006, \kappa_R = 0.0045, \lambda_{\rm eff} = 0.0165$) certifies:
- **9 exact zero Goldstone modes** matching the broken gauge orbit to `2.45e-18`;
- **4 degenerate light SM Higgs modes** matching the target eigenvector $u$ to subspace error `4.44e-16` (at probe $m_h^2 = 10^{-4}v_R^2$) and `3.33e-16` (at criticality $\det\mathcal{M}_H^2 = 0$);
- **175 strictly positive heavy physical real scalar modes** (lightest $\Delta_R$ mode $2\kappa_R = 0.009\,v_R^2$, sextets $(0.110\text{–}0.145)\,v_R$) matching the analytic multiplet formulas to `3.33e-15`.

**Scope limitation (`PERT-01`):** At $\lambda_1 = -\mu_{\rm SM}^2$, the light-Higgs doublet carries the expected tachyonic EWSB curvature at the unbroken EW origin $\langle\Phi\rangle=0$. Full EW-broken vacuum verification ($\langle h\rangle = v_{\rm EW}/\sqrt{2}$, including bidoublet self-quartics and $\langle\Delta_R\rangle$ backreaction) remains open; `PERT-01` is therefore scoped to the 175 heavy modes at the unbroken EW origin. Explicit EW hierarchy fine-tuning is $\Delta_{\rm FT} = v_R^2 / \mu_{\rm SM}^2 = 3.29\times 10^{23}$ (`BM-LR`), $6.83\times 10^{15}$ (`BM-GUT`), and $1.27\times 10^{10}$ (`BM-LOW`).

### 2.4. Exact Tree-Level Yukawa Matching (Corrected Down-Type Tilde Signs)

Because $\Phi_1$ and $\Phi_{15}$ are complex (non-self-dual), gauge invariance allows four renormalisable Dirac Yukawa matrices plus symmetric $f_R = f_R^T$:
\[
-\mathcal{L}_Y = F_L^T C (-\epsilon)\left(Y_1 \Phi_1 + \tilde{Y}_1 \tilde{\Phi}_1 + Y_{15}\Phi_{15} + \tilde{Y}_{15}\tilde{\Phi}_{15}\right)\epsilon F_R^c + \frac{1}{2} F_R^{c\,T} C f_R \Delta_R F_R^c + \text{h.c.}
\]
With $H_d = -\epsilon \phi_d^*$, direct matrix multiplication gives
\[
\Phi = (\epsilon H_d^*,\, H_u), \qquad \tilde{\Phi} = \epsilon \Phi^* \epsilon^T = (\epsilon H_u^*,\, H_d),
\]
so the down-column contributions of $\Phi$ and $\tilde{\Phi}$ **add with the same relative sign**. Writing $\hat{Y}_{15} \equiv Y_{15}/\sqrt{12}$ and $\tilde{\hat{Y}}_{15} \equiv \tilde{Y}_{15}/\sqrt{12}$, matching onto $h$ at $\mu = v_R$ yields:
\[
\begin{aligned}
Y_u &= \alpha_{1u} Y_1 + \alpha_{1d} \tilde{Y}_1 + \alpha_{15u} \hat{Y}_{15} + \alpha_{15d} \tilde{\hat{Y}}_{15}, &
Y_\nu^D &= \alpha_{1u} Y_1 + \alpha_{1d} \tilde{Y}_1 - 3\alpha_{15u} \hat{Y}_{15} - 3\alpha_{15d} \tilde{\hat{Y}}_{15}, \\
Y_d &= \alpha_{1d}^* Y_1 + \alpha_{1u}^* \tilde{Y}_1 + \alpha_{15d}^* \hat{Y}_{15} + \alpha_{15u}^* \tilde{\hat{Y}}_{15}, &
Y_e &= \alpha_{1d}^* Y_1 + \alpha_{1u}^* \tilde{Y}_1 - 3\alpha_{15d}^* \hat{Y}_{15} - 3\alpha_{15u}^* \tilde{\hat{Y}}_{15},
\end{aligned}
\]
with $M_R = \frac{1}{\sqrt{2}} f_R v_R$ and Type-I seesaw $m_\nu = -\frac{v_{\rm EW}^2}{2} Y_\nu^D M_R^{-1} (Y_\nu^D)^T$.

This defines two Yukawa sub-branches:
1. **`PS1-EW-gen` (Full gauge-invariant 4-Yukawa branch):** For $a = \alpha_u, b = \alpha_d$ and combinations $A_u = \frac{3Y_u+Y_\nu^D}{4}$, $A_d = \frac{3Y_d+Y_e}{4}$, $B_u = \frac{Y_u-Y_\nu^D}{4}$, $B_d = \frac{Y_d-Y_e}{4}$, the exact inverse has determinant $D_1 = |\alpha_{1u}|^2 - |\alpha_{1d}|^2$ and $D_{15} = |\alpha_{15u}|^2 - |\alpha_{15d}|^2$ (**singular whenever $|\alpha_u| = |\alpha_d|$**):
   \[
   Y_1 = \frac{\alpha_{1u}^* A_u - \alpha_{1d} A_d}{D_1}, \quad
   \tilde{Y}_1 = \frac{-\alpha_{1d}^* A_u + \alpha_{1u} A_d}{D_1}, \quad
   \hat{Y}_{15} = \frac{\alpha_{15u}^* B_u - \alpha_{15d} B_d}{D_{15}}, \quad
   \tilde{\hat{Y}}_{15} = \frac{-\alpha_{15d}^* B_u + \alpha_{15u} B_d}{D_{15}}.
   \]
   This forward and inverse system is independently verified against literal $2\times 2$ $SU(2)_L\times SU(2)_R$ tensor contractions in `verify_yukawa_forward_contraction()` to `< 2e-12` (and `< 1e-12` on generic random matrices).
2. **`PS1-EW-min` (Minimal 2-Yukawa sub-branch, $\tilde{Y}_1 = \tilde{Y}_{15} = 0$):** Eliminating $Y_1, \hat{Y}_{15}$ yields
   \[
   Y_u = c_d Y_d + c_e Y_e, \qquad Y_\nu^D = 3 c_e Y_d + (c_d - 2 c_e) Y_e,
   \]
   where $c_d = \frac{3r_1+r_{15}}{4}$, $c_e = \frac{r_1-r_{15}}{4}$, $r_1 = \alpha_{1u}/\alpha_{1d}^*$, $r_{15} = \alpha_{15u}/\alpha_{15d}^*$. **Parameter-count note:** Even in `PS1-EW-min`, $(Y_1, Y_{15}, f_R = f_R^T)$ contains $18 + 18 + 12 = 48$ real parameters; removing the $U(3)_L\times U(3)_R$ flavour basis ($18$ real) leaves **30 real Yukawa parameters** (plus $r_1, r_{15}$) against **18 real flavour observables**, so matching data is an existence/interpolation test rather than an overconstrained prediction.

---

## 3. Gauge-Only 2-Loop RGEs, Thresholds, Corrected $136\lambda_\Delta^2$ Landau Pole, and Tree-Level Higgs Stability Failure

### 3.1. Exact Complex `PS1` Gauge Beta Functions and Scope

For $3[F_L(4,2,1) + F_R^c(\bar{4},1,2)]$ plus complex $\Phi_1(1,2,2) + \Phi_{15}(15,2,2) + \Delta_R(10,1,3)$ in ordering $(SU(4)_C, SU(2)_L, SU(2)_R)$, the gauge-only 1-loop and 2-loop Machacek–Vaughn beta coefficients are:
\[
b^{\rm PS1} = \begin{pmatrix} -7/3 \\ +2 \\ +26/3 \end{pmatrix}, \qquad
B^{\rm PS1} = \begin{pmatrix}
2435/6 & 105/2 & 249/2 \\
525/2 & 73 & 48 \\
1245/2 & 48 & 779/3
\end{pmatrix}.
\]
The off-diagonal dimension-symmetry identity $\dim(G_i) B_{ij} = \dim(G_j) B_{ji}$ closes to machine precision (`0.0`). **Scope note:** Above $v_R$, 2-loop UV Yukawa traces are omitted (gauge-only 2-loop PS evolution + 1-loop Weinberg–Hall thresholds at $v_R$).

### 3.2. Weinberg–Hall 1-Loop Threshold Matching and Approximate $SO(10)$ Crossing

Using the 9 heavy real vectors ($X, W_R, Z_R$) and 175 heavy real physical scalars at $\lambda_\Delta = 0.03, \kappa_4 = 0.006, \kappa_R = 0.0045$, the 1-loop $\overline{\rm MS}$ matching satisfies all three UV–IR group-theory sum rules $\Delta b_i = b_i^{\rm UV} - b_i^{\rm SM}$ to `2.28e-15`.

| Regime | $v_R(g_{2R}=g_{2L})$ [GeV] | $v_R^{\rm cross}$ [GeV] | $M_{\rm GUT}$ [GeV] | $\alpha_{\rm GUT}^{-1}$ | $g_{\rm GUT}$ |
|---|---:|---:|---:|---:|---:|
| 1-loop, no thresholds | $5.078\times 10^{13}$ | $3.153\times 10^{11}$ | $2.259\times 10^{16}$ | $37.10$ | $0.5820$ |
| Gauge-only 2-loop + 1-loop Weinberg–Hall thresholds ($\lambda_\Delta=0.03$) | $4.682\times 10^{13}$ | $7.322\times 10^9$ | $8.147\times 10^{16}$ | $31.05$ | $0.6361$ |

Because rescaling $\kappa_4, \kappa_R$ lowers the $\Delta_R$ physical masses to $(0.11\text{–}0.14)\,v_R$, the approximate $SO(10)$ triple crossing shifts to $v_R = 7.322\times 10^9\text{ GeV}$, $M_{\rm GUT} = 8.147\times 10^{16}\text{ GeV}$. This is an **approximate gauge crossing without $M_{\rm GUT}$ parent-multiplet thresholds** (nor 2-loop UV Yukawa traces). All three gauge couplings remain perturbative up to $M_{\rm Pl}$ across $v_R \in [10^{5.5}, 10^{16}]\text{ GeV}$ ($\max g_i(M_{\rm Pl}) \le 0.88$).

### 3.3. Corrected $136\lambda_\Delta^2$ Beta Function (`PERT-05` = PARTIAL)

With canonical real components $\varphi \in \mathbb{R}^{60}$ ($r = \varphi^T\varphi/2$) and $V_4 = \lambda_\Delta (\varphi^T\varphi)^2 / 4 - \kappa_4 \sum_A (\mu_4^A)^2 - \kappa_R \sum_i (\mu_R^i)^2$, the pure-$\lambda_\Delta$ Hessian has eigenvalues $3\lambda_\Delta\varphi^2$ (multiplicity 1) and $\lambda_\Delta\varphi^2$ (multiplicity 59). Substituting into $16\pi^2 \beta_{V_4} = \frac{1}{2}\operatorname{Tr}(V_4'')^2$ gives
\[
16\pi^2 \beta_{\lambda_\Delta} \supset 2(60 + 8)\lambda_\Delta^2 - 36\lambda_\Delta\kappa_4 - 16\lambda_\Delta\kappa_R = 136\lambda_\Delta^2 - 36\lambda_\Delta\kappa_4 - 16\lambda_\Delta\kappa_R,
\]
correcting the factor-of-2 error ($68 \to 136$) in the earlier draft. In the pure-self-coupling truncation ($\kappa^2$, bidoublet portal, gauge, and Yukawa terms omitted):
- Phase 2B's $\lambda_\Delta = 2.0$ hits its formal pole at $\exp(16\pi^2/(136\times 2.0))\,v_R = 1.787\,v_R$;
- Planck-scale starting caps $\lambda_{\Delta,\max} = \frac{16\pi^2}{136\ln(M_{\rm Pl}/v_R)}$ are `0.0937` (`BM-LR`), `0.0547` (`BM-GUT` at $7.32\times 10^9\text{ GeV}$; `0.0576` at $2.15\times 10^{10}\text{ GeV}$), and `0.0417` (`BM-LOW`);
- Rescaling to $\lambda_\Delta = 0.03, \kappa_4 = 0.006, \kappa_R = 0.0045$ ($\lambda_{\rm eff} = 0.0165$) stays below the pure-self-coupling cap at all three benchmarks. However, this is only a pure-self-coupling diagnostic; the full coupled 138-parameter scalar RGE system above $v_R$ remains open.

### 3.4. Tree-Level Global Higgs+$\Delta_R$ Stability Failure at Matched `BM-LR` (`NP-02` = FAIL)

Integrating the 2-loop SM $(g_1, g_2, g_3, y_t, \lambda_H)$ RGEs (Buttazzo et al., 2013) gives $\mu_{\rm inst}^{(2\ell)} = 9.04\times 10^9\text{ GeV}$. Thus:
- At `BM-LOW` ($10^7\text{ GeV}$) and the rescaled `BM-GUT` ($7.32\times 10^9\text{ GeV}$): $\lambda_H^{\rm SM}(v_R) = +0.02119 > 0$ and $+0.00045 > 0$, respectively (no SM instability below $v_R$).
- At `BM-LR` ($5.08\times 10^{13}\text{ GeV}$): $\lambda_H^{\rm SM}(v_R) = -0.01122 < 0$. The two-field radial quartic potential is $V_4(x, r) = \lambda_H^{\rm UV} x^2 + \lambda_{h\Delta} x r + \lambda_{\rm eff} r^2$ ($x = |h|^2 \ge 0, r \ge 0$) with tree-level matching $\lambda_H^{\rm UV} = \lambda_H^{\rm SM}(v_R) + \frac{\lambda_{h\Delta}^2}{4\lambda_{\rm eff}}$. Extracting the actual effective portal coupling at the `BM-LR` criticality point gives **$\lambda_{h\Delta} = -1.648 < 0$**. Consequently, along the physical coherent ray
  \[
  r = -\frac{\lambda_{h\Delta}}{2\lambda_{\rm eff}} x = 49.95\,x > 0,
  \]
  the tree-level quartic potential evaluates to
  \[
  V_4(x, r_{\rm ray}) = \left(\lambda_H^{\rm UV} - \frac{\lambda_{h\Delta}^2}{4\lambda_{\rm eff}}\right)x^2 = \lambda_H^{\rm SM}(v_R)\,x^2 = -0.01122\,x^2 < 0.
  \]
  **The matched `BM-LR` negative-portal potential is unbounded below at tree level.** The earlier claim that $|\lambda_{h\Delta}| > 2\sqrt{\lambda_{\rm eff}|\lambda_H^{\rm SM}|}$ suffices for UV stability is **retracted**: tree-level copositivity on $x, r \ge 0$ requires either $\lambda_H^{\rm SM}(v_R) > 0$, or a **positive** portal $\lambda_{h\Delta} > 0$ (plus positive $\lambda_H^{\rm UV}$), or radiative Coleman–Weinberg / RG stabilization above $v_R$. Gate `NP-02` is therefore graded **FAIL (0)** for the matched `BM-LR` point.

---

## 4. Three-Generation Fermion, CKM, Neutrino, and PMNS Existence Fits (`REC-03` = PARTIAL)

### 4.1. Corrected Charged-Lepton Basis in Seesaw & PMNS Round-Trip Verification

With $-\mathcal{L}_D = \bar{e}_L Y_e e_R + \bar{\nu}_L Y_\nu^D \nu_R$ and $Y_e = U_{eL} \hat{Y}_e U_{eR}^\dagger$, rotating to the charged-lepton mass basis ($L_L = U_{eL} L_L^\ell$) gives $Y_\nu^\ell = U_{eL}^\dagger Y_\nu^D$ and $m_\nu^\ell = U_{eL}^\dagger m_\nu U_{eL}^*$. The weak-basis target is therefore
\[
m_\nu = U_{eL} m_\nu^\ell U_{eL}^T, \qquad m_\nu^\ell = U_{\rm PMNS}\operatorname{diag}(m_1, m_2, m_3) U_{\rm PMNS}^T,
\]
correcting the inconsistent $U_{eL}^* m_\nu^\ell U_{eL}^\dagger$ formula in the earlier draft. Every fit below is verified by rotating the reconstructed $m_\nu = -\frac{v_{\rm EW}^2}{2} Y_\nu^D M_R^{-1} (Y_\nu^D)^T$ back into the charged-lepton mass basis ($m_\nu^\ell = U_{eL}^\dagger m_\nu U_{eL}^*$) and directly recovering $\sin^2\theta_{12}, \sin^2\theta_{23}, \sin^2\theta_{13}, \delta_{\rm PMNS} = 197^\circ$, and running $\Delta m_{21}^2, \Delta m_{31}^2$ to `< 2e-13`.

### 4.2. Recomputed Benchmark Fits & Retracted `PS1-EW-min` Exclusions

| Benchmark | $v_R$ [GeV] | Sub-branch | Max charged/CKM err. | $\|Y_1\|_2$ | $\|Y_{15}\|_2$ | $\|\tilde{Y}_1\|_2, \|\tilde{Y}_{15}\|_2$ | $\|f_R\|_2$ | $M_R$ spectrum [GeV] | PMNS round-trip err. | Perturbative? |
|---|---:|---|---:|---:|---:|---|---:|---|---:|---|
| **`BM-LR`** | $5.08\times 10^{13}$ | `PS1-EW-min` (complex) | `7.34e-13` | 0.522 | 0.566 | 0, 0 | **0.0380** | $(6.80\times 10^9,\, 1.19\times 10^{12},\, 1.36\times 10^{12})$ | `1.92e-13` | **PASS** |
| **`BM-LR`** | $5.08\times 10^{13}$ | `PS1-EW-min` (**real witness**) | `5.87e-13` | 0.522 | 0.571 | 0, 0 | **0.1972** | $(1.13\times 10^{10},\, 7.10\times 10^{11},\, 7.08\times 10^{12})$ | `1.10e-13` | **PASS** |
| **Refit** | $6.00\times 10^{11}$ | `PS1-EW-min` (complex refit) | `4.84e-13` | 0.565 | 0.594 | 0, 0 | **2.7986** | $(1.39\times 10^{10},\, 5.30\times 10^{11},\, 1.19\times 10^{12})$ | `2.36e-14` | **PASS** |
| `BM-LR` | $5.08\times 10^{13}$ | `PS1-EW-gen` (4 Yukawas) | `6.94e-15` | 1.193 | 1.019 | 0.783, 0.732 | 0.828 | $(5.43\times 10^{12},\, 1.12\times 10^{13},\, 2.97\times 10^{13})$ | `1.36e-14` | **PASS** |
| `BM-GUT` | $7.32\times 10^9$ | `PS1-EW-min` (local fit) | `6.85e-13` | 0.613 | 0.637 | 0, 0 | **498.4** | $(2.10\times 10^9,\, 7.15\times 10^{11},\, 2.58\times 10^{12})$ | `2.13e-14` | FAIL (local fit) |
| **`BM-GUT`** | $7.32\times 10^9$ | **`PS1-EW-gen` (4 Yukawas)** | `8.49e-14` | 1.244 | 1.766 | 0.815, 1.265 | **0.828** | $(7.82\times 10^8,\, 1.62\times 10^9,\, 4.29\times 10^9)$ | `6.05e-15` | **PASS** |
| `BM-LOW` | $1.00\times 10^7$ | `PS1-EW-min` (local fit) | `4.42e-13` | 0.707 | 0.725 | 0, 0 | **$3.53\times 10^5$** | $(3.27\times 10^{10},\, 5.17\times 10^{11},\, 2.50\times 10^{12})$ | `3.32e-14` | FAIL (local fit) |
| **`BM-LOW`** | $1.00\times 10^7$ | **`PS1-EW-gen` (4 Yukawas)** | `7.23e-13` | 1.429 | 2.034 | 0.937, 1.454 | **0.828** | $(1.07\times 10^6,\, 2.21\times 10^6,\, 5.86\times 10^6)$ | `1.06e-14` | **PASS** |

**Why the earlier `PS1-EW-min` exclusions were wrong:**
- Even when $c_d, c_e \in \mathbb{R}$, the unitary matrices $U_{eL}, U_{eR}$ carry relative signs/phases (specifically $\phi_3 = \pi$), allowing $3 c_e y_b$ and $(c_d - 2c_e) y_\tau$ to cancel destructively in $(Y_\nu^D)_{33}$ near $c_d \approx 113.4, c_e \approx 28.4$ while recovering $y_t = c_d y_b - c_e y_\tau$. The earlier code skipped the $\|Y_\nu^D\|_F$ minimization stage for real ratios and therefore misattributed a local optimizer artifact to a theorem.
- Likewise, the earlier $7.7\times 10^{11}\text{ GeV}$ "hard floor" merely extrapolated a single fixed `BM-LR` fit without refitting the running inputs; refitting at $v_R = 6.0\times 10^{11}\text{ GeV}$ yields a strictly perturbative witness ($\|f_R\|_2 = 2.80 < \sqrt{4\pi}$; even lower $\|f_R\|_2 \approx 0.23$ is achievable). Local fits at `BM-GUT` and `BM-LOW` remain non-perturbative, but no global no-go theorem is claimed.

---

## 5. Flavour, Baryon-Number Stability (`LAB-02` = PARTIAL), and Cosmological Relics (`COS-01` = OPEN / PARTIAL)

| Observable / Gate | Experimental Bound / Scope | `BM-LR` ($5.08\times 10^{13}$ GeV) | `BM-GUT` ($7.32\times 10^9$ GeV) | `BM-LOW` ($1.00\times 10^7$ GeV) | Status |
|---|---|---:|---:|---:|---|
| $M_X$ [GeV] | $\gtrsim 2.06\times 10^6$ (aligned VW) | $2.05\times 10^{13}$ | $3.42\times 10^9$ | $5.44\times 10^6$ | PASS |
| $M_{W_R}, M_{Z_R}$ [GeV] | $\gtrsim 6\times 10^3$ (**preliminary**) | $1.94\times 10^{13},\; 4.48\times 10^{13}$ | $2.38\times 10^9,\; 6.82\times 10^9$ | $2.97\times 10^6,\; 1.03\times 10^7$ | PRELIM PASS |
| $\operatorname{BR}(K_L \to \mu^\pm e^\mp)$ (fitted $K_{L,R}$) | $< 4.7\times 10^{-12}$ (BNL E871) | $1.34\times 10^{-40}$ | $3.33\times 10^{-25}$ | $9.58\times 10^{-14}$ | PASS |
| $\operatorname{BR}(B_s \to \mu^\pm e^\mp)$ (aligned) | $< 5.4\times 10^{-9}$ (LHCb) | $5.77\times 10^{-43}$ | $1.33\times 10^{-27}$ | $3.84\times 10^{-16}$ | PASS |
| $\operatorname{BR}(\mu \to e\gamma)$ (prelim 1-loop) | $< 1.5\times 10^{-13}$ (**MEG II**) | $1.88\times 10^{-46}$ | $4.36\times 10^{-31}$ | $1.25\times 10^{-19}$ | PRELIM PASS |
| $M_{H_2}$ heavy-Higgs FCNC [GeV] | $\gtrsim 5\times 10^4$ (**preliminary**) | $4.54\times 10^{13}$ | $6.55\times 10^9$ | $8.94\times 10^6$ | PRELIM PASS |
| SMEFT suppression $v_{\rm EW}^2 / v_R^2$ | $\lesssim 10^{-4}$ (EWPO) | $2.35\times 10^{-23}$ | $1.13\times 10^{-15}$ | $6.06\times 10^{-10}$ | PASS |
| $d=6$ proton decay (pure PS) | $\tau_p > 2.4\times 10^{34}$ yr | **FORBIDDEN** (pert. $3B+L$) | **FORBIDDEN** (pert. $3B+L$) | **FORBIDDEN** (pert. $3B+L$) | PASS |
| Optional $SO(10)$ $\tau(p\to e^+\pi^0)$ | $> 2.4\times 10^{34}$ yr (ballpark) | N/A | $4.87\times 10^{39}$ yr | N/A | PRELIM |
| $\tau_{n\bar{n}}$ (`PS1-MM` / prelim $\lambda_{\Delta 4}\sim 1$, $M_{\Delta_6}=0.11\,v_R$) | $> 4.7\times 10^8$ s (**preliminary**) | $\infty$ / $5.64\times 10^{53}$ s | $\infty$ / $6.93\times 10^{25}$ s | $\infty$ / $3.30\times 10^{11}$ s | PRELIM PASS |
| Monopoles ($\pi_2=\mathbb{Z}$) & $\mathbb{Z}_2$ strings ($\pi_1=\mathbb{Z}_2$) | Requires $T_{\rm rh} < v_R$ | $M_{\rm mon}=7.92\times 10^{14}$ | $M_{\rm mon}=9.83\times 10^{10}$ | $M_{\rm mon}=1.15\times 10^8$ | CONDITIONAL |
| $D$-parity domain walls | Must not overclose | ABSENT (no $\Delta_L$) | ABSENT (no $\Delta_L$) | ABSENT (no $\Delta_L$) | PASS |
| Vanilla $N_1$ thermal leptogenesis ($\eta_B^{\rm obs}=6.1\times 10^{-10}$) | $|\epsilon_1|$ / $\eta_B^{\max}$ ($\kappa_{\rm eff}\le 0.1$) | `min`: $1.88\times 10^{-7}$ ($3.4\times$ short); `gen`: $5.33\times 10^{-5}$ | **`gen`: $7.45\times 10^{-9}$ ($85\times$ short)** | **CLOSED** ($6.5\times 10^4\times$ short) | **OPEN / SHORT** |

### Key Physics Notes on Flavour, Stability, and Relics

1. **Corrected Valencia–Willenbrock $K_L \to \mu^\pm e^\mp$ width:** Summing over $\mu^- e^+$ and $\mu^+ e^-$ gives
   \[
   \Gamma(K_L \to \mu^\pm e^\mp) = \frac{g_4^4 f_K^2 m_K}{32\pi M_X^4}\left(\frac{\eta_{\rm QCD} m_K^2}{m_s + m_d}\right)^2\left(1 - \frac{m_\mu^2}{m_K^2}\right)^2 |c_{\rm mix}|^2,
   \]
   where $|c_{\rm mix}|^2 = \frac{1}{2}(|K_{L00}^* K_{R11}|^2 + |K_{R00}^* K_{L11}|^2 + |K_{L01}^* K_{R10}|^2 + |K_{R01}^* K_{L10}|^2) = 1$ for aligned $K_L = K_R = I$. This corrects the earlier factor-of-2 width overestimate and gives the aligned lower bound $M_X \gtrsim 2.06\times 10^6\text{ GeV}$ ($v_R \gtrsim 3.78\times 10^6\text{ GeV}$ at `BM-LOW`; $M_X \gtrsim 2.04\times 10^6\text{ GeV}$ at $g_4 \approx 0.766$). $\mu \to e\gamma$, $W_R/Z_R$, heavy-Higgs FCNC, and $n\text{--}\bar{n}$ remain **preliminary order-of-magnitude checks** pending full SMEFT Wilson-coefficient matching.
2. **Baryon number vs. gauged $B-L$ and actual sextet masses:** Pure Pati–Salam preserves perturbative baryon number via accidental $3B+L$ charges ($F_L:+1$, $F_R^c:-1$, $\Phi_{1,15}:0$, $\Delta_R:+2$), forbidding $d=6$ $\Delta B=1$ proton decay, whereas gauged $B-L \subset SU(4)_C$ is broken by $\langle\Delta_R\rangle$ by $\Delta(B-L) = 2$. In `PS1-MM`, $\Delta B = 2$ $n\text{--}\bar{n}$ vanishes at tree level by $U(1)_\Delta$; if $\lambda_{\Delta 4} = \mathcal{O}(1)$ is turned on, the sextet mediators have actual masses $M_{\Delta_6} \in [0.110, 0.145]\,v_R$ (at $\kappa_4=0.006, \kappa_R=0.0045$; $0.18\text{–}0.24\,v_R$ at the old $\kappa_4=0.016, \kappa_R=0.012$), which we use directly in the preliminary $\tau_{n\bar{n}}$ bound.
3. **Topological defects and leptogenesis shortfall:** Breaking $SU(4)_C\times SU(2)_R \to SU(3)_C\times U(1)_Y$ with $\Delta_R(10,1,3)$ leaves a disconnected $\mathbb{Z}_2$ stabilizer (from $\Delta(B-L)=2$), producing **both** $\pi_2(G_{\rm PS}/G_{\rm SM}) = \mathbb{Z}$ doubly-charged monopoles and a $\pi_1(G_{\rm PS}/G_{\rm SM}) = \mathbb{Z}_2$ cosmic-string sector; inflation/reheating must satisfy $T_{\rm rh} < v_R$. Furthermore, vanilla $N_1$-dominated unflavored thermal leptogenesis falls short of $\eta_B^{\rm obs} \simeq 6.1\times 10^{-10}$ at `BM-GUT` ($|\epsilon_1| = 7.45\times 10^{-9}$, $M_{R1} = 7.82\times 10^8\text{ GeV}$, $\sim 85\times$ short at rescaled `BM-GUT`, and $\sim 44\times$ short even at pre-rescaled $2.15\times 10^{10}\text{ GeV}$ with $|\epsilon_1|\sim 1.45\times 10^{-9}$) as well as for the `BM-LR` `PS1-EW-min` witness ($3.4\times$ short). Only `BM-LR` in `PS1-EW-gen` exceeds the naive $\eta_B$ ceiling before Boltzmann washout, and full flavored/resonant Boltzmann transport and dark matter remain open (`COS-01` = OPEN / PARTIAL).

---

## 6. Regraded TP-00 Gate Update

No aggregate score is formed; every gate remains independent:

| Gate | Score | Revised Phase 3 (`PS1-EW`) status |
|---|---:|---|
| `ALG-01` | 1 | Partial / branch-specific: `PS1-EW-min` and `PS1-EW-gen` declared; bare `PS1` retains 138 scalar parameters |
| `ALG-05` | 2 | Full $188\times 188$ Hessian at unbroken EW origin closes: 9 Goldstones + 4 light SM Higgs + 175 heavy physical modes |
| `PERT-01` | **1** | **PARTIAL / scoped to heavy spectrum:** 175 positive heavy modes + 9 Goldstones at unbroken EW origin ($\langle\Phi\rangle=0$); $-\mu_{\rm SM}^2$ gives expected tachyonic EWSB curvature and full EW-broken vacuum verification remains open |
| `PERT-03` | 1 | Partial: tree-level Yukawa and gauge-only 2-loop perturbativity pass; 1-loop unitarity/pole residues open |
| `PERT-05` | **1** | **PARTIAL:** Gauge-only 2-loop PS RGEs (omitting 2-loop UV Yukawa traces) + 1-loop thresholds pass; corrected pure-self-coupling $136\lambda_\Delta^2$ diagnostic passes at $\lambda_\Delta=0.03$; coupled 138-parameter scalar RGEs and EW hierarchy fine-tuning ($\Delta_{\rm FT}\sim 10^{10}\text{–}10^{23}$) remain open |
| `REC-02` | 2 | Chiral SM matter, hypercharge, gauge matching, and one light SM Higgs doublet recovered |
| `REC-03` | **1** | **PARTIAL (existence/interpolation):** Perturbative witnesses exist for `PS1-EW-min` (both real & complex ratios at `BM-LR`, and refitted at $6\times 10^{11}\text{ GeV}$) and `PS1-EW-gen` (all 3 benchmarks, verified by direct contraction & PMNS round-trip), but 30 real Yukawa parameters vs 18 observables is an interpolation test, not a constrained prediction |
| `NP-02` | **0** | **FAIL / OPEN AT TREE LEVEL:** While Phase 2B $\Delta_R$-only global minimum holds, the matched negative-portal `BM-LR` point ($\lambda_{h\Delta}=-1.648, \lambda_H^{\rm SM}=-0.01122$) is **unbounded below at tree level** along the physical coherent ray $r = 49.95\,x > 0$; positive-portal or radiative stabilization remains open |
| `LAB-01` | 2 | Single light SM-like Higgs doublet recovered with SMEFT suppression $v_{\rm EW}^2/v_R^2 \le 6\times 10^{-10}$ |
| `LAB-02` | **1** | **PARTIAL:** Corrected Valencia–Willenbrock $K_L/B_s \to \mu e$ ($v_R \gtrsim 3.78\times 10^6\text{ GeV}$) and MEG II $\mu\to e\gamma < 1.5\times 10^{-13}$ checked; $n\text{--}\bar{n}$ (with actual sextet masses $0.11\text{–}0.14\,v_R$), heavy-Higgs FCNC, and $W_R/Z_R$ remain preliminary order-of-magnitude checks |
| `COS-01` | **1** | **OPEN / PARTIAL:** $\pi_2=\mathbb{Z}$ monopoles and $\pi_1=\mathbb{Z}_2$ strings require $T_{\rm rh} < v_R$; vanilla $N_1$-dominated thermal leptogenesis at `BM-GUT` falls short of $\eta_B^{\rm obs}$; Boltzmann transport and dark matter remain open |
| `REP-01` | 2 | All Phase 2B + Phase 3 verifiers, JSON/Markdown outputs, and 22/22 unit tests execute deterministically |

---

## 7. Reproduction

```bash
python -m pip install -r requirements.txt
make verify
```

All Phase 3 computations live in `code/verify_phase3_ew_matching.py`, unit tests in `code/tests/test_phase3_ew.py`, machine-readable outputs in `results/phase3_ew_results.json`, and the concise summary in `results/phase3_ew_summary.md`.
