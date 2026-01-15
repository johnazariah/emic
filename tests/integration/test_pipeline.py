"""Integration tests for pipeline composition."""

from __future__ import annotations

from emic.analysis import analyze
from emic.inference import CSSR, CSSRConfig
from emic.pipeline import Pipeline, identity, tap
from emic.sources import BiasedCoinSource, GoldenMeanSource
from emic.sources.transforms import TakeN


class TestPipelineOperator:
    """Tests for the >> pipeline operator."""

    def test_source_to_transform(self) -> None:
        """Test Source >> Transform."""
        source = GoldenMeanSource(p=0.5, _seed=42)
        result = source >> TakeN(100)

        assert len(result) == 100
        assert all(s in {0, 1} for s in result)

    def test_source_to_transform_to_inference(self) -> None:
        """Test Source >> Transform >> Inference."""
        result = GoldenMeanSource(p=0.5, _seed=42) >> TakeN(5000) >> CSSR(CSSRConfig(max_history=3))

        assert result.converged
        assert len(list(result.machine.states)) >= 2

    def test_full_pipeline(self) -> None:
        """Test full pipeline Source >> Transform >> Inference >> Analysis."""
        result = GoldenMeanSource(p=0.5, _seed=42) >> TakeN(5000) >> CSSR(CSSRConfig(max_history=3))
        summary = analyze(result.machine)

        assert summary.num_states >= 2
        assert 0.5 <= summary.entropy_rate <= 0.8

    def test_different_sources(self) -> None:
        """Test pipeline works with different sources."""
        # Biased coin should infer ~1 state
        result = BiasedCoinSource(p=0.7, _seed=42) >> TakeN(5000) >> CSSR(CSSRConfig(max_history=3))
        summary = analyze(result.machine)

        # Biased coin is IID, should have few states
        assert summary.num_states <= 3


class TestTapHelper:
    """Tests for the tap debugging helper."""

    def test_tap_returns_input(self) -> None:
        """Test that tap returns input unchanged."""
        called = []

        def log(x: object) -> None:
            called.append(x)

        tapper = tap(log)
        result = tapper(42)

        assert result == 42
        assert called == [42]

    def test_tap_in_pipeline(self) -> None:
        """Test tap works in a pipeline."""
        log: list[str] = []

        source = GoldenMeanSource(p=0.5, _seed=42)
        transformed = source >> tap(lambda _: log.append("source")) >> TakeN(100)

        assert len(transformed) == 100
        assert log == ["source"]


class TestIdentity:
    """Tests for identity function."""

    def test_identity_returns_input(self) -> None:
        """Test identity returns input unchanged."""
        assert identity(42) == 42
        assert identity("hello") == "hello"
        assert identity([1, 2, 3]) == [1, 2, 3]


class TestPipelineBuilder:
    """Tests for Pipeline builder class."""

    def test_empty_pipeline(self) -> None:
        """Test empty pipeline returns initial value."""
        pipeline = Pipeline()
        result = pipeline.run(42)
        assert result == 42

    def test_single_stage(self) -> None:
        """Test pipeline with single stage."""
        pipeline = Pipeline().then(lambda x: x * 2)
        result = pipeline.run(21)
        assert result == 42

    def test_multiple_stages(self) -> None:
        """Test pipeline with multiple stages."""
        pipeline = Pipeline().then(lambda x: x + 1).then(lambda x: x * 2)
        result = pipeline.run(20)
        assert result == 42
