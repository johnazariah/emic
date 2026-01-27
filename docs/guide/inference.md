# Inference

The `emic` framework provides multiple algorithms for inferring epsilon-machines from data. Each algorithm has different strengths and trade-offs.

## Available Algorithms

| Algorithm | Approach | Correctness* | Best For |
|-----------|----------|--------------|----------|
| **Spectral** | Matrix decomposition | **98%** | General purpose, best accuracy |
| **CSSR** | Top-down splitting | 80% | Well-studied reference, lowest Cμ error |
| **NSD** | Clustering | 75% | Fast exploratory analysis |
| **CSM** | Bottom-up merging | 45% | Complement to CSSR |
| **BSI** | Bayesian inference | 25% | Uncertainty quantification |

*Correctness measured at sample sizes N ≥ 1,000 on canonical test processes. At N ≥ 10,000, Spectral achieves 100% and CSSR achieves 75%.

## CSSR (Causal State Splitting Reconstruction)

CSSR is the primary algorithm, based on Shalizi & Crutchfield (2001).

### How it Works

1. Build a suffix tree from observed sequences
2. Initialize each unique history as a potential causal state
3. Iteratively split states with statistically different futures
4. Merge states with statistically indistinguishable futures

### Basic Usage

```python
from emic.inference import CSSR, CSSRConfig

config = CSSRConfig(
    max_history=5,
    significance=0.001,
)

result = CSSR(config).infer(data)
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_history` | 5 | Maximum history length (L) to consider |
| `significance` | 0.001 | Chi-squared test significance level (α) |
| `min_count` | 1 | Minimum observations per history |
| `post_merge` | True | Enable post-convergence merging |
| `merge_significance` | None | Significance for post-merge (uses `significance` if None) |

```python
config = CSSRConfig(
    max_history=6,
    significance=0.01,
    min_count=5,
    post_merge=True,
)
```

### Reference

Shalizi, C.R. & Klinkner, K.L. (2004). "Blind Construction of Optimal Nonlinear Recursive Predictors for Discrete Sequences". *AUAI*.

---

## CSM (Causal State Merging)

CSM is a bottom-up approach that complements CSSR.

### How it Works

1. Create a state for each unique history of specified length
2. Compute pairwise distances between state predictive distributions
3. Iteratively merge the closest pair until threshold is exceeded

### Basic Usage

```python
from emic.inference import CSM, CSMConfig

config = CSMConfig(
    history_length=5,
    merge_threshold=0.05,
)

result = CSM(config).infer(data)
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `history_length` | 5 | Fixed history length for initial states |
| `merge_threshold` | 0.05 | Distance threshold for merging |
| `distance_metric` | "kl" | Metric: "kl", "hellinger", "tv", "chi2" |
| `min_count` | 5 | Minimum observations per history |
| `hierarchical` | False | Return full merge hierarchy |

```python
config = CSMConfig(
    history_length=6,
    merge_threshold=0.1,
    distance_metric="hellinger",
)
```

---

## BSI (Bayesian Structural Inference)

BSI uses Bayesian inference with MCMC sampling for uncertainty quantification.

### How it Works

1. Place Dirichlet priors on transition probabilities
2. Use Gibbs sampling to explore posterior over state assignments
3. Select model with highest marginal likelihood

### Basic Usage

```python
from emic.inference import BSI, BSIConfig

config = BSIConfig(
    max_states=5,
    n_samples=1000,
)

result = BSI(config).infer(data)
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_states` | 10 | Maximum number of states |
| `max_history` | 5 | History length for likelihood |
| `alpha_prior` | 1.0 | Dirichlet concentration (higher = more uniform) |
| `n_samples` | 1000 | Number of MCMC samples |
| `burnin` | 200 | Burn-in samples to discard |
| `seed` | None | Random seed |

```python
config = BSIConfig(
    max_states=8,
    n_samples=2000,
    alpha_prior=0.5,  # Sparse prior
)
```

### Reference

Strelioff, C.C. & Crutchfield, J.P. (2014). "Bayesian Structural Inference for Hidden Processes".

---

## Spectral Learning

Spectral methods use SVD of Hankel matrices for polynomial-time inference. After recent improvements (adaptive parameters, belief state clustering), Spectral achieves the highest correctness of all algorithms.

### How it Works

1. Build Hankel matrices from history/future statistics
2. Compute SVD to find observable operator representation
3. Apply belief state clustering to discretize continuous states
4. Extract epsilon-machine from learned operators

For a complete explanation, see the [Spectral Learning Deep Dive](spectral-learning-deep-dive.md).

### Basic Usage

```python
from emic.inference import Spectral, SpectralConfig

# Default: adaptive parameters (recommended)
result = Spectral(SpectralConfig()).infer(data)

# Or with explicit settings
config = SpectralConfig(
    max_history=5,
    rank_threshold=0.01,
)
result = Spectral(config).infer(data)
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_history` | None (adaptive) | History length for Hankel matrix. Auto-computed as `min(8, 2 + log₂(N/100))` |
| `rank_threshold` | 0.001 | Relative singular value cutoff for rank selection |
| `rank` | None | Fixed rank (overrides threshold) |
| `regularization` | 1e-6 | Numerical stability |
| `min_count` | None (adaptive) | Min observations per history. Auto-computed as `max(3, N/10000)` |

```python
# Adaptive defaults work well for most cases
config = SpectralConfig()

# Force exactly 3 states
config = SpectralConfig(rank=3)

# More aggressive filtering for noisy data
config = SpectralConfig(rank_threshold=0.1)
```

### Reference

Hsu, D., Kakade, S.M., & Zhang, T. (2012). "Spectral Algorithm for Learning Hidden Markov Models".

---

## NSD (Neural State Discovery)

NSD uses embedding and clustering for state discovery.

### How it Works

1. Embed histories into a vector space based on next-symbol distributions
2. Cluster embeddings using k-means
3. Build machine from cluster assignments

### Basic Usage

```python
from emic.inference import NSD, NSDConfig

config = NSDConfig(
    max_states=5,
    history_length=10,
)

result = NSD(config).infer(data)
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_states` | 10 | Maximum number of states |
| `history_length` | 10 | History window length |
| `embedding_dim` | 16 | Embedding dimensionality |
| `n_iterations` | 100 | Clustering iterations |
| `seed` | None | Random seed |

---

## Inference Result

All algorithms return an `InferenceResult`:

```python
result = CSSR(config).infer(data)

# The inferred machine
machine = result.machine
print(f"States: {len(machine.states)}")

# Convergence status
print(f"Converged: {result.converged}")
print(f"Iterations: {result.iterations}")
```

## Choosing an Algorithm

| Scenario | Recommended Algorithm |
|----------|----------------------|
| General use | Spectral (highest accuracy) |
| Well-studied reference | CSSR |
| Need uncertainty | BSI |
| CSSR gives too many states | CSM or post_merge=True |
| Exploratory analysis | NSD |

## Troubleshooting

### Too Many States

1. **Increase data**: More samples reduce finite-sample effects
2. **Lower significance**: Use `significance=0.01` or `0.05` (CSSR)
3. **Raise merge threshold**: Use higher `merge_threshold` (CSM)
4. **Enable post-merge**: `post_merge=True` (CSSR)

### Too Few States

1. **Increase `max_history`**: May not capture full structure
2. **Raise significance**: Use `significance=0.001` (CSSR)
3. **Lower merge threshold**: Use smaller `merge_threshold` (CSM)

### Algorithm Comparison

Run multiple algorithms and compare:

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSM, CSSRConfig, CSMConfig
from emic.analysis import analyze

source = GoldenMeanSource(p=0.5, _seed=42)
data = TakeN(10_000)(source)

# CSSR
cssr_result = CSSR(CSSRConfig(max_history=5)).infer(data)
cssr_summary = analyze(cssr_result.machine)

# CSM
csm_result = CSM(CSMConfig(history_length=5)).infer(data)
csm_summary = analyze(csm_result.machine)

print(f"CSSR: {cssr_summary.num_states} states, Cμ={cssr_summary.statistical_complexity:.4f}")
print(f"CSM:  {csm_summary.num_states} states, Cμ={csm_summary.statistical_complexity:.4f}")
```
