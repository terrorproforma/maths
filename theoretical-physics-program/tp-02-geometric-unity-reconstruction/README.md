# TP-02 — Independent Reconstruction of Geometric Unity

**Author:** Angus Muffatti  
**Project status:** **ACTIVE — source audit complete; observation-projected completion is the only surviving physical branch**  
**Source freeze:** 31 August 2026  
**Current version:** 0.5.0

## Research question

Can the official Geometric Unity primary material be converted into a complete, independently reproducible theory and pass the frozen TP-00 successor gates?

## Current verdict

\[
\boxed{
\begin{array}{c}
\textbf{Substantial geometric architecture: YES.}\\
\textbf{Literal printed first-order covariance: NO.}\\
\textbf{Explicit substitute Shiab typeable: YES.}\\
\textbf{Einstein contraction on geometric curvature: VERIFIED.}\\
\textbf{Exact full-adjoint algebraic completion: YES, as project work.}\\
\textbf{Local full-}(7,7)\textbf{ propagation: NO.}\\
\textbf{Observation-projected physical completion: OPEN.}
\end{array}
}
\]

## Earned results

### 1. Printed sign failure

With the 2021 draft's right action and tilted stabiliser,

\[
T_-\bigl(g\tau_-(h)\bigr)
=
h^{-1}T_-(g)h
-
2h^{-1}d_{A_0}h.
\]

The stabiliser-compatible repair is

\[
T_+
=
a+\varepsilon^{-1}d_{A_0}\varepsilon.
\]

### 2. First-order action covariance

The exact finite witness gives

\[
I_-^h-I_-=14,
\qquad
I_+^h-I_+=0.
\]

The literal first-order branch is rejected in its claimed invariant form.

### 3. Source-faithful Shiab reconstruction

The substitute in draft eq. (9.3) is a zeroth-order map

\[
\operatorname{Sh}_{\varepsilon}:
\Omega^2(Y,\operatorname{ad}P_H)
\longrightarrow
\Omega^{13}(Y,\operatorname{ad}P_H).
\]

On algebraic Riemann curvature, the mixed Clifford commutator/Jordan pattern gives

\[
[\gamma^c,F_{cd}]
=
R_{db}\gamma^b,
\]

\[
\{\gamma^{cd},F_{cd}\}
=
-R\mathbf1,
\]

and therefore the Einstein tensor. In fourteen dimensions the algebraic Riemann-sector map has rank 105 and a 3080-dimensional Weyl kernel.

The official corpus does not uniquely define the full \(U(64,64)\)-adjoint extension, observation derivative, Hessian, boundary domain or spectrum.

### 4. Exact \(\mathrm{Cl}(7,7)\) completion

The \(\mathsf R_+\)-EIN project branch now contains exact real \(128\times128\) gamma matrices and a symmetric spinor form

\[
H^T=H,
\qquad
H^2=\mathbf1,
\qquad
\operatorname{sig}(H)=(64,64).
\]

The canonical tensors are

\[
\Phi_1=e^A\otimes\Gamma_A,
\qquad
\Phi_2=\frac12e^A\wedge e^B\otimes\Gamma_{AB}.
\]

The minimal full-adjoint Einstein extension is

\[
\boxed{
\mathcal E_d(X)
=
[\Gamma^c,X_{cd}]
+
\frac14
\left\{
\left\{\Gamma^{cd},X_{cd}\right\},
\Gamma_d
\right\}.
}
\]

It closes exactly in \(u(64,64)\). The maximum closure residual is zero. The naive unsymmetrised continuation fails with exact residual 90.

### 5. Fatal split-signature symbol result

If this Einstein-like block propagates locally on the full total space with signature \((7,7)\), its characteristic factor is not hyperbolic with respect to any covector.

An explicit tangential witness gives

\[
q(\xi+\lambda n)
=
-(1+\lambda^2),
\qquad
\lambda=\pm i.
\]

Therefore:

\[
\boxed{
\texttt{PERT-02}=0
\quad\text{for }\mathsf R_+\text{-EIN-FULL-Y}.
}
\]

That branch is frozen as rejected.

## Only surviving physical route

The open branch is

\[
\mathsf R_+\text{-EIN-OBS4}.
\]

It must derive, from the equations and symmetries, a rank-four Lorentzian characteristic projector

\[
\Pi_{\rm obs}:T^*Y\to T^*X
\]

that is dynamically preserved and leaves exactly two graviton helicities.

Without that object, saying that observers “see” four dimensions does not solve the initial-value problem.

## Next calculation

- reconstruct the differential of the observation map;
- classify source-compatible horizontal/vertical characteristic projectors;
- test their gauge/BRST invariance and constraint propagation;
- derive the projected symbol;
- count modes;
- terminate the branch on the first fatal zero.

## Reproduce

```bash
make verify
```

This runs all source, sign, action, Clifford-Einstein, exact \(\mathrm{Cl}(7,7)\), full-adjoint closure and unit-test audits.

## Key files

- `STATUS.md`
- `phase3b_shiab_reconstruction.md`
- `phase4_rplus_ein_algebraic_completion.md`
- `rplus_ein_branch.yaml`
- `rplus_ein_acceptance_matrix.csv`
- `code/verify_cl77_rplus_ein.py`
- `results/cl77_rplus_ein.json`
- `acceptance_matrix.csv`

## Epistemic rule

Official sources establish what was proposed. Repairs, matrix representatives, full-adjoint extensions and branch verdicts are independent project work and are labelled as such.
