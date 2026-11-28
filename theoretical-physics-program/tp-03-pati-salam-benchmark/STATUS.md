# TP-03 status

**Author:** Angus Muffatti  
**Version:** 0.4.0  
**Status date:** 29 November 2026  
**Project state:** **ACTIVE — Phase 3 (`PS1-EW`) complete; benchmark viable with explicit branch/tuning boundaries**

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
- global boundedness and desired-orbit theorem: **PASS**;
- full \(188\times188\) high-scale scalar Hessian: **PASS**;
- accidental exact Goldstones: **NONE**;
- physical tachyons: **NONE**;
- deeper colour/charge-breaking minimum: **EXCLUDED IN `PS1-MM`**;
- Phase 2B reproducibility suite: **12/12 tests pass**.

### Phase 3 — `PS1-EW` electroweak matching, RG running, fermion/neutrino fit and stability audit

- explicit gauge-invariant \(\Phi_1\)–\(\Phi_{15}\)–\(\Delta_R\) portal potential and \(4\times 4\) \(\mathcal{M}_H^2\): **PASS** (gauge invariance `< 1e-14`; all \(\Delta_R^2\) portals vanish identically on \(\langle\Delta_R\rangle\));
- full \(188\times 188\) `PS1-EW` one-light-Higgs Hessian: **PASS** (9 Goldstones, 4 light SM Higgs modes matching target \(u\), 175 positive heavy modes);
- electroweak hierarchy fine-tuning: **EXPLICIT** (\(\Delta_{\rm FT} = v_R^2/\mu_{\rm SM}^2 \sim 10^{10}\text{–}10^{23}\));
- 1- and 2-loop gauge RGEs + Weinberg–Hall 1-loop thresholds: **PASS** (perturbative to \(M_{\rm Pl}\) across \(v_R\in[10^{5.5},10^{16}]\text{ GeV}\); 2-loop \(SO(10)\) triple unification at \(v_R = 2.15\times 10^{10}\text{ GeV}\), \(M_{\rm GUT} = 5.13\times 10^{16}\text{ GeV}\));
- 60-component \(\Delta_R\) scalar Landau pole: **OBSTRUCTION** at Phase 2B's \(\lambda_\Delta = 2.0\) (\(\Lambda_{\rm LP} = 3.19\,v_R\)); **PASS** after rescaling to \(\lambda_\Delta = 0.08, \kappa_4 = 0.016, \kappa_R = 0.012\);
- 2-loop SM Higgs quartic stability: \(\mu_{\rm inst}^{(2\ell)} = 9.04\times 10^9\text{ GeV}\); UV-stabilized above \(\mu_{\rm inst}\) by radial-\(\Delta_R\) portal shift \(|\lambda_{h\Delta}| > 0.044\) (`BM-LR`);
- `PS1-EW-min` (2 Dirac Yukawas \(Y_1, Y_{15}, f_R\)): **FAIL** for real Higgs-mixing ratios (\(\|f_R\|_2 = 6.54 > \sqrt{4\pi}\) at `BM-LR`); **PASS** with complex relative phase at `BM-LR` (\(\|Y_1\|_2=0.519, \|Y_{15}\|_2=0.576, \|f_R\|_2=0.0539\), fit err \(<5\times 10^{-13}\)); **FAIL** below \(v_R \simeq 7.7\times 10^{11}\text{ GeV}\) (`BM-GUT`, `BM-LOW`);
- `PS1-EW-gen` (all 4 gauge-allowed Dirac Yukawas + \(f_R\)): **PASS** across all three benchmarks (`BM-LR`, `BM-GUT`, `BM-LOW`) to \(<10^{-12}\) with \(\max\|Y\|_2 < 0.84\);
- flavour & EWPO gates (\(K_L\to\mu e\), \(B_s\to\mu e\), \(\mu\to e\gamma\), \(W_R/Z_R\), heavy-Higgs FCNC): **PASS** for \(v_R \ge 4.49\times 10^6\text{ GeV}\);
- baryon-number stability: \(d=6\) \(\Delta B=1\) proton decay **FORBIDDEN** in pure PS; \(n\text{--}\bar{n}\) **FORBIDDEN** in `PS1-MM` by \(U(1)_\Delta\) and passes \(\tau_{n\bar{n}}>4.7\times 10^8\text{ s}\) even for \(\lambda_{\Delta 4}=\mathcal{O}(1)\);
- topological relics & leptogenesis: **CONDITIONAL** on \(T_{\rm rh} < v_R\) for \(\pi_2=\mathbb{Z}\) monopole inflation; no \(D\)-parity domain walls; monopole-safe hierarchical thermal leptogenesis open at `BM-LR` and `BM-GUT`, closed at `BM-LOW`;
- combined reproducibility suite: **20/20 tests pass** (12 Phase 2B + 8 Phase 3).

## Current frontier

TP-03's core Pati–Salam benchmark (`PS1-EW-min` at `BM-LR` and `PS1-EW-gen` across `BM-LR`/`BM-GUT`/`BM-LOW`) is phenomenologically viable under the stated fine-tuning and inflationary-reheating conditions, and ready to feed concrete broken-generator and scalar/vector inputs into **TP-04** (`tp-04-quark-lepton-rotations/`).

## Remaining open items (optional Phase 4 / future extensions)

- full 138-coupling 1-loop scalar quartic RG flow above \(v_R\);
- full Boltzmann transport for flavored thermal leptogenesis and dark-matter completion;
- parity-completed `PS1P` (\(\Delta_L\) + Type-II seesaw + domain-wall audit) and explicit \(SO(10)\) UV completion above \(M_{\rm GUT}\).
