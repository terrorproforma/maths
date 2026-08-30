# ANANKE — Project Brief v0

**Author:** Angus Muffatti  
**Repository project:** `ananke-necessity-transformations`

## Research question

Can we identify structures that are not artifacts of a chosen mathematical representation by extracting only what survives every operationally equivalent realization of a process?

## v0 working principle

ANANKE begins with exact observable sequential behaviour

\[
f(w)=\text{observed scalar after operation word }w.
\]

It constructs behavioural Hankel matrices, extracts the minimal reachable-observable linear realization, and treats invertible similarity transformations as changes of representation rather than changes of process.

## v0 deliverables

- Exact finite-rank Hankel realization.
- Removal of unreachable hidden dynamics.
- Recovery of transition tuples up to simultaneous similarity.
- Exact peripheral-spectrum obstruction to finite-state classical stochastic realization for the declared qubit process.
- Five automated tests.

## Current epistemic status

The implementation combines established system-realization, weighted-automata, operational-equivalence, gate-set gauge, and Perron–Frobenius machinery. The research contribution being tested is the adversarial programme: deliberately destroy representational choices and retain only the operational core and the realization classes it excludes.

## Next target

Move from exact oracle access to finite-shot observations, uncertain predictive rank, confidence regions for invariant spectra, and graded lower bounds on the size of competing classical realizations.
