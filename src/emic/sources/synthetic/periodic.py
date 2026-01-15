"""Periodic (deterministic) source."""

from __future__ import annotations

from collections.abc import Hashable, Iterator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)


@dataclass
class PeriodicSource(Generic[A]):
    """
    A deterministic periodic process.

    Repeats a fixed pattern indefinitely.
    The epsilon-machine has N states (one per position in pattern).

    Parameters:
        pattern: The repeating sequence of symbols

    Statistical properties:
        - Entropy rate: h = 0 (deterministic)
        - Statistical complexity: C_μ = log(N) where N = len(pattern)

    Examples:
        >>> source = PeriodicSource(pattern=(0, 1, 0))
        >>> symbols = [next(iter(source)) for _ in range(9)]
        >>> symbols
        [0, 1, 0, 0, 1, 0, 0, 1, 0]
    """

    pattern: tuple[A, ...]
    _alphabet: frozenset[A] = field(init=False)

    def __post_init__(self) -> None:
        """Validate pattern and set alphabet."""
        if len(self.pattern) == 0:
            msg = "Pattern must be non-empty"
            raise ValueError(msg)
        object.__setattr__(self, "_alphabet", frozenset(self.pattern))

    @property
    def alphabet(self) -> frozenset[A]:
        """The set of symbols in the pattern."""
        return self._alphabet

    def __iter__(self) -> Iterator[A]:
        """
        Generate symbols by repeating the pattern.

        Yields:
            Symbols from the pattern, cycling indefinitely.
        """
        i = 0
        n = len(self.pattern)
        while True:
            yield self.pattern[i]
            i = (i + 1) % n

    def __rshift__(self, transform: object) -> object:
        """Pipeline operator for composing with transforms."""
        if callable(transform):
            return transform(self)
        return NotImplemented

    @property
    def true_machine(self) -> EpsilonMachine[A]:
        """
        Return the known epsilon-machine for this process.

        A periodic process with period N has exactly N causal states,
        arranged in a cycle.

        Returns:
            The epsilon-machine that generates this process.
        """
        from emic.types import EpsilonMachineBuilder

        n = len(self.pattern)
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder[A]()

        for i, symbol in enumerate(self.pattern):
            current_state = f"S{i}"
            next_state = f"S{(i + 1) % n}"
            builder.add_transition(current_state, symbol, next_state, 1.0)

        # Uniform stationary distribution (each state visited equally)
        stationary = {f"S{i}": 1.0 / n for i in range(n)}

        return builder.with_start_state("S0").with_stationary_distribution(stationary).build()
