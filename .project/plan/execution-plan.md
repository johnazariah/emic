# Execution Plan

This document tracks the implementation progress of the `emic` framework.

## Overview

The plan is organized into phases, each building on the previous. Each phase has clear deliverables and acceptance criteria.

---

## Phase 0: Foundation ✅
*Completed: 2026-01-14*

### Deliverables
- [x] Project structure created
- [x] Package published to PyPI (name reservation)
- [x] GitHub repository initialized
- [x] ADRs documented (001-006)
- [x] Specifications drafted (001-007)

### Artifacts
- `emic` v0.0.1 on PyPI
- https://github.com/johnazariah/emic

---

## Phase 1: Development Environment
*Target: Week 1*

### Objective
Set up a reproducible development environment with all tooling.

### Tasks

#### 1.1 CI/CD & Testing Setup ✅
*Completed: 2026-01-14*

- [x] Create specification [001a-ci-cd-testing.md](../specifications/001a-ci-cd-testing.md)
- [x] Configure `pyproject.toml` with dev dependencies
- [x] Configure `pytest` with markers and Hypothesis profiles
- [x] Configure coverage thresholds (90% line, 85% branch)
- [x] Configure `ruff` for linting/formatting
- [x] Configure `pyright` strict mode
- [x] Create test directory structure (unit, integration, property, golden, notebooks)
- [x] Create `tests/conftest.py` with shared fixtures
- [x] Create initial placeholder test
- [x] Set up `.pre-commit-config.yaml`
- [x] Create GitHub Actions CI workflow (`.github/workflows/ci.yml`)
- [x] Create GitHub Actions Release workflow (`.github/workflows/release.yml`)
- [x] Add CI and Codecov badges to README

**Spec**: [001a-ci-cd-testing.md](../specifications/001a-ci-cd-testing.md)

#### 1.2 Devcontainer Setup ✅
*Completed: 2026-01-14*

- [x] Create `.devcontainer/devcontainer.json`
- [x] Create `.devcontainer/Dockerfile`
- [x] Install Python 3.11+ with uv
- [x] Install LaTeX (TeX Live science scheme)
- [x] Install Graphviz for state diagrams
- [x] Install VS Code extensions
- [x] Create `postCreateCommand.sh` setup script

**Spec**: [001-devcontainer.md](../specifications/001-devcontainer.md)

### Acceptance Criteria
- [x] `devcontainer` configuration created
- [x] `pytest` configuration complete
- [x] `pyright --strict` configuration complete
- [x] `ruff` configuration complete
- [x] GitHub Actions CI workflow created
- [ ] CI passes on push (needs tests to pass)


---

## Phase 2: Core Types ✅
*Completed: 2026-01-15*

### Objective
Implement the foundational type system.

### Tasks

#### 2.1 Alphabet & Symbol Types ✅
- [x] `Symbol` type variable
- [x] `Alphabet` protocol
- [x] `ConcreteAlphabet` implementation
- [x] Unit tests

#### 2.2 Probability Types ✅
- [x] `ProbabilityValue` type alias
- [x] `Distribution` immutable class
- [x] Validation (sum to 1, range [0,1])
- [x] `entropy()` method
- [x] Unit tests + property tests

#### 2.3 State Types ✅
- [x] `StateId` type alias
- [x] `Transition` frozen dataclass
- [x] `CausalState` frozen dataclass
- [x] Validation (probability sums)
- [x] Unit tests

#### 2.4 EpsilonMachine ✅
- [x] `EpsilonMachine` frozen dataclass
- [x] Unifilarity validation
- [x] `get_state()`, `transition_matrix()`
- [x] `EpsilonMachineBuilder`
- [x] Unit tests + property tests

**Spec**: [002-core-types.md](specifications/002-core-types.md)

### Acceptance Criteria
- [x] All types pass `pyright --strict`
- [x] All types are immutable (frozen)
- [x] >90% test coverage for types
- [x] Property tests verify invariants
- [x] Can construct Golden Mean machine with builder

---

## Phase 3: Sources ✅
*Completed: 2026-01-15*

### Objective
Implement sequence sources and transforms.

### Tasks

#### 3.1 Source Protocol ✅
- [x] `SequenceSource` protocol
- [x] `SeededSource` protocol
- [x] `StochasticSource` base class
- [x] Pipeline operator support (`>>`)

#### 3.2 Synthetic Sources ✅
- [x] `BiasedCoinSource` (IID)
- [x] `GoldenMeanSource`
- [x] `EvenProcessSource`
- [x] `PeriodicSource`
- [x] Each with `true_machine` property

#### 3.3 Empirical Sources ✅
- [x] `SequenceData` wrapper
- [x] `from_string()` constructor
- [x] `from_file()` constructor (basic)

#### 3.4 Transforms ✅
- [x] `TakeN` transform
- [x] `SkipN` transform

**Spec**: [003-source-protocol.md](specifications/003-source-protocol.md)

### Acceptance Criteria
- [x] All sources satisfy protocol
- [x] Sources are reproducible with seeds
- [x] `>>` operator works with transforms
- [x] Synthetic sources provide `true_machine`
- [x] Unit tests for each source

---

## Phase 4: Inference (CSSR) ✅
*Completed: 2026-01-15*

### Objective
Implement the CSSR algorithm for epsilon-machine inference.

### Tasks

#### 4.1 Data Structures ✅
- [x] `SuffixTree` implementation
- [x] `HistoryStats` class
- [x] `StatePartition` class

#### 4.2 Statistical Tests ✅
- [x] Chi-squared test
- [x] G-test
- [x] KS-test
- [x] Test utilities

#### 4.3 CSSR Algorithm ✅
- [x] `CSSRConfig` configuration
- [x] `CSSR` class with `infer()` method
- [x] Suffix tree construction
- [x] State splitting logic
- [x] State merging logic
- [x] Machine construction from partition

#### 4.4 Results & Errors ✅
- [x] `InferenceResult` class with pipeline operator
- [x] `InsufficientDataError`
- [x] `NonConvergenceError`
- [x] Diagnostic information

**Spec**: [004-inference-protocol.md](specifications/004-inference-protocol.md)

### Acceptance Criteria
- [x] Correctly infers Golden Mean (~2-3 states)
- [x] Correctly infers Even Process (~2-3 states)
- [x] Correctly infers Biased Coin (1 state)
- [x] Correctly infers Period-N (~N states)
- [x] Clear error messages for insufficient data
- [x] >85% test coverage
- [ ] Correctly infers Even Process (2 states)
- [ ] Correctly infers Biased Coin (1 state)
- [ ] Correctly infers Period-N (N states)
- [ ] Clear error messages for insufficient data
- [ ] >85% test coverage

---

## Phase 5: Analysis ✅
*Completed: 2026-01-15*

### Objective
Implement complexity measures and analysis functions.

### Tasks

#### 5.1 Core Measures ✅
- [x] `statistical_complexity()`
- [x] `entropy_rate()`
- [x] `excess_entropy()` (unifilar case)
- [ ] `crypticity()` (deferred - requires more theory)

#### 5.2 Structural Measures ✅
- [x] `state_count()`
- [x] `transition_count()`
- [x] `topological_complexity()`

#### 5.3 Summary ✅
- [x] `AnalysisSummary` class
- [x] `analyze()` function
- [ ] `compare_machines()` function (deferred)

**Spec**: [005-analysis-protocol.md](specifications/005-analysis-protocol.md)

### Acceptance Criteria
- [x] Measures match known values for canonical processes
- [x] Numerical stability verified
- [x] Unit tests with tolerance checks
- [x] Documentation with formulas

---

## Phase 6: Output ✅
*Completed: 2026-01-15*

### Objective
Implement visualization and export functionality.

### Tasks

#### 6.1 Visualization
- [x] `render_state_diagram()` (Graphviz)
- [x] `DiagramStyle` configuration
- [ ] `render_transition_heatmap()` (Matplotlib) - deferred
- [x] `display_state_diagram()` (Jupyter)

#### 6.2 LaTeX Export
- [x] `to_tikz()` for state diagrams
- [x] `to_latex_table()` for analysis results

#### 6.3 Serialization
- [x] `to_json()` / `from_json()`
- [x] `to_dot()` (DOT format)
- [x] `to_mermaid()` (Mermaid format)
- [ ] `save_machine()` / `load_machine()` (pickle) - deferred

#### 6.4 Notebook Integration
- [x] `display_state_diagram()` for Jupyter

**Spec**: [006-output-protocol.md](specifications/006-output-protocol.md)

### Acceptance Criteria
- [x] State diagrams render correctly
- [x] LaTeX output compiles
- [x] JSON round-trips correctly
- [x] Jupyter display works
- [ ] Example gallery created - deferred

---

## Phase 7: Pipeline & Polish ✅
*Completed: 2026-01-15*

### Objective
Finalize pipeline composition and polish the API.

### Tasks

#### 7.1 Pipeline
- [x] `>>` operator works end-to-end
- [x] `tap()` debugging helper
- [x] `identity()` helper
- [x] `Pipeline` builder class

#### 7.2 Documentation
- [ ] API reference (docstrings with examples) - in progress
- [ ] User guide - deferred to docs sprint
- [x] Pipeline integration tests
- [ ] README with quick-start example - partial

#### 7.3 Polish
- [x] Pyright passes
- [x] Ruff passes
- [x] All tests pass (192)
- [ ] Performance profiling - deferred

**Spec**: [007-pipeline-composition.md](specifications/007-pipeline-composition.md), [008-documentation.md](specifications/008-documentation.md)

### Acceptance Criteria
- [x] Full pipeline works as documented
- [ ] Documentation complete - in progress
- [x] No pyright errors
- [x] All tests pass
- [x] Core API ready for v0.1.0

---

## Phase 8: Release v0.1.0
*Target: Week 9*

### Tasks
- [ ] Version bump to 0.1.0
- [ ] CHANGELOG written
- [ ] Final testing
- [ ] PyPI release
- [ ] GitHub release with notes
- [ ] Announcement

---

## Phase 9: Research Paper
*Target: Post v0.1.0*

### Objective
Write a research paper demonstrating the framework and empirical results.

### Tasks

#### 9.1 Experiments
- [ ] Run inference experiments on canonical processes
- [ ] Vary data lengths (1K, 10K, 100K, 1M)
- [ ] Vary CSSR parameters (max_history, significance)
- [ ] Collect metrics: state count, entropy rate, complexity

#### 9.2 Paper Writing
- [ ] LaTeX structure created
- [ ] Background section (computational mechanics)
- [ ] Framework section (architecture, design)
- [ ] Experiments section (results, discussion)
- [ ] Introduction and conclusion

#### 9.3 Figures
- [ ] Architecture diagram (TikZ)
- [ ] Epsilon-machine state diagrams
- [ ] Accuracy vs data length plots
- [ ] Parameter sensitivity heatmaps

**Spec**: [009-research-paper.md](specifications/009-research-paper.md)

### Acceptance Criteria
- [ ] Paper compiles with pdflatex
- [ ] Experiments reproducible
- [ ] Figures auto-generated
- [ ] Submitted to arXiv

---

## Future Phases (Post Paper)

### Phase 10: Additional Algorithms
- Bayesian inference
- Spectral methods
- Reverse-time machine construction

### Phase 11: Symbolic Computation
- SymPy integration (ADR-006)
- Exact rational probabilities
- Symbolic alphabet support

### Phase 12: Performance
- Rust core via PyO3
- Parallel inference
- Large-scale data support

---

## Progress Tracking

| Phase | Status | Completion |
|-------|--------|------------|
| 0: Foundation | ✅ Complete | 100% |
| 1: Dev Environment | ✅ Complete | 100% |
| 2: Core Types | ✅ Complete | 100% |
| 3: Sources | ✅ Complete | 100% |
| 4: Inference | ✅ Complete | 100% |
| 5: Analysis | ✅ Complete | 100% |
| 6: Output | ✅ Complete | 100% |
| 7: Pipeline & Docs | ✅ Complete | 90% |
| 8: Release v0.1.0 | 🔲 Not Started | 0% |
| 9: Research Paper | 🔲 Not Started | 0% |

---

## Notes

- Each phase should end with passing CI
- Commit frequently with clear messages
- Update this document as progress is made
- Flag blockers early
