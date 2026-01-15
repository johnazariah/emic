"""Tests for SequenceData empirical source."""

from __future__ import annotations

import pytest

from emic.sources.empirical.sequence_data import SequenceData


class TestSequenceData:
    """Tests for SequenceData wrapper."""

    def test_from_string_splits_characters(self) -> None:
        """from_string splits string into characters."""
        data = SequenceData.from_string("abc")
        result = list(data)
        assert result == ["a", "b", "c"]

    def test_from_binary_string_zeros_and_ones(self) -> None:
        """from_binary_string converts to integers."""
        data = SequenceData.from_binary_string("01101")
        result = list(data)
        assert result == [0, 1, 1, 0, 1]

    def test_from_binary_string_invalid_chars(self) -> None:
        """from_binary_string raises on invalid characters."""
        with pytest.raises(ValueError, match="Expected binary string"):
            SequenceData.from_binary_string("01201")

    def test_from_tuple(self) -> None:
        """Direct construction from sequence."""
        data = SequenceData(("x", "y", "z"))
        result = list(data)
        assert result == ["x", "y", "z"]

    def test_length(self) -> None:
        """Length returns correct count."""
        data = SequenceData((1, 2, 3, 4, 5))
        assert len(data) == 5

    def test_iteration(self) -> None:
        """Can iterate multiple times."""
        data = SequenceData(("a", "b"))

        result1 = list(data)
        result2 = list(data)

        assert result1 == result2 == ["a", "b"]

    def test_symbols_property(self) -> None:
        """Symbols tuple is accessible."""
        data = SequenceData(("a", "b", "c", "d"))
        assert data.symbols == ("a", "b", "c", "d")

    def test_empty_sequence(self) -> None:
        """Empty sequence works correctly."""
        data = SequenceData(())
        assert len(data) == 0
        assert list(data) == []

    def test_alphabet_inferred(self) -> None:
        """Alphabet is inferred from symbols."""
        data = SequenceData((0, 1, 1, 0, 1))
        assert data.alphabet == frozenset({0, 1})

    def test_alphabet_explicit(self) -> None:
        """Explicit alphabet overrides inference."""
        data = SequenceData((0, 1), _alphabet=frozenset({0, 1, 2}))
        assert data.alphabet == frozenset({0, 1, 2})

    def test_frozen(self) -> None:
        """SequenceData is immutable."""
        data = SequenceData(("a", "b"))
        with pytest.raises(AttributeError):
            data.symbols = ("c", "d")  # type: ignore[misc]


class TestSequenceDataWithTransforms:
    """Tests for SequenceData with transform pipeline."""

    def test_pipeline_with_take(self) -> None:
        """SequenceData works with TakeN transform."""
        from emic.sources.transforms.take import TakeN

        data = SequenceData.from_string("abcdefgh")
        pipeline = data >> TakeN(5)

        result = list(pipeline)
        assert result == ["a", "b", "c", "d", "e"]

    def test_pipeline_with_skip(self) -> None:
        """SequenceData works with SkipN transform."""
        from emic.sources.transforms.skip import SkipN

        data = SequenceData.from_string("abcdefgh")
        pipeline = data >> SkipN(3)

        result = list(pipeline)
        assert result == ["d", "e", "f", "g", "h"]

    def test_pipeline_chaining(self) -> None:
        """Multiple transforms chain correctly."""
        from emic.sources.transforms.skip import SkipN
        from emic.sources.transforms.take import TakeN

        data = SequenceData.from_binary_string("0011100110")
        # Skip 2, take 5: positions 2-6
        pipeline = data >> SkipN(2) >> TakeN(5)

        result = list(pipeline)
        assert result == [1, 1, 1, 0, 0]
