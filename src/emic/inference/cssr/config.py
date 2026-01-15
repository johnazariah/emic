"""CSSR configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CSSRConfig:
    """
    Configuration for the CSSR algorithm.

    Attributes:
        max_history: Maximum history length L to consider
        significance: Significance level for statistical tests (lower = fewer states)
        min_count: Minimum observations for a history to be considered
        test: Statistical test type ("chi2", "ks", "g")
        max_iterations: Maximum iterations for convergence
        post_merge: Enable post-convergence state merging for minimality
        merge_significance: Significance for post-merge (None = use significance)

    Examples:
        >>> config = CSSRConfig(max_history=5, significance=0.01)
        >>> config.max_history
        5
    """

    max_history: int
    significance: float = 0.05
    min_count: int = 5
    test: str = "chi2"
    max_iterations: int = 1000
    post_merge: bool = True
    merge_significance: float | None = None

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.max_history < 1:
            msg = f"max_history must be >= 1, got {self.max_history}"
            raise ValueError(msg)
        if not (0 < self.significance < 1):
            msg = f"significance must be in (0, 1), got {self.significance}"
            raise ValueError(msg)
        if self.min_count < 1:
            msg = f"min_count must be >= 1, got {self.min_count}"
            raise ValueError(msg)
        if self.test not in ("chi2", "ks", "g"):
            msg = f"test must be 'chi2', 'ks', or 'g', got {self.test}"
            raise ValueError(msg)
        if self.merge_significance is not None and not (0 < self.merge_significance < 1):
            msg = f"merge_significance must be in (0, 1), got {self.merge_significance}"
            raise ValueError(msg)
