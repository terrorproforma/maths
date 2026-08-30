# Obstruction 01: no exact finite-state classical realization

The first extracted process does more than erase coordinates. It contains a
basis-independent spectral feature that rules out an entire ontology class.

## Setup

The minimal transition associated with operation \(x\) has spectrum

\[
\operatorname{spec}(T_x)=\{1,1,e^{i\theta_x},e^{-i\theta_x}\},
\qquad \theta_x=73/100\text{ radians}.
\]

Likewise,

\[
\operatorname{spec}(T_z)=\{1,1,e^{i\theta_z},e^{-i\theta_z}\},
\qquad \theta_z=111/100\text{ radians}.
\]

Spectra are invariant under the similarity freedom of minimal realization.

## Classical candidate class

An exact finite-state classical controlled process would use:

- a finite probability vector;
- one nonnegative stochastic matrix \(M_a\) for each operation \(a\); and
- a final response function with values in \([0,1]\).

Any higher-dimensional realization reduces to the minimal reachable-observable
one by an intertwining quotient. Therefore every eigenvalue of \(T_a\) must also
occur in the spectrum of \(M_a\).

## Perron--Frobenius obstruction

For a finite nonnegative stochastic matrix, every eigenvalue on the unit circle
is a root of unity. Equivalently, each peripheral phase must be a rational
multiple of \(2\pi\).

Now let \(r\neq0\) be rational. If \(e^{ir}\) were a root of unity, then for some
integers \(n>0\) and \(k\neq0\),

\[
nr=2\pi k.
\]

Hence

\[
\pi=\frac{nr}{2k}
\]

would be rational, a contradiction. Thus \(e^{i73/100}\) and
\(e^{i111/100}\) are not roots of unity.

Therefore no finite stochastic matrices \(M_x,M_z\) can contain the required
peripheral modes, and:

\[
\boxed{
\text{no exact finite-state classical stochastic realization exists.}
}
\]

A qubit realization does exist. Infinite classical state spaces and finite
approximations remain possible.

## Why this is closer to “cannot be otherwise”

The result is not a preferred coordinate description. It is a surviving
obstruction:

1. sequence probabilities fix a minimal transition tuple up to similarity;
2. similarity fixes its spectrum;
3. the spectrum violates a necessary condition for every finite classical
   stochastic realization.

The positive statement “the world is quantum” is still too strong. The precise
forced statement is narrower and better:

> Any exact realization in the declared finite controlled-process class must be
> nonclassical, infinite, or abandon stochastic-state ontology.

## Epistemic warning

The analytic proof uses exact model angles. Finite experimental data cannot prove
that a measured phase is irrational; it can only exclude roots of unity up to a
bounded order and confidence level. The noisy version of ANANKE must therefore
return graded obstruction certificates, not metaphysical declarations.
