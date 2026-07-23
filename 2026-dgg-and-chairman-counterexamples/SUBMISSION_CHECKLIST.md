# Submission checklist

The source is written as an anonymous journal manuscript. Complete the following before sending it to an editor.

## Mathematical validation

- Run `python3 code/verify_all.py` in a clean Python environment.
- Confirm that `verify_dgg.py` lists exactly eight routings, exactly four additive-`D`-good routings, fractional cost 58, and good optimum 60.
- Confirm that the all-positive-cost variant reports 409 versus 415.
- Confirm that `verify_chairman_certificate.py` reports every strict rational margin and final bound `619/600`.
- Confirm that the SciPy/HiGHS model returns infeasible, not a time limit or solver error.
- Ask at least two experts in unsplittable flow or discrepancy theory to audit the statements and definitions against the cited papers.

## Priority and scope

- Repeat a literature and preprint search on the submission date.
- Check whether either construction has been independently posted or formally published.
- Distinguish carefully between the Dinitz--Garg--Goemans theorem, which remains true, and Goemans' cost-preserving conjecture, which the first certificate refutes.
- State that the Morell--Skutella costless two-sided existence conjecture is not refuted by the flow instance.

## Authorship and disclosure

- Replace the anonymous author block using `paper/author-info.tex.example`.
- Add affiliations, corresponding-author details, ORCID identifiers, funding, and acknowledgements.
- Adapt `AI_DISCLOSURE.md` to the target journal's policy.
- Ensure that every human author has independently reviewed and approved the final manuscript.

## Production

- Run `make clean && make`.
- Inspect every page of `artifacts/counterexamples.pdf`, including figure labels and bibliography links.
- Check the journal's class file, length limit, theorem style, data/code policy, and supplementary-material rules.
- Archive the exact submitted commit SHA and verification output.

## Suggested target format

The result is naturally suited to a concise combinatorial-optimization note. The final venue choice should be made by the human author after expert feedback; no journal endorsement is implied by the current generic `article` layout.
