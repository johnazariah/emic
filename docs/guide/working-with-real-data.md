# Working with Real Data

*A practical guide for applying epsilon-machine inference to empirical sequences.*

**Prerequisites**: Familiarity with emic basics, your data in symbolic form

**Reading time**: 25-35 minutes

---

## Table of Contents

1. [The Empirical Challenge](#1-the-empirical-challenge)
2. [Preparing Your Data](#2-preparing-your-data)
3. [Alphabet Design](#3-alphabet-design)
4. [Sample Size Considerations](#4-sample-size-considerations)
5. [Choosing an Algorithm](#5-choosing-an-algorithm)
6. [Handling Noise](#6-handling-noise)
7. [Validation Strategies](#7-validation-strategies)
8. [Complete Workflow Example](#8-complete-workflow-example)
9. [Domain-Specific Tips](#9-domain-specific-tips)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. The Empirical Challenge

### 1.1 Synthetic vs Real Data

Synthetic data (like `GoldenMeanSource`) is:
- Clean, noise-free
- Exactly follows the generative model
- Infinite in principle

Real data is:
- Noisy, messy
- May not follow any simple model
- Finite (often too short)

### 1.2 What Can Go Wrong

| Problem | Symptom | Cause |
|---------|---------|-------|
| Too many states | Cμ explodes | Noise, undersampling |
| Too few states | Miss structure | Insufficient history |
| Unstable results | Changes with seed | Insufficient data |
| Non-unifilar machine | Ambiguous transitions | Algorithm failure |

### 1.3 The Goal

Transform your real-world observations into a **useful epsilon-machine** that captures the underlying structure without overfitting to noise.

---

## 2. Preparing Your Data

### 2.1 From Raw to Symbolic

emic expects data as a sequence of integers (`Sequence[int]`). Your first task is mapping raw observations to symbols.

```python
from emic.sources import SequenceData

# Option 1: Already integers
data = [0, 1, 0, 0, 1, 1, 0, 1, 0, 0]
source = SequenceData(data)

# Option 2: Categorical labels
raw = ["A", "B", "A", "A", "B", "C", "A"]
mapping = {"A": 0, "B": 1, "C": 2}
data = [mapping[x] for x in raw]
source = SequenceData(data)

# Option 3: Continuous → discretized
import numpy as np
continuous = np.random.randn(1000)
data = (continuous > 0).astype(int).tolist()  # Binary
source = SequenceData(data)
```

### 2.2 Handling Missing Values

Don't include missing values in your sequence! Options:

**Option A: Exclude (simple but breaks continuity)**
```python
raw = [1, 0, None, 1, 0, 1]
data = [x for x in raw if x is not None]
```

**Option B: Impute (introduces bias)**
```python
from statistics import mode
common = mode([x for x in raw if x is not None])
data = [common if x is None else x for x in raw]
```

**Option C: Segment (preserves structure)**
```python
# Split into contiguous segments, analyze separately
segments = []
current = []
for x in raw:
    if x is None:
        if current:
            segments.append(current)
            current = []
    else:
        current.append(x)
if current:
    segments.append(current)
```

### 2.3 Stationarity Check

Epsilon-machines assume the process is **stationary**—statistics don't change over time.

**Quick check**: Compare first half to second half:

```python
import numpy as np

data = [...]  # Your data
n = len(data)
first_half = data[:n//2]
second_half = data[n//2:]

# Compare symbol frequencies
from collections import Counter
freq1 = Counter(first_half)
freq2 = Counter(second_half)

print("First half:", dict(freq1))
print("Second half:", dict(freq2))
# These should be similar
```

**If non-stationary**: Consider segmenting data or using a sliding window.

---

## 3. Alphabet Design

### 3.1 Size Matters

| Alphabet Size | Needed Data | Notes |
|---------------|-------------|-------|
| 2 symbols | ~1,000+ | Works well |
| 4 symbols | ~5,000+ | Good balance |
| 8 symbols | ~20,000+ | Getting harder |
| 16+ symbols | 100,000+ | Often too sparse |

**Rule of thumb**: Expect to need $O(|\mathcal{A}|^{L_{\max}})$ samples where $|\mathcal{A}|$ is alphabet size and $L_{\max}$ is max history length.

### 3.2 Strategies for Continuous Data

**Threshold binning**:
```python
def threshold_bin(values, thresholds):
    """Map continuous values to discrete bins."""
    bins = [0] * len(values)
    for i, v in enumerate(values):
        for j, thresh in enumerate(thresholds):
            if v > thresh:
                bins[i] = j + 1
    return bins

# Example: Binary by median
median = np.median(values)
data = threshold_bin(values, [median])

# Example: Terciles
t1, t2 = np.percentile(values, [33, 67])
data = threshold_bin(values, [t1, t2])
```

**Symbolization methods**:
- **SAX** (Symbolic Aggregate approXimation): Popular for time series
- **Quantile binning**: Equal probability per symbol
- **Domain-specific**: Use natural categories when available

### 3.3 Choosing Number of Symbols

Start small and increase only if needed:

1. **Binary (2 symbols)**: Try this first
2. **Check results**: Does the machine capture expected structure?
3. **Increase if needed**: Add symbols if structure seems missing
4. **Stop when**: Adding symbols doesn't change Cμ/hμ meaningfully

---

## 4. Sample Size Considerations

### 4.1 How Much Data?

**Minimum requirements** (rough guidelines):

| States | Max History | Minimum N |
|--------|-------------|-----------|
| 2-3 | 3 | 1,000 |
| 3-5 | 4 | 5,000 |
| 5-10 | 5 | 20,000 |
| 10+ | 6+ | 50,000+ |

### 4.2 Diagnosing Insufficient Data

Signs you need more data:
- Cμ keeps increasing with max_history
- Many states with similar predictive distributions
- Results change significantly with different random seeds
- Many rare transitions (< 5 occurrences)

### 4.3 Convergence Check

Run inference with increasing data sizes:

```python
from emic.sources import SequenceData
from emic.inference import Spectral, SpectralConfig
from emic.analysis import analyze

data = [...]  # Your full dataset

sizes = [500, 1000, 2000, 5000, 10000, len(data)]
for n in sizes:
    if n > len(data):
        continue
    source = SequenceData(data[:n])
    result = Spectral(SpectralConfig()).infer(source.get_data())
    summary = analyze(result.machine)
    print(f"N={n:6d}: States={summary.num_states}, Cμ={summary.statistical_complexity:.3f}")
```

**Good sign**: Values stabilize as N increases.

**Bad sign**: Values keep changing significantly.

---

## 5. Choosing an Algorithm

### 5.1 Algorithm Overview

| Algorithm | Best For | Pros | Cons |
|-----------|----------|------|------|
| **Spectral** | General use | Fast, robust, no χ² | Less interpretable |
| **CSSR** | Understanding structure | Classic, well-studied | Sensitive to params |
| **CSM** | Clean data | Exact theory | Computationally expensive |
| **BSI** | Uncertainty quantification | Bayesian posteriors | Slow, complex |
| **NSD** | Manifold structure | Novel approach | Experimental |

### 5.2 Recommended Workflow

```python
from emic.inference import Spectral, SpectralConfig, CSSR, CSSRConfig

# Step 1: Quick exploration with Spectral
result1 = Spectral(SpectralConfig(num_states=None)).infer(data)  # Auto-detect
print(f"Spectral found {result1.machine.num_states} states")

# Step 2: Refine with CSSR for interpretability
config = CSSRConfig(
    max_history=5,
    significance_level=0.01,
    post_merge=True,
)
result2 = CSSR(config).infer(data)
print(f"CSSR found {result2.machine.num_states} states")

# Step 3: Compare
from emic.analysis import analyze
s1, s2 = analyze(result1.machine), analyze(result2.machine)
print(f"Spectral: Cμ={s1.statistical_complexity:.3f}, hμ={s1.entropy_rate:.3f}")
print(f"CSSR:     Cμ={s2.statistical_complexity:.3f}, hμ={s2.entropy_rate:.3f}")
```

### 5.3 When Algorithms Disagree

If Spectral and CSSR give very different results:
- **Spectral finds more states**: May be overfitting, try setting `num_states` explicitly
- **CSSR finds more states**: May need post-merging or lower significance level
- **Both unstable**: Likely insufficient data

---

## 6. Handling Noise

### 6.1 Types of Noise

**Observation noise**: Correct symbol but random errors in observation
- Example: Sensor measurement error

**Process noise**: The underlying process is itself noisy
- Example: Random events affecting transitions

**Structural noise**: Symbols occasionally swapped/corrupted
- Example: Transmission errors

### 6.2 Robustness Strategies

**Strategy 1: Higher significance level**
```python
# More conservative splitting (fewer spurious states)
config = CSSRConfig(max_history=4, significance_level=0.001)
```

**Strategy 2: Post-merging**
```python
# Merge similar states after inference
config = CSSRConfig(max_history=5, post_merge=True)
```

**Strategy 3: Spectral with fixed states**
```python
# Fix number of states based on domain knowledge
config = SpectralConfig(num_states=3)
```

**Strategy 4: Validation on held-out data**
```python
# Use subset for inference, test on rest
train_data = data[:len(data)//2]
test_data = data[len(data)//2:]
# Infer on train, evaluate on test (see validation section)
```

### 6.3 Simulating Noise Robustness

Test your pipeline's robustness:

```python
from emic.sources import SequenceData, BitFlipNoise, TakeN
from emic.inference import Spectral, SpectralConfig
from emic.analysis import analyze

original_data = [...]  # Your clean data (if you have it)

for noise_level in [0.0, 0.01, 0.02, 0.05, 0.10]:
    # Add noise
    source = SequenceData(original_data) >> BitFlipNoise(flip_prob=noise_level, seed=42)
    noisy_data = list(source)

    # Infer
    result = Spectral(SpectralConfig()).infer(noisy_data)
    summary = analyze(result.machine)

    print(f"Noise {noise_level:.0%}: States={summary.num_states}, "
          f"Cμ={summary.statistical_complexity:.3f}")
```

---

## 7. Validation Strategies

### 7.1 Log-Likelihood on Held-Out Data

The most rigorous validation: Does the inferred machine predict unseen data well?

```python
import math
from emic.types import EpsilonMachine

def compute_log_likelihood(machine: EpsilonMachine, data: list[int]) -> float:
    """Compute per-symbol log-likelihood of data under machine."""
    # Start from stationary distribution
    state_probs = dict(machine.stationary_distribution)

    log_lik = 0.0
    for symbol in data:
        # Probability of symbol given current state distribution
        p_symbol = 0.0
        new_state_probs = {}

        for state, state_prob in state_probs.items():
            for (s, sym), (next_state, trans_prob) in machine.transitions.items():
                if s == state and sym == symbol:
                    p_symbol += state_prob * trans_prob
                    new_state_probs[next_state] = new_state_probs.get(next_state, 0.0) + state_prob * trans_prob

        if p_symbol > 0:
            log_lik += math.log2(p_symbol)
            # Normalize for next step
            total = sum(new_state_probs.values())
            state_probs = {s: p/total for s, p in new_state_probs.items()}
        else:
            # Impossible transition - large penalty
            log_lik -= 100
            break

    return log_lik / len(data)  # Per-symbol

# Usage
train_data = data[:len(data)*3//4]
test_data = data[len(data)*3//4:]

result = Spectral(SpectralConfig()).infer(train_data)
ll = compute_log_likelihood(result.machine, test_data)
print(f"Test log-likelihood: {ll:.3f} bits/symbol")
```

**Interpretation**:
- Higher (less negative) is better
- Compare to entropy rate: should be close to -hμ

### 7.2 Cross-Validation

For more robust estimates:

```python
import numpy as np

def k_fold_cv(data: list[int], k: int = 5) -> list[float]:
    """K-fold cross-validation for epsilon-machine inference."""
    n = len(data)
    fold_size = n // k
    scores = []

    for i in range(k):
        test_start = i * fold_size
        test_end = (i + 1) * fold_size if i < k - 1 else n

        train_data = data[:test_start] + data[test_end:]
        test_data = data[test_start:test_end]

        result = Spectral(SpectralConfig()).infer(train_data)
        ll = compute_log_likelihood(result.machine, test_data)
        scores.append(ll)

    return scores

scores = k_fold_cv(data, k=5)
print(f"CV scores: {scores}")
print(f"Mean: {np.mean(scores):.3f} ± {np.std(scores):.3f}")
```

### 7.3 Bootstrap Stability

Check if results are stable across resamples:

```python
import random

def bootstrap_stability(data: list[int], n_bootstrap: int = 20):
    """Assess stability of inferred machine via bootstrap."""
    results = []
    n = len(data)

    for seed in range(n_bootstrap):
        random.seed(seed)
        # Resample with replacement
        resampled = [data[random.randint(0, n-1)] for _ in range(n)]

        result = Spectral(SpectralConfig()).infer(resampled)
        summary = analyze(result.machine)
        results.append({
            'states': summary.num_states,
            'c_mu': summary.statistical_complexity,
            'h_mu': summary.entropy_rate,
        })

    # Report variability
    states = [r['states'] for r in results]
    c_mus = [r['c_mu'] for r in results]

    print(f"States: {min(states)}-{max(states)}, mode={max(set(states), key=states.count)}")
    print(f"Cμ: {np.mean(c_mus):.3f} ± {np.std(c_mus):.3f}")
```

---

## 8. Complete Workflow Example

Here's a complete example analyzing DNA sequence data:

```python
"""
Example: Analyzing a DNA sequence for hidden structure.
"""
from collections import Counter
from emic.sources import SequenceData
from emic.inference import Spectral, SpectralConfig, CSSR, CSSRConfig
from emic.analysis import analyze
from emic.output import diagram

# =============================================================================
# Step 1: Load and convert data
# =============================================================================

# Simulated DNA sequence (in practice, load from FASTA file)
dna = "ATGCGATCGATCGATCGATCGATCGATCGATCGAATTCCGGAATTCCGGAATTCCGG" * 50
print(f"Sequence length: {len(dna)}")

# Map to integers
mapping = {"A": 0, "T": 1, "G": 2, "C": 3}
data = [mapping[base] for base in dna]

# =============================================================================
# Step 2: Basic statistics
# =============================================================================

counts = Counter(data)
print(f"Symbol frequencies: {dict(counts)}")
total = sum(counts.values())
print(f"Proportions: {[counts[i]/total for i in range(4)]}")

# =============================================================================
# Step 3: Initial exploration with Spectral
# =============================================================================

source = SequenceData(data)
result = Spectral(SpectralConfig(num_states=None)).infer(source.get_data())
summary = analyze(result.machine)

print(f"\nSpectral results:")
print(f"  States: {summary.num_states}")
print(f"  Cμ = {summary.statistical_complexity:.4f} bits")
print(f"  hμ = {summary.entropy_rate:.4f} bits/symbol")

# =============================================================================
# Step 4: Refine with CSSR
# =============================================================================

config = CSSRConfig(
    max_history=6,
    significance_level=0.01,
    post_merge=True,
)
result2 = CSSR(config).infer(source.get_data())
summary2 = analyze(result2.machine)

print(f"\nCSSR results:")
print(f"  States: {summary2.num_states}")
print(f"  Cμ = {summary2.statistical_complexity:.4f} bits")
print(f"  hμ = {summary2.entropy_rate:.4f} bits/symbol")

# =============================================================================
# Step 5: Validate
# =============================================================================

# Train/test split
train_data = data[:len(data)*3//4]
test_data = data[len(data)*3//4:]

result_train = Spectral(SpectralConfig()).infer(train_data)
# ... compute log-likelihood on test_data ...

# =============================================================================
# Step 6: Visualize
# =============================================================================

mermaid = diagram(result2.machine)
print(f"\nState diagram:\n{mermaid}")
```

---

## 9. Domain-Specific Tips

### 9.1 Genomic Sequences

- **Alphabet**: Use 4 symbols (A, T, G, C) or 2 (purine/pyrimidine)
- **History**: Codons suggest history length of 3 or 6
- **Stationarity**: Gene regions may differ from intergenic
- **Sample size**: Genes are short—may need to pool similar sequences

### 9.2 Financial Time Series

- **Discretization**: Returns → {down, flat, up} or finer
- **Stationarity**: Use rolling windows, regime detection
- **History**: Daily patterns suggest history 5-20
- **Noise**: High—use conservative parameters

### 9.3 Natural Language

- **Alphabet**: Characters (26-52) or word categories
- **History**: Long dependencies—may need L_max > 10
- **Size**: Need millions of characters for good estimates
- **Structure**: Rich—expect many states

### 9.4 Sensor/IoT Data

- **Discretization**: Based on operating thresholds
- **Missing values**: Common—segment carefully
- **Noise**: Often high—consider smoothing first
- **Periodicity**: Check for diurnal/weekly patterns

### 9.5 Neuroscience (Spike Trains)

- **Alphabet**: Binary (spike/no-spike) or multi-unit
- **Binning**: Careful choice of time bin width
- **Stationarity**: Task-related changes
- **Length**: Often limited—pool across trials

---

## 10. Troubleshooting

### 10.1 "Too Many States"

**Symptoms**: 10+ states, Cμ seems too high

**Causes and fixes**:
1. **Noise**: Lower significance level, use post_merge
2. **Overfitting**: Reduce max_history
3. **True complexity**: Process may genuinely be complex

```python
# Diagnostic: Check state sizes
from collections import Counter
# After CSSR: look at state occupation counts
```

### 10.2 "Too Few States"

**Symptoms**: 1-2 states when more expected

**Causes and fixes**:
1. **Insufficient history**: Increase max_history
2. **Over-merging**: Increase significance level
3. **Data issues**: Check for errors in preprocessing

### 10.3 "Unstable Results"

**Symptoms**: Different runs give different answers

**Causes and fixes**:
1. **Insufficient data**: Get more data or reduce complexity
2. **Near decision boundaries**: States may be on the edge of merging
3. **Stochastic algorithms**: Fix random seeds, average over runs

### 10.4 "Non-Unifilar Machine"

**Symptoms**: Transitions are ambiguous

**Causes and fixes**:
1. **Algorithm issue**: Try different algorithm
2. **True ambiguity**: Process may not admit a finite-state εM
3. **Numerical issues**: Check for very small probabilities

### 10.5 "Takes Too Long"

**Symptoms**: Inference doesn't complete

**Causes and fixes**:
1. **Too much data**: Subsample
2. **Large alphabet**: Reduce symbol count
3. **Long history**: Reduce max_history
4. **Wrong algorithm**: Spectral is fastest

---

## Summary Checklist

Before running epsilon-machine inference on real data:

- [ ] Data is a sequence of integers (0, 1, 2, ...)
- [ ] Missing values handled appropriately
- [ ] Stationarity checked (or data segmented)
- [ ] Alphabet size is reasonable (≤ 8 ideally)
- [ ] Sample size is adequate for expected complexity
- [ ] Algorithm chosen based on data characteristics
- [ ] Validation strategy planned (train/test, CV)

**Key parameters to tune**:
- `max_history`: Start at 5, adjust based on results
- `significance_level`: 0.01 for noisy data, 0.05 for clean
- `post_merge`: True for noisy data
- `num_states` (Spectral): Set if you have domain knowledge

**When in doubt**:
1. Start with Spectral (fast, robust)
2. Verify with CSSR (interpretable)
3. Bootstrap for stability
4. Report confidence intervals

Happy analyzing! 🔬
