# Solver-neutral field-output contract

Cross-code comparisons fail surprisingly often because two files use the same field name but different units, staggering or metric conventions. E-track outputs therefore pass through a minimal HDF5 interchange contract.

## Root attributes

Every snapshot declares:

- `contract_version`;
- `campaign_id` and `solver`;
- `coordinate_system`;
- `length_unit`, `mass_unit` and `time_unit`;
- the exact simulation time in `/meta/time_s` measured relative to merger.

## Coordinates

`/coordinates/x`, `/coordinates/y` and `/coordinates/z` contain one-dimensional cell-centre coordinates. AMR-native output may remain in the solver’s native format, but any exported comparison snapshot must state the resampling method and preserve conservative integrals where applicable.

## Required three-dimensional fields

- `/fields/rho` — rest-mass density;
- `/fields/pressure`;
- `/fields/temperature`;
- `/fields/ye`;
- `/fields/b_squared` — \(b^\mu b_\mu\) in the declared unit convention;
- `/fields/u_t` — covariant temporal component;
- `/fields/sqrt_gamma`;
- `/metric/lapse`.

Additional velocity, magnetic-vector, radiation, metric and mask fields are expected for complete diagnostics. The minimal set is deliberately too small to replace native checkpoints.

## Validation

```bash
python -c 'from bnsjet.field_contract import validate_field_snapshot; print(validate_field_snapshot("snapshot.h5"))'
```

A production exporter must also include an accompanying JSON record containing native source files, interpolation/restriction method, coordinate map and hashes.
