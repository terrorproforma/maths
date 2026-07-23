# Status and claim boundary

**Date:** 23 July 2026  
**Status:** research draft; exact algebraic checks encoded; independent expert review still required.

## Claimed theorem

For the fixed pair

```text
d = 7, p = 15,
```

and for every integer `m >= 1`, let `k = 3m`. The constant function on the planar 7-ary Catalan trees with `k` internal vertices does not belong to the span of the length-15 shuffle-class indicators.

The dual witness is defined by the average tree weights of an explicit homogeneous map `Phi = I - H` in 15 variables. It satisfies

```text
(JH)^15 = 0,
M^T w_m = 0,
1^T w_m = (7!)^(3m) (-1)^m 2^m binom(3m+1,m) != 0.
```

## Explicitly not claimed

- The repository does **not** claim failure for every `p >= 15`.
- It does not claim minimality of `d = 7`, `p = 15`, dimension 15, or degree 7.
- It does not settle Singer's original binary-tree conjecture.
- It does not enumerate the enormous vector `w_m`; it gives a finite closed definition and proves its two required linear identities.
- It does not claim historical priority beyond the dated repository record.

## Verification layers

1. SymPy checks the original and normalized Jacobian determinants and all displayed collisions.
2. The generic Horner builder reconstructs the displayed 15-variable map from the normalized 3-variable map.
3. Telescoping identities certify `det(I+s JN)=1`; Cayley-Hamilton then gives `(JN)^14=0`.
4. Homogenization gives `(JH)^15=0`; exact integer specializations are checked as regression tests.
5. Lagrange inversion gives the coefficient formula, cross-checked by truncated formal series.
6. The final shuffle separation uses the published shuffle lemma and tree-inverse formula.

## Review gate

Do not present this as established mathematics until reviewers have independently checked:

- the weighted Horner suspension theorem;
- the inverse-slice identity;
- the normalization conventions in the tree-inverse formula;
- the application of the length-15 shuffle lemma;
- the provenance and authorship statement.
