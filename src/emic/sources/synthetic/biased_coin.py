"""Biased coin (IID) source."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from emic.sources.base import StochasticSource

if TYPE_CHECKING:
    from collections.abc import Iterator

    from emic.types import EpsilonMachine


@dataclass
class BiasedCoinSource(StochasticSource[int]):
    """
    Independent identically distributed binary source.

    The simplest stochastic process: each symbol is independent.
    The epsilon-machine has exactly one state.

    Parameters:
        p: Probability of emitting 1 (default: 0.5)

    Statistical properties:
        - Entropy rate: h = H(p) = -p*log(p) - (1-p)*log(1-p)
        - Statistical complexity: C_μ = 0 (no memory needed)

    Examples:
        >>> source = BiasedCoinSource(p=0.7, _seed=42)
        >>> symbols = [next(iter(source)) for _ in range(1000)]
        >>> # Should be roughly 70% ones
        >>> 0.65 < sum(symbols) / len(symbols) < 0.75
        True
    """

    p: float = 0.5
    _alphabet: frozenset[int] = field(default_factory=lambda: frozenset({0, 1}))

    def __post_init__(self) -> None:
        """Validate parameters and initialize RNG."""
        super().__post_init__()
        if not (0 <= self.p <= 1):
            msg = f"p must be in [0, 1], got {self.p}"
            raise ValueError(msg)

    def __iter__(self) -> Iterator[int]:
        """
        Generate IID symbols.

        Yields:
            Symbols from {0, 1} drawn independently.
        """
        while True:
            yield 1 if self._rng.random() < self.p else 0

    def with_seed(self, seed: int) -> BiasedCoinSource:
        """
        Return a new source with the given seed.

        Args:
            seed: The random seed to use.

        Returns:
            A new BiasedCoinSource with the given seed.
        """
        return BiasedCoinSource(p=self.p, _seed=seed)

    @property
    def true_machine(self) -> EpsilonMachine[int]:
        """
        Return the known epsilon-machine for this process.

        An IID process has exactly 1 causal state.

        Returns:
            The epsilon-machine that generates this process.
        """
        from emic.types import EpsilonMachineBuilder

        return (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", 1.0 - self.p)
            .add_transition("A", 1, "A", self.p)
            .with_start_state("A")
            .with_stationary_distribution({"A": 1.0})
            .build()
        )
