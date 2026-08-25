#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

out = Path('/mnt/data/in_in_two_loop_topology_v1_0.png')
fig, ax = plt.subplots(figsize=(12.6, 5.8))
ax.set_xlim(0, 12.6)
ax.set_ylim(0, 5.8)
ax.axis('off')

nodes = [
    (0.35, 3.75, 1.55, 0.88, 'selector\n' + r'$Q_0(t)$'),
    (2.35, 3.75, 1.55, 0.88, 'reheaton\n' + r'$R_0$'),
    (4.35, 3.75, 1.70, 0.88, 'sector bath\n' + r'$H_k,\,q_k,\,g_k$'),
    (6.55, 3.75, 1.85, 0.88, 'statistical state\n' + r'$\rho_k,\,n_k$'),
    (8.90, 3.75, 1.55, 0.88, 'threshold\n' + r'$\Psi_k$'),
    (11.00, 3.75, 1.15, 0.88, 'ratio mode\n' + r'$a$'),
    (1.10, 1.18, 3.15, 0.98, r'$Q$--$R$ and $R$--$H$ skeletons' + '\n(no $a$ dependence)'),
    (8.10, 1.18, 3.45, 0.98, 'only two-loop $a$ skeleton\n' + r'$\Psi_k$--gluon exchange'),
]

for x, y, w, h, label in nodes:
    patch = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.045', linewidth=1.35, fill=False)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, label, ha='center', va='center', fontsize=10.7)


def arrow(x1, y1, x2, y2, label=None, label_y=0.0, linestyle='-'):
    patch = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                            mutation_scale=13, linewidth=1.35, linestyle=linestyle)
    ax.add_patch(patch)
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + label_y, label,
                ha='center', va='center', fontsize=8.8)

midy = 4.19
arrow(1.90, midy, 2.35, midy, r'$Q^2R^2$', -0.25)
arrow(3.90, midy, 4.35, midy, r'$RH^\dagger H$', -0.25)
arrow(6.05, midy, 6.55, midy, 'decay /\nthermalisation', 0.34)
arrow(8.40, midy, 8.90, midy, 'state-dressed\npropagators', 0.34)
arrow(10.45, midy, 11.00, midy, r'$M_k(a)$', -0.25)

arrow(3.12, 3.75, 2.65, 2.16, linestyle='--')
arrow(5.20, 3.75, 3.45, 2.16, linestyle='--')
arrow(9.68, 3.75, 9.45, 2.16, linestyle='--')
arrow(11.58, 3.75, 10.55, 2.16, linestyle='--')

ax.text(
    6.30, 2.78,
    r'No connected two-loop 1PI graph contains both $Q_0$ and $a$' +
    '\nin the displayed v0.9 interaction graph.',
    ha='center', va='center', fontsize=12.0,
    bbox=dict(boxstyle='round,pad=0.32', fill=False, linewidth=1.35),
)

ax.text(
    6.30, 0.42,
    r'The selector reaches the $a$ sector through the density matrix and occupations, not through a hard late-vacuum vertex.',
    ha='center', va='center', fontsize=10.7,
)

plt.tight_layout()
plt.savefig(out, dpi=200, bbox_inches='tight')
print(out)
