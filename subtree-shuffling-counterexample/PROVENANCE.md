# Provenance

## Starting map

**The starting map is attributed third-party work.** It is due to **Levent Alpöge**, with
the problem suggested by Akhil Mathew and the map found with Anthropic's Claude Fable 5,
announced publicly on 19–20 July 2026:
<https://x.com/__alpoge__/status/2079028340955197566>. It was pasted into the research
conversation as a prompt. The repository owner claims no part of the map, its verification,
or its fiber-geometry analysis; this project builds on the map with credit, and any
manuscript derived from this repository must cite the announcement. See
`../ATTRIBUTIONS.md` and `../PROVENANCE_AUDIT.md` at the repository root.

The project begins with the polynomial map supplied in the research discussion:

```text
((1+xy)^3 z + y^2(1+xy)(4+3xy),
 y + 3x(1+xy)^2 z + 3xy^2(4+3xy),
 2x - 3x^2y - x^3z).
```

Its Jacobian determinant is `-2`, and the three rational inputs

```text
(0,0,-1/4), (1,-3/2,13/2), (-1,3/2,13/2)
```

have the common image `(-1/4,0,0)`.

A contemporaneous public source for the broader 2026 Jacobian-counterexample announcement is Christopher D. Long, *Small Counterexamples to the Gaussian Moments Conjecture*, arXiv:2607.18186. The present repository does not attempt to adjudicate priority for the starting map.

## Contributions documented here

The repository develops and records:

1. the determinant-one identity-linear normalization `G`;
2. the hidden cubic coordinates for `G`;
3. the weighted Horner suspension theorem;
4. the explicit degree-seven 15-variable homogeneous Keller map;
5. the inverse-slice identity;
6. the exact Lagrange coefficient `(-1)^m 2^m binom(3m+1,m)`;
7. the fixed-parameter tree separator for `(d,p)=(7,15)`;
8. executable SymPy verification and a journal-style manuscript.

## Authorship and disclosure

The manuscript currently uses `Anonymous for review`. Before submission, the human authors must decide authorship, acknowledgements, and any journal-required disclosure of AI-assisted research and drafting. The repository history should be preserved as part of the provenance record.
