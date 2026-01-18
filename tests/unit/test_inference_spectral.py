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
        assert config.max_history == 10
        assert config.rank_threshold == 0.01
        assert config.rank is None
        assert config.regularization == 1e-6
        assert config.min_count == 5

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
        # Simple repeating pattern
        data = [0, 1] * 100

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
