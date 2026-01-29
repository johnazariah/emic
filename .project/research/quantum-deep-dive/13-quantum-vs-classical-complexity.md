# Chapter 13: Quantum vs Classical Complexity

*Why $C_q < C_\mu$ — The culmination of everything we've learned*

---

## The Central Result

We've built all the machinery. Now we answer the key question:

> **Why can quantum models be more memory-efficient than classical ones?**

The answer uses everything from Parts I-III:
- Density matrices (Chapter 3)
- Von Neumann entropy (Chapter 4)
- Non-orthogonality (Chapter 2)
- Decoherence (Chapter 8)

---

## Classical Epsilon-Machines

An **epsilon-machine** (ε-machine) is the optimal classical model for a stochastic process. It consists of:

- **Causal states** $\{S_1, S_2, \ldots, S_N\}$: equivalence classes of histories with identical futures
- **Transitions** $T^{(x)}_{jk}$: probability of emitting symbol $x$ and going from state $S_j$ to $S_k$
- **Stationary distribution** $\pi = (\pi_1, \ldots, \pi_N)$: long-run state probabilities

The **statistical complexity** measures memory:

$$C_\mu = H(\pi) = -\sum_j \pi_j \log_2 \pi_j$$

This is the entropy of the causal state distribution—the minimum classical memory needed.

### The Classical Constraint

Here's the key limitation: a classical model must **perfectly distinguish** different causal states. Even if two states make very similar predictions, they occupy orthogonal memory slots:

$$\langle S_j | S_k \rangle = \delta_{jk} = \begin{cases} 1 & j = k \\ 0 & j \neq k \end{cases}$$

Classical distinguishability is all-or-nothing.

---

## The Quantum Insight

Quantum states don't have this constraint. Two states can **partially overlap**:

$$0 < |\langle s_j | s_k \rangle| < 1$$

This means: distinguish states only to the degree necessary.

### When Is Perfect Distinguishability Unnecessary?

Consider two causal states $S_j$ and $S_k$ that can both transition to the same state $S_l$:

```
     S_j ──(emit 'a')──→ S_l
                 ↗
     S_k ──(emit 'a')
```

Once you reach $S_l$, the information about whether you came from $S_j$ or $S_k$ is **lost forever**. But the classical machine stored that information anyway!

This is crypticity—information stored but never used.

### The Quantum Solution

The **quantum epsilon-machine** (q-machine) encodes states non-orthogonally. States that merge in the future get larger overlaps. States that never merge stay orthogonal.

---

## Constructing the Q-Machine

Given an ε-machine, we build a q-machine as follows.

### Step 1: Define Signal States

For each causal state $S_j$, define a **signal state**:

$$|s_j\rangle = \sum_{k=1}^{N} \sum_{x \in \Sigma} \sqrt{T^{(x)}_{jk}} \, |x\rangle \otimes |k\rangle$$

This encodes the transition probabilities as quantum amplitudes.

### Step 2: Form the Ensemble

The q-machine's memory is the mixed state:

$$\rho = \sum_j \pi_j |s_j\rangle\langle s_j|$$

### Step 3: Compute Quantum Complexity

The **quantum statistical complexity** is:

$$C_q = S(\rho) = -\text{Tr}(\rho \log_2 \rho)$$

---

## The Key Inequality

**Theorem (Gu et al. 2012):** For any stationary stochastic process:

$$E \leq C_q \leq C_\mu$$

where:
- $E$ = excess entropy (mutual information between past and future)
- $C_q$ = quantum statistical complexity
- $C_\mu$ = classical statistical complexity

### What This Means

| Relationship | Interpretation |
|--------------|----------------|
| $C_q < C_\mu$ | Quantum is more efficient than classical |
| $C_q = E$ | Quantum achieves the information-theoretic lower bound |
| $C_q = C_\mu$ | No quantum advantage (rare) |

For almost all processes: $C_q < C_\mu$.

---

## Worked Example: Perturbed Coin

The simplest process with quantum advantage.

### Process Definition

A two-state process:
- State $A$: emit 0 with prob $1-p$, emit 1 with prob $p$
- State $B$: emit 0 with prob $p$, emit 1 with prob $1-p$
- After each emission, switch to the other state

### Classical Complexity

Two causal states with equal probability:

$$C_\mu = H(1/2, 1/2) = 1 \text{ bit}$$

The classical machine needs 1 bit to track which state it's in.

### Quantum Complexity

The signal states are:

$$|s_A\rangle = \sqrt{1-p}|0\rangle|B\rangle + \sqrt{p}|1\rangle|B\rangle$$
$$|s_B\rangle = \sqrt{p}|0\rangle|A\rangle + \sqrt{1-p}|1\rangle|A\rangle$$

Their overlap:

$$\langle s_A | s_B \rangle = 2\sqrt{p(1-p)}$$

For $p = 0.3$:
- Overlap $= 2\sqrt{0.3 \times 0.7} \approx 0.917$
- Nearly identical states!

The density matrix:

$$\rho = \frac{1}{2}|s_A\rangle\langle s_A| + \frac{1}{2}|s_B\rangle\langle s_B|$$

Computing $S(\rho)$:

| $p$ | Overlap | $C_q$ | Advantage |
|-----|---------|-------|-----------|
| 0.5 | 1.0 | 0 bits | 1 bit |
| 0.3 | 0.917 | 0.25 bits | 0.75 bits |
| 0.1 | 0.6 | 0.71 bits | 0.29 bits |
| 0.01 | 0.2 | 0.97 bits | 0.03 bits |

### The Pattern

When $p \approx 0.5$, the two states are nearly identical → large overlap → low $C_q$ → big advantage.

When $p \approx 0$ or $p \approx 1$, states are very different → small overlap → $C_q \approx C_\mu$ → little advantage.

---

## Why Does This Work?

Three key insights:

### 1. Off-Diagonal Coherence

The density matrix $\rho = \sum_j \pi_j |s_j\rangle\langle s_j|$ has off-diagonal elements when signal states overlap.

Off-diagonals reduce entropy: the eigenvalues become more concentrated, lowering $S(\rho)$.

This is the unified theme: **off-diagonal = information compression**.

### 2. Irreversibility Condition

Quantum advantage exists if and only if the ε-machine has **merging transitions**—where multiple states can reach the same destination.

If the ε-machine is a tree (no merging), then $C_q = C_\mu$. No advantage.

### 3. Crypticity as Waste

The gap $\chi = C_\mu - E$ is called **crypticity**. It measures information stored but never used for prediction.

Quantum models eliminate this waste:

$$C_q \leq C_\mu - \chi = E$$

In the ideal case, $C_q = E$.

---

## The Decoherence Perspective

What happens if we apply decoherence to a q-machine?

Decoherence destroys off-diagonal elements. As coherence decays:
- Off-diagonals → 0
- Entropy increases
- $C_q → C_\mu$

The classical ε-machine is the **fully decohered** q-machine. Classicality is a special case of quantumness.

---

## Summary

| Concept | Classical | Quantum |
|---------|-----------|---------|
| Memory representation | Orthogonal states | Non-orthogonal states |
| Distinguishability | Perfect | Partial |
| Complexity measure | $C_\mu = H(\pi)$ | $C_q = S(\rho)$ |
| Information stored | Includes waste | Only what's needed |
| Lower bound | $C_\mu \geq E$ | $C_q \geq E$ (achievable) |

**Key Takeaway:**

> Quantum models are more efficient because they don't waste memory on distinctions that will be erased anyway.

The gap $C_\mu - C_q$ quantifies the cost of classical distinguishability.

---

## Common Misconceptions

**"Quantum advantage comes from parallel processing."**

No—there's no parallelism here. The advantage comes from information geometry: encoding in a smaller state space.

**"This requires entanglement."**

No—single-qubit q-machines can achieve advantage. Entanglement isn't required for memory compression (though it matters for multipartite processes).

**"Quantum advantage is exponential."**

Not always. For some processes (like Ising models), the advantage can be **unbounded**—but for others it's modest. The gap depends on the process structure.

---

## Code Example

```python
import numpy as np

def signal_state(T, j):
    """Build signal state |s_j⟩ from transition matrix."""
    N = T.shape[1]  # number of states
    A = T.shape[0]  # alphabet size
    dim = A * N
    s = np.zeros(dim, dtype=complex)
    for x in range(A):
        for k in range(N):
            idx = x * N + k
            s[idx] = np.sqrt(T[x, j, k])
    return s

def quantum_complexity(T, pi):
    """Compute C_q from transition tensor and stationary dist."""
    N = len(pi)
    signal_states = [signal_state(T, j) for j in range(N)]

    # Build density matrix
    dim = len(signal_states[0])
    rho = np.zeros((dim, dim), dtype=complex)
    for j, pj in enumerate(pi):
        s = signal_states[j]
        rho += pj * np.outer(s, s.conj())

    # Von Neumann entropy
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-12]
    return -np.sum(eigenvalues * np.log2(eigenvalues))

# Perturbed coin example
p = 0.3
# T[x, from, to] = P(emit x, go to 'to' | in state 'from')
# States: 0=A, 1=B. Symbols: 0, 1
T = np.zeros((2, 2, 2))
T[0, 0, 1] = 1 - p  # A: emit 0, go to B
T[1, 0, 1] = p      # A: emit 1, go to B
T[0, 1, 0] = p      # B: emit 0, go to A
T[1, 1, 0] = 1 - p  # B: emit 1, go to A

pi = np.array([0.5, 0.5])

C_q = quantum_complexity(T, pi)
C_mu = 1.0  # H(0.5, 0.5)

print(f"C_μ = {C_mu:.3f} bits")
print(f"C_q = {C_q:.3f} bits")
print(f"Quantum advantage = {C_mu - C_q:.3f} bits")
```

---

## Connection to Part III

The quantum advantage in complexity is the same phenomenon as in quantum algorithms:

| Algorithms | Complexity |
|------------|------------|
| Superposition explores options | Non-orthogonal states overlap |
| Interference cancels wrong answers | Off-diagonals reduce entropy |
| Measurement extracts result | Prediction uses compressed memory |

**Same physics, different application.**

---

## Looking Ahead

Chapter 14 addresses a practical question: if quantum memory is so delicate, how can we protect it from decoherence?

The answer is error correction—and it has surprising connections to the crypticity we've been discussing.

---

*Next: [Chapter 14: Error Correction](14-error-correction.md)*
