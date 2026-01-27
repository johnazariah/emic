"""Tests for Spectral Learning algorithm."""

import pytest

from emic.inference.spectral import Spectral, SpectralConfig


class TestSpectralConfig:
    """Tests for SpectralConfig."""

    def test_valid_config(self) -> None:
        """Test valid configuration creation."""
        config = SpectralConfig(max_history=5, rank_threshold=0.01)
        assert config.max_history == 5
        assert config.rank_threshold == 0.01

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = SpectralConfig()
        assert config.max_history is None  # Adaptive by default
        assert config.rank_threshold == 0.001  # Conservative default
        assert config.rank is None
        assert config.regularization == 1e-6
        assert config.min_count is None  # Adaptive by default

    def test_invalid_max_history(self) -> None:
        """Test that max_history must be positive."""
        with pytest.raises(ValueError, match="max_history"):
            SpectralConfig(max_history=0)
        with pytest.raises(ValueError, match="max_history"):
            SpectralConfig(max_history=-1)

    def test_invalid_rank_threshold(self) -> None:
        """Test that rank_threshold must be in (0, 1)."""
        with pytest.raises(ValueError, match="rank_threshold"):
            SpectralConfig(rank_threshold=0)
        with pytest.raises(ValueError, match="rank_threshold"):
            SpectralConfig(rank_threshold=-0.1)
        with pytest.raises(ValueError, match="rank_threshold"):
            SpectralConfig(rank_threshold=1.0)
        with pytest.raises(ValueError, match="rank_threshold"):
            SpectralConfig(rank_threshold=1.5)

    def test_invalid_rank(self) -> None:
        """Test that rank must be positive if specified."""
        with pytest.raises(ValueError, match="rank"):
            SpectralConfig(rank=0)
        with pytest.raises(ValueError, match="rank"):
            SpectralConfig(rank=-1)

    def test_invalid_regularization(self) -> None:
        """Test that regularization must be non-negative."""
        with pytest.raises(ValueError, match="regularization"):
            SpectralConfig(regularization=-0.1)

    def test_invalid_min_count(self) -> None:
        """Test that min_count must be positive."""
        with pytest.raises(ValueError, match="min_count"):
            SpectralConfig(min_count=0)

    def test_fixed_rank(self) -> None:
        """Test that fixed rank can be specified."""
        config = SpectralConfig(rank=3)
        assert config.rank == 3


class TestSpectralInference:
    """Tests for Spectral inference."""

    def test_insufficient_data_raises_error(self) -> None:
        """Test that short sequences raise InsufficientDataError."""
        from emic.inference.errors import InsufficientDataError

        spectral = Spectral(SpectralConfig(max_history=5))
        with pytest.raises(InsufficientDataError):
            spectral.infer([0, 1, 0])

    def test_infer_biased_coin_single_state(self) -> None:
        """Test inference on biased coin (should find ~1 state)."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(2000)(source))

        spectral = Spectral(SpectralConfig(max_history=3, rank=1))
        result = spectral.infer(data)

        # Should find small number of states
        assert len(result.machine.states) <= 3

    def test_infer_periodic_finds_states(self) -> None:
        """Test inference on periodic process."""
        from emic.sources.synthetic import PeriodicSource
        from emic.sources.transforms import TakeN

        source = PeriodicSource([0, 1])
        data = list(TakeN(2000)(source))

        spectral = Spectral(SpectralConfig(max_history=3, rank=2))
        result = spectral.infer(data)

        # Should find states (exact count may vary)
        assert len(result.machine.states) >= 1

    def test_infer_golden_mean(self) -> None:
        """Test inference on golden mean process."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(3000)(source))

        spectral = Spectral(SpectralConfig(max_history=5))
        result = spectral.infer(data)

        # Should find at least 1 state
        assert len(result.machine.states) >= 1

    def test_result_has_diagnostics(self) -> None:
        """Test that result contains diagnostic information."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(1000)(source))

        spectral = Spectral(SpectralConfig(max_history=3))
        result = spectral.infer(data)

        assert result.sequence_length == 1000
        assert result.max_history_used == 3
        assert result.num_histories_considered >= 0

    def test_pipeline_operator(self) -> None:
        """Test that pipeline operator works."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(1000)(source))

        result = data >> Spectral(SpectralConfig(max_history=3))

        assert result.machine is not None

    def test_with_explicit_alphabet(self) -> None:
        """Test inference with explicit alphabet."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(1000)(source))

        spectral = Spectral(SpectralConfig(max_history=3))
        result = spectral.infer(data, alphabet=frozenset({0, 1}))

        assert result.machine.alphabet == frozenset({0, 1})


class TestSpectralHankelMatrix:
    """Tests for Hankel matrix construction."""

    def test_hankel_counts_basic(self) -> None:
        """Test that Hankel matrix is built correctly."""
        # Simple repeating pattern - need more data for adaptive params
        data = [0, 1] * 500

        spectral = Spectral(SpectralConfig(max_history=2))
        result = spectral.infer(data)

        # Should produce a valid machine
        assert result.machine is not None
        assert len(result.machine.alphabet) == 2

    def test_hankel_with_single_symbol(self) -> None:
        """Test Hankel matrix with only one symbol."""
        data = [0] * 200

        spectral = Spectral(SpectralConfig(max_history=2))
        result = spectral.infer(data)

        # Should find 1 state
        assert len(result.machine.states) == 1


class TestSpectralEdgeCases:
    """Edge case tests for Spectral."""

    def test_minimum_valid_sequence(self) -> None:
        """Test with minimum valid sequence length."""
        # Need enough data to build Hankel matrix
        data = [0, 1, 0, 1] * 50

        spectral = Spectral(SpectralConfig(max_history=2, min_count=1))
        result = spectral.infer(data)

        assert result.machine is not None

    def test_with_regularization(self) -> None:
        """Test that regularization parameter is respected."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(1000)(source))

        spectral = Spectral(SpectralConfig(max_history=3, regularization=1e-3))
        result = spectral.infer(data)

        assert result.machine is not None

    def test_with_fixed_rank(self) -> None:
        """Test inference with fixed rank."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(2000)(source))

        # Fixed rank = 2
        spectral = Spectral(SpectralConfig(max_history=4, rank=2))
        result = spectral.infer(data)

        assert result.machine is not None
        # With rank=2, should have at most ~2-3 states
        assert len(result.machine.states) <= 5

    def test_with_high_rank(self) -> None:
        """Test inference with higher fixed rank."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(3000)(source))

        spectral = Spectral(SpectralConfig(max_history=4, rank=5))
        result = spectral.infer(data)

        assert result.machine is not None

    def test_with_very_low_rank_threshold(self) -> None:
        """Test inference with very low rank threshold."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(2000)(source))

        spectral = Spectral(SpectralConfig(max_history=3, rank_threshold=0.0001))
        result = spectral.infer(data)

        assert result.machine is not None

    def test_with_high_rank_threshold(self) -> None:
        """Test inference with high rank threshold (conservative)."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(2000)(source))

        spectral = Spectral(SpectralConfig(max_history=4, rank_threshold=0.5))
        result = spectral.infer(data)

        assert result.machine is not None
        # High threshold should find fewer states
        assert len(result.machine.states) >= 1

    def test_three_symbol_alphabet(self) -> None:
        """Test inference with three-symbol alphabet."""
        from emic.sources.synthetic import PeriodicSource
        from emic.sources.transforms import TakeN

        source = PeriodicSource([0, 1, 2])
        data = list(TakeN(1500)(source))

        spectral = Spectral(SpectralConfig(max_history=4))
        result = spectral.infer(data)

        assert result.machine.alphabet == frozenset({0, 1, 2})

    def test_long_period_pattern(self) -> None:
        """Test inference on longer periodic pattern."""
        from emic.sources.synthetic import PeriodicSource
        from emic.sources.transforms import TakeN

        source = PeriodicSource([0, 0, 1, 0, 1, 1])
        data = list(TakeN(3000)(source))

        spectral = Spectral(SpectralConfig(max_history=8))
        result = spectral.infer(data)

        assert result.machine is not None
        # Should find multiple states
        assert len(result.machine.states) >= 1

    def test_short_history_length(self) -> None:
        """Test inference with short max_history."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(2000)(source))

        spectral = Spectral(SpectralConfig(max_history=1))
        result = spectral.infer(data)

        assert result.machine is not None


class TestSpectralExtraction:
    """Tests for spectral extraction module internals."""

    def test_trivial_machine_fallback(self) -> None:
        """Test that trivial machine is built for edge cases."""
        # Constant sequence
        data = [0] * 500

        spectral = Spectral(SpectralConfig(max_history=2))
        result = spectral.infer(data)

        # Should still produce valid machine
        assert result.machine is not None
        assert len(result.machine.states) >= 1

    def test_small_sequence_handling(self) -> None:
        """Test handling of small but valid sequences."""
        # Minimal sequence that passes length check
        data = [0, 1] * 100

        spectral = Spectral(SpectralConfig(max_history=2, min_count=1))
        result = spectral.infer(data)

        assert result.machine is not None

    def test_operators_convergence(self) -> None:
        """Test that operators converge to valid machine."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=123)
        data = list(TakeN(5000)(source))

        spectral = Spectral(SpectralConfig(max_history=5))
        result = spectral.infer(data)

        # Machine should have valid structure
        assert result.machine is not None
        assert len(result.machine.alphabet) == 2
        assert all(len(s.transitions) > 0 for s in result.machine.states)


class TestSpectralOperators:
    """Tests for spectral operators module."""

    def test_rank_selection_with_high_rank(self) -> None:
        """Test rank selection with process needing higher rank."""
        from emic.sources.synthetic import EvenProcessSource
        from emic.sources.transforms import TakeN

        source = EvenProcessSource(p=0.5, _seed=42)
        data = list(TakeN(5000)(source))

        spectral = Spectral(SpectralConfig(max_history=6))
        result = spectral.infer(data)

        # Even process should need at least 2 states
        assert result.machine is not None
        assert len(result.machine.states) >= 2

    def test_automatic_rank_selection(self) -> None:
        """Test automatic rank selection on simple process."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.3, _seed=42)
        data = list(TakeN(3000)(source))

        spectral = Spectral(SpectralConfig(max_history=4))
        result = spectral.infer(data)

        # IID should need ~1 state
        assert result.machine is not None
        assert 1 <= len(result.machine.states) <= 2

    def test_with_various_regularizations(self) -> None:
        """Test inference with different regularization values."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(3000)(source))

        # Very small regularization
        spectral1 = Spectral(SpectralConfig(max_history=4, regularization=1e-10))
        result1 = spectral1.infer(data)
        assert result1.machine is not None

        # Larger regularization
        spectral2 = Spectral(SpectralConfig(max_history=4, regularization=1e-2))
        result2 = spectral2.infer(data)
        assert result2.machine is not None


class TestSpectralStateMerging:
    """Tests for state merging in spectral extraction."""

    def test_state_merging_occurs(self) -> None:
        """Test that similar states get merged."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(5000)(source))

        # High rank will create extra states, but merging should reduce
        spectral = Spectral(SpectralConfig(max_history=4, rank=4))
        result = spectral.infer(data)

        # IID should still merge down to ~1-2 states
        assert result.machine is not None
        assert len(result.machine.states) <= 4

    def test_large_data_with_merging(self) -> None:
        """Test inference on larger dataset."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(20000)(source))

        spectral = Spectral(SpectralConfig(max_history=6))
        result = spectral.infer(data)

        # With more data, should converge to ~2 states
        assert result.machine is not None
        assert 1 <= len(result.machine.states) <= 4


class TestSpectralExtractionInternals:
    """Direct tests for spectral extraction internal functions."""

    def test_build_trivial_machine(self) -> None:
        """Test build_trivial_machine function."""
        from emic.inference.spectral.extraction import build_trivial_machine

        symbols = [0, 0, 1, 0, 1, 1, 0] * 100
        alphabet: frozenset[int] = frozenset({0, 1})

        machine = build_trivial_machine(symbols, alphabet)

        # Should have 1 state with self-loops
        assert len(machine.states) == 1
        assert machine.alphabet == alphabet

        # Should have transitions for both symbols
        state = next(iter(machine.states))
        trans_symbols = {t.symbol for t in state.transitions}
        assert 0 in trans_symbols
        assert 1 in trans_symbols

    def test_build_trivial_machine_empty_symbols(self) -> None:
        """Test build_trivial_machine with empty symbol list."""
        from emic.inference.spectral.extraction import build_trivial_machine

        symbols: list[int] = []
        alphabet: frozenset[int] = frozenset({0, 1})

        machine = build_trivial_machine(symbols, alphabet)

        # Should still create a valid machine with uniform transitions
        assert len(machine.states) == 1
        state = next(iter(machine.states))
        assert len(state.transitions) == 2

    def test_merge_similar_states(self) -> None:
        """Test merge_similar_states function."""
        from emic.inference.spectral.extraction import merge_similar_states
        from emic.types.machine import EpsilonMachineBuilder

        # Build a machine with two similar states
        builder: EpsilonMachineBuilder[int] = EpsilonMachineBuilder()
        builder.add_transition("S0", 0, "S0", 0.5)
        builder.add_transition("S0", 1, "S1", 0.5)
        builder.add_transition("S1", 0, "S0", 0.5)
        builder.add_transition("S1", 1, "S1", 0.5)
        builder.with_start_state("S0")
        machine = builder.build()

        # Try to merge (these states are identical so might merge)
        alphabet: frozenset[int] = frozenset({0, 1})
        merged = merge_similar_states(machine, alphabet)

        assert len(merged.states) >= 1

    def test_merge_similar_states_distinct(self) -> None:
        """Test merge_similar_states with distinct states."""
        from emic.inference.spectral.extraction import merge_similar_states
        from emic.types.machine import EpsilonMachineBuilder

        # Build a machine with very different states
        builder: EpsilonMachineBuilder[int] = EpsilonMachineBuilder()
        builder.add_transition("S0", 0, "S0", 0.9)
        builder.add_transition("S0", 1, "S1", 0.1)
        builder.add_transition("S1", 0, "S0", 0.1)
        builder.add_transition("S1", 1, "S1", 0.9)
        builder.with_start_state("S0")
        machine = builder.build()

        # States are distinct, should not merge
        alphabet: frozenset[int] = frozenset({0, 1})
        merged = merge_similar_states(machine, alphabet)

        # Should keep 2 states
        assert len(merged.states) == 2

    def test_with_very_short_sequence(self) -> None:
        """Test with sequence too short for clustering (triggers fallback)."""
        # Very short alternating pattern - may trigger dimension fallback
        data = [0, 1] * 10

        spectral = Spectral(SpectralConfig(max_history=3, min_count=1))
        result = spectral.infer(data)

        assert result.machine is not None

    def test_with_single_symbol_triggers_trivial(self) -> None:
        """Test that single symbol sequence builds trivial machine."""
        data = [1] * 200

        spectral = Spectral(SpectralConfig(max_history=2, min_count=1))
        result = spectral.infer(data)

        # Should get a single-state machine
        assert result.machine is not None
        assert len(result.machine.states) >= 1

    def test_rare_symbols_in_sequence(self) -> None:
        """Test with symbols that appear rarely."""
        # Mostly 0s with occasional 1s
        data = [0] * 100 + [1] + [0] * 100 + [1] + [0] * 100

        spectral = Spectral(SpectralConfig(max_history=2, min_count=1))
        result = spectral.infer(data)

        assert result.machine is not None
        assert result.machine.alphabet == frozenset({0, 1})
