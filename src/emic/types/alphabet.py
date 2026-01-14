"""Alphabet and Symbol types for epsilon-machines."""

from collections.abc import Hashable, Iterator
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

# Generic symbol type - any hashable value (covariant for use in Protocol)
Symbol_co = TypeVar("Symbol_co", bound=Hashable, covariant=True)

# Invariant version for concrete implementations
Symbol = TypeVar("Symbol", bound=Hashable)


class Alphabet(Protocol[Symbol_co]):
    """
    A finite set of symbols.

    This protocol defines the interface for alphabets used in epsilon-machines.
    Any type implementing this protocol can be used as an alphabet.
    """

    def __contains__(self, symbol: object) -> bool:
        """Check if symbol is in alphabet."""
        ...

    def __iter__(self) -> Iterator[Symbol_co]:
        """Iterate over symbols."""
        ...

    def __len__(self) -> int:
        """Number of symbols."""
        ...

    @property
    def symbols(self) -> frozenset[Symbol_co]:
        """The set of all symbols."""
        ...


A = TypeVar("A", bound=Hashable)


@dataclass(frozen=True)
class ConcreteAlphabet(Generic[A]):
    """
    Immutable alphabet implementation.

    A concrete implementation of the Alphabet protocol using a frozenset
    to store symbols. This is the standard alphabet type for most use cases.

    Examples:
        >>> alpha = ConcreteAlphabet.binary()
        >>> 0 in alpha
        True
        >>> len(alpha)
        2

        >>> alpha = ConcreteAlphabet.from_symbols('a', 'b', 'c')
        >>> list(sorted(alpha))
        ['a', 'b', 'c']
    """

    _symbols: frozenset[A]

    def __contains__(self, symbol: object) -> bool:
        """Check if symbol is in alphabet."""
        return symbol in self._symbols

    def __iter__(self) -> Iterator[A]:
        """Iterate over symbols."""
        return iter(self._symbols)

    def __len__(self) -> int:
        """Number of symbols."""
        return len(self._symbols)

    @property
    def symbols(self) -> frozenset[A]:
        """The set of all symbols."""
        return self._symbols

    @staticmethod
    def binary() -> "ConcreteAlphabet[int]":
        """
        Create binary alphabet {0, 1}.

        Returns:
            An alphabet containing exactly the integers 0 and 1.

        Examples:
            >>> alpha = ConcreteAlphabet.binary()
            >>> sorted(alpha.symbols)
            [0, 1]
        """
        return ConcreteAlphabet(frozenset({0, 1}))

    @classmethod
    def from_symbols(cls, *symbols: A) -> "ConcreteAlphabet[A]":
        """
        Create alphabet from symbols.

        Args:
            *symbols: Variable number of hashable symbols.

        Returns:
            An alphabet containing the given symbols.

        Examples:
            >>> alpha = ConcreteAlphabet.from_symbols('H', 'T')
            >>> 'H' in alpha
            True
        """
        return cls(frozenset(symbols))
