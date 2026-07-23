# Independent review checklist

## Algebraic map

- [ ] Recompute the Jacobian determinant of the supplied three-variable map.
- [ ] Recompute all three collisions exactly over `Q`.
- [ ] Check the source and target normalization giving `G` with identity linear part and determinant one.
- [ ] Verify the hidden identities `B = y + 3rC` and `A = r - r^2B + 2r^3C`.

## Weighted Horner suspension

- [ ] Check the homogeneous decomposition `G_i = X_i + sum_j K_{i,j}`.
- [ ] Verify every line of the telescoping identity.
- [ ] Verify that the auxiliary-output Jacobian is unit triangular.
- [ ] Confirm that `det(I+sJN)=1` implies `(JN)^14=0` over the polynomial ring.
- [ ] Confirm the one-variable homogenization and the block-power argument giving `(JH)^15=0`.
- [ ] Substitute the three lifted rational points into the explicit 15-variable map.

## Formal inverse

- [ ] Derive the inverse-slice formula independently.
- [ ] Apply Lagrange inversion to `A = r + 2Cr^3`.
- [ ] Confirm the coefficient and its sign for several values of `m`.
- [ ] Check that the homogenizing exponent is exactly `15m` and the total degree is `18m+1`.

## Tree translation

- [ ] Match the factorial normalization of `H` to the convention in Bisi et al.
- [ ] Confirm that the coefficient formula uses ordinary inverse coefficients and the factor `(7!)^(3m)`.
- [ ] Confirm that Lemma 3.3 applies with dimension `n=15` and path length `p=15`.
- [ ] Confirm that the resulting vector is integer-valued.
- [ ] Confirm that a nonzero total sum separates the constant vector from the shuffle span.

## Scope and history

- [ ] Keep the theorem fixed at `(d,p)=(7,15)`.
- [ ] Avoid implying a result for all `p >= 15` without a separate proof.
- [ ] Distinguish Singer's binary conjecture from its all-degree extension.
- [ ] Audit priority claims against the public record as of the submission date.
