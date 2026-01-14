"""Tests for probability types."""

import math

import pytest

from emic.types import Distribution


class TestDistribution:
    """Tests for Distribution."""

    def test_basic_distribution(self) -> None:
        """Basic distribution creation."""
        dist = Distribution({"a": 0.7, "b": 0.3})
        assert dist["a"] == 0.7
        assert dist["b"] == 0.3

    def test_missing_symbol_returns_zero(self) -> None:
        """Missing symbols return 0.0."""
        dist = Distribution({"a": 1.0})
        assert dist["b"] == 0.0

    def test_probabilities_must_sum_to_one(self) -> None:
        """Probabilities must sum to 1."""
        with pytest.raises(ValueError, match="must sum to 1"):
            Distribution({"a": 0.5, "b": 0.3})

    def test_probabilities_in_valid_range(self) -> None:
        """Probabilities must be in [0, 1]."""
        with pytest.raises(ValueError, match="must be in"):
            Distribution({"a": 1.5, "b": -0.5})

    def test_support(self) -> None:
        """Support returns symbols with non-zero probability."""
        dist = Distribution({"a": 0.6, "b": 0.4})
        assert dist.support == frozenset({"a", "b"})

    def test_entropy_uniform(self) -> None:
        """Entropy of uniform binary is 1 bit."""
        dist = Distribution.uniform(frozenset({0, 1}))
        assert math.isclose(dist.entropy(), 1.0)

    def test_entropy_deterministic(self) -> None:
        """Entropy of deterministic distribution is 0."""
        dist = Distribution.deterministic("x")
        assert dist.entropy() == 0.0

    def test_entropy_calculation(self) -> None:
        """Entropy calculation is correct."""
        # H(0.5, 0.25, 0.25) = -0.5*log2(0.5) - 2*0.25*log2(0.25)
        # = 0.5 + 0.5 * 2 = 1.5
        dist = Distribution({"a": 0.5, "b": 0.25, "c": 0.25})
        assert math.isclose(dist.entropy(), 1.5)

    def test_uniform(self) -> None:
        """Uniform distribution has equal probabilities."""
        dist = Distribution.uniform(frozenset({1, 2, 3}))
        assert math.isclose(dist[1], 1 / 3)
        assert math.isclose(dist[2], 1 / 3)
        assert math.isclose(dist[3], 1 / 3)

    def test_uniform_empty_raises(self) -> None:
        """Uniform over empty set raises."""
        with pytest.raises(ValueError, match="empty"):
            Distribution.uniform(frozenset())

    def test_deterministic(self) -> None:
        """Deterministic has all mass on one symbol."""
        dist = Distribution.deterministic("only")
        assert dist["only"] == 1.0
        assert dist["other"] == 0.0

    def test_iteration(self) -> None:
        """Distribution is iterable over support."""
        dist = Distribution({"a": 0.5, "b": 0.5})
        assert set(dist) == {"a", "b"}

    def test_len(self) -> None:
        """Length is size of support."""
        dist = Distribution({"a": 0.5, "b": 0.3, "c": 0.2})
        assert len(dist) == 3

    def test_immutable(self) -> None:
        """Distribution is immutable."""
        dist = Distribution({"a": 1.0})
        with pytest.raises(AttributeError):
            dist._probs = {"b": 1.0}  # type: ignore[misc]
