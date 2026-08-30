# Chronometric Emergence storage policy

This project follows [`../REPOSITORY_STORAGE_POLICY.md`](../REPOSITORY_STORAGE_POLICY.md).

## Canonical locations

- `sources/` stores the source conversation, briefs and independent reviews.
- `original-info/` is the immutable recovered v0.1-v1.9 historical archive.
- `frontier-evidence-v2/` is the active post-audit calculation and evidence layer.

New work belongs in one of those locations or in a clearly named new subproject directory inside `chronometric-emergence/`. A genuinely independent paper or research programme should instead receive its own root-level repository folder.

No paper, code file, array, result or review is considered durably stored while it exists only in a chat attachment or sandbox path. Historical packages are not silently edited; corrections live in errata, source-control commits and superseding evidence packages.
