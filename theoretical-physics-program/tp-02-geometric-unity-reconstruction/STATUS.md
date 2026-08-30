# TP-02 status

**Author:** Angus Muffatti  
**Version:** 0.5.0  
**Status date:** 31 August 2026  
**Project state:** **ACTIVE — source reconstruction complete; first explicit completion branch reaches a fatal propagation test**

## Completed phases

### Phase 1 — primary-source reconstruction

The official corpus, initial theory tuple, definition/claim ledgers and representation dimensions are frozen and executable.

### Phase 2 — sign-convention audit

The 2021 printed augmented torsion obeys

\[
T_-\bigl(g\tau_-(h)\bigr)
=
h^{-1}T_-(g)h
-
2h^{-1}d_{A_0}h,
\]

not the claimed equivariance law. The stabiliser-compatible repair is

\[
T_+
=
a+\varepsilon^{-1}d_{A_0}\varepsilon.
\]

### Phase 3A — first-order action covariance

The exact witness gives

\[
I_-^h-I_-=14,
\qquad
I_+^h-I_+=0.
\]

The literal branch is rejected in its claimed invariant form. The repaired branch survives the kinematic test.

### Phase 3B — explicit substitute Shiab

Draft eq. (9.3) is typeable as

\[
\operatorname{Sh}_\varepsilon:
\Omega^2(Y,\operatorname{ad}P_H)
\to
\Omega^{13}(Y,\operatorname{ad}P_H).
\]

The mixed Clifford contraction reproduces the Einstein tensor on algebraic Riemann curvature, with rank 105 and a 3080-dimensional Weyl kernel in fourteen dimensions.

The official corpus still does not define one full-adjoint Hessian, boundary domain, observation derivative or physical spectrum. That is the terminal source-faithful incompleteness result.

### Phase 4 — \(\mathsf R_+\)-EIN algebraic completion and symbol test

Completed:

- exact real \(128\times128\) \(\mathrm{Cl}(7,7)\) generators;
- explicit symmetric spinor form \(H\) with signature \((64,64)\);
- exact \(64+64\) chirality split;
- canonical
  \[
  \Phi_1=e^A\otimes\Gamma_A,
  \qquad
  \Phi_2=\tfrac12e^A\wedge e^B\otimes\Gamma_{AB};
  \]
- unique minimal full-adjoint Einstein extension
  \[
  \mathcal E_d(X)
  =
  [\Gamma^c,X_{cd}]
  +
  \frac14
  \left\{
  \left\{\Gamma^{cd},X_{cd}\right\},
  \Gamma_d
  \right\};
  \]
- exact full-adjoint closure residual \(0\);
- exact failure of the naive unsymmetrised extension, residual \(90\);
- split-signature principal-symbol theorem.

## Decisive Phase 4 verdict

\[
\boxed{
\begin{array}{c}
\text{Algebraic }\mathsf R_+\text{-EIN completion: PASS.}\\[1mm]
\text{Local propagation on full }(7,7)\text{ total space: FAIL.}
\end{array}
}
\]

For any timelike normal \(n\), \(n^\perp\) still contains a timelike tangential covector \(\xi\). The Einstein characteristic equation contains

\[
q(\xi+\lambda n)=-(1+\lambda^2),
\]

whose roots are \(\lambda=\pm i\). Therefore the geometric block is not hyperbolic with respect to any covector.

The local full-\(Y\) branch receives

\[
\boxed{\texttt{PERT-02}=0}
\]

and is rejected.

## Surviving branch

Only an explicitly observation-projected branch remains open:

\[
\mathsf R_+\text{-EIN-OBS4}.
\]

It must derive a dynamically preserved map

\[
\Pi_{\rm obs}:T^*Y\to T^*X
\]

with rank four and Lorentzian signature \((1,3)\) **before** propagation is defined.

## Next decisive calculation

1. Extract the observation-map differential and horizontal/vertical splitting from the source.
2. Construct every source-compatible rank-four characteristic projector.
3. Test gauge/BRST invariance and propagation of the projector constraint.
4. Derive the reduced principal symbol.
5. Count physical modes.
6. Stop if no invariant projector exists or if the reduced system does not have two graviton helicities.

No aggregate score is used. A fatal zero terminates only the branch to which it applies.

## Reproduction

```bash
make verify
```
