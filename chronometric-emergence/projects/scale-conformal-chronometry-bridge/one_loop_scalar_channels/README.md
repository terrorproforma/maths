# Two quantum scalar channels: one-loop scale response and infrared limits

**Author:** Angus Muffatti  
**Assistance:** AI-assisted derivation, implementation and checking.  
**Date:** 11 October 2026  
**Status:** Executed one-loop scalar benchmark. No claim of a complete quantum theory, Yukawa calculation, physical clock, or new theorem.

## Result and scope

This starts the quantum calculation proposed by the preceding scale/conformal applicability audit. It does not merely restate the homogeneous scaling ansatz. We calculate the momentum-dependent one-loop inverse propagators for two massive scalar channels, include the finite interactions induced by a field-dependent regulator, check zero-momentum dilaton-source insertions, and inspect an on-shell three-point subdiagram at nonzero momentum transfer.

The homogeneous perturbative mass-shell locations co-scale with the vacuum parameter through one loop. But the massless dynamical dilaton makes the propagator derivative logarithmically singular at the tree threshold. A triangle contribution also has an infrared-divergent momentum-transfer expansion. Thus the calculation does NOT yet supply two well-defined clock transitions or a finite physical gradient-response coefficient.

The scope is the scalar branch of the proposed scalar/Yukawa test: no fermions are included. The two scalar fields are physical gauge singlets, not gauge-fixed elementary gauge-sector variables. Nevertheless, their asymptotic pole interpretation needs infrared treatment. We calculate zero-soft source insertions and one finite-transfer subdiagram, not the complete inclusive/dressed three-point response.

## 1. Defined quantum model

Use four-dimensional signature (+---), positive canonical kinetic terms for three real fields chi, A and B, and the tree potential

$$
V=\frac{a}{2}\chi^2 A^2+\frac{b}{2}\chi^2 B^2
 +\frac{\lambda_A}{24}A^4+\frac{\lambda_B}{24}B^4
 +\frac{\kappa}{4}A^2B^2+\frac{\lambda_\chi}{24}\chi^4.
$$

Take a,b,lambda_A,lambda_B,kappa positive and lambda_chi zero at tree order. The tree vacuum ray has chi=f>0, A=B=0. The massive channels have m_A^2=a f^2 and m_B^2=b f^2; the radial dilaton is massless. Independent A and B reflection symmetries forbid a one-particle state from decaying entirely into the other species. They do not remove soft-dilaton dressing.

The bare potential in d=4-2 epsilon is defined, before expansion or integration, by

$$
\widetilde V=\mu_\chi^{2\epsilon}(V+\delta V),
\qquad \mu_\chi=z\chi^{1/(1-\epsilon)}.
$$

The dimensionless parameter z and renormalized couplings specify the subtraction prescription. Calculations are a local effective-field-theory expansion around f>0. This is not ordinary fixed-mu renormalization followed by substitution of a field expectation value. Higher orders require the allowed effective operators, including nonpolynomial interactions. This construction and its flat-direction qualification have prior art [1,2].

We use the MS-bar-type prescription of [2], retain its regulator-induced finite term, and impose a one-loop flat-vacuum condition below. A finite homogeneous term can be moved between parameters by a scheme change, so numerical mass shifts at fixed displayed couplings are not scheme-independent predictions without physical matching.

## 2. Regulator-induced interaction, derived from the Hessian

Let H_ij=V_ij, ell=ln(z chi), and

$$
K_{ij}=\ell_i V_j+\ell_j V_i+\ell_{ij}V.
$$

To the necessary order, the Hessian of the regulated potential is

$$
\widetilde H=\mu_\chi^{2\epsilon}(H+2\epsilon K)+O(\epsilon^2).
$$

Its one-loop determinant has a pole proportional to -Tr(H^2)/(64 pi^2 epsilon). The O(epsilon) Hessian term multiplying that pole supplies the finite contribution

$$
U_{\rm ev}=\frac{\Delta U}{64\pi^2},\qquad
\Delta U=-4\,\mathrm{Tr}(HK)
=-\frac4{\chi^2}\left[V_{\chi\chi}(2\chi V_\chi-V)
 +2\chi\sum_{i=A,B} V_i V_{i\chi}\right].
$$

This is the direct multi-field version of [2, equations (12)-(20)], not a new regularization theorem. The code independently constructs the Hessian and K and checks their trace against the field formula. Inserting the chosen V gives the quadratic terms

$$
\Delta U=-16 a^2\chi^2 A^2-16 b^2\chi^2 B^2+O((A,B)^4),
$$

and hence

$$
\delta m_{A,\rm ev}^2=-\frac{8a^2 f^2}{16\pi^2},\qquad
\delta m_{B,\rm ev}^2=-\frac{8b^2 f^2}{16\pi^2}.
$$

lambda_chi is counted as one-loop order after vacuum tuning, so terms proportional to it inside a one-loop graph belong to the next order. The local terms above would be missed by substituting mu=z f in the conventional completed diagrams. Their homogeneous form also means that the scale-only response test cannot detect their omission. Finite redefinitions of a and b can absorb these quadratic pieces; the full regulated theory and its matching, not one polynomial coefficient alone, is what must be compared.

## 3. Explicit momentum-dependent inverse propagators

Write s=p^2 and use

$$
\Gamma_A^{(2)}(s;f)=s-a f^2-\Sigma_A(s;f).
$$

At the stated one-loop order, let L_a=ln(a/z^2), L_b=ln(b/z^2), r=s/(a f^2), and

$$
I(r;L)=\int_0^1 dx\,\ln\!\left[\frac{x(m^2-(1-x)s)-i0}{z^2 f^2}\right]
=L-2-\frac{1-r}{r}\ln(1-r-i0).
$$

The continuous values are I(0;L)=L-1 and I(1;L)=L-2. The result is

$$
\Sigma_A=\frac{f^2}{16\pi^2}
\left[\frac{\lambda_A a}{2}(L_a-1)
+\frac{\kappa b}{2}(L_b-1)
+4a^2 I(r;L_a)-8a^2\right].
$$

The B expression follows by exchanging a with b and lambda_A with lambda_B.

These terms have explicit diagrammatic origins: the A quartic tadpole, the B cross-quartic tadpole, the A/dilaton bubble, and the regulator-induced local term. Expanding the portal gives a cubic vertex of strength 2 a f. The two internal bubble lines are distinct species, giving the coefficient 4 a^2 f^2. The massless dilaton tadpole is scaleless in dimensional regularization. Tadpole-reducible contributions are removed by the stationary-background condition. There is no one-loop UV wavefunction counterterm for this scalar potential; the bubble's momentum dependence is retained, not approximated by a potential curvature.

As a separate check, the zero-momentum result agrees with the second derivative of the Coleman-Weinberg potential constructed by numerical eigenvalues of H, with the evanescent term kept separate. The absorptive part above threshold obeys

$$
\mathrm{Im}\,\Sigma_A(s+i0)=-\frac{a^2 f^2}{4\pi}
\left(1-\frac{a f^2}{s}\right),\qquad s>a f^2.
$$

The sign is the required positive-cut convention for the propagator with the stated inverse. A two-body cut is not an all-order spectral-positivity proof.

## 4. Stationarity and subtraction-parameter running

At A=B=0 the one-loop potential is

$$
U(f)=\frac{\lambda_\chi f^4}{24}
+\frac{f^4}{64\pi^2}
\left[a^2(L_a-3/2)+b^2(L_b-3/2)\right].
$$

We impose the finite tuning

$$
\lambda_\chi=-\frac6{16\pi^2}
\left[a^2(L_a-3/2)+b^2(L_b-3/2)\right]+O(\hbar^2).
$$

The ray then has vanishing potential, first derivative, and radial curvature through this order. This is a tuning, not a derived selection of a preferred f and not a solution to vacuum-energy naturalness. The local transverse masses remain positive at the chosen benchmark; global stability at arbitrary field ratios is not established.

The UV Hessian gives, at the order used,

$$
\beta_a=\frac{a\lambda_A+\kappa b+8a^2}{16\pi^2},\qquad
\beta_b=\frac{b\lambda_B+\kappa a+8b^2}{16\pi^2},\qquad
\beta_{\lambda_\chi}=\frac{12(a^2+b^2)}{16\pi^2}.
$$

Here beta means differentiation of the renormalized couplings with respect to ln z. The explicit z derivative of each inverse propagator cancels the tree beta term through one loop. Differentiation of the flat-vacuum tuning gives beta_lambda_chi at the same order. Holding all dimensionless data fixed while varying f is different from varying the subtraction convention and running the couplings.

## 5. The zero-soft source test

Differentiating a regulated diagram with respect to f inserts a zero-momentum background dilaton. We calculate these insertions by differentiating the internal masses, cubic prefactors, subtraction factors, and local evanescent term. This is a diagram-differentiation check, not a separately constructed finite-momentum vertex.

For the bubble denominator, the differentiated integrand is

$$
f\partial_f I=\int_0^1 dx\left[\frac{2m^2}{m^2-(1-x)s}-2\right]=-2r I'(r).
$$

The final -2 is the compensator-dependent subtraction contribution. The tadpoles have corresponding terms. The assembled insertion S_A=f partial_f(m_A^2+Sigma_A), calculated by quadrature, obeys

$$
(f\partial_f+2s\partial_s)\Gamma_A^{(2)}=2\Gamma_A^{(2)}+O(\hbar^2).
$$

Numerical differentiation at fixed external s independently agrees with the insertion result over both channels and 24 off-shell sample points. The largest error normalized to the tree squared mass is below 1.4e-12 for this run.

Two negative controls matter. Omitting the subtraction-source vertices leaves the nonzero residual beta_a f^2, or beta_b f^2. But retaining mu=z f and omitting only the finite evanescent potential still passes a homogeneous mass-scaling test, despite changing the mass estimates in the fixed parameter convention. Thus a vanishing scaling residual alone is not adequate validation of a quantum calculation.

## 6. What happens to the mass ratio

The one-loop mass-shell estimate is evaluated perturbatively at the tree shell:

$$
M_A^2=a f^2+\Sigma_A(a f^2;f)+O(\hbar^2).
$$

We do not solve the truncated Dyson equation near the threshold and interpret any resulting displaced singularity as an exact physical pole. The internal threshold also needs consistent dressing.

The displayed expression scales as f^2. Consequently R_A=partial_ln_f ln(M_A)-1 and R_A-R_B vanish through this order at fixed dimensionless data. This is a perturbative realization of the expected scaling relation, not an independent nonperturbative theorem.

For a=0.04, b=0.09, lambda_A=0.3, lambda_B=0.4, kappa=0.1, z=0.5, the computed values are:

| Quantity | Channel A | Channel B |
|---|---:|---:|
| Tree mass / f | 0.2 | 0.3 |
| One-loop squared-mass shift / tree squared mass | -0.010040524135232314 | -0.014407055116595915 |
| Mass / f, expanded through one loop | 0.19899594758647676 | 0.2978389417325106 |
| Fixed-mu control response through one loop | 0.0026755125055554817 | 0.0036869652936517353 |

The last row is beta_i/(2 a_i), independently checked by differentiating the fixed-mu loop correction. It is a control in the conventionally scale-broken theory at a fixed external subtraction scale, not a contradiction between renormalization schemes after complete physical matching. Also, that theory's varying background need not remain a vacuum ray.

The ratio of the two displayed truncated mass estimates is 0.6681327378781624, versus the tree value 2/3. Radiative corrections change the constant ratio but do not introduce f-dependence in the defined scale-preserving calculation. Digits describe numerical reproducibility, not experimental precision; forming a ratio of truncated masses carries algebraic higher-order terms beyond one-loop accuracy.

## 7. Infrared limit: finite mass shift does not establish an isolated pole

Differentiation gives

$$
I'(r)=\frac{r+\ln(1-r)}{r^2},\qquad
\partial_s\Sigma_A=\frac{4a}{16\pi^2}I'(r).
$$

As r approaches 1 from below, the self-energy remains finite while its derivative diverges logarithmically. The A plus massless-dilaton continuum starts at the same tree mass. A finite-order residue formula is therefore not uniformly controlled at the shell. The formal tendency of 1/(1-Sigma') toward zero is an infrared warning, NOT an all-order proof that the exact spectral delta weight vanishes.

For 1-r equal to 1e-3, 1e-6, and 1e-9 the A-channel derivatives are approximately -0.00599881, -0.01298485, and -0.01998385. The logarithmic divergence is established analytically, not inferred solely from this finite scan.

No finite local counterterm can remove the nonanalytic threshold dependence. A physical response needs an infrared-resolved definition, such as an appropriate inclusive or dressed observable, or an explicitly specified lifting mechanism whose effects on scale symmetry are then audited.

## 8. Actual finite-transfer calculation: an infrared-sensitive triangle

The dilaton/A/A vertex has a triangle with one massless and two massive internal lines. Put the two massive external legs on their tree mass shell and set q^2=-Q^2, Q^2>=0. Omitting its coupling and conventional overall loop factor, its Feynman-parameter denominator is

$$
D=(x_1+x_2)m^2-x_0(x_1+x_2)m^2+x_1x_2Q^2.
$$

Set x_1=v u, x_2=v(1-u), x_0=1-v. The measure is v du dv and

$$
D=v^2[m^2+u(1-u)Q^2].
$$

Cutting off v at v_min isolates the soft logarithm:

$$
C(Q^2;v_{\min})=\ln(1/v_{\min})J(Q^2),\qquad
J(Q^2)=\int_0^1\frac{du}{m^2+u(1-u)Q^2}
=\frac{4\,\operatorname{artanh}\sqrt{Q^2/(4m^2+Q^2)}}{\sqrt{Q^2(4m^2+Q^2)}}.
$$

J(0)=1/m^2. Even the zero-transfer-subtracted triangle contains

$$
C(Q^2)-C(0)=-\frac{Q^2}{6m^4}\ln(1/v_{\min})+O(Q^4\ln(1/v_{\min})).
$$

The two-parameter integral is checked numerically against this factorization. For m^2=1 and Q^2=0.1, the subtracted integrals are -0.07524995903636186, -0.15049991807272406, and -0.22574987710908576 at v_min=1e-2, 1e-4, and 1e-6.

The parameter cutoff is a device for exposing a subdiagram's infrared coefficient. It is NOT a detector resolution or a symmetry-preserving regulator for the full theory. Nor is this subdiagram by itself an observable. We have not summed and dressed the entire finite-transfer response, so this is not proof that an inclusive clock coefficient diverges. It establishes why a finite local gradient coefficient cannot be certified by simply Taylor expanding the untreated on-shell triangle.

The next physical target must specify the infrared-safe observable first. A scalar-mass or finite-time regulator alone would need a demonstrated regulator-independent limit or an explicit physical interpretation. The previous externally prescribed oscillator result is not a substitute for that quantum calculation.

## 9. Verification and provenance

Run from this directory:

```bash
python -m pip install -r requirements.txt
python verify.py
```

The script writes results.json beside itself and exits with failure if any gate fails. This run passes 62/62 checks: 17 symbolic identities and 45 numerical checks, including deliberately incomplete negative controls. These are not 62 independent confirmations of the theory. They test the stated formulae, integral evaluations, soft-source differentiation, subtraction running, and infrared structure.

All executable source is included; results.json records dependency versions and both SHA-256 and Git-blob SHA-1 of the executed script. The run used Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, and SymPy 1.14.0. No gauge-plasma, non-Abelian, cosmological or experimental status is upgraded by these checks.

The preceding audit is pinned to terrorproforma/maths commit 0bebfa0f1296423b85ecf8cf637c7146d260fac4, directory chronometric-emergence/projects/scale-conformal-chronometry-bridge. Its OpenAI paper comparison used openai/math commit fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb. We do not independently validate that paper's enhancement proof here and do not use it to justify a scale-selecting invariant vacuum.

Primary references inspected as HTML on 11 October 2026:

[1] Carlos Tamarit, *Running couplings with a vanishing scale anomaly*, arXiv:1309.0913v4. Scale-preserving effective theory, spontaneous breaking, and the flat-direction qualification. https://arxiv.org/html/1309.0913v4

[2] D. M. Ghilencea, *A manifestly scale-invariant regularization and quantum effective operators*, arXiv:1508.00595v4, especially equations (12)-(20). Regulated Hessian, evanescent determinant term, and subtraction prescription. https://arxiv.org/html/1508.00595v4

The three-field specialization, momentum-dependent diagrams, negative controls, and triangle audit are worked out explicitly here using standard perturbative methods. No priority or novelty claim is made. The code's successful execution is internal evidence, not independent specialist review.
