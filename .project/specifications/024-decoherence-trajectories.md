# Specification 024: Decoherence Trajectories

## Status
📝 Planning

## Overview

This specification defines the framework for studying how quantum statistical complexity $C_q(\gamma)$ evolves under decoherence, interpolating between the fully quantum model ($\gamma = 0$) and the fully classical model ($\gamma = 1$). This addresses **RQ2** from the research programme.

## Dependencies

- Spec 021: Quantum Core Types (DensityMatrix, GramMatrix)
- Spec 022: q-Machine Construction (QMachine)
- Spec 023: Quantum Analysis (quantum measures)

---

## 1. Decoherence Models

### 1.1 The General Framework

A decoherence channel $\mathcal{D}_\gamma$ is a completely positive trace-preserving (CPTP) map parameterised by $\gamma \in [0, 1]$:
- $\gamma = 0$: Identity channel (no decoherence)
- $\gamma = 1$: Full decoherence (classical limit)

The decoherence acts on the quantum causal states. Given quantum causal states $\{|\sigma_i\rangle\}$, the decohered Gram matrix is:

$$G_{ij}(\gamma) = \sqrt{\pi_i \pi_j} \; \mathrm{Tr}\!\left[\mathcal{D}_\gamma(|\sigma_i\rangle\langle\sigma_j|)\right]$$

### 1.2 Protocol

```python
class DecoherenceModel(Protocol):
    """A parameterised decoherence channel."""
    
    @property
    def name(self) -> str:
        """Human-readable name (e.g. 'depolarising', 'dephasing')."""
        ...
    
    def apply(
        self, 
        rho: DensityMatrix, 
        gamma: float,
    ) -> DensityMatrix:
        """
        Apply decoherence channel D_γ to density matrix ρ.
        
        Args:
            rho: Input density matrix
            gamma: Decoherence parameter in [0, 1]
        
        Returns:
            D_γ(ρ) — decohered density matrix
        """
        ...
    
    def apply_to_gram(
        self,
        gram: GramMatrix,
        quantum_states: Mapping[StateId, QuantumState],
        gamma: float,
    ) -> GramMatrix:
        """
        Compute the decohered Gram matrix.
        
        More efficient than applying to each pair of states individually
        for some channel types.
        """
        ...
```

### 1.3 Built-in Channels

#### Depolarising Channel

$$\mathcal{D}_\gamma^{\text{depol}}(\rho) = (1 - \gamma)\rho + \gamma \frac{I}{d}$$

Mixes the state with the maximally mixed state. The simplest decoherence model.

**Effect on Gram matrix**: Off-diagonal elements scale as $(1-\gamma)$:
$$G_{ij}(\gamma) = (1 - \gamma) G_{ij} + \gamma \cdot \delta_{ij} \sqrt{\pi_i \pi_j}$$

Wait — more precisely, the depolarising channel doesn't factor so simply on the off-diagonal Gram elements. Direct computation via:

```python
@dataclass(frozen=True)
class DepolarizingChannel:
    """
    D_γ(ρ) = (1-γ)ρ + γ I/d
    
    At γ=1: all states become I/d (maximally mixed, classical limit).
    """
    
    def apply(self, rho: DensityMatrix, gamma: float) -> DensityMatrix:
        d = rho.dimension
        mixed = np.eye(d) / d
        result = (1 - gamma) * rho.matrix + gamma * mixed
        return DensityMatrix.from_matrix(result)
    
    def apply_to_gram(
        self,
        gram: GramMatrix,
        quantum_states: Mapping[StateId, QuantumState],
        gamma: float,
    ) -> GramMatrix:
        """
        For depolarising: recompute Gram from decohered states.
        
        Note: Depolarising on individual states ≠ depolarising on ρ.
        We apply decoherence to the stationary state ρ directly.
        """
```

#### Dephasing Channel

$$\mathcal{D}_\gamma^{\text{dephase}}(\rho) = (1 - \gamma)\rho + \gamma \sum_k |k\rangle\langle k| \rho |k\rangle\langle k|$$

Destroys off-diagonal coherences in the computational basis while preserving diagonal elements (populations).

**Effect on Gram matrix**: Off-diagonal elements of $\rho$ are damped by $(1-\gamma)$, which corresponds to reducing the inner products $\langle\sigma_i|\sigma_j\rangle$ for $i \neq j$.

```python
@dataclass(frozen=True)
class DephasingChannel:
    """
    Dephasing in the computational basis.
    Kills off-diagonal elements of ρ at rate γ.
    
    At γ=1: ρ becomes diagonal — equivalent to classical state.
    """
```

#### Amplitude Damping Channel

$$\mathcal{D}_\gamma^{\text{amp}}(\rho) = E_0 \rho E_0^\dagger + E_1 \rho E_1^\dagger$$

where $E_0 = |0\rangle\langle 0| + \sqrt{1-\gamma}|1\rangle\langle 1|$ and $E_1 = \sqrt{\gamma}|0\rangle\langle 1|$.

This models energy relaxation (decay to ground state). Only well-defined for qubit systems — extend via tensor product for higher dimensions.

```python
@dataclass(frozen=True)  
class AmplitudeDampingChannel:
    """
    Amplitude damping (energy relaxation).
    
    Note: Only defined for qubit-encoded states.
    For higher dimensions, uses tensor product of qubit channels.
    """
```

---

## 2. Trajectory Computation

### 2.1 Single Trajectory

```python
@dataclass(frozen=True)
class DecoherenceTrajectory:
    """
    Cq(γ) trajectory for a single process under a single decoherence model.
    """
    process_name: str
    channel_name: str
    gamma_values: tuple[float, ...]   # γ grid points
    cq_values: tuple[float, ...]      # Cq at each γ
    cmu: float                        # Classical Cμ (constant)
    excess_entropy: float             # E (constant)
    
    @property
    def num_points(self) -> int:
        return len(self.gamma_values)
    
    def cq_at(self, gamma: float) -> float:
        """Interpolated Cq at arbitrary γ (linear interpolation)."""
    
    @property
    def critical_gamma(self) -> float | None:
        """
        γ* at which Cq crosses some threshold (e.g., midpoint of gap).
        Returns None if no clear critical point.
        """
    
    @property
    def is_monotone(self) -> bool:
        """True if Cq(γ) is monotonically non-decreasing."""


def compute_decoherence_trajectory(
    qmachine: QMachine[A],
    channel: DecoherenceModel,
    gamma_values: Sequence[float] | None = None,
    num_points: int = 101,
) -> DecoherenceTrajectory:
    """
    Map Cq(γ) for a q-machine under a decoherence channel.
    
    Args:
        qmachine: The quantum epsilon-machine
        channel: The decoherence model
        gamma_values: Explicit γ grid (default: uniform 0 to 1)
        num_points: Number of grid points if gamma_values not given
    
    Returns:
        DecoherenceTrajectory with Cq at each γ
    
    Expected behaviour:
        Cq(0) = quantum Cq (no decoherence)
        Cq(1) = Cμ (fully classical)
        Cq(γ) is monotonically non-decreasing (conjecture — verify!)
    """
```

### 2.2 Multi-Channel Comparison

```python
@dataclass(frozen=True)
class MultiChannelTrajectory:
    """Cq(γ) trajectories under multiple decoherence channels."""
    
    process_name: str
    trajectories: Mapping[str, DecoherenceTrajectory]  # channel_name → trajectory
    
    def channels(self) -> tuple[str, ...]:
        return tuple(self.trajectories.keys())


def compute_multi_channel_trajectories(
    qmachine: QMachine[A],
    channels: Sequence[DecoherenceModel] | None = None,
    num_points: int = 101,
) -> MultiChannelTrajectory:
    """
    Compute Cq(γ) under all provided channels (default: all built-in).
    """
```

---

## 3. Analysis Questions

The trajectory analysis should help answer:

1. **Monotonicity**: Is $C_q(\gamma)$ always non-decreasing? (Conjecture: yes for depolarising)
2. **Smoothness**: Is the trajectory $C^\infty$, or are there kinks/cusps?
3. **Channel dependence**: Does the trajectory shape depend on the channel type?
4. **Critical points**: Are there values of $\gamma$ where $dC_q/d\gamma$ changes qualitatively?
5. **Process dependence**: Do processes with higher crypticity show steeper trajectories?

```python
@dataclass(frozen=True)
class TrajectoryFeatures:
    """Extracted features of a decoherence trajectory."""
    
    is_monotone: bool
    max_derivative: float              # max |dCq/dγ|
    gamma_at_max_derivative: float     # where the steepest change occurs
    gamma_at_half_gap: float           # γ where Cq = (Cq(0) + Cμ) / 2
    smoothness_violations: int         # number of non-monotone steps (0 if monotone)
    total_gap: float                   # Cμ - Cq(0) = classical advantage

def extract_trajectory_features(
    trajectory: DecoherenceTrajectory,
) -> TrajectoryFeatures:
    """Extract quantitative features from a trajectory for analysis."""
```

---

## 4. Output Formats

### 4.1 Plot Data Export

```python
def trajectory_to_csv(trajectory: DecoherenceTrajectory, path: Path) -> None:
    """
    CSV with columns: gamma, cq, cmu, E
    For direct import into matplotlib, pgfplots, or gnuplot.
    """

def trajectory_to_pgfplot(trajectory: DecoherenceTrajectory) -> str:
    """
    LaTeX pgfplots data block for embedding in papers:
    
    \\addplot table {
      gamma  cq
      0.00   0.834
      0.01   0.835
      ...
    };
    """
```

### 4.2 Summary Table

```python
def trajectory_summary_to_latex(
    trajectories: Sequence[DecoherenceTrajectory],
) -> str:
    """
    LaTeX table comparing trajectories across processes/channels:
    
    Process     Channel        Cq(0)  Cμ     ΔC    γ*
    Golden Mean Depolarising   0.834  0.918  0.084  0.43
    Golden Mean Dephasing      0.834  0.918  0.084  0.51
    Even Proc.  Depolarising   0.872  1.000  0.128  0.38
    """
```

---

## 5. Validation Requirements

| Test | Description |
|------|-------------|
| `test_depolarising_identity_at_zero` | $\mathcal{D}_0(\rho) = \rho$ |
| `test_depolarising_mixed_at_one` | $\mathcal{D}_1(\rho) = I/d$ |
| `test_dephasing_identity_at_zero` | $\mathcal{D}_0(\rho) = \rho$ |
| `test_dephasing_diagonal_at_one` | $\mathcal{D}_1(\rho)$ is diagonal |
| `test_channel_preserves_trace` | $\mathrm{Tr}[\mathcal{D}_\gamma(\rho)] = 1$ for all $\gamma$ |
| `test_channel_preserves_positivity` | $\mathcal{D}_\gamma(\rho)$ is PSD for all $\gamma$ |
| `test_trajectory_endpoints` | $C_q(0) = C_q$, $C_q(1) \approx C_\mu$ |
| `test_trajectory_bounds` | $E \leq C_q(\gamma) \leq C_\mu$ for all $\gamma$ |
| `test_trivial_process_flat` | Biased coin: $C_q(\gamma) = 0$ for all $\gamma$ |
| `test_no_advantage_flat` | Periodic: $C_q(\gamma) = C_\mu$ for all $\gamma$ |
| `test_trajectory_features` | Feature extraction produces sensible values |

---

## 6. File Layout

```
src/emic/quantum/decoherence/
├── __init__.py
├── protocol.py            # DecoherenceModel protocol
├── channels.py            # DepolarizingChannel, DephasingChannel, AmplitudeDampingChannel
├── trajectory.py          # DecoherenceTrajectory, compute_decoherence_trajectory
├── multi_channel.py       # MultiChannelTrajectory
├── features.py            # TrajectoryFeatures, extract_trajectory_features
└── output.py              # CSV, LaTeX export
```

---

## 7. Experimental Programme

This spec directly supports the following experiments (connect to `emic-research/research/experiments/`):

| Experiment | Process | Channels | Grid | Deliverable |
|------------|---------|----------|------|-------------|
| EXP-Q01 | Golden Mean ($p \in [0.1, 0.9]$) | All 3 | 101 pts | Trajectory plots |
| EXP-Q02 | Even Process ($p \in [0.1, 0.9]$) | All 3 | 101 pts | Trajectory plots |
| EXP-Q03 | Perturbed Coin ($\epsilon \in [0.01, 0.5]$) | Depolarising | 101 pts | Unbounded advantage under decoherence |
| EXP-Q04 | All built-in processes | Depolarising | 101 pts | Feature comparison table |
| EXP-Q05 | Asymmetric processes | Depolarising | 101 pts | Bidirectional trajectories |

---

*Depends on: Spec 021, Spec 022, Spec 023*
*Required by: Research experiments EXP-Q01 through EXP-Q05*
