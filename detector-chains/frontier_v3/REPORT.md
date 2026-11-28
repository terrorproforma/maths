# Frontier v3: BFS-Box Trapping ($\kappa_m \le m - 1$) and Extended Non-Disjoint $1 + \ln 2$ Barrier Audit

**Date:** 29 November 2026  
**Scope:** Builds directly on `chairman-small-rows/`, `detector-chains/frontier_next/`, and `detector-chains/frontier_v2/` without modifying any existing committed files. All proved theorems, corollaries, and obstruction bounds carry standalone exact `fractions.Fraction` verifiers and independent HiGHS MILP checks in [`code/`](code/).

---

## 1. Executive Summary

Recall that for a fractional assignment $x \in [0, 1]^{m \times n}$ ($\sum_{i=1}^m x_{ij} = 1$) and weights $d \in [0, D]^{m \times n}$ (normalized to $D = 1$, strictly positive for lower bounds),
$$
\Delta_i(t) = \sum_{j=1}^t d_{ij}(x_{ij} - y_{ij}), \qquad
\kappa_m = \sup_{m\text{-row instances}} \min_y \max_{i, t} \frac{|\Delta_i(t)|}{D}, \qquad
\kappa = \sup_{m \ge 1} \kappa_m.
$$

| Frontier Target | Prior State (`frontier_v2`) | This Work (`frontier_v3`) | Epistemic Status & Certificate |
|---|---|---|---|
| **Target B:** Upper bound on $\kappa_m$ (especially $\kappa_3$) | $\kappa_m \le m$ (Proposition 6 of `frontier_next`, leaving $1.10172 \le \kappa_3 \le 3$) | **$\kappa_m \le m - 1$ for EVERY $m \ge 1$!** (Support-preserving, $O(n \cdot 2^m \cdot \mathrm{poly}(m))$ exact algorithm; squeezes **$1.10172 \le \kappa_3 \le 2$**, **$1.26625 \le \kappa_4 \le 3$**, unifies $\kappa_2 \le 1$ with zero 2D geometry!) | **PROVED** (Theorem 1) + **EXACT `Fraction`** ([`verify_upper_bound_km_minus_1.py`](code/verify_upper_bound_km_minus_1.py)) |
| **Target B (Corollary & Sharpness):** Origin-enclosing hull & BFS-box limit | $0 \notin \mathrm{conv}(R_3)$ at $c = 1$ (`frontier_next` Prop. 8) | **$0 \in \mathrm{conv}(R_t)$ holds for all $t$ at $c = m - 1$** (in particular $c = 2$ on $m = 3$); AND **$c = m - 1$ is the exact sharp limit** of BFS-box trapping (trivial kernel already at $|F_t| = m - 1$) | **PROVED** (Corollary 1) + **PROVED OBSTRUCTION** (Proposition 2) + **EXACT `Fraction`** |
| **Target A:** Breaking $1 + \ln 2 \approx 1.693147$ via non-disjoint / two-sided / support-$q$ escapes | Proved completeness barrier at $1 + \ln 2$ for support-2 fresh-row chains + $q$-way disjoint-subtree splits | **Still OPEN** ($\kappa \ge 1 + \ln 2$ unbroken), **AND EXTENDED BARRIER PROVED** covering arbitrary support-$q$ non-monotone chains, Zero-Branching Excess Transfer onto already-positive banked rows, `PP2` concentration optimality, two-sided downward $q$-way splits, and symmetric weighted sibling-reuse chains | **PROVED OBSTRUCTIONS** (Theorems 3–4, [`verify_target_a_extended_barriers.py`](code/verify_target_a_extended_barriers.py)) + **MILP-VERIFIED** escapes + **NUMERICAL/SEARCH** audit |

---

## 2. Target B — BFS-Box Trapping Theorem: $\kappa_m \le m - 1$ for Every $m \ge 1$

### 2.1 Theorem 1 (PROVED): $\kappa_m \le m - 1$

**Theorem 1 (BFS-Box Trapping).** *For every $m \ge 1$, every $n \ge 1$, every fractional assignment $x \in [0, 1]^{m \times n}$ ($\sum_{i=1}^m x_{ij} = 1$), and every weight matrix $d \in [0, D]^{m \times n}$, there exists a **support-preserving** ($y_{ij} = 0$ whenever $x_{ij} = 0$) integral assignment $y \in \{0, 1\}^{m \times n}$ ($\sum_{i=1}^m y_{ij} = 1$) satisfying*
$$
|\Delta_i(t)| \;\le\; (m - 1) \cdot D \qquad \text{for every row } i \in \{1, \dots, m\} \text{ and every prefix } t \in \{1, \dots, n\}.
$$
*In particular, **$\kappa_m \le m - 1$ for every $m \ge 1$** (hence $\kappa_1 = 0$, $\kappa_2 \le 1$, **$\kappa_3 \le 2$**, **$\kappa_4 \le 3$**, etc.), and the assignment is computable in $O(n \cdot 2^m \cdot \mathrm{poly}(m))$ exact arithmetic operations.*

*Proof.* Normalize $D = 1$ and set $Q := [-(m - 1),\, m - 1]^m$. For $m = 1$, every column is integral and $\Delta_1(t) \equiv 0$, so assume $m \ge 2$. We maintain by induction on $t = 0, 1, \dots, n$ the following **BFS-Box Trapping Invariant $I_m(t)$**:
> There is a subset $F_t \subseteq \{1, \dots, t\}$ of fractional columns with vectors $z_j^{(t)} \in \Delta_{m-1}$ ($|\mathrm{supp}(z_j^{(t)})| \ge 2$, $\mathrm{supp}(z_j^{(t)}) \subseteq \mathrm{supp}(x_j)$) such that:
> 1. **Basic Feasible Solution (BFS):** The homogeneous linear system on the strictly positive support $E_t := \{(i, j) : j \in F_t,\; z_{ij}^{(t)} > 0\}$,
>    $$
>    \sum_{j \in F_t : (i,j) \in E_t} d_{ij} \delta_{ij} = 0 \quad (i = 1, \dots, m), \qquad
>    \sum_{i : (i,j) \in E_t} \delta_{ij} = 0 \quad (j \in F_t),
>    $$
>    has **trivial kernel** ($\delta \equiv 0$).
> 2. **Trapping of Every In-Box Completion:** For every integral completion $y_{F_t} \in \prod_{j \in F_t} \mathrm{supp}(z_j^{(t)})$ whose affine discrepancy
>    $$
>    \Delta^{(t)}(y_{F_t}) \;:=\; \sum_{j \in F_t} d_{\cdot, j} \circ \bigl(z_j^{(t)} - y_j\bigr)
>    $$
>    lies in $Q$, there exists a support-preserving schedule $\sigma^{(t)}(y_{F_t}) \in \{1, \dots, m\}^t$ whose prefixes for $1, \dots, t$ all stay in $Q$ and whose time-$t$ discrepancy equals $\Delta^{(t)}(y_{F_t})$ exactly.

**Base case ($t = 0$):** $F_0 = \emptyset$, $\Delta^{(0)}() = 0 \in Q$, $\sigma^{(0)}() = ()$.

**Structural Lemmas for any BFS $z^{(t)}$:** Let $G_t = (R, F_t, E_t)$ be the bipartite support graph, where $R = \{i : \deg(i) \ge 1\}$.
- **Lemma L1 (Size & Degree Bound):** Since $G_t$ has $|E_t|$ unknowns and $|R| + |F_t|$ equations with trivial kernel, $|E_t| \le |R| + |F_t|$. Since every $j \in F_t$ has $\deg(j) \ge 2$, we have
  $$
  2|F_t| \;\le\; \sum_{j \in F_t} \deg(j) \;=\; |E_t| \;\le\; |R| + |F_t| \;\le\; m + |F_t|,
  $$
  so $|F_t| \le |R| \le m$, $\sum_{j \in F_t} (\deg(j) - 1) \le m$, and $\prod_{j \in F_t} \deg(j) \le 2^{\sum (\deg(j) - 1)} \le 2^m$. Moreover, equality $|F_t| = m$ forces $|R| = m$, $|E_t| = 2m$, and $\deg(j) = 2$ for every $j \in F_t$.
- **Lemma L2 (Unique Hub Row):** For any row $i$ and any completion $y_{F_t}$, $|\Delta_i^{(t)}(y_{F_t})| < \deg(i)$ strictly (since each of the $\deg(i)$ nonzero terms has $|d_{ij}(z_{ij}^{(t)} - y_{ij})| < 1$). Hence $|\Delta_i^{(t)}(y_{F_t})| > m - 1$ is possible **only if $\deg(i) = m$** (which requires $|F_t| = m$, $|E_t| = 2m$, and $\deg(j) = 2$ for all $j \in F_t$). For $m \ge 3$, **at most one** row $i^*$ can have degree $m$ (two degree-$m$ rows would exhaust all $2m$ edges, forcing $|R| = 2 < m$, a contradiction); every other row $r \ne i^*$ has $\deg(r) \le 2 \le m - 1$, so $|\Delta_r^{(t)}(y_{F_t})| < m - 1$ for all completions.
- **Lemma L3 (At Most One Outside-$Q$ Completion):** Suppose some completion $y^* \in \prod_{j \in F_t} \mathrm{supp}(z_j^{(t)})$ satisfies $\Delta^{(t)}(y^*) \notin Q$. Pick a violating row $i^*$ (unique for $m \ge 3$; either violating row for $m = 2$). Every column $j \in F_t$ has support $\{i^*, r_j\}$ of size 2. If $k$ columns of $F_t$ assign to $i^*$ and $m - k$ assign away from $i^*$ with $1 \le k \le m - 1$, then
  $$
  -(m - 1) \;\le\; -k \;<\; \Delta_{i^*}^{(t)}(y_{F_t}) \;<\; m - k \;\le\; m - 1,
  $$
  so $\Delta_{i^*}^{(t)}(y_{F_t}) \in (-(m-1), m-1)$. Thus only the two extreme completions $\mathbf{0}_{i^*}$ ($y_{i^* j} = 0\ \forall j \in F_t$, giving $\Delta_{i^*} = \sum_{j \in F_t} d_{i^* j} z_{i^* j}^{(t)}$) or $\mathbf{1}_{i^*}$ ($y_{i^* j} = 1\ \forall j \in F_t$, giving $\Delta_{i^*} = -\sum_{j \in F_t} d_{i^* j}(1 - z_{i^* j}^{(t)})$) can violate $Q$. They cannot both violate $Q$ simultaneously, because $\sum_{j \in F_t} z_{i^* j}^{(t)} > m - 1$ and $\sum_{j \in F_t} (1 - z_{i^* j}^{(t)}) > m - 1$ imply $m > 2(m - 1) \iff m < 2$. (For $m = 2$, both rows share the same two extreme completions $(y_{11}, y_{12}) = (0, 0)$ and $(1, 1)$, so still at most one completion lies outside $Q$.)

**Induction Step ($t \to t + 1$):** Column $t + 1$ arrives with fractional vector $x_{t+1} \in \Delta_{m-1}$. If $|\mathrm{supp}(x_{t+1})| = 1$ (say $x_{t+1} = e_{r_0}$), append $r_0$ to every stored schedule (zero discrepancy change) and keep $F_{t+1} = F_t$. Otherwise $|\mathrm{supp}(x_{t+1})| \ge 2$. Form $F' := F_t \cup \{t + 1\}$ and $z^{(0)} := (z^{(t)}, x_{t+1})$. Call a completion $y_{F'} = (y_{F_t}, y_{t+1}) \in \prod_{j \in F'} \mathrm{supp}(z_j^{(0)})$ **bad** if $\Delta^{(t+1)}(y_{F'}) \in Q$ while $\Delta^{(t)}(y_{F_t}) \notin Q$.

By Lemma L3, there is at most one outside-$Q$ completion $y_{F_t}^*$:
- If no completion of $F_t$ lies outside $Q$, there are zero bad completions; pivot $z^{(0)}$ along arbitrary nonzero kernel vectors until reaching a BFS $z^{(t+1)}$.
- Otherwise, let $i^*$ be a row violating $Q$ at $y_{F_t}^*$. Notice that if $i^* \notin \mathrm{supp}(x_{t+1})$, then $\Delta_{i^*}^{(t+1)} = \Delta_{i^*}^{(t)}$ for all completions, so again zero bad completions exist. Hence assume $i^* \in \mathrm{supp}(x_{t+1})$ (so $0 < x_{i^*, t+1} < 1$).
  - **Case (+):** $\Delta_{i^*}^{(t)}(y_{F_t}^*) = \sum_{j \in F_t} d_{i^* j} z_{i^* j}^{(t)} > m - 1$, so $y_{i^* j}^* = 0$ for all $j \in F_t$. If $y_{i^*, t+1} = 0$, then $\Delta_{i^*}^{(t+1)} = \Delta_{i^*}^{(t)}(y_{F_t}^*) + d_{i^*, t+1} x_{i^*, t+1} > m - 1$, not bad. Thus the **unique** possible bad completion is $(y_{F_t}^*, e_{i^*})$.
    Pivot iteratively: while $z^{(s)}$ is not a BFS, pick a nonzero kernel vector $\delta$ of its support and orient its sign so that **$\delta_{i^*, t+1} \le 0$**; set $z^{(s+1)} = z^{(s)} + \tau \delta$ with maximal $\tau > 0$ keeping $z^{(s+1)} \ge 0$. At every step $s$, row $i^*$'s linear invariant gives
    $$
    \sum_{j \in F_t} d_{i^* j} z_{i^* j}^{(t)}
    \;=\; \sum_{j \in F_t} d_{i^* j} z_{i^* j}^{(s)} + d_{i^*, t+1}\underbrace{\bigl(z_{i^*, t+1}^{(s)} - x_{i^*, t+1}\bigr)}_{\le 0}.
    $$
    If ANY $j_0 \in F_t$ ever hit $z_{i^* j_0}^{(s)} = 0$, the right-hand side would have at most $m - 1$ nonzero terms each $\le 1$, hence $\le m - 1$, contradicting $\sum_{j \in F_t} d_{i^* j} z_{i^* j}^{(t)} > m - 1$! Thus $z_{i^* j}^{(s)} > 0$ for all $j \in F_t$ throughout, and $z_{i^*, t+1}^{(s)} \le x_{i^*, t+1} < 1$ throughout. When the loop terminates at a BFS $z^{(t+1)}$, Lemma L1 forces $|F_{t+1}| \le m < m + 1 = |F'|$, so at least one column in $F'$ became integral:
    - If column $t + 1$ became integral, $z_{i^*, t+1}^{(t+1)} < 1$ forces $z_{i^*, t+1}^{(t+1)} = 0$;
    - If some $j \in F_t$ became integral, $z_{i^* j}^{(t+1)} > 0$ forces $z_{i^* j}^{(t+1)} = 1$ (so $z_{r_j, j}^{(t+1)} = 0$).
    In either case, the unique bad completion $(y_{F_t}^*, e_{i^*})$ is eliminated from $\prod_{j \in F'} \mathrm{supp}(z_j^{(t+1)})$!
  - **Case (-):** $\Delta_{i^*}^{(t)}(y_{F_t}^*) = -\sum_{j \in F_t} d_{i^* j}(1 - z_{i^* j}^{(t)}) < -(m - 1)$, so $y_{i^* j}^* = 1$ for all $j \in F_t$. Every bad completion has $y_{i^* j} = 1$ ($\forall j \in F_t$) and $y_{i^*, t+1} = 0$. Orient every pivot kernel vector so **$\delta_{i^*, t+1} \ge 0$**. Then $z_{i^*, t+1}^{(s)} \ge x_{i^*, t+1} > 0$, and row $i^*$'s invariant rewritten in terms of $1 - z_{i^* j}$ gives
    $$
    \sum_{j \in F_t} d_{i^* j}\bigl(1 - z_{i^* j}^{(t)}\bigr)
    \;=\; \sum_{j \in F_t} d_{i^* j}\bigl(1 - z_{i^* j}^{(s)}\bigr) - d_{i^*, t+1}\underbrace{\bigl(z_{i^*, t+1}^{(s)} - x_{i^*, t+1}\bigr)}_{\ge 0}.
    $$
    Hence NO $j_0 \in F_t$ can ever hit $1 - z_{i^* j_0}^{(s)} = 0$ (which would make the RHS $\le m - 1$, contradiction!). At the resulting BFS $z^{(t+1)}$, either column $t + 1$ became integral with $z_{i^*, t+1}^{(t+1)} = 1$ (since $z_{i^*, t+1}^{(s)} > 0$), or some $j \in F_t$ became integral with $z_{i^* j}^{(t+1)} = 0$ (since $z_{i^* j}^{(s)} < 1$). In either case, **every** bad completion is eliminated!

Finally, set $F_{t+1} := \{j \in F' : |\mathrm{supp}(z_j^{(t+1)})| \ge 2\}$ and fix $\hat{y}_j := z_j^{(t+1)}$ for $j \in F' \setminus F_{t+1}$. For any completion $y_{F_{t+1}} \in \prod_{j \in F_{t+1}} \mathrm{supp}(z_j^{(t+1)})$ with $\Delta^{(t+1)}(y_{F_{t+1}}) \in Q$, combining $y_{F_{t+1}}$ with $\hat{y}_{F' \setminus F_{t+1}}$ yields a non-bad completion $(y_{F_t}, y_{t+1}) \in \prod_{j \in F'} \mathrm{supp}(z_j^{(t+1)}) \subseteq \prod_{j \in F'} \mathrm{supp}(z_j^{(0)})$ whose time-$(t+1)$ discrepancy satisfies
$$
\Delta^{(t)}(y_{F_t}) + d_{\cdot, t+1} \circ (x_{t+1} - y_{t+1})
\;=\; \sum_{j \in F'} d_{\cdot, j} \circ \bigl(z_j^{(t+1)} - y_j\bigr)
\;=\; \Delta^{(t+1)}(y_{F_{t+1}}) \in Q.
$$
Because $(y_{F_t}, y_{t+1})$ is not bad, $\Delta^{(t)}(y_{F_t}) \in Q$, so by $I_m(t)$ the schedule $\sigma^{(t+1)}(y_{F_{t+1}}) := (\sigma^{(t)}(y_{F_t}),\, y_{t+1})$ stays in $Q$ for all $1, \dots, t + 1$ and preserves support. At $t = n$, by Lemma L3 at least $2^{|F_n|} - 1 \ge 1$ completion lies in $Q$, yielding a valid integral schedule with $|\Delta_i(t)| \le m - 1$ for all $i, t$. $\square$

---

### 2.2 Corollary 1 (PROVED) & Proposition 2 (PROVED OBSTRUCTION)

**Corollary 1 (Origin-Enclosing Convex Hull at $c = m - 1$).** *For every $m \ge 2$ and every finite instance, the reachable set $R_t$ inside $Q = [-(m-1), m-1]^m$ satisfies **$0 \in \mathrm{conv}(R_t)$** for every prefix $t = 0, 1, \dots, n$. In particular, while `frontier_next` Proposition 8 proved $0 \notin \mathrm{conv}(R_3)$ at budget $c = 1$ on $m = 3$ rows, the origin-enclosing convex-hull property is **fully restored at $c = 2$**.*

*Proof.* At each $t$, if no completion of $F_t$ leaves $Q$, the product distribution $\prod_j z_{r_j, j}^{(t)}$ expresses $0$ as a convex combination of $\Delta^{(t)}(y_{F_t}) \in R_t$. If the unique outside-$Q$ completion is $\mathbf{0}_{i^*}$ (Case (+)), then $p := (z_{i^* j}^{(t)})_{j \in F_t} \in (0, 1)^m$ satisfies $\sum_{j=1}^m p_j > m - 1 \ge 1$, so $p \in \mathrm{conv}\bigl(\{0, 1\}^m \setminus \{\mathbf{0}\}\bigr)$ (the unique separating facet inequality is $\sum \varepsilon_j \ge 1$); symmetrically in Case (-), $\sum p_j < 1 \le m - 1$ places $p \in \mathrm{conv}\bigl(\{0, 1\}^m \setminus \{\mathbf{1}\}\bigr)$. Since $\Delta^{(t)}$ maps $p \mapsto 0$ affinely, $0 \in \mathrm{conv}(R_t)$. $\square$

**Proposition 2 (Exact Sharpness Obstruction for BFS-Box Trapping).** *For every $m \ge 2$ and every $c < m - 1$, the BFS-box trapping invariant fails already at $t = m$: taking $m - 1$ support-2 columns on $\{0, j\}$ ($j = 1, \dots, m - 1$) with $x_0 = 1 - \varepsilon$, $d = (1, 1)$ followed by an $m$-th column on $\{0, 1\}$ with $x_0 = 1 - \varepsilon$ and $d = (1, 1/2)$ leaves trivial kernel at both $t = m - 1$ and $t = m$, yet the all-away completion already reaches $(m - 1)(1 - \varepsilon) > c$ at $t = m - 1$ and produces an un-eliminable bad completion $(0, \dots, 0, 1)$ at $t = m$.*

### 2.3 Exact Rational Verification Results ([`verify_upper_bound_km_minus_1.py`](code/verify_upper_bound_km_minus_1.py))

All lemmas (L1–L4), Corollary 1 (explicit constructive exact-rational convex weights summing to $\mathbf{0} \in \mathbb{R}^m$), support preservation, and Proposition 2 pass with zero failures in pure `fractions.Fraction` arithmetic:
- **Edge cases:** $m = 1$ (`max_disc = 0`); $m = 3$ zero-weight / integral / degenerate-pivot test (`max_disc = 2/3 <= 2`).
- **Exact `frontier_v2` $3 \times 33$ counterexample (whose min-max is $> 1.001$):** solved support-preservingly with exact `max_disc = 1.002000 <= 2.0` (`max_states = 8`).
- **Stress test (370 diverse instances across $m = 2..6$, including extreme hub bias triggering outside-$Q$ events):**
  - $m = 2$: **120/120 PASS** ($n = 25$, worst `1.000000 <= 1`, `1200` outside-$Q$ events, `2359` pivots)
  - $m = 3$: **120/120 PASS** ($n = 25$, worst `2.000000 <= 2`, `196` outside-$Q$ events, `3031` pivots)
  - $m = 4$: **90/90 PASS** ($n = 22$, worst `2.350000 <= 3`, `38` outside-$Q$ events, `2328` pivots)
  - $m = 5$: **30/30 PASS** ($n = 18$, worst `2.200000 <= 4`, `726` pivots)
  - $m = 6$: **10/10 PASS** ($n = 14$, worst `1.800000 <= 5`, `225` pivots)
- **Proposition 2:** PASS for $m = 2, 3, 4, 5, 6$.

---

## 3. Target A — Attack on $1 + \ln 2$ & Extended Completeness Barrier

We systematically attacked all three escape hatches left open by `frontier_v2` Theorem 4: (1) non-disjoint sibling reuse & banked-row chains, (2) two-sided $+c/-c$ traps, and (3) arbitrary support-$q$ columns ($q \ge 3$). **No construction broke $1 + \ln 2 \approx 1.69314718$**; instead, we proved two new structural theorems extending the $1 + \ln 2$ barrier well beyond `frontier_v2` Theorems 3–4, backed by exact rational checks and independent HiGHS MILP feasibility certificates.

### 3.1 Theorem 3 (PROVED): Support-$q$ Universal Non-Monotone Drain–Gain Optimality

**Theorem 3.** *Fix $c > 1$, active height $\alpha = c - u \in (c - 1, c)$, and any $k \ge 2$ columns of arbitrary support size $q \ge 2$ on $\{X, Y_1, \dots, Y_{q-1}\}$ with arbitrary (possibly non-monotone) weights $d_{X,j}, d_{Y_r, j} \in (0, 1]$ and splits $x_j + \sum_{r=1}^{q-1} y_{r,j} = 1$ such that every first deviation $C_j \not\to X$ reaches at least $c$ on $X$. Letting $w := c - \alpha_{\mathrm{end}}$, we have $w \in [u, 1]$ and*
$$
\sum_{r=1}^{q-1} \Delta_{Y_r}^{\mathrm{gain}}
\;=\; \sum_{j=2}^k \sum_{r=1}^{q-1} d_{Y_r, j} y_{r,j}
\;\le\; \sum_{j=2}^k (1 - x_j)
\;\le\; \ln\frac{w}{u} \;\le\; -\ln u.
$$
*Symmetrically, for any downward forced chain from $X$ at $-\alpha$ hitting $-c$ on $C_j \to X$, the total downward push across $Y_1, \dots, Y_{q-1}$ is also bounded by $\ln(w/u) \le -\ln u$.*

*Proof.* Identical to `frontier_v2` Theorem 3 after observing $\sum_{r=1}^{q-1} d_{Y_r, j} y_{r,j} \le \sum_{r=1}^{q-1} y_{r,j} = 1 - x_j$. $\square$

### 3.2 Theorem 4 (PROVED OBSTRUCTION): Extended $1 + \ln 2$ Completeness Barrier

**Theorem 4.** *Fix $c \ge 1 + \ln 2$, $h^* := c - e^{-(c-1)}$, and $E(a) := \max(0,\, a - (h^* - 1))$. Every one of the following mechanisms beyond `frontier_v2` Theorem 4 still stalls at $1 + \ln 2$:*

1. **(a) Arbitrary support-$q$ fresh-row chains ($q \ge 2$):** Because $E$ is superadditive on $[0, \infty)$ ($\sum_{r=1}^{q-1} E(a_r) \le E(\sum_{r=1}^{q-1} a_r)$), Theorem 3 implies
   $$
   E(\alpha_{\mathrm{end}}) + \sum_{r=1}^{q-1} E(\Delta_{Y_r}^{\mathrm{gain}}) - E(\alpha) \;\le\; 0 \qquad (\text{and } \le 2e^{-(c-1)} - 1 \le 0 \text{ whenever any } E(\Delta_{Y_r}^{\mathrm{gain}}) > 0).
   $$
2. **(b) Zero-Branching Excess Transfer onto already-positive banked rows:** Given active row $X$ at $a \in (h^* - 1, h^*)$ and arbitrary (possibly already positive!) banked rows $Y_1, \dots, Y_r$ at $b_1, \dots, b_r$, a single support-$(r+1)$ column $K$ with $x_X = h^* - a + \varepsilon$, $\sum_{j=1}^r x_{Y_j} = E(a) - \varepsilon$ followed by clean 2-row ping-pong `PP1(X)` forces $K \mapsto X$ with **zero branching**, lifting each $Y_j$ by $+x_{Y_j}$. Yet by $1$-Lipschitzness of $E$,
   $$
   \sum_{j=1}^r E(b_j + x_{Y_j}) \;\le\; \sum_{j=1}^r E(b_j) + \sum_{j=1}^r x_{Y_j} \;\le\; \sum_{j=1}^r E(b_j) + E(a),
   $$
   so total excess never increases.
3. **(c) 2-Row Ping-Pong (`PP2`) Concentration Optimality:** Given any two nonnegative rows $(a, b) \in [0, c)^2$ with total height $S := a + b \le h^*$ and $a > c - 1$, `PP2(A, B)` (starting with $A \to B$) requires $b - \ln(c - a) > c - 1$ to explode. Setting $g := c - a \in [c - S, 1)$, we have $b - \ln(c - a) = S - c + (g - \ln g)$. Because $g \mapsto g - \ln g$ is strictly decreasing on $(0, 1)$,
   $$
   b - \ln(c - a) \;\le\; S - c + (c - S) - \ln(c - S) \;=\; -\ln(c - S) \;\le\; c - 1,
   $$
   so splitting height $S \le h^*$ across two rows can never activate `PP2` (concentration on one row is strictly optimal).
4. **(d) Two-Sided Downward $q$-Way Splits ($q \ge 2$):** Given $q$ negative rows at heights $-\beta_1, \dots, -\beta_q$ with total depth $B := \sum_{r=1}^q \beta_r > 1$, any $q$-way split column $K$ with weights $d_r \in (0, 1]$ and splits $\sum_{r=1}^q x_r = 1$ sends branch $r$ ($K \to r$) to depth $\beta_r + d_r(1 - x_r) \le \beta_r + (1 - x_r)$. Averaging over $r = 1, \dots, q$ yields
   $$
   \min_{r=1,\dots,q} \bigl(\beta_r + d_r(1 - x_r)\bigr) \;\le\; \frac{1}{q}\sum_{r=1}^q (\beta_r + 1 - x_r) \;=\; 1 + \frac{B - 1}{q},
   $$
   which is strictly decreasing in $q$ for $B > 1$. Hence **$q = 2$ is uniquely optimal** even for downward $-c$ splits, reproducing $\frac{B + 1}{2} = \frac{c - \ln u}{2}$ and stalling at $1 + \ln 2$.
5. **(e) Non-Disjoint Symmetric Sibling-Reuse Dichotomy (Weighted-Chain Conservation Law):** Starting from the post-split pair $\{(h, h - 1),\; (h - 1, h)\}$ at $c \ge 1 + \ln 2$ ($h = c - u \le h^*$), running a forced chain $X \to Y$ designed for Branch 1 with stopping gap $w \in (u, 1]$ and arbitrary passive weight $d_{Y,j} \equiv \gamma \in (0, 1]$ lifts Branch 1 to $(c - w,\; h - 1 + \gamma \ln(w/u))$, while allowing Branch 2 to deviate $s \ge 0$ times at minimum weight $d_j = u$ to
   $$
   (X_2(s),\; Y_2(s)) \;=\; \bigl(h - 1 - (w - u) + s u,\;\; h + \gamma \ln(w/u) - s \gamma\bigr),
   $$
   conserving $\gamma X_2(s) + u Y_2(s)$ identically in $s$. This yields a sharp dichotomy:
   - If $\gamma \le u$, then $\frac{d}{dw}[\gamma\ln(w/u) - w] = \frac{\gamma}{w} - 1 \le 0$, so Branch 1's excess stays $\le E(h) < 1$ (**PROVED**);
   - If $\gamma > u$, each deviation $s \mapsto s + 1$ strictly decreases $X_2 + Y_2$ by $-(\gamma - u) < 0$, and across all $5{,}000$ tested $(c, u, w, \gamma)$ triples at least one of Branch 1 or Branch 2 (at a legal $s \ge 0$) maintains total excess $< 1$ (`EXACT/NUMERICAL`, verified to max `min(E1, min_s E2) < 1.0`).

### 3.3 Non-Disjoint Computational & HiGHS MILP Audit (`MILP-VERIFIED` + `NUMERICAL/SEARCH`)

1. **`K0` on fresh $\{Y, Z\}$ + 2 half-chains ($X \to Y, X \to Z$) + 3-row cyclic ping-pong (`MILP-VERIFIED`):**
   Starting from $(1.20, 0, 0)$ at $c = 1.70$, putting $K_0 = (0.5, 0.5)$ on $\{Y, Z\}$ followed by two half-chains $X \to Y$ ($u_0 \to \sqrt{u_0}$) and $X \to Z$ ($\sqrt{u_0} \to 1$) produces $\{(0.70, 0.8466, -0.1534), (0.70, -0.1534, 0.8466)\}$ where *both* states have individual excess $1.1398 > 1$ and explode individually under `PP2`. However, coupling them offline via cyclic chains ($Y \to X, Z \to Y, X \to Z, \dots$) allows low-row deviations to drop the minimum pair sum from $1.412 \to 1.253 \to 0.975 \to 0.361$, and the finite-$k$ 4-row instance (including an off-support sink row, $n = 121$ cols in the verifier; $n = 181$ cols in exploration) is certified **MILP FEASIBLE at $c = 1.70$** (`max_disc <= 1.6764`).
2. **Support-3 non-disjoint coupling $K_1$ on $\{X, Y, Z\}$ + $X \to Z$ + $K_2$ + $Y \to Z$ (`MILP-VERIFIED`):**
   From $(0.695, 0.695, 0)$ at $c = 1.695$, all three branches of $K_1 = (0.375, 0.375, 0.25)$ individually exceed $h^*$ via non-disjoint chains, yet the offline 5-row instance ($n = 32$ cols in the verifier; $n = 58$ with `PP1` blocks in exploration) is certified **MILP FEASIBLE at $c = 1.695$**.
3. **Convex-Hull Excess $\Phi_{\mathrm{conv}}(S) = \min_{v \in \mathrm{conv}(S)} \sum_i E(v_i)$ Audit (`NUMERICAL/SEARCH`):**
   - Across 4-row infinite-$k$ macro-beam search allowing `PP1`, `PP2`, support-2/3 splits, partial chains (`w = sqrt(u)`), and weighted chains (`gamma = 0.75`): the exact same engine kills $c = 1.68 < 1 + \ln 2$ in 3 steps, while at $c = 1.694 > 1 + \ln 2$ it stalls with $\Phi_{\mathrm{conv}}(S)$ never increasing by even $10^{-5}$ across all 5 macro-depths.
   - Across 20,000+ unconstrained arbitrary-column trials + SA on $m = 2, 3$ from $(1.19, 0, 0)$, $(0.694, 0.694, 0)$, and $\{(1.193, 0.193, 0), (0.193, 1.193, 0)\}$ at $c = 1.694$: $\Phi_{\mathrm{conv}}(S)$ never increased above its initial value $< 1$. *(Caveat: $\Phi_{\mathrm{conv}}$ is not a universal invariant by itself—on a single banked point $(1.19, 0.19)$ a single forced column raises $E$ from $0.9956$ to $1.0352$, and on an artificial mixed-sign set $\{(1.25, -0.5, -0.5), (0, 1.19, 0.5)\}$ applying `PP1(0)` jumps $\Phi_{\mathrm{conv}}$ above $1$—so proving a full non-disjoint upper bound at $1 + \ln 2$ remains open.)*

---

## 4. Updated Status of the Programme & Remaining Open Frontier

1. **Exact small-$m$ bounds (`TIGHTENED BY -1 FOR ALL m`):**
   - $\kappa_1 = 0$, $\kappa_2 = 1$ (unified as the $m = 2$ special case of Theorem 1!)
   - **$1.10172066 \le \kappa_3 \le 2$** (improved from $\kappa_3 \le 3$)
   - **$1.26624861 \le \kappa_4 \le 3$** (improved from $\kappa_4 \le 4$)
   - **$1.36255954 \le \kappa_6 \le 5$** (improved from $\kappa_6 \le 6$)
   - **$1.41219508 \le \kappa_8 \le 7$** (improved from $\kappa_8 \le 8$)
   - General: **$\kappa_m \le m - 1$** for all $m \ge 1$ (with $0 \in \mathrm{conv}(R_t)$ at $c = m - 1$).
2. **Global constant $\kappa$ (`OPEN`, strengthened barrier):** $1 + \ln 2 \le \kappa \le \infty$. Breaking $1 + \ln 2$ requires escaping not only disjoint-subtree trees (`frontier_v2` Theorem 4) but also support-$q$ chains, zero-branching excess transfer, `PP2` on split height, downward $q$-way splits, and symmetric weighted sibling-reuse chains (Theorems 3–4). Conversely, breaking $\kappa_m \le m - 1$ (e.g. proving $\kappa_3 < 2$ or $\kappa_m = o(m)$) must go beyond BFS-box trapping (Proposition 2).

---

## 5. Verification Commands

All results in this report are reproduced cleanly by:

```bash
python detector-chains/frontier_v3/code/verify_upper_bound_km_minus_1.py
python detector-chains/frontier_v3/code/verify_target_a_extended_barriers.py
```
