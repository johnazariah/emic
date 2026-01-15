"""Skip first N symbols transform."""

from __future__ import annotations

from collections.abc import Hashable, Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from emic.sources.protocol import SequenceSource

A = TypeVar("A", bound=Hashable)


@dataclass(frozen=True)
class SkipN(Generic[A]):
    """
    Skip the first N symbols (burn-in period).

    Useful for allowing a process to reach stationarity
    before collecting data.

    Parameters:
        n: Number of symbols to skip

    Examples:
        >>> from emic.sources import GoldenMeanSource, SkipN, TakeN
        >>> source = GoldenMeanSource(p=0.5, _seed=42)
        >>> # Skip first 1000 symbols, then take 100
        >>> skipped = SkipN[int](1000)(source)
        >>> data = TakeN[int](100)(skipped)
    """

    n: int

    def __call__(self, source: SequenceSource[A]) -> _SkippedSource[A]:
        """
        Apply the transform to a source.

        Args:
            source: The source to skip symbols from.

        Returns:
            A new source that skips the first n symbols.
        """
        return _SkippedSource(source, self.n)


@dataclass
class _SkippedSource(Generic[A]):
    """Internal wrapper that skips initial symbols."""

    _source: SequenceSource[A]
    _skip: int

    @property
    def alphabet(self) -> frozenset[A]:
        """The alphabet of the underlying source."""
        return self._source.alphabet

    def __iter__(self) -> Iterator[A]:
        """Iterate, skipping the first n symbols."""
        it = iter(self._source)
        for _ in range(self._skip):
            try:
                next(it)
            except StopIteration:
                return
        yield from it

    def __rshift__(self, transform: object) -> object:
        """Pipeline operator for composing with transforms."""
        if callable(transform):
            return transform(self)
        return NotImplemented
