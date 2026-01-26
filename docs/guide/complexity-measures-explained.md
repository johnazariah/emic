# Complexity Measures Explained

*Understanding what Cμ, hμ, E, and χ actually mean—with intuition and examples.*

**Prerequisites**: Basic probability, logarithms, entropy concept helpful but not required

**Reading time**: 30-40 minutes

---

## Table of Contents

1. [Why Measure Complexity?](#1-why-measure-complexity)
2. [Entropy: The Foundation](#2-entropy-the-foundation)
3. [Statistical Complexity (Cμ)](#3-statistical-complexity-c)
4. [Entropy Rate (hμ)](#4-entropy-rate-h)
5. [Excess Entropy (E)](#5-excess-entropy-e)
6. [Crypticity (χ)](#6-crypticity)
7. [The Complexity-Entropy Plane](#7-the-complexity-entropy-plane)
8. [Worked Examples](#8-worked-examples)
9. [Practical Usage in emic](#9-practical-usage-in-emic)
10. [Common Questions](#10-common-questions)

---

## 1. Why Measure Complexity?

### 1.1 Not All Sequences Are Equal

Consider three binary sequences:

**Sequence A** (Random coin flips):
```
1 0 1 1 0 0 1 0 1 1 1 0 0 0 1 0 ...
```

**Sequence B** (Alternating):
```
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 ...
```

**Sequence C** (Golden Mean—no consecutive 1s):
```
0 1 0 0 1 0 1 0 0 1 0 0 0 1 0 1 ...
```

Which is most "complex"? The answer depends on what we mean by complexity:

| Sequence | Predictable? | Structured? | Interesting? |
|----------|--------------|-------------|--------------|
| A (Random) | ❌ No | ❌ No | ❌ Boring |
| B (Periodic) | ✅ Yes | ✅ Yes | ❌ Trivial |
| C (Golden Mean) | 🔶 Partially | ✅ Yes | ✅ Interesting |

### 1.2 The Insight from Computational Mechanics

Computational mechanics provides measures that capture different aspects:

- **Cμ (Statistical Complexity)**: How much memory is needed to predict optimally?
- **hμ (Entropy Rate)**: How much is fundamentally unpredictable?
- **E (Excess Entropy)**: How much predictable structure exists?
- **χ (Crypticity)**: How much structure is hidden from direct observation?

These four numbers tell us almost everything about a process's complexity.

---

## 2. Entropy: The Foundation

### 2.1 What is Entropy?

Entropy measures **uncertainty** or **surprise**.

For a random variable $X$ with probabilities $p_1, p_2, \ldots, p_n$:

$$H(X) = -\sum_{i=1}^n p_i \log_2 p_i$$

**Units**: Bits (when using log base 2)

### 2.2 Intuition

| Scenario | Entropy | Intuition |
|----------|---------|-----------|
| Fair coin (50/50) | 1.0 bits | Maximum uncertainty for 2 outcomes |
| Biased coin (90/10) | 0.47 bits | Less uncertain—usually see heads |
| Certain outcome (100/0) | 0.0 bits | No uncertainty at all |

### 2.3 Examples

**Fair coin**: $H = -0.5 \log_2(0.5) - 0.5 \log_2(0.5) = 1.0$ bits

**Biased coin (p=0.9)**:
$$H = -0.9 \log_2(0.9) - 0.1 \log_2(0.1) = 0.47 \text{ bits}$$

**Fair die (6 sides)**:
$$H = -6 \times \frac{1}{6} \log_2\left(\frac{1}{6}\right) = \log_2(6) = 2.58 \text{ bits}$$

### 2.4 Key Properties

- $H(X) \geq 0$ (entropy is non-negative)
- $H(X) \leq \log_2(n)$ (maximum when uniform)
- $H(X) = 0$ only when one outcome is certain

---

## 3. Statistical Complexity (Cμ)

### 3.1 The Definition

Statistical complexity is the **entropy of the causal state distribution**:

$$C_\mu = H(S) = -\sum_{s \in \mathcal{S}} \pi_s \log_2 \pi_s$$

where $\pi_s$ is the probability of being in state $s$ at any given time (the stationary distribution).

### 3.2 What It Measures

Cμ answers: **How much information about the past must we remember to predict optimally?**

| Cμ Value | Interpretation |
|----------|----------------|
| 0 bits | No memory needed (i.i.d. process) |
| 1 bit | 2 equally likely states |
| 2 bits | 4 equally likely states |
| High | Many states or unequal probabilities |

### 3.3 Intuition: The Memory Cost

Imagine you're a prediction machine:
- You watch symbols stream by
- You want to predict what comes next
- You can store some information about the past

Cμ tells you the **minimum storage** (in bits) you need for optimal prediction.

### 3.4 Examples

**Biased Coin (i.i.d.)**:
- 1 state → $C_\mu = 0$ bits
- No memory helps—each symbol is independent

**Golden Mean** (2 states, roughly 2/3 and 1/3):
- $C_\mu = -\frac{2}{3}\log_2\frac{2}{3} - \frac{1}{3}\log_2\frac{1}{3} \approx 0.918$ bits
- Must remember if last symbol was 0 or 1

**Alternating (0101...)** (2 states, each 1/2):
- $C_\mu = 1.0$ bit exactly
- Must remember parity (even or odd position)

---

## 4. Entropy Rate (hμ)

### 4.1 The Definition

Entropy rate is the **average uncertainty per symbol**, given optimal prediction:

$$h_\mu = \lim_{n \to \infty} \frac{H(X_1, X_2, \ldots, X_n)}{n}$$

Or equivalently:

$$h_\mu = H(X_{t+1} | S_t) = -\sum_{s \in \mathcal{S}} \pi_s \sum_{x \in \mathcal{A}} P(x|s) \log_2 P(x|s)$$

### 4.2 What It Measures

hμ answers: **How much randomness is intrinsic to the process?**

| hμ Value | Interpretation |
|----------|----------------|
| 0 bits/symbol | Completely deterministic |
| 1 bit/symbol | Maximum randomness (binary) |
| Between | Partially predictable |

### 4.3 Intuition: Irreducible Randomness

Even with perfect knowledge of the current state, you still can't predict perfectly. hμ measures this **irreducible uncertainty**.

- Low hμ → Process is mostly predictable
- High hμ → Process is mostly random

### 4.4 Examples

**Periodic (0101...)**:
- $h_\mu = 0$ bits/symbol
- Given your position, you know exactly what comes next

**Fair Coin**:
- $h_\mu = 1.0$ bit/symbol
- Each symbol is completely unpredictable

**Golden Mean** (p=0.5):
- From state A: 50% chance of 0, 50% chance of 1 → 1 bit uncertainty
- From state B: 100% chance of 0 → 0 bits uncertainty
- Weighted average: $h_\mu = \frac{2}{3}(1.0) + \frac{1}{3}(0) = 0.667$ bits/symbol

### 4.5 Relationship to Entropy

The entropy rate is always less than or equal to the per-symbol entropy:

$$h_\mu \leq H(X)$$

The difference comes from **predictability**—correlations between symbols.

---

## 5. Excess Entropy (E)

### 5.1 The Definition

Excess entropy is the **mutual information between past and future**:

$$E = I(\overleftarrow{X}; \overrightarrow{X})$$

where $\overleftarrow{X}$ is the entire past and $\overrightarrow{X}$ is the entire future.

### 5.2 What It Measures

E answers: **How much information does the past provide about the future?**

| E Value | Interpretation |
|---------|----------------|
| 0 bits | Past tells nothing about future (i.i.d.) |
| High | Strong past-future correlation |

### 5.3 Intuition: Total Predictable Structure

Excess entropy measures the **total amount of predictable structure** in the process.

- E = 0: No correlations (random)
- E = ∞: Infinitely long correlations (possible in some processes)

### 5.4 Computation

For a finite-state process:

$$E = C_\mu - \chi$$

where χ is crypticity (see next section).

Or directly:

$$E = \lim_{L \to \infty} \left[ H(X_1, \ldots, X_L) - L \cdot h_\mu \right]$$

### 5.5 Examples

**Fair Coin**: $E = 0$ (no correlations)

**Golden Mean**: $E \approx 0.459$ bits (knowing we saw 1 means next must be 0)

**Periodic**: $E = \log_2(\text{period})$ (correlations extend to period length)

---

## 6. Crypticity (χ)

### 6.1 The Definition

Crypticity is the **difference between statistical complexity and excess entropy**:

$$\chi = C_\mu - E$$

### 6.2 What It Measures

χ answers: **How much of the stored information is "hidden" from direct observation?**

### 6.3 Intuition: Hidden Information

Some processes store information that affects their behavior but isn't directly visible in the output. This "cryptic" information is captured by χ.

**Example**: Imagine a machine that remembers a secret and only reveals it through subtle correlations. The memory (Cμ) is high, but the visible structure (E) is low. The difference (χ) represents the hidden part.

### 6.4 Properties

- $\chi \geq 0$ always
- $\chi = 0$ means all stored information is directly observable
- $\chi > 0$ means some information is "encrypted" in the state

### 6.5 Examples

**Golden Mean**:
- $C_\mu = 0.918$, $E = 0.459$
- $\chi = 0.918 - 0.459 = 0.459$ bits

This means about half the stored information is "cryptic"—it affects future behavior but isn't immediately obvious from short observations.

---

## 7. The Complexity-Entropy Plane

### 7.1 Visualizing Process Types

The **Cμ-hμ plane** reveals different regimes of behavior:

```
       Cμ (Statistical Complexity)
        ↑
   High │    ●  Complex            ●  Chaotic
        │       processes             edge-of-chaos
        │
   Med  │    ●  Structured         ●  Random with
        │       stochastic            structure
        │
   Low  │    ●  Simple             ●  Pure
        │       periodic              random
        └─────────────────────────────→ hμ
             Low              High     (Entropy Rate)
```

### 7.2 Process Archetypes

| Location | Example | Cμ | hμ |
|----------|---------|----|----|
| Bottom-left | Constant (000...) | 0 | 0 |
| Bottom-right | Fair coin | 0 | 1 |
| Top-left | Period-1000 | ~10 | 0 |
| Middle | Golden Mean | ~0.9 | ~0.67 |

### 7.3 The "Interesting" Region

The most interesting processes live in the **middle**—neither purely random nor purely deterministic. They have:
- Moderate Cμ: Some structure to remember
- Moderate hμ: Some genuine unpredictability
- High E: Rich correlations between past and future

Examples: natural language, biological sequences, financial time series.

---

## 8. Worked Examples

### 8.1 The Biased Coin

A coin that shows heads with probability 0.7:

```python
from emic.sources import BiasedCoinSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

source = BiasedCoinSource(p=0.7, _seed=42)
data = TakeN(10_000)(source)

result = CSSR(CSSRConfig(max_history=3)).infer(data)
summary = analyze(result.machine)

print(f"States: {summary.num_states}")           # 1
print(f"Cμ = {summary.statistical_complexity}")  # 0.0
print(f"hμ = {summary.entropy_rate}")            # ~0.88
print(f"E  = {summary.excess_entropy}")          # 0.0
```

**Interpretation**:
- 1 state: No memory helps
- Cμ = 0: Nothing to remember
- hμ = 0.88: Close to maximum entropy (0.88 for p=0.7)
- E = 0: No correlations

### 8.2 The Periodic Process

A process that repeats "01":

```python
from emic.sources import PeriodicSource, TakeN

source = PeriodicSource(pattern=(0, 1))
data = TakeN(1_000)(source)

result = CSSR(CSSRConfig(max_history=3)).infer(data)
summary = analyze(result.machine)

print(f"States: {summary.num_states}")           # 2
print(f"Cμ = {summary.statistical_complexity}")  # 1.0
print(f"hμ = {summary.entropy_rate}")            # 0.0
print(f"E  = {summary.excess_entropy}")          # 1.0
```

**Interpretation**:
- 2 states: "Just saw 0" and "Just saw 1"
- Cμ = 1.0: Need 1 bit to store which state
- hμ = 0: Perfectly predictable
- E = 1.0: Strong past-future correlation

### 8.3 The Golden Mean Process

No consecutive 1s allowed:

```python
from emic.sources import GoldenMeanSource, TakeN

source = GoldenMeanSource(p=0.5, _seed=42)
data = TakeN(10_000)(source)

result = CSSR(CSSRConfig(max_history=5)).infer(data)
summary = analyze(result.machine)

print(f"States: {summary.num_states}")           # 2
print(f"Cμ = {summary.statistical_complexity:.3f}")  # ~0.918
print(f"hμ = {summary.entropy_rate:.3f}")            # ~0.667
print(f"E  = {summary.excess_entropy:.3f}")          # ~0.459
print(f"χ  = {summary.crypticity:.3f}")              # ~0.459
```

**Interpretation**:
- 2 states: "Can emit 0 or 1" vs "Must emit 0"
- Cμ ≈ 0.918: Less than 1 bit (unequal state probabilities)
- hμ ≈ 0.667: Moderate randomness
- E ≈ 0.459: Moderate structure
- χ ≈ 0.459: Half of Cμ is "cryptic"

### 8.4 The Even Process

1s must come in pairs:

```python
from emic.sources import EvenProcessSource, TakeN

source = EvenProcessSource(p=0.5, _seed=42)
data = TakeN(10_000)(source)

result = CSSR(CSSRConfig(max_history=5, post_merge=True)).infer(data)
summary = analyze(result.machine)

print(f"States: {summary.num_states}")           # 2
print(f"Cμ = {summary.statistical_complexity:.3f}")  # ~1.0
print(f"hμ = {summary.entropy_rate:.3f}")            # ~0.5
print(f"E  = {summary.excess_entropy:.3f}")          # ~0.5
```

**Interpretation**:
- 2 states: "Neutral" vs "Must emit another 1"
- Higher structure, lower randomness than Golden Mean

---

## 9. Practical Usage in emic

### 9.1 The analyze() Function

```python
from emic.analysis import analyze

summary = analyze(machine)

# Access all measures
summary.statistical_complexity  # Cμ in bits
summary.entropy_rate           # hμ in bits/symbol
summary.excess_entropy         # E in bits
summary.crypticity             # χ in bits

# Structural info
summary.num_states             # Number of causal states
summary.num_transitions        # Number of transitions
summary.topological_complexity # log₂(num_states)
```

### 9.2 Individual Functions

```python
from emic.analysis import (
    statistical_complexity,
    entropy_rate,
    excess_entropy,
)

c_mu = statistical_complexity(machine)
h_mu = entropy_rate(machine)
e = excess_entropy(machine)
```

### 9.3 Comparing Inferred vs True

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import Spectral, SpectralConfig
from emic.analysis import analyze

source = GoldenMeanSource(p=0.5, _seed=42)

# Theoretical machine
true_summary = analyze(source.true_machine)
print(f"True Cμ = {true_summary.statistical_complexity:.4f}")

# Inferred machine
data = TakeN(10_000)(source)
result = Spectral(SpectralConfig()).infer(data)
inferred_summary = analyze(result.machine)
print(f"Inferred Cμ = {inferred_summary.statistical_complexity:.4f}")

# Error
error = abs(true_summary.statistical_complexity - inferred_summary.statistical_complexity)
print(f"Error = {error:.4f}")
```

---

## 10. Common Questions

### 10.1 Why is Cμ sometimes called "statistical complexity"?

The word "statistical" distinguishes it from other complexity measures (like Kolmogorov complexity). It's computed from the stationary probability distribution, hence "statistical."

### 10.2 What if Cμ = 0?

This means the process is **i.i.d.** (independent and identically distributed). No memory helps prediction—each symbol is independent of the past.

### 10.3 What if hμ = 0?

This means the process is **deterministic**. Given the current state, the next symbol is completely predictable.

### 10.4 Can E > Cμ?

No! We always have:

$$E \leq C_\mu$$

This is because the past-future information (E) can't exceed the information stored in the causal state (Cμ).

### 10.5 What's the relationship between these measures?

Key equations:
- $\chi = C_\mu - E$ (definition of crypticity)
- $E \leq C_\mu$ (structure can't exceed storage)
- $h_\mu \leq H(X)$ (entropy rate ≤ marginal entropy)

### 10.6 Which measure should I report?

**For most purposes, report Cμ and hμ together.** They give the complete picture:
- Cμ: The memory/structure side
- hμ: The randomness side

Add E if you're studying correlations, and χ if you're interested in "hidden" structure.

### 10.7 Are these measures robust to noise?

Moderate noise (< 10%) typically:
- Increases Cμ slightly (noise adds spurious states)
- Increases hμ (more apparent randomness)
- Decreases E (correlations are obscured)

Use `BitFlipNoise` to study robustness:

```python
from emic.sources import GoldenMeanSource, TakeN, BitFlipNoise

source = GoldenMeanSource(p=0.5, _seed=42)
noisy = source >> BitFlipNoise(flip_prob=0.05, seed=123) >> TakeN(10_000)
```

---

## Summary

| Measure | Symbol | Question Answered | Range |
|---------|--------|-------------------|-------|
| Statistical Complexity | Cμ | How much memory for optimal prediction? | 0 to ∞ |
| Entropy Rate | hμ | How much is irreducibly random? | 0 to log₂(\|A\|) |
| Excess Entropy | E | How much past-future correlation? | 0 to ∞ |
| Crypticity | χ | How much structure is hidden? | 0 to Cμ |

**Key relationships**:
- Random processes: Cμ = 0, hμ = max
- Deterministic processes: hμ = 0
- "Interesting" processes: Moderate Cμ and hμ
- Always: E ≤ Cμ, χ = Cμ - E

These measures, developed through computational mechanics, provide a principled vocabulary for describing the complexity of stochastic processes.
