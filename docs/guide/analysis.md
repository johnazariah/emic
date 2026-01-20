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

$$E = I(\overleftarrow{X}; \overrightarrow{X})$$

**Interpretation**: The total predictable information, or "complexity" of patterns.

```python
summary.excess_entropy  # In bits
```

### Crypticity (χ)

The difference between statistical complexity and excess entropy:

$$\chi = C_\mu - E$$

**Interpretation**: The "hidden" information stored in the causal states that is not directly revealed in the bi-infinite sequence.

```python
summary.crypticity  # In bits
```

### Topological Complexity

The logarithm of the number of causal states:

$$C_{top} = \log_2 |S|$$

**Interpretation**: An upper bound on statistical complexity that ignores state probabilities.

```python
summary.topological_complexity  # In bits
```

## Using the analyze Function

The `analyze` function computes all measures at once:

```python
from emic.analysis import analyze

summary = analyze(machine)

# Core measures
summary.statistical_complexity  # Cμ in bits
summary.entropy_rate           # hμ in bits/symbol
summary.excess_entropy         # E in bits
summary.crypticity             # χ in bits

# Structural measures
summary.num_states             # Number of causal states
summary.num_transitions        # Number of transitions
summary.alphabet_size          # Size of symbol alphabet
summary.topological_complexity # log₂(num_states)
```

## Individual Measure Functions

You can also compute measures individually:

```python
from emic.analysis import (
    statistical_complexity,
    entropy_rate,
    excess_entropy,
    state_count,
    transition_count,
    topological_complexity,
)

c_mu = statistical_complexity(machine)
h_mu = entropy_rate(machine)
e = excess_entropy(machine)
n_states = state_count(machine)
n_trans = transition_count(machine)
c_top = topological_complexity(machine)
```

## Analysis Summary

The `AnalysisSummary` dataclass contains all computed measures:

```python
summary = analyze(machine)

# Print human-readable summary
print(summary)
# Output:
# ε-Machine Analysis:
#   States: 2
#   Transitions: 3
#   Alphabet: 2 symbols
#   Statistical Complexity Cμ: 0.9183 bits
#   Entropy Rate hμ: 0.5500 bits/symbol
#   Excess Entropy E: 0.4591 bits
#   Crypticity χ: 0.4591 bits

# Convert to dictionary for serialization
data = summary.to_dict()
```

## Comparing Machines

Compare inferred vs theoretical machines:

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

source = GoldenMeanSource(p=0.5, _seed=42)

# Theoretical
true_summary = analyze(source.true_machine)

# Inferred
data = TakeN(10_000)(source)
result = CSSR(CSSRConfig(max_history=5)).infer(data)
inferred_summary = analyze(result.machine)

# Compare
print(f"True Cμ:     {true_summary.statistical_complexity:.4f}")
print(f"Inferred Cμ: {inferred_summary.statistical_complexity:.4f}")
print(f"Error:       {abs(true_summary.statistical_complexity - inferred_summary.statistical_complexity):.4f}")
```

## Theoretical Background

The measures computed by `emic` are central to **computational mechanics**:

- **Cμ** quantifies the *memory* required for optimal prediction
- **hμ** quantifies the *intrinsic randomness* that cannot be predicted
- **E** quantifies the *total predictable structure*
- **χ** quantifies the *hidden complexity* not visible in the data

For a deterministic process (like Periodic), hμ = 0. For an i.i.d. process (like Biased Coin), Cμ = 0.
