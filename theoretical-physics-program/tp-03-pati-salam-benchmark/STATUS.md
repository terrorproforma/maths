# TP-03 status

**Version:** 0.1.0  
**Status:** **Phase 1 complete / PS1 active**

## Completed

\[
G_{\rm PS}=SU(4)_C\times SU(2)_L\times SU(2)_R
\]

with

\[
F_L=(4,2,1),
\qquad
F_R^c=(\bar4,1,2).
\]

Exact results:

1. \(SU(4)^3\) anomaly cancels per generation.
2. Both \(SU(2)\) Witten anomalies cancel per generation.
3. \(Y=T^3_R+(B-L)/2\) yields the complete Standard Model family plus \(\nu^c\).
4. All low-energy Standard Model local anomalies cancel.
5. \(T^{15}=\sqrt{3/2}\,(B-L)/2\) has canonical trace normalization.
6. \(\Delta_R=(10,1,3)\) contains a neutral \((1,-2,T^3_R=+1)\) breaking direction.
7. One \((1,2,2)\) bidoublet forces
   \[
   M_d=M_e,\qquad M_u=M_D^\nu.
   \]
8. Adding \((15,2,2)\) gives the \(+1:-3\) Clebsch and reconstructs arbitrary quark/lepton matrix pairs exactly.
9. An illustrative one-loop parity-matching baseline gives
   \[
   M_{\rm PS}\simeq5.07\times10^{13}\ {\rm GeV}.
   \]

## Gate result

- `ALG-03`: **2 — PASS**
- `ALG-04` Witten parity component: **2 — PASS**
- `REC-02`: **2 — PASS at representation level**
- `REC-03` for `PS0`: **0 — FATAL FAIL**
- `PS1`: remains open; no aggregate score.

## Current branch

\[
\boxed{
\texttt{PS1}=
F_L+F_R^c+\Phi_1(1,2,2)+\Phi_{15}(15,2,2)+\Delta_R(10,1,3).
}
\]

## Next decisive calculation

Construct and solve the complete renormalisable scalar potential. Required outputs:

- invariant operator basis;
- desired symmetry-breaking stationary point;
- Hessian and Goldstone count;
- boundedness;
- gauge-boson masses;
- scalar thresholds;
- one/two-loop RG;
- realistic fermion and neutrino fit;
- flavour, baryon-violation and defect constraints.
