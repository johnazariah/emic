"""Tests for StochasticSource base class."""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from emic.sources.base import StochasticSource

if TYPE_CHECKING:
    from collections.abc import Iterator


class DeterministicTestSource(StochasticSource[str]):
    """Simple test source that yields predetermined symbols."""

    symbols: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.symbols is None:
            object.__setattr__(self, "symbols", ["a", "b", "c"])
        object.__setattr__(self, "_alphabet", frozenset(self.symbols))

    def __iter__(self) -> Iterator[str]:
        yield from self.symbols


class TestStochasticSourceBase:
    """Tests for StochasticSource base class."""

    def test_seed_property(self) -> None:
        """Seed is stored and retrievable."""
        source = DeterministicTestSource(_seed=42)
        assert source.seed == 42

    def test_default_seed_is_none(self) -> None:
        """Default seed is None when not provided."""
        source = DeterministicTestSource()
        assert source.seed is None

    def test_iter_yields_symbols(self) -> None:
        """__iter__ yields the symbols."""
        source = DeterministicTestSource()
        result = list(source)
        assert result == ["a", "b", "c"]

    def test_alphabet_property(self) -> None:
        """Alphabet property returns the symbol set."""
        source = DeterministicTestSource()
        assert source.alphabet == frozenset({"a", "b", "c"})

    def test_rng_is_seeded_reproducibly(self) -> None:
        """RNG produces reproducible values when seeded."""
        from emic.sources.synthetic.biased_coin import BiasedCoinSource

        source1 = BiasedCoinSource(p=0.5, _seed=12345)
        source2 = BiasedCoinSource(p=0.5, _seed=12345)

        seq1 = list(itertools.islice(source1, 100))
        seq2 = list(itertools.islice(source2, 100))

        assert seq1 == seq2

    def test_rng_differs_with_different_seeds(self) -> None:
        """RNG produces different values with different seeds."""
        from emic.sources.synthetic.biased_coin import BiasedCoinSource

        source1 = BiasedCoinSource(p=0.5, _seed=1)
        source2 = BiasedCoinSource(p=0.5, _seed=2)

        seq1 = list(itertools.islice(source1, 100))
        seq2 = list(itertools.islice(source2, 100))

        assert seq1 != seq2


class TestStochasticSourcePipelineOperator:
    """Tests for the >> pipeline operator."""

    def test_pipeline_with_take_transform(self) -> None:
        """>> operator works with TakeN transform."""
        from emic.sources.empirical.sequence_data import SequenceData
        from emic.sources.transforms.take import TakeN

        source = SequenceData(tuple("abcde"))
        pipeline = source >> TakeN(3)

        result = list(pipeline)
        assert result == ["a", "b", "c"]

    def test_pipeline_with_skip_transform(self) -> None:
        """>> operator works with SkipN transform."""
        from emic.sources.empirical.sequence_data import SequenceData
        from emic.sources.transforms.skip import SkipN

        source = SequenceData(tuple("abcde"))
        pipeline = source >> SkipN(2)

        result = list(pipeline)
        assert result == ["c", "d", "e"]

    def test_pipeline_chaining(self) -> None:
        """Multiple transforms can be chained."""
        from emic.sources.empirical.sequence_data import SequenceData
        from emic.sources.transforms.skip import SkipN
        from emic.sources.transforms.take import TakeN

        source = SequenceData(tuple("abcdefg"))
        # Skip 2, then take 3: should get ["c", "d", "e"]
        pipeline = source >> SkipN(2) >> TakeN(3)

        result = list(pipeline)
        assert result == ["c", "d", "e"]
