# Chapter 5: Measurement

*Forcing the matrix to become diagonal*

---

## The Measurement Problem

Measurement is where quantum mechanics gets weird—and where the density matrix picture really shines.

When we measure a quantum system, something dramatic happens: superpositions collapse. In the density matrix language, this means **off-diagonals get killed**.

---

## What Measurement Does

### Before Measurement

Consider a qubit in superposition:

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$

$$\rho = \begin{pmatrix} |\alpha|^2 & \alpha\beta^* \\ \alpha^*\beta & |\beta|^2 \end{pmatrix}$$

Off-diagonals present → coherence → can interfere.

### After Measurement in the $\{|0\rangle, |1\rangle\}$ basis

The density matrix becomes:

$$\rho' = \begin{pmatrix} |\alpha|^2 & 0 \\ 0 & |\beta|^2 \end{pmatrix}$$

Off-diagonals gone → classical mixture → no interference possible.

### The Outcome

With probability $|\alpha|^2$, we get outcome "0" and the state becomes $|0\rangle\langle 0|$.
With probability $|\beta|^2$, we get outcome "1" and the state becomes $|1\rangle\langle 1|$.

---

## Projection Operators

Mathematically, measurement in basis $\{|i\rangle\}$ is described by projection operators:

$$P_i = |i\rangle\langle i|$$

These satisfy:
- $P_i^2 = P_i$ (projecting twice does nothing new)
- $P_i P_j = 0$ for $i \neq j$ (orthogonal projections)
- $\sum_i P_i = I$ (complete set)

### Measurement Rule

**Probability** of outcome $i$:
$$p_i = \text{Tr}(P_i \rho) = \langle i|\rho|i\rangle = \rho_{ii}$$

**Post-measurement state** given outcome $i$:
$$\rho_i = \frac{P_i \rho P_i}{\text{Tr}(P_i \rho)} = |i\rangle\langle i|$$

### Average Effect (No Selection)

If we measure but don't look at the result:

$$\rho' = \sum_i P_i \rho P_i = \sum_i |i\rangle\langle i|\rho|i\rangle\langle i|$$

This extracts only the diagonal elements:

$$\rho' = \text{diag}(\rho)$$

---

## Worked Example: Measuring a Superposition

Start with $|\psi\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$:

$$\rho = \begin{pmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{pmatrix}$$

Measure in the computational basis:

$$\rho' = P_0 \rho P_0 + P_1 \rho P_1$$

$$= |0\rangle\langle 0|\rho|0\rangle\langle 0| + |1\rangle\langle 1|\rho|1\rangle\langle 1|$$

$$= 0.5 |0\rangle\langle 0| + 0.5 |1\rangle\langle 1|$$

$$= \begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}$$

**Before**: Pure state, $S = 0$ bits, can interfere.
**After**: Mixed state, $S = 1$ bit, classical.

Measurement created entropy! The coherence was destroyed.

---

## Measurement in Different Bases

Here's the crucial point: **the basis matters**.

The same state looks different depending on which measurement you perform.

### Example: Hadamard Basis

Define the Hadamard basis:
$$|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle), \quad |-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$$

Our state $|\psi\rangle = |+\rangle$ is an eigenstate of this basis!

Measuring in the Hadamard basis:
- Probability of $|+\rangle$: 100%
- Probability of $|-\rangle$: 0%

The state is unchanged—no entropy created.

### The Lesson

A state that looks like a superposition in one basis may be a definite state in another. Measurement in the "right" basis is non-destructive.

This is related to the quantum Zeno effect and is crucial for quantum error correction.

---

## General Measurements: POVMs

For more general measurements, we use Positive Operator-Valued Measures (POVMs).

A POVM is a set of positive operators $\{E_m\}$ satisfying $\sum_m E_m = I$.

**Probability** of outcome $m$:
$$p_m = \text{Tr}(E_m \rho)$$

POVMs can describe:
- Noisy measurements
- Incomplete measurements
- Measurements that don't fully collapse the state

For our purposes, projective measurements suffice, but POVMs are the full story.

---

## Why Measurement Kills Coherence

Here's the deep insight: measurement involves **interaction with a macroscopic apparatus**.

The apparatus has many degrees of freedom. When the quantum system interacts with it, information about "which outcome" gets copied to the environment.

Once the environment knows, the coherence is gone—not because of any mysterious "collapse," but because the off-diagonal terms now involve correlations with the environment that we don't track.

This is the **decoherence interpretation** of measurement, which we'll explore fully in Chapter 8.

---

## Connection to Computational Mechanics

In computational mechanics, we observe the output symbols of a process. Each observation is a measurement.

The key insight: **we measure outputs, not causal states**.

The causal states are internal—we never directly observe them. We infer them from the output sequence.

For q-machines:
- The system is in a superposition of signal states (in general)
- Outputting a symbol is a measurement in the symbol basis
- This collapses the symbol part but may leave residual coherence in the state index

The interplay between what's measured and what's preserved is subtle and beautiful.

---

## Key Takeaway

> **Measurement forces diagonality in the measurement basis.**
>
> - Off-diagonals are killed → coherence destroyed
> - Entropy increases (for superpositions measured in the "wrong" basis)
> - The post-measurement state is classical (in that basis)
>
> Measurement is not mysterious—it's the extraction of diagonal elements and destruction of off-diagonal elements.

---

## Common Misconceptions

### "Measurement causes collapse"

This is the textbook story, but it's more accurate to say measurement causes **decoherence with respect to the measurement basis**. The off-diagonals don't disappear magically—they become entangled with the apparatus.

### "Measurement always creates entropy"

Only if you measure in a basis where the state has coherence. If you measure in the state's eigenbasis, nothing changes.

### "We choose when to collapse the wavefunction"

We choose what to measure, but whether "collapse" happens is a matter of interpretation. The density matrix formalism avoids this debate—measurement just transforms $\rho$ according to precise rules.

### "Measurement reveals pre-existing values"

This is the classical intuition, and it's wrong. For a superposition, the outcome didn't exist before measurement. Measurement creates the outcome from the probability distribution encoded in $\rho$.

---

## Code Example

```python
import numpy as np

def measure_in_basis(rho, basis_states):
    """
    Apply projective measurement in given basis.
    Returns (post_measurement_rho, probabilities).
    """
    d = rho.shape[0]
    probs = []
    rho_post = np.zeros_like(rho)

    for state in basis_states:
        state = np.array(state, dtype=complex)
        state = state / np.linalg.norm(state)
        P = np.outer(state, np.conj(state))  # Projector
        prob = np.real(np.trace(P @ rho))
        probs.append(prob)
        rho_post += P @ rho @ P  # Contribution to mixture

    return rho_post, np.array(probs)

def von_neumann_entropy(rho):
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    return -np.sum(eigenvalues * np.log2(eigenvalues))

# Superposition state
psi = np.array([1, 1], dtype=complex) / np.sqrt(2)
rho = np.outer(psi, np.conj(psi))

print("Before measurement:")
print(f"ρ =\n{rho}")
print(f"Entropy: {von_neumann_entropy(rho):.3f} bits")

# Measure in computational basis
basis_01 = [[1, 0], [0, 1]]
rho_after, probs = measure_in_basis(rho, basis_01)

print("\nAfter measurement in {|0⟩, |1⟩} basis:")
print(f"ρ =\n{rho_after}")
print(f"Probabilities: {probs}")
print(f"Entropy: {von_neumann_entropy(rho_after):.3f} bits")

# Measure in Hadamard basis
basis_pm = [[1, 1], [1, -1]]  # |+⟩, |−⟩
rho_after_h, probs_h = measure_in_basis(rho, basis_pm)

print("\nAfter measurement in {|+⟩, |−⟩} basis:")
print(f"ρ =\n{np.round(rho_after_h, 3)}")
print(f"Probabilities: {probs_h}")
print(f"Entropy: {von_neumann_entropy(rho_after_h):.3f} bits")
```

---

## What's Next

In [Chapter 6: Composite Systems](06-composite-systems.md), we'll see how to describe multiple quantum systems together using tensor products—the key to understanding entanglement.

---

*[← Previous: Entropy and Purity](04-entropy-purity.md) | [Back to Overview](00-overview.md) | [Next: Composite Systems →](06-composite-systems.md)*
