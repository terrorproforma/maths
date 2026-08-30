# TP-02 status

**Author:** Angus Muffatti  
**Version:** 0.6.0  
**Status date:** 31 August 2026  
**Project state:** **FROZEN — terminal source-incompleteness result reached**

## Terminal verdict

\[
\boxed{
\begin{array}{c}
\textbf{Substantial geometric architecture: YES.}\\
\textbf{Literal printed first-order theory: INCONSISTENT AS PRINTED.}\\
\textbf{Coherent repaired algebraic completion: YES.}\\
\textbf{Healthy local dynamics on }Y^{7,7}\textbf{: NO.}\\
\textbf{Four-dimensional dynamics from pullback alone: NO.}\\
\textbf{Complete source-defined successor theory: NO.}
\end{array}
}
\]

## Earned results

### Exact source-level failures

The printed augmented torsion satisfies

\[
T_-(g\tau_-(h))
=
h^{-1}T_-(g)h
-
2h^{-1}d_{A_0}h.
\]

The corresponding first-order action has the exact finite defect

\[
I_-^h-I_-=14.
\]

### Exact repaired algebra

The stabiliser-compatible branch

\[
T_+
=
a+\varepsilon^{-1}d_{A_0}\varepsilon
\]

passes the finite covariance test.

The source substitute Shiab reproduces the Einstein contraction on algebraic Riemann curvature. Its fourteen-dimensional Riemann-sector rank is 105 and its Weyl kernel has dimension 3080.

The explicit project completion supplies:

\[
\mathrm{Cl}(7,7)\cong\operatorname{Mat}_{128}(\mathbb R),
\]

a split spinor form of signature \((64,64)\), and the closed full-adjoint map

\[
\mathcal E_d(X)
=
[\Gamma^c,X_{cd}]
+
\frac14
\left\{
\left\{\Gamma^{cd},X_{cd}\right\},
\Gamma_d
\right\}.
\]

Its exact codomain-closure residual is zero.

### Fatal dynamical failures

For local propagation on the full split-signature total space,

\[
q(\xi+\lambda n)=-(1+\lambda^2)
\]

has roots \(\lambda=\pm i\). The branch is not hyperbolic:

\[
\texttt{PERT-02}=0.
\]

The source-motivated observation pullback also fails to produce autonomous four-dimensional dynamics. For normal coordinates \(z^a\),

\[
f_a=(z^a)^2,
\qquad
\iota^*f_a=0,
\]

but

\[
\iota^*(L_Yf_a)=2g^{aa}\neq0.
\]

Thus the ambient differential operator does not preserve the ideal of fields vanishing on the observed section. Normal jets remain necessary.

## Final branch ledger

- `DRAFT_LITERAL`: rejected.
- `R_PLUS_EIN_FULL_Y`: rejected.
- `R_PLUS_EIN_OBS4_PULLBACK`: rejected.
- `R_PLUS_EIN_ALG`: mathematically retained, not a physical successor.
- any normal-constrained, localized or induced-action completion: independent new theory, not defined by the primary source.

## Publication position

TP-02 is suitable as a source-faithful mathematical audit, not as a claim that every imaginable theory inspired by the geometry is impossible.

The narrow paper result is:

> The available primary formulation contains an exact sign inconsistency, does not determine a unique full Hessian, and its two most direct repaired propagation mechanisms fail respectively by split-signature non-hyperbolicity and non-closure of ambient dynamics under observation pullback.

## Reproduction

```bash
make verify
```

All committed checks are exact and standard-library-only.

## Next programme project

The numbered programme should now move to TP-03, the Pati–Salam benchmark. Any future use of TP-02 geometry must occur under a separately named completion project.
