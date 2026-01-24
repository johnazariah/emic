"""Spectral Learning configuration."""

from __future__ import annotations

import math
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
            If None (default), automatically adapts based on sample size
            and alphabet size. Larger values capture longer-range correlations
            but require more data to estimate reliably.
        rank_threshold: Relative singular value threshold for rank selection.
            Singular values below max_sv * threshold are discarded.
            Lower values are more conservative (keep fewer singular values),
            which can prevent overfitting but may miss structure.
            Higher values keep more singular values but may include noise.
            If the inferred machine has too many states, try lowering this.
            If it has too few states, try raising it or use explicit `rank`.
        rank: Fixed rank (overrides threshold if set). Use this when you
            know the true number of hidden states.
        regularization: Regularization for numerical stability.
        min_count: Minimum observations for a history to be included.
            If None (default), automatically adapts based on sample size.

    Examples:
        >>> # Default configuration (adaptive)
        >>> config = SpectralConfig()
        >>> config.max_history is None  # Will be set adaptively
        True

        >>> # Fixed history length for large data
        >>> config = SpectralConfig(max_history=10)

        >>> # Fixed rank when you know the true model
        >>> config = SpectralConfig(rank=2)
    """

    max_history: int | None = None  # None = adaptive
    rank_threshold: float = 0.001
    rank: int | None = None
    regularization: float = 1e-6
    min_count: int | None = None  # None = adaptive

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.max_history is not None and self.max_history < 1:
            msg = f"max_history must be >= 1 or None, got {self.max_history}"
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
        if self.min_count is not None and self.min_count < 1:
            msg = f"min_count must be >= 1 or None, got {self.min_count}"
            raise ValueError(msg)

    def get_effective_params(self, n_samples: int, alphabet_size: int) -> tuple[int, int]:
        """
        Get effective max_history and min_count for given data size.

        The heuristic is based on ensuring the Hankel matrix is well-populated:
        - We need approximately |Σ|^L unique histories of length L
        - Each history needs min_count occurrences
        - So we need n >= |Σ|^L * min_count * constant

        Args:
            n_samples: Number of samples in the sequence.
            alphabet_size: Size of the alphabet.

        Returns:
            Tuple of (effective_max_history, effective_min_count).
        """
        if self.max_history is not None and self.min_count is not None:
            return (self.max_history, self.min_count)

        # Adaptive heuristic based on sample size and alphabet.
        # We use L = floor(log(n/50) / log(|A|)), giving a history length
        # such that the expected count per cell is at least 50.
        safety_factor = 50

        if alphabet_size < 2:
            alphabet_size = 2  # Avoid log(1) = 0

        if self.max_history is not None:
            effective_max_history = self.max_history
        else:
            # L such that |Σ|^L * safety_factor <= n
            # L <= log(n / safety_factor) / log(|Σ|)
            max_L = math.log(max(1, n_samples / safety_factor)) / math.log(alphabet_size)
            effective_max_history = max(2, min(10, int(max_L)))

        if self.min_count is not None:
            effective_min_count = self.min_count
        else:
            # Adaptive min_count: higher for small data, lower for large
            # Scale roughly as sqrt(n) / 10, capped between 2 and 10
            effective_min_count = max(2, min(10, int(math.sqrt(n_samples) / 10)))

        return (effective_max_history, effective_min_count)
