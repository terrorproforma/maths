---
title: "Exact Selector-Threshold Matching and Nonlinear Momentum-Lattice Cascade"
author: "Angus Muffatti"
version: "v1.2"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 45. Factorised three-loop matching

Because the first mixed graph is two-particle reducible, its zero-momentum coefficient factorises into a one-loop selector kernel and a mass derivative of the known two-loop fermion-fermion-scalar effective potential [@Martin2001]. In the scalar proxy,

$$
\mathcal I_3(\bar\mu)
=2m_R^2K_{RRH}(m_R^2,m_h^2)
D_{FFS}(M^2,m_h^2;\bar\mu).
$$

At $\bar\mu=M$,

$$
\boxed{
\mathcal I_3(M)=6.57973508149\simeq\frac{2\pi^2}{3}.
}
$$

The first proxy coefficient gave

$$
|\Delta V_{Qa}^{(3)}|
=2.1723\times10^3\,\mathrm{GeV}^4,
$$

or only $1.546\times10^{-12}$ of the intended thermal focusing potential.

The fixed-order hard function had a huge apparent scale excursion. This was explicitly identified as missing RG completion, not a physical uncertainty.

## 46. Spurion-graded operator mixing

A correction to the earlier claim was necessary. Exact $Z_6$ does not make the complete invariant transient basis block diagonal, because combinations $e^{ipx}\mathcal X_{-p}$ are individually invariant. The correct selection rule is

$$
\boxed{
\gamma_{(A,p)(B,q)}
=\sum_{r,s\ge0}
\delta^{(6)}_{p-q,r-s}
\epsilon^{r+s}\Gamma_{AB}^{(r,s)}.
}
$$

Changing harmonic charge requires explicit shift-breaking spurions. The powers of $\epsilon$ are fixed, although the finite tensors depend on the messenger completion.

## 47. Nonlinear momentum-lattice cascade and corrected branching

The repaired sequence is

$$
\phi\rightarrow N_0\bar N_0
\rightarrow R_0\nu_0
\rightarrow H_0,H_5
\rightarrow D_k,q_k,g_k.
$$

A radial momentum-lattice calculation included expansion, backreaction, two-body decays, Pauli blocking, and an energy-conserving plasma closure. It exposed a genuine error in the v0.9 branching argument.

The massless $\nu_0$ daughter deposits visible-sector energy earlier than the reheaton products and experiences a different redshift history. Therefore the attractive exact choice

$$
\tan\theta=\frac1{16}
$$

does not yield the desired final temperature ratio. The simulation gave

$$
\mathcal R_\nu
=\frac{E_\nu}{E_R^{(1)}}
=0.35551328.
$$

Imposing $E_5/E_0=1/256$ requires

$$
\boxed{
B_5^*=\frac{1+\mathcal R_\nu}{257}
=0.00527437074,
}
$$

The v1.2 note reported

$$
\tan\theta=0.0728196.
$$

Direct recomputation from the displayed value of $B_5^*$ gives

$$
\tan\theta
=\sqrt{\frac{B_5^*}{1-B_5^*}}
=0.07281715.
$$

The difference is a small historical rounding inconsistency and is recorded rather than silently erased. The resulting v1.2 calculation obtained

$$
\frac{T_5}{T_0}=0.250000001.
$$

After restoring the complete Higgs-doublet and relativistic-$D$ contribution to $g_*$ in v1.3, the superseding branch was

$$
B_5=0.00529888708,
\qquad
\tan\theta=0.0729871.
$$

This correction is retained as a warning against replacing a resolved cascade with an aesthetically neat branching identity.
