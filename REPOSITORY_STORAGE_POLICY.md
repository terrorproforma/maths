# Repository-first storage and provenance policy

**Effective:** 30 August 2026  
**Maintainer:** Angus Muffatti

## 1. Canonical storage

GitHub is the durable source of truth for this research programme. Chat attachments, temporary sandboxes and generated download links are ingestion or build environments only. A file is not considered safely stored until it is committed to this repository or, for an oversized binary, attached to a documented GitHub release or Git LFS object.

## 2. One root folder per self-contained project

Every independently understandable research project receives one root-level directory using a stable kebab-case name. A project must not be split across unrelated root folders merely because it accumulated several conversations or versions.

A normal project should contain, as applicable:

```text
project-name/
├── README.md
├── sources/
├── paper/ or manuscript/
├── code/ or src/
├── tests/
├── data/ and/or results/
├── figures/
├── working/ or versioned historical packages/
└── manifest/checksum and reproduction instructions
```

Not every project needs every directory, but its README must identify the canonical source, status, author, evidence limits and reproduction path.

## 3. Iterations and historical record

Successive papers, audits and computational stages remain inside their parent project. Use versioned directories or a clearly indexed `working/`, `history/` or `original-info/` archive. Preserve superseded files when they are part of the research record.

Material corrections require one of:

- an explicit `ERRATA.md`;
- a superseding version with a cross-reference;
- a retraction/status entry in a claim matrix.

Do not silently convert a failed calculation into an apparently clean history.

## 4. Source provenance

Source conversations, briefs, external reviews and user-supplied starting material belong in `sources/` with a short provenance README. Source material is evidence of project history, not automatic evidence that its scientific claims are correct.

Third-party mathematical or scientific contributions must remain attributed in the project README, manuscript and repository-level attribution files. AI assistance must be disclosed where required; it is not authorship.

## 5. Commits and branches

Every material change is committed with a descriptive message. Large research transitions should use a branch and pull request so that the diff, review discussion and merge point remain inspectable. Generated results may be committed by CI when the generating source and workflow are also version controlled.

## 6. Reproducibility

Active code must use repository-relative paths, declare dependencies and provide a clean-checkout command. Stored-number regressions, constructed identities and independent physical validations must be labelled differently. A green CI run must not be described as scientific validation beyond what the tests can actually falsify.

## 7. Large and generated files

Files below GitHub's normal limits may be stored directly when they are useful research artefacts. Larger files must use Git LFS or a GitHub release and be linked from the project README with checksums. Build products must never be the only surviving copy of their source.

## 8. Migration staging

`_bootstrap/` is retained only as migration provenance. No new project or canonical deliverable may be stored there.
