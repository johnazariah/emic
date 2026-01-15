# Specification 009: Research Paper

## Overview

This specification defines the structure and content for a LaTeX research paper demonstrating the `emic` framework and presenting empirical results on epsilon-machine inference.

## Paper Metadata

**Working Title**: "Emic: A Python Framework for Epsilon-Machine Inference and Computational Mechanics"

**Target Venue**: Journal of Computational Physics / Entropy / arXiv preprint

**Authors**: [To be determined]

## Paper Structure

### Abstract (~200 words)

Key points:
- Computational mechanics provides minimal predictive models
- Gap between theory and accessible tools
- Introduce `emic` framework
- Summarize key results (accuracy, complexity measures)
- Open-source availability

### 1. Introduction (~1 page)

#### 1.1 Motivation
- Hidden structure in stochastic processes
- Epsilon-machines as optimal predictors
- Need for accessible computational tools

#### 1.2 Contributions
- Open-source Python framework
- Implementation of CSSR algorithm
- Empirical evaluation on canonical processes
- Educational resources

#### 1.3 Paper Organization
- Overview of remaining sections

### 2. Background (~2 pages)

#### 2.1 Computational Mechanics
- Causal states and equivalence relation
- Epsilon-machines as minimal predictive models
- Unifilarity property

#### 2.2 Complexity Measures
- Statistical complexity (Cμ): memory in optimal prediction
  $$ C_\mu = -\sum_{\sigma \in \mathcal{S}} \pi_\sigma \log_2 \pi_\sigma $$

- Entropy rate (hμ): intrinsic randomness
  $$ h_\mu = \lim_{L \to \infty} \frac{H[X_0^L]}{L} $$

- Excess entropy (E): mutual information between past and future
  $$ E = I[\overleftarrow{X}; \overrightarrow{X}] $$

#### 2.3 Canonical Processes
- Biased Coin (IID): 1 state, Cμ = 0
- Golden Mean: 2 states, no consecutive 1s
- Even Process: 3 states, parity tracking
- k-Periodic: k states, deterministic

#### 2.4 CSSR Algorithm
- Suffix tree construction
- Statistical equivalence testing
- State splitting and merging
- Convergence properties

### 3. The Emic Framework (~2 pages)

#### 3.1 Architecture
- Core types (Symbol, State, Transition, EpsilonMachine)
- Source protocol (synthetic, empirical, transforms)
- Inference interface
- Analysis functions

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Sources   │ ──▶ │  Inference  │ ──▶ │  Analysis   │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
   Sequence          EpsilonMachine      AnalysisSummary
```

#### 3.2 Pipeline Composition
- The `>>` operator for chaining
- Functional design philosophy
- Immutability guarantees

```python
result = (
    GoldenMeanSource(p=0.5, _seed=42)
    >> TakeN(10000)
    >> CSSR(CSSRConfig(max_history=5))
)
summary = analyze(result.machine)
```

#### 3.3 Extensibility
- Protocol-based design
- Adding new sources
- Adding new inference algorithms

### 4. Empirical Evaluation (~3 pages)

#### 4.1 Experimental Setup
- Canonical processes as ground truth
- Data lengths: 1K, 10K, 100K, 1M symbols
- CSSR parameters: max_history ∈ {3, 5, 7}, significance ∈ {0.01, 0.05, 0.1}
- Metrics: state count accuracy, entropy rate error, complexity error

#### 4.2 Results: Golden Mean Process

| Data Length | True States | Inferred States | hμ Error | Cμ Error |
|-------------|-------------|-----------------|----------|----------|
| 1,000       | 2           | 3.2 ± 0.4       | 0.032    | 0.215    |
| 10,000      | 2           | 2.8 ± 0.3       | 0.018    | 0.142    |
| 100,000     | 2           | 2.1 ± 0.2       | 0.005    | 0.048    |
| 1,000,000   | 2           | 2.0 ± 0.0       | 0.001    | 0.012    |

*(Placeholder values - actual experiments to be run)*

#### 4.3 Results: Even Process

Similar table for Even Process (true: 3 states)

#### 4.4 Results: Periodic Processes

Accuracy vs period length

#### 4.5 Parameter Sensitivity

- Effect of `max_history`
- Effect of `significance` threshold
- Effect of `min_count`

#### 4.6 Discussion

- State over-estimation at small data sizes
- Entropy rate robustness
- Computational complexity scaling

### 5. Related Work (~1 page)

- Original CSSR papers (Shalizi & Klinkner)
- CMPY toolkit (Marzen et al.)
- Other epsilon-machine implementations
- Related inference methods (Bayesian, spectral)

### 6. Conclusion (~0.5 pages)

- Summary of contributions
- Future work:
  - Bayesian inference implementation
  - Spectral methods
  - Symbolic computation mode
  - Performance optimization

### References

Key citations:
- Shalizi & Klinkner (2004): CSSR algorithm
- Crutchfield & Young (1989): Computational mechanics
- Upper (1997): Epsilon-machine theory
- Marzen et al.: CMPY toolkit

## LaTeX Structure

```
paper/
├── main.tex           # Main document
├── abstract.tex       # Abstract
├── introduction.tex   # Section 1
├── background.tex     # Section 2
├── framework.tex      # Section 3
├── experiments.tex    # Section 4
├── related.tex        # Section 5
├── conclusion.tex     # Section 6
├── appendix.tex       # Appendices (proofs, code)
├── references.bib     # Bibliography
├── figures/
│   ├── architecture.tikz
│   ├── golden-mean-machine.tikz
│   ├── even-process-machine.tikz
│   ├── accuracy-vs-data.pdf
│   └── parameter-sensitivity.pdf
└── tables/
    ├── results-golden-mean.tex
    ├── results-even-process.tex
    └── results-periodic.tex
```

## Figures to Generate

### Figure 1: Framework Architecture
- Block diagram showing sources → inference → analysis
- Generated with TikZ

### Figure 2: Canonical Epsilon-Machines
- State diagrams for Golden Mean, Even Process
- Generated with TikZ or Graphviz

### Figure 3: Accuracy vs Data Length
- Plot showing state count error decreasing with data
- Line for each process type

### Figure 4: Entropy Rate Comparison
- True vs inferred entropy rate
- Error bars across multiple runs

### Figure 5: Parameter Sensitivity
- Heatmap of accuracy vs (max_history, significance)

## Experiments to Run

Create `experiments/` directory with scripts:

```python
# experiments/run_experiments.py
"""Run all experiments and save results."""

from emic.sources import GoldenMeanSource, EvenProcessSource, PeriodicSource
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze
import json
import itertools

PROCESSES = {
    "golden_mean": (GoldenMeanSource, {"p": 0.5}),
    "even": (EvenProcessSource, {"p": 0.5}),
    "periodic_3": (PeriodicSource, {"pattern": [0, 1, 2]}),
    "periodic_5": (PeriodicSource, {"pattern": [0, 1, 2, 3, 4]}),
}

DATA_LENGTHS = [1000, 10000, 100000]
SEEDS = list(range(20))  # 20 runs per config

MAX_HISTORIES = [3, 5, 7]
SIGNIFICANCES = [0.01, 0.05, 0.1]

def run_experiment(process_name, data_length, seed, max_history, significance):
    """Run single experiment and return metrics."""
    process_class, params = PROCESSES[process_name]
    source = process_class(**params, _seed=seed)

    data = list(itertools.islice(source, data_length))

    config = CSSRConfig(max_history=max_history, significance=significance)
    result = CSSR(config).infer(data)

    inferred = analyze(result.machine)
    true_analysis = analyze(source.true_machine)

    return {
        "process": process_name,
        "data_length": data_length,
        "seed": seed,
        "max_history": max_history,
        "significance": significance,
        "true_states": true_analysis.num_states,
        "inferred_states": inferred.num_states,
        "true_entropy_rate": true_analysis.entropy_rate,
        "inferred_entropy_rate": inferred.entropy_rate,
        "true_complexity": true_analysis.statistical_complexity,
        "inferred_complexity": inferred.statistical_complexity,
        "converged": result.converged,
    }
```

## Timeline

| Week | Task |
|------|------|
| 1 | Create LaTeX structure, write background section |
| 2 | Write framework section, generate architecture diagrams |
| 3 | Run experiments, generate figures |
| 4 | Write experiments section with results |
| 5 | Write introduction, conclusion, related work |
| 6 | Review, edit, polish |

## Acceptance Criteria

- [ ] Paper compiles with `pdflatex`
- [ ] All figures generated programmatically from data
- [ ] Experiments reproducible with single script
- [ ] Results tables auto-generated from experiment output
- [ ] Draft reviewed by collaborators
- [ ] Submitted to arXiv
