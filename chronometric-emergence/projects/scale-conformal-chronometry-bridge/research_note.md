# From scale/conformal symmetry to spectral chronometry: applicability audit v0.1

**Author:** Angus Muffatti  
**Assistance:** AI-assisted analysis, derivation and implementation.  
**Date:** 10 October 2026  
**Status:** First applicability audit and conditional bridge, not a new proof of scale-to-conformal enhancement or a quantum completion.

## 1. Question and result

Can OpenAI's *Scale and conformal symmetry in four-dimensional operational quantum field theory* (26 September 2026) provide the missing microscopic justification for our common spectral scale?

**Direct application to our massive, scale-selecting vacuum: no.** A dilation-invariant vacuum is an explicit hypothesis of the paper. Our nonzero scale-selecting order parameter does not satisfy it. A Coleman-Weinberg realization also lacks the required exact quantum scale symmetry in its conventional anomalous formulation. The paper's reconstructed improvement operator is not automatically our scale field.

**A conditional connection: yes.** Exact dilation covariance across a family of broken vacua, with every independent dimensionless datum fixed, implies that physical spectral locations scale with one mass-coordinate f. This implication uses dilation covariance, not the paper's new scale-to-conformal enhancement machinery. It does not, by itself, justify replacing f by an arbitrary spacetime-dependent field.

A concrete classical two-scalar model verifies the homogeneous bridge and exposes a massless radial mode. A specified time-dependent probe calculation shows why derivative and state-preparation corrections must be audited before treating local clock-ratio drift as a fundamental failure of metric universality.

The results below are standard identities and a targeted synthesis with our existing framework. No literature-priority claim is made.

## 2. Source boundary

The OpenAI source snapshot is `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. This audit reads the abstract, theorem and scope discussion in Section 1; the assumptions and conventions in Section 2; and the opening reconstruction statement in Section 8. It does not independently validate the intermediate modular, dispersion, short-product or domain arguments. Source was inspected as LaTeX; the PDF fetch was unavailable.

Our comparison snapshot is `terrorproforma/maths@dbf9d2372773b219a5d5088862643431170c2c9f`. The canonical v0.5 notes identify themselves as an archive reconstruction. They are evidence of the project's stated assumptions, not an independent proof of those assumptions. The frontier-evidence-v2 report supersedes earlier expansive PASS labels and remains unchanged by this audit.

Primary sources and precise repository paths are in `sources.json`. In this note [O1] denotes the OpenAI manuscript; [P1] our v0.5 QCD notes; [P2] the frontier report; [T1] Tamarit's *Running couplings with a vanishing scale anomaly*, arXiv:1309.0913v4; and [W1] Wetterich's *Quantum scale symmetry*, arXiv:1901.04741v2.

## 3. What the OpenAI theorem supplies

The paper assumes a four-dimensional positive-energy local quantum theory in a Poincare- and dilation-invariant vacuum representation. Its field labels have a discrete bounded-below dimension spectrum, finite multiplicity and finite scaling support. It additionally requires a physical local dilation current and compatible realizations of fields in a fixed bounded local net. These are stronger statements than having a classically scale-invariant Lagrangian or successful numerical Ward-identity tests. Vacuum uniqueness is NOT required. [O1, Assumption 2.1]

Its conclusion is a Hermitian physical scalar L of scaling dimension two with

$$
T^{(4)\mu}{}_{\mu}=\Box L,
\qquad
t_{\mu\nu}=T^{(4)}_{\mu\nu}
+\frac13(\partial_\mu\partial_\nu-\eta_{\mu\nu}\Box)L,
$$

where t is symmetric, conserved and traceless, preserving translation and Lorentz Ward charges. The conformal conclusion concerns local Ward identities in the specified physical algebra. A global conformal action on the whole bounded net is expressly not proved. [O1, Theorem 1.1]

Three different claims must stay separate:

1. Improving a stress tensor in flat spacetime.
2. Selecting a nonzero vacuum scale and generating physical spectral standards.
3. Establishing a curved-spacetime local Weyl symmetry and universal matter coupling.

The theorem establishes the first under its assumptions, not the latter two.

## 4. Two elementary obstructions to a direct import

### 4.1 A scale-invariant vacuum does not supply the desired condensate

For a homogeneous scalar operator O of nonzero dimension Delta, a translation- and dilation-invariant vacuum has a finite one-point function satisfying

$$
\langle O\rangle=e^{s\Delta}\langle O\rangle
\quad\hbox{for every }s.
$$

Hence that expectation is zero. In particular, the paper's dimension-two L has zero expectation in that state. A nonzero f obtained from a condensate instead requires a different, symmetry-breaking state. An engineering mass dimension, a Weyl weight and an exact quantum scaling dimension must not be identified without a model-specific argument.

The paper's free-scalar example makes the distinction explicit: L = -:phi^2:/2 is an improvement operator in a massless theory. Its existence supplies neither a positive condensate nor a selected massive clock transition. A renormalized composite is not automatically a positive operator whose square root can be declared a new physical scalar. [O1, Section 1]

### 4.2 Unbroken dilations do not select an isolated positive mass

In the paper's convention,

$$
U_D(s)P_\mu U_D(-s)=e^sP_\mu.
$$

Thus the joint momentum spectrum, and the invariant-mass spectrum derived from it, are closed under arbitrary positive scaling. Any positive spectral mass would bring its entire dilation orbit. There can be no isolated positive mass scale or strictly positive lower bound on a nonempty massive sector under this unbroken action. This is not a claim that every timelike spectral contribution vanishes: a gapless continuum of timelike masses is allowed.

A massless theory can still support frequencies fixed by preparation, momentum, a cavity or a thermal state. Those frequencies are not a dynamically selected vacuum standard supplied by this theorem. Nor does the obstruction exclude massive excitations in a spontaneously broken phase; then dilations need not be unitarily implemented within one fixed-vacuum sector. [O1, Section 2; W1]

## 5. The conditional homogeneous correlator bridge

Assume separately:

- a family of homogeneous vacua labeled by a positive mass-coordinate f;
- exact dilation covariance relating those vacua, not necessarily a dilation unitary within each broken-vacuum Hilbert sector;
- fixed independent dimensionless parameters q, including shape moduli, physical coupling data and threshold ratios;
- corresponding physical operator channels, with well-defined identifiable spectral features.

For a dilation eigenoperator of dimension Delta, separated-point covariance has the form

$$
G_O(x;f,q)=f^{2\Delta}\,\mathcal G_O(fx;q).
$$

The parameter f is chosen to have scaling weight one. It need not equal the expectation of an exact dimension-one interacting local operator. With operator mixing, use matrix covariance; the spectral-location conclusion is unchanged if the same family and channels are tracked.

In momentum space, modulo contact polynomials and normalization conventions,

$$
\widetilde G_O(p;f,q)
=f^{2\Delta-4}\widetilde{\mathcal G}_O(p/f;q).
$$

Therefore poles or other identifiable spectral locations move as

$$
M_A(f,q)=f\,c_A(q).
$$

For a scalar spectral density in a compatible convention,

$$
\rho_O(s;f,q)=f^{2\Delta-4}\widehat\rho_O(s/f^2;q).
$$

Contact terms do not move a physical spectral singularity. Operator residues can scale differently without spoiling the statement about masses. The existence, stability and observability of a useful transition still have to be demonstrated; a mass pole is not itself a functioning clock.

Along the fixed-q orbit,

$$
\partial_{\ln f}\ln\frac{M_A}{M_B}=0.
$$

If suitable transition frequencies obey the same covariance, their leading local adiabatic approximation gives

$$
\omega_A(x)=c_A\chi(x),\qquad
\widehat g_{\mu\nu}=(\chi/\chi_*)^2g_{\mu\nu}.
$$

This reproduces the existing spectral-factorization criterion. The additional physical task is proving that the actual background motion stays on the fixed-q orbit. In general,

$$
\mathcal S_{AB}
=d\ln(\omega_A/\omega_B)
=\sum_I\partial_{q^I}\ln(c_A/c_B)\,dq^I
+\hbox{derivative and state corrections}.
$$

The zero-form coefficients here are dimensionless. This is a conditional application of familiar scaling and broken-phase Ward reasoning, with close precedent in [T1]; it is not a new consequence unique to [O1].

## 6. Concrete local two-scalar benchmark

Use the paper's signature (+---), canonical positive kinetic terms, and

$$
\mathcal L=\tfrac12(\partial\chi)^2+\tfrac12(\partial h)^2-V,
\qquad
V=\frac\lambda4(h^2-\zeta^2\chi^2)^2,
\quad\lambda>0,\ \zeta>0.
$$

This is a conventional dilaton-portal toy model, not a new microscopic construction; [T1, Section 3] treats the same class with different quartic normalization. We use it to test the bridge, not to claim that the full Standard Model or the full operational-net hypotheses have been constructed.

The vacuum ray is (chi,h) = (f,zeta f), f > 0. In field order (chi,h), the Hessian is

$$
H=2\lambda\zeta^2f^2
\begin{pmatrix}\zeta^2&-\zeta\\-\zeta&1\end{pmatrix}.
$$

Its radial vector (1,zeta) has eigenvalue zero, while (-zeta,1) has

$$
m_\perp^2=2\lambda\zeta^2(1+\zeta^2)f^2>0.
$$

With Q = chi^2 + h^2, choose L = -Q/2. The standard improvement gives, on the classical equations of motion,

$$
t^\mu{}_{\mu}=4V-\chi V_\chi-hV_h=0.
$$

Optional singlet probes psi_i, with canonical kinetic terms and potential y_i^2 h^2 psi_i^2/2, have positive tree-level masses m_i = y_i zeta f around psi_i = 0. Their Euclidean tree propagators are

$$
G_i(p;f)=\frac1{p^2+y_i^2\zeta^2f^2},
\qquad
(f\partial_f+p\partial_p+2)G_i=0.
$$

This is an explicit correlator-level realization of the homogeneous mass scaling. It is a tree-level statement. Interactions, infrared dressing, beta functions, composite-operator mixing and transition readout are not solved by this check.

The massless radial mode is compulsory for this exactly homogeneous stationary valley, not a numerical accident: differentiating Euler's quartic identity at a stationary nonzero point gives H phi = 0. An additional allowed eta chi^4/4 remains scale invariant but requires eta = 0 for this nonzero valley. Scale invariance alone therefore does not guarantee the desired vacuum. The corresponding quantum flat-direction tuning is discussed in [T1].

## 7. The Coleman-Weinberg branch is a different branch

As a local diagnostic of conventional anomalous scale generation, add

$$
V_{\rm CW}(\chi)=B\chi^4\left(\ln\frac{\chi^2}{f_0^2}-\frac12\right)
+\frac B2f_0^4,\qquad B>0.
$$

The constant is chosen solely to set the minimum's potential to zero. The equations are

$$
V'_{\rm CW}(f_0)=0,\qquad V''_{\rm CW}(f_0)=8Bf_0^2,
$$

but

$$
\Theta_{\rm CW}=4V_{\rm CW}-\chi V'_{\rm CW}
=-2B(\chi^4-f_0^4).
$$

A vanishing trace expectation at the tuned minimum is NOT a vanishing trace operator. In the full two-field model at f = f0,

$$
\det H_{\rm lifted}=16B\lambda\zeta^2f_0^4>0.
$$

With positive trace, both eigenvalues are positive. The single-field curvature 8B f0^2 is not generally an eigenvalue of that mixed two-field Hessian. Lifting the radial direction here comes with explicit quantum scale breaking in the effective description.

Our older conventional Coleman-Weinberg generator and our separately proposed exact scale-preserving compensator EFT must not be merged without checking their Ward identities. Exact scale-preserving effective regularization can coexist with dimensionless running, but needs its additional interactions and a flat direction; it is not automatically a finite-parameter UV completion. [P1; T1]

This audit does not retract the v0.5 notes, which already distinguish a flat global dilaton, a possible local-Weyl gauge realization and completion-dependent lifting. It makes that branch distinction a prerequisite for importing [O1].

## 8. QCD: a concrete physical-lock diagnostic

At one loop in a fixed-flavor conventional theory,

$$
\Lambda=\mu\exp[-8\pi^2/(b g^2(\mu))],\qquad
\beta_g=-\frac{b g^3}{16\pi^2}.
$$

The total renormalization-scale derivative obeys

$$
\frac{d\ln\Lambda}{d\ln\mu}
=1+\frac{16\pi^2}{b g^3}\beta_g=0.
$$

Consequently, simply naming the subtraction point mu = kappa chi does not make Lambda proportional to a physical chi. With the underlying RGI scale fixed, d ln(Lambda/chi)/d ln chi = -1 in this fixed-flavor diagnostic. This is not the physical derivative of a fully specified compensator theory.

For our existing seven-to-three-flavor threshold chain, the leading-log relation is

$$
\Lambda_3^9=\Lambda_7^{19/3}(M_\Psi m_t m_b m_c)^{2/3}.
$$

Define delta_n = d ln(Lambda_n/chi) and epsilon_j = d ln(m_j/chi). Then

$$
\boxed{\delta_3=\frac{19}{27}\delta_7
+\frac{2}{27}(\epsilon_\Psi+\epsilon_t+\epsilon_b+\epsilon_c).}
$$

If Lambda7 and all four thresholds co-scale with chi, delta3 = 0. If only the four thresholds co-scale while Lambda7 remains fixed, then delta3 = -(19/27) d ln chi. If the high scale and ordinary heavy quarks are locked but Psi has a ratio defect, the previous 2/27 result is recovered. These are conditional one-loop identities, not a new QCD coefficient or a nuclear clock prediction. [P1]

The OpenAI theorem provides no missing argument that delta7 = 0 in our theory. That must come from the actual quantum construction, not from a choice of subtraction variable.

## 9. A finite-gradient test of promoting f to chi(x)

To isolate a failure of exact local promotion without invoking unknown QCD, consider specified spatially homogeneous free scalar probe modes on an externally prescribed flat-spacetime background chi(t). Set spatial momentum to zero and absorb the fixed portal ratio into y_A:

$$
\ddot u_A+y_A^2\chi(t)^2u_A=0.
$$

For the adiabatically prepared complex mode

$$
u_A=(2W_A)^{-1/2}\exp[-i\!\int W_A dt],
$$

substitution gives

$$
W_A^2=\Omega_A^2-\frac{\ddot W_A}{2W_A}
+\frac34\left(\frac{\dot W_A}{W_A}\right)^2,
\qquad\Omega_A=y_A\chi.
$$

Through second adiabatic order,

$$
W_A=y_A\chi\left[1+\frac{J}{y_A^2}\right]+O(\partial^4),
\qquad
J=\frac{3\dot\chi^2}{8\chi^4}-\frac{\ddot\chi}{4\chi^3}.
$$

Thus, within this preparation and approximation,

$$
\ln\frac{W_A}{W_B}=\ln\frac{y_A}{y_B}
+\left(\frac1{y_A^2}-\frac1{y_B^2}\right)J
+O(\partial^4).
$$

Even perfectly co-scaling instantaneous masses do not make these finite-frequency evolving phases exactly co-scale. This is an ordinary adiabatic/finite-frequency effect, not evidence of fundamental equivalence-principle violation or nonexistence of a metric. Real clocks also require their actual finite-size, acceleration, curvature and readout corrections to be separated. A field redefinition or different preparation can change intermediate phase conventions; the code fixes its canonical modes and initial state explicitly.

### Numerical check

Use dimensionless units chi(0)=1, time in the corresponding inverse scale, chi(t)=1+a t, 0 <= t <= 20, y = 1 and 2, and a = 0.01, 0.02, 0.04. The maximum adiabatic parameter |dot Omega/Omega^2| is 0.04. Prepare second-order adiabatic initial data and independently integrate the exact linear ODE with DOP853. Repeat with tighter tolerances.

At a = 0.02, the y=1 leading-frequency approximation has maximum relative error 1.5000e-4; the second-order formula reduces it to 6.6043e-7. The ratio prediction's maximum absolute log error is 6.7310e-7, against a maximum log deviation 1.1249e-4. Initial agreement with the second-order approximation is set by preparation, not counted as independent evidence. The subsequent interval comparison tests its dynamical persistence.

Over all six solves, the maximum Wronskian error is 7.23e-12 and the solver-refinement difference is 2.64e-13. These are numerical diagnostics of this specified oscillator system, not evidence for a completed cosmological model.

## 10. Decision and next calculation

| Claim | Result |
|---|---|
| Apply [O1] directly to our f != 0 physical vacuum | OUTSIDE STATED HYPOTHESES |
| Identify the reconstructed L with a positive clock scale | NOT ESTABLISHED |
| Homogeneous spectral scaling on a fixed-q dilation orbit | CONDITIONAL DERIVATION |
| Classical local two-scalar illustration | EXPLICITLY VERIFIED |
| Conventional CW lifting preserves exact unbroken scale Ward identity | NO |
| Choosing mu proportional to chi alone proves QCD locking | NO |
| Exact homogeneous scaling guarantees exact local evolving clock ratios | NO; GRADIENT/PREPARATION QUALIFICATIONS NEEDED |
| Operational-net hypotheses or quantum UV completion verified | NO |
| OpenAI enhancement proof independently audited | NO |

The next model-specific calculation is the renormalized zero-momentum dilaton insertion into TWO independent physical spectral channels of a chosen scale-preserving scalar/Yukawa EFT, together with the leading nonzero-momentum correction. Fix the regulator and counterterm basis, include the allowed quartic and evanescent interactions, and check the flat-direction condition rather than imposing a cancellation in the answer.

The homogeneous target is

$$
\mathcal R_A=\left.f\partial_f\ln M_A\right|_{q}-1=0,
\qquad \mathcal R_A-\mathcal R_B=0.
$$

The physical derivative holds independent dimensionless inputs fixed; it is not merely mu d/dmu. The local target is the independently calculated difference of derivative-response coefficients for the same chosen probes. Only after these checks should one connect the common-scale argument back to QCD thresholds or use finite-data clock-ratio rank as evidence of additional non-universal scalar fields.

No previous non-Abelian transport, compact-object or UV-completion blocker is removed by this audit. [P2]
