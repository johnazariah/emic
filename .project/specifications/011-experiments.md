# Specification 011: Experiments and Empirical Validation

## Overview

This specification defines a comprehensive experimental program to validate the `emic` framework, characterize algorithm behavior, and generate results for the research paper.

---

## Experiment Categories

### Category 1: Convergence Analysis

#### Experiment 1.1: States vs Sample Size

**Question**: How does inferred state count converge to true state count as data increases?

**Design**:
```python
processes = [GoldenMean, EvenProcess, Periodic(5)]
sample_sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
repetitions = 50

for process in processes:
    for n in sample_sizes:
        for rep in range(repetitions):
            data = process.take(n)
            result = CSSR(config).infer(data)
            record(process, n, rep, len(result.machine.states))
```

**Metrics**:
- Mean inferred states ± std
- Convergence rate
- Probability of correct state count

**Visualization**: Line plot with confidence bands

---

#### Experiment 1.2: Complexity Measure Convergence

**Question**: How do Cμ and hμ estimates converge to true values?

**Design**:
```python
for process in processes:
    true_Cmu = analyze(process.true_machine).statistical_complexity
    for n in sample_sizes:
        for rep in range(repetitions):
            result = CSSR(config).infer(process.take(n))
            inferred_Cmu = analyze(result.machine).statistical_complexity
            record(process, n, rep, abs(inferred_Cmu - true_Cmu))
```

**Metrics**:
- Mean absolute error in Cμ
- Mean absolute error in hμ
- Bias (systematic over/under-estimation)

**Visualization**: Error decay plot (log-log for rate estimation)

---

### Category 2: Parameter Sensitivity

#### Experiment 2.1: Significance Level Sensitivity

**Question**: How does significance threshold affect state count and accuracy?

**Design**:
```python
significances = [0.001, 0.005, 0.01, 0.05, 0.1, 0.2]
n = 10000

for process in processes:
    for sig in significances:
        config = CSSRConfig(max_history=5, significance=sig)
        result = CSSR(config).infer(process.take(n))
        record(process, sig, result)
```

**Metrics**:
- State count vs significance
- Cμ error vs significance
- Optimal significance per process

**Visualization**: Heatmap or line plot

---

#### Experiment 2.2: History Length Sensitivity

**Question**: How does max_history affect inference quality?

**Design**:
```python
max_histories = [2, 3, 4, 5, 6, 7, 8, 10]

for process in processes:
    for L in max_histories:
        config = CSSRConfig(max_history=L, significance=0.001)
        result = CSSR(config).infer(process.take(n))
        record(process, L, result)
```

**Metrics**:
- State count vs L
- Runtime vs L
- Minimum L for correct inference

---

#### Experiment 2.3: Data Size vs History Length Trade-off

**Question**: What's the relationship between required data and history length?

**Design**:
```python
for L in [3, 5, 7, 10]:
    for n in sample_sizes:
        config = CSSRConfig(max_history=L)
        result = CSSR(config).infer(process.take(n))
        record(L, n, result)
```

**Visualization**: 2D heatmap of success rate

---

### Category 3: Algorithm Comparison

#### Experiment 3.1: Cross-Algorithm Validation

**Question**: Do different algorithms agree on inferred structure?

**Design**:
```python
algorithms = [CSSR, CSM, Spectral, BSI]

for process in processes:
    data = process.take(10000)
    results = {alg.__name__: alg(config).infer(data) for alg in algorithms}
    compare_results(results)
```

**Metrics**:
- Agreement on state count
- Machine similarity (edit distance, isomorphism)
- Cμ agreement

---

#### Experiment 3.2: Computational Cost

**Question**: How do algorithms scale with data size?

**Design**:
```python
for alg in algorithms:
    for n in sample_sizes:
        t_start = time.perf_counter()
        alg(config).infer(data[:n])
        runtime = time.perf_counter() - t_start
        record(alg, n, runtime)
```

**Visualization**: Log-log runtime plot

---

### Category 4: Finite Sample Effects

#### Experiment 4.1: Even Process Over-Splitting

**Question**: Characterize the finite-sample state inflation in Even Process.

**Design**:
```python
process = EvenProcess(p=0.5)
for n in sample_sizes:
    for rep in range(repetitions):
        result = CSSR(config).infer(process.take(n))
        result_merged = CSSR(merge_config).infer(process.take(n))
        record(n, rep, len(result.machine.states), len(result_merged.machine.states))
```

**Metrics**:
- State count with/without post-merge
- Sample size required for correct inference

---

#### Experiment 4.2: Rare Symbol Effects

**Question**: How do rare symbols affect inference?

**Design**:
```python
biases = [0.5, 0.3, 0.1, 0.05, 0.01]

for p in biases:
    process = GoldenMean(p=p)  # p controls symbol frequency
    result = CSSR(config).infer(process.take(n))
    record(p, result)
```

---

### Category 5: Real-World Data

#### Experiment 5.1: Natural Language

**Question**: What structure emerges from character-level text?

**Data Sources**:
- Shakespeare corpus
- Wikipedia articles
- Programming code (Python, C)

**Analysis**:
- Inferred state count
- Entropy rate comparison to known values
- Visualization of state diagram

---

#### Experiment 5.2: Financial Time Series

**Question**: Can ε-machines detect structure in discretized returns?

**Data Sources**:
- S&P 500 daily returns (discretized: up/down/flat)
- Bitcoin prices
- Forex pairs

---

#### Experiment 5.3: Biological Sequences

**Question**: What structure exists in DNA/protein sequences?

**Data Sources**:
- E. coli genome
- Human chromosome segments
- Protein families

---

### Category 6: Stress Tests

#### Experiment 6.1: Non-Stationary Data

**Question**: How does CSSR behave on non-stationary processes?

**Design**: Generate data with regime changes, measure detection.

---

#### Experiment 6.2: Noisy Observations

**Question**: How robust is inference to observation noise?

**Design**: Add bit-flip noise at various rates.

---

#### Experiment 6.3: Missing Data

**Question**: Can we infer from incomplete sequences?

---

## Visualization Catalog

| Experiment | Visualization Type |
|------------|-------------------|
| Convergence | Line plot with confidence bands |
| Parameter sensitivity | Heatmaps |
| Algorithm comparison | Bar charts, radar plots |
| State diagrams | Graphviz with edge weights |
| Complexity landscape | 3D surface plots |
| Time series | Annotated sequence plots |

## Implementation

### Experiment Runner

```python
@dataclass
class Experiment:
    name: str
    description: str
    parameters: dict
    run: Callable[..., ExperimentResult]

class ExperimentRunner:
    def run_all(self, experiments: list[Experiment]) -> ResultsDB:
        ...

    def run_parallel(self, experiment: Experiment, n_workers: int) -> ResultsDB:
        ...
```

### Results Storage

```
experiments/
├── results/
│   ├── convergence_analysis.parquet
│   ├── parameter_sensitivity.parquet
│   └── ...
├── figures/
│   ├── fig1_convergence.pdf
│   └── ...
└── notebooks/
    ├── analysis.ipynb
    └── visualization.ipynb
```

## Paper Figures

Target figures for the research paper:

1. **Figure 1**: State diagram examples (Golden Mean, Even Process)
2. **Figure 2**: Convergence analysis (states and Cμ vs n)
3. **Figure 3**: Parameter sensitivity heatmap
4. **Figure 4**: Algorithm comparison
5. **Figure 5**: Real-world application example
