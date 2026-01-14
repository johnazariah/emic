# emic

[![CI](https://github.com/johnazariah/emic/actions/workflows/ci.yml/badge.svg)](https://github.com/johnazariah/emic/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/johnazariah/emic/branch/main/graph/badge.svg)](https://codecov.io/gh/johnazariah/emic)
[![PyPI version](https://badge.fury.io/py/emic.svg)](https://pypi.org/project/emic/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**E**psilon **M**achine **I**nference & **C**haracterization

A Python framework for constructing and analyzing epsilon-machines based on computational mechanics.

> ⚠️ **This package is under active development.** The API is not yet stable.

## What is an Epsilon-Machine?

An **epsilon-machine** (ε-machine) is the minimal, optimal predictor of a stochastic process. Introduced by James Crutchfield and collaborators, ε-machines capture the intrinsic computational structure hidden in sequential data.

Key concepts:
- **Causal states**: Equivalence classes of histories that yield identical predictions
- **Statistical complexity** (Cμ): The entropy of the causal state distribution — a measure of structural complexity
- **Entropy rate** (hμ): The irreducible randomness in the process

ε-machines reveal the *emic* structure of a process — the computational organization that exists within the system itself, not imposed from outside.

## Features (Planned)

- 🔮 **Inference**: Reconstruct ε-machines from observed sequences (CSSR algorithm and more)
- 📊 **Analysis**: Compute complexity measures (Cμ, hμ, excess entropy, crypticity)
- 🎲 **Sources**: Built-in stochastic process generators (Golden Mean, Even Process, etc.)
- 📈 **Visualization**: State diagrams, transition matrices, complexity curves
- 📝 **LaTeX Export**: Publication-ready figures and tables
- 🧩 **Extensible**: Protocol-based architecture for custom algorithms and sources

## Installation

```bash
pip install emic
```

## Quick Start

```python
import emic

# Coming soon!
```

## Project Status

🚧 **Planning phase**

We're currently designing the architecture and writing specifications. See the `.project/` directory for:
- `adr/` — Architecture Decision Records
- `specifications/` — Feature specifications
- `plan/` — Execution tracking

## Etymology

The name **emic** works on multiple levels:

1. **Acronym**: **E**psilon **M**achine **I**nference & **C**haracterization
2. **Linguistic**: In linguistics/anthropology, *emic* refers to analysis from within the system — understanding structure on its own terms. This resonates with computational mechanics: ε-machines reveal the intrinsic structure of a process.
3. **Phonetic**: Sounds like "ε-mic" (epsilon-machine)

## References

- Crutchfield, J.P. (1994). ["The Calculus of Emergence: Computation, Dynamics, and Induction"](https://doi.org/10.1016/0167-2789(94)90273-9). *Physica D*.
- Shalizi, C.R. & Crutchfield, J.P. (2001). ["Computational Mechanics: Pattern and Prediction, Structure and Simplicity"](https://arxiv.org/abs/cond-mat/9907176). *Journal of Statistical Physics*.
- Crutchfield, J.P. & Young, K. (1989). "Inferring Statistical Complexity". *Physical Review Letters*.

## Contributing

Contributions are welcome! Please see the architecture decision records in `.project/adr/` to understand the design principles.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

John Azariah ([@johnazariah](https://github.com/johnazariah))
