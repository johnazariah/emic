# emic.experiments

The experiments module provides a framework for reproducible algorithm benchmarking.

## Command-Line Interface

```bash
emic-experiment --help
```

### Options

| Option | Description |
|--------|-------------|
| `--all` | Run all experiments |
| `--quick` | Quick mode (reduced params, skip slow algorithms) |
| `--parallel N` | Run with N parallel workers |
| `--shard M/N` | Run shard M of N (for distributed execution) |
| `--combine DIR` | Combine sharded results from DIR |
| `--list` | List available experiments |
| `--algorithms` | Comma-separated list of algorithms (e.g., `--algorithms cssr,spectral`) |
| `--timeout` | Per-run timeout in seconds (default: 120) |
| `-o`, `--output-dir` | Output directory (default: experiments/runs)
| `-q`, `--quiet` | Suppress progress output | |

## Core Classes

::: emic.experiments.ExperimentRunner
    options:
      show_root_heading: true
      members:
        - run_experiment
        - run_all

::: emic.experiments.run_single_benchmark
    options:
      show_root_heading: true

## Configuration

::: emic.experiments.ExperimentConfig
    options:
      show_root_heading: true

::: emic.experiments.ExperimentsConfig
    options:
      show_root_heading: true

::: emic.experiments.load_config
    options:
      show_root_heading: true

## Registries

::: emic.experiments.ProcessRegistry
    options:
      show_root_heading: true
      members:
        - register
        - get
        - list

::: emic.experiments.ProcessInfo
    options:
      show_root_heading: true

::: emic.experiments.AlgorithmRegistry
    options:
      show_root_heading: true
      members:
        - register
        - get
        - list

::: emic.experiments.AlgorithmInfo
    options:
      show_root_heading: true

## Result Schema

::: emic.experiments.BenchmarkResult
    options:
      show_root_heading: true

::: emic.experiments.RunMetadata
    options:
      show_root_heading: true

::: emic.experiments.ResultsWriter
    options:
      show_root_heading: true

::: emic.experiments.read_results
    options:
      show_root_heading: true

::: emic.experiments.read_latest_results
    options:
      show_root_heading: true

## Functions

::: emic.experiments.get_process_registry

::: emic.experiments.get_algorithm_registry
