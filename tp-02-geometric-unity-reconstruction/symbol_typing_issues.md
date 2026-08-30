# Symbol and typing issues

This ledger prevents silent correction of the primary source.

| Source symbol/term | Project alias | Issue | Rule |
|---|---|---|---|
| `X` | `X` | Four-manifold, initially without metric. | Preserve. |
| `Y`, sometimes `U` in the lecture | `Y` | Einsteinian total space `Met(X)`, dimension 14 for `dim X=4`. | The 2021 draft's `Y` controls. |
| `ג` | `gimel` | Observation/metric section and embedding map. | Use `gimel`; never replace with a fixed background metric silently. |
| `ℵג` | `aleph_gimel` | Observation-induced connection. | Keep functional dependence on `gimel`. |
| `C` | `C` | Chimeric bundle, not a generic complex number/charge conjugation. | Type as a rank-14 real metric vector bundle. |
| `H` | `H_finite`, `mathcal H` | Overloaded for `U(64,64)` and its gauge-transformation group. | Split aliases explicitly. |
| `G` | `mathcal G` | Inhomogeneous infinite-dimensional gauge group. | Do not confuse with Newton's constant or a finite structure group. |
| `N` | `N` | `Omega^1(Y,ad P_H)` additive/affine model space. | Preserve. |
| `ε` | `varepsilon` | Group-valued field/gauge transformation; source also uses epsilon tensors elsewhere. | Use `varepsilon` for the field. |
| Source glyph rendered as `$` | `a` or `dollar_field` | Adjoint-valued one-form. The PDF glyph is unstable in plain text. | Alias mechanically and record every substitution. |
| `ω=(β,χ)` | `omega` | Unified boson/fermion assemblage. | Preserve source decomposition. |
| `ν` | `nu` | Spinor zero-form. | Preserve. |
| `ζ` | `zeta` | Spinor one-form; physical spin decomposition requires constraints. | Do not call it a healthy Rarita-Schwinger field before analysis. |
| `A0` | `A0[gimel]` | Distinguished connection induced by observation. | Track variation with `gimel`. |
| `}·` / ship-in-a-bottle glyph | `Sh_omega` | Shiab operator family. | Freeze a specific branch before varying the action. |
| `Υ_omega` | `Upsilon_omega` | First-order equation/swervature assemblage. | Domain/codomain must be reconstructed. |
| `d_A^*` | `D_A_star` | Formal adjoint depends on metric, pairing and boundary conditions. | Never use without declaring all three. |
| `Spin(7,7)-832` | `RS_832` | Chiral gamma-traceless vector-spinor representation by dimension. | Dimension is not a unique representation label. |

## Source-internal instability warnings

1. A Clifford-algebra decomposition is accompanied by a footnote saying it comes from an old file and should be checked.
2. The mixed deformation-complex diagram is marked as possibly inconsistent.
3. The lecture acknowledges an unresolved sign issue in moving from Euclidean to Minkowski signature.
4. The lecture acknowledges that 14-dimensional propagation must be shown to look four-dimensional.
5. The draft changes notation between sections and between the lecture and manuscript.

TP-02 treats these as explicit reconstruction tasks, not as reasons to invent missing definitions.
