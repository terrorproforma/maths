# TP-03 — Complete Pati–Salam benchmark

**Author:** Angus Muffatti  
**Status:** **ACTIVE — Phase 1 complete; scalar-vacuum phase next**  
**Version:** 0.1.0  
**Date:** 31 August 2026

## Goal

Construct the smallest anomaly-free, symmetry-broken and phenomenologically testable model based on

\[
G_{\rm PS}=SU(4)_C\times SU(2)_L\times SU(2)_R,
\]

then test it against the frozen TP-00 gates.

## Phase 1 result

The chiral matter embedding

\[
F_L\sim(4,2,1),
\qquad
F_R^c\sim(\bar4,1,2)
\]

is anomaly-free generation by generation and reproduces one Standard Model family plus \(\nu^c\) under

\[
Y=T^3_R+\frac{B-L}{2}.
\]

The minimal one-bidoublet branch

\[
\Phi_1\sim(1,2,2)
\]

is nevertheless rejected because it enforces

\[
\boxed{
M_d=M_e,
\qquad
M_u=M_D^\nu.
}
\]

The surviving benchmark adds

\[
\Phi_{15}\sim(15,2,2),
\qquad
\Delta_R\sim(10,1,3).
\]

Its Dirac mass matrices are

\[
\begin{aligned}
M_d&=A_d+B_d,&
M_e&=A_d-3B_d,\\
M_u&=A_u+B_u,&
M_D^\nu&=A_u-3B_u,
\end{aligned}
\]

while

\[
M_R=f_Rv_R,
\qquad
m_\nu=-M_D^\nu M_R^{-1}(M_D^\nu)^T.
\]

The exact verifier confirms:

- Pati–Salam local anomaly cancellation;
- both Witten \(SU(2)\) anomaly cancellations;
- Standard Model hypercharges and anomaly cancellation;
- canonical \(B-L\) normalization;
- a neutral breaking direction in \(\Delta_R\);
- the one-bidoublet mass obstruction;
- exact matrix reconstruction with \((15,2,2)\);
- an illustrative one-loop parity-matching scale.

Under a one-light-doublet, threshold-free one-loop baseline,

\[
M_{\rm PS}\simeq5.07\times10^{13}\ {\rm GeV}.
\]

That number is not a fit and will be replaced by the threshold-corrected Phase 2 calculation.

## Branches

| Branch | Status |
|---|---|
| `PS0` — one bidoublet | **Rejected: `REC-03=0`** |
| `PS1` — add \((15,2,2)\) | **Active** |
| `PS1P` — parity-symmetric triplet branch | Queued |
| `PS-D` — doublet-breaking branch | Deferred |

## Next step

Build the complete renormalisable scalar potential for

\[
\Phi_1,\quad\Phi_{15},\quad\Delta_R,
\]

derive the vacuum, scalar/gauge spectrum, boundedness and threshold-corrected RG trajectory, then perform the fermion and neutrino fit.

## Reproduce

```bash
make verify
```

## Key files

- `phase1_algebraic_baseline.md`
- `model_branches_v0_1.md`
- `field_content_v0_1.yaml`
- `acceptance_matrix.csv`
- `code/verify_pati_salam_phase1.py`
- `results/phase1_algebraic_baseline.json`
- `references.bib`

## Epistemic rule

The original Pati–Salam mechanism is established prior art. The branch definitions, exact audit package and kill-test organization here are project work. No phenomenological success is claimed until the full scalar, threshold and likelihood calculations pass.
