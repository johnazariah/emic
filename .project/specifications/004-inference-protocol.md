# Specification 004: Inference Protocol

## Status
📋 Draft

## Overview

This specification defines the **Inference Protocol** — the interface for algorithms that reconstruct epsilon-machines from observed sequences.

The primary algorithm is **CSSR** (Causal State Splitting Reconstruction), introduced by Shalizi and Crutchfield. The architecture supports future algorithms via the protocol.

## Design Principles

- **Protocol-based**: Any algorithm matching the interface can be used
- **Configurable**: Algorithms have explicit configuration objects
- **Observable**: Inference can report progress and intermediate states
- **Validated**: Results include quality metrics and diagnostics

---

## 1. Core Protocol

### `InferenceAlgorithm[A]` (Protocol)

```python
from typing import Protocol, TypeVar, Iterable, Hashable

A = TypeVar('A', bound=Hashable)

class InferenceAlgorithm(Protocol[A]):
    """
    An algorithm that infers an epsilon-machine from a sequence.
    """
    
    def infer(
        self, 
        sequence: Iterable[A],
        alphabet: frozenset[A] | None = None,
    ) -> 'InferenceResult[A]':
        """
        Infer an epsilon-machine from the given sequence.
        
        Args:
            sequence: The observed symbols
            alphabet: Known alphabet (inferred from sequence if None)
        
        Returns:
            InferenceResult containing the machine and diagnostics
        
        Raises:
            InsufficientDataError: If sequence too short
            NonConvergenceError: If algorithm fails to converge
        """
        ...
```

### `InferenceResult[A]`

```python
from dataclasses import dataclass
from typing import Generic

@dataclass(frozen=True)
class InferenceResult(Generic[A]):
    """
    The result of epsilon-machine inference.
    
    Contains the inferred machine plus diagnostics and quality metrics.
    """
    
    machine: EpsilonMachine[A]
    
    # Diagnostics
    sequence_length: int
    max_history_used: int
    num_histories_considered: int
    
    # Quality metrics
    log_likelihood: float | None = None
    aic: float | None = None  # Akaike Information Criterion
    bic: float | None = None  # Bayesian Information Criterion
    
    # Convergence info
    converged: bool = True
    iterations: int | None = None
    
    # Warnings
    warnings: tuple[str, ...] = ()
    
    def summary(self) -> str:
        """Return a human-readable summary."""
        return (
            f"Inferred ε-machine:\n"
            f"  States: {len(self.machine)}\n"
            f"  Alphabet size: {len(self.machine.alphabet)}\n"
            f"  Sequence length: {self.sequence_length}\n"
            f"  Max history: {self.max_history_used}\n"
            f"  Converged: {self.converged}\n"
        )
```

---

## 2. CSSR Algorithm

### 2.1 Algorithm Overview

**CSSR** (Causal State Splitting Reconstruction) works by:

1. **Build suffix tree**: Collect statistics for all observed histories up to length L
2. **Initialize**: Start with one state containing all histories
3. **Split**: Recursively split states when histories have statistically different futures
4. **Merge**: Combine states that are statistically indistinguishable
5. **Construct machine**: Build transitions from final state partition

Key insight: Two histories are in the same causal state iff they predict the same distribution over next symbols.

### 2.2 Configuration

```python
@dataclass(frozen=True)
class CSSRConfig:
    """
    Configuration for the CSSR algorithm.
    """
    
    max_history: int
    """Maximum history length L to consider."""
    
    significance: float = 0.05
    """
    Significance level for statistical tests.
    Lower values = more conservative splitting (fewer states).
    """
    
    min_count: int = 5
    """
    Minimum observation count for a history to be considered.
    Histories with fewer observations are merged with parent.
    """
    
    test: str = "chi2"
    """
    Statistical test for comparing distributions.
    Options: "chi2" (chi-squared), "ks" (Kolmogorov-Smirnov), "g" (G-test)
    """
    
    max_iterations: int = 1000
    """Maximum iterations for convergence."""
    
    verbose: bool = False
    """Print progress information."""
    
    def __post_init__(self) -> None:
        if self.max_history < 1:
            raise ValueError(f"max_history must be >= 1, got {self.max_history}")
        if not (0 < self.significance < 1):
            raise ValueError(f"significance must be in (0, 1)")
        if self.min_count < 1:
            raise ValueError(f"min_count must be >= 1")
```

### 2.3 Implementation

```python
@dataclass
class CSSR(Generic[A]):
    """
    Causal State Splitting Reconstruction algorithm.
    
    Infers an epsilon-machine from an observed sequence by:
    1. Building a suffix tree of observed histories
    2. Grouping histories into causal states based on
       statistical indistinguishability of their futures
    
    Reference:
        Shalizi, C.R. & Crutchfield, J.P. (2001).
        "Computational Mechanics: Pattern and Prediction,
        Structure and Simplicity"
    
    Example:
        >>> from emic.sources import GoldenMeanSource, TakeN
        >>> from emic.inference import CSSR
        >>> 
        >>> source = GoldenMeanSource(p=0.5, seed=42)
        >>> sequence = TakeN(10_000)(source)
        >>> 
        >>> cssr = CSSR(CSSRConfig(max_history=5))
        >>> result = cssr.infer(sequence)
        >>> print(result.summary())
    """
    
    config: CSSRConfig
    
    def infer(
        self,
        sequence: Iterable[A],
        alphabet: frozenset[A] | None = None,
    ) -> InferenceResult[A]:
        """Infer epsilon-machine from sequence."""
        
        # Convert to list for multiple passes
        symbols = list(sequence)
        n = len(symbols)
        
        # Check minimum data requirement
        min_required = self.config.min_count * (self.config.max_history + 1)
        if n < min_required:
            raise InsufficientDataError(
                required=min_required,
                provided=n,
                algorithm="CSSR",
            )
        
        # Infer alphabet if not provided
        if alphabet is None:
            alphabet = frozenset(symbols)
        
        # Build suffix tree
        suffix_tree = self._build_suffix_tree(symbols, alphabet)
        
        # Initialize: all histories in one state
        states = self._initialize_states(suffix_tree)
        
        # Iterate: split and merge until convergence
        converged = False
        for iteration in range(self.config.max_iterations):
            old_states = states
            states = self._split_states(states, suffix_tree)
            states = self._merge_states(states)
            
            if states == old_states:
                converged = True
                break
        
        if not converged:
            raise NonConvergenceError(
                iterations=self.config.max_iterations,
                tolerance=self.config.significance,
            )
        
        # Build machine from final states
        machine = self._build_machine(states, suffix_tree, alphabet)
        
        return InferenceResult(
            machine=machine,
            sequence_length=n,
            max_history_used=self.config.max_history,
            num_histories_considered=len(suffix_tree),
            converged=converged,
            iterations=iteration + 1,
        )
    
    def _build_suffix_tree(
        self, 
        symbols: list[A], 
        alphabet: frozenset[A]
    ) -> 'SuffixTree[A]':
        """
        Build a suffix tree collecting next-symbol statistics.
        
        For each history h of length 0..L, count:
        - How many times h was observed
        - Distribution of next symbol after h
        """
        # Implementation detail - see internal module
        ...
    
    def _initialize_states(self, suffix_tree: 'SuffixTree[A]') -> 'StatePartition':
        """Start with all histories in one equivalence class."""
        ...
    
    def _split_states(
        self, 
        states: 'StatePartition',
        suffix_tree: 'SuffixTree[A]'
    ) -> 'StatePartition':
        """
        Split states where histories have different next-symbol distributions.
        
        Uses chi-squared (or configured test) to determine if distributions
        are significantly different.
        """
        ...
    
    def _merge_states(self, states: 'StatePartition') -> 'StatePartition':
        """
        Merge states that are statistically indistinguishable.
        
        Two states are merged if their histories have the same
        distribution over next states (not just next symbols).
        """
        ...
    
    def _build_machine(
        self,
        states: 'StatePartition',
        suffix_tree: 'SuffixTree[A]',
        alphabet: frozenset[A],
    ) -> EpsilonMachine[A]:
        """
        Construct the epsilon-machine from the final state partition.
        """
        ...
    
    # Pipeline operator support
    def __rrshift__(self, source: Iterable[A]) -> InferenceResult[A]:
        """Support: sequence >> CSSR(config)"""
        if hasattr(source, 'alphabet'):
            return self.infer(source, alphabet=source.alphabet)
        return self.infer(source)
```

---

## 3. Internal Data Structures

### `SuffixTree[A]`

```python
@dataclass
class HistoryStats(Generic[A]):
    """Statistics for a single history string."""
    
    history: tuple[A, ...]
    count: int
    next_symbol_counts: dict[A, int]
    
    @property
    def next_symbol_distribution(self) -> Distribution[A]:
        total = sum(self.next_symbol_counts.values())
        return Distribution({
            s: c / total 
            for s, c in self.next_symbol_counts.items()
        })


class SuffixTree(Generic[A]):
    """
    A tree collecting statistics for all observed histories.
    
    Each node represents a history string and stores:
    - Count of observations
    - Distribution of next symbols
    """
    
    def __init__(self, max_depth: int, alphabet: frozenset[A]):
        self.max_depth = max_depth
        self.alphabet = alphabet
        self._stats: dict[tuple[A, ...], HistoryStats[A]] = {}
    
    def add_observation(self, history: tuple[A, ...], next_symbol: A) -> None:
        """Record an observation of history followed by next_symbol."""
        ...
    
    def get_stats(self, history: tuple[A, ...]) -> HistoryStats[A] | None:
        """Get statistics for a history, or None if not observed."""
        return self._stats.get(history)
    
    def histories_of_length(self, length: int) -> Iterator[tuple[A, ...]]:
        """Iterate over all observed histories of given length."""
        for h in self._stats:
            if len(h) == length:
                yield h
```

### `StatePartition`

```python
class StatePartition:
    """
    A partition of histories into equivalence classes (causal states).
    """
    
    def __init__(self) -> None:
        self._history_to_state: dict[tuple[Any, ...], str] = {}
        self._state_to_histories: dict[str, set[tuple[Any, ...]]] = {}
    
    def assign(self, history: tuple[Any, ...], state_id: str) -> None:
        """Assign a history to a state."""
        ...
    
    def get_state(self, history: tuple[Any, ...]) -> str | None:
        """Get the state ID for a history."""
        return self._history_to_state.get(history)
    
    def split_state(
        self, 
        state_id: str, 
        partition: list[set[tuple[Any, ...]]]
    ) -> list[str]:
        """Split a state into multiple new states."""
        ...
    
    def merge_states(self, state_ids: list[str]) -> str:
        """Merge multiple states into one."""
        ...
```

---

## 4. Statistical Tests

```python
from scipy import stats

def chi_squared_test(
    dist1: dict[Any, int],
    dist2: dict[Any, int],
    significance: float,
) -> bool:
    """
    Test if two count distributions are significantly different.
    
    Returns True if distributions are significantly different
    (should be in different states).
    """
    # Align distributions
    all_keys = set(dist1.keys()) | set(dist2.keys())
    obs1 = [dist1.get(k, 0) for k in all_keys]
    obs2 = [dist2.get(k, 0) for k in all_keys]
    
    # Chi-squared test
    contingency = [obs1, obs2]
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
    
    return p_value < significance


def ks_test(
    counts1: dict[Any, int],
    counts2: dict[Any, int],
    significance: float,
) -> bool:
    """
    Kolmogorov-Smirnov test for distribution difference.
    """
    # Convert to samples
    samples1 = []
    samples2 = []
    for i, (k, c) in enumerate(counts1.items()):
        samples1.extend([i] * c)
    for i, (k, c) in enumerate(counts2.items()):
        samples2.extend([i] * c)
    
    statistic, p_value = stats.ks_2samp(samples1, samples2)
    return p_value < significance
```

---

## 5. Error Types

```python
class InferenceError(EpsilonMachineError):
    """Base class for inference errors."""
    pass


class InsufficientDataError(InferenceError):
    """Raised when sequence is too short for reliable inference."""
    
    def __init__(
        self, 
        required: int, 
        provided: int, 
        algorithm: str = "unknown",
        **context
    ):
        super().__init__(
            f"Insufficient data for {algorithm}: "
            f"need {required} symbols, got {provided}",
            **context
        )
        self.required = required
        self.provided = provided
        self.algorithm = algorithm
    
    def explain(self) -> str:
        return (
            f"The sequence you provided has {self.provided} symbols, "
            f"but the {self.algorithm} algorithm needs at least {self.required} "
            f"to produce reliable results. Try:\n"
            f"  • Using a longer sequence\n"
            f"  • Reducing max_history parameter\n"
            f"  • Reducing min_count parameter (less reliable)"
        )


class NonConvergenceError(InferenceError):
    """Raised when algorithm fails to converge."""
    
    def __init__(self, iterations: int, tolerance: float, **context):
        super().__init__(
            f"Algorithm did not converge after {iterations} iterations",
            **context
        )
        self.iterations = iterations
        self.tolerance = tolerance
    
    def explain(self) -> str:
        return (
            f"The algorithm did not stabilize after {self.iterations} iterations. "
            f"This might indicate:\n"
            f"  • The process has complex structure requiring more iterations\n"
            f"  • The significance level ({self.tolerance}) is too sensitive\n"
            f"  • The data contains anomalies\n"
            f"Try increasing max_iterations or significance level."
        )
```

---

## 6. Module Structure

```
emic/inference/
├── __init__.py           # Re-exports
├── protocol.py           # InferenceAlgorithm protocol
├── result.py             # InferenceResult
├── cssr/
│   ├── __init__.py       # CSSR class
│   ├── config.py         # CSSRConfig
│   ├── suffix_tree.py    # SuffixTree implementation
│   ├── partition.py      # StatePartition
│   └── tests.py          # Statistical tests
├── errors.py             # InferenceError hierarchy
└── _future/              # Placeholder for future algorithms
    ├── bayesian.py
    └── spectral.py
```

---

## 7. Usage Examples

### Basic Usage

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig

# Generate data
source = GoldenMeanSource(p=0.5, seed=42)
sequence = TakeN(50_000)(source)

# Infer machine
config = CSSRConfig(max_history=5, significance=0.01)
result = CSSR(config).infer(sequence)

print(result.summary())
# Inferred ε-machine:
#   States: 2
#   Alphabet size: 2
#   Sequence length: 50000
#   Max history: 5
#   Converged: True
```

### Pipeline Syntax

```python
result = (
    GoldenMeanSource(p=0.5, seed=42)
    >> TakeN(50_000)
    >> CSSR(CSSRConfig(max_history=5))
)
```

### Validation Against Known Machine

```python
source = GoldenMeanSource(p=0.5, seed=42)
sequence = TakeN(50_000)(source)

result = CSSR(CSSRConfig(max_history=5)).infer(sequence)
inferred = result.machine
true = source.true_machine

# Compare
assert len(inferred) == len(true), "State count mismatch!"
```

---

## Acceptance Criteria

- [ ] CSSR algorithm correctly infers known processes:
  - [ ] Golden Mean (2 states)
  - [ ] Even Process (2 states)
  - [ ] Biased Coin (1 state)
  - [ ] Period-N (N states)
- [ ] Statistical tests properly implemented
- [ ] Clear error messages for insufficient data
- [ ] Pipeline operator works
- [ ] Configurable via `CSSRConfig`
- [ ] Results include diagnostics
- [ ] Unit tests with >90% coverage
- [ ] Property tests: inferred machine is unifilar

## Dependencies

- Python 3.11+
- `scipy` (for statistical tests)
- `numpy` (for numerical operations)

## References

- Shalizi, C.R. & Crutchfield, J.P. (2001). "Computational Mechanics: Pattern and Prediction, Structure and Simplicity"
- CSSR implementation notes: https://bactra.org/CSSR/

## Related Specifications

- Spec 002: Core Types (EpsilonMachine produced)
- Spec 003: Source Protocol (sequences consumed)
- Spec 005: Analysis Protocol (analyzes inferred machines)
