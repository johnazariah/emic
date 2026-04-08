# Specification 021: Quantum Core Types

## Status
📝 Planning

## Overview

This specification defines the core immutable data types for representing quantum epsilon-machines (q-machines) within emic. These types extend the classical type system (Spec 002) to support quantum causal states, density matrices, and related structures.

## Design Principles

- **Consistent with classical types**: Same patterns — frozen dataclasses, Protocols, generics
- **Immutable**: All quantum types are frozen dataclasses
- **NumPy-backed**: Density matrices and state vectors use `numpy.ndarray` internally, wrapped in immutable types
- **Composable**: Quantum types work with the existing pipeline (`>>`) and analysis modules  
- **Validated**: Construction enforces physical constraints (hermiticity, trace, positivity)

## Dependencies

- `numpy` (already available — used in spectral inference)
- `scipy.linalg` (eigenvalue computation for von Neumann entropy)
- Classical types from `emic.types`: `EpsilonMachine`, `CausalState`, `StateId`, `Distribution`

---

## 1. QuantumState

A pure quantum state vector. Used to represent individual quantum causal states.

```python
@dataclass(frozen=True)
class QuantumState:
    """
    A pure quantum state |ψ⟩ represented as a complex column vector.
    
    Invariants:
    - Normalised: ⟨ψ|ψ⟩ = 1 (within tolerance)
    - Dimension ≥ 1
    """
    _amplitudes: np.ndarray  # shape (d,), dtype=complex128
    
    @property
    def dimension(self) -> int:
        """Hilbert space dimension."""
        return len(self._amplitudes)
    
    @property
    def amplitudes(self) -> np.ndarray:
        """Read-only copy of the amplitude vector."""
        result = self._amplitudes.copy()
        result.flags.writeable = False
        return result
    
    def inner_product(self, other: "QuantumState") -> complex:
        """⟨self|other⟩"""
        return np.vdot(self._amplitudes, other._amplitudes)
    
    def fidelity(self, other: "QuantumState") -> float:
        """
        |⟨self|other⟩|² — overlap probability.
        
        For quantum causal states, this equals the classical fidelity
        F(P_i, P_j)² between the conditional future distributions.
        """
        return float(abs(self.inner_product(other)) ** 2)
    
    def to_density_matrix(self) -> "DensityMatrix":
        """|ψ⟩⟨ψ| — pure state density matrix."""
        rho = np.outer(self._amplitudes, np.conj(self._amplitudes))
        return DensityMatrix(rho)
    
    @classmethod
    def from_amplitudes(cls, amplitudes: Sequence[complex]) -> "QuantumState":
        """
        Create from amplitude vector. Validates normalisation.
        
        Raises:
            ValueError: If not normalised (tolerance: 1e-10)
        """
    
    @classmethod
    def computational_basis(cls, index: int, dimension: int) -> "QuantumState":
        """Create |index⟩ in the computational basis of given dimension."""
```

### Implementation Notes

- The `_amplitudes` array must be made immutable at construction time via `amplitudes.flags.writeable = False` inside `__post_init__`.
- Since frozen dataclasses don't allow `__post_init__` to assign normally, use `object.__setattr__` for the readonly-flag trick (same pattern as `Distribution`).
- Hash via `tuple(amplitudes)` — expensive but correct for small dimensions.

---

## 2. DensityMatrix

A general (possibly mixed) quantum state represented as a density matrix.

```python
@dataclass(frozen=True)
class DensityMatrix:
    """
    A density matrix ρ — Hermitian, positive semi-definite, trace 1.
    
    Invariants:
    - ρ = ρ† (Hermitian)
    - Tr(ρ) = 1
    - All eigenvalues ≥ 0
    - Shape is (d, d) for dimension d
    """
    _matrix: np.ndarray  # shape (d, d), dtype=complex128
    
    @property
    def dimension(self) -> int:
        return self._matrix.shape[0]
    
    @property
    def matrix(self) -> np.ndarray:
        """Read-only copy."""
        result = self._matrix.copy()
        result.flags.writeable = False
        return result
    
    def trace(self) -> float:
        """Tr(ρ) — should be 1.0."""
        return float(np.real(np.trace(self._matrix)))
    
    def eigenvalues(self) -> np.ndarray:
        """Eigenvalues of ρ, sorted descending. All non-negative."""
        vals = np.linalg.eigvalsh(self._matrix)
        # Clip tiny negatives from numerical noise
        vals = np.clip(vals, 0.0, None)
        return np.sort(vals)[::-1]
    
    def von_neumann_entropy(self) -> float:
        """
        S(ρ) = -Tr(ρ log₂ ρ) = -Σᵢ λᵢ log₂(λᵢ)
        
        where λᵢ are the eigenvalues of ρ.
        Convention: 0 log 0 = 0.
        """
        vals = self.eigenvalues()
        # Filter zeros to avoid log(0)
        vals = vals[vals > 0]
        return float(-np.sum(vals * np.log2(vals)))
    
    def purity(self) -> float:
        """Tr(ρ²) — 1 for pure states, 1/d for maximally mixed."""
        return float(np.real(np.trace(self._matrix @ self._matrix)))
    
    def is_pure(self, tolerance: float = 1e-10) -> bool:
        """True if Tr(ρ²) ≈ 1."""
        return abs(self.purity() - 1.0) < tolerance
    
    @classmethod
    def from_matrix(cls, matrix: np.ndarray) -> "DensityMatrix":
        """
        Create from a numpy array. Validates:
        - Hermiticity (tolerance: 1e-10)
        - Trace 1 (tolerance: 1e-10) 
        - Positive semi-definiteness (eigenvalues ≥ -1e-10)
        
        Raises:
            ValueError: If any constraint violated.
        """
    
    @classmethod
    def from_ensemble(
        cls, 
        weights: Sequence[float], 
        states: Sequence[QuantumState]
    ) -> "DensityMatrix":
        """
        ρ = Σᵢ wᵢ |ψᵢ⟩⟨ψᵢ|
        
        Note: states need NOT be orthogonal. This is essential
        for q-machine construction where quantum causal states
        are generically non-orthogonal.
        """
    
    @classmethod
    def maximally_mixed(cls, dimension: int) -> "DensityMatrix":
        """I/d — maximally mixed state."""
```

---

## 3. GramMatrix

The weighted overlap matrix used to compute quantum statistical complexity.

```python
@dataclass(frozen=True)
class GramMatrix:
    """
    Weighted Gram matrix G_ij = √(πᵢ πⱼ) ⟨σᵢ|σⱼ⟩
    
    where πᵢ are stationary weights and |σᵢ⟩ are quantum causal states.
    
    The eigenvalues of G give the spectrum of the stationary
    density matrix ρ = Σᵢ πᵢ |σᵢ⟩⟨σᵢ|, and hence:
    
        Cq = S(ρ) = H(eigenvalues of G)
    
    Properties:
    - Hermitian positive semi-definite
    - Tr(G) = 1 (since Σᵢ πᵢ = 1 and ⟨σᵢ|σᵢ⟩ = 1)
    - Rank ≤ min(k, d) where k = num states, d = Hilbert dimension
    """
    _matrix: np.ndarray  # shape (k, k), dtype=complex128
    state_ids: tuple[StateId, ...]  # ordering of rows/columns
    
    @property
    def num_states(self) -> int:
        return len(self.state_ids)
    
    @property
    def matrix(self) -> np.ndarray:
        """Read-only copy."""
        result = self._matrix.copy()
        result.flags.writeable = False
        return result
    
    def eigenvalues(self) -> np.ndarray:
        """Eigenvalues sorted descending, clipped to ≥ 0."""
        vals = np.linalg.eigvalsh(self._matrix)
        vals = np.clip(vals, 0.0, None)
        return np.sort(vals)[::-1]
    
    def quantum_statistical_complexity(self) -> float:
        """
        Cq = -Σᵢ λᵢ log₂(λᵢ)
        
        Shannon entropy of the Gram matrix eigenvalues.
        Equivalent to von Neumann entropy S(ρ) of the stationary state.
        """
        vals = self.eigenvalues()
        vals = vals[vals > 0]
        return float(-np.sum(vals * np.log2(vals)))
    
    def overlap(self, state_i: StateId, state_j: StateId) -> complex:
        """G_ij entry — weighted overlap between two quantum causal states."""
        i = self.state_ids.index(state_i)
        j = self.state_ids.index(state_j)
        return complex(self._matrix[i, j])
    
    @classmethod
    def from_quantum_states(
        cls,
        states: Mapping[StateId, QuantumState],
        weights: Distribution[StateId],
    ) -> "GramMatrix":
        """
        Construct from quantum causal states and stationary distribution.
        
        G_ij = √(πᵢ πⱼ) ⟨σᵢ|σⱼ⟩
        """
```

---

## 4. QuantumCausalState

Wraps a classical `CausalState` with its quantum representation.

```python
@dataclass(frozen=True)
class QuantumCausalState(Generic[A]):
    """
    A causal state with both classical and quantum representations.
    
    The classical part defines the transition structure (same as CausalState).
    The quantum part encodes the conditional future distribution.
    """
    classical: CausalState[A]
    quantum_state: QuantumState
    
    @property
    def id(self) -> StateId:
        return self.classical.id
    
    @property
    def transitions(self) -> frozenset:
        return self.classical.transitions
```

---

## 5. QMachine

The quantum epsilon-machine.

```python
@dataclass(frozen=True)
class QMachine(Generic[A]):
    """
    Quantum epsilon-machine — a q-machine.
    
    Contains:
    - The classical ε-machine (transition structure and stationary distribution)
    - Quantum causal states (non-orthogonal state assignments)
    - The Gram matrix (precomputed for efficiency)
    - The stationary density matrix ρ
    """
    classical_machine: EpsilonMachine[A]
    quantum_states: Mapping[StateId, QuantumCausalState[A]]
    gram_matrix: GramMatrix
    stationary_state: DensityMatrix
    
    @property
    def num_states(self) -> int:
        return len(self.classical_machine)
    
    @property
    def alphabet(self) -> frozenset[A]:
        return self.classical_machine.alphabet
    
    @property
    def state_ids(self) -> frozenset[StateId]:
        return self.classical_machine.state_ids
    
    def quantum_statistical_complexity(self) -> float:
        """Cq = S(ρ) via Gram matrix eigenvalues."""
        return self.gram_matrix.quantum_statistical_complexity()
    
    def classical_statistical_complexity(self) -> float:
        """Cμ from the underlying classical machine."""
        return self.classical_machine.stationary_distribution.entropy()
    
    def complexity_gap(self) -> float:
        """Cμ - Cq — the quantum memory advantage."""
        return self.classical_statistical_complexity() - self.quantum_statistical_complexity()
```

---

## 6. Type Relationships

```
                 EpsilonMachine[A]
                    │
                    │ (contains classical structure)
                    ▼
    ┌──────────  QMachine[A]  ──────────┐
    │               │                    │
    │  quantum_states: {StateId →        │
    │    QuantumCausalState[A]}          │
    │       │                            │
    │       ├── .classical: CausalState  │
    │       └── .quantum_state:          │
    │               QuantumState         │
    │                                    │
    │  gram_matrix: GramMatrix           │
    │  stationary_state: DensityMatrix   │
    └────────────────────────────────────┘
```

---

## 7. File Layout

```
src/emic/quantum/
├── __init__.py           # Re-exports public quantum types
├── types/
│   ├── __init__.py
│   ├── state.py          # QuantumState
│   ├── density.py        # DensityMatrix
│   ├── gram.py           # GramMatrix
│   ├── causal.py         # QuantumCausalState
│   └── machine.py        # QMachine
├── construction/         # Spec 022
├── analysis/             # Spec 023
└── decoherence/          # Spec 024
```

---

## 8. Validation Requirements

| Test | Description |
|------|-------------|
| `test_quantum_state_normalisation` | Reject unnormalised states |
| `test_density_matrix_hermiticity` | Reject non-Hermitian matrices |
| `test_density_matrix_trace` | Reject trace ≠ 1 |
| `test_density_matrix_positivity` | Reject negative eigenvalues |
| `test_von_neumann_entropy_pure` | S(|ψ⟩⟨ψ|) = 0 |
| `test_von_neumann_entropy_mixed` | S(I/d) = log₂(d) |
| `test_gram_matrix_trace` | Tr(G) = 1 |
| `test_gram_matrix_psd` | All eigenvalues ≥ 0 |
| `test_ensemble_density_matrix` | ρ = Σᵢ πᵢ |σᵢ⟩⟨σᵢ| matches from_ensemble |
| `test_cq_equals_von_neumann` | Gram eigenvalue method matches direct S(ρ) |
| `test_cq_leq_cmu` | Cq ≤ Cμ for all test machines |
| `test_orthogonal_states_cq_equals_cmu` | When all states orthogonal, Cq = Cμ |

---

## 9. Open Design Questions

1. **Truncation depth**: Quantum causal states (Eq. in paper) sum over all futures. In practice, we truncate to depth $L$. What $L$ is sufficient? → Configurable, with convergence check.

2. **Numerical tolerance**: What tolerance for normalisation, Hermiticity, trace? → 1e-10 default, configurable.

3. **Large state spaces**: For machines with many causal states, the Gram matrix is $k \times k$. For $k > 1000$, we may need sparse representations. → Defer to Spec 016 (performance).

---

*Depends on: Spec 002 (Core Types)*
*Required by: Spec 022 (q-Machine Construction), Spec 023 (Quantum Analysis)*
