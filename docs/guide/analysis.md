# Analysis

The analysis module computes complexity measures from epsilon-machines.

## Quick Start

```python
from emic.analysis import analyze

summary = analyze(machine)
print(summary)
```

## Complexity Measures

### Statistical Complexity (Cμ)

The entropy of the stationary distribution over causal states:

$$C_\mu = -\sum_{s \in S} \pi_s \log_2 \pi_s$$

where $\pi_s$ is the stationary probability of state $s$.

**Interpretation**: The minimum information about the past needed to optimally predict the future.

```python
summary.statistical_complexity  # In bits
```

### Entropy Rate (hμ)

The conditional entropy of the next symbol given the current state:

$$h_\mu = -\sum_{s \in S} \pi_s \sum_{x \in A} P(x|s) \log_2 P(x|s)$$

**Interpretation**: The irreducible randomness per symbol.

```python
summary.entropy_rate  # In bits per symbol
```

### Excess Entropy (E)

The mutual information between the past and future:

$$E = C_\mu - h_\mu \cdot \tau$$

where $\tau$ is a characteristic timescale.

**Interpretation**: The total predictable information, or "complexity" of patterns.

```python
summary.excess_entropy  # In bits
```

## Using the Analyzer

### Direct Function

```python
from emic.analysis import analyze

summary = analyze(machine)
```

### Pipeline Component

```python
from emic.analysis import Analyzer

result = (
    source
    >> CSSR(config)
    >> Analyzer()
)

print(result.summary)
```

## Analysis Summary

The `AnalysisSummary` contains all computed measures:

```python
summary = analyze(machine)

# Core measures
summary.statistical_complexity  # Cμ in bits
summary.entropy_rate           # hμ in bits/symbol
summary.excess_entropy         # E in bits

# Machine properties
summary.num_states             # Number of causal states
summary.alphabet_size          # Size of symbol alphabet

# Stationary distribution
summary.stationary_distribution  # Dict[state_id, probability]
```

## Comparing Machines

Compare inferred vs theoretical machines:

```python
from emic.sources import GoldenMeanSource
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

source = GoldenMeanSource(p=0.5, seed=42)

# Theoretical
true_summary = analyze(source.true_machine)

# Inferred
result = CSSR(CSSRConfig(max_history=5)).infer(source.take(10_000))
inferred_summary = analyze(result.machine)

# Compare
print(f"True Cμ:     {true_summary.statistical_complexity:.4f}")
print(f"Inferred Cμ: {inferred_summary.statistical_complexity:.4f}")
print(f"Error:       {abs(true_summary.statistical_complexity - inferred_summary.statistical_complexity):.4f}")
```

## Working with Stationary Distribution

```python
summary = analyze(machine)

for state_id, prob in summary.stationary_distribution.items():
    print(f"State {state_id}: π = {prob:.4f}")
```

## Theoretical Background

The measures computed by `emic` are central to **computational mechanics**:

- **Cμ** quantifies the *memory* required for optimal prediction
- **hμ** quantifies the *intrinsic randomness* that cannot be predicted
- **E** quantifies the *total predictable structure*

For a deterministic process (like Periodic), hμ = 0. For an i.i.d. process (like Biased Coin), Cμ = 0.
