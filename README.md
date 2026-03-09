# emic

[![CI](https://github.com/johnazariah/emic/actions/workflows/ci.yml/badge.svg)](https://github.com/johnazariah/emic/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/emic)](https://pypi.org/project/emic/)
[![Docs](https://github.com/johnazariah/emic/actions/workflows/docs.yml/badge.svg)](https://johnazariah.github.io/emic/)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](https://github.com/johnazariah/emic)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18869131.svg)](https://doi.org/10.5281/zenodo.18869131)

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
- 📊 **Analysis**: Compute complexity measures (Cμ, hμ, excess entropy E, crypticity χ)
- 🎲 **Sources**: Built-in stochastic process generators (Golden Mean, Even Process, Biased Coin, Periodic) with noise transforms (BitFlipNoise)
- 🔗 **Pipeline**: Composable `>>` operator for source → inference → analysis workflows
- 🧪 **Experiments**: CLI and framework for reproducible algorithm benchmarking
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

## Built-in Sources

| Process | Description | True States |
|---------|-------------|-------------|
| **Golden Mean** | No consecutive 1s allowed | 2 |
| **Even Process** | Even number of 1s between 0s | 2 |
| **Biased Coin** | i.i.d. Bernoulli process | 1 |
| **Periodic** | Deterministic repeating pattern | n (period length) |

## Experiments

Run reproducible experiments to evaluate algorithm performance:

```bash
# Run all experiments with parallel execution
emic-experiment --all --parallel 4

# Quick mode for development
emic-experiment --quick

# List available experiments
emic-experiment --list
```

### Algorithm Accuracy (January 2026)

| Algorithm | State Count Accuracy | Cμ Error |
|-----------|---------------------|----------|
| **Spectral** | 85% (100% at N≥10K) | 0.15 |
| **CSSR** | 82% | **0.05** |
| NSD | 73% | 0.12 |
| CSM | 39% | 0.10 |
| BSI | 32% | 0.53 |

See the [Experiments Guide](https://johnazariah.github.io/emic/guide/experiments/) for full details.

## Project Status

✅ **Core implementation complete** — The framework is functional with:
- Multiple inference algorithms: CSSR, CSM, BSI, Spectral, NSD
- Full analysis suite (Cμ, hμ, excess entropy E, crypticity χ)
- Synthetic and empirical data sources with noise transforms
- Pipeline composition
- 429 tests with 82%+ coverage
- Deep dive documentation: CSSR, Spectral Learning, Complexity Measures, Working with Real Data

📚 **[Full documentation available](https://johnazariah.github.io/emic/)**

## Testing

All 429 tests are catalogued in the [Testing Register](.project/testing-register.md), each with a plain English intent and classified by kind:

| Kind | Count | What it verifies |
|------|-------|------------------|
| **Fact** | 280 | Deterministic structural truths — immutability, validation, construction |
| **Theory** | 73 | Mathematical relationships from computational mechanics — Cμ, hμ, E, χ values |
| **Property** | 30 | Invariants across inputs — reproducibility, algorithm agreement, stochastic validity |

Test categories:
- **Unit tests** — Types, analysis measures, all 5 inference algorithms, sources, transforms, output formats
- **Golden tests** — Algorithms verified against analytically known ε-machines (Golden Mean, Even Process, Biased Coin, Periodic)
- **Integration tests** — Pipeline composition from source through inference to analysis
- **Machine invariant tests** — Every algorithm's output validated for stochastic correctness (transition sums ≤ 1.0)

Pre-commit hooks enforce that the testing register is updated whenever tests change.

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
