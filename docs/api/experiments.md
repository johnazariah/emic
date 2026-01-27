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
| `-o`, `--output-dir` | Output directory (default: experiments/runs) |

## Core Classes

::: emic.experiments.ExperimentRunner
    options:
      show_root_heading: true
      members:
        - run_experiment
        - run_all

::: emic.experiments.config.ExperimentConfig
    options:
      show_root_heading: true

## Registries

::: emic.experiments.registry.ProcessRegistry
    options:
      show_root_heading: true
      members:
        - register
        - get
        - list

::: emic.experiments.registry.AlgorithmRegistry
    options:
      show_root_heading: true
      members:
        - register
        - get
        - list

## Result Schema

::: emic.experiments.schema.ExperimentRecord
    options:
      show_root_heading: true

## Functions

::: emic.experiments.get_process_registry

::: emic.experiments.get_algorithm_registry
