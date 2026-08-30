---
title: "Environmental Non-Screening of the Z6 Chronometric Ratio Mode"
author: "Angus Muffatti"
version: "v0.7"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 26. Nonlinear environmental equation

Let $x=a/f_a$. The static spherical equation is

$$
\nabla^2x
=-\frac{m_a^2}{6}\sin6x
+\sum_A\frac{\rho_A}{f_a^2}
 p_A\epsilon\sin x
 (1-\epsilon\cos x)^{p_A-1}.
$$

The benchmark

$$
M=10\,\mathrm{TeV},
\qquad
f_a=M_{\mathrm{P}},
\qquad
\epsilon=10^{-6}
$$

has

$$
m_a=3.797\times10^{-21}\,\mathrm{eV},
\qquad
\lambda_a=347.4\,\mathrm{AU}.
$$

### Homogeneous spinodal versus finite-body conversion

Define the local density parameter

$$
t=\frac{\rho p\epsilon}{m_a^2f_a^2}.
$$

The branch connected to $x_\infty=\pi/2$ disappears in an infinite homogeneous medium above

$$
t_*=0.17272340294,
$$

corresponding in the benchmark to

$$
\rho_{\mathrm{spinodal}}=46.25\,\mathrm{g\,cm^{-3}}.
$$

The solar core exceeds this local threshold. A finite body must also pay gradient energy. For a core of radius $R_c$, define

$$
q(R_c)=\frac{M(<R_c)p\epsilon}{4\pi f_a^2R_c}.
$$

Conversion to the adjacent phase requires at least

$$
\boxed{q(R_c)>q_{\mathrm{conv}}=0.633135.}
$$

Earth, Sun, and a 5 cm tungsten source fall short by enormous margins.

| Source | Largest $q/q_{\mathrm{conv}}$ | Surface shift | Screening factor |
|---|---:|---:|---:|
| Earth | $1.63\times10^{-16}$ | $-1.03\times10^{-16}$ | $1.000000$ |
| Sun | $1.02\times10^{-12}$ | $-3.15\times10^{-13}$ | $1.000000$ |
| 5 cm tungsten | $3.50\times10^{-32}$ | $-2.22\times10^{-32}$ | $1.000000$ |

![Density can prefer another phase locally, but finite objects are much too weakly compact to realise it.](figures/environmental_conversion_margin.png){#fig:environment width=82%}

The Sun therefore provides the desired source without screening it. The field’s response length is vastly larger than the source, so it reacts to integrated scalar charge rather than tracking a local density minimum. This is a thick-shell/no-shell regime rather than a chameleon thin shell [@Chameleon2008; @FiniteDensity2024].

### Finite-size bound

Using $G=(8\pi M_{\mathrm{P}}^2)^{-1}$,

$$
q=2p\epsilon\left(\frac{M_{\mathrm{P}}}{f_a}\right)^2\Phi,
$$

where $\Phi=GM/(Rc^2)$. If

$$
f_a\ge M_{\mathrm{P}},
\qquad
\epsilon\le1,
\qquad
p\le\frac{2}{27},
$$

then any nonsingular spherical body outside a trapped surface has

$$
q<\frac{2}{27}<q_{\mathrm{conv}}.
$$

This excludes complete matter-driven conversion for that parameter class, not cosmological domains or more elaborate UV interactions.
