# TP-03 — Complete Pati–Salam benchmark

**Author:** Angus Muffatti  
**Project status:** **ACTIVE — Phase 3 audited — partial/revised with sharp obstructions recorded**  
**Current version:** 0.4.1

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
\textbf{Certified high-scale }PS1\textbf{-MM }\Delta_R\textbf{-only vacuum: PASS (rescaled }\lambda_\Delta=0.03\textbf{; coupled scalar RGEs open).}\\
\textbf{Phase 3 }PS1\textbf{-EW (post-referee audit): PARTIAL / REVISED — NP-02 FAIL at negative-portal BM-LR;}\\
\textbf{PERT-01, PERT-05, REC-03, LAB-02 PARTIAL; COS-01 OPEN / PARTIAL.}
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

the desired SM-preserving coherent orbit is the certified global minimum of \(V_\Delta\). The explicit full \(188\times188\) real Hessian has:

- nine and only nine Goldstones;
- 51 positive physical \(\Delta_R\) modes;
- eight positive \(\Phi_1\) spectator modes;
- 120 positive \(\Phi_{15}\) spectator modes;
- no deeper colour- or charge-breaking vacuum in `PS1-MM`.

### Phase 3 (`PS1-EW`, post-referee revision)

Extending `PS1-MM` with all **17** gauge-invariant quadratic and \(\Delta_R^\dagger\Delta_R\) bidoublet portal operators (**25 real parameters**) yields a **rank-16 surjective linear map (9-dimensional kernel)** onto the \(4\times 4\) colour-singlet Higgs doublet mass matrix \(\mathcal{M}_H^2\) decoupled from the colour-octet (\(\Omega_{1,2}\)) and triplet-leptoquark (\(\Sigma_{7/6},\Sigma_{1/6}\)) blocks. Tuning one determinant condition isolates a single light SM Higgs doublet \(h\) at the unbroken EW origin (\(\langle\Phi\rangle=0\)) with a full \(188\times 188\) real Hessian splitting into 9 Goldstones, 4 light SM Higgs modes, and 175 positive heavy physical modes (explicit EW fine-tuning \(\Delta_{\rm FT} = v_R^2/\mu_{\rm SM}^2\); full EW-broken vacuum verification remains open under `PERT-01`).

Key revised Phase 3 outcomes and honest obstructions across three benchmarks (`BM-LR` at \(5.08\times 10^{13}\text{ GeV}\), `BM-GUT` at \(7.32\times 10^9\text{ GeV}\), and `BM-LOW` at \(1.00\times 10^7\text{ GeV}\)):

- **Tree-level Higgs+\(\Delta_R\) stability obstruction (`NP-02` = FAIL):** At the matched negative-portal `BM-LR` criticality point (\(\lambda_{h\Delta} = -1.648 < 0\), \(\lambda_H^{\rm SM}(v_R) = -0.01122 < 0\)), the physical coherent ray \(r = -\lambda_{h\Delta} x/(2\lambda_{\rm eff}) = 49.95\,x > 0\) gives \(V_4(x,r) = \lambda_H^{\rm SM}(v_R) x^2 < 0\) — **unbounded below at tree level**;
- **Gauge-only 2-loop RGEs & corrected \(136\lambda_\Delta^2\) Landau pole (`PERT-05` = PARTIAL):** Gauge couplings stay perturbative to \(M_{\rm Pl}\) across \(v_R\in[10^{5.5},10^{16}]\text{ GeV}\) (2-loop UV Yukawa traces omitted), with an approximate \(SO(10)\) triple crossing at \(v_R = 7.32\times 10^9\text{ GeV}\), \(M_{\rm GUT}=8.15\times 10^{16}\text{ GeV}\) (no \(M_{\rm GUT}\) parent thresholds). Phase 2B's \(\lambda_\Delta=2.0\) hits a pure-self-coupling \(136\lambda_\Delta^2\) pole at \(1.787\,v_R\); rescaling to \(\lambda_\Delta=0.03, \kappa_4=0.006, \kappa_R=0.0045\) (\(\lambda_{\rm eff}=0.0165\)) stays below the pure-self-coupling Planck starting cap (`0.0417` at `BM-LOW`), while the full coupled 138-parameter scalar RGE system remains open;
- **Fermion/neutrino existence witnesses (`REC-03` = PARTIAL):** Earlier false exclusions of real ratios and \(v_R < 7.7\times 10^{11}\text{ GeV}\) in `PS1-EW-min` are retracted: perturbative witnesses pass at `BM-LR` for **both** real (\(\|f_R\|_2=0.197\)) and complex (\(\|f_R\|_2=0.0380\)) ratios and at refitted \(v_R=6.0\times 10^{11}\text{ GeV}\) (\(\|f_R\|_2=2.80 < \sqrt{4\pi}\)). `PS1-EW-min` has 30 real Yukawa parameters vs 18 observables (existence/interpolation test, not a constrained prediction). `PS1-EW-gen` (with corrected down-type tilde signs, \(D=|\alpha_u|^2-|\alpha_d|^2\), and direct \(2\times 2\) contraction) passes across all three benchmarks with charged-lepton-basis PMNS round-trip verified to `< 1e-12`;
- **Flavour, baryon stability (`LAB-02` = PARTIAL) & cosmology (`COS-01` = OPEN / PARTIAL):** Corrected Valencia–Willenbrock \(K_L\to\mu e\) (\(1/(32\pi)\)) sets the aligned floor \(M_X\gtrsim 2.06\times 10^6\text{ GeV}\) (\(v_R\gtrsim 3.78\times 10^6\text{ GeV}\)) and MEG II \(\mu\to e\gamma < 1.5\times 10^{-13}\) passes; \(n\text{--}\bar{n}\) (using actual sextet masses \(0.11\text{–}0.14\,v_R\)), heavy-Higgs FCNC, and \(W_R/Z_R\) are preliminary order-of-magnitude checks; \(\pi_2=\mathbb{Z}\) monopoles and \(\pi_1=\mathbb{Z}_2\) cosmic strings require \(T_{\rm rh}<v_R\); vanilla \(N_1\)-dominated thermal leptogenesis at `BM-GUT` falls \(\sim 85\times\) short of \(\eta_B^{\rm obs}\).

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
- 1- and gauge-only 2-loop RGEs, Weinberg–Hall 1-loop thresholds, corrected \(136\lambda_\Delta^2\) Landau-pole audit, tree-level negative-portal stability audit, fermion/neutrino existence witnesses with direct tensor contraction and PMNS round-trip checks, and flavour/stability/relic audits;
- twenty-two unit tests (12 Phase 2B + 10 Phase 3).

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

Close the Phase 3 obstructions recorded in `acceptance_matrix.csv`: resolve `NP-02` via a positive-portal parameter choice or radiative effective-potential analysis, verify the full EW-broken vacuum (`PERT-01`), compute the coupled scalar RGE system and UV Yukawa 2-loop gauge traces (`PERT-05`), upgrade preliminary flavour/baryon checks to full SMEFT matching (`LAB-02`), and complete Boltzmann flavored/resonant leptogenesis + dark matter (`COS-01`). Concrete broken-generator, vector, scalar, and mixing structures also feed into **TP-04** (`../tp-04-quark-lepton-rotations/`).

No aggregate TP-00 score is used. An applicable fatal zero terminates the claimed branch.
