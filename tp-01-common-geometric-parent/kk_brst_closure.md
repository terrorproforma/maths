# Kaluza-Klein and BRST closure audit

## 1. Exact mode algebra

On a circle of radius `R`, expand

\[
A_\mu(x,y)=\sum_{n\in\mathbb Z}A_\mu^{(n)}(x)e^{iny/R},
\qquad
\phi(x,y)=\sum_{n\in\mathbb Z}\phi^{(n)}(x)e^{iny/R},
\]

and similarly for the ghost `c`.

The internal-gauge BRST differential is

\[
sA_\mu^{(n)}
=D_\mu c^{(n)}
+\sum_m[A_\mu^{(m)},c^{(n-m)}],
\]

\[
s\phi^{(n)}
=\frac{in}{R}c^{(n)}
+\sum_m[\phi^{(m)},c^{(n-m)}],
\]

\[
sc^{(n)}
=-\frac12\sum_m[c^{(m)},c^{(n-m)}].
\]

These are the BRST equations of the loop algebra

\[
L\mathfrak g=\mathfrak g\otimes\mathbb C[z,z^{-1}],
\qquad
[Xz^m,Yz^n]=[X,Y]z^{m+n}.
\]

## 2. Finite-mode closure theorem

**Theorem.** Let `g` be non-Abelian and suppose every generator of `g` is retained at every mode in a set `S subset Z`. If `0 in S`, `n in S` for some nonzero `n`, and the truncation is closed under the nonlinear gauge bracket, then `S` is infinite.

**Proof.** Choose `X,Y in g` with `[X,Y] != 0`. Closure of `[X z^n,Y z^n]` requires `2n in S`. Repeating with `X z^n` and a noncommuting generator at mode `kn` requires `(k+1)n in S`. Thus every positive multiple of `n` belongs to `S`; reality supplies the negative multiples. A finite `S` is impossible. The only finite full-algebra truncation closed under addition is `S={0}`. QED.

For the requested set

\[
S=\{-1,0,+1\},
\]

the first missing products are

\[
(+1)+(+1)=+2,
\qquad
(-1)+(-1)=-2.
\]

Equivalently,

\[
sc^{(2)}=-\frac12[c^{(1)},c^{(1)}]
\]

is generically nonzero. The retained fields do not form a BRST subcomplex.

A finite first-level model can be used only as:

1. a linearized/quadratic diagnostic around a `y`-independent background;
2. an Abelian or specially commuting restriction;
3. an orbifold/projection with a separately proved consistent multiplication law; or
4. a new projected theory whose gauge algebra is no longer the original loop algebra.

## 3. Linearized first-level complex

Around a `y`-independent background `(Bbar_mu, phibar)`, the linear BRST differential is mode diagonal:

\[
s_0a_\mu^{(n)}=\bar D_\mu c^{(n)},
\]

\[
s_0\varphi^{(n)}
=\left(\frac{in}{R}+\operatorname{ad}_{\bar\phi}\right)c^{(n)},
\qquad
s_0c^{(n)}=0.
\]

Define

\[
\mathcal D_y^{(n)}
=\frac{in}{R}+\operatorname{ad}_{\bar\phi}.
\]

Where `D_y^(n)` is invertible, the scalar fluctuation is a Stueckelberg variable for the longitudinal part of `a_mu^(n)`. Where it has a kernel, additional massless/holonomy-centralizer modes survive.

This is only a linear statement. Nonlinear interactions immediately couple `n=+/-1` to `n=+/-2` and beyond.

## 4. Degree count at the first level

On a `y`-translation-invariant regular canonical background, Fourier modes block-diagonalize the quadratic first-order form. The complexified `n=1` block carries the same 13 configuration degrees of freedom as the local five-dimensional regular sector. Reality pairs `n=+1` and `n=-1`, yielding

\[
N_{\rm dof}^{|n|=1}=26
\]

real configuration degrees of freedom.

The zero mode already carries 13 rather than the 2 of GR. Adding the first level therefore worsens the mismatch. Retaining the exact nonlinear theory requires the entire tower.

## 5. Why small radius does not finish the job

In ordinary metric Kaluza-Klein theory, the operator `n/R` often produces a positive mass gap and supports decoupling as `R -> 0`. Pure five-dimensional Chern-Simons theory is first order and background dependent. Its kinetic matrix is the curvature-dependent presymplectic form `Omega`; at the AdS point `Omega=0`. Therefore `n/R` by itself does not establish:

- a positive Hamiltonian;
- a standard massive pole;
- Appelquist-Carazzone decoupling;
- or a two-helicity low-energy limit.

A decoupling claim would require a regular quadratic propagator, positive residues and an explicit matching calculation. TP-01 supplies none, and the AdS candidate has no ordinary quadratic propagator at all.
