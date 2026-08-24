---
title: "Universal Scale Locking and the Turok-36 Test"
author: "Angus Muffatti"
version: "v0.4"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 16. A conventional hidden-sector generator

A safe infrared proof of principle uses

$$
G=G_{\mathrm{SM}}\times SU(2)_X,
$$

with the Standard Model Higgs doublet $H$ and a hidden scalar doublet $\Phi$:

$$
h=\sqrt{2H^\dagger H},
\qquad
\chi=\sqrt{2\Phi^\dagger\Phi}.
$$

The Jordan-frame action includes

$$
\frac12(\xi_\chi\chi^2+\xi_Hh^2)R,
$$

ordinary two-derivative kinetic terms, the hidden gauge field, and

$$
V
=\frac{\lambda_\chi}{2}(\Phi^\dagger\Phi)^2
-\lambda_p(H^\dagger H)(\Phi^\dagger\Phi)
+\frac{\lambda_H}{2}(H^\dagger H)^2.
$$

Hidden gauge loops generate a Coleman-Weinberg scale $f=\langle\chi\rangle$. The portal valley gives

$$
h^2=\frac{\lambda_p}{\lambda_H}\chi^2
\equiv\zeta_h^2\chi^2,
$$

and the gravitational coefficient becomes

$$
F=\xi_{\mathrm{eff}}\chi^2,
\qquad
M_{\mathrm{P}}^2=\xi_{\mathrm{eff}}f^2.
$$

This construction is not proposed as the final UV theory. Its role is to demonstrate that a conventional, unitary, two-derivative matter sector can generate and transmit one common scale [@HiddenSU22013; @CurvedSM2018].

### Exact common mode and fifth-force cancellation

In the Einstein frame,

$$
m_A^E=\frac{M_{\mathrm{P}}^{(0)}m_A(\chi)}{\sqrt{F(\chi)}}.
$$

If $m_A=c_A\chi$ and $F=\xi_{\mathrm{eff}}\chi^2$, then

$$
m_A^E=\frac{c_AM_{\mathrm{P}}^{(0)}}{\sqrt{\xi_{\mathrm{eff}}}},
$$

independent of the radial field. Therefore

$$
\alpha_A\equiv\partial_\varphi\ln m_A^E=0.
$$

Exact universal scaling produces no composition-dependent fifth force. Imperfect locking gives

$$
\alpha_A-\alpha_B
=\partial_\varphi\ln\frac{m_A}{m_B}
=\partial_\varphi\ln\frac{\omega_A}{\omega_B}.
$$

Differential fifth-force charge and differential clock drift are the same derivative obstruction [@ScaleFifthForce2016; @ScaleFifthForce2021].

## 17. Turok's 36 fields as an optional microscopic origin

Boyle and Turok proposed 36 dimension-zero fourth-order scalar fields in a programme involving anomaly cancellation, vacuum energy, and an emergent Higgs [@BoyleTurok2022]. A possible chronometric connection is that the 36-field sector might generate one collective infrared singlet $\chi$, for example through a mass gap or an invariant composite related to

$$
\mathcal O_2
=\frac1{36}G_{IJ}g^{\mu\nu}
\nabla_\mu\varphi^I\nabla_\nu\varphi^J.
$$

The mapping would be

$$
36\text{ microscopic dimension-zero fields}
\longrightarrow
1\text{ dimensionful infrared order parameter}.
$$

However, an elementary propagator with leading behaviour $1/p^4$ cannot possess a nontrivial conventional positive Källén-Lehmann spectral measure. If

$$
G(Q^2)=\int_0^\infty ds\,\frac{\rho(s)}{Q^2+s},
\qquad\rho(s)\ge0,
$$

then the leading term is

$$
G(Q^2)=\frac1{Q^2}\int\rho(s)ds+O(Q^{-4}).
$$

To begin at $1/Q^4$ requires $\int\rho=0$, which with positivity forces $\rho=0$. This does not exclude an indefinite-metric formalism, a gauge redundancy, or a healthy composite pole. It means physical positivity must be demonstrated for invariant observables, not inferred from the elementary fourth-order field.

Bateman and Turok propose a Krein-space and hidden-ghost-parity resolution, while Cline and Hell argue that ghosts, unitarity violation, and a confining fifth force remain [@BatemanTurok2026; @ClineHell2026]. The chronometric programme therefore treats the 36-field theory as an optional UV candidate subject to four mandatory tests:

1. Lorentzian unitarity on a physical state space;
2. positive spectral density or an equally strong reconstruction theorem for an invariant composite;
3. a stable condensate with $Z_\chi>0$ and real dispersion;
4. acceptable universal matter coupling without a macroscopic confining force.

The safe low-energy construction survives whether or not that candidate passes.
