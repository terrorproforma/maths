# TP-03 status

**Author:** Angus Muffatti  
**Version:** 0.4.1  
**Status date:** 29 November 2026  
**Project state:** **ACTIVE — Phase 3 audited — partial/revised with sharp obstructions recorded**

## Phase ledger

### Phase 1 — algebra and Yukawa structure

- generation-by-generation local anomaly cancellation: **PASS**;
- both \(SU(2)\) Witten parities: **PASS**;
- Standard Model hypercharges: **PASS**;
- `PS0` one-bidoublet mass relations: **FATAL FAIL**;
- \((15,2,2)\) Clebsch repair: **PASS algebraically**.

### Phase 2A — breaking orbit

- unique full-SM-singlet high-scale direction: **IDENTIFIED**;
- unbroken group \(SU(3)_C\times SU(2)_L\times U(1)_Y\): **PASS**;
- broken generators/eaten Goldstones: **9**;
- heavy-vector spectrum: **PASS**.

### Phase 2B — scalar invariants and vacuum

- complete complex-field invariant count:
  \[
  N_2=7,\quad N_3=0,\quad N_4=131;
  \]
- complete 138-element irreducible coupling-channel basis: **PASS**;
- gauge-only `PS1` predictivity: **FAIL — 138 scalar parameters**;
- named `PS1-MM` branch: **DEFINED**;
- global boundedness and desired-orbit theorem (\(\Delta_R\)-only): **PASS**;
- full \(188\times188\) high-scale scalar Hessian: **PASS**;
- accidental exact Goldstones: **NONE**;
- physical tachyons: **NONE**;
- deeper colour/charge-breaking minimum: **EXCLUDED IN `PS1-MM`**;
- Phase 2B reproducibility suite: **12/12 tests pass**.

### Phase 3 — `PS1-EW` electroweak matching, RG running, fermion/neutrino fit and stability audit (post-referee revision)

- explicit gauge-invariant \(\Phi_1\)–\(\Phi_{15}\)–\(\Delta_R\) portal potential: **17 operators (25 real parameters)** mapping via a **rank-16 surjective linear map (9-dim kernel)** onto \(\mathcal{M}_H^2\) (NOT a bijection); gauge invariance `< 1e-14`; all \(\Delta_R^2\) portals vanish identically on \(\langle\Delta_R\rangle\);
- full \(188\times 188\) `PS1-EW` one-light-Higgs Hessian at the unbroken EW origin (\(\langle\Phi\rangle=0\)): **PARTIAL / HEAVY-SPECTRUM SCOPED (`PERT-01`)** — 9 Goldstones, 4 light SM Higgs modes matching target \(u\), 175 positive heavy modes; \(-\mu_{\rm SM}^2\) gives expected tachyonic EWSB curvature and full EW-broken vacuum verification remains open;
- tree-level global Higgs+\(\Delta_R\) stability (`NP-02`): **FAIL / OPEN AT TREE LEVEL** at the matched negative-portal `BM-LR` point (\(\lambda_{h\Delta} = -1.648 < 0\), \(\lambda_H^{\rm SM}(v_R) = -0.01122 < 0\)), where the physical coherent ray \(r = -\lambda_{h\Delta} x/(2\lambda_{\rm eff}) = 49.95\,x > 0\) gives \(V_4 = \lambda_H^{\rm SM}(v_R) x^2 < 0\) (unbounded below); stabilizing requires \(\lambda_H^{\rm SM}(v_R) > 0\), positive-portal copositivity, or radiative effective-potential analysis;
- electroweak hierarchy fine-tuning: **EXPLICIT** (\(\Delta_{\rm FT} = v_R^2/\mu_{\rm SM}^2 \sim 10^{10}\text{–}3.3\times 10^{23}\));
- gauge-only 2-loop PS RGEs + Weinberg–Hall 1-loop thresholds: **PARTIAL (`PERT-05`)** — perturbative to \(M_{\rm Pl}\) across \(v_R\in[10^{5.5},10^{16}]\text{ GeV}\), approximate \(SO(10)\) triple crossing at \(v_R = 7.32\times 10^9\text{ GeV}\), \(M_{\rm GUT} = 8.15\times 10^{16}\text{ GeV}\) (2-loop UV Yukawa traces and \(M_{\rm GUT}\) parent thresholds omitted);
- corrected 60-real-component \(\Delta_R\) pure-self-coupling Landau pole (\(136\lambda_\Delta^2 - 36\lambda_\Delta\kappa_4 - 16\lambda_\Delta\kappa_R\)): **OBSTRUCTION** at Phase 2B's \(\lambda_\Delta = 2.0\) (formal pole at \(1.787\,v_R\)); rescaled to \(\lambda_\Delta = 0.03, \kappa_4 = 0.006, \kappa_R = 0.0045\) (\(\lambda_{\rm eff}=0.0165\)), staying below the pure-self-coupling Planck starting cap (`0.0417` at `BM-LOW`) across all 3 benchmarks, while the full coupled 138-parameter scalar RGE system remains open;
- fermion/neutrino existence fits (`REC-03`): **PARTIAL (existence/interpolation)** — `PS1-EW-min` has 30 real Yukawa parameters after \(U(3)_L\times U(3)_R\) basis removal vs 18 observables. Earlier false exclusions are **retracted**: perturbative `PS1-EW-min` witnesses exist at `BM-LR` with **real** ratios (\(\|f_R\|_2 = 0.197\)), with **complex** ratios (\(\|f_R\|_2 = 0.0380\)), and refitted at \(v_R = 6.0\times 10^{11}\text{ GeV}\) (\(\|f_R\|_2 = 2.80 < \sqrt{4\pi}\)). `PS1-EW-gen` (with corrected down-type tilde signs and determinant \(D=|\alpha_u|^2-|\alpha_d|^2\), verified by direct \(2\times 2\) contraction) passes across all 3 benchmarks (`max ||Y||_2` = `1.19–2.03`), and all seesaw fits verify charged-lepton-basis PMNS round-trip recovery to `< 1e-12`;
- flavour & baryon stability (`LAB-02`): **PARTIAL** — corrected Valencia–Willenbrock \(K_L\to\mu e\) aligned floor \(M_X \gtrsim 2.06\times 10^6\text{ GeV}\) (\(v_R \gtrsim 3.78\times 10^6\text{ GeV}\)) and MEG II \(\mu\to e\gamma < 1.5\times 10^{-13}\) pass; pure PS perturbative baryon number (\(3B+L\)) forbids \(d=6\) proton decay (while gauged \(B-L\) is broken by \(\Delta(B-L)=2\)); \(n\text{--}\bar{n}\) (with actual sextet masses \(0.11\text{–}0.14\,v_R\)), heavy-Higgs FCNC, and \(W_R/Z_R\) remain preliminary order-of-magnitude checks;
- topological relics & leptogenesis (`COS-01`): **OPEN / PARTIAL** — both \(\pi_2=\mathbb{Z}\) monopoles and \(\pi_1=\mathbb{Z}_2\) cosmic strings (from disconnected stabilizer) require \(T_{\rm rh} < v_R\); no \(D\)-parity domain walls; vanilla \(N_1\)-dominated thermal leptogenesis at `BM-GUT` falls \(\sim 85\times\) short of observed \(\eta_B\); Boltzmann transport and dark matter remain open;
- combined reproducibility suite: **22/22 tests pass** (12 Phase 2B + 10 Phase 3).

## Current frontier

Phase 3 has been audited and revised with all 5 fatal bugs fixed and 6 scope/overclaim issues corrected honestly under TP-00. Concrete broken-generator, vector, scalar, and quark–lepton mixing inputs remain available for **TP-04** (`tp-04-quark-lepton-rotations/`), while closing TP-03's open/failed gates requires addressing the items below.

## Remaining open items / obstructions to resolve

- resolve the tree-level negative-portal Higgs+\(\Delta_R\) unbounded-below obstruction at `BM-LR` (`NP-02`: positive-portal parameter branch or 1-loop Coleman–Weinberg / RG-improved effective potential) and verify the full EW-broken vacuum (`PERT-01`);
- complete the full coupled 138-parameter 1-loop scalar quartic RGE system and 2-loop UV Yukawa gauge traces above \(v_R\) (`PERT-05`), plus explicit \(SO(10)\) parent thresholds if unified;
- replace preliminary \(n\text{--}\bar{n}\), heavy-Higgs FCNC, and \(W_R/Z_R\) order-of-magnitude checks with full SMEFT Wilson-coefficient matching (`LAB-02`);
- perform flavored/resonant Boltzmann leptogenesis transport and dark-matter completion alongside \(\pi_2=\mathbb{Z}\) monopole / \(\pi_1=\mathbb{Z}_2\) string cosmology (`COS-01`);
- parity-completed `PS1P` (\(\Delta_L\) + Type-II seesaw + domain-wall audit).
