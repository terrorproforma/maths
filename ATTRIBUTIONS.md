# Attributions

This repository builds on two pieces of third-party work. Neither is claimed as the
repository owner's contribution; both are foundations that the owner's results extend.
Cite them wherever the derived material appears.

## 1. The Dinitz–Garg–Goemans / Goemans cost-conjecture counterexample

- **Who:** Dmitry Rybin, working with GPT-5.6 Pro.
- **What:** the seven-vertex, nine-arc planar instance with fractional cost 58 where every
  unsplittable routing within the additive max-demand bound costs at least 60 — including
  the exhaustive eight-routing certificate. The parametric family, positive-cost variant,
  Morell–Skutella corollaries, and the 9/8 planar bound in this repository are direct
  developments of that instance.
- **Announcement (X):**
  - <https://x.com/DmitryRybin1/status/2079904005652893709> (main announcement, with the
    public ChatGPT share log)
  - <https://x.com/DmitryRybin1/status/2079907499545919968> (context thread)
- **Note:** the AI conversation continued in this repository is the shared continuation of
  Rybin's original session.

## 2. The three-dimensional Jacobian-conjecture counterexample map

- **Who:** Levent Alpöge (Harvard), with the problem suggested by Akhil Mathew and the map
  found with Anthropic's Claude Fable 5.
- **What:** the polynomial map
  `((1+xy)^3 z + y^2(1+xy)(4+3xy), y + 3x(1+xy)^2 z + 3xy^2(4+3xy), 2x − 3x^2y − x^3z)`
  from C³ to C³ with Jacobian determinant −2 and a three-point collision. Everything in
  `subtree-shuffling-counterexample/` starts from this map, and the in-conversation
  analyses of it (fiber stratification, gradient/symplectic/Weyl lifts) are derivative of
  it.
- **Announcement (X, 19–20 July 2026):**
  - <https://x.com/__alpoge__/status/2079028340955197566>
- **Secondary write-ups:**
  - Secret Blogging Seminar, *The new counterexample to the Jacobian conjecture*
    (20 July 2026): <https://sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/>
  - Christopher D. Long, *Small Counterexamples to the Gaussian Moments Conjecture*,
    arXiv:2607.18186 (independent verification context).

## How the owner's results relate

- The **machine-dependent weighted-chairman counterexample** (Liu–Reis Conjectures 19/21)
  is the owner's session's construction; it uses the *methodology* popularized by item 1
  (violated-facet / forcing-gadget searches) but no part of Rybin's instance.
- The **subtree-shuffling certificate** ((d,p) = (7,15)) is the owner's session's
  construction built directly on item 2; the starting map and its normalization must always
  be attributed to Alpöge–Mathew–Fable.
