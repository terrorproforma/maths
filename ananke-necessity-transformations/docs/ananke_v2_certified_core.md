# ANANKE v2: Certified Karpelevič Separation, Non-Asymptotic Spectral Perturbation, and the Karpelevič Markov Theorem

This document records the theorem-and-algorithm core of **ANANKE v2**, upgrading the
v1 finite-shot pipeline (`docs/formal_core_v1.md`, `docs/research_status_v1.md`) from
floating-point boundary minimization and plug-in bootstrap heuristics to
machine-certified interval arithmetic and non-asymptotic concentration theorems.

Every mathematical and empirical claim below carries an explicit epistemic label:
- **PROVED**: complete analytic proof or exact algebraic reduction;
- **CERTIFIED**: machine-checked via outward-rounded arbitrary-precision interval
  arithmetic (`src/ananke/interval.py`, `src/ananke/karpelevich_certified.py`);
- **NUMERICAL**: empirical simulation or grid search;
- **CONJECTURAL / OPEN**: unproved target for subsequent work.

---

## 1. Outward-Rounded Interval Arithmetic and Certified Karpelevič Separation

### 1.1 Reduced Positive-Trinomial and Zero-Cancellation Form (PROVED)

Recall that the Karpelevič region $\Theta_N \subset \overline{\mathbb{D}}$ is the set
of all eigenvalues of $N \times N$ row-stochastic matrices.

**Lemma 1.1 (Star-shapedness, PROVED).**
For every $N \ge 2$, $\Theta_N$ is compact, symmetric under complex conjugation, and
star-shaped with respect to $0$:
$$\Theta_N = \bigl\{ r e^{i\theta} : \theta \in [0, 2\pi),\; 0 \le r \le \rho_N(\theta) \bigr\}.$$

*Proof.* Let $M \in \mathbb{R}_{\ge 0}^{N \times N}$ be stochastic ($M\mathbf{1}=\mathbf{1}$)
with stationary distribution $\pi^T M = \pi^T$, $\pi \ge 0$, $\pi^T\mathbf{1}=1$.
For any $t \in [0, 1]$, $M_t := t M + (1-t)\mathbf{1}\pi^T$ is nonnegative and
satisfies $M_t\mathbf{1} = \mathbf{1}$. Any left eigenvector (or generalized eigenvector)
orthogonal to $\mathbf{1}$ has its eigenvalue scaled by $t$, while $[0, 1] \subset \Theta_2 \subseteq \Theta_N$
covers all real scales of the Perron root $1$. $\square$

Between consecutive Farey fractions $p/q < r/s$ of order $N$ ($N \ge 2$), we always have
$qr - ps = 1$ and $q \neq s$ (since $q = s$ implies $q(r-p)=1$, forcing $N = 1$).
By conjugation symmetry $\Theta_N = \overline{\Theta_N}$, we orient every arc so that
$1 \le q < s \le N$.

**Theorem 1 (Reduced Positive-Trinomial & Zero-Cancellation Gap Form, PROVED).**
Let $N \ge 3$ and let $(p/q, r/s)$ be an oriented Farey arc of $\mathcal{F}_N$ with
$1 \le q < s \le N$ and $qr - ps = 1$. Set $d = \lfloor N/q \rfloor$,
$\delta = \gcd(d, s)$, $s_1 = s/\delta$, $d_1 = d/\delta$, and parameterize the open
arc by
$$\theta(t) = 2\pi\!\left(\frac{p}{q} + \frac{t}{q s}\right), \qquad t \in (0, 1).$$
Define the half-angles and full angles
$$\beta_1(t) := \frac{2\pi t}{s}, \qquad \beta_2(t) := \frac{2\pi (1 - t)}{q d}.$$
Then:
1. All modular shift parameters $(r_1, j_0, l_0, \hat{r})$ of the Kirkland–Laffey–Šmigoc
   (2020) radial formula cancel identically modulo $2\pi$, yielding
   $$\sin\bigl(\beta_1(t)\bigr)\,\hat{\rho}^{s_1} + \sin\bigl(\beta_2(t)\bigr)\,\hat{\rho}^{q d_1} = \sin\bigl(\beta_1(t) + \beta_2(t)\bigr), \qquad \rho_N(\theta(t)) = \hat{\rho}^{d_1}.$$
2. For all $N \ge 3$ and $t \in (0, 1)$, we have $\beta_1(t), \beta_2(t), \beta_1(t) + \beta_2(t) \in (0, \pi)$,
   so all three sine coefficients are strictly positive, the left-hand side is strictly
   increasing in $\hat{\rho} \in [0, 1]$, and there is a **unique** root $\hat{\rho}(t) \in (0, 1)$.
3. Setting the radial gap variable $y := 1 - \hat{\rho} \in (0, 1)$ and
   $P_m(y) := 1 - (1 - y)^m$, the equation transforms identically into the
   **zero-cancellation positive gap equation**
   $$\sin\bigl(\beta_1(t)\bigr)\,P_{s_1}(y) + \sin\bigl(\beta_2(t)\bigr)\,P_{q d_1}(y) = 4 \sin\!\left(\frac{\beta_1(t)}{2}\right)\sin\!\left(\frac{\beta_2(t)}{2}\right)\sin\!\left(\frac{\beta_1(t) + \beta_2(t)}{2}\right).$$

*Proof.* Write $r = \delta r_1 + j_0$ ($0 \le j_0 < \delta$) and choose the unique
$l_0 \in \{0, \dots, d_1 - 1\}$ with $r_1 + l_0 s_1 = \hat{r} d_1$ (possible since
$\gcd(d_1, s_1) = 1$). With $\hat{\theta} = (\theta(t) + 2\pi l_0)/d_1$:
- $q d_1 \hat{\theta} = q(\theta(t) + 2\pi l_0) = 2\pi(p + q l_0) + \frac{2\pi t}{s}$,
  so $A = \sin(q d_1 \hat{\theta}) = \sin(\beta_1(t))$.
- Using $\theta(t) = \frac{2\pi r}{s} - \frac{2\pi(1-t)}{qs}$,
  $$s_1 \hat{\theta} - \frac{2\pi j_0}{\delta d_1} = \frac{2\pi(r_1 + l_0 s_1)}{d_1} - \frac{2\pi(1-t)}{q \delta d_1} = 2\pi \hat{r} - \frac{2\pi(1-t)}{q d},$$
  so $-B = -\sin\bigl(s_1 \hat{\theta} - \frac{2\pi j_0}{\delta d_1}\bigr) = \sin(\beta_2(t))$.
- Finally, $(q d_1 - s_1)\hat{\theta} + \frac{2\pi j_0}{\delta d_1} = q d_1 \hat{\theta} - \bigl(s_1 \hat{\theta} - \frac{2\pi j_0}{\delta d_1}\bigr) = 2\pi(p + q l_0 - \hat{r}) + \beta_1(t) + \beta_2(t)$,
  so $C = \sin(\beta_1(t) + \beta_2(t))$.

Since $1 \le q < s$ and $N \ge 3$, we have $s \ge 2$, $q d = q\lfloor N/q \rfloor \ge 2$,
and $\max(s, q d) \ge 3$ (if $s = 2$ then $q = 1$ and $qd = N \ge 3$). Hence
$\beta_1(t), \beta_2(t), \beta_1(t)+\beta_2(t) \in (0, \pi)$, giving strict positivity
and strict monotonicity of $g(x;t) = \sin\beta_1 \cdot x^{s_1} + \sin\beta_2 \cdot x^{qd_1} - \sin(\beta_1+\beta_2)$
with $g(0;t) < 0 < g(1;t)$. Substituting $x = 1 - y$ and applying the exact identity
$$\sin\beta_1 + \sin\beta_2 - \sin(\beta_1 + \beta_2) = 4\sin(\beta_1/2)\sin(\beta_2/2)\sin((\beta_1+\beta_2)/2)$$
yields (3). Moreover $P_m(y)$ is evaluated without subtraction cancellation in $O(\log m)$
positive operations via $P_{2k}(y) = P_k(y)(2 - P_k(y))$ and $P_{2k+1}(y) = y + (1-y)P_{2k}(y)$. $\square$

### 1.2 Global Interval Branch-and-Bound Over All Farey Arcs (PROVED & CERTIFIED)

For any point $z = |z| e^{i\phi} \in \mathbb{C}$, any polar sector
$T = [\theta_{\mathrm{lo}}, \theta_{\mathrm{hi}}]$, and any certified radial upper bound
$\rho_{\max} \ge \sup_{\theta \in T} \rho_N(\theta)$, the exact zero-dependency polar
identity
$$|z - r e^{i\theta}|^2 = \bigl(r - |z|\cos(\theta - \phi)\bigr)^2 + \bigl(|z|\sin(\theta - \phi)\bigr)^2$$
gives the certified lower bound
$$\inf_{w \in \Theta_N,\, \arg(w)\in T} |z - w|^2 \;\ge\; \operatorname{dist}\bigl([0, \rho_{\max}],\, |z|\cos(T - \phi)\bigr)^2 + \operatorname{dist}\bigl(0,\, |z|\sin(T - \phi)\bigr)^2.$$

Our certifier (`src/ananke/interval.py`, `src/ananke/karpelevich_certified.py`) uses
self-contained outward-rounded `Decimal` arithmetic (`ROUND_FLOOR`/`ROUND_CEILING`,
explicitly verified outward `sqrt`, Machin $\pi$ enclosure, and Horner Taylor
`sin`/`cos`/`atan2` with Lagrange remainders and critical-point checks; zero external
dependencies beyond the Python standard library):
1. Checks exact cases $N=1$ ($\Theta_1=\{1\}$) and $N=2$ ($\Theta_2=[-1,1]$), and tests
   ray containment $|z|_{\mathrm{hi}} \le \rho_{N,\mathrm{lo}}(\phi)$ for $N \ge 3$.
2. Computes a certified upper bound $d_{\mathrm{hi}} \ge \operatorname{dist}(z, \Theta_N)$
   from Farey roots $e^{2\pi i p/q} \in \Theta_N$ and the ray projection.
3. Sweeps **every** Farey arc $(p/q, r/s)$ of $\mathcal{F}_N$ covering $[0, 2\pi)$,
   rigorously pruning far arcs where the unit-disk ($\rho_{\max} = 1$) sector lower bound
   exceeds $d_{\mathrm{hi}}$ while recording `pruned_min_lb`.
4. Runs best-first branch-and-bound on the remaining arcs using Theorem 1's gap upper
   bound $\rho_{\max}(T)$, returning a **CERTIFIED** global two-sided enclosure
   $[d_{\mathrm{lo}}, d_{\mathrm{hi}}] \ni \operatorname{dist}(z, \Theta_N)$.

### 1.3 Audit of v1 Benchmarks and Baseline Qubit Exclusion (CERTIFIED)

Running `experiments/certify_baseline_v2.py` (`results/certify_baseline_v2.json`):
- **Kirkland–Laffey–Šmigoc (2020) benchmark** at $\theta = 7\pi/12$, $z = 0.9 e^{7\pi i/12}$:
  - $\rho_5(7\pi/12) \in [0.8675221204970267,\; 0.8675221204970268]$ (width $1.11 \times 10^{-16}$, $< 0.9$),
    $\operatorname{dist}(z, \Theta_5) \in [0.032165,\; 0.032264]$ (**CERTIFIED** $z \notin \Theta_5$).
  - $\rho_6(7\pi/12) \in [0.9114159452656425,\; 0.9114159452656426]$ ($> 0.9$),
    $\operatorname{dist}(z, \Theta_6) = [0, 0]$ (**CERTIFIED** $z \in \Theta_6$).
- **v1 baseline qubit disk** (`results/noisy_qubit_v1.json`:
  $\hat{\lambda} = 0.7462648445835013 + 0.667842916840135 i$,
  $r_{\text{boot}, 99\%} = 0.007926034862237889$):
  - For $N = 9, \dots, 15$: $\operatorname{dist}(\hat{\lambda}, \Theta_N) \in [0.0088719,\; 0.0089425] > 0.0079260$ (**CERTIFIED EXCLUDED**).
  - For $N = 16$: $\operatorname{dist}(\hat{\lambda}, \Theta_{16}) \in [0.0073782,\; 0.0074660] < 0.0079260$ (**CERTIFIED NOT EXCLUDED**).
  - **Verdict**: The v1 full-region exclusion **$N_{\mathrm{classical}} \ge 16$** is **genuinely CERTIFIED** as a geometric statement for the v1 bootstrap disk (completing in $< 0.8\,\text{s}$ with early stopping).
- **Bug caught in v1's floating-point $N = 2$ minimizer**: For $N = 2$ ($\Theta_2 = [-1, 1]$),
  v1's `distance_to_karpelevich_region` sampled only boundary points $\rho_2(\theta) e^{i\theta}$
  (which jump discontinuously from $1$ to $0$ at $\theta = 0$), missing the open segment
  $(0, 1) \subset \Theta_2$ and reporting $0.714420 = |\hat{\lambda} - 1|$ instead of the
  exact distance $|\operatorname{Im}\hat{\lambda}| = 0.667843$. The v2 star-shaped interval
  certifier catches and fixes this automatically.

---

## 2. Non-Asymptotic Finite-Sample Spectral Perturbation Certificates

To eliminate v1's reliance on plug-in bootstrap coverage, we derive exact finite-sample
concentration and matrix perturbation theorems from independent binomial word counts
$S_w \sim \operatorname{Binomial}(M_w, f(w))$ using unbiased empirical rates
$\hat{f}(w) = S_w / M_w$.

### 2.1 Hankel Matrix Hoeffding Inequality (PROVED)

Let $\hat{H} \in \mathbb{R}^{m \times n}$ be the empirical Hankel block indexed by
prefixes $u \in \mathcal{P}$ and suffixes $v \in \mathcal{S}$ (or shifted block
$\hat{H}_a$ with entries $\hat{f}(u a v)$). Decompose the estimation error over unique
observed words $w \in \mathcal{W}$:
$$\Delta H = \hat{H} - H = \sum_{w \in \mathcal{W}} \sum_{j=1}^{M_w} \frac{Y_{w,j} - f(w)}{M_w}\, E_w, \qquad (E_w)_{u,v} = \mathbf{1}[u v = w],$$
where $Y_{w,j} \sim \operatorname{Bernoulli}(f(w))$ are mutually independent.

**Theorem 2 (Hankel Matrix Hoeffding Inequality, PROVED).**
Define the variance parameter
$$\sigma_H^2 := \max\!\left(\max_{u \in \mathcal{P}} \sum_{v \in \mathcal{S}} \frac{1}{M_{u v}},\; \max_{v \in \mathcal{S}} \sum_{u \in \mathcal{P}} \frac{1}{M_{u v}}\right)$$
(and identically $\sigma_{H_a}^2$ with $M_{u a v}$). Then for every $t > 0$ and every
choice of positive shot counts $\{M_w\}$:
$$\Pr\!\bigl(\|\hat{H} - H\|_2 \ge t\bigr) \;\le\; (m + n)\exp\!\left(-\frac{2 t^2}{\sigma_H^2}\right).$$
Equivalently, setting $\varepsilon_H(\delta) := \sqrt{\frac{\sigma_H^2}{2}\ln\frac{m + n}{\delta}}$
gives $\Pr(\|\hat{H} - H\|_2 \le \varepsilon_H(\delta)) \ge 1 - \delta$.

*Proof.* Every incidence matrix $E_w$ (and shifted $E_{a,w}$) has at most one `1` per row
and at most one `1` per column (a partial permutation matrix), because fixing $u$ and $w$
uniquely determines $v$ in $uv = w$ (or $uav = w$) and vice versa. Hence $E_w E_w^T$ and
$E_w^T E_w$ are diagonal binary matrices. Let $\mathcal{S}(B) = \begin{pmatrix}0 & B \\ B^T & 0\end{pmatrix}$
be the Hermitian dilation, so $\lambda_{\max}(\mathcal{S}(\Delta H)) = \|\Delta H\|_2$
and $\mathcal{S}(E_w)^2 = \operatorname{diag}(E_w E_w^T, E_w^T E_w)$. For each scalar
$X_{w,j} = (Y_{w,j} - f(w))/M_w \in [-f(w)/M_w, (1-f(w))/M_w]$, diagonalizing the
deterministic symmetric matrix $\mathcal{S}(E_w)$ and applying scalar Hoeffding's lemma
entrywise yields
$$\ln \mathbb{E}\bigl[e^{\theta X_{w,j} \mathcal{S}(E_w)}\bigr] \preceq \frac{\theta^2}{8 M_w^2}\,\mathcal{S}(E_w)^2.$$
Summing over $w$ and $j = 1, \dots, M_w$ yields $\frac{\theta^2}{8}\sum_w \frac{1}{M_w}\mathcal{S}(E_w)^2 \preceq \frac{\theta^2 \sigma_H^2}{8} I_{m+n}$.
Applying Tropp's Master Tail Bound (Lieb's concavity theorem, Tropp 2012 Theorem 3.6) and
optimizing $\theta = 4t/\sigma_H^2$ gives $(m+n)\exp(-2t^2/\sigma_H^2)$. $\square$

On the $15 \times 15$ baseline Hankel block at $M = 10{,}000$, $\delta = 0.005$,
Theorem 2 gives $\varepsilon_H = 0.0808$, which is **$3.83\times$ tighter** than the
entrywise Chernoff–KL union bound + Frobenius norm ($0.3097$).

**Corollary 2.1 (Unconditional Certified Rank Lower Bound, PROVED).**
By Weyl's singular value inequality $|\sigma_i(H) - \hat{\sigma}_i| \le \|\Delta H\|_2$:
on the event $\|\Delta H\|_2 \le \varepsilon_H$, if $\hat{\sigma}_r > \varepsilon_H$ then
$\operatorname{rank}(H) \ge r$ unconditionally, and $\sigma_{r+1}(H) \le \hat{\sigma}_{r+1} + \varepsilon_H$.
On the baseline qubit at $M = 10{,}000$ ($\alpha = 0.01$), $\hat{\sigma}_4 = 0.535 > 0.081$,
**unconditionally certifying $\operatorname{rank}(H) \ge 4$**.

### 2.2 Exact Similarity Elimination and Schur-Complement Block Isolation (PROVED)

**Theorem 3 (Exact Similarity Elimination & Schur-Complement Block Isolation, PROVED).**
Assume the exact rank-$r$ structural condition $\operatorname{rank}(H_f) = \operatorname{rank}(H) = r$,
so $H = U\Sigma V^T$ and $H_a = U T_a \Sigma V^T$ with $T_a$ similar to the minimal
transition $B_a$. Let $\hat{U}_r \in \mathbb{R}^{m \times r}$, $\hat{V}_r \in \mathbb{R}^{n \times r}$
be any matrices with orthonormal columns, and define
$$X := \hat{U}_r^T H \hat{V}_r, \qquad Y_a := \hat{U}_r^T H_a \hat{V}_r, \qquad \hat{X} := \hat{U}_r^T \hat{H} \hat{V}_r, \qquad \hat{Y}_a := \hat{U}_r^T \hat{H}_a \hat{V}_r.$$
1. **Exact Similarity Elimination**: Whenever $\sigma_{\min}(\hat{X}) > \|\Delta X\|_2$
   (where $\Delta X = \hat{X} - X$, $\Delta Y_a = \hat{Y}_a - Y_a$), the $r \times r$ matrix
   $X = (\hat{U}_r^T U)\Sigma(V^T \hat{V}_r)$ is invertible, so $A := \hat{U}_r^T U$ is
   invertible, and
   $$M_a^* := Y_a X^{-1} = A T_a A^{-1}$$
   is **exact-spectrum similar to $B_a$**, with the exact algebraic identity (no Wedin
   $\sin\Theta$ error):
   $$\hat{T}_a - M_a^* = (\Delta Y_a - \hat{T}_a \Delta X)\, X^{-1}, \qquad \hat{T}_a := \hat{Y}_a \hat{X}^{-1}.$$
2. **Schur-Complement Block Isolation (handles degenerate complementary spectra)**:
   Let $W = [q_1, Q_\perp] \in \mathbb{C}^{r \times r}$ be any invertible matrix with
   $D_0 := \operatorname{diag}(\hat{\lambda}, R_\perp)$ and
   $W^{-1} M_a^* W = D_0 - \begin{pmatrix} e_{11} & e_{12}^H \\ e_{21} & E_{22} \end{pmatrix}$.
   Let $\gamma := \sigma_{\min}(R_\perp - \hat{\lambda} I)$ and suppose
   $|e_{11}| \le b_{11}$, $\|e_{12}\|_2 \le b_{12}$, $\|e_{21}\|_2 \le b_{21}$, $\|E_{22}\|_2 \le b_{22}$.
   If $\Delta_{\mathrm{gap}} := \gamma - b_{11} - b_{22} > 0$ and $\Delta_{\mathrm{gap}}^2 > 4 b_{12} b_{21}$,
   then for any $\rho > 0$ satisfying
   $$\gamma - \rho - b_{22} > 0 \qquad \text{and} \qquad \rho > b_{11} + \frac{b_{12} b_{21}}{\gamma - \rho - b_{22}},$$
   the disk $D(\hat{\lambda}, \rho)$ contains a **unique** eigenvalue of $B_a$.

*Proof.* (1) Invertibility of $X = A \Sigma C^T$ forces invertibility of all three
$r \times r$ factors, giving $Y_a X^{-1} = (A T_a \Sigma C^T)(A \Sigma C^T)^{-1} = A T_a A^{-1}$.
Multiplying $\hat{T}_a - M_a^*$ on the right by $X = \hat{X} - \Delta X$ gives
$\hat{Y}_a - \hat{T}_a \Delta X - Y_a = \Delta Y_a - \hat{T}_a \Delta X$.
(2) Consider the linear homotopy $M(t) := D_0 - t(D_0 - W^{-1} M_a^* W)$ for $t \in [0, 1]$.
For every $\lambda$ on the circle $|\lambda - \hat{\lambda}| = \rho$ and every $t \in [0, 1]$,
Weyl's inequality gives $\sigma_{\min}(R_\perp - t E_{22} - \lambda I) \ge \gamma - \rho - b_{22} > 0$,
so the $(2,2)$ block is invertible and the Schur complement
$\hat{\lambda} - \lambda - t e_{11} - t^2 e_{12}^H (R_\perp - t E_{22} - \lambda I)^{-1} e_{21}$
has modulus at least $\rho - b_{11} - \frac{b_{12} b_{21}}{\gamma - \rho - b_{22}} > 0$.
Thus $\det(M(t) - \lambda I) \neq 0$ along the entire circle for all $t \in [0, 1]$. By
continuity of roots, $M(1) = W^{-1} M_a^* W$ (and hence $B_a$) has the same number of
eigenvalues inside $D(\hat{\lambda}, \rho)$ as $M(0) = D_0$, namely **one** (since
$\gamma > \rho$ excludes $\operatorname{spec}(R_\perp)$). $\square$

> **Why Block Isolation beats Bauer–Fike here:** For a qubit $R_x$ rotation on the
> homogeneous Bloch space $\mathbb{R}^4$, $\lambda = 1$ has algebraic multiplicity $2$
> (both the trace coordinate and the $x$-axis are fixed). Noise splits this double
> eigenvalue with nearly parallel eigenvectors, blowing up $\kappa(\hat{Q})$ in
> Bauer–Fike by $5\times$–$30\times$. Block isolation keeps $R_\perp$ intact without
> ever diagonalizing the degenerate block.

### 2.3 Two-Stage Split-Sample Scalar+Projected Certificate (PROVED)

Given a binomial `ShotDataset`, `split_shot_dataset` draws
$S_w^{(1)} \mid S_w \sim \operatorname{Hypergeometric}(S_w, M_w - S_w, M_{w,1})$ and sets
$S_w^{(2)} = S_w - S_w^{(1)}$, yielding **strictly independent** binomial datasets
`ds1` (pilot, e.g. 15%) and `ds2` (main, 85%). Conditional on `ds1`:
- $(\tilde{U}_r, \tilde{V}_r, T_1, X_1, \lambda_1, W = [q_1, Q_\perp])$ are **deterministic**;
- $\Delta X, \Delta Y_a$ are $r \times r$ ($4 \times 4$) matrices bounded by projected
  Matrix Hoeffding (dimension $2r = 8$ instead of $m + n = 30$, levels $\delta_X = \delta_Y = \alpha/4$);
- the leading $(1,1)$ error $S = p_1^H (\Delta Y_a - \lambda_1 \Delta X) X_1^{-1} q_1 = \sum_w c_w (\hat{f}^{(2)}(w) - f(w))$
  is a **deterministic scalar linear functional** bounded directly by scalar Hoeffding
  (level $\delta_s = \alpha/2$), while the $O(\varepsilon^2)$ remainder is bounded via
  $\varepsilon_X, \varepsilon_Y$.

By the law of total expectation, unconditional failure probability is $\le \delta_X + \delta_Y + \delta_s = \alpha$.

> **Epistemic Scope Box (Honest Boundary of Theorem 3):**
> 1. **Unconditional (no rank upper bound needed):** $\operatorname{rank}(H) \ge r$ and
>    $\sigma_{r+1}(H) \le \hat{\sigma}_{r+1} + \varepsilon_H$ hold with probability $\ge 1 - \alpha$
>    for *any* underlying sequential process $f$.
> 2. **Conditional on exact minimal rank $r$ ($\operatorname{rank}(H_f) = \operatorname{rank}(H) = r$):**
>    The certified eigenvalue disk $D(\hat{\lambda}, \rho)$ contains a unique eigenvalue of
>    $B_a$ with probability $\ge 1 - \alpha$, so interval-certified separation
>    $D(\hat{\lambda}, \rho) \cap \Theta_N = \varnothing$ excludes every exact $N$-state
>    classical stochastic realization of that rank-$r$ process.
> 3. **What remains outside Theorem 3:** Finite-shot data on a finite Hankel block can
>    never prove $\operatorname{rank}(H_f) \le r$ without a structural bound, so an
>    *approximate* classical counterfeit with rank $> r$ and tiny tail singular values
>    $\sigma_{r+1}(H) \le \hat{\sigma}_{r+1} + \varepsilon_H$ is not ruled out by a
>    single-block spectral perturbation theorem alone.

### 2.4 Non-Asymptotic Shot Scaling on the Baseline Qubit (CERTIFIED, $\alpha = 0.01$)

From `experiments/certify_baseline_v2.py` (`results/certify_baseline_v2.json`), baseline
qubit $\theta_x = 0.73$, $\theta_z = 1.11$, $15 \times 15$ Hankel block (255 words of length $\le 7$):

| Shots/word $M$ | Rank LB | Bauer–Fike rad | Single-sample Block rad | Single $N_{\mathrm{cl}}$ | Split-sample Scalar+Block rad | Split $N_{\mathrm{cl}}$ | True err (split) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10,000 | 4 | 1.1493 | (unisolated) | $\ge 4$ | (unisolated) | $\ge 4$ | 0.00304 |
| 30,000 | 4 | 0.9453 | 0.14469 | $\ge 6$ | **0.04073** | **$\ge 8$** | 0.00182 |
| 100,000 | 4 | 0.3067 | 0.05776 | $\ge 8$ | **0.01369** | **$\ge 9$** | 0.00097 |
| 300,000 | 4 | 0.1629 | 0.02999 | $\ge 8$ | **0.00538** | **$\ge 17$** | 0.00092 |
| 1,000,000 | 4 | 0.2792 | 0.01556 | $\ge 9$ | **0.00244** | **$\ge 17$** | 0.00028 |
| 3,000,000 | 4 | 0.0525 | 0.00874 | $\ge 9$ | **0.00121** | **$\ge 18$** | 0.00031 |
| 10,000,000 | 4 | 0.1358 | 0.00471 | $\ge 17$ | **0.00061** | **$\ge 26$** | 0.00004 |

Key comparisons:
- **End-to-end certified $N \ge 17$** (beating v1's plug-in bootstrap $N \ge 16$) is
  achieved at **$M = 300{,}000$ shots/word** via our split-sample scalar+projected
  certificate ($30\times$ more shots than v1's heuristic bootstrap, vs $> 300\times$
  for single-sample and $> 3000\times$ for naive Bauer–Fike).
- **Empirical calibration (40 independent trials at $\alpha = 0.01$)**:
  - Baseline qubit ($M = 100{,}000$): exact mode covered in **40/40** trials.
  - Exact 3-state classical cycle ($M = 50{,}000$, boundary mode $e^{2\pi i/3} \in \partial\Theta_3$):
    **0/40** false exclusions of $\Theta_3$.

---

## 3. Diophantine Gate Design and the Noble-Phase Optimality Conjecture

### 3.1 Asymptotic Karpelevič Gap Scaling and the Karpelevič Markov Theorem (PROVED)

Expanding Theorem 1(3) as $\min(s, q d) \to \infty$ (where $\sin u = u(1 - u^2/6 + \dots)$
and $P_m(y) = m y(1 - O(my))$ with $m y = O(N^{-2})$), the coefficient of $y$ on the
left-hand side simplifies identically to $\frac{2\pi}{\delta}(t + (1-t)) = \frac{2\pi}{\delta}$,
and multiplying by $d_1 = d/\delta$ cancels $d$:

**Corollary 4.1 (Asymptotic Karpelevič Radial & Euclidean Gap, PROVED).**
On an oriented Farey arc $(p/q, r/s)$ of $\mathcal{F}_N$ ($q < s$, $d = \lfloor N/q \rfloor$),
for $t \in (0, 1)$ bounded away from $\{0, 1\}$:
$$1 - \rho_N(\theta(t)) = 2\pi^2\,\frac{t(1 - t)}{q s}\!\left(\frac{t}{s} + \frac{1 - t}{q d}\right)\bigl(1 + O(N^{-2})\bigr),$$
and because the boundary tangent slope is $\rho_N'(\theta) = O(1/N)$, the Euclidean
distance obeys $\operatorname{dist}(e^{i\theta(t)}, \Theta_N) = (1 - \rho_N(\theta(t)))(1 + O(N^{-2}))$.

In contrast to nearest roots of unity ($\delta_N(\alpha) \asymp N^{-2}$ for badly
approximable phases), the Karpelevič distance scales as **$N^{-3}$** (larger than the
straight-chord sagitta $2\pi^2 t(1-t)/(q^2 s^2)$ by the inward-bowing factor $q t + \frac{s}{d}(1-t)$).

**Theorem 4 (Karpelevič Markov Theorem — Asymptotic Optimality of Noble Phases, PROVED).**
For any irrational $\alpha \in (0, 1)$, define its Karpelevič Markov constant
$$\kappa_\Theta(\alpha) := \liminf_{N \to \infty} N^3\,\operatorname{dist}\!\left(e^{2\pi i \alpha}, \Theta_N\right).$$
1. For every **noble** irrational $\alpha_* = [0; a_1, \dots, a_m, \overline{1}]$
   (including every $[0; k, \overline{1}]$):
   $$\kappa_\Theta(\alpha_*) = \frac{2\pi^2 \varphi^3}{5\sqrt{5}} \approx 7.478899, \qquad \varphi = \frac{1 + \sqrt{5}}{2}.$$
2. For every **non-noble** irrational $\alpha$:
   $$\kappa_\Theta(\alpha) \le \frac{3\pi^2}{4} \approx 7.402203 < \frac{2\pi^2 \varphi^3}{5\sqrt{5}} = \kappa_\Theta(\alpha_*).$$

*Proof.* Write $\alpha = [0; a_1, a_2, \dots]$ with convergents $p_k/q_k$, ratios
$\beta_k := q_k / q_{k-1} = [a_k; a_{k-1}, \dots, a_1] \in (a_k, a_k+1)$, and tails
$\alpha_{k+1} := [a_{k+1}; a_{k+2}, \dots] > a_{k+1}$.
At order $N = q_k$, the oriented Farey bracket is $(p_{k-1}/q_{k-1}, p_k/q_k)$ with
$q = q_{k-1}$, $s = q_k = N$, $d = \lfloor q_k/q_{k-1} \rfloor = a_k$, and
$t = \frac{u}{u + 1}$ where $u := \alpha_{k+1}\beta_k$. Setting $\gamma := \beta_k / a_k \in (1, 2)$:
$$C_0(\beta_k, \alpha_{k+1}) := \lim_{q_k \to \infty} q_k^3 \cdot 2\pi^2 \frac{t(1-t)}{q_{k-1} q_k}\!\left(\frac{t}{q_k} + \frac{1-t}{q_{k-1} a_k}\right) = 2\pi^2 \beta_k\,\frac{u(u + \gamma)}{(u + 1)^3}.$$

*(Part 1 — Noble numbers).* Eventually $a_j = 1$, so $\beta_k \to \varphi$, $\alpha_{k+1} \to \varphi$,
$u \to \varphi^2$, $\gamma \to \varphi$, $t \to \varphi/\sqrt{5}$, and $t(1-t) \to 1/5$.
Between $q_k$ and $q_{k+1}-1$, the Farey bracket is constant with $d=1$ on $[q_k, 2q_{k-1}-1]$
and $d=2$ on $[2q_{k-1}, q_{k+1}-1]$. Minimizing $N^3(1-\rho_N)$ at the two plateau left
endpoints gives $\frac{2\pi^2 \varphi^3}{5\sqrt{5}} \approx 7.4789$ at $N = q_k$ and
$\frac{8\pi^2\varphi}{5\sqrt{5}} \approx 11.4280$ at $N = 2q_{k-1}$, proving (1).

*(Part 2 — Non-noble numbers).* Since $\gamma = \beta_k / \lfloor \beta_k \rfloor < 2$,
we have $u(u + \gamma) < u(u + 2) = (u+1)^2 - 1 < (u+1)^2$, hence universally:
$$C_0(\beta_k, \alpha_{k+1}) < \frac{2\pi^2 \beta_k}{\alpha_{k+1}\beta_k + 1}.$$
Because $\alpha$ is non-noble, $a_{k+1} \ge 2$ for infinitely many $k$:
- **Case 1**: $a_{k+1} \ge 3$ infinitely often. Then $\alpha_{k+1} > 3$, so
  $C_0 < \frac{2\pi^2}{3} \approx 6.5797 < \frac{2\pi^2\varphi^3}{5\sqrt{5}}$.
- **Case 2**: Eventually $a_j \in \{1, 2\}$ for all $j \ge J_0$, and $a_{k+1} = 2$ infinitely
  often. Then $\alpha_{k+1} = 2 + \frac{1}{a_{k+2} + 1/\alpha_{k+3}} > 2 + \frac{1}{2+1} = \frac{7}{3}$.
  - If $a_k = 1$, then $\beta_k = 1 + \frac{1}{a_{k-1} + 1/\beta_{k-2}} \le 1 + \frac{1}{1+1/3} = \frac{7}{4}$,
    giving $C_0 < \frac{2\pi^2(7/4)}{(7/3)(7/4)+1} = \frac{42\pi^2}{61} \approx 6.7955$.
  - If $a_k = 2$, then $\beta_k < 3$, giving
    $C_0 < \frac{2\pi^2 \cdot 3}{(7/3)\cdot 3 + 1} = \frac{3\pi^2}{4} \approx 7.4022$.

Finally, $\frac{3}{4} < \frac{2\varphi^3}{5\sqrt{5}} \iff 15\sqrt{5} < 8(2 + \sqrt{5}) \iff 7\sqrt{5} < 16 \iff 245 < 256$. $\square$

### 3.2 Honest Refinements of the v1 Conjecture (PROVED & CERTIFIED)

While Theorem 4 **proves** the asymptotic lower-envelope half of the v1 conjecture, our
analysis reveals two sharp finite-regime refinements (`experiments/diophantine_design_v2.py`,
`results/diophantine_design_v2.json`):

1. **Refinement A — Finite-Horizon Arc-Asymmetry Counterexample (PROVED/CERTIFIED):**
   On a single oriented Farey arc $(p/q, r/s)$ with $s > q d$, the cubic
   $t(1-t)(t/s + (1-t)/(qd))$ is skewed toward $t < 1/2$, whereas noble phases sit at
   $t > 0.64$ (asymptotically $\varphi/\sqrt{5} \approx 0.7236$). Thus at fixed finite $N$,
   non-noble competitors strictly outperform $[0; 8, \overline{1}]$ inside sector $k = 8$:
   - At $N = 15$: silver $[0; 8, \overline{2}]$ has certified distance $[0.008149, 0.008199]$
     and the sector peak ($\theta = 0.7431$) achieves $[0.008211, 0.008258]$, beating noble
     $[0; 8, \overline{1}]$ ($[0.007337, 0.007381]$) by **$+11.1\%$** and **$+11.9\%$**.
   - At $N = 25$: $[0; 8, \overline{1,2}]$ achieves $[0.001833, 0.001852]$, beating noble
     $[0; 8, \overline{1}]$ ($[0.001377, 0.001394]$) by **$+33.1\%$**.
   (Conversely, silver collapses to $0.000555$ at $N = 25$, illustrating why noble
   maximizes the *asymptotic lower envelope* rather than any single fixed $N$.)

2. **Refinement B — Cross-Sector Hankel Conditioning Dominates Fixed-Shot Budgets (CERTIFIED):**
   Within sector $k = 8$, Hankel conditioning $\sigma_4(H)$ varies by $< 0.5\%$. Across
   sectors, moving to larger-angle noble phases doubles $\sigma_4(H)$ and halves the
   exact scalar Hoeffding sensitivity $\|c\|_2$, dramatically raising the certified
   classical-memory lower bound at identical shot budgets (99% split-sample certified):

   | Phase design | $\theta_x$ (rad) | $\sigma_4(H)$ | Sensitivity $\|c\|_2$ | Certified $N_{\mathrm{cl}}$ ($100\text{k}$ shots) | Certified $N_{\mathrm{cl}}$ ($300\text{k}$ shots) |
   |---|---:|---:|---:|---:|---:|
   | Baseline $0.73$ ($k=8$) | 0.7300 | 0.5415 | 0.8728 | $\ge 9$ (rad $0.01302$) | $\ge 16$ (rad $0.00566$) |
   | Noble $[0;8,\overline{1}]$ | 0.7291 | 0.5413 | 0.8738 | $\ge 9$ (rad $0.01238$) | $\ge 17$ (rad $0.00554$) |
   | Silver $[0;8,\overline{2}]$ | 0.7467 | 0.5437 | 0.8557 | $\ge 9$ (rad $0.01278$) | $\ge 17$ (rad $0.00515$) |
   | Noble $[0;3,\overline{1}]$ | 1.7366 | **0.9928** | **0.4718** | **$\ge 14$** (rad $0.00410$) | **$\ge 18$** (rad $0.00204$) |
   | Golden $[0;2,\overline{1}]$ | 2.4000 | **1.0856** | **0.4827** | **$\ge 13$** (rad $0.00433$) | **$\ge 21$** (rad $0.00209$) |

   **Refined Design Principle:** Use a **large-angle noble phase** such as the golden angle
   $[0; 2, \overline{1}] = 1/\varphi^2$ ($\theta_x \approx 2.400\,\text{rad}$) or
   $[0; 3, \overline{1}]$ ($\theta_x \approx 1.737\,\text{rad}$): it simultaneously
   attains the globally optimal asymptotic Karpelevič Markov constant
   $2\pi^2\varphi^3/(5\sqrt{5})$ (Theorem 4) *and* cuts finite-shot certified radii by
   $2.5\times$–$3\times$ via superior Hankel conditioning.

---

## 4. Open Targets for ANANKE v3 (CONJECTURAL / OPEN)

1. **Rank-unrestricted approximate counterfeit complexity $C_{\mathrm{classical}}(f; \varepsilon, \mathcal{W})$**:
   extend Theorem 3 to certify lower bounds even against higher-rank classical models
   whose $(r+1)$-th Hankel singular value lies below $\hat{\sigma}_{r+1} + \varepsilon_H$
   (e.g. via positive-rank / nonnegative-matrix-factorization or SDP relaxations).
2. **Joint multi-operator invariants**: move beyond single-symbol transition spectra
   $\operatorname{spec}(B_a)$ to simultaneous noncommuting invariants of $\{B_x, B_z\}$
   (e.g. commutator / semigroup spectral constraints).
3. **Cross-ontology comparison**: compare classical simplicial, quantum semidefinite, and
   general GPT realization costs on the same extracted core.

---

## 5. Reproduction

From `ananke-necessity-transformations/`:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python experiments/certify_baseline_v2.py
PYTHONPATH=src python experiments/diophantine_design_v2.py
```
