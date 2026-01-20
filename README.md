# emic

[![CI](https://github.com/johnazariah/emic/actions/workflows/ci.yml/badge.svg)](https://github.com/johnazariah/emic/actions/workflows/ci.yml)
[![Docs](https://github.com/johnazariah/emic/actions/workflows/docs.yml/badge.svg)](https://johnazariah.github.io/emic/)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](https://github.com/johnazariah/emic)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**E**psilon **M**achine **I**nference & **C**haracterization

A Python framework for constructing and analyzing epsilon-machines based on computational mechanics.

📚 **[Documentation](https://johnazariah.github.io/emic/)** | 🚀 **[Getting Started](https://johnazariah.github.io/emic/getting-started/)**

## What is an Epsilon-Machine?

An **epsilon-machine** (ε-machine) is the minimal, optimal predictor of a stochastic process. Introduced by James Crutchfield and collaborators, ε-machines capture the intrinsic computational structure hidden in sequential data.

Key concepts:
- **Causal states**: Equivalence classes of histories that yield identical predictions
- **Statistical complexity** (Cμ): The entropy of the causal state distribution — a measure of structural complexity
- **Entropy rate** (hμ): The irreducible randomness in the process

ε-machines reveal the *emic* structure of a process — the computational organization that exists within the system itself, not imposed from outside.

## Features

- 🔮 **Inference**: Reconstruct ε-machines using multiple algorithms (CSSR, CSM, BSI, Spectral, NSD)
- 📊 **Analysis**: Compute complexity measures (Cμ, hμ, excess entropy, crypticity)
- 🎲 **Sources**: Built-in stochastic process generators (Golden Mean, Even Process, Biased Coin, Periodic)
- 🔗 **Pipeline**: Composable `>>` operator for source → inference → analysis workflows
- 📈 **Visualization**: State diagram rendering with Graphviz
- 📝 **Export**: LaTeX tables, TikZ diagrams, DOT, Mermaid, and JSON formats
- 🧩 **Extensible**: Protocol-based architecture for custom algorithms and sources

## Installation

```bash
pip install emic
```

Or install from source with [uv](https://github.com/astral-sh/uv):

```bash
git clone https://github.com/johnazariah/emic.git
cd emic
uv sync --dev
```

## Quick Start

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Generate data from the Golden Mean process (no consecutive 1s)
source = GoldenMeanSource(p=0.5, _seed=42)
data = TakeN(10_000)(source)

# Infer the epsilon-machine using CSSR
config = CSSRConfig(max_history=5, significance=0.001)
result = CSSR(config).infer(data)

# Analyze the inferred machine
summary = analyze(result.machine)
print(f"States: {len(result.machine.states)}")
print(f"Statistical Complexity: Cμ = {summary.statistical_complexity:.4f}")
print(f"Entropy Rate: hμ = {summary.entropy_rate:.4f}")
```

### Pipeline Composition

Chain operations using the `>>` operator:

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Compose source and transforms
source = GoldenMeanSource(p=0.5, _seed=42)
data = source >> TakeN(10_000)

# Infer and analyze
config = CSSRConfig(max_history=5, significance=0.001)
result = CSSR(config).infer(data)
summary = analyze(result.machine)

print(summary)
```

## Supported Processes

| Process | Description | True States |
|---------|-------------|-------------|
| **Golden Mean** | No consecutive 1s allowed | 2 |
| **Even Process** | Even number of 1s between 0s | 2 |
| **Biased Coin** | i.i.d. Bernoulli process | 1 |
| **Periodic** | Deterministic repeating pattern | n (period length) |

## Project Status

✅ **Core implementation complete** — The framework is functional with:
- Multiple inference algorithms: CSSR, CSM, BSI, Spectral, NSD
- Full analysis suite (Cμ, hμ, excess entropy, crypticity)
- Synthetic and empirical data sources
- Pipeline composition
- 194 tests with 90% coverage

📚 **[Full documentation available](https://johnazariah.github.io/emic/)**

## Etymology

The name **emic** works on multiple levels:

1. **Acronym**: **E**psilon **M**achine **I**nference & **C**haracterization
2. **Linguistic**: In linguistics/anthropology, *emic* refers to analysis from within the system — understanding structure on its own terms. This resonates with computational mechanics: ε-machines reveal the intrinsic structure of a process.
3. **Phonetic**: Pronounced "EE-mik" or "EH-mic" — a nod to "ε-machine"

## References

- Crutchfield, J.P. (1994). ["The Calculus of Emergence: Computation, Dynamics, and Induction"](https://doi.org/10.1016/0167-2789(94)90273-9). *Physica D*.
- Shalizi, C.R. & Crutchfield, J.P. (2001). ["Computational Mechanics: Pattern and Prediction, Structure and Simplicity"](https://arxiv.org/abs/cond-mat/9907176). *Journal of Statistical Physics*.
- Crutchfield, J.P. & Young, K. (1989). "Inferring Statistical Complexity". *Physical Review Letters*.

## Contributing

Contributions are welcome! See the [Contributing Guide](https://johnazariah.github.io/emic/contributing/) for details.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

John Azariah ([@johnazariah](https://github.com/johnazariah))
