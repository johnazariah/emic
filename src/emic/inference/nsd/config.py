"""NSD configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NSDConfig:
    """
    Configuration for Neural State Discovery.

    NSD learns state representations using a neural network approach.
    This is a simplified implementation that uses clustering on learned
    embeddings rather than full neural network training.

    Attributes:
        max_states: Maximum number of states to discover.
        history_length: Length of history window for state embedding.
        embedding_dim: Dimensionality of state embeddings.
        n_iterations: Number of clustering iterations.
        convergence_threshold: Threshold for convergence detection.
        seed: Random seed for reproducibility.

    Examples:
        >>> config = NSDConfig(max_states=5, history_length=10)
        >>> config.history_length
        10
    """

    max_states: int = 10
    history_length: int = 10
    embedding_dim: int = 16
    n_iterations: int = 100
    convergence_threshold: float = 1e-4
    seed: int | None = None

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.max_states < 1:
            msg = f"max_states must be >= 1, got {self.max_states}"
            raise ValueError(msg)
        if self.history_length < 1:
            msg = f"history_length must be >= 1, got {self.history_length}"
            raise ValueError(msg)
        if self.embedding_dim < 1:
            msg = f"embedding_dim must be >= 1, got {self.embedding_dim}"
            raise ValueError(msg)
        if self.n_iterations < 1:
            msg = f"n_iterations must be >= 1, got {self.n_iterations}"
            raise ValueError(msg)
        if self.convergence_threshold <= 0:
            msg = f"convergence_threshold must be > 0, got {self.convergence_threshold}"
            raise ValueError(msg)
