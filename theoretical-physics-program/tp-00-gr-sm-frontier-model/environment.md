# Reproduction environment

The package was validated on **Python 3.13.5** with:

- PyYAML 6.0.3
- pandas 2.2.3
- matplotlib 3.10.8
- NumPy 2.3.5

The paper was compiled using **pdfTeX 1.40.26**, **Biber 2.20** and **latexmk 4.86** from the installed TeX Live 2025/development distribution. The Python code has no random branch; no seed is required. All source data are frozen to the `2026-08-27` evidence snapshot and identified in `source_ledger.csv`.

Reproduction is supported on a newer compatible environment, but a byte-identical PDF is not guaranteed across TeX/font versions. Numerical JSON/NPZ and CSV/YAML semantics are the canonical machine outputs.
