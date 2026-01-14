"""Tests for EpsilonMachine types."""

import pytest

from emic.types import (
    CausalState,
    Distribution,
    EpsilonMachine,
    EpsilonMachineBuilder,
    Transition,
)


class TestEpsilonMachine:
    """Tests for EpsilonMachine."""

    def test_basic_machine(self) -> None:
        """Build basic epsilon machine."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", 0.5)
            .add_transition("A", 1, "B", 0.5)
            .add_transition("B", 0, "A", 1.0)
            .with_start_state("A")
            .with_stationary_distribution({"A": 2 / 3, "B": 1 / 3})
            .build()
        )
        assert len(machine) == 2
        assert machine.alphabet == frozenset({0, 1})
        assert machine.state_ids == frozenset({"A", "B"})

    def test_get_state(self) -> None:
        """Get state by ID."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", 1.0)
            .with_start_state("A")
            .build()
        )
        state = machine.get_state("A")
        assert state.id == "A"

    def test_get_state_not_found(self) -> None:
        """KeyError for missing state."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", 1.0)
            .with_start_state("A")
            .build()
        )
        with pytest.raises(KeyError):
            machine.get_state("B")

    def test_is_unifilar(self) -> None:
        """Check unifilarity."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", 1.0)
            .add_transition("A", 1, "B", 1.0)
            .with_start_state("A")
            .build()
        )
        assert machine.is_unifilar()

    def test_transition_matrix(self) -> None:
        """Get transition matrix for symbol."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "B", 1.0)
            .add_transition("B", 0, "A", 1.0)
            .with_start_state("A")
            .build()
        )
        matrix = machine.transition_matrix(0)
        assert matrix["A"]["B"] == 1.0
        assert matrix["B"]["A"] == 1.0

    def test_invalid_start_state(self) -> None:
        """Invalid start state raises."""
        t = Transition(symbol=0, probability=1.0, target="A")
        state = CausalState(id="A", transitions=frozenset({t}))
        with pytest.raises(ValueError, match="not in states"):
            EpsilonMachine(
                alphabet=frozenset({0}),
                states=frozenset({state}),
                start_state="B",  # Not a valid state
                stationary_distribution=Distribution({"A": 1.0}),
            )

    def test_invalid_stationary_distribution(self) -> None:
        """Stationary dist over unknown state raises."""
        t = Transition(symbol=0, probability=1.0, target="A")
        state = CausalState(id="A", transitions=frozenset({t}))
        with pytest.raises(ValueError, match="unknown state"):
            EpsilonMachine(
                alphabet=frozenset({0}),
                states=frozenset({state}),
                start_state="A",
                stationary_distribution=Distribution({"X": 1.0}),  # Unknown state
            )

    def test_unifilarity_violation(self) -> None:
        """Non-unifilar machine raises."""
        t1 = Transition(symbol=0, probability=0.5, target="A")
        t2 = Transition(symbol=0, probability=0.5, target="B")  # Same symbol, diff target
        state_a = CausalState(id="A", transitions=frozenset({t1, t2}))
        state_b = CausalState(id="B", transitions=frozenset())
        with pytest.raises(ValueError, match="unifilarity"):
            EpsilonMachine(
                alphabet=frozenset({0}),
                states=frozenset({state_a, state_b}),
                start_state="A",
                stationary_distribution=Distribution({"A": 0.5, "B": 0.5}),
            )

    def test_is_ergodic_not_implemented(self) -> None:
        """is_ergodic raises NotImplementedError."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", 1.0)
            .with_start_state("A")
            .build()
        )
        with pytest.raises(NotImplementedError):
            machine.is_ergodic()


class TestEpsilonMachineBuilder:
    """Tests for EpsilonMachineBuilder."""

    def test_fluent_api(self) -> None:
        """Builder supports fluent API."""
        builder = EpsilonMachineBuilder[int]()
        result = (
            builder.with_alphabet({0, 1})
            .add_state("A")
            .add_transition("A", 0, "B", 1.0)
            .with_start_state("A")
        )
        assert result is builder

    def test_auto_creates_states(self) -> None:
        """add_transition creates states automatically."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "B", 1.0)
            .with_start_state("A")
            .build()
        )
        assert "A" in machine.state_ids
        assert "B" in machine.state_ids

    def test_auto_creates_alphabet(self) -> None:
        """add_transition adds to alphabet automatically."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", 0.5)
            .add_transition("A", 1, "A", 0.5)
            .with_start_state("A")
            .build()
        )
        assert machine.alphabet == frozenset({0, 1})

    def test_missing_start_state(self) -> None:
        """Build without start state raises."""
        builder = EpsilonMachineBuilder[int]().add_transition("A", 0, "A", 1.0)
        with pytest.raises(ValueError, match="Start state not set"):
            builder.build()

    def test_default_stationary_distribution(self) -> None:
        """Default stationary is uniform."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "B", 1.0)
            .add_transition("B", 0, "A", 1.0)
            .with_start_state("A")
            .build()
        )
        assert machine.stationary_distribution["A"] == 0.5
        assert machine.stationary_distribution["B"] == 0.5

    def test_golden_mean_machine(self) -> None:
        """Build the Golden Mean process machine."""
        machine = (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", 0.5)
            .add_transition("A", 1, "B", 0.5)
            .add_transition("B", 0, "A", 1.0)
            .with_start_state("A")
            .with_stationary_distribution({"A": 2 / 3, "B": 1 / 3})
            .build()
        )

        assert len(machine) == 2
        assert machine.is_unifilar()
        assert machine.alphabet == frozenset({0, 1})

        # Check state A has both transitions
        state_a = machine.get_state("A")
        assert state_a.alphabet == frozenset({0, 1})

        # Check state B only has 0 transition
        state_b = machine.get_state("B")
        assert state_b.alphabet == frozenset({0})
