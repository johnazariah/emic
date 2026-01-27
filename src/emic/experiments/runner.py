"""
Benchmark runner with timeout handling and progress tracking.

Core execution engine that runs experiments and collects results.
"""

from __future__ import annotations

import platform
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from itertools import islice
from typing import TYPE_CHECKING, Any

from emic.analysis import entropy_rate, state_count, statistical_complexity
from emic.experiments.registry import (
    AlgorithmInfo,
    AlgorithmRegistry,
    ProcessInfo,
    ProcessRegistry,
    get_algorithm_registry,
    get_process_registry,
)
from emic.experiments.schema import BenchmarkResult, ResultsWriter, RunMetadata

if TYPE_CHECKING:
    from emic.experiments.config import ExperimentConfig, ExperimentsConfig


class TimeoutError(Exception):
    """Raised when a benchmark run exceeds the timeout."""

    pass


def _timeout_handler(_signum: int, _frame: Any) -> None:
    """Signal handler for timeout."""
    raise TimeoutError("Benchmark run timed out")


@dataclass
class RunProgress:
    """Track progress of benchmark runs."""

    total: int
    completed: int = 0
    failed: int = 0
    skipped: int = 0
    start_time: float | None = None

    def start(self) -> None:
        """Mark the start of benchmark runs."""
        self.start_time = time.perf_counter()

    def record_complete(self) -> None:
        """Record a completed run."""
        self.completed += 1

    def record_failed(self) -> None:
        """Record a failed run."""
        self.failed += 1

    def record_skipped(self) -> None:
        """Record a skipped run."""
        self.skipped += 1

    @property
    def elapsed(self) -> float:
        """Elapsed time in seconds."""
        if self.start_time is None:
            return 0.0
        return time.perf_counter() - self.start_time

    @property
    def done(self) -> int:
        """Total done (completed + failed + skipped)."""
        return self.completed + self.failed + self.skipped

    @property
    def remaining(self) -> int:
        """Remaining runs."""
        return self.total - self.done

    @property
    def eta_seconds(self) -> float | None:
        """Estimated time remaining in seconds."""
        if self.done == 0:
            return None
        avg_time = self.elapsed / self.done
        return avg_time * self.remaining

    def format_progress(self) -> str:
        """Format progress as a string."""
        pct = (self.done / self.total) * 100 if self.total > 0 else 0
        eta = self.eta_seconds
        eta_str = f" ETA: {eta:.0f}s" if eta is not None else ""
        return f"[{self.done}/{self.total}] {pct:.1f}%{eta_str}"


def get_git_info() -> tuple[str, bool]:
    """Get git commit hash and dirty status."""
    try:
        commit = (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
        dirty = (
            subprocess.call(["git", "diff", "--quiet"], stderr=subprocess.DEVNULL) != 0
            or subprocess.call(["git", "diff", "--cached", "--quiet"], stderr=subprocess.DEVNULL)
            != 0
        )
        return commit, dirty
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown", False


def get_emic_version() -> str:
    """Get emic package version."""
    import importlib.metadata

    try:
        return importlib.metadata.version("emic")
    except importlib.metadata.PackageNotFoundError:
        return "dev"


def run_single_benchmark(
    algorithm_info: AlgorithmInfo,
    process_info: ProcessInfo,
    n_samples: int,
    experiment_name: str,
    seed: int = 42,
    timeout_seconds: int = 120,
) -> list[BenchmarkResult]:
    """
    Run a single benchmark configuration.

    Args:
        algorithm_info: Algorithm to benchmark
        process_info: Process to generate data from
        n_samples: Number of samples to generate
        experiment_name: Name of the parent experiment
        seed: Random seed for reproducibility
        timeout_seconds: Maximum time for this run

    Returns:
        List of BenchmarkResult for each metric
    """
    results: list[BenchmarkResult] = []
    timestamp = datetime.now(UTC)
    error_message = None
    old_handler = None

    # Set up timeout (Unix only)
    has_alarm = hasattr(signal, "SIGALRM")
    if has_alarm:
        old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout_seconds)

    start_time = time.perf_counter()

    try:
        # Create source and generate data
        source = process_info.create_source(seed=seed)
        data = list(islice(source, n_samples))

        # Create algorithm and run inference
        config_overrides = {}
        algo = algorithm_info.create_algorithm(**config_overrides)
        result = algo.infer(data)

        # Extract machine
        machine = result.machine

        # Compute metrics
        duration = time.perf_counter() - start_time

        # State count
        n_states = state_count(machine)
        results.append(
            BenchmarkResult(
                experiment=experiment_name,
                algorithm=algorithm_info.name,
                process=process_info.name,
                n_samples=n_samples,
                metric="state_count",
                value=float(n_states),
                ground_truth=process_info.ground_truth.get("state_count"),
                timestamp=timestamp,
            )
        )

        # Statistical complexity (Cμ)
        cmu = statistical_complexity(machine)
        results.append(
            BenchmarkResult(
                experiment=experiment_name,
                algorithm=algorithm_info.name,
                process=process_info.name,
                n_samples=n_samples,
                metric="cmu",
                value=cmu,
                ground_truth=process_info.ground_truth.get("cmu"),
                timestamp=timestamp,
            )
        )

        # Entropy rate (hμ)
        hmu = entropy_rate(machine)
        results.append(
            BenchmarkResult(
                experiment=experiment_name,
                algorithm=algorithm_info.name,
                process=process_info.name,
                n_samples=n_samples,
                metric="hmu",
                value=hmu,
                ground_truth=process_info.ground_truth.get("hmu"),
                timestamp=timestamp,
            )
        )

        # Duration
        results.append(
            BenchmarkResult(
                experiment=experiment_name,
                algorithm=algorithm_info.name,
                process=process_info.name,
                n_samples=n_samples,
                metric="duration_s",
                value=duration,
                timestamp=timestamp,
            )
        )

    except TimeoutError:
        error_message = f"Timeout after {timeout_seconds}s"
    except Exception as e:
        error_message = str(e)
    finally:
        # Clear timeout
        if has_alarm and old_handler is not None:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)

    # If error, record error results
    if error_message is not None:
        duration = time.perf_counter() - start_time
        for metric in ["state_count", "cmu", "hmu", "duration_s"]:
            results.append(
                BenchmarkResult(
                    experiment=experiment_name,
                    algorithm=algorithm_info.name,
                    process=process_info.name,
                    n_samples=n_samples,
                    metric=metric,
                    value=float("nan"),
                    ground_truth=process_info.ground_truth.get(metric),
                    error=error_message,
                    timestamp=timestamp,
                )
            )

    return results


class ExperimentRunner:
    """
    Run benchmark experiments and collect results.

    Example:
        runner = ExperimentRunner()
        runner.run_all()  # Run all default experiments
        runner.run_experiment("accuracy")  # Run specific experiment

    Sharding example:
        runner = ExperimentRunner(shard=(0, 4))  # Run shard 0 of 4
    """

    def __init__(
        self,
        config: ExperimentsConfig | None = None,
        process_registry: ProcessRegistry | None = None,
        algorithm_registry: AlgorithmRegistry | None = None,
        output_dir: str | None = None,
        verbose: bool = True,
        shard: tuple[int, int] | None = None,
        algorithms_filter: list[str] | None = None,
    ):
        """
        Initialize the benchmark runner.

        Args:
            config: Benchmark configuration (uses defaults if None)
            process_registry: Process registry (uses defaults if None)
            algorithm_registry: Algorithm registry (uses defaults if None)
            output_dir: Override output directory
            verbose: Print progress to stdout
            shard: Optional (shard_index, total_shards) for parallel execution
            algorithms_filter: Optional list of algorithm names to run (overrides config)
        """
        from emic.experiments.config import create_default_config

        self.config = config or create_default_config()
        self.process_registry = process_registry or get_process_registry()
        self.algorithm_registry = algorithm_registry or get_algorithm_registry()
        self.output_dir = output_dir or self.config.output_dir
        self.verbose = verbose
        self.shard = shard
        self.algorithms_filter = algorithms_filter

        self.writer = ResultsWriter(self.output_dir, shard=shard)
        self.progress: RunProgress | None = None

    def _log(self, msg: str) -> None:
        """Print message if verbose."""
        if self.verbose:
            print(msg)

    def run_experiment(self, experiment: ExperimentConfig) -> list[BenchmarkResult]:
        """
        Run a single experiment.

        Args:
            experiment: Experiment configuration

        Returns:
            List of all results from the experiment
        """
        results: list[BenchmarkResult] = []

        # Get effective sample sizes
        if self.config.quick_mode:
            sample_sizes = self.config.quick_sample_sizes
        else:
            sample_sizes = experiment.sample_sizes

        # Get algorithms (skip slow in quick mode, filter if specified)
        algorithm_names = (
            self.algorithms_filter if self.algorithms_filter else experiment.algorithms
        )
        algorithms = []
        for name in algorithm_names:
            try:
                algo_info = self.algorithm_registry.get(name)
                if self.config.quick_mode and algo_info.slow:
                    self._log(f"  Skipping {name} (slow, quick mode)")
                    continue
                algorithms.append(algo_info)
            except KeyError:
                self._log(f"  Warning: Unknown algorithm {name}")

        # Get processes
        processes = []
        for name in experiment.processes:
            try:
                processes.append(self.process_registry.get(name))
            except KeyError:
                self._log(f"  Warning: Unknown process {name}")

        # Build flat list of all runs
        all_runs: list[tuple[AlgorithmInfo, ProcessInfo, int, int]] = []
        for algo_info in algorithms:
            for proc_info in processes:
                for n in sample_sizes:
                    reps = experiment.get_repetitions(n)
                    for rep in range(reps):
                        all_runs.append((algo_info, proc_info, n, rep))

        # Filter by shard if specified
        if self.shard is not None:
            shard_index, total_shards = self.shard
            all_runs = [run for i, run in enumerate(all_runs) if i % total_shards == shard_index]

        total_runs = len(all_runs)
        self.progress = RunProgress(total=total_runs)
        self.progress.start()

        self._log(f"\n=== {experiment.name}: {experiment.description} ===")
        if self.shard is not None:
            shard_index, total_shards = self.shard
            self._log(f"Shard {shard_index}/{total_shards}: {total_runs} runs")
        else:
            self._log(f"Total runs: {total_runs}")

        for algo_info, proc_info, n, rep in all_runs:
            seed = experiment.seed_offset + rep

            self._log(
                f"  {algo_info.name} x {proc_info.name} x N={n} {self.progress.format_progress()}"
            )

            run_results = run_single_benchmark(
                algorithm_info=algo_info,
                process_info=proc_info,
                n_samples=n,
                experiment_name=experiment.name,
                seed=seed,
                timeout_seconds=experiment.timeout_seconds,
            )

            results.extend(run_results)
            self.writer.add_results(run_results)

            # Check for errors
            if any(r.error for r in run_results):
                self.progress.record_failed()
            else:
                self.progress.record_complete()

        return results

    def run_all(self) -> list[BenchmarkResult]:
        """
        Run all experiments in the configuration.

        Returns:
            List of all results
        """
        all_results: list[BenchmarkResult] = []
        start_time = time.perf_counter()

        git_commit, git_dirty = get_git_info()

        self._log("=" * 60)
        self._log("EMIC Benchmark Suite")
        self._log("=" * 60)
        self._log(f"Output: {self.output_dir}")
        self._log(f"Quick mode: {self.config.quick_mode}")
        if self.shard is not None:
            shard_index, total_shards = self.shard
            self._log(f"Shard: {shard_index}/{total_shards}")
        self._log(f"Git: {git_commit}{' (dirty)' if git_dirty else ''}")

        for experiment in self.config.experiments:
            results = self.run_experiment(experiment)
            all_results.extend(results)

            # Incremental save after each experiment
            self.writer.save_incremental()

        # Finalize
        duration = time.perf_counter() - start_time
        metadata = RunMetadata(
            timestamp=self.writer.timestamp,
            git_commit=git_commit,
            git_dirty=git_dirty,
            python_version=platform.python_version(),
            emic_version=get_emic_version(),
            cli_args=sys.argv[1:],
            duration_seconds=duration,
            completed=True,
        )

        result_path = self.writer.finalize(metadata)

        self._log("")
        self._log("=" * 60)
        self._log(f"Complete! Duration: {duration:.1f}s")
        self._log(f"Results: {result_path}")
        self._log("=" * 60)

        return all_results

    def run_by_name(self, experiment_name: str) -> list[BenchmarkResult]:
        """
        Run a specific experiment by name.

        Args:
            experiment_name: Name of the experiment to run

        Returns:
            List of results from the experiment
        """
        import platform

        start_time = time.perf_counter()
        git_commit, git_dirty = get_git_info()

        self._log("=" * 60)
        self._log("EMIC Benchmark Suite")
        self._log("=" * 60)
        self._log(f"Output: {self.output_dir}")
        self._log(f"Quick mode: {self.config.quick_mode}")
        if self.shard is not None:
            shard_index, total_shards = self.shard
            self._log(f"Shard: {shard_index}/{total_shards}")
        self._log(f"Git: {git_commit}{' (dirty)' if git_dirty else ''}")

        experiment = self.config.get_experiment(experiment_name)
        results = self.run_experiment(experiment)

        # Finalize
        duration = time.perf_counter() - start_time
        metadata = RunMetadata(
            timestamp=self.writer.timestamp,
            git_commit=git_commit,
            git_dirty=git_dirty,
            python_version=platform.python_version(),
            emic_version=get_emic_version(),
            cli_args=sys.argv[1:],
            duration_seconds=duration,
            completed=True,
        )

        result_path = self.writer.finalize(metadata)

        self._log("")
        self._log("=" * 60)
        self._log(f"Complete! Duration: {duration:.1f}s")
        self._log(f"Results: {result_path}")
        self._log("=" * 60)

        return results
