# Experiments

This directory contains reproducible experiments for the `emic` project.

## Structure

```
experiments/
├── registry.yaml       # Catalog of experiments
├── README.md           # This file
├── results/            # Benchmark output (timestamped folders)
│   ├── 2026-01-26T14-32-05/
│   │   ├── metadata.yaml
│   │   └── results.parquet
│   └── latest -> ...   # Symlink to most recent run
└── benchmarks/         # Algorithm performance benchmarks (legacy)
```

## Running Benchmarks

### Using the CLI

```bash
# Run all experiments
emic-benchmark --all

# Run specific experiment
emic-benchmark accuracy

# Quick mode (reduced params, skip slow algorithms)
emic-benchmark --quick

# List available experiments
emic-benchmark --list

# Custom output directory
emic-benchmark --output-dir ./my-results
```

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
from emic.benchmarks import read_latest_results

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
emic-benchmark --config my_config.yaml --all
```
