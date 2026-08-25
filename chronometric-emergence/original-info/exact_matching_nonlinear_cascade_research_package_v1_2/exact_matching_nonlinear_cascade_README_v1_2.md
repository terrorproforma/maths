# Exact Transient Matching and Nonlinear Reheating Cascade v1.2

## Contents

- `exact_matching_nonlinear_cascade_v1_2.pdf` - rendered technical paper.
- `exact_matching_nonlinear_cascade_v1_2.md` - editable Markdown source.
- `exact_matching_nonlinear_cascade_v1_2.tex` - complete LaTeX source.
- `verify_exact_matching_cascade_v1_2.py` - symbolic, high-precision, preheating, and radial momentum-lattice verification code.
- `exact_matching_cascade_results_v1_2.json` - machine-readable headline results.
- `exact_matching_cascade_arrays_v1_2.npz` - numerical arrays from the momentum-lattice calculation.
- `exact_matching_cascade_acceptance_matrix_v1_2.csv` - requirement/status matrix.
- `exact_matching_cascade_benchmark_v1_2.csv` - benchmark parameters and outputs.
- `exact_matching_cascade_runlog_v1_2.txt` - final verification run summary.
- PNG files - figures used in the paper.

## Reproduce the numerical results

```bash
python verify_exact_matching_cascade_v1_2.py
```

The Python calculation uses a radial momentum lattice and an energy-conserving quantum-BGK collision closure. It is not a full non-Abelian 3+1-dimensional two-time 2PI/Kadanoff-Baym calculation.

## Scope of the exact matching result

The quoted `I3` is the exact zero-external-momentum factorised matching function in the explicitly normalised scalar proxy used in the paper. Full Standard Model gauge, doublet, multiplicity, and RG-improvement effects remain separate calculations.
