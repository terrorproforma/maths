---
title: "Cosmological Vacuum Selection and the Maximal Chronometric-Shear Ridge"
author: "Angus Muffatti"
version: "v0.8"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 27. Homogeneous evolution

The cosmological mode obeys

$$
\ddot x+3H\dot x+\frac{1}{f_a^2}
\frac{\partial V_{\mathrm{eff}}(x,t)}{\partial x}=0,
$$

with

$$
V_{\mathrm{eff}}=V_0+V_{\Psi,T}+V_{{\mathrm{QCD}},T}+V_b.
$$

The protected vacuum is

$$
V_0(x)=\frac{m_a^2f_a^2}{N^2}(1+\cos Nx),
$$

with minima $x_v=(2j+1)\pi/N$.

## 28. Reheating phasor

Let sector temperatures be $T_k=\xi_kT_0$. The leading field-dependent high-temperature threshold potential is governed by

$$
W_2=\sum_{k=0}^{N-1}\xi_k^2e^{2\pi ik/N},
$$

and selects

$$
x_T=-\arg W_2.
$$

The successful sparse population is

$$
\xi_0=1,
\qquad
\xi_5=0.25,
\qquad
\xi_{1,2,3,4}\ll1.
$$

For $N=6$,

$$
x_T=0.0524383.
$$

The bias scales as $\xi^2$, while dark radiation scales as $\xi^4$. One adjacent complete Standard Model copy at $\xi=0.25$ gives the project value

$$
\Delta N_{\mathrm{eff}}=0.0289,
$$

whereas populating all five hidden replicas at that temperature would be excessive under the cited cosmological bound [@GoldsteinHill2026].

## 29. QCD crossover as a second lens

Write the QCD pressure as

$$
p(T,\Lambda)=T^4P(T/\Lambda).
$$

Dimensional analysis gives

$$
\frac{\partial F}{\partial\ln\Lambda}=\rho-3p\equiv\Theta(T).
$$

Since

$$
\Lambda_k(x)=\Lambda_0
\left[1-\epsilon\cos\left(x+\frac{2\pi k}{N}\right)\right]^{2/27},
$$

the leading QCD term is

$$
\boxed{
V_{{\mathrm{QCD}},k}
=\frac{2}{27}\Theta(T_k)
\ln\left[1-\epsilon\cos\left(x+\frac{2\pi k}{N}\right)\right].
}
$$

The lattice-QCD trace anomaly produces a second focusing epoch near $T\simeq0.179$ GeV in the strong benchmark [@Borsanyi2016].

## 30. Baryon locking and late release

Visible baryons contribute

$$
V_b(x,a)=\rho_b(a)(1-\epsilon\cos x)^{2/27}.
$$

Near the even-$N$ thermal point, baryons supply positive curvature. The vacuum potential eventually becomes tachyonic there and releases the field into an adjacent minimum. In the preferred benchmark, this occurs around

$$
z_{\mathrm{inst}}\simeq450.
$$

The chronology is

$$
\boxed{
\text{heavy-threshold focusing}
\rightarrow
\text{QCD refocusing}
\rightarrow
\text{baryon locking}
\rightarrow
\text{late vacuum release}.
}
$$

## 31. Strong-attractor benchmark and ridge

The original Planck-scale benchmark was cosmologically unsatisfactory: thermal focusing was negligible and generic misalignment overclosed the Universe. The successful strong-attractor point is

$$
\boxed{
\begin{aligned}
N&=6,\\
f_a&=2.435\times10^{10}\,\mathrm{GeV},\\
\epsilon&=2.70\times10^{-13},\\
M&=1.002\times10^6\,\mathrm{GeV},\\
T_R&=1.002\times10^8\,\mathrm{GeV},\\
m_a&=7.5\times10^{-29}\,\mathrm{eV},\\
d_g&=10^{-6}.
\end{aligned}}
$$

The focusing measures are

$$
\eta_{\Psi,\max}=612,
\qquad
\eta_{{\mathrm{QCD}},\max}=759.
$$

Twelve tested homogeneous initial phases converged to

$$
x_v=+\frac\pi6.
$$

This is a numerical existence result, not a global theorem. A moderate point with $\eta_{\Psi,\max}\approx30.6$ did not select a unique branch. Merely having $m_T/H>1$ is insufficient.

The viable $N=6$ ridge at representative $m_a$ and the stated cuts is approximately

$$
1.6\times10^9\,\mathrm{GeV}
\lesssim f_a\lesssim
9.4\times10^{12}\,\mathrm{GeV},
$$

$$
2.6\times10^3\,\mathrm{GeV}
\lesssim M\lesssim
1.6\times10^7\,\mathrm{GeV}.
$$

Cosmology chooses a viable branch and sign; equivalence-principle tests cap the magnitude of shear.

## 32. Observable scale and domain conditions

For annual solar-potential modulation $\Delta\Phi_\odot=3.29\times10^{-10}$,

$$
\left|\Delta\ln\frac{\nu_A}{\nu_B}\right|_{\mathrm{yr}}
=2|K_{AB}|d_g^2\Delta\Phi_\odot.
$$

At $d_g=10^{-6}$,

$$
\boxed{
\left|\Delta\ln\frac{\nu_A}{\nu_B}\right|_{\mathrm{yr}}
=6.58\times10^{-22}|K_{AB}|.
}
$$

Ordinary atomic sensitivities are far below current reach. Provisional thorium strong-sector enhancements of order $10^4$ would raise the illustrative signal to $6.58\times10^{-18}$, but the nuclear coefficients remain model dependent [@Arakawa2026; @Thorium2026].

The six vacua require either pre-inflation symmetry breaking with no restoration or a gauged/discrete completion. A sufficient homogeneity condition is

$$
\frac{H_{\mathrm{inf}}}{2\pi f_a}\ll x_T.
$$

For the benchmark,

$$
H_{\mathrm{inf}}\ll8.0\times10^9\,\mathrm{GeV}.
$$

The compact field is not the dark matter on the optimised ridge; its abundance is negligible.
