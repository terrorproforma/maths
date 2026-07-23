# arXiv submission package

Self-contained source for the arXiv upload — verified to compile standalone:

- `chairman_counterexample.tex` (figure path adjusted to the flat layout)
- `chairman_gadget.tex` (TikZ figure, input by the main file)
- `chairman_counterexample.bbl` (bibliography — arXiv does not run BibTeX, so the
  compiled .bbl must be included)
- `chairman_counterexample.pdf` (reference build; arXiv recompiles from source)

## Upload steps

1. arxiv.org → START NEW SUBMISSION.
2. Upload the three source files (`.tex`, the figure `.tex`, `.bbl`) — or a zip of them.
   Do **not** upload the PDF; arXiv builds from TeX source.
3. **Primary category: `math.CO`** (combinatorics / discrepancy theory); suggested
   cross-list: `cs.DM`. Note the account's default is `cs.CE` — change it for this
   submission.
4. License: the common choice for preprints intended for journal submission is the
   arXiv non-exclusive license; CC BY 4.0 if maximum reuse is preferred.
5. Abstract: use the abstract from the paper.

## Pre-submission checklist (already done)

- Conjecture statements audited against the published ITCS 2026 version (Conjectures 19
  and 21; arXiv preprint 2511.18546 numbers them 3 and 5 — noted in the paper).
- Author metadata corrected (Siyue Liu, pages 98:1–98:15, correct paper title).
- Certificate verified three independent ways (two exact-rational verifiers + HiGHS MILP
  infeasibility).
- No existing counterexample to these conjectures found in public sources as of
  24 July 2026.

## Notes

- New arXiv accounts without an institutional affiliation typically need an
  **endorsement** for a first `math.CO` submission — the submission system will say if
  so and will provide an endorsement code to send to an endorser.
- After the paper is announced, consider emailing Siyue Liu and Victor Reis directly:
  the authors of the refuted conjecture are the natural first readers, the fastest
  independent verifiers, and the paper is small enough to check in an afternoon.
