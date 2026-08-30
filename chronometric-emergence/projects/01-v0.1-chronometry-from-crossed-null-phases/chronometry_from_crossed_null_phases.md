---
title: "Chronometry from Crossed Null Phases"
author: "Angus Muffatti"
version: "v0.1"
---

> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.

## 5. Exact crossed-phase theorem

Let $\phi_+$ and $\phi_-$ be circle-valued phases with null gradients

$$
k_a=\nabla_a\phi_+,
\qquad
\ell_a=\nabla_a\phi_-,
$$

$$
g^{ab}k_ak_b=g^{ab}\ell_a\ell_b=0.
$$

Assume they are nonparallel and define

$$
C=-\frac12g^{ab}k_a\ell_b>0.
$$

Set

$$
T=\frac{\phi_++\phi_-}{2},
\qquad
R=\frac{\phi_+-\phi_-}{2},
$$

and introduce the conformally invariant tensor

$$
h_{ab}=C g_{ab}.
$$

Because

$$
\nabla T=\frac{k+\ell}{2},
\qquad
\nabla R=\frac{k-\ell}{2},
$$

the inverse Gram matrix under $g$ is

$$
\begin{pmatrix}
\nabla T\cdot\nabla T & \nabla T\cdot\nabla R\\
\nabla R\cdot\nabla T & \nabla R\cdot\nabla R
\end{pmatrix}
=
\begin{pmatrix}
-C&0\\
0&C
\end{pmatrix}.
$$

Since $h^{ab}=C^{-1}g^{ab}$,

$$
\boxed{
\begin{aligned}
h^{ab}\nabla_aT\nabla_bT&=-1,\\
h^{ab}\nabla_aR\nabla_bR&=+1,\\
h^{ab}\nabla_aT\nabla_bR&=0.
\end{aligned}}
$$

Thus two crossed null phases define a unit clock direction and a unit ruler direction in their two-plane. Under $g_{ab}\rightarrow\Omega^2g_{ab}$,

$$
C\rightarrow\Omega^{-2}C,
$$

so $h_{ab}=Cg_{ab}$ is invariant.

In flat spacetime, choose

$$
\phi_+=\omega_+(t-x),
\qquad
\phi_-=\omega_-(t+x).
$$

Then

$$
C=\omega_+\omega_-,
\qquad
\eta=\frac12\ln\frac{\omega_+}{\omega_-}.
$$

Therefore

$$
\boxed{
\omega_+\omega_- = \text{clock or mass scale}^{2},
\qquad
\frac{\omega_+}{\omega_-}=\text{rapidity data}.
}
$$

The wave sum factorises as

$$
e^{i\phi_+}+e^{i\phi_-}=2e^{iT}\cos R.
$$

The mean phase is a temporal carrier and the difference phase supplies standing-wave nodes. This is the algebraic skeleton of a clock-and-ruler pair.

### Novelty correction

The exact map is not a new conformal completion. Writing $\phi_\pm=T\pm R$ and imposing exact nullity gives

$$
C=-(\nabla T)^2,
$$

and hence

$$
h_{\mu\nu}=-(g^{\alpha\beta}\partial_\alpha T\partial_\beta T)g_{\mu\nu},
$$

which is the singular conformal map of mimetic gravity, with $R$ supplying an orthogonal equal-norm ruler field [@Mimetic2013]. The theorem remains exact and useful; the broad novelty claim does not.

## 6. Homogeneous locking potential and its limitation

The first proposed mechanism introduced a mass-squared order parameter $\Sigma$ and

$$
V(C,\Sigma)
=\frac\kappa2(C-\Sigma)^2
+\frac\beta4\Sigma^2\left(\ln\frac{\Sigma}{\Lambda^2}-\frac12\right)
+\frac\beta8\Lambda^4.
$$

The stationary point

$$
C=\Sigma=\Lambda^2
$$

has Hessian

$$
H=
\begin{pmatrix}
\kappa&-\kappa\\
-\kappa&\kappa+\beta/2
\end{pmatrix},
$$

so

$$
H_{11}=\kappa>0,
\qquad
\det H=\frac{\kappa\beta}{2}>0.
$$

For $\kappa,\beta>0$, this is a strict homogeneous minimum. It demonstrates a possible algebraic lock of a crossed phase invariant to a transmuted scale. It does **not** establish kinetic rank, hyperbolicity, absence of ghosts, or a healthy $3+1$ dimensional field theory.

That distinction proved decisive.
