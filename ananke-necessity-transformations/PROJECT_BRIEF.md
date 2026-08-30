# ANANKE — Project Brief

**Author:** Angus Muffatti  
**Repository project:** `ananke-necessity-transformations`

## Research question

Can we identify structures that are not artifacts of a chosen mathematical representation by extracting only what survives every operationally equivalent realization of a process?

## Working principle

ANANKE begins with observable sequential behaviour

\[
f(w)=\Pr(1\mid w),
\]

where `w` is a finite word of controlled operations. It constructs a minimal predictive realization from behavioural Hankel matrices, quotients away unreachable and unobservable coordinates, and studies the residual transformations only up to similarity.

The programme then asks a stronger question: how expensive must a competing ontology become to reproduce the same operational core to precision \(\varepsilon\)? This motivates the counterfeit-complexity function

\[
C_{\mathcal O}(f;\varepsilon,\mathcal W),
\]

the minimum size of a realization in ontology class \(\mathcal O\) reproducing behaviour `f` on experiment set \(\mathcal W\) within the declared error.

## Completed stages

### v0 — exact operational core

- Exact finite-rank Hankel realization.
- Removal of unreachable hidden dynamics.
- Recovery of transition tuples up to simultaneous similarity.
- Exact peripheral-spectrum obstruction to finite-state classical stochastic realization for the declared qubit process.
- Five automated tests.

### v1 — finite-shot counterfeit complexity

- Binomial finite-shot observations.
- Held-out predictive-rank selection.
- Bootstrap confidence regions for invariant spectral modes.
- Analytic and numerical lower bounds from stochastic-matrix eigenvalue regions.
- Calibration against genuine three-state classical processes.
- Continued-fraction analysis of finite classical counterfeits.
- Eighteen automated tests.

## Current status

The machinery used by ANANKE has substantial prior art: Hankel realization, weighted automata, system minimization, gate-set gauge freedom, hidden-state dimension witnesses, Perron–Frobenius theory, Karpelevič regions, and Diophantine approximation are established subjects.

The candidate contribution is their integration into an adversarial, finite-data programme that reports a graded ontology-cost profile rather than asserting a privileged hidden model. The current full-region bound is convergence-checked floating-point evidence, not yet an interval-certified theorem. Bootstrap coverage has been calibrated on declared examples but is not uniformly proved.

## Next decisive target — v2

1. Interval-certified distance from spectral confidence sets to stochastic eigenvalue regions.
2. Joint rank-and-spectrum finite-sample coverage.
3. Optimal badly approximable or noble-phase experiment design under a shot budget.
4. Joint invariants of noncommuting transformation tuples.
5. Direct comparison of classical simplicial, quantum semidefinite, and broader generalized-probabilistic realization costs.

## Reproduction

The current implementation is in this directory. Install from a clean checkout and run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[plots]'
python -m unittest discover -s tests -v
```
