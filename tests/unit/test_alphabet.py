"""Tests for alphabet types."""

import pytest

from emic.types import ConcreteAlphabet


class TestConcreteAlphabet:
    """Tests for ConcreteAlphabet."""

    def test_binary_alphabet(self) -> None:
        """Binary alphabet contains 0 and 1."""
        alpha = ConcreteAlphabet.binary()
        assert 0 in alpha
        assert 1 in alpha
        assert 2 not in alpha
        assert len(alpha) == 2

    def test_from_symbols(self) -> None:
        """Create alphabet from symbols."""
        alpha = ConcreteAlphabet.from_symbols("a", "b", "c")
        assert "a" in alpha
        assert "b" in alpha
        assert "c" in alpha
        assert "d" not in alpha
        assert len(alpha) == 3

    def test_iteration(self) -> None:
        """Alphabet is iterable."""
        alpha = ConcreteAlphabet.from_symbols(1, 2, 3)
        assert set(alpha) == {1, 2, 3}

    def test_symbols_property(self) -> None:
        """Symbols property returns frozenset."""
        alpha = ConcreteAlphabet.from_symbols("x", "y")
        assert alpha.symbols == frozenset({"x", "y"})

    def test_immutable(self) -> None:
        """Alphabet is immutable (frozen dataclass)."""
        alpha = ConcreteAlphabet.binary()
        with pytest.raises(AttributeError):
            alpha._symbols = frozenset({0, 1, 2})  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Alphabet is hashable."""
        alpha1 = ConcreteAlphabet.binary()
        alpha2 = ConcreteAlphabet.binary()
        assert hash(alpha1) == hash(alpha2)
        assert {alpha1, alpha2} == {alpha1}

    def test_equality(self) -> None:
        """Alphabets with same symbols are equal."""
        alpha1 = ConcreteAlphabet.from_symbols(1, 2)
        alpha2 = ConcreteAlphabet.from_symbols(2, 1)
        assert alpha1 == alpha2

    def test_empty_alphabet(self) -> None:
        """Empty alphabet is valid."""
        alpha: ConcreteAlphabet[int] = ConcreteAlphabet(frozenset())
        assert len(alpha) == 0
        assert list(alpha) == []
