---
title: "RG-Improved Transient Matching and Explicit Thermal Collision Kernel"
author: "Angus Muffatti"
version: "v1.3"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 48. RG-improved hard function

The fixed-order function was

$$
\begin{aligned}
D_{FFS}^{\mathrm{fixed}}(\bar\mu)
={}&2\ln\frac xz\ln\frac{x-z}{\bar\mu^2}
-\ln^2\frac{x}{\bar\mu^2}\\
&-2\operatorname{Li}_2\left(\frac zx\right)
+\frac{\pi^2}{3}.
\end{aligned}
$$

Combining it with operator running and the matching counterterm yields

$$
\boxed{
D_{FFS}^{\mathrm{hard}}
=2\ln\frac xz\ln\left(1-\frac zx\right)
-2\operatorname{Li}_2\left(\frac zx\right)
+\frac{\pi^2}{3}.
}
$$

Its explicit matching-scale derivative vanishes. The benchmark remains

$$
\mathcal I_3^{\mathrm{hard}}=6.57973508149.
$$

Ordinary coupling and portal running leaves only

$$
0.96469<\frac{C_3(\mu_D)}{C_3(M)}<1.03745
$$

for $M/2<\mu_D<2M$.

Restoring the full Higgs doublet and colour multiplicities gives

$$
C_3^{\mathrm{full}}=1.58896\times10^{-4}\,\mathrm{GeV}^2,
$$

$$
|\Delta V_{Qa}^{(3)}|
=4.2902\times10^3\,\mathrm{GeV}^4,
$$

still only $3.053\times10^{-12}$ of the thermal potential.

A separate warning survives: in the minimal one-loop high-scale run, the Higgs quartic becomes negative. The matching calculation is stable, but the displayed scalar sector is not yet a complete metastable UV benchmark.

## 49. Reduced explicit collision kernel

The v1.3 calculation replaced a fitted BGK closure by a microscopic discrete gain/loss operator for

$$
H,\quad D,\quad q,\quad g.
$$

It included six $1\leftrightarrow2$ channel families, eight $2\leftrightarrow2$ families, Bose enhancement, Pauli blocking, Debye screening, asymptotic thermal masses, an LPM formation-time reduction, and exact discrete energy conservation.

The lattice contained 514 collinear transitions and 14,289 elastic transitions. It reached $99\%$ of the equilibrium entropy gain by $Tt=3920$, with detailed-balance residual $8.57\times10^{-17}$ and energy drift $1.44\times10^{-15}$. The resulting hierarchy was

$$
\frac{\Gamma_{\mathrm{kin}}^{(99)}}{\Gamma_R}
=1.729\times10^6.
$$

Therefore homogeneous energy bookkeeping can adiabatically eliminate the fast plasma without a phenomenological BGK rate [@AMY2002; @Boedeker2019].
