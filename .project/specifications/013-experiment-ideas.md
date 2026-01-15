# Specification 013: Experiment Ideas Catalog

## Overview

A prioritized catalog of experiments, organized by effort and scientific value.

---

## Quick Wins (1-2 days each)

### QW-1: Golden Test Suite Expansion

**Goal**: Build a comprehensive set of known processes for testing.

**New Processes**:
```python
# 1. RRXOR Process (3 states)
# Outputs XOR of previous two bits

# 2. Nemo Process (6 states)
# Crutchfield's classic example

# 3. Simple Nonunifilar Machine (SNS)
# Minimal example where observation doesn't determine state

# 4. Period-n for various n
# Easy parametric family

# 5. Random Regular Graphs
# Generate random machines, test inference
```

**Deliverable**: `src/emic/sources/golden.py` with 10+ reference processes

---

### QW-2: Entropy Rate Benchmarks

**Goal**: Validate hμ computation against analytical values.

| Process | True hμ | Formula |
|---------|---------|---------|
| Biased Coin(p) | H(p) | -p log p - (1-p) log (1-p) |
| Golden Mean | log(φ) ≈ 0.694 | Known exactly |
| Even Process | 0.5 | By construction |
| Period-n | 0 | Deterministic |

**Deliverable**: Table of analytical vs computed values with error bounds

---

### QW-3: Visualization Gallery

**Goal**: Generate publication-ready figures.

**Figures**:
1. State diagrams with edge weights
2. Morph plots (time series colored by state)
3. Complexity plane (Cμ vs hμ scatter)
4. Convergence curves

---

## Medium Effort (1 week each)

### ME-1: Finite Sample Bias Characterization

**Goal**: Quantify how CSSR over-estimates states in finite samples.

**Design**:
```python
def bias_experiment():
    results = []
    for n in [100, 500, 1000, 5000, 10000]:
        for _ in range(100):
            data = EvenProcess().take(n)
            result = CSSR(config).infer(data)
            results.append({
                'n': n,
                'states': len(result.machine.states),
                'true_states': 2
            })
    return pd.DataFrame(results)
```

**Analysis**:
- Fit bias model: E[states] = f(n)
- Find n* where P(correct) > 0.95

---

### ME-2: Cross-Validation for Parameter Selection

**Goal**: Automatic selection of max_history and significance.

**Approach**:
```python
def cross_validate(data, k_folds=5):
    best_score = -inf
    best_params = None

    for L in range(2, 10):
        for sig in [0.001, 0.01, 0.05]:
            scores = []
            for train, test in k_fold_split(data, k_folds):
                machine = CSSR(CSSRConfig(L, sig)).infer(train).machine
                score = log_likelihood(machine, test) - penalty(machine)
                scores.append(score)
            if mean(scores) > best_score:
                best_score = mean(scores)
                best_params = (L, sig)

    return best_params
```

**Variants**:
- AIC/BIC for model selection
- Held-out likelihood
- Predictive information

---

### ME-3: CSSR vs True Machine Comparison

**Goal**: Systematically compare inferred to true for known processes.

**Metrics**:
1. **State count error**: |S_inferred| - |S_true|
2. **Edit distance**: Minimum edits to transform one to other
3. **Isomorphism check**: Are they structurally identical?
4. **Distribution distance**: KL(P_inferred || P_true)

**Processes**: All golden processes at various sample sizes

---

### ME-4: Noise Robustness Study

**Goal**: How does inference degrade with noisy observations?

**Noise Models**:
```python
def bit_flip_noise(data, p):
    """Flip each symbol with probability p."""
    return [x if random() > p else 1-x for x in data]

def insertion_noise(data, p):
    """Insert random symbol with probability p."""
    ...

def deletion_noise(data, p):
    """Delete symbol with probability p."""
    ...
```

**Analysis**: State count and Cμ error vs noise level

---

## High Effort (2+ weeks each)

### HE-1: Streaming/Online CSSR

**Goal**: Update ε-machine incrementally as data arrives.

**Challenges**:
- Maintain sufficient statistics
- Handle state splitting/merging online
- Detect non-stationarity

**Approach**:
```python
class StreamingCSSR:
    def __init__(self, config: CSSRConfig):
        self.suffix_tree = StreamingSuffixTree()
        self.machine = None

    def update(self, symbol: Symbol) -> EpsilonMachine | None:
        """Process one symbol, return updated machine if changed."""
        self.suffix_tree.add(symbol)
        if self.should_reconstruct():
            self.machine = self.reconstruct()
        return self.machine
```

---

### HE-2: Mixed-State Discovery

**Goal**: Handle processes where observation doesn't determine state.

**Theory**: Need to track distributions over states, not single states.

**Approach**:
1. Learn observable operator model
2. Extract mixed causal states
3. Compute crypticity (Cμ - E)

---

### HE-3: Multiscale Analysis

**Goal**: Analyze structure at different timescales.

**Approach**:
```python
def multiscale_analysis(data, scales=[1, 2, 5, 10, 50, 100]):
    results = {}
    for s in scales:
        coarsened = data[::s]  # Subsample
        # Or: block symbols at scale s
        machine = CSSR(config).infer(coarsened)
        results[s] = analyze(machine)
    return results
```

**Visualization**: Complexity vs scale plot

---

### HE-4: Real Data Applications

#### Finance: Market Microstructure

**Data**: Order book events (bid, ask, trade, cancel)

**Questions**:
- State structure of limit order books?
- Entropy rate as liquidity measure?
- Regime detection via state changes?

#### Genomics: Regulatory Sequences

**Data**: Promoter/enhancer sequences

**Questions**:
- Structural motifs as causal states?
- Compare across species?
- Predictive vs generative complexity?

#### Neuroscience: Spike Trains

**Data**: Neural spike times (discretized)

**Questions**:
- State structure of neural activity?
- Complexity differences by brain region?
- Changes with stimuli?

---

## Moonshot Ideas

### MS-1: ε-Machines for Reinforcement Learning

**Idea**: Use causal states as state representation for RL agents.

**Potential**: Minimal sufficient state for optimal control.

---

### MS-2: Generative ε-Machine Models

**Idea**: Train generative models that explicitly use ε-machine structure.

**Connection**: ε-machine as interpretable latent space.

---

### MS-3: ε-Machine Compression

**Idea**: Use predictive structure for data compression.

**Theory**: Entropy rate gives theoretical compression limit.

---

### MS-4: Causal State Similarity for Time Series Clustering

**Idea**: Cluster time series by their ε-machine structure.

**Distance**: D(ts1, ts2) = min edit distance between machines.

---

## Priority Matrix

| Experiment | Effort | Scientific Value | Paper Ready |
|------------|--------|------------------|-------------|
| QW-1 Golden Suite | Low | Medium | ✓ |
| QW-2 Entropy Bench | Low | High | ✓ |
| QW-3 Viz Gallery | Low | Medium | ✓ |
| ME-1 Bias Study | Medium | High | ✓ |
| ME-2 Cross-Val | Medium | High | ✓ |
| ME-3 Truth Compare | Medium | High | ✓ |
| ME-4 Noise Study | Medium | Medium | ✓ |
| HE-1 Streaming | High | High | Future |
| HE-2 Mixed States | High | Very High | Future |
| HE-3 Multiscale | High | High | ✓ |
| HE-4 Real Data | High | Very High | ✓ |

---

## Recommended Sequence

### Week 1: Foundation
1. QW-1: Expand golden test suite
2. QW-2: Entropy rate validation
3. QW-3: Create visualization functions

### Week 2: Core Experiments
4. ME-1: Bias characterization
5. ME-3: Inferred vs true comparison

### Week 3: Paper Figures
6. Generate convergence plots
7. Parameter sensitivity heatmaps
8. State diagram gallery

### Week 4: Real Data
9. Pick one domain (finance/genomics/neuro)
10. Run analysis, interpret results

### Ongoing: Alternative Algorithms
11. Implement CSM (simplest alternative)
12. Compare CSSR vs CSM
