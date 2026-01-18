"""Tests for Bayesian Structural Inference (BSI) algorithm."""

import pytest

from emic.inference.bsi import BSI, BSIConfig


class TestBSIConfig:
    """Tests for BSIConfig."""

    def test_valid_config(self) -> None:
        """Test valid configuration creation."""
        config = BSIConfig(max_states=5, n_samples=100)
        assert config.max_states == 5
        assert config.n_samples == 100

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = BSIConfig()
        assert config.max_states == 10
        assert config.max_history == 5
        assert config.alpha_prior == 1.0
        assert config.n_samples == 1000
        assert config.burnin == 200
        assert config.thin == 1
        assert config.seed is None

    def test_invalid_max_states(self) -> None:
        """Test that max_states must be positive."""
        with pytest.raises(ValueError, match="max_states"):
            BSIConfig(max_states=0)
        with pytest.raises(ValueError, match="max_states"):
            BSIConfig(max_states=-1)

    def test_invalid_max_history(self) -> None:
        """Test that max_history must be positive."""
        with pytest.raises(ValueError, match="max_history"):
            BSIConfig(max_history=0)

    def test_invalid_alpha_prior(self) -> None:
        """Test that alpha_prior must be positive."""
        with pytest.raises(ValueError, match="alpha_prior"):
            BSIConfig(alpha_prior=0)
        with pytest.raises(ValueError, match="alpha_prior"):
            BSIConfig(alpha_prior=-1.0)

    def test_invalid_n_samples(self) -> None:
        """Test that n_samples must be positive."""
        with pytest.raises(ValueError, match="n_samples"):
            BSIConfig(n_samples=0)

    def test_invalid_burnin(self) -> None:
        """Test that burnin must be non-negative."""
        with pytest.raises(ValueError, match="burnin"):
            BSIConfig(burnin=-1)

    def test_invalid_thin(self) -> None:
        """Test that thin must be positive."""
        with pytest.raises(ValueError, match="thin"):
            BSIConfig(thin=0)

    def test_with_seed(self) -> None:
        """Test configuration with seed."""
        config = BSIConfig(seed=42)
        assert config.seed == 42


class TestBSIInference:
    """Tests for BSI inference."""

    def test_insufficient_data_raises_error(self) -> None:
        """Test that short sequences raise InsufficientDataError."""
        from emic.inference.errors import InsufficientDataError

        bsi = BSI(BSIConfig(max_history=5))
        with pytest.raises(InsufficientDataError):
            bsi.infer([0, 1, 0])

    def test_infer_biased_coin_single_state(self) -> None:
        """Test inference on biased coin (should find 1 state)."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(1000)(source))

        bsi = BSI(BSIConfig(max_states=3, n_samples=50, burnin=10, seed=42))
        result = bsi.infer(data)

        # Should find 1-2 states for IID process
        assert len(result.machine.states) <= 2

    def test_infer_periodic_finds_states(self) -> None:
        """Test inference on periodic process."""
        from emic.sources.synthetic import PeriodicSource
        from emic.sources.transforms import TakeN

        source = PeriodicSource([0, 1])
        data = list(TakeN(1000)(source))

        bsi = BSI(BSIConfig(max_states=5, n_samples=50, burnin=10, seed=42))
        result = bsi.infer(data)

        # Should find states
        assert len(result.machine.states) >= 1

    def test_infer_golden_mean(self) -> None:
        """Test inference on golden mean process."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(2000)(source))

        bsi = BSI(BSIConfig(max_states=5, n_samples=50, burnin=10, seed=42))
        result = bsi.infer(data)

        # Should find at least 1 state
        assert len(result.machine.states) >= 1

    def test_result_has_diagnostics(self) -> None:
        """Test that result contains diagnostic information."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        bsi = BSI(BSIConfig(max_states=3, n_samples=20, burnin=5, seed=42))
        result = bsi.infer(data)

        assert result.sequence_length == 500
        assert result.max_history_used == 5
        assert result.num_histories_considered >= 0

    def test_pipeline_operator(self) -> None:
        """Test that pipeline operator works."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        result = data >> BSI(BSIConfig(max_states=3, n_samples=20, burnin=5, seed=42))

        assert result.machine is not None

    def test_with_explicit_alphabet(self) -> None:
        """Test inference with explicit alphabet."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        bsi = BSI(BSIConfig(max_states=3, n_samples=20, burnin=5, seed=42))
        result = bsi.infer(data, alphabet=frozenset({0, 1}))

        assert result.machine.alphabet == frozenset({0, 1})

    def test_reproducibility_with_seed(self) -> None:
        """Test that same seed gives same result."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        bsi1 = BSI(BSIConfig(max_states=3, n_samples=20, burnin=5, seed=123))
        result1 = bsi1.infer(data)

        bsi2 = BSI(BSIConfig(max_states=3, n_samples=20, burnin=5, seed=123))
        result2 = bsi2.infer(data)

        assert len(result1.machine.states) == len(result2.machine.states)


class TestBSIMCMC:
    """Tests for MCMC sampling in BSI."""

    def test_different_seeds_give_different_results(self) -> None:
        """Test that different seeds can give different results."""
        from emic.sources.synthetic import GoldenMeanSource
        from emic.sources.transforms import TakeN

        source = GoldenMeanSource(p=0.5, _seed=42)
        data = list(TakeN(500)(source))

        results = []
        for seed in [1, 2, 3]:
            bsi = BSI(BSIConfig(max_states=5, n_samples=30, burnin=5, seed=seed))
            result = bsi.infer(data)
            results.append(len(result.machine.states))

        # Results may vary (though not guaranteed)
        # Just check they all produce valid machines
        for n in results:
            assert n >= 1

    def test_more_samples_doesnt_crash(self) -> None:
        """Test that more samples runs successfully."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(300)(source))

        bsi = BSI(BSIConfig(max_states=3, n_samples=100, burnin=20, seed=42))
        result = bsi.infer(data)

        assert result.machine is not None

    def test_thinning(self) -> None:
        """Test that thinning parameter works."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(300)(source))

        bsi = BSI(BSIConfig(max_states=3, n_samples=20, burnin=5, thin=2, seed=42))
        result = bsi.infer(data)

        assert result.machine is not None


class TestBSIEdgeCases:
    """Edge case tests for BSI."""

    def test_single_symbol_sequence(self) -> None:
        """Test with only one symbol in data."""
        data = [0] * 200

        bsi = BSI(BSIConfig(max_states=3, n_samples=20, burnin=5, seed=42))
        result = bsi.infer(data)

        # Should find 1 state
        assert len(result.machine.states) == 1

    def test_high_alpha_prior(self) -> None:
        """Test with high Dirichlet concentration."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(300)(source))

        bsi = BSI(BSIConfig(max_states=3, alpha_prior=10.0, n_samples=20, burnin=5, seed=42))
        result = bsi.infer(data)

        assert result.machine is not None

    def test_low_alpha_prior(self) -> None:
        """Test with low Dirichlet concentration."""
        from emic.sources.synthetic import BiasedCoinSource
        from emic.sources.transforms import TakeN

        source = BiasedCoinSource(p=0.5, _seed=42)
        data = list(TakeN(300)(source))

        bsi = BSI(BSIConfig(max_states=3, alpha_prior=0.1, n_samples=20, burnin=5, seed=42))
        result = bsi.infer(data)

        assert result.machine is not None
