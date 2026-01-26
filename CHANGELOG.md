# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-01-26

### Added
- **Spectral Learning improvements**: Complete SVD-based spectral learning with belief state clustering and automatic rank selection
- **Algorithm benchmark suite**: Comprehensive benchmarking framework for comparing inference algorithms across processes and sample sizes
- **Noise robustness experiments**: Analysis of algorithm behavior under observation noise with entropy rate and statistical complexity metrics
- **Visualization gallery**: State diagram visualization examples with GraphViz integration
- **Comprehensive tutorial**: 32-page computational mechanics tutorial with worked examples
- **Technical report**: 49-page technical documentation of the emic library
- **Golden tests**: BSI, NSD, and Spectral algorithm golden tests against known processes

### Changed
- Refactored Spectral algorithm with modular belief state clustering for improved interpretability
- Expanded user guide with Spectral learning deep-dive and parameter formulas

### Fixed
- macOS devcontainer compatibility and git user configuration
- Expired Yarn repository in devcontainer base image

## [0.2.1] - 2026-01-20

### Fixed
- Fixed 6 failing doctest examples (iterator usage, seed values, floating-point comparison)

### Changed
- Rewrote user guides (inference, sources, analysis, pipelines) to match current API
- Updated all API reference pages to include complete module exports
- Refreshed README with correct examples and updated feature descriptions

### Added
- Documentation update prompt for systematic doc audits

## [0.2.0] - 2026-01-18

### Added

#### Alternative Inference Algorithms
- **CSM** (Causal State Merging) - Bottom-up algorithm that starts with finest partition and iteratively merges states with similar predictive distributions
  - Supports four distance metrics: KL divergence, Hellinger, total variation, chi-squared
  - `CSMConfig` with `history_length`, `merge_threshold`, `distance_metric`, `hierarchical`

- **BSI** (Bayesian Structural Inference) - MCMC-based Bayesian approach
  - Gibbs sampling over state assignments with Dirichlet-multinomial likelihood
  - BIC-based model selection for automatic state count
  - `BSIConfig` with `max_states`, `alpha_prior`, `n_samples`, `burnin`, `thin`, `seed`

- **NSD** (Neural State Discovery) - Clustering-based approach
  - History embeddings from predictive distributions
  - K-means++ clustering with automatic k selection via information-theoretic scoring
  - `NSDConfig` with `max_states`, `history_length`, `embedding_dim`, `n_iterations`, `seed`

- **Spectral** - Spectral learning via Hankel matrix decomposition
  - Simplified SVD implementation (no NumPy dependency)
  - Automatic rank selection via singular value threshold
  - `SpectralConfig` with `max_history`, `rank_threshold`, `rank`, `regularization`

#### Documentation
- Project standards documents (coding, documentation, experimentation, governance)
- Specification 010-015 for algorithms, experiments, and quantum roadmap
- CSM demonstration notebook
- AI assistant instructions (copilot-instructions.md)
- Release protocol prompt (prepare-release.prompt.md)

#### Testing
- 309 tests with 92% coverage (up from 194 tests, 90% coverage)
- Comprehensive tests for all new inference algorithms
- Golden tests comparing algorithm outputs
- Edge case tests for CSSR partition operations
- Source validation tests

### Changed
- Updated roadmap to reflect completed M3 (Alternative Algorithms) milestone
- All inference algorithms now follow unified `InferenceAlgorithm` protocol
- Improved project organization with `.project/` structure

## [0.1.1] - 2026-01-15

### Fixed
- README now links to published documentation at johnazariah.github.io/emic
- Updated contributing section to link to docs site
- Fixed etymology pronunciation description

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

[0.2.1]: https://github.com/johnazariah/emic/releases/tag/v0.2.1
[0.2.0]: https://github.com/johnazariah/emic/releases/tag/v0.2.0
[0.1.1]: https://github.com/johnazariah/emic/releases/tag/v0.1.1
[0.1.0]: https://github.com/johnazariah/emic/releases/tag/v0.1.0
