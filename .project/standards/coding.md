# Coding Standards

*Standards for code quality, style, and architecture in the emic project.*

---

## Language & Runtime

- **Python 3.11+** required
- **Type hints** on all public APIs
- **Immutable by default** — use `@dataclass(frozen=True)`

---

## Style

### Formatting

- **Ruff** for formatting and linting
- Line length: 88 characters (ruff default)
- Run before commit: `uv run ruff format . && uv run ruff check . --fix`

### Naming

| Element | Convention | Example |
|---------|------------|---------|
| Modules | `snake_case` | `epsilon_machine.py` |
| Classes | `PascalCase` | `EpsilonMachine` |
| Functions | `snake_case` | `infer_machine()` |
| Constants | `UPPER_SNAKE` | `DEFAULT_SIGNIFICANCE` |
| Type aliases | `PascalCase` | `Symbol`, `StateId` |
| Private | `_leading_underscore` | `_internal_helper()` |

### Imports

```python
# Standard library
from collections.abc import Sequence
from dataclasses import dataclass

# Third-party
import numpy as np

# Local
from emic.types import Symbol, EpsilonMachine
```

---

## Type System

### Required Annotations

```python
def infer(
    self,
    data: Sequence[Symbol],
    *,
    validate: bool = True,
) -> InferenceResult:
    """All parameters and return types annotated."""
    ...
```

### Generic Protocols

Use `Protocol` with generics for extensibility:

```python
class Source(Protocol[C]):
    """Protocol for data sources."""
    config: C
    def take(self, n: int) -> list[Symbol]: ...
```

### NewType for Domain Concepts

```python
from typing import NewType

StateId = NewType("StateId", str)
Symbol = NewType("Symbol", str)
```

---

## Architecture

### Immutability

- All dataclasses are `frozen=True`
- Use `tuple` instead of `list` for fixed collections
- Never mutate input arguments

### Composition over Inheritance

- Use protocols, not base classes
- Compose via `>>` pipeline operator
- Keep classes small and focused

### Configuration Pattern

```python
@dataclass(frozen=True)
class AlgorithmConfig:
    """Configuration is immutable and separate from logic."""
    param1: int = 10
    param2: float = 0.05

class Algorithm:
    def __init__(self, config: AlgorithmConfig):
        self.config = config
```

---

## Documentation

### Docstrings

- **Google style** docstrings
- Required on all public functions, classes, methods
- Include `Args`, `Returns`, `Raises`, `Example` sections

```python
def analyze(machine: EpsilonMachine) -> AnalysisSummary:
    """Compute complexity measures for an epsilon-machine.

    Args:
        machine: The epsilon-machine to analyze.

    Returns:
        Summary containing statistical complexity, entropy rate,
        and other measures.

    Raises:
        InvalidMachineError: If machine has no states.

    Example:
        >>> summary = analyze(machine)
        >>> print(f"Cμ = {summary.statistical_complexity:.3f}")
    """
```

### Module Docstrings

Every module has a docstring explaining its purpose:

```python
"""Inference algorithms for epsilon-machine reconstruction.

This module provides implementations of various algorithms for
inferring epsilon-machines from symbolic time series data.
"""
```

---

## Testing

### Structure

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Cross-module tests
├── property/       # Hypothesis property tests
├── golden/         # Known-answer tests
└── notebooks/      # Notebook execution tests
```

### Naming

- Test files: `test_<module>.py`
- Test functions: `test_<behavior>_<condition>()`
- Fixtures in `conftest.py`

### Coverage

- Minimum 85% line coverage
- 100% coverage on public API
- Property tests for core algorithms

---

## Error Handling

### Custom Exceptions

```python
class EmicError(Exception):
    """Base exception for emic package."""

class InferenceError(EmicError):
    """Error during machine inference."""

class InvalidMachineError(EmicError):
    """Machine violates structural constraints."""
```

### Validation

- Validate inputs at public API boundaries
- Fail fast with descriptive messages
- Use `assert` only for internal invariants

---

## Performance

### Guidelines

- Profile before optimizing
- Document complexity in docstrings
- Use generators for large sequences
- Consider `numpy` for numerical work

### Caching

```python
from functools import cached_property

@cached_property
def stationary_distribution(self) -> dict[StateId, float]:
    """Compute once, cache result."""
    return self._compute_stationary()
```

---

## Git Practices

### Commits

- Atomic commits (one logical change)
- Present tense: "Add feature" not "Added feature"
- Reference issues: "Fix #123: Handle empty input"

### Branches

- `main` — always deployable
- `feature/<name>` — new features
- `fix/<name>` — bug fixes

---

## Pre-commit Checks

All commits must pass:

```yaml
- ruff format (formatting)
- ruff check (linting)
- pyright (type checking)
- pytest (tests)
- check_docstrings.py (documentation)
```
