"""Protocol definitions for sequence sources."""

from collections.abc import Hashable, Iterator
from typing import Protocol, TypeVar

A_co = TypeVar("A_co", bound=Hashable, covariant=True)


class SequenceSource(Protocol[A_co]):
    """
    A source of symbols for epsilon-machine inference.

    Any object that is iterable over symbols and knows its alphabet
    satisfies this protocol.

    Examples:
        >>> class MySource:
        ...     @property
        ...     def alphabet(self) -> frozenset[int]:
        ...         return frozenset({0, 1})
        ...     def __iter__(self):
        ...         yield from [0, 1, 0, 1]
        >>> source: SequenceSource[int] = MySource()
    """

    def __iter__(self) -> Iterator[A_co]:
        """Yield symbols from the source."""
        ...

    @property
    def alphabet(self) -> frozenset[A_co]:
        """The set of possible symbols."""
        ...


class SeededSource(SequenceSource[A_co], Protocol[A_co]):
    """
    A source that can be seeded for reproducibility.

    Extends SequenceSource with seed management for stochastic sources.
    """

    @property
    def seed(self) -> int | None:
        """The random seed, if set."""
        ...

    def with_seed(self, seed: int) -> "SeededSource[A_co]":
        """Return a new source with the given seed."""
        ...
