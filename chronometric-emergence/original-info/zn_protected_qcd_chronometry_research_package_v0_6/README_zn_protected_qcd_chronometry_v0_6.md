# Z_N-Protected QCD Chronometry v0.6

This package contains the working construction requested in the QCD chronometry programme: a cyclic discrete-Goldstone ratio mode whose complete replicated-sector orbit suppresses the vacuum mass to order \(\epsilon^N\), while a single visible vectorlike-quark threshold retains the QCD transmission coefficient \(2/27\).

## Main files

- `zn_protected_qcd_chronometry_v0_6.pdf` - 18-page technical paper.
- `zn_protected_qcd_chronometry_v0_6.md` - editable research notes.
- `zn_protected_qcd_chronometry_v0_6.tex` - complete LaTeX source.
- `zn_protected_qcd_claim_matrix_v0_6.csv` - claim, evidence, caveat, and novelty matrix.
- `verify_zn_protected_qcd_chronometry_v0_6.py` - symbolic and numerical tests.
- `zn_protected_qcd_chronometry_verification_v0_6.json` - machine-readable test results.
- `zn_protected_mass_scaling_v0_6.png` - mass-suppression figure.

## Central benchmark

For \(N=6\), \(a_0/f_a=\pi/2\), and a visible Dirac colour fundamental,

\[
\frac{\partial}{\partial(a/f_a)}\ln\frac{M_0}{\chi}=\epsilon,
\]

\[
\mathrm d\ln\frac{\Lambda_3}{\chi}
=\left[\frac{2}{27}+O(\alpha_s)\right]\epsilon\,\mathrm d\left(\frac a{f_a}\right),
\]

while

\[
m_a^2=\frac{27}{320\pi^2}\frac{M^4}{f_a^2}\epsilon^6+O(\epsilon^7).
\]

The result is a technically natural perturbative EFT under an exact cyclic symmetry. Its principal unresolved issues are ultraviolet quality, replicated-sector cosmology, and finite-density screening.
