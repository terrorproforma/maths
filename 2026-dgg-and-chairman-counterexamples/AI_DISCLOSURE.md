# AI-use and authorship disclosure

GPT-5.6 Pro was used as a research assistant during exploration, construction of the finite certificates, algebraic checking, code drafting, literature orientation, and preparation of the manuscript source.

**Provenance boundary.** The flow (DGG/Goemans) counterexample is due to Dmitry Rybin
(with GPT-5.6 Pro), and the material derived from his seven-vertex instance builds on his
work; it is credited, not claimed. The machine-dependent weighted-chairman counterexample
originates from the repository owner's session. See `../ATTRIBUTIONS.md` and
`../PROVENANCE_AUDIT.md`.

The repository is deliberately organized so that the claims do not depend on trusting an AI-generated narrative. The flow result is exhaustively checkable over eight routings. The chairman result has an exact rational proof certificate and an independent mixed-integer infeasibility model. All data used by those checks are included.

An AI system is not an author. Before submission, the human author must:

1. rerun every verifier in a clean environment;
2. inspect the mathematical proofs line by line;
3. obtain independent expert review, especially because the main flow conjecture was longstanding;
4. verify priority and bibliography immediately before submission;
5. provide the journal's required generative-AI disclosure; and
6. accept full responsibility for the claims, wording, citations, and code.

Suggested manuscript disclosure:

> During the discovery and drafting process, the author used GPT-5.6 Pro for mathematical exploration, algebraic checking, code generation, and language editing. All stated results were subsequently reduced to finite exact certificates and independently checked by the human author. The AI system is not an author and bears no responsibility for the contents.
