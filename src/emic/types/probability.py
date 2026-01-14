"""Probability distribution types for epsilon-machines."""

from __future__ import annotations

import math
from collections.abc import Hashable, Iterator, Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from typing import Self

# For v1, probabilities are floats
# Extension point for Rational/symbolic (ADR-006)
ProbabilityValue = float

A = TypeVar("A", bound=Hashable)

# Tolerance for probability validation
_PROBABILITY_TOLERANCE = 1e-9
_SUM_TOLERANCE = 1e-3


@dataclass(frozen=True)
class Distribution(Generic[A]):
    """
    An immutable probability distribution over symbols.

    Invariants:
        - All probabilities are in [0, 1]
        - Probabilities sum to 1 (within tolerance)
        - Only non-zero probabilities are stored

    Examples:
        >>> dist = Distribution({'a': 0.7, 'b': 0.3})
        >>> dist['a']
        0.7
        >>> dist['c']  # Not in distribution
        0.0
        >>> dist.entropy()  # doctest: +ELLIPSIS
        0.881...
    """

    _probs: Mapping[A, ProbabilityValue]

    def __post_init__(self) -> None:
        """Validate probabilities sum to 1 and are in valid range."""
        total = sum(self._probs.values())
        if not (1.0 - _SUM_TOLERANCE <= total <= 1.0 + _SUM_TOLERANCE):
            msg = f"Probabilities must sum to 1, got {total}"
            raise ValueError(msg)
        for symbol, p in self._probs.items():
            if not (0.0 - _PROBABILITY_TOLERANCE <= p <= 1.0 + _PROBABILITY_TOLERANCE):
                msg = f"Probability must be in [0,1], got {p} for symbol {symbol}"
                raise ValueError(msg)

    def __getitem__(self, symbol: A) -> ProbabilityValue:
        """Get probability of a symbol (0.0 if not in support)."""
        return self._probs.get(symbol, 0.0)

    def __iter__(self) -> Iterator[A]:
        """Iterate over symbols in the support."""
        return iter(self._probs)

    def __len__(self) -> int:
        """Number of symbols in the support."""
        return len(self._probs)

    @property
    def support(self) -> frozenset[A]:
        """Symbols with non-zero probability."""
        return frozenset(self._probs.keys())

    @property
    def probs(self) -> Mapping[A, ProbabilityValue]:
        """The underlying probability mapping (read-only)."""
        return self._probs

    def entropy(self) -> float:
        """
        Shannon entropy of the distribution in bits.

        Returns:
            The entropy H = -Σ p(x) log₂ p(x)

        Examples:
            >>> Distribution.uniform(frozenset({0, 1})).entropy()
            1.0
            >>> Distribution.deterministic('a').entropy()
            0.0
        """
        return -sum(p * math.log2(p) for p in self._probs.values() if p > 0)

    @classmethod
    def uniform(cls, symbols: frozenset[A]) -> Self:
        """
        Create uniform distribution over symbols.

        Args:
            symbols: Set of symbols to distribute probability over.

        Returns:
            A distribution with equal probability for each symbol.

        Raises:
            ValueError: If symbols is empty.

        Examples:
            >>> dist = Distribution.uniform(frozenset({'a', 'b'}))
            >>> dist['a']
            0.5
        """
        if not symbols:
            msg = "Cannot create uniform distribution over empty set"
            raise ValueError(msg)
        n = len(symbols)
        return cls(dict.fromkeys(symbols, 1.0 / n))

    @classmethod
    def deterministic(cls, symbol: A) -> Self:
        """
        Create distribution with all mass on one symbol.

        Args:
            symbol: The symbol to assign probability 1.0.

        Returns:
            A distribution where only the given symbol has non-zero probability.

        Examples:
            >>> dist = Distribution.deterministic('x')
            >>> dist['x']
            1.0
            >>> dist['y']
            0.0
        """
        return cls({symbol: 1.0})
