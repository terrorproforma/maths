---
title: "QCD Chronometric Lock: All-Orders Threshold Propagation and the 2/27 Signal"
author: "Angus Muffatti"
version: "v0.5"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 18. Scale-invariant quantum definition

To prevent QCD from acquiring an independent subtraction standard, work in $d=4-2\varepsilon$ and replace the external regularisation scale by

$$
\mu_\chi=z\,\chi^{1/(1-\varepsilon)},
$$

where $z$ is dimensionless. The bare strong coupling is

$$
g_{s,0}=\mu_\chi^\varepsilon Z_g g_s.
$$

Renormalisation generates an infinite tower of scale-invariant higher-dimensional operators. The result is an all-orders Wilsonian EFT, not a finite-parameter UV completion. In a homogeneous background, every physical gap takes the form

$$
M_A=f\,\mathcal F_A(g_i,z,c_k,\ldots),
$$

and

$$
\Lambda_{n_f}=c_{n_f}\chi.
$$

Slowly varying backgrounds receive derivative corrections such as

$$
\Lambda_{n_f}(x)=c_{n_f}\chi(x)
\left[1+c_\Box\frac{\Box\chi}{\chi^3}
+c_\partial\frac{(\nabla\chi)^2}{\chi^4}+\cdots\right].
$$

The physical statement is not merely "evaluate $g_s$ at $\mu=\chi$." It is that the quantum theory contains no independent dimensionful standard besides $\chi$.

## 19. Exact threshold propagation theorem

Let a heavy coloured particle $j$ with renormalisation-group-invariant mass $\widehat m_j$ be integrated out. Dimensional analysis gives

$$
\Lambda_{n-1}
=\widehat m_j\,
\mathcal F_j\left(\frac{\Lambda_n}{\widehat m_j}\right).
$$

Define

$$
A_j=\frac{\partial\ln\mathcal F_j}
{\partial\ln(\Lambda_n/\widehat m_j)}.
$$

Differentiation yields

$$
d\ln\Lambda_{n-1}
=A_jd\ln\Lambda_n
+(1-A_j)d\ln\widehat m_j.
$$

Define the lock and threshold defects

$$
\delta_n=d\ln\frac{\Lambda_n}{\chi},
\qquad
\epsilon_j=d\ln\frac{\widehat m_j}{\chi}.
$$

Then

$$
\boxed{
\delta_{n-1}=A_j\delta_n+(1-A_j)\epsilon_j.
}
$$

For many thresholds,

$$
\delta_3
=\left(\prod_{n=4}^{N}A_n\right)\delta_N
+\sum_{n=4}^{N}(1-A_n)
\left(\prod_{k=4}^{n-1}A_k\right)\epsilon_n.
$$

If the high-energy theory and every threshold are locked, the low-energy theory remains locked to all orders. Scheme and loop dependence live in the physical response coefficients $A_j$, not in the structure of the recursion [@Chetyrkin1997].

## 20. A controlled coloured defect

Introduce one real scalar $S$ and a vectorlike Dirac fermion

$$
\Psi\sim(\mathbf3,\mathbf1,0),
$$

with

$$
\mathcal L_{\Psi S}
=\bar\Psi(i\gamma^\mu D_\mu-y_\chi\chi-y_SS)\Psi
-\frac12(\partial S)^2
-V_{\chi S},
$$

$$
V_{\chi S}
=V_\chi(\chi)
+\frac{\lambda_S}{4}(S^2-r^2\chi^2)^2
+\Delta V_{\mathrm{ct}}.
$$

At alignment, $S=r\chi$ and

$$
M_\Psi=\chi(y_\chi+y_Sr).
$$

Parameterise the ratio fluctuation by

$$
\frac S\chi=re^\theta.
$$

Then

$$
\boxed{
 d\ln\frac{M_\Psi}{\chi}
 =\varepsilon_\Psi d\theta,
\qquad
\varepsilon_\Psi=\frac{y_Sr}{y_\chi+y_Sr}.
}
$$

This is a physical crack in universal locking: it changes a dimensionless threshold ratio rather than merely rescaling every mass.

## 21. The $2/27$ transmission coefficient

The threshold chain is

$$
7\xrightarrow{\Psi}6\xrightarrow{t}5\xrightarrow{b}4\xrightarrow{c}3.
$$

Assume the high-energy QCD scale and the top, bottom, and charm thresholds remain exactly locked. At one loop,

$$
A_\Psi=\frac{19}{21},
\qquad
A_t=\frac{21}{23},
\qquad
A_b=\frac{23}{25},
\qquad
A_c=\frac{25}{27}.
$$

Therefore

$$
\begin{aligned}
\mathcal D_{\Psi\to3}^{(1)}
&=\left(1-\frac{19}{21}\right)
\frac{21}{23}\frac{23}{25}\frac{25}{27}\\
&=\boxed{\frac{2}{27}}.
\end{aligned}
$$

The first controlled defect is

$$
\boxed{
 d\ln\frac{\Lambda_3}{\chi}
 =\frac{2}{27}\varepsilon_\Psi d\theta
 +O\left(\alpha_s\varepsilon_\Psi,
 \varepsilon_\Psi^2,
 \frac{\partial^2}{\chi^2}\right).
}
$$

For a Dirac fermion in colour representation $R$,

$$
\mathcal D_{R\to3}^{(1)}=\frac{4T(R)}{27}.
$$

Again, the coefficient is not new. The new use is to make the first low-energy failure of universal time calibration calculable rather than arbitrary.

## 22. Clock and equivalence-principle predictions

A low-energy clock ratio obeys

$$
\mathcal S_{AB}
=\Delta K_\alpha d\ln\alpha
+\Delta K_\mu d\ln\mu
+\Delta K_q d\ln X_q+\cdots,
$$

with

$$
\mu=\frac{m_p}{m_e},
\qquad
X_q=\frac{\widehat m}{\Lambda_3}.
$$

In the pure-QCD benchmark,

$$
d\ln\alpha=0,
\qquad
d\ln\mu\simeq\delta_3,
\qquad
d\ln X_q=-\delta_3.
$$

Thus

$$
\boxed{
\mathcal S_{AB}
=(\Delta K_\mu-\Delta K_q)
\frac{2}{27}\varepsilon_\Psi d\theta+\cdots.
}
$$

At leading sensitivity, the illustrative ratios give

$$
\mathcal S_{\mathrm{Sr}/Cs}
=2\mathcal S_{\mathrm{Sr}/CaF}.
$$

This is a rank-one pattern, conditional on one dominant scalar and the stated clock sensitivities [@ClockData2023; @ClockReview2025].

Let $a=f_a\theta$ and $\varphi=a/M_{\mathrm{P}}$. The gluonic coupling is

$$
d_g
=\frac{\partial}{\partial\varphi}
\ln\frac{\Lambda_3}{\chi}
=\frac{2}{27}\varepsilon_\Psi\frac{M_{\mathrm{P}}}{f_a}+\cdots.
$$

In the one-scalar, unscreened, QCD-dominated limit, the anomalous clock redshift $\beta_{AB}$ and Eötvös parameter $\eta_{CD}$ satisfy

$$
\boxed{
\frac{\beta_{AB}}{\eta_{CD}}
=-\frac{\Delta K_\mu-\Delta K_q}
{\Delta Q'_{\widehat m}{}^{CD}}.
}
$$

For the project’s leading Ti/Pt charge model, the conditional values are approximately $150.38$ for Sr/CaF and $300.76$ for Sr/Cs. They are model-consistency lines, not new experimental limits [@DamourDonoghue2010; @MICROSCOPE2022].

## 23. The radiative naturalness obstruction

The coloured fermion contributes

$$
\Delta V_\Psi
=-\frac{N_c}{16\pi^2}M_\Psi(\theta)^4
\left[\ln\frac{M_\Psi(\theta)^2}{\mu^2}-\frac32\right].
$$

The ratio mode receives

$$
\boxed{
m_a^2\sim\frac{N_c}{4\pi^2}
\varepsilon_\Psi^2\frac{M_\Psi^4}{f_a^2}.
}
$$

A long-range observable signal is therefore catastrophically unnatural in the minimal one-threshold model. The programme requires a symmetry that suppresses the vacuum mass more strongly than the visible linear coupling.
