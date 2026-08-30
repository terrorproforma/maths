# Primary-source notes

These notes are narrow paraphrases keyed to official sources. They are not substitutes for the manuscript or lecture.

## Source hierarchy

1. The 2021 working draft controls written definitions and equations.
2. The official Oxford page is a composite source:
   - 2013 lecture;
   - 2020 Portal publication context;
   - supplementary PowerPoint using updated notation.
3. Conflicts are recorded, not silently reconciled.

## Draft status

- Title: *Geometric Unity: Author's Working Draft*, v1.0, 1 April 2021.
- The title-page notice describes the work as entertainment and work in progress and restricts derivative use.
- The PDF is cited rather than mirrored.

## Initial data and objective

- Draft pp. 3–4, eq. (1.1): begins with an oriented smooth \(X^4\), a unique spin structure and no chosen geometry.
- The source asks how much observed field-theory structure can be generated from that sparse input.
- It explicitly does not claim to derive existence from nothing.

## Observerse and metric bundle

- Draft pp. 15–16, Definition 3.1 and eq. (3.1): defines an Observerse \((X,Y,\{\iota\})\).
- The Einsteinian choice is \(Y=\operatorname{Met}(X)\).
- The official lecture describes \(Y^{14}=\operatorname{Met}(X^4)\) and the ten-dimensional metric fibre.

## Chimeric bundle and spinors

- Draft pp. 17–24: constructs vertical/horizontal data, the Chimeric Bundle and \(Spin(7,7)\) spinors.
- The main structure group is presented as \(U(64,64)\).
- One Clifford decomposition is explicitly flagged for checking.

## Observation and internal quantum numbers

- Draft pp. 24–30: observation pulls topological spinors back to spacetime spinors with normal-bundle factors interpreted as apparent internal quantum numbers.
- Pati–Salam-like subgroup structure is proposed, but no complete low-energy gauge Lagrangian or anomaly audit is supplied.

## Unified fields and inhomogeneous gauge group

- Draft pp. 30–34: defines the affine connection space, \(N=\Omega^1(Y,\operatorname{ad}P_H)\), and the inhomogeneous group.
- The semidirect-product law and affine action have been independently checked.

## Distinguished connection and sign conflict

- The observation field induces a distinguished connection \(A_0[\gimel]\).
- Draft eq. (6.4) uses
  \[
  \tau_-(h)=\left(h,-h^{-1}d_{A_0}h\right).
  \]
- The Oxford lecture at approximately `01:27:54` instead uses the plus sign.
- The draft itself warns that multiple sign conventions were combined.
- The exact TP-02 audit shows that, under the printed 2021 right action, \(\tau_-\) is the stabiliser but the printed \(T_-\) is not equivariant.

## Augmented torsion

- Draft section 7 prints
  \[
  T_-=a-\varepsilon^{-1}d_{A_0}\varepsilon.
  \]
- The Oxford transcript and supplementary slide also use the minus torsion sign.
- The stabiliser-compatible repaired branch is
  \[
  T_+=a+\varepsilon^{-1}d_{A_0}\varepsilon.
  \]

## Shiab family

- Draft section 8 describes gauge-conjugated invariant contractions using Hodge operations and commutator or \(i\)-Jordan products.
- Definition 8.1 introduces invariant tensors \(\Phi_i\).
- The official lecture states
  \[
  \operatorname{Sh}:\Omega^i(\operatorname{ad})\to\Omega^{d-3+i}(\operatorname{ad}).
  \]
- Draft eq. (9.3) gives an explicit substitute
  \[
  \Omega^2(Y,\operatorname{ad})\to\Omega^{d-1}(Y,\operatorname{ad}).
  \]
- The source says the originally preferred Bianchi-selected operator cannot presently be located.

## Clifford–Einstein interpretation

The draft labels the first term Ricci-like, the nested term scalar-like and states that Weyl curvature is annihilated.

The exact project audit proves that, on spin curvature,

\[
[\gamma^c,F_{cd}]=R_{db}\gamma^b,
\]

\[
\{\gamma^{cd},F_{cd}\}=-R\mathbf1,
\]

so the mixed commutator/Jordan pattern reproduces the Einstein tensor and kills Weyl curvature.

This fixes the intended product pattern on the geometric Riemann sector, not the complete \(U(64,64)\)-adjoint extension.

## First-order bosonic action

- Draft eq. (9.4) pairs augmented torsion with a Shiab-contracted curvature/transgression-like expression and a quadratic torsion term.
- The literal printed sign branch fails the claimed finite covariance test.
- The repaired branch passes that kinematic test but still lacks a complete source-defined Hessian.

## Deformation complex and dynamics

- Draft section 10 proposes a deformation complex and explicitly caveats possible inconsistencies.
- The official lecture states that propagation in 14 dimensions must still be shown to appear four-dimensional.
- No complete Hamiltonian/BRST count, positive spectrum, anomaly polynomial, quantum measure or empirical fit is supplied.

## Audit consequence

The source corpus is rich enough for exact algebraic reconstruction and a meaningful Einstein-sector Shiab test.

It is not complete enough to determine one full physical spectrum without separately declared completion data.
