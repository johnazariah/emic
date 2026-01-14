# ADR-006: Symbolic Computation Strategy

## Status
**Accepted** — 2026-01-14

## Context

The framework needs to support different alphabet types for epsilon-machines. A key question is whether to include symbolic computation (SymPy-based) support from the start or defer it.

### Use Cases for Symbolic Computation

1. **Exact arithmetic**: Represent probabilities as rationals (e.g., `Rational(1, 3)`) instead of floats
2. **Symbolic alphabets**: Use mathematical symbols instead of concrete values
3. **Algebraic manipulation**: Simplify transition matrices symbolically
4. **Verification**: Prove properties exactly rather than numerically
5. **Publication**: Generate exact expressions for papers

### Options Considered

#### Option A: Full Symbolic Support in v1
- Implement SymPy-based alphabets and probability types immediately
- **Pros**: Complete capability from day one
- **Cons**: Increased complexity, longer development time, potential over-engineering

#### Option B: Extension Point Design
- Design generic types (`Alphabet[A]`, `Probability`) from the start
- Implement with concrete types first (`int`, `str`, `float`)
- Ensure architecture accommodates symbolic types
- Add SymPy support in a later version

## Decision

**We adopt Option B: Extension Point Design**

### The Bold Gambit

We will:

1. **Design generically**: The type parameter `A` in `EpsilonMachine[A]` supports any hashable symbol type
2. **Abstract probability representation**: Use a `Probability` protocol/type that can be backed by `float` or `Rational`
3. **Start concrete**: Implement with `int`/`str` alphabets and `float` probabilities
4. **Validate first**: Prove the architecture works before adding complexity
5. **Extend later**: Add `emic.symbolic` module when core is stable

### Generic Design Patterns

```python
from typing import Protocol, TypeVar, Generic, Hashable

# Symbol type is generic and hashable
A = TypeVar('A', bound=Hashable)

# Probability can be float or exact
class SupportsArithmetic(Protocol):
    def __add__(self, other: 'SupportsArithmetic') -> 'SupportsArithmetic': ...
    def __mul__(self, other: 'SupportsArithmetic') -> 'SupportsArithmetic': ...
    def __float__(self) -> float: ...

P = TypeVar('P', bound=SupportsArithmetic)

# Core types are parameterized
@dataclass(frozen=True)
class Transition(Generic[A, P]):
    symbol: A
    probability: P
    target_state: str

@dataclass(frozen=True)
class EpsilonMachine(Generic[A]):
    """Works with any alphabet type."""
    alphabet: frozenset[A]
    states: frozenset[CausalState[A]]
    # ...
```

### Extension Point for Symbolic

Future `emic.symbolic` module would provide:

```python
from sympy import Symbol, Rational
from emic.symbolic import SymbolicMachine

# Symbolic alphabet
a, b = Symbol('a'), Symbol('b')
machine: SymbolicMachine = infer_symbolic(sequence, alphabet={a, b})

# Exact probabilities
machine.transitions  # Returns Rational values
machine.statistical_complexity  # Exact symbolic expression
```

### Validation Criteria

Before adding symbolic support, the core must:
- [ ] Successfully infer machines for all canonical processes
- [ ] Pass comprehensive property-based tests
- [ ] Have stable public API
- [ ] Demonstrate extensibility with at least one custom alphabet type

## Consequences

### Positive
- **Faster v1**: Focus on core functionality first
- **Validated architecture**: Prove design before adding complexity  
- **Clean extension**: Symbolic support adds to, doesn't modify, core
- **Lower risk**: Avoid over-engineering for features that may not be needed

### Negative
- **Delayed capability**: Symbolic computation not immediately available
- **Potential rework**: If generic design proves insufficient (mitigated by careful upfront design)

### Neutral
- Must document extension points clearly
- Tests should include at least one non-trivial alphabet type (e.g., custom enum)

## Future Work

When adding symbolic support:
1. Create `emic.symbolic` subpackage
2. Implement `SymbolicProbability` backed by `sympy.Rational`
3. Add symbolic-aware inference algorithms
4. Provide conversion utilities between numeric and symbolic representations

## References
- [SymPy Documentation](https://docs.sympy.org/)
- [Python Generics (PEP 484)](https://peps.python.org/pep-0484/)
