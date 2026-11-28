# Frontier v2: Resolution of $m^* = 3$, Small-$m$ Ladder, and Exact $1 + \ln 2$ Completeness Barrier

**Date:** 28 November 2026  
**Scope:** Builds directly on `chairman-small-rows/` and `detector-chains/frontier_next/` without modifying any existing committed files. All lower bounds, structural barrier theorems, and algebraic identities carry standalone exact `fractions.Fraction` verifiers in [`code/`](code/) plus independent HiGHS MILP confirmations (allowing all off-support assignments).

---

## 1. Executive Summary

Recall that for fractional assignments $x \in [0, 1]^{m \times n}$ ($\sum_{i=1}^m x_{ij} = 1$) and strictly positive machine-dependent weights $d \in (0, D]^{m \times n}$ (normalized to $D = 1$),
$$
\Delta_i(t) = \sum_{j=1}^t d_{ij}(x_{ij} - y_{ij}), \qquad
\kappa_m = \sup_{m\text{-row instances}} \min_y \max_{i, t} |\Delta_i(t)|, \qquad
\kappa = \sup_{m \ge 1} \kappa_m.
$$

| Open Question / Target | Prior State (`frontier_next`) | This Work (`frontier_v2`) | Epistemic Status & Certificate |
|---|---|---|---|
| **Target 1:** Minimal machine count $m^*$ with $\kappa_{m^*} > 1$ | $m^* \in \{3, 4\}$ ($1 \le \kappa_3 \le 3$) | **$m^* = 3$ SETTLED!** $\kappa_3 \ge c_3^* \approx \mathbf{1.10172066}$ (and ultra-compact **$m = 3, n = 33$** with $\kappa_3 > 1001/1000$) | **PROVED** (Theorem 1) + **EXACT `Fraction`** ([`verify_m3_and_small_m_ladder.py`](code/verify_m3_and_small_m_ladder.py)) + **MILP-VERIFIED** ([`verify_independent_milp_v2.py`](code/verify_independent_milp_v2.py)) |
| **Target 1 (Bonus):** Tight small-$m$ lower-bound ladder | $\kappa_4 \ge 1.079253$; compact $m = 5, n = 47$ | **$\kappa_4 \ge 1.26624861$**, $\kappa_6 \ge 1.36255954$, $\kappa_8 \ge 1.41219508 > 1 + 1/e$, and general even-$m$ closed form $e^{-(c-1)} - (c - 1) = 2/m$ | **PROVED** (Theorem 2) + **EXACT `Fraction`** + **MILP-VERIFIED** ($m = 4$ at $1.24$, $m = 6$ at $1.32$, $m = 8$ at $1.37$) |
| **Target 2:** Breaking $1 + \ln 2 \approx 1.693147$ | Open ($\kappa \ge 1 + \ln 2$; beam search stalled) | **Still OPEN** ($\kappa \ge 1 + \ln 2$ unbroken), **AND PROVED** to be an exact completeness barrier for *all* non-monotone forced-chain + $q$-way disjoint-subtree splitting constructions | **PROVED OBSTRUCTION** (Theorems 3–4, [`verify_barrier_theorems.py`](code/verify_barrier_theorems.py)) + **MILP-VERIFIED** escape + **NUMERICAL/SEARCH** audit of 5 candidate non-disjoint escapes |

---

## 2. Target 1 — Settling $m^* = 3$ and the Zero-Pollution Small-$m$ Ladder

### 2.1 The Key Mechanism: Zero-Pollution Initial Split $J_0$

Why did 2-block ping-pong on $m = 3$ miss $1$ by $3.3 \times 10^{-7}$ in `frontier_next` Section 3.3, while $m = 4$ only reached $c_4^* \approx 1.079253$?
1. On $m = 3$, running Block 1 directly from $(0, 0, 0)$ only lifted $B$ to $p_1$, requiring a *second* coupling column $J_2$ on $\{B, H\}$ plus cleanup.
2. On $m = 4$, `frontier_next` Theorem 5 used $J_0$ on $\{B, R_0\}$ with weights $(1, 1)$ and then needed a second coupling column $J_2$ on $\{R_0, B\}$ to overflow $R_0$.

**New mechanism (Zero-Pollution Split $J_0$):** Put $J_0$ on $\{B, R_0\}$ (or $\{B, A\}$ for $m = 3$) with weights **$d_B = 1,\; d_{\text{other}} = \eta \ll 1$** and splits $x_B = u = 1 - \varepsilon$, $x_{\text{other}} = \varepsilon$ (all off-support rows have $x = 0, d = \eta$):
- **If $J_0 \not\to B$** (whether assigned to $R_0$ or off-support): $B = +u = 1 - \varepsilon$, while *every other row* stays within $[-\eta, +\eta]$!
- **If $J_0 \to B$**: $B = -(1 - u) = -\varepsilon$, while *every other row* stays within $[0, +\eta]$!

Thus $J_0$ splits $B$ into $\{-\varepsilon,\; 1 - \varepsilon\}$ with **zero pollution** of the remaining $m - 1$ rows. After $q$ clean ping-pong blocks lift $B$ by $+q p_1$:
- Every non-$(J_0 \to B)$ branch hits $B = u + q p_1 > c$ and **dies immediately**;
- The unique surviving branch ($J_0 \to B$) now has $B = u + q p_1 - 1 \approx q p_1$ high enough to be attacked **directly** by a final ping-pong block—with **no $J_{\text{final}}$ coupling column needed!**

---

### 2.2 Theorem 1 (PROVED): Three Machines Suffice ($m^* = 3$, $\kappa_3 \ge c_3^* \approx 1.10172066$)

**Theorem 1.** *Let $c_3^* \approx 1.1017206620$ be the unique real root of*
$$
2c - 1 \;=\; e^{-(c - 1)} + e^{1 - 2c}.
$$
*Then $\kappa_3 \ge c_3^* > 1$. Together with $\kappa_2 = 1$ (`chairman-small-rows`), the minimal number of machines on which the machine-dependent chairman bound exceeds $D$ is **$m^* = 3$**.*

*Proof.* Fix any $c \in (1, c_3^*)$ and use $3$ rows $\{B, A, H\}$ starting at $(0, 0, 0)$:
1. **Initial zero-pollution split $J_0$ on $\{B, A\}$:** $d_B = 1$, $d_A = d_H = \eta$, $x_B = u = 1 - \varepsilon$, $x_A = \varepsilon$, $x_H = 0$.
   - Every assignment $J_0 \not\to B$ (to $A$ or off-support to $H$) gives $B = u$, $A \ge -\eta$, $H \ge -\eta$.
   - The assignment $J_0 \to B$ gives $B = -(1 - u)$, $A = (1 - u)\eta \ge 0$, $H = 0$.
2. **Block 1 ($J_1$ on $\{B, H\}$ + 2-row ping-pong on $\{H, A\}$):** Put $J_1$ with $d_B = d_H = 1, d_A = \eta$ and $x_B = p_1, x_H = 1 - p_1$. If $J_1 \not\to H$, then $H \ge 1 - p_1 - \eta$ and $A \ge -2\eta$ in **all three** branches of $J_0$. By Theorem 2 of `frontier_next`, clean 2-row ping-pong on $\{H, A\}$ forces $J_1 \mapsto H$ whenever
   $$
   c - (1 - p_1) < e^{-(c - 1)} \iff p_1 < 1 - c + e^{-(c - 1)}.
   $$
   Choose $u + p_1 > c$ (which is automatically implied by Step 3 below since $e^{1 - 2c} < 1$):
   - Every $J_0 \not\to B$ branch immediately hits $B = u + p_1 > c$ and **dies**.
   - Only $J_0 \to B, J_1 \to H$ survives. Throughout Block 1's $\{H, A\}$ chain, $B$ only incurs off-support weight $\eta$, so at the end of Block 1:
     $$
     B \;\ge\; -(1 - u) + p_1 - (n_1 - 1)\eta \;=\; u + p_1 - 1 - O(\eta), \qquad A \;\ge\; -c.
     $$
3. **Block 2 (Dirty-helper ping-pong directly on $\{B, A\}$):** By Lemma C of `frontier_next`, dirty-helper 2-row ping-pong on $\{B, A\}$ (assuming only $A \ge -c$) explodes past $c$ whenever
   $$
   c - (u + p_1 - 1) < e^{1 - 2c} \iff u + p_1 > c + 1 - e^{1 - 2c}.
   $$
4. Letting $u \uparrow 1$ and $p_1 \uparrow 1 - c + e^{-(c - 1)}$, an admissible pair $(u, p_1) \in (0, 1)^2$ exists if and only if
   $$
   1 + \bigl(1 - c + e^{-(c - 1)}\bigr) > c + 1 - e^{1 - 2c} \iff 2c - 1 < e^{-(c - 1)} + e^{1 - 2c},
   $$
   i.e., $c < c_3^* \approx 1.1017206620$. Choosing $\eta > 0$ small enough absorbs all off-support drift. $\square$

*(Remark: Notice that $c_3^* \approx 1.101721$ on **3 machines** strictly exceeds the prior **4-machine** supremum $c_4^* \approx 1.079253$ of `frontier_next`!)*

#### Ultra-Compact $m = 3, n = 33$ Variant (PROVED + MILP-VERIFIED)
At budget $c = 1$, replacing Block 1's multi-level ping-pong with a single 1-level chain $H \to A$ ($k_1 = 10$, 9 columns) plus **one** cleanup column $Z_1$ on $\{H, A\}$ ($d_H = \eta, d_A = 1$) cleans $A$ back to $\ge -1/200$ (since $A$ has weight $1$ on every column of Block 1), so Block 2 only needs 7 short levels ($k = 4$, 21 columns) of clean ping-pong on $\{B, A\}$. This yields an **$m = 3, n = 33$** exact rational counterexample (smaller in both $m$ and $n$ than `frontier_next`'s $m = 5, n = 47$!). *(Note: at $c > 1$, the cleaned-helper variant gives $2c - 1 < e^{-c} + e^{2 - 2c} \implies c \approx 1.087 < c_3^*$, because cleaning $[-c, c]$ only guarantees $A \ge -(c - 1)$; hence dirty-helper Block 2 is asymptotically stronger while cleaned-helper Block 2 is much more compact at $c = 1$.)*

#### Exact Rational & Independent HiGHS MILP Certificates for $m = 3$
- **EXACT `Fraction`** ([`verify_m3_and_small_m_ladder.py`](code/verify_m3_and_small_m_ladder.py)):
  - Ultra-compact cleaned-helper ($m = 3, n = 33$): certified $\kappa_3 > \mathbf{1001/1000 = 1.001000}$
  - Dirty-helper Rung 1 ($n = 100$): certified $\kappa_3 > \mathbf{1.000000}$
  - Dirty-helper Rung 2 ($n = 366$): certified $\kappa_3 > \mathbf{1.050000}$
  - Dirty-helper Rung 3 ($n = 1535$): certified $\kappa_3 > \mathbf{1.080000}$ (strictly beating the old $m = 4$ supremum!)
  - Dirty-helper Rung 4 ($n = 12410$): certified $\kappa_3 > \mathbf{1.095000}$ (within $0.0068$ of $c_3^*$)
- **MILP-VERIFIED** ([`verify_independent_milp_v2.py`](code/verify_independent_milp_v2.py), off-support allowed):
  - $m = 3, n = 33$ (cleaned-helper): **INFEASIBLE at budget $1.00$** (`0.064s`)
  - $m = 3, n = 74$ (compact dirty-helper): **INFEASIBLE at budget $1.00$** (`0.003s`)
  - $m = 3, n = 1349$ (high-$c$ dirty-helper): **INFEASIBLE at budget $1.08$** (`0.066s`)

---

### 2.3 Theorem 2 (PROVED): Tight Even-$m$ Zero-Pollution Ladder ($\kappa_4 \ge 1.266249$, $\kappa_6 \ge 1.362560$, $\kappa_8 \ge 1.412195$)

**Theorem 2.** *For every even $m = 2q + 2 \ge 4$ ($q \ge 1$), let $c_m^* \in (1, 1 + W(1))$ be the unique root of*
$$
e^{-(c - 1)} - (c - 1) \;=\; \frac{2}{m}.
$$
*Then $\kappa_m \ge c_m^*$. In particular:*
- *$\kappa_4 \ge c_4^{**} \approx \mathbf{1.2662486082}$ (improving `frontier_next`'s $1.079253$ by $+0.1870$);*
- *$\kappa_6 \ge c_6^* \approx \mathbf{1.3625595433}$;*
- *$\kappa_8 \ge c_8^* \approx \mathbf{1.4121950815}$ (strictly exceeding the $L$-level fresh cascade supremum $1 + 1/e \approx 1.367879$ on just $8$ machines!);*
- *$\kappa_{10} \ge c_{10}^* \approx \mathbf{1.4424563704}$, and $c_m^* \uparrow 1 + W(1) \approx 1.5671432904$ as $m \to \infty$.*

*Proof.* Use rows $\{B, R_0, A_1, H_1, \dots, A_q, H_q\}$ ($m = 2q + 2$):
1. Apply zero-pollution $J_0$ on $\{B, R_0\}$ ($d_B = 1, d_{\text{other}} = \eta, x_B = u \uparrow 1$).
2. For $r = 1, \dots, q$, run Block $r$: $J_r$ on $\{B, A_r\}$ ($x_B = p_1$) followed by clean 2-row ping-pong on $\{A_r, H_r\}$. Every block forces $J_r \mapsto A_r$ whenever $p_1 < 1 - c + e^{-(c - 1)}$.
3. Every $J_0 \not\to B$ branch hits $B = u + q p_1 > c$ and dies (since $u + q p_1 > c + 1 - e^{-(c-1)} > c$). The surviving $J_0 \to B$ branch reaches $B = u + q p_1 - 1 \to q p_1$ while **$R_0$ remains completely fresh at $\ge -O(\eta)$**!
4. Run **clean** 2-row ping-pong directly on $\{B, R_0\}$, which explodes past $c$ whenever
   $$
   c - q p_1 < e^{-(c - 1)} \iff c - q\bigl(1 - c + e^{-(c - 1)}\bigr) < e^{-(c - 1)} \iff e^{-(c - 1)} - (c - 1) > \frac{1}{q + 1} = \frac{2}{m}. \quad \square
   $$

#### Exact Rational & Independent HiGHS MILP Certificates for Theorem 2
- **EXACT `Fraction`** ([`verify_m3_and_small_m_ladder.py`](code/verify_m3_and_small_m_ladder.py)):
  - $m = 4$: certified $\kappa_4 > \mathbf{1.200}$ ($n = 353$), $\mathbf{1.240}$ ($n = 1730$), $\mathbf{1.258}$ ($n = 13575$)
  - $m = 6$: certified $\kappa_6 > \mathbf{1.320}$ ($n = 1238$), $\mathbf{1.355}$ ($n = 20199$)
  - $m = 8$: certified $\kappa_8 > \mathbf{1.370}$ ($n = 1957$), $\mathbf{1.402}$ ($n = 21564$)
- **MILP-VERIFIED** ([`verify_independent_milp_v2.py`](code/verify_independent_milp_v2.py), off-support allowed):
  - $m = 4$: **INFEASIBLE at $1.20$** ($n = 321$, `0.021s`) and **at $1.24$** ($n = 2021$, `0.086s`)
  - $m = 6$: **INFEASIBLE at $1.32$** ($n = 1227$, `0.249s`)
  - $m = 8$: **INFEASIBLE at $1.37 > 1 + 1/e$** ($n = 1961$, `0.975s`)

---

## 3. Target 2 — Exact $1 + \ln 2$ Completeness Barrier & Obstruction Audit

We attacked $\kappa > 1 + \ln 2 \approx 1.69314718$ from seven distinct directions. **No construction broke $1 + \ln 2$**; instead, we discovered **why** every tree-splitting, non-monotone-weight, partial-drain, and pigeonhole variant stalls at the exact same constant $1 + \ln 2$, and proved two clean structural theorems pinning down the barrier unconditionally.

### 3.1 Theorem 3 (PROVED): Universal Non-Monotone Drain–Gain Optimality

**Theorem 3.** *Fix any $c > 1$, starting heights $(\alpha, \beta)$ with $u := c - \alpha \in (0, 1)$, any length $k \ge 2$, any (not necessarily monotone) weights $d_2, \dots, d_k \in (0, 1]$ on $X$ and $d_{Y,2}, \dots, d_{Y,k} \in (0, 1]$ on $Y$, and any splits $x_2, \dots, x_k \in [0, 1]$ such that every first deviation on $X$ reaches at least $c$:*
$$
\alpha - \sum_{i=2}^{j-1} d_i(1 - x_i) + d_j x_j \;\ge\; c \qquad (j = 2, \dots, k).
$$
*Let $\alpha_{\mathrm{end}} = \alpha - \sum_{j=2}^k d_j(1 - x_j)$ and $w := c - \alpha_{\mathrm{end}}$. Then $w \in [u, 1]$ and*
$$
\Delta_Y^{\mathrm{gain}} \;=\; \sum_{j=2}^k d_{Y,j}(1 - x_j) \;\le\; \ln\frac{w}{u} \;\le\; -\ln u, \qquad
\alpha_{\mathrm{end}} + \Delta_Y^{\mathrm{gain}} \;\le\; c - 1 - \ln u.
$$

*Proof.* Set $g_j := c - \bigl(\alpha - \sum_{i=2}^{j-1} d_i(1 - x_i)\bigr)$ ($j = 2, \dots, k + 1$), so $g_2 = u$ and $g_{k+1} = w$. The deviation inequality says $g_j \le d_j x_j$ for every $j = 2, \dots, k$. Hence:
1. $g_{j+1} = g_j + d_j(1 - x_j) \le d_j x_j + d_j(1 - x_j) = d_j \le 1$, so $w = g_{k+1} \in [u, 1]$.
2. If $x_j = 1$, then $1 - x_j = 0 = \ln(g_{j+1}/g_j)$. If $x_j < 1$, then $g_{j+1} - g_j = d_j(1 - x_j) \ge \frac{g_j}{x_j}(1 - x_j)$, whence $x_j \ge \frac{g_j}{g_{j+1}}$, and using $1 - t \le -\ln t$ for $t > 0$:
   $$
   1 - x_j \;\le\; 1 - \frac{g_j}{g_{j+1}} \;\le\; \ln\frac{g_{j+1}}{g_j}.
   $$
3. Summing $j = 2, \dots, k$ telescopes to $\Delta_Y^{\mathrm{gain}} \le \sum_{j=2}^k (1 - x_j) \le \ln(w/u) \le -\ln u$. Finally, $\alpha_{\mathrm{end}} + \Delta_Y^{\mathrm{gain}} \le c - w + \ln w - \ln u \le c - 1 - \ln u$ since $\ln w - w \le -1$ on $(0, 1]$ (attained uniquely at $w = 1$). $\square$

Verified in [`verify_barrier_theorems.py`](code/verify_barrier_theorems.py) across 5,000 random non-monotone rational chains.

---

### 3.2 Theorem 4 (PROVED OBSTRUCTION): Exact $1 + \ln 2$ Completeness Barrier via the $1$-Lipschitz Excess Invariant

**Theorem 4.** *Fix any budget $c \ge 1 + \ln 2$, let $h^* := c - e^{-(c - 1)} > 1$ be the 2-row ping-pong threshold, and define the $1$-Lipschitz row excess*
$$
E(a) \;:=\; \max\bigl(0,\; a - (h^* - 1)\bigr).
$$
*Consider any finite block starting from a single active row at height $h_0 \le 1$ (so total excess $E(h_0) \le 2 - h^* < 1$) plus unlimited fresh rows at height $0$ ($E(0) = 0$), built from any finite combination of:*
1. **Arbitrary forced fresh-row chains** $X \to Y_{\mathrm{fresh}}$ *(arbitrary length $k$, arbitrary non-monotone weights $d_j, d_{Y,j} \in (0, 1]$, arbitrary splits $x_j \in [0, 1]$, arbitrary stopping gap $w \in [u, 1]$);*
2. **Arbitrary $q$-way disjoint-subtree splits** *($q \ge 2$, arbitrary weights $d_i \in (0, 1]$, arbitrary splits $x_i \in \Delta_{q-1}$, partitioning the surviving rows into pairwise-disjoint subsets $I_1, \dots, I_q$—even allowing a branch $r$ to retain its own loser row $r \in I_r$!—for independent recursive killing);*
3. **2-row ping-pong leaf killers** *(killing any single row reaching height $> h^*$, i.e. $E(a) > 1$).*

*Then at least one surviving branch maintains total excess $\sum_{i \in I} E(a_i) < 1$ throughout, so no leaf ever crosses $h^*$. Hence **$1 + \ln 2$ is the exact supremum** of the entire class of disjoint-subtree forced-chain constructions.*

*Proof.* Induct on the invariant $S := \sum_{i \in I} E(a_i) < 1$ (which implies $a_i < h^*$ for all $i \in I$):
- **Base case:** $E(h_0) \le 1 - (h^* - 1) = 2 - h^* < 1$ since $h^* \ge 1 + \ln 2 - \frac{1}{2} = \frac{1}{2} + \ln 2 > 1$.
- **Forced fresh-row chain ($X \to Y_{\mathrm{fresh}}$):** If $a_X \le c - 1$, no forced chain is admissible. Otherwise $u := c - a_X \in (e^{-(c-1)}, 1)$. By Theorem 3, $a_X' = c - w$ ($w \in [u, 1]$) and $a_Y' \le \ln(w/u)$. Check all four sign cases of $(E(a_X'), E(a_Y'))$:
  1. $E(a_X') = E(a_Y') = 0 \implies E(a_X') + E(a_Y') = 0 \le E(a_X)$.
  2. $E(a_X') > 0, E(a_Y') = 0 \implies a_X' = c - w \le c - u = a_X \implies E(a_X') \le E(a_X)$.
  3. $E(a_X') = 0, E(a_Y') > 0 \implies a_Y' - a_X \le \ln(w/u) - (c - u) \le -\ln u + u - c < (c - 1) + e^{-(c-1)} - c = e^{-(c-1)} - 1 < 0$ (since $u \mapsto u - \ln u$ decreases on $(0, 1]$), so $E(a_Y') < E(a_X)$.
  4. $E(a_X') > 0, E(a_Y') > 0$:
     $$
     E(a_X') + E(a_Y') - E(a_X) \;\le\; (\ln w - w) + (u - \ln u) - (h^* - 1) \;<\; -1 + e^{-(c-1)} + (c - 1) - \bigl(c - e^{-(c-1)} - 1\bigr) \;=\; 2e^{-(c-1)} - 1 \;\le\; 0,
     $$
     since $c \ge 1 + \ln 2 \iff e^{-(c-1)} \le \frac{1}{2}$.
- **$q$-way disjoint-subtree split:** On branch $r \in J$ ($|J| = q \ge 2$), row $i \ne r$ changes by $+d_i x_i \le x_i$ and row $r$ changes by $-d_r(1 - x_r) \le 0$. Because $E$ is $1$-Lipschitz ($E(a + \delta) \le E(a) + \delta$ for $\delta \ge 0$) and nondecreasing, every row $i$ satisfies $E(a_i^{(r)}) \le E(a_i) + x_i$ (with $x_i = 0$ for $i \notin J$). Because $I_1, \dots, I_q$ are pairwise disjoint, each row $i$ appears in at most one $I_r$, so
  $$
  \sum_{r=1}^q \sum_{i \in I_r} E(a_i^{(r)}) \;\le\; \sum_{i \in I \cup J} \bigl(E(a_i) + x_i\bigr) \;=\; S + 1 \;<\; 2 \;\le\; q.
  $$
  Thus $\min_{r} \sum_{i \in I_r} E(a_i^{(r)}) < \frac{2}{q} \le 1$. $\square$

Verified numerically in [`verify_barrier_theorems.py`](code/verify_barrier_theorems.py) over 10,000 chains and 10,000 $q$-way splits ($q = 2..6$).

---

### 3.3 Obstruction Audit of Five Non-Disjoint / Alternative Mechanisms Beyond Theorem 4

Because Theorem 4 rules out *all* disjoint-subtree forced-chain trees, breaking $1 + \ln 2$ requires violating one of its hypotheses: (i) using an *existing* positive row $Y$ inside a chain (which increases excess by $u - \ln u - 1 > 0$ with zero "birth tax"), (ii) running *non-disjoint* shared continuations across branches, or (iii) finding an offline leaf killer beating $h^* = c - e^{-(c-1)}$. We tested five concrete mechanisms attempting to exploit these loopholes:

1. **Multi-accumulator pigeonhole $(h, f)$-trading across $N$ blocks (`OBSTRUCTION` + `NUMERICAL`):**
   Running a global accumulator $B$ over $N$ blocks where fraction $f$ sit at height $h$ trades fraction for height via $(h, f) \mapsto (h + \alpha, f - \alpha)$ (conserving $h + f$). Coupling this with 1-level chains (keeping $Y$, keeping $\min(X, Y)$, or binary-splitting) in a fine-grid DP ([`verify_barrier_theorems.py`](code/verify_barrier_theorems.py)) stalls strictly below $h_{\mathrm{pp}}$ at every $c > 1 + \ln 2$ (e.g., at $c = 1.70$, max reachable $h = 1.1322 < h_{\mathrm{pp}} = 1.2034$).
2. **Non-disjoint Branch-1 annihilation merge $K_1$ on $\{X, Y\}$ (`PROVED OBSTRUCTION`):**
   After Level 1 ($X \to Y$) yields $(c - 1, b)$ and a split $K_0$ on $\{X, Y\}$ gives Branch 1 $(c - 1 + x, b - t)$ ($t = 1 - x$) and Branch 2 $(c - 1 - x, b + t)$, running $X \to Z_1$ followed by an annihilation column $K_1$ on $\{X, Y\}$ with $d_X = 1, d_Y \in (0, 1]$ and $1 - \varepsilon = e^{-(c-1)}/t$ kills Branch 1's $K_1 \not\to X$ sub-branch via $\{X, Z_1\}$ ping-pong and forces $K_1 \to Y$ in Branch 2 (dropping $Y$ by only $d_Y \varepsilon$!). Remarkably, this **merges both branches back onto the single row $Y$** with zero tree branching—yet maximizing $\min(Y_{\mathrm{Branch 1}}, Y_{\mathrm{Branch 2}})$ over all $(t, d_Y)$ gives exactly $b + e^{-(c-1)}$, which again stalls at $c = 1 + \ln 2$!
3. **Target-$T < c$ chains with arbitrary $d_2 \ge T - h$ (`PROVED OBSTRUCTION`):**
   Running a chain $X \to Y$ targeting $T = h + u < c$ gives the exact identity $X_{\mathrm{end}} = (T - 1) + \sum_{j: C_j \not\to X} d_j \ge h + u + d_2 - 1$ on any deviating schedule, and $Y_{\mathrm{end}} = 1 - \frac{u}{d_2} - \ln d_2$ on the non-deviating schedule. Requiring $X_{\mathrm{end}} > h$ forces $u + d_2 > 1$, which bounds $Y_{\mathrm{end}} < 2 - \frac{1}{d_2} - \ln d_2 \le 1$; adding a post-chain split $K$ enforces $x \in [0, 1]$ and stalls at the same barrier.
4. **2-row pre-column + shared ping-pong leaf killer from $(1.20, 0)$ at $c = 1.70$ (`MILP-VERIFIED` + `OBSTRUCTION`):**
   A single weighted pre-column $(d_0 = 0.60, x_0 = 0.45)$ on $\{X, Z\}$ starting from $(1.20, 0)$ splits into Branch 1 $(0.87, +0.55)$ and Branch 2 $(1.47, -0.45)$, *both* of which individually explode past $1.70$ under $X \to Z$ ping-pong. However, in the **offline** game (single fixed column sequence), if $d_2 < d_0$, Branch 1 escapes by deviating early on $C_2$ and slipping below Branch 2 (confirmed explicitly as **MILP FEASIBLE** in [`verify_independent_milp_v2.py`](code/verify_independent_milp_v2.py) Check `[7]` for `pp2 + pp1`); conversely, enforcing $d_2 \ge d_0$ analytically forces $R_Z^{(B)} \le \ln(1 + x_0) - x_0 - \ln(1 - x_2) < -\ln(1 - x_2)$, failing to beat Lemma B.
5. **Unconstrained C exact-BFS simulated annealing (`NUMERICAL/SEARCH`):**
   Compiled `-O3` exact reachable-set annealing over unconstrained $(x, d)$ on $m = 2$ from $(1, 0)$ ($n = 10, 14$, with/without dummy off-support), $m = 3$ from $(1, 0, 0)$ ($n = 10$), and $m = 3$ from $(0, 0, 0)$ ($n = 10, 14$) reached at most `1.3201` (2-row from $(1,0)$), `1.2173` (3-row from $(1,0,0)$), and `0.8758` (3-row from $(0,0,0)$), discovering no small-$n$ mechanism breaking $1 + W(1)$ on 2 rows or $1 + \ln 2$ on 3 rows.

---

## 4. Updated Status of the Programme & Remaining Open Frontier

1. **Minimal machine count $m^*$ (`SETTLED`):** **$m^* = 3$**, with $\kappa_2 = 1$ and $1.10172066 \le \kappa_3 \le 3$ (and an explicit $3 \times 33$ rational counterexample to $\kappa_3 \le 1$).
2. **Small-$m$ bounds (`SHARPENED`):**
   - $1.10172066 \le \kappa_3 \le 3$
   - $1.26624861 \le \kappa_4 \le 4$
   - $1.36255954 \le \kappa_6 \le 6$
   - $1.41219508 \le \kappa_8 \le 8$
3. **Global constant $\kappa$ (`OPEN`, sharpened obstruction):** $1 + \ln 2 \le \kappa \le \infty$. By Theorem 4, any further lower-bound progress past $1 + \ln 2 \approx 1.693147$ must leave the entire class of disjoint-subtree forced-chain trees and construct a genuinely **offline, non-disjoint** multi-row gadget (or lower the 2-row offline leaf-killer threshold below $c - e^{-(c-1)}$). Conversely, proving $\kappa < \infty$ (or even $\kappa_m = o(m)$) remains open and must be offline and non-mass-conserving.

---

## 5. Verification Commands

All results in this report are reproduced cleanly by:

```bash
python detector-chains/frontier_v2/code/verify_m3_and_small_m_ladder.py
python detector-chains/frontier_v2/code/verify_independent_milp_v2.py
python detector-chains/frontier_v2/code/verify_barrier_theorems.py
```
