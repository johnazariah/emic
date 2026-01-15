"""Finite sequence data wrapper."""

from __future__ import annotations

from collections.abc import Hashable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

A = TypeVar("A", bound=Hashable)


@dataclass(frozen=True)
class SequenceData(Generic[A]):
    """
    A finite sequence of observed symbols.

    Wraps empirical data for use in inference pipelines.
    Immutable to ensure data integrity.

    Parameters:
        symbols: The sequence of observed symbols
        _alphabet: Optional explicit alphabet (inferred from symbols if None)

    Examples:
        >>> data = SequenceData(symbols=(0, 1, 0, 1, 0))
        >>> list(data)
        [0, 1, 0, 1, 0]
        >>> len(data)
        5
        >>> data.alphabet
        frozenset({0, 1})
    """

    symbols: tuple[A, ...]
    _alphabet: frozenset[A] | None = None

    def __iter__(self) -> Iterator[A]:
        """Iterate over symbols."""
        return iter(self.symbols)

    def __len__(self) -> int:
        """Number of symbols."""
        return len(self.symbols)

    @property
    def alphabet(self) -> frozenset[A]:
        """
        The set of possible symbols.

        If an explicit alphabet was provided, returns that.
        Otherwise, returns the set of symbols observed in the data.
        """
        if self._alphabet is not None:
            return self._alphabet
        return frozenset(self.symbols)

    def __rshift__(self, transform: object) -> object:
        """Pipeline operator for composing with transforms."""
        if callable(transform):
            return transform(self)
        return NotImplemented

    @staticmethod
    def from_string(s: str) -> SequenceData[str]:
        """
        Create from a string (each character is a symbol).

        Args:
            s: A string where each character is treated as a symbol.

        Returns:
            A SequenceData containing the characters.

        Examples:
            >>> data = SequenceData.from_string("AABBA")
            >>> list(data)
            ['A', 'A', 'B', 'B', 'A']
        """
        return SequenceData(tuple(s))

    @staticmethod
    def from_binary_string(s: str) -> SequenceData[int]:
        """
        Create from a binary string like "01010".

        Args:
            s: A string of '0' and '1' characters.

        Returns:
            A SequenceData containing integers 0 and 1.

        Raises:
            ValueError: If string contains non-binary characters.

        Examples:
            >>> data = SequenceData.from_binary_string("01010")
            >>> list(data)
            [0, 1, 0, 1, 0]
        """
        for c in s:
            if c not in ("0", "1"):
                msg = f"Expected binary string, got character '{c}'"
                raise ValueError(msg)
        return SequenceData(tuple(int(c) for c in s), _alphabet=frozenset({0, 1}))
