# Quantum Advantage in Computational Mechanics

*Why quantum models can be more efficient than classical epsilon-machines*

---

## The Core Question

Computational mechanics studies how much memory is needed to optimally predict a stochastic process. The **epsilon-machine** (ε-machine) is the provably optimal *classical* predictor—it uses the minimum memory required to generate correct predictions.

But what if we allow quantum memory? Can quantum systems do better?

**Yes.** For many stochastic processes, quantum models require strictly less memory than the best classical model. This page explains why, and precisely when this advantage occurs.

---

## Classical Memory: The Epsilon-Machine

An ε-machine tracks **causal states**—equivalence classes of histories that make identical predictions about the future. The key insight is that we don't need to remember the full history; we only need to know which causal state we're in.

### Statistical Complexity

The memory required is the **statistical complexity**:

$$C_\mu = H(\mathcal{S}) = -\sum_i \pi_i \log_2 \pi_i$$

where $\pi_i$ is the probability of being in causal state $S_i$.

### The Classical Limitation

Here's the problem: classical memory must perfectly distinguish different causal states. Even if two states $S_j$ and $S_k$ are "almost identical" in their predictions, a classical system stores them in completely separate memory slots.

---

## The Quantum Insight: Non-Orthogonal Encoding

Quantum systems can encode information in **non-orthogonal states**—states that partially overlap and can't be perfectly distinguished.

### Why This Helps

Consider two causal states $S_j$ and $S_k$ that:

1. Have different pasts (so classically must be distinguished)
2. Can both transition to the **same** future state $S_l$ on the same symbol

```
     S_j ──(emit 'a')──→ S_l
     S_k ──(emit 'a')──→ S_l
```

Once both reach $S_l$, the information distinguishing $S_j$ from $S_k$ is **irreversibly lost**. But the classical machine stored it anyway! This is waste.

### Quantum Solution

Instead of orthogonal states:

```
Classical: |S_j⟩ ⊥ |S_k⟩  (perfectly distinguishable)
```

Use non-orthogonal states:

```
Quantum: ⟨s_j|s_k⟩ ≠ 0  (partially distinguishable)
```

The overlap $\langle s_j | s_k \rangle$ is proportional to how "similar" the futures are. We only distinguish states to the degree necessary for correct prediction—no more.

---

## Crypticity: The Measure of Waste

The gap between what's stored and what's used is called **crypticity**:

$$\chi = C_\mu - E$$

where:

- $C_\mu$ = statistical complexity (memory stored)
- $E$ = excess entropy = $I(\text{Past}; \text{Future})$ (memory actually used for prediction)

Crypticity $\chi$ measures the "hidden" or "cryptic" information that doesn't help predict the future.

**Key result:** Quantum models can eliminate the cryptic waste, achieving:

$$C_q \leq C_\mu$$

with $C_q \approx E$ in the ideal case.

---

## The Q-Machine Construction

Given an ε-machine, we construct a quantum model (q-machine) as follows.

### Signal States

For each causal state $S_j$ with transitions:

- Probability $T^{(x)}_{jk}$ of emitting symbol $x$ and going to state $S_k$

Define the **quantum signal state**:

$$|s_j\rangle = \sum_{k=1}^{N} \sum_{x \in \Sigma} \sqrt{T^{(x)}_{jk}} |x\rangle \otimes |k\rangle$$

### Quantum Complexity

The average quantum state is:

$$\rho = \sum_{j=1}^{N} \pi_j |s_j\rangle\langle s_j|$$

The quantum complexity is the von Neumann entropy:

$$C_q = S(\rho) = -\text{Tr}(\rho \log_2 \rho)$$

---

## Worked Example: The Perturbed Coin

The perturbed coin is the canonical example demonstrating quantum advantage.

### Setup

A coin that "persists" — it tends to repeat its previous value:

- With probability $1-p$: emit the same symbol as last time
- With probability $p$: flip to the other symbol

### Classical Machine

Two causal states:

- $S_0$: Last observation was 0
- $S_1$: Last observation was 1

Transitions:

- From $S_0$: emit 0 with prob $1-p$, stay in $S_0$; emit 1 with prob $p$, go to $S_1$
- From $S_1$: emit 1 with prob $1-p$, stay in $S_1$; emit 0 with prob $p$, go to $S_0$

```
        1-p              1-p
     ┌──────┐         ┌──────┐
     │  0   │         │  1   │
     └──►S₀◄─────p────►S₁◄───┘
            ◄────p────
```

Stationary distribution: $\pi_0 = \pi_1 = 0.5$

**Classical complexity:**

$$C_\mu = -0.5 \log_2(0.5) - 0.5 \log_2(0.5) = 1 \text{ bit}$$

Always 1 bit, regardless of $p$!

### Quantum States

$$|s_0\rangle = \sqrt{1-p}|0,0\rangle + \sqrt{p}|1,1\rangle$$
$$|s_1\rangle = \sqrt{p}|0,0\rangle + \sqrt{1-p}|1,1\rangle$$

These states overlap:

$$\langle s_0 | s_1 \rangle = 2\sqrt{p(1-p)}$$

As $p \to 0.5$: the overlap approaches 1 (states become identical).

### Quantum Complexity Calculation

The density matrix:

$$\rho = 0.5 |s_0\rangle\langle s_0| + 0.5 |s_1\rangle\langle s_1|$$

Eigenvalues: $\lambda_\pm = 0.5 \pm \sqrt{p(1-p)}$

**Quantum complexity:**

$$C_q = -\lambda_+ \log_2(\lambda_+) - \lambda_- \log_2(\lambda_-)$$

### Numerical Comparison

| $p$ | $C_\mu$ | $C_q$ | $\Delta_q$ | Savings |
|:---:|:-------:|:-----:|:----------:|:-------:|
| 0.1 | 1.000 | 0.722 | 0.278 | 28% |
| 0.2 | 1.000 | 0.469 | 0.531 | 53% |
| 0.3 | 1.000 | 0.250 | 0.750 | 75% |
| 0.4 | 1.000 | 0.081 | 0.919 | 92% |
| 0.49 | 1.000 | 0.002 | 0.998 | 99.8% |

As $p \to 0.5$, the signal states become nearly identical, overlap approaches 1, and $C_q \to 0$.

---

## The Signal State Overlap Criterion

Our validation experiments reveal a precise, computable criterion:

!!! success "The Main Result"
    **Quantum advantage exists if and only if signal states have non-zero overlap.**

    Mathematically: $\Delta_q = C_\mu - C_q > 0$ ⟺ $\exists j \neq k: \langle s_j | s_k \rangle > 0$

### The Overlap Formula

The overlap between signal states is:

$$\langle s_j | s_k \rangle = \sum_{x,l} \sqrt{T^{(x)}_{jl} \cdot T^{(x)}_{kl}}$$

This is non-zero when there exists a symbol $x$ and target state $l$ such that **both**:

- $T^{(x)}_{jl} > 0$ (state $j$ can emit $x$ and reach $l$)
- $T^{(x)}_{kl} > 0$ (state $k$ can emit $x$ and reach $l$)

In graph terms: **paths merge**.

---

## Taxonomy: Which Processes Have Quantum Advantage?

Based on our validation of 10+ process types:

### ❌ Processes WITHOUT Quantum Advantage

| Process Type | Why No Advantage |
|:------------|:-----------------|
| **IID (e.g., biased coin)** | Single state → pure signal state → $C_q = 0 = C_\mu$ |
| **Deterministic (e.g., periodic)** | Each state emits unique symbol → orthogonal signal states |
| **Co-unifilar** | No merging paths → orthogonal futures |

### ✅ Processes WITH Quantum Advantage

| Process Type | Why Advantage | Typical Savings |
|:------------|:--------------|:----------------|
| **Perturbed coin** | Symmetric merging transitions | Up to 100% |
| **Golden mean** | Shared $S_0 \to S_0$ transition | ~40% |
| **Most Markov chains** | Irreversible transitions | Varies |

### The Even Process: A Subtle Case

The Even Process (1s must come in pairs) has 2 states like Golden Mean, but **no quantum advantage**:

```
Even Process:              Golden Mean:
  ┌─0─┐                      ┌─0─┐
  │   ▼                      │   ▼
  └──A◄───B                  └──S₀◄───S₁
        │                        1    │
        1                        ▲    │
        └────┘                   └─0──┘
```

**Why the difference?**

- **Golden Mean**: Both states can emit 0 and reach $S_0$ → overlap → advantage
- **Even Process**: State A emits {0,1}, but state B can **only** emit 1 → disjoint futures → orthogonal signal states → no advantage

The key is not the number of states, but whether different states can take the **same transition**.

---

## Decision Tree: Does Your Process Have Quantum Advantage?

```
1. How many causal states?
   └─ 1 state → NO (IID, trivially classical)
   └─ 2+ states → continue...

2. Is the ε-machine deterministic (each state has unique output)?
   └─ Yes → NO (orthogonal signal states)
   └─ No → continue...

3. Do any two states share a transition?
   (Can states j and k both emit symbol x and reach state l?)
   └─ No → NO (orthogonal signal states)
   └─ Yes → ✅ YES! Quantum advantage exists
```

---

## Key Inequalities

The fundamental hierarchy:

$$E \leq C_q \leq C_\mu$$

- **$E$**: Excess entropy (fundamental lower bound—cannot be beaten)
- **$C_q$**: Quantum complexity (achievable with quantum memory)
- **$C_\mu$**: Classical complexity (achievable with classical memory)

### When Equality Holds

**$C_q = C_\mu$:** When the ε-machine has no merging transitions (orthogonal signal states).

**$C_q = E$:** When the q-machine achieves the theoretical optimum. The perturbed coin approaches this as $p \to 0.5$.

---

## Physical Interpretation

### Information Destined to be Lost

The quantum advantage represents information that classical models must store but which is **destined to be lost** when paths merge.

**Analogy**: Imagine two roads (histories) that merge into one highway (future). A classical traffic counter must remember which road each car came from. A quantum counter encodes this information "non-orthogonally" — just distinguishable enough for correct predictions, but no more.

### The Thermodynamic Connection

A model must store at least $E$ bits to capture the past-future correlation. This is a fundamental limit with thermodynamic implications.

Classical models pay a penalty of $\chi = C_\mu - E$ bits because they can't encode partial distinguishability. This extra storage represents wasted resources.

---

## Computing Quantum Complexity in emic

```python
from emic.sources.synthetic.perturbed_coin import PerturbedCoinSource
from emic.analysis import (
    statistical_complexity,
    quantum_complexity,
    quantum_advantage,
)

# Create a perturbed coin with p=0.3
source = PerturbedCoinSource(p=0.3)
machine = source.true_machine

# Compute complexities
c_mu = statistical_complexity(machine)  # 1.0 bits
c_q = quantum_complexity(machine)       # 0.25 bits
delta = quantum_advantage(machine)      # 0.75 bits (75% savings!)

print(f"Classical: {c_mu:.3f} bits")
print(f"Quantum:   {c_q:.3f} bits")
print(f"Advantage: {delta:.3f} bits ({100*delta/c_mu:.0f}% savings)")
```

---

## Further Reading

1. **Gu et al. (2012)** - "Quantum mechanics can reduce the complexity of classical models" - The foundational paper proving quantum advantage
2. **Thompson et al. (2018)** - "Causal Asymmetry in a Quantum World" - Extends to time-reversal and bidirectional prediction
3. **Garner et al. (2017)** - "Unbounded Memory Advantage" - Proves the advantage can be arbitrarily large

---

*Part of the emic quantum extension documentation*
