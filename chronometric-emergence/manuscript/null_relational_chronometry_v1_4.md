---
title: "Null-Relational Chronometry"
subtitle: "From causal structure to universal spectral time: crossed-null kinematics, scale locking, QCD-transmitted chronometric shear, protected cosmology, and nonequilibrium transport"
author: "Angus Muffatti"
date: "Consolidated manuscript incorporating research notes v0.1-v1.4"
lang: en-GB
bibliography: references.bib
link-citations: true
reference-section-title: References
abstract: |
  This manuscript consolidates the complete research programme developed from the question of whether a photon, a null frame, or relations among massless fields can supply the structure normally attributed to time. The result is not a theory in which a photon has a rest-frame perspective, nor a claim that causal order is created by matter. The defensible thesis is narrower: causal or conformal structure may be primitive, while the metric calibration of duration can be reconstructed from physical spectra when all viable clocks share one local scalar factor. The programme begins with exact crossed-null kinematics, records the failure of an exact-null constrained action, replaces it with a healthy soft-null effective theory, proves a universal-clock factorisation theorem, and constructs a conventional scale-generating matter model. It then derives an all-orders QCD threshold recursion and the leading $2/27$ transmission of a controlled scale-lock defect into observable clock disagreement. A cyclic $Z_6$ construction protects an ultralight ratio mode, nonlinear environmental calculations show that Earth and the Sun do not screen it, and a cosmological attractor selects a nonzero branch. Exact action symmetry is reconciled with asymmetric reheating by placing the asymmetry in the state rather than in a permanent coupling. Closed-time-path, higher-loop matching, nonlinear cascade, renormalisation-group, and Arnold-Moore-Yaffe transport audits progressively remove several failure modes. The present frontier is the complete electroweak/Yukawa LPM problem for $H\leftrightarrow qD$ and, beyond it, a reduced gauge-covariant Schwinger-Keldysh treatment. All claims are classified as established, derived within the displayed model, conditional, failed, or open; no absolute priority or quantum-gravity completion is claimed.
---

\newpage

# Executive synthesis

## The question that started the programme

A photon follows a null curve and accumulates zero proper time between emission and absorption. That fact does **not** endow it with an inertial rest frame. A Lorentz boost to the speed of light is singular, and coordinates adapted to a null generator do not become the coordinates of a clock-bearing observer. Their stationary curves are null, their intrinsic metric is degenerate, and no ordinary three-dimensional rest space exists. The phrase "from the photon's perspective" therefore fails at the level of observer structure, not merely at the level of a difficult measurement.

The failure is productive. It isolates what a single null direction lacks:

1. a complementary null direction or nonparallel energy flow from which a timelike direction can be formed;
2. a relative normalisation that distinguishes common scale from rapidity;
3. a dimensionful spectral standard that can turn progression into measured duration;
4. an observable relative phase rather than an unobservable overall phase.

The research programme asks whether those missing structures can be generated relationally. The mature question is not "does a photon experience the Universe instantaneously?" It is:

> Given causal/conformal structure and interacting physical fields, under what conditions does one operational proper-time metric emerge for every material clock, and what observable measures the failure of that universality?

The answer developed here is:

$$
\boxed{
\text{causal order is input; universal duration calibration can be a derived field relation.}
}
$$

This is compatible with the Ehlers-Pirani-Schild programme, causal-reconstruction theorems, and the fact that null propagation determines conformal rather than metric geometry [@EPS1972; @HKM1976; @Malament1977; @Braun2025]. The new work lies, if anywhere, in the restricted conjunction of a universal spectral theorem, its QCD-transmitted obstruction, a protected cosmological realisation, and a controlled nonequilibrium preparation mechanism. It does **not** lie in the elementary observation that two null vectors can be combined into a timelike one.

![The consolidated emergence chain.](figures/chronometric_emergence_chain.png){#fig:emergence width=95%}

## The integrated claim

Let $(\mathcal M,[g])$ be a Lorentzian conformal spacetime. Let every physically viable clock transition $A$ be represented by a positive local angular frequency $\omega_A(x)$ of Weyl weight $-1$, so its accumulated phase is

$$
\Phi_A[\gamma]=\int_\gamma \omega_A\,ds_g.
$$

The phase is invariant under

$$
g_{\mu\nu}\rightarrow \Omega^2g_{\mu\nu},
\qquad
\omega_A\rightarrow \Omega^{-1}\omega_A.
$$

One conformal representative calibrates **all** clocks if and only if

$$
\boxed{
\omega_A(x)=c_A\chi(x)
\quad\text{for every clock }A,
}
$$

where $c_A$ is a constant and $\chi$ is one shared Weyl-weight $-1$ scalar. Equivalently,

$$
\boxed{
\mathcal S_{AB}
\equiv d\ln\frac{\omega_A}{\omega_B}=0
\quad\text{for every pair }A,B.
}
$$

When factorisation holds, the operational metric is

$$
\boxed{
\widehat g_{\mu\nu}
=\left(\frac{\chi}{\chi_*}\right)^2 g_{\mu\nu},
}
$$

unique up to one global unit convention. The one-forms $\mathcal S_{AB}$ are called **chronometric shear**. They are Weyl invariant and measure an obstruction that cannot be removed by changing conformal frame.

A concrete matter model can lock

$$
\frac{h}{\chi},
\qquad
\frac{\Lambda_{\mathrm{QCD}}}{\chi},
\qquad
\frac{M_{\mathrm{P}}}{\chi}
$$

to constants. Exact locking yields rank-zero clock response and no composition-dependent fifth force from the common radial mode. A controlled threshold defect produces

$$
\boxed{
 d\ln\frac{\Lambda_3}{\chi}
 =\frac{2}{27}\,\varepsilon_\Psi\,d\theta+\text{controlled corrections},
}
$$

so clock drift and equivalence-principle violation become two views of the same failure of universal spectral scaling. The coefficient $2/27$ is ordinary QCD threshold physics; its use as a transmission coefficient for chronometric shear is the project-specific synthesis [@Chetyrkin1997; @DamourDonoghue2010].

## What survived, what failed, and what remains open

| Layer | Current status | Meaning |
|---|---:|---|
| Photon rest-frame language | **FAIL** | A null-adapted coordinate system exists, but not a timelike observer frame. |
| Crossed-null clock/ruler algebra | **PASS** | Exact kinematics; useful organising language, not a novelty claim. |
| Exact-null constrained field theory | **FAIL** | Its transverse quadratic principal symbol is rank deficient in $3+1$ dimensions. |
| Soft-null two-phase EFT | **PASS** | Positive Hamiltonian, real subluminal modes for $0<\epsilon<1$. |
| Universal spectral factorisation theorem | **PASS** | Exact necessary-and-sufficient criterion for one clock metric. |
| Conventional scale-generating matter model | **PASS AS EFT** | Two-derivative matter is healthy; gravity remains an EFT. |
| Turok 36-field microscopic origin | **OPEN** | Physical composite positivity and unitarity remain disputed. |
| QCD lock and threshold recursion | **PASS AS WILSONIAN EFT** | Exact functional recursion; coefficients calculable order by order. |
| Protected long-range ratio mode | **PASS CONDITIONALLY** | Requires exact $Z_6$, shift-spurion counting, and UV quality. |
| Earth/Sun screening | **PASS** | Finite bodies do not convert or thin-shell-screen the benchmark field. |
| Cosmological branch selection | **PASS CONDITIONALLY** | Strong low-$f_a$ attractor benchmark; domain and inflation conditions remain. |
| State-selected reheating | **PASS AS EFT** | Action symmetric, state asymmetric; hard sector spurions avoided. |
| Original scalar preheating portal | **FAIL** | Tachyonic/resonant production makes the kinematic argument unsafe. |
| Fermionic cascade repair | **PASS AT RESOLVED ORDER** | Pauli limited and selector gated; full nonlinear gauge evolution remains. |
| RG-improved matching | **PASS AT RESOLVED ORDER** | Fixed-order scale excursion cancels after operator running. |
| Direct QCD AMY transport | **PASS** | QCD redistribution is far faster than reheaton decay. |
| Complete electroweak/Yukawa LPM | **OPEN** | Present decisive kinetic calculation. |
| Full non-Abelian $3+1$D 2PI/KB | **OPEN** | Separate HPC programme. |
| Emergent Einstein gravity | **OPEN** | Not derived. |
| Absolute novelty | **UNESTABLISHED** | Only a restricted candidate conjunction is defensible. |

![The research did not proceed as a straight triumphal march. Each version either killed a weak formulation, repaired it, or localised the next uncertainty.](figures/research_version_timeline.png){#fig:timeline width=100%}

## Results taxonomy

Throughout this manuscript, statements are labelled by one of five categories.

- **Established:** standard mathematics or physics already present in the literature.
- **Derived:** an analytic result obtained inside the displayed model, with assumptions stated.
- **Numerically verified:** a result checked by the supplied code within its declared discretisation or benchmark.
- **Conditional:** dependent on a UV completion, approximation, or parameter regime not yet independently established.
- **Open or failed:** either not calculated or explicitly ruled out by the audit.

This taxonomy is not cosmetic. The project repeatedly improved by abandoning formulations that were attractive but wrong. The exact-null action, the direct composite gravitational metric, the Planck-scale cosmological benchmark, the naive reheaton branching ratio, and the bosonic preheating portal are all retained in the manuscript as failures because removing them would falsify the research history.


## Bibliographic audit and two corrected source-role mismatches

The consolidated source ledger preserves the literature cited throughout the working notes, but its metadata has been checked against the corresponding records where possible. This exposed two late-stage identifier-role mismatches that must not be silently laundered into the final argument:

1. arXiv:2605.22822 is *Bottom-up open EFT for non-Abelian gauge theory with dynamical color environment*, not a paper deriving the scalar-Yukawa $H\leftrightarrow qD$ LPM normalisation. It is relevant to the proposed gauge-covariant open-EFT direction, but it does not support the direct scalar conversion rate.
2. arXiv:2211.15454 is *AMY Lorentz invariant parton cascade---the thermal equilibrium case*. It supports AMY cascade implementation and equilibrium validation, but not the narrower description “direct numerical solution of the AMY transverse integral equations.”

Accordingly, neither identifier is used here as evidentiary support for the v1.4 $H\leftrightarrow qD$ rate. That rate is retained as a project-derived numerical result whose supplied consolidated verification script checks the reported benchmark algebra, while the **complete electroweak/Yukawa LPM derivation remains open**. The source ledger records both the corrected metadata and the original project role so that the provenance remains inspectable.

# Part I - Null frames, photons, and relational time

## 1. Why a photon has no ordinary perspective

For light in flat spacetime,

$$
c^2\Delta t^2-\Delta x^2=0,
$$

and therefore the proper-time interval along the ray is

$$
\Delta\tau=0.
$$

This statement is invariant. It does not mean that the emission and absorption events are one spacetime event, and it does not define an experience of instantaneous traversal. A Lorentz transformation to a frame with $v=c$ does not exist. If an observer chases the ray at $v<c$, then for a coordinate interval $T$ in the laboratory frame,

$$
\Delta t'
=\gamma T(1-\beta)
=T\sqrt{\frac{1-\beta}{1+\beta}},
$$

which tends to zero as $\beta\rightarrow1$. The limiting values exist; the limiting frame does not. At $\beta=1$ the boost is noninvertible.

A useful way to expose the degeneration is to introduce photon-adapted coordinates

$$
T=t,
\qquad
\xi=x-ct.
$$

The ray sits at $\xi=0$, but the metric becomes

$$
 ds^2=d\xi^2+2c\,dT\,d\xi+dy^2+dz^2,
$$

with $g_{TT}=0$. Curves of constant $(\xi,y,z)$ are null. They cannot carry functioning proper-time clocks. The coordinates are valid; the putative observer frame is not.

The deeper obstruction is geometric. A massive observer has timelike four-velocity $U^\mu$ with $U^2=-1$, and the subspace orthogonal to $U$ is a spacelike rest space. A null tangent $k^\mu$ satisfies $k^2=0$ and belongs to its own orthogonal complement. The quotient

$$
Q_k=k^\perp/\langle k\rangle
$$

is a two-dimensional screen space, not an observer's three-dimensional rest space. Null tetrads and Carrollian geometry are the appropriate structures [@Gourgoulhon2006].

This gives the first sober ontology:

> A single photon is better represented as a null connection between interactions than as a small enduring object carrying an internal clock.

## 2. Compactifying observer space

Massive unit four-velocities form a hyperboloid. Write a boost in direction $\hat{\mathbf n}$ as

$$
U_\eta=(\cosh\eta,\sinh\eta\,\hat{\mathbf n}).
$$

The vector diverges as $\eta\rightarrow\infty$, but the projectively rescaled limit exists:

$$
\lim_{\eta\to\infty}2e^{-\eta}U_\eta
=(1,\hat{\mathbf n})
\equiv k,
\qquad k^2=0.
$$

The ideal photon frame is therefore a projective null ray $[k]$, not a unit four-velocity. Massive observers occupy the interior of hyperbolic velocity space; null directions form its ideal boundary. This is a geometric completion, not an algebraic invention analogous to adjoining $i$ to the reals.

An ideal null frame can be represented as

$$
\mathcal F_\gamma=(\gamma,[k],Q_k,\mathcal A_\gamma),
$$

where $\gamma$ is a null geodesic, $Q_k$ is its screen space, and $\mathcal A_\gamma$ is its affine structure with

$$
\lambda\sim a\lambda+b.
$$

It retains causal order, transverse geometry, polarisation, and affine ratios. It does not contain proper time, longitudinal metric distance, an absolute energy scale, or ordinary simultaneity.

## 3. Two null directions and the timelike interior

Let $k^a$ and $\ell^a$ be future-directed, nonparallel null covectors with

$$
k^2=\ell^2=0,
\qquad
k\cdot\ell=-2C<0.
$$

Define

$$
u^a=\frac{k^a+\ell^a}{2\sqrt C},
\qquad
e^a=\frac{k^a-\ell^a}{2\sqrt C}.
$$

Then

$$
u^2=-1,
\qquad
e^2=+1,
\qquad
u\cdot e=0.
$$

This is standard null-basis algebra. Its interpretive value is that reciprocal rescaling

$$
k\rightarrow e^\eta k,
\qquad
\ell\rightarrow e^{-\eta}\ell
$$

acts as

$$
\begin{aligned}
 u&\rightarrow\cosh\eta\,u+\sinh\eta\,e,\\
 e&\rightarrow\sinh\eta\,u+\cosh\eta\,e,
\end{aligned}
$$

so rapidity is the relative logarithmic weighting of two null directions.

Independent rescalings $k\rightarrow ak$, $\ell\rightarrow b\ell$ separate into

$$
\alpha=\frac12\ln(ab),
\qquad
\eta=\frac12\ln\frac ab.
$$

The ratio controls boost; the product controls common scale. Two unscaled null rays do not select a unique observer. Physical momenta do, because their energies fix the weighting. For two nonparallel null momenta $p$ and $q$,

$$
P^a=p^a+q^a,
\qquad
M^2=-P^2=-2p\cdot q>0,
$$

and

$$
u^a=\frac{P^a}{M}
$$

is their centre-of-momentum time direction. An ensemble of nonparallel null momenta generally lies inside the convex future cone and admits a timelike Landau energy frame. A single plane wave does not.

The useful slogan is therefore precise but limited:

$$
\boxed{
\text{timelike structure occupies the convex interior generated by null relations.}
}
$$

It does not yet fix a unit of time.

## 4. Why a single light phase cannot be its own clock

For a plane wave with phase $\phi(x)=k_\mu x^\mu$ and a ray

$$
x^\mu(\lambda)=x_0^\mu+\lambda k^\mu,
$$

one has

$$
\frac{d\phi}{d\lambda}=k_\mu k^\mu=0.
$$

The phase is constant along its own generator. Oscillation appears to a timelike detector, not as an internal pendulum attached to the ray. An autonomous clock requires comparison: two nonparallel modes, a cavity, a bound state, emission and absorption events, or some other interaction that supplies a second phase and a scale.

This observation motivates the crossed-phase construction.

# Part II - Crossed-null chronometry

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

## 7. Failure of the exact-null action

The first complete constrained action was

$$
S_0=\int d^4x\sqrt{-g}\left[
\frac{M_{\mathrm{P}}^2}{2}R
+A_+Y_++A_-Y_-
-\frac\kappa2(C-\sigma^2)^2
-\frac12(\nabla\sigma)^2
-V(\sigma)
\right],
$$

where

$$
Y_\pm=(\nabla\phi_\pm)^2,
\qquad
C=-\frac12\nabla\phi_+\cdot\nabla\phi_-.
$$

Around

$$
\bar\phi_+=m(t-x),
\qquad
\bar\phi_-=m(t+x),
$$

the linearised constraints are

$$
(\partial_t+\partial_x)\pi_+=0,
\qquad
(\partial_t-\partial_x)\pi_-=0.
$$

Define

$$
s=\frac{\pi_++\pi_-}{\sqrt2},
\qquad
r=\frac{\pi_+-\pi_-}{\sqrt2}.
$$

The lock fluctuation is

$$
\delta C=\frac{m}{\sqrt2}(\dot s-\partial_x r).
$$

Neither the linear constraints nor the quadratic lock contains $\partial_y$ or $\partial_z$. Transverse gradients first enter nonlinearly through terms such as $(\nabla\pi_\pm)^2$. The quadratic principal symbol is therefore rank deficient for generic transverse perturbations. Nonlinear terms control directions with no quadratic restoring operator.

$$
\boxed{
\text{Verdict: the exact-null constrained action is not a controlled ordinary }3+1\text{D EFT.}
}
$$

The positive homogeneous Hessian did not detect this because it tested only algebraic order-parameter fluctuations.

## 8. Healthy soft-null repair

The minimal repair makes the phases ordinary propagating compact fields and treats crossed nullity as a background state:

$$
\boxed{
\mathcal L_{\mathrm{EFT}}
=-\frac F2(Y_++Y_-)
+\frac\kappa2(C-m^2)^2.
}
$$

Define

$$
a=\frac{\kappa m^2}{2},
\qquad
\epsilon=\frac aF.
$$

The quadratic Lagrangian in $s,r$ is

$$
\begin{aligned}
\mathcal L^{(2)}={}&
\frac12(F+a)\dot s^2
+\frac12F\dot r^2
-a\dot s\,\partial_xr\\
&-\frac F2[(\nabla s)^2+(\nabla r)^2]
+\frac a2(\partial_xr)^2.
\end{aligned}
$$

The Hamiltonian is positive when

$$
\boxed{F>0,\qquad0<a<F,}
$$

or $0<\epsilon<1$. The principal polynomial factorises:

$$
F(\omega^2-k^2)
\left[(F+a)\omega^2-Fk^2+ak_x^2\right]=0.
$$

The modes are

$$
\omega_1^2=k^2,
$$

$$
\omega_2^2=\frac{Fk^2-ak_x^2}{F+a}.
$$

Writing $k_x=k\cos\theta$,

$$
\boxed{
c_2^2(\theta)=\frac{1-\epsilon\cos^2\theta}{1+\epsilon}.
}
$$

For $0<\epsilon<1$, the second mode is real, positive, and subluminal for every direction. The model belongs to the established two-superfluid/entrainment class rather than defining a new species of matter [@Superfluid2015].

### Local mediator completion

Introduce a healthy massive scalar $H$:

$$
\mathcal L_{\mathrm{med}}
=-\frac F2(Y_++Y_-)
-\frac12(\nabla H)^2
-\frac12M^2H^2
+g_HH(C-m^2).
$$

Integrating it out below $M$ gives

$$
\Delta\mathcal L
=\frac{g_H^2}{2}(C-m^2)\frac1{M^2-\Box}(C-m^2),
$$

and therefore

$$
\boxed{\kappa=\frac{g_H^2}{M^2}>0.}
$$

The sign is compatible with exchange of a positive-residue massive state and with standard positivity reasoning [@Adams2006].

### Model-specific tree-level sum rules

Parallel and perpendicular speeds satisfy

$$
c_\parallel^2=\frac{1-\epsilon}{1+\epsilon},
\qquad
c_\perp^2=\frac1{1+\epsilon},
$$

hence

$$
\boxed{c_\parallel^2=2c_\perp^2-1.}
$$

For the minimal one-mediator completion, the $k^4$ dispersion coefficients also obey

$$
\boxed{\alpha_\parallel=4\alpha_\perp.}
$$

These are not universal laws of two-fluid physics. They are consistency relations of the minimal model and will be perturbed by additional operators, resonances, and loops.

## 9. Gravity coupling and circularity

The direct substitution

$$
g^{\mathrm{physical}}_{\mu\nu}=Cg_{\mu\nu}
$$

is singular and mimetic. It does not evade the noninvertibility or extra-mode problem. A regular alternative introduces a Weyl compensator $\chi$:

$$
g_{\mu\nu}\rightarrow\Omega^2g_{\mu\nu},
\qquad
\chi\rightarrow\Omega^{-1}\chi,
$$

$$
\widehat g_{\mu\nu}
=\frac{\chi^2}{6M_{\mathrm{P}}^2}g_{\mu\nu}.
$$

A representative action is

$$
\begin{aligned}
S_W=\int\sqrt{-g}\Big[&
\frac{\chi^2}{12}R
+\frac12(\nabla\chi)^2
-\frac{f^2\chi^2}{2}(Y_++Y_-)\\
&+\frac\kappa2(C-\zeta\chi^2)^2
\Big].
\end{aligned}
$$

On the locking surface, the phase state calibrates the same invariant metric used by gravity. This is a regular EFT representation of chronometric calibration. It does not derive Einstein dynamics from null phases. The conformal manifold and gravitational action remain inputs.

# Part III - Universal spectral chronometry

## 10. Clock spectral fields

A local clock is represented not by a coordinate label but by a positive transition frequency $\omega_A(x)$. The invariant quantity is its phase accumulation

$$
d\Phi_A=\omega_A ds_g.
$$

Each individual clock defines a representative

$$
g^{(A)}_{\mu\nu}
=\left(\frac{\omega_A}{\omega_{A*}}\right)^2g_{\mu\nu},
$$

for which its intrinsic rate is constant. The nontrivial question is whether every clock defines the same representative.

## 11. Universal clock factorisation theorem

**Theorem.** Let $U\subset\mathcal M$ be connected and let $\{\omega_A\}$ be positive clock spectral fields. The following are equivalent:

1. There exists $\widehat g\in[g]$ and positive constants $\bar\omega_A$ such that $\Phi_A[\gamma]=\bar\omega_A\int_\gamma ds_{\widehat g}$ for every timelike curve $\gamma$ in $U$.
2. Every pairwise ratio is constant: $d\ln(\omega_A/\omega_B)=0$.
3. There is one positive Weyl-weight $-1$ scalar $\chi$ and constants $c_A$ such that $\omega_A=c_A\chi$.

**Proof.** Write $\widehat g=e^{2\sigma}g$. Equality of phase integrands gives $\omega_A=\bar\omega_Ae^\sigma$, proving constant ratios. If all ratios are constant, choose one reference clock and set $\chi$ proportional to its spectrum; the other spectra are constant multiples. Conversely, if $\omega_A=c_A\chi$, then $\widehat g=(\chi/\chi_*)^2g$ gives

$$
\Phi_A=c_A\chi_*\int ds_{\widehat g}.
$$

Uniqueness is up to one global multiplicative unit convention. $\square$

The theorem is elementary once stated. Its value is that it turns the phrase "all clocks measure the same proper time" into an exact integrability condition.

## 12. Chronometric shear and clock-space rank

Define

$$
\boxed{
\mathcal S_{AB}=d\ln\frac{\omega_A}{\omega_B}.
}
$$

This is invariant under Weyl rescaling. A useful clock-space decomposition begins with

$$
\ell_A=\ln\omega_A,
$$

where conformal gauge shifts all components in the common direction $(1,\ldots,1)$. Physical clock disagreement lives in the quotient of log-spectrum space by that common direction.

With positive weights $w_A$ satisfying $\sum_Aw_A=1$, define

$$
B^A_\mu=-\partial_\mu\ln\omega_A,
\qquad
W_\mu=\sum_Aw_AB^A_\mu,
$$

$$
\Sigma^A_\mu=B^A_\mu-W_\mu.
$$

Then $\Sigma^A$ and $\mathcal S_{AB}$ are gauge invariant, and

$$
\mathfrak C_{\mu\nu}=\sum_Aw_A\Sigma^A_\mu\Sigma^A_\nu
$$

is positive semidefinite. It vanishes exactly when one chronometric metric exists.

Suppose spectra depend on $r$ nonuniversal dimensionless fields $q^I$:

$$
\delta\ln\omega_A
=\delta\ln\chi+K_{AI}\delta q^I.
$$

Clock ratios obey

$$
\delta\ln\frac{\omega_A}{\omega_B}
=(K_{AI}-K_{BI})\delta q^I,
$$

so

$$
\boxed{
\operatorname{rank}\left[\delta\ln(\omega_A/\omega_B)\right]\le r.
}
$$

One nonuniversal scalar predicts a rank-one network across arbitrarily many clocks. Exact universal chronometry is rank zero.

## 13. The role of electromagnetism

Source-free Maxwell theory in four dimensions is conformally invariant. It transports phase, null structure, polarisation, and causal information, but it does not select an absolute spectral scale. A free wave's frequency is state data.

Matter interactions create bound-state gaps. A hydrogenic scale is schematically

$$
E_{\mathrm{Ry}}\sim m_e\alpha_{\mathrm{em}}^2,
\qquad
m_e=\frac{y_eh}{\sqrt2}.
$$

If $E_A=c_A\chi$, then

$$
d\Phi_A=\frac{E_A}{\hbar}ds_g
=c_A\chi_*ds_{\widehat g}.
$$

The division of labour is therefore:

$$
\boxed{
\begin{aligned}
\chi&:\text{ universal normalisation},\\
\text{Higgs and QCD}&:\text{ transmission into material spectra},\\
\text{electromagnetism}&:\text{ phase organisation, transport, and readout}.
\end{aligned}}
$$

The correct statement is not "the Higgs and photons create time." It is that a deeper scale field calibrates duration, material sectors relay the scale, and electromagnetic phase makes the count operational.

## 14. Why the Standard Model Higgs is insufficient by itself

A general clock frequency has the structure

$$
\omega_A
=h\,F_A\left(
\alpha_{\mathrm{em}},g_s,y_f,
\frac{\Lambda_{\mathrm{QCD}}}h,
\frac{M_{\mathrm{P}}}h,\ldots
\right).
$$

The ordinary Higgs sets elementary electroweak masses, but it does not impose

$$
d\ln\frac{\Lambda_{\mathrm{QCD}}}h=0,
\qquad
d\ln\frac{M_{\mathrm{P}}}h=0.
$$

Nuclear clocks depend on confinement, quark masses, nuclear magnetic moments, and many-body structure. The Higgs is a relay, not automatically a universal source.

Higgs-only induced gravity would require

$$
M_{\mathrm{P}}^2=\xi_hv^2,
$$

so

$$
\xi_h\sim10^{32},
$$

far beyond the minimal phenomenologically plausible range [@Atkins2012]. Using the sole radial Higgs mode as a local Weyl compensator also removes the physical scalar remaining after the electroweak Goldstones are eaten. A second radial direction is structurally required.

## 15. Higgs-dilaton and deeper-scale completion

Introduce a positive scalar $\chi$ and impose

$$
\boxed{
h=\alpha\chi,
\qquad
\Lambda_{\mathrm{QCD}}=c_Q\chi,
\qquad
M_{\mathrm{P}}=c_P\chi.
}
$$

If all dimensionless couplings are fixed, every physical gap is

$$
\omega_A=c_A\chi.
$$

Write

$$
h=\rho\sin\theta,
\qquad
\chi=\rho\cos\theta.
$$

The radial coordinate $\rho$ is the common scale; the angular coordinate $\theta$ measures Higgs/dilaton alignment. A pure radial fluctuation rescales every clock together and is invisible to local ratios. An angular fluctuation produces

$$
\delta\ln\frac{\omega_A}{\omega_B}
=(K_A-K_B)\delta\theta.
$$

A healthy globally scale-invariant representative has

$$
F(h,\chi)=\xi_hh^2+\xi_\chi\chi^2,
$$

$$
V(h,\chi)=\frac\lambda4(h^2-\alpha^2\chi^2)^2+\beta\chi^4.
$$

In the Einstein frame, the scalar field-space metric

$$
G_{ij}=\frac{M_{\mathrm{P}}^2}{F}\delta_{ij}
+\frac{3M_{\mathrm{P}}^2}{2F^2}F_{,i}F_{,j}
$$

is positive for positive Jordan kinetic signs and $F>0$. In the exact global scale limit, one radial dilaton direction can remain flat; local Weyl symmetry can gauge it; quantum breaking can lift it. These are different physical theories and should not be conflated [@Shaposhnikov2009; @Foot2007].

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

# Part IV - QCD locking and the first nonzero prediction

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

# Part V - Cyclic protection and environmental response

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

# Part VI - Cosmological branch selection

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

# Part VII - Exact symmetry with an asymmetric cosmological state

## 33. Why hard asymmetric reheating is dangerous

The cyclic cancellation of lower vacuum harmonics relies on exact microscopic symmetry. A permanent sector-specific reheating coupling is a hard $Z_6$-breaking spurion and generically feeds lower harmonics back into the vacuum potential. The correct architecture is therefore

$$
\boxed{
\text{exact }Z_6\text{ action}
+\text{temporarily asymmetric state}.
}
$$

This distinction is strongly supported by later cyclic finite-density models [@Delaunay2026].

## 34. Orbit-symmetric reheaton and transient selector

Introduce two complete reheaton orbits $X_k,Y_k$ with oriented cyclic mixing. Light eigenstates have the schematic form

$$
R_k=\cos\theta\,X_k+\sin\theta\,Y_{k-1}.
$$

A selected population of $R_0$ decays into sectors 0 and 5. A complete selector orbit $Q_k$ has one-hot inflationary branches. On the $Q_0$ branch, all reheaton copies except $R_0$ are made kinematically inaccessible by an exactly $Z_6$-invariant mass pattern.

The key chronology is

$$
\Gamma_{\phi\rightarrow R_0R_0}
\gg\Gamma_Q\gg\Gamma_R.
$$

The inflaton first produces the labelled state. The selector returns to the symmetric origin before the reheaton decays. The asymmetry survives in occupation numbers, not in late-time masses or couplings.

At the first homogeneous level, a branching ratio $\Gamma_5/\Gamma_0=1/256$ gives $T_5/T_0=1/4$. The nonlinear cascade later corrects the exact mixing required to achieve that final temperature ratio.

## 35. Perturbations and isocurvature

For fixed branching fractions,

$$
\rho_i=B_i\rho_R,
$$

and radiation curvature perturbations satisfy

$$
\zeta_i=\zeta_R+\frac14\delta\ln B_i.
$$

If the branching fractions are fixed constants,

$$
\delta B_0=\delta B_5=0,
$$

so

$$
S_{50}=3(\zeta_5-\zeta_0)=0.
$$

The extra radiation is adiabatic at linear order. This would fail if the mixing angle were a light modulus, because its fluctuation would be amplified by the small adjacent branching fraction. The benchmark keeps the mixing and selector sectors heavy during inflation.

The initial chronometric phase fluctuation

$$
\delta x_{\mathrm{reh}}=\frac{H_*}{2\pi f_a}
$$

is strongly damped by threshold, QCD, and baryon focusing. The staged calculation found a transfer magnitude of about $10^{-6}$ by recombination and a residual QCD-lock fluctuation near $10^{-23}$. This remains a reduced perturbation calculation, not a full Einstein-Boltzmann likelihood.

# Part VIII - Closed-time-path radiative audit

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

# Part IX - Mixed higher loops, preheating repair, and Wilson-line quality

## 40. First mixed selector-threshold topology

Using only the displayed interactions

$$
Q^\dagger QR^2,
\qquad
RH^\dagger H,
\qquad
H\bar qD,
\qquad
a\bar DD,
$$

the first connected mixed graph has

$$
I=8,
\qquad
V=6,
\qquad
L=I-V+1=3.
$$

It is one-particle irreducible but two-particle reducible. In the self-consistent 2PI description, it is generated by coupled lower-loop kernels rather than one primitive 2PI skeleton. The transient operator has

$$
\Delta V_{Qa}^{(3)}
=\epsilon C_3
\operatorname{Re}[e^{ia/f_a}\mathcal Q_1]
+O(\epsilon^2).
$$

A first NDA estimate made it negligible relative to the intended thermal potential. The subsequent exact factorised matching confirmed that conclusion.

## 41. Two-time surrogate and what it did not prove

The project evolved complete unequal-time propagators for an exact quadratic non-Markovian surrogate with 20 coordinates, 10 momentum modes, 1,801 time steps, and 301 stored two-time slices. It preserved the symplectic structure to $7.11\times10^{-15}$, reproduced $T_5/T_0=1/4$, and suppressed unselected leakage to approximately $1.14\times10^{-7}$.

This was a genuine two-time consistency test. It was not a nonlinear, non-Abelian $3+1$ dimensional plasma simulation. The distinction remains explicit [@Tranberg2024; @Lindner2007; @Bhattacharya2022].

## 42. Failure of the direct bosonic inflaton portal

The original trilinear

$$
\mathcal L_{\phi R}
=-\frac{g_{\phi R}}2\phi R^2
$$

requires a coupling large enough that post-inflationary oscillations make selected and nominally heavy reheaton modes tachyonic. The illustrative resonance parameter was $q_{\mathrm{end}}\sim6\times10^3$. Late-time kinematic closure therefore does not prevent early tachyonic or resonant production. This portal fails generically [@Dufaux2006].

## 43. Selector-gated fermionic cascade

Replace it with a complete fermionic parent orbit $N_k$:

$$
\mathcal L_N
=-y_\phi\phi\sum_k\bar N_kN_k
-\sum_km_{N_k}(Q)\bar N_kN_k
-y_R\sum_kR_k\bar N_k\nu_k+\mathrm{h.c.}
$$

On the one-hot branch, $N_0$ is accessible while the other copies are extremely heavy. The hidden Landau-Zener exponent in the benchmark is about $460.4$, giving a linear production suppression near $10^{-200}$. Selected fermions can be nonperturbatively produced, but Pauli blocking caps their occupancy rather than allowing unbounded bosonic amplification [@GreeneKofman1998].

The repair passes at the resolved linear and cascade levels. Full backreaction, rescattering, and gauge-plasma production remain part of the nonlinear programme.

## 44. Deconstructed Wilson-line completion

A candidate quality completion uses an 18-link deconstructed gauge theory. The collective Wilson line is

$$
\mathcal W
=\prod_{j=0}^{17}\frac{\Sigma_j}{f/\sqrt2}
=e^{ia/f_a}.
$$

A cyclic transformation shifts replica labels and rotates $\mathcal W$. A messenger chain generates

$$
\mathcal L_{\Psi,\mathrm{eff}}
=-\sum_k\left[
M-\kappa(\omega^k\mathcal W+\omega^{-k}\mathcal W^\dagger)
\right]\bar\Psi_k\Psi_k.
$$

The first local winding operator requires all 18 links, so low-dimension local operators cannot directly depend on the complete phase. This is the type of nonlocal/collective protection needed to turn the infrared $Z_6$ model into a credible gauge-quality completion [@Hor2026].

Perturbative discrete anomaly sums pass for the displayed vectorlike orbits, but the full global/cobordism anomaly problem is open [@Byakti2017].

# Part X - Exact matching, nonlinear cascade, and RG completion

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

# Part XI - Explicit thermalisation and direct AMY transport

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

# Part XII - Integrated interpretation, novelty, and falsification

## 52. What “time emerges” means here

The final hierarchy is

$$
\boxed{
\begin{aligned}
\text{causal/conformal structure}
&\longrightarrow\text{before/after and null directions},\\
\text{nonparallel fields or phase gradients}
&\longrightarrow\text{local timelike energy directions},\\
\text{generated universal scale }\chi
&\longrightarrow\text{metric normalisation},\\
\text{material spectral gaps}
&\longrightarrow\text{stable relative phases},\\
\text{phase counting}
&\longrightarrow\text{operational duration}.
\end{aligned}}
$$

The programme derives a chronometric calibration conditional on a conformal causal structure and physical quantum dynamics. It does not derive:

- events or causal order;
- the differentiable manifold;
- Einstein's field equations;
- a universal global present;
- the thermodynamic arrow;
- every quantum interaction;
- a UV-complete theory of gravity.

The strongest defensible sentence is:

> Causality may be primitive; proper duration can be the universally calibrated phase relation generated by interacting fields.

## 53. Non-circularity

If $\chi$ is a pure Weyl compensator, the construction can be interpreted as gauge-invariant bookkeeping. No local dimensionless experiment detects a universal rescaling of all masses. The result is conceptually clean but may not constitute new dynamics.

If $\chi$ is a physical condensate or dilaton, the theory becomes stronger only if it supplies at least one of:

1. a microscopic derivation of the scale;
2. gravitational or cosmological dynamics controlled by it;
3. controlled nonuniversal residuals;
4. a relation among clock, fifth-force, collider, or cosmological observables.

The QCD defect, the $Z_6$ protection, and the clock/EP consistency relation are the project’s attempt to meet this requirement.

## 54. Novelty boundary

The following are established and should not be claimed as novel:

- null-pair and null-tetrad algebra;
- reciprocal null scaling as Lorentz boost freedom;
- timelike total momentum from nonparallel massless momenta;
- causal order determining conformal structure under suitable conditions;
- clocks selecting a conformal representative;
- mimetic conformal maps;
- two-superfluid entrainment;
- dimensional transmutation;
- Higgs-dilaton and induced-scale models;
- QCD threshold decoupling and the $2/27$ coefficient;
- cyclic $Z_N$ suppression of an ultralight scalar potential;
- asymmetric reheating and finite-density potentials;
- Schwinger-Keldysh, 2PI/KB, AMY, LPM, and screened collision methods.

The candidate contribution is narrower:

$$
\boxed{
\begin{gathered}
\text{universal clock factorisation and chronometric shear}
+\text{three-sector scale locking}\\
+\text{QCD-transmitted }2/27\text{ defect}
+\text{protected }Z_6\text{ long-range mode}\\
+\text{state-selected exact-symmetry reheating}
+\text{transient matching and microscopic transport}.
\end{gathered}}
$$

No exact indexed match for that full conjunction was located in the staged searches. That is a candidate paper claim, not an absolute priority claim. Publication requires backward and forward citation chaining, non-arXiv databases, and specialist review in mimetic gravity, relativistic superfluids, varying constants, axion quality, nonequilibrium QFT, and thermal field theory.

## 55. Falsification routes

The programme is falsifiable at several levels.

### Soft-null analogue or hidden-sector spectrum

The minimal phase EFT predicts

$$
c_\parallel^2=2c_\perp^2-1,
\qquad
\alpha_\parallel=4\alpha_\perp.
$$

Deviation indicates additional operators or falsifies the minimal mediator completion.

### Clock-network rank

One nonuniversal scalar predicts a rank-one matrix of differential clock-ratio responses. Rank two or higher falsifies the single-mode model, though not the general chronometric-shear formalism.

### Clock/EP consistency line

Under one long-range unscreened QCD-dominated scalar,

$$
\frac{\beta_{AB}}{\eta_{CD}}
=-\frac{\Delta K_{AB}}{\Delta Q_{\widehat m}^{\prime\,CD}}.
$$

Inconsistent clock and free-fall signals would rule out the benchmark assumptions.

### Cosmological sign and amplitude

The state-selected reheating construction predicts a selected sign of $d_g$, sparse adjacent-sector dark radiation, and negligible chronometric isocurvature in the strong attractor. A full perturbation calculation could falsify this architecture.

### Kinetic hierarchy

The model requires the visible and adjacent plasma to equilibrate much faster than reheaton decay. Direct AMY transport currently supports a hierarchy above $10^6$. A complete electroweak/Yukawa result would have to lower the portal rate by more than six orders of magnitude to overturn the cascade approximation.

## 56. Integrated acceptance matrix

![The present project contains genuine passes, useful conditional results, explicit failures, and several large open problems.](figures/integrated_status_counts.png){#fig:status width=82%}

The machine-readable integrated matrix is supplied as `data/integrated_acceptance_matrix.csv`. The manuscript’s central open items are:

1. complete electroweak/Yukawa LPM for $H\leftrightarrow qD$;
2. two-loop or higher RG-improved vacuum and tunnelling analysis of the full scalar sector;
3. complete reheating cascade with the repaired fermionic parent, rescattering, and gauge interactions;
4. full cosmological perturbations and likelihoods;
5. UV completion of the collective Wilson line and all discrete anomalies;
6. a positive invariant spectrum for any proposed Turok-36 completion;
7. a non-circular microscopic origin of gravity, if the ambition extends beyond duration calibration;
8. a publication-grade novelty audit.

# Conclusion

The project began with a seductive but invalid phrase: "the photon's perspective." Relativity does not permit such an observer. What survives is more interesting. A null direction supplies causal propagation without an internal clock. Two nonparallel null relations can supply a timelike direction, but not an absolute duration scale. Interactions can generate a common spectral scale. A family of clocks defines one proper-time metric exactly when every local spectrum shares that factor. The failure of this condition is a Weyl-invariant, experimentally meaningful chronometric shear.

The first exact-null dynamics failed. The theory became healthier by softening nullity and separating kinematics from scale generation. The Higgs alone proved insufficient, so a deeper scale field was introduced. QCD thresholds made the first nonuniversal defect calculable. A $Z_6$ orbit protected an ultralight mode. Finite-size analysis showed that ordinary bodies do not screen it. Cosmology selected a branch only after the parameter space moved away from the original Planck-scale benchmark. State-selected reheating preserved vacuum symmetry, while closed-time-path analysis showed why transient asymmetry need not become a permanent spurion. A bosonic preheating portal failed and was replaced by a fermionic cascade. Exact factorised matching, RG completion, explicit collision kernels, and direct AMY transport progressively reduced the remaining uncertainty.

The result is not a completed theory of time, gravity, or quantum cosmology. It is a coherent and increasingly constrained theory of **duration calibration**:

$$
\boxed{
\begin{gathered}
\text{null incidence}
+\text{interaction-generated universal scale}\\
+\text{spectral factorisation}
+\text{phase comparison}\\
\Longrightarrow
\text{operational proper duration}.
\end{gathered}
}
$$

The next decisive calculation is sharply localised. It is the complete electroweak/Yukawa LPM problem for $H\leftrightarrow qD$. That calculation will determine the last meaningful kinetic normalisation before the project earns the computational bloodletting of a full non-Abelian $3+1$ dimensional two-time treatment.

\newpage

# Appendix A - Core notation

| Symbol | Meaning |
|---|---|
| $[g]$ | Lorentzian conformal class |
| $k_a,\ell_a$ | crossed null phase gradients or null covectors |
| $C=-\tfrac12k\cdot\ell$ | crossed-null invariant scale |
| $T,R$ | mean and difference phases |
| $h_{ab}=Cg_{ab}$ | singular crossed-phase/mimetic representative in exact-null formulation |
| $\chi$ | common Weyl-weight $-1$ spectral scale |
| $\widehat g_{\mu\nu}$ | operational chronometric metric |
| $\omega_A$ | local spectrum of clock transition $A$ |
| $\mathcal S_{AB}$ | chronometric shear $d\ln(\omega_A/\omega_B)$ |
| $\delta_n$ | QCD lock defect $d\ln(\Lambda_n/\chi)$ |
| $\epsilon_j$ | threshold defect $d\ln(\widehat m_j/\chi)$ |
| $a=f_a\theta$ | canonical ratio mode |
| $d_g$ | dimensionless scalar coupling to the low-energy QCD scale |
| $x=a/f_a$ | compact phase variable |
| $Q_k$ | transient selector orbit |
| $X_k,Y_k,R_k$ | reheaton orbit fields/eigenstates |
| $N_k$ | selector-gated fermionic parent orbit |
| $H,D,q,g$ | Higgs, vectorlike fermion, light quark, gluon kinetic species |

# Appendix B - Consolidated benchmark values

The machine-readable source is `data/benchmark_parameters.json`. Key values are reproduced here.

| Benchmark | Value |
|---|---:|
| Reduced Planck mass | $2.435\times10^{18}$ GeV |
| QCD threshold transmission | $2/27$ |
| $Z_6$ Planck benchmark range | $347.4$ AU |
| Environmental conversion threshold $q_{\mathrm{conv}}$ | $0.633135$ |
| Strong-attractor $f_a$ | $2.435\times10^{10}$ GeV |
| Strong-attractor $\epsilon$ | $2.70\times10^{-13}$ |
| Strong-attractor $M$ | $1.002\times10^6$ GeV |
| Strong-attractor $d_g$ | $10^{-6}$ |
| Adjacent-sector $\Delta N_{\mathrm{eff}}$ | $0.0289$ |
| Updated $g_*$ | $117.25$ |
| Updated reheaton width | $1.47850065\times10^{-2}$ GeV |
| Updated adjacent branch $B_5$ | $0.00529888708$ |
| RG-improved $\mathcal I_3$ | $6.57973508149$ |
| Transient/thermal potential ratio | $3.053\times10^{-12}$ |
| Direct-AMY kinetic rate | $3.1918\times10^4$ GeV |
| Direct-AMY hierarchy | $2.1588\times10^6$ |

# Appendix C - Version-by-version correction ledger

| Version | Retained result | Correction introduced |
|---|---|---|
| v0.1 | Exact crossed-phase algebra and product/ratio split | Homogeneous stability was not field-theory stability. |
| v0.2 | Soft-null EFT and mediator completion | Exact-null map is mimetic; constrained action strongly coupled transversely. |
| v0.3 | Universal factorisation theorem and chronometric shear | Ordinary Higgs is insufficient as sole common scale. |
| v0.4 | Conventional hidden scale generator | Turok-36 moved from assumption to optional candidate under hard tests. |
| v0.5 | All-orders threshold recursion and $2/27$ | Minimal long-range defect is radiatively unnatural. |
| v0.6 | $Z_6$ protection | Global scalar quality and finite-density effects become decisive. |
| v0.7 | No environmental screening | Cosmological homogeneous selection remains separate. |
| v0.8 | Low-$f_a$ strong attractor | Original Planck benchmark overcloses and does not select a vacuum. |
| v0.9 | State-selected exact-symmetry reheating | Naive branching and preheating still unresolved. |
| v1.0 | Vacuum/state CTP separation through two loops | Exact $Z_6$ alone is insufficient without shift spurion counting. |
| v1.1 | Three-loop transient topology and fermionic repair | Direct bosonic portal fails generically. |
| v1.2 | Exact factorised matching and nonlinear cascade | $\tan\theta=1/16$ fails; corrected branch required. |
| v1.3 | RG completion and explicit collision kernel | Fixed-order scale excursion and BGK closure removed. |
| v1.4 | Direct QCD AMY transport | Electroweak/Yukawa LPM, not QCD, is the remaining kinetic bottleneck. |

# Appendix D - Reproducibility and provenance

This consolidation is based on:

1. the current-conversation chat snapshot stored in the `sources` directory;
2. the staged manuscript, source, code, result, matrix, and figure records from v0.1-v1.4 located in the project File Library;
3. the equations, benchmarks, caveats, and correction history explicitly reported in those staged notes;
4. a source ledger that preserves the cited literature, corrected metadata, and source-role audit notes.

Historical sandbox links from earlier chats are not assumed to be durable local paths. The archive therefore contains a complete **consolidated** manuscript, bibliography, source ledger, verification suite, benchmark data, figures, and an inventory of the historical filenames. It does not falsely claim to contain byte-identical copies of every ephemeral historical ZIP or figure. See `data/historical_artifact_inventory.csv` and `SOURCE_PROVENANCE.md`.

The verification suite checks the main algebraic and numerical identities reproduced in this manuscript. It is not a substitute for peer review, independent code, lattice gauge theory, or the unresolved high-performance calculations.
