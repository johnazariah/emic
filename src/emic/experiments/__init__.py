"""
Experiments module for emic.

Provides systematic experimentation and benchmarking of epsilon-machine
inference algorithms.

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
    - ExperimentsConfig: Top-level configuration
    - load_config: Load YAML configuration

    - ExperimentRunner: Main runner class
    - run_single_benchmark: Run a single benchmark

Example:
    from emic.experiments import ExperimentRunner

    runner = ExperimentRunner()
    runner.run_all()

CLI:
    emic-experiment --all
    emic-experiment accuracy --quick
"""

from emic.experiments.config import (
    ExperimentConfig,
    ExperimentsConfig,
    load_config,
)
from emic.experiments.registry import (
    AlgorithmInfo,
    AlgorithmRegistry,
    ProcessInfo,
    ProcessRegistry,
    get_algorithm_registry,
    get_process_registry,
)
from emic.experiments.runner import (
    ExperimentRunner,
    run_single_benchmark,
)
from emic.experiments.schema import (
    BenchmarkResult,
    ResultsWriter,
    RunMetadata,
    read_latest_results,
    read_results,
)

__all__ = [
    "AlgorithmInfo",
    "AlgorithmRegistry",
    "BenchmarkResult",
    "ExperimentConfig",
    "ExperimentRunner",
    "ExperimentsConfig",
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
