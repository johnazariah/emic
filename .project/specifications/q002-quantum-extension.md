# Specification: Quantum Extension to emic

*Design specification for implementing quantum complexity measures*

**Spec ID:** q002-quantum-extension
**Status:** Draft
**Created:** 2026-01-28
**Dependencies:** Prerequisites must be addressed first (see [prerequisites.md](../../research/quantum-emergence/prerequisites.md))

---

## Overview

This specification defines the quantum extension to emic, enabling computation of:
- Quantum statistical complexity ($C_q$)
- Quantum memory advantage ($\Delta_q = C_\mu - C_q$)
- Decoherence trajectories
- (Future) Causal asymmetry

---

## Part 1: Module Structure

### New Package: `emic.quantum`

```
src/emic/quantum/
├── __init__.py          # Public API exports
├── types.py             # Core quantum types
├── construction.py      # Q-machine construction
├── measures.py          # Quantum complexity measures
├── channels.py          # Decoherence channels
└── utils.py             # Linear algebra utilities
```

### Dependencies

**Required:**
- `numpy` (already in project) — linear algebra, eigenvalue computation

**Not Required:**
- No additional quantum libraries (Qiskit, Cirq, etc.)
- No new external dependencies

---

## Part 2: Type Definitions

### 2.1 QuantumCausalState

```python
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

from emic.types import StateId

@dataclass(frozen=True)
class QuantumCausalState:
    """
    Quantum state associated with a classical causal state.

    Represents the signal state |s_j⟩ from Gu et al. (2012).

    Attributes:
        classical_id: ID of the corresponding classical causal state
        state_vector: Complex state vector in C^d

    Invariants:
        - state_vector is normalized: ||state_vector||² = 1
        - state_vector has shape (hilbert_dim,)
    """
    classical_id: StateId
    state_vector: NDArray[np.complex128]

    def __post_init__(self) -> None:
        """Validate state vector is normalized."""
        norm_sq = np.vdot(self.state_vector, self.state_vector).real
        if abs(norm_sq - 1.0) > 1e-10:
            raise ValueError(f"State vector not normalized: ||v||² = {norm_sq}")

    @property
    def dimension(self) -> int:
        """Hilbert space dimension."""
        return len(self.state_vector)

    def overlap(self, other: "QuantumCausalState") -> complex:
        """Compute inner product ⟨self|other⟩."""
        return np.vdot(self.state_vector, other.state_vector)

    def density_matrix(self) -> NDArray[np.complex128]:
        """Compute |s⟩⟨s| outer product."""
        v = self.state_vector
        return np.outer(v, np.conj(v))
```

### 2.2 QuantumEpsilonMachine

```python
from functools import cached_property
from collections.abc import Hashable
from typing import TypeVar, Generic

from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)

@dataclass(frozen=True)
class QuantumEpsilonMachine(Generic[A]):
    """
    Quantum epsilon-machine (q-machine) representation.

    Constructed from a classical epsilon-machine following Gu et al. (2012).

    Attributes:
        classical_machine: The source epsilon-machine
        quantum_states: Mapping from state ID to quantum signal state
        hilbert_dimension: Total Hilbert space dimension (|Σ| × N)

    Properties:
        density_matrix: Average density matrix ρ = Σ πⱼ |sⱼ⟩⟨sⱼ|
        quantum_complexity: C_q = S(ρ)
        quantum_advantage: Δ_q = C_μ - C_q
    """
    classical_machine: EpsilonMachine[A]
    quantum_states: dict[StateId, QuantumCausalState]
    hilbert_dimension: int

    @cached_property
    def density_matrix(self) -> NDArray[np.complex128]:
        """
        Average density matrix ρ = Σⱼ πⱼ |sⱼ⟩⟨sⱼ|.

        Returns:
            Complex Hermitian matrix of shape (d, d)
        """
        d = self.hilbert_dimension
        rho = np.zeros((d, d), dtype=np.complex128)

        stationary = self.classical_machine.stationary_distribution
        for state_id, qstate in self.quantum_states.items():
            pi_j = stationary.probs.get(state_id, 0.0)
            if pi_j > 0:
                rho += pi_j * qstate.density_matrix()

        return rho

    @cached_property
    def quantum_complexity(self) -> float:
        """
        Quantum statistical complexity C_q = S(ρ).

        Returns:
            Von Neumann entropy in bits
        """
        from emic.quantum.utils import von_neumann_entropy
        return von_neumann_entropy(self.density_matrix)

    @cached_property
    def quantum_advantage(self) -> float:
        """
        Memory advantage Δ_q = C_μ - C_q.

        Returns:
            Bits saved by quantum encoding
        """
        from emic.analysis.measures import statistical_complexity
        c_mu = statistical_complexity(self.classical_machine)
        return c_mu - self.quantum_complexity

    def overlap_matrix(self) -> NDArray[np.float64]:
        """
        Matrix of pairwise overlaps |⟨sⱼ|sₖ⟩|².

        Useful for visualizing non-orthogonality.
        """
        n = len(self.quantum_states)
        ids = list(self.quantum_states.keys())
        overlaps = np.zeros((n, n))

        for i, id_i in enumerate(ids):
            for j, id_j in enumerate(ids):
                inner = self.quantum_states[id_i].overlap(self.quantum_states[id_j])
                overlaps[i, j] = abs(inner) ** 2

        return overlaps
```

---

## Part 3: Construction Algorithm

### 3.1 construct_qmachine

```python
def construct_qmachine(
    machine: EpsilonMachine[A],
) -> QuantumEpsilonMachine[A]:
    """
    Construct q-machine from classical epsilon-machine.

    Implements the construction from Gu et al. (2012):

    |sⱼ⟩ = Σₖ Σₓ √T^(x)_{jk} |x⟩ ⊗ |k⟩

    Args:
        machine: Source epsilon-machine

    Returns:
        QuantumEpsilonMachine with signal states and measures

    Raises:
        ValueError: If machine has no states or invalid transitions

    Examples:
        >>> from emic.sources.synthetic import PerturbedCoinSource
        >>> machine = PerturbedCoinSource(p=0.4).true_machine
        >>> qm = construct_qmachine(machine)
        >>> abs(qm.quantum_complexity - 0.08) < 0.01
        True
    """
    states = list(machine.states)
    alphabet = list(machine.alphabet)

    N = len(states)
    m = len(alphabet)
    d = N * m  # Hilbert space dimension

    # Create mappings for indexing
    state_to_idx = {s.id: i for i, s in enumerate(states)}
    symbol_to_idx = {sym: i for i, sym in enumerate(alphabet)}

    # Build quantum states
    quantum_states: dict[StateId, QuantumCausalState] = {}

    for j, state in enumerate(states):
        # Initialize state vector
        psi = np.zeros(d, dtype=np.complex128)

        # Accumulate amplitudes from transitions
        for transition in state.transitions:
            x_idx = symbol_to_idx[transition.symbol]
            k_idx = state_to_idx[transition.target]

            # Tensor product index: |x⟩ ⊗ |k⟩
            idx = x_idx * N + k_idx

            # Amplitude = √(transition probability)
            psi[idx] += np.sqrt(transition.probability)

        # Validate normalization
        norm = np.linalg.norm(psi)
        if abs(norm - 1.0) > 1e-10:
            raise ValueError(f"State {state.id} has non-unit norm: {norm}")

        quantum_states[state.id] = QuantumCausalState(
            classical_id=state.id,
            state_vector=psi,
        )

    return QuantumEpsilonMachine(
        classical_machine=machine,
        quantum_states=quantum_states,
        hilbert_dimension=d,
    )
```

---

## Part 4: Utility Functions

### 4.1 von_neumann_entropy

```python
def von_neumann_entropy(
    rho: NDArray[np.complex128],
    base: float = 2.0,
    tol: float = 1e-12,
) -> float:
    """
    Compute von Neumann entropy S(ρ) = -Tr(ρ log ρ).

    Args:
        rho: Density matrix (Hermitian, unit trace, positive semi-definite)
        base: Logarithm base (2 for bits, e for nats)
        tol: Eigenvalue threshold below which treated as zero

    Returns:
        Entropy in specified units

    Raises:
        ValueError: If rho is not a valid density matrix
    """
    # Validate density matrix
    _validate_density_matrix(rho, tol)

    # Compute eigenvalues (Hermitian, so real)
    eigenvalues = np.linalg.eigvalsh(rho)

    # Filter near-zero eigenvalues
    eigenvalues = eigenvalues[eigenvalues > tol]

    if len(eigenvalues) == 0:
        return 0.0

    # Compute entropy: -Σ λ log(λ)
    if base == 2.0:
        log_eigenvalues = np.log2(eigenvalues)
    elif base == np.e:
        log_eigenvalues = np.log(eigenvalues)
    else:
        log_eigenvalues = np.log(eigenvalues) / np.log(base)

    return float(-np.sum(eigenvalues * log_eigenvalues))


def _validate_density_matrix(
    rho: NDArray[np.complex128],
    tol: float = 1e-12,
) -> None:
    """Validate that rho is a valid density matrix."""
    # Check square
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        raise ValueError(f"Density matrix must be square, got shape {rho.shape}")

    # Check Hermitian
    if not np.allclose(rho, rho.conj().T, atol=tol):
        raise ValueError("Density matrix must be Hermitian")

    # Check unit trace
    trace = np.trace(rho).real
    if abs(trace - 1.0) > tol:
        raise ValueError(f"Density matrix must have unit trace, got {trace}")

    # Check positive semi-definite
    eigenvalues = np.linalg.eigvalsh(rho)
    if np.any(eigenvalues < -tol):
        raise ValueError(f"Density matrix must be positive semi-definite, min eigenvalue: {min(eigenvalues)}")
```

---

## Part 5: Decoherence Channels

### 5.1 apply_dephasing

```python
def apply_dephasing(
    rho: NDArray[np.complex128],
    gamma: float,
) -> NDArray[np.complex128]:
    """
    Apply dephasing channel with strength γ.

    E_γ(ρ) = (1-γ)ρ + γ·diag(ρ)

    Args:
        rho: Density matrix
        gamma: Dephasing strength in [0, 1]
            - γ=0: no dephasing (identity)
            - γ=1: full dephasing (classical limit)

    Returns:
        Decohered density matrix

    Raises:
        ValueError: If gamma not in [0, 1]
    """
    if not 0.0 <= gamma <= 1.0:
        raise ValueError(f"gamma must be in [0, 1], got {gamma}")

    if gamma == 0.0:
        return rho.copy()

    diagonal = np.diag(np.diag(rho))
    return (1.0 - gamma) * rho + gamma * diagonal


def apply_depolarizing(
    rho: NDArray[np.complex128],
    gamma: float,
) -> NDArray[np.complex128]:
    """
    Apply depolarizing channel with strength γ.

    E_γ(ρ) = (1-γ)ρ + γ·I/d

    Args:
        rho: Density matrix
        gamma: Depolarizing strength in [0, 1]

    Returns:
        Depolarized density matrix
    """
    if not 0.0 <= gamma <= 1.0:
        raise ValueError(f"gamma must be in [0, 1], got {gamma}")

    if gamma == 0.0:
        return rho.copy()

    d = rho.shape[0]
    maximally_mixed = np.eye(d, dtype=np.complex128) / d
    return (1.0 - gamma) * rho + gamma * maximally_mixed
```

### 5.2 decoherence_trajectory

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class DecoherencePoint:
    """Single point on decoherence trajectory."""
    gamma: float
    complexity: float


def decoherence_trajectory(
    qmachine: QuantumEpsilonMachine,
    gamma_values: Sequence[float] | None = None,
    channel: Literal["dephasing", "depolarizing"] = "dephasing",
) -> list[DecoherencePoint]:
    """
    Compute complexity as function of decoherence strength.

    Args:
        qmachine: Quantum epsilon-machine
        gamma_values: Decoherence strengths to sample (default: 0 to 1 in 0.05 steps)
        channel: Type of decoherence channel

    Returns:
        List of (gamma, complexity) points

    Examples:
        >>> qm = construct_qmachine(machine)
        >>> trajectory = decoherence_trajectory(qm)
        >>> trajectory[0].complexity == qm.quantum_complexity  # gamma=0
        True
    """
    if gamma_values is None:
        gamma_values = [i / 20 for i in range(21)]  # 0.0, 0.05, ..., 1.0

    rho = qmachine.density_matrix
    apply_channel = apply_dephasing if channel == "dephasing" else apply_depolarizing

    results = []
    for gamma in gamma_values:
        rho_decohered = apply_channel(rho, gamma)
        complexity = von_neumann_entropy(rho_decohered)
        results.append(DecoherencePoint(gamma=gamma, complexity=complexity))

    return results
```

---

## Part 6: Measures Module

### 6.1 Public API

```python
# emic/quantum/measures.py

def quantum_complexity(machine: EpsilonMachine[A]) -> float:
    """
    Compute quantum statistical complexity C_q.

    Convenience function that constructs q-machine internally.

    Args:
        machine: Epsilon-machine

    Returns:
        Quantum complexity in bits
    """
    qm = construct_qmachine(machine)
    return qm.quantum_complexity


def quantum_advantage(machine: EpsilonMachine[A]) -> float:
    """
    Compute quantum memory advantage Δ_q = C_μ - C_q.

    Args:
        machine: Epsilon-machine

    Returns:
        Memory saved by quantum encoding, in bits
    """
    qm = construct_qmachine(machine)
    return qm.quantum_advantage


def has_quantum_advantage(machine: EpsilonMachine[A]) -> bool:
    """
    Check if process has strict quantum advantage.

    Equivalent to checking irreversibility condition.

    Args:
        machine: Epsilon-machine

    Returns:
        True if C_q < C_μ
    """
    return quantum_advantage(machine) > 1e-10
```

---

## Part 7: Integration with Existing Code

### 7.1 AnalysisSummary Extension

Add quantum fields to `AnalysisSummary`:

```python
@dataclass(frozen=True)
class AnalysisSummary:
    # ... existing fields ...

    # Quantum measures (optional, computed on demand)
    quantum_complexity: float | None = None
    quantum_advantage: float | None = None
```

### 7.2 analyze() Function Update

```python
def analyze(
    machine: EpsilonMachine[A],
    include_quantum: bool = False,
) -> AnalysisSummary:
    """
    Compute all standard measures for an epsilon-machine.

    Args:
        machine: The epsilon-machine to analyze
        include_quantum: If True, also compute C_q (slower)

    Returns:
        AnalysisSummary with all computed measures
    """
    # ... existing code ...

    quantum_c = None
    quantum_a = None
    if include_quantum:
        from emic.quantum import quantum_complexity, quantum_advantage
        quantum_c = quantum_complexity(machine)
        quantum_a = quantum_advantage(machine)

    return AnalysisSummary(
        # ... existing fields ...
        quantum_complexity=quantum_c,
        quantum_advantage=quantum_a,
    )
```

---

## Part 8: Public API Exports

### `emic.quantum.__init__.py`

```python
"""Quantum complexity measures for epsilon-machines."""

from emic.quantum.types import (
    QuantumCausalState,
    QuantumEpsilonMachine,
)
from emic.quantum.construction import construct_qmachine
from emic.quantum.measures import (
    quantum_complexity,
    quantum_advantage,
    has_quantum_advantage,
)
from emic.quantum.channels import (
    apply_dephasing,
    apply_depolarizing,
    decoherence_trajectory,
    DecoherencePoint,
)
from emic.quantum.utils import von_neumann_entropy

__all__ = [
    # Types
    "QuantumCausalState",
    "QuantumEpsilonMachine",
    # Construction
    "construct_qmachine",
    # Measures
    "quantum_complexity",
    "quantum_advantage",
    "has_quantum_advantage",
    # Channels
    "apply_dephasing",
    "apply_depolarizing",
    "decoherence_trajectory",
    "DecoherencePoint",
    # Utilities
    "von_neumann_entropy",
]
```

---

## Part 9: Testing Strategy

### Unit Tests

| Test | Description |
|------|-------------|
| `test_von_neumann_entropy_pure` | $S(\|ψ⟩⟨ψ\|) = 0$ |
| `test_von_neumann_entropy_mixed` | Known values for simple matrices |
| `test_density_matrix_validation` | Rejects invalid matrices |
| `test_signal_state_normalization` | All signal states have unit norm |
| `test_density_matrix_properties` | Hermitian, unit trace, positive |

### Integration Tests

| Test | Description |
|------|-------------|
| `test_fair_coin_zero_advantage` | $C_q = C_\mu = 0$ |
| `test_perturbed_coin_advantage` | $C_q < C_\mu$ for $p \neq 0, 1$ |
| `test_decoherence_limits` | $C_q(0) = C_q$, $C_q(1) \approx C_\mu$ |

### Golden Tests

| Test | Source |
|------|--------|
| Perturbed coin $p=0.1$ | Gu et al. (2012) |
| Perturbed coin $p=0.4$ | Gu et al. (2012) |
| Golden mean | Computed |

---

## Part 10: Documentation

### Docstrings

All public functions must have:
- One-line summary
- Extended description with math notation
- Args/Returns/Raises sections
- Examples that run as doctests

### Guide Page

Add `docs/guide/quantum-complexity.md`:
- Conceptual introduction
- How to use the API
- Interpretation of measures
- Example workflow

### API Reference

Add `docs/api/quantum.md`:
- Auto-generated from docstrings
- Type signatures
- Cross-references

---

## Part 11: Future Extensions

### Phase 2: Causal Asymmetry

Requires reverse machine construction (see prerequisites).

```python
def causal_asymmetry(machine: EpsilonMachine[A]) -> float:
    """Compute ΔC = |C_μ⁺ - C_μ⁻|."""
    ...

def quantum_causal_asymmetry(machine: EpsilonMachine[A]) -> float:
    """Compute quantum causal asymmetry (should be ≈ 0)."""
    ...
```

### Phase 3: Finite-Sample Estimation

```python
def estimate_quantum_complexity(
    data: Sequence[Symbol],
    confidence: float = 0.95,
) -> tuple[float, float, float]:
    """
    Estimate C_q from data with confidence interval.

    Returns:
        (estimate, lower_bound, upper_bound)
    """
    ...
```

### Phase 4: Visualization

```python
def plot_decoherence_trajectory(
    trajectory: list[DecoherencePoint],
    ax: matplotlib.axes.Axes | None = None,
) -> matplotlib.axes.Axes:
    """Plot C_q(γ) trajectory."""
    ...
```

---

## Acceptance Criteria

### Minimum Viable

- [ ] `construct_qmachine()` works for any valid ε-machine
- [ ] `quantum_complexity()` returns correct values for perturbed coin
- [ ] `decoherence_trajectory()` produces monotonic curves
- [ ] All tests pass, 90%+ coverage on new code

### Target

- [ ] Full validation suite passes
- [ ] Documentation complete
- [ ] Integration with existing analysis module
- [ ] Performance acceptable (< 1s for machines up to 100 states)

---

*Document version: 1.0*
*Created: 2026-01-28*
*Status: Ready for review*
