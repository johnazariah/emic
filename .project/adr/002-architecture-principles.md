# ADR-002: Core Architecture Principles

## Status
**Accepted** — 2026-01-14

## Context

We need to establish the fundamental architectural principles that will guide the design of the epsilon-machine framework. The framework must be:

- Extensible for new algorithms and data sources
- Composable so users can build custom pipelines
- Maintainable with clear separation of concerns
- Testable with comprehensive automated verification

### Requirements Gathered

1. **Extensibility**: Each facet (sources, inference algorithms, analyses) must be pluggable
2. **Composability**: Pipeline stages must compose cleanly into user-defined workflows
3. **Generic Alphabets**: Support different symbol types including symbolic/exact representations
4. **Dual Audience**: Serve both researchers (who extend) and learners (who explore)

## Decision

We adopt the following core architectural principles:

### 1. Protocol-Based Extensibility

Each pipeline stage is defined by a **Protocol** (structural typing), not abstract base classes.

```python
from typing import Protocol, TypeVar, Iterator

A = TypeVar('A')  # Alphabet/Symbol type

class SequenceSource(Protocol[A]):
    """Any object that can produce a sequence of symbols."""

    def __iter__(self) -> Iterator[A]: ...

    @property
    def alphabet(self) -> frozenset[A]: ...
```

**Rationale**: Protocols allow duck typing with type checker support. Users can implement the protocol without inheriting from framework classes, enabling maximum flexibility.

### 2. Immutable Core Data Structures

All core data structures are **immutable** using frozen dataclasses or NamedTuple.

```python
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class CausalState:
    """An immutable causal state."""
    id: str
    transitions: Mapping[str, 'TransitionDistribution']
```

**Rationale**: Immutability prevents bugs from shared mutable state, makes code easier to reason about, enables safe parallelism, and aligns with functional programming principles.

### 3. Generic Alphabet Support

The framework is parameterized by alphabet type `A` throughout.

```python
@dataclass(frozen=True)
class EpsilonMachine(Generic[A]):
    """An epsilon-machine over alphabet A."""
    alphabet: frozenset[A]
    states: frozenset[CausalState[A]]
    initial_state: CausalState[A]
    # ...
```

**Rationale**: This allows the same algorithms to work with:
- `int` (binary: 0, 1)
- `str` (characters, words)
- `Symbol` (SymPy symbolic atoms)
- Custom user-defined symbol types

### 4. Composable Pipeline Architecture

Pipeline stages compose via a clean operator interface.

```
Source[A] ──▶ Inference[A] ──▶ EpsilonMachine[A] ──▶ Analysis ──▶ Output
```

```python
# User-facing API
result = (
    GoldenMeanSource(p=0.5)
    >> TakeN(10_000)
    >> CSSR(max_history=5)
    >> compute_statistical_complexity
    >> to_latex_table
)
```

**Rationale**: Composability is the key to extensibility. Researchers can swap any stage, insert custom processing, or create entirely new pipelines.

### 5. Lazy Sequence Evaluation

Sources produce `Iterator[A]` or `Iterable[A]`, supporting infinite streams and memory-efficient processing.

```python
class GoldenMeanSource:
    def __iter__(self) -> Iterator[int]:
        while True:
            yield self._next_symbol()
```

**Rationale**: Many interesting processes are infinite (stationary stochastic processes). Lazy evaluation allows working with them naturally while also supporting finite empirical data.

### 6. Explicit Error Handling

Operations that can fail raise structured exceptions from a well-defined hierarchy.

```python
def infer_machine(
    sequence: Iterable[A],
    max_history: int
) -> EpsilonMachine[A]:
    """
    Raises:
        InsufficientDataError: If sequence is too short
        NonConvergenceError: If algorithm doesn't stabilize
    """
    ...
```

**Rationale**: Python's exception system is idiomatic and well-understood. Rich exception types with `.explain()` methods provide both technical details for researchers and friendly messages for learners. See ADR-003 for details.

### 7. Separation of Pure Logic and Effects

- **Pure functions** for all computation (inference, analysis, transformation)
- **Effects** (I/O, randomness, visualization) isolated at the boundaries

```python
# Pure: computation
def compute_entropy_rate(machine: EpsilonMachine[A]) -> float: ...

# Effectful: boundary
def render_to_file(machine: EpsilonMachine[A], path: Path) -> IO[None]: ...
```

**Rationale**: Pure functions are easier to test, reason about, and compose. Effects at the boundaries keep the core clean.

## Pipeline Stage Protocols

| Stage | Protocol | Input | Output |
|-------|----------|-------|--------|
| Source | `SequenceSource[A]` | (parameters) | `Iterator[A]` |
| Transform | `SequenceTransform[A, B]` | `Iterator[A]` | `Iterator[B]` |
| Inference | `MachineInference[A]` | `Iterable[A]` | `EpsilonMachine[A]` |
| Analysis | `MachineAnalysis[A, T]` | `EpsilonMachine[A]` | `T` |
| Output | `MachineRenderer[A]` | `EpsilonMachine[A]` | `None` |

## Consequences

### Positive
- Maximum extensibility via protocols
- Safe concurrent execution due to immutability
- Flexible alphabet support for diverse applications
- Clear separation enables independent testing of components
- Pipelines are self-documenting

### Negative
- Learning curve for functional patterns (mitigated by good documentation)
- Some verbosity in type annotations (mitigated by type aliases)
- Immutability has performance cost for large structures (mitigated by structural sharing)

### Neutral
- Need comprehensive documentation of protocols for contributors
- Example implementations serve as templates for extensions

## References
- Crutchfield, J.P. "The Calculus of Emergence" (foundational theory)
- [Python Protocols (PEP 544)](https://peps.python.org/pep-0544/)
