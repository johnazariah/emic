"""Tests for CSSR algorithm."""

from __future__ import annotations

import pytest

from emic.inference import CSSR, CSSRConfig, InsufficientDataError
from emic.sources.synthetic.biased_coin import BiasedCoinSource
from emic.sources.synthetic.golden_mean import GoldenMeanSource
from emic.sources.synthetic.periodic import PeriodicSource
from emic.sources.transforms.take import TakeN


class TestCSSRConfig:
    """Tests for CSSRConfig."""

    def test_valid_config(self) -> None:
        """Valid configuration is accepted."""
        config = CSSRConfig(max_history=5, significance=0.01)
        assert config.max_history == 5
        assert config.significance == 0.01

    def test_invalid_max_history(self) -> None:
        """max_history < 1 raises error."""
        with pytest.raises(ValueError, match="max_history must be >= 1"):
            CSSRConfig(max_history=0)

    def test_invalid_significance(self) -> None:
        """significance outside (0, 1) raises error."""
        with pytest.raises(ValueError, match="significance must be in"):
            CSSRConfig(max_history=3, significance=0.0)
        with pytest.raises(ValueError, match="significance must be in"):
            CSSRConfig(max_history=3, significance=1.0)

    def test_invalid_min_count(self) -> None:
        """min_count < 1 raises error."""
        with pytest.raises(ValueError, match="min_count must be >= 1"):
            CSSRConfig(max_history=3, min_count=0)

    def test_invalid_test(self) -> None:
        """Unknown test type raises error."""
        with pytest.raises(ValueError, match="test must be"):
            CSSRConfig(max_history=3, test="unknown")


class TestCSSRInference:
    """Tests for CSSR inference."""

    def test_insufficient_data_raises_error(self) -> None:
        """Too few symbols raises InsufficientDataError."""
        config = CSSRConfig(max_history=5, min_count=10)
        cssr = CSSR(config)

        with pytest.raises(InsufficientDataError):
            cssr.infer([0, 1, 0, 1])

    def test_infer_biased_coin_single_state(self) -> None:
        """IID process (biased coin) should yield 1 state."""
        source = BiasedCoinSource(p=0.5, _seed=42)
        sequence = list(TakeN(5000)(source))

        config = CSSRConfig(max_history=3, significance=0.05)
        result = CSSR(config).infer(sequence)

        # IID process has exactly 1 state
        assert len(result.machine.states) == 1
        assert result.converged

    def test_infer_periodic_correct_states(self) -> None:
        """Periodic source should yield approximately correct number of states."""
        source = PeriodicSource(pattern=(0, 1, 0))
        sequence = list(TakeN(3000)(source))

        config = CSSRConfig(max_history=5, significance=0.01, min_count=5)
        result = CSSR(config).infer(sequence)

        # Period-3 pattern should yield ~3 states (algorithm may over-split slightly)
        assert 2 <= len(result.machine.states) <= 5
        assert result.converged

    def test_infer_golden_mean_approximately_two_states(self) -> None:
        """Golden Mean should yield ~2 states with enough data."""
        source = GoldenMeanSource(p=0.5, _seed=123)
        sequence = list(TakeN(20000)(source))

        config = CSSRConfig(max_history=5, significance=0.01)
        result = CSSR(config).infer(sequence)

        # Should have 2-3 states (algorithm approximates)
        assert 2 <= len(result.machine.states) <= 4
        assert result.converged

    def test_result_has_diagnostics(self) -> None:
        """InferenceResult contains diagnostics."""
        source = BiasedCoinSource(p=0.5, _seed=42)
        sequence = list(TakeN(1000)(source))

        config = CSSRConfig(max_history=3)
        result = CSSR(config).infer(sequence)

        assert result.sequence_length == 1000
        assert result.max_history_used == 3
        assert result.num_histories_considered > 0
        assert result.iterations is not None

    def test_pipeline_operator(self) -> None:
        """>> operator works with sources."""
        from emic.sources.empirical.sequence_data import SequenceData

        data = SequenceData.from_binary_string("0" * 500 + "1" * 500)

        config = CSSRConfig(max_history=2, significance=0.05, min_count=3)
        result = data >> CSSR(config)

        assert result.machine is not None
        assert result.converged


class TestCSSRMachineProperties:
    """Tests for properties of inferred machines."""

    def test_inferred_machine_is_valid(self) -> None:
        """Inferred machine passes validation."""
        source = BiasedCoinSource(p=0.7, _seed=42)
        sequence = list(TakeN(3000)(source))

        config = CSSRConfig(max_history=3, significance=0.05)
        result = CSSR(config).infer(sequence)

        # If we got here, machine was validated at construction
        assert result.machine is not None
        assert len(result.machine.alphabet) == 2

    def test_inferred_machine_has_correct_alphabet(self) -> None:
        """Inferred machine has correct alphabet."""
        source = PeriodicSource(pattern=("a", "b", "c"))
        sequence = list(TakeN(500)(source))

        config = CSSRConfig(max_history=4, min_count=3)
        result = CSSR(config).infer(sequence)

        assert result.machine.alphabet == frozenset({"a", "b", "c"})
