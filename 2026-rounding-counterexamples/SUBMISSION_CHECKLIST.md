# Journal submission checklist

## Mathematical audit

- [ ] Two independent experts have checked the seven-vertex SSUF certificate.
- [ ] An expert has checked the exact wording and quantifiers of Goemans' conjecture against the cited sources.
- [ ] An expert has checked the chairman forcing proof, including assignments outside fractional support.
- [ ] `python3 code/verify_all.py` passes on a clean checkout.
- [ ] The GitHub Actions verification and PDF-build jobs are green.
- [ ] The parametric `9/8` planar lower-bound calculation has been independently checked.

## Priority and literature

- [ ] Repeat the literature search immediately before submission.
- [ ] Check arXiv, DBLP, MathSciNet, zbMATH, conference proceedings, and authors' webpages for overlapping results.
- [ ] Consider notifying the conjecture originators and the authors of the most recent positive results.
- [ ] Replace all `to our knowledge` claims with wording supported by the final search date.

## Authorship and ethics

- [ ] Replace `Anonymous for review` as required by the journal.
- [ ] Add affiliations, corresponding-author details, funding, acknowledgements, and contributions.
- [ ] Review `AI_DISCLOSURE.md` against the journal's current policy.
- [ ] Confirm that every human author has read and approved the final manuscript.
- [ ] Confirm that the title, abstract, and press language do not overstate peer-review status.

## Typesetting and artifacts

- [ ] Build all PDFs from a clean checkout with `make all`.
- [ ] Inspect every compiled page at readable resolution.
- [ ] Check that figure labels are legible in grayscale and at one-column width.
- [ ] Check references, DOIs, hyperlinks, theorem numbering, and equation cross-references.
- [ ] Remove build auxiliaries and verify that source archives contain everything needed.
- [ ] Select and apply an explicit code/data license approved by the authors.

## Recommended circulation order

1. Private mathematical audit.
2. Author-originator courtesy check where appropriate.
3. Preprint deposit with immutable versioned certificate.
4. Journal or conference submission.
5. Public announcement only after the authors are satisfied with priority and correctness.
