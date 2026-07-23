# Validation report

## SSUF certificate

The following checks are implemented in `code/verify_dgg.py`.

1. The aggregate fractional flow has source divergence `-40`, terminal divergences `(15,10,15)`, and zero divergence at `u,v,w`.
2. All source-terminal paths are reconstructed by depth-first search from the nine-arc graph.
3. Each terminal has exactly two paths, giving exactly eight unsplittable routings.
4. The fractional cost is exactly `58`.
5. Exactly four routings satisfy `y_a <= x_a+15` on every arc.
6. The minimum cost among those four routings is exactly `60`.
7. The three two-cheap-path routings have unit excess on `s->u`, `u->v`, and `v->w`, respectively.

No floating-point operations or optimization solver are used.

## Chairman certificate

The following checks are implemented in `code/verify_chairman.py`.

1. Every one of the 15 fractional columns sums exactly to one and has support two.
2. Every weight is strictly positive and the largest weight is exactly one.
3. A fresh detector row can lose at most `12/1000` before its block.
4. If `J_k` is not sent to `A_k`, assigning `K_k` away from `A_k` gives discrepancy at least `25/24-12/1000 > 1`.
5. After the forced `K_k` choice, either assignment of `L_k` gives discrepancy at least `6047/6000 > 1`.
6. Therefore all five decision columns are forced, and the accumulator discrepancy is at least `619/600 > 1`.

The proof permits every column to be assigned to any of the eleven rows; no support-preservation assumption is used.

## Human audit points

Before submission, an independent expert should verify:

- that the manuscript quotes each external conjecture with exactly the quantifiers and conventions used in its source;
- that no later paper, preprint, erratum, or private communication has already resolved either statement;
- that the journal's authorship and AI-disclosure policies are followed;
- that the compiled figures and equations are visually inspected page by page;
- that the title and abstract do not overstate collateral consequences.

## Current limitations

This report records an internal exact audit, not peer review. The GitHub Actions workflow is the authoritative build check for the committed sources. Its status should be green before the branch is merged or a manuscript is circulated.
