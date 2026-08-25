#!/usr/bin/env python3
"""Symbolic checks for the crossed-null chronometry research note.

The script verifies:
1. The clock/ruler Gram matrix for two null covectors.
2. The Lorentz-boost action of reciprocal null rescalings.
3. The flat-space standing-wave formulas.
4. The stationary point and positive-definite homogeneous Hessian of the
   proposed scale-locking potential.

Run with:
    python verify_crossed_null_chronometry.py
"""

from __future__ import annotations

import sympy as sp


def verify_null_gram_matrix() -> None:
    """Verify that the average and difference of crossed null covectors
    become orthonormal after the conformal completion h = C g.
    """
    C = sp.symbols("C", positive=True, real=True)

    # We work only with the invariant contractions:
    # k.k = 0, l.l = 0, k.l = -2 C.
    kk = sp.Integer(0)
    ll = sp.Integer(0)
    kl = -2 * C

    tt = sp.simplify((kk + 2 * kl + ll) / 4)
    rr = sp.simplify((kk - 2 * kl + ll) / 4)
    tr = sp.simplify((kk - ll) / 4)

    # h^{-1} = C^{-1} g^{-1}.
    h_tt = sp.simplify(tt / C)
    h_rr = sp.simplify(rr / C)
    h_tr = sp.simplify(tr / C)

    assert h_tt == -1
    assert h_rr == 1
    assert h_tr == 0

    print("[PASS] Crossed-null Gram matrix: diag(-1, +1).")


def verify_reciprocal_rescaling_is_boost() -> None:
    """Verify that k -> exp(eta) k and l -> exp(-eta) l acts as a
    Lorentz boost on dT=(k+l)/2 and dR=(k-l)/2.
    """
    eta = sp.symbols("eta", real=True)
    T, R = sp.symbols("T R")

    # k = T + R and l = T - R at the level of covector components.
    k = T + R
    ell = T - R

    boosted_T = sp.expand((sp.exp(eta) * k + sp.exp(-eta) * ell) / 2)
    boosted_R = sp.expand((sp.exp(eta) * k - sp.exp(-eta) * ell) / 2)

    expected_T = sp.cosh(eta) * T + sp.sinh(eta) * R
    expected_R = sp.sinh(eta) * T + sp.cosh(eta) * R

    assert sp.simplify(boosted_T - expected_T.rewrite(sp.exp)) == 0
    assert sp.simplify(boosted_R - expected_R.rewrite(sp.exp)) == 0

    print("[PASS] Reciprocal null rescaling is a Lorentz boost.")


def verify_flat_space_example() -> None:
    """Verify the flat-space expressions for T, R, and C."""
    omega_bar, eta, t, x = sp.symbols(
        "omega_bar eta t x", positive=True, real=True
    )
    omega_plus = omega_bar * sp.exp(eta)
    omega_minus = omega_bar * sp.exp(-eta)

    phi_plus = omega_plus * (t - x)
    phi_minus = omega_minus * (t + x)

    T = sp.simplify((phi_plus + phi_minus) / 2)
    R = sp.simplify((phi_plus - phi_minus) / 2)

    expected_T = omega_bar * (sp.cosh(eta) * t - sp.sinh(eta) * x)
    expected_R = omega_bar * (sp.sinh(eta) * t - sp.cosh(eta) * x)

    assert sp.simplify(T - expected_T.rewrite(sp.exp)) == 0
    assert sp.simplify(R - expected_R.rewrite(sp.exp)) == 0
    assert sp.simplify(omega_plus * omega_minus - omega_bar**2) == 0

    print("[PASS] Flat-space clock/ruler and geometric-mean scale formulas.")


def verify_locking_potential() -> None:
    """Verify the locked vacuum and homogeneous stability matrix.

    Variables C and Sigma both have mass dimension two, so the Hessian entries
    can be compared directly. Positivity follows from Sylvester's criterion.
    """
    C, Sigma = sp.symbols("C Sigma", positive=True, real=True)
    kappa, beta, Lambda = sp.symbols(
        "kappa beta Lambda", positive=True, real=True
    )

    potential = (
        sp.Rational(1, 2) * kappa * (C - Sigma) ** 2
        + sp.Rational(1, 4)
        * beta
        * Sigma**2
        * (sp.log(Sigma / Lambda**2) - sp.Rational(1, 2))
        + sp.Rational(1, 8) * beta * Lambda**4
    )

    gradient = sp.Matrix(
        [sp.diff(potential, C), sp.diff(potential, Sigma)]
    )
    vacuum_substitution = {C: Lambda**2, Sigma: Lambda**2}
    gradient_at_vacuum = sp.simplify(gradient.subs(vacuum_substitution))

    assert gradient_at_vacuum == sp.zeros(2, 1)

    hessian = sp.hessian(potential, (C, Sigma))
    hessian_at_vacuum = sp.simplify(hessian.subs(vacuum_substitution))
    expected_hessian = sp.Matrix(
        [[kappa, -kappa], [-kappa, kappa + beta / 2]]
    )
    assert sp.simplify(hessian_at_vacuum - expected_hessian) == sp.zeros(2, 2)

    first_principal_minor = hessian_at_vacuum[0, 0]
    determinant = sp.factor(hessian_at_vacuum.det())

    assert first_principal_minor == kappa
    assert determinant == beta * kappa / 2

    print("[PASS] Locked vacuum: C = Sigma = Lambda^2.")
    print("[PASS] Hessian positive for kappa > 0 and beta > 0.")
    print("       Hessian =")
    sp.pprint(hessian_at_vacuum)
    print(f"       det(H) = {determinant}")


def main() -> None:
    verify_null_gram_matrix()
    verify_reciprocal_rescaling_is_boost()
    verify_flat_space_example()
    verify_locking_potential()
    print("\nAll symbolic checks passed.")


if __name__ == "__main__":
    main()
