# ANANKE v1

**Author:** Angus Muffatti  
**Research and implementation assistance:** OpenAI models, disclosed as computational assistance.

**ANANKE** extracts the part of a sequential process that survives changes of
representation, then asks how expensive alternative realization classes must become
to reproduce it.

The primitive input is operational behaviour:

\[
f(w)=\Pr(1\mid\text{operation word }w).
\]

No Hilbert space, hidden states, preferred coordinates or equations of motion are
assumed at the input.

## What v1 adds

V0 recovered exact finite-rank behaviour up to simultaneous similarity and proved an
exact no-finite-classical-realization result for a qubit rotation process.

V1 makes the programme finite-data and graded:

1. simulates or ingests binomial counts for operation words;
2. constructs empirical Hankel and shifted Hankel blocks;
3. selects predictive rank on longer held-out words;
4. bootstraps similarity-invariant transition eigenmodes;
5. compares their confidence disks with stochastic-matrix eigenvalue regions;
6. returns lower bounds on the hidden states required by any exact finite classical
   realization;
7. exposes the continued-fraction arithmetic controlling those bounds.

## Baseline result

For a qubit with two controlled rotations, every word through length nine was
measured with 10,000 synthetic shots:

- 1,023 measured words;
- 10,230,000 Bernoulli trials;
- selected Hankel rank: **4**;
- rank-four bootstrap frequency: **100/100**;
- 99% analytic classical-memory lower bound: **9 states**;
- 99% convergence-guarded full Karpelevič lower bound: **16 states**.

The exact synthetic eigenmode lies inside the reported confidence disk.

A known three-state classical cycle was then used as a boundary calibration. Across
100 independent datasets, the nominal 99% full-region test falsely excluded the true
three-state model once. A damped three-state cycle was also correctly retained.

## The arithmetic surprise

The chosen rotation phase satisfies

\[
\frac{0.73}{2\pi}=[0;8,1,1,1,1,5,\ldots],
\]

so its early finite-classical thresholds follow near-Fibonacci denominators

\[
8,9,17,26,43,\ldots
\]

and sit only 0.000926 radians from the noble phase

\[
[0;8,\overline{1}].
\]

This suggests deliberate **Diophantine gate design**: choose transformations whose
phases resist low-denominator rational approximation over the classical-memory range
one wants to exclude.

## Repository map

```text
src/ananke/
  process.py          finite-dimensional linear process coordinates
  hankel.py           exact spectral realization
  observations.py     finite-shot word-count datasets
  rank_selection.py   held-out rank selection and bootstrap stability
  bootstrap.py        confidence regions for invariant spectral modes
  karpelevich.py       stochastic eigenvalue regions and state-count bounds
  diophantine.py       continued fractions and finite-cycle approximants
  invariants.py        similarity-invariant fingerprints
  obstructions.py      exact v0 peripheral-spectrum obstruction
  examples.py          qubit and finite classical cycle examples

experiments/
  qubit_v0.py
  classical_obstruction_v0.py
  noisy_qubit_v1.py
  calibration_v1.py
  shot_scaling_v1.py
  arithmetic_staircase_v1.py
  plot_eigenmode_regions_v1.py

results/
  noisy_qubit_v1.json
  calibration_v1.json
  shot_scaling_v1.json
  arithmetic_staircase_v1.json
  eigenmode_regions_v1.png
  shot_scaling_v1.png
  root_approximation_staircase_v1.png
  karpelevich_gap_staircase_v1.png
```

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

python experiments/qubit_v0.py
python experiments/classical_obstruction_v0.py
python experiments/noisy_qubit_v1.py
python experiments/calibration_v1.py
python experiments/shot_scaling_v1.py
python experiments/arithmetic_staircase_v1.py
python experiments/plot_eigenmode_regions_v1.py

python -m unittest discover -s tests -v
```

The core package depends only on NumPy. Plotting experiments additionally require
Matplotlib.

## Read next

- [`docs/research_program.md`](docs/research_program.md): basis-free necessity core.
- [`docs/noisy_inference_v1.md`](docs/noisy_inference_v1.md): finite-shot pipeline.
- [`docs/obstruction_02_karpelevich.md`](docs/obstruction_02_karpelevich.md): classical
  state-count certificate.
- [`docs/arithmetic_necessity_v1.md`](docs/arithmetic_necessity_v1.md): continued
  fractions and experimental design.
- [`docs/formal_core_v1.md`](docs/formal_core_v1.md): propositions, proof sketches and
  the ontology-cost definition.
- [`docs/research_status_v1.md`](docs/research_status_v1.md): epistemic status,
  candidate contribution and v2 target.

## Epistemic status

The ingredients have substantial prior art: Hankel realization, observable dimension
inference, hidden Markov realization, classical/quantum memory gaps and Karpelevič
regions are established mathematics.

The candidate contribution is their integration into an adversarial finite-data
pipeline that returns an **ontology-cost profile** rather than a preferred model.
The current full-region certificate is convergence-checked floating-point numerics,
not interval-certified proof. Bootstrap coverage is empirically calibrated but not
yet established uniformly.
