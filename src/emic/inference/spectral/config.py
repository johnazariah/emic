"""Spectral Learning configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SpectralConfig:
    """
    Configuration for the Spectral Learning algorithm.

    Spectral learning uses SVD/eigendecomposition of Hankel matrices
    to learn observable operator representations, then extracts the
    epsilon-machine.

    Attributes:
        max_history: Maximum history length for Hankel matrix rows/columns.
        rank_threshold: Singular value threshold for rank selection.
            Singular values below max_sv * threshold are discarded.
        rank: Fixed rank (overrides threshold if set).
        regularization: Regularization for numerical stability.
        min_count: Minimum observations for a history to be included.

    Examples:
        >>> config = SpectralConfig(max_history=5, rank_threshold=0.01)
        >>> config.max_history
        5
    """

    max_history: int = 10
    rank_threshold: float = 0.01
    rank: int | None = None
    regularization: float = 1e-6
    min_count: int = 5

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.max_history < 1:
            msg = f"max_history must be >= 1, got {self.max_history}"
            raise ValueError(msg)
        if self.rank_threshold <= 0 or self.rank_threshold >= 1:
            msg = f"rank_threshold must be in (0, 1), got {self.rank_threshold}"
            raise ValueError(msg)
        if self.rank is not None and self.rank < 1:
            msg = f"rank must be >= 1, got {self.rank}"
            raise ValueError(msg)
        if self.regularization < 0:
            msg = f"regularization must be >= 0, got {self.regularization}"
            raise ValueError(msg)
        if self.min_count < 1:
            msg = f"min_count must be >= 1, got {self.min_count}"
            raise ValueError(msg)
