# TP-03 branch ledger

| Branch | Scalar / Yukawa convention | Status | Reason |
|---|---|---|---|
| `PS0` | Complex \((1,2,2)\) plus \((10,1,3)\) | **REJECTED** | Tree-level relations \(M_d=M_e\) and \(M_u=M_D^\nu\). |
| `PS1` | `PS0` plus complex \((15,2,2)\), gauge symmetry only | **UNDERDETERMINED** | The general scalar potential has 7 quadratic and 131 quartic real parameters. |
| `PS1-MM` | `PS1` with the declared moment-map high-scale potential | **PHASE 2B PASS (QUARTIC RESCALED IN PHASE 3)** | Bounded global SM-preserving vacuum, 9 Goldstones, no physical scalar tachyon; Phase 2B's \(\lambda_\Delta=2.0\) hits a 60-component scalar Landau pole at \(3.2\,v_R\), repaired by rescaling to \(\lambda_\Delta=0.08\). |
| `PS1-EW-min` | `PS1-MM` + bidoublet portals + minimal 2 Dirac Yukawas \((Y_1, Y_{15}, f_R)\) | **PHASE 3 CONDITIONAL PASS (\(v_R \gtrsim 7.7\times 10^{11}\text{ GeV}\), COMPLEX PHASE REQUIRED)** | Real Higgs-mixing ratios fail \(f_R\) perturbativity (\(\|f_R\|_2=6.54>\sqrt{4\pi}\)). With a complex phase, passes all fermion/CKM/PMNS/flavour/stability/leptogenesis gates at `BM-LR` (\(5.08\times 10^{13}\text{ GeV}\)); fails perturbativity at `BM-GUT` and `BM-LOW`. |
| `PS1-EW-gen` | `PS1-MM` + bidoublet portals + all 4 gauge-allowed Dirac Yukawas \((Y_1, \tilde{Y}_1, Y_{15}, \tilde{Y}_{15}, f_R)\) | **PHASE 3 PASS ACROSS \(v_R\in[4.5\times 10^6,10^{16}]\text{ GeV}\)** | Passes 188x188 Higgs matching, 2-loop gauge perturbativity to \(M_{\rm Pl}\), all 18 flavour observables to \(<10^{-12}\), and flavour/baryon gates at `BM-LR`, `BM-GUT` (exact 2-loop \(SO(10)\) unification), and `BM-LOW`; subject to explicit EW hierarchy fine-tuning and \(T_{\rm rh}<v_R\) monopole dilution. |
| `PS1P` | Parity-completed branch including a left triplet \(\Delta_L(10,3,1)\) | **DEFERRED** | Different vacuum, Type-II seesaw, and \(D\)-parity domain-wall structure. |
| `PS-D` | Doublet-breaking alternative | **DEFERRED** | Different neutrino and topological-defect structure. |

No result from one branch is silently transferred to another.
