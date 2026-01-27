# Experiments

The `emic.experiments` module provides a framework for running reproducible experiments to evaluate inference algorithms against known ground truth.

## Overview

The experimentation framework supports:

- **Multiple algorithms**: CSSR, Spectral, CSM, BSI
- **Canonical processes**: Even Process, Golden Mean, Biased Coin
- **Experiment types**: Accuracy, convergence, scalability
- **Parallel execution**: Run experiments across multiple workers
- **Structured output**: JSON/Parquet results with metadata

## Quick Start

### Command-Line Interface

```bash
# Run all experiments
emic-experiment --all

# Run specific experiment
emic-experiment accuracy

# Parallel execution (4 workers)
emic-experiment --all --parallel 4

# Quick mode (skip slow algorithms, reduced sample sizes)
emic-experiment --quick

# Run only specific algorithms
emic-experiment accuracy --algorithms cssr,spectral

# List available experiments
emic-experiment --list
```

### Programmatic Usage

```python
from emic.experiments import ExperimentRunner
from emic.experiments.config import DEFAULT_EXPERIMENTS

runner = ExperimentRunner()
results = runner.run_experiment(DEFAULT_EXPERIMENTS["accuracy"])
```

## Experiment Types

### Accuracy

Measures how well each algorithm recovers the true number of states and complexity measures on canonical processes.

**Configuration:**
- Algorithms: CSSR, Spectral, CSM, BSI
- Processes: Even Process, Golden Mean, Biased Coin
- Sample sizes: 1000, 5000, 10000
- Repetitions: 1

**Metrics:**
- `state_count`: Number of inferred states
- `cmu`: Statistical complexity
- `hmu`: Entropy rate
- `duration_s`: Inference time

### Convergence

Measures how accuracy improves with increasing data size.

**Configuration:**
- Algorithms: CSSR, Spectral, CSM, BSI
- Processes: Even Process, Golden Mean
- Sample sizes: 100, 500, 1000, 2000, 5000, 10000, 20000
- Repetitions: 5

### Scalability

Measures runtime scaling with data size.

**Configuration:**
- Algorithms: CSSR, Spectral, CSM, BSI
- Processes: Even Process
- Sample sizes: 1000, 2000, 5000, 10000, 20000, 50000
- Repetitions: 3

## Results

### Latest Results (January 2026)

#### Algorithm Accuracy (State Count)

| Algorithm | Even Process | Golden Mean | Biased Coin | Overall |
|-----------|--------------|-------------|-------------|---------|
| **Spectral** | 100% | 100% | 67% | **89%** |
| **CSSR** | 67% | 100% | 0% | 56% |
| **CSM** | 0% | 67% | 33% | 33% |
| **BSI** | 0% | 0% | 100% | 33% |

#### Statistical Complexity Error (Mean |Cμ - true|)

| Algorithm | Mean Error |
|-----------|------------|
| **CSSR** | **0.053** |
| CSM | 0.104 |
| BSI | 0.528 |
| Spectral | 0.667 |

#### Convergence by Sample Size

| N | Correct Rate |
|---|--------------|
| 100 | 32% |
| 500 | 22% |
| 1000 | 50% |
| 2000 | 60% |
| 5000 | 52% |
| 10000 | 57% |
| 20000 | 60% |

!!! note "Interpretation"
    - **Spectral** excels at state count recovery but has higher Cμ error
    - **CSSR** has the lowest Cμ error but struggles with biased coin
    - **BSI** performs well on IID processes but struggles with structure
    - Convergence is non-monotonic — more data doesn't always help

### Output Format

Results are stored in `experiments/runs/<timestamp>/`:

```
experiments/runs/2026-01-27T06-35-40/
├── metadata.yaml    # Git commit, config, timing
└── results.json     # All experiment records
```

#### Record Schema

| Field | Type | Description |
|-------|------|-------------|
| `experiment` | str | "accuracy", "convergence", "scalability" |
| `algorithm` | str | "cssr", "spectral", "csm", "bsi" |
| `process` | str | "even_process", "golden_mean", "biased_coin" |
| `n_samples` | int | Data length used |
| `metric` | str | "state_count", "cmu", "hmu", "duration_s" |
| `value` | float | Measured value |
| `ground_truth` | float | Expected value (if known) |
| `error` | str | Exception message (if failed) |
| `timestamp` | datetime | When recorded |

## Parallel Execution

For large experiments, use parallel execution:

```bash
# 4 parallel workers
emic-experiment --all --parallel 4

# Sharded execution (for distributed systems)
emic-experiment --all --shard 1/4  # Run on machine 1
emic-experiment --all --shard 2/4  # Run on machine 2
# ... etc

# Combine sharded results
emic-experiment --combine experiments/runs/<timestamp>/
```

## Custom Configuration

Create a YAML config file:

```yaml
experiments:
  - name: my_experiment
    algorithms: [cssr, spectral]
    processes: [even_process, golden_mean]
    sample_sizes: [1000, 5000, 10000]
    repetitions: 3
    timeout_seconds: 60

output_dir: experiments/runs
quick_sample_sizes: [1000]
```

Run with:

```bash
emic-experiment --config my_config.yaml --all
```

## Adding Custom Experiments

### Register a Process

```python
from emic.experiments import get_process_registry

registry = get_process_registry()
registry.register(
    name="my_process",
    display_name="My Process",
    factory=MyProcessSource,
    parameters={"param": 0.5},
    ground_truth={"state_count": 3, "cmu": 1.5},
)
```

### Register an Algorithm

```python
from emic.experiments import get_algorithm_registry

registry = get_algorithm_registry()
registry.register(
    name="my_algo",
    display_name="My Algorithm",
    factory=MyAlgorithm,
    config_class=MyConfig,
    default_config={"max_history": 5},
    slow=False,
)
```

## Best Practices

1. **Use `--quick` for development**: Skip slow algorithms and use small sample sizes
2. **Run parallel for production**: Use `--parallel N` for faster execution
3. **Check for errors**: Results include an `error` field for failed runs
4. **Version control results**: Commit important experiment results
5. **Use metadata**: Each run includes git commit hash for reproducibility
