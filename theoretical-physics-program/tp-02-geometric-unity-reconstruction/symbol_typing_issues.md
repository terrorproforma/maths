# Symbol and typing issues

This ledger prevents silent correction of the primary source.

| Source symbol/term | Project alias | Issue | Rule |
|---|---|---|---|
| `X` | `X` | Four-manifold, initially without metric. | Preserve. |
| `Y`, sometimes `U` | `Y` | Einsteinian total space `Met(X)`, dimension 14. | The 2021 draft's `Y` controls. |
| `ג` | `gimel` | Observation/metric section and embedding. | Never freeze silently. |
| `ℵג` | `aleph_gimel` | Observation-induced connection. | Keep functional dependence on `gimel`. |
| `C` | `C` | Chimeric bundle. | Type as rank-14 real metric bundle. |
| `H` | `H_finite`, `mathcal H` | Overloaded for the finite group and gauge group. | Split aliases. |
| `G` | `mathcal G` | Inhomogeneous gauge group. | Do not confuse with Newton's constant. |
| `N` | `N` | `Omega^1(Y,ad P_H)`. | Preserve. |
| `ε` | `varepsilon` | Group-valued field. | Use `varepsilon`. |
| PDF glyph rendered as `$` | `a` | Adjoint-valued one-form. | Alias mechanically. |
| `A0` | `A0[gimel]` | Distinguished connection. | Track observation variation. |
| `τ` in Oxford source | `tau_plus` | Plus-sign second component. | Version separately. |
| `τ` in 2021 draft | `tau_minus` | Minus-sign stabiliser. | 2021 branch controls written definitions. |
| `T=a-ε^-1d_A0ε` | `T_minus` | Fails covariance with `tau_minus`. | Preserve as literal failed branch. |
| `T=a+ε^-1d_A0ε` | `T_plus` | Stabiliser-compatible repair. | Label `R_PLUS`. |
| `}·` | `Sh` | Shiab family. | Freeze degree, invariant tensors and each product. |
| `Φ_i` | `Phi_i` | Invariant pure-trace tensor basis. | Subscript is form degree in the 2021 draft; specify normalisation. |
| Square brackets in Shiab | `B_j` | May denote commutator or `i`-Jordan product. | Do not use one uniform bracket by typography alone. |
| `*` | `star_g` | Hodge star in signature `(7,7)`. | Track degree and `*^2` sign. |
| `Υ_omega` | `Upsilon_omega` | First-order equation. | Domain/codomain depends on completion. |
| `d_A^*` | `D_A_star` | Formal adjoint. | Declare pairing, metric and boundary domain. |
| `Spin(7,7)-832` | `RS_832` | Dimension label, not unique representation identifier. | Prove branching separately. |

## Source-internal instability warnings

1. Draft footnote 7 explicitly warns of multiple sign conventions in section 6.
2. The Oxford source uses `tau_plus`; the 2021 draft uses `tau_minus`.
3. The proof of the printed torsion lemma changes the effective sign needed for cancellation.
4. The source says the preferred Bianchi-selected Shiab cannot presently be located.
5. Eq. (8.1) permits commutator or anticommutator products; eq. (9.3) does not typographically mark each choice.
6. A Clifford decomposition is flagged as needing verification.
7. The deformation-complex diagram is caveated as possibly inconsistent.
8. The lecture acknowledges unresolved Lorentzian-signature and 14D propagation problems.

## Project convention after Phase 3B

On geometric spin curvature, the Einstein requirement selects:

- vector–bivector commutator for Ricci;
- bivector anticommutator/Jordan trace for scalar curvature;
- scalar multiplication in the final term.

This selection is not automatically extended to every `U(64,64)` adjoint direction.
