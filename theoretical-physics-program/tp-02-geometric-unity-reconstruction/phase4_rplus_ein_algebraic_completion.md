# Phase 4 — Exact \(\mathrm{Cl}(7,7)\), full-adjoint completion, and the split-signature symbol obstruction

**Project:** TP-02 — Independent Reconstruction of Geometric Unity  
**Branch:** \(\mathsf{R}_{+}\)-EIN  
**Status:** **ALGEBRAIC COMPLETION PASSES; LOCAL FULL-\(Y\) PROPAGATION FAILS**

## 1. Executive result

The strongest source-motivated completion can now be made completely explicit at the Clifford-algebra level:

\[
\boxed{
\mathrm{Cl}(7,7)\cong \operatorname{Mat}_{128}(\mathbb R)
}
\]

is realised by exact \(128\times128\) signed-permutation matrices, the spin module carries an explicit symmetric form of signature \((64,64)\), and the canonical one- and two-form tensors can be written as

\[
\Phi_1=e^A\otimes\Gamma_A,
\qquad
\Phi_2=\frac12e^A\wedge e^B\otimes\Gamma_{AB}.
\]

The geometric Einstein contraction extends to arbitrary \(u(64,64)\)-valued curvature by the unique minimal left/right symmetrisation that preserves the adjoint codomain:

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

This extension passes exact algebraic closure tests.

However, the same calculation exposes the decisive physical obstruction:

\[
\boxed{
\text{the Einstein-like principal block on a local }(7,7)\text{ total space is not hyperbolic.}
}
\]

Therefore the local full-\(Y\) \(\mathsf R_+\)-EIN branch receives a fatal `PERT-02 = 0`. A viable continuation would have to derive a four-dimensional Lorentzian characteristic projector **before** propagation, not merely recover four-dimensional-looking algebra after the fact.

This result rejects one explicit completion branch. It does not prove that every possible completion of the broader geometric idea is impossible.

## 2. Exact real Clifford representation

Let

\[
I=
\begin{pmatrix}1&0\\0&1\end{pmatrix},
\quad
X=
\begin{pmatrix}0&1\\1&0\end{pmatrix},
\quad
Z=
\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\quad
J=
\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

Then

\[
X^2=Z^2=I,
\qquad
J^2=-I,
\]

and \(Z\) anticommutes with both \(X\) and \(J\), while \(XJ=-JX\).

For \(j=1,\ldots,7\), define

\[
P_j
=
Z^{\otimes(j-1)}
\otimes X
\otimes I^{\otimes(7-j)},
\]

\[
N_j
=
Z^{\otimes(j-1)}
\otimes J
\otimes I^{\otimes(7-j)}.
\]

Set

\[
\Gamma_A
=
(P_1,\ldots,P_7,N_1,\ldots,N_7).
\]

The verifier proves exactly that

\[
\Gamma_A\Gamma_B+\Gamma_B\Gamma_A
=
2\eta_{AB}\mathbf1_{128},
\]

with

\[
\eta=\operatorname{diag}(+1,\ldots,+1,-1,\ldots,-1)
\]

containing seven signs of each type.

No floating-point arithmetic is used. Each gamma matrix is stored as a signed permutation.

## 3. Explicit \((64,64)\) spinor form

Define

\[
H=N_1N_2\cdots N_7.
\]

The exact identities are

\[
H^T=H,
\qquad
H^2=\mathbf1,
\qquad
\operatorname{tr}H=0.
\]

Consequently \(H\) has 64 eigenvalues \(+1\) and 64 eigenvalues \(-1\):

\[
\boxed{\operatorname{sig}(H)=(64,64).}
\]

Every gamma generator obeys

\[
\Gamma_A^T H+H\Gamma_A=0,
\]

and all 91 bivectors

\[
\Gamma_{AB}=\frac12[\Gamma_A,\Gamma_B]
\]

obey the same \(H\)-skew condition. After complexification this gives the declared embedding of the spin action into \(u(64,64)\).

The volume element

\[
\Gamma_*=\Gamma_1\Gamma_2\cdots\Gamma_{14}
\]

satisfies

\[
\Gamma_*^2=\mathbf1,
\qquad
\operatorname{tr}\Gamma_*=0,
\qquad
\{\Gamma_*,\Gamma_A\}=0.
\]

Its chiral eigenspaces have dimensions \(64+64\). Moreover,

\[
\{H,\Gamma_*\}=0,
\]

so the split Hermitian form pairs opposite chiralities rather than restricting nondegenerately to one chiral half.

## 4. Canonical \(\Phi_1,\Phi_2\)

On a local oriented orthonormal coframe \(e^A\) of the split-signature total space, choose

\[
\boxed{
\Phi_1=e^A\otimes\Gamma_A,
}
\]

\[
\boxed{
\Phi_2=\frac12e^A\wedge e^B\otimes\Gamma_{AB}.
}
\]

These are explicit project-selected representatives of the invariant pure-trace tensors motivating draft eq. (9.3). Their normalisation and the choice of spinor form are now fixed for the \(\mathsf R_+\)-EIN branch.

They are **not** retroactively attributed to the official source, which does not provide these complete matrices and domains.

## 5. The full-adjoint codomain problem

Let the \(H\)-adjoint be

\[
M^\sharp=H^{-1}M^\dagger H.
\]

The adjoint algebra is

\[
u(H)=\{X:X^\sharp=-X\}.
\]

For \(X_{cd}\in u(H)\), the Ricci-like channel

\[
\mathcal R_d(X)=[\Gamma^c,X_{cd}]
\]

is again \(H\)-skew.

The scalar-like channel

\[
S(X)=\{\Gamma^{cd},X_{cd}\}
\]

is instead \(H\)-self-adjoint:

\[
S^\sharp=S.
\]

This is harmless on geometric Riemann curvature, where \(S\) is central. It becomes decisive on arbitrary full-adjoint curvature.

The naive continuation

\[
S\Gamma_d
\]

does **not** generally lie in \(u(H)\). The exact random-integer witness gives a maximum \(H\)-skew residual of

\[
\boxed{90}.
\]

## 6. Minimal codomain-preserving extension

Consider the most general real left/right linear completion

\[
aS\Gamma_d+b\Gamma_dS.
\]

Because \(S^\sharp=S\) and \(\Gamma_d^\sharp=-\Gamma_d\),

\[
(aS\Gamma_d+b\Gamma_dS)^\sharp
=
-a\Gamma_dS-bS\Gamma_d.
\]

Requiring this to equal minus the original expression for every \(S\) gives

\[
a=b.
\]

On the geometric sector \(S=s\mathbf1\), the source-motivated scalar term is \(\frac12s\Gamma_d\). Therefore

\[
2a=\frac12,
\qquad
a=b=\frac14.
\]

Hence the unique minimal completion in this class is

\[
\boxed{
\mathcal E_d(X)
=
[\Gamma^c,X_{cd}]
+
\frac14\{S(X),\Gamma_d\}.
}
\]

Equivalently,

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

The exact \(128\times128\) integer audit gives

\[
\boxed{
\max_d
\left\|
\mathcal E_d^\sharp+\mathcal E_d
\right\|_\infty
=0.
}
\]

Thus the algebraic completion is closed on the declared full adjoint.

On geometric spin curvature, the earlier Phase 3B identities give

\[
[\Gamma^c,F_{cd}]=R_{db}\Gamma^b,
\]

\[
\{\Gamma^{cd},F_{cd}\}=-R\mathbf1,
\]

so the symmetrised extension reduces exactly to

\[
\mathcal E_d(F)
=
\left(R_{db}-\frac12Rg_{db}\right)\Gamma^b.
\]

## 7. Split-signature principal-symbol obstruction

Suppose this geometric block is allowed to propagate locally on the full total space \(Y\) with metric signature \((7,7)\). Around a flat background, the de Donder-gauge Einstein principal factor is

\[
q(k)=g^{AB}k_Ak_B.
\]

A quadratic polynomial is hyperbolic with respect to a covector \(n\) only if

\[
\lambda\mapsto q(\xi+\lambda n)
\]

has real roots for every covector \(\xi\).

For any timelike \(n\) in signature \((p,q)\) with more than one timelike direction, the orthogonal complement \(n^\perp\) still contains a timelike covector \(\xi\). Choose

\[
g^{-1}(n,n)=-1,
\qquad
g^{-1}(\xi,\xi)=-1,
\qquad
g^{-1}(n,\xi)=0.
\]

Then

\[
q(\xi+\lambda n)
=
-(1+\lambda^2),
\]

with roots

\[
\lambda=\pm i.
\]

Therefore:

\[
\boxed{
q(k)\text{ is not hyperbolic with respect to any covector in signature }(7,7).
}
\]

No ordinary codimension-one strongly hyperbolic Cauchy problem exists for generic local data in this block.

A purely formal fourteen-dimensional Einstein metric count would also give

\[
\frac{14(14-3)}2=77
\]

metric polarizations, rather than the two helicities required in four-dimensional GR. In split signature, the more immediate failure is the absence of a standard hyperbolic/positive-energy propagation problem.

## 8. Branch verdict

The completion tree must now split:

| Branch | Result |
|---|---|
| `R_PLUS_EIN_ALG` | **PASS** — exact Clifford representation and full-adjoint codomain closure |
| `R_PLUS_EIN_FULL_Y` | **REJECTED** — fatal split-signature hyperbolicity failure |
| `R_PLUS_EIN_OBS4` | **OPEN** — requires a dynamically derived four-dimensional Lorentzian characteristic projector |

The fatal result is:

\[
\boxed{
\texttt{PERT-02}=0
\quad\text{for local propagation on the full split-signature total space.}
}
\]

This cannot be repaired by saying observers only *perceive* four dimensions. The equations must contain an invariant constraint or projector that removes the extra characteristic directions before the initial-value problem is posed.

## 9. Exact next calculation

The only surviving route inside this completion family is to construct

\[
\Pi_{\mathrm{obs}}:
T^*Y\longrightarrow T^*X
\]

or an equivalent constrained characteristic distribution satisfying all of:

1. rank four on the claimed background;
2. induced signature \((1,3)\);
3. invariance under the repaired gauge/BRST flow;
4. propagation under the equations rather than external imposition;
5. no hidden second-class inconsistency;
6. two graviton helicities after reduction;
7. recovery of the Standard Model characteristic cone.

If no such source-motivated projector can be derived, the physical \(\mathsf R_+\)-EIN programme terminates even though its Clifford algebra is elegant and exact.

## 10. Reproduction

Run

```bash
python code/verify_cl77_rplus_ein.py --root .
python -m unittest code.tests.test_cl77_rplus_ein -v
```

or simply

```bash
make verify
```

The verifier uses only the Python standard library and exact integer arithmetic.
