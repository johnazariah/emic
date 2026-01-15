"""Tests for source transforms."""

from __future__ import annotations

from emic.sources.empirical.sequence_data import SequenceData
from emic.sources.transforms.skip import SkipN
from emic.sources.transforms.take import TakeN


class TestTakeN:
    """Tests for TakeN transform."""

    def test_takes_first_n_elements(self) -> None:
        """TakeN returns first n elements."""
        source = SequenceData(("a", "b", "c", "d", "e"))
        result = list(TakeN(3)(source))
        assert result == ["a", "b", "c"]

    def test_takes_all_if_n_exceeds_length(self) -> None:
        """TakeN returns all elements if n > length."""
        source = SequenceData((1, 2, 3))
        result = list(TakeN(10)(source))
        assert result == [1, 2, 3]

    def test_take_zero(self) -> None:
        """TakeN(0) returns empty sequence."""
        source = SequenceData(("a", "b", "c"))
        result = list(TakeN(0)(source))
        assert result == []

    def test_take_from_empty(self) -> None:
        """TakeN from empty source returns empty."""
        source = SequenceData(())
        result = list(TakeN(5)(source))
        assert result == []

    def test_repr(self) -> None:
        """TakeN has informative repr."""
        transform = TakeN(42)
        assert "TakeN" in repr(transform)
        assert "42" in repr(transform)

    def test_callable_protocol(self) -> None:
        """TakeN can be called as function."""
        transform = TakeN(2)
        source = SequenceData(("x", "y", "z"))
        result = list(transform(source))
        assert result == ["x", "y"]


class TestSkipN:
    """Tests for SkipN transform."""

    def test_skips_first_n_elements(self) -> None:
        """SkipN skips first n elements."""
        source = SequenceData(("a", "b", "c", "d", "e"))
        result = list(SkipN(2)(source))
        assert result == ["c", "d", "e"]

    def test_skip_all_returns_empty(self) -> None:
        """Skipping all elements returns empty."""
        source = SequenceData((1, 2, 3))
        result = list(SkipN(3)(source))
        assert result == []

    def test_skip_more_than_length(self) -> None:
        """Skipping more than length returns empty."""
        source = SequenceData(("a", "b"))
        result = list(SkipN(10)(source))
        assert result == []

    def test_skip_zero(self) -> None:
        """SkipN(0) returns all elements."""
        source = SequenceData(("a", "b", "c"))
        result = list(SkipN(0)(source))
        assert result == ["a", "b", "c"]

    def test_skip_from_empty(self) -> None:
        """SkipN from empty source returns empty."""
        source = SequenceData(())
        result = list(SkipN(5)(source))
        assert result == []

    def test_repr(self) -> None:
        """SkipN has informative repr."""
        transform = SkipN(10)
        assert "SkipN" in repr(transform)
        assert "10" in repr(transform)


class TestTransformChaining:
    """Tests for chaining multiple transforms."""

    def test_skip_then_take(self) -> None:
        """Skip followed by take works correctly."""
        source = SequenceData(tuple(range(10)))
        # Skip 3, take 4: should get [3, 4, 5, 6]
        pipeline = source >> SkipN(3) >> TakeN(4)
        result = list(pipeline)
        assert result == [3, 4, 5, 6]

    def test_take_then_skip(self) -> None:
        """Take followed by skip works correctly."""
        source = SequenceData(tuple(range(10)))
        # Take 6, skip 2: should get [2, 3, 4, 5]
        pipeline = source >> TakeN(6) >> SkipN(2)
        result = list(pipeline)
        assert result == [2, 3, 4, 5]

    def test_multiple_takes(self) -> None:
        """Multiple takes take minimum."""
        source = SequenceData(tuple(range(10)))
        pipeline = source >> TakeN(7) >> TakeN(5) >> TakeN(3)
        result = list(pipeline)
        assert result == [0, 1, 2]

    def test_multiple_skips(self) -> None:
        """Multiple skips accumulate."""
        source = SequenceData(tuple(range(10)))
        pipeline = source >> SkipN(2) >> SkipN(3) >> SkipN(1)
        result = list(pipeline)
        # Skip 2+3+1=6: should get [6, 7, 8, 9]
        assert result == [6, 7, 8, 9]

    def test_complex_chain(self) -> None:
        """Complex chain of transforms."""
        source = SequenceData(tuple("abcdefghij"))
        # Skip 1, take 8, skip 2, take 3
        # After skip 1: [b, c, d, e, f, g, h, i, j]
        # After take 8: [b, c, d, e, f, g, h, i]
        # After skip 2: [d, e, f, g, h, i]
        # After take 3: [d, e, f]
        pipeline = source >> SkipN(1) >> TakeN(8) >> SkipN(2) >> TakeN(3)
        result = list(pipeline)
        assert result == ["d", "e", "f"]
