# Experiments

This directory contains reproducible experiments for the `emic` project.

## Latest Results (January 2026)

### Algorithm Accuracy (State Count Recovery)

| Algorithm | Even Process | Golden Mean | Biased Coin | Overall |
|-----------|--------------|-------------|-------------|---------|
| **Spectral** | 100% | 100% | 67% | **89%** |
| **CSSR** | 67% | 100% | 0% | 56% |
| CSM | 0% | 67% | 33% | 33% |
| BSI | 0% | 0% | 100% | 33% |

### Statistical Complexity Error

| Algorithm | Mean |Cμ - true| |
|-----------|-------------------|
| **CSSR** | **0.053** |
| CSM | 0.104 |
| BSI | 0.528 |
| Spectral | 0.667 |

**Key findings:**

- **Spectral** excels at state count recovery (89%) but has higher Cμ error
- **CSSR** has the lowest Cμ error (0.053) but struggles with IID processes
- Algorithms show complementary strengths across different process types

## Structure

```
experiments/
├── registry.yaml       # Catalog of experiments
├── README.md           # This file
├── runs/               # Experiment output (timestamped folders)
│   ├── 2026-01-27T06-35-40/
│   │   ├── metadata.yaml     # Git commit, timing, CLI args
│   │   └── results.json      # Raw experiment data (1552 records)
│   └── latest -> ...   # Symlink to most recent run
└── results/            # Legacy location
```

## Running Experiments

### Using the CLI

```bash
# Run all experiments
emic-experiment --all

# Run specific experiment
emic-experiment accuracy

# Quick mode (reduced params, skip slow algorithms)
emic-experiment --quick

# List available experiments
emic-experiment --list

# Custom output directory
emic-experiment --output-dir ./my-results

# Parallel execution
emic-experiment accuracy --parallel 4
```

### Interactive Session

For a guided experiment workflow, use the Copilot prompt:

1. Open GitHub Copilot Chat
2. Reference `.github/prompts/run-experiment.prompt.md`
3. Follow the interactive steps

### Default Experiments

| Experiment | Description |
|------------|-------------|
| accuracy | Measure algorithm accuracy on canonical processes |
| convergence | How accuracy changes with sample size |
| scalability | Runtime scaling with data size |

## Results Format

Each run creates a timestamped folder:

```
results/2026-01-26T14-32-05/
├── metadata.yaml    # Git commit, Python version, CLI args
└── results.parquet  # Or results.json if pyarrow not installed
```

### Reading Results

```python
from emic.experiments import read_latest_results

df = read_latest_results("experiments/results")
print(df.groupby(["algorithm", "process"])["value"].mean())
```

### Schema

| Column | Type | Description |
|--------|------|-------------|
| experiment | str | "accuracy", "convergence", etc. |
| algorithm | str | "cssr", "spectral", "bsi", etc. |
| process | str | "even_process", "golden_mean", etc. |
| n_samples | int | Data length used |
| metric | str | "state_count", "cmu", "hmu", "duration_s" |
| value | float | Measured value |
| ground_truth | float | Expected value (if known) |
| error | str | Exception message (if failed) |
| timestamp | datetime | When recorded |

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

output_dir: experiments/results
quick_sample_sizes: [1000]
```

Run with:

```bash
emic-experiment --config my_config.yaml --all
```
