# Repository-first storage and provenance policy

**Maintainer:** Angus Muffatti

## Canonical storage

GitHub is the durable source of truth for this research repository. Chat attachments, temporary sandboxes, notebook state and generated download links are ingress or build environments only. Work is not considered safely stored until the relevant source, inputs, code, results and status notes are committed here, or an oversized binary is attached through a documented Git LFS/release workflow.

## Project structure

Every independently understandable project gets one stable project directory. Independent programmes normally live at repository root. Research stages that are inseparable parts of an existing programme may live as self-contained subdirectories inside that programme root; for example, TP-00 through TP-16 live under `theoretical-physics-program/`, while Chronometric Emergence stages live under `chronometric-emergence/projects/`.

A normal project should contain, as applicable, a README, sources/provenance, manuscript material, code, tests, data/results, figures and reproduction instructions.

## Historical record and corrections

Historical iterations remain versioned rather than silently rewritten. Material corrections require an explicit erratum, a superseding version with a cross-reference, or a machine-readable status/claim update. Third-party contributions retain attribution; AI assistance is disclosed where required and is not authorship.

## Commits and branches

Every material change ends in a descriptive Git commit. Large or risky changes should use a branch and pull request. Generated results may be committed by CI only when the generating source, inputs and workflow are themselves version controlled.

## Reproducibility

Active code uses repository-relative paths, declares dependencies and provides a clean-checkout command. Stored-number regressions, identities, independent recomputations, convergence tests and external validation must be labelled distinctly. A green CI run is evidence only for what its tests can actually falsify.

## Large files

Generated binaries must never be the only surviving copy of their source. Files above ordinary repository limits belong in Git LFS or a documented release, with checksums and links from the relevant project README.

## Migration staging

`_bootstrap/` is migration provenance only. No new canonical project or deliverable belongs there.
