# Chapter 3: The Density Matrix

*The one object that captures everything*

---

## The Central Character

If there's one object you should master in quantum mechanics, it's the **density matrix**. It unifies:

- Pure states and mixed states
- Classical probability and quantum superposition
- Measurement and decoherence
- Entropy and information

And most importantly for us: **the density matrix makes the classical/quantum boundary visible**.

---

## Definition

A density matrix $\rho$ is a matrix that satisfies three properties:

1. **Hermitian**: $\rho^\dagger = \rho$ (equals its conjugate transpose)
2. **Unit trace**: $\text{Tr}(\rho) = 1$ (probabilities sum to 1)
3. **Positive semi-definite**: All eigenvalues $\geq 0$ (no negative probabilities)

Any matrix satisfying these three properties represents a valid quantum state.

---

## Pure States

A **pure state** is a quantum system in a definite state vector $|\psi\rangle$.

Its density matrix is the outer product:

$$\rho = |\psi\rangle\langle\psi|$$

### Worked Example: A Qubit Superposition

Let $|\psi\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$.

As a column vector: $|\psi\rangle = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$

The bra (conjugate transpose): $\langle\psi| = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \end{pmatrix}$

The density matrix:

$$\rho = |\psi\rangle\langle\psi| = \frac{1}{2}\begin{pmatrix} 1 \\ 1 \end{pmatrix}\begin{pmatrix} 1 & 1 \end{pmatrix} = \frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix} = \begin{pmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{pmatrix}$$

**Key observation**: The off-diagonals are nonzero! This encodes the superposition.

### Pure State Test

A state is pure if and only if $\rho^2 = \rho$ (idempotent).

Equivalently: $\text{Tr}(\rho^2) = 1$.

Let's verify:

$$\rho^2 = \begin{pmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{pmatrix}\begin{pmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{pmatrix} = \begin{pmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{pmatrix} = \rho \quad \checkmark$$

---

## Mixed States

A **mixed state** represents classical uncertainty about which quantum state a system is in.

If the system is in state $|\psi_i\rangle$ with probability $p_i$, the density matrix is:

$$\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$$

### Worked Example: Classical Coin Flip

Suppose someone flips a fair coin:
- Heads → prepare $|0\rangle$
- Tails → prepare $|1\rangle$

You don't know the outcome. Your density matrix:

$$\rho = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1| = \frac{1}{2}\begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} + \frac{1}{2}\begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}$$

**Key observation**: The off-diagonals are zero! This is purely classical uncertainty.

### Mixed State Test

For a mixed state: $\text{Tr}(\rho^2) < 1$.

$$\rho^2 = \begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}^2 = \begin{pmatrix} 0.25 & 0 \\ 0 & 0.25 \end{pmatrix}$$

$$\text{Tr}(\rho^2) = 0.25 + 0.25 = 0.5 < 1 \quad \checkmark$$

---

## The Punchline: Diagonal = Classical

Compare our two examples:

| State | Density Matrix | Off-diagonals | Interpretation |
|-------|---------------|---------------|----------------|
| Superposition | $\begin{pmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{pmatrix}$ | **Nonzero** | Quantum coherence |
| Classical mixture | $\begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}$ | **Zero** | Classical probability |

Both have the same diagonal: 50% probability of measuring $|0\rangle$, 50% for $|1\rangle$.

But they're fundamentally different states:
- The superposition can interfere
- The classical mixture cannot

**The off-diagonal elements are called "coherences."** They encode quantum superposition. When they're zero, the state is effectively classical.

---

## Reading a Density Matrix

Given any density matrix, you can immediately extract:

### 1. Measurement Probabilities

The diagonal elements give probabilities of measuring each basis state:

$$P(i) = \rho_{ii}$$

### 2. Coherences

The off-diagonal elements $\rho_{ij}$ (for $i \neq j$) tell you about superposition between basis states $|i\rangle$ and $|j\rangle$.

- $\rho_{ij} = 0$: No coherence between $|i\rangle$ and $|j\rangle$
- $\rho_{ij} \neq 0$: Quantum superposition present

### 3. Purity

$$\gamma = \text{Tr}(\rho^2)$$

- $\gamma = 1$: Pure state (maximum quantum-ness)
- $\gamma = 1/d$: Maximally mixed (maximum classical uncertainty, where $d$ is dimension)
- In between: Partially mixed

### 4. Entropy

$$S(\rho) = -\text{Tr}(\rho \log_2 \rho) = -\sum_i \lambda_i \log_2 \lambda_i$$

where $\lambda_i$ are the eigenvalues.

- $S = 0$: Pure state (perfect knowledge)
- $S = \log_2 d$: Maximally mixed (maximum uncertainty)

---

## Why Eigenvalues Matter

The eigenvalues of $\rho$ are the key to understanding it.

For our two examples:

**Superposition** $\begin{pmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{pmatrix}$:
- Eigenvalues: $\lambda = 1, 0$
- Entropy: $S = -1 \cdot \log_2(1) - 0 \cdot \log_2(0) = 0$ bits

**Classical mixture** $\begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}$:
- Eigenvalues: $\lambda = 0.5, 0.5$
- Entropy: $S = -0.5 \log_2(0.5) - 0.5 \log_2(0.5) = 1$ bit

The superposition has **zero entropy**—it's a definite quantum state. The classical mixture has **one bit of entropy**—genuine uncertainty about which state it is.

---

## The Bloch Ball: Visualizing Qubit States

For a single qubit, any density matrix can be written as:

$$\rho = \frac{1}{2}(I + \vec{r} \cdot \vec{\sigma})$$

where $\vec{r} = (r_x, r_y, r_z)$ is the **Bloch vector** and $\vec{\sigma}$ are the Pauli matrices.

The constraint: $|\vec{r}| \leq 1$.

- $|\vec{r}| = 1$: Pure state (on the surface of the Bloch sphere)
- $|\vec{r}| < 1$: Mixed state (inside the Bloch ball)
- $|\vec{r}| = 0$: Maximally mixed (at the center)

```
        |0⟩ (pure)
         ●
        /|\
       / | \
      /  ●  \    ← mixed states (inside)
     /   |   \
    ●----●----●  ← maximally mixed (center)
     \   |   /
      \  |  /
       \ | /
        \|/
         ●
        |1⟩ (pure)
```

Pure states live on the surface. Decoherence moves states toward the center.

---

## Connection to Computational Mechanics

In the quantum approach to computational mechanics:

1. Each classical causal state $S_j$ gets a quantum "signal state" $|s_j\rangle$
2. The process's overall quantum state is:

$$\rho = \sum_{j=1}^{N} \pi_j |s_j\rangle\langle s_j|$$

where $\pi_j$ is the stationary probability of causal state $S_j$.

This is a mixed state—classical uncertainty over which causal state we're in, but each causal state is encoded quantumly.

**The key insight**: If the signal states $|s_j\rangle$ are not orthogonal (i.e., $\langle s_i | s_j \rangle \neq 0$ for some $i \neq j$), then $\rho$ has structure beyond its diagonal. The eigenvalues are "compressed" compared to the classical case.

**Result**: The von Neumann entropy $S(\rho)$ can be less than the Shannon entropy $H(\pi)$. This is the quantum advantage:

$$C_q = S(\rho) \leq H(\pi) = C_\mu$$

---

## Operations on Density Matrices

### Unitary Evolution

A closed quantum system evolves by unitary transformation:

$$\rho \to U \rho U^\dagger$$

This preserves eigenvalues (and hence entropy). It rotates the Bloch vector but doesn't shrink it.

### Measurement

Measuring in basis $\{|i\rangle\}$ transforms:

$$\rho \to \sum_i |i\rangle\langle i| \rho |i\rangle\langle i| = \text{diag}(\rho)$$

This **kills all off-diagonals**. The state becomes classical.

### Partial Trace (Entanglement)

For composite systems, tracing out one subsystem can increase entropy—even starting from a pure state. This is entanglement, which we'll cover in Chapter 7.

---

## Key Takeaway

> **The density matrix is the complete description of a quantum state.**
>
> - Diagonal elements = measurement probabilities (classical)
> - Off-diagonal elements = coherences (quantum)
> - Eigenvalues determine entropy and purity
>
> **Classical states have zero off-diagonals. Quantum states populate the full matrix.**

---

## Common Misconceptions

### "The density matrix is just for mixed states"

No—pure states have density matrices too. The density matrix is the universal representation. Pure states are the special case where $\rho^2 = \rho$.

### "Off-diagonals mean the state is uncertain"

The opposite! Off-diagonals encode definite phase relationships—quantum coherence. A pure superposition has off-diagonals and zero entropy. A classical mixture has no off-diagonals but nonzero entropy.

### "You can tell if a state is mixed by looking at the diagonal"

No! The diagonal only gives measurement probabilities. Two very different states can have the same diagonal. You need the full matrix (or eigenvalues) to determine purity.

### "Density matrices are 2×2"

Only for qubits! For $d$-level systems, density matrices are $d \times d$. For $n$ qubits, they're $2^n \times 2^n$. The formalism generalizes completely.

---

## Code Example

```python
import numpy as np

def make_pure_state_dm(psi):
    """Density matrix from state vector."""
    psi = np.array(psi, dtype=complex)
    psi = psi / np.linalg.norm(psi)  # normalize
    return np.outer(psi, np.conj(psi))

def purity(rho):
    """Tr(ρ²) - equals 1 for pure states."""
    return np.real(np.trace(rho @ rho))

def von_neumann_entropy(rho):
    """S(ρ) = -Tr(ρ log₂ ρ) in bits."""
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    return -np.sum(eigenvalues * np.log2(eigenvalues))

# Pure superposition: (|0⟩ + |1⟩)/√2
psi_super = [1, 1]
rho_super = make_pure_state_dm(psi_super)

# Classical mixture: 50% |0⟩, 50% |1⟩
rho_0 = make_pure_state_dm([1, 0])
rho_1 = make_pure_state_dm([0, 1])
rho_mix = 0.5 * rho_0 + 0.5 * rho_1

print("=== Superposition (|0⟩ + |1⟩)/√2 ===")
print(f"Density matrix:\n{rho_super}")
print(f"Purity: {purity(rho_super):.3f}")
print(f"Entropy: {von_neumann_entropy(rho_super):.3f} bits")
print(f"Eigenvalues: {np.linalg.eigvalsh(rho_super)}")

print("\n=== Classical 50/50 mixture ===")
print(f"Density matrix:\n{rho_mix}")
print(f"Purity: {purity(rho_mix):.3f}")
print(f"Entropy: {von_neumann_entropy(rho_mix):.3f} bits")
print(f"Eigenvalues: {np.linalg.eigvalsh(rho_mix)}")
```

---

## What's Next

In [Chapter 4: Entropy and Purity](04-entropy-purity.md), we'll dive deeper into how to quantify "how quantum" a state is, and see why von Neumann entropy is the natural measure.

---

*[← Previous: The Quantum Twist](02-quantum-twist.md) | [Back to Overview](00-overview.md) | [Next: Entropy and Purity →](04-entropy-purity.md)*
