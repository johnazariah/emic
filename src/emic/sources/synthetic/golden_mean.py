"""Golden Mean Process source."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from emic.sources.base import StochasticSource

if TYPE_CHECKING:
    from collections.abc import Iterator

    from emic.types import EpsilonMachine


@dataclass
class GoldenMeanSource(StochasticSource[int]):
    """
    The Golden Mean Process.

    A binary process where consecutive 1s are forbidden.
    After emitting a 1, the next symbol must be 0.

    State machine:
        A --0 (p)--> A
        A --1 (1-p)--> B
        B --0 (1.0)--> A

    Parameters:
        p: Probability of emitting 0 from state A (default: 0.5)

    Statistical properties:
        - Entropy rate: h = (2/3) * H(p) where H is binary entropy
        - Statistical complexity: C_μ ≈ 0.918 bits for p=0.5

    Examples:
        >>> source = GoldenMeanSource(p=0.5, _seed=42)
        >>> symbols = list(next(iter(source)) for _ in range(10))
        >>> # No consecutive 1s in output
        >>> '11' not in ''.join(map(str, symbols))
        True
    """

    p: float = 0.5
    _alphabet: frozenset[int] = field(default_factory=lambda: frozenset({0, 1}))

    def __post_init__(self) -> None:
        """Validate parameters and initialize RNG."""
        super().__post_init__()
        if not (0 < self.p < 1):
            msg = f"p must be in (0, 1), got {self.p}"
            raise ValueError(msg)

    def __iter__(self) -> Iterator[int]:
        """
        Generate symbols from the Golden Mean process.

        Yields:
            Symbols from {0, 1} with no consecutive 1s.
        """
        state = "A"
        while True:
            if state == "A":
                if self._rng.random() < self.p:
                    yield 0
                    state = "A"
                else:
                    yield 1
                    state = "B"
            else:  # state == 'B'
                yield 0
                state = "A"

    def with_seed(self, seed: int) -> GoldenMeanSource:
        """
        Return a new source with the given seed.

        Args:
            seed: The random seed to use.

        Returns:
            A new GoldenMeanSource with the given seed.
        """
        return GoldenMeanSource(p=self.p, _seed=seed)

    @property
    def true_machine(self) -> EpsilonMachine[int]:
        """
        Return the known epsilon-machine for this process.

        The Golden Mean process has exactly 2 causal states.

        Returns:
            The epsilon-machine that generates this process.
        """
        from emic.types import EpsilonMachineBuilder

        # Stationary distribution: π_A = 1/(2-p), π_B = (1-p)/(2-p)
        # For p=0.5: π_A = 2/3, π_B = 1/3
        pi_a = 1.0 / (2.0 - self.p)
        pi_b = (1.0 - self.p) / (2.0 - self.p)

        return (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", self.p)
            .add_transition("A", 1, "B", 1.0 - self.p)
            .add_transition("B", 0, "A", 1.0)
            .with_start_state("A")
            .with_stationary_distribution({"A": pi_a, "B": pi_b})
            .build()
        )
