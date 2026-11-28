# TP-03 — Complete Pati–Salam benchmark

**Author:** Angus Muffatti  
**Project status:** **ACTIVE — Phase 3 (`PS1-EW`) complete**  
**Current version:** 0.4.0

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
\textbf{Certified high-scale }PS1\textbf{-MM vacuum: PASS (rescaled }\lambda_\Delta=0.08\textbf{).}\\
\textbf{Phase 3 }PS1\textbf{-EW electroweak matching, 2-loop RGEs, fermion/neutrino fit \& stability: PASS (branch- and }T_{\rm rh}<v_R\textbf{-conditional).}
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

### Phase 3 (`PS1-EW`)

Extending `PS1-MM` with all 16 gauge-invariant quadratic and \(\Delta_R^\dagger\Delta_R\) bidoublet portal operators yields a surjective bijection onto the \(4\times 4\) colour-singlet Higgs doublet mass matrix \(\mathcal{M}_H^2\) decoupled from the colour-octet (\(\Omega_{1,2}\)) and triplet-leptoquark (\(\Sigma_{7/6},\Sigma_{1/6}\)) blocks. Tuning one determinant condition isolates a single light SM Higgs doublet \(h\) with a full \(188\times 188\) real Hessian splitting into 9 Goldstones, 4 light SM Higgs modes, and 175 positive heavy physical modes (explicit EW fine-tuning \(\Delta_{\rm FT} = v_R^2/\mu_{\rm SM}^2\)).

Key Phase 3 outcomes across three benchmarks (`BM-LR` at \(5.08\times 10^{13}\text{ GeV}\), `BM-GUT` at \(2.15\times 10^{10}\text{ GeV}\), and `BM-LOW` at \(1.00\times 10^7\text{ GeV}\)):

- 1- and 2-loop gauge couplings stay perturbative to \(M_{\rm Pl}\) across \(v_R\in[10^{5.5},10^{16}]\text{ GeV}\), with exact 2-loop threshold-matched \(SO(10)\) triple unification at \(v_R = 2.15\times 10^{10}\text{ GeV}\), \(M_{\rm GUT}=5.13\times 10^{16}\text{ GeV}\);
- Phase 2B's \(\lambda_\Delta=2.0\) hits a 60-component \(\Delta_R\) scalar Landau pole at \(3.19\,v_R\); rescaling to \(\lambda_\Delta=0.08, \kappa_4=0.016, \kappa_R=0.012\) keeps all three benchmarks perturbative to \(M_{\rm Pl}\);
- `PS1-EW-min` (2 Dirac Yukawas \(Y_1, Y_{15}, f_R\)) **fails** for real Higgs-mixing ratios (\(\|f_R\|_2=6.54>\sqrt{4\pi}\)) and below \(v_R\simeq 7.7\times 10^{11}\text{ GeV}\), but **passes** all 18 flavour observables to \(<5\times 10^{-13}\) at `BM-LR` with a complex phase (\(\|Y_1\|_2=0.519, \|Y_{15}\|_2=0.576, \|f_R\|_2=0.0539\));
- `PS1-EW-gen` (all 4 gauge-allowed Dirac Yukawas + \(f_R\)) **passes** perturbatively to \(<10^{-12}\) across the full \(v_R\in[4.5\times 10^6,10^{16}]\text{ GeV}\) window;
- \(K_L\to\mu e\), \(B_s\to\mu e\), \(\mu\to e\gamma\), \(W_R/Z_R\), heavy-Higgs FCNCs, and \(\Delta B=1,2\) stability pass at all three benchmarks; \(\pi_2=\mathbb{Z}\) monopoles require \(T_{\rm rh}<v_R\), leaving an open monopole-safe hierarchical thermal leptogenesis window at `BM-LR` and `BM-GUT`.

## Reproduce

```bash
python -m pip install -r requirements.txt
make verify
```

This runs:

- exact multigraded invariant counting;
- the complete 138-channel invariant-basis construction;
- the explicit \(60\times60\) \(\Delta_R\) Hessian and complete \(188\times188\) benchmark Hessians (Phase 2B and Phase 3 `PS1-EW`);
- the gauge-boson mass matrix and Goldstone-orbit matching;
- 1- and 2-loop gauge/Yukawa/Higgs-quartic RGEs, Weinberg–Hall 1-loop thresholds, fermion/neutrino fits, and flavour/stability/relic audits;
- twenty unit tests (12 Phase 2B + 8 Phase 3).

## Key files

- `phase1_algebraic_baseline.md`
- `phase2a_breaking_spectrum.md`
- `phase2b_scalar_invariants_and_vacuum.md`
- `phase3_electroweak_and_fermion_matching.md`
- `invariant_basis_multidegrees.csv`
- `invariant_coupling_basis.csv`
- `results/invariant_coupling_basis.json`
- `branch_ledger.md`
- `acceptance_matrix.csv`
- `code/count_scalar_invariants.py`
- `code/generate_invariant_coupling_basis.py`
- `code/verify_phase2b_vacuum.py`
- `code/verify_phase3_ew_matching.py`
- `code/tests/test_phase2b.py`
- `code/tests/test_phase3_ew.py`
- `results/scalar_invariant_count.json`
- `results/phase2b_vacuum_spectrum.json`
- `results/phase3_ew_results.json`
- `results/phase3_ew_summary.md`

## Next decisive calculation

TP-03's concrete broken-generator, vector, scalar, and quark–lepton mixing spectra now feed directly into **TP-04** (`../tp-04-quark-lepton-rotations/`). Within TP-03, optional future extensions cover the full 138-coupling scalar RG flow, Boltzmann flavored leptogenesis/dark-matter completion, and the deferred parity-completed branch `PS1P`.

No aggregate TP-00 score is used. An applicable fatal zero terminates the claimed branch.
