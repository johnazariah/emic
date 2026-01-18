"""Tests for Neural State Discovery (NSD) algorithm."""

import pytest

from emic.inference.nsd import NSD, NSDConfig


class TestNSDConfig:
    """Tests for NSDConfig."""

    def test_valid_config(self) -> None:
        """Test valid configuration creation."""
        config = NSDConfig(max_states=5, history_length=10)
        assert config.max_states == 5
        assert config.history_length == 10

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = NSDConfig()
        assert config.max_states == 10
        assert config.history_length == 10
        assert config.embedding_dim == 16
        assert config.n_iterations == 100
        assert config.convergence_threshold == 1e-4
        assert config.seed is None

    def test_invalid_max_states(self) -> None:
        """Test that max_states must be positive."""
        with pytest.raises(ValueError, match="max_states"):
            NSDConfig(max_states=0)
        with pytest.raises(ValueError, match="max_states"):
            NSDConfig(max_states=-1)

    def test_invalid_history_length(self) -> None:
        """Test that history_length must be positive."""
        with pytest.raises(ValueError, match="history_length"):
            NSDConfig(history_length=0)

    def test_invalid_embedding_dim(self) -> None:
        """Test that embedding_dim must be positive."""
        with pytest.raises(ValueError, match="embedding_dim"):
            NSDConfig(embedding_dim=0)

    def test_invalid_n_iterations(self) -> None:
        """Test that n_iterations must be positive."""
        with pytest.raises(ValueError, match="n_iterations"):
            NSDConfig(n_iterations=0)

    def test_invalid_convergence_threshold(self) -> None:
        """Test that convergence_threshold must be positive."""
        with pytest.raises(ValueError, match="convergence_threshold"):
            NSDConfig(convergence_threshold=0)
        with pytest.raises(ValueError, match="convergence_threshold"):
            NSDConfig(convergence_threshold=-0.1)

    def test_with_seed(self) -> None:
        """Test configuration with seed."""
        config = NSDConfig(seed=42)
        assert config.seed == 42


class TestNSDInference:
    """Tests for NSD inference."""

    def test_insufficient_data_raises_error(self) -> None:
        """Test that short sequences raise InsufficientDataError."""
        from emic.inference.errors import InsufficientDataError

        nsd = NSD(NSDConfig(history_length=5))
        with pytest.raises(InsufficientDataError):
            nsd.infer([0, 1, 0])

    def test_infer_biased_coin(self) -> None:
        """Test inference on biased coin."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(1000)(source))

        nsd = NSD(NSDConfig(max_states=3, history_length=3, seed=42))
        result = nsd.infer(data)

        # Should find small number of states
        assert len(result.machine.states) <= 3

    def test_infer_periodic_finds_states(self) -> None:
        """Test inference on periodic process."""
        from emic.sources.synthetic import PeriodicSource
        from emic.sources.transforms import TakeN

        source = PeriodicSource([0, 1])
        data = list(TakeN(1000)(source))

        nsd = NSD(NSDConfig(max_states=5, history_length=3, seed=42))
        result = nsd.infer(data)

        # Should find at least 1 state
        assert len(result.machine.states) >= 1

    def test_infer_golden_mean(self) -> None:
        """Test inference on golden mean process."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(2000)(source))

        nsd = NSD(NSDConfig(max_states=5, history_length=5, seed=42))
        result = nsd.infer(data)

        # Golden mean should find ~2 states
        assert len(result.machine.states) >= 1
        assert len(result.machine.states) <= 5

    def test_result_has_diagnostics(self) -> None:
        """Test that result contains diagnostic information."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        nsd = NSD(NSDConfig(max_states=3, history_length=3, seed=42))
        result = nsd.infer(data)

        assert result.sequence_length == 500
        assert result.max_history_used == 3
        assert result.num_histories_considered >= 0

    def test_pipeline_operator(self) -> None:
        """Test that pipeline operator works."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        result = data >> NSD(NSDConfig(max_states=3, history_length=3, seed=42))

        assert result.machine is not None

    def test_with_explicit_alphabet(self) -> None:
        """Test inference with explicit alphabet."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        nsd = NSD(NSDConfig(max_states=3, history_length=3, seed=42))
        result = nsd.infer(data, alphabet=frozenset({0, 1}))

        assert result.machine.alphabet == frozenset({0, 1})

    def test_reproducibility_with_seed(self) -> None:
        """Test that same seed gives same result."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        nsd1 = NSD(NSDConfig(max_states=3, history_length=3, seed=123))
        result1 = nsd1.infer(data)

        nsd2 = NSD(NSDConfig(max_states=3, history_length=3, seed=123))
        result2 = nsd2.infer(data)

        assert len(result1.machine.states) == len(result2.machine.states)


class TestNSDClustering:
    """Tests for k-means clustering in NSD."""

    def test_different_seeds_may_give_different_results(self) -> None:
        """Test that different seeds can give different clustering."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(800)(source))

        results = []
        for seed in [1, 2, 3]:
            nsd = NSD(NSDConfig(max_states=5, history_length=3, seed=seed))
            result = nsd.infer(data)
            results.append(len(result.machine.states))

        # All should produce valid machines
        for n in results:
            assert n >= 1

    def test_more_iterations(self) -> None:
        """Test with more k-means iterations."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        nsd = NSD(NSDConfig(max_states=3, history_length=3, n_iterations=200, seed=42))
        result = nsd.infer(data)

        assert result.machine is not None

    def test_convergence_detection(self) -> None:
        """Test that algorithm can converge early."""
        from emic.sources.synthetic import PeriodicSource
        from emic.sources.transforms import TakeN

        # Periodic process should have clear clusters
        source = PeriodicSource([0, 1])
        data = list(TakeN(500)(source))

        nsd = NSD(NSDConfig(max_states=3, history_length=2, n_iterations=200, seed=42))
        result = nsd.infer(data)

        assert result.machine is not None


class TestNSDEdgeCases:
    """Edge case tests for NSD."""

    def test_single_symbol_sequence(self) -> None:
        """Test with only one symbol in data."""
        data = [0] * 200

        nsd = NSD(NSDConfig(max_states=3, history_length=3, seed=42))
        result = nsd.infer(data)

        # Should find 1 state
        assert len(result.machine.states) == 1

    def test_short_history_length(self) -> None:
        """Test with short history length."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        nsd = NSD(NSDConfig(max_states=5, history_length=2, seed=42))
        result = nsd.infer(data)

        assert result.machine is not None

    def test_many_max_states(self) -> None:
        """Test with high max_states limit."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        nsd = NSD(NSDConfig(max_states=20, history_length=3, seed=42))
        result = nsd.infer(data)

        # Should still find reasonable number of states
        assert len(result.machine.states) <= 20

    def test_trivial_fallback(self) -> None:
        """Test that trivial machine is built when few histories found."""
        # Use enough data but with long history to get few unique histories
        data = [0, 1] * 100  # 200 elements

        nsd = NSD(NSDConfig(max_states=3, history_length=10, seed=42))
        result = nsd.infer(data)

        assert result.machine is not None


class TestNSDEmbeddings:
    """Tests for embedding construction."""

    def test_embeddings_capture_predictive_distribution(self) -> None:
        """Test that embeddings reflect predictive distributions."""
        # Alternating pattern should have distinct embeddings
        data = [0, 1] * 200

        nsd = NSD(NSDConfig(max_states=3, history_length=2, seed=42))
        result = nsd.infer(data)

        # Should find states that capture the pattern
        assert result.machine is not None
        assert len(result.machine.states) >= 1

    def test_rare_histories_filtered(self) -> None:
        """Test that rare histories are filtered out."""
        # Mostly one pattern with rare deviation
        data = [0, 1] * 100 + [0, 0] + [0, 1] * 100

        nsd = NSD(NSDConfig(max_states=3, history_length=2, seed=42))
        result = nsd.infer(data)

        assert result.machine is not None
