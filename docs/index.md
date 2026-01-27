# emic

**E**psilon **M**achine **I**nference & **C**haracterization

A Python framework for constructing and analyzing epsilon-machines based on computational mechanics.

## What is an Epsilon-Machine?

An **epsilon-machine** (ε-machine) is the minimal, optimal predictor of a stochastic process. Introduced by James Crutchfield and collaborators, ε-machines capture the intrinsic computational structure hidden in sequential data.

## Features

| Feature | Description |
|---------|-------------|
| 🔮 **[Inference](guide/inference.md)** | Reconstruct ε-machines using multiple algorithms (CSSR, CSM, BSI, Spectral, NSD) |
| 📊 **[Analysis](guide/analysis.md)** | Compute complexity measures: statistical complexity (Cμ), entropy rate (hμ), excess entropy |
| 🎲 **[Sources](guide/sources.md)** | Built-in stochastic process generators and empirical data loading |
| 🔗 **[Pipelines](guide/pipelines.md)** | Compose workflows with the `>>` operator |
| 🧪 **[Experiments](guide/experiments.md)** | CLI for reproducible algorithm benchmarking and validation |

## Quick Example

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Generate data from the Golden Mean process
source = GoldenMeanSource(p=0.5, _seed=42)
data = TakeN(10_000)(source)

# Infer the epsilon-machine
config = CSSRConfig(max_history=5, significance=0.001)
result = CSSR(config).infer(data)

# Analyze
summary = analyze(result.machine)
print(f"States: {len(result.machine.states)}")
print(f"Cμ = {summary.statistical_complexity:.4f}")
```

## Installation

```bash
pip install emic
```

## Key Concepts

- **Causal states**: Equivalence classes of histories that yield identical predictions
- **Statistical complexity** (Cμ): The entropy of the causal state distribution
- **Entropy rate** (hμ): The irreducible randomness in the process
- **Unifilarity**: Given a state and symbol, the next state is deterministic

## References

- Crutchfield, J.P. (1994). ["The Calculus of Emergence"](https://doi.org/10.1016/0167-2789(94)90273-9). *Physica D*.
- Shalizi, C.R. & Crutchfield, J.P. (2001). ["Computational Mechanics: Pattern and Prediction, Structure and Simplicity"](https://arxiv.org/abs/cond-mat/9907176). *Journal of Statistical Physics*.
