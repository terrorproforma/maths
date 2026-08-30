---
title: "Direct AMY LPM Transport and Full-Angle Screened Thermalisation"
author: "Angus Muffatti"
version: "v1.4"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 50. Direct AMY upgrade

The v1.4 calculation directly solved the isotropic AMY transverse LPM equation for the QCD splitting channels and replaced angle-averaged elastic scattering by deterministic full-angle screened quadrature. At the reheating benchmark

$$
\frac{M_D}{T}=0.01,
\qquad
\alpha_s=0.0393544,
\qquad
y_D=0.30,
\qquad
\frac pT=3,
$$

the dimensionless rates are

$$
\frac{\Gamma_{g\to gg}}T=0.261356,
$$

$$
\frac{\Gamma_{q\to gq}}T=0.204516,
\qquad
\frac{\Gamma_{D\to gD}}T=0.201417,
$$

$$
\frac{\Gamma_{g,\mathrm{elastic}}}T=0.106177,
\qquad
\frac{\Gamma_{q,\mathrm{elastic}}}T=0.0119151,
$$

and

$$
\boxed{
\frac{\Gamma_{H\leftrightarrow qD}}T
=3.18544\times10^{-4}.
}
$$

The QCD rates are fast. The slow mode is the scalar-Yukawa conversion $H\leftrightarrow qD$. At

$$
T_0=1.002\times10^8\,\mathrm{GeV},
$$

the kinetic rate is

$$
\Gamma_{\mathrm{kin}}=3.1918\times10^4\,\mathrm{GeV}.
$$

Compared with

$$
\Gamma_R=1.47850065\times10^{-2}\,\mathrm{GeV},
$$

one obtains

$$
\boxed{
\frac{\Gamma_{\mathrm{kin}}}{\Gamma_R}
=2.1588\times10^6.
}
$$

Even a conservative factor-of-two normalisation uncertainty leaves $1.0794\times10^6$. The correction to the desired reheating branch is negligible.

![The slow portal conversion remains more than six orders of magnitude faster than reheaton decay.](figures/kinetic_rate_hierarchy.png){#fig:rates width=84%}

## 51. What v1.4 did and did not solve

The direct AMY calculation substantially closes the QCD kinetic problem. It does not yet contain the complete electroweak/Yukawa LPM structure of $H\leftrightarrow qD$. The outstanding calculation requires:

1. the complete helicity and Higgs-doublet source structure;
2. simultaneous $SU(3)_c$, $SU(2)_L$, and $U(1)_Y$ soft collision kernels;
3. thermal widths and asymptotic masses;
4. exact matching to the scalar retarded self-energy;
5. insertion into a reduced gauge-covariant Schwinger-Keldysh model.

Only after that does a full $3+1$ dimensional non-Abelian 2PI/Kadanoff-Baym computation become the rational next expenditure. The QCD sector is already far too fast to be the weak link.
