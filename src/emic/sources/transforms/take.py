"""Take first N symbols transform."""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from itertools import islice
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from emic.sources.protocol import SequenceSource

from emic.sources.empirical import SequenceData

A = TypeVar("A", bound=Hashable)


@dataclass(frozen=True)
class TakeN(Generic[A]):
    """
    Take the first N symbols from a source.

    Converts an infinite source into a finite SequenceData.
    Useful for sampling from stochastic sources.

    Parameters:
        n: Number of symbols to take

    Examples:
        >>> from emic.sources import GoldenMeanSource, TakeN
        >>> source = GoldenMeanSource(p=0.5, _seed=42)
        >>> data = TakeN[int](100)(source)
        >>> len(data)
        100
        >>> isinstance(data, SequenceData)
        True
    """

    n: int

    def __call__(self, source: SequenceSource[A]) -> SequenceData[A]:
        """
        Apply the transform to a source.

        Args:
            source: The source to take symbols from.

        Returns:
            A SequenceData containing the first n symbols.
        """
        symbols = tuple(islice(source, self.n))
        return SequenceData(symbols, _alphabet=source.alphabet)
