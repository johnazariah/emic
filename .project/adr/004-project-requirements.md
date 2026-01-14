# ADR-004: Project Requirements Summary

## Status
**Living Document** — 2026-01-14

## Purpose

This document captures the requirements gathered during project planning discussions. It serves as a reference for all architectural and design decisions.

---

## Project Vision

Build an **open-source experimental framework** for constructing and analyzing epsilon-machines based on Crutchfield's computational mechanics. The framework should:

1. Allow users to **derive structure and characteristics** of epsilon-machines from different kinds of sequences
2. Provide **clear understanding** of how epsilon-machines are constructed and characterized
3. Be **educational** and accessible to diverse audiences
4. Be **research-grade** and extensible for novel investigations

---

## Target Audience

### Primary: Researchers
- Want to **tweak and extend** the framework
- Need to **compose custom pipelines** for novel experiments
- Require access to intermediate results and algorithm internals
- Value correctness, reproducibility, and performance

### Secondary: Curious Learners
- Students and curious minds exploring computational mechanics
- Want to understand **emergence as a property of computational sophistication of the viewer**
- Need clear explanations, visualizations, and guided notebooks
- Value intuition-building over mathematical rigor

---

## Functional Requirements

### FR-1: Sequence Sources
- [ ] Support multiple built-in sequence generators (Golden Mean, Even Process, etc.)
- [ ] Support empirical/user-provided sequences
- [ ] Sources must be **pluggable** via a common interface
- [ ] Support **different alphabet types** (binary, symbolic, custom)
- [ ] Support **lazy/infinite sequences** for stochastic processes

### FR-2: Inference Algorithms
- [ ] Implement CSSR (Causal State Splitting Reconstruction) as primary algorithm
- [ ] Design for **extensibility** to add future algorithms (Bayesian, spectral, etc.)
- [ ] Each algorithm is a **pluggable component** in the pipeline
- [ ] Algorithms work with generic alphabet types

### FR-3: Epsilon-Machine Representation
- [ ] Immutable, well-typed representation of epsilon-machines
- [ ] Support for transition probabilities and state distributions
- [ ] Serialization/deserialization (JSON, pickle)
- [ ] Export to standard formats (e.g., DOT for Graphviz)

### FR-4: Analysis & Characterization
- [ ] Statistical Complexity (C_μ)
- [ ] Entropy Rate (h_μ)
- [ ] Excess Entropy (E)
- [ ] Crypticity and related measures
- [ ] Extensible for new measures

### FR-5: Visualization & Output
- [ ] State diagram visualization (Graphviz/Matplotlib)
- [ ] Transition matrix heatmaps
- [ ] Complexity vs. history length curves
- [ ] **LaTeX export** for publication-ready figures and tables

### FR-6: Pipeline Composition
- [ ] Stages **compose** into user-defined pipelines
- [ ] Clean operator syntax (e.g., `source >> transform >> infer >> analyze`)
- [ ] Each stage follows a defined protocol

### FR-7: Educational Notebooks
- [ ] Step-by-step epsilon-machine construction
- [ ] Comparison of canonical processes
- [ ] Interactive parameter exploration
- [ ] Publishable on GitHub

---

## Non-Functional Requirements

### NFR-1: Code Quality
- **Functional style**: Pure functions, immutable data, explicit effects
- **Typed**: Full type annotations, strict type checking (pyright)
- **Tested**: Comprehensive test suite with property-based testing
- **Documented**: Docstrings, API reference, user guide

### NFR-2: Extensibility
- Protocol-based design (structural typing)
- Clear extension points at each pipeline stage
- Examples of custom implementations

### NFR-3: Reproducibility
- Deterministic results with seeded randomness
- Version-pinned dependencies
- Devcontainer for consistent environment

### NFR-4: Accessibility
- Python as primary language (familiar to target audience)
- Jupyter notebook support
- Clear error messages with educational context

---

## Technical Requirements

### TR-1: Development Environment
- [ ] **Devcontainer** with Python 3.11+ and LaTeX (TeX Live)
- [ ] Package manager: `uv` (modern, fast)
- [ ] Type checker: `pyright` in strict mode
- [ ] Linter/formatter: `ruff`
- [ ] Testing: `pytest` with `hypothesis` for property-based tests
- [ ] Jupyter kernel linked to project environment

### TR-2: Dependencies (Preliminary)
- `numpy`: Numerical computation
- `networkx`: Graph representation
- `sympy`: Symbolic computation (optional/extension)
- `matplotlib`: Visualization
- `graphviz`: State diagram rendering
- `hypothesis`: Property-based testing

### TR-3: Project Structure
```
epsilon-machines/
├── .devcontainer/          # Development container
├── .project/
│   ├── adr/                # Architecture Decision Records
│   ├── specifications/     # Feature specifications
│   ├── plan/               # Execution tracking
│   └── references/         # Papers and resources
├── src/
│   └── emic/               # Main package
│       ├── sources/        # Sequence generators
│       ├── inference/      # CSSR and future algorithms
│       ├── machines/       # EpsilonMachine representation
│       ├── analysis/       # Complexity measures
│       ├── output/         # Visualization, LaTeX
│       └── pipeline/       # Composition utilities
├── tests/                  # Test suite
├── notebooks/              # Educational Jupyter notebooks
├── papers/                 # LaTeX documents
└── docs/                   # Documentation
```

---

## Open Questions

1. ~~**Package Name**: What should the package be called?~~ → **Decided: `emic`** (see ADR-005)

2. **Symbolic Computation Priority**: Should SymPy-based alphabets be in v1 or a later extension?

3. **ADR-003 Open Questions**: See error handling ADR for pending decisions

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | Initial requirements capture | — |
