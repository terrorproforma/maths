"""ANANKE: representation-invariant process extraction under exact and finite data."""

from .bootstrap import (
    EigenmodeBootstrapResult,
    SingularValueBootstrapResult,
    bootstrap_hankel_singular_values,
    bootstrap_transition_eigenmode,
    select_transition_eigenvalue,
)
from .diophantine import (
    RationalApproximant,
    approximation_record_sequence,
    continued_fraction,
    convergents,
    nearest_root_of_unity,
)
from .examples import classical_cycle_process, qubit_rotation_process
from .hankel import HankelData, SpectralExtraction, build_hankel, extract_minimal_process
from .invariants import process_fingerprint
from .karpelevich import (
    BoundaryDistanceResult,
    FiniteStateExclusionReport,
    boundary_points,
    distance_to_karpelevich_region,
    dmitriev_dynkin_wedge_distance,
    exclude_finite_stochastic_orders,
    farey_sequence,
    karpelevich_boundary_radius,
    karpelevich_contains,
)
from .observations import (
    PredictiveScore,
    ShotDataset,
    binomial_cross_entropy,
    build_empirical_hankel,
    score_process_on_dataset,
    simulate_shot_dataset,
    simulate_words_upto,
)
from .obstructions import (
    finite_classical_channel_obstruction_from_rational_angles,
    peripheral_phase_report,
)
from .process import LinearProcess
from .rank_selection import (
    RankCandidate,
    RankSelectionResult,
    RankStabilityResult,
    bootstrap_rank_stability,
    select_hankel_rank,
)
from .words import words_upto

__all__ = [
    "BoundaryDistanceResult",
    "EigenmodeBootstrapResult",
    "FiniteStateExclusionReport",
    "HankelData",
    "LinearProcess",
    "PredictiveScore",
    "RationalApproximant",
    "RankCandidate",
    "RankSelectionResult",
    "RankStabilityResult",
    "ShotDataset",
    "SingularValueBootstrapResult",
    "SpectralExtraction",
    "approximation_record_sequence",
    "binomial_cross_entropy",
    "bootstrap_hankel_singular_values",
    "bootstrap_rank_stability",
    "bootstrap_transition_eigenmode",
    "boundary_points",
    "build_empirical_hankel",
    "build_hankel",
    "classical_cycle_process",
    "continued_fraction",
    "convergents",
    "distance_to_karpelevich_region",
    "dmitriev_dynkin_wedge_distance",
    "exclude_finite_stochastic_orders",
    "extract_minimal_process",
    "farey_sequence",
    "finite_classical_channel_obstruction_from_rational_angles",
    "karpelevich_boundary_radius",
    "karpelevich_contains",
    "nearest_root_of_unity",
    "peripheral_phase_report",
    "process_fingerprint",
    "qubit_rotation_process",
    "score_process_on_dataset",
    "select_hankel_rank",
    "select_transition_eigenvalue",
    "simulate_shot_dataset",
    "simulate_words_upto",
    "words_upto",
]
