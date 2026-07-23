# Fixed-parameter subtree-shuffling counterexample

This folder contains a research draft, derivations, executable symbolic checks, and a journal-style manuscript for the following fixed-parameter claim:

> For `d = 7`, `p = 15`, and every `m >= 1`, the constant function on the set of planar 7-ary Catalan trees with `k = 3m` internal vertices is not in the span of the length-15 shuffle-class indicators.

Equivalently, if `M_{7,15,3m}` is the tree-by-shuffle-class incidence matrix, the construction defines an exact integer vector `w_m` with

```text
M_{7,15,3m}^T w_m = 0,
1^T w_m = (7!)^(3m) (-1)^m 2^m binom(3m+1,m) != 0.
```

The construction starts with a three-dimensional noninjective Keller map, normalizes it to identity linear part and determinant one, applies a weighted Horner suspension to obtain a degree-seven homogeneous Keller map in fifteen variables with `(JH)^15 = 0`, and extracts an infinite family of nonzero inverse coefficients by Lagrange inversion. The shuffle lemma and tree-inverse formula then turn those coefficients into the separating vectors.

## Status

This is a **research draft for independent mathematical review**, not a peer-reviewed result. The repository deliberately states only the fixed pair `(d,p)=(7,15)`. It does not claim the same construction works for every `p >= 15`.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m shuffle_counterexample.verify --strict
pytest -q
make paper
```

The GitHub Actions workflow runs the verifier and tests, compiles the LaTeX manuscript, uploads the PDF as an artifact, and commits the compiled PDF back to the review branch.

## Layout

- `paper/` — manuscript source and compiled PDF.
- `derivation/` — equation-by-equation derivations separated from the paper exposition.
- `src/shuffle_counterexample/` — exact SymPy construction and certificate code.
- `tests/` — regression tests for the Jacobians, collisions, suspension, and coefficient formula.
- `STATUS.md` — precise claim boundary and open checks.
- `PROVENANCE.md` — origin of the map and contribution boundaries.
- `REVIEW_CHECKLIST.md` — an audit guide for algebraists and combinatorialists.

## Importance

The subtree-shuffling conjecture was introduced in a January 2023 preprint and appeared in final journal form in January 2026. It was designed as an unlabelled-tree route toward the Jacobian conjecture. The certificate here replaces the immediate logical contrapositive arising from a noninjective Keller map with a concrete fixed pair, a fixed nilpotency index, and an exact dual witness formula. It also explains why the published asymptotic approximation theorem can remain valid: the separator vanishes on every 15-perfect tree and is supported only on the exponentially rare exceptional trees.
