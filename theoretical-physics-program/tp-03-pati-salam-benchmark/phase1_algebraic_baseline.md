# TP-03 Phase 1 — Algebraic Pati–Salam baseline and minimal Yukawa obstruction

**Author:** Angus Muffatti  
**Status:** **PHASE 1 COMPLETE**

## Terminal result

For

\[
G_{\rm PS}=SU(4)_C\times SU(2)_L\times SU(2)_R,
\]

with all-left-handed matter

\[
F_L\sim(4,2,1),
\qquad
F_R^c\sim(\bar4,1,2),
\]

the chiral embedding is anomaly-free generation by generation and reproduces one Standard Model family plus \(\nu^c\).

The strict one-bidoublet branch

\[
\texttt{PS0}=F_L+F_R^c+\Phi_1(1,2,2)+\Delta_R(10,1,3)
\]

is nevertheless rejected because

\[
\boxed{M_d=M_e,\qquad M_u=M_D^\nu.}
\]

The minimal algebraic repair is

\[
\texttt{PS1}=\texttt{PS0}+\Phi_{15}(15,2,2).
\]

It yields

\[
\begin{aligned}
M_d&=A_d+B_d,& M_e&=A_d-3B_d,\\
M_u&=A_u+B_u,& M_D^\nu&=A_u-3B_u,
\end{aligned}
\]

with exact inverses

\[
\begin{aligned}
A_d&=\frac{3M_d+M_e}{4},& B_d&=\frac{M_d-M_e}{4},\\
A_u&=\frac{3M_u+M_D^\nu}{4},& B_u&=\frac{M_u-M_D^\nu}{4}.
\end{aligned}
\]

The verifier reconstructs arbitrary exact rational \(3\times3\) matrix pairs with zero residual. This is algebraic sufficiency only; scalar dynamics and the physical fit remain open.

## 1. Anomalies

The \(SU(4)^3\) anomaly per generation is

\[
2A(4)+2A(\bar4)=2-2=0.
\]

Each \(SU(2)\) factor sees four left-handed doublets per generation:

\[
N_{2L}=N_{2R}=4\equiv0\pmod2.
\]

Thus both Witten anomalies vanish. This does not determine the number of generations because the cancellation is already true for one.

## 2. Standard Model recovery

Under

\[
SU(4)_C\rightarrow SU(3)_C\times U(1)_{B-L},
\]

\[
4\rightarrow(3,1/3)\oplus(1,-1),
\qquad
\bar4\rightarrow(\bar3,-1/3)\oplus(1,+1).
\]

Using

\[
Y=T^3_R+\frac{B-L}{2},
\]

one obtains

\[
F_L\rightarrow
Q_L:(3,2)_{1/6}
\oplus
L_L:(1,2)_{-1/2},
\]

and

\[
F_R^c\rightarrow
u^c:(\bar3,1)_{-2/3}
\oplus
d^c:(\bar3,1)_{1/3}
\oplus
\nu^c:(1,1)_0
\oplus
e^c:(1,1)_1.
\]

The exact code checks this complete decomposition and verifies

\[
[SU(3)]^3,
\quad
[SU(3)]^2U(1)_Y,
\quad
[SU(2)]^2U(1)_Y,
\quad
[U(1)_Y]^3,
\quad
\mathrm{grav}^2U(1)_Y,
\]

as well as the low-energy Witten parity. All vanish per generation.

## 3. Hypercharge normalization

For

\[
Q_{BL}=\frac{B-L}{2}
=\operatorname{diag}\left(\frac16,\frac16,\frac16,-\frac12\right),
\]

\[
\operatorname{tr}Q_{BL}^2=\frac13.
\]

The canonically normalized generator is

\[
T^{15}=\sqrt{\frac32}\,Q_{BL}
=\frac1{2\sqrt6}\operatorname{diag}(1,1,1,-3),
\]

so

\[
\operatorname{tr}(T^{15})^2=\frac12.
\]

Consequently

\[
g_{BL}=\sqrt{\frac32}\,g_4
\]

for the charge \((B-L)/2\), and

\[
\boxed{
\frac1{g_Y^2}
=
\frac1{g_R^2}
+
\frac{2}{3g_4^2}.
}
\]

## 4. Symmetry-breaking field

The Phase 1 triplet branch uses

\[
\Delta_R\sim(10,1,3).
\]

Its \(SU(4)\) decomposition is

\[
10\rightarrow
(6,2/3)\oplus(3,-2/3)\oplus(1,-2).
\]

The colour singlet with

\[
B-L=-2,
\qquad
T^3_R=+1
\]

has \(Y=0\). Its VEV can therefore break

\[
SU(4)_C\times SU(2)_R
\rightarrow
SU(3)_C\times U(1)_Y
\]

and generate

\[
M_R=f_Rv_R,
\qquad
m_\nu=-M_D^\nu M_R^{-1}(M_D^\nu)^T.
\]

## 5. Why PS0 fails

With only \(\Phi_1=(1,2,2)\), the renormalisable Dirac Yukawa interaction has one \(SU(4)\)-singlet contraction. Therefore

\[
M_d=v_dY_1=M_e,
\qquad
M_u=v_uY_1=M_D^\nu.
\]

The equality is matrix-level and hence enforces equal singular-value spectra. A realistic three-family charged-fermion benchmark cannot satisfy it. Thus

\[
\boxed{\texttt{PS0: REC-03=0}.}
\]

## 6. Why \((15,2,2)\) is the minimal repair

Align the adjoint bidoublet along

\[
\operatorname{diag}(1,1,1,-3).
\]

Quarks receive Clebsch \(+1\), leptons \(-3\). The exact inverse formulas above show that arbitrary quark/lepton matrix pairs can then be represented when the relevant VEVs are nonzero.

This does not yet prove:

- a viable scalar potential;
- the required VEV hierarchy;
- acceptable flavour-changing effects;
- proton stability;
- threshold-corrected coupling evolution;
- a successful neutrino and baryogenesis history.

## 7. Illustrative one-loop scale

Using one-loop Standard Model running, one light Higgs doublet, no thresholds, and the parity condition

\[
g_R(M_{\rm PS})=g_L(M_{\rm PS}),
\qquad
g_4(M_{\rm PS})=g_3(M_{\rm PS}),
\]

the declared baseline inputs give

\[
\boxed{M_{\rm PS}^{(1\ell)}\simeq5.07\times10^{13}\ {\rm GeV}.}
\]

This is not a fitted prediction. Extra light doublets, scalar thresholds, two-loop running and finite matching corrections may move it substantially.

## 8. Next decisive calculation

Construct the complete renormalisable scalar potential for

\[
\Phi_1,
\qquad
\Phi_{15},
\qquad
\Delta_R,
\]

then derive:

1. the invariant operator basis;
2. stationary points and the unbroken group;
3. boundedness;
4. scalar and gauge-boson Hessians;
5. Goldstone counting;
6. threshold spectrum and RG flow;
7. charged-fermion and neutrino fits;
8. flavour, baryon-violation and defect constraints.

## 9. Reproduction

```bash
make verify
```

All group-theory and matrix checks use exact rational arithmetic. Only the explicitly labelled one-loop scale uses floating-point arithmetic.
