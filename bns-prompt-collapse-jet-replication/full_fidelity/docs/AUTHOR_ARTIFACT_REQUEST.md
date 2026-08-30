# Draft request for exact-replication artifacts

Subject: Reproduction package request — Hayashi et al., PRL 134, 211407

Dear Drs. Hayashi, Kiuchi, Kyutoku, Sekiguchi and Shibata,

We are preparing an independently auditable reproduction of “Jet from Binary Neutron Star Merger with Prompt Black Hole Formation” (PRL 134, 211407; arXiv:2410.10958). We intend to preserve both an exact SACRA-MPI lineage and an independent cross-code equivalent calculation.

Could you provide, or point us to an archive containing, the following artifacts for the published production run?

1. the exact SACRA-MPI revision and any local/uncommitted patches;
2. compiler, MPI/library versions and complete build flags;
3. the LORENE initial-data file and its generation parameters;
4. the exact SFHo EOS and neutrino opacity/weak-rate tables, including hashes and interpolation settings;
5. the complete evolution input deck, grid hierarchy and regridding/moving-box rules;
6. magnetic-field seed prescription and normalisation;
7. atmosphere, floor, ceiling, primitive-recovery and magnetisation-cap settings;
8. checkpoint/restart chronology, including the Cowling transition and any manual interventions;
9. scripts/definitions used for horizon, disk, ejecta, neutrino and Poynting-flux diagnostics;
10. any reduced diagnostic time series or selected checkpoints that can serve as validation anchors.

We will preserve original authorship and licensing, cite the paper and method papers, publish hashes/provenance for all permitted artifacts, and clearly distinguish exact-lineage from independently equivalent results. Restricted access or an embargoed transfer is acceptable if public redistribution is not possible.

Kind regards,

The replication team
