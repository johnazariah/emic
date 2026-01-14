"""Tests for state types."""

import pytest

from emic.types import CausalState, Transition


class TestTransition:
    """Tests for Transition."""

    def test_basic_transition(self) -> None:
        """Basic transition creation."""
        t = Transition(symbol=0, probability=0.5, target="A")
        assert t.symbol == 0
        assert t.probability == 0.5
        assert t.target == "A"

    def test_probability_must_be_positive(self) -> None:
        """Probability must be > 0."""
        with pytest.raises(ValueError, match="must be in"):
            Transition(symbol=0, probability=0.0, target="A")

    def test_probability_at_most_one(self) -> None:
        """Probability must be <= 1."""
        with pytest.raises(ValueError, match="must be in"):
            Transition(symbol=0, probability=1.5, target="A")

    def test_immutable(self) -> None:
        """Transition is immutable."""
        t = Transition(symbol=0, probability=1.0, target="A")
        with pytest.raises(AttributeError):
            t.probability = 0.5  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Transition is hashable."""
        t1 = Transition(symbol=0, probability=0.5, target="A")
        t2 = Transition(symbol=0, probability=0.5, target="A")
        assert hash(t1) == hash(t2)
        assert {t1, t2} == {t1}


class TestCausalState:
    """Tests for CausalState."""

    def test_basic_state(self) -> None:
        """Basic state creation."""
        t1 = Transition(symbol=0, probability=0.5, target="A")
        t2 = Transition(symbol=1, probability=0.5, target="B")
        state = CausalState(id="S", transitions=frozenset({t1, t2}))
        assert state.id == "S"
        assert len(state.transitions) == 2

    def test_alphabet_property(self) -> None:
        """Alphabet returns symbols with transitions."""
        t1 = Transition(symbol="a", probability=0.5, target="A")
        t2 = Transition(symbol="b", probability=0.5, target="B")
        state = CausalState(id="S", transitions=frozenset({t1, t2}))
        assert state.alphabet == frozenset({"a", "b"})

    def test_transition_distribution(self) -> None:
        """Get distribution over next states."""
        t = Transition(symbol=0, probability=1.0, target="B")
        state = CausalState(id="A", transitions=frozenset({t}))
        dist = state.transition_distribution(0)
        assert dist["B"] == 1.0

    def test_transition_distribution_missing_symbol(self) -> None:
        """KeyError for missing symbol."""
        t = Transition(symbol=0, probability=1.0, target="B")
        state = CausalState(id="A", transitions=frozenset({t}))
        with pytest.raises(KeyError):
            state.transition_distribution(1)

    def test_emission_distribution(self) -> None:
        """Emission distribution sums probabilities."""
        t1 = Transition(symbol=0, probability=0.5, target="A")
        t2 = Transition(symbol=1, probability=0.5, target="B")
        state = CausalState(id="S", transitions=frozenset({t1, t2}))
        dist = state.emission_distribution()
        assert dist[0] == 0.5
        assert dist[1] == 0.5

    def test_next_states(self) -> None:
        """Get possible next states for a symbol."""
        t1 = Transition(symbol=0, probability=1.0, target="B")
        t2 = Transition(symbol=1, probability=1.0, target="C")
        state = CausalState(id="A", transitions=frozenset({t1, t2}))
        assert state.next_states(0) == frozenset({"B"})
        assert state.next_states(1) == frozenset({"C"})

    def test_probabilities_sum_validation(self) -> None:
        """Transitions for same symbol cannot sum > 1."""
        t1 = Transition(symbol=0, probability=0.7, target="A")
        t2 = Transition(symbol=0, probability=0.7, target="B")
        with pytest.raises(ValueError, match="sum to"):
            CausalState(id="S", transitions=frozenset({t1, t2}))

    def test_immutable(self) -> None:
        """State is immutable."""
        t = Transition(symbol=0, probability=1.0, target="B")
        state = CausalState(id="A", transitions=frozenset({t}))
        with pytest.raises(AttributeError):
            state.id = "X"  # type: ignore[misc]

    def test_empty_state(self) -> None:
        """State with no transitions is valid (sink state)."""
        state: CausalState[int] = CausalState(id="sink", transitions=frozenset())
        assert len(state.transitions) == 0
        assert state.alphabet == frozenset()
