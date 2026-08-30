# ANANKE: extracting transformations that cannot be otherwise

## 1. Operational starting point

Choose an intervention alphabet \(\Sigma\). A finite word

\[
w=a_1a_2\cdots a_k\in\Sigma^*
\]

means: prepare the system, apply the declared transformations in order, then
perform the declared observation. The only primitive datum is the resulting
scalar behaviour

\[
f:\Sigma^*\rightarrow\mathbb R.
\]

For a binary measurement, \(f(w)\) is an outcome probability. The programme
does **not** initially assume a Hilbert space, particles, fields, coordinates,
or hidden states.

## 2. The canonical predictive core

For each prefix \(u\), define its future-response function

\[
r_u(v)=f(uv).
\]

Two histories are operationally identical when they induce the same response
to every admitted continuation. Define

\[
\mathcal R_f=\operatorname{span}\{r_u:u\in\Sigma^*\}.
\]

Every operation \(a\in\Sigma\) induces a transformation

\[
T_a r_u=r_{ua}.
\]

The empty history gives \(r_\epsilon\), and evaluation at the empty continuation
provides \(\varepsilon(r_u)=f(u)\). The basis-free tuple

\[
\mathfrak N(f)=
(\mathcal R_f,r_\epsilon,\varepsilon,\{T_a\}_{a\in\Sigma})
\]

is the v0 candidate for a **necessity core**.

It is not metaphysical necessity without qualification. It is what is forced by:

1. the admitted interventions;
2. the admitted observations;
3. exact sequential composition; and
4. the chosen equivalence tolerance.

Changing that interface can refine or enlarge the core. This relativity is not a
bug: a claim that something “cannot be otherwise” is meaningless until the
counterfactual variations have been specified.

## 3. Hankel form

The behavioural Hankel operator is

\[
H_f(u,v)=f(uv).
\]

Its row space is \(\mathcal R_f\). If \(\operatorname{rank}H_f=n<\infty\), then:

- an \(n\)-dimensional linear realization exists;
- no lower-dimensional linear realization reproduces all words; and
- minimal reachable-observable realizations differ only by invertible similarity.

Coordinates therefore vary as

\[
\alpha' = \alpha S,\qquad
B'_a=S^{-1}B_aS,\qquad
\omega'=S^{-1}\omega,
\]

while every observable value

\[
f(w)=\alpha B_w\omega
\]

remains fixed.

The necessity object is not a preferred matrix. It is the simultaneous similarity
class—or, more cleanly, the abstract Hankel row space with its shift operators.

## 4. What v0 tests

The first synthetic process is a qubit with two noncommuting rotations and one
prepare-measure interface. It is rendered as:

1. a four-dimensional homogeneous Bloch/Pauli-transfer description;
2. a randomly scrambled invertible coordinate system; and
3. a seven-dimensional description containing three unreachable hidden modes.

All three generate the same probabilities. The extractor sees only those
probabilities. A successful run must:

- detect Hankel rank four;
- discard the three hidden dimensions;
- predict held-out longer sequences;
- recover transformation matrices similar to the physical Pauli-transfer maps;
- preserve spectra, characteristic polynomials, fixed-space dimensions, and
  traces of transformation words.

## 5. Falsifiable hypotheses

### H1 — exact finite-core recovery

For exact finite-rank behaviour and sufficiently rich prefix/suffix sets, spectral
Hankel extraction recovers the minimal process up to similarity.

**Failure condition:** held-out sequence errors remain nonzero after increasing the
Hankel basis, or extracted ranks disagree across exactly equivalent descriptions.

### H2 — representational ornament is removable

Invertible coordinate changes and unreachable/unobservable hidden dynamics do not
alter the extracted core.

**Failure condition:** a coordinate scramble changes any similarity invariant, or
hidden padding raises the exact Hankel rank.

### H3 — experimental enrichment is monotone

Adding genuine interventions or measurements may split operational equivalence
classes and increase the core, but cannot invalidate predictions on the original
interface.

**Failure condition:** the enriched model cannot restrict consistently to the old
behaviour.

### H4 — ontology appears as a realizability constraint, not as raw coordinates

The same operational core may admit classical, quantum, generalized-probabilistic,
or no finite realization within a selected physical model class. What is forced is
captured by feasibility and obstruction results over those classes.

**Failure condition:** purportedly different model classes are distinguished only by
coordinate conventions rather than invariant feasibility conditions.

## 6. Research ladder

### Phase 0 — exact sequential processes

Finite alphabet, scalar outputs, exact synthetic data, finite Hankel rank.

### Phase 1 — noisy operational extraction

Use finite-shot binomial data, weighted low-rank estimation, bootstrap confidence
intervals, held-out sequence prediction, and rank-stability diagrams.

### Phase 2 — adversarial representations

Automatically generate gauge transformations, redundant embeddings, nonlinear
coordinate charts, hidden-state models, and alternative classical/quantum/GPT
realizations. Search for purported invariants and actively try to destroy them.

### Phase 3 — positivity and convex geometry

Recover the minimal and maximal invariant cones compatible with the process.
Determine whether classical simplicial cones, quantum semidefinite cones, or only
more general GPT cones can realize the operational core.

### Phase 4 — typed composition

Replace strings by typed circuits. Infer which tensor, parallel-composition, causal,
or compact structures are actually forced by observed composition rather than
inserted by the theorist.

### Phase 5 — obstruction atlas

Catalogue structures that survive all admitted realizations and structures whose
existence is impossible. No-go results become first-class outputs: necessity can
appear as the impossibility of consistently deleting a relation.

## 7. The sharper philosophical claim

The programme does not ask an optimiser to invent a beautiful ontology. It asks an
adversary to erase structure while preserving every possible intervention-response
relation. What survives repeated successful erasure is the candidate necessity.

In compact form:

\[
\boxed{
\text{necessity}=
\text{minimal compositional predictive structure modulo every observationally silent change}
}
\]

## 8. Status after ANANKE v1

Phase 1 is now implemented in prototype form:

- finite-shot binomial word data;
- held-out predictive rank selection;
- bootstrap rank stability;
- bootstrap confidence disks for invariant eigenmodes;
- analytic and numerical finite-classical state-count lower bounds;
- boundary-model false-positive calibration.

Phase 2 has begun through adversarial classical cycle and damped-cycle controls.
The continued-fraction analysis also adds an experimental-design branch not present
in the original ladder: choose transformations to maximize the cost of low-complexity
counterfeit ontologies.

The programme's next canonical object is therefore not merely
\(\mathfrak N(f)\), but the pair

\[
\boxed{
\left(
\mathfrak N(f),
\{C_{\mathcal O}(f;\varepsilon,\mathcal W)\}_{\mathcal O,\varepsilon,\mathcal W}
\right),
}
\]

combining the representation-invariant predictive core with its ontology-cost
profiles.
