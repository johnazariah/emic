# Specification 002: Core Type System

## Status
📋 Draft

## Overview

This specification defines the foundational data types for the `emic` framework. These types represent epsilon-machines and their components, forming the core that all other modules build upon.

## Design Principles

From our ADRs:
- **Immutable**: All core types are frozen dataclasses (ADR-002)
- **Generic**: Parameterized by alphabet type `A` (ADR-006)
- **Protocol-based**: Structural typing for extensibility (ADR-002)
- **Hashable**: Core types can be used in sets and as dict keys

## Type Hierarchy

```
emic/
├── types/
│   ├── __init__.py          # Re-exports all public types
│   ├── alphabet.py          # Symbol and Alphabet types
│   ├── probability.py       # Probability distributions
│   ├── states.py            # CausalState, Transition
│   └── machine.py           # EpsilonMachine
└── ...
```

---

## 1. Alphabet Types

### `Symbol` (Type Alias)

```python
from typing import TypeVar, Hashable

# Generic symbol type - any hashable value
Symbol = TypeVar('Symbol', bound=Hashable)
```

### `Alphabet[A]` (Protocol)

```python
from typing import Protocol, TypeVar, Iterator, Hashable

A = TypeVar('A', bound=Hashable)

class Alphabet(Protocol[A]):
    """A finite set of symbols."""
    
    def __contains__(self, symbol: A) -> bool:
        """Check if symbol is in alphabet."""
        ...
    
    def __iter__(self) -> Iterator[A]:
        """Iterate over symbols."""
        ...
    
    def __len__(self) -> int:
        """Number of symbols."""
        ...
    
    @property
    def symbols(self) -> frozenset[A]:
        """The set of all symbols."""
        ...
```

### `ConcreteAlphabet[A]` (Implementation)

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ConcreteAlphabet(Generic[A]):
    """Immutable alphabet implementation."""
    
    _symbols: frozenset[A]
    
    def __contains__(self, symbol: A) -> bool:
        return symbol in self._symbols
    
    def __iter__(self) -> Iterator[A]:
        return iter(self._symbols)
    
    def __len__(self) -> int:
        return len(self._symbols)
    
    @property
    def symbols(self) -> frozenset[A]:
        return self._symbols
    
    @classmethod
    def binary(cls) -> 'ConcreteAlphabet[int]':
        """Create binary alphabet {0, 1}."""
        return cls(frozenset({0, 1}))
    
    @classmethod
    def from_symbols(cls, *symbols: A) -> 'ConcreteAlphabet[A]':
        """Create alphabet from symbols."""
        return cls(frozenset(symbols))
```

---

## 2. Probability Types

### `ProbabilityValue` (Type Alias)

```python
# For v1, probabilities are floats
# Extension point for Rational/symbolic (ADR-006)
ProbabilityValue = float
```

### `Distribution[A]` (Immutable Mapping)

```python
from typing import Mapping, Iterator

@dataclass(frozen=True)
class Distribution(Generic[A]):
    """
    An immutable probability distribution over symbols.
    
    Invariants:
    - All probabilities are in [0, 1]
    - Probabilities sum to 1 (within tolerance)
    - Only non-zero probabilities are stored
    """
    
    _probs: Mapping[A, ProbabilityValue]
    
    def __post_init__(self) -> None:
        # Validate probabilities
        total = sum(self._probs.values())
        if not (0.999 <= total <= 1.001):
            raise ValueError(f"Probabilities must sum to 1, got {total}")
        for p in self._probs.values():
            if not (0 <= p <= 1):
                raise ValueError(f"Probability must be in [0,1], got {p}")
    
    def __getitem__(self, symbol: A) -> ProbabilityValue:
        return self._probs.get(symbol, 0.0)
    
    def __iter__(self) -> Iterator[A]:
        return iter(self._probs)
    
    def __len__(self) -> int:
        return len(self._probs)
    
    @property
    def support(self) -> frozenset[A]:
        """Symbols with non-zero probability."""
        return frozenset(self._probs.keys())
    
    def entropy(self) -> float:
        """Shannon entropy of the distribution."""
        import math
        return -sum(
            p * math.log2(p) 
            for p in self._probs.values() 
            if p > 0
        )
    
    @classmethod
    def uniform(cls, symbols: frozenset[A]) -> 'Distribution[A]':
        """Create uniform distribution over symbols."""
        n = len(symbols)
        return cls({s: 1.0 / n for s in symbols})
    
    @classmethod
    def deterministic(cls, symbol: A) -> 'Distribution[A]':
        """Create distribution with all mass on one symbol."""
        return cls({symbol: 1.0})
```

---

## 3. State Types

### `StateId` (Type Alias)

```python
# States are identified by strings
StateId = str
```

### `Transition[A]`

```python
@dataclass(frozen=True)
class Transition(Generic[A]):
    """
    A labeled transition from one state to another.
    
    Represents: "On symbol `symbol`, go to `target` with probability `probability`"
    """
    
    symbol: A
    probability: ProbabilityValue
    target: StateId
    
    def __post_init__(self) -> None:
        if not (0 < self.probability <= 1):
            raise ValueError(f"Probability must be in (0,1], got {self.probability}")
```

### `CausalState[A]`

```python
@dataclass(frozen=True)
class CausalState(Generic[A]):
    """
    A causal state in an epsilon-machine.
    
    A causal state is an equivalence class of histories that induce
    the same conditional distribution over futures.
    """
    
    id: StateId
    transitions: frozenset[Transition[A]]
    
    def __post_init__(self) -> None:
        # Validate: transitions for each symbol should sum to <= 1
        # (can be < 1 if machine is partial)
        by_symbol: dict[A, float] = {}
        for t in self.transitions:
            by_symbol[t.symbol] = by_symbol.get(t.symbol, 0.0) + t.probability
        for symbol, total in by_symbol.items():
            if total > 1.001:
                raise ValueError(
                    f"Transitions for symbol {symbol} sum to {total} > 1"
                )
    
    @property
    def alphabet(self) -> frozenset[A]:
        """Symbols that have transitions from this state."""
        return frozenset(t.symbol for t in self.transitions)
    
    def transition_distribution(self, symbol: A) -> Distribution[StateId]:
        """
        Get the distribution over next states given a symbol.
        
        Raises:
            KeyError: If symbol has no transitions from this state
        """
        relevant = [t for t in self.transitions if t.symbol == symbol]
        if not relevant:
            raise KeyError(f"No transition for symbol {symbol} from state {self.id}")
        return Distribution({t.target: t.probability for t in relevant})
    
    def emission_distribution(self) -> Distribution[A]:
        """
        Get the distribution over emitted symbols from this state.
        
        Note: This assumes the machine is "edge-emitting" (symbols on transitions).
        """
        probs: dict[A, float] = {}
        for t in self.transitions:
            probs[t.symbol] = probs.get(t.symbol, 0.0) + t.probability
        return Distribution(probs)
    
    def next_states(self, symbol: A) -> frozenset[StateId]:
        """Get possible next states given a symbol."""
        return frozenset(t.target for t in self.transitions if t.symbol == symbol)
```

---

## 4. Epsilon-Machine

### `EpsilonMachine[A]`

```python
@dataclass(frozen=True)
class EpsilonMachine(Generic[A]):
    """
    An epsilon-machine (ε-machine) over alphabet A.
    
    An ε-machine is the minimal, optimal predictor of a stationary stochastic
    process. It consists of:
    - A finite set of causal states
    - Labeled transitions between states
    - A stationary distribution over states
    
    Properties:
    - Unifilarity: Each (state, symbol) pair has at most one outgoing transition
    - Minimality: No two states have the same conditional future distribution
    
    This class represents the result of inference - the discovered structure.
    """
    
    alphabet: frozenset[A]
    states: frozenset[CausalState[A]]
    start_state: StateId
    stationary_distribution: Distribution[StateId]
    
    def __post_init__(self) -> None:
        # Validate start state exists
        state_ids = frozenset(s.id for s in self.states)
        if self.start_state not in state_ids:
            raise ValueError(f"Start state {self.start_state} not in states")
        
        # Validate stationary distribution is over states
        for state_id in self.stationary_distribution.support:
            if state_id not in state_ids:
                raise ValueError(
                    f"Stationary distribution contains unknown state {state_id}"
                )
        
        # Validate unifilarity
        for state in self.states:
            seen: dict[A, StateId] = {}
            for t in state.transitions:
                if t.symbol in seen and seen[t.symbol] != t.target:
                    raise ValueError(
                        f"State {state.id} violates unifilarity: "
                        f"symbol {t.symbol} goes to both {seen[t.symbol]} and {t.target}"
                    )
                seen[t.symbol] = t.target
    
    def __len__(self) -> int:
        """Number of causal states."""
        return len(self.states)
    
    @property
    def state_ids(self) -> frozenset[StateId]:
        """Set of all state IDs."""
        return frozenset(s.id for s in self.states)
    
    def get_state(self, state_id: StateId) -> CausalState[A]:
        """
        Get a state by ID.
        
        Raises:
            KeyError: If state not found
        """
        for state in self.states:
            if state.id == state_id:
                return state
        raise KeyError(f"State {state_id} not found")
    
    def transition_matrix(self, symbol: A) -> dict[StateId, Distribution[StateId]]:
        """
        Get the transition matrix for a given symbol.
        
        Returns a mapping from source state to distribution over target states.
        """
        return {
            state.id: state.transition_distribution(symbol)
            for state in self.states
            if symbol in state.alphabet
        }
    
    def is_unifilar(self) -> bool:
        """Check if machine is unifilar (deterministic given state and symbol)."""
        for state in self.states:
            symbols_seen: set[A] = set()
            for t in state.transitions:
                if t.symbol in symbols_seen:
                    return False
                symbols_seen.add(t.symbol)
        return True
    
    def is_ergodic(self) -> bool:
        """Check if machine is ergodic (single recurrent class)."""
        # TODO: Implement graph connectivity check
        raise NotImplementedError()
```

---

## 5. Builder Pattern (for Construction)

Since core types are immutable, provide builders for ergonomic construction:

```python
class EpsilonMachineBuilder(Generic[A]):
    """
    Mutable builder for constructing EpsilonMachine instances.
    
    Usage:
        machine = (
            EpsilonMachineBuilder[int]()
            .with_alphabet({0, 1})
            .add_state("A")
            .add_state("B")
            .add_transition("A", 0, "A", 0.5)
            .add_transition("A", 1, "B", 0.5)
            .add_transition("B", 0, "A", 1.0)
            .with_start_state("A")
            .build()
        )
    """
    
    def __init__(self) -> None:
        self._alphabet: set[A] = set()
        self._states: dict[StateId, list[Transition[A]]] = {}
        self._start_state: StateId | None = None
        self._stationary: dict[StateId, float] | None = None
    
    def with_alphabet(self, symbols: set[A]) -> 'EpsilonMachineBuilder[A]':
        self._alphabet = symbols
        return self
    
    def add_state(self, state_id: StateId) -> 'EpsilonMachineBuilder[A]':
        if state_id not in self._states:
            self._states[state_id] = []
        return self
    
    def add_transition(
        self,
        source: StateId,
        symbol: A,
        target: StateId,
        probability: float
    ) -> 'EpsilonMachineBuilder[A]':
        self.add_state(source)
        self.add_state(target)
        self._alphabet.add(symbol)
        self._states[source].append(Transition(symbol, probability, target))
        return self
    
    def with_start_state(self, state_id: StateId) -> 'EpsilonMachineBuilder[A]':
        self._start_state = state_id
        return self
    
    def with_stationary_distribution(
        self, 
        dist: dict[StateId, float]
    ) -> 'EpsilonMachineBuilder[A]':
        self._stationary = dist
        return self
    
    def build(self) -> EpsilonMachine[A]:
        if self._start_state is None:
            raise ValueError("Start state not set")
        
        states = frozenset(
            CausalState(id=sid, transitions=frozenset(trans))
            for sid, trans in self._states.items()
        )
        
        # Compute stationary distribution if not provided
        if self._stationary is None:
            # TODO: Compute from transition matrices
            # For now, use uniform
            n = len(states)
            self._stationary = {s.id: 1.0/n for s in states}
        
        return EpsilonMachine(
            alphabet=frozenset(self._alphabet),
            states=states,
            start_state=self._start_state,
            stationary_distribution=Distribution(self._stationary),
        )
```

---

## 6. Type Aliases & Exports

### `emic/types/__init__.py`

```python
"""
Core types for epsilon-machine representation.

Public API:
    - Symbol (TypeVar)
    - Alphabet (Protocol)
    - ConcreteAlphabet
    - Distribution
    - Transition
    - CausalState
    - EpsilonMachine
    - EpsilonMachineBuilder
"""

from emic.types.alphabet import Symbol, Alphabet, ConcreteAlphabet
from emic.types.probability import ProbabilityValue, Distribution
from emic.types.states import StateId, Transition, CausalState
from emic.types.machine import EpsilonMachine, EpsilonMachineBuilder

__all__ = [
    'Symbol',
    'Alphabet',
    'ConcreteAlphabet',
    'ProbabilityValue',
    'Distribution',
    'StateId',
    'Transition',
    'CausalState',
    'EpsilonMachine',
    'EpsilonMachineBuilder',
]
```

---

## 7. Example Usage

```python
from emic.types import EpsilonMachineBuilder

# Build the Golden Mean Process ε-machine
#
#     0 (p=0.5)
#   ┌────────┐
#   ▼        │
#  (A) ─────►(B)
#       1         │
#      (p=0.5)    │ 0 (p=1.0)
#                 ▼
#             ┌───┘
#             │
#   (A) ◄─────┘
#
golden_mean = (
    EpsilonMachineBuilder[int]()
    .add_transition("A", 0, "A", 0.5)
    .add_transition("A", 1, "B", 0.5)
    .add_transition("B", 0, "A", 1.0)
    .with_start_state("A")
    .with_stationary_distribution({"A": 2/3, "B": 1/3})
    .build()
)

print(f"States: {golden_mean.state_ids}")
print(f"Alphabet: {golden_mean.alphabet}")
print(f"Is unifilar: {golden_mean.is_unifilar()}")
```

---

## Acceptance Criteria

- [ ] All types are immutable (frozen dataclasses)
- [ ] All types are generic over alphabet type `A`
- [ ] Full type annotations pass `pyright --strict`
- [ ] Invariants validated in `__post_init__`
- [ ] Builder provides ergonomic construction
- [ ] Unit tests cover all public methods
- [ ] Property-based tests verify invariants
- [ ] Docstrings with examples for all public types

## Dependencies

- Python 3.11+ (for modern typing features)
- No external dependencies for core types

## Related Specifications

- Spec 003: Source Protocol (produces sequences for inference)
- Spec 004: Inference Protocol (produces EpsilonMachine from sequences)
- Spec 005: Analysis Protocol (computes measures from EpsilonMachine)
