# Generated artifacts

The following outputs are generated from committed source and are rebuilt by `.github/workflows/tp-project-packages.yml`:

- `frontier_model_constraint_ledger.pdf`
- `minimum_viable_successor_checklist.pdf`
- `paper/*.pdf`
- `figures/*.png`
- `figures/*.pdf`
- `results/benchmark_arrays.npz`
- `dist/TP-00_GR_SM_frontier_model_v1.0.zip`
- `dist/TP-00_GR_SM_frontier_model_v1.0.zip.sha256`

Reproduce locally with:

```bash
python -m pip install -r requirements.txt
make all
```

The generated release archive excludes its own `dist/` directory to avoid recursive packaging.
