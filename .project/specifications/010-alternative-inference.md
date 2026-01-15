# Specification 010: Alternative Inference Mechanisms

## Overview

This specification defines additional epsilon-machine inference algorithms beyond CSSR, providing users with multiple approaches suited to different data characteristics and requirements.

## Motivation

CSSR has known limitations:
- Requires tuning `max_history` and `significance` parameters
- May over-estimate states with finite samples
- Assumes stationarity and unifilarity
- O(n²) complexity in history length

Alternative algorithms address these limitations and provide complementary approaches.

---

## Algorithm 1: Bayesian Structural Inference (BSI)

### Overview

Bayesian approach that infers both structure and parameters simultaneously, with natural uncertainty quantification.

### Key Features

- **Model selection via Bayesian evidence** — automatically selects number of states
- **Posterior over machines** — quantifies uncertainty in structure
- **Prior specification** — encode domain knowledge
- **No significance threshold** — avoids arbitrary p-value cutoffs

### Algorithm Outline

```
1. Define prior P(M) over machine structures
2. Define prior P(θ|M) over parameters given structure
3. Compute posterior P(M|data) ∝ P(data|M) P(M)
4. Use MCMC or variational inference to sample/approximate
5. Return MAP machine or posterior samples
```

### Configuration

```python
@dataclass(frozen=True)
class BSIConfig:
    """Configuration for Bayesian Structural Inference."""

    max_states: int = 10
    """Maximum number of states to consider."""

    alpha_prior: float = 1.0
    """Dirichlet concentration for transition priors."""

    n_samples: int = 1000
    """Number of MCMC samples."""

    burnin: int = 200
    """Burn-in samples to discard."""

    seed: int | None = None
    """Random seed for reproducibility."""
```

### Interface

```python
class BSI(InferenceAlgorithm[BSIConfig]):
    """Bayesian Structural Inference for epsilon-machines."""

    def infer(self, data: Sequence[Symbol]) -> BSIResult:
        """Infer epsilon-machine with posterior uncertainty."""
        ...

@dataclass
class BSIResult(InferenceResult):
    """Result with posterior information."""

    posterior_samples: list[EpsilonMachine]
    """Samples from the posterior over machines."""

    log_evidence: float
    """Log marginal likelihood (model evidence)."""

    state_count_posterior: dict[int, float]
    """Posterior probability over number of states."""
```

### References

- Strelioff, C.C. & Crutchfield, J.P. (2014). "Bayesian Structural Inference for Hidden Processes"

---

## Algorithm 2: Spectral Learning

### Overview

Use spectral methods (SVD/eigendecomposition) to learn observable operator representations, then extract the epsilon-machine.

### Key Features

- **Polynomial complexity** — O(n) in data length
- **Statistically consistent** — converges to true model
- **No local optima** — convex optimization
- **Handles mixed states** — generalizes beyond unifilar machines

### Algorithm Outline

```
1. Compute empirical Hankel matrix H from data
2. Perform SVD: H = U Σ V^T
3. Truncate to k singular values (model selection)
4. Extract observable operators A_x for each symbol x
5. Convert to stochastic representation
6. Extract epsilon-machine from minimal representation
```

### Configuration

```python
@dataclass(frozen=True)
class SpectralConfig:
    """Configuration for Spectral Learning."""

    max_history: int = 10
    """Maximum history length for Hankel matrix."""

    rank_threshold: float = 0.01
    """Singular value threshold for rank selection."""

    rank: int | None = None
    """Fixed rank (overrides threshold if set)."""

    regularization: float = 1e-6
    """Regularization for numerical stability."""
```

### References

- Hsu, D., Kakade, S.M., & Zhang, T. (2012). "Spectral Algorithm for Learning Hidden Markov Models"
- Boots, B., Siddiqi, S., & Gordon, G. (2011). "Closing the Learning-Planning Loop with Predictive State Representations"

---

## Algorithm 3: Causal State Merging (CSM)

### Overview

Bottom-up approach that starts with the finest partition and merges states based on predictive equivalence.

### Key Features

- **Complementary to CSSR** — merging vs splitting
- **Simpler state counting** — starts with observed distinctions
- **Good for short histories** — doesn't require long context

### Algorithm Outline

```
1. Initialize: each unique history of length L is a state
2. Compute pairwise distribution distances
3. Merge most similar pair if below threshold
4. Repeat until no more merges possible
5. Build machine from final partition
```

### Configuration

```python
@dataclass(frozen=True)
class CSMConfig:
    """Configuration for Causal State Merging."""

    history_length: int = 5
    """Fixed history length for initial partition."""

    merge_threshold: float = 0.05
    """Distance threshold for merging."""

    distance_metric: str = "kl"
    """Distance metric: 'kl', 'hellinger', 'tv', 'chi2'."""

    hierarchical: bool = False
    """If True, return full merge hierarchy."""
```

---

## Algorithm 4: Neural State Discovery (NSD)

### Overview

Use recurrent neural networks to learn state representations, then cluster hidden states to extract discrete causal states.

### Key Features

- **Data-driven features** — learns representations from data
- **Scalable** — handles very long sequences
- **Flexible** — can capture complex dependencies
- **Transfer learning** — pre-trained models for common processes

### Algorithm Outline

```
1. Train RNN/LSTM/Transformer on next-symbol prediction
2. Extract hidden state representations for each history
3. Cluster hidden states (k-means, DBSCAN, etc.)
4. Validate clusters as causal states (predictive equivalence)
5. Build machine from cluster assignments
```

### Configuration

```python
@dataclass(frozen=True)
class NSDConfig:
    """Configuration for Neural State Discovery."""

    hidden_dim: int = 64
    """Hidden state dimension."""

    n_layers: int = 2
    """Number of RNN layers."""

    architecture: str = "lstm"
    """Architecture: 'rnn', 'lstm', 'gru', 'transformer'."""

    n_clusters: int | None = None
    """Number of clusters (None = auto-select)."""

    clustering: str = "kmeans"
    """Clustering method: 'kmeans', 'dbscan', 'hdbscan'."""

    epochs: int = 100
    """Training epochs."""
```

### Dependencies

- `torch` or `tensorflow` (optional dependency)

---

## Unified Interface

All algorithms implement the same protocol:

```python
class InferenceAlgorithm(Protocol[C]):
    """Protocol for epsilon-machine inference algorithms."""

    config: C

    def infer(self, data: Sequence[Symbol]) -> InferenceResult:
        """Infer an epsilon-machine from data."""
        ...

    def __rshift__(self, other: Any) -> Any:
        """Pipeline composition."""
        ...
```

## Comparison Matrix

| Algorithm | Complexity | Uncertainty | Auto States | Assumptions |
|-----------|------------|-------------|-------------|-------------|
| CSSR | O(n·L²) | No | Via merging | Stationarity, unifilarity |
| BSI | O(n·S²·I) | Yes | Yes | Prior specification |
| Spectral | O(n·L²) | No | Via SVD | Stationarity |
| CSM | O(n·L²) | No | Via merging | Stationarity |
| NSD | O(n·H²) | No | Via clustering | None |

Where: n=data length, L=max history, S=max states, I=MCMC iterations, H=hidden dim

## Implementation Priority

1. **CSM** — Simple, complements CSSR
2. **Spectral** — Well-understood, polynomial
3. **BSI** — Principled uncertainty
4. **NSD** — Future work, requires DL stack

## Test Strategy

- All algorithms must pass golden tests on:
  - Golden Mean (2 states)
  - Even Process (2 states)
  - Biased Coin (1 state)
  - Periodic (n states)
- Cross-validate against CSSR results
- Measure computational cost
