# Primary sources

The replication target is defined from primary sources only. Secondary articles are useful for orientation but do not control numerical choices.

## Target calculation

1. K. Hayashi, K. Kiuchi, K. Kyutoku, Y. Sekiguchi and M. Shibata, **“Jet from Binary Neutron Star Merger with Prompt Black Hole Formation,”** *Physical Review Letters* 134, 211407 (2025). DOI: `10.1103/PhysRevLett.134.211407`.
2. arXiv manuscript and source: `arXiv:2410.10958`.
3. APS supplemental material attached to the PRL article.
4. The official visualisation distributed with the paper/institutional release, analysed under `../reduced_order/`.

## Method lineage to freeze for X-track

The paper identifies SACRA-MPI and its numerical-method references. The exact replication must additionally freeze:

- the precise SACRA-MPI source revision and local patches;
- compiler, MPI implementation, flags, math libraries and architecture-dependent options;
- LORENE initial-data binary and the LORENE revision used to produce it;
- finite-temperature SFHo table as an exact byte sequence;
- neutrino interaction, opacity and weak-rate tables as exact byte sequences;
- grid hierarchy, regridding/moving-box policy and domain decomposition;
- atmosphere, density/temperature/electron-fraction floors and ceilings;
- reconstruction, Riemann-solver, constrained-transport and metric-evolution switches;
- checkpoint lineage and every manual intervention.

A literature citation is not a substitute for those artifacts. Their absence is recorded rather than guessed.

## Independent-equivalence lineage

E-track may use a different implementation only after it passes the test ladder and the cross-code equivalence gates in `../full_fidelity/docs/VALIDATION_MATRIX.md`. The governing equations, microphysics, initial data, effective resolution and diagnostics must be held fixed before code-to-code comparisons are meaningful.
