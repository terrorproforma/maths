# TP-03 Phase 3 (`PS1-EW`) — Electroweak Matching, RG Evolution, Fermion/Neutrino Fit, and Stability Audit

**Author:** Angus Muffatti  
**Project:** TP-03 — Complete Pati–Salam benchmark  
**Status:** **PHASE 3 COMPLETE FOR THE DECLARED `PS1-EW` BRANCHES**  
**Active branches:** `PS1-EW-min` (minimal 2-Dirac-Yukawa sub-branch) and `PS1-EW-gen` (full gauge-invariant 4-Dirac-Yukawa branch)

---

## 1. Terminal result

Extending the certified Phase 2B high-scale vacuum (`PS1-MM`) through electroweak matching, one- and two-loop renormalisation-group evolution, three-generation fermion/neutrino fitting, and flavour/baryon/relic audits yields a sharply differentiated verdict with **no hidden fine-tuning and no averaged failures**:

\[
\boxed{
\begin{array}{c}
\textbf{Explicit }188\times 188\textbf{ PS1-EW Higgs-mixing Hessian (9 Goldstones, 4 light Higgs, 175 heavy): PASS.}\\
\textbf{2-loop gauge perturbativity up to }M_{\rm Pl}\textbf{ across }v_R\in[10^{5.5},10^{16}]\text{ GeV}\textbf{: PASS.}\\
\textbf{Phase 2B }\lambda_\Delta=2.0\textbf{ scalar Landau pole at }3.2\,v_R\textbf{: OBSTRUCTION; rescaled }\lambda_\Delta=0.08\textbf{: PASS.}\\
\textbf{PS1-EW-min (real Higgs-mixing ratios): FAIL (}\|f_R\|_2=6.54>\sqrt{4\pi}\textbf{ at BM-LR).}\\
\textbf{PS1-EW-min (complex phase): PASS at }v_R\gtrsim 7.7\times 10^{11}\text{ GeV}\textbf{; FAIL at BM-GUT and BM-LOW.}\\
\textbf{PS1-EW-gen (4 gauge-allowed Yukawas): PASS across }v_R\in[4.5\times 10^6,10^{16}]\text{ GeV}.\\
\textbf{Flavour, }\Delta B=1,2\textbf{ stability, and monopole-safe leptogenesis (BM-LR / BM-GUT): PASS (conditional on }T_{\rm rh}<v_R\textbf{).}
\end{array}
}
\]

The Phase 3 calculation therefore delivers:
1. A **complete, reproducible, phenomenologically viable Pati–Salam benchmark** at `BM-LR` ($v_R = 5.08\times 10^{13}\text{ GeV}$, passing even in the minimal two-Yukawa branch `PS1-EW-min` with complex phases) and at `BM-GUT` ($v_R = 2.15\times 10^{10}\text{ GeV}$, exact 2-loop $SO(10)$ triple unification in `PS1-EW-gen`);
2. Three **sharp, decisive negative/obstruction results**:
   - The 60-real-component $\Delta_R$ self-coupling drives a 1-loop beta function $16\pi^2 \beta_{\lambda_\Delta} \supset 68 \lambda_\Delta^2$, so Phase 2B's $\mathcal{O}(1)$ certificate ($\lambda_\Delta = 2.0$) hits a sub-Planckian scalar Landau pole at $3.19\,v_R$ and must be rescaled to $\lambda_\Delta \le 0.08$;
   - Restricting `PS1-EW-min` ($Y_1, Y_{15}, f_R$ only) to **real** light-Higgs mixing ratios forces $\|Y_\nu^D\|_2 \gtrsim 0.42\text{–}0.65$, pushing $M_{R3} \gtrsim 2.3\times 10^{14}\text{ GeV}$ and violating Majorana perturbativity ($\|f_R\|_2 = 6.54 > \sqrt{4\pi}$) at `BM-LR`;
   - Even **with complex phases**, `PS1-EW-min` hits a hard seesaw-perturbativity floor $v_R \gtrsim 7.7\times 10^{11}\text{ GeV}$, ruling it out at both the 2-loop triple-unification scale (`BM-GUT`, $\|f_R\|_2 = 182.9$) and the low-scale flavour frontier (`BM-LOW`, $\|f_R\|_2 = 7.77\times 10^5$);
3. Two **explicit, unremoved theoretical/cosmological conditions**:
   - Tree-level electroweak hierarchy fine-tuning $\Delta_{\rm FT} = v_R^2 / \mu_{\rm SM}^2$ ranges from $1.27\times 10^{10}$ (`BM-LOW`) to $5.87\times 10^{16}$ (`BM-GUT`) and $3.29\times 10^{23}$ (`BM-LR`);
   - Homotopy $\pi_2(G_{\rm PS}/G_{\rm SM}) = \mathbb{Z}$ enforces doubly-charged magnetic monopoles ($M_{\rm mon} \sim 15\,v_R$), requiring $T_{\rm rh} < v_R$ (monopole dilution by inflation).

---

## 2. Complete $\Phi_1$–$\Phi_{15}$ High-Scale Bidoublet Mass Matrix and One-Light-Higgs Matching

### 2.1. Exact SM Decomposition of the 188 Real Scalar Modes

In `PS1`, the three independent complex multiplets are $\Phi_1(1,2,2)$ (8 real), $\Phi_{15}(15,2,2)$ (120 real), and $\Delta_R(10,1,3)$ (60 real). There is **no** $\Delta_L(10,3,1)$ in `PS1-MM` / `PS1-EW` (that belongs to the deferred parity branch `PS1P`), so:
- Type-II seesaw is identically absent at tree level;
- Because $\Delta_R$ is an $SU(2)_L$ singlet while $\Phi_1, \Phi_{15}$ are $SU(2)_L$ doublets, unbroken $SU(2)_L$ at $\mu = v_R$ **forbids** any quadratic mixing between $\Delta_R$ and the bidoublets.

Writing $\Phi_1 = (\phi_{1d}, \, \phi_{1u})$ with $H_{1u} \equiv \phi_{1u} \sim (1,2)_{+1/2}$ and $H_{1d} \equiv -i\sigma_2 \phi_{1d}^* \sim (1,2)_{+1/2}$, and expanding $\Phi_{15} = \sqrt{2}\sum_{A=1}^{15} T^A \Phi_{15}^A$ with $T^{15} = \frac{1}{\sqrt{24}}\operatorname{diag}(1,1,1,-3)$, the 128 real bidoublet degrees of freedom decompose under $G_{\rm SM} = SU(3)_C \times SU(2)_L \times U(1)_Y$ into four independent Hermitian mass blocks:

| SM multiplet | Components | Mass-matrix dimension | Real d.o.f. |
|---|---|---:|---:|
| Colour-singlet Higgs doublets $(1,2)_{+1/2}$ | $\mathbf{H} = (H_{1u}, H_{1d}, H_{15u}, H_{15d})^T$ | $4\times 4$ Hermitian $\mathcal{M}_H^2$ | 16 |
| Colour-octet doublets $(8,2)_{+1/2}$ | $\mathbf{\Omega} = (\Omega_u, \tilde{\Omega}_d)^T$ | $2\times 2$ Hermitian $\mathcal{M}_\Omega^2$ | 64 |
| Triplet leptoquarks $(3,2)_{+7/6}$ | $\mathbf{\Sigma}_{7/6} = (\Sigma_{+7/6}, \tilde{\bar{\Sigma}}_{-7/6})^T$ | $2\times 2$ Hermitian $\mathcal{M}_{7/6}^2$ | 24 |
| Triplet leptoquarks $(3,2)_{+1/6}$ | $\mathbf{\Sigma}_{1/6} = (\Sigma_{+1/6}, \tilde{\bar{\Sigma}}_{-1/6})^T$ | $2\times 2$ Hermitian $\mathcal{M}_{1/6}^2$ | 24 |
| **Total bidoublet sector** | $\Phi_1 + \Phi_{15}$ | Block-diagonal | **128** |

Combined with the 60 real components of $\Delta_R$ (9 eaten Goldstones + 51 physical modes), all $128 + 60 = 188$ real scalar modes are accounted for.

### 2.2. Exact Vanishing of $\Delta_R^2$ Cross-Couplings and Complete $\Delta_R^\dagger \Delta_R$ Portal Structure

On the certified Phase 2B coherent vacuum
\[
\langle \Delta_R \rangle = \frac{v_R}{\sqrt{2}} |44\rangle_{\rm sym} \otimes |T_R^3 = +1\rangle,
\]
the tensor square $\langle \Delta_R \rangle \otimes \langle \Delta_R \rangle$ is totally symmetric in $SU(4)_C$ ($|4444\rangle \in [4,0,0]$) and highest-weight in $SU(2)_R$ ($|T_R^3 = +2\rangle \in \mathbf{5}$). Consulting the Phase 2B invariant basis (`invariant_coupling_basis.csv`, lines 16–17, 22–23, 28–29, 38–39, 46–47, 52–53), every $\Phi_{15}^2 \Delta_R^2$ and $\Phi_{15}\Phi_{15}^\dagger \Delta_R^2$ invariant couples through the $[0,2,0]$ or $[2,1,0]$ $SU(4)$ channels and $j_R \le 1$, **none of which overlap with $([4,0,0], 1, 5)$**. Consequently, **all $\Delta_R^2$ and $(\Delta_R^\dagger)^2$ bidoublet portals vanish identically on $\langle \Delta_R \rangle$** (machine residual `0.00e+00`).

Defining the $SU(4)$-adjoint and $84$-channel vacuum bilinears
\[
(D_0)_a{}^b = \sum_{c,i} (\Delta_R)_{ac,i} (\Delta_R^\dagger)^{bc,i}, \qquad
(D_k)_a{}^b = \sum_{c,i,j} (\Delta_R^\dagger)^{bc,i} (t_3^k)_{ij} (\Delta_R)_{ac,j},
\]
which evaluate on $\langle \Delta_R \rangle$ to $D_0 = \frac{v_R^2}{2} P_4$ and $D_k = \frac{v_R^2}{2}\delta_{k3} P_4$ with $P_4 = \operatorname{diag}(0,0,0,1)$, the declared gauge-invariant `PS1-EW` quadratic + portal Lagrangian is:
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
where $\mathcal{O}_{15}^{(84)} = (\Delta_R)_{ab,i}(\Delta_R^\dagger)^{cd,i}\operatorname{Tr}_2\!\big((\Phi_{15}^\dagger)_d{}^b (\Phi_{15})_c{}^a\big)$ and its $SU(2)_R$-triplet and holomorphic partners $\mathcal{O}_{15}^{(84,R)}, \mathcal{O}_{15}^{(84,\rm hol)}$ project **exclusively onto $|(\Phi_{15})_4{}^4|^2 = \frac{3}{4}|\Phi_{15}^{(15)}|^2$** and vanish identically on $\Omega, \Sigma_{7/6}, \Sigma_{1/6}$. All 16 operators are directly verified $SU(4)_C\times SU(2)_L\times SU(2)_R$-invariant on random group transformations to relative error `7.37e-15`.

Evaluating on $\langle \Delta_R \rangle$ gives the exact $4\times 4$ Hermitian doublet mass matrix $\mathcal{M}_H^2$ in basis $(H_{1u}, H_{1d}, H_{15u}, H_{15d})^T$:
- Diagonal entries:
  \[
  (\mathcal{M}_H^2)_{11,22} = \mu_1^2 + \frac{v_R^2}{2}(\alpha_{1,0} \mp \alpha_{1,R}), \qquad
  (\mathcal{M}_H^2)_{33,44} = M_{15,\rm bare}^2 + \frac{3v_R^2}{8}(\alpha_{15,a}+\alpha_{15,b}+\alpha_{15,c} \mp \alpha_{15,cR}),
  \]
- Intra-bidoublet off-diagonals:
  \[
  (\mathcal{M}_H^2)_{21} = 2\tilde{\mu}_1^2 + v_R^2 \tilde{\alpha}_{1,0}, \qquad
  (\mathcal{M}_H^2)_{43} = 2\tilde{\mu}_{15}^2 + \frac{3}{4}v_R^2 \tilde{\alpha}_{15,c},
  \]
- $\Phi_1$–$\Phi_{15}$ mixing entries (with $c_{\rm mix} = -\frac{\sqrt{3}}{4}v_R^2$):
  \[
  (\mathcal{M}_H^2)_{13} = c_{\rm mix}(\beta_0 - \beta_R), \quad
  (\mathcal{M}_H^2)_{31}^* = (\mathcal{M}_H^2)_{13}, \quad
  (\mathcal{M}_H^2)_{32}^* = c_{\rm mix}(\beta_0 + \beta_R)^* \text{ (i.e. } (\mathcal{M}_H^2)_{42} = c_{\rm mix}(\beta_0+\beta_R)\text{)},
  \]
  \[
  (\mathcal{M}_H^2)_{23} = c_{\rm mix}(\tilde{\beta}_0 - \tilde{\beta}_R), \qquad
  (\mathcal{M}_H^2)_{41} = c_{\rm mix}(\tilde{\beta}_0 + \tilde{\beta}_R).
  \]

Because the $84$-channel and $\Phi_1$–$\Phi_{15}$ portals vanish identically on all coloured states, **the 16 real parameters above form a surjective bijection onto the entire space of $4\times 4$ Hermitian matrices $\mathcal{M}_H^2$**, completely decoupled from the coloured mass matrices:
\[
\mathcal{M}_\Omega^2 = \begin{pmatrix} M_{15,\rm bare}^2 & 2\tilde{\mu}_{15}^{2*} \\ 2\tilde{\mu}_{15}^2 & M_{15,\rm bare}^2 \end{pmatrix}, \qquad
\mathcal{M}_{7/6}^2 = \mathcal{M}_{1/6}^2 = \begin{pmatrix} M_{15,\rm bare}^2 + \frac{v_R^2}{2}\alpha_{15,a} & 2\tilde{\mu}_{15}^{2*} \\ 2\tilde{\mu}_{15}^2 & M_{15,\rm bare}^2 + \frac{v_R^2}{2}\alpha_{15,b} \end{pmatrix},
\]
where $M_{15,\rm bare}^2 = \mu_{15}^2 + \frac{v_R^2}{2}\alpha_{15,0}$.

### 2.3. One-Light-Higgs Fine-Tuning Condition and Full $188\times 188$ Hessian Certificate

Tuning the single determinant condition
\[
\det \mathcal{M}_H^2 = \lambda_1(\mathcal{M}_H^2)\, M_{H_2}^2 M_{H_3}^2 M_{H_4}^2, \qquad \lambda_1(\mathcal{M}_H^2) = -\mu_{\rm SM}^2 \simeq -(88.57\text{ GeV})^2,
\]
with $M_{H_{2,3,4}}^2 = (0.80, 1.20, 1.60)v_R^2$, $M_{\Omega_{1,2}}^2 = (1.10, 1.30)v_R^2$, and $M_{\Sigma_{7/6,1/6}}^2 = (1.40, 1.80)v_R^2$ isolates **exactly one light SM Higgs doublet** $h \sim (1,2)_{+1/2}$ aligned along any unit eigenvector
\[
u = (\alpha_{1u}, \alpha_{1d}, \alpha_{15u}, \alpha_{15d})^T \in \mathbb{C}^4, \qquad \sum |\alpha|^2 = 1,
\]
so that below $\mu = v_R$:
\[
H_{1u} = \alpha_{1u} h, \qquad H_{1d} = \alpha_{1d} h, \qquad H_{15u} = \alpha_{15u} h, \qquad H_{15d} = \alpha_{15d} h.
\]

Direct assembly of the full $188\times 188$ real scalar Hessian from the gauge-invariant potential at the perturbative `PS1-EW` quartic point ($\lambda_\Delta = 0.08, \kappa_4 = 0.016, \kappa_R = 0.012, \lambda_{\rm eff} = 0.044$) certifies:
- **9 exact zero Goldstone modes** matching the broken gauge orbit to `4.91e-18`;
- **4 degenerate light SM Higgs modes** matching the target eigenvector $u$ to subspace error `6.66e-16` (at probe $m_h^2 = 10^{-4}v_R^2$) and `4.44e-16` (at criticality $\det\mathcal{M}_H^2 = 0$);
- **175 strictly positive heavy physical real scalar modes** (51 from $\Delta_R$, 12 from $H_{2,3,4}$, 64 from $\Omega_{1,2}$, 48 from $\Sigma_{7/6}, \Sigma_{1/6}$) matching the analytic multiplet formulas to `3.11e-15`.

The required electroweak hierarchy fine-tuning $\Delta_{\rm FT} = v_R^2 / \mu_{\rm SM}^2$ is $3.29\times 10^{23}$ (`BM-LR`), $5.87\times 10^{16}$ (`BM-GUT`), and $1.27\times 10^{10}$ (`BM-LOW`). This fine-tuning is inherent to non-supersymmetric high-scale Pati–Salam breaking and is recorded openly under `PERT-05`.

### 2.4. Exact Tree-Level Yukawa Matching (`PS1-EW-min` vs `PS1-EW-gen`)

Because $\Phi_1$ and $\Phi_{15}$ are complex (non-self-dual), gauge invariance allows **four** renormalisable Dirac Yukawa matrices plus the symmetric Majorana matrix $f_R = f_R^T$:
\[
-\mathcal{L}_Y = F_L^T C\left(Y_1 \Phi_1 + \tilde{Y}_1 \tilde{\Phi}_1 + Y_{15}\Phi_{15} + \tilde{Y}_{15}\tilde{\Phi}_{15}\right) F_R^c + \frac{1}{2} F_R^{c\,T} C f_R \Delta_R F_R^c + \text{h.c.}
\]
Writing $\hat{Y}_{15} \equiv Y_{15}/\sqrt{12}$ and $\tilde{\hat{Y}}_{15} \equiv \tilde{Y}_{15}/\sqrt{12}$ (from $\sqrt{2} T^{15} = \frac{1}{\sqrt{12}}\operatorname{diag}(1,1,1,-3)$), matching onto $h$ at $\mu = v_R$ yields:
\[
\begin{aligned}
Y_u &= \alpha_{1u} Y_1 + \alpha_{1d} \tilde{Y}_1 + \alpha_{15u} \hat{Y}_{15} + \alpha_{15d} \tilde{\hat{Y}}_{15}, &
Y_\nu^D &= \alpha_{1u} Y_1 + \alpha_{1d} \tilde{Y}_1 - 3\alpha_{15u} \hat{Y}_{15} - 3\alpha_{15d} \tilde{\hat{Y}}_{15}, \\
Y_d &= \alpha_{1d}^* Y_1 - \alpha_{1u}^* \tilde{Y}_1 + \alpha_{15d}^* \hat{Y}_{15} - \alpha_{15u}^* \tilde{\hat{Y}}_{15}, &
Y_e &= \alpha_{1d}^* Y_1 - \alpha_{1u}^* \tilde{Y}_1 - 3\alpha_{15d}^* \hat{Y}_{15} + 3\alpha_{15u}^* \tilde{\hat{Y}}_{15},
\end{aligned}
\]
with Type-I seesaw Majorana matrix $M_R = \frac{1}{\sqrt{2}} f_R v_R$ and low-energy neutrino mass matrix $m_\nu = -\frac{v_{\rm EW}^2}{2} Y_\nu^D M_R^{-1} (Y_\nu^D)^T$.

This naturally defines **two distinct Yukawa sub-branches**:
1. **`PS1-EW-gen` (Full gauge-invariant 4-Yukawa branch):** No extra symmetry beyond $G_{\rm PS}$. Defining $s_1^2 = |\alpha_{1u}|^2 + |\alpha_{1d}|^2$, $s_{15}^2 = |\alpha_{15u}|^2 + |\alpha_{15d}|^2$, and the Phase 1 combinations $A_u = \frac{3Y_u+Y_\nu^D}{4}$, $A_d = \frac{3Y_d+Y_e}{4}$, $B_u = \frac{Y_u-Y_\nu^D}{4}$, $B_d = \frac{Y_d-Y_e}{4}$, the exact inverse is:
   \[
   Y_1 = \frac{\alpha_{1u}^* A_u + \alpha_{1d} A_d}{s_1^2}, \quad
   \tilde{Y}_1 = \frac{\alpha_{1d}^* A_u - \alpha_{1u} A_d}{s_1^2}, \quad
   \hat{Y}_{15} = \frac{\alpha_{15u}^* B_u + \alpha_{15d} B_d}{s_{15}^2}, \quad
   \tilde{\hat{Y}}_{15} = \frac{\alpha_{15d}^* B_u - \alpha_{15u} B_d}{s_{15}^2}.
   \]
   Here $Y_\nu^D$ is independent of $(Y_u, Y_d, Y_e)$ and can scale as $\sqrt{v_R}$ across the entire $v_R$ window.
2. **`PS1-EW-min` (Minimal 2-Yukawa sub-branch, $\tilde{Y}_1 = \tilde{Y}_{15} = 0$, e.g. via $U(1)_{\rm PQ}$):** Eliminating $Y_1, \hat{Y}_{15}$ yields two **rigid matrix predictions** governed solely by the two complex Higgs-mixing ratios $r_1 = \alpha_{1u}/\alpha_{1d}^*$ and $r_{15} = \alpha_{15u}/\alpha_{15d}^*$ (with $c_d = \frac{3r_1+r_{15}}{4}$ and $c_e = \frac{r_1-r_{15}}{4}$):
   \[
   \boxed{Y_u = c_d Y_d + c_e Y_e, \qquad Y_\nu^D = 3 c_e Y_d + (c_d - 2 c_e) Y_e.}
   \]

---

## 3. One- and Two-Loop Gauge/Yukawa RGEs, Thresholds, and Landau-Pole Audit

### 3.1. Exact Complex `PS1` Beta Functions Above $v_R$

For $3[F_L(4,2,1) + F_R^c(\bar{4},1,2)]$ plus complex $\Phi_1(1,2,2) + \Phi_{15}(15,2,2) + \Delta_R(10,1,3)$ in the ordering $(SU(4)_C, SU(2)_L, SU(2)_R)$, the exact 1-loop and 2-loop Machacek–Vaughn gauge beta coefficients are:
\[
b^{\rm PS1} = \begin{pmatrix} -7/3 \\ +2 \\ +26/3 \end{pmatrix}, \qquad
B^{\rm PS1} = \begin{pmatrix}
2435/6 & 105/2 & 249/2 \\
525/2 & 73 & 48 \\
1245/2 & 48 & 779/3
\end{pmatrix}.
\]
The off-diagonal dimension-symmetry identity $\dim(G_i) B_{ij} = \dim(G_j) B_{ji}$ closes to machine precision (`0.0`).

### 3.2. Exact Weinberg–Hall 1-Loop Threshold Matching at $\mu = v_R$

Using the 9 heavy real vectors ($X, W_R, Z_R$) and 175 heavy real physical scalars from the `PS1-EW` Hessian, the 1-loop $\overline{\rm MS}$ matching relation is
\[
\frac{1}{\alpha_i^{\rm SM}(v_R)} = \sum_A w_{iA}\frac{1}{\alpha_A^{\rm PS}(v_R)} - \frac{\lambda_i(v_R)}{12\pi}, \qquad
\lambda_i(\mu) = \operatorname{Tr}_{\rm real}(t_{iV}^2) - 21\operatorname{Tr}_{\rm real}\!\left(t_{iV}^2\ln\frac{M_V}{\mu}\right) + \operatorname{Tr}_{\rm real}\!\left(t_{iS}^2\ln\frac{M_S}{\mu}\right),
\]
with $w_{3,4}=1$, $w_{2L,2L}=1$, $w_{Y,2R}=1$, $w_{Y,4}=2/3$. The traces satisfy all three UV–IR group-theory sum rules $\Delta b_i = b_i^{\rm UV} - b_i^{\rm SM}$ to `2.28e-15`.

### 3.3. High-Scale Landmarks and Exact $SO(10)$ Triple Unification

| Regime | $v_R(g_{2R}=g_{2L})$ [GeV] | $v_R^{\rm unif}$ [GeV] | $M_{\rm GUT}$ [GeV] | $\alpha_{\rm GUT}^{-1}$ | $g_{\rm GUT}$ |
|---|---:|---:|---:|---:|---:|
| 1-loop, no thresholds | $5.078\times 10^{13}$ | $3.153\times 10^{11}$ | $2.259\times 10^{16}$ | $37.10$ | $0.5820$ |
| 2-loop + 1-loop Weinberg–Hall thresholds | $5.715\times 10^{13}$ | $2.145\times 10^{10}$ | $5.129\times 10^{16}$ | $32.40$ | $0.6228$ |

Across the entire scanned range $v_R \in [10^{5.5}, 10^{16}]\text{ GeV}$, **all three Pati–Salam gauge couplings remain strictly perturbative up to $M_{\rm Pl} = 1.221\times 10^{19}\text{ GeV}$ at both 1-loop and 2-loop** ($\max g_i(M_{\rm Pl}) \le 0.88$). Notice that although $B_{44} = 405.83$ flips the sign of $\beta(g_4)$ at low $v_R \sim 10^{5.5}\text{ GeV}$, no sub-Planckian gauge Landau pole occurs.

### 3.4. Scalar Landau-Pole Obstruction in Phase 2B and SM Higgs Quartic Stability

1. **60-component $\Delta_R$ scalar Landau pole:** Because $\Delta_R$ has $N_c = 30$ complex (60 real) components, $16\pi^2 \frac{d\lambda_\Delta}{d\ln\mu} \supset (2 N_c + 8)\lambda_\Delta^2 = 68\lambda_\Delta^2$. Phase 2B's arbitrary $\mathcal{O}(1)$ benchmark ($\lambda_\Delta = 2.0$) hits a Landau pole at $\Lambda_{\rm LP} = 3.19\,v_R$! Maintaining perturbativity up to $M_{\rm Pl}$ requires $\lambda_\Delta(v_R) < \frac{16\pi^2}{68\ln(M_{\rm Pl}/v_R)}$ ($0.187$ at `BM-LR`, $0.115$ at `BM-GUT`, $0.0834$ at `BM-LOW`). Rescaling the `PS1-MM` / `PS1-EW` quartics to $\lambda_\Delta = 0.08, \kappa_4 = 0.016, \kappa_R = 0.012$ ($\lambda_{\rm eff} = 0.044$) preserves every Phase 2B global-minimum inequality and eliminates all sub-Planckian $\Delta_R$ Landau poles across all three benchmarks.
2. **SM Higgs quartic stability:** Integrating the 2-loop SM $(g_1, g_2, g_3, y_t, \lambda_H)$ RGEs (Buttazzo et al., 2013) from $\mu = M_t = 172.69\text{ GeV}$ gives the SM instability scale $\mu_{\rm inst}^{(2\ell)} = 9.04\times 10^9\text{ GeV}$. Thus:
   - At `BM-LOW` ($10^7\text{ GeV}$): $\lambda_H^{\rm SM}(v_R) = +0.0212 > 0$ (no electroweak vacuum instability below $v_R$);
   - At `BM-GUT` ($2.15\times 10^{10}\text{ GeV}$) and `BM-LR` ($5.08\times 10^{13}\text{ GeV}$): $\lambda_H^{\rm SM}(v_R) = -0.00172$ and $-0.01122$, respectively. Integrating out the heavy radial $\Delta_R$ mode shifts $\lambda_H^{\rm SM}(v_R) = \lambda_H^{\rm UV}(v_R) - \frac{\lambda_{h\Delta}^2}{4\lambda_{\rm eff}}$, so the UV potential remains bounded ($\lambda_H^{\rm UV}(v_R) > 0$) whenever $|\lambda_{h\Delta}| > 0.0174$ (`BM-GUT`) or $|\lambda_{h\Delta}| > 0.0444$ (`BM-LR`).

---

## 4. Three-Generation Fermion, CKM, Neutrino, and PMNS Fit at $\mu = v_R$

Running the PDG 2024/2026 $\overline{\rm MS}$ charged-fermion masses, CKM matrix, and NuFIT 5.3 (Normal Ordering, $m_1 = 0.015\text{ eV}$, $\sum m_\nu = 0.0846\text{ eV} < 0.12\text{ eV}$, $m_\beta = 0.0174\text{ eV} < 0.45\text{ eV}$, $m_{\beta\beta} = 0.0163\text{ eV}$) Weinberg operator from $M_Z$ to $v_R$ via the full $3\times 3$ complex matrix SM RGEs gives the following quantitative benchmark results:

| Benchmark | $v_R$ [GeV] | Sub-branch | Max charged/CKM rel. err. | $\|Y_1\|_2$ | $\|Y_{15}\|_2$ | $\|f_R\|_2$ | $M_R$ spectrum [GeV] | Perturbative ($<\sqrt{4\pi}$)? |
|---|---:|---|---:|---:|---:|---:|---|---|
| **`BM-LR`** | $5.08\times 10^{13}$ | **`PS1-EW-min` (complex phase)** | **`4.95e-13`** | **0.519** | **0.576** | **0.0539** | $(7.28\times 10^9,\, 1.06\times 10^{12},\, 1.93\times 10^{12})$ | **PASS** |
| `BM-LR` | $5.08\times 10^{13}$ | `PS1-EW-min` (**real ratios**) | `8.63e-13` | 0.613 | 0.840 | **6.538** | $(5.94\times 10^{10},\, 1.20\times 10^{12},\, 2.35\times 10^{14})$ | **FAIL** |
| `BM-LR` | $5.08\times 10^{13}$ | `PS1-EW-gen` (4 Yukawas) | `4.83e-16` | 0.459 | 0.365 | 0.831 | $(5.43\times 10^{12},\, 1.12\times 10^{13},\, 2.98\times 10^{13})$ | **PASS** |
| **`BM-GUT`** | $2.15\times 10^{10}$ | `PS1-EW-min` (complex phase) | `3.03e-13` | 0.595 | 0.631 | **182.9** | $(1.81\times 10^{10},\, 2.90\times 10^{11},\, 2.72\times 10^{12})$ | **FAIL** |
| **`BM-GUT`** | $2.15\times 10^{10}$ | **`PS1-EW-gen` (4 Yukawas)** | **`6.80e-15`** | **0.480** | **0.555** | **0.831** | $(2.29\times 10^9,\, 4.72\times 10^9,\, 1.26\times 10^{10})$ | **PASS** |
| **`BM-LOW`** | $1.00\times 10^7$ | `PS1-EW-min` (complex phase) | `3.74e-13` | 0.699 | 0.750 | **$7.77\times 10^5$** | $(1.77\times 10^{10},\, 4.13\times 10^{11},\, 5.50\times 10^{12})$ | **FAIL** |
| **`BM-LOW`** | $1.00\times 10^7$ | **`PS1-EW-gen` (4 Yukawas)** | **`7.26e-13`** | **0.565** | **0.659** | **0.831** | $(1.07\times 10^6,\, 2.20\times 10^6,\, 5.87\times 10^6)$ | **PASS** |

### Why Complex Phases Are Required in `PS1-EW-min`

In `PS1-EW-min`, $Y_u = c_d Y_d + c_e Y_e$ and $Y_\nu^D = 3 c_e Y_d + (c_d - 2c_e) Y_e$. When $c_d, c_e \in \mathbb{R}$, Weyl's singular-value inequality prevents simultaneous cancellation of $(Y_\nu^D)_{33}$ and recovery of $y_c \ll y_t$, forcing $\sigma_1(Y_\nu^D) \gtrsim 0.42\text{–}0.65 \sim y_t$. Through Type-I seesaw $M_{R3} \sim (\sigma_1(Y_\nu^D) v_{\rm EW}/\sqrt{2})^2 / m_\nu$, this drives $M_{R3} = 2.35\times 10^{14}\text{ GeV}$ and $\|f_R\|_2 = 6.54 > \sqrt{4\pi} = 3.545$ at `BM-LR`.

Allowing a **complex relative phase** between $r_1$ and $r_{15}$ ($c_d = 42.31 + 35.50i$, $c_e = 17.75 + 0.02i$, arising naturally from complex $\Phi_1\Phi_{15}\Delta_R^\dagger\Delta_R$ portals) makes $3|c_e| y_b \approx |c_d - 2c_e| y_\tau \approx 0.355$ cancel destructively in $(Y_\nu^D)_{33}$ while adding constructively to $y_t = 0.483$ in $(Y_u)_{33}$. This lowers $\sigma_1(Y_\nu^D)$ by an order of magnitude to $0.0585$ and lowers $M_{R3}$ by two orders of magnitude to $1.93\times 10^{12}\text{ GeV}$, yielding $\|f_R\|_2 = 0.0539 \ll 1$ at `BM-LR`. Even with this complex cancellation, however, `PS1-EW-min` cannot remain perturbative below $v_R \simeq \sqrt{2} M_{R3}/\sqrt{4\pi} \approx 7.7\times 10^{11}\text{ GeV}$.

---

## 5. Flavour, Baryon-Number Stability, and Cosmological Relic Audit

| Observable / Gate | Experimental Bound | `BM-LR` ($5.08\times 10^{13}$ GeV) | `BM-GUT` ($2.15\times 10^{10}$ GeV) | `BM-LOW` ($1.00\times 10^7$ GeV) | Status |
|---|---|---:|---:|---:|---|
| $M_X$ [GeV] | $\gtrsim 2.43\times 10^6$ (generic) | $2.04\times 10^{13}$ | $9.79\times 10^9$ | $5.42\times 10^6$ | PASS |
| $M_{W_R}, M_{Z_R}$ [GeV] | $\gtrsim 6\times 10^3$ (LHC) | $1.93\times 10^{13},\; 4.47\times 10^{13}$ | $7.08\times 10^9,\; 1.97\times 10^{10}$ | $2.96\times 10^6,\; 1.03\times 10^7$ | PASS |
| $\operatorname{BR}(K_L \to \mu^\pm e^\mp)$ (fitted $K_{L,R}$) | $< 4.7\times 10^{-12}$ | $5.37\times 10^{-40}$ | $1.81\times 10^{-26}$ | $3.83\times 10^{-13}$ | PASS |
| $\operatorname{BR}(B_s \to \mu^\pm e^\mp)$ (generic) | $< 5.4\times 10^{-9}$ | $1.15\times 10^{-42}$ | $1.41\times 10^{-29}$ | $7.67\times 10^{-16}$ | PASS |
| $\operatorname{BR}(\mu \to e\gamma)$ (1-loop est.) | $< 3.1\times 10^{-13}$ | $1.88\times 10^{-46}$ | $2.31\times 10^{-33}$ | $1.25\times 10^{-19}$ | PASS |
| $M_{H_2}$ heavy-Higgs FCNC [GeV] | $\gtrsim 5\times 10^4$ | $4.54\times 10^{13}$ | $1.92\times 10^{10}$ | $8.94\times 10^6$ | PASS |
| SMEFT suppression $v_{\rm EW}^2 / v_R^2$ | $\lesssim 10^{-4}$ (EWPO) | $2.35\times 10^{-23}$ | $1.32\times 10^{-16}$ | $6.06\times 10^{-10}$ | PASS |
| $d=6$ proton decay (pure PS) | $\tau_p > 2.4\times 10^{34}$ yr | **FORBIDDEN** | **FORBIDDEN** | **FORBIDDEN** | PASS |
| Optional $SO(10)$ $\tau(p\to e^+\pi^0)$ | $> 2.4\times 10^{34}$ yr | N/A | $8.34\times 10^{38}$ yr | N/A | PASS |
| $\tau_{n\bar{n}}$ (in `PS1-MM` / if $\lambda_{\Delta 4}\sim 1$) | $> 4.7\times 10^8$ s | $\infty$ / $2.66\times 10^{59}$ s | $\infty$ / $8.66\times 10^{33}$ s | $\infty$ / $1.91\times 10^{17}$ s | PASS |
| Monopole mass $M_{\rm mon}$ [GeV] | Requires $T_{\rm rh} < v_R$ | $7.94\times 10^{14}$ | $2.95\times 10^{11}$ | $1.16\times 10^8$ | CONDITIONAL |
| $D$-parity domain walls | Must not overclose | ABSENT (no $\Delta_L$) | ABSENT (no $\Delta_L$) | ABSENT (no $\Delta_L$) | PASS |
| Monopole-safe thermal leptogenesis ($M_{R1} < T_{\rm rh} < v_R$) | $M_{R1} \gtrsim 10^9$ GeV | **OPEN** ($M_{R1}=7.28\times 10^9$) | **OPEN** ($M_{R1}=2.29\times 10^9$) | **CLOSED** ($M_{R1}=1.07\times 10^6$) | BM-DEPENDENT |

### Key Physics Notes on Flavour, Stability, and Relics

1. **Chiral enhancement of $K_L \to \mu^\pm e^\mp$:** Because Pati–Salam $X_\mu$ couples with equal gauge strength $g_4/\sqrt{2}$ to both left- and right-handed currents, the $(V-A)(V+A)$ Fierz rearrangement generates a pseudoscalar operator enhanced by $R_\chi = \frac{2\eta_{\rm QCD} m_K^2}{m_\mu(m_s+m_d)} \approx 100.4$ in amplitude ($\sim 10^4$ in rate), enforcing $M_X \gtrsim 2.43\times 10^6\text{ GeV}$ ($v_R \gtrsim 4.49\times 10^6\text{ GeV}$) for generic $\mathcal{O}(1)$ quark–lepton mixing. `BM-LOW` ($v_R = 10^7\text{ GeV}$) sits just above this frontier with $\operatorname{BR}(K_L \to \mu^\pm e^\mp) \simeq 3.8\times 10^{-13}$, making it directly falsifiable by next-generation kaon rare-decay experiments.
2. **Baryon-number selection rules:** Assigning global matter number $3B+L = +1$ to $F_L$ and $-1$ to $F_R^c$ gives $3B+L = 0$ on $\Phi_1, \Phi_{15}$ and $3B+L = +2$ on $\Delta_R$. Thus neither gauge bosons ($X_\mu$ is a pure leptoquark) nor any scalar in `PS1` can mediate $d=6$ $\Delta B = 1$ proton decay. Neutron–antineutron oscillations ($\Delta B = 2$, $d=9$ via $\Delta_R^4$) vanish at tree level in `PS1-MM` by exact $U(1)_\Delta$ symmetry, and remain safely above $4.7\times 10^8\text{ s}$ even if $\lambda_{\Delta 4} = \mathcal{O}(1)$ is turned on.
3. **Monopole inflation vs. thermal leptogenesis:** Because $\pi_2(G_{\rm PS}/G_{\rm SM}) = \mathbb{Z}$, reheating above $v_R$ fatally overproduces doubly-charged Pati–Salam monopoles. Requiring $T_{\rm rh} < v_R$ alongside the Davidson–Ibarra bound $M_{R1} \gtrsim 10^9\text{ GeV}$ selects high-scale benchmarks (`BM-LR` with $\epsilon_1 = 1.72\times 10^{-7}$ in `PS1-EW-min` and `BM-GUT` with $\epsilon_1 = 1.45\times 10^{-9}$ in `PS1-EW-gen`) and closes standard hierarchical thermal leptogenesis at `BM-LOW` (which would require resonant leptogenesis).

---

## 6. TP-00 Gate Update

No aggregate score is formed; every gate remains independent:

| Gate | Score | Phase 3 (`PS1-EW`) status |
|---|---:|---|
| `ALG-01` | 1 | Complete for `PS1-EW-min` and `PS1-EW-gen`; bare `PS1` remains 138-parameter underdetermined |
| `ALG-05` | 2 | Full $188\times 188$ Hessian closes: 9 Goldstones + 4 light SM Higgs + 175 heavy physical modes |
| `PERT-01` | 2 | No tree-level tachyon or accidental Goldstone in the declared `PS1-EW` vacuum |
| `PERT-03` | 1 | Tree-level Yukawa and 2-loop gauge perturbativity pass; full 1-loop unitarity/pole residues open |
| `PERT-05` | 1 | 2-loop gauge/Higgs-quartic RGEs, 1-loop thresholds, and $\lambda_\Delta=0.08$ Landau-pole control pass; EW hierarchy fine-tuning ($\Delta_{\rm FT}\sim 10^{10}\text{–}10^{23}$) and full 138-coupling scalar RG flow remain open |
| `REC-02` | 2 | Chiral SM matter, hypercharge, gauge matching, and one light SM Higgs doublet recovered |
| `REC-03` | 2 | All 9 charged-fermion masses, 4 CKM, 2 $\Delta m^2$, and 3 PMNS angles + $\delta_{\rm PMNS}$ fit to $<10^{-12}$ perturbatively in `PS1-EW-min` (`BM-LR`, complex phase) and `PS1-EW-gen` (all 3 benchmarks) |
| `NP-02` | 2 | Global high-scale vacuum certified; SM Higgs metastability stabilized by radial $\Delta_R$ threshold shift |
| `LAB-01` | 2 | Single light SM-like Higgs doublet recovered with SMEFT shifts $\le 6\times 10^{-10}$ |
| `LAB-02` | 2 | $K_L\to\mu e$, $B_s\to\mu e$, $\mu\to e\gamma$, $W_R/Z_R$, heavy-Higgs FCNCs, $\Delta B=1,2$ stability all pass for $v_R \ge 4.5\times 10^6\text{ GeV}$ |
| `COS-01` | 1 | Conditional on $T_{\rm rh} < v_R$ for monopole dilution; no $D$-parity domain walls; monopole-safe thermal leptogenesis open at `BM-LR` / `BM-GUT`; full Boltzmann transport and dark matter remain open |
| `REP-01` | 2 | All Phase 2B + Phase 3 verifiers, JSON/Markdown outputs, and 20/20 unit tests execute deterministically |

---

## 7. Reproduction

```bash
python -m pip install -r requirements.txt
make verify
```

All Phase 3 computations live in `code/verify_phase3_ew_matching.py`, unit tests in `code/tests/test_phase3_ew.py`, machine-readable outputs in `results/phase3_ew_results.json`, and the concise summary in `results/phase3_ew_summary.md`.
