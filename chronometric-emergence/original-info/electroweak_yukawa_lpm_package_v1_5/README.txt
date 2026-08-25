Electroweak/Yukawa LPM Matching v1.5
====================================

Core result:
  I_LPM = Gamma_Y/(Nc y_D^2 T^3) = 8.895e-4 (benchmark)
  Gamma_H_occ/T = 3.603e-4
  Gamma_H_occ/Gamma_R = 2.44e6 at T0 = 1.002e8 GeV

Scope:
  - Complete leading-order collinear/LPM sector for H <-> Q_L D_R.
  - Simultaneous SU(3)c, SU(2)L and U(1)Y soft kernels.
  - Exact integrated matching to the qD contribution to Im Pi_H^R.
  - Reduced Wilson-line-dressed Schwinger-Keldysh benchmark.
  - Hard Yukawa-assisted 2 <-> 2 cuts are not included and remain the next
    part of the complete leading-order portal self-energy.

Run:
  python verify_electroweak_yukawa_lpm_v1_5.py

Optional expensive checks:
  python verify_electroweak_yukawa_lpm_v1_5.py --recompute-high
  python verify_electroweak_yukawa_lpm_v1_5.py --recompute-scan
