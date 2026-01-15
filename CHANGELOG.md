# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-15

### Added

#### Core Types
- `EpsilonMachine` - Immutable representation of ε-machines with causal states and transitions
- `CausalState` - Individual causal states with emission probabilities
- `Alphabet` - Symbol alphabet handling
- `Probability` - Validated probability distributions

#### Sources
- `GoldenMeanSource` - Golden Mean process (no consecutive 1s)
- `EvenProcessSource` - Even Process (even 1s between 0s)
- `BiasedCoinSource` - i.i.d. Bernoulli process
- `PeriodicSource` - Deterministic periodic patterns
- `SequenceData` - Empirical data from sequences/files
- Source transforms: `skip()`, `take()`

#### Inference
- `CSSR` - Causal State Splitting Reconstruction algorithm
- `CSSRConfig` - Configuration with `max_history`, `significance`, `min_count`
- Post-merge state optimization for finite-sample effects
- `InferenceResult` - Result container with convergence info

#### Analysis
- `analyze()` - Compute complexity measures from machines
- `Analyzer` - Pipeline-compatible analyzer
- Statistical complexity (Cμ)
- Entropy rate (hμ)
- Excess entropy (E)
- `AnalysisSummary` - Results container

#### Output
- `render_diagram()` - Graphviz state diagram rendering
- `to_latex()` - LaTeX export for publications
- `to_json()` / `from_json()` - JSON serialization

#### Pipeline
- `>>` operator for composing Source → Inference → Analysis workflows

#### Infrastructure
- 194 tests with 90% coverage
- Pre-commit hooks (ruff, pyright, docstring checks)
- MkDocs documentation with Material theme
- GitHub Actions CI/CD
- GitHub Pages documentation hosting

### References

- Crutchfield, J.P. (1994). "The Calculus of Emergence". *Physica D*.
- Shalizi, C.R. & Crutchfield, J.P. (2001). "Computational Mechanics: Pattern and Prediction, Structure and Simplicity". *Journal of Statistical Physics*.

[0.1.0]: https://github.com/johnazariah/emic/releases/tag/v0.1.0
