"""Base class for stochastic sources."""

from __future__ import annotations

import random
from collections.abc import Hashable, Iterator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from typing import Self

A = TypeVar("A", bound=Hashable)


def _empty_frozenset() -> frozenset[Hashable]:
    """Factory for empty frozenset with proper typing."""
    return frozenset()


@dataclass
class StochasticSource(Generic[A]):
    """
    Base class for stochastic process sources.

    Handles random state management and provides common functionality.
    Not frozen because it maintains RNG state.

    Subclasses should:
    1. Set _alphabet in __post_init__
    2. Implement __iter__ to yield symbols
    3. Implement with_seed to return a properly typed copy

    Attributes:
        _alphabet: The set of possible symbols
        _seed: The random seed (None for unseeded)
        _rng: The random number generator

    Examples:
        >>> class MyStohasticSource(StochasticSource[int]):
        ...     def __post_init__(self):
        ...         super().__post_init__()
        ...         object.__setattr__(self, '_alphabet', frozenset({0, 1}))
        ...     def __iter__(self):
        ...         while True:
        ...             yield self._rng.choice([0, 1])
    """

    _alphabet: frozenset[A] = field(default_factory=_empty_frozenset)  # type: ignore[assignment]
    _seed: int | None = None
    _rng: random.Random = field(default_factory=random.Random, repr=False)

    def __post_init__(self) -> None:
        """Initialize RNG with seed if provided."""
        if self._seed is not None:
            self._rng.seed(self._seed)

    @property
    def alphabet(self) -> frozenset[A]:
        """The set of possible symbols."""
        return self._alphabet

    @property
    def seed(self) -> int | None:
        """The random seed, if set."""
        return self._seed

    def with_seed(self, seed: int) -> Self:
        """
        Return a new source with the given seed.

        Subclasses should override to return the correct type.

        Args:
            seed: The random seed to use.

        Returns:
            A new source instance with the given seed.
        """
        raise NotImplementedError("Subclasses must implement with_seed")

    def __iter__(self) -> Iterator[A]:
        """
        Yield symbols from the source.

        Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement __iter__")

    def __rshift__(self, transform: object) -> object:
        """
        Pipeline operator for composing sources with transforms.

        Usage:
            source >> TakeN(1000) >> CSSR()

        Args:
            transform: A callable that accepts this source.

        Returns:
            The result of applying the transform to this source.
        """
        if callable(transform):
            return transform(self)
        return NotImplemented
