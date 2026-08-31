# TP-03 — Complete Pati–Salam benchmark

**Author:** Angus Muffatti  
**Project status:** **ACTIVE — Phase 2B complete; `PS1-EW` next**  
**Current version:** 0.3.0

## Research question

Can a complete, anomaly-free and phenomenologically viable model based on

\[
SU(4)_C\times SU(2)_L\times SU(2)_R
\]

recover the Standard Model, generate neutrino masses, preserve matter stability and produce at least
one discriminating observable?

## Current result

\[
\boxed{
\begin{array}{c}
\textbf{Chiral anomaly cancellation: PASS.}\\
\textbf{Strict one-bidoublet Yukawa branch: FAIL.}\\
\textbf{General gauge-only scalar potential: 138 real parameters.}\\
\textbf{Certified high-scale }PS1\textbf{-MM vacuum: PASS.}\\
\textbf{Complete low-energy fit: OPEN.}
\end{array}
}
\]

### Phase 1

For

\[
F_L\sim(4,2,1),
\qquad
F_R^c\sim(\bar4,1,2),
\]

local anomalies and both \(SU(2)\) Witten parities cancel generation by generation. The hypercharge
embedding

\[
Y=T_R^3+\frac{B-L}{2}
\]

reproduces one Standard Model family plus \(\nu^c\).

The strict branch with only

\[
\Phi_1\sim(1,2,2)
\]

forces

\[
M_d=M_e,
\qquad
M_u=M_D^\nu,
\]

and is rejected. Adding

\[
\Phi_{15}\sim(15,2,2)
\]

provides the \(+1:-3\) quark–lepton Clebsch and is algebraically sufficient to escape those relations.

### Phase 2A

The neutral component of

\[
\Delta_R\sim(10,1,3)
\]

breaks

\[
SU(4)_C\times SU(2)_R
\rightarrow
SU(3)_C\times U(1)_Y.
\]

The heavy-vector masses are

\[
m_X^2=\frac12g_4^2v_R^2,
\qquad
m_{W_R}^2=\frac12g_R^2v_R^2,
\]

\[
m_{Z_R}^2=
\left(
\frac32g_4^2+g_R^2
\right)v_R^2.
\]

### Phase 2B

The scalar fields are treated as independent complex multiplets:

\[
\Phi_1(1,2,2),
\qquad
\Phi_{15}(15,2,2),
\qquad
\Delta_R(10,1,3).
\]

Exact multigraded Molien–Weyl integration gives

\[
\boxed{
7\ \text{quadratic}
+
0\ \text{cubic}
+
131\ \text{quartic}
=
138
}
\]

independent real scalar-potential parameters. An exact Gelfand–Tsetlin/character decomposition
then constructs all 138 invariant coupling channels in a fixed left-associated basis; the coupling
paths are stored in JSON and CSV rather than disguised as 138 arbitrary trace expressions.

Therefore `PS1` as a representation list is not one predictive scalar theory. The named branch
`PS1-MM` uses

\[
V_\Delta
=
-m_\Delta^2r+\lambda_\Delta r^2
-\kappa_4\sum_A(\mu_4^A)^2
-\kappa_R\sum_i(\mu_R^i)^2.
\]

For

\[
\kappa_4>0,\qquad
\kappa_R>0,\qquad
\lambda_\Delta-\frac32\kappa_4-\kappa_R>0,
\]

the desired SM-preserving coherent orbit is the certified global minimum. The explicit full \(188\times188\) real Hessian has:

- nine and only nine Goldstones;
- 51 positive physical \(\Delta_R\) modes;
- eight positive \(\Phi_1\) spectator modes;
- 120 positive \(\Phi_{15}\) spectator modes;
- no deeper colour- or charge-breaking vacuum.

## Reproduce

```bash
python -m pip install -r requirements.txt
make verify
```

This runs:

- exact multigraded invariant counting;
- the explicit \(60\times60\) \(\Delta_R\) Hessian;
- the gauge-boson mass matrix;
- Goldstone-orbit matching;
- deterministic moment-map diagnostics;
- eight unit tests.

## Key files

- `phase1_algebraic_baseline.md`
- `phase2a_breaking_spectrum.md`
- `phase2b_scalar_invariants_and_vacuum.md`
- `invariant_basis_multidegrees.csv`
- `invariant_coupling_basis.csv`
- `results/invariant_coupling_basis.json`
- `branch_ledger.md`
- `acceptance_matrix.csv`
- `code/count_scalar_invariants.py`
- `code/verify_phase2b_vacuum.py`
- `results/scalar_invariant_count.json`
- `results/phase2b_vacuum_spectrum.json`

## Next decisive calculation

The next branch is `PS1-EW`:

1. derive the complete bidoublet mass/mixing matrix induced by the high-scale vacuum;
2. retain one light Standard Model Higgs doublet;
3. integrate out the remaining scalar thresholds;
4. run one- and two-loop matching;
5. fit charged fermions, CKM, neutrinos and PMNS;
6. calculate flavour, proton/nuclear stability, leptogenesis and topological relics.

No aggregate TP-00 score is used. An applicable fatal zero terminates the claimed branch.
