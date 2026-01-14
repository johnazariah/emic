# Specification 003: Source Protocol

## Status
📋 Draft

## Overview

This specification defines the **Source Protocol** — the interface for sequence generators that produce symbol streams for epsilon-machine inference.

Sources are the entry point of any `emic` pipeline. They can be:
- **Synthetic**: Known stochastic processes with analytical solutions
- **Empirical**: Real-world data loaded from files or streams
- **Custom**: User-defined generators

## Design Principles

- **Protocol-based**: Any iterable over symbols can be a source (ADR-002)
- **Lazy**: Sources yield symbols on demand, supporting infinite streams
- **Generic**: Parameterized by alphabet type `A`
- **Composable**: Sources can be transformed and combined

---

## 1. Core Protocol

### `SequenceSource[A]` (Protocol)

```python
from typing import Protocol, TypeVar, Iterator, Hashable

A = TypeVar('A', bound=Hashable)

class SequenceSource(Protocol[A]):
    """
    A source of symbols for epsilon-machine inference.
    
    Any object that is iterable over symbols and knows its alphabet
    satisfies this protocol.
    """
    
    def __iter__(self) -> Iterator[A]:
        """Yield symbols from the source."""
        ...
    
    @property
    def alphabet(self) -> frozenset[A]:
        """The set of possible symbols."""
        ...
```

### `SeededSource[A]` (Extended Protocol)

```python
class SeededSource(SequenceSource[A], Protocol[A]):
    """A source that can be seeded for reproducibility."""
    
    @property
    def seed(self) -> int | None:
        """The random seed, if set."""
        ...
    
    def with_seed(self, seed: int) -> 'SeededSource[A]':
        """Return a new source with the given seed."""
        ...
```

---

## 2. Base Implementation

### `StochasticSource[A]` (Abstract Base)

```python
from dataclasses import dataclass
from typing import Iterator
import random

@dataclass
class StochasticSource(Generic[A]):
    """
    Base class for stochastic process sources.
    
    Handles random state management and provides common functionality.
    Not frozen because it maintains RNG state.
    """
    
    _alphabet: frozenset[A]
    _seed: int | None = None
    _rng: random.Random = field(default_factory=random.Random, repr=False)
    
    def __post_init__(self) -> None:
        if self._seed is not None:
            self._rng.seed(self._seed)
    
    @property
    def alphabet(self) -> frozenset[A]:
        return self._alphabet
    
    @property
    def seed(self) -> int | None:
        return self._seed
    
    def with_seed(self, seed: int) -> 'StochasticSource[A]':
        """Return a new source with the given seed."""
        # Subclasses should override to return correct type
        raise NotImplementedError()
    
    def __iter__(self) -> Iterator[A]:
        """Subclasses must implement."""
        raise NotImplementedError()
```

---

## 3. Built-in Synthetic Sources

### 3.1 Golden Mean Process

The **Golden Mean Process** is a classic example: no consecutive 1s allowed.

```
States: A, B
Alphabet: {0, 1}

Transitions:
  A --0 (p)--> A
  A --1 (1-p)--> B
  B --0 (1.0)--> A

Constraint: After emitting 1, must emit 0.
```

```python
@dataclass
class GoldenMeanSource(StochasticSource[int]):
    """
    The Golden Mean Process.
    
    A binary process where consecutive 1s are forbidden.
    After emitting a 1, the next symbol must be 0.
    
    Parameters:
        p: Probability of emitting 0 from state A (default: 0.5)
        seed: Random seed for reproducibility
    
    Statistical properties:
        - Entropy rate: h = -p*log(p) - (1-p)*log(1-p) for state A
        - Statistical complexity: C_μ = H(π) where π = (2/3, 1/3) for p=0.5
    """
    
    p: float = 0.5
    
    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, '_alphabet', frozenset({0, 1}))
        if not (0 < self.p < 1):
            raise ValueError(f"p must be in (0, 1), got {self.p}")
    
    def __iter__(self) -> Iterator[int]:
        state = 'A'
        while True:
            if state == 'A':
                if self._rng.random() < self.p:
                    yield 0
                    state = 'A'
                else:
                    yield 1
                    state = 'B'
            else:  # state == 'B'
                yield 0
                state = 'A'
    
    def with_seed(self, seed: int) -> 'GoldenMeanSource':
        return GoldenMeanSource(p=self.p, _seed=seed)
    
    @property
    def true_machine(self) -> 'EpsilonMachine[int]':
        """Return the known epsilon-machine for this process."""
        from emic.types import EpsilonMachineBuilder
        return (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", self.p)
            .add_transition("A", 1, "B", 1 - self.p)
            .add_transition("B", 0, "A", 1.0)
            .with_start_state("A")
            .with_stationary_distribution({"A": 2/3, "B": 1/3})
            .build()
        )
```

### 3.2 Even Process

The **Even Process**: 1s must come in pairs (even runs).

```
States: A, B
Alphabet: {0, 1}

Transitions:
  A --0 (p)--> A
  A --1 (1-p)--> B
  B --1 (1.0)--> A

Constraint: Once a 1 is started, must emit another 1.
```

```python
@dataclass
class EvenProcessSource(StochasticSource[int]):
    """
    The Even Process.
    
    A binary process where 1s must appear in runs of even length.
    After emitting a 1, must emit another 1 before any 0.
    
    Parameters:
        p: Probability of emitting 0 from state A (default: 0.5)
        seed: Random seed for reproducibility
    """
    
    p: float = 0.5
    
    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, '_alphabet', frozenset({0, 1}))
        if not (0 < self.p < 1):
            raise ValueError(f"p must be in (0, 1), got {self.p}")
    
    def __iter__(self) -> Iterator[int]:
        state = 'A'
        while True:
            if state == 'A':
                if self._rng.random() < self.p:
                    yield 0
                    state = 'A'
                else:
                    yield 1
                    state = 'B'
            else:  # state == 'B'
                yield 1
                state = 'A'
    
    def with_seed(self, seed: int) -> 'EvenProcessSource':
        return EvenProcessSource(p=self.p, _seed=seed)
```

### 3.3 Biased Coin (IID)

```python
@dataclass
class BiasedCoinSource(StochasticSource[int]):
    """
    Independent identically distributed binary source.
    
    The simplest stochastic process: each symbol is independent.
    The ε-machine has exactly one state.
    
    Parameters:
        p: Probability of emitting 1 (default: 0.5)
    """
    
    p: float = 0.5
    
    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, '_alphabet', frozenset({0, 1}))
    
    def __iter__(self) -> Iterator[int]:
        while True:
            yield 1 if self._rng.random() < self.p else 0
    
    @property
    def true_machine(self) -> 'EpsilonMachine[int]':
        from emic.types import EpsilonMachineBuilder
        return (
            EpsilonMachineBuilder[int]()
            .add_transition("A", 0, "A", 1 - self.p)
            .add_transition("A", 1, "A", self.p)
            .with_start_state("A")
            .with_stationary_distribution({"A": 1.0})
            .build()
        )
```

### 3.4 Period-N Process

```python
@dataclass
class PeriodicSource(StochasticSource[int]):
    """
    A deterministic periodic process.
    
    Repeats a fixed pattern indefinitely.
    The ε-machine has N states (one per position in pattern).
    
    Parameters:
        pattern: The repeating sequence of symbols
    """
    
    pattern: tuple[int, ...]
    
    def __post_init__(self) -> None:
        super().__post_init__()
        if len(self.pattern) == 0:
            raise ValueError("Pattern must be non-empty")
        object.__setattr__(self, '_alphabet', frozenset(self.pattern))
    
    def __iter__(self) -> Iterator[int]:
        i = 0
        while True:
            yield self.pattern[i]
            i = (i + 1) % len(self.pattern)
```

### 3.5 Simple Nonunifilar Source (SNS)

A source that produces a process that is **not unifilar** — demonstrating a case where the forward-time ε-machine differs from reverse-time.

```python
@dataclass  
class SimpleNonunifilarSource(StochasticSource[int]):
    """
    Simple Nonunifilar Source.
    
    A process where the ε-machine requires looking at more history
    than a naive Markov model would suggest.
    
    This is useful for testing inference algorithms.
    """
    
    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, '_alphabet', frozenset({0, 1}))
    
    def __iter__(self) -> Iterator[int]:
        # Implementation depends on specific SNS variant
        raise NotImplementedError("TODO: Implement specific SNS")
```

---

## 4. Empirical Sources

### `SequenceData[A]` (Finite Sequence)

```python
@dataclass(frozen=True)
class SequenceData(Generic[A]):
    """
    A finite sequence of observed symbols.
    
    Wraps empirical data for use in inference pipelines.
    """
    
    symbols: tuple[A, ...]
    _alphabet: frozenset[A] | None = None
    
    def __iter__(self) -> Iterator[A]:
        return iter(self.symbols)
    
    def __len__(self) -> int:
        return len(self.symbols)
    
    @property
    def alphabet(self) -> frozenset[A]:
        if self._alphabet is not None:
            return self._alphabet
        return frozenset(self.symbols)
    
    @classmethod
    def from_string(cls, s: str) -> 'SequenceData[str]':
        """Create from a string (each character is a symbol)."""
        return cls(tuple(s))
    
    @classmethod
    def from_file(cls, path: str, alphabet: frozenset[A] | None = None) -> 'SequenceData[A]':
        """Load sequence from a file."""
        # TODO: Support various file formats
        raise NotImplementedError()
```

---

## 5. Source Transforms

Transforms take sources and produce new sources.

### `TakeN[A]`

```python
@dataclass(frozen=True)
class TakeN(Generic[A]):
    """
    Take the first N symbols from a source.
    
    Converts an infinite source into a finite sequence.
    """
    
    n: int
    
    def __call__(self, source: SequenceSource[A]) -> SequenceData[A]:
        from itertools import islice
        symbols = tuple(islice(source, self.n))
        return SequenceData(symbols, _alphabet=source.alphabet)
```

### `SkipN[A]`

```python
@dataclass(frozen=True)
class SkipN(Generic[A]):
    """
    Skip the first N symbols (burn-in period).
    
    Useful for allowing a process to reach stationarity.
    """
    
    n: int
    
    def __call__(self, source: SequenceSource[A]) -> Iterator[A]:
        it = iter(source)
        for _ in range(self.n):
            next(it)
        yield from it
```

---

## 6. Pipeline Integration

Sources work with the `>>` pipeline operator:

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR

# Pipeline: source >> transform >> inference
machine = (
    GoldenMeanSource(p=0.5, seed=42)
    >> TakeN(10_000)
    >> CSSR(max_history=5)
)
```

The `>>` operator is implemented via `__rshift__`:

```python
def __rshift__(self, other: Callable[[SequenceSource[A]], T]) -> T:
    return other(self)
```

---

## 7. Module Structure

```
emic/sources/
├── __init__.py           # Re-exports
├── protocol.py           # SequenceSource protocol
├── base.py               # StochasticSource base class
├── synthetic/
│   ├── __init__.py
│   ├── golden_mean.py
│   ├── even_process.py
│   ├── biased_coin.py
│   ├── periodic.py
│   └── sns.py
├── empirical/
│   ├── __init__.py
│   ├── sequence_data.py
│   └── loaders.py
└── transforms/
    ├── __init__.py
    ├── take.py
    └── skip.py
```

---

## Acceptance Criteria

- [ ] `SequenceSource` protocol defined and documented
- [ ] All synthetic sources implement the protocol
- [ ] Sources are reproducible with seeds
- [ ] `TakeN` and `SkipN` transforms work
- [ ] Pipeline operator `>>` implemented
- [ ] Unit tests for each source
- [ ] Property tests: outputs respect alphabet
- [ ] Each synthetic source provides `true_machine` for validation

## Dependencies

- Python 3.11+
- `random` (standard library)

## Related Specifications

- Spec 002: Core Types (EpsilonMachine used in `true_machine`)
- Spec 004: Inference Protocol (consumes sources)
