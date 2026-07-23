from shuffle_counterexample.certificates import (
    alpha_vector,
    first_fully_covered_k,
    gamma,
    separator_total,
    truncated_inverse_coefficient,
)


def test_lagrange_coefficients() -> None:
    assert truncated_inverse_coefficient(5) == {m: gamma(m) for m in range(6)}


def test_leaf_vector_and_nonzero_total() -> None:
    for m in range(1, 7):
        alpha = alpha_vector(m)
        assert len(alpha) == 15
        assert sum(alpha) == 18 * m + 1
        assert separator_total(m) != 0


def test_fully_covered_threshold() -> None:
    assert first_fully_covered_k(7, 15) == 113_037_178_809
    assert first_fully_covered_k(7, 15) % 3 == 0
