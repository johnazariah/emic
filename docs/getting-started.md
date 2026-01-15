# Getting Started

This guide will help you get up and running with `emic` in just a few minutes.

## Installation

Install from PyPI:

```bash
pip install emic
```

Or install from source for development:

```bash
git clone https://github.com/johnazariah/emic.git
cd emic
pip install -e ".[dev]"
```

## Your First Epsilon-Machine

Let's infer an epsilon-machine from the **Golden Mean** process — a simple stochastic process where consecutive 1s are forbidden.

### Step 1: Generate Data

```python
from emic.sources import GoldenMeanSource

# Create a source with p=0.5 (probability of emitting 1 when allowed)
source = GoldenMeanSource(p=0.5, seed=42)

# Generate 10,000 symbols
data = source.take(10_000)
print(f"First 50 symbols: {data[:50]}")
```

### Step 2: Infer the Machine

```python
from emic.inference import CSSR, CSSRConfig

# Configure the CSSR algorithm
config = CSSRConfig(
    max_history=5,      # Maximum history length to consider
    significance=0.001, # Significance level for state splitting
)

# Run inference
result = CSSR(config).infer(data)

print(f"Inferred {len(result.machine.states)} states")
print(f"Converged: {result.converged}")
```

### Step 3: Analyze the Machine

```python
from emic.analysis import analyze

summary = analyze(result.machine)

print(f"Statistical Complexity: Cμ = {summary.statistical_complexity:.4f}")
print(f"Entropy Rate: hμ = {summary.entropy_rate:.4f}")
print(f"Excess Entropy: E = {summary.excess_entropy:.4f}")
```

### Step 4: Visualize (Optional)

```python
from emic.output import render_diagram

# Render to a file (requires graphviz)
render_diagram(result.machine, "golden_mean.png")
```

## Using Pipelines

The `>>` operator lets you compose operations:

```python
from emic.sources import GoldenMeanSource
from emic.inference import CSSR, CSSRConfig
from emic.analysis import Analyzer

# One-liner pipeline
result = (
    GoldenMeanSource(p=0.5, seed=42)
    >> CSSR(CSSRConfig(max_history=5))
    >> Analyzer()
)

print(result.summary.statistical_complexity)
```

## Compare with True Machine

Synthetic sources provide their theoretical epsilon-machine:

```python
from emic.sources import GoldenMeanSource
from emic.analysis import analyze

source = GoldenMeanSource(p=0.5)

# Get the true (theoretical) machine
true_machine = source.true_machine
true_summary = analyze(true_machine)

print(f"True Cμ = {true_summary.statistical_complexity:.4f}")
print(f"True states: {len(true_machine.states)}")
```

## Next Steps

- [Sources Guide](guide/sources.md) — Learn about available data sources
- [Inference Guide](guide/inference.md) — Deep dive into CSSR parameters
- [Analysis Guide](guide/analysis.md) — Understanding complexity measures
- [API Reference](api/index.md) — Full API documentation
