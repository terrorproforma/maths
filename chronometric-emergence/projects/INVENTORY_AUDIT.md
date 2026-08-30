# Chronometric-emergence storage audit

**Audit date:** 30 August 2026  
**Repository:** `terrorproforma/maths`  
**Default branch at audit start:** `main` at `97bd3d968e293b9d79ed58f6097c88de44da9e6f`

## Audit result

The substantive project record was already present in Git, but it was fragmented across `main` and three historical branches:

- `main` contained `chronometric-emergence/original-info/`, with recovered original packages from v0.1 through v1.9 and the source conversation.
- `chronometric-response-history` contained the numbered, self-contained working folders v0.1 through v1.8.
- `chronometric-frontier-evidence-v2` contained the current adversarial evidence-repair suite.
- `chronometric-frontier-repair-v2` retained its bootstrap/source archive history.

Two organisation defects were found:

1. the programme README on `main` linked to `frontier-evidence-v2/`, but that directory existed only on the evidence branch;
2. the numbered self-contained folders existed only on the response-history branch, while `main` exposed the less navigable `original-info/` archive.

This commit fixes both defects without regenerating or altering historical research artefacts. Existing Git trees are reused byte-for-byte.

## Git-object provenance

| Material | Source Git tree | Main destination |
|---|---|---|
| Original packages v0.1-v1.9 | `1b2f260d7cce866fae0c461cb7b91bcb1291e1e6` | `../original-info/` |
| Numbered working projects v0.1-v1.8 | `cc75f7302ce8c54df27211eaf2f5657ac3a7f094` | this directory |
| v1.9 production-theory package | `c974eae9035f7254b66021c0798b611b0e9ac6b8` | `19-v1.9-production-theory-closure/` |
| Source conversation | `d3157c90d3e072e96a454be990de12f2f7dcb345` | `00-photon-frame-foundations/` and `../sources/` |
| Current evidence repair v2 | `e10c31cf3ab97766e5e448220b405787249696b5` | `20-frontier-evidence-v2/` and `../frontier-evidence-v2/` |
| Historical consolidated response tree | `8e4165f2926b964073df53cc4c13c6668c0e04cf` | retained on branch `chronometric-response-history` |

## Completeness check

The numbered sequence is continuous:

```text
00 source foundations
01 v0.1
02 v0.2
03 v0.3
04 v0.4
05 v0.5
06 v0.6
07 v0.7
08 v0.8
09 v0.9
10 v1.0
11 v1.1
12 v1.2
13 v1.3
14 v1.4
15 v1.5
16 v1.6
17 v1.7
18 v1.8
19 v1.9
20 evidence repair v2
```

The recovered originals include papers, LaTeX/Markdown sources, verification code, machine-readable results, numerical arrays, figures, matrices and launch specifications where they were generated. Binary objects are referenced by their existing Git blob/tree SHAs rather than re-uploaded, so the organised folders and original archive are byte-identical where they share an artefact.

## Epistemic warning

Completeness of storage is not validation of the physics. The current evidence status is controlled by `20-frontier-evidence-v2/`, whose errata retract or narrow several historical claims. In particular:

- v1.3's claimed RG cancellation is retracted;
- v1.4 transport numbers are deprecated;
- v1.7-v1.8 off-shell kernels are model/initialisation families rather than calculated physical uncertainty bands;
- v1.9 specifies a solver but does not implement the claimed non-Abelian three-loop 3PI/Kadanoff-Baym pilot;
- the archived cosmological low-`f_a` ridge is blocked by compact-object conversion.

Historical artefacts remain intact for provenance and should not be silently rewritten to match later conclusions.