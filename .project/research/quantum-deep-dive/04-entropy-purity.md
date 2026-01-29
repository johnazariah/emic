# Chapter 4: Entropy and Purity

*Measuring "how quantum" a state is*

---

## Two Measures, One Story

We've seen that pure states and mixed states are fundamentally different. Now we need to quantify that difference.

Two key measures:
1. **Purity** ($\gamma$): How "pure" is the state?
2. **Von Neumann Entropy** ($S$): How much uncertainty is there?

They're related but not identical—and both tell us about the classical/quantum boundary.

---

## Purity

### Definition

$$\gamma = \text{Tr}(\rho^2)$$

The trace of the density matrix squared.

### Range

- **Maximum**: $\gamma = 1$ for pure states ($\rho^2 = \rho$)
- **Minimum**: $\gamma = 1/d$ for maximally mixed states (dimension $d$)

### Intuition

Purity measures how "concentrated" the eigenvalue distribution is.

For a pure state, one eigenvalue is 1 and the rest are 0:
$$\gamma = 1^2 + 0^2 + \cdots = 1$$

For a maximally mixed state ($d$ dimensions), all eigenvalues are $1/d$:
$$\gamma = d \times (1/d)^2 = 1/d$$

### Worked Example

**Pure qubit** ($\rho = |0\rangle\langle 0|$):
$$\rho = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}, \quad \rho^2 = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$$
$$\gamma = \text{Tr}(\rho^2) = 1 + 0 = 1$$

**Maximally mixed qubit** ($\rho = I/2$):
$$\rho = \begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}, \quad \rho^2 = \begin{pmatrix} 0.25 & 0 \\ 0 & 0.25 \end{pmatrix}$$
$$\gamma = \text{Tr}(\rho^2) = 0.25 + 0.25 = 0.5 = 1/2$$

---

## Von Neumann Entropy

### Definition

$$S(\rho) = -\text{Tr}(\rho \log_2 \rho)$$

Since $\rho$ is Hermitian, we can diagonalize it. If $\rho$ has eigenvalues $\{\lambda_i\}$:

$$S(\rho) = -\sum_i \lambda_i \log_2 \lambda_i$$

This is just Shannon entropy of the eigenvalue distribution!

### Range

- **Minimum**: $S = 0$ for pure states (one eigenvalue = 1)
- **Maximum**: $S = \log_2 d$ for maximally mixed states (uniform eigenvalues)

### Why Eigenvalues?

The eigenvalues of $\rho$ represent the probabilities in the "most diagonal" basis—the basis where $\rho$ has no coherences.

Every density matrix can be written as:
$$\rho = \sum_i \lambda_i |e_i\rangle\langle e_i|$$

where $|e_i\rangle$ are the eigenvectors. In this basis, $\rho$ is diagonal with entries $\lambda_i$.

The entropy measures uncertainty in this optimal basis.

---

## Relationship Between Purity and Entropy

Both depend on eigenvalues, but differently:

| Measure | Formula | Pure State | Max Mixed |
|---------|---------|------------|-----------|
| Purity | $\sum_i \lambda_i^2$ | 1 | $1/d$ |
| Entropy | $-\sum_i \lambda_i \log_2 \lambda_i$ | 0 | $\log_2 d$ |

Purity is higher when eigenvalues are "peaked." Entropy is lower when eigenvalues are peaked.

They're inversely related but not simple inverses—the functional forms differ.

### The Linear Entropy Approximation

For states close to pure, there's a useful approximation:

$$S_{\text{linear}} = 1 - \gamma = 1 - \text{Tr}(\rho^2)$$

This "linear entropy" is zero for pure states and positive for mixed states. It's easier to compute than von Neumann entropy (no logarithms) and often used in experiments.

---

## The Classical Limit: Diagonal Matrices

If $\rho$ is diagonal:
$$\rho = \text{diag}(p_1, p_2, \ldots, p_n)$$

Then:
- Eigenvalues = diagonal entries: $\lambda_i = p_i$
- Von Neumann entropy = Shannon entropy: $S(\rho) = H(p)$
- No coherences: purely classical state

**This is why diagonal = classical**: a diagonal density matrix is just a probability distribution in disguise.

---

## Entropy Under Operations

### Unitary Evolution: Entropy Preserved

If $\rho \to U\rho U^\dagger$ (unitary evolution):
$$S(U\rho U^\dagger) = S(\rho)$$

Unitary transformations preserve eigenvalues, so entropy is unchanged. A closed quantum system doesn't gain or lose information.

### Measurement: Entropy Increases (Usually)

Measuring in basis $\{|i\rangle\}$ gives:
$$\rho \to \sum_i |i\rangle\langle i|\rho|i\rangle\langle i| = \text{diag}(\rho)$$

This kills off-diagonals. For a pure superposition, this **increases** entropy—you're destroying coherence.

### Partial Trace: Entropy Can Increase

For entangled systems, tracing out one part can turn a pure global state into a mixed local state. This is how entanglement creates local uncertainty.

---

## Connection to Quantum Advantage

In computational mechanics:

$$C_q = S(\rho) = S\left(\sum_j \pi_j |s_j\rangle\langle s_j|\right)$$

$$C_\mu = H(\pi) = -\sum_j \pi_j \log_2 \pi_j$$

The quantum complexity is the von Neumann entropy of the q-machine density matrix.
The classical complexity is the Shannon entropy of the causal state distribution.

**When signal states overlap**: The eigenvalues of $\rho$ are more "peaked" than the $\pi_j$ values. This gives:
$$C_q = S(\rho) < H(\pi) = C_\mu$$

The quantum representation compresses the information.

---

## Worked Example: Varying Overlap

Let's see how entropy changes with signal state overlap.

Consider two causal states with equal probability ($\pi_0 = \pi_1 = 0.5$) and signal states:

$$|s_0\rangle = \cos\theta |0\rangle + \sin\theta |1\rangle$$
$$|s_1\rangle = \sin\theta |0\rangle + \cos\theta |1\rangle$$

The overlap is: $\langle s_0 | s_1 \rangle = 2\sin\theta\cos\theta = \sin(2\theta)$

| $\theta$ | Overlap | $C_q$ | $C_\mu$ | Advantage |
|----------|---------|-------|---------|-----------|
| 0° | 0 | 1.00 | 1.00 | 0.00 |
| 15° | 0.50 | 0.81 | 1.00 | 0.19 |
| 30° | 0.87 | 0.40 | 1.00 | 0.60 |
| 45° | 1.00 | 0.00 | 1.00 | 1.00 |

At $\theta = 45°$, the signal states become identical: $|s_0\rangle = |s_1\rangle$. The quantum complexity drops to zero—the q-machine needs no memory at all!

At $\theta = 0°$, the states are orthogonal. No overlap, no advantage.

---

## Key Takeaway

> **Purity and entropy quantify the classical/quantum boundary.**
>
> - **Purity** $\gamma = \text{Tr}(\rho^2)$: Ranges from $1/d$ (max mixed) to $1$ (pure)
> - **Entropy** $S = -\text{Tr}(\rho \log \rho)$: Ranges from $0$ (pure) to $\log_2 d$ (max mixed)
>
> For diagonal matrices (classical states), von Neumann entropy equals Shannon entropy.
>
> Signal state overlap compresses eigenvalues → lower entropy → quantum advantage.

---

## Common Misconceptions

### "Pure states have no uncertainty"

True for the state itself, but measurement outcomes can still be uncertain! A superposition $(|0\rangle + |1\rangle)/\sqrt{2}$ has $S = 0$ (it's a definite quantum state) but measuring gives 0 or 1 with 50% each.

The entropy measures uncertainty about the *state*, not about measurement outcomes.

### "High purity means classical"

The opposite! Pure states ($\gamma = 1$) are the *most* quantum—they can have maximum coherence. Mixed states are partially classical (some coherence destroyed).

### "Entropy always increases"

Not for quantum systems! Unitary evolution preserves entropy. Entropy increases through measurement or decoherence—interactions with the environment that destroy coherence.

### "Von Neumann entropy is just Shannon entropy"

Only for diagonal matrices! For general density matrices with coherences, you must compute eigenvalues first. The off-diagonals affect the eigenvalues, which affects the entropy.

---

## Code Example

```python
import numpy as np

def von_neumann_entropy(rho):
    """Von Neumann entropy in bits."""
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    return -np.sum(eigenvalues * np.log2(eigenvalues))

def purity(rho):
    """Tr(ρ²)"""
    return np.real(np.trace(rho @ rho))

def linear_entropy(rho):
    """1 - Tr(ρ²), approximation to von Neumann for near-pure states."""
    return 1 - purity(rho)

# Vary overlap angle
print("Signal state overlap vs quantum complexity")
print("=" * 50)
print(f"{'θ (deg)':<10} {'Overlap':<10} {'C_q':<10} {'C_μ':<10} {'Advantage':<10}")
print("-" * 50)

for theta_deg in [0, 15, 30, 45]:
    theta = np.radians(theta_deg)

    # Signal states
    s0 = np.array([np.cos(theta), np.sin(theta)])
    s1 = np.array([np.sin(theta), np.cos(theta)])

    overlap = np.abs(np.dot(s0, s1))

    # Quantum density matrix
    rho = 0.5 * np.outer(s0, s0) + 0.5 * np.outer(s1, s1)

    C_q = von_neumann_entropy(rho)
    C_mu = 1.0  # H([0.5, 0.5]) = 1 bit

    print(f"{theta_deg:<10} {overlap:<10.2f} {C_q:<10.2f} {C_mu:<10.2f} {C_mu - C_q:<10.2f}")
```

---

## What's Next

We've now completed **Part I: Foundations**. You understand:
- Classical probability (diagonal matrices)
- Quantum amplitudes (complex, with phases)
- Density matrices (the unified representation)
- Entropy and purity (quantifying the classical/quantum boundary)

In **Part II**, we'll explore the core quantum phenomena:
- [Chapter 5: Measurement](05-measurement.md) — Forcing diagonality
- [Chapter 6: Composite Systems](06-composite-systems.md) — Tensor products
- [Chapter 7: Entanglement](07-entanglement.md) — Non-factorizable states
- [Chapter 8: Decoherence](08-decoherence.md) — The quantum→classical transition

---

*[← Previous: The Density Matrix](03-density-matrix.md) | [Back to Overview](00-overview.md) | [Next: Measurement →](05-measurement.md)*
