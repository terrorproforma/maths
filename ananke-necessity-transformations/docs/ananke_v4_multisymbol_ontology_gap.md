# ANANKE v4: Multi-Symbol Rank-Unrestricted Obstructions & Classical-vs-Quantum Ontology Gap

This document presents **ANANKE v4**, extending the rank-unrestricted framework of [ananke_v3_rank_unrestricted.md](ananke_v3_rank_unrestricted.md) from unary experiments $\{a^k : 0 \le k \le L\}$ to **multi-symbol noncommuting operation alphabets** $\Sigma = \{x, z\}$, and explicitly quantifying the **classical-vs-quantum ontology gap** between $C_{\mathrm{classical}}(f; \varepsilon, \mathcal{W})$ and $C_{\mathrm{quantum}}(f; \varepsilon, \mathcal{W})$ on the exact same finite word sets $\mathcal{W}$.

Every result in this report carries an explicit epistemic label:
- **PROVED**: A mathematical theorem with a complete, assumption-explicit proof.
- **CERTIFIED**: A finite-shot or noiseless lower bound produced by a sound deterministic verifier (exact branch-and-bound, Chernoff–KL, Matrix Hoeffding, or B-spline Cayley–Hamilton + Subharmonic Dual) with **zero rank-upper-bound assumption**.
- **NUMERICAL**: An empirical upper bound or diagnostic from non-convex optimization (NMF, L-BFGS-B HMM training, or finite-sample simulation) that does not constitute a lower-bound proof.
- **CONJECTURAL / OPEN**: A boundary or mechanism not yet closed by a certified lower bound.

---

## 0. Cross-Ontology Formulation and the Two Open Questions from v3

Let $\Sigma$ be a finite alphabet of deterministic experimental interventions, $\mathcal{W} \subset \Sigma^*$ a finite set of tested words, and $f : \mathcal{W} \to [0, 1]$ an observed acceptance-probability process.

- **Classical state complexity** $C_{\mathrm{classical}}(f; \varepsilon, \mathcal{W})$ (definition, inherited from v3): the smallest integer $N \ge 1$ admitting a valid $N$-state classical hidden Markov model $(p, \{M_a\}_{a \in \Sigma}, e)$ with $p \in \Delta_N$, row-stochastic $M_a \in [0, 1]^{N \times N}$, and $e \in [0, 1]^N$ such that $\max_{w \in \mathcal{W}} |p M_w e - f(w)| \le \varepsilon$.
- **Quantum Hilbert-space complexity** $C_{\mathrm{quantum}}(f; \varepsilon, \mathcal{W})$ (definition, implemented and numerically verified in `src/ananke/ontology_gap.py`): the smallest integer $d \ge 1$ admitting a $d$-dimensional quantum realization $(\rho_0, \{U_a\}_{a \in \Sigma}, E)$ with $\rho_0 \succeq 0$, $\operatorname{Tr}(\rho_0) = 1$, $U_a^\dagger U_a = I_d$, and $0 \preceq E \preceq I_d$ such that
  $$\max_{w = a_1 \cdots a_k \in \mathcal{W}} \left| \operatorname{Tr}\!\left(E\, U_{a_k} \cdots U_{a_1}\, \rho_0\, U_{a_1}^\dagger \cdots U_{a_k}^\dagger\right) - f(w) \right| \le \varepsilon.$$
  In an orthonormal Hermitian basis of $\mathbb{C}^{d \times d}$, every exact $d$-level quantum realization defines a $d^2$-dimensional real linear process (`QuantumRealization.to_linear_process()`); on our qubit benchmarks, `qubit_quantum_realization` agrees with the exact Bloch `qubit_rotation_process` to $\le 6.7 \times 10^{-16}$ across all 127 words of length $\le 6$ (`results/ontology_gap_v4.json`).

ANANKE v3 proved the **Unary Shift-Register Loophole**: on any unary word set $\mathcal{W}_L = \{a^k : 0 \le k \le L\}$, every function $f$ admits an exact classical shift register of size $N \le L + 1$, forcing $C_{\mathrm{classical}}(f; 0, \{a^k\}_{k \le L}) \le L + 1$. Consequently, v3 required deep unary words ($L = 320\text{--}4000$) to certify $N \ge 8\text{--}9$ from finite shots. v3 also discovered a striking teaser puzzle on two noncommuting symbols $\{x, z\}^{\le 7}$: static simplex-box NMF on the mixed-qubit $15\times 15$ Hankel block already reached error `0.0066` at $N = 8$, whereas dynamical Bloch-polytope counterfeits suffered error `0.310` at $N = 12$ and `0.049` at $N = 128$.

ANANKE v4 resolves both questions through **four cross-model-audited theorems** and an explicit **dynamical-vs-static analysis**:
1. **Theorem 1 (Kochen–Specker Linear-Witness Ceiling on Single Qubits, PROVED):** While linear matrix witnesses $\langle W, H_f \rangle / \gamma_+(W)$ *can* exceed $2$ on a single qubit (e.g., exact ratio $9/4 = 2.25$ on a $3\times 3$ trine qubit block and $2.292$ on a $12\times 12$ icosahedral block, certifying $N \ge 3$), **no** linear matrix witness can ever exceed $4$ on any single-qubit Hankel block (via the total-mass-$4$ Kochen–Specker integral decomposition on $S^2$, matching Toner–Bacon 2003 / Renner–Tavakoli–Quintino 2023).
2. **Theorem 2 (Eliminated-Effect Support-Envelope Obstruction, PROVED & CERTIFIED):** A non-convex single-state support-envelope invariant with directed-rounding box-scaled secant branch-and-bound certifies $C_{\mathrm{classical}} \ge 8$ (**doubling** both the qubit's Hankel rank $4$ and the linear-witness ceiling $4$) on a pure two-symbol qubit at depth just **$L = 8$** — both noiselessly and at 99% finite-shot confidence via cancellation-free Chernoff–KL — **$20\times$ shallower** than v3 Mode B's $L = 160$ for $N \ge 8$.
3. **Theorem 3 (Noncommutative Semigroup Spectral Synergy via Niven's Theorem, PROVED & CERTIFIED):** Two finite-order single-qubit gates $R_x(\pi/2)$ (order 4) and $R_z(\pi/3)$ (order 6) individually satisfy $C_{\mathrm{classical}}(x^*) \le 4$ and $C_{\mathrm{classical}}(z^*) \le 6$ even at $L = \infty$, yet their noncommuting product $w = xz$ has exact irrational angle $\theta_{xz} = \arccos(-1/4)$ and certifies $C_{\mathrm{classical}} \ge 7 > \max(4, 6)$ at 99% confidence in **120,100 total shots** (and $N \ge 13$ noiselessly at $K = 800, \varepsilon = 10^{-3}$).
4. **Theorem 4 (Unconditional Short-Depth Spectral Rank Beyond the Unary $L+1$ Ceiling, PROVED & CERTIFIED):** Combining $\operatorname{rank}(H_g) \le N$, Weyl's inequality, and Hankel Matrix Hoeffding (with **zero** rank-upper-bound assumption) on verified $d$-level two-symbol quantum systems ($C_{\mathrm{quantum}} = d$, Liouville rank $d^2$) certifies at **99% finite-shot confidence** classical lower bounds strictly exceeding both $C_{\mathrm{quantum}} = d$ (quadratic $d^2$ vs. $d$ rank gap) and the unary shift-register ceiling $L + 1$:
   - Qutrit ($d = 3$) at $L = 6$ ($L+1 = 7$): $C_{\mathrm{classical}} \ge 9 > 7$ in **63,500 total shots**;
   - Two-qubit ($d = 4$) at $L = 8$ ($L+1 = 9$): $C_{\mathrm{classical}} \ge 16 > 9$ in **306,600 total shots**;
   - Ququint ($d = 5$) at $L = 8$ ($L+1 = 9$): $C_{\mathrm{classical}} \ge 25 > 9$, and at $L = 10$ ($L+1 = 11$): $C_{\mathrm{classical}} \ge 25 > 11$ in **1,228,200 total shots**.
5. **Avenue 3 (Fejes Tóth Scaling Benchmark & Local Dynamical-vs-Static Upper Bounds, PROVED/HEURISTIC/NUMERICAL):** Fejes Tóth's (1953) proved inradius bound $\rho_{\mathrm{in}}(K_N) \le \frac{1}{\sqrt{3}}\cot\!\left(\frac{\pi N}{6(N-2)}\right)$ (exact at $N = 4, 6, 12$) supplies an isotropic depth-compounding heuristic scaling benchmark for Bloch-polytope counterfeits, and monotone local upper-bound fits of two-symbol HMMs vs. static $15\times 15$ simplex-box NMF at $L = 6$ show optimizer upper-bound ratios of $15\times$–$121\times$ at $N = 10\text{--}12$ (a numerical motivation, not a proved dynamical lower bound).

---

## 1. Theorem 1 — Kochen–Specker Linear-Witness Ceiling ($\le 4$) for Single Qubits (PROVED)

Before designing non-convex multi-symbol obstructions on a single qubit, we determine the exact limitation of linear hyperplane witnesses $\langle W, H_f \rangle$ compared against the rank-1 simplex-box maximum
$$\gamma_+(W) := \max_{a \in \{0,1\}^m,\; b \in \{0,1\}^n} a^T W b.$$

*(Note on prior draft revision: Unlike fixed-measurement single-POVM tables covered by Frenkel–Weiner 2015, Hankel blocks index independently selectable binary measurements across columns, so linear witnesses on a single qubit **can** exceed $2$ — e.g. $9/4 = 2.25$ on a $3\times 3$ trine qubit block and $2.292$ on a $12\times 12$ icosahedral block, certifying $N \ge 3$. However, as proved below, they can **never** exceed $4$.)*

### Statement (PROVED)
Let $H_f \in [0, 1]^{m \times n}$ be any prepare-and-measure probability table generated by a single qubit ($d = 2$):
$$H_f(i, j) = \operatorname{Tr}(\rho_i E_j), \qquad \rho_i \succeq 0,\; \operatorname{Tr}(\rho_i) = 1,\; 0 \preceq E_j \preceq I_2.$$
Then for **every** real witness matrix $W \in \mathbb{R}^{m \times n}$ with $\gamma_+(W) > 0$,
$$\frac{\langle W, H_f \rangle}{\gamma_+(W)} \;\le\; 4.$$
In particular, **no** linear matrix witness $\langle W, H_f \rangle / \gamma_+(W)$ can certify $N > 4$ on any single-qubit Hankel block of any size (consistent with Toner–Bacon 2003 and Renner–Tavakoli–Quintino 2023, which establish that $2$ classical bits $= 4$ states assisted by shared randomness suffice to simulate arbitrary single-qubit prepare-and-measure correlations).

### Proof
By the Kochen–Specker (1967) hidden-variable representation on the Bloch sphere $S^2$, for any pure state Bloch vector $r \in S^2$ and projective effect Bloch vector $e \in S^2$,
$$\frac{1 + r \cdot e}{2} = \int_{S^2} \frac{d\Omega(\lambda)}{\pi}\,(r \cdot \lambda)_+\,\mathbf{1}[e \cdot \lambda \ge 0],$$
and for the trivial effects $E = I_2$ and $E = 0$, $\int_{S^2} \frac{d\Omega(\lambda)}{\pi}(r\cdot\lambda)_+ \cdot 1 = 1$ and $\int_{S^2} \frac{d\Omega(\lambda)}{\pi}(r\cdot\lambda)_+ \cdot 0 = 0$. Since every density matrix $\rho_i$ is a convex combination of pure states and every binary POVM effect $0 \preceq E_j \preceq I_2$ is a convex combination of $\{0, I_2, \Pi_j\}$, linearity yields functions $a_\lambda \in [0, 1]^m$ and $b_\lambda \in [0, 1]^n$ for each $\lambda \in S^2$ such that
$$H_f = \int_{S^2} \frac{d\Omega(\lambda)}{\pi}\, a_\lambda b_\lambda^T.$$
By multilinearity of $(a, b) \mapsto a^T W b$ over $[0, 1]^m \times [0, 1]^n$, $a_\lambda^T W b_\lambda \le \gamma_+(W)$ for every $\lambda \in S^2$. Since the total measure is $\int_{S^2} \frac{d\Omega(\lambda)}{\pi} = \frac{4\pi}{\pi} = 4$, integrating gives
$$\langle W, H_f \rangle = \int_{S^2} \frac{d\Omega(\lambda)}{\pi}\, a_\lambda^T W b_\lambda \;\le\; 4\,\gamma_+(W). \qquad \square$$

### Computational Audit (`results/certify_multisymbol_v4.json`)
Evaluated with exact binary maximization `simplex_box_linear_ratio` in `src/ananke/multisymbol_obstructions.py`:

| Qubit Hankel / P&M block | Witness matrix $W$ | $\langle W, H_f \rangle$ | $\gamma_+(W)$ | Linear ratio $\langle W, H_f \rangle / \gamma_+(W)$ | Proved ceiling |
|---|---|---:|---:|---:|---:|
| $3\times 3$ trine qubit ($x$-axis, $2\pi/3$ $z$-rot) | $\frac{3}{2}I - \frac{1}{2}\mathbf{1}\mathbf{1}^T$ | `2.2500` | `1.0000` | **`2.2500`** (certifies $N \ge 3$) | $\le 4$ |
| $12\times 12$ icosahedral pure qubit | $2 H_f - \mathbf{1}$ | `24.0000` | `10.4721` | **`2.2918`** (certifies $N \ge 3$) | $\le 4$ |
| $7\times 7$ two-symbol pure qubit | Centered $2 H_f - \mathbf{1}$ | `9.3692` | `6.7786` | `1.3822` | $\le 4$ |
| $7\times 7$ two-symbol pure qubit | Polar nuclear dual $U_3 V_3^T$ | `4.0240` | `3.2113` | `1.2531` | $\le 4$ |
| $7\times 7$ two-symbol pure qubit | Extreme cap minus antipodal | `9.1744` | `8.0000` | `1.1468` | $\le 4$ |
| $7\times 7$ two-symbol pure qubit | Random Gaussian #1 | `4.0832` | `15.0448` | `0.2714` | $\le 4$ |
| $7\times 7$ two-symbol pure qubit | Random Gaussian #2 | `2.1081` | `7.9054` | `0.2667` | $\le 4$ |

**Takeaway:** Linear matrix witnesses can certify $N \ge 3$ on a single qubit (and at most $N \ge 4$ in the continuum), but breaking past **$N = 4$** on a single qubit without a rank assumption *requires* a **non-convex** structural invariant — precisely what Theorem 2 supplies ($N \ge 8$ at depth $L = 8$).

---

## 2. Theorem 2 — Eliminated-Effect Support-Envelope Obstruction (PROVED & CERTIFIED)

### 2.1 Mathematical Statement & Proof (PROVED)

Let $\mathcal{P} = \{u_1, \dots, u_m\}$ be prefixes and $\mathcal{S} = \{v_1, \dots, v_n\}$ be suffixes, and let $\mathcal{E} \subseteq \{1, \dots, m\} \times \{1, \dots, n\}$ be **any** observed index pattern — in particular, the **depth-$L$ staircase** $\mathcal{E}_L = \{(i, j) : |u_i| + |v_j| \le L\}$ where every entry $(i, j) \in \mathcal{E}_L$ corresponds to a tested word $u_i v_j \in \Sigma^{\le L}$.

Suppose $g$ is any $N$-state classical process ($p \in \Delta_N$, row-stochastic $M_a$, $e \in [0, 1]^N$) whose probabilities lie inside certified lower/upper bounds on $\mathcal{E}$:
$$L_{i, j} \le g(u_i v_j) \le U_{i, j} \qquad \forall (i, j) \in \mathcal{E}.$$
Write $V_{i, j} := 1 - L_{i, j}$, and let $P \in \Delta_N^m$ have rows $P_{i, \cdot} = p M_{u_i}$ and $Q \in [0, 1]^{N \times n}$ have columns $Q_{\cdot, j} = M_{v_j} e$, so $g(u_i v_j) = \sum_{s=1}^N P_{i, s} Q_{s, j}$.

**Lemma 2.1 (Eliminated-Effect Hyperbola Characterization, PROVED).**
For each classical hidden state $s \in \{1, \dots, N\}$, its state-weight vector $a = P_{\cdot, s} \in [0, 1]^m$ satisfies:
$$\text{there exists } q \in [0, 1]^n \text{ with } a_i q_j \le U_{i, j} \text{ and } a_i (1 - q_j) \le V_{i, j}\;\;\forall (i, j) \in \mathcal{E}$$
**if and only if** $a$ belongs to the **support-envelope feasible set**
$$\mathcal{A}(U, V) := \left\{ a \in [0, 1]^m : a_{i_1} a_{i_2} \le U_{i_1, j} a_{i_2} + V_{i_2, j} a_{i_1} \;\;\forall j \in \{1,\dots,n\},\; \forall (i_1, j), (i_2, j) \in \mathcal{E} \right\}$$
(equivalently, $\frac{U_{i_1, j}}{a_{i_1}} + \frac{V_{i_2, j}}{a_{i_2}} \ge 1$ whenever $a_{i_1}, a_{i_2} > 0$, while any row with $a_i = 0$ imposes no constraint on $q_j$, and $U_{i_1, j} = V_{i_2, j} = 0$ simply forces $a_{i_1} a_{i_2} = 0$).

*Proof.* Since $P \ge 0$ and $Q, \mathbf{1}-Q \ge 0$, for every state $s$ and every $(i, j) \in \mathcal{E}$,
$$P_{i, s} Q_{s, j} \le \sum_{t=1}^N P_{i, t} Q_{t, j} = g(u_i v_j) \le U_{i, j}, \qquad P_{i, s} (1 - Q_{s, j}) \le \sum_{t=1}^N P_{i, t}(1 - Q_{t, j}) = 1 - g(u_i v_j) \le V_{i, j}.$$
For a fixed column $j$, a scalar $q_j \in [0, 1]$ satisfies $a_i q_j \le U_{i, j}$ and $a_i (1 - q_j) \le V_{i, j}$ for all $i$ with $(i, j) \in \mathcal{E}$ if and only if the upper interval endpoints $\min(1, U_{i_1, j}/a_{i_1})$ lie at or above the lower interval endpoints $(1 - V_{i_2, j}/a_{i_2})_+$ for every pair $(i_1, j), (i_2, j) \in \mathcal{E}$. Rearranging $1 - V_{i_2, j}/a_{i_2} \le U_{i_1, j}/a_{i_1}$ gives $U_{i_1, j}/a_{i_1} + V_{i_2, j}/a_{i_2} \ge 1$. $\square$

**Theorem 2 (Weighted Support-Envelope State Lower Bound, PROVED).**
For **any** probability weight vector $w \in \Delta_m$ ($w \ge 0, \sum_{i=1}^m w_i = 1$), since $\sum_{s=1}^N P_{i, s} = 1$ for every prefix $i$,
$$1 = \sum_{i=1}^m w_i = \sum_{s=1}^N \sum_{i=1}^m w_i P_{i, s} \le N \cdot \sup_{a \in \mathcal{A}(U, V)} \sum_{i=1}^m w_i a_i.$$
Therefore, with **zero rank assumption** and **zero Jordan-structure assumption**,
$$C_{\mathrm{classical}}(f; \varepsilon, \mathcal{W}) \;\ge\; \left\lceil \frac{1}{\sup_{a \in \mathcal{A}(U, V)} \sum_{i=1}^m w_i a_i} \right\rceil.$$
In the noiseless case with tolerance $\varepsilon \ge 0$, set $L_{i, j} = \max(0, f(u_i v_j) - \varepsilon)$ and $U_{i, j} = \min(1, f(u_i v_j) + \varepsilon)$. In the finite-shot case with $n_w$ independent Bernoulli shots per word $w \in \mathcal{W}$ and family-wise failure budget $\alpha \in (0, 1)$, set $[L_w, U_w]$ to the exact non-asymptotic Chernoff–KL binomial confidence interval (`kl_binomial_confidence_interval`) at per-word level $\alpha / |\mathcal{W}|$; by a union bound, the true process satisfies $L_{i, j} \le f(u_i v_j) \le U_{i, j}$ simultaneously on all $(i, j) \in \mathcal{E}$ with probability at least $1 - \alpha$. $\square$

### 2.2 Sound Deterministic Upper-Bound Verification: Box-Scaled Secant Branch-and-Bound (PROVED)

The feasible set $\mathcal{A}(U, V)$ is non-convex (precisely why it bypasses Theorem 1!). To obtain a **100% sound, certified** lower bound on $N$, we must compute a **certified upper bound** $\overline{S} \ge \sup_{a \in \mathcal{A}(U, V)} \sum_{i=1}^m w_i a_i$, because $N \ge \lceil 1 / \overline{S} \rceil$ holds for *any* valid upper bound $\overline{S}$ — even if branch-and-bound terminates at a node budget before closing the gap.

**Lemma 2.2 (Box-Scaled Secant Inequality, PROVED).**
Suppose $a$ lies inside a coordinate box $0 \le a_i \le B_i$ ($i = 1, \dots, m$) and satisfies the hyperbola constraint $U_{p, j} a_q + V_{q, j} a_p \ge a_p a_q$ for a pair $(p, q)$ and suffix $j$ with $U_{p, j} \le B_p$ and $V_{q, j} \le B_q$. Then:
$$(B_q - V_{q, j})\, a_p + (B_p - U_{p, j})\, a_q \;\le\; B_p B_q.$$

*Proof.* Expand the right-hand minus left-hand side directly:
$$B_p B_q - (B_q - V_{q, j}) a_p - (B_p - U_{p, j}) a_q = (B_p - a_p)(B_q - a_q) + \left(U_{p, j} a_q + V_{q, j} a_p - a_p a_q\right) \ge 0,$$
since $B_p \ge a_p$, $B_q \ge a_q$, and $U_{p, j} a_q + V_{q, j} a_p \ge a_p a_q$. $\square$

Inside each box $[\ell, B]$ of our best-first spatial branch-and-bound solver (`certify_support_envelope_lower_bound` in `src/ananke/multisymbol_obstructions.py`):
1. **Outward-rounded hyperbola bound propagation:** Writing $V_{q,j}/(1 - U_{p,j}/\ell_p) = (V_{q,j}\ell_p)/(\ell_p - U_{p,j})$ (so $\ell_p - U_{p,j}$ is Sterbenz-exact near cancellation) and applying directed IEEE-754 outward rounding (`nextafter`), we tighten $B_q$ (and symmetrically $B_p$) to a fixed point without clipping any feasible point in $[\ell, B] \cap \mathcal{A}(U, V)$.
2. **Dual secant matching relaxation:** For every unordered pair $\{p, q\}$ and suffix $j$ with $U_{p, j} < B_p$ and $V_{q, j} < B_q$, Lemma 2.2 gives the valid dual saving
   $$\Delta_{p, q} = \min\!\left(\frac{w_p}{B_q - V_{q,j}},\, \frac{w_q}{B_p - U_{p,j}}\right)\bigl(B_p B_q - V_{q,j} B_p - U_{p,j} B_q\bigr)_+ \ge 0$$
   (evaluated with outward-safe directed rounding so the subtracted saving never overestimates). Taking a greedy vertex-disjoint matching $M$ guarantees
   $$\sup_{a \in [\ell, B] \cap \mathcal{A}(U, V)} \sum_{i=1}^m w_i a_i \;\le\; \sum_{i=1}^m w_i B_i - \sum_{\{p, q\} \in M} \Delta_{p, q}.$$
3. **Best-first splitting:** Always pop the active box with the highest certified upper bound, split on the most-violated pair $\{p, q\}$ (retaining terminal narrow boxes in `global_ub`), and repeat until convergence or the node budget `max_nodes_per_star` is reached. The global maximum upper bound across all terminal and remaining open boxes is a guaranteed upper bound $\overline{S}$ even when `converged = false` (which holds on several larger blocks below where the node budget is reached before `tol`, while still yielding a valid global upper bound).

### 2.3 Continuous Sphere Cap Estimates (`NUMERICAL` Diagnostic, Ceiling $\le 12$ on $S^2$)

On the continuous Bloch sphere $S^2$ ($p(r, e) = \frac{1 + r \cdot e}{2}$), optimizing the pairwise support-envelope condition over all $e \in S^2$ reduces to the pairwise bound $(1 - a(r_1))(1 - a(r_2)) \ge \sin^2(\gamma(r_1, r_2)/2)$, where $\gamma$ is the geodesic separation. Discretizing axisymmetric caps on a 32-point midpoint grid (`continuous_sphere_support_envelope_ceiling`, **NUMERICAL** estimate — neither a certified upper nor lower enclosure of the continuum supremum):

| Geometry | Maximizing cap half-angle | Numerical grid integral | $1 / \text{integral}$ | Rounded integer | Epistemic label |
|---|---:|---:|---:|---:|---|
| Pure qubit sphere $S^2$ | $65^\circ$ | `0.08772` | `11.3997` | `12` | **NUMERICAL** |
| Pure rebit circle $S^1$ | $60^\circ$ | `0.14934` | `6.6960` | `7` | **NUMERICAL** |

*Scope note:* An explicit piecewise-constant axisymmetric cap satisfying the exact continuous pairwise constraint at cell upper edges achieves integral $> 1/12$ (`~0.08595`), proving that the uniform-weight single-state envelope on $S^2$ cannot certify $N \ge 13$ (ceiling $\le 12$); certifying attainment of $N \ge 12$ over arbitrary (possibly non-axisymmetric) functions on $S^2$ remains **OPEN**.

### 2.4 Certified Results on Ideal Fibonacci Blocks & Pure Two-Symbol Qubit Staircases (`results/certify_multisymbol_v4.json`)

*(Disclosure: In the finite-shot runs below, the prefix weights $\mu \in \Delta_m$ are computed a priori from the noiseless design model, never from the simulated shot data, so no post-selection bias enters the simultaneous Chernoff–KL confidence envelope. Several larger tables below reach the per-star node cap with `converged = false`; by Theorem 2 every remaining heap upper bound is retained in $\overline{S}$, so the reported lower bounds remain valid.)*

#### Ideal Pure-Qubit Fibonacci Prepare-and-Measure Blocks (CERTIFIED)
| Block shape ($m \times n$) | Tolerance $\varepsilon$ | Certified $\overline{S}$ | Continuous LB $1/\overline{S}$ | **Certified $C_{\mathrm{classical}}$ LB** |
|---|---:|---:|---:|---:|
| $12 \times 64$ | `0.000` | `0.13415` | `7.4543` | **$\ge 8$** |
| $12 \times 64$ | `0.002` | `0.13780` | `7.2567` | **$\ge 8$** |
| $16 \times 64$ | `0.000` | `0.12364` | `8.0878` | **$\ge 9$** |
| $16 \times 64$ | `0.002` | `0.12734` | `7.8533` | **$\ge 8$** |
| $20 \times 128$ | `0.000` | `0.11517` | `8.6824` | **$\ge 9$** |
| $20 \times 128$ | `0.002` | `0.11885` | `8.4140` | **$\ge 9$** |

#### Designed Pure Two-Symbol Qubit ($C_{\mathrm{quantum}} = 2$, Hankel Rank $= 4$) — Noiseless Depth-$L$ Staircase (CERTIFIED)
Parameters: $\theta_x = 2.39656466\,\text{rad}$, $\theta_z = 1.76664438\,\text{rad}$, pure initial Bloch vector $r_0 = (-0.6690, 0.0416, 0.7421)$, projective measurement axis $m = (-0.8722, 0.4845, 0.0673)$. All words tested satisfy $|u| + |v| \le L$ (no words longer than $L$).

| Depth $L$ | Unique words $|\mathcal{W}_L|$ | Active prefixes | Tolerance $\varepsilon$ | Certified $\overline{S}$ | Continuous LB | **Certified $C_{\mathrm{classical}}$ LB** | Ratio vs. Hankel rank $4$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 | 127 | 9 | `0.000` | `0.17476` | `5.7221` | **$\ge 6$** | $1.5\times$ |
| 6 | 127 | 9 | `0.002` | `0.17819` | `5.6120` | **$\ge 6$** | $1.5\times$ |
| 6 | 127 | 9 | `0.005` | `0.18335` | `5.4539` | **$\ge 6$** | $1.5\times$ |
| 7 | 255 | 17 | `0.000` | `0.14488` | `6.9023` | **$\ge 7$** | $1.75\times$ |
| 7 | 255 | 17 | `0.002` | `0.14823` | `6.7464` | **$\ge 7$** | $1.75\times$ |
| 7 | 255 | 17 | `0.005` | `0.15326` | `6.5248` | **$\ge 7$** | $1.75\times$ |
| **8** | **511** | **19** | **`0.000`** | **`0.13020`** | **`7.6803`** | **$\ge 8$** | **$2.0\times$** |
| **8** | **511** | **19** | **`0.002`** | **`0.13423`** | **`7.4497`** | **$\ge 8$** | **$2.0\times$** |
| **8** | **511** | **19** | **`0.005`** | **`0.14033`** | **`7.1259`** | **$\ge 8$** | **$2.0\times$** |

#### Designed Pure Two-Symbol Qubit at $L = 8$ — 99% Finite-Shot Chernoff–KL Certification (CERTIFIED)
| Depth $L$ | Words $|\mathcal{W}_8|$ | Shots / word | Total shots | Confidence $1-\alpha$ | Certified $\overline{S}$ | Continuous LB | **Certified $C_{\mathrm{classical}}$ LB** |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 511 | `10,000` | `5,110,000` | `99%` | `0.14548` | `6.8738` | **$\ge 7$** |
| **8** | **511** | **`30,000`** | **`15,330,000`** | **`99%`** | **`0.13989`** | **`7.1482`** | **$\ge 8$** |
| **8** | **511** | **`100,000`** | **`51,100,000`** | **`99%`** | **`0.13420`** | **`7.4515`** | **$\ge 8$** |

**Comparison with ANANKE v3:** On a single qubit with zero rank-upper-bound assumption, v3 Mode B required unary depth **$L = 160$** (and Mode A required **$L = 4000$**) to reach $C_{\mathrm{classical}} \ge 8$ from finite shots. Theorem 2 achieves the **exact same rank-unrestricted $C_{\mathrm{classical}} \ge 8$ at depth just $L = 8$** — **$20\times$ shallower** than v3 Mode B and **$500\times$ shallower** than v3 Mode A — strictly **doubling** both the qubit's Hankel rank 4 and the linear-witness ceiling 4 (Theorem 1)!

**Soundness & Reproducible Calibration (`results/certify_multisymbol_v4.json`):**
- On a 4-state classical 2-symbol HMM at $L = 6$, Theorem 2 certifies $N \ge 2 \le 4$ (no false exclusion).
- On a sharp full-rank 4-state deterministic 2-symbol permutation automaton (`mc_calibration_4state_perm` in `certify_multisymbol_v4.py`, $L = 6$, 5,000 shots/word, $\alpha = 0.01$, 20 trials), Theorem 2 returned **exact $N \ge 4$ in 20/20 trials** and **0/20 false exclusions ($> 4$)**.

---

## 3. Theorem 3 — Noncommutative Semigroup Spectral Synergy via Niven's Theorem (PROVED & CERTIFIED)

What if every individual generator $x$ and $z$ is *individually* classically simulable by a tiny finite-state machine across all depths $L = \infty$? While noncommutativity alone is not always sufficient (e.g., orthogonal quarter-turns generate a finite symmetry group of the cube), Theorem 3 exhibits an explicit finite-order pair whose noncommuting product generates an irrational angle and therefore an unbounded classical state obstruction.

### Statement & Proof (PROVED)
Consider the single-qubit two-symbol system (`niven_rational_gate_qubit` in `src/ananke/multisymbol_obstructions.py`):
$$U_x = R_x\!\left(\frac{\pi}{2}\right) = \exp\!\left(-i \frac{\pi}{4} \sigma_x\right), \qquad U_z = R_z\!\left(\frac{\pi}{3}\right) = \exp\!\left(-i \frac{\pi}{6} \sigma_z\right).$$
1. **Individual unary ceilings (PROVED):** Since $R_x(\pi/2)^4 = I$ (on $\mathrm{SO}(3)$) and $R_z(\pi/3)^6 = I$, every unary process along $x^*$ is 4-periodic and every unary process along $z^*$ is 6-periodic. Therefore, even on the **infinite** unary languages,
   $$C_{\mathrm{classical}}(f; 0, \{x^k : k \ge 0\}) \le 4, \qquad C_{\mathrm{classical}}(f; 0, \{z^k : k \ge 0\}) \le 6.$$
   No unary experiment using $x$ alone or $z$ alone can ever certify $N \ge 7$ at any horizon $L \le \infty$.
2. **Noncommutative irrationality of $w = xz$ (PROVED):** In $\mathrm{SU}(2)$,
   $$U_{xz} = U_z U_x = \left(\cos\tfrac{\pi}{6}\, I - i\sin\tfrac{\pi}{6}\, \sigma_z\right)\!\left(\cos\tfrac{\pi}{4}\, I - i\sin\tfrac{\pi}{4}\, \sigma_x\right),$$
   so $\tfrac{1}{2}\operatorname{Tr}(U_{xz}) = \cos(\pi/6)\cos(\pi/4) = \frac{\sqrt{3}}{2}\cdot\frac{\sqrt{2}}{2} = \frac{\sqrt{6}}{4}$. By the double-angle formula for the $\mathrm{SO}(3)$ rotation angle $\theta_{xz}$,
   $$\cos(\theta_{xz}) = 2\left(\frac{1}{2}\operatorname{Tr}(U_{xz})\right)^2 - 1 = 2\cdot\frac{6}{16} - 1 = -\frac{1}{4}.$$
   By **Niven's Theorem** (1956), the only rational values of $\cos(\pi q)$ for $q \in \mathbb{Q}$ are $\{0, \pm \frac{1}{2}, \pm 1\}$. Since $-\frac{1}{4} \notin \{0, \pm \frac{1}{2}, \pm 1\}$, the rotation angle
   $$\theta_{xz} = \arccos\!\left(-\frac{1}{4}\right) \approx 1.82347658\,\text{rad}$$
   is **strictly irrational** modulo $2\pi$.
3. **Semigroup spectral obstruction (PROVED):** For any $N$-state classical realization $(p, \{M_x, M_z\}, e)$ of $f$, the product $M_{xz} := M_x M_z$ is itself an $N \times N$ row-stochastic matrix realizing the composite ray $k \mapsto f((xz)^k)$. Because $e^{i\theta_{xz}} \notin \Theta_N$ for every finite $N$ (peripheral stochastic eigenvalues are roots of unity), at $\varepsilon = 0$ no finite $N$ can match all $k \ge 0$ (and a linear recurrence argument shows $C_{\mathrm{classical}}(f; 0, \{(xz)^k\}_{k \le K}) \ge K - 1$ for $K \ge 3$); for finite horizons and nonzero noise $\varepsilon > 0$, ANANKE v3's rank-unrestricted B-spline Cayley–Hamilton + Subharmonic Dual verifier applied to $k \mapsto f((xz)^k)$ certifies explicit lower bounds strictly exceeding $\max(4, 6) = 6$. $\square$

### Certified Results (`results/certify_multisymbol_v4.json`)

#### Noiseless Composite-Ray $(xz)^k$ Sweep (CERTIFIED; search cap $N_{\max} = \min(14, \lfloor K/2 \rfloor)$)
| Repetitions $K$ | Max word length $2K$ | LB ($\varepsilon = 0$) | LB ($\varepsilon = 10^{-3}$) | LB ($\varepsilon = 5 \times 10^{-3}$) | LB ($\varepsilon = 10^{-2}$) | Beats $\max(4, 6) = 6$? |
|---:|---:|---:|---:|---:|---:|:---:|
| 24 | 48 | **$\ge 13$** (cap) | **$\ge 7$** | $\ge 6$ | $\ge 5$ | Yes ($\varepsilon \le 10^{-3}$) |
| 60 | 120 | **$\ge 15$** (cap) | **$\ge 7$** | **$\ge 7$** | **$\ge 7$** | Yes |
| 160 | 320 | **$\ge 15$** (cap) | **$\ge 9$** | **$\ge 7$** | **$\ge 7$** | Yes |
| 400 | 800 | **$\ge 15$** (cap) | **$\ge 11$** | **$\ge 9$** | **$\ge 8$** | Yes |
| 800 | 1600 | **$\ge 15$** (cap) | **$\ge 13$** | **$\ge 11$** | **$\ge 10$** | Yes |

#### 99% Finite-Shot Certification Along $(xz)^k$ (CERTIFIED)
| Mode | Repetitions $K$ | Max word length $2K$ | Shots / word | Total shots | **Certified $C_{\mathrm{classical}}$ LB** | Beats both unary ceilings ($> 6$)? |
|---|---:|---:|---:|---:|---:|:---:|
| Mode A (Fourier Cap) | 400 | 800 | 200 | `80,200` | $\ge 6$ | Ties $z^*$ ceiling |
| **Mode A (Fourier Cap)** | **1200** | **2400** | **100** | **`120,100`** | **$\ge 7$** | **YES ($7 > 6$)** |
| **Mode A (Fourier Cap)** | **2400** | **4800** | **80** | **`192,080`** | **$\ge 7$** | **YES ($7 > 6$)** |
| **Mode B (Split-Sample)** | **80** | **160** | **50,000** | **`4,050,000`** | **$\ge 7$** | **YES ($7 > 6$)** |
| **Mode B (Split-Sample)** | **160** | **320** | **100,000** | **`16,100,000`** | **$\ge 7$** | **YES ($7 > 6$)** |

**Significance:** With only **120,100 total shots**, a single qubit driven by two finite-order gates $R_x(\pi/2)$ and $R_z(\pi/3)$ certifies a rank-unrestricted classical state lower bound strictly greater than the exact infinite-horizon classical cost of either generator taken alone.

---

## 4. Theorem 4 — Unconditional Short-Depth Spectral Rank Beyond the Unary $L + 1$ Ceiling (PROVED & CERTIFIED)

On a unary alphabet $|\Sigma| = 1$, a depth-$L$ Hankel matrix $H_f^{(p, s)}$ with $p + s \le L$ has at most $\min(p+1, s+1) \le \lfloor L/2 \rfloor + 1$ rows and columns, and the shift-register construction forces $C_{\mathrm{classical}} \le L + 1$. On a binary alphabet $\Sigma = \{x, z\}$, the word count grows as $2^{L+1} - 1$ (so the trivial tree-automaton bound is $2^{L+1}-1$ rather than $L+1$), allowing short-depth Hankel blocks to witness quadratic classical-vs-quantum rank separation ($d^2$ vs. $d$) that cleanly breaks the *unary* $L + 1$ wall.

### Statement & Proof
Let $H_f \in [0, 1]^{m \times n}$ be the Hankel block of a process $f$ on prefixes $\mathcal{P} = \Sigma^{\le p}$ ($m = 2^{p+1}-1$) and suffixes $\mathcal{S} = \Sigma^{\le s}$ ($n = 2^{s+1}-1$), touching only words of length $\le L = p + s$.

1. **Unconditional Weyl + Hankel Matrix Hoeffding Lower Bound (PROVED):**
   Let $\widehat{H}$ be the empirical Hankel matrix from independent finite-shot Bernoulli samples on $\mathcal{W}_L = \Sigma^{\le L}$, and let $r_{\mathrm{Hoef}}(\alpha)$ be ANANKE v2's non-asymptotic Matrix Hoeffding operator-norm radius (`hankel_matrix_hoeffding_bound`, valid with probability $\ge 1 - \alpha$ even with shared words $uv = w$ because each word incidence matrix $E_w$ is a partial permutation). For **any** $N$-state classical realization $g$ with $\max_{w \in \mathcal{W}_L} |g(w) - f(w)| \le \varepsilon$, its Hankel matrix satisfies $\operatorname{rank}(H_g) \le N$ and $\|H_g - H_f\|_2 \le \sqrt{m n}\, \varepsilon$. By Weyl's singular-value inequality, on the $(1 - \alpha)$ Hoeffding event,
   $$\sigma_{N+1}(\widehat{H}) \le \sigma_{N+1}(H_g) + \|H_g - H_f\|_2 + \|\widehat{H} - H_f\|_2 \le 0 + \sqrt{mn}\,\varepsilon + r_{\mathrm{Hoef}}(\alpha).$$
   Consequently, defining $\tau := r_{\mathrm{Hoef}}(\alpha) + \sqrt{mn}\,\varepsilon + \eta_{\mathrm{SVD}}$ (with floating-point SVD perturbation guard $\eta_{\mathrm{SVD}}$),
   $$C_{\mathrm{classical}}(f; \varepsilon, \Sigma^{\le L}) \;\ge\; \#\!\left\{ k : \sigma_k(\widehat{H}) > \tau \right\}$$
   with probability at least $1 - \alpha$, with **ZERO rank-upper-bound assumption** and **ZERO Markov/Jordan structural assumption**. $\square$

2. **Verified Short-Depth $d^2$ vs. $d$ Separation Beyond the Unary $L + 1$ Wall (`CERTIFIED` for $d = 2, 3, 4, 5$; `CONJECTURAL / GENERIC` for arbitrary $d$):**
   For a $d$-dimensional quantum system ($C_{\mathrm{quantum}} = d$) driven by two generic Haar $U(d)$ unitaries $U_x, U_z$, the Liouville space $\mathrm{Herm}(\mathbb{C}^d)$ has real dimension $d^2$. Once $|\Sigma^{\le p}| = 2^{p+1} - 1 \ge d^2$ (i.e. $p = \lceil \log_2(d^2 + 1) - 1 \rceil$, depth $L = 2p$), our verified witnesses attain full rank $d^2$ explicitly for $d \in \{2, 3, 4, 5\}$ (giving quadratic classical-vs-quantum separation $C_{\mathrm{classical}} \ge d^2$ vs. $C_{\mathrm{quantum}} = d$ while breaking the unary $L + 1$ ceiling at $L = 6, 8, 10$); proving full spanning at minimal depth $p = \lceil\log_2(d^2+1)-1\rceil$ for all $d$ requires an explicit family witness for every $d$ and is left open in general.

### Certified Results (`results/certify_multisymbol_v4.json`)

Using deterministic two-symbol Haar $U(d)$ qudit constructions (`qudit_two_symbol_quantum_realization` in `src/ananke/ontology_gap.py`):

| Quantum system | $C_{\mathrm{quantum}} = d$ | Depth $L$ ($p, s$) | Unary wall $L + 1$ | Hankel shape | Words $|\mathcal{W}_L|$ | $\sigma_{d^2}(H_f)$ | Noiseless LB (up to $\varepsilon$) | 99% Finite-Shot LB (total shots) | Breaks unary $L+1$? |
|---|---:|---:|---:|---|---:|---:|---|---|---|
| Qubit ($d=2$, seed 11) | 2 | 6 (3, 3) | 7 | $15 \times 15$ | 127 | `1.8273` | $\ge 4$ ($\varepsilon = 0.01$) | $\ge 4$ (`63,500` shots) | No (see Thm 2) |
| **Qutrit ($d=3$, seed 5)** | **3** | **6 (3, 3)** | **7** | **$15 \times 15$** | **127** | **`0.3828`** | **$\ge 9$ ($\varepsilon = 0.01$)** | **$\ge 9$ (`63,500` shots, 500/word)** | **YES ($9 > 7$)** |
| Qutrit ($d=3$, seed 5) | 3 | 8 (4, 4) | 9 | $31 \times 31$ | 511 | `1.3526` | $\ge 9$ ($\varepsilon = 0.02$) | $\ge 9$ (`102,200` shots, 200/word) | Ties $L+1$ |
| **Two-Qubit ($d=4$, seed 9)** | **4** | **8 (4, 4)** | **9** | **$31 \times 31$** | **511** | **`0.5207`** | **$\ge 16$ ($\varepsilon = 0.01$)** | **$\ge 16$ (`306,600` shots, 600/word)** | **YES ($16 > 9$)** |
| **Ququint ($d=5$, seed 11)** | **5** | **8 (4, 4)** | **9** | **$31 \times 31$** | **511** | **`0.1227`** | **$\ge 25$ ($\varepsilon = 0.002$)** | **$\ge 25$ (`5,110,000` shots, 10k/word)** | **YES ($25 > 9$)** |
| **Ququint ($d=5$, seed 11)** | **5** | **10 (5, 5)** | **11** | **$63 \times 63$** | **2,047** | **`0.7755`** | **$\ge 25$ ($\varepsilon = 0.005$)** | **$\ge 25$ (`1,228,200` shots, 600/word)** | **YES ($25 > 11$)** |

**Soundness & Reproducible Calibration (`results/certify_multisymbol_v4.json`):**
- On a random 6-state classical 2-symbol HMM at $L = 8$ (2,000 shots/word, 1.022M total shots, $\alpha = 0.01$), Theorem 4 certifies $N \ge 1 \le 6$.
- Across 30 independent Monte Carlo trials on random 6-state classical 2-symbol HMMs (`mc_calibration_6state_hmm` in `certify_multisymbol_v4.py`, $L = 8$, 2,000 shots/word, $\alpha = 0.01$), Theorem 4 returned `max_lb = 2` and **0/30 false exclusions ($> 6$)**.

---

## 5. Unified Cross-Ontology Summary: Classical vs. Quantum on Identical Short-Depth Word Sets

The table below puts all four audited ANANKE v4 theorems side by side on the exact same word sets $\mathcal{W}$, comparing the quantum Hilbert-space dimension $C_{\mathrm{quantum}}(f; 0, \mathcal{W})$ against our **rank-unrestricted, 99% finite-shot certified** classical state lower bounds $C_{\mathrm{classical}}(f; 0, \mathcal{W})$ and the unary shift-register ceiling $L + 1$:

| Process & Word Set $\mathcal{W}$ | Method | $C_{\mathrm{quantum}}$ | Unary ceiling $L+1$ | **Certified $C_{\mathrm{classical}}$ (99% finite-shot)** | Total shots | Ontology gap $C_{\mathrm{cl}} / C_{\mathrm{q}}$ |
|---|---|---:|---:|---:|---:|---:|
| Pure 2-symbol qubit, $\Sigma^{\le 8}$ | **Thm 2** (Support Envelope) | **2** | 9 | **$\ge 8$** | 15.33M | **$\ge 4.0\times$** |
| Rational-gate qubit ($R_x(\pi/2), R_z(\pi/3)$), $\{(xz)^k\}_{k \le 1200}$ | **Thm 3** (Niven Synergy) | **2** | 4 ($x^*$), 6 ($z^*$) | **$\ge 7$** | 120.1k | **$\ge 3.5\times$** |
| Qutrit, $\Sigma^{\le 6}$ | **Thm 4** (Spectral Rank) | **3** | 7 | **$\ge 9$** ($> L+1$) | **63.5k** | **$\ge 3.0\times$** |
| Two-qubit, $\Sigma^{\le 8}$ | **Thm 4** (Spectral Rank) | **4** | 9 | **$\ge 16$** ($> L+1$) | **306.6k** | **$\ge 4.0\times$** |
| Ququint, $\Sigma^{\le 8}$ | **Thm 4** (Spectral Rank) | **5** | 9 | **$\ge 25$** ($> L+1$) | 5.11M | **$\ge 5.0\times$** |
| Ququint, $\Sigma^{\le 10}$ | **Thm 4** (Spectral Rank) | **5** | 11 | **$\ge 25$** ($> L+1$) | **1.228M** | **$\ge 5.0\times$** |

Every lower bound in the table requires **ZERO rank-upper-bound assumption** and **ZERO assumptions on the hidden classical transition structure**.

---

## 6. Avenue 3 — Fejes Tóth Polytope Scaling & Local Dynamical-vs-Static Upper Bounds (`PROVED` / `HEURISTIC` / `NUMERICAL`)

Why did ANANKE v3 observe that static simplex-box NMF on the mixed-qubit $15\times 15$ Hankel block already reached error `0.0066` at $N = 8$, whereas constructed two-symbol Bloch-polytope counterfeits still suffered error `0.310` at $N = 12$ and `0.049` at $N = 128$?

### 6.1 Fejes Tóth's Inradius Theorem (`PROVED`) & Isotropic Compounding Benchmark (`HEURISTIC`)

**Theorem (L. Fejes Tóth, 1953 — Spherical-Polytope Inradius Bound, PROVED).**
For every convex polytope $K_N \subset B^3$ with $N \ge 4$ vertices contained in the closed unit ball, its Euclidean inradius satisfies
$$\rho_{\mathrm{in}}(K_N) \;\le\; \rho_{\mathrm{FT}}(N) \;:=\; \frac{1}{\sqrt{3}}\,\cot\!\left(\frac{\pi N}{6(N - 2)}\right) \;=\; 1 - \frac{4\pi}{3\sqrt{3}\,N} + O(N^{-2}) \;\approx\; 1 - \frac{2.4184}{N},$$
with **exact equality** achieved by the regular tetrahedron ($N = 4$, $\rho_{\mathrm{FT}} = 1/3$), regular octahedron ($N = 6$, $\rho_{\mathrm{FT}} = 1/\sqrt{3}$), and regular icosahedron ($N = 12$, $\rho_{\mathrm{FT}} = \sqrt{(5 + 2\sqrt{5})/15} \approx 0.794654$).

*Epistemic clarification (`HEURISTIC`, NOT a lower bound):* Because the centered inball guarantees a feasible radial scale $\ge \rho_{\mathrm{in}}(K_N)$ in *every* direction while specific rotations can achieve larger vertex scales (e.g., at $N = 6$ our empirical rotated-vertex minimum scale is `0.7078 > 0.5774`), the compounded quantity $\frac{1}{2}(1 - \rho_{\mathrm{FT}}(N)^L)$ is an **isotropic worst-case scaling heuristic** for Bloch-polytope constructions, **not** a proved lower bound on dynamical error (and whether optimal dynamical classical models require $N = \Omega(L/\varepsilon)$ remains **CONJECTURAL / OPEN**).

### 6.2 Fejes Tóth Heuristic Benchmark vs. Two-Symbol Bloch-Polytope Counterfeits at $L = 7$ (`results/ontology_gap_v4.json`)

| Classical states $N$ | Fejes Tóth UB $\rho_{\mathrm{FT}}(N)$ (`PROVED`) | True polytope $\rho_{\mathrm{in}}(K_N)$ | Isotropic $L=7$ heuristic $\frac{1}{2}(1-\rho_{\mathrm{FT}}^7)$ (`HEURISTIC`) | Empirical pure-qubit $L=7$ max err (`NUMERICAL`) | Empirical mixed-qubit $L=7$ max err (`NUMERICAL`) |
|---:|---:|---:|---:|---:|---:|
| 4 | `0.33333` | `0.33333` | `0.4998` | `0.4985` | `0.4234` |
| 6 | `0.57735` | `0.57735` | `0.4893` | `0.4208` | `0.3627` |
| 8 | `0.68806` | `0.57735` | `0.4635` | `0.4362` | `0.3908` |
| 12 | `0.79465` | `0.79465` | `0.3999` | `0.3893` | `0.3102` |
| 20 | `0.87782` | `0.81892` | `0.2992` | `0.2851` | `0.2370` |
| 32 | `0.92395` | `0.88557` | `0.2126` | `0.2022` | `0.1611` |
| 64 | `0.96210` | `0.94230` | `0.1185` | `0.1272` | `0.0961` |
| 128 | `0.98108` | `0.97104` | `0.0626` | `0.0632` | `0.0493` |

Every geometric polytope satisfies `true_polytope_inradius <= fejes_toth_inradius_ub` (exact to 12+ digits at $N = 4, 6, 12$). Notice that the empirical errors frequently fall *below* the isotropic heuristic (e.g., by ~14% at $N = 6$), confirming that the heuristic is an order-of-magnitude scaling reference rather than a floor.

### 6.3 Local Upper-Bound Comparison: Static NMF vs. Monotone Two-Symbol Classical HMM Fits (`NUMERICAL`)

Comparing monotone upper bounds across $N = 4, 6, 8, 10, 12$ on all 127 words of length $\le 6$ — taking the minimum of multi-start L-BFGS-B HMM training, explicit Bloch-polytope realizations, and embedded smaller-$N$ models — against static $15\times 15$ simplex-box NMF (`results/ontology_gap_v4.json`):

#### Baseline Mixed Qubit ($C_{\mathrm{quantum}} = 2$, $L = 6$, 127 words)
| Classical states $N$ | Static $15\times 15$ NMF UB | Monotone Dynamical UB ($L=5$) | Monotone Dynamical UB ($L=6$) | Optimizer UB ratio ($L=6$) |
|---:|---:|---:|---:|---:|
| 4 | `0.12355` | `0.2508` | `0.3197` | `2.6×` |
| 6 | `0.01909` | `0.1595` | `0.2655` | `13.9×` |
| 8 | `0.00506` | `0.1467` | `0.2332` | `46.1×` |
| 10 | `0.00260` | `0.1157` | `0.1970` | `75.7×` |
| 12 | `0.00163` | `0.1157` | `0.1970` | `120.7×` |

#### Golden + Noble-3 Pure Qubit ($C_{\mathrm{quantum}} = 2$, $L = 6$, 127 words)
| Classical states $N$ | Static $15\times 15$ NMF UB | Monotone Dynamical UB ($L=5$) | Monotone Dynamical UB ($L=6$) | Optimizer UB ratio ($L=6$) |
|---:|---:|---:|---:|---:|
| 4 | `0.25016` | `0.3670` | `0.4356` | `1.7×` |
| 6 | `0.10662` | `0.3233` | `0.3712` | `3.5×` |
| 8 | `0.05592` | `0.2103` | `0.3712` | `6.6×` |
| 10 | `0.02445` | `0.2103` | `0.3712` | `15.2×` |
| 12 | `0.02445` | `0.2103` | `0.3712` | `15.2×` |

**Epistemic note (`NUMERICAL` / `CONJECTURAL`):** Both columns above are *upper bounds* produced by non-convex local optimizers (plus explicit polytope realizations); a large optimizer upper-bound ratio does **not** prove a lower bound on the true optimal dynamical error beyond Theorem 2. Turning this empirical gap into a certified dynamical lower bound is a prime open problem for ANANKE v5.

---

## 7. Honest Epistemic Scope Comparison (v2 vs. v3 vs. v4) & Open Targets for v5

> **Honest Epistemic Scope Box**
>
> | Release | Word set $\mathcal{W}$ | Structural assumption | Best 99% finite-shot certified $C_{\mathrm{classical}}$ | Beats unary $L+1$ at short $L \le 12$? |
> |---|---|---|---|---|
> | **ANANKE v2** | Two-symbol $\{x, z\}^{\le 7}$ | Fixed rank $\operatorname{rank}(H_f) = r$ | $N \ge 17$ (baseline), $N \ge 21$ (golden) | Conditional on $\operatorname{rank}(H_f) = 4$ |
> | **ANANKE v3** | Unary $\{a^k\}_{k \le L}$ | **None (rank-unrestricted)** | $N \ge 8$ ($L = 4000$, 200k shots), $N \ge 9$ ($L = 320$) | Impossible on unary ($N \le L + 1$ proved) |
> | **ANANKE v4 (Thm 2)** | Pure qubit $\{x, z\}^{\le 8}$ | **None (rank-unrestricted)** | **$N \ge 8$ at $L = 8$** (15.33M shots; $2\times$ rank 4 & $2\times$ Thm 1 ceiling) | Approaches $L+1 = 9$ (uniform $S^2$ ceiling $\le 12$) |
> | **ANANKE v4 (Thm 3)** | Rational-gate qubit $\{(xz)^k\}$ | **None (rank-unrestricted)** | **$N \ge 7 > \max(4, 6)$** (120.1k shots) | Breaks both infinite-horizon unary ceilings |
> | **ANANKE v4 (Thm 4)** | Qudit ($d=3,4,5$) $\{x, z\}^{\le L}$ | **None (rank-unrestricted)** | **$N \ge 9$ ($L=6$, 63.5k), $\ge 16$ ($L=8$, 307k), $\ge 25$ ($L=10$, 1.23M)** | **YES — breaks unary $L + 1$ ($d^2$ vs. $d$ rank gap)** |
>
> **Explicit Boundary (CONJECTURAL / OPEN):**
> 1. On a **single qubit ($d = 2$)** at fixed short depth $L \le 12$ with **zero rank-upper-bound assumption**, ANANKE v4 certifies $N \ge 8$ at $L = 8$ (Theorem 2, doubling both Hankel rank 4 and the linear-witness ceiling 4, and $20\times$ shallower than v3) and strictly breaks both single-generator infinite-horizon ceilings $\max(4, 6) = 6$ (Theorem 3), **but** strictly certifying $N > L + 1$ on a *single qubit* at $L \le 12$ remains **OPEN**.
> 2. Theorem 2 is purely **static** (it depends only on the Hankel entries $H_f(u, v)$ and never enforces that $P_{ua, \cdot} = P_{u, \cdot} M_a$ for shared stochastic operators $M_x, M_z$).
> 3. **Prime Target for ANANKE v5 (CONJECTURAL / OPEN):** Construct a **rank-unrestricted dynamical operator obstruction** combining noncommuting stochastic contraction inequalities on the $N$-simplex with multi-state support envelopes or noncommutative polynomial / SDP hierarchies to certify $N > L + 1$ on a single qubit at $L \le 8$.

---

## 8. Reproducibility & Verification

All modules use pure Python stdlib + NumPy/SciPy only:
- Core theory & verifiers:
  - `src/ananke/multisymbol_obstructions.py` (Theorems 1–4)
  - `src/ananke/ontology_gap.py` (`QuantumRealization`, Fejes Tóth bound, 2-symbol HMM optimizer)
- Unit tests (**70 tests total**: 13 v4 tests including Codex/Fable 5.2 soundness regressions + 57 v0–v3 tests):
  - `tests/test_multisymbol_obstructions_v4.py`
  - `tests/test_ontology_gap_v4.py`
- Reproducible experiment scripts & saved JSON outputs:
  - `experiments/certify_multisymbol_v4.py` $\to$ `results/certify_multisymbol_v4.json`
  - `experiments/ontology_gap_v4.py` $\to$ `results/ontology_gap_v4.json`

To re-run the complete test suite and both v4 experiments from `ananke-necessity-transformations/`:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
python experiments/certify_multisymbol_v4.py
python experiments/ontology_gap_v4.py
```
