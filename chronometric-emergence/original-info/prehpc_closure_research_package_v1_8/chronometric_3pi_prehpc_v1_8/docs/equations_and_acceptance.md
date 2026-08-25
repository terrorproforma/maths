# Equations and acceptance gates

## Matched retarded kernel

The reduced benchmark is organized as

\[
\widehat\Pi_H^R=
\Pi_{1\leftrightarrow2}^{\rm Born/LPM\,interp}
+\Pi_{2\leftrightarrow2,1\leftrightarrow3}^{\rm hard,reg}
+\Pi_{\rm HTL}^{\rm soft}
-\Pi_{\rm overlap}.
\]

The physical production implementation must verify

\[
\frac{\partial\widehat\Pi_H^R}{\partial\ln q_*}=0
\]

at the resolved order and match the independent on-shell hard-plus-LPM anchor.

## Vertex closure

Background vertices obey linear Ward identities. Quantum vertices must satisfy the appropriate Slavnov-Taylor identities including ghost dressing and matter-ghost scattering kernels. Transverse components are determined dynamically rather than by Ward identities.

## Composite control

The gauge-singlet correlator obeys a conserving Bethe-Salpeter equation with kernel

\[
K=\frac{\delta\Sigma}{\delta G}.
\]

The same truncation must be used in the self-energy and ladder kernel.

## Failure conditions

The run fails if any of the configured thresholds for Ward/STI residuals, Nielsen pole stability, KMS, equal-time normalization, conservation, factorization-scale cancellation or singlet spectral positivity are exceeded.
