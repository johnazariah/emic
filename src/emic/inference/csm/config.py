"""CSM configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DistanceMetric = Literal["kl", "hellinger", "tv", "chi2"]


@dataclass(frozen=True)
class CSMConfig:
    """
    Configuration for the Causal State Merging (CSM) algorithm.

    CSM is a bottom-up approach to epsilon-machine inference. Unlike CSSR,
    which splits states, CSM starts with the finest possible partition
    (each unique history of length L is a state) and merges states based
    on predictive equivalence.

    Attributes:
        history_length: Fixed history length for initial partition. All unique
            histories of this length become initial states.
        merge_threshold: Distance threshold for merging. Two states are merged
            if their predictive distributions are closer than this threshold.
            Lower values = more states, higher values = fewer states.
        distance_metric: Metric for comparing predictive distributions.
            - 'kl': Kullback-Leibler divergence (asymmetric)
            - 'hellinger': Hellinger distance (symmetric)
            - 'tv': Total variation distance (symmetric)
            - 'chi2': Chi-squared distance (symmetric)
        min_count: Minimum observations required for a history to be considered.
        hierarchical: If True, return the full merge hierarchy (dendrogram).
            Useful for visualization and choosing merge threshold.

    Examples:
        >>> config = CSMConfig(history_length=5, merge_threshold=0.05)
        >>> config.history_length
        5
        >>> config.distance_metric
        'kl'
    """

    history_length: int
    merge_threshold: float = 0.05
    distance_metric: DistanceMetric = "kl"
    min_count: int = 5
    hierarchical: bool = False

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.history_length < 1:
            msg = f"history_length must be >= 1, got {self.history_length}"
            raise ValueError(msg)
        if self.merge_threshold <= 0:
            msg = f"merge_threshold must be > 0, got {self.merge_threshold}"
            raise ValueError(msg)
        if self.distance_metric not in ("kl", "hellinger", "tv", "chi2"):
            msg = f"distance_metric must be 'kl', 'hellinger', 'tv', or 'chi2', got {self.distance_metric}"
            raise ValueError(msg)
        if self.min_count < 1:
            msg = f"min_count must be >= 1, got {self.min_count}"
            raise ValueError(msg)
