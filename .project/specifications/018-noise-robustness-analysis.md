# Specification 018: Noise Robustness Analysis

## Overview

This specification defines experiments to analyze how epsilon-machine inference algorithms behave under various types of noise. Understanding noise robustness is critical for:

1. **Real-world applications** — Empirical data always contains noise
2. **Algorithm selection** — Different algorithms may have different noise profiles
3. **Confidence estimation** — Knowing when to trust inferred structure
4. **Theoretical insight** — Understanding the limits of inference

---

## Noise Models

### Model 1: Binary Symmetric Channel (Bit-Flip Noise)

**Description**: Each symbol is independently flipped with probability ε.

**Mathematical Model**:
$$P(\tilde{x}_t = 1 - x_t) = \epsilon$$
$$P(\tilde{x}_t = x_t) = 1 - \epsilon$$

**Implementation**:

```python
from dataclasses import dataclass
from typing import Iterator
from emic.sources.base import Source

@dataclass
class BitFlipNoise:
    """
    Binary symmetric channel noise.

    Flips each binary symbol with probability epsilon.
    """
    epsilon: float = 0.0
    _seed: int | None = None

    def __post_init__(self):
        if not (0 <= self.epsilon <= 0.5):
            raise ValueError(f"epsilon must be in [0, 0.5], got {self.epsilon}")
        self._rng = random.Random(self._seed)

    def __call__(self, source: Source[int]) -> Iterator[int]:
        """Apply noise to source output."""
        for symbol in source:
            if self._rng.random() < self.epsilon:
                yield 1 - symbol  # flip
            else:
                yield symbol
```

**Properties**:
- Preserves alphabet
- Symmetric (0→1 and 1→0 equally likely)
- At ε = 0.5, output is completely random

---

### Model 2: Erasure Channel

**Description**: Each symbol is replaced with an erasure symbol '?' with probability ε.

**Implementation**:

```python
@dataclass
class ErasureNoise:
    """
    Erasure channel noise.

    Replaces symbols with None (erasure) with probability epsilon.
    """
    epsilon: float = 0.0
    _seed: int | None = None

    def __call__(self, source: Source[int]) -> Iterator[int | None]:
        for symbol in source:
            if self._rng.random() < self.epsilon:
                yield None  # erasure
            else:
                yield symbol
```

**Challenge**: Inference must handle missing data.

---

### Model 3: Insertion Noise

**Description**: Random symbols are inserted into the stream with probability ε per position.

**Implementation**:

```python
@dataclass
class InsertionNoise:
    """
    Insertion noise.

    After each symbol, insert a random symbol with probability epsilon.
    """
    epsilon: float = 0.0
    alphabet: frozenset[int] = frozenset({0, 1})
    _seed: int | None = None

    def __call__(self, source: Source[int]) -> Iterator[int]:
        for symbol in source:
            yield symbol
            if self._rng.random() < self.epsilon:
                yield self._rng.choice(list(self.alphabet))
```

**Effect**: Breaks synchronization between observer and process.

---

### Model 4: Deletion Noise

**Description**: Each symbol is deleted with probability ε.

**Implementation**:

```python
@dataclass
class DeletionNoise:
    """
    Deletion noise.

    Each symbol is dropped with probability epsilon.
    """
    epsilon: float = 0.0
    _seed: int | None = None

    def __call__(self, source: Source[int]) -> Iterator[int]:
        for symbol in source:
            if self._rng.random() > self.epsilon:
                yield symbol
            # else: symbol is dropped
```

**Effect**: Also breaks synchronization; harder to detect than insertion.

---

### Model 5: State-Dependent Noise

**Description**: Noise rate depends on the hidden state of the generating process.

**Motivation**: More realistic — measurement quality may depend on system state.

**Implementation**:

```python
@dataclass
class NoisyGoldenMeanSource:
    """
    Golden Mean with state-dependent observation noise.

    Parameters:
        p: Transition probability (as in standard Golden Mean)
        noise_A: Bit-flip probability when in state A
        noise_B: Bit-flip probability when in state B
    """
    p: float = 0.5
    noise_A: float = 0.0
    noise_B: float = 0.0
    _seed: int | None = None

    def __iter__(self) -> Iterator[int]:
        state = "A"
        while True:
            if state == "A":
                if self._rng.random() < self.p:
                    symbol = 0
                    state = "A"
                else:
                    symbol = 1
                    state = "B"
                # Apply state-A noise
                if self._rng.random() < self.noise_A:
                    symbol = 1 - symbol
            else:  # state == "B"
                symbol = 0
                state = "A"
                # Apply state-B noise
                if self._rng.random() < self.noise_B:
                    symbol = 1 - symbol

            yield symbol
```

---

### Model 6: Burst Noise

**Description**: Noise occurs in bursts rather than independently.

**Implementation**:

```python
@dataclass
class BurstNoise:
    """
    Burst noise model.

    Parameters:
        p_enter: Probability of entering noisy state
        p_exit: Probability of exiting noisy state
        noise_rate: Flip probability while in noisy state
    """
    p_enter: float = 0.01
    p_exit: float = 0.5
    noise_rate: float = 0.3
    _seed: int | None = None

    def __call__(self, source: Source[int]) -> Iterator[int]:
        in_burst = False
        for symbol in source:
            if in_burst:
                if self._rng.random() < self.p_exit:
                    in_burst = False
                if self._rng.random() < self.noise_rate:
                    symbol = 1 - symbol
            else:
                if self._rng.random() < self.p_enter:
                    in_burst = True
            yield symbol
```

---

## Experiments

### Category 1: Bit-Flip Noise Analysis

#### Experiment 1.1: State Count vs Noise Rate

**Question**: At what noise level does inference fail to find the correct number of states?

**Design**:

```python
noise_rates = [0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
n_samples = 10_000
n_reps = 50

results = []
for epsilon in noise_rates:
    for rep in range(n_reps):
        # Generate clean data
        source = GoldenMeanSource(p=0.5, _seed=rep)
        clean_data = list(TakeN(n_samples)(source))

        # Add noise
        noisy_data = list(BitFlipNoise(epsilon, _seed=rep+1000)(clean_data))

        # Infer
        result = CSSR(config).infer(noisy_data)

        results.append({
            'epsilon': epsilon,
            'rep': rep,
            'states': len(result.machine.states),
            'C_mu': statistical_complexity(result.machine),
            'h_mu': entropy_rate(result.machine),
        })
```

**Expected Results**:
- ε = 0: Correct 2 states
- ε small: Still 2 states, slightly biased Cμ
- ε ≈ 0.1-0.2: Transition region
- ε → 0.5: 1 state (looks like IID)

**Visualization**:
- Box plot of state count vs ε
- Line plot of Cμ vs ε with true value marked

---

#### Experiment 1.2: Cμ Bias Under Noise

**Question**: Does noise cause systematic over- or under-estimation of complexity?

**Hypothesis**:
- Low noise → slight over-estimation (noise creates spurious patterns)
- High noise → under-estimation (structure washed out)

```python
for epsilon in noise_rates:
    C_mu_true = 0.9183  # Golden Mean
    C_mu_estimates = [run_inference(epsilon, rep) for rep in range(n_reps)]

    bias = np.mean(C_mu_estimates) - C_mu_true
    print(f"ε={epsilon}: bias={bias:+.4f}")
```

---

#### Experiment 1.3: Algorithm Comparison Under Noise

**Question**: Which algorithm is most robust to bit-flip noise?

```python
algorithms = {
    'CSSR': CSSR(CSSRConfig(max_history=5, significance=0.001)),
    'CSM': CSM(CSMConfig(max_history=5, significance=0.001)),
    'BSI': BSI(BSIConfig(max_states=5, n_samples=100)),
    'Spectral': Spectral(SpectralConfig(max_history=5)),
}

for epsilon in [0, 0.05, 0.1, 0.2]:
    noisy_data = add_noise(clean_data, epsilon)

    for name, alg in algorithms.items():
        result = alg.infer(noisy_data)
        record(epsilon, name, result)
```

**Metrics**:
- State count accuracy
- Cμ error
- hμ error
- Runtime

---

### Category 2: Synchronization Noise

#### Experiment 2.1: Insertion Noise Threshold

**Question**: How much insertion noise can be tolerated?

**Challenge**: Insertions break the Markov property of observation sequences.

```python
insertion_rates = [0, 0.01, 0.02, 0.05, 0.1]

for rate in insertion_rates:
    noisy_data = list(InsertionNoise(rate)(source))
    result = CSSR(config).infer(noisy_data)
    # Expect rapid degradation
```

---

#### Experiment 2.2: Deletion Noise Effects

**Question**: How does deletion noise affect inference?

**Note**: Deletion is particularly insidious because it's undetectable.

---

#### Experiment 2.3: Insertion + Deletion Combined

**Question**: What happens with both insertion and deletion?

---

### Category 3: State-Dependent Noise

#### Experiment 3.1: Asymmetric State Noise

**Question**: What happens when noise is asymmetric across states?

```python
configs = [
    {'noise_A': 0.0, 'noise_B': 0.0},   # No noise
    {'noise_A': 0.1, 'noise_B': 0.0},   # Noise only in A
    {'noise_A': 0.0, 'noise_B': 0.1},   # Noise only in B
    {'noise_A': 0.1, 'noise_B': 0.1},   # Symmetric noise
    {'noise_A': 0.2, 'noise_B': 0.05},  # Asymmetric
]

for config in configs:
    source = NoisyGoldenMeanSource(**config)
    data = list(TakeN(10_000)(source))
    result = CSSR(cssr_config).infer(data)

    # State-dependent noise might cause spurious state splitting
    print(f"Config: {config} → {len(result.machine.states)} states")
```

**Hypothesis**: Asymmetric noise may cause state splitting.

---

#### Experiment 3.2: State-Noise Interaction

**Question**: Can inference algorithms distinguish between:
1. A 2-state process with state-dependent noise
2. A genuine 3+ state process

---

### Category 4: Robustness Characterization

#### Experiment 4.1: Critical Noise Threshold

**Question**: For each process, what is the critical noise level εc where inference fails?

**Definition of "failure"**:
- Wrong number of states (mode over repetitions)
- Cμ error > 20%
- hμ error > 20%

```python
def find_critical_noise(process, algorithm, n_samples=10000, n_reps=50):
    """Binary search for critical noise level."""
    low, high = 0.0, 0.5

    while high - low > 0.01:
        mid = (low + high) / 2
        success_rate = evaluate_at_noise(process, algorithm, mid, n_samples, n_reps)

        if success_rate > 0.5:
            low = mid
        else:
            high = mid

    return mid
```

---

#### Experiment 4.2: Sample Size vs Noise Trade-off

**Question**: Can more data compensate for noise?

```python
for epsilon in [0, 0.05, 0.1, 0.2]:
    for n in [1000, 5000, 10000, 50000, 100000]:
        result = run_experiment(epsilon, n)
        record(epsilon, n, result)
```

**Visualization**: Heatmap of success rate in (ε, n) space.

---

#### Experiment 4.3: Parameter Sensitivity Under Noise

**Question**: How should algorithm parameters be adjusted for noisy data?

**Hypothesis**: Noisy data may require:
- Higher significance threshold (less aggressive splitting)
- Larger sample size
- Lower max_history (less overfitting)

```python
for epsilon in [0, 0.1]:
    for sig in [0.001, 0.01, 0.05, 0.1]:
        for L in [3, 5, 7]:
            config = CSSRConfig(max_history=L, significance=sig)
            result = CSSR(config).infer(noisy_data)
            record(epsilon, sig, L, result)
```

---

### Category 5: Noise Detection

#### Experiment 5.1: Detecting Noise Presence

**Question**: Can we detect that a sequence is noisy?

**Possible Indicators**:
- Unusually high entropy rate
- State count instability across parameters
- Transition probability irregularities

---

#### Experiment 5.2: Noise Rate Estimation

**Question**: Given a known process structure, can we estimate the noise rate?

**Approach**: Maximum likelihood estimation assuming known ε-machine + BSC noise.

---

## Implementation Plan

### Phase 1: Noise Transforms (Week 1)

Create `emic.sources.transforms.noise` module:

```python
# src/emic/sources/transforms/noise.py

from emic.sources.transforms.noise import (
    BitFlipNoise,
    ErasureNoise,
    InsertionNoise,
    DeletionNoise,
    BurstNoise,
)
```

---

### Phase 2: State-Dependent Sources (Week 1)

Create noisy variants of synthetic sources:

```python
# src/emic/sources/synthetic/noisy_golden_mean.py

@dataclass
class NoisyGoldenMeanSource(StochasticSource[int]):
    """Golden Mean with state-dependent noise."""
    p: float = 0.5
    noise_A: float = 0.0
    noise_B: float = 0.0
```

---

### Phase 3: Core Experiments (Weeks 2-3)

Run experiments 1.1 through 4.3.

---

### Phase 4: Analysis and Visualization (Week 4)

Generate publication-ready figures.

---

## Expected Deliverables

### Code

1. `emic.sources.transforms.noise` module
2. `NoisyGoldenMeanSource` and similar
3. Experiment scripts in `experiments/noise_robustness/`
4. Analysis notebooks

### Figures

1. **Figure: State Count vs Noise Rate** — Box plots for multiple processes
2. **Figure: Cμ Bias Curve** — Shows over/under-estimation pattern
3. **Figure: Algorithm Comparison** — Bar chart at fixed noise levels
4. **Figure: Critical Noise Heatmap** — (ε, n) success rate
5. **Figure: Parameter Sensitivity** — 3D surface or heatmaps

### Tables

1. **Table: Critical Noise Thresholds** — εc for each (process, algorithm) pair
2. **Table: Algorithm Ranking** — By robustness metric
3. **Table: Recommended Parameters** — For different noise regimes

---

## Theoretical Context

### Information-Theoretic Limits

**Channel Capacity**: For a BSC with flip probability ε:
$$C = 1 - H(\epsilon)$$

If the clean process has entropy rate hμ, the noisy process has:
$$h_{\text{noisy}} = h_\mu + H(\epsilon) - I(\text{noise; state})$$

### Connection to Rate-Distortion Theory

The problem of inferring structure under noise relates to rate-distortion theory:
- We want to recover the "source" (clean ε-machine)
- We observe a "noisy" version
- There's a trade-off between fidelity and complexity

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Noise transforms tested | 100% coverage |
| Critical thresholds computed | All 5 algorithms × 4 processes |
| Algorithm ranking | Clear ordering established |
| Parameter guidelines | Documented recommendations |
| Paper figures | 5 publication-ready |

---

## References

1. Cover, T.M. & Thomas, J.A. (2006). Elements of Information Theory.
2. Shalizi, C.R. (2001). Causal Architecture, Complexity and Self-Organization in Time Series and Cellular Automata. PhD Thesis.
3. Strelioff, C.C. & Crutchfield, J.P. (2014). Bayesian Structural Inference for Hidden Processes. Physical Review E.
