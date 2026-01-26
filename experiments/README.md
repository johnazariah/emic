# Experiments

This directory contains reproducible experiments for the `emic` project.

## Structure

```
experiments/
├── registry.yaml       # Catalog of experiments
├── README.md           # This file
└── benchmarks/         # Algorithm performance benchmarks
```

## Running Benchmarks

```bash
# Run the benchmark suite
cd experiments/benchmarks
make benchmarks

# Generate analysis and LaTeX tables
make analyze

# Full pipeline: run benchmarks → generate report data
make report
```

## Experiment Lifecycle

1. **Configure** — Edit `config.yaml` in experiment directory
2. **Run** — Execute `run.py` or use Makefile
3. **Results** — Output saved to `results/` subdirectory
4. **Report** — Analysis in `analyze_results.py`

## Results Format

- **Tabular data**: Parquet files in `results/`
- **Figures**: PNG/PDF in `results/figures/`
- **LaTeX tables**: Generated in paper's `tex/generated/` directory

Query results with:
```python
import polars as pl
df = pl.read_parquet("experiments/benchmarks/results/summary.parquet")
```
