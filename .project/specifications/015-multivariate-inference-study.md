# Specification 015: Multivariate Inference Study

## Overview

This specification defines a comprehensive multivariate study comparing all inference algorithms (CSSR, CSM, BSI, Spectral, NSD) across a range of processes, sample sizes, and parameter settings.

## Motivation

With multiple inference algorithms now available, we need:
1. **Performance characterization** — understand when each algorithm excels
2. **Convergence analysis** — how accuracy improves with sample size
3. **Parameter sensitivity** — which hyperparameters matter most
4. **Computational cost** — runtime vs accuracy tradeoffs
5. **Robustness** — behavior under noise and model misspecification

---

## Study Design

### Independent Variables (Factors)

#### 1. Inference Algorithm
| Algorithm | Parameters to Vary |
|-----------|-------------------|
| CSSR | `max_history ∈ {3, 5, 7, 10}`, `significance ∈ {0.01, 0.05, 0.10}` |
| CSM | `history_length ∈ {3, 5, 7, 10}`, `merge_threshold ∈ {0.01, 0.05, 0.10}`, `distance_metric ∈ {'hellinger', 'tv', 'kl', 'chi2'}` |
| BSI | `max_states ∈ {3, 5, 10, 15}`, `alpha_prior ∈ {0.1, 1.0, 10.0}`, `n_samples ∈ {100, 500, 1000}` |
| Spectral | `max_history ∈ {3, 5, 7, 10}`, `rank_threshold ∈ {0.001, 0.01, 0.1}`, `rank ∈ {None, 2, 5}` |
| NSD | `max_states ∈ {3, 5, 10, 15}`, `history_length ∈ {3, 5, 10}`, `n_iterations ∈ {50, 100, 200}` |

#### 2. Ground Truth Process
| Process | True States | Complexity (Cμ) | Parameters |
|---------|-------------|-----------------|------------|
| Biased Coin | 1 | 0.0 | `p ∈ {0.1, 0.3, 0.5, 0.7, 0.9}` |
| Golden Mean | 2 | 0.918 bits | `p ∈ {0.3, 0.5, 0.7}` |
| Even Process | 2 | 1.0 bit | `p ∈ {0.3, 0.5, 0.7}` |
| Periodic | 2-5 | log₂(k) bits | `period ∈ {2, 3, 4, 5}` |
| Simple Nondeterministic Source | 3 | ~1.58 bits | `p ∈ {0.5}` |
| R-k Process | k | log₂(k) bits | `k ∈ {2, 3, 4}` |

#### 3. Sample Size
```python
SAMPLE_SIZES = [100, 500, 1000, 5000, 10000, 50000, 100000]
```

#### 4. Random Seeds
```python
N_REPLICATIONS = 30  # For statistical significance
SEEDS = list(range(42, 42 + N_REPLICATIONS))
```

### Dependent Variables (Metrics)

#### Accuracy Metrics
| Metric | Formula | Description |
|--------|---------|-------------|
| State Count Error | `|Ŝ - S|` | Absolute error in number of states |
| State Count Ratio | `Ŝ / S` | Ratio (1.0 = perfect) |
| Statistical Complexity Error | `|Ĉμ - Cμ|` | Error in complexity estimate |
| Entropy Rate Error | `|ĥμ - hμ|` | Error in entropy rate |
| Structural Distance | `d(M̂, M)` | Machine graph edit distance |
| Prediction Error | `KL(P̂(x|past) || P(x|past))` | Predictive distribution error |

#### Computational Metrics
| Metric | Description |
|--------|-------------|
| Wall Time (s) | Total inference time |
| Memory (MB) | Peak memory usage |
| Iterations | Number of algorithm iterations |

#### Robustness Metrics
| Metric | Description |
|--------|-------------|
| Variance across seeds | Stability of estimates |
| Sensitivity to parameters | Gradient of error w.r.t. hyperparameters |

---

## Experiment Matrix

### Full Factorial Design

Total configurations per algorithm:
- **CSSR**: 4 × 3 = 12 parameter combinations
- **CSM**: 4 × 3 × 4 = 48 parameter combinations
- **BSI**: 4 × 3 × 3 = 36 parameter combinations
- **Spectral**: 4 × 3 × 3 = 36 parameter combinations
- **NSD**: 4 × 3 × 3 = 36 parameter combinations

Total: **168 parameter combinations**

Processes: 6 processes × ~3 parameter settings each = ~18 process configurations

Sample sizes: 7

Replications: 30

**Total experiments**: 168 × 18 × 7 × 30 ≈ **635,040** individual runs

### Reduced Design (Recommended)

Use Latin hypercube sampling for algorithm parameters:
- 10 parameter configurations per algorithm × 5 algorithms = 50
- 6 core processes (canonical parameters) = 6
- 5 sample sizes: [500, 1000, 5000, 10000, 50000] = 5
- 10 replications = 10

**Total experiments**: 50 × 6 × 5 × 10 = **15,000** runs

---

## Implementation

### Experiment Runner

```python
@dataclass(frozen=True)
class ExperimentConfig:
    """Configuration for a single experiment."""

    # Algorithm
    algorithm: str  # 'cssr', 'csm', 'bsi', 'spectral', 'nsd'
    algorithm_params: dict[str, Any]

    # Process
    process: str  # 'biased_coin', 'golden_mean', etc.
    process_params: dict[str, Any]

    # Data
    sample_size: int
    seed: int

@dataclass
class ExperimentResult:
    """Result from a single experiment."""

    config: ExperimentConfig

    # Ground truth
    true_states: int
    true_complexity: float
    true_entropy_rate: float

    # Inferred
    inferred_states: int
    inferred_complexity: float
    inferred_entropy_rate: float

    # Metrics
    wall_time: float
    peak_memory_mb: float
    converged: bool

    # Raw machine for further analysis
    machine: EpsilonMachine
```

### Experiment Grid

```python
class ExperimentGrid:
    """Generate experiment configurations."""

    def __init__(
        self,
        algorithms: dict[str, list[dict]],
        processes: dict[str, list[dict]],
        sample_sizes: list[int],
        n_replications: int,
        base_seed: int = 42,
    ):
        self.algorithms = algorithms
        self.processes = processes
        self.sample_sizes = sample_sizes
        self.n_replications = n_replications
        self.base_seed = base_seed

    def __iter__(self) -> Iterator[ExperimentConfig]:
        """Yield all experiment configurations."""
        for alg_name, alg_params_list in self.algorithms.items():
            for alg_params in alg_params_list:
                for proc_name, proc_params_list in self.processes.items():
                    for proc_params in proc_params_list:
                        for n in self.sample_sizes:
                            for rep in range(self.n_replications):
                                yield ExperimentConfig(
                                    algorithm=alg_name,
                                    algorithm_params=alg_params,
                                    process=proc_name,
                                    process_params=proc_params,
                                    sample_size=n,
                                    seed=self.base_seed + rep,
                                )

    def __len__(self) -> int:
        """Total number of experiments."""
        n_alg_configs = sum(len(v) for v in self.algorithms.values())
        n_proc_configs = sum(len(v) for v in self.processes.values())
        return n_alg_configs * n_proc_configs * len(self.sample_sizes) * self.n_replications
```

### Parallel Execution

```python
class StudyRunner:
    """Run experiments in parallel."""

    def __init__(
        self,
        grid: ExperimentGrid,
        n_workers: int = -1,  # -1 = all CPUs
        output_dir: Path = Path("results"),
    ):
        self.grid = grid
        self.n_workers = n_workers
        self.output_dir = output_dir

    def run(self, progress: bool = True) -> pd.DataFrame:
        """Run all experiments and return results DataFrame."""
        from joblib import Parallel, delayed

        results = Parallel(n_jobs=self.n_workers)(
            delayed(self._run_single)(config)
            for config in tqdm(self.grid, disable=not progress)
        )

        return pd.DataFrame([r.__dict__ for r in results])
```

---

## Analysis Plan

### Primary Analyses

1. **Convergence Curves**
   - Plot accuracy metrics vs sample size
   - Separate lines for each algorithm
   - Error bars from replications

2. **Parameter Sensitivity**
   - Partial dependence plots for each hyperparameter
   - SHAP values for feature importance

3. **Algorithm Comparison**
   - Pairwise Win/Loss/Tie counts
   - Critical difference diagrams (Nemenyi test)
   - Pareto frontiers (accuracy vs runtime)

4. **Process-Specific Performance**
   - Heatmap: algorithm × process → accuracy
   - Identify which algorithm best for which process type

### Visualizations

```python
def plot_convergence(results: pd.DataFrame, metric: str = "state_count_error"):
    """Plot convergence curves for all algorithms."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    for ax, process in zip(axes.flat, PROCESSES):
        data = results[results["process"] == process]

        for algorithm in ALGORITHMS:
            alg_data = data[data["algorithm"] == algorithm]
            grouped = alg_data.groupby("sample_size")[metric]

            ax.errorbar(
                grouped.groups.keys(),
                grouped.mean(),
                yerr=grouped.std(),
                label=algorithm,
                marker="o",
            )

        ax.set_xlabel("Sample Size")
        ax.set_ylabel(metric)
        ax.set_xscale("log")
        ax.set_title(process)
        ax.legend()

    plt.tight_layout()
    return fig

def plot_pareto_frontier(results: pd.DataFrame):
    """Plot accuracy vs runtime Pareto frontier."""
    fig, ax = plt.subplots(figsize=(10, 8))

    for algorithm in ALGORITHMS:
        alg_data = results[results["algorithm"] == algorithm]

        # Mean across replications
        grouped = alg_data.groupby("algorithm_params").agg({
            "state_count_error": "mean",
            "wall_time": "mean",
        })

        ax.scatter(
            grouped["wall_time"],
            grouped["state_count_error"],
            label=algorithm,
            alpha=0.7,
        )

    ax.set_xlabel("Runtime (s)")
    ax.set_ylabel("State Count Error")
    ax.set_xscale("log")
    ax.legend()

    return fig
```

---

## Deliverables

1. **Raw Results**
   - CSV with all experiment results
   - Pickled machine objects for further analysis

2. **Summary Statistics**
   - Tables of mean ± std for each algorithm × process
   - Best hyperparameter configurations

3. **Figures for Paper**
   - Convergence curves (Figure 1)
   - Parameter sensitivity (Figure 2)
   - Algorithm comparison heatmap (Figure 3)
   - Pareto frontier (Figure 4)

4. **Recommendations**
   - Default hyperparameter settings
   - Algorithm selection guide based on data characteristics
   - Computational budget guidance

---

## Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| Setup | 1 day | Implement experiment infrastructure |
| Pilot | 1 day | Run reduced study (100 experiments) |
| Full Run | 2-3 days | Run complete study (15,000+ experiments) |
| Analysis | 2 days | Generate all figures and tables |
| Writing | 2 days | Document findings in JOURNAL and paper |

Total: ~1 week

---

## Dependencies

```python
# Required packages
required = [
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "joblib",  # Parallel execution
    "tqdm",    # Progress bars
]

# Optional (for advanced analysis)
optional = [
    "scikit-learn",  # For clustering analysis
    "shap",          # For parameter importance
    "scipy",         # For statistical tests
]
```

---

## Success Criteria

1. All 5 algorithms successfully run on all 6 processes
2. Convergence curves show expected 1/√n behavior
3. Identify clear performance differences between algorithms
4. Produce publication-quality figures
5. Document algorithm selection recommendations
