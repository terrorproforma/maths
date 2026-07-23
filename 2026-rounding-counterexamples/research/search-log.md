# Structured search log

This is a concise, reproducible account of the ideas that led to the final certificates. It is not a transcript of private scratch work and does not claim to preserve every exploratory solver call.

## Phase 1: exact separation formulation

For a fixed fractional flow `x`, define `U(x)` as the load vectors of all unsplittable routings satisfying `y <= x+D`. A cost counterexample exists exactly when `x` lies outside `conv U(x)`. The corresponding separating functional can be shifted by vertex potentials to a nonnegative arc-cost vector on a DAG.

This led to two exact tests:

- enumerate all paths and routings, then solve finite convex-hull separation;
- for larger graphs, use column generation with a binary min-cost routing oracle under `y <= x+D`.

## Phase 2: abstract cube and resource gadgets

Hypercube and clause-resource systems produced strong abstract counterexamples. Their intended binary path choices violated one resource for every integral selection. They failed as graph counterexamples because the union of designated paths contains additional prefix-suffix hybrids.

Two no-go principles emerged:

1. **Suffix splicing:** after paths merge and split, all compatible prefixes and suffixes are graph paths.
2. **Common-source prefix borrowing:** a terminal may begin on another designated track and switch later into a route to its own sink.

Exact pricing repeatedly found inexpensive hybrid routings and drove restricted positive separators back to zero.

## Phase 3: capacity-enforced state systems

Four-track token-and-hole braids were tested so that the `+D` allowance itself enforced collision-free configurations. This converted all hybrids into states of a small matching automaton. Shallow symmetric braids remained convex-combination feasible and did not separate.

## Phase 4: discrepancy and circular-interval abstractions

Weighted partition-constrained and circular-interval selection systems yielded finite abstract obstructions. Their graph realizations again acquired hybrids. The useful lesson was that a successful graph should realize a conflict facet with **nested shared prefixes**, rather than independent resource intersections.

## Phase 5: nested triangle breakthrough

The final SSUF topology uses three nested bottlenecks:

```text
s->u, u->v, v->w.
```

The cheap paths are nested so that:

```text
Z1+Z2 conflicts on s->u because every t3 path uses s->u;
Z1+Z3 conflicts on u->v;
Z2+Z3 conflicts on v->w.
```

Each sink has exactly two paths, so there are no hidden splice paths. Choosing cheap-path marginals `(1/3,2/5,1/3)` violates the triangle stable-set inequality by `1/15`. Scaling by 15 and assigning common expensive-path cost 30 gives the exact `58<60` certificate.

## Phase 6: machine-dependent forcing gadget

For the chairman problem, machine-dependent weights permit a local detector:

```text
J not assigned to A
  => K must be assigned to A
  => either choice on L violates A or H.
```

A small positive default weight `eta` blocks the objection that an integral assignment may leave the fractional support. Repeating the detector five times forces five decisions into a global accumulator and gives `619/600>1`.

## Final verification standard

A candidate was accepted only after it had:

- rational or integer data;
- a proof covering every path or every assignment category;
- an exact standard-library verifier;
- no floating-point tolerance or omitted-column assumption;
- a clean LaTeX build in GitHub Actions.
