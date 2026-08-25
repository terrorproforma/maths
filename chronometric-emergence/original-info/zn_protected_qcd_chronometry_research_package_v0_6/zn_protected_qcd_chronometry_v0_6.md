# Cyclic Discrete-Goldstone Protection of QCD Chronometric Shear

**A \(Z_6\) replicated-sector construction that preserves the \(2/27\) QCD threshold while suppressing the ratio-mode mass**  
**Technical research note — v0.6**  
**Date:** 16 August 2026  
**Status:** Working theoretical construction; not peer reviewed.

## Executive result

The radiative-naturalness obstruction in v0.5 can be removed without sacrificing the calculable visible-QCD transmission coefficient.

Replace the unprotected real ratio mode by a compact field

\[
x\equiv \frac{a}{f_a}
\]

that nonlinearly realizes an exact cyclic symmetry \(Z_N\). Introduce \(N\) identical QCD-like sectors and one vectorlike colour triplet \(\Psi_k\) in each sector, with masses

\[
\boxed{
M_k(a)=M\left[1-\epsilon\cos\left(x+\frac{2\pi k}{N}\right)\right],
\qquad k=0,\ldots,N-1.
}
\]

The cyclic transformation is

\[
x\rightarrow x+\frac{2\pi}{N},
\qquad
k\rightarrow k+1.
\]

The full vacuum energy sums over the complete orbit. Root-of-unity identities cancel every field-dependent Coleman-Weinberg term below order \(\epsilon^N\). For \(N>4\),

\[
\boxed{
V_{\rm CW}(a)
=
\frac{N_cM^4\epsilon^N}{8\pi^2}
F_N
\cos\left(\frac{Na}{f_a}\right)
\left[1+O(\epsilon)\right],
}
\]

where

\[
\boxed{
F_N
=
\frac{24\,2^{1-N}}
{(N-1)(N-2)(N-3)(N-4)}.
}
\]

Therefore,

\[
\boxed{
m_a^2
=
\frac{N_cM^4N^2\epsilon^N}{8\pi^2f_a^2}F_N
\left[1+O(\epsilon)\right].}
\]

The coupling of \(a\) to **our** QCD sector is not orbit-summed. Only \(\Psi_0\) is charged under visible \(SU(3)_0\); its partners are charged under the hidden groups \(SU(3)_k\). Consequently the visible threshold remains

\[
\boxed{
\mathrm d\ln\frac{\Lambda_{3,0}}{\chi}
=
\left[\frac{2}{27}+O(\alpha_s)\right]
\mathrm d\ln\frac{M_0}{\chi}.
}
\]

Thus the scalar coupling is order \(\epsilon\), while its radiative mass is order \(\epsilon^{N/2}\):

\[
\boxed{
\text{visible QCD response}\sim\epsilon,
\qquad
m_a^2\sim\epsilon^N.
}
\]

For the minimal especially clean choice \(N=6\), select the symmetry-related vacuum

\[
\frac{a_0}{f_a}=\frac{\pi}{2}.
\]

Then

\[
\frac{\partial}{\partial(a/f_a)}
\ln\frac{M_0}{\chi}
=\epsilon,
\]

while

\[
\boxed{
 m_a^2
 =
 \frac{27}{320\pi^2}
 \frac{M^4}{f_a^2}\epsilon^6
 \left[1+O(\epsilon)\right]
}
\]

for \(N_c=3\). The visible gluonic response is

\[
\boxed{
 d_g
 \equiv
 M_{\rm P}\frac{\partial}{\partial a}
 \ln\frac{\Lambda_{3,0}}{\chi}
 =
 \frac{2}{27}\frac{M_{\rm P}}{f_a}\epsilon
 +O(\alpha_s\epsilon,\epsilon^2).
}
\]

The catastrophic one-threshold estimate

\[
m_{a,\rm naive}^2
\sim
\frac{N_c}{4\pi^2}
\frac{M^4}{f_a^2}\epsilon^2
\]

is replaced, in the \(Z_6\) model, by

\[
\boxed{
\frac{m_{a,Z_6}^2}{m_{a,\rm naive}^2}
=
\frac{9}{80}\epsilon^4
}
\]

under the stated normalization. This is a symmetry cancellation, not a tuning between unrelated counterterms.

---

## 1. Status matrix

| Requirement | Verdict | Result |
|---|---:|---|
| Preserve visible-QCD \(2/27\) threshold | **PASS** | Hidden partners live in separate colour sectors, so only one fundamental Dirac threshold enters visible QCD. |
| Cancel \(M_\Psi^4/f_a^2\) mass problem | **PASS parametrically** | All terms through \(O(\epsilon^{N-1})\) cancel; the first vacuum harmonic is \(O(\epsilon^N)\). |
| Conventional Lorentzian unitarity | **PASS** | Two-derivative scalar, gauge and vectorlike-fermion sectors; no higher-time-derivative elementary field. |
| Positive physical spectrum | **PASS perturbatively** | Canonical kinetic terms, anomaly-free vectorlike representations, positive radial curvature and positive angular curvature at a selected minimum. |
| All-loop protection | **PASS conditionally** | Follows from exact \(Z_N\), the restored continuous shift at \(\epsilon=0\), and absence of independent shift-breaking spurions. |
| Renormalizable protection sector | **PASS** | The displayed scalar, Yukawa and gauge interactions are dimension four. |
| UV quality against \(\Phi^N\) operators | **PARTIAL** | An elementary global-field version has a quality problem; a discrete-gauge or deconstructed Wilson-line completion is required. |
| Mirror-sector cosmology | **OPEN** | Reheating, dark radiation, hidden confinement and domain selection need a dedicated model. |
| Finite-density behavior | **OPEN but calculable** | Visible matter spontaneously selects one sector and gives an unsuppressed environmental potential; this is both the signal source and a possible screening mechanism. |
| Novelty | **NARROW** | The \(Z_N\) protection mechanism is established. The CP-even QCD-threshold implementation, preserved \(2/27\) transmission and chronometric/EP application appear to be the candidate new package. |

---

## 2. Why the single-threshold model failed

The v0.5 model used one vectorlike colour triplet with

\[
M_\Psi(a)=M\left[1+\varepsilon_\Psi\frac{a}{f_a}+\cdots\right].
\]

Its one-loop vacuum energy contains

\[
V_{\rm CW}
=-\frac{N_c}{16\pi^2}
M_\Psi(a)^4
\left[
\ln\frac{M_\Psi(a)^2}{\mu^2}-\frac32
\right].
\]

Taking two derivatives gives generically

\[
m_a^2
\sim
\frac{N_c}{4\pi^2}
\varepsilon_\Psi^2
\frac{M^4}{f_a^2}.
\]

The same derivative that produces the useful QCD coupling therefore produces a large scalar mass. With a TeV-scale or higher coloured threshold, an astronomical-range field demands absurdly small \(\varepsilon_\Psi\), and the observable signal vanishes with it.

The required structure must therefore separate:

\[
\text{first derivative of one visible threshold}
\]

from

\[
\text{second derivative of the complete vacuum energy}.
\]

A cyclic exchange symmetry does exactly this. The visible experiment samples one sector; the vacuum sums the complete symmetry orbit.

---

## 3. Microscopic \(3+1\)-dimensional construction

### 3.1 Gauge and matter content

Take

\[
\mathcal G
=
\left[\prod_{k=0}^{N-1}SU(3)_k\right]\rtimes Z_N.
\]

For exact radiative protection, every sector must contain an identical renormalization environment for the protected heavy fermion. The conservative completion replicates the complete coloured sector, and the simplest known cosmological implementations replicate the full Standard Model:

\[
\mathcal L_{\rm sectors}
=
\sum_{k=0}^{N-1}
\left[
\mathcal L_{\rm SM}^{(k)}
+\bar\Psi_k i\!\not\!D_k\Psi_k
\right].
\]

Each \(\Psi_k\) is a vectorlike Dirac fundamental of \(SU(3)_k\). It can be assigned electroweak quantum numbers permitting decay, provided those assignments and decay operators are replicated identically.

Introduce:

- the universal scale field \(\chi\);
- a complex scalar \(\Phi\), neutral under the colour sectors;
- a radial locking potential

\[
V_{\rm rad}
=
\lambda_\Phi
\left(
|\Phi|^2-\frac{\zeta_a^2\chi^2}{2}
\right)^2,
\qquad
\lambda_\Phi>0.
\]

Write

\[
\Phi
=
\frac{f_a+\rho}{\sqrt2}
\exp\left(\frac{ia}{f_a}\right),
\qquad
f_a=\zeta_a\chi
\]

in the adiabatic locked background.

### 3.2 Exact cyclic symmetry

Let

\[
\omega=e^{2\pi i/N}.
\]

The symmetry acts as

\[
\boxed{
\Phi\rightarrow\omega\Phi,
\qquad
\Psi_k\rightarrow\Psi_{k+1},
\qquad
SU(3)_k\rightarrow SU(3)_{k+1}.
}
\]

The renormalizable Yukawa orbit is

\[
\boxed{
\mathcal L_Y
=-\sum_{k=0}^{N-1}
\left[
 y_\chi\chi
-y\left(\omega^k\Phi+\omega^{-k}\Phi^\dagger\right)
\right]
\bar\Psi_k\Psi_k.
}
\]

After radial locking,

\[
M=y_\chi\chi,
\qquad
\epsilon=\frac{\sqrt2yf_a}{M}
=\frac{\sqrt2y\zeta_a}{y_\chi},
\]

and

\[
\boxed{
M_k(a)
=M\left[
1-\epsilon\cos\left(\frac a{f_a}+\frac{2\pi k}{N}\right)
\right].
}
\]

All masses remain strictly positive for

\[
0<\epsilon<1.
\]

Because \(M\propto\chi\) and \(f_a\propto\chi\), \(\epsilon\) is dimensionless and independent of the common radial scale. The compact field \(a/f_a\) is therefore a genuine ratio mode.

### 3.3 Perturbative health

The scalar kinetic term gives

\[
|\partial\Phi|^2
=
\frac12(\partial\rho)^2
+\frac12\left(1+\frac{\rho}{f_a}\right)^2(\partial a)^2.
\]

Around \(\rho=0\), both kinetic eigenvalues are positive. The radial mass is

\[
m_\rho^2=2\lambda_\Phi f_a^2>0.
\]

The \(\Psi_k\) are vectorlike, so their colour representations introduce no chiral gauge anomaly. Each gauge sector is an ordinary local Yang-Mills theory. The construction therefore avoids the Lorentzian and spectral difficulties associated with elementary fourth-order fields.

---

## 4. All-orders cyclic-protection theorem

### Theorem

Assume:

1. the complete microscopic action, path-integral measure and regulator preserve the cyclic \(Z_N\);
2. the limit \(\epsilon\to0\) restores a continuous shift symmetry of \(a\);
3. the only local shift-breaking spurions are those appearing in the complete Yukawa orbit;
4. the effective action is analytic in those spurions near \(\epsilon=0\).

Then the vacuum effective potential has the form

\[
\boxed{
V_{\rm eff}(a)
=
V_0
+
\sum_{q=1}^{\infty}
\Lambda_q^4
\cos\left(
\frac{qNa}{f_a}+\delta_q
\right),
}
\]

with

\[
\boxed{
\Lambda_q^4=O\left(\epsilon^{qN}\right).
}
\]

In particular, the leading field-dependent term is \(O(\epsilon^N)\).

### Proof

The exact exchange symmetry implies

\[
V_{\rm eff}(x)=V_{\rm eff}\left(x+\frac{2\pi}{N}\right).
\]

Its Fourier series can therefore contain only harmonics \(e^{iqNx}\). In the \(\epsilon=0\) limit, the continuous shift symmetry makes every nonconstant Fourier coefficient vanish.

Each Yukawa mass insertion supplies one factor of \(\epsilon e^{ix}\) or \(\epsilon e^{-ix}\). A term proportional to \(e^{iqN x}\) requires at least \(qN\) net insertions. Hence its coefficient is at least order \(\epsilon^{qN}\). This argument is independent of loop order. Gauge and scalar corrections can alter coefficients but cannot create a forbidden harmonic or reduce the required spurion power.

### Consequence

The dangerous order-\(\epsilon^2\) mass is not balanced against an unrelated bosonic loop. It is absent because no symmetry-compatible invariant exists at that order.

---

## 5. Explicit one-loop Coleman-Weinberg potential

For \(N_c\) colours,

\[
V_{\rm CW}(a)
=-\frac{N_c}{16\pi^2}
\sum_{k=0}^{N-1}
M_k(a)^4
\left[
\ln\frac{M_k(a)^2}{\mu^2}-\frac32
\right].
\]

For \(m<N\), the orbit sums obey

\[
\sum_{k=0}^{N-1}
\cos^m\left(x+\frac{2\pi k}{N}\right)
=
\text{constant in }x.
\]

The first field-dependent identity is

\[
\sum_{k=0}^{N-1}
\cos^N\left(x+\frac{2\pi k}{N}\right)
=
\frac{N}{2^{N-1}}\cos(Nx)+\text{constant}.
\]

For \(N>4\), the divergent and renormalization-scale-dependent terms are field independent, and expansion of the finite part gives

\[
V_{\rm CW}(a)
=
\frac{N_cM^4\epsilon^N}{8\pi^2}
F_N\cos(Nx)
\left[1+O(\epsilon)\right].
\]

The literature expression

\[
F_N
=
2^{1-N}N
\sum_{\ell=0}^{4}
\binom4\ell\frac{(-1)^\ell}{N-\ell}
\]

simplifies exactly to

\[
\boxed{
F_N
=
\frac{24\,2^{1-N}}
{(N-1)(N-2)(N-3)(N-4)}.
}
\]

At a minimum,

\[
\boxed{
 m_a^2
 =
 \frac{N_cM^4N^2\epsilon^N}{8\pi^2f_a^2}F_N
 \left[1+O(\epsilon)\right]>0.
}
\]

The symmetry statement is all-order; this coefficient is the leading one-loop realization.

---

## 6. Why the visible \(2/27\) survives

The partners \(\Psi_{k\ne0}\) cancel the vacuum potential because the vacuum functional sums over all sectors. They do **not** enter the visible QCD beta function because they are not charged under \(SU(3)_0\).

For our sector, the exact threshold recursion from v0.5 remains

\[
\delta_{n-1}
=A_j\delta_n+(1-A_j)\epsilon_j,
\]

where

\[
\delta_n=\mathrm d\ln\frac{\Lambda_n}{\chi},
\qquad
\epsilon_j=\mathrm d\ln\frac{\widehat m_j}{\chi}.
\]

For the visible threshold chain

\[
7\xrightarrow{\Psi_0}6\xrightarrow{t}5\xrightarrow{b}4\xrightarrow{c}3,
\]

with the Standard Model heavy quarks exactly locked to \(\chi\),

\[
\mathrm d\ln\frac{\Lambda_{3,0}}{\chi}
=\mathcal D_{\Psi\to3}
\mathrm d\ln\frac{M_0}{\chi}.
\]

At one loop,

\[
\begin{aligned}
\mathcal D_{\Psi\to3}^{(1)}
&=
\left(1-\frac{19}{21}\right)
\frac{21}{23}\frac{23}{25}\frac{25}{27}
\\
&=\boxed{\frac{2}{27}}.
\end{aligned}
\]

At higher orders,

\[
\mathcal D_{\Psi\to3}
=\frac{2}{27}+O(\alpha_s(M)),
\]

with corrections calculable from standard decoupling functions.

For a general background \(x_0=a_0/f_a\), define

\[
\kappa_0
\equiv
\frac{\partial}{\partial x}
\ln\frac{M_0}{\chi}
\bigg|_{x_0}
=
\frac{\epsilon\sin x_0}{1-\epsilon\cos x_0}.
\]

Then

\[
\boxed{
\frac{\partial}{\partial a}
\ln\frac{\Lambda_{3,0}}{\chi}
=
\left[\frac{2}{27}+O(\alpha_s)\right]
\frac{\kappa_0}{f_a}.
}
\]

This is the key decoupling:

\[
\kappa_0=O(\epsilon),
\qquad
m_a^2=O(\epsilon^N).
\]

---

## 7. Minimal working benchmark: \(Z_6\)

For \(N=6\),

\[
F_6=\frac1{160}.
\]

The potential has six minima

\[
x_m=\frac{(2m-1)\pi}{6}.
\]

Choose the symmetry-related vacuum

\[
\boxed{x_0=\frac\pi2.}
\]

Then

\[
\cos x_0=0,
\qquad
\sin x_0=1,
\]

so

\[
M_0=M,
\qquad
\boxed{\kappa_0=\epsilon.}
\]

For \(N_c=3\),

\[
\boxed{
V_{\rm CW}^{(6)}
=
\frac{3M^4\epsilon^6}{1280\pi^2}
\cos\left(\frac{6a}{f_a}\right)
+O(\epsilon^7),
}
\]

and

\[
\boxed{
 m_a^2
 =
 \frac{27}{320\pi^2}
 \frac{M^4}{f_a^2}\epsilon^6
 +O(\epsilon^7).
}
\]

The QCD coupling is

\[
\boxed{
 d_g
 =
 \frac{2}{27}\frac{M_{\rm P}}{f_a}\epsilon
 +O(\alpha_s\epsilon,\epsilon^2).
}
\]

Eliminating \(\epsilon\) gives the model's mass-coupling protection law:

\[
\boxed{
\frac{m_a^2f_a^2}{M^4}
=
\frac{27}{320\pi^2}
\left(
\frac{27}{2}\frac{f_a}{M_{\rm P}}d_g
\right)^6
+\cdots.
}
\]

This is the central quantitative gain: the coupling enters the radiative mass at sixth order rather than second order.

### Numerical illustration

Take

\[
M=10\ \mathrm{TeV},
\qquad
f_a=M_{\rm P}=2.435\times10^{18}\ \mathrm{GeV}.
\]

| \(N\) | \(\epsilon\) | \(d_g\) at maximal slope | \(m_a\) | Compton range |
|---:|---:|---:|---:|---:|
| 5 | \(10^{-6}\) | \(7.41\times10^{-8}\) | \(1.00\times10^{-17}\) eV | \(0.132\) AU |
| 6 | \(10^{-6}\) | \(7.41\times10^{-8}\) | \(3.80\times10^{-21}\) eV | \(347\) AU |
| 8 | \(10^{-6}\) | \(7.41\times10^{-8}\) | \(9.57\times10^{-28}\) eV | \(1.38\times10^9\) AU |
| 6 | \(10^{-3}\) | \(7.41\times10^{-5}\) | \(3.80\times10^{-12}\) eV | \(3.47\times10^{-7}\) AU |

For the \(N=6,\epsilon=10^{-6}\) point, the ordinary unprotected estimate is

\[
m_{a,\rm naive}\simeq1.13\times10^{-8}\ \mathrm{eV},
\]

whereas the protected result is

\[
m_{a,Z_6}\simeq3.80\times10^{-21}\ \mathrm{eV}.
\]

The squared-mass suppression is

\[
\frac{m_{a,Z_6}^2}{m_{a,\rm naive}^2}
=1.125\times10^{-25}.
\]

---

## 8. Chronometric and equivalence-principle predictions

The protection changes the naturalness relation; it does not erase the low-energy prediction derived in v0.5.

For clock transitions \(A\) and \(B\),

\[
\mathcal S_{AB}
\equiv
\mathrm d\ln\frac{\nu_A}{\nu_B}.
\]

In the pure-QCD benchmark,

\[
\boxed{
\mathcal S_{AB}
=
(\Delta K_\mu-\Delta K_q)
\frac{2}{27}\kappa_0\,\mathrm dx
+\cdots.
}
\]

At the \(Z_6\) benchmark vacuum, \(\kappa_0=\epsilon\), so

\[
\boxed{
\mathcal S_{AB}
=
(\Delta K_\mu-\Delta K_q)
\frac{2\epsilon}{27}\frac{\mathrm da}{f_a}
+\cdots.
}
\]

The rank-one relation remains

\[
\boxed{
\mathcal S_{\rm Sr/Cs}
=2\mathcal S_{\rm Sr/CaF}
}
\]

under the same leading sensitivity assumptions used in v0.5.

For one unscreened scalar and one dominant QCD spurion, the clock--equivalence-principle consistency line also remains

\[
\boxed{
\frac{\beta_{AB}}{\eta_{CD}}
=-
\frac{\Delta K_\mu-\Delta K_q}
{\Delta Q'_{\widehat m}{}^{CD}}.
}
\]

The \(Z_N\) sector changes the technically natural relation between \(m_a\) and the common coupling \(d_g\); the coupling cancels from the dimensionless clock/EP ratio.

---

## 9. Exact symmetry requirements and failure modes

### 9.1 The complete renormalization environment must be replicated

It is not enough to add \(N-1\) arbitrary spectator fermions. If \(\Psi_0\) interacts with visible QCD while its partners see different gauge or matter content, gauge corrections split their masses and Yukawa functions. That splitting is a hard \(Z_N\)-breaking spurion and regenerates low harmonics.

The safe microscopic options are:

1. replicate the full Standard Model, as in existing \(Z_N\)-protected modulus constructions;
2. replicate at least every gauge and matter interaction entering the \(\Psi_k\) renormalization functions;
3. derive the exchange symmetry from a discrete gauge or geometric translation symmetry.

### 9.2 Quantitative tolerance to hard breaking

Let sector-dependent corrections be represented by weights \(1+\Delta_k\). Define their discrete Fourier components

\[
\widetilde\Delta_p
=\frac1N\sum_{k=0}^{N-1}
\Delta_k e^{-2\pi ipk/N}.
\]

An order-\(p\) harmonic can then appear parametrically as

\[
\delta V_p
\sim
\frac{N_cM^4}{16\pi^2}
\widetilde\Delta_p\epsilon^p
\cos(px+\delta_p).
\]

For the protected \(N\)-th harmonic to dominate,

\[
\boxed{
|\widetilde\Delta_p|
\lesssim
\epsilon^{N-p},
\qquad p<N,
}
\]

up to order-one coefficient ratios.

For \(N=6\) and \(\epsilon=10^{-6}\), this is ferocious. The symmetry must be exact in the Lagrangian; approximate sector equality is not enough.

### 9.3 Elementary-field quality problem

The operator

\[
\frac{c_N}{M_*^{N-4}}
\left(\Phi^N+\Phi^{\dagger N}\right)
\]

is allowed by \(Z_N\). It produces

\[
\delta m_a^2
\sim
N^2|c_N|
\frac{f_a^{N-2}}{M_*^{N-4}}.
\]

For a high decay constant, this can overwhelm the protected fermion-loop potential. Therefore the elementary-global-\(\Phi\) theory is an infrared model, not a sufficient ultraviolet explanation.

A credible completion must make the approximate continuous shift a gauge or geometric remnant, or otherwise suppress \(c_N\) by a controlled microscopic mechanism.

---

## 10. Preferred quality completion: a deconstructed Wilson-line ratio mode

The most attractive ultraviolet direction is to realize \(a\) as the gauge-invariant Wilson-line phase of a four-dimensional deconstructed gauge theory.

Take a cyclic moose of gauge groups connected by link scalars. Local gauge transformations remove all but one collective phase. The remaining gauge-invariant variable is schematically

\[
\exp\left(i\frac a{f_a}\right)
\sim
\prod_j\frac{\Sigma_j}{|\Sigma_j|}.
\]

Its shift symmetry descends from gauge invariance. Local renormalizable operators cannot depend on the full Wilson loop; an \(a\)-dependent potential requires propagation around the complete theory-space circle or explicit boundary/nonlocal breaking. This supplies:

- a discrete/geometric origin for the cyclic exchange;
- protection against generic local ultraviolet operators;
- a natural explanation for why the first field-dependent invariant requires a complete orbit;
- a route to a fully renormalizable four-dimensional quality completion.

A complete model must still derive the separate-QCD-sector mass orbit while keeping the colour groups distinct. The technically clean implementation is a replicated colour quiver linked only through a gauge-protected singlet Wilson-line sector and symmetry-related messenger chains. This is a concrete next construction rather than a solved detail of the present note.

---

## 11. Cosmological and environmental issues

### 11.1 Mirror sectors and reheating

Exact microscopic \(Z_N\) implies degenerate sectors. If all are reheated equally, hidden radiation and relics are generally unacceptable. The symmetry should be broken by the **state**, not by hard couplings:

\[
\text{exact symmetric Lagrangian}
+\text{asymmetric initial condition/reheating state}.
\]

A reheating model must preserve the ultraviolet cancellation while populating primarily one sector. Recent cyclic models explicitly exploit spontaneous asymmetry of the relic state while retaining exact microscopic symmetry.

### 11.2 Finite-density potential

Visible matter is itself a sector-asymmetric state. It generates

\[
V_{\rm matter}(a)
=\rho_{\rm vis}
\left[
1+\alpha_{\rm vis}\frac{a-a_0}{M_{\rm P}}+\cdots
\right].
\]

This term is not \(\epsilon^N\)-suppressed. It is the physical source of the fifth force and clock redshift, but it can also:

- shift the local vacuum;
- increase the in-medium effective mass;
- screen or pin the field inside dense bodies;
- create nontrivial boundary profiles between sectors of different density.

The next phenomenological calculation must solve the nonlinear static field profile for Earth, Sun and laboratory source geometries.

### 11.3 Domain walls

The protected vacuum has \(N\) degenerate minima. Domain walls are avoided if:

- symmetry breaking occurs before inflation and is not thermally restored;
- a tiny symmetry-compatible bias removes the degeneracy without spoiling the mass hierarchy;
- or the discrete symmetry is gauged/geometric so apparently distinct vacua are identified appropriately.

### 11.4 Heavy coloured fermions

A stable visible colour triplet is excluded cosmologically. The visible \(\Psi_0\) must decay. A vectorlike down-type or up-type assignment with small replicated mixing can provide decays while preserving the one-loop fundamental-representation threshold coefficient. The exact collider bound is decay-model dependent and is not fixed in this note.

### 11.5 CP structure

The mass orbit is real. Integrating out \(\Psi_k\) produces \(aG_k^{\mu\nu}G^k_{\mu\nu}\)-type scalar couplings, not an anomalous \(aG\widetilde G\) term from a complex fermion mass phase. A generalized CP assignment and the chosen vacuum must nevertheless be specified in a full phenomenological model.

---

## 12. Novelty boundary

The broad protection mechanism is established:

- nonlinearly realized discrete symmetries can permit nonderivative Yukawa couplings while forcing the radiative potential to begin at high spurion order;
- replicated-Standard-Model \(Z_N\) models have used the same orbit cancellation to keep a photon-coupled modulus ultralight;
- mirror-QCD \(Z_N\) constructions suppress axion masses while preserving comparatively large couplings;
- a 2026 axion--WIMP model again uses cyclic fermions to project the Coleman-Weinberg potential onto the \(N\)-th harmonic.

Therefore the following cannot be claimed as new:

\[
\text{``use }Z_N\text{ copies to obtain }V\sim\epsilon^N\text{ while a one-sector coupling is }O(\epsilon).''
\]

The candidate original contribution is narrower:

1. a **CP-even vectorlike QCD threshold** rather than a photon threshold or anomalous axion coupling;
2. preservation of the exact visible-QCD decoupling response
   \[
   \mathcal D_{\Psi\to3}^{(1)}=\frac{2}{27};
   \]
3. embedding that response in the universal-scale-lock/chronometric-shear framework;
4. the \(Z_6\) mass--coupling law
   \[
   m_a^2\propto d_g^6;
   \]
5. the observation that cyclic protection leaves the dimensionless clock--EP consistency line unchanged while making an ultralight mediator technically possible.

A systematic priority search found close precedents for every mechanism, but no exact indexed match for this combined QCD-threshold/chronometric construction. That remains a candidate priority claim, not a declaration of priority.

---

## 13. What has been solved and what has not

### Solved in this step

\[
\boxed{
\begin{gathered}
\text{exact cyclic symmetry}
\Longrightarrow
V_{\rm vac}(a)=O(\epsilon^N),\\[1mm]
\text{one visible fundamental threshold}
\Longrightarrow
\mathrm d\ln(\Lambda_3/\chi)
=\frac{2}{27}\mathrm d\ln(M_0/\chi)+\cdots,\\[1mm]
N=6,\ x_0=\pi/2
\Longrightarrow
m_a^2=\frac{27}{320\pi^2}\frac{M^4}{f_a^2}\epsilon^6,
\quad
d_g=\frac{2}{27}\frac{M_{\rm P}}{f_a}\epsilon.
\end{gathered}
}
\]

This removes the catastrophic \(M^4\epsilon^2/f_a^2\) contribution without nullifying the desired QCD response.

### Still open

1. construct the full discrete-gauge/deconstructed messenger completion that produces the orbit while keeping \(SU(3)_k\) sectors distinct;
2. derive two-loop gauge/Yukawa corrections and verify the \(O(\epsilon^N)\) spurion counting in the complete replicated theory;
3. solve asymmetric reheating without hard \(Z_N\) breaking;
4. calculate finite-density screening around realistic sources;
5. specify the decaying vectorlike-quark phenomenology;
6. combine current clock, MICROSCOPE, torsion-balance, stellar and cosmological limits in one likelihood;
7. test whether the same protection can arise from the proposed deeper 36-field/Turok sector rather than an added elementary \(\Phi\).

---

## 14. Immediate next calculation

The next decisive calculation is no longer the vacuum mass. It is the **environmental field profile**.

For the \(Z_6\) benchmark, derive and solve

\[
\Box a
=
\frac{\partial V_{Z_6}}{\partial a}
+\sum_A
\frac{\partial\ln m_A(a)}{\partial a}\rho_A(x)
\]

for spherical sources, including the QCD composition charges of Earth, Sun and laboratory test bodies. This will determine whether the same finite-density effect that makes the model observable also screens it.

A parallel ultraviolet task is to construct the deconstructed gauge-quality completion and compute its leading nonlocal breaking operator. Those two tasks now dominate the viability question.

---

## References

1. S. Das and A. Hook, *Non-linearly realized discrete symmetries*, arXiv:2006.10767.
2. D. Brzeminski, Z. Chacko, A. Dev and A. Hook, *A Time-Varying Fine Structure Constant from Naturally Ultralight Dark Matter*, Phys. Rev. D 104, 075019 (2021), arXiv:2012.02787.
3. L. Di Luzio, B. Gavela, P. Quilez and A. Ringwald, *An even lighter QCD axion*, JHEP 05 (2021) 184, arXiv:2102.00012.
4. C. Delaunay, S. J. Lee, Y. Yin and B. Yu, *Natural Phantom Crossing from Axion-WIMP Interactions*, arXiv:2607.28721.
5. S. Hor, Y. Nakai, M. Suzuki and J. Xu, *Deconstructing the Extra-Dimensional Axion*, arXiv:2606.02728.
6. K. G. Chetyrkin, B. A. Kniehl and M. Steinhauser, *Decoupling relations to O(alpha_s^3) and their connection to low-energy theorems*, Nucl. Phys. B 510 (1998) 61, arXiv:hep-ph/9708255.
7. T. Damour and J. F. Donoghue, *Equivalence principle violations and couplings of a light dilaton*, Phys. Rev. D 82, 084033 (2010), arXiv:1007.2792.
8. P. Touboul et al., *MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle*, Phys. Rev. Lett. 129, 121102 (2022), arXiv:2209.15487.

---

## Verification statement

The accompanying verification script independently checks:

- the closed form of \(F_N\);
- root-of-unity cancellation for \(m<N\);
- the numerical one-loop Fourier coefficient for representative \(N\);
- the telescoping \(2/27\) threshold coefficient;
- the exact \(Z_6\) identities \(F_6=1/160\), \(\kappa_0=\epsilon\) and \(m_a^2=(27/320\pi^2)M^4\epsilon^6/f_a^2\);
- positivity of all \(M_k\) over 100,000 random points with \(0<\epsilon<1\);
- representative mass/range benchmarks.

All programmed checks pass.
