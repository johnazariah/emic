"""
Benchmarking module for emic.

Provides systematic benchmarking of epsilon-machine inference algorithms.

Public API:
    - BenchmarkResult: Single measurement dataclass
    - RunMetadata: Run context dataclass
    - ResultsWriter: Write results to disk
    - read_results: Read Parquet/JSON results
    - read_latest_results: Read from 'latest' symlink

    - ProcessRegistry: Register data sources
    - AlgorithmRegistry: Register inference algorithms
    - get_process_registry: Default process registry
    - get_algorithm_registry: Default algorithm registry

    - ExperimentConfig: Single experiment configuration
    - BenchmarkConfig: Top-level configuration
    - load_config: Load YAML configuration

    - BenchmarkRunner: Main runner class
    - run_single_benchmark: Run a single benchmark

Example:
    from emic.benchmarks import BenchmarkRunner

    runner = BenchmarkRunner()
    runner.run_all()

CLI:
    emic-benchmark --all
    emic-benchmark accuracy --quick
"""

from emic.benchmarks.config import (
    BenchmarkConfig,
    ExperimentConfig,
    load_config,
)
from emic.benchmarks.registry import (
    AlgorithmInfo,
    AlgorithmRegistry,
    ProcessInfo,
    ProcessRegistry,
    get_algorithm_registry,
    get_process_registry,
)
from emic.benchmarks.runner import (
    BenchmarkRunner,
    run_single_benchmark,
)
from emic.benchmarks.schema import (
    BenchmarkResult,
    ResultsWriter,
    RunMetadata,
    read_latest_results,
    read_results,
)

__all__ = [
    "AlgorithmInfo",
    "AlgorithmRegistry",
    "BenchmarkConfig",
    "BenchmarkResult",
    "BenchmarkRunner",
    "ExperimentConfig",
    "ProcessInfo",
    "ProcessRegistry",
    "ResultsWriter",
    "RunMetadata",
    "get_algorithm_registry",
    "get_process_registry",
    "load_config",
    "read_latest_results",
    "read_results",
    "run_single_benchmark",
]
