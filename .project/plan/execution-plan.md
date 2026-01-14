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

## Phase 2: Core Types
*Target: Week 2*

### Objective
Implement the foundational type system.

### Tasks

#### 2.1 Alphabet & Symbol Types
- [ ] `Symbol` type variable
- [ ] `Alphabet` protocol
- [ ] `ConcreteAlphabet` implementation
- [ ] Unit tests

#### 2.2 Probability Types
- [ ] `ProbabilityValue` type alias
- [ ] `Distribution` immutable class
- [ ] Validation (sum to 1, range [0,1])
- [ ] `entropy()` method
- [ ] Unit tests + property tests

#### 2.3 State Types
- [ ] `StateId` type alias
- [ ] `Transition` frozen dataclass
- [ ] `CausalState` frozen dataclass
- [ ] Validation (probability sums)
- [ ] Unit tests

#### 2.4 EpsilonMachine
- [ ] `EpsilonMachine` frozen dataclass
- [ ] Unifilarity validation
- [ ] `get_state()`, `transition_matrix()`
- [ ] `EpsilonMachineBuilder`
- [ ] Unit tests + property tests

**Spec**: [002-core-types.md](specifications/002-core-types.md)

### Acceptance Criteria
- [ ] All types pass `pyright --strict`
- [ ] All types are immutable (frozen)
- [ ] >90% test coverage for types
- [ ] Property tests verify invariants
- [ ] Can construct Golden Mean machine with builder

---

## Phase 3: Sources
*Target: Week 3*

### Objective
Implement sequence sources and transforms.

### Tasks

#### 3.1 Source Protocol
- [ ] `SequenceSource` protocol
- [ ] `SeededSource` protocol
- [ ] `StochasticSource` base class
- [ ] Pipeline operator support (`>>`)

#### 3.2 Synthetic Sources
- [ ] `BiasedCoinSource` (IID)
- [ ] `GoldenMeanSource`
- [ ] `EvenProcessSource`
- [ ] `PeriodicSource`
- [ ] Each with `true_machine` property

#### 3.3 Empirical Sources
- [ ] `SequenceData` wrapper
- [ ] `from_string()` constructor
- [ ] `from_file()` constructor (basic)

#### 3.4 Transforms
- [ ] `TakeN` transform
- [ ] `SkipN` transform

**Spec**: [003-source-protocol.md](specifications/003-source-protocol.md)

### Acceptance Criteria
- [ ] All sources satisfy protocol
- [ ] Sources are reproducible with seeds
- [ ] `>>` operator works with transforms
- [ ] Synthetic sources provide `true_machine`
- [ ] Unit tests for each source

---

## Phase 4: Inference (CSSR)
*Target: Weeks 4-5*

### Objective
Implement the CSSR algorithm for epsilon-machine inference.

### Tasks

#### 4.1 Data Structures
- [ ] `SuffixTree` implementation
- [ ] `HistoryStats` class
- [ ] `StatePartition` class

#### 4.2 Statistical Tests
- [ ] Chi-squared test
- [ ] G-test (optional)
- [ ] Test utilities

#### 4.3 CSSR Algorithm
- [ ] `CSSRConfig` configuration
- [ ] `CSSR` class with `infer()` method
- [ ] Suffix tree construction
- [ ] State splitting logic
- [ ] State merging logic
- [ ] Machine construction from partition

#### 4.4 Results & Errors
- [ ] `InferenceResult` class
- [ ] `InsufficientDataError`
- [ ] `NonConvergenceError`
- [ ] Diagnostic information

**Spec**: [004-inference-protocol.md](specifications/004-inference-protocol.md)

### Acceptance Criteria
- [ ] Correctly infers Golden Mean (2 states)
- [ ] Correctly infers Even Process (2 states)
- [ ] Correctly infers Biased Coin (1 state)
- [ ] Correctly infers Period-N (N states)
- [ ] Clear error messages for insufficient data
- [ ] >85% test coverage

---

## Phase 5: Analysis
*Target: Week 6*

### Objective
Implement complexity measures and analysis functions.

### Tasks

#### 5.1 Core Measures
- [ ] `statistical_complexity()`
- [ ] `entropy_rate()`
- [ ] `excess_entropy()` (unifilar case)
- [ ] `crypticity()`

#### 5.2 Structural Measures
- [ ] `state_count()`
- [ ] `transition_count()`
- [ ] `topological_complexity()`

#### 5.3 Summary
- [ ] `AnalysisSummary` class
- [ ] `analyze()` function
- [ ] `compare_machines()` function

**Spec**: [005-analysis-protocol.md](specifications/005-analysis-protocol.md)

### Acceptance Criteria
- [ ] Measures match known values for canonical processes
- [ ] Numerical stability verified
- [ ] Unit tests with tolerance checks
- [ ] Documentation with formulas

---

## Phase 6: Output
*Target: Week 7*

### Objective
Implement visualization and export functionality.

### Tasks

#### 6.1 Visualization
- [ ] `render_state_diagram()` (Graphviz)
- [ ] `DiagramStyle` configuration
- [ ] `render_transition_heatmap()` (Matplotlib)
- [ ] `display_state_diagram()` (Jupyter)

#### 6.2 LaTeX Export
- [ ] `to_tikz()` for state diagrams
- [ ] `to_latex_table()` for analysis results

#### 6.3 Serialization
- [ ] `to_json()` / `from_json()`
- [ ] `to_dot()` (DOT format)
- [ ] `save_machine()` / `load_machine()` (pickle)

#### 6.4 Notebook Integration
- [ ] `MachineDisplay` rich display
- [ ] `display_machine()` helper

**Spec**: [006-output-protocol.md](specifications/006-output-protocol.md)

### Acceptance Criteria
- [ ] State diagrams render correctly
- [ ] LaTeX output compiles
- [ ] JSON round-trips correctly
- [ ] Jupyter display works
- [ ] Example gallery created

---

## Phase 7: Pipeline & Polish
*Target: Week 8*

### Objective
Finalize pipeline composition and polish the API.

### Tasks

#### 7.1 Pipeline
- [ ] `PipeableMixin` base
- [ ] Verify `>>` works end-to-end
- [ ] `tap()` debugging helper
- [ ] `Pipeline` builder (optional)

#### 7.2 Documentation
- [ ] API reference (docstrings)
- [ ] User guide
- [ ] Tutorial notebooks
- [ ] Example gallery

#### 7.3 Polish
- [ ] Error message review
- [ ] API consistency review
- [ ] Performance profiling
- [ ] Memory usage check

**Spec**: [007-pipeline-composition.md](specifications/007-pipeline-composition.md)

### Acceptance Criteria
- [ ] Full pipeline works as documented
- [ ] Documentation complete
- [ ] No pyright errors
- [ ] All tests pass
- [ ] Ready for v0.1.0 release

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

## Future Phases (Post v0.1.0)

### Phase 9: Educational Notebooks
- Interactive tutorials
- Visualization improvements
- Binder/Colab support

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
| 2: Core Types | 🔲 Not Started | 0% |
| 3: Sources | 🔲 Not Started | 0% |
| 4: Inference | 🔲 Not Started | 0% |
| 5: Analysis | 🔲 Not Started | 0% |
| 6: Output | 🔲 Not Started | 0% |
| 7: Pipeline | 🔲 Not Started | 0% |
| 8: Release | 🔲 Not Started | 0% |

---

## Notes

- Each phase should end with passing CI
- Commit frequently with clear messages
- Update this document as progress is made
- Flag blockers early
