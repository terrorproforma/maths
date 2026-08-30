# ANANKE v1 research status

## Terminal result

ANANKE now converts finite sequential data into a graded statement about ontology:

\[
\boxed{
\text{Any exact finite classical stochastic realization compatible with the data}
\text{ requires at least }N\text{ hidden states.}
}
\]

For the baseline finite-shot qubit experiment:

\[
\boxed{
\begin{aligned}
\text{selected predictive dimension} &=4,\\
\text{analytic classical lower bound} &\ge9,\\
\text{full-region numerical lower bound} &\ge16.
\end{aligned}
}
\]

The rank was selected in 100/100 bootstrap repetitions. A known three-state classical
cycle produced a 1/100 false-exclusion rate at the nominal 99% level.

## What is genuinely established

1. **Representation erasure survives noise.** The inferred object remains a minimal
   predictive process up to similarity, rather than a preferred coordinate matrix.
2. **Finite data can force finite ontological cost.** Exact irrationality is not
   required; a confidence set can be separated from every stochastic eigenvalue
   region through a chosen state count.
3. **The cost forms an arithmetic staircase.** Increasing precision crosses
   Farey/continued-fraction thresholds rather than improving a smooth scalar score.
4. **The gate angle contains a counterfeit hierarchy.** Its rational approximants
   identify classical cycle sizes that can imitate it unusually well.

## What is prior art

The project stands on established machinery:

- Hankel-rank and observable-dynamics dimension inference;
- spectral/quasi-realization methods;
- positive and hidden Markov realization theory;
- classical-versus-quantum dimension gaps;
- Karpelevič regions for stochastic-matrix eigenvalues;
- Perron–Frobenius peripheral-spectrum restrictions.

Particularly close precedents are:

- Michael M. Wolf and David Pérez-García, *Assessing dimensions from evolution*
  (2009), <https://arxiv.org/abs/0901.2542>;
- Stephen Kirkland, Thomas Laffey and Helena Šmigoc, *The Karpelevič Region
  Revisited* (2020), <https://arxiv.org/abs/2005.02452>;
- Fanizza et al., *Quantum theory in finite dimension cannot explain every
  finite-dimensional process* (2022/2024), <https://arxiv.org/abs/2209.11225>;
- Qingqing Huang, Rong Ge, Sham Kakade and Munther Dahleh, *Minimal Realization
  Problems for Hidden Markov Models* (2014),
  <https://arxiv.org/abs/1411.3698>.

## Candidate contribution

A quick literature review did not reveal this exact combination as a packaged
method:

\[
\text{controlled word experiments}
\rightarrow
\text{held-out rank selection}
\rightarrow
\text{bootstrap similarity-invariant spectrum}
\rightarrow
\text{Karpelevič hidden-state lower bound}
\rightarrow
\text{Diophantine gate design}.
\]

That is a **candidate** methodological contribution, not yet a defensible novelty
claim. A proper paper requires a systematic literature review and comparison against
positive-realization and quantum-memory-dimension witnesses.

## Most important caveats

### Bootstrap validity

The confidence disk is a plug-in parametric bootstrap. Rank selection and mode
selection introduce additional uncertainty. The three-cycle calibration is useful but
far from a coverage theorem.

### Full-region numerical status

The lower bound of nine uses a simple analytic necessary half-plane. The sharper
bound of sixteen uses numerical global minimization over algebraic Karpelevič
boundaries with a convergence guard. It should be replaced by interval arithmetic
before being called machine-certified.

### Interface relativity

The core is necessary only relative to the admitted preparations, operations,
measurements and sequential composition. Expanding the interface can reveal more
structure; restricting it can erase structure.

### Exact versus approximate realizations

The bound concerns exact finite classical realizations compatible with a confidence
set. It does not prohibit approximate models outside the tested accuracy, nor
infinite-state classical models.

## The genuinely new-looking direction

The arithmetic result changes the research programme. We should no longer ask only:

> Which structures survive representation changes?

We should also ask:

> How expensive is the cheapest alternative ontology at each observational
> precision?

Define an ontology-cost profile

\[
C_{\mathcal O}(\varepsilon)
=
\min\{\text{realization size in ontology class }\mathcal O:
\text{error}\le\varepsilon\}.
\]

For finite classical stochastic models, ANANKE v1 measures lower bounds on
\(C_{\mathrm{classical}}(\varepsilon)\). Different phases generate different
continued-fraction staircases. The invariant is therefore not just a transformation
class but a **counterfeit-complexity function**.

That may be the first formulation in this programme that is both philosophically
alien and experimentally operational.

## Next decisive target: ANANKE v2

The next phase should be a theorem-and-algorithm package, not merely more simulation:

1. construct interval-certified distances from complex confidence regions to
   \(\Theta_N\);
2. derive joint coverage for rank selection and spectral invariants;
3. optimize operation phases, preparation, measurement and word allocation to
   maximize classical-memory exclusion per shot;
4. generalize from a single transition eigenvalue to joint invariants of a
   noncommuting transition tuple;
5. compare classical simplicial cones, quantum semidefinite cones and general GPT
   cones on the same extracted core;
6. define and estimate the ontology-cost profile
   \(C_{\mathcal O}(\varepsilon)\).

The highest-leverage theoretical calculation is now:

\[
\boxed{
\text{prove a finite-sample, interval-certified lower bound on}
\ C_{\mathrm{classical}}(\varepsilon)
\text{ and optimize it over noble phase families.}
}
\]
