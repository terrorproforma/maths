# HPC and storage architecture

The reported calculation is leadership-class. The campaign tooling therefore assumes failures, queue limits and petascale data movement rather than treating them as surprises.

## Execution model

- MPI-first domain decomposition with optional threading/GPU execution as supported by the selected solver.
- scheduler templates for Slurm and Fugaku-style PJM;
- segmented jobs with signal-aware checkpointing;
- immutable run snapshots separated from mutable scratch;
- checksummed checkpoint promotion from scratch to durable storage;
- analysis performed from reduced diagnostics wherever full-volume fields are unnecessary.

## Output tiers

1. **Tier 0 — restart state:** enough to restart exactly; highest durability.
2. **Tier 1 — native diagnostics:** horizon, flux surfaces, wave extraction, budgets and spectra at high cadence.
3. **Tier 2 — sparse 3D fields:** cadence chosen for turbulence, jet propagation and rendering.
4. **Tier 3 — derived products:** slices, spherical maps, histograms and movies.

Do not save full 3D state at movie-frame cadence merely because the reference movie has 431 frames. Rendering cadence and checkpoint cadence solve different problems.

## Resource model

`bnsjet estimate-resources` anchors estimates to the reported reference CPU-hours and scales resolution using a configurable exponent. This is only a planning model. Actual throughput must be measured with production-like weak/strong-scaling pilots, including neutrino transport and I/O.

## Failure recovery

Every segment must:

- checkpoint before scheduler wall-time;
- emit a machine-readable completion record;
- record rank/thread/GPU topology;
- hash promoted checkpoints;
- refuse to overwrite an existing successful segment;
- log any floor-policy or solver-fallback threshold changes as a new campaign lineage.
