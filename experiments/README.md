# Experiments

This directory contains reproducible experiments for the `emic` project.

## Structure

```
experiments/
├── registry.yaml       # Master catalog of all experiments
├── README.md           # This file
├── runner.py           # Experiment execution utilities
│
├── convergence/        # EXP-001: Convergence analysis
├── noise_robustness/   # EXP-002: Noise robustness
├── paper_verification/ # EXP-003: Reproduce paper results
└── algorithm_compare/  # EXP-004: Algorithm comparison
```

## Running Experiments

```bash
# Run a specific experiment
uv run python experiments/convergence/run.py

# Check experiment status
uv run python experiments/runner.py status
```

## Experiment Lifecycle

1. **Configure** — Edit `config.yaml` in experiment directory
2. **Run** — Execute `run.py`
3. **Results** — Output saved to `results/` subdirectory
4. **Report** — Summarize findings in `report.md`

## Adding New Experiments

1. Create directory: `experiments/my_experiment/`
2. Add to registry: Edit `registry.yaml`
3. Create config: `config.yaml`
4. Write runner: `run.py`
5. Document: `report.md` (after running)

## Results Format

- **Tabular data**: Parquet files in `results/`
- **Figures**: PNG/PDF in `results/figures/`
- **Metadata**: YAML in `results/metadata.yaml`

Query results with:
```python
import polars as pl
df = pl.read_parquet("experiments/convergence/results/summary.parquet")
```
