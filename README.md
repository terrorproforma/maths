# maths

Research notes, computational certificates, and reproducible manuscripts.

> **Provenance notice.** This repository builds on attributed third-party work: the
> DGG/Goemans flow counterexample is due to Dmitry Rybin (with GPT-5.6 Pro), and the
> Jacobian-conjecture starting map is due to Levent Alpöge, Akhil Mathew, and Claude
> Fable 5. See [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md) for citations and
> [`PROVENANCE_AUDIT.md`](PROVENANCE_AUDIT.md) for the exact boundary between that work
> and the owner's results. Candidate future research targets are catalogued in
> [`CONJECTURE_TARGETS.md`](CONJECTURE_TARGETS.md).

## Projects

- [`2026-rounding-counterexamples/`](2026-rounding-counterexamples/) — standalone
  manuscripts and exact certificates for two weighted-rounding results:
  the machine-dependent weighted-chairman counterexample (owner's session) and the
  DGG/Goemans cost-conjecture counterexample (due to Rybin — attributed).
- [`2026-dgg-and-chairman-counterexamples/`](2026-dgg-and-chairman-counterexamples/) — a
  later combined package of the same two results with a single merged manuscript carrying
  an explicit attribution note for the Rybin-derived sections.
- [`subtree-shuffling-counterexample/`](subtree-shuffling-counterexample/) — the
  fixed-parameter (d,p) = (7,15) obstruction to the subtree-shuffling conjecture
  (owner's session, building on the attributed Alpöge–Mathew–Fable starting map — see its
  `PROVENANCE.md`).

Every project carries its own status, provenance, review checklist, tests, and build
instructions. All mathematical claims are AI-generated and unverified until independently
audited.
