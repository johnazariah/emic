# Experimentation Protocol

*Standards for designing, running, and documenting experiments.*

---

## Experiment Lifecycle

```
1. Design    → Define hypothesis, parameters, metrics
2. Implement → Write reproducible code
3. Execute   → Run with proper controls
4. Analyze   → Statistical analysis of results
5. Document  → Record findings in journal
6. Archive   → Store artifacts for reproduction
```

---

## Design Standards

### Hypothesis First

Every experiment must have a clear hypothesis:

```markdown
**Hypothesis**: CSSR correctly infers the Golden Mean machine
with >95% probability when n ≥ 5000 samples.
```

### Parameter Specification

Document all parameters with ranges and defaults:

```python
@dataclass
class ExperimentConfig:
    """Fully specified experiment configuration."""

    # Process parameters
    process: str = "golden_mean"

    # Data parameters
    sample_sizes: tuple[int, ...] = (100, 500, 1000, 5000, 10000)
    repetitions: int = 50
    seed: int = 42

    # Algorithm parameters
    max_history: int = 5
    significance: float = 0.001
```

### Metrics

Define metrics before running:

| Metric | Definition | Target |
|--------|------------|--------|
| State count accuracy | P(inferred states = true states) | > 0.95 |
| Cμ error | \|Cμ_inferred - Cμ_true\| | < 0.01 |
| Runtime | Wall clock seconds | Report |

---

## Implementation Standards

### Reproducibility

```python
def set_reproducible(seed: int) -> None:
    """Set all random seeds for reproducibility."""
    import random
    import numpy as np

    random.seed(seed)
    np.random.seed(seed)
```

### Experiment Runner

```python
@dataclass
class ExperimentResult:
    """Structured result from one experiment run."""
    config: ExperimentConfig
    metrics: dict[str, float]
    artifacts: dict[str, Any]
    runtime_seconds: float
    timestamp: datetime

def run_experiment(config: ExperimentConfig) -> ExperimentResult:
    """Single experiment with timing and artifact collection."""
    start = time.perf_counter()
    # ... run experiment ...
    return ExperimentResult(
        config=config,
        metrics=metrics,
        artifacts=artifacts,
        runtime_seconds=time.perf_counter() - start,
        timestamp=datetime.now(UTC),
    )
```

### Batch Execution

```python
def run_batch(
    configs: Sequence[ExperimentConfig],
    parallel: bool = True,
    n_workers: int = 4,
) -> list[ExperimentResult]:
    """Run multiple experiments with optional parallelism."""
    ...
```

---

## Statistical Standards

### Sample Sizes

- Minimum 30 repetitions for statistical tests
- Report mean ± standard error
- Use bootstrap for confidence intervals when needed

### Comparisons

- Use appropriate statistical tests:
  - Paired t-test for algorithm comparisons
  - Chi-squared for categorical outcomes
  - Mann-Whitney for non-normal distributions
- Report effect sizes, not just p-values
- Correct for multiple comparisons (Bonferroni/Holm)

### Visualization

- Error bars on all plots (std error or 95% CI)
- Use colorblind-friendly palettes
- Label axes with units
- Include sample sizes in captions

---

## Documentation Standards

### Experiment Log Entry

```markdown
### EXP-001: State Count Convergence

**Date**: 2026-01-15
**Hypothesis**: State count converges to true value as n → ∞
**Status**: ✅ Complete

**Configuration**:
- Processes: Golden Mean, Even Process
- Sample sizes: 100, 500, 1000, 5000, 10000
- Repetitions: 50
- Seed: 42

**Results**:
| Process | n=1000 | n=5000 | n=10000 |
|---------|--------|--------|---------|
| Golden Mean | 85% | 96% | 99% |
| Even Process | 40% | 78% | 92% |

**Conclusion**: Even Process requires more data due to
finite-sample effects. Post-merge helps significantly.

**Artifacts**: `experiments/exp001/`
```

### Figure Standards

```python
def create_figure(
    data: pd.DataFrame,
    title: str,
    filename: str,
) -> None:
    """Create publication-ready figure."""
    fig, ax = plt.subplots(figsize=(6, 4))
    # ... plotting code ...

    ax.set_xlabel("Sample Size (n)", fontsize=12)
    ax.set_ylabel("State Count Accuracy", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend()

    fig.tight_layout()
    fig.savefig(f"figures/{filename}.pdf", dpi=300)
    fig.savefig(f"figures/{filename}.png", dpi=150)
```

---

## Artifact Management

### Directory Structure

```
experiments/
├── exp001_convergence/
│   ├── config.json
│   ├── results.parquet
│   ├── figures/
│   │   ├── convergence.pdf
│   │   └── convergence.png
│   └── analysis.ipynb
├── exp002_sensitivity/
│   └── ...
└── README.md
```

### Data Formats

- **Config**: JSON (human-readable, version-controlled)
- **Results**: Parquet (efficient, typed columns)
- **Figures**: PDF (vector) + PNG (preview)
- **Analysis**: Jupyter notebooks

### Version Control

- Commit experiment configs
- `.gitignore` large result files
- Store artifacts in releases or external storage

---

## Checklists

### Pre-Experiment

- [ ] Hypothesis documented
- [ ] Parameters fully specified
- [ ] Metrics defined
- [ ] Random seed set
- [ ] Output directory created

### Post-Experiment

- [ ] Results saved to structured format
- [ ] Figures generated
- [ ] Analysis documented
- [ ] Journal entry written
- [ ] Artifacts organized

### Pre-Publication

- [ ] Results reproducible from config
- [ ] Statistical tests appropriate
- [ ] Error bars on all plots
- [ ] Code cleaned and documented
