# TP-02 status

**Author:** Angus Muffatti  
**Version:** 0.3.0  
**Status date:** 30 August 2026  
**Project state:** **ACTIVE — repaired branch survives; literal printed first-order branch rejected in its claimed invariant form**

## Phase ledger

### Phase 1 — primary-source reconstruction

Completed:

- frozen official source manifest;
- typed initial theory tuple;
- source-definition and claim ledgers;
- exact dimension bookkeeping;
- explicit separation of source claims from independent checks.

### Phase 2 — inhomogeneous gauge-group sign audit

Completed:

\[
T_-\bigl(g\tau_-(h)\bigr)
=
h^{-1}T_-(g)h-2h^{-1}d_{A_0}h.
\]

The printed augmented torsion is not equivariant under the printed tilted stabilizer. The source's semidirect product, affine right action, tilted-map homomorphism, and stabilization of \(A_0\) independently pass. A reversible repair was frozen:

\[
T_+=a+\varepsilon^{-1}d_{A_0}\varepsilon.
\]

### Phase 3A — first-order action covariance and universal variation

Completed:

- exact finite action-level counterexample for the literal branch;
- exact action invariance for the repaired branch under the same test;
- infinitesimal Noether-defect derivation;
- exact formula for the variation of \(K=\varepsilon^{-1}d_{A_0}\varepsilon\);
- explicit retention of \(A_0=A_0[\gimel]\);
- source-completeness ledger for the remaining Shiab variation.

Terminal Phase 3A result:

\[
\boxed{
\begin{array}{c}
\text{Literal printed branch: fails the claimed tilted-gauge-invariant action form.}\\[1mm]
\text{Repaired plus-sign branch: passes the kinematic covariance test.}
\end{array}}
\]

The exact matrix witness gives

\[
I_-^{h}-I_-=14,
\qquad
I_+^{h}-I_+=0.
\]

## Current gate status

- Literal branch `ALG-02`: **0** for the claimed covariant first-order action, absent an additional compensator or modified transformation law.
- Repaired branch `ALG-02`: **1**, because the complete deformation/BRST complex is still unproved.
- `ALG-05`, `ALG-06`, `PERT-01` through `PERT-05`, and recovery gates remain unresolved pending a fully typed Hessian and low-energy map.

No aggregate score is used.

## Next decisive calculation — Phase 3B

1. Type the explicit substitute Shiab displayed in draft eq. (9.3) as a map between declared bundles.
2. Derive its Fréchet derivative with respect to both the unified field and observation field.
3. Derive \(D A_0[\delta\gimel]\) for the source's observation-induced connection.
4. Compute the complete repaired first variation \(\delta I_+\), including measure, pairing, and boundary terms.
5. Choose the simplest source-compatible background and compute \(\delta^2I_+\).
6. Extract the principal symbol and determine whether the proposed deformation sequence composes to zero.
7. Count gauge and propagating modes before attempting Standard Model matching.

If the primary source does not uniquely type one of the required maps, the output will be a precise source-incompleteness theorem rather than an invented completion.

## Reproduction

```bash
python code/verify_representation_dimensions.py --root .
python code/verify_inhomogeneous_group_signs.py --root .
python code/verify_first_order_action_covariance.py --root .
python -m unittest discover -s code/tests -v
```
