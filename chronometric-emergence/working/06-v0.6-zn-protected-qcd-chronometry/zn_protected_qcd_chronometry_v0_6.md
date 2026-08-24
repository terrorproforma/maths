---
title: "Z_N-Protected QCD Chronometry"
author: "Angus Muffatti"
version: "v0.6"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 24. Exact $Z_N$ orbit

Take

$$
\mathcal G
=\left[\prod_{k=0}^{N-1}SU(3)_k\right]\rtimes Z_N,
$$

with one vectorlike colour triplet $\Psi_k$ in each sector and a compact field $a/f_a$. The masses form the exact orbit

$$
\boxed{
M_k(a)=M\left[1-\epsilon\cos\left(\frac a{f_a}+\frac{2\pi k}{N}\right)\right].
}
$$

All masses are positive for $0<\epsilon<1$. The full vacuum sums all sectors, but visible experiments probe only sector zero.

The root-of-unity identity ensures that for $m<N$,

$$
\sum_{k=0}^{N-1}\cos^m\left(x+\frac{2\pi k}{N}\right)
$$

is independent of $x$. The first nonconstant Coleman-Weinberg harmonic is therefore the $N$th:

$$
V_{\mathrm{CW}}(a)
=\frac{N_cM^4\epsilon^N}{8\pi^2}F_N
\cos\frac{Na}{f_a}[1+O(\epsilon)],
$$

where for $N>4$,

$$
F_N=\frac{24\,2^{1-N}}
{(N-1)(N-2)(N-3)(N-4)}.
$$

The one-sector visible threshold derivative remains $O(\epsilon)$, while the complete-orbit vacuum mass is $O(\epsilon^N)$. This established discrete-Goldstone mechanism is adapted here to a real vectorlike QCD threshold [@DasHook2020; @Brzeminski2020; @DiLuzio2021].

![The complete orbit cancels lower vacuum harmonics while preserving a one-sector linear threshold response.](figures/z6_mass_orbit_and_potential.png){#fig:z6 width=88%}

## 25. Minimal clean choice: $Z_6$

The smallest even $N>4$ that supplies a symmetry-related vacuum with maximal visible slope is $N=6$. Choose

$$
x_0=\frac{a_0}{f_a}=\frac\pi2.
$$

Then $M_0=M$ and

$$
\frac{\partial}{\partial x}
\ln\frac{M_0}{\chi}=\epsilon.
$$

Since $F_6=1/160$,

$$
\boxed{
m_a^2
=\frac{27}{320\pi^2}
\frac{M^4}{f_a^2}\epsilon^6+O(\epsilon^7).
}
$$

The visible QCD coupling remains

$$
\boxed{
d_g=\frac{2}{27}\frac{M_{\mathrm{P}}}{f_a}\epsilon
+O(\alpha_s\epsilon,\epsilon^2).
}
$$

Compared with the unprotected mass,

$$
\boxed{
\frac{m_{a,Z_6}^2}{m_{a,\mathrm{naive}}^2}
=\frac9{80}\epsilon^4.
}
$$

This makes an astronomical-range scalar compatible with a much larger visible response. The quality conditions are severe: the exact exchange symmetry must be microscopic, and local operators such as $\Phi^6$ must be forbidden or nonlocally suppressed. A Wilson-line or collective-pNGB completion is the preferred route [@Hor2026].
