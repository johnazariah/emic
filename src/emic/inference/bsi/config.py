"""BSI configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BSIConfig:
    """
    Configuration for Bayesian Structural Inference.

    BSI uses Bayesian inference to learn epsilon-machines with natural
    uncertainty quantification. It can automatically select the number
    of states via model evidence.

    Attributes:
        max_states: Maximum number of states to consider.
        max_history: Maximum history length for likelihood computation.
        alpha_prior: Dirichlet concentration for transition priors.
            Higher values = more uniform priors.
        n_samples: Number of MCMC samples to draw.
        burnin: Number of burn-in samples to discard.
        thin: Thinning factor (keep every n-th sample).
        seed: Random seed for reproducibility.

    Examples:
        >>> config = BSIConfig(max_states=5, n_samples=500)
        >>> config.max_states
        5
    """

    max_states: int = 10
    max_history: int = 5
    alpha_prior: float = 1.0
    n_samples: int = 1000
    burnin: int = 200
    thin: int = 1
    seed: int | None = None

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.max_states < 1:
            msg = f"max_states must be >= 1, got {self.max_states}"
            raise ValueError(msg)
        if self.max_history < 1:
            msg = f"max_history must be >= 1, got {self.max_history}"
            raise ValueError(msg)
        if self.alpha_prior <= 0:
            msg = f"alpha_prior must be > 0, got {self.alpha_prior}"
            raise ValueError(msg)
        if self.n_samples < 1:
            msg = f"n_samples must be >= 1, got {self.n_samples}"
            raise ValueError(msg)
        if self.burnin < 0:
            msg = f"burnin must be >= 0, got {self.burnin}"
            raise ValueError(msg)
        if self.thin < 1:
            msg = f"thin must be >= 1, got {self.thin}"
            raise ValueError(msg)
