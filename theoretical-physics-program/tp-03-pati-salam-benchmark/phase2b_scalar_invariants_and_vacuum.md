# TP-03 Phase 2B — Complete invariant-channel basis and certified Pati–Salam vacuum

**Author:** Angus Muffatti  
**Project:** TP-03 — Complete Pati–Salam benchmark  
**Status:** **PHASE 2B COMPLETE FOR THE DECLARED HIGH-SCALE BRANCH**  
**Active branch:** `PS1-MM`

## 1. Terminal result

The initially declared field content

\[
\mathrm{PS1}
=
\Phi_1(1,2,2)
+
\Phi_{15}(15,2,2)
+
\Delta_R(10,1,3)
\]

does **not** define one scalar theory. With all three multiplets treated as independent complex
fields, exact multigraded Molien–Weyl integration gives

\[
\boxed{
N_2=7,\qquad N_3=0,\qquad N_4=131.
}
\]

Thus the most general gauge-invariant renormalisable scalar potential contains

\[
\boxed{138\ \text{independent real parameters}.}
\]

The representation list alone cannot determine a unique vacuum Hessian, threshold spectrum, or
one-/two-loop gauge matching correction.

A separate, explicitly named high-scale branch has therefore been constructed:

\[
\boxed{\mathrm{PS1\text{-}MM}.}
\]

Its \(\Delta_R\) potential is a moment-map potential with a certified global lower bound. It has a
global minimum on exactly the desired highest-weight orbit,

\[
SU(4)_C\times SU(2)_R
\longrightarrow
SU(3)_C\times U(1)_Y,
\]

with:

- exactly nine broken gauge generators;
- exactly nine scalar Goldstone directions;
- no accidental exact Goldstone;
- no physical tachyon;
- no deeper colour- or charge-breaking minimum;
- a fully analytic heavy-vector and \(\Delta_R\)-scalar spectrum.

The result is a **positive existence proof for a healthy high-scale breaking branch** and a
**negative predictivity result for the bare field-content declaration**.

## 2. Reality convention

The Phase 2B count uses the maximally general renormalisable convention compatible with the
Phase 1 Yukawa objective:

\[
\Phi_1\in\mathbb C\otimes(1,2,2),
\]

\[
\Phi_{15}\in\mathbb C\otimes(15,2,2),
\]

\[
\Delta_R\in(10,1,3).
\]

Although \((1,2,2)\) and \((15,2,2)\) are real representations as abstract group
representations, the scalar multiplets are **complexified** rather than subjected to an
\(SO(10)\)-parent reality constraint. Their conjugate polynomial variables are therefore counted
independently. The genuinely complex \(SU(4)\) representation \(10\) is paired with
\(\overline{10}\) only through \(\Delta_R^\dagger\); no independent \(\overline{\Delta}_R\)
multiplet is added.

The real component count is

\[
2\left[4+60+30\right]=188.
\]

Any reality-constrained \(SO(10)\) daughter is a separate, smaller branch and must be recounted
rather than being silently substituted here.

## 3. Complete renormalisable invariant count

### 3.1 Method

For multidegree

\[
\mathbf n
=
(n_{\Phi_1},n_{\Phi_1^\dagger},
n_{\Phi_{15}},n_{\Phi_{15}^\dagger},
n_{\Delta},n_{\Delta^\dagger}),
\]

the invariant space is

\[
\mathcal I_{\mathbf n}
=
\operatorname{Hom}_{G_{\rm PS}}
\left[
\mathbf1,
\bigotimes_X
\operatorname{Sym}^{n_X}(R_X)
\right].
\]

Its dimension is computed by exact Weyl-character integration:

\[
m_{\mathbf n}
=
\int_{G_{\rm PS}}
d\mu(g)\,
\prod_X
\chi_{\operatorname{Sym}^{n_X}R_X}(g).
\]

The implementation converts this integral into an integer constant-term calculation for

\[
SU(4)\times SU(2)_L\times SU(2)_R.
\]

This automatically:

- symmetrises identical commuting scalar insertions;
- quotients Clebsch, Fierz, trace, and finite-rank tensor identities;
- identifies the true dimension of every invariant hom-space;
- avoids overcounting different index contractions representing the same polynomial.

There are no derivative operators in a renormalisable scalar potential, so integration by parts is
irrelevant.

### 3.2 Counts

The seven quadratic real parameters decompose as:

| Sector | Real quadratic parameters |
|---|---:|
| \(\Phi_1\) | 3 |
| \(\Phi_{15}\) | 3 |
| \(\Delta_R\) | 1 |
| **Total** | **7** |

There is no cubic invariant:

\[
\boxed{N_3=0.}
\]

The reasons can also be seen directly: an odd number of \(SU(2)\) doublets cannot form a singlet,
while products containing an unmatched \(10\) carry nontrivial \(SU(4)\) centre charge.

The 131 quartic parameters split as:

| Field support | Real quartic parameters |
|---|---:|
| \(\Phi_1\) | 6 |
| \(\Phi_{15}\) | 34 |
| \(\Delta_R\) | 7 |
| \(\Phi_1+\Phi_{15}\) | 44 |
| \(\Phi_1+\Delta_R\) | 4 |
| \(\Phi_{15}+\Delta_R\) | 28 |
| \(\Phi_1+\Phi_{15}+\Delta_R\) | 8 |
| **Total** | **131** |

The complete multidegree ledger is in `invariant_basis_multidegrees.csv`. The executable
`generate_invariant_coupling_basis.py` further decomposes every symmetric power and tensor product
into irreducible \(SU(4)\times SU(2)_L\times SU(2)_R\) channels using exact Gelfand–Tsetlin
characters. It generates one fixed left-associated coupling path for every invariant:

\[
\boxed{7+0+131=138\ \text{independent coupling channels}.}
\]

The paths are stored in `invariant_coupling_basis.csv` and
`results/invariant_coupling_basis.json`. Each path becomes an explicit component polynomial once a
standard orthonormal Clebsch–Gordan phase convention is chosen. The phase convention is not
physical and is therefore not inflated into hundreds of kilobytes of redundant component tensors.

### 3.3 Predictivity consequence

A threshold spectrum quoted from the representations alone is not a prediction. It is a choice of
point in a 138-dimensional scalar-coupling space. This is why Phase 2B introduces a named branch
rather than retroactively treating one convenient potential as “the” Pati–Salam potential.

## 4. All Standard-Model-singlet high-scale directions

At the \(G_{\rm PS}\to G_{\rm SM}\) transition:

- \(\Phi_1(1,2,2)\) is an \(SU(2)_L\) doublet and contains no full SM singlet;
- \(\Phi_{15}(15,2,2)\) is also an \(SU(2)_L\) doublet and contains no full SM singlet;
- \(\Delta_R(10,1,3)\) contains exactly one complex SM-singlet direction.

Use

\[
10\rightarrow
(6,2/3)\oplus(3,-2/3)\oplus(1,-2)
\]

under \(SU(3)_C\times U(1)_{B-L}\). The component

\[
(1,-2)\otimes |T_R^3=+1\rangle
\]

has

\[
Y=T_R^3+\frac{B-L}{2}=1-1=0.
\]

Thus every SM-preserving high-scale VEV is gauge-equivalent to

\[
\boxed{
\langle\Delta_R\rangle
=
\frac{v_R}{\sqrt2}
|44\rangle_{\rm sym}
\otimes
|T_R^3=+1\rangle.
}
\]

Its complex phase is contained in the broken gauge orbit; it is not an additional physical neutral
modulus.

## 5. The `PS1-MM` potential

Let

\[
r=\Delta_R^\dagger\Delta_R,
\]

and define the moment maps in the \(10\) and \(3\) representations:

\[
\mu_4^A
=
\Delta_R^\dagger T_{10}^A\Delta_R,
\qquad
\mu_R^i
=
\Delta_R^\dagger t_3^i\Delta_R.
\]

The declared high-scale potential is

\[
\boxed{
V_\Delta
=
-m_\Delta^2 r
+
\lambda_\Delta r^2
-
\kappa_4\sum_A(\mu_4^A)^2
-
\kappa_R\sum_i(\mu_R^i)^2.
}
\]

The bidoublets are inert spectators at this stage:

\[
V_{\rm spec}
=
M_1^2\,\Phi_1^\dagger\Phi_1
+
M_{15}^2\,\Phi_{15}^\dagger\Phi_{15}
+
V_{\rm quartic}^{\rm positive},
\]

where \(M_1^2\) and \(M_{15}^2\) denote the complete positive eigenvalues after allowed
\(\Delta_R^\dagger\Delta_R\) cross-couplings are evaluated on the vacuum. Setting off-diagonal
spectator terms to zero defines the benchmark point; an open neighbourhood remains healthy as long
as their operator norm is smaller than the positive mass gap.

This is a sparse, explicitly declared member of the complete invariant space. It is not a claim
that the many other gauge-allowed coefficients vanish in a generic ultraviolet completion.

## 6. Global vacuum theorem

For every \(\Delta_R\),

\[
\sum_A(\mu_4^A)^2
\leq
\frac32r^2,
\]

\[
\sum_i(\mu_R^i)^2
\leq
r^2.
\]

The two bounds are saturated simultaneously precisely on the product highest-weight coherent orbit.
Therefore,

\[
V_\Delta
\geq
-m_\Delta^2r
+
\lambda_{\rm eff}r^2,
\]

where

\[
\boxed{
\lambda_{\rm eff}
=
\lambda_\Delta
-\frac32\kappa_4
-\kappa_R.
}
\]

For

\[
\boxed{
\kappa_4>0,
\qquad
\kappa_R>0,
\qquad
\lambda_{\rm eff}>0,
\qquad
m_\Delta^2>0,
}
\]

the complete potential is bounded below and its global minima satisfy

\[
r=\frac{m_\Delta^2}{2\lambda_{\rm eff}}
=\frac{v_R^2}{2}.
\]

Every global minimum is gauge-equivalent to the desired coherent VEV. Hence no colour- or
charge-breaking configuration lies below it.

This is stronger than checking a neutral one-dimensional ray: it controls the entire 60-real-
dimensional \(\Delta_R\) field space.

## 7. Full \(\Delta_R\) Hessian

The decomposition after symmetry breaking is

\[
\Delta_R
\rightarrow
\begin{array}{lll}
(6,1)_{4/3}, &(6,1)_{1/3}, &(6,1)_{-2/3},\\
(3,1)_{2/3}, &(3,1)_{-1/3}, &(3,1)_{-4/3},\\
(1,1)_0, &(1,1)_{-1}, &(1,1)_{-2}.
\end{array}
\]

The \((3,1)_{2/3}\), \((1,1)_{-1}\), and the phase of \((1,1)_0\) supply the nine eaten
Goldstones.

The physical tree-level spectrum is:

| Multiplet | Real multiplicity | \(m^2/v_R^2\) |
|---|---:|---:|
| \((6,1)_{4/3}\) | 12 | \(2\kappa_4\) |
| \((6,1)_{1/3}\) | 12 | \(2\kappa_4+\kappa_R\) |
| \((6,1)_{-2/3}\) | 12 | \(2\kappa_4+2\kappa_R\) |
| \((3,1)_{-1/3}\) | 6 | \(\kappa_4+\kappa_R\) |
| \((3,1)_{-4/3}\) | 6 | \(\kappa_4+2\kappa_R\) |
| \((1,1)_{-2}\) | 2 | \(2\kappa_R\) |
| radial \((1,1)_0\) | 1 | \(2\lambda_{\rm eff}\) |
| Goldstones | 9 | \(0\) |

The count is

\[
9+12+12+12+6+6+2+1=60.
\]

With the complex bidoublets included, the benchmark has

\[
188-9=179
\]

physical real scalar modes at the Pati–Salam breaking scale.

The explicit \(60\times60\) \(\Delta_R\) Hessian and the complete block-diagonal
\(188\times188\) benchmark Hessian agree with the analytic spectrum to better than
\(10^{-10}\). The nine-dimensional nullspace agrees with the tangent space generated by broken
gauge transformations to a maximum residual of

\[
1.57\times10^{-16}.
\]

There is no accidental massless scalar.

## 8. Heavy-vector spectrum

The VEV breaks nine of the 21 Pati–Salam generators. The three \(SU(2)_L\) generators remain
massless at this stage. For the broken sector,

\[
\boxed{
m_X^2=\frac12g_4^2v_R^2
}
\]

for the six real vector-leptoquark directions,

\[
\boxed{
m_{W_R}^2=\frac12g_R^2v_R^2
}
\]

for the two charged right-handed vectors, and

\[
\boxed{
m_{Z_R}^2=
\left(
\frac32g_4^2+g_R^2
\right)v_R^2
}
\]

for the orthogonal neutral combination.

The massless neutral combination is hypercharge, with

\[
\boxed{
\frac1{g_Y^2}
=
\frac1{g_R^2}
+
\frac{2}{3g_4^2}.
}
\]

## 9. Numerical certificate

The dimensionless benchmark is

\[
\lambda_\Delta=2.0,
\qquad
\kappa_4=0.4,
\qquad
\kappa_R=0.3,
\]

so

\[
\lambda_{\rm eff}=1.1.
\]

It takes

\[
M_1^2=2.2v_R^2,
\qquad
M_{15}^2=3.3v_R^2,
\]

and orientation couplings

\[
g_4=0.570,
\qquad
g_R=0.540.
\]

The smallest physical scalar eigenvalue is

\[
0.6v_R^2,
\]

and all 179 physical scalar eigenvalues are positive.

The gauge masses are

\[
m_X^2=0.16245v_R^2,
\]

\[
m_{W_R}^2=0.14580v_R^2,
\]

\[
m_{Z_R}^2=0.77895v_R^2.
\]

The deterministic verifier also samples 20,000 normalized complex \(\Delta_R\) configurations and
finds no violation of the analytic moment-map bounds. This scan is diagnostic only; the global
minimum statement follows from the analytic moment-map inequalities.

## 10. What passed

\[
\boxed{
\begin{array}{c}
\text{complete gauge-only invariant count and coupling basis: PASS}\\
\text{bounded high-scale branch: PASS}\\
\text{desired global vacuum orbit: PASS}\\
\text{Goldstone count: PASS}\\
\text{tree-level scalar positivity: PASS}\\
\text{heavy-vector spectrum: PASS}
\end{array}
}
\]

## 11. What failed or remains non-unique

### Gauge-only predictivity

The bare `PS1` declaration has 138 scalar-potential parameters. It does not select a unique threshold
spectrum. Any one- or two-loop matching result requires a complete benchmark point, renormalisation
scheme, and running prescription.

### Stationary-orbit catalogue

The global inequality proves that no other stationary orbit can be a deeper vacuum, so the fatal
vacuum-selection test is closed. A complete Kirwan–Ness catalogue of every saddle and metastable
stationary orbit has not been enumerated and is not used as evidence for the global-minimum claim.

### Electroweak vacuum

The high-scale proof keeps both bidoublets inert. A realistic low-energy model must fine-tune one
linear combination of their SM doublets to remain light, generate the electroweak VEV, and retain a
positive heavy spectrum.

### Flavour and neutrinos

The \((15,2,2)\) Clebsch repair is algebraically sufficient, but no charged-fermion, CKM, PMNS, or
right-handed-neutrino fit has yet been performed with RG evolution and thresholds.

### Baryon violation and cosmology

Scalar diquark/leptoquark exchange, proton and nuclear stability, leptogenesis, monopoles, and any
parity/domain-wall branch remain open.

## 12. Gate update

| Gate | Score | Phase 2B status |
|---|---:|---|
| `ALG-01` | 1 | Complete for `PS1-MM`; bare `PS1` remains underdetermined |
| `ALG-03` | 2 | Local anomalies cancel generation by generation |
| `ALG-04` | 1 | Witten parity passes; faithful global quotient still to be frozen |
| `ALG-05` | 2 | High-scale scalar/gauge degree count closes |
| `PERT-01` | 2 | No tree-level tachyon in the declared high-scale domain |
| `REC-02` | 2 | Correct chiral SM representation recovery |
| `REC-03` | 1 | `PS0` failed; `PS1-MM` has no complete fermion fit |
| `NP-02` | 2 | Desired high-scale vacuum is a certified global minimum |
| `LAB-02` | 1 | Flavour, rare-process, and stability bounds not yet calculated |
| `COS-01` | 1 | Relic/defect and thermal-history calculation remains open |
| `REP-01` | 2 | Exact invariant count, Hessian, spectra, and tests are executable |

No aggregate score is formed.

## 13. Next decisive calculation

The next branch is `PS1-EW`:

1. construct the complete \(\Phi_1\)-\(\Phi_{15}\) quadratic mass matrix induced by the
   `PS1-MM` vacuum;
2. tune and identify one light SM Higgs doublet;
3. integrate out every other scalar and derive the matched two-Higgs/SM EFT;
4. run gauge, Yukawa, and scalar couplings with one- and two-loop threshold matching;
5. fit charged fermions, CKM, neutrinos, and PMNS;
6. calculate scalar-mediated flavour, proton/nuclear stability, and leptogenesis;
7. retain the TP-00 rule that any applicable fatal zero terminates the branch.

The high-scale vacuum problem is closed. The phenomenological matching problem is not.
