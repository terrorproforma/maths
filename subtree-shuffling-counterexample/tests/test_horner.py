import sympy as sp

from shuffle_counterexample.horner import (
    auxiliary_jacobian,
    build_counterexample_suspension,
    specialized_nilpotency_checks,
    telescoping_residuals,
    verify_counterexample_suspension,
)


def test_weighted_horner_certificate() -> None:
    report = verify_counterexample_suspension()
    assert report["dimension"] == 15
    assert report["degree"] == 7
    assert report["component_degrees"] == [4, 6, 7]
    assert report["collision_count"] == 3


def test_telescoping_and_auxiliary_block() -> None:
    suspension = build_counterexample_suspension()
    assert telescoping_residuals(suspension) == (0, 0, 0)
    assert sp.factor(auxiliary_jacobian(suspension).det()) == 1


def test_specialized_matrix_powers() -> None:
    assert all(specialized_nilpotency_checks().values())
