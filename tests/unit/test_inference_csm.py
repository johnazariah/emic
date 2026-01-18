"""Tests for CSM algorithm."""

from __future__ import annotations

import pytest

from emic.inference.csm import CSM, CSMConfig
from emic.inference.errors import InsufficientDataError
from emic.sources.synthetic.biased_coin import BiasedCoinSource
from emic.sources.synthetic.golden_mean import GoldenMeanSource
from emic.sources.synthetic.periodic import PeriodicSource
from emic.sources.transforms.take import TakeN


class TestCSMConfig:
    """Tests for CSMConfig."""

    def test_valid_config(self) -> None:
        """Valid configuration is accepted."""
        config = CSMConfig(history_length=5, merge_threshold=0.01)
        assert config.history_length == 5
        assert config.merge_threshold == 0.01

    def test_default_values(self) -> None:
        """Default configuration values are correct."""
        config = CSMConfig(history_length=5)
        assert config.merge_threshold == 0.05
        assert config.distance_metric == "kl"
        assert config.min_count == 5
        assert config.hierarchical is False

    def test_invalid_history_length(self) -> None:
        """history_length < 1 raises error."""
        with pytest.raises(ValueError, match="history_length must be >= 1"):
            CSMConfig(history_length=0)

    def test_invalid_merge_threshold(self) -> None:
        """merge_threshold <= 0 raises error."""
        with pytest.raises(ValueError, match="merge_threshold must be > 0"):
            CSMConfig(history_length=3, merge_threshold=0.0)
        with pytest.raises(ValueError, match="merge_threshold must be > 0"):
            CSMConfig(history_length=3, merge_threshold=-0.1)

    def test_invalid_min_count(self) -> None:
        """min_count < 1 raises error."""
        with pytest.raises(ValueError, match="min_count must be >= 1"):
            CSMConfig(history_length=3, min_count=0)

    def test_invalid_distance_metric(self) -> None:
        """Unknown distance_metric type raises error."""
        with pytest.raises(ValueError, match="distance_metric must be"):
            CSMConfig(history_length=3, distance_metric="unknown")  # type: ignore[arg-type]

    def test_all_valid_metrics(self) -> None:
        """All valid distance metrics are accepted."""
        for metric in ("kl", "hellinger", "tv", "chi2"):
            config = CSMConfig(history_length=3, distance_metric=metric)  # type: ignore[arg-type]
            assert config.distance_metric == metric


class TestCSMInference:
    """Tests for CSM inference."""

    def test_insufficient_data_raises_error(self) -> None:
        """Too few symbols raises InsufficientDataError."""
        config = CSMConfig(history_length=5, min_count=10)
        csm = CSM(config)

        with pytest.raises(InsufficientDataError):
            csm.infer([0, 1, 0, 1])

    def test_infer_biased_coin_single_state(self) -> None:
        """IID process (biased coin) should yield 1 state."""
        source = BiasedCoinSource(p=0.5, _seed=42)
        sequence = list(TakeN(5000)(source))

        config = CSMConfig(history_length=3, merge_threshold=0.1)
        result = CSM(config).infer(sequence)

        # IID process: all histories are predictively equivalent
        # So they should all merge into 1 state
        assert len(result.machine.states) == 1
        assert result.converged

    def test_infer_periodic_correct_states(self) -> None:
        """Periodic source should yield approximately correct number of states."""
        source = PeriodicSource(pattern=(0, 1, 0))
        sequence = list(TakeN(3000)(source))

        config = CSMConfig(history_length=5, merge_threshold=0.01, min_count=5)
        result = CSM(config).infer(sequence)

        # Period-3 pattern should yield ~3 states
        assert 2 <= len(result.machine.states) <= 5
        assert result.converged

    def test_infer_golden_mean_approximately_two_states(self) -> None:
        """Golden Mean should yield ~2 states with enough data."""
        source = GoldenMeanSource(p=0.5, _seed=123)
        sequence = list(TakeN(20000)(source))

        config = CSMConfig(history_length=5, merge_threshold=0.05)
        result = CSM(config).infer(sequence)

        # Should have 2-4 states (algorithm approximates)
        assert 2 <= len(result.machine.states) <= 4
        assert result.converged

    def test_result_has_diagnostics(self) -> None:
        """InferenceResult contains diagnostics."""
        source = BiasedCoinSource(p=0.5, _seed=42)
        sequence = list(TakeN(1000)(source))

        config = CSMConfig(history_length=3, merge_threshold=0.1)
        result = CSM(config).infer(sequence)

        assert result.sequence_length == 1000
        assert result.max_history_used == 3
        assert result.num_histories_considered > 0
        assert result.iterations is not None

    def test_pipeline_operator(self) -> None:
        """>> operator works with sources."""
        from emic.sources.empirical.sequence_data import SequenceData

        data = SequenceData.from_binary_string("0" * 500 + "1" * 500)

        config = CSMConfig(history_length=2, merge_threshold=0.1, min_count=3)
        result = data >> CSM(config)

        assert result.machine is not None
        assert result.converged


class TestDistanceMetrics:
    """Tests for different distance metrics."""

    def test_hellinger_metric(self) -> None:
        """Hellinger distance metric produces valid results."""
        source = BiasedCoinSource(p=0.5, _seed=42)
        sequence = list(TakeN(2000)(source))

        config = CSMConfig(history_length=3, merge_threshold=0.1, distance_metric="hellinger")
        result = CSM(config).infer(sequence)

        assert result.converged
        assert len(result.machine.states) >= 1

    def test_tv_metric(self) -> None:
        """Total variation distance metric produces valid results."""
        source = BiasedCoinSource(p=0.5, _seed=42)
        sequence = list(TakeN(2000)(source))

        config = CSMConfig(history_length=3, merge_threshold=0.1, distance_metric="tv")
        result = CSM(config).infer(sequence)

        assert result.converged
        assert len(result.machine.states) >= 1

    def test_chi2_metric(self) -> None:
        """Chi-squared distance metric produces valid results."""
        source = BiasedCoinSource(p=0.5, _seed=42)
        sequence = list(TakeN(2000)(source))

        config = CSMConfig(history_length=3, merge_threshold=0.5, distance_metric="chi2")
        result = CSM(config).infer(sequence)

        assert result.converged
        assert len(result.machine.states) >= 1


class TestCSMvsCSSR:
    """Tests comparing CSM and CSSR results."""

    def test_both_find_single_state_for_iid(self) -> None:
        """Both algorithms should find 1 state for IID process."""
        from emic.inference import CSSR, CSSRConfig

        source = BiasedCoinSource(p=0.5, _seed=42)
        sequence = list(TakeN(5000)(source))

        # CSM
        csm_config = CSMConfig(history_length=3, merge_threshold=0.1)
        csm_result = CSM(csm_config).infer(sequence)

        # CSSR
        cssr_config = CSSRConfig(max_history=3, significance=0.05)
        cssr_result = CSSR(cssr_config).infer(sequence)

        # Both should find 1 state
        assert len(csm_result.machine.states) == 1
        assert len(cssr_result.machine.states) == 1

    def test_both_find_similar_states_for_golden_mean(self) -> None:
        """Both algorithms should find similar number of states for Golden Mean."""
        from emic.inference import CSSR, CSSRConfig

        source = GoldenMeanSource(p=0.5, _seed=42)
        sequence = list(TakeN(20000)(source))

        # CSM
        csm_config = CSMConfig(history_length=5, merge_threshold=0.05)
        csm_result = CSM(csm_config).infer(sequence)

        # CSSR
        cssr_config = CSSRConfig(max_history=5, significance=0.01)
        cssr_result = CSSR(cssr_config).infer(sequence)

        # Both should find approximately 2 states (within some tolerance)
        assert 2 <= len(csm_result.machine.states) <= 4
        assert 2 <= len(cssr_result.machine.states) <= 4
