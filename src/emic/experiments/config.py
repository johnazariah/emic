"""
Experiment configuration parsing.

Provides YAML-based experiment configuration with sensible defaults.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ExperimentConfig:
    """
    Configuration for a single experiment.

    Attributes:
        name: Experiment identifier (e.g., "accuracy")
        description: Human-readable description
        algorithms: List of algorithm names to benchmark
        processes: List of process names to test
        sample_sizes: List of N values for data generation
        metrics: List of metrics to compute
        repetitions: Default number of times to repeat each configuration
        repetitions_by_sample_size: Override repetitions per sample size (e.g., {1000: 5, 10000: 3})
        seed_offset: Base seed for random number generation
        algorithm_configs: Per-algorithm config overrides
        timeout_seconds: Per-run timeout in seconds
    """

    name: str
    description: str = ""
    algorithms: list[str] = field(default_factory=lambda: ["cssr", "spectral"])
    processes: list[str] = field(default_factory=lambda: ["even_process", "golden_mean"])
    sample_sizes: list[int] = field(default_factory=lambda: [1_000, 10_000, 100_000])
    metrics: list[str] = field(default_factory=lambda: ["state_count", "cmu", "hmu", "duration_s"])
    repetitions: int = 1
    repetitions_by_sample_size: dict[int, int] = field(default_factory=dict)
    seed_offset: int = 0
    algorithm_configs: dict[str, dict[str, Any]] = field(default_factory=dict)
    timeout_seconds: int = 120

    def get_repetitions(self, sample_size: int) -> int:
        """Get repetitions for a specific sample size."""
        return self.repetitions_by_sample_size.get(sample_size, self.repetitions)

    @property
    def total_runs(self) -> int:
        """Total number of individual benchmark runs."""
        total_reps = sum(self.get_repetitions(n) for n in self.sample_sizes)
        return len(self.algorithms) * len(self.processes) * total_reps


@dataclass(frozen=True)
class ExperimentsConfig:
    """
    Top-level experiments configuration.

    Attributes:
        experiments: List of experiment configurations
        output_dir: Directory for results output
        quick_mode: If True, use reduced sample sizes and skip slow algorithms
        quick_sample_sizes: Sample sizes to use in quick mode
    """

    experiments: list[ExperimentConfig]
    output_dir: str = "experiments/runs"
    quick_mode: bool = False
    quick_sample_sizes: list[int] = field(default_factory=lambda: [1000])

    @classmethod
    def from_yaml(cls, path: str | Path) -> ExperimentsConfig:
        """Load configuration from a YAML file."""
        with Path(path).open() as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExperimentsConfig:
        """Create configuration from a dictionary."""
        experiments = []
        for exp_data in data.get("experiments", []):
            experiments.append(ExperimentConfig(**exp_data))

        return cls(
            experiments=experiments,
            output_dir=data.get("output_dir", "experiments/runs"),
            quick_mode=data.get("quick_mode", False),
            quick_sample_sizes=data.get("quick_sample_sizes", [1000]),
        )

    def get_experiment(self, name: str) -> ExperimentConfig:
        """Get an experiment by name."""
        for exp in self.experiments:
            if exp.name == name:
                return exp
        raise KeyError(
            f"Unknown experiment: {name}. Available: {[e.name for e in self.experiments]}"
        )

    def list_experiments(self) -> list[str]:
        """List all experiment names."""
        return [exp.name for exp in self.experiments]


# Default experiment configurations
DEFAULT_ACCURACY_EXPERIMENT = ExperimentConfig(
    name="accuracy",
    description="Measure algorithm accuracy on canonical processes",
    algorithms=["cssr", "spectral", "csm", "bsi"],
    processes=["even_process", "golden_mean", "biased_coin"],
    sample_sizes=[1_000, 10_000, 100_000, 1_000_000],
    metrics=["state_count", "cmu", "hmu", "duration_s"],
    repetitions=1,
)

DEFAULT_CONVERGENCE_EXPERIMENT = ExperimentConfig(
    name="convergence",
    description="Measure how accuracy changes with sample size",
    algorithms=["cssr", "spectral", "csm", "bsi"],
    processes=["even_process", "golden_mean"],
    sample_sizes=[1_000, 10_000, 100_000, 1_000_000],
    metrics=["state_count", "cmu", "hmu", "duration_s"],
    repetitions=3,  # default fallback
    repetitions_by_sample_size={1_000: 5, 10_000: 4, 100_000: 3, 1_000_000: 3},
    seed_offset=100,
)

DEFAULT_SCALABILITY_EXPERIMENT = ExperimentConfig(
    name="scalability",
    description="Measure runtime scaling with data size",
    algorithms=["cssr", "spectral", "csm", "bsi"],
    processes=["even_process"],
    sample_sizes=[1_000, 10_000, 100_000, 1_000_000],
    metrics=["duration_s", "state_count"],
    repetitions=3,  # default fallback
    repetitions_by_sample_size={1_000: 5, 10_000: 4, 100_000: 3, 1_000_000: 3},
    timeout_seconds=300,
)


def create_default_config(quick_mode: bool = False) -> ExperimentsConfig:
    """Create the default benchmark configuration."""
    return ExperimentsConfig(
        experiments=[
            DEFAULT_ACCURACY_EXPERIMENT,
            DEFAULT_CONVERGENCE_EXPERIMENT,
            DEFAULT_SCALABILITY_EXPERIMENT,
        ],
        quick_mode=quick_mode,
        quick_sample_sizes=[1000],
    )


def load_config(path: str | Path | None = None, quick_mode: bool = False) -> ExperimentsConfig:
    """
    Load benchmark configuration.

    Args:
        path: Path to YAML config file. If None, uses defaults.
        quick_mode: If True, use reduced parameter space.

    Returns:
        Loaded or default configuration
    """
    if path is not None:
        config = ExperimentsConfig.from_yaml(path)
        if quick_mode:
            # Override quick mode setting from CLI
            return ExperimentsConfig(
                experiments=config.experiments,
                output_dir=config.output_dir,
                quick_mode=True,
                quick_sample_sizes=config.quick_sample_sizes,
            )
        return config
    return create_default_config(quick_mode=quick_mode)
