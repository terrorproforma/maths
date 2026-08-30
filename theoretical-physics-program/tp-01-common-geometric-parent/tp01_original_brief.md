# Standalone Agent Prompt — TP-01

## Project title

**A Common Geometric Parent for Einstein–Hilbert and Chern–Simons/Transgression Actions**

## Instruction to the agent

This is a self-contained research assignment. You have no access to earlier chats and should not assume any prior work. Begin immediately and carry the project through to the completion standard below.

## Mission

Investigate the interview-motivated conjecture that Einstein–Hilbert gravity and Chern–Simons transgression may be “daughter” actions of a deeper geometric parent. The interview does not supply that parent, a dimension, a group, or a reduction mechanism. Those are the research problem.

## Provenance and epistemic status

This project was motivated by concepts raised in the interview transcript **“Eric Weinstein: The State of American Science, Breakthrough Coverups, and the Danger of Physics.”** The transcript is a source of questions and terminology, not evidence that its speculative claims are correct. Where the transcript does not define a mathematical object, the construction in this brief is a new research proposal and must be labeled as such.

## Technical context

Use differential-form conventions and begin from
\[
S_{\rm EH}
=
\frac{1}{32\pi G}\int_{M_4}
\epsilon_{abcd}\,e^a\wedge e^b\wedge R^{cd}
-\frac{\Lambda}{192\pi G}\int_{M_4}
\epsilon_{abcd}\,e^a\wedge e^b\wedge e^c\wedge e^d,
\]
and
\[
d\,{\rm CS}_{2n-1}(A)=\langle F^n\rangle,
\]
or, for two connections,
\[
d\,T_{2n-1}(A_1,A_0)
=
\langle F_1^n\rangle-\langle F_0^n\rangle.
\]
The dimensional mismatch is central: ordinary four-dimensional Einstein–Hilbert dynamics and odd-dimensional Chern–Simons forms cannot simply be declared equivalent.

## Central research question

Does there exist a mathematically explicit parent gauge/geometric theory whose controlled boundary descent, dimensional reduction, symmetry breaking, or sector restriction yields both Einstein–Hilbert gravity and a genuine Chern–Simons/transgression action?

## Project goal

Either construct such a parent with complete reductions and a healthy spectrum, or prove a useful no-go theorem under clearly stated assumptions. The terminal result must be stronger than an analogy between characteristic classes and gravity.

## Required work programme

1. Perform a priority audit of Chern–Weil theory, transgression forms, Cartan and MacDowell–Mansouri gravity, BF/Plebanski formulations, odd-dimensional Chern–Simons gravity, Lovelock gravity, anomaly inflow, holographic boundary actions, and dimensional reduction. Identify which versions already realize part or all of the conjecture.
2. Define the candidate parent tuple
\[
(\mathcal P,\mathcal G,\mathcal A,\Phi,S_{\rm parent},\partial\mathcal M)
\]
including spacetime dimension, principal bundle, gauge group, invariant polynomial, connection decomposition, symmetry-breaking fields, boundary conditions, and variational principle.
3. Study at least three candidate mechanisms: (i) an AdS/de Sitter Cartan connection \(\mathcal A=\omega+\ell^{-1}e\); (ii) a BF or constrained-topological parent; and (iii) an odd-dimensional transgression theory with boundary or compactification. Select the strongest candidate after explicit comparison.
4. Derive each daughter action line by line. Track all coefficients, topological terms, Gibbons–Hawking-like boundary terms, torsion terms, cosmological terms, and discarded modes. State whether the reduction is exact, low-energy, on-shell, or gauge-fixed.
5. Count physical degrees of freedom before and after reduction. Determine whether the parent contains unwanted higher-spin, torsional, scalar, Kaluza–Klein, or topological sectors.
6. Linearize around at least one maximally symmetric background. Calculate the propagating spectrum, kinetic signs, characteristic equations, and strong-coupling scales.
7. Check gauge symmetry, large-gauge invariance, level quantization where relevant, boundary anomalies, and whether the variational problem is well posed.
8. Identify a dimensionless prediction or structural theorem not already guaranteed by GR or standard Chern–Simons gravity. If none exists, say the construction is a unifying reformulation rather than new physics.
9. Attempt a no-go theorem for the restricted class of local, finite-field, polynomial parent actions if the constructive route fails. Make the assumptions narrow enough that the theorem is true and useful.

## Operating rules

Work as an autonomous mathematical-physics research lead. Do not stop after producing a plan, a literature summary, or a list of equations. Execute the programme with the tools available to you until you reach one of two terminal outcomes:

1. a mathematically explicit construction that passes the stated consistency and empirical gates; or  
2. a decisive negative result, no-go statement, incompatibility proof, or sharply delimited reason the construction fails.

A negative result counts as successful completion. Never force a positive conclusion.

Use current primary literature: original papers, authoritative reviews, official experimental results, and standard monographs. Search broadly enough to avoid reinventing known work. Record exact citations and versions. Do not invent references. Separate every substantive statement into one of four categories:

- established result;
- transcript-motivated claim;
- inference;
- new construction or conjecture developed in this project.

State conventions before calculating: spacetime dimension, metric signature, units, index conventions, gauge group, representations, normalization of generators, boundary conditions, and regularization/renormalization scheme.

Derive rather than gesture. Every proposed theory must specify, as applicable:

\[
\mathfrak T=(\mathcal X,\ \text{fields},\ \text{symmetries},\ S\text{ or equivalent dynamics},\ \text{observables},\ \text{boundary/initial data}).
\]

Run the relevant hard consistency gates early:

- covariance and symmetry closure;
- gauge redundancy versus physical degrees of freedom;
- local and global anomaly cancellation;
- constraint algebra;
- Hamiltonian boundedness;
- hyperbolicity and well-posedness;
- absence of ghosts and gradient instabilities;
- unitarity or positive physical spectral density;
- causality and characteristic cones;
- radiative stability and renormalization or Wilsonian EFT closure;
- recovery of established low-energy limits;
- compatibility with current experimental and observational bounds.

Use symbolic algebra and numerical checks wherever they can falsify a derivation. Supply complete, executable code with tests, fixed random seeds where relevant, machine-readable outputs, and enough comments for independent reproduction. Cross-check key equations by at least two methods when practical.

Conduct a claim-by-claim novelty audit. A conjunction of known ingredients is not automatically novel. State the narrowest defensible contribution. Never use the motivating interview as evidence that a physical claim is true.

Do not ask the user for missing context unless the project is logically impossible without a specific datum. Make the most conservative defensible assumption, state it, and continue. If a large HPC calculation is genuinely required, finish all analytic reductions, reduced-compute tests, convergence criteria, solver architecture, input tables, acceptance tests, and launch configuration first. Do not describe an unrun calculation as completed.

## Required output package

Create a self-contained research package containing at least:

1. `README.md` — question, status, how to reproduce, and exact terminal verdict.
2. A technical paper in complete LaTeX, compiled to PDF when possible.
3. Editable Markdown research notes.
4. A source and notation ledger.
5. A claim/novelty/acceptance matrix in CSV.
6. Complete symbolic and numerical verification code.
7. Machine-readable numerical results in JSON or NPZ as appropriate.
8. Figures and tables generated from code, not manually fabricated.
9. A bibliography with persistent identifiers.
10. A ZIP archive containing the complete package.

The paper must include: abstract, provenance and scope, definitions, literature position, derivations, consistency analysis, empirical constraints, numerical verification, failure modes, novelty boundary, and next decisive test.

## Completion standard

The work is complete only when another technically competent researcher can:

- reconstruct the model or no-go argument from the package;
- rerun every reported calculation;
- distinguish sourced facts from new claims;
- see exactly which acceptance tests passed or failed;
- identify the strongest result that survives scrutiny;
- identify every unresolved assumption without reading this prompt.

## Project-specific deliverables

In addition to the standard package, deliver:

- a literature map of all known EH/CS parent mechanisms;
- `parent_action.tex`;
- `reduction_EH.tex` and `reduction_CS.tex`;
- a coefficient and boundary-term audit;
- symbolic exterior-algebra verification;
- a linearized-spectrum notebook;
- a comparison table separating exact descent, effective descent, and mere analogy.

## Acceptance criteria

A pass requires an explicit parent action, two reproducible daughter derivations, a well-posed variational principle, a consistent degree-of-freedom count, and at least one nontrivial discriminator—or a rigorous no-go result for a clearly defined candidate class.

## Failure and kill criteria

Fail the project if the only result is that both actions can be written using differential forms, if the dimensional mismatch is hidden, or if topological and propagating theories are conflated.

## Safety boundary

Keep all discussion at the level of fundamental theory. Do not develop weapon applications.

## Final instruction

Do not return merely a roadmap. Perform the literature audit, derivations, calculations, code, verification, and writing. Continue until the project reaches a terminal positive or negative result under the stated completion standard. End with a concise verdict containing:

- strongest result;
- what failed;
- what remains genuinely open;
- whether the result is publishable now, publishable after a named calculation, or not publishable;
- the exact next decisive calculation, if one remains.

# End of standalone prompt
