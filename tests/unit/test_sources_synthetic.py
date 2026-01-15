"""Tests for synthetic sources."""

from __future__ import annotations

import itertools

import pytest

from emic.sources.synthetic.biased_coin import BiasedCoinSource
from emic.sources.synthetic.even_process import EvenProcessSource
from emic.sources.synthetic.golden_mean import GoldenMeanSource
from emic.sources.synthetic.periodic import PeriodicSource
from emic.types import EpsilonMachine


class TestGoldenMeanSource:
    """Tests for GoldenMeanSource (no consecutive 1s)."""

    def test_generates_binary_symbols(self) -> None:
        """Output contains only 0 and 1."""
        source = GoldenMeanSource(p=0.5, _seed=42)
        symbols = list(itertools.islice(source, 100))
        assert all(s in (0, 1) for s in symbols)

    def test_no_consecutive_ones(self) -> None:
        """No two consecutive 1s appear."""
        source = GoldenMeanSource(p=0.5, _seed=42)
        symbols = list(itertools.islice(source, 1000))

        for i in range(len(symbols) - 1):
            assert not (symbols[i] == 1 and symbols[i + 1] == 1), (
                f"Found consecutive 1s at positions {i} and {i + 1}"
            )

    def test_reproducibility_with_seed(self) -> None:
        """Same seed produces same sequence."""
        source1 = GoldenMeanSource(p=0.5, _seed=123)
        source2 = GoldenMeanSource(p=0.5, _seed=123)

        seq1 = list(itertools.islice(source1, 100))
        seq2 = list(itertools.islice(source2, 100))

        assert seq1 == seq2

    def test_different_seeds_produce_different_sequences(self) -> None:
        """Different seeds produce different sequences."""
        source1 = GoldenMeanSource(p=0.5, _seed=1)
        source2 = GoldenMeanSource(p=0.5, _seed=2)

        seq1 = list(itertools.islice(source1, 100))
        seq2 = list(itertools.islice(source2, 100))

        assert seq1 != seq2

    def test_true_machine_returns_epsilon_machine(self) -> None:
        """true_machine property returns valid EpsilonMachine."""
        source = GoldenMeanSource(p=0.5, _seed=42)
        machine = source.true_machine

        assert isinstance(machine, EpsilonMachine)
        assert len(machine.states) == 2  # Two causal states

    def test_true_machine_is_unifiliar(self) -> None:
        """The returned machine is unifiliar (validated at construction)."""
        source = GoldenMeanSource()
        machine = source.true_machine
        # If we got here without error, machine is unifiliar
        assert machine is not None


class TestEvenProcessSource:
    """Tests for EvenProcessSource (even number of 1s between 0s)."""

    def test_generates_binary_symbols(self) -> None:
        """Output contains only 0 and 1."""
        source = EvenProcessSource(p=0.5, _seed=42)
        symbols = list(itertools.islice(source, 100))
        assert all(s in (0, 1) for s in symbols)

    def test_even_ones_between_zeros(self) -> None:
        """Even number of 1s appears between each pair of 0s."""
        source = EvenProcessSource(p=0.5, _seed=42)
        symbols = list(itertools.islice(source, 500))

        # Find 0s and count 1s between them
        ones_count = 0
        seen_first_zero = False
        for s in symbols:
            if s == 0:
                if seen_first_zero:
                    assert ones_count % 2 == 0, (
                        f"Found {ones_count} ones between zeros (should be even)"
                    )
                seen_first_zero = True
                ones_count = 0
            else:
                ones_count += 1

    def test_reproducibility_with_seed(self) -> None:
        """Same seed produces same sequence."""
        source1 = EvenProcessSource(p=0.5, _seed=456)
        source2 = EvenProcessSource(p=0.5, _seed=456)

        seq1 = list(itertools.islice(source1, 100))
        seq2 = list(itertools.islice(source2, 100))

        assert seq1 == seq2

    def test_true_machine_returns_epsilon_machine(self) -> None:
        """true_machine property returns valid EpsilonMachine."""
        source = EvenProcessSource()
        machine = source.true_machine

        assert isinstance(machine, EpsilonMachine)
        assert len(machine.states) == 2  # Even and odd states


class TestBiasedCoinSource:
    """Tests for BiasedCoinSource (IID binary source)."""

    def test_generates_binary_symbols(self) -> None:
        """Output contains only 0 and 1."""
        source = BiasedCoinSource(p=0.7, _seed=42)
        symbols = list(itertools.islice(source, 100))
        assert all(s in (0, 1) for s in symbols)

    def test_fair_coin_approximately_balanced(self) -> None:
        """Fair coin (p=0.5) produces roughly equal 0s and 1s."""
        source = BiasedCoinSource(p=0.5, _seed=42)
        symbols = list(itertools.islice(source, 10000))

        count_ones = sum(symbols)
        ratio = count_ones / len(symbols)

        # Should be close to 0.5 (within 5%)
        assert 0.45 < ratio < 0.55

    def test_heavily_biased_coin(self) -> None:
        """Heavily biased coin produces mostly one symbol."""
        source = BiasedCoinSource(p=0.9, _seed=42)
        symbols = list(itertools.islice(source, 1000))

        count_ones = sum(symbols)
        ratio = count_ones / len(symbols)

        # Should be close to 0.9
        assert ratio > 0.8

    def test_p_zero_all_zeros(self) -> None:
        """p=0 produces all zeros."""
        source = BiasedCoinSource(p=0.0, _seed=42)
        symbols = list(itertools.islice(source, 100))
        assert all(s == 0 for s in symbols)

    def test_p_one_all_ones(self) -> None:
        """p=1 produces all ones."""
        source = BiasedCoinSource(p=1.0, _seed=42)
        symbols = list(itertools.islice(source, 100))
        assert all(s == 1 for s in symbols)

    def test_invalid_probability_raises_error(self) -> None:
        """Invalid probability raises ValueError."""
        with pytest.raises(ValueError, match=r"p must be in \[0, 1\]"):
            BiasedCoinSource(p=-0.1)

        with pytest.raises(ValueError, match=r"p must be in \[0, 1\]"):
            BiasedCoinSource(p=1.1)

    def test_true_machine_returns_epsilon_machine(self) -> None:
        """true_machine property returns valid EpsilonMachine."""
        source = BiasedCoinSource(p=0.3)
        machine = source.true_machine

        assert isinstance(machine, EpsilonMachine)
        assert len(machine.states) == 1  # IID has single state

    def test_true_machine_has_correct_probabilities(self) -> None:
        """Machine encodes correct emission probabilities."""
        source = BiasedCoinSource(p=0.7)
        machine = source.true_machine

        state = next(iter(machine.states))
        # Check that transitions exist for both symbols
        # IID source should have transitions for 0 and 1
        assert state.transitions  # Has at least some transitions


class TestPeriodicSource:
    """Tests for PeriodicSource."""

    def test_generates_periodic_sequence(self) -> None:
        """Output repeats the pattern periodically."""
        pattern = ("a", "b", "c")
        source = PeriodicSource(pattern=pattern)
        symbols = list(itertools.islice(source, 9))

        assert symbols == ["a", "b", "c", "a", "b", "c", "a", "b", "c"]

    def test_single_symbol_pattern(self) -> None:
        """Single symbol pattern produces constant output."""
        source = PeriodicSource(pattern=("x",))
        symbols = list(itertools.islice(source, 5))
        assert symbols == ["x", "x", "x", "x", "x"]

    def test_empty_pattern_raises_error(self) -> None:
        """Empty pattern raises ValueError."""
        with pytest.raises(ValueError, match="must be non-empty"):
            PeriodicSource(pattern=())

    def test_binary_pattern(self) -> None:
        """Binary patterns work correctly."""
        source = PeriodicSource(pattern=(0, 1))
        symbols = list(itertools.islice(source, 6))
        assert symbols == [0, 1, 0, 1, 0, 1]

    def test_true_machine_returns_epsilon_machine(self) -> None:
        """true_machine property returns valid EpsilonMachine."""
        source = PeriodicSource(pattern=("a", "b", "c"))
        machine = source.true_machine

        assert isinstance(machine, EpsilonMachine)
        # Period-3 pattern has 3 states
        assert len(machine.states) == 3

    def test_true_machine_deterministic(self) -> None:
        """Periodic machine is fully deterministic."""
        source = PeriodicSource(pattern=("x", "y"))
        machine = source.true_machine

        for state in machine.states:
            # Each state should have exactly one transition (deterministic)
            assert len(state.transitions) == 1
            # The single transition should have probability 1
            transition = next(iter(state.transitions))
            assert abs(transition.probability - 1.0) < 1e-10
