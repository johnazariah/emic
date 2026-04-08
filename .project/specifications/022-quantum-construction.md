# Specification 022: q-Machine Construction

## Status
📝 Planning

## Overview

This specification defines the algorithm and API for constructing a quantum epsilon-machine (q-machine) from a classical epsilon-machine. This is the core transformation that enables quantum complexity analysis.

The construction follows Gu et al. (2012): given a classical ε-machine, assign each causal state a quantum state encoding its conditional future distribution, then compute the Gram matrix and stationary density matrix.

## Dependencies

- Spec 002: Core Types (EpsilonMachine, CausalState, Distribution, StateId)
- Spec 021: Quantum Core Types (QuantumState, DensityMatrix, GramMatrix, QMachine)

---

## 1. The Construction Algorithm

### 1.1 Input

A classical `EpsilonMachine[A]` with:
- $k$ causal states $\{s_1, \ldots, s_k\}$
- Transition matrices $T^{(x)}_{ij} = P(s_j, x \mid s_i)$
- Stationary distribution $\boldsymbol{\pi}$
- Alphabet $\Sigma$

### 1.2 Step 1: Compute Conditional Future Distributions

For each causal state $s_i$, compute $P(\overrightarrow{x} \mid s_i)$ for all futures $\overrightarrow{x}$ up to a truncation depth $L$.

A future of length $L$ is a string $x_0 x_1 \cdots x_{L-1} \in \Sigma^L$.
The probability of emitting future $\overrightarrow{x} = x_0 x_1 \cdots x_{L-1}$ from state $s_i$ is:

$$P(\overrightarrow{x} \mid s_i) = \sum_{j_1, \ldots, j_{L-1}} T^{(x_0)}_{i, j_1} \cdot T^{(x_1)}_{j_1, j_2} \cdots T^{(x_{L-1})}_{j_{L-2}, j_{L-1}}$$

This is a path probability through the ε-machine.

**Implementation**: Use matrix multiplication. For each symbol $x$, the symbol-labelled transition matrix is $T^{(x)}$ with entries $T^{(x)}_{ij}$. The joint probability of future string $x_0 x_1 \cdots x_{L-1}$ starting from state $s_i$ is:

$$P(\overrightarrow{x} \mid s_i) = \left( T^{(x_0)} \cdot T^{(x_1)} \cdots T^{(x_{L-1})} \right)_{i, \cdot} \cdot \mathbf{1}$$

where $\mathbf{1}$ is the all-ones vector (sum over terminal states).

```python
def compute_future_distributions(
    machine: EpsilonMachine[A],
    depth: int,
) -> dict[StateId, dict[tuple[A, ...], float]]:
    """
    Compute P(future | state) for all states and all futures up to length depth.
    
    Args:
        machine: The classical ε-machine
        depth: Truncation depth L for future strings
    
    Returns:
        Mapping from state_id to {future_string: probability}.
        future_string is a tuple of symbols of length depth.
        
    Note:
        Probabilities may not sum to 1 if the machine has absorbing states.
        For ergodic machines, they sum to 1 for each state.
    """
```

### 1.3 Step 2: Construct Quantum Causal States

For each causal state $s_i$, construct the quantum state:

$$|\sigma_i\rangle = \sum_{\overrightarrow{x} \in \Sigma^L} \sqrt{P(\overrightarrow{x} \mid s_i)} \; |\overrightarrow{x}\rangle$$

The Hilbert space dimension is $|\Sigma|^L$ (exponential in depth). Each future string $\overrightarrow{x}$ maps to a computational basis vector $|\overrightarrow{x}\rangle$.

```python
def construct_quantum_causal_state(
    state_id: StateId,
    future_distribution: dict[tuple[A, ...], float],
    basis_ordering: Sequence[tuple[A, ...]],
) -> QuantumState:
    """
    Construct |σᵢ⟩ = Σ √P(x⃗|sᵢ) |x⃗⟩
    
    Args:
        state_id: The causal state identifier
        future_distribution: P(future | state) for each future string
        basis_ordering: Ordering of basis vectors (consistent for all states)
    
    Returns:
        QuantumState with amplitudes √P for each basis vector
    """
```

### 1.4 Step 3: Compute Gram Matrix

$$G_{ij} = \sqrt{\pi_i \pi_j} \; \langle\sigma_i|\sigma_j\rangle$$

```python
def compute_gram_matrix(
    quantum_states: Mapping[StateId, QuantumState],
    stationary_distribution: Distribution[StateId],
) -> GramMatrix:
    """
    Compute the weighted Gram matrix.
    
    G_ij = √(πᵢ πⱼ) ⟨σᵢ|σⱼ⟩
    
    The inner product ⟨σᵢ|σⱼ⟩ equals the Bhattacharyya coefficient
    (classical fidelity) between the future distributions:
    
        ⟨σᵢ|σⱼ⟩ = Σ_x⃗ √(P(x⃗|sᵢ) P(x⃗|sⱼ))
    """
```

### 1.5 Step 4: Compute Stationary Density Matrix

$$\rho = \sum_i \pi_i \; |\sigma_i\rangle\langle\sigma_i|$$

```python
def compute_stationary_state(
    quantum_states: Mapping[StateId, QuantumState],
    stationary_distribution: Distribution[StateId],
) -> DensityMatrix:
    """
    ρ = Σᵢ πᵢ |σᵢ⟩⟨σᵢ|
    
    Note: states are NOT orthogonal in general, so this is not
    a spectral decomposition.
    """
```

### 1.6 Step 5: Assemble the QMachine

```python
def construct_qmachine(
    machine: EpsilonMachine[A],
    depth: int = 10,
    tolerance: float = 1e-10,
) -> QMachine[A]:
    """
    Full pipeline: classical ε-machine → q-machine.
    
    Args:
        machine: The classical epsilon-machine
        depth: Truncation depth for future distributions (default: 10)
        tolerance: Numerical tolerance for validation (default: 1e-10)
    
    Returns:
        QMachine with quantum causal states, Gram matrix, and stationary state
    
    Raises:
        ValueError: If machine is not unifilar or has no states
    """
```

---

## 2. The Convergence Problem

Quantum causal states require summing over **all** futures, but we truncate to depth $L$. The truncation introduces error.

### 2.1 Convergence Criterion

The Gram matrix entries converge as $L \to \infty$ because later terms contribute exponentially less (for ergodic processes). We monitor convergence by computing:

$$\Delta G(L) = \| G^{(L)} - G^{(L-1)} \|_F$$

where $\|\cdot\|_F$ is the Frobenius norm. Stop when $\Delta G < \epsilon$.

```python
@dataclass(frozen=True)
class QMachineConfig:
    """Configuration for q-machine construction."""
    
    min_depth: int = 5
    """Minimum truncation depth."""
    
    max_depth: int = 50
    """Maximum truncation depth."""
    
    convergence_tolerance: float = 1e-8
    """Stop when Gram matrix Frobenius norm change < this."""
    
    numerical_tolerance: float = 1e-10
    """Tolerance for validation checks (normalisation, Hermiticity)."""
```

### 2.2 Adaptive Depth

Rather than fixing $L$, increase depth until convergence:

```python
def construct_qmachine_adaptive(
    machine: EpsilonMachine[A],
    config: QMachineConfig = QMachineConfig(),
) -> QMachine[A]:
    """
    Construct q-machine with adaptive depth selection.
    
    Increases depth from min_depth until the Gram matrix converges
    or max_depth is reached.
    
    Returns:
        QMachine with metadata about convergence depth
    """
```

---

## 3. Computational Complexity

| Step | Time | Space |
|------|------|-------|
| Future distributions | $O(k \cdot |\Sigma|^L \cdot k)$ | $O(k \cdot |\Sigma|^L)$ |
| Quantum states | $O(k \cdot |\Sigma|^L)$ | $O(k \cdot |\Sigma|^L)$ |
| Gram matrix | $O(k^2 \cdot |\Sigma|^L)$ | $O(k^2)$ |
| Density matrix | $O(k \cdot |\Sigma|^{2L})$ | $O(|\Sigma|^{2L})$ |

The exponential scaling in $L$ is unavoidable in the exact construction. For practical use:
- Binary alphabet ($|\Sigma| = 2$): $L = 20$ gives $\sim 10^6$ dimensions — feasible
- Ternary ($|\Sigma| = 3$): $L = 12$ gives $\sim 5 \times 10^5$ — feasible
- Larger alphabets: $L$ must be small, or use Gram matrix shortcut (avoid constructing full density matrix)

**Key optimisation**: Computing $C_q$ only requires the $k \times k$ Gram matrix eigenvalues, NOT the full $|\Sigma|^L$-dimensional density matrix. Always prefer the Gram matrix route.

---

## 4. Pipeline Integration

The construction integrates with emic's pipeline via `>>`:

```python
# Direct construction
qm = construct_qmachine(machine, depth=15)

# Pipeline style  
result = (
    GoldenMeanSource(p=0.5)
    >> TakeN(100_000)
    >> SpectralInference(SpectralConfig())
    >> construct_qmachine
)

# With config
config = QMachineConfig(min_depth=5, max_depth=30)
qm = machine >> partial(construct_qmachine_adaptive, config=config)
```

To support this, `construct_qmachine` must accept an `EpsilonMachine` as first argument and return a `QMachine`. For the adaptive variant, use `functools.partial` for config binding.

---

## 5. Built-in Process Validation Targets

Each built-in process has known analytic (or high-precision numerical) values for $C_q$:

| Process | $k$ | $C_\mu$ | $E$ | $\chi$ | $C_q$ (expected) | Source |
|---------|-----|---------|-----|---------|-------------------|--------|
| Biased Coin ($p$) | 1 | 0 | 0 | 0 | 0 | Trivial |
| Golden Mean ($p=0.5$) | 2 | 0.918 | 0.811 | 0.107 | TBD (compute) | Gu 2012 |
| Even Process ($p=0.5$) | 2 | 1.0 | 0.811 | 0.189 | TBD (compute) | Gu 2012 |
| Periodic(3) | 3 | 1.585 | 1.585 | 0 | 1.585 | Trivial ($\chi=0$) |

**Note**: Periodic processes have $\chi = 0$, so $C_q = C_\mu = E$ — no quantum advantage. This is a useful sanity check.

---

## 6. Validation Requirements

| Test | Description |
|------|-------------|
| `test_biased_coin_no_advantage` | $C_q = C_\mu = 0$ for single-state machine |
| `test_periodic_no_advantage` | $C_q = C_\mu$ when $\chi = 0$ |
| `test_golden_mean_strict_advantage` | $C_q < C_\mu$ for Golden Mean |
| `test_even_process_strict_advantage` | $C_q < C_\mu$ for Even Process |
| `test_cq_geq_E` | $C_q \geq E$ for all test processes |
| `test_cq_leq_cmu` | $C_q \leq C_\mu$ for all test processes |
| `test_gram_matrix_trace_one` | $\mathrm{Tr}(G) = 1$ |
| `test_convergence_with_depth` | $C_q(L)$ converges as $L$ increases |
| `test_future_probs_sum_to_one` | $\sum_{\overrightarrow{x}} P(\overrightarrow{x} \mid s_i) = 1$ for each state |
| `test_orthogonal_states_give_cmu` | If all futures disjoint, $C_q = C_\mu$ |
| `test_pipeline_integration` | `machine >> construct_qmachine` works |

---

## 7. File Layout

```
src/emic/quantum/construction/
├── __init__.py
├── config.py              # QMachineConfig
├── futures.py             # compute_future_distributions
├── states.py              # construct_quantum_causal_state
├── gram.py                # compute_gram_matrix
├── builder.py             # construct_qmachine, construct_qmachine_adaptive
└── pipeline.py            # Pipeline integration (__rshift__ support)
```

---

*Depends on: Spec 002, Spec 021*
*Required by: Spec 023 (Quantum Analysis), Spec 024 (Decoherence)*
