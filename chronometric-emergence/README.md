# Null-Relational Chronometry - Consolidated Research Package

**Author: Angus Muffatti**

This archive consolidates the full research chain developed from the original photon-frame discussion through the v1.4 transport calculation.

## Primary deliverables

- `chronometric_emergence_full_manuscript.pdf` - publication-style consolidated manuscript.
- `chronometric_emergence_full_manuscript.docx` - editable Word text with renderer-safe display-equation images; the Markdown and LaTeX contain the editable equations.
- `chronometric_emergence_full_manuscript.tex` - generated LaTeX source used for the PDF.
- `chronometric_emergence_full_manuscript.md` - canonical editable source.
- `references.bib` - consolidated bibliography.

## Working files

- `scripts/build_support.py` regenerates the data ledgers and manuscript figures.
- `scripts/verify_consolidated_chronometry.py` checks the principal exact identities and benchmark arithmetic.
- `scripts/prepare_docx_math.py` renders display equations from the canonical TeX into tightly cropped images for reliable Word/LibreOffice layout.
- `scripts/centre_docx_images.py` centres standalone equation and figure images in the DOCX.
- `data/consolidated_verification_results.json` records all verification results.
- `data/benchmark_parameters.json` contains the integrated benchmark values.
- `data/source_ledger.csv` records the literature sources, their role, and metadata provenance.
- `data/version_crosswalk.csv` maps every research version to its decisive result and correction.
- `data/integrated_acceptance_matrix.csv` records PASS, FAIL, CONDITIONAL, and OPEN outcomes.
- `data/historical_artifact_inventory.csv` lists every historical working filename named in the staged chat.
- `figures/` contains the consolidated figures.
- `sources/Photon_Perspective_in_Relativity_chat_snapshot.txt` is the locally available source-chat snapshot.

## Reproduction

From this directory:

```bash
./reproduce.sh
```

The script regenerates figures and ledgers, runs the verification suite, rebuilds the LaTeX, PDF, and DOCX versions, and updates the SHA-256 manifest. It requires Python 3, NumPy, SymPy, Matplotlib, Pandoc, XeLaTeX, and LibreOffice for DOCX rendering.

## Scientific status

This is a technical research manuscript, not a peer-reviewed paper. It deliberately preserves negative results and superseded assumptions:

- the photon has no physical rest frame;
- the original exact-null action fails its transverse principal-symbol test;
- the direct crossed-phase composite metric is mimetic and singular;
- the original Planck-scale cosmological benchmark does not generically select the vacuum and overcloses under generic displacement;
- the naive reheaton branch and the direct bosonic inflaton portal were superseded;
- Einstein gravity, the full electroweak/Yukawa LPM calculation, a complete non-Abelian two-time calculation, and an absolute novelty claim remain open.

The strongest current claim is that universal operational duration exists precisely when all physical clock spectra factorise through one common local scalar. The Weyl-invariant obstruction is chronometric shear. A controlled QCD threshold defect transmits into this shear with the leading coefficient `2/27`, while a protected `Z6` cosmology supplies one conditional realisation.

## Historical-file limitation

Earlier chat turns named many PDFs, source files, scripts, arrays, and ZIP archives. Their old `sandbox:/...` links were ephemeral and are not assumed to be locally recoverable now. This archive therefore contains:

1. a complete new consolidated manuscript and editable sources;
2. regenerated consolidated data, figures, verification, and build files;
3. the locally available chat snapshot;
4. a precise inventory of every historical filename and version.

It does **not** falsely claim that every historical binary was recovered byte-for-byte. See `SOURCE_PROVENANCE.md`.
