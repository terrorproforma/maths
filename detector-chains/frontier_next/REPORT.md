# Next-Frontier Theorems for Machine-Dependent Weighted Chairman Assignment

**Date:** 28 November 2026  
**Scope:** Builds directly on `chairman-counterexample/`, `detector-chains/`, and `origin/claude/clever-davinci-ztxm29:chairman-small-rows/`. All lower bounds, upper bounds, and algebraic identities carry standalone exact `fractions.Fraction` verifiers in [`code/`](code/) plus independent HiGHS MILP confirmations.

---

## 1. Executive Summary of Results

For a fractional assignment $x \in [0, 1]^{m \times n}$ ($\sum_{i=1}^m x_{ij} = 1$) and strictly positive machine-dependent weights $d \in (0, D]^{m \times n}$ (normalize $D = \max_{i,j} d_{ij} = 1$), define the row-prefix discrepancy of an integral assignment $y \in \{0, 1\}^{m \times n}$ ($\sum_{i=1}^m y_{ij} = 1$) by
$$
\Delta_i(t) = \sum_{j=1}^t d_{ij}(x_{ij} - y_{ij}), \qquad
\kappa_m = \sup_{m\text{-row instances}} \min_y \max_{i, t} \frac{|\Delta_i(t)|}{D}, \qquad
\kappa = \sup_{m \ge 1} \kappa_m.
$$

| Quantity / Open Question | Prior Best | This Work | Proof / Certificate |
|---|---|---|---|
| Lower bound on $\kappa$ | $1 + W(1/e) \approx 1.278465$ | **$1 + \ln 2 \approx 1.693147$** (via $1 + 1/e \to 1 + W(1) \to 1 + \ln 2$) | Theorems 1–3; [`verify_cascade_and_pingpong.py`](code/verify_cascade_and_pingpong.py) (LB $\ge 1.681499$) & [`verify_independent_milp.py`](code/verify_independent_milp.py) |
| Minimal $m^*$ with $\kappa_{m^*} > 1$ | $m^* \in [3, 11]$ | **$m^* \in \{3, 4\}$** ($\kappa_4 \ge 1.079253$; compact $m = 5, n = 47$) | Theorems 4–5; [`verify_small_rows_m4_m5.py`](code/verify_small_rows_m4_m5.py) & [`verify_independent_milp.py`](code/verify_independent_milp.py) |
| Upper bound on $\kappa_m$ | $\kappa_m \le 2m$ (Bárány–Grinberg) | **$\kappa_m \le m$** (strictly $< m$, support-preserving, poly-time) | Theorem 6; [`verify_upper_bound_km.py`](code/verify_upper_bound_km.py) |
| Range for $\kappa_3$ | $1 \le \kappa_3 \le 6$ | **$1 \le \kappa_3 \le 3$**, and $0 \notin \mathrm{conv}(R_3)$ in 3 columns | Theorem 6 + Proposition 8; [`verify_small_rows_m4_m5.py`](code/verify_small_rows_m4_m5.py) |
| Open Problem 3 of `detector-chains` | 2000-trial empirical LP sweep | **Proved unconditionally** for all nondecreasing $d$ | Theorem 7; [`verify_split_optimality_proof.py`](code/verify_split_optimality_proof.py) |

---

## 2. Problem B (Lower Bound): Breaking the Lambert-$W$ Barrier to $\kappa \ge 1 + \ln 2$

In `detector-chains/`, single-level detector chains on fresh row pairs $\{A_b, H_b\}$ hit the exact supremum $1 + W(1/e) \approx 1.278465$, and every attempt to beat it by composing banked blocks across blocks failed due to entry pollution, accumulator venting, and disjunctive exits.

**Key conceptual shift:** Do **not** carry banked height *between* blocks. Instead, amplify height **inside each fresh block** before coupling to the global accumulator $B$. Because every row inside block $b$ starts fresh (at $\ge -O(\eta)$) and every off-support assignment *adds* nonnegative discrepancy $+d_{ij} x_{ij} \ge 0$ to both support rows while subtracting only $\eta$ from the recipient, **internal amplification suffers zero entry pollution and zero accumulator venting**, and retains fractional support two throughout.

### 2.1 The Primitive: One Chain Level (Drain–Gain Identity)

Fix a target budget $c > 1$. Suppose an active row $X$ starts at height $\Delta_X \ge \alpha$ with $0 < c - \alpha < 1$, and a passive row $Y$ starts at height $\Delta_Y \ge \beta$. Append $k - 1$ geometric chain columns $C_2, \dots, C_k$ on $\{X, Y\}$ with weights $d_j = r^{k - j}$ on $X$ ($d_k = 1$, $r \in (0, 1)$ chosen so $d_2 = r^{k-2} \ge c - \alpha$) and weight $1$ on $Y$, and splits
$$
x_2 = \frac{c - \alpha}{d_2} \in (0, 1], \qquad x_j = r \in (0, 1) \quad (j = 3, \dots, k).
$$

**Lemma A (Single-Level Drain–Gain).** *Assume every prefix stays within $[-c, c]$. If any column $C_j$ is not assigned to $X$ (whether assigned to $Y$ or off-support), let $j$ be the first such column. Then at prefix $C_j$, row $X$ reaches height $\ge c$. Otherwise, all $k - 1$ columns are assigned to $X$, and immediately after $C_k$:*
$$
\Delta_X \;\ge\; \alpha - \sum_{j=2}^k d_j(1 - x_j) \;=\; \alpha - \bigl(1 - (c - \alpha)\bigr) \;=\; \mathbf{c - 1},
$$
$$
\Delta_Y \;\ge\; \beta + \sum_{j=2}^k (1 - x_j) \;=\; \beta + \bigl(1 - x_2 + (k - 2)(1 - r)\bigr).
$$
*In the limit $k \to \infty$ with $d_2 \downarrow c - \alpha$ (so $x_2 \uparrow 1$ and $(k - 2)(1 - r) \to -\ln(c - \alpha)$):*
$$
\Delta_X \;\longrightarrow\; c - 1, \qquad \Delta_Y \;\longrightarrow\; \beta - \ln(c - \alpha).
$$

*Proof.* The telescoping drain sum is exact for every $k \ge 3$:
$$
\sum_{j=2}^k d_j(1 - x_j) = d_2\left(1 - \frac{c - \alpha}{d_2}\right) + \sum_{j=3}^k r^{k-j}(1 - r) = (d_2 - (c - \alpha)) + (1 - d_2) = 1 - (c - \alpha).
$$
At the first deviation $C_j$: for $j = 2$, $\Delta_X \ge \alpha + d_2 x_2 = c$; for $j \ge 3$, the drain before $C_j$ is $d_{j-1} - (c - \alpha)$ and $d_j x_j = d_{j-1}$, so $\Delta_X \ge \alpha - (d_{j-1} - c + \alpha) + d_{j-1} = c$. Off-support assignments deny both $X$ and $Y$ and only preserve or raise these inequalities (up to the explicit $\eta$-bookkeeping below). $\square$

---

### 2.2 Theorem 1 ($L$-Level Fresh Cascade): $\kappa \ge 1 + 1/e \approx 1.36787944$

**Theorem 1.** *For every $\varepsilon > 0$, there is a finite support-2, strictly positive instance with $D = 1$ on which every integral assignment incurs prefix discrepancy at least $1 + \frac{1}{e} - \varepsilon$. Hence $\kappa \ge 1 + 1/e \approx 1.3678794412$.*

*Proof.* Fix $c \in (1,\; 1 + 1/e)$. In each block $b = 1, \dots, N$, take fresh rows $A_b, H_{b,1}, \dots, H_{b,L}$ and append $J_b$ on $\{B, A_b\}$ ($x_B = p, x_{A_b} = 1 - p$, weights $1, 1$) followed by $L$ chained levels:
$$
\text{Level } 1:\; A_b \to H_{b,1}, \qquad \text{Level } 2:\; H_{b,1} \to H_{b,2}, \qquad \dots, \qquad \text{Level } L:\; H_{b,L-1} \to H_{b,L}.
$$
If $J_b$ is denied to $A_b$, then $A_b$ enters Level $1$ at $\alpha_0 = 1$ (up to $-p - O(\eta)$), and each $H_{b,r}$ enters Level $r$ at $\beta = 0$ (up to $-O(\eta)$). By Lemma A, as $k \to \infty$, the heights satisfy the recurrence
$$
\alpha_0 = 1, \qquad \alpha_{r+1} = -\ln(c - \alpha_r).
$$
For $c < 1 + 1/e$, we have $\alpha + e^{-\alpha} \ge 1 + 1/e > c$ for every $\alpha \ge 1$, so $-\ln(c - \alpha) > \alpha$ strictly on $[1, c)$. Moreover $c - \alpha_r \le c - 1 < 1/e < 1$ throughout, keeping every level admissible. Hence $\alpha_0 < \alpha_1 < \dots$ strictly exceeds $c$ at some finite level $L = L(c)$. Choosing $k$ large enough per level, $p > 0$ small enough, $N = \lceil (c + 1)/p \rceil$, and $\eta$ small enough absorbs all $p$ and $\eta$ drift (re-verified exactly in [`verify_cascade_and_pingpong.py`](code/verify_cascade_and_pingpong.py)): every block forces $J_b \mapsto A_b$, and finally $\Delta_B \ge Np - (n - N)\eta > c$. $\square$

- **Exact certified full-instance rungs:** `L=2, k=16` $\implies \mathbf{1.309999}$ (`m=601, n=6200`); `L=3, k=35` $\implies \mathbf{1.347999}$; `L=8, k=90` $\implies \mathbf{1.363999}$.
- **Independent MILP confirmation:** A 12-column, 4-row 2-level block (`k1=8, k2=5`, off-support allowed) has MILP min-max **$1.285000 > 1 + W(1/e) \approx 1.278465$**.

---

### 2.3 Theorem 2 (2-Row Ping-Pong Cascade): $\kappa \ge 1 + W(1) = 1 + \Omega \approx 1.56714329$

Look again at Lemma A: at the end of Level $1$ ($A \to H$), row $A$ does **not** drop to $0$—it drops to **$\mathbf{c - 1 > 0}$**! Instead of introducing a fresh row $H_2$ at height $0$ for Level $2$, we immediately **loop Level $2$ back from $H$ onto $A$**, giving $A$ a free head start of $\beta = c - 1$! Alternating $A \to H \to A \to H \to \dots$ uses **only two fresh rows per block** (identical to `detector-chains`).

**Theorem 2.** *For every $\varepsilon > 0$, there is a finite support-2, strictly positive instance with $D = 1$ (and only $2N + 1$ rows) forcing prefix discrepancy at least $1 + W(1) - \varepsilon$, where $\Omega = W(1) \approx 0.5671432904$ satisfies $\Omega e^\Omega = 1$. Hence $\kappa \ge 1 + \Omega \approx 1.5671432904$.*

*Proof.* Fix $c \in (1,\; 1 + \Omega)$. On two fresh rows $\{A, H\}$ starting from $(1, 0)$ (after $J_b$ denied to $A$):
- **Level 1 ($A \to H$):** $A$ drops to $c - 1$, and $H$ rises from $0$ to $\alpha_1 = -\ln(c - 1)$.
  Check admissibility of Level $2$: the gap on $H$ is
  $$
  u_1 := c - \alpha_1 = c + \ln(c - 1) = 1 + (c - 1) + \ln(c - 1) < 1,
  $$
  because $(c - 1) + \ln(c - 1) < 0 \iff (c - 1)e^{c - 1} < 1 \iff c - 1 < W(1) = \Omega$.
- **Levels $r \ge 2$ (alternating $H \to A$ and $A \to H$):** At entry to every level $r \ge 2$, the passive row already sits at $c - 1$! By Lemma A, the active row drops to $c - 1$, and the passive row rises to $\alpha_r = (c - 1) - \ln(c - \alpha_{r-1})$. Setting $u_r := c - \alpha_r$ (the remaining gap to $c$),
  $$
  u_r \;=\; c - \bigl((c - 1) - \ln u_{r-1}\bigr) \;=\; \mathbf{1 + \ln u_{r-1}} \qquad (r \ge 2).
  $$
  Since $1 + \ln u < u$ strictly for all $u \in (0, 1)$, the sequence $1 > u_1 > u_2 > \dots$ has no fixed point in $(0, 1)$ and therefore crosses $0$ (i.e., $\alpha_r > c$) in finitely many levels! Note also that every level's active drain is a constant independent of $p$ and $\eta$, so $A$'s $(p, \eta)$ sensitivity stays $(1, E)$ and $H$'s stays $(0, E)$ across all levels without exponential error blowup. $\square$

- **Exact certified full-instance rungs:** `c=1.40, k=10` (4 levels) $\implies \mathbf{1.395000}$; `c=1.50, k=15` (11 levels) $\implies \mathbf{1.497999}$; `c=1.55, k=25` (50 levels) $\implies \mathbf{1.548995}$; `c=1.562, k=40` (213 levels) $\implies \mathbf{1.561479}$.
- **Independent MILP confirmation:** A 29-column, 3-row ping-pong block (`c=1.40`, 4 levels, off-support allowed) has MILP min-max **$1.390000 > 1 + 1/e \approx 1.367879$**.

---

### 2.4 Theorem 3 (Recursive Binary-Tree Splitting + Ping-Pong): $\kappa \ge 1 + \ln 2 \approx 1.69314718$

Why did 2-row ping-pong stop at $1 + \Omega$? Because at $c > 1 + \Omega$, after Level $1$ ($A \to H$) we have $A = c - 1$ and $H = -\ln(c - 1)$, with $H < c - 1$ so neither row alone is within distance $1$ of $c$! Yet **their sum** $A + H = (c - 1) - \ln(c - 1)$ still strictly exceeds $1$ for every $c \in (1, 2)$!

**Lemma B (Height-Amplifying Binary Split).** *Suppose at budget $c$, row $X$ sits at height $h$ with $0 < c - h < 1$, and $Y$ is a fresh row at $0$. Run Level $1$ ($X \to Y$) so $(X, Y) \to (c - 1,\; -\ln(c - h))$, followed by **one** weight-$(1, 1)$ split column $K$ on $\{X, Y\}$ with $x_X = \frac{1 + Y - X}{2} \in [0, 1]$ and $x_Y = 1 - x_X$. Then regardless of how $K$ is assigned (to $X$, to $Y$, or off-support), **at least one** of $\{X, Y\}$ reaches height:*
$$
h' \;=\; \frac{1 + (c - 1) - \ln(c - h)}{2} \;=\; \mathbf{\frac{c - \ln(c - h)}{2}}.
$$
*Moreover, attaching independent killer subtrees on $X$ (using fresh rows disjoint from $Y$) and then on $Y$ (using fresh rows disjoint from $X$'s subtree) kills **both** branches with zero interference.*

**Theorem 3.** *For every $\varepsilon > 0$, there is a finite support-2, strictly positive instance with $D = 1$ forcing prefix discrepancy at least $1 + \ln 2 - \varepsilon$. Hence $\kappa \ge 1 + \ln 2 \approx 1.6931471806$.*

*Proof.* Fix $c \in (1,\; 1 + \ln 2)$. Consider the amplification map $h \mapsto h' = \frac{c - \ln(c - h)}{2}$, or in gap coordinates $u := c - h \in (0, 1)$:
$$
u' = c - h' = \frac{c + \ln u}{2}, \qquad u - u' = \frac{2u - \ln u - c}{2}.
$$
The function $\phi(u) = 2u - \ln u$ on $(0, 1)$ attains its unique global minimum at $u = 1/2$, with value
$$
\min_{u \in (0, 1)} (2u - \ln u) \;=\; 2 \cdot \frac{1}{2} - \ln\frac{1}{2} \;=\; \mathbf{1 + \ln 2 \approx 1.6931471806}.
$$
Therefore, for every $c < 1 + \ln 2$, we have $u - u' \ge \frac{1 + \ln 2 - c}{2} > 0$ uniformly on $(0, 1)$! Starting from $h_0 = 1$ ($u_0 = c - 1 < 1$), after finitely many binary-split depths $D = D(c)$, the guaranteed child height $h_D$ strictly crosses the ping-pong threshold $c - e^{-(c - 1)}$, after which a 2-row ping-pong leaf killer (Theorem 2) finishes each of the $2^D$ leaves in finitely many levels. Sensitivity to $(p, \eta)$ is non-amplifying down the tree: in every split, the left child inherits $X$'s slack ($\le p + E\eta$) and the right child inherits only $Y$'s fresh slack ($\le E\eta$). $\square$

- **Exact certified full-instance rungs (`verify_cascade_and_pingpong.py`):**
  - `c = 1.60, D = 2` $\implies$ certified full-instance LB $= \mathbf{1.597999}$
  - `c = 1.65, D = 6` $\implies$ certified full-instance LB $= \mathbf{1.648999}$
  - `c = 1.67, D = 12` $\implies$ certified full-instance LB $= \mathbf{1.669499}$
  - `c = 1.682, D = 26` $\implies$ certified full-instance LB $= \mathbf{1.681499}$ (within $0.0117$ of $1 + \ln 2$)
- **Independent MILP confirmation (`verify_independent_milp.py`):** A 5-row, depth-1 binary-tree split + ping-pong block (`c = 1.578`, off-support allowed) is certified **INFEASIBLE at budget $1.569 > 1 + W(1) \approx 1.567143$**.

### 2.5 Exact Barrier at $1 + \ln 2$

Remarkably, **two** distinct mechanisms meet tangentially at the exact same point $(u, c) = (1/2,\; 1 + \ln 2)$:
1. Binary-tree splitting stalls when $2u - \ln u = c$ ($\min = 1 + \ln 2$ at $u = 1/2$).
2. Ping-pong from a single row $h$ requires $u = c - h < e^{-(c - 1)}$, which at $c = 1 + \ln 2$ is also $u < e^{-\ln 2} = 1/2$!

Moreover, exhaustive beam search over multi-column weighted 2-row splits starting from $(0.70, 0.6931)$ at budget $c = 1.70$ up to depth 7 never beat the 1-column split baseline $\frac{a + b + 1}{2}$, and replacing binary splits by $q$-way Tijdeman splits on $(A, H, 0, \dots, 0)$ yields a strictly lower threshold ($\frac{5/4 + 1 + \ln 3}{2} \approx 1.6743$ for $q = 3$). Breaking $1 + \ln 2$ therefore requires a genuinely new mechanism beyond single-row-height amplification trees.

---

## 3. Problem A: Pinning $m^* \in \{3, 4\}$ (Proving $\kappa_4 \ge 1.079253$ and Compact $m = 5$)

Previously, `chairman-small-rows` proved $\kappa_2 = 1$ while `chairman-counterexample` gave $m = 11$, leaving $3 \le m^* \le 11$. We collapse this interval to **$m^* \in \{3, 4\}$** via two new mechanisms.

### 3.1 Theorem 4 (Compact $m = 5, n = 47$ Counterexample via Permanent Cleaned Helper)

At budget $c = 1$, an **asymmetric** 1-level chain (requiring $\mathrm{dev}_j - p > 1$ on $A$ and only $\mathrm{term}_H > 1$ on $H$, rather than equalizing both to $\tau$) can transfer $p$ up to
$$
\sup_{d_2 \in [1/e, 1]} (-d_2 \ln d_2) \;=\; \frac{1}{e} \;\approx\; 0.36788 \;>\; \frac{1}{3}
$$
in a single block—so **$N = 3$ blocks** suffice to overflow $B$!

Furthermore, because $H$ has weight $1$ on every chain column, if $H$ enters block $b$ congruent to $h_b \pmod 1$ (up to $O(\eta)$), it exits congruent to $h_b + \mathrm{term}_H \pmod 1$ in only two legal values separated by $1$ (near $\delta - 1$ and $\delta$). Appending **one cleanup column** $Z_b$ on $\{R_b, H\}$ with $d_{R_b} = \eta$, $d_H = 1$, and $x_{R_b} = \delta + \gamma$ forbids $Z_b \to H$ from the lower value (pushing it below $-1$), thereby lifting $H$ back to $\ge -\gamma$ on **every** surviving schedule! Thus a single **permanent helper row $H$** serves all 3 blocks: $m = 1\ (B) + 3\ (R_0, R_1, R_2) + 1\ (H) = \mathbf{5}$ rows.

- **Exact rational certificate (`verify_small_rows_m4_m5.py`):** $m = 5$, $n = 47$ ($k = 15$, $r = 116/125$, $x_2 = 23/25$, $p = 17/50$, $x_c = 1/50$, $\eta = 10^{-5}$) proves $\kappa_5 > 1001/1000$.
- **Independent MILP confirmation (`verify_independent_milp.py`):** $5 \times 47$ full instance is **INFEASIBLE at budget $1.0$**.

### 3.2 Theorem 5 (Four Machines: $\kappa_4 \ge c_4^* \approx 1.07925345$)

**Lemma C (Dirty-Helper Ping-Pong).** *At budget $c \ge 1$, suppose row $A$ enters a ping-pong block on $\{A, H\}$ at height $\alpha_0$ (gap $g_0 = c - \alpha_0 \in (0, 1)$), while the helper row $H$ enters at **any** legal height $\Delta_H \ge -c$ (completely polluted, no cleanup!). After Level $1$ ($A \to H$), $A$ sits at $c - 1$ and $H$ rises to $\ge -c - \ln g_0$. Ping-pong on $\{A, H\}$ explodes past $c$ whenever $c - (-c - \ln g_0) < 1$, i.e.:*
$$
g_0 \;<\; e^{1 - 2c}.
$$

**Theorem 5.** *Let $c_4^* \approx 1.07925345$ be the unique root of $3c - 2 = e^{-(c - 1)} + e^{1 - 2c}$. Then $\kappa_4 \ge c_4^* > 1$. Consequently, the minimal number of machines with $\kappa_{m^*} > 1$ satisfies $m^* \in \{3, 4\}$.*

*Proof.* Use only **4 rows** $\{B, R_0, R_1, R_2\}$ and budget $c < c_4^*$:
1. **Initial split $J_0$ on $\{B, R_0\}$:** weights $(1, 1)$, splits $(u,\; 1 - u)$.
   - *Branch 1 ($J_0 \not\to B$):* $\Delta_B = +u$, $R_1 = R_2 = 0$.
   - *Branch 2 ($J_0 \to B$):* $\Delta_B = -(1 - u)$, $\Delta_{R_0} = +(1 - u)$, $R_1 = R_2 = 0$.
2. **Block 1 (Ping-pong on $(B, R_1, R_2)$ with share $p_1$):** Since $R_1, R_2$ are fresh, Block 1 forces $J_1 \mapsto R_1$ in **both** branches whenever $c - (1 - p_1) < e^{-(c - 1)}$, i.e., $p_1 < 1 - c + e^{-(c - 1)}$. Choose $u + p_1 > c$:
   - *Branch 1* immediately hits $\Delta_B = u + p_1 > c$ and dies!
   - *Branch 2* survives with $\Delta_B = u + p_1 - 1 > c - 1$ (**cleaned automatically!**), $\Delta_{R_0} = 1 - u$, and $\Delta_{R_1} \ge -c$ (legal schedule!).
3. **Block 2 (Dirty-helper ping-pong on $(R_0, B, R_1)$ with share $p_2$):** Choose $(1 - u) + p_2 > c$, i.e., $p_2 = c - 1 + u + \delta$. If $J_2$ is denied to $B$, then $B$ starts at $(u + p_1 - 1) + (1 - p_2) = u + p_1 - p_2$, giving gap
   $$
   g_0 = c - (u + p_1 - p_2) \approx c - (c - (c - 1 + u)) = c - 1 + u.
   $$
   By Lemma C, Block 2 forces $J_2 \mapsto B$ (even with $R_1 = -c$!) whenever $c - 1 + u < e^{1 - 2c}$. Then $\Delta_{R_0}$ hits $(1 - u) + p_2 > c$, killing Branch 2 as well!
4. An admissible $u \in (0, 1)$ satisfying both $u > 2c - 1 - e^{-(c-1)}$ and $u < e^{1 - 2c} - (c - 1)$ exists iff $3c - 2 < e^{-(c - 1)} + e^{1 - 2c}$, i.e., $c < c_4^* \approx 1.07925345$. $\square$

- **Exact certified $m = 4$ rungs (`verify_small_rows_m4_m5.py`):**
  - Rung 1: certified $\kappa_4 > \mathbf{1.000000}$ ($n = 219$ cols)
  - Rung 2: certified $\kappa_4 > \mathbf{1.030000}$ ($n = 425$ cols)
  - Rung 3: certified $\kappa_4 > \mathbf{1.060000}$ ($n = 1983$ cols)
  - Rung 4: certified $\kappa_4 > \mathbf{1.072000}$ ($n = 14971$ cols, within $0.0073$ of $c_4^*$)
- **Independent MILP confirmation (`verify_independent_milp.py`):** Full $m = 4, n = 291$ instance (off-support allowed) is **INFEASIBLE at budget $1.0$**.

### 3.3 Exact Status of $m = 3$

With $\kappa_2 = 1$ and $\kappa_4 \ge 1.079253$, the sole remaining machine count for $m^*$ is **$m = 3$**, where we establish:
1. **Tightened bounds:** $1 \le \kappa_3 \le 3$ (lower bound from $\kappa_2 = 1$; upper bound from Theorem 6 below, halving Bárány–Grinberg's $6$).
2. **Proposition 8 (Failure of 3D convex-hull trapping in 3 columns):** Unlike $m = 2$ (where `chairman-small-rows` Theorem 3 maintains $0 \in \mathrm{conv}(R_t)$ via a parallelogram invariant), on $m = 3$ rows $(B, A, H)$ just **3 columns** (Block 1 of `chairman-counterexample`, $\eta = 1/1000$) leave $|R_3| = 4$ surviving states in $[-1, 1]^3$, **every one** of which satisfies $\Delta_B \ge 311/1500 \approx 0.207333 > 0$, so $0 \notin \mathrm{conv}(R_3)$ (certified exactly in [`verify_small_rows_m4_m5.py`](code/verify_small_rows_m4_m5.py)). Hence no direct 3D lifting of the $0 \in \mathrm{conv}(R_t)$ invariant can prove $\kappa_3 = 1$.
3. **Exact near-miss obstruction for 2-block ping-pong on $m = 3$:** Running a 1-level chain on $(B, A, H)$ with starting weight $d_1 \in (0, 1)$, helper overshoot $\gamma = \mathrm{term}_H - 1 \ge 0$, and general cleanup column $Z_1$ ($d_A = w \in [0, 1], x_A = z \in (0, 1)$) gives $p_1 = d_1(-\ln d_1 - \gamma)$ and leaves $A \ge a_{\min} = -1 + d_1 + \gamma e^{-\gamma}$ when $H$ is cleaned to $0$. A second ping-pong block on $(B, H, A)$ can transfer up to $p_2 = e^{a_{\min}}$, yielding total $p_1 + p_2 = 1 - \frac{1}{2}\alpha^2 \epsilon^2 - \frac{1}{3}\epsilon^3 + O(\epsilon^4) < 1$ (for $d_1 = 1 - \epsilon, \gamma = \alpha \epsilon$), approaching $1$ to $0.99999967$ without crossing $1$! Resolving whether $\kappa_3 = 1$ or $\kappa_3 > 1$ remains the sharpest small-row open problem.

---

## 4. Problem B (Upper Bound): Cutting $\kappa_m \le 2m$ in Half to $\kappa_m \le m$, and Obstruction Audit for $\kappa < \infty$

### 4.1 Theorem 6 (Iterated Prefix Basis-Rounding): $\kappa_m \le m$

**Theorem 6.** *For every finite instance $(x, d)$ with $m$ rows, $n$ columns, and maximum weight $D = \max_{i,j} d_{ij} > 0$, there is a polynomial-time, support-preserving ($y_{ij} = 0$ whenever $x_{ij} = 0$) integral assignment $y \in \{0, 1\}^{m \times n}$ satisfying*
$$
|\Delta_i(t)| \;<\; m \cdot D \qquad \text{for every row } i \in \{1, \dots, m\} \text{ and every prefix } t \in \{1, \dots, n\}.
$$
*In particular, $\kappa_m \le m$ for every $m \ge 1$ (halving Bárány–Grinberg's $2m$ bound, and giving $\kappa_3 \le 3$, $\kappa_4 \le 4$).*

*Proof.* Process columns $t = 1, \dots, n$ sequentially. Maintain a subset $F_t \subseteq \{1, \dots, t\}$ of currently fractional columns with vectors $z_j^{(t)} \in \Delta_{m-1}$ ($j \in F_t$), and already-fixed integral assignments $y_j \in \{0, 1\}^m$ for $j \in \{1, \dots, t\} \setminus F_t$, satisfying:
1. $\mathrm{supp}(z_j^{(t)}) \subseteq \mathrm{supp}(x_j)$ and $\mathrm{supp}(y_j) \subseteq \mathrm{supp}(x_j)$,
2. $\sum_{j \in \{1,\dots,t\} \setminus F_t} d_{ij} y_{ij} + \sum_{j \in F_t} d_{ij} z_{ij}^{(t)} = \sum_{j=1}^t d_{ij} x_{ij}$ for all $i = 1, \dots, m$,
3. $\sum_{j \in F_t} (|\mathrm{supp}(z_j^{(t)})| - 1) \le m$ (which implies $|F_t| \le m$, since every fractional column has $|\mathrm{supp}(z_j^{(t)})| \ge 2$).

Initialize $F_0 = \emptyset$. When column $t$ arrives, set $z_t := x_t$ (if $|\mathrm{supp}(x_t)| = 1$, fix $y_t = x_t$ immediately; otherwise add $t$ to $F$). While $\sum_{j \in F} (|\mathrm{supp}(z_j)| - 1) > m$, consider the homogeneous linear system over the strictly positive variables $\{ \delta_{ij} : j \in F,\, z_{ij} > 0 \}$:
$$
\sum_{j \in F : z_{ij} > 0} d_{ij} \delta_{ij} = 0 \quad (i = 1, \dots, m), \qquad
\sum_{i : z_{ij} > 0} \delta_{ij} = 0 \quad (j \in F).
$$
The number of unknowns is $\sum_{j \in F} |\mathrm{supp}(z_j)| > m + |F|$, strictly exceeding the $m + |F|$ equations! Hence there is a nonzero kernel vector $\delta \ne 0$ (computable in exact rational arithmetic by Gaussian elimination). Replacing $\delta$ by $-\delta$ if necessary so some $\delta_{ij} < 0$, set $\lambda := \min \{ -z_{ij}/\delta_{ij} : \delta_{ij} < 0 \} > 0$ and update $z \leftarrow z + \lambda \delta$. This preserves all equations and nonnegativity while driving at least one positive entry to $0$, strictly decreasing $\sum_{j \in F} |\mathrm{supp}(z_j)|$. Whenever a column's support shrinks to size $1$, fix $y_j := z_j$ permanently and remove $j$ from $F$. This terminates in at most $m$ pivots per column with $|F_t| \le m$.

After column $n$, round each remaining column $j \in F_n$ arbitrarily within its support (e.g., $y_{ij} = 1$ at $i = \arg\max z_{ij}^{(n)}$). Because supports only shrink across steps $t' \ge t$, every column $j \in F_t$ satisfies $y_{ij} = 0$ whenever $z_{ij}^{(t)} = 0$, and $z_{ij}^{(t)} \in (0, 1)$ whenever $z_{ij}^{(t)} > 0$. By invariant (2), at every prefix $t$ and every row $i$:
$$
\Delta_i(t) \;=\; \sum_{j=1}^t d_{ij}(x_{ij} - y_{ij}) \;=\; \sum_{j \in F_t} d_{ij}\bigl(z_{ij}^{(t)} - y_{ij}\bigr).
$$
Each term with $z_{ij}^{(t)} > 0$ satisfies $|z_{ij}^{(t)} - y_{ij}| \le \max(z_{ij}^{(t)}, 1 - z_{ij}^{(t)}) < 1$, and terms with $z_{ij}^{(t)} = 0$ vanish. Hence $|\Delta_i(t)| < |F_t| \cdot D \le m \cdot D$ whenever $F_t \ne \emptyset$ (and $0$ if $F_t = \emptyset$). $\square$

Implemented in pure exact `fractions.Fraction` Gaussian elimination in [`verify_upper_bound_km.py`](code/verify_upper_bound_km.py) and verified on 125 random rational instances ($m = 2..6$) plus the $11 \times 15$ `chairman-counterexample` instance (where it finds an exact support-preserving schedule with discrepancy $25/24 < 11$).

### 4.2 Exact Obstruction Audit: Where Candidate Offline Routes to $\kappa < \infty$ or $\kappa_m = o(m)$ Break

Since the online problem is unbounded already for $m = 2$ (`chairman-small-rows` Theorem 2), any proof of $\kappa < \infty$ or $\kappa_m = o(m)$ must be offline. We audited all four candidate offline methods:

1. **Iterated LP Rounding / Beck–Fiala (Theorem 6):** Tight at $|F_t| \le m$. For common weights ($d_{ij} = d_j$), the row-sum constraint $\sum_{i=1}^m \Delta_i(t) = 0$ is redundant, giving $|F_t| \le m - 1$. Under machine-dependent weights, all $m$ row equations can be linearly independent (even on support-2 columns: parallel edges on $\{i, k\}$ with distinct weight ratios $d_{ij}/d_{kj}$ are linearly independent), so basis-size counting alone cannot beat $O(m)$.
2. **Bárány–Grinberg / Steinitz / Banaszczyk / Nikolov:**
   - Bárány–Grinberg (1981) gives $2m$ for any norm in $\mathbb{R}^m$; Theorem 6 improves this to $m$ in $\ell_\infty^m$ by exploiting the simplex structure $z_{ij} - y_{ij} \in (-1, 1)$ instead of the triangle-inequality diameter $2$.
   - Banaszczyk (2012) on signed series (and Bansal–Rohwedder–Svensson 2022 for prefix discrepancy) yields $O(\sqrt{\log n})$—still growing with $n$, not constant—and applies directly to symmetric $\pm v_j$ colorings with $\|v_j\|_2 \le 1$. Although our column shifts satisfy $\|v_j\|_1 \le 2 \implies \|v_j\|_2 \le \sqrt{2}$, passing from symmetric $\pm 1$ discrepancy to general fractional $x_{ij} \in [0, 1]$ via Lovász–Spencer–Vesztergombi requires *hereditary* prefix discrepancy (which adds a factor of 2, still $O(\sqrt{\log n})$ rather than $O(1)$ or $o(m)$ uniformly in $n$).
   - The September 2026 proofs of the Komlós and Beck–Fiala conjectures control the *final* sum $t = n$ only, not all prefixes $t = 1, \dots, n$; prefix Komlós remains open.
3. **Liu–Reis Earliest-Deadline / Tree-of-Intervals:** Relies critically on column-wise mass conservation $\sum_{i=1}^m d_j(x_{ij} - y_{ij}) = 0$, which lets the scheduler pair surplus on one machine with matching deficit on another via a balanced interval tree. Our Theorems 1–3 directly exploit the failure of conservation ($d_{A,j} \ne d_{H,j}$): every level converts a small active drain into a logarithmically amplified passive gain, pushing $\kappa$ past $1.693$.
4. **Multi-Row Trapping Families generalizing $m = 2$:** Proposition 8 shows $0 \notin \mathrm{conv}(R_3)$ already in 3 columns on 3 rows, ruling out any direct 3D generalization of the $m = 2$ origin-enclosing parallelogram invariant.

**Conclusion on Conjecture 1 ($\kappa < \infty$):** Conjecture 1 remains **open**, now squeezed from below to $\kappa \ge 1 + \ln 2 \approx 1.693147$ (with $\kappa_m \le m$ from above). Whether $\kappa$ is finite (perhaps $2$ or $O(1)$) or $\kappa = \infty$ (via a mechanism that amplifies discrepancy across *multiple* rows simultaneously without single-column venting) is the central open question of the programme.

---

## 5. Open Problem 3 of `detector-chains`: Complete Analytic Resolution

**Theorem 7 (Exact Split Optimality & Admissibility Separation).** *Fix $k \ge 3$ and any nondecreasing weights $0 < d_2 \le d_3 \le \dots \le d_{k-1} \le d_k = 1$. Let $R = \sum_{j=2}^{k-1} \frac{d_j}{d_{j+1}}$ and $\tau_{\mathrm{bal}}(d) = \frac{d_2(k - 1 - R) + 1}{1 + d_2}$. For the $p = 0$ heights $\mathrm{dev}_j(x) = 1 - \sum_{i=2}^{j-1} d_i(1 - x_i) + d_j x_j$ ($2 \le j \le k$, with $\mathrm{dev}_k = \mathrm{term}_A$) and $\mathrm{term}_H(x) = \sum_{i=2}^k (1 - x_i)$,*
$$
\max_{x \in [0, 1]^{k-1}} \min\bigl\{\mathrm{dev}_2(x), \dots, \mathrm{dev}_{k-1}(x),\, \mathrm{term}_A(x),\, \mathrm{term}_H(x)\bigr\}
\;=\; \min\bigl\{\tau_{\mathrm{bal}}(d),\; 1 + d_2\bigr\}.
$$

*Proof.* Observe that $\mathrm{dev}_j(x) = \bigl(1 - \sum_{i=2}^{j-1} d_i\bigr) + \sum_{i=2}^j d_i x_i$ has $+d_i x_i$ for every $j \ge i$. Define nonnegative dual weights
$$
\alpha_j := \frac{1}{d_j} - \frac{1}{d_{j+1}} \ge 0 \quad (2 \le j \le k - 1), \qquad \alpha_k := 1, \qquad \beta := 1.
$$
Then $\sum_{j=i}^k \alpha_j = \frac{1}{d_i}$ for every $i = 2, \dots, k$, so the coefficient of $x_i$ in $\sum_{j=2}^k \alpha_j \mathrm{dev}_j(x) + \beta\,\mathrm{term}_H(x)$ is $d_i \cdot \frac{1}{d_i} - 1 = 0$ identically! Evaluating the remaining constant terms gives the exact identity for all $x \in \mathbb{R}^{k-1}$:
$$
\sum_{j=2}^{k-1} \left(\frac{1}{d_j} - \frac{1}{d_{j+1}}\right) \mathrm{dev}_j(x) + \mathrm{term}_A(x) + \mathrm{term}_H(x)
\;\equiv\; \frac{1}{d_2} + (k - 1) - \sum_{i=2}^{k-1} d_i \cdot \frac{1}{d_{i+1}}
\;=\; \frac{1}{d_2} + k - 1 - R.
$$
Dividing by the sum of nonnegative weights $\sum_{j=2}^k \alpha_j + \beta = \frac{1}{d_2} + 1 = \frac{1 + d_2}{d_2}$ yields $\min\{\mathrm{dev}_2, \dots, \mathrm{term}_A, \mathrm{term}_H\} \le \tau_{\mathrm{bal}}(d)$. On $[0, 1]^{k-1}$ we also have $\min \le \mathrm{dev}_2(x) = 1 + d_2 x_2 \le 1 + d_2$.

For matching primal attainment in $[0, 1]^{k-1}$, set $x_{j+1} = d_j/d_{j+1} \in (0, 1]$ ($2 \le j \le k - 1$). Since $d_j \le d_{j+1}$, $R \le k - 2$, hence $\tau_{\mathrm{bal}}(d) \ge 1$.
- **Admissible case ($\tau_{\mathrm{bal}}(d) \le 1 + d_2$):** $x_2 = (\tau_{\mathrm{bal}}(d) - 1)/d_2 \in [0, 1]$ makes all $k$ heights equal to $\tau_{\mathrm{bal}}(d)$.
- **Inadmissible case ($\tau_{\mathrm{bal}}(d) > 1 + d_2$):** $x_2 = 1$ makes every $A$-side height equal to $1 + d_2$, while $\mathrm{term}_H = (k - 2) - R > 1 + d_2$ (equivalent to $1 + d_2(k - 1 - R) > (1 + d_2)^2$, i.e., $\tau_{\mathrm{bal}}(d) > 1 + d_2$). $\square$

Verified symbolically and on 3,007 rational weight vectors in [`verify_split_optimality_proof.py`](code/verify_split_optimality_proof.py).

---

## 6. Problem C: Concise Roadmap of Classical & Adjacent Conjectures

| Statement / Conjecture | Exact Status | Notes for the Programme |
|---|---|---|
| **Tijdeman (1973) / Meijer (1973)** — Unweighted chairman assignment | **Proved theorem** (not open) | Exact optimal constant is $1 - \frac{1}{2m - 2}$ (hence supremum $1$ over all $m$). Cannot be counterexampled. |
| **Liu–Reis (ITCS 2026 / arXiv:2511.18546)** — Common-weight weighted chairman ($d_{ij} = d_j$) | **Proved theorem** (not open) | Every instance admits an integral assignment with $|\Delta_i(t)| \le \max_j d_j$ ($\kappa(1) = 1$). Cannot be counterexampled. |
| **Liu–Reis Conjecture 19 (arXiv Conj. 3) & Conjecture 21 (arXiv Conj. 5)** — Machine-dependent weighted chairman ($d_{ij} > 0$) | **Refuted** (`chairman-counterexample`, `detector-chains`, and this work) | Refuted for $m \ge 4$ ($\kappa_4 \ge 1.079253$); globally $\kappa \ge 1 + \ln 2 \approx 1.693147$; holds for $m = 2$ ($\kappa_2 = 1$, `chairman-small-rows`). |
| **Morell–Skutella (2022)** — Costless two-sided unsplittable flow ($|f(e) - x(e)| \le d_{\max}$ on general single-source/sink or multi-commodity networks) | **Still OPEN** | Liu–Reis's common-weight theorem resolves the special case of parallel/series-chain prefix networks (weighted carpooling). Machine-dependent chairman counterexamples do **not** refute Morell–Skutella because Morell–Skutella has commodity-specific (not edge-by-commodity-dependent) demands! |
| **Finiteness of $\kappa$ (`detector-chains` Conjecture 1)** | **Still OPEN** | Now bounded by $1 + \ln 2 \le \kappa \le \infty$, with $\kappa_m \le m$ for every fixed $m$. |
| **Minimal machine count $m^*$ with $\kappa_{m^*} > 1$** | **Open in $\{3, 4\}$ only** | $m^* = 3$ iff $\kappa_3 > 1$; otherwise $m^* = 4$ (with $1 \le \kappa_3 \le 3$ and $\kappa_4 \ge 1.079253$). |
| **Prefix Komlós / Beck–Fiala (all prefixes, $\ell_1$-bounded columns)** | **Still OPEN** | Final-sum Komlós and Beck–Fiala were proved in Sept. 2026; the prefix version (even for sparsity 2) remains open. |
