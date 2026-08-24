# Source and Provenance Statement

## Basis of the consolidation

The consolidated manuscript was prepared from three source layers:

1. **Current local source snapshot** - `sources/Photon_Perspective_in_Relativity_chat_snapshot.txt`, copied from the file attached to this conversation.
2. **Staged project records** - the v0.1-v1.4 manuscripts, LaTeX/Markdown sources, verification scripts, result JSON files, matrices, and figures surfaced in the project File Library and the first-chat transcript.
3. **Literature ledger** - the references cited by those staged records, normalised in `data/source_ledger.csv` and `references.bib`.

The text preserves the project vocabulary and sequence of corrections. It does not merge mutually inconsistent historical numbers without comment. Where a later version superseded an earlier benchmark, the later result is used in the integrated benchmark table and the earlier value remains in the correction ledger. One small v1.2 rounding inconsistency in the displayed value of `tan(theta)` is explicitly recorded.

## Metadata quality flags

The `metadata_provenance` column in `data/source_ledger.csv` distinguishes:

- metadata taken from the project bibliography;
- metadata checked against a primary arXiv record;
- abbreviated records retained exactly because the staged source did not supply a full journal citation.

A source appearing in the ledger does not imply that every claim in the manuscript was independently replicated. The manuscript labels results as established, derived, numerically verified, conditional, failed, or open.

## Historical working files

`data/historical_artifact_inventory.csv` contains the complete filename inventory named across v0.1-v1.4. These items include manuscripts, source files, verification scripts, matrices, numerical arrays, figures, and per-version ZIP packages.

Historical sandbox links are session-scoped. Unless a historical file was locally present in the active runtime, no byte-for-byte copy was invented. Each unavailable item is marked `inventory_only`. The new archive contains reproducible consolidated replacements rather than counterfeit historical binaries.

## Verification boundary

`scripts/verify_consolidated_chronometry.py` checks workstation-scale identities and benchmark consistency, including:

- crossed-null clock/ruler algebra;
- null scale/rapidity decomposition;
- soft-null speed relation;
- universal factorisation and rank-one response;
- the telescoping `2/27` QCD coefficient;
- `Z6` harmonic cancellation and mass scaling;
- the environmental compactness bound;
- reheating phasor and dark-radiation arithmetic;
- cascade branch reconstruction;
- RG cancellation of the explicit matching logarithm;
- the direct-AMY hierarchy.

It does not reproduce the unresolved full electroweak/Yukawa LPM problem, non-Abelian `3+1D` 2PI/Kadanoff-Baym evolution, multi-field tunnelling, nonperturbative spectral reconstruction, complete anomaly classification, or quantum-gravity completion.
