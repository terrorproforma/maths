# ANANKE v1: finite-shot operational inference

## 1. Why v0 was insufficient

ANANKE v0 assumed an exact behavioural oracle

\[
f:\Sigma^*\rightarrow[0,1].
\]

That is useful for proving the algebraic idea, but no experiment returns exact
probabilities. For each operation word \(w\), v1 instead observes

\[
K_w\sim\operatorname{Binomial}(N_w,p_w),
\qquad p_w=f(w).
\]

A finite dataset therefore contains counts \((K_w,N_w)\), not a privileged state
vector or transition matrix.

## 2. One noisy estimate per operational word

The same word may occur in several Hankel cells through different prefix/suffix
splittings:

\[
uv=u'v'.
\]

Those cells are not independent measurements of different quantities. They are
the same operational probability. v1 estimates each unique word once, using the
Jeffreys-smoothed value

\[
\widehat p_w=\frac{K_w+1/2}{N_w+1},
\]

and reuses it wherever that word occurs. This preserves the exact combinatorial
identity of the behavioural Hankel construction while retaining finite-shot
uncertainty.

## 3. Rank selection

Noise makes every finite Hankel matrix numerically full rank, so a raw singular-value
threshold is not a statistical answer. v1 fits fixed-rank spectral realizations
\(r=1,\ldots,r_{\max}\) on words needed for the Hankel and shifted Hankel blocks,
then evaluates each realization on strictly longer held-out words.

For each held-out word it computes binomial cross entropy. The selected rank is the
smallest rank whose mean held-out loss is within one across-word standard error of
the best predictive rank. This is deliberately conservative: extra dimensions must
buy a reproducible predictive improvement rather than merely absorb noise.

The complete selection is parametrically bootstrapped to produce a rank-stability
distribution.

## 4. Uncertainty on similarity invariants

After choosing a rank, v1 repeats the following procedure:

1. resample every word count from a plug-in binomial model;
2. rebuild the empirical Hankel and shifted Hankel blocks;
3. extract a fixed-rank minimal process;
4. match the chosen transition eigenmode to the original estimate.

For a point estimate \(\widehat\lambda\), the complex confidence disk has radius

\[
R_{1-\alpha}
=
Q_{1-\alpha}
\left(
\left|\widehat\lambda^{*}-\widehat\lambda\right|
\right),
\]

where \(\widehat\lambda^{*}\) is a bootstrap replicate. The disk is invariant under
similarity because eigenvalues are similarity invariants. Percentile intervals for
modulus and unwrapped phase are also returned.

This is a plug-in parametric bootstrap, not a finite-sample coverage theorem. Its
coverage must therefore be calibrated against known models.

## 5. Main noisy-qubit run

The baseline run measured every word through length nine over the alphabet
\(\{x,z\}\):

- 1,023 distinct operation words;
- 10,000 shots per word;
- 10,230,000 Bernoulli trials total;
- prefix and suffix depth three;
- held-out validation lengths eight and nine.

Results:

\[
\widehat{\operatorname{rank}}H=4,
\]

with rank four selected in all 100 rank-bootstrap replicates. The first eight
empirical singular values were

\[
8.8913,\ 1.5754,\ 1.2094,\ 0.5352,\ 0.0261,\ 0.0219,\ 0.0203,\ 0.0169.
\]

The extracted positive-imaginary \(x\)-mode was

\[
\widehat\lambda_x
=0.7462648+0.6678429i,
\]

with a 99% bootstrap-disk radius

\[
R_{0.99}=0.0079260.
\]

The exact synthetic reference \(e^{0.73i}\) lies inside that disk.

## 6. Shot scaling

Five independent datasets were run at each shot budget. The median numerical
classical-state lower bound was:

| Shots per word | Median selected rank | Median classical-state lower bound |
|---:|---:|---:|
| 200 | 4 | 8 |
| 500 | 4 | 8 |
| 1,000 | 4 | 8 |
| 2,000 | 4 | 9 |
| 5,000 | 4 | 9 |
| 10,000 | 4 | 16 |
| 50,000 | 4 | 17 |

The non-smooth jumps are structural. Finite stochastic eigenvalue regions expand
through Farey-labelled boundary arcs, so shrinking statistical uncertainty crosses
discrete arithmetic thresholds.

## 7. Calibration

A deterministic three-state classical cycle and a damped three-state cycle were
processed through the same inference machinery. Neither was incorrectly excluded.

In 100 independent finite-shot datasets from the exact three-cycle, the nominal
99% full-region test falsely excluded the true three-state model once:

\[
\widehat{\Pr}(\text{false exclusion})=0.01.
\]

All 100 datasets selected rank three. This small calibration does not prove general
coverage, but it catches the most obvious failure mode: interpreting any noisy
complex mode as nonclassical.

## 8. Remaining statistical work

The current implementation still conditions the spectral bootstrap on the selected
rank. A publication-grade version should add:

- sample splitting or nested bootstrap for joint rank-and-spectrum coverage;
- bias-corrected or studentized complex confidence regions;
- shot allocation optimized by Fisher information rather than equal shots per word;
- robustness to drift and correlated sequence errors;
- confidence sets for the entire simultaneous-similarity class, not one mode;
- interval-certified separation from the Karpelevič boundary.
