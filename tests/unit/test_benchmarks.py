"""Tests for the benchmarks module."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


class TestBenchmarkResult:
    """Tests for BenchmarkResult dataclass."""

    def test_create_result(self) -> None:
        """Test creating a benchmark result."""
        from emic.benchmarks.schema import BenchmarkResult

        result = BenchmarkResult(
            experiment="accuracy",
            algorithm="cssr",
            process="even_process",
            n_samples=1000,
            metric="state_count",
            value=2.0,
            ground_truth=2.0,
        )

        assert result.experiment == "accuracy"
        assert result.algorithm == "cssr"
        assert result.process == "even_process"
        assert result.n_samples == 1000
        assert result.metric == "state_count"
        assert result.value == 2.0
        assert result.ground_truth == 2.0
        assert result.error is None

    def test_result_with_error(self) -> None:
        """Test creating a result with an error."""
        from emic.benchmarks.schema import BenchmarkResult

        result = BenchmarkResult(
            experiment="accuracy",
            algorithm="cssr",
            process="even_process",
            n_samples=1000,
            metric="state_count",
            value=float("nan"),
            error="Timeout after 120s",
        )

        assert result.error == "Timeout after 120s"

    def test_to_dict(self) -> None:
        """Test converting result to dict."""
        from emic.benchmarks.schema import BenchmarkResult

        result = BenchmarkResult(
            experiment="accuracy",
            algorithm="cssr",
            process="even_process",
            n_samples=1000,
            metric="state_count",
            value=2.0,
        )

        d = result.to_dict()
        assert d["experiment"] == "accuracy"
        assert d["algorithm"] == "cssr"
        assert isinstance(d["timestamp"], str)  # ISO format


class TestProcessRegistry:
    """Tests for ProcessRegistry."""

    def test_default_registry(self) -> None:
        """Test default process registry has expected processes."""
        from emic.benchmarks.registry import get_process_registry

        registry = get_process_registry()

        assert "even_process" in registry.list()
        assert "golden_mean" in registry.list()
        assert "biased_coin" in registry.list()

    def test_get_process(self) -> None:
        """Test getting a process by name."""
        from emic.benchmarks.registry import get_process_registry

        registry = get_process_registry()
        process = registry.get("even_process")

        assert process.name == "even_process"
        assert process.display_name == "Even Process"
        assert "state_count" in process.ground_truth
        assert process.ground_truth["state_count"] == 2

    def test_create_source(self) -> None:
        """Test creating a source from registry."""
        from itertools import islice

        from emic.benchmarks.registry import get_process_registry

        registry = get_process_registry()
        process = registry.get("even_process")
        source = process.create_source(seed=42)

        # Take some samples (sources are iterable, not iterators)
        samples = list(islice(source, 10))
        assert len(samples) == 10
        assert all(s in (0, 1) for s in samples)

    def test_unknown_process(self) -> None:
        """Test that unknown process raises KeyError."""
        from emic.benchmarks.registry import get_process_registry

        registry = get_process_registry()

        with pytest.raises(KeyError):
            registry.get("unknown_process")


class TestAlgorithmRegistry:
    """Tests for AlgorithmRegistry."""

    def test_default_registry(self) -> None:
        """Test default algorithm registry has expected algorithms."""
        from emic.benchmarks.registry import get_algorithm_registry

        registry = get_algorithm_registry()

        assert "cssr" in registry.list()
        assert "spectral" in registry.list()
        assert "csm" in registry.list()
        assert "bsi" in registry.list()

    def test_get_algorithm(self) -> None:
        """Test getting an algorithm by name."""
        from emic.benchmarks.registry import get_algorithm_registry

        registry = get_algorithm_registry()
        algo = registry.get("cssr")

        assert algo.name == "cssr"
        assert algo.display_name == "CSSR"
        assert algo.slow is False

    def test_bsi_is_slow(self) -> None:
        """Test that BSI is marked as slow."""
        from emic.benchmarks.registry import get_algorithm_registry

        registry = get_algorithm_registry()
        bsi = registry.get("bsi")

        assert bsi.slow is True

    def test_list_excluding_slow(self) -> None:
        """Test listing algorithms excluding slow ones."""
        from emic.benchmarks.registry import get_algorithm_registry

        registry = get_algorithm_registry()
        fast_algos = registry.list(include_slow=False)

        assert "bsi" not in fast_algos
        assert "cssr" in fast_algos


class TestExperimentConfig:
    """Tests for ExperimentConfig."""

    def test_default_config(self) -> None:
        """Test creating default config."""
        from emic.benchmarks.config import ExperimentConfig

        config = ExperimentConfig(name="test")

        assert config.name == "test"
        assert len(config.algorithms) > 0
        assert len(config.processes) > 0
        assert len(config.sample_sizes) > 0

    def test_total_runs(self) -> None:
        """Test calculating total runs."""
        from emic.benchmarks.config import ExperimentConfig

        config = ExperimentConfig(
            name="test",
            algorithms=["cssr", "spectral"],
            processes=["even_process"],
            sample_sizes=[1000, 5000],
            repetitions=3,
        )

        # 2 algorithms * 1 process * 2 sample sizes * 3 reps = 12
        assert config.total_runs == 12


class TestResultsWriter:
    """Tests for ResultsWriter."""

    def test_write_results(self) -> None:
        """Test writing results creates expected files."""
        from datetime import UTC, datetime

        from emic.benchmarks.schema import BenchmarkResult, ResultsWriter, RunMetadata

        with tempfile.TemporaryDirectory() as tmpdir:
            writer = ResultsWriter(tmpdir)

            # Add a result
            result = BenchmarkResult(
                experiment="test",
                algorithm="cssr",
                process="even_process",
                n_samples=1000,
                metric="state_count",
                value=2.0,
            )
            writer.add_result(result)

            # Finalize
            metadata = RunMetadata(
                timestamp=datetime.now(UTC),
                git_commit="abc123",
                git_dirty=False,
                python_version="3.11.0",
                emic_version="0.3.1",
                cli_args=["--quick"],
                duration_seconds=1.0,
                completed=True,
            )
            result_path = writer.finalize(metadata)

            # Check files exist
            assert (result_path / "metadata.yaml").exists()
            # Either parquet or json should exist
            assert (result_path / "results.parquet").exists() or (
                result_path / "results.json"
            ).exists()

            # Check latest symlink
            latest = Path(tmpdir) / "latest"
            assert latest.is_symlink()


class TestRunSingleBenchmark:
    """Tests for run_single_benchmark function."""

    def test_run_benchmark(self) -> None:
        """Test running a single benchmark."""
        from emic.benchmarks.registry import get_algorithm_registry, get_process_registry
        from emic.benchmarks.runner import run_single_benchmark

        proc_registry = get_process_registry()
        algo_registry = get_algorithm_registry()

        process = proc_registry.get("biased_coin")  # Simplest process
        algorithm = algo_registry.get("cssr")

        results = run_single_benchmark(
            algorithm_info=algorithm,
            process_info=process,
            n_samples=500,
            experiment_name="test",
            seed=42,
            timeout_seconds=30,
        )

        # Should have 4 metrics
        assert len(results) == 4
        metrics = {r.metric for r in results}
        assert metrics == {"state_count", "cmu", "hmu", "duration_s"}

        # Check no errors
        assert all(r.error is None for r in results)

        # Biased coin should have 1 state (but CSSR may find 2 at small N)
        state_count_result = next(r for r in results if r.metric == "state_count")
        # Ground truth is 1, but algorithm might find 1-2 with limited data
        assert state_count_result.ground_truth == 1
        assert 1 <= state_count_result.value <= 3  # Reasonable range


class TestCLI:
    """Tests for CLI module."""

    def test_parser_help(self) -> None:
        """Test parser creation."""
        from emic.benchmarks.cli import create_parser

        parser = create_parser()
        # Should not raise
        assert parser is not None

    def test_list_experiments(self, capsys: pytest.CaptureFixture) -> None:
        """Test --list command."""
        from emic.benchmarks.cli import list_experiments

        list_experiments()
        captured = capsys.readouterr()

        assert "accuracy" in captured.out
        assert "convergence" in captured.out
        assert "scalability" in captured.out
