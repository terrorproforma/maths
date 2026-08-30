# TP-03 Phase 1 — Algebraic Pati–Salam baseline and the minimal Yukawa obstruction

**Project:** TP-03 — Complete Pati–Salam benchmark  
**Author:** Angus Muffatti  
**Status:** **PHASE 1 COMPLETE**  
**Gauge group:**

\[
G_{\rm PS}=SU(4)_C\times SU(2)_L\times SU(2)_R.
\]

## 1. Executive result

The Pati–Salam fermion embedding passes its first algebraic kill tests:

\[
\boxed{
\text{local anomalies cancel generation by generation}
}
\]

\[
\boxed{
\text{both }SU(2)\text{ Witten anomalies cancel generation by generation}
}
\]

and the breaking rule

\[
Y=T^3_R+\frac{B-L}{2}
\]

reproduces one complete Standard Model family plus a right-handed neutrino.

However, the genuinely minimal renormalisable Dirac-mass sector with only one bidoublet

\[
\Phi_1\sim(1,2,2)
\]

fails immediately:

\[
\boxed{
M_d=M_e,
\qquad
M_u=M_D^\nu.
}
\]

The first relation is incompatible with the observed three-family charged-fermion spectrum. Therefore the one-bidoublet branch `PS0` is rejected before a numerical fit.

The minimal algebraic repair is to add

\[
\Phi_{15}\sim(15,2,2).
\]

Then

\[
\begin{aligned}
M_d&=A_d+B_d,\\
M_e&=A_d-3B_d,\\
M_u&=A_u+B_u,\\
M_D^\nu&=A_u-3B_u,
\end{aligned}
\]

and any pair of quark/lepton mass matrices can be reconstructed algebraically through

\[
A_d=\frac{3M_d+M_e}{4},
\qquad
B_d=\frac{M_d-M_e}{4},
\]

with the analogous up/neutrino formulas.

This defines the surviving Phase 2 candidate `PS1`.

## 2. Matter convention

Use an all-left-handed basis:

\[
F_L\sim(4,2,1),
\qquad
F_R^c\sim(\bar4,1,2).
\]

For one generation, the \(SU(4)^3\) anomaly is

\[
2A(4)+2A(\bar4)=2-2=0.
\]

The number of \(SU(2)_L\) doublets is

\[
\dim 4=4,
\]

and the number of \(SU(2)_R\) doublets is also four. Both are even, so both global \(SU(2)\) anomalies vanish.

This cancellation is generation-by-generation and therefore does not explain why there are exactly three generations.

## 3. Standard Model decomposition

Under

\[
SU(4)_C\rightarrow SU(3)_C\times U(1)_{B-L},
\]

\[
4\rightarrow(3,1/3)\oplus(1,-1),
\]

\[
\bar4\rightarrow(\bar3,-1/3)\oplus(1,+1).
\]

With

\[
Y=T^3_R+\frac{B-L}{2},
\]

the left multiplet gives

\[
F_L\rightarrow
Q_L:(3,2)_{1/6}
\oplus
L_L:(1,2)_{-1/2}.
\]

The right-conjugate multiplet gives

\[
F_R^c\rightarrow
u^c:(1,1)_0
\oplus
e^c:(1,1)_1
\oplus
u^c:(1,1)_0
\oplus
e^c:(1,1)_1.
\]

The exact verifier independently checks

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

and the low-energy Witten anomaly. All vanish per generation.

## 4. Hypercharge normalization

Define

\[
Q_{BL}=\frac{B-L}{2}
=
\operatorname{diag}
\left(
\frac16,\frac16,\frac16,-\frac12
\right).
\]

The canonically normalized \(SU(4)\) generator is

\[
T^{15}
=
\sqrt{\frac32}\,Q_{BL}
=
\frac{1}{2\sqrt6}
\operatorname{diag}(1,1,1,-3),
\]

because

\[
\operatorname{tr}Q_{BL}^2=\frac13,
\qquad
\operatorname{tr}(T^{15})^2=\frac12.
\]

Therefore

\[
g_{BL}=\sqrt{\frac32}\,g_4
\]

for the charge \(Q_{BL}\), and hypercharge matching is

\[
\boxed{
\frac1{g_Y^2}
=
\frac1{g_R^2}
+
\frac{2}{3g_4^2}.
}
\]

If a parity condition imposes \(g_R=g_L\) at the breaking scale, this becomes a direct relation among the measured Standard Model couplings after threshold and renormalisation-group evolution are specified.

## 5. Breaking field

The Phase 1 Majorana branch uses

\[
\Delta_R\sim(10,1,3)
\]

in the all-left-handed convention.

Under \(SU(3)_C\times U(1)_{B-L}\),

\[
10\rightarrow
(6,2/3)\oplus(3,-2/3)\oplus(1,-2).
\]

The color singlet with

\[
B-L=-2,
\qquad
T^3_R=+1
\]

has

\[
Y=+1+\frac{-2}{2}=0.
\]

Its vacuum expectation value can therefore break

\[
SU(4)_C\times SU(2)_R
\longrightarrow
SU(3)_C\times U(1)_Y
\]

and generate

\[
M_R=f_Rv_R.
\]

The type-I seesaw is then

\[
m_\nu
=
-M_D^\nu M_R^{-1}(M_D^\nu)^T.
\]

A left triplet and type-II contribution are not included in the Phase 1 benchmark. They remain a separate parity-symmetric branch.

## 6. The one-bidoublet obstruction

With only

\[
\Phi_1\sim(1,2,2),
\]

the renormalisable Dirac Yukawa term has one common \(SU(4)\)-singlet contraction. After electroweak breaking, the down-quark and charged-lepton matrices share the same Yukawa matrix and vacuum coefficient:

\[
M_d=v_dY_1,
\qquad
M_e=v_dY_1.
\]

Likewise,

\[
M_u=v_uY_1,
\qquad
M_D^\nu=v_uY_1.
\]

No flavour rotation changes the equality of singular-value spectra. Renormalisation-group running can perturb relations between scales, but it cannot turn this branch into a controlled realistic three-family fit without additional fields or operators.

Thus:

\[
\boxed{
\texttt{PS0: REC-03=0}
}
\]

for a realistic charged-fermion benchmark.

## 7. Minimal Yukawa repair

Add

\[
\Phi_{15}\sim(15,2,2)
\]

with its \(SU(4)\) direction aligned with

\[
\operatorname{diag}(1,1,1,-3).
\]

The relative quark/lepton Clebsch is then \(+1:-3\). Write

\[
A_{u,d}=Y_1v^{u,d}_1,
\qquad
B_{u,d}=Y_{15}v^{u,d}_{15}.
\]

The mass matrices become

\[
\begin{aligned}
M_d&=A_d+B_d,\\
M_e&=A_d-3B_d,\\
M_u&=A_u+B_u,\\
M_D^\nu&=A_u-3B_u.
\end{aligned}
\]

The exact inverse is

\[
\begin{aligned}
A_d&=\frac{3M_d+M_e}{4},
&
B_d&=\frac{M_d-M_e}{4},\\
A_u&=\frac{3M_u+M_D^\nu}{4},
&
B_u&=\frac{M_u-M_D^\nu}{4}.
\end{aligned}
\]

The verifier reconstructs arbitrary exact rational \(3\times3\) matrix pairs with zero residual.

This proves algebraic sufficiency only. It does not prove that one scalar potential generates the required four electroweak vacuum components naturally or that the resulting flavour structure passes all limits.

## 8. One-loop matching baseline

For orientation, the verifier solves the parity matching condition using:

- one-loop Standard Model running;
- one light Higgs doublet;
- no intermediate thresholds;
- \(g_R=g_L\) and \(g_4=g_3\) at \(M_{\rm PS}\);
- declared approximate inputs at \(M_Z\).

The result is

\[
\boxed{
M_{\rm PS}^{(1\ell)}
\simeq
5.07\times10^{13}\ {\rm GeV}.
}
\]

At that scale, the illustrative couplings are approximately

\[
g_L\simeq0.539,
\qquad
g_4\simeq0.570.
\]

This is **not** a fitted prediction. Extra light doublets, scalar threshold splittings, two-loop running and finite matching corrections can move the scale substantially. It is a transparent baseline for Phase 2 rather than a phenomenological conclusion.

## 9. Branch ledger

| Branch | Field content | Verdict |
|---|---|---|
| `PS0` | \(F_L+F_R^c+\Phi_1+\Delta_R\) | **Rejected** by exact fermion-mass relations |
| `PS1` | `PS0` plus \(\Phi_{15}\) | Algebraically viable; scalar dynamics and fits open |
| `PS1P` | `PS1` plus parity partner \(\Delta_L\) and discrete parity | Open; type-I+II seesaw and domain-wall issues |
| `PS-D` | doublet-breaking alternative | Deferred; distinct neutrino and defect structure |

## 10. Next decisive calculation

For `PS1`, construct the complete renormalisable scalar potential for

\[
\Phi_1,
\qquad
\Phi_{15},
\qquad
\Delta_R,
\]

then:

1. classify all independent invariants;
2. solve the stationary equations;
3. prove boundedness in the relevant field directions;
4. identify the unbroken gauge group;
5. compute the scalar and gauge-boson mass matrices;
6. verify the absence of tachyons and unwanted Goldstones;
7. run one- and two-loop gauge/Yukawa/scalar couplings with threshold matching;
8. fit charged fermions and neutrinos;
9. calculate flavour, scalar-leptoquark and baryon-violation constraints;
10. determine monopole and possible domain-wall cosmology.

No collider or cosmological claim should be made before the vacuum and threshold spectrum are explicit.

## 11. Reproduction

```bash
make verify
```

The Phase 1 code uses exact rational arithmetic for group theory and anomalies. Only the explicitly labelled one-loop scale uses floating-point arithmetic.
