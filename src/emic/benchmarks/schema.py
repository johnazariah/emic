"""
Data schema for benchmark results.

Provides standardized result types and Parquet I/O for benchmark data collection.
Downstream consumers (papers, CI, notebooks) read this format.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


@dataclass(frozen=True)
class BenchmarkResult:
    """
    A single benchmark measurement.

    Represents one algorithm run on one process configuration,
    measuring one metric. Multiple BenchmarkResults form a complete
    benchmark run.

    Attributes:
        experiment: Experiment identifier (e.g., "accuracy", "convergence")
        algorithm: Algorithm name (e.g., "cssr", "spectral", "bsi")
        process: Process name (e.g., "even_process", "golden_mean")
        n_samples: Number of samples used for inference
        metric: Metric name (e.g., "cmu", "hmu", "state_count", "duration_s")
        value: Measured value
        ground_truth: Expected value if known, None otherwise
        error: Exception message if run failed, None otherwise
        timestamp: When this measurement was recorded
    """

    experiment: str
    algorithm: str
    process: str
    n_samples: int
    metric: str
    value: float
    ground_truth: float | None = None
    error: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        """Convert to dictionary for DataFrame construction."""
        d = asdict(self)
        # Convert datetime to ISO string for Parquet compatibility
        d["timestamp"] = self.timestamp.isoformat()
        return d


@dataclass(frozen=True)
class RunMetadata:
    """
    Metadata for a complete benchmark run.

    Captures environment and configuration for reproducibility.

    Attributes:
        timestamp: When the run started
        git_commit: Git commit hash (short form)
        git_dirty: Whether working directory had uncommitted changes
        python_version: Python version string
        emic_version: emic package version
        cli_args: Command-line arguments used
        duration_seconds: Total run duration
        completed: Whether all experiments finished successfully
    """

    timestamp: datetime
    git_commit: str
    git_dirty: bool
    python_version: str
    emic_version: str
    cli_args: list[str]
    duration_seconds: float | None = None
    completed: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "git_commit": self.git_commit,
            "git_dirty": self.git_dirty,
            "python_version": self.python_version,
            "emic_version": self.emic_version,
            "cli_args": self.cli_args,
            "duration_seconds": self.duration_seconds,
            "completed": self.completed,
        }


class ResultsWriter:
    """
    Write benchmark results to disk.

    Creates timestamped directories with Parquet data and YAML metadata.
    Updates a 'latest' symlink for convenient access.

    Example:
        writer = ResultsWriter(base_dir="experiments/results")
        writer.add_result(result1)
        writer.add_result(result2)
        writer.finalize(metadata)
        # Creates: experiments/results/2026-01-26T14-32-05/
        #          ├── metadata.yaml
        #          └── results.parquet
    """

    def __init__(self, base_dir: str | Path) -> None:
        """
        Initialize writer with output directory.

        Args:
            base_dir: Base directory for results (e.g., "experiments/results")
        """
        self.base_dir = Path(base_dir)
        self.timestamp = datetime.now(UTC)
        self.results: list[BenchmarkResult] = []
        self._run_dir: Path | None = None

    @property
    def run_dir(self) -> Path:
        """Get the timestamped directory for this run."""
        if self._run_dir is None:
            # Format: YYYY-MM-DDTHH-MM-SS (filesystem-safe ISO)
            dirname = self.timestamp.strftime("%Y-%m-%dT%H-%M-%S")
            self._run_dir = self.base_dir / dirname
        return self._run_dir

    def add_result(self, result: BenchmarkResult) -> None:
        """Add a single result to the collection."""
        self.results.append(result)

    def add_results(self, results: list[BenchmarkResult]) -> None:
        """Add multiple results to the collection."""
        self.results.extend(results)

    def save_incremental(self) -> None:
        """
        Save current results incrementally.

        Useful for long-running benchmarks to preserve partial results.
        """
        if not self.results:
            return
        self._ensure_run_dir()
        self._write_parquet(self.run_dir / "results.parquet")

    def finalize(self, metadata: RunMetadata) -> Path:
        """
        Write final results and metadata, update 'latest' symlink.

        Args:
            metadata: Run metadata to save

        Returns:
            Path to the results directory
        """
        self._ensure_run_dir()

        # Write results
        if self.results:
            self._write_parquet(self.run_dir / "results.parquet")

        # Write metadata
        self._write_metadata(metadata)

        # Update latest symlink
        self._update_latest_symlink()

        return self.run_dir

    def _ensure_run_dir(self) -> None:
        """Create the run directory if it doesn't exist."""
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def _write_parquet(self, path: Path) -> None:
        """Write results to Parquet file."""
        try:
            import pandas as pd

            df = pd.DataFrame([r.to_dict() for r in self.results])
            try:
                df.to_parquet(path, index=False)
            except ImportError:
                # pyarrow not available, fall back to JSON
                self._write_json(path.with_suffix(".json"))
        except ImportError:
            # pandas not available, fall back to JSON
            self._write_json(path.with_suffix(".json"))

    def _write_json(self, path: Path) -> None:
        """Write results to JSON file."""
        import json

        with path.open("w") as f:
            json.dump([r.to_dict() for r in self.results], f, indent=2)

    def _write_metadata(self, metadata: RunMetadata) -> None:
        """Write metadata to YAML file."""
        import yaml

        meta_path = self.run_dir / "metadata.yaml"
        with meta_path.open("w") as f:
            yaml.dump(metadata.to_dict(), f, default_flow_style=False, sort_keys=False)

    def _update_latest_symlink(self) -> None:
        """Update the 'latest' symlink to point to this run."""
        latest = self.base_dir / "latest"

        # Remove existing symlink
        if latest.is_symlink():
            latest.unlink()
        elif latest.exists():
            # Not a symlink - don't overwrite
            return

        # Create relative symlink
        latest.symlink_to(self.run_dir.name)


def read_results(path: str | Path) -> pd.DataFrame:
    """
    Read benchmark results from Parquet or JSON.

    Args:
        path: Path to results.parquet or results.json

    Returns:
        DataFrame with benchmark results
    """
    import pandas as pd

    path = Path(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    elif path.suffix == ".json":
        import json

        with path.open() as f:
            data = json.load(f)
        return pd.DataFrame(data)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def read_latest_results(base_dir: str | Path) -> pd.DataFrame:
    """
    Read results from the 'latest' run.

    Args:
        base_dir: Base results directory (e.g., "experiments/results")

    Returns:
        DataFrame with benchmark results
    """
    base = Path(base_dir)
    latest = base / "latest"

    if not latest.exists():
        raise FileNotFoundError(f"No 'latest' results found in {base}")

    # Try parquet first, then JSON
    parquet_path = latest / "results.parquet"
    if parquet_path.exists():
        return read_results(parquet_path)

    json_path = latest / "results.json"
    if json_path.exists():
        return read_results(json_path)

    raise FileNotFoundError(f"No results file found in {latest}")
