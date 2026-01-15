"""Suffix tree for collecting history statistics."""

from __future__ import annotations

from collections.abc import Hashable, Iterator
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from emic.types import Distribution

A = TypeVar("A", bound=Hashable)


@dataclass
class HistoryStats(Generic[A]):
    """
    Statistics for a single history string.

    Attributes:
        history: The history tuple
        count: Number of times this history was observed
        next_symbol_counts: Count of each following symbol
    """

    history: tuple[A, ...]
    count: int = 0
    next_symbol_counts: dict[A, int] = field(default_factory=lambda: {})

    def add_observation(self, next_symbol: A) -> None:
        """Record an observation of this history followed by next_symbol."""
        self.count += 1
        self.next_symbol_counts[next_symbol] = self.next_symbol_counts.get(next_symbol, 0) + 1

    @property
    def next_symbol_distribution(self) -> Distribution[A] | None:
        """Distribution over the next symbol, or None if no observations."""
        total = sum(self.next_symbol_counts.values())
        if total == 0:
            return None
        return Distribution(_probs={s: c / total for s, c in self.next_symbol_counts.items()})


class SuffixTree(Generic[A]):
    """
    A tree collecting statistics for all observed histories.

    Each node represents a history string and stores:
    - Count of observations
    - Distribution of next symbols

    Examples:
        >>> tree = SuffixTree(max_depth=3, alphabet=frozenset({0, 1}))
        >>> tree.add_observation((0,), 1)
        >>> tree.add_observation((0,), 0)
        >>> stats = tree.get_stats((0,))
        >>> stats.count
        2
    """

    def __init__(self, max_depth: int, alphabet: frozenset[A]) -> None:
        self.max_depth = max_depth
        self.alphabet = alphabet
        self._stats: dict[tuple[A, ...], HistoryStats[A]] = {}

    def add_observation(self, history: tuple[A, ...], next_symbol: A) -> None:
        """Record an observation of history followed by next_symbol."""
        if len(history) > self.max_depth:
            history = history[-self.max_depth :]

        if history not in self._stats:
            self._stats[history] = HistoryStats(history=history)
        self._stats[history].add_observation(next_symbol)

    def get_stats(self, history: tuple[A, ...]) -> HistoryStats[A] | None:
        """Get statistics for a history, or None if not observed."""
        return self._stats.get(history)

    def histories_of_length(self, length: int) -> Iterator[tuple[A, ...]]:
        """Iterate over all observed histories of given length."""
        for h in self._stats:
            if len(h) == length:
                yield h

    def all_histories(self) -> Iterator[tuple[A, ...]]:
        """Iterate over all observed histories."""
        yield from self._stats.keys()

    def __len__(self) -> int:
        """Number of distinct histories."""
        return len(self._stats)

    def build_from_sequence(self, symbols: list[A]) -> None:
        """
        Build the suffix tree from a sequence of symbols.

        Records statistics for all histories of length 0..max_depth.
        """
        n = len(symbols)

        # For each position, record all histories ending at that position
        for i in range(n - 1):
            next_symbol = symbols[i + 1]

            # Record histories of length 0..max_depth
            for length in range(min(i + 1, self.max_depth) + 1):
                start = i - length + 1
                if start < 0:
                    continue
                history = tuple(symbols[start : i + 1])
                self.add_observation(history, next_symbol)

            # Also record the empty history
            self.add_observation((), symbols[i + 1] if i + 1 < n else symbols[i])
