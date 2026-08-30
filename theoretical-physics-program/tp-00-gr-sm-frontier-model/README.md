# TP-00 - The GR + Standard Model Frontier Model: Constraint and Seam Ledger

**Author:** Angus Muffatti  
**Version:** 1.0.0  
**Evidence snapshot:** 2026-08-27  
**Terminal status:** **COMPLETE AS A BASELINE / NOT A SUCCESSOR THEORY**

## Research question

What is the minimal technically correct constraint ledger for any theory claiming to supersede General Relativity plus the Standard Model without losing their verified content?

## Answer

The package treats the current baseline as a **layered effective framework**, not a unified theory:

1. Einstein-Hilbert gravity plus a cosmological constant;
2. the renormalizable Standard Model;
3. the dimension-five neutrino-mass operator required by oscillation data;
4. gravitational and matter EFT operators required for Wilsonian closure or used to parameterize possible new physics;
5. separately declared cosmological background and initial-state assumptions.

It then separates verified domains from seven logically different seam types. A naturalness complaint, a missing initial condition, an empirical anomaly and a mathematical inconsistency are never assigned the same status. Candidate theories are evaluated by independent fatal and nonfatal gates; **there is deliberately no aggregate score**.

## Strongest result

A machine-validated, importable audit standard comprising:

- an explicit baseline action and field-content ledger;
- exact one-generation anomaly checks;
- 18 seam entries tied to equations, evidence and resolution criteria;
- 29 operational successor gates across algebraic, perturbative, nonperturbative, laboratory, astrophysical, cosmological and reproducibility tiers;
- a dependency map for TP-01 through TP-16;
- deterministic code, tests, JSON results and generated figures.

## Terminal verdict

**Positive result:** the baseline acceptance framework is internally coherent and executable.  
**Negative result:** no honest scalar score can compress all successor requirements, and GR+SM cannot be represented as an already unified or UV-complete fundamental theory.  
**Open physics:** quantum gravity, vacuum energy, singularities, dark matter, dark energy microphysics, neutrino-mass origin, baryogenesis, primordial initial conditions, hierarchy, strong CP, flavour, family number, black-hole information and global gauge structure.  
**Publication status:** publishable now as a methods/standards or research-infrastructure note after expert review; it is not a new fundamental-physics discovery. A stronger journal version should blind-audit at least TP-01 and TP-02 using the frozen YAML gates.  
**Next decisive calculation:** no additional TP-00 calculation is required. Apply the gates to a concrete successor by computing its linearized spectrum, constraint algebra, anomaly polynomial and low-energy matching residuals before any expensive phenomenology.

## Reproduce

The one-command build regenerates tables and figures, compiles both PDFs, runs the invariant verifier and unit tests, and writes a SHA-256 manifest:

```bash
python -m pip install -r requirements.txt
make all
```

Equivalent explicit sequence:

```bash
python code/generate_latex_tables.py --root .
python code/generate_figures.py --root .
cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error minimum_viable_successor_checklist.tex
cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error frontier_model_constraint_ledger.tex
cp paper/minimum_viable_successor_checklist.pdf .
cp paper/frontier_model_constraint_ledger.pdf .
python code/verify_frontier_model.py --root .
python -m unittest discover -s tests -v
python code/build_manifest.py --root .
```

The verifier writes `results/verification_results.json` and `results/numerical_diagnostics.json`, and exits nonzero on a failed invariant. Figures are generated from the machine-readable ledgers; their underlying arrays are stored in `results/benchmark_arrays.npz`.

## Key files

- `frontier_model_action.tex` - complete layered action and conventions.
- `seam_ledger.csv` - equation-level seam taxonomy.
- `successor_acceptance_tests.yaml` - importable gate schema and candidate template.
- `known_limits.md` - operational recovery limits.
- `minimum_viable_successor_checklist.md` and `.pdf` - one-page audit.
- `dependency_map.csv` / `.md` - TP-01 through TP-16 mapping.
- `frontier_model_constraint_ledger.pdf` - compiled technical paper; editable source is in `paper/`.
- `source_ledger.csv` and `notation_ledger.csv` - source/version and convention provenance.
- `claim_novelty_acceptance_matrix.csv` - epistemic status and novelty boundary.
- `tables/` and `figures/` - generated paper inputs.
- `results/verification_results.json`, `results/numerical_diagnostics.json`, and `results/benchmark_arrays.npz` - machine-readable checks and arrays.
- `manifest_sha256.csv` - distributable-file checksums.
- `code/` and `tests/` - executable validation, table generation, figures and tests.

## Scope warning

The ledger is intentionally conservative. It does not treat every open question as an internal contradiction, does not declare a precision tension solved, and does not use novelty as a criterion of physical success.
