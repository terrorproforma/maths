# Provenance and reproducibility record

## Final claims

The final mathematical objects are the two JSON certificates in `data/`. The proofs are reproduced independently in:

- the exact Python verifiers in `code/`;
- the derivation notes in `research/`;
- the LaTeX manuscripts in `papers/`.

The SSUF verifier reconstructs paths from the graph and does not trust a user-supplied path list. The chairman verifier uses exact rational arithmetic and explicitly includes the worst effects of assignments outside fractional support.

## Exploratory work

The constructions arose from an interactive sequence of abstract set-system gadgets, path-splicing tests, convex-hull separation models, and small graph searches. Not every ephemeral notebook cell or solver invocation survived as a standalone source file. No claim is made that this directory is a byte-for-byte archive of all exploratory computation.

The repository does contain all code needed to reproduce and verify the **final** certificates, together with compact scripts that reconstruct each selected parameter family. The final proofs do not depend on an unavailable solver, random seed, floating-point tolerance, or omitted path enumeration.

## AI assistance

A generative AI system assisted with exploration, algebraic checking, code drafting, exposition, and repository preparation. It is not an author and cannot assume scholarly responsibility. Human authors must independently verify the results, establish priority, choose the target journal, supply names and affiliations, and approve the final submission.

## Date and status

Package prepared on 23 July 2026. Status: preprint source and exact certificate package, not peer reviewed.
