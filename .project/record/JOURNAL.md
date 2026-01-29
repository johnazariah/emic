# Project Journal

*A chronological record of work done on the emic project.*

---

## 2026

### January 28-29, 2026

**Session Focus**: Quantum Complexity Implementation

**Commits**: `617a0df`, `a044930`

**Completed**:

1. **Fixed `excess_entropy()` Bug**
   - Previous implementation incorrectly claimed $E = C_\mu$ for unifilar machines
   - Rewrote using block entropy convergence method
   - Added `block_entropy()` and `crypticity()` functions
   - Golden Mean now correctly shows: $C_\mu = 0.918$, $E = 0.252$, $\chi = 0.667$

2. **Added Perturbed Coin Source**
   - Canonical example for quantum advantage
   - Two states with symmetric transitions
   - Known analytic formulas for validation

3. **Implemented Quantum Complexity Measures**
   - `quantum_signal_states()`: Construct $|s_j\rangle$ for each causal state
   - `quantum_density_matrix()`: Compute $\rho = \sum_j \pi_j |s_j\rangle\langle s_j|$
   - `quantum_complexity()`: Von Neumann entropy $S(\rho)$
   - `quantum_advantage()`: $\Delta_q = C_\mu - C_q$
   - `decoherence_trajectory()`: Track $C_q(\gamma)$ as $\gamma \to 1$

4. **Created Validation Notebook**
   - `notebooks/quantum_validation.ipynb`
   - Validates $C_q$ matches analytic formula exactly
   - Confirms hierarchy $E \leq C_q \leq C_\mu$ for all test cases
   - Shows decoherence trajectory from quantum to classical

5. **Updated Agent Instructions**
   - Added `write-notes` command for session wrap-up
   - Formalized research breadcrumb requirements

**Key Insight**: The block entropy must be computed *without* knowing the initial state - marginalizing over the stationary distribution. The naive formula that conditions on the state gives $E = C_\mu$, which is wrong.

**Discovery**: The validation plan table had incorrect $C_q$ values that violated $E \leq C_q$. Our implementation is correct.

**Files Created**:
- `src/emic/analysis/quantum.py`
- `src/emic/sources/synthetic/perturbed_coin.py`
- `notebooks/quantum_validation.ipynb`
- `.project/notes/2026-01-28T21-19-fix-excess-entropy.md`
- `.project/notes/2026-01-28T21-19-quantum-research-deliverables.md`
- `.project/notes/2026-01-29T00-39-quantum-complexity-implementation.md`

**Test Results**: 421 tests passing

---

### January 29, 2026 (continued)

**Session Focus**: Decoherence Trajectory Investigation (Investigation 1)

**Commits**: `420c961`, `13141a5`, `239467d`, `8da4873`

**Completed**:

1. **Fixed Validation Plan Table**
   - Corrected $C_q$ values that violated hierarchy $E \leq C_q \leq C_\mu$
   - Added decoherence trajectory reference values for p=0.3

2. **Created Decoherence Trajectory Notebook**
   - `notebooks/decoherence_trajectory.ipynb`
   - Traced $C_q(\gamma)$ for Perturbed Coin at p = 0.1, 0.2, 0.3, 0.4, 0.5
   - Compared with Golden Mean and Even Process
   - Analyzed concavity via numerical second derivatives

3. **Key Findings**
   - All trajectories for processes with quantum advantage are **concave**
   - Quantum advantage is fragile: even weak dephasing ($\gamma \approx 0.1$) destroys much of it
   - Signal state overlap predicts quantum advantage (overlap > 0 → advantage exists)
   - **Even Process anomaly**: dephasing can exceed $C_\mu$ for orthogonal signal states!

4. **Discovered: Dephasing ≠ Classicalization**
   - The Even Process has $C_q(\gamma=1) = 1.585$ vs $C_\mu = 0.918$
   - Dephasing removes coherences but doesn't return to the classical mixed state
   - This only affects processes without quantum advantage (orthogonal signal states)

**Key Insight**: The decoherence trajectory interpretation only works for processes with non-orthogonal signal states. For orthogonal states, the dephased density matrix is not equivalent to the classical model.

**Files Created**:
- `notebooks/decoherence_trajectory.ipynb`
- `.project/notes/2026-01-29T01-01-decoherence-trajectory-investigation.md`

**Test Results**: 421 tests passing

**Next Steps**:
1. Add unit tests for decoherence trajectory
2. Investigate mathematical structure of concavity
3. Consider alternative decoherence channels
2. Add unit tests for quantum measures
3. Begin Investigation 1 (decoherence trajectory analysis)

---

### January 27, 2026

**Session Focus**: Quantum Emergence Research Area

**Completed**:

1. **Created new research area: quantum-emergence/**
   - Focus on extending emic toward quantum computational mechanics
   - Goal: Re-derive Mile Gu's results on quantum memory advantage
   - Structure: review/, experiments/, theory/, implementation/

2. **Literature Review Setup**
   - Created annotated bibliography of key papers
   - Documented core concepts: $C_q$, quantum causal states, crypticity
   - Key papers: Gu et al. (2012), Tan et al. (2014), Garner et al. (2017)

3. **Mathematical Framework**
   - Documented the key inequality: $E \leq C_q \leq C_\mu$
   - Crypticity $\chi = C_\mu - E$ as target for quantum elimination
   - Non-orthogonal encoding as source of quantum advantage

**Key Insight**: The gap between statistical complexity ($C_\mu$) and excess entropy ($E$) represents information waste that quantum models can eliminate. emic already computes both quantities—adding crypticity computation is a natural next step.

**Files Created**:
- `.project/research/quantum-emergence/README.md`
- `.project/research/quantum-emergence/review/README.md`
- `.project/research/quantum-emergence/review/key-papers.md`
- `.project/research/quantum-emergence/review/concepts.md`

**Next Steps**:
1. Add crypticity ($\chi = C_\mu - E$) to emic's analysis module
2. Read and summarize key papers in detail
3. Identify validation targets (perturbed coin, etc.)
4. Design quantum epsilon-machine representation

---

### January 26, 2026 (Evening)

**Session Focus**: General-Purpose Benchmarking Tool

**Completed**:

1. **ADR-008: Benchmarking Tool Architecture**
   - Documented design decision for thin core + rich experiments approach
   - Key principle: Data collection separated from formatting
   - Output: Timestamped Parquet/JSON results + metadata.yaml
   - Downstream consumers (papers, CI) handle their own formatting

2. **Implemented `emic.experiments` Module**
   - `schema.py`: BenchmarkResult dataclass, ResultsWriter, Parquet/JSON I/O
   - `registry.py`: ProcessRegistry and AlgorithmRegistry for declarative registration
   - `config.py`: YAML-based ExperimentConfig and BenchmarkConfig
   - `runner.py`: Core runner with SIGALRM timeout handling, progress tracking
   - `cli.py`: CLI entry point (`emic-benchmark`)

3. **CLI Features**
   - `emic-benchmark --all`: Run all experiments
   - `emic-benchmark accuracy`: Run specific experiment
   - `emic-benchmark --quick`: Skip slow algorithms, use reduced sample sizes
   - `emic-benchmark --list`: List available experiments
   - Results saved to `experiments/results/<timestamp>/`
   - `latest` symlink for convenience

4. **Default Experiments**
   - accuracy: Measure algorithm accuracy on canonical processes
   - convergence: How accuracy changes with sample size
   - scalability: Runtime scaling with data size

5. **Tests**
   - Added 17 unit tests for benchmarks module
   - All 351 tests passing

**Files Created**:
- `src/emic/benchmarks/__init__.py`
- `src/emic/benchmarks/schema.py`
- `src/emic/benchmarks/registry.py`
- `src/emic/benchmarks/config.py`
- `src/emic/benchmarks/runner.py`
- `src/emic/benchmarks/cli.py`
- `tests/unit/test_benchmarks.py`
- `.project/adr/008-benchmarking-tool.md`
- `experiments/results/.gitkeep`

**Files Modified**:
- `pyproject.toml`: Added `emic-benchmark` script entry point, `benchmarks` optional deps

**Branch**: `feature/benchmarks` (worktree at `/workspace/worktrees/benchmarks`)

**Next Steps**:
- Merge to main after review
- Migrate existing paper benchmarks to use new tool
- Add more experiment types as needed

---

### January 26, 2026

**Session Focus**: CSSR Algorithm Correctness & Benchmarking

**Completed**:

1. **CSSR Algorithm Validation Against Shalizi (2004)**
   - Verified emic CSSR matches published benchmarks
   - Key result: At N=10,000, CSSR correctly finds 2 states for Even Process and Golden Mean
   - This matches Shalizi's Table 1 showing 100% correct at N=10^4, α=10^-3, L≥3

2. **Quick Benchmark Script**
   - Created `scripts/quick_benchmark.py` for fast validation (~1 minute vs 6+ hours for full benchmark)
   - Tests CSSR, Spectral, and CSM on Even Process, Golden Mean, Biased Coin
   - Sample sizes: N=1K, 10K, 100K
   - Results:
     - CSSR: 67% overall, 100% at N≥100K
     - Spectral: 100% across all sample sizes (best performer)
     - CSM: 56% overall

3. **Documentation Updates**
   - Updated `docs/guide/cssr-deep-dive.md` with new Section 11 "Algorithm Correctness and Benchmarks"
   - Added validation tables showing Shalizi benchmark comparison
   - Documented sample size sensitivity guidelines

4. **Technical Report Updates**
   - Updated `benchmark-data.tex` with corrected macro values
   - Test count: 326 → 334
   - Updated correctness percentages: Spectral now 100%, CSSR 67%
   - Updated test table in technical-report.tex

**Key Findings**:
- CSSR performance is highly sample-size dependent
- At N < 1,000: Over-splitting due to statistical fluctuation
- At N = 10,000: Matches Shalizi published benchmarks
- At N ≥ 100,000: Reliable reconstruction
- Spectral Learning consistently outperforms CSSR at all sample sizes

**Files Modified**:
- `scripts/quick_benchmark.py` — new file
- `docs/guide/cssr-deep-dive.md` — added Section 11
- `.project/research/computational-mechanics-review/technical-report/tex/generated/benchmark-data.tex`
- `.project/research/computational-mechanics-review/technical-report/tex/technical-report.tex`

**Test Results**:
- 334 tests passing
- All golden tests for CSSR pass at appropriate sample sizes

**Notes**:
- Full benchmark (experiments/benchmarks/run.py) takes 6+ hours due to BSI and large sample sizes
- Quick benchmark provides immediate feedback for algorithm validation
- Recommend using Spectral for production where speed and accuracy matter

---

### January 24, 2026

**Session Focus**: Comprehensive Tutorial Development

**Completed**:

1. **Tutorial Rewrite** — Complete overhaul of tutorial document
   - Now covers all 6 Shalizi theorems (Prescience, Minimality, Uniqueness, Min Stochasticity, Bound, Control)
   - Added Bayesian perspective with Dirichlet-Multinomial framework
   - Structured into 6 Parts: Foundations → Causal States → Theorems → Measures → Inference → Examples
   - ~800 lines of LaTeX with custom environments (keyidea, intuition, theorembox, etc.)

2. **Spell Checker Config** — Added `.vscode/settings.json` with `cSpell.words` for academic names (Crutchfield, Shalizi, Siddiqi, etc.)

**Key Content Added to Tutorial**:
- Part I: Probability refresher, information theory (H, I, conditional entropy)
- Part II: Causal equivalence, causal states, morphs, ε-machine, unifilarity
- Part III: All 6 theorems with intuitive explanations and proof sketches
- Part IV: Cμ, hμ, complexity-entropy plane visualization
- Part V: CSSR algorithm + Bayesian (BSI) with Gibbs sampling explanation
- Part VI: Worked examples (BiasedCoin, GoldenMean, EvenProcess, Periodic)

**Files Modified**:
- `.project/research/papers/tutorial/tex/main.tex` — complete rewrite
- `.vscode/settings.json` — new file

**Notes**:
- Tutorial is now ~30 pages, suitable for university seminars
- References the Bayesian primer in `.project/references/bayesian-inference-primer.md`
- Cross-references the companion review paper for formal proofs

---

### January 23, 2026

**Session Focus**: Publication Strategy & Paper Writing Infrastructure

**Completed**:

1. **Mac Devcontainer Fix** (early session)
   - Fixed missing `postStartCommand.sh` in `.devcontainer/`
   - Added Podman `runArgs` workaround for Mac compatibility
   - Tagged as v0.2.1-mac-safe

2. **Golden Tests for All Algorithms**
   - Extended `tests/golden/test_inference_golden.py` with BSI, NSD, Spectral tests
   - Spectral tests initially xfailed due to stub implementation

3. **Visualization Gallery**
   - Created `docs/gallery.md` with state machine diagrams
   - Added to MkDocs navigation

4. **Proper Spectral Learning Implementation**
   - Rewrote `src/emic/inference/spectral/algorithm.py` (+413/-170 lines)
   - Implemented Hsu, Kakade & Zhang 2012 algorithm with numpy.linalg.svd
   - Observable operators: A_x = U^T H_x V Σ^{-1}
   - State merging with 25% total variation threshold
   - All 326 tests now pass (removed 3 xfail markers)

5. **Publication Strategy**
   - Created `.project/research/papers/publication-strategy.md`
   - Defined three complementary documents:
     - **Tutorial**: "A Practical Guide to Computational Mechanics" — for university presentations
     - **Research Paper**: "Computational Mechanics: A Modern Review" — journal submission
     - **Technical Report**: "emic: A Python Framework" — thesis chapter
   - Set up directory structure with LaTeX templates
   - Created shared bibliography (20+ references)

**Created Files**:
- `.project/research/papers/publication-strategy.md` — master planning doc
- `.project/research/papers/shared/bibliography/references.bib` — shared citations
- `.project/research/papers/tutorial/tex/main.tex` — pedagogical guide template
- `.project/research/papers/review-paper/tex/main.tex` — formal paper template
- `.project/research/papers/technical-report/tex/main.tex` — thesis chapter template
- `.project/notes/spectral-learning-implementation.md` — algorithm analysis

**Test Results**:
- 326 tests passing
- pyright: 0 errors
- All algorithms validated on golden processes

**Notes**:
- The three documents form a hierarchy: Tutorial → Paper → Report
- Each references the others appropriately
- Shared assets (figures, tables, code) avoid duplication
- Existing content in `experiments/paper_verification/tex/` can be salvaged

**Next Steps**:
- Run EXP-003 to populate numerical validation tables
- Generate figures programmatically for reproducibility
- Draft Tutorial Sections 1-6 (narrative content)
- Complete proofs in Research Paper

---

### January 15, 2026 (Session 3)

**Session Focus**: Implementing All Alternative Inference Algorithms (Spec 010)

**Completed**:
- Implemented all four alternative inference algorithms from Spec 010:

1. **Spectral Learning** (`src/emic/inference/spectral/`)
   - Hankel matrix construction from sequence statistics
   - Simplified SVD via power iteration (no numpy dependency)
   - Observable operator extraction
   - Automatic rank selection via singular value threshold
   - `SpectralConfig` with max_history, rank_threshold, rank, regularization, min_count

2. **Bayesian Structural Inference (BSI)** (`src/emic/inference/bsi/`)
   - Gibbs sampling over state assignments
   - Dirichlet-multinomial likelihood
   - BIC-based model selection for number of states
   - `BSIConfig` with max_states, max_history, alpha_prior, n_samples, burnin, thin, seed

3. **Neural State Discovery (NSD)** (`src/emic/inference/nsd/`)
   - History embeddings from predictive distributions
   - K-means++ clustering with automatic k selection
   - Information-theoretic cluster scoring
   - `NSDConfig` with max_states, history_length, embedding_dim, n_iterations, convergence_threshold, seed

4. **Causal State Merging (CSM)** — completed in Session 2

- All algorithms implement `InferenceAlgorithm` protocol
- All support pipeline syntax: `sequence >> Algorithm(config)`
- All use `EpsilonMachineBuilder` to construct machines

**Updated Exports**:
- `emic.inference` now exports: CSSR, CSM, BSI, NSD, Spectral (+ configs)
- All accessible via unified interface

**Created Multivariate Study Specification**:
- Spec 015: Multivariate Inference Study
- Defines comprehensive comparison across all 5 algorithms
- 6 ground truth processes with varying parameters
- 7 sample sizes from 100 to 100,000
- Full factorial and reduced (Latin hypercube) designs
- Analysis plan with convergence curves, Pareto frontiers, sensitivity analysis
- Estimated ~15,000 experiments for reduced design

**Test Results**:
- All 226 tests passing
- pyright: 0 errors (22 warnings from generics)
- Smoke test verified all algorithms work on real data

**Algorithm Performance (Smoke Test)**:
- BSI: 1 state for biased coin ✓
- NSD: 2 states for golden mean ✓
- Spectral: 5 states for golden mean (needs tuning)

**Notes**:
- Spectral learning is a simplified implementation without numpy
- Full SVD would require adding numpy as dependency
- BSI and NSD are stochastic — results vary with seed
- All algorithms would benefit from golden tests

**Next Steps**:
- Add unit tests for Spectral, BSI, NSD
- Add golden tests for new algorithms
- Run pilot multivariate study
- Tune algorithm defaults for better performance

---

### January 15, 2026 (Session 2)

**Session Focus**: Implementing Spec 010 — CSM Algorithm

**Completed**:
- Implemented Causal State Merging (CSM) algorithm
  - Created `src/emic/inference/csm/` module
  - `CSMConfig` with history_length, merge_threshold, distance_metric, min_count, hierarchical
  - Four distance metrics: KL divergence, Hellinger, total variation, chi-squared
  - Full pipeline support via `__rrshift__` operator

- Algorithm features:
  - Bottom-up approach (vs CSSR's top-down splitting)
  - Starts with finest partition (each history = one state)
  - Iteratively merges closest pairs below threshold
  - Consistent with InferenceAlgorithm protocol

- Added comprehensive tests:
  - 18 unit tests in `test_inference_csm.py`
  - 14 golden tests in `test_inference_golden.py`
  - Tests for config validation, inference, pipeline, distance metrics
  - Cross-validation tests comparing CSM and CSSR

- Updated exports:
  - Added CSM and CSMConfig to `emic.inference.__init__.py`
  - Both algorithms now accessible via unified interface

**Test Results**:
- 226 tests passing (up from 212)
- No regressions
- pyright: 0 errors

**Notes**:
- CSM complements CSSR well — different approach, similar results
- Both find correct state counts for known processes
- Next steps: Spectral learning, then BSI

---

### January 15, 2026

**Session Focus**: Planning, specifications, and project organization

**Completed**:
- Created Spec 010: Alternative Inference Mechanisms
  - Defined BSI, Spectral, CSM, and NSD algorithms
  - Established unified interface and comparison matrix

- Created Spec 011: Experiments and Empirical Validation
  - Defined 6 experiment categories
  - Outlined paper figures

- Created Spec 012: Re-Derivation of Computational Mechanics
  - Listed 5 core theorems to derive
  - Identified novel research directions

- Created Spec 013: Experiment Ideas Catalog
  - Prioritized experiments by effort
  - Created recommended sequence

- Created Spec 014: Quantum Computational Mechanics
  - Defined quantum extension roadmap
  - Established 5-phase approach to quantum emergence

- Reorganized project management structure:
  - Moved ROADMAP.md to `.project/plan/`
  - Created `.project/record/` for JOURNAL.md
  - Created specification index (000-index.md)

- Created standards documents in `.project/standards/`:
  - coding.md — Code style, types, architecture
  - documentation.md — Docstrings, README, MkDocs
  - experimentation.md — Experiment protocol
  - governance.md — Project organization, workflow
  - specifications.md — Spec format

- Created `.github/copilot-instructions.md` for AI assistants

**Decisions**:
- Quantum emergence is the long-term target
- Will proceed piece-wise: classical → mixed states → quantum
- CSM is first alternative algorithm to implement
- Project structure now follows plan/record/standards/specifications pattern

**Notes**:
- v0.1.1 successfully released on PyPI
- v0.1.0 yanked due to README documentation link issues
- All CI workflows passing
- Full project context now documented for future AI sessions

---

### January 14, 2026

**Session Focus**: v0.1.1 release

**Completed**:
- Fixed README documentation links (pointed to correct docs URL)
- Released v0.1.1 to PyPI
- User yanked v0.1.0 from PyPI

**Notes**:
- Release workflow working correctly
- TestPyPI made optional in workflow

---

### January 13, 2026

**Session Focus**: First public release

**Completed**:
- Bumped version to 0.1.0
- Created CHANGELOG.md
- Updated pyproject.toml status to Alpha
- Configured release workflow for trusted publishing
- Made CI workflow reusable (added workflow_call)
- Tagged and released v0.1.0

**Issues Encountered**:
- CI workflow not reusable → fixed with workflow_call trigger
- README had old documentation links → led to v0.1.1

---

### January 12, 2026

**Session Focus**: Documentation infrastructure

**Completed**:
- Set up mkdocs with Material theme
- Created full documentation structure:
  - Getting started guide
  - User guide (sources, inference, analysis, pipelines)
  - API reference with mkdocstrings
  - Contributing guide
- Created docs.yml workflow for GitHub Pages
- Added docs build check to CI
- Fixed index.md Material icons issue

**Notes**:
- Documentation deployed to johnazariah.github.io/emic/
- User manually enabled GitHub Pages in repo settings

---

### January 11, 2026

**Session Focus**: README refresh and CI fixes

**Completed**:
- Fixed ruff format errors in errors.py
- Updated README with:
  - Working code examples
  - Current project status
  - Correct etymology pronunciation ("EE-mik")
  - Coverage badge

---

### January 10, 2026

**Session Focus**: CSSR algorithm fixes

**Completed**:
- Fixed empty history handling bug
- Implemented post_merge optimization for state reduction
- Fixed finite-sample state inflation in Even Process

**Tests**: 194 tests passing, 90% coverage

---

### Earlier Work

*[Pre-journal entries not recorded]*

---

## Template

```markdown
### [DATE]

**Session Focus**: [Brief description]

**Completed**:
- Item 1
- Item 2

**In Progress**:
- Item (X% complete)

**Blocked**:
- Item - reason

**Decisions**:
- Decision made and rationale

**Notes**:
- Any other relevant information
```
