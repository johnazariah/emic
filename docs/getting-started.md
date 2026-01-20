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
from emic.sources import GoldenMeanSource, TakeN

# Create a source with p=0.5 (probability of emitting 0 when in state A)
source = GoldenMeanSource(p=0.5, _seed=42)

# Generate 10,000 symbols using the TakeN transform
data = TakeN(10_000)(source)
print(f"First 50 symbols: {list(data)[:50]}")
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
from emic.output import render_state_diagram

# Render to a Graphviz diagram (requires graphviz)
diagram = render_state_diagram(result.machine)
diagram.render("golden_mean", format="png")
```

## Using Pipelines

The `>>` operator lets you compose source transforms:

```python
from emic.sources import GoldenMeanSource, TakeN, SkipN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Chain transforms with >> operator
source = GoldenMeanSource(p=0.5, _seed=42)
data = source >> SkipN(1000) >> TakeN(10_000)  # Skip burn-in, then take

# Run inference
result = CSSR(CSSRConfig(max_history=5)).infer(data)

# Analyze
summary = analyze(result.machine)
print(f"Cμ = {summary.statistical_complexity:.4f}")
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

## Other Inference Algorithms

While CSSR is the default, `emic` provides multiple inference algorithms:

```python
from emic.inference import CSM, CSMConfig
from emic.inference import BSI, BSIConfig
from emic.inference import Spectral, SpectralConfig
from emic.inference import NSD, NSDConfig

# Causal State Merging (bottom-up approach)
csm_result = CSM(CSMConfig(history_length=5)).infer(data)

# Bayesian Structural Inference (uncertainty quantification)
bsi_result = BSI(BSIConfig(max_states=5, n_samples=500)).infer(data)

# Spectral learning (polynomial time)
spectral_result = Spectral(SpectralConfig(max_history=5)).infer(data)

# Neural State Discovery (clustering-based)
nsd_result = NSD(NSDConfig(max_states=5)).infer(data)
```

## Next Steps

- [Sources Guide](guide/sources.md) — Learn about available data sources
- [Inference Guide](guide/inference.md) — All inference algorithms explained
- [Analysis Guide](guide/analysis.md) — Understanding complexity measures
- [Pipelines Guide](guide/pipelines.md) — Composing workflows
- [API Reference](api/index.md) — Full API documentation
