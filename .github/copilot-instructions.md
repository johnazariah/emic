# Copilot Instructions

*Quick context for AI assistants working on this project.*

---

## Working Style

**Default mode: Discuss, don't code.**

- When asked a question, **discuss ideas, design options, and trade-offs first**
- Only write code when explicitly asked to implement something
- Brainstorm and explore alternatives before jumping to implementation
- Ask clarifying questions rather than making assumptions
- For complex tasks, propose a plan and get approval before coding

**When to code:**
- User says "implement", "write", "code", "fix", "add", or similar action words
- User approves a proposed design/plan
- User explicitly asks for a code sample

---

## Project Overview

**emic** is a Python library for computational mechanics — the study of structure and complexity in stochastic processes. The core task is inferring *epsilon-machines* (minimal predictive models) from symbolic time series data.

**Name**: "emic" — phonetic spelling of "εM" (epsilon-machine), pronounced "EE-mik"

**Status**: v0.5.1 on PyPI, actively developed

---

## Key Concepts

| Term | Definition |
|------|------------|
| **Epsilon-machine (εM)** | Minimal unifilar HMM that captures a process's causal structure |
| **Causal state** | Equivalence class of histories with identical predictive distributions |
| **Statistical complexity (Cμ)** | Entropy of causal state distribution — memory required for prediction |
| **Entropy rate (hμ)** | Irreducible randomness per symbol |
| **CSSR** | Causal State Splitting Reconstruction — main inference algorithm |

---

## Architecture

```
Source → Inference → Analysis → Output
  │          │           │         │
  │          │           │         └─ Visualization, export (diagram, latex, serialization)
  │          │           └─ Compute Cμ, hμ, entropy (measures, summary)
  │          └─ 5 algorithms → EpsilonMachine
  └─ Generate/load symbolic data
```

**Pipeline composition**: Components compose with `>>` operator (defined via `__rshift__` on sources/transforms).

### Source Module (`src/emic/sources/`)

- `protocol.py` — `SequenceSource` and `SeededSource` protocols
- `synthetic/` — Built-in process generators (GoldenMean, EvenProcess, BiasedCoin, Periodic)
- `empirical/` — Load data from files
- `transforms/` — `TakeN` and other sequence transforms

### Inference Module (`src/emic/inference/`)

Five algorithms, each in its own subpackage with a `Config` dataclass:

| Algorithm | Subpackage | Config |
|-----------|-----------|--------|
| CSSR | `cssr/` | `CSSRConfig(max_history, significance)` |
| CSM | `csm/` | `CSMConfig(history_length, merge_threshold)` |
| BSI | `bsi/` | `BSIConfig(...)` |
| Spectral | `spectral/` | `SpectralConfig(...)` |
| NSD | `nsd/` | `NSDConfig(...)` |

All satisfy `InferenceAlgorithm` protocol with `.infer(sequence, alphabet=None) -> InferenceResult`.

### Types Module (`src/emic/types/`)

- `machine.py` — `EpsilonMachine[A]` (frozen dataclass, generic over alphabet type `A`)
- `states.py` — `CausalState`, `StateId`, `Transition`
- `probability.py` — `Distribution`
- `alphabet.py` — Alphabet utilities

Use `EpsilonMachineBuilder[A]` to construct machines (fluent API with `.add_transition().with_start_state().build()`).

---

## Critical Files

| File | Purpose |
|------|---------|
| `src/emic/types/` | Core types: `EpsilonMachine`, `CausalState`, `StateId`, `Distribution` |
| `src/emic/inference/protocol.py` | `InferenceAlgorithm` protocol |
| `src/emic/sources/protocol.py` | `SequenceSource` and `SeededSource` protocols |
| `src/emic/analysis/` | Complexity measure computation |
| `pyproject.toml` | Dependencies, version, metadata |

---

## Development Commands

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/unit/test_types.py

# Run a single test by name
uv run pytest -k "test_cssr_finds_one_state"

# Run tests by marker (unit, integration, property, golden, slow, notebooks)
uv run pytest -m golden
uv run pytest -m "unit and not slow"

# Type check (strict mode)
uv run pyright

# Format and lint
uv run ruff format . && uv run ruff check . --fix

# Build docs locally
uv run mkdocs serve

# Run pre-commit hooks
uv run pre-commit run --all-files

# Run experiments
emic-experiment --list          # List available experiments
emic-experiment --quick         # Quick mode for development
emic-experiment --all           # Full experiment suite
```

---

## Standards (READ THESE)

Before making changes, review the relevant standards:

| Standard | When to Read |
|----------|--------------|
| [.project/standards/coding.md](.project/standards/coding.md) | Writing any code |
| [.project/standards/documentation.md](.project/standards/documentation.md) | Writing docstrings, docs |
| [.project/standards/experimentation.md](.project/standards/experimentation.md) | Running experiments |
| [.project/standards/specifications.md](.project/standards/specifications.md) | Designing features |
| [.project/standards/governance.md](.project/standards/governance.md) | Git workflow, releases |

---

## Planning Documents

| Document | Purpose |
|----------|---------|
| [.project/specifications/](.project/specifications/) | Design specifications |
| `joss/paper.md` | JOSS submission paper |

> **Note:** Research planning (ROADMAP, JOURNAL) lives in the private
> `emic-research` repo. This repo focuses on the public software.

---

## Specifications of Interest

| Spec | Topic |
|------|-------|
| 002-007 | Core design (types, protocols) |
| 010 | Alternative inference algorithms |
| 011, 013 | Experiments and validation |
| 012 | Crutchfield derivation project |
| 014 | Quantum computational mechanics roadmap |

---

## Code Patterns

### Immutable Dataclasses

All dataclasses are frozen. Use `tuple` instead of `list` for fixed collections.

```python
@dataclass(frozen=True)
class Config:
    param: int = 10
```

### Protocol-Based Extension

Extension points use `Protocol` with generics — never inherit from base classes.

```python
class Algorithm(Protocol[C]):
    config: C
    def infer(self, data: Sequence[Symbol]) -> Result: ...
```

### Generic Alphabet Type

Core types are generic over `A = TypeVar("A", bound=Hashable)` — the symbol type. Most built-in sources use `int`.

### Pipeline Composition

```python
result = source >> inference >> analysis >> output
```

---

## Testing

- Tests organized by category: `tests/unit/`, `tests/integration/`, `tests/property/`, `tests/golden/`
- Golden tests verify algorithms against known processes with analytically-known ε-machines
- Property tests with Hypothesis (profiles: `dev` default, `ci` for CI, `debug` for verbose)
- Pytest markers: `unit`, `integration`, `property`, `golden`, `slow`, `notebooks`
- Run `uv run pytest` before committing

---

## Type Checking

Pyright is configured in **strict mode** (`typeCheckingMode = "strict"`). All public APIs must have complete type annotations. Line length is 100 characters (ruff config).

---

## Current Focus

1. **JOSS submission** — `joss/paper.md` review and submission
2. **Software quality** — Tests, docs, type checking
3. **Alternative algorithms** — CSM, Spectral, BSI improvements
4. **Quantum extension** — Future direction

---

## Repository Layout

This is the **public software repo**. Research-specific content (papers,
literature reviews, notes, experiment analysis) lives in the private
`emic-research` repo.

| This repo (`emic`) | Private repo (`emic-research`) |
|---------------------|--------------------------------|
| Source code, tests | LaTeX papers, drafts |
| API docs, guides | Literature reviews, reading notes |
| JOSS paper (`joss/`) | Research experiments, hypotheses |
| ADRs, specs, standards | ROADMAP, JOURNAL, plan |
| Software experiments | References (summaries) |

---

## Tips

1. **Ask about context** if unsure — read specs and standards first
2. **Use prompts** — `commit`, `release`, `paper`, `coach`, `pick-next-work` etc.
