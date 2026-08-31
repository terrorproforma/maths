#!/usr/bin/env python3
"""Exact multigraded Molien--Weyl count for the TP-03 PS1 scalar sector.

Fields (all treated as independent complex scalar multiplets):
    Phi1    ~ (1,  2, 2)
    Phi15   ~ (15, 2, 2)
    DeltaR  ~ (10, 1, 3)

The conjugate variables are counted separately.  For each multidegree the
script computes the multiplicity of the trivial representation in the
product of the appropriate symmetric powers.  Weyl integration is performed
as an integer constant-term calculation, so the reported counts are exact.

No derivative operators occur in a renormalisable scalar potential, hence
there are no integration-by-parts redundancies.  Character integration also
quotients all representation/trace identities automatically.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
from math import comb, factorial
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, Sequence, Tuple

Weight = Tuple[int, int, int, int, int]
Poly = Dict[Weight, int]
ZERO: Weight = (0, 0, 0, 0, 0)
FIELD_NAMES = (
    "Phi1",
    "Phi1_dag",
    "Phi15",
    "Phi15_dag",
    "DeltaR",
    "DeltaR_dag",
)


def add_weight(a: Weight, b: Weight) -> Weight:
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]


def scale_weight(a: Weight, n: int) -> Weight:
    return tuple(n * x for x in a)  # type: ignore[return-value]


def multiply_poly(left: Mapping[Weight, int], right: Mapping[Weight, int]) -> Poly:
    out: defaultdict[Weight, int] = defaultdict(int)
    for wa, ca in left.items():
        for wb, cb in right.items():
            out[add_weight(wa, wb)] += ca * cb
    return dict(out)


def embed(su4: Tuple[int, int, int] = (0, 0, 0), su2l: int = 0, su2r: int = 0) -> Weight:
    return su4 + (su2l, su2r)


# SU(4) maximal-torus variables z1,z2,z3 with z4=(z1 z2 z3)^(-1).
SU4_FUND = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, -1, -1),
)


def negate3(weight: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return tuple(-x for x in weight)  # type: ignore[return-value]


SU4_ADJ: List[Tuple[int, int, int]] = []
for i, wi in enumerate(SU4_FUND):
    for j, wj in enumerate(SU4_FUND):
        if i != j:
            SU4_ADJ.append(tuple(wi[k] - wj[k] for k in range(3)))
SU4_ADJ.extend([(0, 0, 0)] * 3)

SU4_10: List[Tuple[int, int, int]] = []
for i in range(4):
    for j in range(i, 4):
        SU4_10.append(tuple(SU4_FUND[i][k] + SU4_FUND[j][k] for k in range(3)))
SU4_10_BAR = [negate3(weight) for weight in SU4_10]

PHI1_WEIGHTS = [embed((0, 0, 0), l, r) for l in (1, -1) for r in (1, -1)]
PHI15_WEIGHTS = [embed(weight, l, r) for weight in SU4_ADJ for l in (1, -1) for r in (1, -1)]
DELTAR_WEIGHTS = [embed(weight, 0, r) for weight in SU4_10 for r in (2, 0, -2)]
DELTAR_DAG_WEIGHTS = [embed(weight, 0, r) for weight in SU4_10_BAR for r in (2, 0, -2)]

FIELD_WEIGHTS: Mapping[str, Sequence[Weight]] = {
    "Phi1": PHI1_WEIGHTS,
    "Phi1_dag": PHI1_WEIGHTS,       # (1,2,2) is a real representation, field remains complex.
    "Phi15": PHI15_WEIGHTS,
    "Phi15_dag": PHI15_WEIGHTS,     # (15,2,2) is a real representation, field remains complex.
    "DeltaR": DELTAR_WEIGHTS,
    "DeltaR_dag": DELTAR_DAG_WEIGHTS,
}


def symmetric_power_character(weights: Sequence[Weight], degree: int) -> Poly:
    """Character of Sym^degree(R), retaining exact integer multiplicities."""
    multiplicities = Counter(weights)
    dp: List[Poly] = [{} for _ in range(degree + 1)]
    dp[0] = {ZERO: 1}

    for weight, multiplicity in multiplicities.items():
        next_dp: List[defaultdict[Weight, int]] = [defaultdict(int) for _ in range(degree + 1)]
        factor_coefficients = [comb(multiplicity + r - 1, r) for r in range(degree + 1)]
        for current_degree in range(degree + 1):
            for current_weight, current_coefficient in dp[current_degree].items():
                for repetitions in range(degree - current_degree + 1):
                    target_degree = current_degree + repetitions
                    target_weight = add_weight(current_weight, scale_weight(weight, repetitions))
                    next_dp[target_degree][target_weight] += (
                        current_coefficient * factor_coefficients[repetitions]
                    )
        dp = [dict(item) for item in next_dp]
    return dp[degree]


def build_weyl_denominator() -> Poly:
    """Return ∏_{all roots}(1-z^alpha) for SU(4)xSU(2)xSU(2)."""
    factors: List[Weight] = []
    for i, wi in enumerate(SU4_FUND):
        for j, wj in enumerate(SU4_FUND):
            if i != j:
                factors.append(embed(tuple(wi[k] - wj[k] for k in range(3))))
    factors.extend(
        [
            embed((0, 0, 0), 2, 0),
            embed((0, 0, 0), -2, 0),
            embed((0, 0, 0), 0, 2),
            embed((0, 0, 0), 0, -2),
        ]
    )

    polynomial: Poly = {ZERO: 1}
    for root in factors:
        polynomial = multiply_poly(polynomial, {ZERO: 1, root: -1})
    return polynomial


WEYL_DENOMINATOR = build_weyl_denominator()
WEYL_GROUP_ORDER = factorial(4) * 2 * 2


def singlet_multiplicity(character: Mapping[Weight, int]) -> int:
    numerator = sum(
        coefficient
        * WEYL_DENOMINATOR.get(tuple(-x for x in weight), 0)
        for weight, coefficient in character.items()
    )
    if numerator % WEYL_GROUP_ORDER != 0:
        raise ArithmeticError(
            f"Weyl constant term {numerator} is not divisible by {WEYL_GROUP_ORDER}"
        )
    return numerator // WEYL_GROUP_ORDER


def compositions(total: int, parts: int) -> Iterator[Tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for remainder in compositions(total - first, parts - 1):
            yield (first,) + remainder


SYMMETRIC_CHARACTERS: Dict[str, Dict[int, Poly]] = {}
for field_name, weights in FIELD_WEIGHTS.items():
    SYMMETRIC_CHARACTERS[field_name] = {0: {ZERO: 1}}
    for degree in range(1, 5):
        SYMMETRIC_CHARACTERS[field_name][degree] = symmetric_power_character(weights, degree)


@lru_cache(maxsize=None)
def monomial_character(exponents: Tuple[int, ...]) -> Poly:
    factors = [
        SYMMETRIC_CHARACTERS[field_name][exponent]
        for field_name, exponent in zip(FIELD_NAMES, exponents)
        if exponent
    ]
    factors.sort(key=len)
    result: Poly = {ZERO: 1}
    for factor in factors:
        result = multiply_poly(result, factor)
    return result


def conjugate_multidegree(exponents: Tuple[int, ...]) -> Tuple[int, ...]:
    return (
        exponents[1],
        exponents[0],
        exponents[3],
        exponents[2],
        exponents[5],
        exponents[4],
    )


def multidegree_label(exponents: Tuple[int, ...]) -> str:
    pieces = [
        f"{field}^{power}"
        for field, power in zip(FIELD_NAMES, exponents)
        if power
    ]
    return " ".join(pieces) if pieces else "1"


def compute_counts() -> Dict[str, object]:
    rows: List[Dict[str, object]] = []
    totals: Dict[int, int] = {}

    for total_degree in (2, 3, 4):
        total_multiplicity = 0
        for exponents in compositions(total_degree, len(FIELD_NAMES)):
            multiplicity = singlet_multiplicity(monomial_character(exponents))
            if multiplicity == 0:
                continue
            total_multiplicity += multiplicity
            conjugate = conjugate_multidegree(exponents)
            rows.append(
                {
                    "total_degree": total_degree,
                    "multidegree": list(exponents),
                    "label": multidegree_label(exponents),
                    "singlet_multiplicity": multiplicity,
                    "self_conjugate_multidegree": exponents == conjugate,
                    "conjugate_multidegree": list(conjugate),
                }
            )
        totals[total_degree] = total_multiplicity

    expected = {2: 7, 3: 0, 4: 131}
    checks = {
        "weyl_denominator_constant_term": WEYL_DENOMINATOR.get(ZERO),
        "weyl_group_order": WEYL_GROUP_ORDER,
        "quadratic_real_parameters": totals[2],
        "cubic_real_parameters": totals[3],
        "quartic_real_parameters": totals[4],
        "expected_counts_match": totals == expected,
        "field_complex_dimensions": {
            "Phi1": len(PHI1_WEIGHTS),
            "Phi15": len(PHI15_WEIGHTS),
            "DeltaR": len(DELTAR_WEIGHTS),
        },
        "total_real_scalar_components": 2
        * (len(PHI1_WEIGHTS) + len(PHI15_WEIGHTS) + len(DELTAR_WEIGHTS)),
    }

    return {
        "schema_version": "1.0.0",
        "group": "SU(4)_C x SU(2)_L x SU(2)_R",
        "field_order": list(FIELD_NAMES),
        "reality_convention": (
            "Phi1, Phi15 and DeltaR are independent complex scalar multiplets; "
            "conjugate polynomial variables are counted separately."
        ),
        "method": "exact multigraded Molien-Weyl constant-term calculation",
        "rows": rows,
        "totals": {
            "quadratic": totals[2],
            "cubic": totals[3],
            "quartic": totals[4],
            "all_renormalisable_scalar_parameters": totals[2] + totals[3] + totals[4],
        },
        "checks": checks,
    }


def write_outputs(root: Path, result: Mapping[str, object]) -> None:
    results_dir = root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    json_path = results_dir / "scalar_invariant_count.json"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    csv_path = root / "invariant_basis_multidegrees.csv"
    rows = result["rows"]
    assert isinstance(rows, list)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "total_degree",
                *FIELD_NAMES,
                "singlet_multiplicity",
                "self_conjugate_multidegree",
                "label",
            ]
        )
        for row in rows:
            assert isinstance(row, dict)
            multidegree = row["multidegree"]
            assert isinstance(multidegree, list)
            writer.writerow(
                [
                    row["total_degree"],
                    *multidegree,
                    row["singlet_multiplicity"],
                    str(row["self_conjugate_multidegree"]).lower(),
                    row["label"],
                ]
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="TP-03 project root",
    )
    args = parser.parse_args()
    result = compute_counts()
    write_outputs(args.root.resolve(), result)
    print(json.dumps(result["totals"], indent=2))
    if not result["checks"]["expected_counts_match"]:  # type: ignore[index]
        raise SystemExit(1)


if __name__ == "__main__":
    main()
