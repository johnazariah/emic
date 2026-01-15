# Specification 008: Documentation

## Overview

This specification defines the documentation deliverables for the `emic` framework, including API reference, user guide, and example notebooks showcasing pipelining and inference mechanisms.

## Deliverables

### 1. API Reference

**Location**: `docs/api/`

Auto-generated from docstrings using `mkdocs` + `mkdocstrings`.

#### Required Docstrings

All public APIs must have Google-style docstrings:

```python
def analyze(machine: EpsilonMachine) -> AnalysisSummary:
    """Compute complexity measures for an epsilon-machine.

    Calculates statistical complexity, entropy rate, and excess entropy
    using the stationary distribution over causal states.

    Args:
        machine: The epsilon-machine to analyze. Must be unifilar
            (deterministic given state and symbol).

    Returns:
        An AnalysisSummary containing all computed measures.

    Raises:
        ValueError: If the machine has no states.

    Example:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.analysis import analyze
        >>> source = GoldenMeanSource(p=0.5)
        >>> summary = analyze(source.true_machine)
        >>> print(f"Cμ = {summary.statistical_complexity:.4f}")
        Cμ = 0.9183
    """
```

#### Module Documentation

Each `__init__.py` must have a module-level docstring:

```python
"""Epsilon-machine inference algorithms.

This module provides algorithms for inferring epsilon-machines from
data sequences. The primary algorithm is CSSR (Causal State Splitting
Reconstruction).

Classes:
    CSSR: The CSSR inference algorithm.
    CSSRConfig: Configuration for CSSR.
    InferenceResult: Result container with pipeline support.

Example:
    >>> from emic.inference import CSSR, CSSRConfig
    >>> config = CSSRConfig(max_history=5)
    >>> result = CSSR(config).infer(data)
    >>> print(f"Inferred {len(result.machine.states)} states")
"""
```

### 2. User Guide

**Location**: `docs/guide/`

#### Chapters

1. **getting-started.md**
   - Installation (`pip install emic`)
   - First example: Golden Mean
   - Core concepts: epsilon-machine, causal state, unifilarity

2. **sources.md**
   - Synthetic sources and their `true_machine` property
   - Empirical sources from files/strings
   - Reproducibility with seeds
   - Transform pipeline (`>>` operator)

3. **inference.md**
   - CSSR algorithm overview
   - Configuration parameters and their effects
   - Interpreting results (convergence, state count)
   - Known limitations and tuning

4. **analysis.md**
   - Statistical complexity (Cμ)
   - Entropy rate (hμ)
   - Excess entropy (E)
   - Comparing true vs inferred machines

5. **visualization.md** (Phase 6)
   - State diagram rendering
   - LaTeX/TikZ export
   - Jupyter integration

6. **pipelines.md**
   - The `>>` operator philosophy
   - Composing sources, transforms, inference, analysis
   - Example pipelines

7. **advanced.md**
   - Custom sources
   - Custom inference algorithms
   - Extending the framework

### 3. Example Notebooks

**Location**: `notebooks/`

#### 3.1 `demo_inference.ipynb` ✅
Already created. Demonstrates basic inference and analysis.

#### 3.2 `pipeline_showcase.ipynb`
**Purpose**: Demonstrate end-to-end pipelines

```python
# Pipeline 1: Source → Transform → Inference → Analysis
result = (
    GoldenMeanSource(p=0.5, _seed=42)
    >> TakeN(10000)
    >> CSSR(CSSRConfig(max_history=5))
    >> analyze
)

# Pipeline 2: File → Inference → Comparison
empirical = SequenceData.from_file("data/sequence.txt")
inferred = (empirical >> CSSR() >> analyze)
true_machine = GoldenMeanSource(p=0.5).true_machine
compare(analyze(true_machine), inferred)

# Pipeline 3: Multiple inference algorithms
from emic.inference import CSSR, BayesianInference  # future

algorithms = [
    ("CSSR", CSSR(CSSRConfig(max_history=5))),
    ("Bayesian", BayesianInference(prior=...)),  # future
]

for name, algo in algorithms:
    result = data >> algo >> analyze
    print(f"{name}: {result.num_states} states, Cμ={result.statistical_complexity:.4f}")
```

#### 3.3 `complexity_landscape.ipynb`
**Purpose**: Explore how complexity varies with process parameters

- Vary `p` in Golden Mean from 0 to 1
- Plot Cμ, hμ, E as functions of p
- Compare theoretical vs inferred values

#### 3.4 `inference_comparison.ipynb` (Future)
**Purpose**: Compare inference algorithms

- CSSR vs Bayesian vs Spectral
- Accuracy vs data length
- Convergence characteristics

### 4. README Updates

The main `README.md` should include:

```markdown
## Quick Start

```python
from emic.sources import GoldenMeanSource
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Generate data from the Golden Mean process
source = GoldenMeanSource(p=0.5, _seed=42)
data = list(source.take(10000))

# Infer the epsilon-machine
result = CSSR(CSSRConfig(max_history=5)).infer(data)
print(f"Inferred {result.machine.num_states} states")

# Analyze complexity
summary = analyze(result.machine)
print(f"Statistical Complexity: {summary.statistical_complexity:.4f} bits")
print(f"Entropy Rate: {summary.entropy_rate:.4f} bits/symbol")
```

## Features

- **Inference**: CSSR algorithm for epsilon-machine reconstruction
- **Analysis**: Statistical complexity, entropy rate, excess entropy
- **Sources**: Golden Mean, Even Process, Periodic, Biased Coin
- **Pipelines**: Composable `>>` operator for clean workflows
- **Visualization**: State diagrams, LaTeX export (coming soon)

## Documentation

- [User Guide](docs/guide/)
- [API Reference](docs/api/)
- [Example Notebooks](notebooks/)
```

## Implementation Notes

### Documentation Tooling

```toml
# pyproject.toml additions
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
    "mkdocstrings[python]>=0.24",
]
```

### Build Commands

```bash
# Serve docs locally
mkdocs serve

# Build static site
mkdocs build
```

### CI Integration

Add to `.github/workflows/ci.yml`:

```yaml
docs:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v4
    - run: uv sync --extra docs
    - run: mkdocs build --strict
```

## Acceptance Criteria

- [ ] All public APIs have docstrings with examples
- [ ] User guide covers all major features
- [ ] Pipeline notebook demonstrates composition
- [ ] Complexity landscape notebook shows parameter exploration
- [ ] README has working quick-start example
- [ ] `mkdocs build` succeeds without warnings
- [ ] Documentation deployed to GitHub Pages
