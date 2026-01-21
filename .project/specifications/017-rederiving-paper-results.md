# Specification 017: Re-Deriving Paper Results

## Overview

This specification defines experiments to numerically reproduce and verify the key theoretical results from the foundational computational mechanics papers:

- **Crutchfield (1994)**: "The Calculi of Emergence"
- **Shalizi & Crutchfield (2000)**: "Computational Mechanics: Pattern and Prediction, Structure and Simplicity"

The goal is to validate both the theory and our implementation by demonstrating that `emic` correctly reproduces known analytical results.

---

## Paper Result Categories

### Category A: Complexity-Entropy Relationships

#### Experiment A.1: Complexity-Entropy Diagrams

**Paper Reference**: Calculi of Emergence, Figure 4

**Theoretical Result**: Statistical complexity Cμ is zero at both extremes (pure order and pure randomness) and maximal for intermediate processes.

**Implementation**:

```python
import numpy as np
from emic.sources.synthetic import GoldenMeanSource, BiasedCoinSource
from emic.analysis import statistical_complexity, entropy_rate

# Golden Mean: sweep p parameter
p_values = np.linspace(0.01, 0.99, 50)
results = []

for p in p_values:
    machine = GoldenMeanSource(p=p).true_machine
    results.append({
        'p': p,
        'C_mu': statistical_complexity(machine),
        'h_mu': entropy_rate(machine),
        'process': 'GoldenMean'
    })

# Biased coin: sweep bias (should have C_mu = 0 always)
for p in p_values:
    machine = BiasedCoinSource(p=p).true_machine
    results.append({
        'p': p,
        'C_mu': statistical_complexity(machine),  # Should be 0
        'h_mu': entropy_rate(machine),            # H(p)
        'process': 'BiasedCoin'
    })
```

**Expected Visualization**:
- Plot of Cμ vs hμ showing:
  - Biased coin: horizontal line at Cμ = 0
  - Golden Mean: arc shape peaking at intermediate hμ

**Verification Criteria**:
- BiasedCoin: Cμ = 0 for all p
- GoldenMean(p=0.5): Cμ ≈ 0.918 bits, hμ ≈ 0.459 bits
- Shape matches Figure 4 qualitatively

---

#### Experiment A.2: Cμ vs hμ Parametric Curves

**Paper Reference**: Shalizi & Crutchfield (2000), conceptual framework

**Goal**: Generate the full Cμ-hμ plane for multiple process families.

**Processes**:
1. **IID (Biased Coin)**: Cμ = 0, hμ = H(p) — the x-axis
2. **Golden Mean**: Parametric curve as p varies
3. **Even Process**: Different curve shape
4. **Periodic(k)**: Cμ = log₂(k), hμ = 0 — points on y-axis
5. **r-k Golden Mean**: Higher-order constraints (future implementation)

**Visualization**: Single plot with all process families overlaid.

---

### Category B: Information-Theoretic Bounds

#### Experiment B.1: Excess Entropy Bound

**Paper Reference**: Shalizi & Crutchfield (2000), Theorem 5

**Theoretical Result**: E ≤ Cμ, with equality iff H[S|→X] = 0.

**Implementation**:

```python
def excess_entropy_from_data(data: list[int], max_L: int = 20) -> float:
    """
    Estimate E = I[←X; →X] = lim_{L→∞} [H(X^L) - L·hμ]

    Using the formula: E = Σ_{L=1}^∞ [h(L) - hμ]
    where h(L) = H(X^L)/L
    """
    h_values = []
    for L in range(1, max_L + 1):
        H_L = block_entropy(data, L)
        h_values.append(H_L / L)

    # Estimate hμ as h(max_L)
    h_mu = h_values[-1]

    # E ≈ Σ [h(L) - hμ]
    E = sum(h - h_mu for h in h_values)
    return E

# Verify bound for each process
for process in [GoldenMeanSource, EvenProcessSource]:
    data = list(TakeN(100_000)(process(_seed=42)))

    E = excess_entropy_from_data(data)
    result = CSSR(config).infer(data)
    C_mu = statistical_complexity(result.machine)

    assert E <= C_mu + 0.01  # numerical tolerance
    print(f"{process}: E={E:.4f}, Cμ={C_mu:.4f}, gap={C_mu - E:.4f}")
```

**Verification Criteria**:
- E ≤ Cμ for all processes
- For renewal processes (like Golden Mean): E should be close to Cμ
- Gap size indicates "causal irreversibility"

---

#### Experiment B.2: Control Theorem Verification

**Paper Reference**: Shalizi & Crutchfield (2000), Theorem 6

**Theoretical Result**: H[S] - h[→S|R̂] ≤ Cμ (Ashby's law of requisite variety)

**Interpretation**: You need at least Cμ bits of internal state to control/predict the process.

**Implementation**: Compare prediction accuracy of models with limited state capacity.

---

### Category C: Entropy Rate Convergence

#### Experiment C.1: Block Entropy Convergence

**Paper Reference**: Both papers, fundamental property

**Theoretical Result**:
$$h_\mu = \lim_{L \to \infty} \frac{H(X^L)}{L} = \lim_{L \to \infty} H(X_L | X_1, \ldots, X_{L-1})$$

**Implementation**:

```python
def verify_entropy_convergence(machine, data, max_L=20):
    """Verify both definitions of entropy rate converge."""
    true_h = entropy_rate(machine)

    # Method 1: H(X^L) / L
    block_estimates = []
    for L in range(1, max_L + 1):
        H_L = block_entropy(data, L)
        block_estimates.append(H_L / L)

    # Method 2: H(X_L | X^{L-1})
    conditional_estimates = []
    for L in range(2, max_L + 1):
        H_L = block_entropy(data, L)
        H_L1 = block_entropy(data, L - 1)
        conditional_estimates.append(H_L - H_L1)

    return {
        'true_h': true_h,
        'block_estimates': block_estimates,
        'conditional_estimates': conditional_estimates,
    }
```

**Visualization**: Line plot showing convergence from above (block) and direct (conditional).

---

#### Experiment C.2: Entropy Rate from ε-Machine

**Paper Reference**: Shalizi & Crutchfield (2000), Theorem 4 derivation

**Theoretical Result**: hμ = Σ_s πs H[X | S=s]

**Verification**:

```python
def verify_entropy_rate_formula(machine):
    """Verify hμ = Σ πᵢ H[X|S=sᵢ]."""
    stationary = machine.stationary_distribution

    h_mu = 0.0
    for state in machine.states:
        pi_s = stationary[state.state_id]
        # Compute emission entropy H[X | S=s]
        probs = [t.probability for t in state.transitions]
        H_emission = -sum(p * log2(p) for p in probs if p > 0)
        h_mu += pi_s * H_emission

    return h_mu

# Compare with analyze() result
for process in processes:
    machine = process.true_machine
    h_formula = verify_entropy_rate_formula(machine)
    h_analyze = entropy_rate(machine)
    assert abs(h_formula - h_analyze) < 1e-10
```

---

### Category D: Causal State Properties

#### Experiment D.1: Morphs and Conditional Independence

**Paper Reference**: Shalizi & Crutchfield (2000), Definition 5, Lemma 2

**Theoretical Result**: Past and future are conditionally independent given causal state.

**Implementation**:

```python
def verify_conditional_independence(data, machine, L=5):
    """
    Verify P(→X | ←X) = P(→X | S) for causal states.

    For each inferred state, check that all histories mapping to it
    have the same future distribution (morph).
    """
    # Group histories by their causal state
    state_histories = defaultdict(list)
    for i in range(L, len(data) - L):
        history = tuple(data[i-L:i])
        future = tuple(data[i:i+L])
        state = machine.state_for_history(history)
        state_histories[state].append(future)

    # For each state, verify future distributions are consistent
    for state, futures in state_histories.items():
        # Chi-squared test for homogeneity
        pass  # Implementation details
```

---

#### Experiment D.2: Unifilarity Verification

**Paper Reference**: Shalizi & Crutchfield (2000), Lemma 5

**Theoretical Result**: ε-machines are deterministic (unifilar) — current state + symbol determines next state.

**Verification**: Already built into EpsilonMachine validation, but explicitly test:

```python
def verify_unifilarity(machine):
    """Confirm no state has two transitions with same symbol."""
    for state in machine.states:
        symbols = [t.symbol for t in state.transitions]
        assert len(symbols) == len(set(symbols)), "Not unifilar!"
```

---

### Category E: Known Process Analytics

#### Experiment E.1: Golden Mean Exact Values

**Paper Reference**: Standard example in both papers

**Analytical Results** (for p = 0.5):

| Quantity | Formula | Value |
|----------|---------|-------|
| π_A | 1/(2-p) = 2/3 | 0.6667 |
| π_B | (1-p)/(2-p) = 1/3 | 0.3333 |
| Cμ | -π_A log π_A - π_B log π_B | 0.9183 bits |
| hμ | π_A · H(p) | 0.6667 bits |
| E | (for renewal process) | ≈ Cμ |

**Verification**:

```python
machine = GoldenMeanSource(p=0.5).true_machine
summary = analyze(machine)

assert abs(summary.statistical_complexity - 0.9183) < 0.001
assert abs(summary.entropy_rate - 0.6667) < 0.001
```

---

#### Experiment E.2: Even Process Exact Values

**Analytical Results** (for p = 0.5):

| Quantity | Formula | Value |
|----------|---------|-------|
| π_A | 1/(2-p) = 2/3 | 0.6667 |
| π_B | (1-p)/(2-p) = 1/3 | 0.3333 |
| Cμ | Same formula | 0.9183 bits |
| hμ | π_A · H(p) | 0.6667 bits |

---

#### Experiment E.3: Periodic Process Values

**Analytical Results** (period k):

| Quantity | Value |
|----------|-------|
| States | k |
| Cμ | log₂(k) bits |
| hμ | 0 bits |

---

### Category F: Finite Sample Effects

#### Experiment F.1: State Count Convergence

**Paper Reference**: Implicit in all empirical studies

**Question**: How many samples are needed to correctly infer the number of states?

```python
sample_sizes = [100, 500, 1000, 5000, 10000, 50000]
true_states = 2  # Golden Mean

for n in sample_sizes:
    correct_count = 0
    for rep in range(100):
        data = list(TakeN(n)(GoldenMeanSource(_seed=rep)))
        result = CSSR(config).infer(data)
        if len(result.machine.states) == true_states:
            correct_count += 1
    print(f"n={n}: {correct_count}% correct")
```

---

#### Experiment F.2: Cμ Bias Analysis

**Question**: Is Cμ systematically over- or under-estimated at finite samples?

```python
for n in sample_sizes:
    C_mu_estimates = []
    for rep in range(100):
        result = CSSR(config).infer(process.take(n, seed=rep))
        C_mu_estimates.append(statistical_complexity(result.machine))

    bias = np.mean(C_mu_estimates) - true_C_mu
    print(f"n={n}: bias={bias:.4f}, std={np.std(C_mu_estimates):.4f}")
```

---

## Implementation Requirements

### New Functions Needed

1. `block_entropy(data, L)` — Compute H(X^L) from empirical data
2. `excess_entropy_from_data(data, max_L)` — Estimate E from data
3. `conditional_entropy_rate(data, L)` — Compute H(X_L | X^{L-1})

### New Processes to Add

1. **r-k Golden Mean** — No runs of 1s longer than k
2. **Nemo Process** — 3-state variant
3. **Simple Nondeterministic HMM** — To demonstrate cost of indeterminism

---

## Success Criteria

| Result | Paper Source | Verification |
|--------|--------------|--------------|
| Cμ = 0 for IID | Both | Exact match |
| Cμ = log₂(k) for period-k | Both | Exact match |
| E ≤ Cμ always | Theorem 5 | Numerical verification |
| hμ convergence | Both | Plot convergence |
| Golden Mean Cμ ≈ 0.918 | Standard | Within 0.01 bits |
| Unifilarity | Lemma 5 | Boolean check |

---

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Core functions | 1 week | block_entropy, excess_entropy |
| 2. Known process verification | 1 week | Exact value tests |
| 3. Theorem verification | 2 weeks | Bounds, convergence plots |
| 4. Paper figures | 1 week | Publication-ready plots |

---

## References

1. Crutchfield, J.P. (1994). The Calculi of Emergence. Physica D.
2. Shalizi, C.R. & Crutchfield, J.P. (2000). Computational Mechanics: Pattern and Prediction, Structure and Simplicity. arXiv:cond-mat/9907176.
3. Crutchfield, J.P. & Young, K. (1989). Inferring Statistical Complexity. Physical Review Letters.
