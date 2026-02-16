# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2026-02-16

### Added
- **Publications workflow**: Added dedicated `.github/workflows/publications.yml` to build and publish versioned tutorial/review/technical PDF artifacts independently of package release.
- **Journal stewardship prompt**: Added `.github/prompts/journal-steward-agent.prompt.md` for repeatable paper-governance checks across projects.
- **Shared paper governance assets**:
  - Canonical author profile in `.project/research/computational-mechanics-review/shared/metadata/author-profile.yaml`
  - Shared AI disclosure snippets for Markdown and LaTeX
  - New-paper setup checklist in `paper-framework/new-paper-checklist.md`

### Changed
- **Release packaging policy**: Release workflow now attaches a JOSS submission bundle (`paper.md` + `paper.bib` tarball) instead of attaching paper PDFs.
- **Prompt and checklist alignment**: Updated release and paper prompts/checklists to reflect:
  - Shared bibliography source of truth
  - Citation key convention `{first-author-name}{year}[{tag}]`
  - Separate publication pipeline for PDFs
- **Paper metadata consistency**: Standardized author/profile fields and AI disclosure wording across JOSS/tutorial/review/technical papers.

### Fixed
- **LaTeX warning hygiene**: Reduced recurring non-blocking warnings in paper sources (`caption` hypcap override, `hyperref` PDF-string substitutions, `fancyhdr` headheight).

## [0.5.0] - 2026-01-28

### Fixed
- **Spectral algorithm**: Complete rewrite of Hankel matrix construction and belief state computation following Hsu, Kakade & Zhang (2012). Fixed three critical bugs:
  - Hankel matrix now uses joint probabilities P(history, future) instead of conditional P(future|history)
  - Symbol-extended matrices H_x now correctly place the symbol *between* history and future
  - Initial/infinite belief vectors computed from SVD decomposition instead of eigenvectors
- **Spectral accuracy**: Algorithm now achieves 100% state recovery on benchmark processes (was 89% due to bugs)

### Changed
- **Benchmarks infrastructure**: Unified experimentation platform using `emic-experiment` CLI instead of ad-hoc scripts
- Benchmark Makefile now supports `make fast` (skip slow BSI) and `make analyze` targets

## [0.4.1] - 2026-01-27

### Fixed
- **CSSR IID detection**: Improved detection of IID processes by skipping history-dependent analysis for L=0, resolving the v0.4.0 known issue where CSSR found spurious states on biased coin processes. CSSR accuracy improved from 67% to 82%.

### Documentation
- Updated experiments guide with `--algorithms` filter flag
- Updated benchmark data across all documentation (README, guides, research papers)

## [0.4.0] - 2026-01-27

### Added
- **Experiments framework**: New `emic.experiments` module with CLI (`emic-experiment`) for reproducible algorithm benchmarking
- **Parallel execution**: Run experiments with `--parallel N` for multi-worker execution
- **Sharded execution**: Distribute experiments across machines with `--shard M/N` and `--combine`
- **Experiment results**: Baseline results comparing CSSR, Spectral, CSM, and BSI across accuracy, convergence, and scalability
- **Experiments guide**: Comprehensive documentation for the experimentation framework

### Results
- **Algorithm comparison** (state count recovery):
  - Spectral: 89% accuracy (best overall)
  - CSSR: 56% accuracy, lowest Cμ error (0.053)
  - CSM: 33% accuracy
  - BSI: 33% accuracy
- **1,552 experiment records** across 4 algorithms, 3 processes, 3 experiment types

### Known Issues
- **CSSR regression on IID processes**: CSSR with `max_history >= 5` finds spurious states on biased coin (IID) processes. Previous versions correctly found 1 state; current version finds 3. This was introduced in v0.3.1 commit 8fe9a9f. Workaround: use `max_history <= 4` for IID processes, or use Spectral algorithm.

## [0.3.1] - 2026-01-26

### Added
- **CSSR deep dive**: Comprehensive guide explaining suffix trees, chi-squared testing, state splitting/merging with worked Golden Mean example
- **Complexity measures explained**: Educational guide covering Cμ, hμ, E, χ with intuition, formulas, and examples
- **Working with real data**: Practical guide for empirical sequences covering preprocessing, alphabet design, noise handling, and validation
- **MathJax support**: LaTeX formula rendering in documentation for mathematical expressions
- **BitFlipNoise documentation**: Added to sources guide and API reference

### Changed
- Reorganized User Guide navigation with Deep Dives subsection
- Updated algorithm recommendation to suggest Spectral for general use
- Added cross-references to emic documentation in research papers

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
