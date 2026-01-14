# Specification 005: Analysis Protocol

## Status
📋 Draft

## Overview

This specification defines the **Analysis Protocol** — functions and classes that compute measures and characteristics of epsilon-machines.

These measures quantify:
- **Complexity**: How much structure does the process have?
- **Randomness**: How unpredictable is the process?
- **Memory**: How much past information is needed?
- **Asymmetry**: Does forward and reverse time look different?

## Design Principles

- **Pure functions**: Analysis functions are stateless
- **Composable**: Analyses can be chained in pipelines
- **Cached**: Expensive computations are memoized
- **Validated**: Inputs are checked, edge cases handled

---

## 1. Core Measures

### 1.1 Statistical Complexity (Cμ)

The **statistical complexity** is the Shannon entropy of the stationary distribution over causal states. It measures the minimum information required to optimally predict the process.

```python
def statistical_complexity(machine: EpsilonMachine[A]) -> float:
    """
    Compute the statistical complexity Cμ.

    Cμ = H(S) = -Σᵢ πᵢ log₂(πᵢ)

    where πᵢ is the stationary probability of state i.

    Args:
        machine: The epsilon-machine

    Returns:
        Statistical complexity in bits

    Example:
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> statistical_complexity(machine)
        0.9182958340544896  # ≈ -2/3 log(2/3) - 1/3 log(1/3)
    """
    return machine.stationary_distribution.entropy()
```

### 1.2 Entropy Rate (hμ)

The **entropy rate** is the conditional entropy of the next symbol given the current state. It measures the irreducible randomness per symbol.

```python
def entropy_rate(machine: EpsilonMachine[A]) -> float:
    """
    Compute the entropy rate hμ.

    hμ = H(X | S) = Σᵢ πᵢ H(X | S = sᵢ)

    where H(X | S = sᵢ) is the entropy of the emission distribution
    from state sᵢ.

    Args:
        machine: The epsilon-machine

    Returns:
        Entropy rate in bits per symbol

    Example:
        >>> machine = BiasedCoinSource(p=0.5).true_machine
        >>> entropy_rate(machine)
        1.0  # Fair coin: 1 bit per flip
    """
    h = 0.0
    for state in machine.states:
        pi = machine.stationary_distribution[state.id]
        emission = state.emission_distribution()
        h += pi * emission.entropy()
    return h
```

### 1.3 Excess Entropy (E)

The **excess entropy** (also called **predictive information**) is the mutual information between the past and the future. It measures total memory in the process.

```python
def excess_entropy(machine: EpsilonMachine[A]) -> float:
    """
    Compute the excess entropy E.

    E = I(Past; Future) = Cμ + Cμ' - I

    where Cμ' is the complexity of the reverse-time machine
    and I is the mutual information between forward and reverse
    causal states.

    For unifilar machines:
    E = Cμ (statistical complexity equals excess entropy)

    Args:
        machine: The epsilon-machine

    Returns:
        Excess entropy in bits

    Note:
        For general (non-unifilar) machines, this requires
        the reverse-time machine which is not yet implemented.
        Currently returns Cμ as an approximation.
    """
    # For unifilar machines, E = Cμ
    if machine.is_unifilar():
        return statistical_complexity(machine)

    # TODO: Implement full excess entropy calculation
    raise NotImplementedError(
        "Excess entropy for non-unifilar machines not yet implemented"
    )
```

### 1.4 Crypticity

**Crypticity** measures how much information about the causal state is hidden from the observer who only sees the output symbols.

```python
def crypticity(machine: EpsilonMachine[A]) -> float:
    """
    Compute the crypticity χ.

    χ = Cμ - E

    For unifilar machines, χ = 0 (no hidden information).

    Args:
        machine: The epsilon-machine

    Returns:
        Crypticity in bits
    """
    return statistical_complexity(machine) - excess_entropy(machine)
```

### 1.5 Gauge Information (Oracularity)

**Oracularity** measures asymmetry between forward and reverse-time prediction.

```python
def oracularity(machine: EpsilonMachine[A]) -> float:
    """
    Compute the oracularity (gauge information).

    Measures the difference between forward and reverse
    statistical complexity.

    Args:
        machine: The epsilon-machine

    Returns:
        Oracularity in bits

    Note:
        Requires reverse-time machine (not yet implemented).
    """
    raise NotImplementedError("Oracularity requires reverse-time machine")
```

---

## 2. Structural Measures

### 2.1 State Count

```python
def state_count(machine: EpsilonMachine[A]) -> int:
    """
    Number of causal states.

    A simple but fundamental measure of structural complexity.
    """
    return len(machine.states)
```

### 2.2 Transition Count

```python
def transition_count(machine: EpsilonMachine[A]) -> int:
    """
    Total number of transitions.
    """
    return sum(len(s.transitions) for s in machine.states)
```

### 2.3 Topological Complexity

```python
def topological_complexity(machine: EpsilonMachine[A]) -> float:
    """
    Topological complexity: log₂(number of states).

    An upper bound on statistical complexity.
    """
    import math
    n = len(machine.states)
    return math.log2(n) if n > 0 else 0.0
```

### 2.4 Markov Order

```python
def effective_markov_order(machine: EpsilonMachine[A]) -> int | None:
    """
    The effective Markov order of the process.

    Returns the minimum history length L such that the process
    is L-th order Markov, or None if infinite.

    For a unifilar machine with N states, this is at most N-1.
    """
    # TODO: Implement by analyzing transition structure
    raise NotImplementedError()
```

---

## 3. Information-Theoretic Functions

### 3.1 Block Entropy

```python
def block_entropy(
    machine: EpsilonMachine[A],
    length: int
) -> float:
    """
    Compute the block entropy H(X₁, ..., Xₗ).

    The entropy of length-L blocks emitted by the process.

    Args:
        machine: The epsilon-machine
        length: Block length L

    Returns:
        Block entropy in bits
    """
    # Compute by iterating transition matrices
    # H_L = H(π) + Σₖ₌₁ᴸ⁻¹ H(X_{k+1} | S_k)
    # But for stationary: H_L = L * h + C for large L
    ...
```

### 3.2 Block Entropy Growth

```python
def block_entropy_curve(
    machine: EpsilonMachine[A],
    max_length: int,
) -> list[tuple[int, float]]:
    """
    Compute block entropy for lengths 1..max_length.

    Returns:
        List of (length, entropy) pairs

    Useful for visualizing the approach to the entropy rate.
    """
    return [(l, block_entropy(machine, l)) for l in range(1, max_length + 1)]
```

---

## 4. Analysis Results

### `AnalysisSummary`

```python
@dataclass(frozen=True)
class AnalysisSummary:
    """
    Complete analysis of an epsilon-machine.
    """

    # Core measures
    statistical_complexity: float
    entropy_rate: float
    excess_entropy: float
    crypticity: float

    # Structural measures
    num_states: int
    num_transitions: int
    alphabet_size: int

    # Optional measures
    oracularity: float | None = None
    markov_order: int | None = None

    def to_dict(self) -> dict[str, float | int | None]:
        """Convert to dictionary for serialization."""
        return {
            'C_mu': self.statistical_complexity,
            'h_mu': self.entropy_rate,
            'E': self.excess_entropy,
            'chi': self.crypticity,
            'num_states': self.num_states,
            'num_transitions': self.num_transitions,
            'alphabet_size': self.alphabet_size,
            'oracularity': self.oracularity,
            'markov_order': self.markov_order,
        }

    def __str__(self) -> str:
        return (
            f"ε-Machine Analysis:\n"
            f"  States: {self.num_states}\n"
            f"  Transitions: {self.num_transitions}\n"
            f"  Alphabet: {self.alphabet_size} symbols\n"
            f"  Statistical Complexity Cμ: {self.statistical_complexity:.4f} bits\n"
            f"  Entropy Rate hμ: {self.entropy_rate:.4f} bits/symbol\n"
            f"  Excess Entropy E: {self.excess_entropy:.4f} bits\n"
            f"  Crypticity χ: {self.crypticity:.4f} bits\n"
        )


def analyze(machine: EpsilonMachine[A]) -> AnalysisSummary:
    """
    Compute all standard measures for an epsilon-machine.

    Args:
        machine: The epsilon-machine to analyze

    Returns:
        AnalysisSummary with all computed measures

    Example:
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> summary = analyze(machine)
        >>> print(summary)
    """
    c_mu = statistical_complexity(machine)
    h_mu = entropy_rate(machine)

    # Excess entropy (approximate for non-unifilar)
    try:
        e = excess_entropy(machine)
    except NotImplementedError:
        e = c_mu  # Approximation

    return AnalysisSummary(
        statistical_complexity=c_mu,
        entropy_rate=h_mu,
        excess_entropy=e,
        crypticity=c_mu - e,
        num_states=len(machine.states),
        num_transitions=transition_count(machine),
        alphabet_size=len(machine.alphabet),
    )
```

---

## 5. Comparison Functions

```python
def compare_machines(
    machine1: EpsilonMachine[A],
    machine2: EpsilonMachine[A],
) -> dict[str, float]:
    """
    Compare two epsilon-machines.

    Returns differences in key measures.
    """
    a1 = analyze(machine1)
    a2 = analyze(machine2)

    return {
        'delta_C_mu': a1.statistical_complexity - a2.statistical_complexity,
        'delta_h_mu': a1.entropy_rate - a2.entropy_rate,
        'delta_states': a1.num_states - a2.num_states,
    }


def is_isomorphic(
    machine1: EpsilonMachine[A],
    machine2: EpsilonMachine[A],
) -> bool:
    """
    Check if two machines are isomorphic (same structure).

    Two machines are isomorphic if there exists a bijection
    between their states that preserves transitions.
    """
    # Quick checks
    if len(machine1) != len(machine2):
        return False
    if machine1.alphabet != machine2.alphabet:
        return False

    # TODO: Implement graph isomorphism check
    raise NotImplementedError()
```

---

## 6. Pipeline Integration

```python
# Analysis functions work in pipelines

result = (
    GoldenMeanSource(p=0.5, seed=42)
    >> TakeN(50_000)
    >> CSSR(CSSRConfig(max_history=5))
    >> analyze
)

# Or individual measures
c_mu = (
    GoldenMeanSource(p=0.5, seed=42)
    >> TakeN(50_000)
    >> CSSR(CSSRConfig(max_history=5))
    >> (lambda r: statistical_complexity(r.machine))
)
```

To support this, `InferenceResult` should have a `>>` operator:

```python
class InferenceResult:
    def __rshift__(self, func: Callable[['EpsilonMachine[A]'], T]) -> T:
        return func(self.machine)
```

---

## 7. Module Structure

```
emic/analysis/
├── __init__.py           # Re-exports
├── measures/
│   ├── __init__.py
│   ├── complexity.py     # Cμ, topological complexity
│   ├── entropy.py        # hμ, block entropy
│   ├── information.py    # Excess entropy, crypticity
│   └── structural.py     # State count, transition count
├── summary.py            # AnalysisSummary, analyze()
└── comparison.py         # compare_machines, is_isomorphic
```

---

## 8. Canonical Values

For testing and documentation, provide expected values for known processes:

```python
# Expected analysis values for canonical processes

GOLDEN_MEAN_P05 = {
    'C_mu': 0.9182958340544896,  # H(2/3, 1/3)
    'h_mu': 0.5,                  # H(0.5) * 2/3 + 0 * 1/3
    'num_states': 2,
}

EVEN_PROCESS_P05 = {
    'C_mu': 0.9182958340544896,  # Same as Golden Mean
    'h_mu': 0.5,
    'num_states': 2,
}

FAIR_COIN = {
    'C_mu': 0.0,  # One state
    'h_mu': 1.0,  # Maximum entropy
    'num_states': 1,
}

PERIOD_3 = {
    'C_mu': 1.584962500721156,  # log₂(3)
    'h_mu': 0.0,                 # Deterministic
    'num_states': 3,
}
```

---

## Acceptance Criteria

- [ ] Core measures implemented:
  - [ ] Statistical complexity (Cμ)
  - [ ] Entropy rate (hμ)
  - [ ] Excess entropy (E) for unifilar machines
  - [ ] Crypticity (χ)
- [ ] Structural measures implemented
- [ ] `analyze()` produces complete summary
- [ ] Values match known processes (Golden Mean, etc.)
- [ ] Pipeline integration works
- [ ] Unit tests with numerical tolerances
- [ ] Docstrings with mathematical definitions

## Dependencies

- Python 3.11+
- `numpy` (for numerical stability)
- `math` (standard library)

## References

- Crutchfield, J.P. & Feldman, D.P. (2003). "Regularities unseen, randomness observed: Levels of entropy convergence"
- Shalizi, C.R. (2001). "Causal Architecture, Complexity and Self-Organization in Time Series and Cellular Automata"

## Related Specifications

- Spec 002: Core Types (EpsilonMachine analyzed)
- Spec 004: Inference Protocol (produces machines to analyze)
- Spec 006: Output Protocol (visualizes analysis results)
