Direct AMY Transport v1.4 - Research Package

Main paper:
  direct_amy_transport_v1_4.pdf
  direct_amy_transport_v1_4.md
  direct_amy_transport_v1_4.tex

Numerical implementation:
  verify_full_amy_collision_v1_4.py
  amy_v14_core.py
  amy_v14_angle.py

Data products:
  amy_collision_results_v1_4.json
  amy_collision_parameter_table_v1_4.csv
  amy_collision_operator_table_v1_4.npz
  amy_collision_acceptance_matrix_v1_4.csv

Figures:
  amy_lpm_exact_v1_4.png
  amy_full_angle_screened_v1_4.png
  amy_parameter_scan_v1_4.png
  amy_rate_hierarchy_v1_4.png
  amy_reduced_kb_v1_4.png
  amy_two_time_F_v1_4.png

Reproduction:
  PYTHONPATH=. python verify_full_amy_collision_v1_4.py

Scope:
  - Direct isotropic leading-order AMY LPM solve for the QCD channels.
  - Full-angle screened 2<->2 transport moments.
  - Generalised H<->qD Yukawa-LPM prefactor carries a factor-two band.
  - Reduced two-time KB benchmark is not a full non-Abelian 2PI simulation.
