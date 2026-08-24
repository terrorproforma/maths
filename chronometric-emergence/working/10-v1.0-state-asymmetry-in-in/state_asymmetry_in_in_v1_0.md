---
title: "State Asymmetry in the In-In Effective Action"
author: "Angus Muffatti"
version: "v1.0"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 36. Vacuum, selector, and state functionals

The in-in effective action separates schematically as

$$
\Gamma_{\mathrm{CTP}}
=\Gamma_{\mathrm{vac}}+\Gamma_Q+\Gamma_\rho.
$$

Exact microscopic $Z_6$ implies

$$
\Gamma_{\mathrm{vac}}[a]
=\sum_{q\in\mathbb Z}c_{6q}e^{i6qa/f_a},
$$

so

$$
c_p^{\mathrm{vac}}=0,
\qquad p=1,\ldots,5.
$$

During a transient one-hot selector background, the action may contain

$$
\epsilon^p e^{ipa/f_a}\mathcal Q_{-p}[Q]+\mathrm{h.c.},
$$

where the selector carries compensating cyclic charge. These terms vanish when $Q\rightarrow0$.

An asymmetric density matrix can also produce lower harmonics through occupation charges

$$
\mathcal N_p=\sum_kn_ke^{-2\pi ipk/6}.
$$

These are intended finite-density forces. They dilute or disappear with the state. The central covariance relation is

$$
\Gamma_{z\rho z^{-1}}[z\phi,zQ]
=\Gamma_\rho[\phi,Q].
$$

A forbidden lower harmonic must therefore be accompanied by selector or state charge. Under the displayed interaction graph, neither can become a permanent state-independent Wilson coefficient merely by disappearing.

## 37. Two-loop result

At two loops, the selector-reheaton-bath graph and the $a$-dependent threshold-QCD graph are not directly joined by a primitive vacuum vertex. Selector information reaches the threshold through propagators and occupation numbers prepared by reheating. Decomposing

$$
S_k=S_{k,\mathrm{vac}}+\delta S_{k,\rho},
\qquad
D_k=D_{k,\mathrm{vac}}+\delta D_{k,\rho},
$$

shows that the complete-orbit all-vacuum term cancels the forbidden harmonics; every $p<6$ contribution contains at least one state insertion.

The physical equation takes the form

$$
\Box a+V_0'(a)
+\sum_kM_k'(a)\langle\bar\Psi_k\Psi_k\rangle_{\rho,\mathrm{ren}}=0.
$$

In influence-functional language, the environment supplies:

- a local finite-density force;
- a retarded memory and dissipation kernel;
- a noise kernel.

A decaying state can leave temporary memory but not automatically a permanent local vacuum term. A conserved relic or hydrodynamic zero mode would preserve a state-dependent source, not a new vacuum spurion.

The NLO thermal-QCD audit increased focusing by about $6.19\%$ and shifted the selected phase by only $1.72\times10^{-4}$ rad. The branch mechanism was perturbatively stable at this order [@ThermalPressure2021].

## 38. Initial-state renormalisation

Non-vacuum initial states can introduce ultraviolet divergences. For UV-soft or Hadamard-like data, ordinary bulk counterterms suffice. More general short-distance structure requires counterterms on the initial hypersurface,

$$
S_{\partial,\rho}
=\int_{t=t_0}d^3x\,\mathcal L_{\partial,\rho}.
$$

This is distinct from a permanent late-time bulk term. The preparation protocol must still be explicitly renormalised [@CollinsHolman2005; @Berges2005].

## 39. Necessary protection package

Exact $Z_6$ is necessary but not sufficient. The UV theory must also satisfy

$$
\epsilon\rightarrow0
\quad\Longrightarrow\quad
U(1)_a\text{ shift symmetry is restored}.
$$

Every nonderivative $a$ dependence must carry explicit powers of the same breaking spurion. The robust package is

$$
\boxed{
\text{exact }Z_6
+\text{continuous-shift spurion counting}
+\text{no direct }Q\text{-threshold portal}
+\text{UV-soft state preparation}.
}
$$
