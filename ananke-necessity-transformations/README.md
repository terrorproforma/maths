# ANANKE v0

**Author:** Angus Muffatti  
**Research and implementation assistance:** OpenAI models, disclosed as computational assistance.

**ANANKE** is an executable attempt to extract the part of a process that survives
changes of representation.

The primitive input is not a state vector or equation. It is a behavioural oracle

\[
f(w)=\text{observed scalar after applying operation word }w.
\]

From finite sequence data, v0 constructs the behavioural Hankel matrix

\[
H(u,v)=f(uv)
\]

and uses a spectral factorization to recover a minimal reachable-observable linear
process. Minimal realizations are unique only up to invertible similarity; that
ambiguity is treated as representation, not ontology.

## First experiment

A single qubit with x- and z-axis rotations is written in three ways:

1. a physical four-dimensional Pauli-transfer representation;
2. a randomly scrambled gauge; and
3. a seven-dimensional representation padded with three unreachable hidden modes.

The three descriptions agree on every tested sequence probability. The extractor
must recover rank four from each, reproduce held-out words, and recover the physical
transformations up to similarity.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python experiments/qubit_v0.py
python experiments/classical_obstruction_v0.py
python -m unittest discover -s tests -v
```

The experiment writes `results/qubit_v0.json`.

## First obstruction certificate

`experiments/classical_obstruction_v0.py` extracts the gate spectra and uses a
Perron--Frobenius obstruction. The exact rational-radian rotation phases are not
roots of unity, whereas every unit-modulus eigenvalue of a finite stochastic
matrix must be one. The process therefore has no exact finite-state classical
stochastic realization, although its qubit realization is explicit. See
[`docs/obstruction_01.md`](docs/obstruction_01.md).

## Current scope

v0 handles exact, finite-rank, scalar sequential processes. It does not yet solve:

- statistical rank selection under finite-shot noise;
- continuous-time processes;
- contextual or adaptive instruments;
- typed multi-system circuit composition;
- classical versus quantum versus GPT realizability;
- uniqueness beyond the declared experimental interface.

Those are the next stages, not concealed assumptions.

## Core definition

See [`docs/research_program.md`](docs/research_program.md) for the basis-free
necessity core, hypotheses, failure conditions, and research ladder.

## Technical ancestry

The implementation combines established ideas rather than pretending the machinery
fell from the sky:

- finite-rank Hankel/quasi-realization theory;
- weighted-automaton spectral realization;
- reachability and observability minimization;
- operational equivalence and GPT quotienting;
- gauge freedom in gate-set tomography;
- process-theoretic composition.

The proposed contribution is the adversarial research programme: vary model language
and ontology aggressively, extract the common minimal process, and treat surviving
structures and realizability obstructions as candidates for necessity.
