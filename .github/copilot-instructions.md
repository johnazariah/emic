# Copilot Instructions

*Quick context for AI assistants working on this project.*

---

## Project Overview

**emic** is a Python library for computational mechanics — the study of structure and complexity in stochastic processes. The core task is inferring *epsilon-machines* (minimal predictive models) from symbolic time series data.

**Name**: "emic" — phonetic spelling of "εM" (epsilon-machine), pronounced "EE-mik"

**Status**: v0.1.1 on PyPI, actively developed

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
  │          │           │         └─ Visualization, export
  │          │           └─ Compute Cμ, hμ, entropy
  │          └─ CSSR algorithm → EpsilonMachine
  └─ Generate/load symbolic data
```

**Pipeline composition**: Components compose with `>>` operator.

---

## Critical Files

| File | Purpose |
|------|---------|
| `src/emic/types.py` | Core types: `Symbol`, `StateId`, `EpsilonMachine` |
| `src/emic/inference/cssr.py` | CSSR algorithm implementation |
| `src/emic/analysis/` | Complexity measure computation |
| `pyproject.toml` | Dependencies, version, metadata |

---

## Development Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Type check
uv run pyright

# Format and lint
uv run ruff format . && uv run ruff check . --fix

# Build docs locally
uv run mkdocs serve

# Run pre-commit hooks
uv run pre-commit run --all-files
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
| [.project/plan/ROADMAP.md](.project/plan/ROADMAP.md) | Current milestones and next actions |
| [.project/record/JOURNAL.md](.project/record/JOURNAL.md) | Chronological work history |
| [.project/specifications/](.project/specifications/) | Design specifications |

**Always check the ROADMAP** to understand current priorities.

**Always update the JOURNAL** after completing work.

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

```python
@dataclass(frozen=True)
class Config:
    param: int = 10
```

### Protocol-Based Extension

```python
class Algorithm(Protocol[C]):
    config: C
    def infer(self, data: Sequence[Symbol]) -> Result: ...
```

### Pipeline Composition

```python
result = source >> inference >> analysis >> output
```

---

## Testing

- 194 tests, 90% coverage
- Golden tests in `tests/golden/` for known processes
- Property tests with Hypothesis
- Run `uv run pytest` before committing

---

## Current Focus

Check `.project/plan/ROADMAP.md` for current priorities, but likely:

1. **Experiments** — Convergence analysis, parameter sensitivity
2. **Alternative algorithms** — CSM, Spectral, BSI
3. **Research paper** — Figures, writing
4. **Quantum extension** — Future direction

---

## Tips

1. **Ask about context** if unsure — read specs and standards first
2. **Use immutable types** — frozen dataclasses, tuples
3. **Write tests** — especially golden tests for new processes
4. **Update documentation** — docstrings required on all public APIs
5. **Update journal** — record what was done each session
6. **Check CI** — all commits must pass formatting, types, tests
