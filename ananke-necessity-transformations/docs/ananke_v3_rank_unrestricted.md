# ANANKE v3: Rank-Unrestricted Approximate Counterfeit Complexity via B-Spline Cayley–Hamilton Obstructions

This document presents the mathematical theory, machine-certified algorithms, and
two-sided upper-versus-lower complexity analysis of **ANANKE v3**. It directly closes
the single remaining epistemic caveat identified in the **Epistemic Scope Box** of
ANANKE v2 (`docs/ananke_v2_certified_core.md`, §2.3):

> ANANKE v2's finite-sample Karpelevič exclusion (Theorem 3) is conditional on the
> exact minimal-rank assumption $\operatorname{rank}(H_f) = \operatorname{rank}(H) = r$.
> Because finite-shot observations on a finite Hankel block can never prove
> $\operatorname{rank}(H_f) \le r$, v2 left open whether a higher-rank *approximate*
> classical stochastic counterfeit $g_N$ ($\operatorname{rank}(H_{g_N}) > r$ with tiny
> tail singular values) could imitate the qubit with fewer than $N_{\mathrm{cl}}$ states.

ANANKE v3 eliminates the rank upper-bound assumption **completely** via an exact
operator-algebraic identity combining the Cayley–Hamilton theorem, $N$-fold discrete
B-spline windows, and the Subharmonic Maximum Principle over the Karpelevič region
$\Theta_N$, while simultaneously constructing explicit classical counterfeits (acyclic
shift registers, Ito/Karpelevič boundary chains, numerical arbitrary-rank HMMs, and
two-symbol Bloch polytopes) to honestly bracket the true approximate counterfeit
complexity $C_{\mathrm{classical}}(f; \varepsilon, \mathcal{W})$ from **both sides**.

Every claim below carries an explicit epistemic label:
- **PROVED**: complete analytic proof or exact algebraic identity;
- **CERTIFIED**: machine-checked via outward-rounded arbitrary-precision `Decimal`
  interval arithmetic (`src/ananke/interval.py`, `src/ananke/rank_unrestricted.py`);
- **NUMERICAL**: empirical optimization, Monte Carlo calibration, or NMF probing;
- **CONJECTURAL / OPEN**: unproved target for future work.

---

## 1. The Finite-Horizon Counterfeit Loophole (PROVED)

Before proving rank-unrestricted lower bounds, we make the exact mechanism of v2's
rank-cap caveat explicit.

**Proposition 1.1 (Acyclic Shift-Register Upper Bound on Unary Rays, PROVED).**
Let $f: \Sigma^* \to [0, 1]$ be *any* behavioural process, fix a symbol $a \in \Sigma$,
and consider the length-$L$ unary word family $\mathcal{W}_L^{\mathrm{unary}} = \{a^0, a^1, \dots, a^L\}$.
Then there exists an exact $(L + 1)$-state classical stochastic realization $g_{L+1}$
with $p = e_0$, deterministic shift matrix $M_a(i, i+1) = 1$ ($0 \le i < L$),
$M_a(L, L) = 1$, and response vector $e_k = f(a^k) \in [0, 1]$ such that:
1. $g_{L+1}(a^k) = f(a^k)$ **identically** ($\varepsilon = 0$) for all $0 \le k \le L$;
2. $\operatorname{spec}(M_a) = \{1, 0, \dots, 0\} \subset \Theta_1 \subset \Theta_{L+1}$
   (completely devoid of any peripheral complex mode $e^{i\theta}$);
3. Consequently, for every process $f$:
   $$C_{\mathrm{classical}}\!\left(f;\; 0,\; \mathcal{W}_L^{\mathrm{unary}}\right) \;\le\; L + 1.$$

*Consequence for ANANKE v2's $L = 7$ horizon:* On unary words of length $\le 7$, an
$8$-state rank-$8$ shift register matches the $4 \times 4$ unary Hankel block $H_f$
and shifted block $H_{f,x}$ with **zero error** even at infinite shots. Thus, **no**
rank-unrestricted unary obstruction at $L = 7$ can ever exceed $N \ge 8$; climbing to
larger rank-unrestricted classical-state lower bounds *provably requires* either longer
word horizons $L > N$ or multi-symbol noncommuting constraints.

---

## 2. The B-Spline Cayley–Hamilton Spectral Obstruction (PROVED)

Let $g(w) = p M_w e$ be **any** $N$-state classical stochastic realization
($p \in \Delta_N$, $M_a \in \mathcal{S}_N$, $e \in [0, 1]^N$) of **arbitrary Hankel
rank $\le N$** and **arbitrary Jordan block structure** (no diagonalizability, no
eigenvector conditioning bound, and no rank cap). Fix a symbol $a \in \Sigma$,
prefix $u$, suffix $v$, and unary ray $w_k := u a^k v$ ($k \ge 0$), so
$$g(w_k) = \mu^T M_a^k \nu, \qquad \mu := (p M_u)^T \in \Delta_N, \qquad \nu := M_v e \in [0, 1]^N.$$

For any boxcar length $M \ge 1$, let $w^{(1)}_t := \frac{1}{M}\mathbf{1}_{0 \le t \le M-1}$
be the uniform boxcar on $\mathbb{Z}$, and define the **$N$-fold discrete B-spline window**
$$w^{(N)} := \underbrace{w^{(1)} * w^{(1)} * \cdots * w^{(1)}}_{N \text{ times}},$$
which is nonnegative, sums to $1$, is supported on $\{0, 1, \dots, N(M - 1)\}$, and has
discrete Fourier transform $W^{(N)}(\phi) = \left(\frac{1}{M}\sum_{r=0}^{M-1} e^{-ir\phi}\right)^N$,
satisfying $|W^{(N)}(2\theta)| = \left|\frac{\sin(M\theta)}{M\sin\theta}\right|^N$.

**Lemma 2.1 (Exact B-Spline Difference-Norm Bound, PROVED).**
Let $(S u)_k := u_{k-1}$ be the unit backward shift and $\nabla := I - S$ the backward
difference on $\ell^1(\mathbb{Z})$. Then for every $0 \le m \le N$:
$$\bigl\|\nabla^m w^{(N)}\bigr\|_1 \;\le\; \left(\frac{2}{M}\right)^m.$$

*Proof.* Since $(\nabla w^{(1)})_k = \frac{1}{M}(\delta_{k,0} - \delta_{k,M})$, we have
$\|\nabla w^{(1)}\|_1 = 2/M$ and $\|w^{(1)}\|_1 = 1$. Because $\nabla$ commutes with
discrete convolution, $\nabla^m w^{(N)} = (\nabla w^{(1)})^{*m} * (w^{(1)})^{*(N-m)}$.
Applying Young's convolution inequality $\|u * v\|_1 \le \|u\|_1 \|v\|_1$ yields
$\|\nabla^m w^{(N)}\|_1 \le (2/M)^m \cdot 1^{N-m} = (2/M)^m$. $\square$

**Theorem 1 (Rank-Unrestricted B-Spline Cayley–Hamilton Obstruction, PROVED).**
Let $N \ge 2$, $M \ge 1$, and $\theta \in (0, 2\pi)$ with $e^{i\theta} \notin \Theta_N$.
Define the universal spectral-product constant
$$\Psi_N(M, \theta) \;:=\; \sup_{A \in \mathcal{S}_N} \prod_{j=1}^N \left(1 + \frac{2}{M \bigl|e^{i\theta} - \lambda_j(A)\bigr|}\right) \;<\; \infty.$$
Then for **every** $N$-state classical stochastic realization $g \in \mathcal{O}_N^{\mathrm{cl}}$
(arbitrary rank $\le N$, arbitrary Jordan structure) and every unary ray $w_k = u a^k v$:
1. **(Mode A — Unconditional Fourier-Amplitude Cap, horizon $L = N(M - 1)$):**
   $$\Biggl|\sum_{k=0}^{N(M-1)} w^{(N)}_k e^{-ik\theta} \bigl(g(w_k) - \tfrac{1}{2}\bigr)\Biggr| \;\le\; \frac{1}{2}\Bigl(\Psi_N(M, \theta) - 1\Bigr).$$
2. **(Mode B — Reference-Sinusoid Residual Bound, horizon $L = N M$):**
   For *any* fixed reference sinusoid $s(k) = c_0 + A\cos(k\theta + \phi)$ with $A > 0$,
   write $\Delta_k := g(w_k) - s(k)$. Then
   $$\frac{A}{2}\bigl(1 - |W^{(N)}(2\theta)|\bigr) \;\le\; \Biggl|\sum_{k=0}^{N(M-1)} w^{(N)}_k e^{-ik\theta} \Delta_k\Biggr| + \bigl(\Psi_N(M, \theta) - 1\bigr) \max_{0 \le k \le NM} |\Delta_k| \;\le\; \Psi_N(M, \theta) \max_{0 \le k \le NM} |\Delta_k|.$$
   In particular, for an exact sinusoidal ray $f(w_k) = c_0 + A\cos(k\theta + \phi)$,
   $$\inf_{g \in \mathcal{O}_N^{\mathrm{cl}}} \max_{0 \le k \le NM} \bigl|f(w_k) - g(w_k)\bigr| \;\ge\; \frac{A\bigl(1 - |W^{(N)}(2\theta)|\bigr)}{2\,\Psi_N(M, \theta)}.$$

*Proof.* Let $\chi(z) = \det(z I - M_a) = \prod_{j=1}^N (z - \lambda_j) = \sum_{j=0}^N c_j z^j$.
Because $M_a \in \mathcal{S}_N$ is stochastic, $\lambda_1 = 1$ so $\chi(1) = \sum_{j=0}^N c_j = 0$,
and by Cayley–Hamilton $\chi(M_a) = 0$. Therefore, for every $t \ge 0$,
$$\sum_{j=0}^N c_j \bigl(g(w_{t+j}) - \tfrac{1}{2}\bigr) = \mu^T M_a^t \chi(M_a) \nu - \tfrac{1}{2}\chi(1) = 0.$$
Weighting by $w^{(N)}_t e^{-it\theta}$ and summing over $t = 0, \dots, N(M-1)$, then
re-indexing by $k = t + j \in \{0, \dots, N M\}$, yields for *any* sequence $h_k$:
$$\sum_{t=0}^{N(M-1)} w^{(N)}_t e^{-it\theta} \sum_{j=0}^N c_j h_{t+j} = \sum_{k=0}^{NM} a_k e^{-ik\theta} h_k, \qquad a_k := \sum_{j=0}^N c_j e^{ij\theta} w^{(N)}_{k-j} = \bigl(\chi(e^{i\theta} S) w^{(N)}\bigr)_k.$$
Because $\chi$ is a degree-$N$ polynomial and $S = I - \nabla$, finite Taylor expansion
around $e^{i\theta}$ is **exact**:
$$a = \chi\bigl(e^{i\theta}(I - \nabla)\bigr) w^{(N)} = \chi(e^{i\theta}) w^{(N)} + \sum_{m=1}^N \frac{(-e^{i\theta})^m \chi^{(m)}(e^{i\theta})}{m!}\,\nabla^m w^{(N)}.$$
By Leibniz's rule, $\frac{\chi^{(m)}(z)}{m!\,\chi(z)} = \sum_{1 \le j_1 < \dots < j_m \le N} \prod_{r=1}^m (z - \lambda_{j_r})^{-1}$.
Dividing by $\chi(e^{i\theta}) \neq 0$ (since $e^{i\theta} \notin \Theta_N$) and applying
Lemma 2.1 yields the **exact operator remainder bound**:
$$\frac{\bigl\|a - \chi(e^{i\theta}) w^{(N)}\bigr\|_1}{|\chi(e^{i\theta})|} \;\le\; \sum_{m=1}^N \left(\frac{2}{M}\right)^m e_m\!\left(\frac{1}{|e^{i\theta} - \lambda_1|}, \dots, \frac{1}{|e^{i\theta} - \lambda_N|}\right) = \prod_{j=1}^N \left(1 + \frac{2}{M |e^{i\theta} - \lambda_j|}\right) - 1 \;\le\; \Psi_N(M, \theta) - 1.$$

- For **(1)**, take $h_k = g(w_k) - \frac{1}{2}$ (which obeys $|h_k| \le \frac{1}{2}$ for *all*
  $k \ge 0$, including $k > N(M - 1)$ without measuring them!). Since the LHS vanishes,
  $\bigl|\sum_{k=0}^{N(M-1)} w^{(N)}_k e^{-ik\theta} h_k\bigr| \le \frac{1}{2} \frac{\|a - \chi w^{(N)}\|_1}{|\chi|} \le \frac{1}{2}(\Psi_N(M, \theta) - 1)$.
- For **(2)**, take $h_k = s(k) = c_0 + \frac{A}{2} e^{i\phi} e^{ik\theta} + \frac{A}{2} e^{-i\phi} e^{-ik\theta}$.
  Since $\chi(1) = 0$ and $\chi$ has real coefficients ($|\chi(e^{-i\theta})| = |\chi(e^{i\theta})|$),
  the LHS equals $\frac{A}{2} e^{i\phi} \chi(e^{i\theta}) + \frac{A}{2} e^{-i\phi} \chi(e^{-i\theta}) W^{(N)}(2\theta)$,
  whose modulus after dividing by $|\chi(e^{i\theta})|$ is at least $\frac{A}{2}(1 - |W^{(N)}(2\theta)|)$.
  On the other hand, since $g$ is annihilated, $h_k = s(k) - g(w_k) = -\Delta_k$ gives
  the exact same sum, and splitting $a/\chi = w^{(N)} + (a/\chi - w^{(N)})$ gives (2). $\square$

> **Why Theorem 1 avoids exponential $2^N / |\chi|$ blowup:**
> Naively applying Cayley–Hamilton to a rectangular Hankel block with a boxcar window
> ($d = 1$) leaves $O(2^N / (K |\chi(e^{i\theta})|))$ boundary error. Convolving to the
> $N$-fold B-spline $w^{(N)}$ converts all $N$ finite differences into the exact elementary
> symmetric product $\prod_{j=1}^N (1 + 2/(M |e^{i\theta} - \lambda_j|)) \le \exp(2 \Lambda_N(\theta)/M)$,
> eliminating $|\chi(e^{i\theta})|^{-1}$ and $2^N$ entirely.

---

## 3. Subharmonic Dual Spectral-Measure Certification of $\Psi_N(M, \theta)$ (PROVED & CERTIFIED)

Evaluating $\Psi_N(M, \theta)$ by naively plugging in $d_N(\theta) := \operatorname{dist}(e^{i\theta}, \Theta_N)$
for all $N - 1$ nontrivial eigenvalues is overly pessimistic because **nonnegative matrices
cannot concentrate all eigenvalues near $e^{i\theta}$**: their power traces satisfy
$\operatorname{tr}(A^k) = \sum_{j=1}^N \lambda_j^k \ge 0$ for every $k \ge 1$, and complex
eigenvalues occur in conjugate pairs.

**Theorem 2 (Subharmonic Dual Spectral-Measure Bound, PROVED & CERTIFIED).**
Fix $N \ge 2$, $M \ge 1$, $\theta \in (0, \pi)$ with $z = e^{i\theta} \notin \Theta_N$,
and *any* nonnegative trace multipliers $y_1, \dots, y_K \ge 0$. Define
$$\psi_{M, y}(\lambda) \;:=\; \frac{1}{2}\ln\!\left(1 + \frac{2}{M |z - \lambda|}\right) + \frac{1}{2}\ln\!\left(1 + \frac{2}{M |z - \bar{\lambda}|}\right) + \sum_{k=1}^K y_k \operatorname{Re}(\lambda^k).$$
1. **Strict Subharmonicity (PROVED):** For every $\lambda \in \mathbb{C} \setminus \{z, \bar{z}\}$,
   $$\Delta \psi_{M, y}(\lambda) = \frac{1}{2}\cdot\frac{2/M}{|z - \lambda|(|z - \lambda| + 2/M)^2} + \frac{1}{2}\cdot\frac{2/M}{|z - \bar{\lambda}|(|z - \bar{\lambda}| + 2/M)^2} \;>\; 0.$$
   By the Subharmonic Maximum Principle and conjugation symmetry of $\Theta_N$,
   $$\sup_{\lambda \in \Theta_N} \psi_{M, y}(\lambda) = \max\!\left(\sup_{\alpha \in [0, \pi]} \psi_{M, y}\bigl(\rho_N(\alpha) e^{i\alpha}\bigr),\; \sup_{x \in [-1, 1]} \psi_{M, y}(x)\right).$$
2. **Universal Dual Upper Bound (PROVED):** For every $U \ge \sup_{\lambda \in \partial\Theta_N^+ \cup [-1,1]} \psi_{M, y}(\lambda)$
   and every $A \in \mathcal{S}_N$,
   $$\prod_{j=1}^N \left(1 + \frac{2}{M |z - \lambda_j(A)|}\right) \;\le\; \left(1 + \frac{2}{M |z - 1|}\right)\exp\!\left(\sum_{k=1}^K y_k + (N - 1) U\right).$$

*Proof.* (1) With $\rho = |\lambda - z| > 0$ and $c = 2/M > 0$,
$\Delta \ln(1 + c/\rho) = \frac{1}{\rho}\frac{d}{d\rho}\!\left(\rho\bigl(\frac{1}{\rho+c} - \frac{1}{\rho}\bigr)\right) = \frac{c}{\rho(\rho+c)^2} > 0$,
while $\operatorname{Re}(\lambda^k)$ is harmonic ($\Delta = 0$). Since $\Theta_N$ is compact,
conjugation-symmetric, and its boundary in the upper half-plane is contained in
$\{\rho_N(\alpha)e^{i\alpha} : \alpha \in [0, \pi]\} \cup [-1, 1]$ (including the real boundary
slit $[-1, -1/2]$ of $\Theta_3$ and $\Theta_2 = [-1, 1]$), the Subharmonic Maximum Principle
reduces the 2D supremum to a 1D boundary supremum.
(2) For any $A \in \mathcal{S}_N$, $\lambda_1 = 1$, $\lambda_2, \dots, \lambda_N \in \Theta_N$
are conjugation-symmetric, and $\operatorname{tr}(A^k) = 1 + \sum_{j=2}^N \operatorname{Re}(\lambda_j^k) \ge 0$.
Adding $\sum_{k=1}^K y_k \operatorname{tr}(A^k) \ge 0$ to $\sum_{j=2}^N \ln(1 + c/|z - \lambda_j|)$
yields $\sum_{j=2}^N \psi_{M,y}(\lambda_j) + \sum_{k=1}^K y_k \le (N - 1) U + \sum_{k=1}^K y_k$.
Exponentiating and multiplying by $(1 + c/|z - 1|)$ gives (2). $\square$

**Machine Certification (`src/ananke/rank_unrestricted.py`, `src/ananke/interval.py`):**
A heuristic linear program first proposes sparse multipliers $y_1, \dots, y_K \ge 0$;
rigor does **not** depend on the LP. We extend ANANKE v2's outward-rounded `Decimal`
interval library with certified `ln2_interval`, `log_interval`, and `exp_interval`, and
run 1D best-first interval branch-and-bound over every Farey arc of $\mathcal{F}_N$ in
$[0, 1/2]$ (using v2's certified gap enclosures $[\rho_{\mathrm{lo}}, \rho_{\mathrm{hi}}]$)
plus $[-1, 1]$. This returns a **CERTIFIED** global upper bound $\Psi_{N,\mathrm{cert}}(M, \theta) \ge \Psi_N(M, \theta)$
typically within $0.4\%$–$1.5\%$ of the LP optimum in $< 1\,\text{s}$ per order.

---

## 4. Non-Asymptotic Finite-Shot Rank-Unrestricted Certificates (PROVED)

Given independent binomial word counts $S_{w_k} \sim \operatorname{Binomial}(M_{w_k}, f(w_k))$
on the unary ray $w_k = u a^k v$ ($k = 0, \dots, L_{\max}$), with **no assumption whatsoever
on $\operatorname{rank}(H_f)$**:

**Theorem 3 (Finite-Shot Rank-Unrestricted Certificates, PROVED).**
Fix failure probability $\alpha \in (0, 1)$ and a finite list of candidate state counts
$\mathcal{N} = \{2, \dots, N_{\max}\}$.

1. **Mode A — Single-Sample Unconditional Fourier-Cap Certificate (`certify_rank_unrestricted_fourier_cap`):**
   For each $N \in \mathcal{N}$ with $M = \lfloor L_{\max} / N \rfloor + 1 \ge 2$, compute
   $\hat{F}_N := \left|\sum_{k=0}^{N(M-1)} w^{(N)}_k e^{-ik\theta}(\hat{f}(w_k) - \frac{1}{2})\right|$
   and the complex scalar Hoeffding radius (with $\delta_N = \alpha / |\mathcal{N}|$)
   $$\varepsilon_{\mathrm{lin}, N} := \sqrt{\frac{1}{2}\left(\sum_{k=0}^{N(M-1)} \frac{(w^{(N)}_k)^2}{M_{w_k}}\right)\ln\frac{4}{\delta_N}}.$$
   Then with simultaneous probability $\ge 1 - \alpha$ over all $N \in \mathcal{N}$, every
   $N$-state classical stochastic model $g \in \mathcal{O}_N^{\mathrm{cl}}$ (arbitrary rank $\le N$) obeys
   $$\max_{0 \le k \le N(M-1)} |f(w_k) - g(w_k)| \;\ge\; \hat{F}_N - \varepsilon_{\mathrm{lin}, N} - \frac{1}{2}\bigl(\Psi_{N,\mathrm{cert}}(M, \theta) - 1\bigr).$$
   *Operational advantage:* Zero word-wise union bound and zero pilot split; requires only
   $O(10^2)$ shots per word (tens to hundreds of thousands of *total* shots across the entire ray!).

2. **Mode B — Two-Stage Hypergeometric Split-Sample Certificate (`certify_rank_unrestricted_split_sample`):**
   Split the counts into strictly independent pilot (`ds1`) and main (`ds2`) datasets via
   exact Hypergeometric thinning (`split_shot_dataset`). Fit a deterministic reference
   sinusoid $s(k) = \hat{c}_0 + \hat{A}\cos(k\theta + \hat{\phi})$ on `ds1`. On `ds2`, let
   $r_k := \hat{f}^{(2)}(w_k) - s(k)$, compute simultaneous Chernoff–KL half-widths
   $\varepsilon_{\mathrm{KL}, k}$ across all $L_{\max}+1$ words (total level $\alpha/2$),
   and for each $N \in \mathcal{N}$ ($M = \lfloor L_{\max}/N \rfloor \ge 2$) compute
   $\hat{R}_{\mathrm{lin}, N} = \left|\sum_{k=0}^{N(M-1)} w^{(N)}_k e^{-ik\theta} r_k\right|$
   and scalar Hoeffding radius $\varepsilon_{\mathrm{lin}, N}$ (level $\alpha / (2|\mathcal{N}|)$).
   Then with simultaneous unconditional probability $\ge 1 - \alpha$, every $g \in \mathcal{O}_N^{\mathrm{cl}}$ obeys
   $$\max_{0 \le k \le NM} |f(w_k) - g(w_k)| \;\ge\; \frac{\frac{\hat{A}}{2}(1 - |W^{(N)}(2\theta)|) - \hat{R}_{\mathrm{lin}, N} - \varepsilon_{\mathrm{lin}, N} - (\Psi_{N,\mathrm{cert}}(M, \theta) - 1)\max_{k \le NM}(|r_k| + \varepsilon_{\mathrm{KL}, k})}{\Psi_{N,\mathrm{cert}}(M, \theta)}.$$
   *Operational advantage:* Works at dramatically shorter circuit depths $L = N M$
   (e.g. $L = 20$–$320$ unary steps), certifying $C_{\mathrm{classical}} \ge 5, \dots, 10$
   strictly beyond the qubit's minimal rank $4$ with zero rank upper bound.

---

## 5. Experimental Results: Lower Bounds vs. Explicit Classical Counterfeits

All numbers below are produced directly by `experiments/certify_rank_unrestricted_v3.py`
(`results/certify_rank_unrestricted_v3.json`) and `experiments/counterfeit_upper_vs_lower_v3.py`
(`results/counterfeit_upper_vs_lower_v3.json`).

### 5.1 Certified Noiseless Rank-Unrestricted Lower Bounds on $C_{\mathrm{classical}}(f; \varepsilon, \{x^k : k \le L\})$ (CERTIFIED)

Every entry below is a **machine-certified, rank-unrestricted** lower bound on the number
of classical hidden states required to approximate the qubit unary ray $\{x^k : 0 \le k \le L\}$
within $\varepsilon$ in $\ell_\infty$ norm, across **all** classical realizations of arbitrary
rank $\le N$ and arbitrary Jordan structure:

| Process | Horizon $L$ | $\varepsilon = 0$ | $\varepsilon = 10^{-3}$ | $\varepsilon = 5 \times 10^{-3}$ | $\varepsilon = 10^{-2}$ |
|---|---:|---:|---:|---:|---:|
| Baseline mixed ($\theta_x = 0.73$, $A = 0.359$) | 12 | $\ge 7$ | $\ge 5$ | $\ge 5$ | $\ge 4$ |
| Baseline mixed ($\theta_x = 0.73$, $A = 0.359$) | 24 | $\ge 13$ | $\ge 7$ | $\ge 5$ | $\ge 5$ |
| Baseline mixed ($\theta_x = 0.73$, $A = 0.359$) | 48 | $\ge 15$ | $\ge 7$ | $\ge 7$ | $\ge 6$ |
| Baseline mixed ($\theta_x = 0.73$, $A = 0.359$) | 96 | $\ge 15$ | $\ge 8$ | $\ge 8$ | $\ge 7$ |
| Baseline mixed ($\theta_x = 0.73$, $A = 0.359$) | 200 | $\ge 15$ | $\ge 9$ | $\ge 8$ | $\ge 8$ |
| Baseline mixed ($\theta_x = 0.73$, $A = 0.359$) | 400 | $\ge 15$ | $\ge 10$ | $\ge 9$ | $\ge 9$ |
| Baseline mixed ($\theta_x = 0.73$, $A = 0.359$) | 800 | $\ge 15$ | $\ge 12$ | $\ge 10$ | $\ge 9$ |
| Baseline mixed ($\theta_x = 0.73$, $A = 0.359$) | 1,600 | $\ge 15$ | $\ge 15$ | $\ge 13$ | $\ge 11$ |
| Golden mixed ($\theta_x = 2.40$, $A = 0.359$) | 12 | $\ge 7$ | $\ge 5$ | $\ge 5$ | $\ge 5$ |
| Golden mixed ($\theta_x = 2.40$, $A = 0.359$) | 48 | $\ge 15$ | $\ge 8$ | $\ge 6$ | $\ge 6$ |
| Golden mixed ($\theta_x = 2.40$, $A = 0.359$) | 200 | $\ge 15$ | $\ge 10$ | $\ge 8$ | $\ge 8$ |
| Golden mixed ($\theta_x = 2.40$, $A = 0.359$) | 400 | $\ge 15$ | $\ge 11$ | $\ge 10$ | $\ge 8$ |
| Golden mixed ($\theta_x = 2.40$, $A = 0.359$) | 800 | $\ge 15$ | $\ge 13$ | $\ge 11$ | $\ge 10$ |
| Golden mixed ($\theta_x = 2.40$, $A = 0.359$) | 1,600 | $\ge 15$ | $\ge 13$ | $\ge 13$ | $\ge 13$ |
| Golden pure ($|0\rangle, Z$, $\theta_x = 2.40$, $A = 0.500$) | 48 | $\ge 15$ | $\ge 8$ | $\ge 7$ | $\ge 6$ |
| Golden pure ($|0\rangle, Z$, $\theta_x = 2.40$, $A = 0.500$) | 400 | $\ge 15$ | $\ge 12$ | $\ge 10$ | $\ge 9$ |
| Golden pure ($|0\rangle, Z$, $\theta_x = 2.40$, $A = 0.500$) | 800 | $\ge 15$ | $\ge 13$ | $\ge 12$ | $\ge 11$ |
| Golden pure ($|0\rangle, Z$, $\theta_x = 2.40$, $A = 0.500$) | 1,600 | $\ge 15$ | $\ge 13$ | $\ge 13$ | $\ge 13$ |

*(Note: $\varepsilon = 0$ tests were capped at $N_{\max} = \min(14, \lfloor L/2 \rfloor)$, so
`>= 15` denotes all orders $N \le 14$ excluded.)*

### 5.2 Non-Asymptotic Finite-Shot Rank-Unrestricted Certifications ($\alpha = 0.01$, CERTIFIED)

With **zero rank upper-bound assumption** and **guaranteed simultaneous coverage $\ge 99\%$**:

**Mode A (Single-Sample Unconditional Fourier-Cap — Ultra-Shot-Efficient):**

| Process | Horizon $L$ | Shots/word | Total shots | Certified $N_{\mathrm{cl}}$ (rank-unrestricted) |
|---|---:|---:|---:|---:|
| Golden pure ($\theta_x = 2.40$) | 120 | 200 | 24,200 | **$\ge 4$** |
| Golden pure ($\theta_x = 2.40$) | 400 | 200 | 80,200 | **$\ge 5$** |
| Golden pure ($\theta_x = 2.40$) | 1,200 | 100 | 120,100 | **$\ge 7$** |
| Golden pure ($\theta_x = 2.40$) | 4,000 | 50 | **200,050** | **$\ge 8$** |
| Golden mixed ($\theta_x = 2.40$) | 1,200 | 200 | 240,200 | **$\ge 6$** |
| Baseline mixed ($\theta_x = 0.73$) | 1,200 | 200 | 240,200 | **$\ge 7$** |

**Mode B (Two-Stage Split-Sample Reference-Sinusoid — Short Circuit Depth):**

| Process | Horizon $L$ | Shots/word | Total shots | Certified $N_{\mathrm{cl}}$ ($\varepsilon = 0$) | Certified $N_{\mathrm{cl}}$ ($\varepsilon = 0.002$) |
|---|---:|---:|---:|---:|---:|
| Golden pure ($\theta_x = 2.40$) | **20** | 50,000 | 1,050,000 | **$\ge 5$** | **$\ge 5$** |
| Golden pure ($\theta_x = 2.40$) | **60** | 50,000 | 3,050,000 | **$\ge 6$** | **$\ge 6$** |
| Golden pure ($\theta_x = 2.40$) | **160** | 100,000 | 16,100,000 | **$\ge 8$** | **$\ge 8$** |
| Golden pure ($\theta_x = 2.40$) | **320** | 200,000 | 64,200,000 | **$\ge 9$** | **$\ge 8$** |
| Golden mixed ($\theta_x = 2.40$) | **160** | 100,000 | 16,100,000 | **$\ge 8$** | **$\ge 8$** |
| Baseline mixed ($\theta_x = 0.73$) | **160** | 100,000 | 16,100,000 | **$\ge 8$** | **$\ge 8$** |

**Empirical Calibration (NUMERICAL, 30 independent trials at $\alpha = 0.01$):**
- **Exact 3-state classical cycle** ($\theta = 2\pi/3$, $L = 60$, 5,000 shots/word):
  $N = 2$ excluded in **30/30** trials; $N = 3$ falsely excluded in **0/30** trials.
- **Golden pure qubit** (Mode A, $L = 400$, 200 shots/word):
  $N \ge 5$ certified in **30/30** trials.

### 5.3 Two-Sided Complexity Bracket: Certified Lower Bounds vs. Explicit Classical Counterfeits (CERTIFIED & NUMERICAL)

Every bracket $[\varepsilon_{\mathrm{LB}}, \varepsilon_{\mathrm{UB}}]$ below satisfies
$\varepsilon_{\mathrm{LB}} \le \inf_{g \in \mathcal{O}_N^{\mathrm{cl}}} \max_{0 \le k \le L} |f(x^k) - g(x^k)| \le \varepsilon_{\mathrm{UB}}$,
where $\varepsilon_{\mathrm{LB}}$ is **CERTIFIED** (Theorems 1–2) and $\varepsilon_{\mathrm{UB}}$ is
witnessed by a strictly verified $N$-state classical stochastic realization (`src/ananke/approximate_realization.py`,
best of Ito/Karpelevič boundary chains, deterministic cycles, acyclic shift registers, and
multi-start L-BFGS-B + LP-polished arbitrary-rank HMMs):

**Baseline mixed qubit ($\theta_x = 0.73$, $A = 0.3593$):**

| Horizon $L$ | $N = 3$ | $N = 4$ | $N = 5$ | $N = 6$ | $N = 7$ | $N = 8$ |
|---:|---|---|---|---|---|---|
| **7** | $[0.0065,\, 0.1234]$ | $[0,\, 0.0807]$ | $[0,\, 0.0484]$ | $[0,\, 0.0234]$ | $[0,\, \mathbf{0.0006}]$ | $[0,\, \mathbf{0.0000}]$ |
| **15** | $[0.0424,\, 0.3194]$ | $[0.0075,\, 0.3192]$ | $[0.0021,\, 0.2982]$ | $[0.0001,\, 0.1999]$ | $[0,\, 0.0864]$ | $[0,\, 0.0290]$ |
| **30** | $[0.0797,\, 0.3430]$ | $[0.0326,\, 0.3415]$ | $[0.0109,\, 0.3415]$ | $[0.0023,\, 0.3171]$ | $[0.0002,\, 0.2189]$ | $[0,\, 0.0763]$ |
| **60** | $[0.1161,\, 0.3588]$ | $[0.0724,\, 0.3587]$ | $[0.0340,\, 0.3585]$ | $[0.0116,\, 0.3570]$ | $[0.0020,\, 0.3333]$ | $[0.0001,\, 0.1660]$ |
| **120** | $[0.1429,\, 0.3591]$ | $[0.1101,\, 0.3591]$ | $[0.0705,\, 0.3588]$ | $[0.0353,\, 0.3588]$ | $[0.0110,\, 0.3583]$ | $[0.0010,\, 0.3021]$ |

**Golden pure qubit ($|0\rangle, Z$, $\theta_x = 2.40$, $A = 0.5000$):**

| Horizon $L$ | $N = 3$ | $N = 4$ | $N = 5$ | $N = 6$ | $N = 7$ | $N = 8$ |
|---:|---|---|---|---|---|---|
| **7** | $[0.0107,\, 0.1947]$ | $[0,\, 0.1946]$ | $[0,\, 0.0799]$ | $[0,\, 0.0253]$ | $[0,\, \mathbf{0.0016}]$ | $[0,\, \mathbf{0.0000}]$ |
| **15** | $[0.0588,\, 0.4148]$ | $[0.0147,\, 0.4087]$ | $[0.0020,\, 0.1555]$ | $[0.0002,\, 0.1273]$ | $[0,\, 0.1272]$ | $[0,\, 0.0367]$ |
| **30** | $[0.1062,\, 0.4912]$ | $[0.0521,\, 0.4863]$ | $[0.0087,\, 0.3534]$ | $[0.0024,\, 0.3176]$ | $[0.0006,\, 0.3176]$ | $[0,\, 0.0976]$ |
| **60** | $[0.1549,\, 0.4975]$ | $[0.1059,\, 0.4981]$ | $[0.0263,\, 0.4725]$ | $[0.0100,\, 0.4561]$ | $[0.0036,\, 0.4562]$ | $[0.0002,\, 0.2091]$ |
| **120** | $[0.1933,\, 0.4999]$ | $[0.1558,\, 0.4999]$ | $[0.0601,\, 0.4971]$ | $[0.0304,\, 0.4955]$ | $[0.0163,\, 0.4880]$ | $[0.0012,\, 0.3620]$ |

**Key quantitative insight:**
At ANANKE v2's short horizon $L = 7$, an unconstrained $7$-state classical HMM reaches
error **$0.0006$** (baseline) and **$0.0016$** (golden pure), and the $8$-state shift
register reaches **$0.0000$** identically! Extending the unary ray horizon $L$ from $7$
to $15, 30, 60, 120$ destroys these finite-horizon counterfeits (pushing even the best
$8$-state model up to error $0.30$–$0.36$ at $L = 120$) and simultaneously causes our
certified rank-unrestricted lower bound to climb smoothly past $N \ge 5, 6, 8, 9, \dots, 15$.

### 5.4 Two-Symbol $\{x, z\}^{\le 7}$ Bloch Polytopes vs. Static Simplex-Box NMF (PROVED & NUMERICAL)

To test whether purely *static* nonnegative matrix factorization ($H_g = P Q$, ignoring
Markov dynamics) could instead certify high $N$ on the $15 \times 15$ v1/v2 Hankel block:
- **Static simplex-box NMF on $H_f \in [0, 1]^{15 \times 15}$ (NUMERICAL):**
  - Baseline mixed ($\|r_0\| = 0.8515$): $N = 4 \to 0.1188$, $N = 6 \to 0.0097$, **$N = 8 \to 0.0066$** (and $0.0037$ with extra restarts).
  - Golden mixed ($\|r_0\| = 0.8515$): $N = 4 \to 0.1243$, $N = 6 \to 0.0377$, **$N = 8 \to 0.0076$**.
  - Golden pure ($\|r_0\| = 1.0000$): $N = 4 \to 0.1854$, $N = 6 \to 0.1014$, $N = 8 \to 0.0348$.
  Because a static 8-state factorization $H_g = P Q$ already achieves error $< 0.007$ on
  the mixed qubit's $15 \times 15$ Hankel block, **no** purely static nonnegative-rank
  bound on that block can certify $N \ge 9$ at $\varepsilon = 0.008$.
- **Dynamical two-symbol Bloch-polytope upper bounds on $\{x, z\}^{\le 7}$ (255 words, PROVED valid realizations):**
  - Regular / Fibonacci spherical polytopes with barycentric LP transitions achieve
    inradius $\rho_{\mathrm{in}}$ and max error on $\{x, z\}^{\le 7}$:
    - Baseline mixed: $N = 6 \to 0.3627$ ($\rho = 0.708$), $N = 12 \to 0.3102$ ($\rho = 0.797$),
      $N = 20 \to 0.2370$ ($\rho = 0.830$), $N = 32 \to 0.1611$ ($\rho = 0.894$),
      $N = 64 \to 0.0961$ ($\rho = 0.945$), $N = 128 \to 0.0493$ ($\rho = 0.974$).
    - Golden pure: $N = 12 \to 0.3888$, $N = 32 \to 0.2361$, $N = 64 \to 0.1343$, $N = 128 \to 0.0721$.
  This exposes an enormous gap between static NMF ($N = 8$ suffices to error $0.007$) and
  dynamical two-symbol imitation ($N = 128$ still incurs error $0.049$–$0.072$ on $L = 7$!),
  confirming that **dynamical operator constraints**—not static factorization—carry the
  true classical memory obstruction.

---

## 6. Honest Epistemic Scope Comparison: ANANKE v2 vs. ANANKE v3

| Property | ANANKE v2 (`certified_inference.py`) | ANANKE v3 Mode A (`fourier_cap`) | ANANKE v3 Mode B (`split_sample`) |
|---|---|---|---|
| **Rank upper-bound assumption?** | **YES** ($\operatorname{rank}(H_f) = r$) | **NONE** (arbitrary rank $\le N$) | **NONE** (arbitrary rank $\le N$) |
| **Jordan / non-normal assumption?** | Simple isolated target mode | **NONE** (arbitrary Jordan blocks) | **NONE** (arbitrary Jordan blocks) |
| **Handles approximate models $\varepsilon > 0$?** | Exact realization only | **YES** (explicit $\varepsilon$-lower bound) | **YES** (explicit $\varepsilon$-lower bound) |
| **Word family** | Two-symbol $\{x, z\}^{\le 7}$ (255 words) | Unary ray $\{x^k : k \le L\}$ | Unary ray $\{x^k : k \le L\}$ |
| **Best certified $N_{\mathrm{cl}}$ (finite shots, 99%)** | $\ge 17$ (baseline), $\ge 21$ (golden) at 76.5M shots *cond. on rank 4* | **$\ge 8$** at **200k total shots** ($L = 4000$, 50 shots/word), **unconditional** | **$\ge 8$** at $L = 160$ (16.1M shots), **$\ge 9$** at $L = 320$ (64.2M shots), **unconditional** |
| **Calibration on 3-state cycle** | 0/40 false exclusions of $N = 3$ | 0/30 false exclusions of $N = 3$ | 0/30 false exclusions of $N = 3$ |

> **What v3 closes and what remains open (CONJECTURAL / OPEN):**
> - **CLOSED:** ANANKE v2's exact-rank loophole is completely closed. Using only unary
>   operation rays and **zero** assumption on $\operatorname{rank}(H_f)$, Theorems 1–3
>   rigorously certify $C_{\mathrm{classical}}(\text{qubit}; \varepsilon, \mathcal{W}_L) \ge 5, \dots, 15$
>   (including finite-shot 99%-certified $N \ge 8$ at just 200k total shots and $N \ge 9$ at
>   short depth $L = 320$).
> - **OPEN TARGET 1 (Tightening the $\Psi_N$ gap):** Our certified lower bound
>   $\varepsilon_{\mathrm{LB}}$ is currently $5\times$–$30\times$ below the best numerical
>   counterfeit $\varepsilon_{\mathrm{UB}}$ because the B-spline window uses fixed equal
>   boxcars and bounds each elementary symmetric polynomial via the scalar trace relaxation.
>   Higher-order spectral constraints (e.g., Loewy–London trace-power inequalities
>   $(\operatorname{tr} A^k)^m \le N^{m-1}\operatorname{tr} A^{km}$ or optimal Chebyshev/Faber
>   filters tailored to $\Theta_N$) could tighten $\varepsilon_{\mathrm{LB}}$ toward
>   $\varepsilon_{\mathrm{UB}}$.
> - **OPEN TARGET 2 (Joint two-symbol rank-unrestricted lower bounds at fixed $L = 7$):**
>   Our Bloch-polytope experiments suggest $C_{\mathrm{classical}}(\text{qubit}; 0.05, \{x,z\}^{\le 7}) \gg 16$
>   even at $L = 7$, whereas unary-only rank-unrestricted bounds are capped at $L + 1 = 8$.
>   Proving a genuinely noncommuting two-operator ($M_x, M_z$) rank-unrestricted lower bound
>   at short depth $L = 7$ remains a prime target for ANANKE v4.

---

## 7. Reproduction

From `ananke-necessity-transformations/`:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python experiments/certify_rank_unrestricted_v3.py
PYTHONPATH=src python experiments/counterfeit_upper_vs_lower_v3.py
```

