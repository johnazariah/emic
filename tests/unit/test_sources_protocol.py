"""Tests for source protocols."""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


class MinimalSequenceSource:
    """Minimal implementation for testing SequenceSource protocol."""

    @property
    def alphabet(self) -> frozenset[str]:
        return frozenset({"a", "b", "c"})

    def __iter__(self) -> Iterator[str]:
        yield from ["a", "b", "c"]


class MinimalSeededSource:
    """Minimal implementation for testing SeededSource protocol."""

    def __init__(self, seed: int = 42) -> None:
        self._seed = seed

    @property
    def alphabet(self) -> frozenset[int]:
        return frozenset({1, 2, 3})

    @property
    def seed(self) -> int:
        return self._seed

    def with_seed(self, seed: int) -> MinimalSeededSource:
        return MinimalSeededSource(seed=seed)

    def __iter__(self) -> Iterator[int]:
        yield from [1, 2, 3]


class TestSequenceSourceProtocol:
    """Tests for SequenceSource protocol."""

    def test_can_iterate_minimal_implementation(self) -> None:
        """Minimal implementation can be iterated."""
        source = MinimalSequenceSource()
        result = list(source)
        assert result == ["a", "b", "c"]

    def test_has_alphabet(self) -> None:
        """Minimal implementation has alphabet property."""
        source = MinimalSequenceSource()
        assert source.alphabet == frozenset({"a", "b", "c"})

    def test_biased_coin_source_can_iterate(self) -> None:
        """BiasedCoinSource can be iterated."""
        from emic.sources.synthetic.biased_coin import BiasedCoinSource

        source = BiasedCoinSource(p=0.5, _seed=42)
        symbols = list(itertools.islice(source, 10))
        assert len(symbols) == 10
        assert all(s in (0, 1) for s in symbols)


class TestSeededSourceProtocol:
    """Tests for SeededSource protocol."""

    def test_has_seed_property(self) -> None:
        """Minimal implementation has seed property."""
        source = MinimalSeededSource(seed=123)
        assert source.seed == 123

    def test_has_with_seed(self) -> None:
        """Minimal implementation has with_seed method."""
        source = MinimalSeededSource(seed=123)
        new_source = source.with_seed(456)
        assert new_source.seed == 456

    def test_biased_coin_source_has_seed(self) -> None:
        """BiasedCoinSource has seed property."""
        from emic.sources.synthetic.biased_coin import BiasedCoinSource

        source = BiasedCoinSource(p=0.5, _seed=42)
        assert source.seed == 42

    def test_biased_coin_source_with_seed(self) -> None:
        """BiasedCoinSource with_seed returns new source."""
        from emic.sources.synthetic.biased_coin import BiasedCoinSource

        source = BiasedCoinSource(p=0.5, _seed=42)
        new_source = source.with_seed(123)
        assert new_source.seed == 123
        assert source.seed == 42  # Original unchanged
