# TP-02 — Independent Reconstruction of Geometric Unity

**Author:** Angus Muffatti  
**Status:** **FROZEN AT v0.6.0 — terminal source-audit outcome**  
**Source freeze:** 31 August 2026

## Result

The official primary corpus contains a serious geometric programme, but it does not define a complete healthy successor theory that can be independently executed.

\[
\boxed{
\begin{array}{c}
\text{Literal printed covariance: FAIL.}\\
\text{Repaired Clifford/Einstein algebra: PASS.}\\
\text{Local full-}(7,7)\text{ propagation: FAIL.}\\
\text{Four-dimensional dynamics by pullback alone: FAIL.}
\end{array}
}
\]

## Main exact results

1. **Sign inconsistency**
   \[
   T_-(g\tau_-(h))
   =
   h^{-1}T_-(g)h
   -
   2h^{-1}d_{A_0}h.
   \]

2. **Action defect**
   \[
   I_-^h-I_-=14,
   \qquad
   I_+^h-I_+=0.
   \]

3. **Einstein contraction**
   \[
   [\Gamma^c,F_{cd}]
   +
   \frac14
   \left\{
   \{\Gamma^{ab},F_{ab}\},
   \Gamma_d
   \right\}
   =
   \left(R_{db}-\frac12Rg_{db}\right)\Gamma^b.
   \]

4. **Exact Clifford completion**
   \[
   \mathrm{Cl}(7,7)
   \cong
   \operatorname{Mat}_{128}(\mathbb R),
   \qquad
   \operatorname{sig}H=(64,64).
   \]

5. **Full-adjoint closure**
   \[
   \max_d\|\mathcal E_d^\sharp+\mathcal E_d\|_\infty=0.
   \]

6. **Split-signature obstruction**
   \[
   q(\xi+\lambda n)=-(1+\lambda^2)
   \]
   gives complex characteristic roots. The local full-\(Y\) branch fails `PERT-02`.

7. **Pullback obstruction**
   For \(f=(z^a)^2\),
   \[
   \iota^*f=0,
   \qquad
   \iota^*(L_Yf)=2g^{aa}\neq0.
   \]
   Pullback of field values does not close the ambient second-order dynamics.

## Interpretation

The source's observation map and bundle splitting are kinematically meaningful. They do not remove normal derivatives from the ambient equations.

A viable theory would need new normal-jet constraints, localization, a tangential/degenerate principal symbol, or an induced effective action. None is fixed by the primary corpus.

Such a construction would be independent model building, not a source-faithful reconstruction.

## Key files

- `STATUS.md`
- `sign_convention_audit.md`
- `phase3_first_order_variational_audit.md`
- `phase3b_shiab_reconstruction.md`
- `phase4_rplus_ein_algebraic_completion.md`
- `phase5_observation_pullback_obstruction.md`
- `completion_branches_v0_6.md`
- `code/`
- `results/`
- `acceptance_matrix.csv`

## Reproduce

```bash
make verify
```

## Next programme step

Proceed to `../tp-03-pati-salam-benchmark/`.
