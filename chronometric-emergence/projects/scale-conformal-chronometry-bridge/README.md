# Scale/conformal symmetry and the chronometry bridge

**Author:** Angus Muffatti  
**Date:** 10 October 2026  
**Status:** v0.1 applicability audit; AI-assisted and not independently reviewed.

## Result

OpenAI's scale-to-conformal theorem cannot be directly applied to our nonzero scale-selecting vacuum. Its exact dilation-invariant-vacuum assumption fails there. Its improvement scalar is not automatically a positive clock-setting field.

A separate conditional bridge survives: along a dilation-related family of homogeneous vacua, with every independent dimensionless datum held fixed, physical spectral locations scale as `M_A = f c_A`. This uses ordinary dilation covariance, not the new enhancement proof. Promoting `f` to a varying field requires a further derivative/state audit.

The accompanying calculation provides a classical two-scalar example, a Coleman-Weinberg trace test, a QCD renormalization-scale-versus-physical-lock diagnostic, and a finite-gradient oscillator benchmark. It does not establish the operational-net hypotheses, a UV completion, or an independent verification of the OpenAI manuscript.

## Reproduce

From this directory:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python verify.py
```

The script writes `results.json` and exits unsuccessfully if a check fails. The recorded run passes 32 checks: 21 symbolic identities and 11 numerical benchmark gates. These are evidence only for the stated identities and oscillator system, not a theorem verifier or experimental validation.

## Files

- `research_note.md`: full derivations, limitations, results and the next model-specific calculation.
- `assumptions.csv`: requirement-by-requirement applicability map.
- `sources.json`: source paths, versions and attribution.
- `verify.py`: complete executable checks and oscillator calculation.
- `results.json`: recorded results and dependency versions.
- `requirements.txt`: versions used for the recorded run.

The canonical previous audit remains `../../frontier-evidence-v2/docs/FRONTIER_EVIDENCE_REPORT.md`. Its non-Abelian, cosmological and UV-completion blockers are not changed.
